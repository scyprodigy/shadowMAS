#!/usr/bin/env python3
"""Compose a task-scoped pre-sign-off review brief; optionally emit a receipt.

Read-only against the repository. ADVISORY. Compiles the one-screen brief a
human consults before signing off on AI-assisted work for ONE bounded task:
evidence and counter-evidence first (scoped rework-guard findings,
memory-validity findings, prior outcomes), then the decision frame, coverage
manifest, risk and reversibility, a typed check list (max seven items), and a
human-judgment section. The compiler recommendation is computed up front but
WITHHELD until the human records a judgment; preview and JSON output never
reveal it, and disconfirming evidence renders ahead of framing.

Finding classes are split and centrally enforced:
- BLOCKING findings stop both recommendation and receipt: unknown or
  over-budget changed lines, binary or unreadable changes, incomplete
  context coverage (source cap reached or a requested source unreadable),
  missing rollback path, irreversible change on a too-low risk tier, and
  check overflow. No receipt exists while any blocking finding is open.
- ADVISORY findings (rework-guard hits, stale memory citations) stay visible
  to the judgment and set the recommendation, but do not force narrowing.
Both classes drive exit code 1; a human decision never clears either.

Bounded intake (task side): reads only ancestor-chain AGENTS.md/CLAUDE.md
above the --path targets, files named by --source, and repository-relative
markdown links inside those files (one hop), collectively capped at
MAX_CONTEXT_SOURCES; the cap check runs before any excess read. History is
capped at MAX_HISTORY commit subjects. Context content is declared in coverage
but excluded from relevance matching: generic repository instructions must not
overwhelm the operator's task goal and acceptance criteria. Corpus side reuses
the rework-guard record set and the memory-validity roots existing advisory
tools already scan; coverage output declares both sides.

Changed-line accounting: git-derived counts diff against HEAD and include
untracked files via --untracked-files=all; binary or unreadable material is
a BLOCKING finding, never silently zero. Declared --changed-loc is labeled
declared_only and must be zero or positive; a negative declaration is a
usage error refused before composition, never a way past the budget check.

One-screen contract: every section carries its own word budget (budgets sum
to <= 600 words) and always keeps its heading; overflow preserves an ordered
prefix of atomic finding groups with an explicit omission notice, so a reopen
condition cannot outlive its finding and sections 1-7 are always present.
Blocking and advisory findings render inside section 1, so
counter-evidence precedes the decision frame; the compiler recommendation
is always the last rendered section. Full content is via --format json.

Receipt: with --emit-receipt on an interactive terminal, after the human
selects finding ids (validated against actual findings) and a judgment, the
recommendation is revealed and ONE terminal review_packet (existing v0
schema) is validated in a temporary file, checked for filename collision,
and only then moved into <workspace>/reviews/ (an existing receipt is never
overwritten). Refusing non-interactive execution does NOT authenticate a
human: a pseudo-terminal can be scripted. The receipt records
interaction_channel:tty, authentication:none, and review_mode:automated_check
(for the compiled checks that demonstrably ran) and never claims
direct_human_evaluation, signatures, identity, attention, or competence.
JSON mode never emits a receipt. Human decisions do not change the exit
code.

Metrics (after workspace validation, workspace-local artifacts only): each
record carries
record_kind (preview | signoff | signoff_attempt | skip), run_id,
signoff_id (pass --signoff-id to correlate a preview with its later receipt;
the declared value is converted with a workspace-local owner-private salt and
is not stored), compose_ms (frozen BEFORE any interaction), triage_ms (brief display
to judgment), judgment, observable_action (human-declared at the terminal,
or derived from the judgment; a behavioral proxy, not a causality claim),
observable_action_source, interaction_channel, authentication (always none),
eligible_signoff, brief_displayed, brief_consulted, exit_code. These provenance
additions define review_brief_run.v1; legacy v0 records are never upgraded by
inference. brief_consulted is
retained as a compatibility alias for display and is not a human-attention
claim. record_kind is signoff ONLY
when a human judgment was recorded; a receipt run refused before the brief
reached the terminal, or cancelled without a judgment, records as
signoff_attempt, and brief_consulted states whether the brief was actually
displayed — a refusal never counts as consultation. Kill-condition
denominators use record_kind signoff and skip; previews and sign-off
attempts are neither denominator nor numerator. --record-skip logs an
eligible sign-off that did not consult the brief.

Exit: 0 = brief composed, no findings; 1 = findings (blocking or advisory);
2 = usage/setup error (bad workspace, missing sources, malformed YAML,
receipt without a terminal, receipt while blocking findings are open,
validator failure, receipt collision).
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import hmac
import json
import os
import re
import secrets
import stat
import subprocess
import sys
import time
import uuid
from pathlib import Path

import yaml

import check_memory_validity as memory_validity
import scope_rework_guard as rework_guard
from _shadowmas_readonly import resolve_repo_reference

REPO = Path(__file__).resolve().parents[1]
VALIDATOR = REPO / "05_scripts" / "validate" / "shadowmas_validate.py"

RISK_TIERS = ["r0_trivial", "r1_routine", "r2_guarded", "r3_sensitive",
              "r4_human_only"]
ELIGIBLE_RISKS = {"r2_guarded", "r3_sensitive", "r4_human_only"}
SUPERVISION_MODES = ["human_live_pair", "human_available_delegate",
                     "human_away_autonomous"]
LOC_BUDGET = 400
MAX_CHECKS = 7
MAX_CONTEXT_SOURCES = 8
MAX_HISTORY = 10
LINE_WORD_LIMIT = 18
SECTION_WORD_BUDGETS = {"header": 25, "evidence": 135, "frame": 100,
                        "coverage": 80, "risk": 75, "checks": 95,
                        "judgment": 55, "recommendation": 35}
OBSERVABLE_ACTIONS = ["none", "added_check", "revision", "rejection", "reopen"]
JUDGMENT_STATUS = {"approve": "approved", "reject": "rejected",
                   "revise": "needs_revision"}
JUDGMENT_ACTION = {"approve": "none", "reject": "rejection",
                   "revise": "revision"}
MEMORY_ROOTS = ["07_working", "examples/packets", "03_memory/shared_memory"]
MD_LINK_RE = re.compile(r"\]\(([^)#\s]+)\)")
SIGNOFF_ID_RE = re.compile(r"^[A-Za-z0-9_.:-]{1,64}$")
FINDING_TIER_RE = re.compile(r"DISCONFIRM \[([A-Z_]+)\]")
FINDING_TIER_ORDER = {
    "EXACT_PATH": 0,
    "PATH_SCOPE": 1,
    "STRONG_KEYWORD": 2,
    "WEAK": 3,
}


def utc_now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:40] or "task"


def opaque_signoff_id(declared: str, fallback: str, salt: bytes) -> str:
    """Return a workspace-scoped opaque correlation id.

    The HMAC prevents recovery from a run-record-only export. It is stable only
    within a workspace and is not anonymization against access to the salt.
    """
    if not declared:
        return fallback
    if len(salt) != 32:
        raise ValueError("workspace sign-off salt must contain 32 bytes")
    digest = hmac.new(
        salt,
        b"shadowmas:review-brief-signoff:" + declared.encode("utf-8"),
        hashlib.sha256,
    ).digest()[:16]
    return str(uuid.UUID(bytes=digest, version=5))


def read_signoff_salt(path: Path) -> bytes:
    """Read one regular owner-private salt without following a symlink."""
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        fd = os.open(path, flags)
    except OSError as exc:
        raise ValueError(f"unable to read workspace sign-off salt: {exc}") \
            from exc
    try:
        metadata = os.fstat(fd)
        if not stat.S_ISREG(metadata.st_mode):
            raise ValueError("workspace sign-off salt is not a regular file")
        if stat.S_IMODE(metadata.st_mode) & 0o077:
            raise ValueError(
                "workspace sign-off salt must not be group/world accessible")
        with os.fdopen(fd, "rb", closefd=False) as handle:
            salt = handle.read(33)
    finally:
        os.close(fd)
    if len(salt) != 32:
        raise ValueError("workspace sign-off salt must contain exactly 32 bytes")
    return salt


def load_or_create_signoff_salt(workspace: Path) -> bytes:
    """Load or atomically create the workspace-local sign-off salt."""
    path = workspace / ".signoff_salt"
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        fd = os.open(path, flags, 0o600)
    except FileExistsError:
        return read_signoff_salt(path)
    except OSError as exc:
        raise ValueError(f"unable to create workspace sign-off salt: {exc}") \
            from exc
    salt = secrets.token_bytes(32)
    try:
        with os.fdopen(fd, "wb", closefd=False) as handle:
            handle.write(salt)
            handle.flush()
            os.fsync(handle.fileno())
    finally:
        os.close(fd)
    return salt


def prepare_record_signoff_id(args, workspace: Path) -> None:
    """Resolve a declared id before any receipt or run record is written."""
    if not args.signoff_id:
        args.record_signoff_id = ""
        return
    salt = load_or_create_signoff_salt(workspace)
    args.record_signoff_id = opaque_signoff_id(args.signoff_id, "", salt)


def trim_line(text: str) -> str:
    indent = text[:len(text) - len(text.lstrip())]
    words = text.lstrip().split()
    if len(words) <= LINE_WORD_LIMIT:
        return text
    return indent + " ".join(words[:LINE_WORD_LIMIT]) + " …[trimmed]"


def line_groups(lines: list[str]) -> list[list[str]]:
    return [[line] for line in lines]


def fit_section(groups: list[list[str]], budget: int) -> list[str]:
    """Fit an ordered prefix of atomic groups within a section budget."""
    out: list[str] = []
    used = 0
    omitted_groups: list[list[str]] = []
    for i, raw_group in enumerate(groups):
        group = [trim_line(raw) for raw in raw_group]
        words = sum(len(line.split()) for line in group)
        if i == 0 or used + words <= budget - 8:
            out.extend(group)
            used += words
        else:
            omitted_groups = groups[i:]
            break
    if omitted_groups:
        tiers = [
            match.group(1)
            for group in omitted_groups
            for line in group
            if (match := FINDING_TIER_RE.search(line))
        ]
        tier_note = ""
        if tiers:
            highest = min(tiers, key=lambda tier: FINDING_TIER_ORDER.get(
                tier, 99))
            tier_note = f"; highest-tier={highest}"
        out.append(f"   (+{len(omitted_groups)} groups omitted{tier_note}; "
                   "full: --format json)")
    return out


def git_lines(repo: Path, args: list[str]) -> list[str] | None:
    try:
        result = subprocess.run(["git", "-C", str(repo), *args],
                                capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    return result.stdout.splitlines()


def changed_loc_from_git(repo: Path, paths: list[str]
                         ) -> tuple[int | None, list[str]]:
    """Count changed lines vs HEAD including untracked files (listed
    individually via --untracked-files=all). Binary or unreadable material
    returns a BLOCKING finding, never a silent zero."""
    blocking: list[str] = []
    numstat = git_lines(repo, ["diff", "--numstat", "HEAD", "--", *paths])
    if numstat is None:
        return None, blocking
    total = 0
    for line in numstat:
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        if parts[0] == "-" or parts[1] == "-":
            blocking.append(f"binary change blocks the unit: {parts[2]} "
                            "(manual chunking required)")
            continue
        total += int(parts[0]) + int(parts[1])
    status = git_lines(repo, ["status", "--porcelain",
                              "--untracked-files=all", "--", *paths]) or []
    for line in status:
        if line.startswith("??"):
            untracked = line[3:].strip()
            target = repo / untracked
            if not target.is_file():
                blocking.append(f"unreadable untracked change blocks the "
                                f"unit: {untracked}")
                continue
            try:
                total += sum(1 for _ in target.open("r", encoding="utf-8"))
            except (OSError, UnicodeError):
                blocking.append(f"unreadable untracked change blocks the "
                                f"unit: {untracked}")
    return total, blocking


def collect_context(repo: Path, paths: list[str], sources: list[str]
                    ) -> tuple[list[str], list[str]]:
    """Return bounded ``(read_files, blocking_findings)`` task context.

    Context is coverage evidence, not relevance-query material. The cap check
    runs before any excess read.
    """
    candidates: list[str] = []
    seen: set[str] = set()

    def add(rel: str):
        if rel not in seen:
            seen.add(rel)
            candidates.append(rel)

    for path in paths:
        parent = Path(path).parent
        chain = [parent] + list(parent.parents)
        for directory in reversed(chain):
            for name in ("AGENTS.md", "CLAUDE.md"):
                rel = str(directory / name) if str(directory) != "." else name
                if (repo / rel).is_file():
                    add(rel)
    for source in sources:
        add(source)

    blocking: list[str] = []
    read_files: list[str] = []
    hop_candidates: list[str] = []

    def read_bounded(rel_list: list[str], collect_links: bool) -> bool:
        for rel in rel_list:
            if len(read_files) >= MAX_CONTEXT_SOURCES:
                blocking.append(
                    f"context-source cap reached ({MAX_CONTEXT_SOURCES}); "
                    "narrow --path/--source instead of reading more")
                return False
            target, error = resolve_repo_reference(repo, rel)
            if error or target is None or not target.is_file():
                blocking.append(f"context source unreadable or outside repo: "
                                f"{rel} (coverage incomplete)")
                continue
            try:
                text = target.read_text(encoding="utf-8")
            except (OSError, UnicodeError):
                blocking.append(f"context source unreadable: {rel} "
                                "(coverage incomplete)")
                continue
            read_files.append(rel)
            if collect_links:
                for link in MD_LINK_RE.findall(text):
                    if not link.startswith(("http://", "https://", "mailto:")):
                        rel_link = str(Path(rel).parent / link)
                        if rel_link not in seen:
                            seen.add(rel_link)
                            hop_candidates.append(rel_link)
        return True

    if read_bounded(candidates, collect_links=True):
        read_bounded(hop_candidates, collect_links=False)  # one hop only
    return read_files, blocking


def gather_memory_findings(repo: Path, paths: list[str]
                           ) -> tuple[list[str], int, list[str]]:
    roots = [repo / r for r in MEMORY_ROOTS if (repo / r).is_dir()]
    if not roots:
        return [], 0, []
    packets, errors = memory_validity.load_memory_packets(roots)
    if errors:
        return [], 0, errors
    scoped: list[str] = []
    out_of_scope = 0
    for packet_path, data in packets:
        findings, _notes = memory_validity.check_packet(packet_path, data, repo)
        for finding in findings:
            if (not paths or any(
                    rework_guard.declared_path_match(finding, path)[0]
                    for path in paths)):
                scoped.append(finding)
            else:
                out_of_scope += 1
    return scoped, out_of_scope, []


def build_units(repo: Path, paths: list[str]) -> list[tuple[str, int | None]]:
    per_path: list[tuple[str, int | None]] = []
    for path in sorted(paths):
        loc, _ = changed_loc_from_git(repo, [path])
        per_path.append((path, loc))
    return per_path


def compose(args, repo: Path) -> tuple[dict, list[str]]:
    records, errors = rework_guard.gather_records(repo)
    if errors:
        return {}, errors

    paths = rework_guard.normalize_paths(list(args.path))
    for path in paths:
        if path == ".":
            return {}, ["invalid task path '.': repository root is not a "
                        "bounded task path"]
        _target, error = resolve_repo_reference(repo, path)
        if error:
            return {}, [f"invalid task path {path!r}: {error}"]
    context_files, blocking = collect_context(
        repo, paths, list(args.source))

    history: list[str] = []
    if paths and args.history_limit:
        limit = min(args.history_limit, MAX_HISTORY)
        history = git_lines(
            repo, ["log", f"-n{limit}", "--format=%h %s", "--", *paths]) or []

    query_tokens = rework_guard.tokenize(
        " ".join([args.goal] + list(args.acceptance)))
    guard_findings, guard_weak = rework_guard.match_records(
        records, query_tokens, paths)

    memory_findings, memory_out_of_scope, mem_errors = gather_memory_findings(
        repo, paths)
    if mem_errors:
        return {}, mem_errors

    advisory: list[str] = []
    loc_source = None
    changed_loc = args.changed_loc
    if changed_loc is not None:
        loc_source = "declared_only"
    elif paths:
        changed_loc, loc_blocking = changed_loc_from_git(repo, paths)
        blocking.extend(loc_blocking)
        loc_source = "git" if changed_loc is not None else None

    loc_unknown = changed_loc is None
    over_budget = changed_loc is not None and changed_loc > LOC_BUDGET
    if loc_unknown:
        blocking.append("changed lines unknown: supply --changed-loc or git "
                        "data before any recommendation or receipt")
    if over_budget:
        blocking.append(
            f"over budget: {changed_loc} changed lines exceed the "
            f"{LOC_BUDGET}-line review unit; narrow before any receipt")

    rollback = args.rollback.strip() if args.rollback else ""
    if not rollback:
        blocking.append("rollback path missing: no recommendation or receipt "
                        "without a recovery path")
    if args.irreversible and args.risk in ("r0_trivial", "r1_routine",
                                           "r2_guarded"):
        blocking.append("irreversible change requires risk r3_sensitive or "
                        "r4_human_only (risk escalation needed)")

    checks: list[tuple[str, str, str]] = []
    if rollback:
        checks.append(("DO-CONFIRM",
                       f"rollback path is real and tested: {rollback}",
                       "operator-input"))
    overflow = 0
    for criterion in args.acceptance:
        if len(checks) < MAX_CHECKS:
            checks.append(("READ-DO", criterion, "operator-input"))
        else:
            overflow += 1
    if overflow:
        blocking.append(f"check overflow: {overflow} acceptance criteria "
                        f"beyond the {MAX_CHECKS}-item limit; narrow the task")

    if guard_findings:
        advisory.append(f"rework-guard: {len(guard_findings)} exact/path-"
                        "scope/strong prior-record hit(s)")
    if memory_findings:
        advisory.append(f"memory-validity: {len(memory_findings)} "
                        "stale/broken citation(s) in scope")

    if args.risk == "r4_human_only":
        recommendation = "escalate"
    elif blocking or advisory:
        recommendation = "revise"
    else:
        recommendation = "approve"

    units = build_units(repo, paths) if over_budget else []

    return {
        "goal": args.goal,
        "paths": paths,
        "risk": args.risk,
        "rollback": rollback,
        "irreversible": bool(args.irreversible),
        "acceptance": list(args.acceptance),
        "query_tokens": sorted(query_tokens),
        "query_provenance": "goal_and_acceptance_only",
        "context_files": context_files,
        "history": history,
        "guard_findings": guard_findings,
        "guard_weak": guard_weak,
        "guard_scanned": {
            kind: sum(1 for r in records if r["kind"] == kind)
            for kind in ("rejection", "decision", "deferral", "lesson")
        },
        "memory_findings": memory_findings,
        "memory_out_of_scope": memory_out_of_scope,
        "changed_loc": changed_loc,
        "loc_source": loc_source,
        "over_budget": over_budget,
        "loc_unknown": loc_unknown,
        "blocking_findings": blocking,
        "advisory_findings": advisory,
        "findings": blocking + advisory,
        "receipt_blocked": bool(blocking),
        "units": units,
        "session_minutes": args.session_minutes,
        "checks": checks,
        "recommendation": recommendation,
    }, []


def render_brief(model: dict) -> str:
    sections: list[tuple[list[list[str]], int]] = []
    loc = model["changed_loc"]
    loc_text = "UNKNOWN (blocking)" if loc is None else (
        f"{loc}/{LOC_BUDGET} ({model['loc_source']})")
    sections.append((line_groups([
        "REVIEW BRIEF (advisory, read-only; recommendation withheld until "
        "judgment)",
        f"risk={model['risk']} changed_loc={loc_text} "
        f"session<={model['session_minutes']}m", "",
    ]), SECTION_WORD_BUDGETS["header"]))

    evidence = [["1. EVIDENCE AND COUNTER-EVIDENCE"]]
    if model["blocking_findings"]:
        evidence.append(["   BLOCKING FINDINGS (no receipt until resolved):"])
        for finding in model["blocking_findings"]:
            evidence.append([f"   - {finding}"])
    if model["advisory_findings"]:
        evidence.append(["   ADVISORY FINDINGS (visible to judgment; never "
                         "auto-cleared):"])
        for finding in model["advisory_findings"]:
            evidence.append([f"   - {finding}"])
    for entry in model["guard_findings"]:
        group = [
            f"   DISCONFIRM [{entry['tier']}] {entry['kind']} "
            f"{entry['record_id']}: {entry['summary']} — ref: "
            f"{entry['source_path']}"]
        for condition in entry["conditions"][:2]:
            group.append(f"     {entry['condition_label']}: {condition}")
        if entry["kind"] == "lesson":
            group.append("     PRIOR-OUTCOME: recorded lesson from a "
                         "similar past decision (see ref)")
        evidence.append(group)
    for finding in model["memory_findings"]:
        evidence.append([f"   STALE {finding}"])
    if model["guard_weak"]:
        evidence.append(["   WEAK — MANUAL CONFIRMATION REQUIRED:"])
        for entry in model["guard_weak"]:
            evidence.append([
                f"   - {entry['kind']} {entry['record_id']}: "
                f"{entry['summary']} — ref: {entry['source_path']}"])
    if not (model["guard_findings"] or model["memory_findings"]
            or model["guard_weak"]):
        evidence.append([
            "   no exact, path-scope, or strong hit within bounded coverage"])
    evidence.append([""])
    sections.append((evidence, SECTION_WORD_BUDGETS["evidence"]))

    frame = ["2. DECISION FRAME", f"   INTENT: {model['goal']}"]
    if model["acceptance"]:
        frame.append("   INVARIANTS:")
        for criterion in model["acceptance"]:
            frame.append(f"   - {criterion} — ref: operator-input")
    else:
        frame.append("   INVARIANTS: none provided")
    frame.append("   PIECES (path — role in this change):")
    for path in model["paths"] or ["(no paths declared)"]:
        frame.append(f"   - {path} — declared change target")
    if model["history"]:
        frame.append("   RECENT HISTORY (bounded):")
        for item in model["history"]:
            frame.append(f"   - {item}")
    frame.append("")
    sections.append((line_groups(frame), SECTION_WORD_BUDGETS["frame"]))

    scanned = model["guard_scanned"]
    coverage = ["3. COVERAGE MANIFEST",
                f"   corpus scanned: rejections={scanned['rejection']} "
                f"decisions={scanned['decision']} "
                f"deferrals={scanned['deferral']} lessons={scanned['lesson']}",
                f"   task context read: "
                f"{', '.join(model['context_files']) or '(none)'}"]
    coverage.append("   relevance query: goal + acceptance only; context file "
                    "content excluded")
    if model["memory_out_of_scope"]:
        coverage.append(f"   memory findings outside task paths: "
                        f"{model['memory_out_of_scope']} (not shown)")
    coverage.append("   a no-hit above means no hit within bounded coverage, "
                    "not all clear")
    coverage.append("")
    sections.append((line_groups(coverage), SECTION_WORD_BUDGETS["coverage"]))

    risk = ["4. RISK AND REVERSIBILITY",
            f"   RISK TIER: {model['risk']}",
            f"   ROLLBACK PATH: {model['rollback'] or 'none provided (blocking)'}",
            f"   IRREVERSIBLE: {'yes' if model['irreversible'] else 'not declared'}"]
    if model["over_budget"]:
        risk.append("   CHUNK SCHEDULE (one unit per session, "
                    f"<= {model['session_minutes']} minutes each):")
        for i, (path, loc_i) in enumerate(model["units"], start=1):
            loc_note = f"{loc_i} changed lines" if loc_i is not None else "size unknown"
            fit = "" if (loc_i is not None and loc_i <= LOC_BUDGET) else \
                " — still over budget: split further before review"
            risk.append(f"   - unit {i}: {path} ({loc_note}){fit}")
    risk.append("")
    sections.append((line_groups(risk), SECTION_WORD_BUDGETS["risk"]))

    checks = ["5. CHECKS (max seven, typed)"]
    for kind, text, ref in model["checks"]:
        checks.append(f"   - [{kind}] {text} — ref: {ref}")
    if len(checks) == 1:
        checks.append("   - (none derivable; supply --acceptance and --rollback)")
    checks.append("")
    sections.append((line_groups(checks), SECTION_WORD_BUDGETS["checks"]))

    judgment = ["6. HUMAN JUDGMENT",
                "   record your own judgment (approve/reject/revise) BEFORE",
                "   viewing the compiler recommendation; selected findings go",
                "   into the receipt", ""]
    sections.append((line_groups(judgment), SECTION_WORD_BUDGETS["judgment"]))

    recommendation = ["7. COMPILER RECOMMENDATION"]
    if model["receipt_blocked"]:
        recommendation.append(
            f"   blocked: {len(model['blocking_findings'])} blocking "
            "finding(s) — resolve before any recommendation or receipt")
    else:
        recommendation.append("   withheld until a human judgment is recorded"
                              " (rerun with --emit-receipt on a terminal)")
    sections.append((line_groups(recommendation),
                     SECTION_WORD_BUDGETS["recommendation"]))

    out: list[str] = []
    for groups, budget in sections:
        out.extend(fit_section(groups, budget))
    return "\n".join(out)


def check_workspace(workspace: Path, repo: Path) -> str | None:
    if not workspace.is_dir():
        return f"workspace is not a directory: {workspace}"
    try:
        workspace.resolve().relative_to(repo.resolve())
        return "workspace must resolve outside the repository"
    except ValueError:
        pass
    for sub in ("reviews", "runs"):
        if not (workspace / sub).is_dir():
            return f"workspace is missing required subdirectory: {sub}/"
    return None


def artifact_and_source_refs(repo: Path, model: dict
                             ) -> tuple[list[dict], list[dict]]:
    artifact_refs: list[dict] = []
    hash_refs: list[dict] = []
    for path in model["paths"]:
        target = repo / path
        exists = target.is_file()
        artifact_refs.append({
            "artifact_type": "file",
            "artifact_path": path,
            "exists": exists,
            "change_kind": "declared_change_target",
        })
        if exists:
            digest = hashlib.sha256(target.read_bytes()).hexdigest()
            hash_refs.append({
                "source_type": "file",
                "source_path": path,
                "source_hash": digest,
                "relation": "reviewed_bytes",
            })
    return artifact_refs, hash_refs


def build_receipt(model: dict, args, judgment: str,
                  selected: list[str], created_at: str, repo: Path) -> dict:
    valid_ids = {e["record_id"] for e in model["guard_findings"]}
    unknown = [fid for fid in selected if fid not in valid_ids]
    if unknown:
        raise ValueError(
            f"selected finding ids not present in this brief: "
            f"{', '.join(unknown)}")
    uid = (f"review-brief-{slugify(args.goal)}-"
           f"{created_at.replace(':', '').replace('-', '')}-"
           f"{uuid.uuid4().hex[:8]}")
    must_read = sorted({e["source_path"] for e in model["guard_findings"]})
    source_refs = [
        {"source_type": "repo_doc", "source_path": e["source_path"],
         "relation": "judgment_basis"}
        for e in model["guard_findings"]
    ]
    artifact_refs, hash_refs = artifact_and_source_refs(repo, model)
    source_refs.extend(hash_refs)
    tags = ["interaction_channel:tty", "authentication:none",
            "review_mode:automated_check"]
    tags += [f"selected_finding:{fid}" for fid in selected]
    receipt = {
        "packet_uid": uid,
        "packet_type": "review_packet",
        "schema_version": "v0",
        "created_at": created_at,
        "created_by": args.created_by,
        "owner": args.owner,
        "supervision_mode": args.supervision_mode,
        "risk": model["risk"],
        "status": JUDGMENT_STATUS[judgment],
        "decision_needed": f"sign off on: {model['goal']}",
        "why_you_are_seeing_this": "interactive terminal judgment recorded "
                                   "after the review brief was displayed; "
                                   "identity, attention, and competence are "
                                   "not authenticated by this receipt",
        "change_summary": f"task-scoped change over {len(model['paths'])} "
                          f"path(s); changed_loc={model['changed_loc']} "
                          f"(loc_source={model['loc_source']})",
        "risk_summary": f"risk {model['risk']}; rollback: "
                        f"{model['rollback'] or 'none provided'}; "
                        f"{len(model['blocking_findings'])} blocking and "
                        f"{len(model['advisory_findings'])} advisory tool "
                        "finding(s)",
        "recommendation": model["recommendation"],
        "tags": tags,
    }
    if source_refs:
        receipt["source_refs"] = source_refs
    if artifact_refs:
        receipt["artifact_refs"] = artifact_refs
    if must_read:
        receipt["minimal_checks"] = {"must_read": must_read}
    return receipt


def finalize_receipt(receipt: dict, workspace: Path) -> tuple[str | None, str | None]:
    """Validate in a temp file, refuse collision, then move into reviews/.
    Returns (final_path, error)."""
    final_path = workspace / "reviews" / f"{receipt['packet_uid']}.v0.yaml"
    temp_path = workspace / "runs" / f".pending-{receipt['packet_uid']}.v0.yaml"
    temp_path.write_text(
        yaml.safe_dump(receipt, sort_keys=False, allow_unicode=False),
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(temp_path)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        temp_path.unlink(missing_ok=True)
        return None, ("receipt failed packet validation; nothing was kept\n"
                      + result.stdout + result.stderr)
    if final_path.exists():
        temp_path.unlink(missing_ok=True)
        return None, f"receipt already exists (collision refused): {final_path}"
    temp_path.replace(final_path)
    return str(final_path), None


def emit_receipt(model: dict, args, workspace: Path, repo: Path
                 ) -> tuple[int, str | None, str, int, str, str, bool]:
    """Interactive receipt flow. Returns (exit_override, receipt_path,
    judgment, triage_ms, observable_action, observable_action_source,
    brief_displayed). -1 = no override. brief_displayed is False when the
    refusal happened before the brief reached the terminal."""
    try:
        tty_in = open("/dev/tty", "r", encoding="utf-8")
        tty_out = open("/dev/tty", "w", encoding="utf-8")
    except OSError:
        print("ERROR: --emit-receipt refuses non-interactive execution "
              "(this refusal does not authenticate a human)", file=sys.stderr)
        return (2, None, "none", 0, "not_applicable", "none", False)

    triage_started = time.monotonic()
    with tty_in, tty_out:
        tty_out.write(render_brief(model) + "\n\n")
        tty_out.write("selected finding ids (comma-separated, may be empty): ")
        tty_out.flush()
        selected = [s.strip() for s in tty_in.readline().split(",") if s.strip()]
        tty_out.write("your judgment [approve/reject/revise] (empty cancels): ")
        tty_out.flush()
        judgment = tty_in.readline().strip().lower()
        triage_ms = int((time.monotonic() - triage_started) * 1000)
        if judgment not in JUDGMENT_STATUS:
            tty_out.write("cancelled; no receipt written\n")
            return -1, None, "cancelled", triage_ms, "none", "none", True
        tty_out.write("observable action attributable to the brief "
                      f"[{'/'.join(OBSERVABLE_ACTIONS)}] "
                      "(empty = derived from judgment): ")
        tty_out.flush()
        declared = tty_in.readline().strip().lower()
        if declared in OBSERVABLE_ACTIONS:
            observable = declared
            observable_source = "operator_declared_unauthenticated"
        else:
            observable = JUDGMENT_ACTION[judgment]
            observable_source = "derived_from_judgment"
        tty_out.write(f"compiler recommendation (advisory, computed before "
                      f"your judgment): {model['recommendation']}\n")

    created_at = utc_now()
    try:
        receipt = build_receipt(model, args, judgment, selected, created_at,
                                repo)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return (2, None, judgment, triage_ms, observable,
                observable_source, True)

    final_path, error = finalize_receipt(receipt, workspace)
    if error:
        print(f"ERROR: {error}", file=sys.stderr)
        return (2, None, judgment, triage_ms, observable,
                observable_source, True)
    print(f"receipt written: {final_path}")
    return (-1, final_path, judgment, triage_ms, observable,
            observable_source, True)


def append_run_record(workspace: Path, model: dict, args, record_kind: str,
                      compose_ms: int, triage_ms: int, judgment: str,
                      observable: str, observable_source: str,
                      displayed: bool, interaction_channel: str,
                      receipt_path: str | None, exit_code: int) -> None:
    run_id = str(uuid.uuid4())
    receipt_reference = None
    if receipt_path:
        receipt_reference = str(
            Path(receipt_path).resolve().relative_to(workspace.resolve()))
    record = {
        "record_version": "review_brief_run.v1",
        "record_kind": record_kind,
        "run_id": run_id,
        "signoff_id": getattr(args, "record_signoff_id", "") or run_id,
        "at": utc_now(),
        "risk": model.get("risk", getattr(args, "risk", None)),
        "eligible_signoff": (model.get("risk") or getattr(args, "risk", ""))
        in ELIGIBLE_RISKS,
        "brief_displayed": displayed,
        "brief_consulted": displayed,
        "consultation_claim": "display_proxy_only",
        "interaction_channel": interaction_channel,
        "authentication": "none",
        "judgment": judgment,
        "judgment_source": ("operator_input_unauthenticated"
                            if judgment in JUDGMENT_STATUS else "none"),
        "observable_action": observable,
        "observable_action_source": observable_source,
        "changed_loc": model.get("changed_loc"),
        "blocking_findings": len(model.get("blocking_findings", [])),
        "advisory_findings": len(model.get("advisory_findings", [])),
        "guard_hits": len(model.get("guard_findings", [])),
        "receipt": receipt_reference,
        "compose_ms": compose_ms,
        "triage_ms": triage_ms,
        "exit_code": exit_code,
    }
    runs_file = workspace / "runs" / "review_brief_runs.v1.jsonl"
    with runs_file.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record) + "\n")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Compose a task-scoped pre-sign-off review brief "
                    "(read-only, advisory)."
    )
    parser.add_argument("--repo", default=str(REPO))
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--goal", default="")
    parser.add_argument("--path", action="append", default=[])
    parser.add_argument("--risk", required=True, choices=RISK_TIERS)
    parser.add_argument("--rollback", default="")
    parser.add_argument("--irreversible", action="store_true")
    parser.add_argument("--acceptance", action="append", default=[])
    parser.add_argument("--source", action="append", default=[],
                        help="repository-relative context file (counted "
                             "against the 8-file cap)")
    parser.add_argument("--history-limit", type=int, default=0,
                        help=f"commit subjects to include (max {MAX_HISTORY})")
    parser.add_argument("--changed-loc", type=int, default=None,
                        help="declared changed lines (labeled declared_only)")
    parser.add_argument("--session-minutes", type=int, default=90,
                        choices=range(60, 91), metavar="60..90")
    parser.add_argument("--signoff-id", default="",
                        help="correlate preview and receipt invocations; the "
                             "declared value is stored only as a workspace-"
                             "scoped keyed UUID")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--emit-receipt", action="store_true")
    parser.add_argument("--record-skip", action="store_true",
                        help="log an eligible sign-off unit where the brief "
                             "was not displayed; composes nothing")
    parser.add_argument("--owner", default="")
    parser.add_argument("--supervision-mode", choices=SUPERVISION_MODES,
                        default="human_live_pair")
    parser.add_argument("--created-by", default="compose_review_brief.v0")
    args = parser.parse_args(argv)

    started = time.monotonic()
    repo = Path(args.repo).resolve()
    if not repo.is_dir():
        print(f"ERROR: repo is not a directory: {repo}", file=sys.stderr)
        return 2
    workspace = Path(args.workspace)
    workspace_error = check_workspace(workspace, repo)
    if workspace_error:
        print(f"ERROR: {workspace_error}", file=sys.stderr)
        return 2

    if args.changed_loc is not None and args.changed_loc < 0:
        print(f"ERROR: --changed-loc must be zero or positive; got "
              f"{args.changed_loc}. A negative line count is not a review "
              "unit, and declared-only provenance does not make it one",
              file=sys.stderr)
        return 2
    if args.signoff_id and not SIGNOFF_ID_RE.fullmatch(args.signoff_id):
        print("ERROR: --signoff-id must be 1-64 characters from "
              "A-Z, a-z, 0-9, underscore, dot, colon, or hyphen",
              file=sys.stderr)
        return 2

    if args.record_skip:
        try:
            prepare_record_signoff_id(args, workspace)
        except ValueError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        append_run_record(workspace, {"risk": args.risk}, args, "skip", 0, 0,
                          "none", "not_applicable", "none", displayed=False,
                          interaction_channel="none",
                          receipt_path=None, exit_code=0)
        print("skip recorded: eligible sign-off unit without brief display")
        return 0

    if not args.goal:
        print("ERROR: --goal is required unless --record-skip", file=sys.stderr)
        return 2

    model, errors = compose(args, repo)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 2
    compose_ms = int((time.monotonic() - started) * 1000)  # frozen pre-interaction

    exit_code = 1 if model["findings"] else 0
    receipt_path = None
    judgment = "none"
    observable = "not_applicable"
    observable_source = "none"
    triage_ms = 0
    record_kind = "preview"
    displayed = True
    interaction_channel = "stdout"

    if args.emit_receipt:
        if args.format == "json":
            print("ERROR: JSON mode never emits a receipt", file=sys.stderr)
            return 2
        if not args.owner:
            print("ERROR: --emit-receipt requires --owner (the accountable "
                  "human)", file=sys.stderr)
            return 2
        try:
            prepare_record_signoff_id(args, workspace)
        except ValueError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        if model["receipt_blocked"]:
            print("ERROR: no receipt while blocking findings are open "
                  "(resolve or narrow first):", file=sys.stderr)
            for finding in model["blocking_findings"]:
                print(f"  - {finding}", file=sys.stderr)
            append_run_record(workspace, model, args, "signoff_attempt",
                              compose_ms, 0, "none", "not_applicable", "none",
                              displayed=False, interaction_channel="none",
                              receipt_path=None, exit_code=2)
            return 2
        (override, receipt_path, judgment, triage_ms, observable,
         observable_source, displayed) = emit_receipt(
             model, args, workspace, repo)
        interaction_channel = "tty" if displayed else "none"
        # a sign-off exists only where a human judgment was recorded
        record_kind = ("signoff" if judgment in JUDGMENT_STATUS
                       else "signoff_attempt")
        if override != -1:
            append_run_record(workspace, model, args, record_kind, compose_ms,
                              triage_ms, judgment, observable,
                              observable_source, displayed=displayed,
                              interaction_channel=interaction_channel,
                              receipt_path=None,
                              exit_code=override)
            return override
    else:
        try:
            prepare_record_signoff_id(args, workspace)
        except ValueError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        if args.format == "json":
            payload = dict(model)
            payload.pop("recommendation")
            payload["recommendation_withheld"] = True
            print(json.dumps(payload, indent=2, default=str))
        else:
            print(render_brief(model))

    append_run_record(workspace, model, args, record_kind, compose_ms,
                      triage_ms, judgment, observable, observable_source,
                      displayed=displayed,
                      interaction_channel=interaction_channel,
                      receipt_path=receipt_path, exit_code=exit_code)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
