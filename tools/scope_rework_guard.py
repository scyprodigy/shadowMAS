#!/usr/bin/env python3
"""Task-scoped rework guard: match a task's scope against recorded rejections,
decisions, deferrals, and lessons before work begins.

Read-only. ADVISORY. This is the task-scoped sibling of
tools/build_rework_guard.py: instead of compiling the global one-screen
DO-NOT-REDO surface, it answers "which already-decided, rejected, deferred,
or lesson-recorded items are relevant to THIS task?" and prints them with
their reopen/unlock conditions. It matches against the owning source files
directly (sources always win over compiled views), so compiled-surface
staleness cannot mislead it.

Matching is deterministic keyword/path overlap only — no embeddings, no
model calls. Path tiers use only each record's declared scope-bearing text,
never incidental paths elsewhere in the source. A no-hit result means
"no hit within bounded coverage", never
"nothing relevant exists" (the coverage manifest is printed with every run).
Weak matches are quarantined under a manual-confirmation heading and do not
change the exit code.

Usage:
  python3 tools/scope_rework_guard.py --goal "replace parser" --path src/parser.py
  python3 tools/scope_rework_guard.py --task-packet <task.yaml>   # or '-' for stdin
  python3 tools/scope_rework_guard.py --goal "..." --format json

Exit: 0 = bounded scan complete, no exact/path-scope/strong findings (weak may
exist); 1 = exact, path-scope, or strong findings; 2 = usage/setup error (no
query subjects, missing sources, unreadable or malformed YAML).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

from _shadowmas_readonly import UniqueKeyLoader, resolve_repo_reference

REPO = Path(__file__).resolve().parents[1]

RATIONALE_DIR = Path("07_working/drafts/rationale")
DEFERRED_FILE = RATIONALE_DIR / "deferred_state_inventory.md"
LESSONS_FILE = Path("07_working/drafts/SHADOWMAS-LESSONS-QUEUE.v0.yaml")

MD_HEADER_RE = re.compile(r"^#\s*(?P<name>[^|]+?)\s*\|\s*(?P<purpose>.+?)\s*$")
SECTION_RE = re.compile(
    r"^##+ (?!Purpose|Discipline|Reconsideration|Out of scope|Other deferred)(?P<title>.+)$"
)
TRIGGER_RE = re.compile(r"^- unlock trigger:\s*(?P<trigger>.*)$")
HEADING_RE = re.compile(r"^#+\s+(?P<title>.+?)\s*$")
SETEXT_UNDERLINE_RE = re.compile(r"^\s*(?:={3,}|-{3,})\s*$")
THEMATIC_BREAK_RE = re.compile(
    r"^(?P<indent>[ ]*)(?P<marker>[-*_])"
    r"(?:[ \t]*(?P=marker)){2,}[ \t]*$"
)
HTML_BLOCK_INTERRUPT_SEQUENCES = (
    (re.compile(r"^<(?i:script|pre|style|textarea)(?=[\s>]|$)"),
     re.compile(r"</(?i:script|pre|style|textarea)>")),
    (re.compile(r"^<!--"), re.compile(r"-->")),
    (re.compile(r"^<\?"), re.compile(r"\?>")),
    (re.compile(r"^<![A-Z]"), re.compile(r">")),
    (re.compile(r"^<!\[CDATA\["), re.compile(r"\]\]>")),
)
LIST_ITEM_RE = re.compile(
    r"^(?P<indent>\s*)(?:(?:[-+*])|(?:\d+[.)]))\s+(?P<text>.+?)\s*$")

TIER_EXACT_PATH = "EXACT_PATH"
TIER_PATH_SCOPE = "PATH_SCOPE"
TIER_STRONG = "STRONG_KEYWORD"
TIER_WEAK = "WEAK"

KIND_ORDER = {"rejection": 0, "decision": 1, "deferral": 2, "lesson": 3}

STOPLIST = {
    "the", "and", "for", "with", "that", "this", "not", "are", "was", "were",
    "must", "should", "may", "into", "from", "only", "all", "one", "per",
    "via", "will", "can", "has", "have", "been", "its", "but", "when",
    "where", "how", "why", "what", "use", "used", "using", "does", "els",
    "any", "out", "our", "you", "your", "before", "after", "record",
}


def tokenize(text: str) -> set[str]:
    tokens = re.split(r"[^a-z0-9]+", text.lower())
    return {t for t in tokens if len(t) >= 3 and t not in STOPLIST}


def load_yaml_file(path: Path) -> tuple[object | None, str | None]:
    try:
        text = path.read_text(encoding="utf-8")
        return yaml.load(text, Loader=UniqueKeyLoader), None
    except (OSError, UnicodeError) as exc:
        return None, f"unable to read YAML file {path}: {exc}"
    except yaml.YAMLError as exc:
        detail = " ".join(str(exc).split())
        return None, f"unable to parse YAML file {path}: {detail}"


def flatten_strings(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        out: list[str] = []
        for item in value:
            out.extend(flatten_strings(item))
        return out
    if isinstance(value, dict):
        out = []
        for item in value.values():
            out.extend(flatten_strings(item))
        return out
    return []


def markdown_list_section(text: str, heading_suffix: str) -> list[str]:
    """Return list items under one unambiguous Markdown heading.

    Exact matching plus a ``v-*`` prefix admits ``v-future Reopen Conditions``
    without treating headings such as ``Rejected reopen conditions`` as live.
    Markdown headings inside fenced code are ignored. Multiple live sections
    are refused instead of silently selecting one.
    """
    wanted = heading_suffix.casefold()
    sections: list[list[str]] = []
    active: list[str] | None = None
    fence: str | None = None
    lines = text.splitlines()
    index = 0
    previous_blank = True
    item_content_indent: int | None = None
    in_indented_code = False
    item_paragraph_open = False
    in_block_quote = False
    html_block_end: re.Pattern[str] | None = None
    while index < len(lines):
        raw = lines[index]
        stripped = raw.strip()
        if html_block_end is not None:
            if html_block_end.search(stripped):
                html_block_end = None
            previous_blank = True
            item_paragraph_open = False
            index += 1
            continue
        marker = stripped[:3]
        if marker in {"```", "~~~"}:
            if fence is None:
                fence = marker
            elif marker == fence:
                fence = None
            previous_blank = True
            item_paragraph_open = False
            in_block_quote = False
            index += 1
            continue
        if fence is not None:
            index += 1
            continue
        if not stripped:
            previous_blank = True
            item_paragraph_open = False
            in_block_quote = False
            index += 1
            continue
        heading = HEADING_RE.match(raw)
        title_text: str | None = None
        if heading:
            title_text = heading.group("title")
        elif (stripped and not LIST_ITEM_RE.match(raw)
              and not (active and item_paragraph_open)
              and not in_block_quote
              and len(raw) - len(raw.lstrip(" ")) <= 3
              and index + 1 < len(lines)
              and SETEXT_UNDERLINE_RE.fullmatch(lines[index + 1])):
            title_text = stripped
            index += 1  # consume the underline with its heading
        if title_text is not None:
            title = title_text.strip().casefold()
            title = title.strip("*_").strip()
            title = title.removesuffix(":").strip()
            title = title.strip("*_").strip()
            if active is not None:
                sections.append(active)
                active = None
            if (title == wanted
                    or re.fullmatch(r"v-[a-z0-9_.-]+\s+" + re.escape(wanted),
                                    title)):
                active = []
            previous_blank = False
            item_content_indent = None
            in_indented_code = False
            item_paragraph_open = False
            in_block_quote = False
            index += 1
            continue
        if active is None:
            previous_blank = False
            item_paragraph_open = False
            in_block_quote = False
            index += 1
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        code_indent = ((item_content_indent + 4)
                       if item_content_indent is not None else None)
        if active and in_indented_code and code_indent is not None:
            if indent >= code_indent:
                previous_blank = False
                index += 1
                continue
            in_indented_code = False
        if (active and previous_blank and code_indent is not None
                and indent >= code_indent):
            in_indented_code = True
            previous_blank = False
            item_paragraph_open = False
            in_block_quote = False
            index += 1
            continue
        thematic_break = THEMATIC_BREAK_RE.fullmatch(raw)
        thematic_indent_limit = ((item_content_indent + 3)
                                 if item_content_indent is not None else 3)
        if (thematic_break is not None
                and len(thematic_break.group("indent"))
                <= thematic_indent_limit):
            previous_blank = False
            in_indented_code = False
            item_paragraph_open = False
            in_block_quote = False
            index += 1
            continue
        item_match = LIST_ITEM_RE.match(raw)
        if item_match:
            item = item_match.group("text").strip()
            if item_match.group("indent"):
                if not active:
                    raise ValueError("nested list item has no parent")
                active[-1] += f" — nested: {item}"
            else:
                active.append(item)
            item_content_indent = item_match.start("text")
            in_indented_code = False
            item_paragraph_open = True
            in_block_quote = False
        elif active:
            interrupt_indent_limit = ((item_content_indent + 3)
                                     if item_content_indent is not None else 3)
            html_end = next(
                (end for start, end in HTML_BLOCK_INTERRUPT_SEQUENCES
                 if start.match(stripped)),
                None,
            )
            if html_end is not None and indent <= interrupt_indent_limit:
                if not html_end.search(stripped):
                    html_block_end = html_end
                previous_blank = True
                item_paragraph_open = False
                in_block_quote = False
                index += 1
                continue
            if stripped.startswith(">") and indent <= interrupt_indent_limit:
                previous_blank = False
                item_paragraph_open = False
                in_block_quote = True
                index += 1
                continue
            if in_block_quote:
                previous_blank = False
                item_paragraph_open = False
                index += 1
                continue
            if raw[:1].isspace() or item_paragraph_open:
                active[-1] += " " + stripped
                item_paragraph_open = True
        previous_blank = False
        index += 1
    if fence is not None:
        raise ValueError("unclosed Markdown fence")
    if active is not None:
        sections.append(active)
    if len(sections) > 1:
        raise ValueError(f"multiple {heading_suffix!r} sections")
    return sections[0] if sections else []


def declared_path_match(path_scope: str, query_path: str
                        ) -> tuple[str | None, str | None]:
    """Match a query path only against declared scope-bearing record text.

    A full file/path reference is EXACT_PATH. A nested directory ancestor is
    PATH_SCOPE. Top-level parents such as ``tools/`` are deliberately excluded:
    they are too broad to establish task relevance by themselves.
    """
    normalized_paths = normalize_paths([query_path])
    normalized = normalized_paths[0] if normalized_paths else ""
    if not normalized:
        return None, None

    boundary = r"(?<![A-Za-z0-9_./-]){}(?=$|[^A-Za-z0-9_./-])"
    for candidate in (normalized, normalized + "/"):
        if re.search(boundary.format(re.escape(candidate)), path_scope):
            return TIER_EXACT_PATH, candidate

    parts = Path(normalized).parts
    for end in range(len(parts) - 1, 1, -1):
        ancestor = "/".join(parts[:end]) + "/"
        if re.search(boundary.format(re.escape(ancestor)), path_scope):
            return TIER_PATH_SCOPE, ancestor
    return None, None


def gather_records(repo: Path) -> tuple[list[dict], list[str]]:
    """Collect rejection, decision, deferral, and lesson records from their
    owning source files. Returns (records, errors); errors are fatal."""

    records: list[dict] = []
    errors: list[str] = []

    rationale_dir = repo / RATIONALE_DIR
    deferred_file = repo / DEFERRED_FILE
    lessons_file = repo / LESSONS_FILE
    for required in (rationale_dir, deferred_file, lessons_file):
        if not required.exists():
            errors.append(f"missing source: {required}")
    if errors:
        return records, errors

    for path in sorted(rationale_dir.glob("rejection_*.v0.yaml")):
        if ".PROPOSAL." in path.name:
            continue
        data, error = load_yaml_file(path)
        if error:
            errors.append(error)
            continue
        if not isinstance(data, dict):
            errors.append(f"rejection_record is not a mapping: {path}")
            continue
        scope_text = " ".join(flatten_strings(data.get("rejection_scope")))
        reasons = flatten_strings(data.get("rejection_reasons"))
        records.append({
            "kind": "rejection",
            "record_id": path.stem,
            "summary": str(data.get("purpose", "(no purpose field)")),
            "primary": " ".join(
                [str(data.get("purpose", "")), str(data.get("rejected_claim", ""))]
            ),
            "secondary": " ".join(reasons + [scope_text]),
            "path_scope": scope_text,
            "conditions": flatten_strings(data.get("reopen_conditions")),
            "condition_label": "reopen",
            "source_path": str(path.relative_to(repo)),
            "raw": path.read_text(encoding="utf-8"),
        })

    for path in sorted(rationale_dir.glob("DECISION-*.md")):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"unable to read decision record {path}: {exc}")
            continue
        first = text.splitlines()[0] if text.splitlines() else ""
        match = MD_HEADER_RE.match(first)
        purpose = match.group("purpose") if match else "(unparseable header)"
        try:
            conditions = markdown_list_section(text, "reopen conditions")
        except ValueError as exc:
            errors.append(f"ambiguous decision record {path}: {exc}")
            continue
        records.append({
            "kind": "decision",
            "record_id": path.stem,
            "summary": purpose,
            "primary": purpose,
            "secondary": "",
            "path_scope": purpose,
            "conditions": conditions,
            "condition_label": "reopen",
            "source_path": str(path.relative_to(repo)),
            "raw": text,
        })

    try:
        deferred_lines = (repo / DEFERRED_FILE).read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        errors.append(f"unable to read deferred inventory: {exc}")
        deferred_lines = []
    title = None
    for i, line in enumerate(deferred_lines):
        section = SECTION_RE.match(line)
        if section:
            title = section.group("title").strip()
            continue
        trigger = TRIGGER_RE.match(line.strip()) if title else None
        if trigger and title:
            parts = [trigger.group("trigger").strip()]
            for cont in deferred_lines[i + 1:]:
                stripped = cont.strip()
                if not stripped or stripped.startswith("- ") or stripped.startswith("#"):
                    break
                parts.append(stripped)
            records.append({
                "kind": "deferral",
                "record_id": title,
                "summary": title,
                "primary": title,
                "secondary": " ".join(parts),
                "path_scope": title,
                "conditions": [" ".join(parts)],
                "condition_label": "unlock",
                "source_path": str(DEFERRED_FILE),
                "raw": title + " " + " ".join(parts),
            })
            title = None

    data, error = load_yaml_file(repo / LESSONS_FILE)
    if error:
        errors.append(error)
    elif isinstance(data, dict):
        for entry in data.get("entries") or []:
            if not isinstance(entry, dict):
                continue
            note = ""
            decision = entry.get("human_decision")
            if isinstance(decision, dict):
                note = str(decision.get("note", ""))
            records.append({
                "kind": "lesson",
                "record_id": str(entry.get("lesson_id", "?")),
                "summary": str(entry.get("short_summary", "(no summary)")),
                "primary": str(entry.get("short_summary", "")),
                "secondary": note,
                "path_scope": str(entry.get("short_summary", "")),
                "conditions": [],
                "condition_label": "reopen",
                "source_path": str(LESSONS_FILE),
                "raw": str(entry.get("short_summary", "")) + " " + note,
            })

    return records, errors


def normalize_paths(paths: list[str]) -> list[str]:
    normalized = []
    for raw in paths:
        cleaned = raw.strip()
        while cleaned.startswith("./"):
            cleaned = cleaned[2:]
        cleaned = str(Path(cleaned)) if cleaned else ""
        if cleaned not in {"/", "//"}:
            cleaned = cleaned.rstrip("/")
        if cleaned:
            normalized.append(cleaned)
    return normalized


def match_records(
    records: list[dict], query_tokens: set[str], paths: list[str]
) -> tuple[list[dict], list[dict]]:
    """Return findings (exact, path-scope, or strong) and quarantined weak."""

    findings: list[dict] = []
    weak: list[dict] = []
    for record in records:
        primary_tokens = tokenize(record["primary"])
        secondary_tokens = tokenize(record["secondary"])
        primary_overlap = sorted(query_tokens & primary_tokens)
        secondary_overlap = sorted(query_tokens & secondary_tokens)

        path_hit = None
        path_tier = None
        for path in paths:
            path_tier, path_hit = declared_path_match(
                record.get("path_scope", ""), path)
            if path_tier:
                break

        if path_tier:
            tier = path_tier
        elif len(primary_overlap) >= 2:
            tier = TIER_STRONG
        elif len(primary_overlap) == 1 or len(secondary_overlap) >= 2:
            tier = TIER_WEAK
        else:
            continue

        entry = dict(record)
        entry.pop("raw", None)
        entry.pop("path_scope", None)
        entry["tier"] = tier
        entry["path_hit"] = path_hit
        entry["primary_overlap"] = primary_overlap
        entry["secondary_overlap"] = secondary_overlap
        (findings if tier != TIER_WEAK else weak).append(entry)

    def sort_key(entry: dict):
        tier_rank = {
            TIER_EXACT_PATH: 0,
            TIER_PATH_SCOPE: 1,
            TIER_STRONG: 2,
            TIER_WEAK: 3,
        }[entry["tier"]]
        return (
            tier_rank,
            -len(entry["primary_overlap"]),
            -len(entry["secondary_overlap"]),
            KIND_ORDER.get(entry["kind"], 9),
            entry["record_id"],
        )

    findings.sort(key=sort_key)
    weak.sort(key=sort_key)
    return findings, weak


def render_entry(entry: dict) -> list[str]:
    lines = [f"- [{entry['tier']}] {entry['kind']} {entry['record_id']}: {entry['summary']}"]
    if entry["path_hit"]:
        lines.append(f"    matched path: {entry['path_hit']}")
    if entry["primary_overlap"]:
        lines.append(f"    matched terms: {', '.join(entry['primary_overlap'])}")
    for condition in entry["conditions"]:
        lines.append(f"    {entry['condition_label']}: {condition}")
    lines.append(f"    source: {entry['source_path']}")
    return lines


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Match a task scope against recorded rejections, decisions, "
                    "deferrals, and lessons (read-only, advisory)."
    )
    parser.add_argument("--repo", default=str(REPO))
    parser.add_argument("--goal", default="")
    parser.add_argument("--path", action="append", default=[],
                        help="task-relevant repository-relative path (repeatable)")
    parser.add_argument("--task-packet", default=None,
                        help="task packet YAML file, or '-' for stdin")
    parser.add_argument("--max-sources", type=int, default=8,
                        help="cap on rendered owning-source findings; 8 is a "
                             "hard ceiling (higher values are clamped), lower "
                             "values narrow further")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)

    repo = Path(args.repo).resolve()
    if not repo.is_dir():
        print(f"ERROR: repo is not a directory: {repo}", file=sys.stderr)
        return 2

    query_parts = [args.goal]
    if args.task_packet:
        if args.task_packet == "-":
            try:
                data = yaml.load(sys.stdin.read(), Loader=UniqueKeyLoader)
            except yaml.YAMLError as exc:
                print(f"ERROR: unable to parse task packet from stdin: {exc}",
                      file=sys.stderr)
                return 2
        else:
            data, error = load_yaml_file(Path(args.task_packet))
            if error:
                print(f"ERROR: {error}", file=sys.stderr)
                return 2
        if not isinstance(data, dict):
            print("ERROR: task packet is not a mapping", file=sys.stderr)
            return 2
        for field in ("goal", "scope", "out_of_scope", "truth_touchpoints"):
            query_parts.extend(flatten_strings(data.get(field)))

    paths = normalize_paths(args.path)
    for path in paths:
        if path == ".":
            print("ERROR: invalid --path '.': repository root is not a "
                  "bounded task path", file=sys.stderr)
            return 2
        _target, error = resolve_repo_reference(repo, path)
        if error:
            print(f"ERROR: invalid --path {path!r}: {error}", file=sys.stderr)
            return 2
    query_tokens = tokenize(" ".join(query_parts))
    if not query_tokens and not paths:
        print("ERROR: no query subjects; provide --goal, --path, or --task-packet",
              file=sys.stderr)
        return 2

    records, errors = gather_records(repo)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 2

    findings, weak = match_records(records, query_tokens, paths)
    effective_cap = min(max(1, args.max_sources), 8)  # 8 is non-raiseable
    suppressed = max(0, len(findings) - effective_cap)
    findings_shown = findings[:effective_cap]
    suppressed_weak = max(0, len(weak) - effective_cap)
    weak_shown = weak[:effective_cap]

    coverage = {
        "scanned": {
            kind: sum(1 for r in records if r["kind"] == kind)
            for kind in ("rejection", "decision", "deferral", "lesson")
        },
        "query_tokens": sorted(query_tokens),
        "paths": paths,
    }

    if args.format == "json":
        print(json.dumps({
            "findings": findings_shown,
            "suppressed_findings": suppressed,
            "weak_manual_confirmation_required": weak_shown,
            "suppressed_weak": suppressed_weak,
            "coverage": coverage,
            "no_hit_statement": None if (findings or weak)
            else "no hit within bounded coverage",
        }, indent=2))
        return 1 if findings else 0

    print("SCOPE REWORK GUARD (advisory, read-only; sources win over compiled views)")
    print(f"query tokens: {', '.join(sorted(query_tokens)) or '(none)'}")
    print(f"paths: {', '.join(paths) or '(none)'}")
    print()
    if findings:
        print("FINDINGS (exact/path-scope/strong — read the owning source before proposing):")
        for entry in findings_shown:
            print("\n".join(render_entry(entry)))
        if suppressed:
            print(f"(+{suppressed} more exact/path-scope/strong findings "
                  "suppressed by the "
                  f"{effective_cap}-source cap; narrow the task scope)")
    else:
        print("no exact, path-scope, or strong hit within bounded coverage")
    if weak:
        print()
        print("WEAK — MANUAL CONFIRMATION REQUIRED (not scoped findings):")
        for entry in weak_shown:
            print("\n".join(render_entry(entry)))
        if suppressed_weak:
            print(f"(+{suppressed_weak} more weak matches suppressed by the "
                  f"{effective_cap}-source cap)")
    if not findings and not weak:
        print("no hit within bounded coverage")
    print()
    scanned = coverage["scanned"]
    print("COVERAGE: scanned "
          f"rejections={scanned['rejection']} decisions={scanned['decision']} "
          f"deferrals={scanned['deferral']} lessons={scanned['lesson']}; "
          "this bounds the claim above — records outside these sources were not read")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
