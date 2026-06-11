#!/usr/bin/env python3
"""Advisory anchor-drift checker for repeated semantic anchors across landing files.

Read-only. ADVISORY. Not runtime enforcement and not a merge blocker by itself;
it surfaces findings so the human git-review gate can act.

Anchors are extracted from canonical files at run time (compiled, not
hand-maintained here — see CURRENT-TRUTH Compiled Intake Rule). Checks:

1. count-claim: a sentence claiming "<word> ... failure modes" must match the
   number of bullets that follow it (CURRENT-TRUTH and README).
2. intake-list duplication: the exact v0 intake pack list is owned by
   CURRENT-TRUTH `Current v0 Intake Pack`; any other file repeating the full
   list is a finding (landing files must reference, not repeat).
3. deprecated vocabulary: superseded layer/term names must not appear outside
   the archive.

Usage:
  python3 tools/check_anchor_drift.py

Exit: 0 = no findings; 1 = findings (advisory); 2 = setup error.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CURRENT_TRUTH = REPO / "01_truth" / "SHADOWMAS-CURRENT-TRUTH.v0.en.md"
COUNT_CLAIM_FILES = [CURRENT_TRUTH, REPO / "README.md"]
SCAN_EXCLUDE_PARTS = {".git", "archive", "__pycache__", "node_modules"}

# superseded wording -> replacement, kept here as the single deprecation list
DEPRECATED_TERMS = {
    "Coordination / Governance Shadow": "shadowMAS Authority-Boundary Orchestration",
}

WORD_NUMBERS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
}

CLAIM_RE = re.compile(
    r"reduce (?P<word>" + "|".join(WORD_NUMBERS) + r")\b.*failure modes",
    re.IGNORECASE,
)


def bullets_after(lines: list[str], start: int) -> int:
    count = 0
    seen_first = False
    for line in lines[start + 1:]:
        stripped = line.strip()
        if stripped.startswith("- "):
            count += 1
            seen_first = True
        elif seen_first and stripped and not stripped.startswith("- "):
            break
        elif seen_first and not stripped:
            break
    return count


def check_count_claims() -> list[str]:
    findings = []
    for path in COUNT_CLAIM_FILES:
        lines = path.read_text(encoding="utf-8").splitlines()
        for i, line in enumerate(lines):
            match = CLAIM_RE.search(line)
            if not match:
                continue
            claimed = WORD_NUMBERS[match.group("word").lower()]
            actual = bullets_after(lines, i)
            if actual and actual != claimed:
                findings.append(
                    f"{path.relative_to(REPO)}:{i + 1}: claims {claimed} failure modes "
                    f"but lists {actual} bullets"
                )
    return findings


def intake_pack_paths() -> list[str]:
    text = CURRENT_TRUTH.read_text(encoding="utf-8")
    section = re.search(
        r"### Current v0 Intake Pack\n(.*?)(?:\n#|$)", text, re.DOTALL
    )
    if not section:
        return []
    return re.findall(r"`([^`]+\.md)`", section.group(1))


def scannable_md_files() -> list[Path]:
    files = []
    for path in REPO.rglob("*.md"):
        if any(part in SCAN_EXCLUDE_PARTS for part in path.parts):
            continue
        files.append(path)
    return files


def check_intake_duplication(pack: list[str], window: int = 8) -> list[str]:
    # scattered mentions across sections are fine; only a co-located full
    # enumeration counts as repeating the list
    findings = []
    for path in scannable_md_files():
        if path == CURRENT_TRUTH:
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        for start in range(len(lines)):
            chunk = "\n".join(lines[start:start + window])
            if all(p in chunk for p in pack):
                findings.append(
                    f"{path.relative_to(REPO)}:{start + 1}: repeats the full v0 intake "
                    f"pack list; reference CURRENT-TRUTH `Current v0 Intake Pack` instead"
                )
                break
    return findings


def check_deprecated_terms() -> list[str]:
    findings = []
    for path in scannable_md_files():
        text = path.read_text(encoding="utf-8")
        for term, replacement in DEPRECATED_TERMS.items():
            if term in text and path.name != Path(__file__).name:
                findings.append(
                    f"{path.relative_to(REPO)}: deprecated term '{term}' "
                    f"(use '{replacement}')"
                )
    return findings


def main() -> int:
    if not CURRENT_TRUTH.exists():
        print(f"ERROR: missing {CURRENT_TRUTH}", file=sys.stderr)
        return 2

    pack = intake_pack_paths()
    findings = check_count_claims()
    if pack:
        findings += check_intake_duplication(pack)
    else:
        findings.append(
            "01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md: could not locate "
            "`Current v0 Intake Pack` section (anchor owner missing or renamed)"
        )
    findings += check_deprecated_terms()

    for finding in findings:
        print(f"FINDING {finding}")
    if findings:
        print(f"{len(findings)} anchor-drift finding(s) (advisory; human review decides).")
        return 1
    print("OK no anchor drift detected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
