#!/usr/bin/env python3
"""Repo-wide packet reference-integrity gate: no packet edge may dangle.

Read-only. ADVISORY. The evidence-chain surfaces (chain tracing, forensics,
genealogy) are only trustworthy if packet references resolve. This gate walks
every packet's reference edges and reports any that do not resolve, for the
human review gate to act on. It mutates nothing.

Edges checked, across all packet types under the scanned roots:
- source_refs[].source_id      -> must resolve to a known packet_uid
- source_refs[].source_path    -> must resolve to a file
- related_packets[]            -> must resolve to a known packet_uid
- minimal_checks.must_read[]   -> must resolve to a file
- promotion_snapshot.source_hashes[].source_path -> must resolve to a file

Packet UIDs must be unique across the scan. File edges must be non-empty,
repository-relative paths that resolve inside --repo. Unreadable, malformed,
or duplicate-key YAML makes the scan incomplete and exits as a setup error.

source_id values that do not look like local packet uids are skipped (an edge
may legitimately name an external artifact); a value matching the local uid
naming shape but absent from the scanned set is a finding.

Usage:
  python3 tools/check_packet_refs.py
  python3 tools/check_packet_refs.py --root <dir> --repo <root>

Exit: 0 = no findings; 1 = findings (advisory); 2 = setup or scan error.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from _shadowmas_readonly import load_yaml_documents, resolve_repo_reference

REPO = Path(__file__).resolve().parents[1]
DEFAULT_ROOTS = ["07_working", "examples/packets", "03_memory/shared_memory"]
PACKET_TYPES = {"task_packet", "memory_packet", "review_packet"}


def load_packets(
    roots: list[Path],
) -> tuple[list[tuple[Path, dict]], list[str]]:
    documents, errors = load_yaml_documents(roots)
    packets = [
        (path, data)
        for path, data in documents
        if isinstance(data, dict)
        and (
            "packet_uid" in data
            or (
                isinstance(data.get("packet_type"), str)
                and data.get("packet_type") in PACKET_TYPES
            )
        )
    ]
    return packets, errors


def looks_like_packet_uid(value: str) -> bool:
    # local uids in this repo are hyphenated tokens ending -vN-NNN or similar;
    # heuristic: contains a hyphen and no path separator or whitespace
    return "-" in value and "/" not in value and " " not in value


def check_packet(path: Path, data: dict, known_uids: set[str], repo: Path) -> list[str]:
    findings = []
    uid = data.get("packet_uid", path.name)

    def check_file_reference(label: str, value: object, missing_message: str) -> None:
        target, error = resolve_repo_reference(repo, value)
        if error:
            findings.append(f"{uid}: invalid {label}: {value!r} ({error})")
        elif target is not None and not target.is_file():
            findings.append(f"{uid}: {missing_message}: {value}")

    source_refs = data.get("source_refs")
    if source_refs is not None and not isinstance(source_refs, list):
        findings.append(f"{uid}: invalid source_refs shape (expected list)")
    elif isinstance(source_refs, list):
        for index, ref in enumerate(source_refs):
            if not isinstance(ref, dict):
                findings.append(f"{uid}: invalid source_refs[{index}] shape (expected object)")
                continue
            sid = ref.get("source_id")
            if sid and looks_like_packet_uid(str(sid)) and str(sid) not in known_uids:
                findings.append(f"{uid}: dangling source_id (no such packet): {sid}")
            if "source_path" in ref and ref["source_path"] is not None:
                check_file_reference(
                    "source_path",
                    ref["source_path"],
                    "dangling source_path (no such file)",
                )

    related_packets = data.get("related_packets")
    if related_packets is not None and not isinstance(related_packets, list):
        findings.append(f"{uid}: invalid related_packets shape (expected list)")
    elif isinstance(related_packets, list):
        for rid in related_packets:
            if looks_like_packet_uid(str(rid)) and str(rid) not in known_uids:
                findings.append(f"{uid}: dangling related_packet (no such packet): {rid}")

    checks = data.get("minimal_checks")
    if checks is not None and not isinstance(checks, dict):
        findings.append(f"{uid}: invalid minimal_checks shape (expected object)")
    elif isinstance(checks, dict):
        must_read = checks.get("must_read")
        if must_read is not None and not isinstance(must_read, list):
            findings.append(f"{uid}: invalid must_read shape (expected list)")
        elif isinstance(must_read, list):
            for ref in must_read:
                check_file_reference(
                    "must_read",
                    ref,
                    "dangling must_read (no such file)",
                )

    snapshot = data.get("promotion_snapshot")
    if snapshot is not None and not isinstance(snapshot, dict):
        findings.append(f"{uid}: invalid promotion_snapshot shape (expected object)")
    elif isinstance(snapshot, dict):
        source_hashes = snapshot.get("source_hashes")
        if source_hashes is not None and not isinstance(source_hashes, list):
            findings.append(f"{uid}: invalid promotion_snapshot.source_hashes shape (expected list)")
        elif isinstance(source_hashes, list):
            for index, entry in enumerate(source_hashes):
                if not isinstance(entry, dict):
                    findings.append(
                        f"{uid}: invalid promotion_snapshot.source_hashes[{index}] "
                        "shape (expected object)"
                    )
                    continue
                if "source_path" in entry and entry["source_path"] is not None:
                    check_file_reference(
                        "promotion_snapshot source_path",
                        entry["source_path"],
                        "dangling promotion_snapshot source_path",
                    )

    return findings


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Check packet reference integrity across the repo.")
    parser.add_argument("--root", action="append", help="search root (repeatable)")
    parser.add_argument("--repo", help="repo root for resolving paths (default: this repo)")
    args = parser.parse_args(argv)

    repo = Path(args.repo).resolve() if args.repo else REPO
    if not repo.is_dir():
        print(f"ERROR: repo root not a directory: {repo}", file=sys.stderr)
        return 2
    roots = [Path(r) if Path(r).is_absolute() else repo / r
             for r in (args.root or DEFAULT_ROOTS)]

    packets, load_errors = load_packets(roots)
    if load_errors:
        for error in load_errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 2

    uid_paths: dict[str, list[Path]] = {}
    findings: list[str] = []
    for path, data in packets:
        packet_type = data.get("packet_type")
        if not isinstance(packet_type, str) or packet_type not in PACKET_TYPES:
            findings.append(
                f"{path}: invalid packet_type {packet_type!r} for packet reference scan"
            )
        raw_uid = data.get("packet_uid")
        if not isinstance(raw_uid, str) or not raw_uid.strip():
            findings.append(f"{path}: invalid packet_uid (expected non-empty string)")
            continue
        uid_paths.setdefault(raw_uid, []).append(path)

    for uid, paths in sorted(uid_paths.items()):
        if len(paths) > 1:
            rendered = ", ".join(str(path) for path in paths)
            findings.append(f"duplicate packet_uid {uid}: {rendered}")

    known_uids = set(uid_paths)

    for path, data in packets:
        findings.extend(check_packet(path, data, known_uids, repo))

    for line in findings:
        print(f"FINDING {line}")
    print(f"checked {len(packets)} packet(s), {len(known_uids)} known uid(s)")
    if findings:
        print(f"{len(findings)} reference-integrity finding(s) "
              f"(advisory; human review decides).")
        return 1
    print("OK no packet reference-integrity findings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
