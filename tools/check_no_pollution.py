#!/usr/bin/env python3
"""Scan the tracked tree for known pollution patterns.

Standing automated defense against re-introducing personal identifiers,
third-party PII, commercial-project names, or credentials into the
shadowMAS repository.

Exit codes:
  0  no pollution found
  1  pollution found (one or more matches)
  2  usage / environment error

Usage:
  python3 tools/check_no_pollution.py
"""

from __future__ import annotations

import base64
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple


# (pattern, human label) — patterns are regex; matches are case-sensitive
# Patterns derived from the R8b history scan + general credential shapes.

# Personally-identifying handle decoded at runtime; literal never appears in source.
_PERSONAL_HANDLE = base64.b64decode("ZGFrdWFudGF4aQ==").decode()

PATTERNS: List[Tuple[str, str]] = [
    # Personal email handle (encoded above so literal never appears in source)
    (rf"\b{_PERSONAL_HANDLE}\b", "personal email handle"),
    # Third-party PII surfaced in R8b
    (r"@schmidtsciences\.org", "third-party email domain"),
    (r"\bmcoyne@", "third-party contact"),
    (r"\btrustworthyai@", "third-party contact"),
    # Cryptographic / SSH key headers
    (r"BEGIN OPENSSH PRIVATE KEY", "SSH private key"),
    (r"BEGIN RSA PRIVATE KEY", "RSA private key"),
    (r"BEGIN DSA PRIVATE KEY", "DSA private key"),
    (r"BEGIN EC PRIVATE KEY", "EC private key"),
    (r"BEGIN PGP PRIVATE KEY", "PGP private key"),
    # Cloud / SaaS credential patterns
    (r"ghp_[a-zA-Z0-9]{30,}", "GitHub personal access token"),
    (r"AKIA[A-Z0-9]{16}", "AWS access key id"),
    (r"\bsk-[a-zA-Z0-9]{30,}", "OpenAI/Anthropic-style API key"),
    (r"xoxb-[0-9]+-[0-9]+-", "Slack bot token"),
    (r"AIza[0-9A-Za-z_-]{35}", "Google API key"),
    (r"glpat-[0-9a-zA-Z_-]{20}", "GitLab personal access token"),
]

# Files exempted from scan. The scanner itself necessarily contains the
# patterns by definition. The rationale doc is written to NOT reproduce
# the actual strings, but is exempted defensively.
EXCLUDE_PATHS = {
    "tools/check_no_pollution.py",
    "07_working/drafts/rationale/history_pollution_residual_risk.md",
}


def list_tracked_files() -> List[Path]:
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        print(f"ERROR: failed to enumerate tracked files: {exc}", file=sys.stderr)
        sys.exit(2)
    return [Path(p) for p in result.stdout.splitlines() if p]


def scan_file(path: Path, compiled_patterns) -> List[Tuple[Path, int, str, str]]:
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeDecodeError):
        return []

    findings: List[Tuple[Path, int, str, str]] = []
    for line_num, line in enumerate(content.splitlines(), start=1):
        for compiled, label in compiled_patterns:
            if compiled.search(line):
                snippet = line.strip()
                if len(snippet) > 80:
                    snippet = snippet[:77] + "..."
                findings.append((path, line_num, label, snippet))
    return findings


def main() -> int:
    compiled = [(re.compile(p), label) for p, label in PATTERNS]

    paths = list_tracked_files()
    all_findings: List[Tuple[Path, int, str, str]] = []
    scanned = 0

    for path in paths:
        if str(path) in EXCLUDE_PATHS:
            continue
        if not path.is_file():
            continue
        scanned += 1
        all_findings.extend(scan_file(path, compiled))

    if all_findings:
        print(f"POLLUTION FOUND: {len(all_findings)} match(es) in {scanned} scanned files")
        for path, line_num, label, snippet in all_findings:
            print(f"  {path}:{line_num} [{label}] {snippet}")
        return 1

    print(f"OK no pollution patterns in {scanned} scanned files")
    print(f"   (patterns: {len(PATTERNS)}, exclusions: {len(EXCLUDE_PATHS)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
