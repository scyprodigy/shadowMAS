#!/usr/bin/env python3
"""Validate rejection_record instances against the field contract in their proposal.

Read-only. ADVISORY. The rejection_record working family (see
07_working/drafts/rationale/rejection_record.PROPOSAL.v0.yaml) is not a
02_packets family and has no schema validator; this checker gives it the same
machine-first discipline the packet families get, so a malformed instance does
not pass silently. The required-field contract is read from the proposal's
`required_fields` block — the proposal stays the single owner of the contract,
and this checker compiles its rules from it rather than hardcoding them.

Scope: 07_working/drafts/rationale/rejection_*.v0.yaml, excluding the
`.PROPOSAL.` marker file.

Usage:
  python3 tools/check_rejection_records.py

Exit: 0 = all instances valid (or none present); 1 = at least one invalid; 2 = setup error.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
RATIONALE_DIR = REPO / "07_working" / "drafts" / "rationale"
PROPOSAL = RATIONALE_DIR / "rejection_record.PROPOSAL.v0.yaml"


def load_contract() -> list[str]:
    data = yaml.safe_load(PROPOSAL.read_text(encoding="utf-8"))
    required = data.get("required_fields") if isinstance(data, dict) else None
    if not isinstance(required, dict):
        raise ValueError("proposal has no required_fields mapping")
    return list(required.keys())


def is_empty(value: object) -> bool:
    if value is None:
        return True
    if isinstance(value, (str, list, dict)) and len(value) == 0:
        return True
    return False


def check_instance(path: Path, required: list[str]) -> list[str]:
    findings = []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        return [f"{path.name}: not parseable yaml: {exc}"]
    if not isinstance(data, dict):
        return [f"{path.name}: not a mapping"]

    for field in required:
        if field not in data or is_empty(data[field]):
            findings.append(f"{path.name}: missing or empty required field: {field}")

    # rejection_scope must carry applies_to (the paper-simulation split)
    scope = data.get("rejection_scope")
    if isinstance(scope, dict):
        if is_empty(scope.get("applies_to")):
            findings.append(f"{path.name}: rejection_scope.applies_to missing or empty")
    elif "rejection_scope" in data:
        findings.append(f"{path.name}: rejection_scope must be a mapping with applies_to")

    return findings


def main() -> int:
    if not PROPOSAL.exists():
        print(f"ERROR: missing proposal owner: {PROPOSAL}", file=sys.stderr)
        return 2
    try:
        required = load_contract()
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    instances = sorted(
        p for p in RATIONALE_DIR.glob("rejection_*.v0.yaml")
        if ".PROPOSAL." not in p.name
    )
    findings = []
    for path in instances:
        findings.extend(check_instance(path, required))

    for line in findings:
        print(f"FINDING {line}")
    print(f"checked {len(instances)} rejection_record instance(s) "
          f"against {len(required)} required field(s)")
    if findings:
        print(f"{len(findings)} rejection_record finding(s) (advisory; human review decides).")
        return 1
    print("OK all rejection_record instances satisfy the proposal contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
