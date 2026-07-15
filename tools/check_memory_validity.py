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
The v0 schema's string-only invalidation.source_hashes entries are also noted
as uncheckable when they do not identify a source_path; the checker does not
invent a path-to-hash association.
When --generation is supplied, a packet declaring validity.runtime_generation
different from the supplied value is reported stale (the model-churn
invalidation class becomes mechanically checkable for packets that opt in).
The checker never mutates packet status; marking a packet stale or
broken_reference remains a human/review action.

Usage:
  python3 tools/check_memory_validity.py                 # default roots
  python3 tools/check_memory_validity.py --root <dir>    # explicit roots (repeatable)

Exit: 0 = no findings; 1 = findings (advisory); 2 = setup error.

Unreadable, malformed, or duplicate-key YAML is a setup error rather than a
silently skipped packet. File references are never followed outside --repo.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

from _shadowmas_readonly import load_yaml_documents, resolve_repo_reference

REPO = Path(__file__).resolve().parents[1]
DEFAULT_ROOTS = ["07_working", "examples/packets", "03_memory/shared_memory"]


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_memory_packets(
    roots: list[Path],
) -> tuple[list[tuple[Path, dict]], list[str]]:
    documents, errors = load_yaml_documents(roots)
    packets = [
        (path, data)
        for path, data in documents
        if isinstance(data, dict) and data.get("packet_type") == "memory_packet"
    ]
    return packets, errors


def check_packet(packet_path: Path, data: dict, repo: Path,
                 generation: str | None = None) -> tuple[list[str], list[str]]:
    findings: list[str] = []
    notes: list[str] = []
    uid = data.get("packet_uid", packet_path.name)

    refs = data.get("source_refs")
    if refs is not None and not isinstance(refs, list):
        findings.append(
            f"{uid}: broken_reference: source_refs has invalid shape (expected list)"
        )
    elif isinstance(refs, list):
        for index, ref in enumerate(refs):
            if not isinstance(ref, dict):
                findings.append(
                    f"{uid}: broken_reference: source_refs[{index}] has invalid shape "
                    "(expected object)"
                )
                continue
            if "source_path" not in ref:
                continue
            source_path = ref.get("source_path")
            target, error = resolve_repo_reference(repo, source_path)
            if error:
                findings.append(
                    f"{uid}: broken_reference: invalid source_refs path "
                    f"{source_path!r} ({error})"
                )
            elif target is not None and not target.is_file():
                findings.append(
                    f"{uid}: broken_reference: source_refs path does not resolve: {source_path}"
                )

    invalidation = data.get("invalidation")
    if isinstance(invalidation, dict):
        source_hashes = invalidation.get("source_hashes")
        if source_hashes is not None and not isinstance(source_hashes, list):
            notes.append(
                f"{uid}: NOTE invalidation.source_hashes is not a list; "
                "source drift is not mechanically checkable"
            )
            source_hashes = []
        for index, entry in enumerate(source_hashes or []):
            if isinstance(entry, str):
                notes.append(
                    f"{uid}: NOTE invalidation.source_hashes[{index}] uses the v0 "
                    "string shape without a source_path mapping; source drift is not "
                    "mechanically checkable"
                )
                continue
            if not isinstance(entry, dict):
                notes.append(
                    f"{uid}: NOTE invalidation.source_hashes[{index}] has an "
                    "unrecognized shape; source drift is not mechanically checkable"
                )
                continue
            source_path = entry.get("source_path")
            recorded = entry.get("sha256")
            if not source_path or not recorded:
                notes.append(
                    f"{uid}: NOTE invalidation.source_hashes[{index}] lacks "
                    "source_path or sha256; source drift is not mechanically checkable"
                )
                continue
            target, error = resolve_repo_reference(repo, source_path)
            if error:
                findings.append(
                    f"{uid}: broken_reference: invalid hashed source path "
                    f"{source_path!r} ({error})"
                )
            elif target is not None and not target.is_file():
                findings.append(
                    f"{uid}: broken_reference: hashed source does not resolve: {source_path}"
                )
            elif target is not None:
                try:
                    current_hash = sha256_of(target)
                except OSError as exc:
                    findings.append(
                        f"{uid}: broken_reference: hashed source is unreadable: "
                        f"{source_path} ({exc})"
                    )
                else:
                    if current_hash != recorded:
                        findings.append(
                            f"{uid}: stale: source content drifted from recorded hash: "
                            f"{source_path}"
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

    packets, load_errors = load_memory_packets(roots)
    if load_errors:
        for error in load_errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 2
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
