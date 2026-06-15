#!/usr/bin/env python3
"""Advisory memory-validity checker: the ghost-dependency rule's mechanical reader.

Read-only. ADVISORY. Not runtime enforcement, not a promotion gate, and not a
status writer; it surfaces findings so the human review gate can act.

Implements the MEMORY-PLANE-HARNESS ghost-dependency rule for memory packets:
a memory whose cited source no longer resolves must not keep behaving as
active reusable memory. Finding classes use harness vocabulary:

- broken_reference: a source_refs / invalidation.source_hashes path no longer
  resolves inside the repo
- stale: a recorded invalidation.source_hashes sha256 no longer matches the
  current content of the cited path

Declared-but-not-mechanically-checkable conditions (validity.stale_on entries
such as a model or runtime generation change) are echoed as NOTE lines only.
When --generation is supplied, a packet declaring validity.runtime_generation
different from the supplied value is reported stale (the model-churn
invalidation class becomes mechanically checkable for packets that opt in).
The checker never mutates packet status; marking a packet stale or
broken_reference remains a human/review action.

Usage:
  python3 tools/check_memory_validity.py                 # default roots
  python3 tools/check_memory_validity.py --root <dir>    # explicit roots (repeatable)

Exit: 0 = no findings; 1 = findings (advisory); 2 = setup error.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
DEFAULT_ROOTS = ["07_working", "examples/packets", "03_memory/shared_memory"]


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_memory_packets(roots: list[Path]) -> list[tuple[Path, dict]]:
    packets = []
    for root in roots:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.yaml")) + sorted(root.rglob("*.yml")):
            try:
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
            except (OSError, yaml.YAMLError):
                continue
            if isinstance(data, dict) and data.get("packet_type") == "memory_packet":
                packets.append((path, data))
    return packets


def check_packet(packet_path: Path, data: dict, repo: Path,
                 generation: str | None = None) -> tuple[list[str], list[str]]:
    findings: list[str] = []
    notes: list[str] = []
    uid = data.get("packet_uid", packet_path.name)

    refs = data.get("source_refs")
    if isinstance(refs, list):
        for ref in refs:
            if not isinstance(ref, dict):
                continue
            source_path = ref.get("source_path")
            if not source_path:
                continue
            if not (repo / source_path).exists():
                findings.append(
                    f"{uid}: broken_reference: source_refs path does not resolve: {source_path}"
                )

    invalidation = data.get("invalidation")
    if isinstance(invalidation, dict):
        for entry in invalidation.get("source_hashes") or []:
            if not isinstance(entry, dict):
                continue
            source_path = entry.get("source_path")
            recorded = entry.get("sha256")
            if not source_path or not recorded:
                continue
            target = repo / source_path
            if not target.exists():
                findings.append(
                    f"{uid}: broken_reference: hashed source does not resolve: {source_path}"
                )
            elif sha256_of(target) != recorded:
                findings.append(
                    f"{uid}: stale: source content drifted from recorded hash: {source_path}"
                )

    validity = data.get("validity")
    if isinstance(validity, dict):
        declared_generation = validity.get("runtime_generation")
        if generation and declared_generation and str(declared_generation) != generation:
            findings.append(
                f"{uid}: stale: declared runtime_generation "
                f"{declared_generation!r} != current {generation!r}"
            )
        for condition in validity.get("stale_on") or []:
            notes.append(
                f"{uid}: NOTE declared stale_on condition (not mechanically checkable here): {condition}"
            )

    return findings, notes


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Advisory ghost-dependency check over memory packets."
    )
    parser.add_argument("--root", action="append",
                        help="search root for memory packets (repeatable)")
    parser.add_argument("--repo", help="repo root for resolving source_refs (default: this repo)")
    parser.add_argument("--generation",
                        help="current model/runtime generation id; packets declaring a "
                             "different validity.runtime_generation are reported stale")
    args = parser.parse_args(argv)

    repo = Path(args.repo).resolve() if args.repo else REPO
    if not repo.is_dir():
        print(f"ERROR: repo root not a directory: {repo}", file=sys.stderr)
        return 2
    roots = [Path(r) if Path(r).is_absolute() else repo / r
             for r in (args.root or DEFAULT_ROOTS)]

    packets = load_memory_packets(roots)
    all_findings: list[str] = []
    for packet_path, data in packets:
        findings, notes = check_packet(packet_path, data, repo, generation=args.generation)
        all_findings.extend(findings)
        for line in findings + notes:
            print(line)

    print(f"checked {len(packets)} memory packet(s)")
    if all_findings:
        print(f"FINDING {len(all_findings)} memory-validity finding(s) "
              f"(advisory; human review decides status changes).")
        return 1
    print("OK no broken_reference or stale findings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
