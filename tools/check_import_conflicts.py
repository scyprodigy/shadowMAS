#!/usr/bin/env python3
"""Read-only, advisory comparison of two separate directory trees.

Usage: python3 tools/check_import_conflicts.py SOURCE DESTINATION [--json]
Exit: 0 = inspected without conflicts (duplicates allowed); 1 = conflicts or
portability findings; 2 = incomplete inspection, unsupported input, or setup error.
Exit 2 takes precedence. No copying, renaming, deletion, upload, or reconciliation.

The relative paths are compared as a hypothetical name mapping, never overlaid.
Original names remain in every finding. NFC/casefold and Win32 trailing-dot/space
aliases are diagnostic keys, not replacement names or filesystem equivalence
proofs. Limits are a conservative 255-byte/UTF-16-unit component profile and a
260-unit relative-path warning; destination prefixes and API limits still matter.
See https://www.unicode.org/reports/tr15/ and
https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file .
Case-mixing motivation: https://www.usenix.org/conference/fast23/presentation/basu .

Inspection currently requires 64-bit Linux x86_64, openat2 (Linux 5.6+), and procfs.
Input symlinks (including root ancestors), hard-linked files, nested mounts,
devices, sockets, and FIFOs are refused. openat2 anchors every input lookup to an
opened root with NO_SYMLINKS/BENEATH/NO_XDEV. O_PATH pins objects before deciding
whether to read them. Only verified regular files/directories are reopened via
the tool's own procfs descriptors; input symlink targets are never opened.
See https://man7.org/linux/man-pages/man2/openat2.2.html .

Use quiescent local trees. Recheck both inventories after both scans; observed
file, ancestor, or root-locator changes invalidate affected hashes. These checks
are not an atomic snapshot or a runtime safety guarantee. Byte equality uses
SHA-256 plus size, not authenticated origin or SWHID. ACLs, xattrs, filesystem-
specific collation/short-name aliases, historical checkout losses, archive member
paths, dependency closure, provenance, licensing, and authority are not verified.
No cache or network access. Read operations may update filesystem access times.
Output contains names and hashes: keep it local unless separately authorized.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from contextlib import contextmanager
import ctypes
import errno
from functools import lru_cache
import hashlib
import json
import os
import platform
import re
import stat
import sys
import unicodedata


class InspectionError(Exception):
    pass


class OpenHow(ctypes.Structure):
    _fields_ = [("flags", ctypes.c_uint64), ("mode", ctypes.c_uint64),
                ("resolve", ctypes.c_uint64)]


def platform_supported() -> bool:
    return (sys.platform == "linux" and platform.machine() == "x86_64"
            and ctypes.sizeof(ctypes.c_void_p) == 8 and hasattr(os, "O_PATH"))


@lru_cache(maxsize=1)
def openat2_call():
    """Reuse the process's libc binding; never cache input metadata or content."""
    libc = ctypes.CDLL(None, use_errno=True)
    libc.syscall.restype = ctypes.c_long
    return libc.syscall


@contextmanager
def pinned(path: str, root: int = -100):
    """Pin an input object without activating a device or following a link."""
    if not platform_supported():
        raise InspectionError("unsupported_platform")
    # Linux x86_64 syscall ABI; no guessed syscall number on other platforms.
    resolve = 0x04 if root == -100 else 0x04 | 0x08 | 0x01
    how = OpenHow(os.O_PATH | os.O_NOFOLLOW | os.O_CLOEXEC, 0, resolve)
    fd = openat2_call()(ctypes.c_long(437), ctypes.c_int(root),
                       ctypes.c_char_p(os.fsencode(path)), ctypes.byref(how),
                       ctypes.c_size_t(ctypes.sizeof(how)))
    if fd < 0:
        code = ctypes.get_errno()
        raise OSError(code, errno.errorcode.get(code, "UNKNOWN"))
    try:
        yield fd
    finally:
        os.close(fd)


def fingerprint(info: os.stat_result) -> tuple:
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size,
            info.st_mtime_ns, info.st_ctime_ns, info.st_uid, info.st_gid)


def object_kind(mode: int) -> str:
    for check, name in ((stat.S_ISREG, "file"), (stat.S_ISDIR, "directory"),
                        (stat.S_ISLNK, "symlink"), (stat.S_ISFIFO, "fifo"),
                        (stat.S_ISSOCK, "socket"), (stat.S_ISCHR, "character_device"),
                        (stat.S_ISBLK, "block_device")):
        if check(mode):
            return name
    return "unknown_object"


@contextmanager
def readable(fd: int, expected: os.stat_result):
    """Reopen our pinned inode, never a path supplied by the input tree."""
    if not (stat.S_ISDIR(expected.st_mode) or stat.S_ISREG(expected.st_mode)):
        raise InspectionError("unsupported_object")
    flags = os.O_RDONLY | os.O_CLOEXEC | os.O_NONBLOCK
    if stat.S_ISDIR(expected.st_mode):
        flags |= os.O_DIRECTORY
    actual = os.open(f"/proc/self/fd/{fd}", flags)
    try:
        if fingerprint(os.fstat(actual)) != fingerprint(expected):
            raise InspectionError("changed_during_inspection")
        yield actual
        if fingerprint(os.fstat(actual)) != fingerprint(expected):
            raise InspectionError("changed_during_inspection")
    finally:
        os.close(actual)


def digest_file(fd: int, size: int) -> str:
    digest = hashlib.sha256()
    remaining = size
    while remaining:
        block = os.read(fd, min(1024 * 1024, remaining))
        if not block:
            raise InspectionError("changed_during_inspection")
        remaining -= len(block)
        digest.update(block)
    if os.read(fd, 1):
        raise InspectionError("changed_during_inspection")
    return digest.hexdigest()


def portable_key(path: str) -> str:
    def component(name):
        folded = unicodedata.normalize("NFC", name).casefold()
        return unicodedata.normalize("NFC", folded).rstrip(" .")
    return "/".join(component(part) for part in path.split("/"))


def path_issues(path: str) -> list[str]:
    """Validate relative artifact names, not host root locators."""
    problems = set()
    if path.startswith(("/", "\\")) or re.match(r"^[A-Za-z]:", path):
        problems.add("absolute_or_drive_path")
    if "\\" in path:
        problems.add("separator_ambiguity")
    for part in path.split("/"):
        if part in ("", ".", ".."):
            problems.add("empty_or_traversal_component")
        if any(c in '<>:"\\|?*' or ord(c) < 32 for c in part):
            problems.add("windows_illegal_character")
        stem = part.split(".", 1)[0].rstrip(" ").upper()
        if stem in {"CON", "PRN", "AUX", "NUL"} or re.fullmatch(r"(?:COM|LPT)[1-9¹²³]", stem):
            problems.add("windows_reserved_name")
        if part.endswith((".", " ")):
            problems.add("windows_trailing_dot_or_space")
        if any(unicodedata.category(c) in {"Cs", "Cn"} for c in part):
            problems.add("unverifiable_unicode")
        if len(os.fsencode(part)) > 255 or len(part.encode("utf-16-le", "surrogatepass")) // 2 > 255:
            problems.add("component_length_risk")
    if len(path.encode("utf-16-le", "surrogatepass")) // 2 >= 260:
        problems.add("relative_path_length_risk")
    return sorted(problems)


def locator(entry: dict) -> dict:
    return {key: entry[key] for key in ("tree", "path", "kind")}


def finding(kind: str, entries: list[dict], detail: str, relation: str | None = None) -> dict:
    value = {"kind": kind, "entries": [locator(e) for e in entries], "detail": detail}
    if relation is not None:
        value["content_relation"] = relation
    return value


def content_relation(entries: list[dict]) -> str:
    if not all(e["kind"] == "file" and "sha256" in e for e in entries):
        return "unverified_or_not_regular_files"
    identities = {(e["size"], e["sha256"]) for e in entries}
    return "identical_by_sha256_and_size" if len(identities) == 1 else "divergent"


def scan_tree(root: int, tree: str, findings: list[dict]) -> tuple[list[dict], dict[str, tuple]]:
    entries = []
    observed = {}
    pending = ["."]
    while pending:
        path = pending.pop()
        entry = {"tree": tree, "path": path, "kind": "uninspected"}
        recorded = False
        try:
            with pinned(path, root) as fd:
                before = os.fstat(fd)
                observed[path] = fingerprint(before)
                entry["kind"] = object_kind(before.st_mode)
                if path != ".":
                    entries.append(entry)
                    recorded = True
                    for problem in path_issues(path):
                        kind = "incomplete_inspection" if problem == "unverifiable_unicode" else "path_portability"
                        findings.append(finding(kind, [entry], problem))
                if entry["kind"] not in ("file", "directory") or (entry["kind"] == "file" and before.st_nlink != 1):
                    detail = "hard_link" if entry["kind"] == "file" else entry["kind"]
                    findings.append(finding("unsupported_object", [entry], detail))
                    continue
                with readable(fd, before) as data:
                    if entry["kind"] == "directory":
                        names = sorted(os.listdir(data), reverse=True)
                        pending.extend(name if path == "." else path + "/" + name for name in names)
                    else:
                        entry["size"] = before.st_size
                        entry["mode"] = stat.S_IMODE(before.st_mode)
                        entry["sha256"] = digest_file(data, before.st_size)
        except (OSError, ValueError, InspectionError) as exc:
            entry.pop("sha256", None)
            if path != "." and not recorded:
                entries.append(entry)
            detail = errno.errorcode.get(exc.errno, "io_error") if isinstance(exc, OSError) else str(exc)
            findings.append(finding("incomplete_inspection", [entry], detail))
    return entries, observed


def recheck_tree(root: int, tree: str, entries: list[dict], observed: dict[str, tuple],
                 findings: list[dict]) -> None:
    """Invalidate evidence after both scans, including changed ancestor bindings."""
    by_path = {e["path"]: e for e in entries}
    changed = set()
    for path, expected in sorted(observed.items()):
        try:
            with pinned(path, root) as fd:
                if fingerprint(os.fstat(fd)) != expected:
                    raise InspectionError("changed_during_inspection")
        except (OSError, InspectionError):
            entry = by_path.get(path, {"tree": tree, "path": path, "kind": "directory"})
            changed.add(path)
            findings.append(finding("incomplete_inspection", [entry], "changed_or_unavailable_on_recheck"))
    if changed:
        # Check component ancestors, not all changed-prefix/entry pairs.
        for entry in entries:
            path = entry["path"]
            while True:
                if path in changed:
                    entry.pop("sha256", None)
                    break
                if path == ".":
                    break
                path = path.rpartition("/")[0] or "."


def compare_entries(entries: list[dict]) -> list[dict]:
    findings = []
    exact, aliases, contents = defaultdict(list), defaultdict(list), defaultdict(list)
    for entry in entries:
        exact[entry["path"]].append(entry)
        aliases[portable_key(entry["path"])].append(entry)
        if "sha256" in entry:
            contents[(entry["size"], entry["sha256"])].append(entry)
    for path, group in sorted(exact.items()):
        if len(group) < 2 or all(e["kind"] == "directory" for e in group):
            continue
        relation = content_relation(group)
        if relation == "identical_by_sha256_and_size":
            if len({e["mode"] for e in group}) > 1:
                findings.append(finding("metadata_conflict", group, "same_path_different_mode", relation))
        elif relation == "divergent":
            findings.append(finding("divergent_conflict", group, "same_relative_path", relation))
        elif len({e["kind"] for e in group}) > 1:
            findings.append(finding("object_type_conflict", group, "same_relative_path", relation))
    for alias, group in sorted(aliases.items()):
        if len({e["path"] for e in group}) > 1:
            findings.append(finding("name_portability_collision", group, alias, content_relation(group)))
    for (size, digest), group in sorted(contents.items()):
        if len(group) > 1:
            findings.append(finding("identical_content_duplication", group, "sha256:" + digest,
                                    "identical_by_sha256_and_size"))
    return findings


def inspect(source: str, destination: str) -> dict:
    findings, entries = [], []
    roots = {"source": source, "destination": destination}
    try:
        for value in roots.values():
            if not value or "\0" in value or ".." in value.split("/") or value.startswith("//"):
                raise InspectionError("ambiguous_root_locator")
        roots = {key: os.path.abspath(value) for key, value in roots.items()}
        common = os.path.commonpath(list(roots.values()))
        if common in roots.values():
            raise InspectionError("roots_must_be_separate_and_non_nested")
        with pinned(roots["source"]) as src, pinned(roots["destination"]) as dst:
            for fd in (src, dst):
                if not stat.S_ISDIR(os.fstat(fd).st_mode):
                    raise InspectionError("root_is_not_a_directory_or_is_a_symlink")
            if (os.fstat(src).st_dev, os.fstat(src).st_ino) == (os.fstat(dst).st_dev, os.fstat(dst).st_ino):
                raise InspectionError("roots_alias_same_directory")
            root_start = {"source": fingerprint(os.fstat(src)),
                          "destination": fingerprint(os.fstat(dst))}
            inventories = {}
            for tree, fd in (("source", src), ("destination", dst)):
                inventories[tree] = scan_tree(fd, tree, findings)
                entries.extend(inventories[tree][0])
            for tree, fd in (("source", src), ("destination", dst)):
                recheck_tree(fd, tree, *inventories[tree], findings)
                inventories[tree][1].clear()  # Release fingerprints before comparison indexes are built.
            for tree in roots:
                try:
                    with pinned(roots[tree]) as current:
                        if fingerprint(os.fstat(current)) != root_start[tree]:
                            raise InspectionError("root_changed_during_inspection")
                except (OSError, InspectionError) as exc:
                    for entry in inventories[tree][0]:
                        entry.pop("sha256", None)
                    detail = errno.errorcode.get(exc.errno, "io_error") if isinstance(exc, OSError) else str(exc)
                    root_entry = {"tree": tree, "path": ".", "kind": "directory"}
                    findings.append(finding("incomplete_inspection", [root_entry], detail))
    except (OSError, ValueError, InspectionError) as exc:
        for entry in entries:
            entry.pop("sha256", None)
        detail = errno.errorcode.get(exc.errno, "io_error") if isinstance(exc, OSError) else str(exc)
        findings.append(finding("incomplete_inspection", [], detail))
    entries.sort(key=lambda e: (e["tree"], e["path"]))
    findings.extend(compare_entries(entries))
    findings.sort(key=lambda f: json.dumps(f, sort_keys=True, ensure_ascii=True))
    incomplete = any(f["kind"] in ("incomplete_inspection", "unsupported_object") for f in findings)
    conflicts = any(f["kind"] != "identical_content_duplication" for f in findings)
    return {
        "advisory": True,
        "roots": roots,
        "coverage": {"inspection": "incomplete" if incomplete else "complete",
                     "dependency": "not_assessed", "provenance": "not_assessed",
                     "licensing": "not_assessed",
                     "portability": "diagnostic_profile_only"},
        "profile": {"unicode_version": unicodedata.unidata_version,
                    "alias": "NFC_casefold_NFC_then_trim_Win32_component_suffix",
                    "hash": "sha256_raw_bytes", "backend": "linux_x86_64_openat2_procfs"},
        "limits": ["quiescent_local_trees_required", "not_an_atomic_snapshot",
                   "no_acl_xattr_or_filesystem_collation_verification",
                   "no_archive_or_missing_dependency_inspection",
                   "length_limits_depend_on_target_root_filesystem_and_API",
                   "no_authorization_or_canonical_promotion"],
        "counts": {"entries": len(entries), "hashed_files": sum("sha256" in e for e in entries),
                   "hashed_bytes": sum(e["size"] for e in entries if "sha256" in e)},
        "entries": entries,
        "findings": findings,
        "exit_code": 2 if incomplete else 1 if conflicts else 0,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source", help="Existing selected source root")
    parser.add_argument("destination", help="Existing separate selected destination root")
    parser.add_argument("--json", action="store_true", help="Emit deterministic JSON")
    args = parser.parse_args(argv)
    report = inspect(args.source, args.destination)
    if args.json:
        print(json.dumps(report, ensure_ascii=True, sort_keys=True, indent=2))
    else:
        print("ADVISORY import conflict inspection")
        print("roots: " + json.dumps(report["roots"], ensure_ascii=True, sort_keys=True))
        print("profile: " + json.dumps(report["profile"], sort_keys=True))
        print("coverage: " + json.dumps(report["coverage"], sort_keys=True))
        print("counts: " + json.dumps(report["counts"], sort_keys=True))
        for item in report["findings"]:
            print(json.dumps(item, ensure_ascii=True, sort_keys=True))
        print("limits: " + json.dumps(report["limits"]))
        print(f"exit: {report['exit_code']}")
    return report["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
