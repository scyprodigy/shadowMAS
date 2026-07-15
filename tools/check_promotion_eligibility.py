#!/usr/bin/env python3
"""Check whether a memory_packet meets the seven T4->T3 promotion preconditions.

Read-only. ADVISORY. Mechanizes the eligibility preconditions specified in
07_working/drafts/PROMOTION-GATE-SEMANTICS.PROPOSAL.v0.en.md. Eligibility is
NOT approval: a passing packet is merely ready for a promotion review packet
and a human/delegated decision. This tool promotes nothing and writes nothing.

It reuses the real ghost-dependency logic from check_memory_validity rather
than reimplementing it, so the gate and the validity checker cannot drift.

Usage:
  python3 tools/check_promotion_eligibility.py <memory_packet.yaml>

Exit: 0 = eligible for review; 1 = not eligible; 2 = setup / input error.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

from _shadowmas_readonly import UniqueKeyLoader, resolve_repo_reference

REPO = Path(__file__).resolve().parents[1]
VALIDATOR = REPO / "05_scripts" / "validate" / "shadowmas_validate.py"

sys.path.insert(0, str(REPO / "tools"))
import check_memory_validity  # noqa: E402


def evaluate(path: Path, data: dict) -> list[tuple[str, bool, str]]:
    results: list[tuple[str, bool, str]] = []

    proc = subprocess.run([sys.executable, str(VALIDATOR), str(path)],
                          capture_output=True, text=True)
    results.append(("1 packet validator passes", proc.returncode == 0,
                    "OK" if proc.returncode == 0 else "validator returned non-zero"))

    pc = data.get("promotion_candidate")
    results.append(("2 promotion_candidate is yes", pc == "yes", f"promotion_candidate={pc!r}"))

    status = data.get("status")
    results.append(("3 status is candidate", status == "candidate", f"status={status!r}"))

    refs = data.get("source_refs") or []
    paths = [r.get("source_path") for r in refs if isinstance(r, dict) and r.get("source_path")]
    unresolved = []
    for source_path in paths:
        target, error = resolve_repo_reference(REPO, source_path)
        if error:
            unresolved.append(f"{source_path!r} ({error})")
        elif target is not None and not target.is_file():
            unresolved.append(str(source_path))
    ok4 = bool(refs) and not unresolved
    detail4 = "OK" if ok4 else (
        "source_refs empty" if not refs else f"unresolved: {unresolved}")
    results.append(("4 source_refs non-empty and resolve", ok4, detail4))

    triggers = data.get("invalidation_triggers") or []
    results.append(("5 invalidation_triggers non-empty", bool(triggers),
                    f"{len(triggers)} trigger(s)"))

    findings, _ = check_memory_validity.check_packet(path, data, REPO)
    results.append(("6 no broken_reference or stale", not findings,
                    "OK" if not findings else f"{len(findings)} finding(s)"))

    has_conf = data.get("confidence") is not None
    results.append(("7 confidence present (visible, not a gate)", has_conf,
                    f"confidence={data.get('confidence')!r}"))

    return results


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("usage: check_promotion_eligibility.py <memory_packet.yaml>", file=sys.stderr)
        return 2
    path = Path(argv[0])
    if not path.is_file():
        print(f"ERROR: not a file: {path}", file=sys.stderr)
        return 2
    try:
        data = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    except (OSError, UnicodeError) as exc:
        print(f"ERROR: unable to read packet: {exc}", file=sys.stderr)
        return 2
    except yaml.YAMLError as exc:
        print(f"ERROR: yaml parse failed: {exc}", file=sys.stderr)
        return 2
    if not isinstance(data, dict) or data.get("packet_type") != "memory_packet":
        print("NOT ELIGIBLE: not a memory_packet")
        return 1

    results = evaluate(path, data)
    print(f"promotion eligibility for {data.get('packet_uid', path.name)}:\n")
    for label, ok, detail in results:
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}  ({detail})")
    eligible = all(ok for _, ok, _ in results)
    print()
    if eligible:
        print("ELIGIBLE FOR REVIEW — author a promotion review packet; eligibility is not approval")
        return 0
    print("NOT ELIGIBLE — see FAIL rows above")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
