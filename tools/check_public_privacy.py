#!/usr/bin/env python3
"""Check a Git snapshot or complete reachable history using generic privacy rules.

Only categories, object IDs, and line numbers are reported. No matched values
or snippets are printed. This is pattern detection, not proof of anonymity;
operator-specific identifiers must be checked privately as well.
"""
from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

EMAIL = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
HOME = re.compile(r"(?:/home/|/Users/|[A-Za-z]:[\\/]Users[\\/])([A-Za-z0-9_.-]+)")
PRIVATE_BRANCH = re.compile(r"\bprivate/[A-Za-z0-9][A-Za-z0-9._/-]*")
ENCODED_LITERAL = re.compile(r'''\bb64decode\(\s*b?["'][A-Za-z0-9+/=]{8,}["']''')
SECRET = re.compile(
    r"-----BEGIN (?:[A-Z0-9 ]+ )?PRIVATE KEY-----|"
    r"\bghp_[A-Za-z0-9]{30,}\b|\bgithub_pat_[A-Za-z0-9_]{40,}\b|"
    r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b|"
    r"\bsk-(?:proj-|ant-)?[A-Za-z0-9_\-]{30,}\b"
)
PLACEHOLDER_USERS = {"user", "username", "developer", "operator", "example"}
EXAMPLE_DOMAINS = {"example.com", "example.org", "example.net"}
EXPORT_SUFFIXES = {".pdf", ".docx", ".pptx"}


def public_email(value: str) -> bool:
    name, domain = value.lower().rsplit("@", 1)
    return (
        domain in EXAMPLE_DOMAINS
        or domain.endswith((".invalid", ".test", ".example"))
        or domain == "users.noreply.github.com"
        or (name == "noreply" and domain == "github.com")
    )


def categories(line: str) -> list[str]:
    # Also inspect email addresses written as regex literals.
    normalized = line.replace(r"\.", ".").replace(r"\@", "@")
    found = []
    if any(not public_email(m.group()) for m in EMAIL.finditer(normalized)):
        found.append("contact_email")
    if any(m.group(1).lower() not in PLACEHOLDER_USERS for m in HOME.finditer(line)):
        found.append("local_user_path")
    if PRIVATE_BRANCH.search(line):
        found.append("private_branch_reference")
    if ENCODED_LITERAL.search(line):
        found.append("encoded_literal_review")
    if SECRET.search(line):
        found.append("credential_shape")
    return found


def git(repo: Path, *args: str) -> bytes:
    return subprocess.check_output(
        ["git", "--no-replace-objects", "-C", str(repo), *args],
        stderr=subprocess.PIPE,
    )


def scan(repo: Path, revision: str, history: bool) -> tuple[list[dict], dict]:
    if history and git(repo, "rev-parse", "--is-shallow-repository").strip() == b"true":
        raise ValueError("complete history required")
    tip = git(repo, "rev-parse", "--verify", "--end-of-options", revision + "^{commit}").decode().strip()
    commits = git(repo, "rev-list", tip).decode().splitlines() if history else [tip]
    blobs: set[str] = set()
    paths: set[tuple[str, str]] = set()
    findings = []
    for sha in commits:
        metadata = git(repo, "cat-file", "commit", sha).decode("utf-8", "replace")
        for number, line in enumerate(metadata.splitlines(), 1):
            for category in categories(line):
                findings.append({"object": sha, "line": number, "category": category})
        for entry in git(repo, "ls-tree", "-rz", sha).split(b"\0"):
            if not entry:
                continue
            header, name = entry.split(b"\t", 1)
            _, kind, oid = header.decode().split()
            if kind == "blob":
                blobs.add(oid)
                paths.add((oid, name.decode("utf-8", "replace")))
    for oid, name in sorted(paths):
        for category in categories(name):
            findings.append({"object": oid, "line": 0, "category": "filename_" + category})
        if Path(name).suffix.lower() in EXPORT_SUFFIXES:
            findings.append({"object": oid, "line": 0, "category": "generated_export"})
    for oid in sorted(blobs):
        data = git(repo, "cat-file", "blob", oid)
        # Scan raw bytes as text too, including strings in binary metadata.
        for number, line in enumerate(data.decode("utf-8", "replace").splitlines(), 1):
            for category in categories(line):
                findings.append({"object": oid, "line": number, "category": category})
    return findings, {"commits": len(commits), "blobs": len(blobs)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", default="HEAD", help="commit or ref to inspect")
    parser.add_argument("--history", action="store_true", help="require and inspect full reachable history")
    args = parser.parse_args()
    try:
        findings, coverage = scan(Path(__file__).resolve().parents[1], args.ref, args.history)
    except (OSError, ValueError, subprocess.SubprocessError):
        print("ERROR privacy inspection incomplete; no clean result")
        return 2
    for finding in findings:
        print(f"{finding['object']}:{finding['line']} {finding['category']}")
    print(f"{'FINDINGS' if findings else 'PASS'} public privacy: "
          f"{len(findings)} findings; {coverage['commits']} commits, {coverage['blobs']} blobs")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
