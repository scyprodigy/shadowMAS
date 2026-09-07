"""Temporary-tree checks for the advisory import conflict inspector."""

from contextlib import contextmanager
import errno
import hashlib
import json
import os
from pathlib import Path
import socket
import stat
import subprocess
import sys
import tempfile
import time
from types import SimpleNamespace
import unittest
from unittest import mock

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools"))
import check_import_conflicts as checker


def snapshot(root):
    """Independent byte/object inventory; never open fixture symlink targets."""
    rows = []
    pending = [root]
    while pending:
        current = pending.pop()
        info = current.lstat()
        relative = str(current.relative_to(root))
        value = None
        if stat.S_ISREG(info.st_mode):
            value = hashlib.sha256(current.read_bytes()).hexdigest()
        elif stat.S_ISLNK(info.st_mode):
            value = os.readlink(current)
        elif stat.S_ISDIR(info.st_mode):
            pending.extend(current.iterdir())
        rows.append((relative, info.st_mode, info.st_nlink, info.st_rdev, value))
    return sorted(rows)


@unittest.skipUnless(checker.platform_supported(), "inspection backend requires Linux x86_64")
class ImportConflictTests(unittest.TestCase):
    def setUp(self):
        # Explicitly outside the repository, independent of TMPDIR configuration.
        self.temp = tempfile.TemporaryDirectory(prefix="shadowmas-import-", dir="/tmp")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source, self.destination = self.root / "source", self.root / "destination"
        self.source.mkdir()
        self.destination.mkdir()

    def write(self, tree, path, data=b"content"):
        target = tree / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        return target

    def inspect(self, source=None, destination=None):
        before = (snapshot(self.source), snapshot(self.destination))
        try:
            return checker.inspect(str(source or self.source), str(destination or self.destination))
        finally:
            self.assertEqual(before, (snapshot(self.source), snapshot(self.destination)))

    def kinds(self, report):
        return {item["kind"] for item in report["findings"]}

    @contextmanager
    def changed_after_destination_scan(self, path):
        """Model later metadata drift while preserving all fixture bytes."""
        info = path.stat()
        real_scan, real_fstat = checker.scan_tree, os.fstat
        destination_scanned = False

        def scan(root, tree, findings):
            nonlocal destination_scanned
            result = real_scan(root, tree, findings)
            if tree == "destination":
                destination_scanned = True
            return result

        def fstat(fd):
            value = real_fstat(fd)
            if not destination_scanned or (value.st_dev, value.st_ino) != (info.st_dev, info.st_ino):
                return value
            changed = SimpleNamespace(**{name: getattr(value, name) for name in
                                      ("st_dev", "st_ino", "st_mode", "st_nlink", "st_size",
                                       "st_mtime_ns", "st_ctime_ns", "st_uid", "st_gid")})
            changed.st_ctime_ns += 1
            return changed

        with mock.patch.object(checker, "scan_tree", scan), mock.patch.object(checker.os, "fstat", fstat):
            yield

    def cli(self, *args, expected=0):
        before = (snapshot(self.source), snapshot(self.destination))
        result = subprocess.run([sys.executable, str(REPO / "tools/check_import_conflicts.py"),
                                 str(self.source), str(self.destination), *args],
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(before, (snapshot(self.source), snapshot(self.destination)))
        self.assertEqual(result.returncode, expected, result.stderr + result.stdout)
        return result

    def test_empty_tree_and_exit_zero(self):
        report = self.inspect()
        self.assertEqual(report["exit_code"], 0)
        self.assertEqual(report["counts"]["entries"], 0)
        self.assertEqual(report["coverage"]["dependency"], "not_assessed")
        self.assertEqual(json.loads(self.cli("--json").stdout), report)

    def test_case_collision_within_source(self):
        self.write(self.source, "Foo", b"A")
        self.write(self.source, "foo", b"B")
        report = self.inspect()
        collision = next(f for f in report["findings"] if f["kind"] == "name_portability_collision")
        self.assertEqual(collision["content_relation"], "divergent")
        self.assertEqual({e["path"] for e in collision["entries"]}, {"Foo", "foo"})
        self.cli(expected=1)

    def test_parent_directory_case_collision_across_trees(self):
        self.write(self.source, "Foo/one")
        self.write(self.destination, "foo/two", b"different")
        report = self.inspect()
        self.assertIn("name_portability_collision", self.kinds(report))
        self.assertEqual(report["exit_code"], 1)

    def test_composed_and_decomposed_unicode_preserve_names(self):
        names = ("caf\u00e9.md", "cafe\u0301.md")
        self.write(self.source, names[0])
        self.write(self.destination, names[1])
        report = self.inspect()
        self.assertIn("name_portability_collision", self.kinds(report))
        self.assertIn("identical_content_duplication", self.kinds(report))
        self.assertEqual({e["path"] for e in report["entries"]}, set(names))

    def test_windows_reserved_and_trailing_aliases(self):
        for name in ("NUL.txt", "COM¹.log", "AUX", "report", "report. "):
            self.write(self.source, name)
        report = self.inspect()
        self.assertIn("path_portability", self.kinds(report))
        self.assertIn("name_portability_collision", self.kinds(report))
        self.assertIn("windows_reserved_name", {f["detail"] for f in report["findings"]})

    def test_exact_identical_and_divergent_content(self):
        self.write(self.source, "same", b"yes")
        self.write(self.destination, "same", b"yes")
        self.write(self.source, "changed", b"left")
        self.write(self.destination, "changed", b"right")
        report = self.inspect()
        self.assertEqual(report["exit_code"], 1)
        self.assertEqual(self.kinds(report), {"identical_content_duplication", "divergent_conflict"})

    def test_exact_identical_empty_files_are_nonblocking(self):
        self.write(self.source, "same", b"")
        self.write(self.destination, "same", b"")
        report = self.inspect()
        self.assertEqual(report["exit_code"], 0)
        self.assertEqual(self.kinds(report), {"identical_content_duplication"})
        self.assertEqual(report["entries"][0]["sha256"], hashlib.sha256(b"").hexdigest())

    def test_same_content_has_multiple_legitimate_locators(self):
        self.write(self.source, "one/original name.txt")
        self.write(self.source, "two/複本.txt")
        self.write(self.destination, "reference.txt")
        report = self.inspect()
        self.assertEqual(report["exit_code"], 0)
        duplicates = next(f for f in report["findings"] if f["kind"] == "identical_content_duplication")
        self.assertEqual(len(duplicates["entries"]), 3)

    def test_symlinks_inside_and_escaping_are_never_opened(self):
        self.write(self.source, "ordinary")
        outside = self.write(self.root, "outside", b"outside must not be hashed")
        (self.source / "inside_link").symlink_to("ordinary")
        (self.source / "escape_link").symlink_to(outside)
        (self.source / "escape_dir").symlink_to(self.root, target_is_directory=True)
        outside_before = outside.read_bytes()
        report = self.inspect()
        self.assertEqual(report["exit_code"], 2)
        self.assertEqual(report["counts"]["hashed_files"], 1)
        self.assertEqual(sum(e["kind"] == "symlink" for e in report["entries"]), 3)
        self.assertEqual(outside_before, outside.read_bytes())

    def test_root_and_ancestor_symlinks_refused(self):
        alias = self.root / "alias"
        alias.symlink_to(self.source, target_is_directory=True)
        report = self.inspect(source=alias)
        self.assertEqual(report["exit_code"], 2)
        nested = self.source / "nested"
        nested.mkdir()
        report = self.inspect(source=alias / "nested")
        self.assertEqual(report["exit_code"], 2)
        self.assertEqual(report["counts"]["hashed_files"], 0)

    def test_hard_links_refused_even_when_alias_is_outside(self):
        outside = self.write(self.root, "outside")
        os.link(outside, self.source / "linked")
        report = self.inspect()
        self.assertEqual(report["exit_code"], 2)
        self.assertEqual(report["counts"]["hashed_files"], 0)
        self.assertIn("hard_link", {f["detail"] for f in report["findings"]})

    def test_directory_regular_file_fifo_and_socket(self):
        (self.source / "empty directory").mkdir()
        self.write(self.source, "普通 文件.txt")
        os.mkfifo(self.source / "pipe")
        sock = socket.socket(socket.AF_UNIX)
        self.addCleanup(sock.close)
        sock.bind(str(self.destination / "socket"))
        report = self.inspect()
        self.assertEqual(report["exit_code"], 2)
        self.assertEqual({e["kind"] for e in report["entries"]}, {"file", "directory", "fifo", "socket"})
        self.cli("--json", expected=2)

    def test_devices_classified_without_opening_them(self):
        # Never create or activate a real device. Feed device metadata at the
        # classification boundary and assert the content-open helper is unused.
        self.write(self.source, "device_placeholder")
        real_fstat = os.fstat
        info = (self.source / "device_placeholder").stat()
        for mode, expected in ((stat.S_IFCHR, "character_device"), (stat.S_IFBLK, "block_device")):
            fake = mock.Mock(wraps=info)
            for attr in ("st_dev", "st_ino", "st_nlink", "st_size", "st_mtime_ns", "st_ctime_ns", "st_uid", "st_gid"):
                setattr(fake, attr, getattr(info, attr))
            fake.st_mode = mode | 0o600
            def fstat(fd):
                value = real_fstat(fd)
                return fake if value.st_ino == info.st_ino and value.st_dev == info.st_dev else value
            real_readable = checker.readable
            @contextmanager
            def guarded(fd, metadata):
                self.assertTrue(stat.S_ISDIR(metadata.st_mode))
                with real_readable(fd, metadata) as data:
                    yield data
            with mock.patch.object(checker.os, "fstat", side_effect=fstat), mock.patch.object(checker, "readable", guarded):
                report = self.inspect()
            self.assertEqual(report["exit_code"], 2)
            self.assertIn(expected, {e["kind"] for e in report["entries"]})

    def test_file_directory_conflict(self):
        self.write(self.source, "item")
        self.write(self.destination, "item/child")
        self.assertIn("object_type_conflict", self.kinds(self.inspect()))

    def test_mode_conflict_is_not_hidden_by_identical_bytes(self):
        self.write(self.source, "script").chmod(0o600)
        self.write(self.destination, "script").chmod(0o700)
        self.assertIn("metadata_conflict", self.kinds(self.inspect()))

    def test_deterministic_order_text_and_json(self):
        for name in ("z", "é", "文 書", "A", "a"):
            self.write(self.source, name)
        first = self.cli("--json", expected=1).stdout
        self.assertEqual(first, self.cli("--json", expected=1).stdout)
        self.assertEqual(self.cli(expected=1).stdout, self.cli(expected=1).stdout)
        entries = json.loads(first)["entries"]
        self.assertEqual(entries, sorted(entries, key=lambda e: (e["tree"], e["path"])))

    def test_control_characters_are_escaped_in_text(self):
        self.write(self.source, "escape\x1b[31m\nname")
        output = self.cli(expected=1).stdout
        self.assertNotIn("\x1b", output)
        self.assertIn("\\u001b", output)
        self.assertIn("\\nname", output)

    def test_missing_nested_identical_and_ambiguous_roots(self):
        for src, dst in ((self.root / "missing", self.destination),
                         (self.source, self.source), (self.source, self.source / "nested"),
                         (str(self.source) + "/../source", self.destination)):
            report = self.inspect(src, dst)
            self.assertEqual(report["exit_code"], 2)

    def test_unreadable_or_mount_input_is_incomplete(self):
        self.write(self.source, "blocked")
        real_pinned = checker.pinned
        for error in (errno.EACCES, errno.EXDEV, errno.ENOENT):
            @contextmanager
            def fail(path, root=-100):
                if path == "blocked":
                    raise OSError(error, "injected inspection failure")
                with real_pinned(path, root) as fd:
                    yield fd
            with mock.patch.object(checker, "pinned", fail):
                report = self.inspect()
            self.assertEqual(report["coverage"]["inspection"], "incomplete")
            self.assertEqual(report["exit_code"], 2)

    def test_observed_content_change_discards_hash(self):
        self.write(self.source, "changed")
        # Model a racing read without modifying either fixture tree.
        with mock.patch.object(checker, "digest_file", side_effect=checker.InspectionError("changed_during_inspection")):
            report = self.inspect()
        self.assertEqual(report["exit_code"], 2)
        self.assertEqual(report["counts"]["hashed_files"], 0)

    def test_metadata_change_after_read_invalidates_digest(self):
        info = self.write(self.source, "observed").stat()
        real_fstat = os.fstat
        calls = 0
        def changed(fd):
            nonlocal calls
            value = real_fstat(fd)
            if (value.st_dev, value.st_ino) != (info.st_dev, info.st_ino):
                return value
            calls += 1
            if calls < 3:
                return value
            result = SimpleNamespace(**{name: getattr(value, name) for name in
                                      ("st_dev", "st_ino", "st_mode", "st_nlink", "st_size",
                                       "st_mtime_ns", "st_ctime_ns", "st_uid", "st_gid")})
            result.st_ctime_ns += 1
            return result
        with mock.patch.object(checker.os, "fstat", side_effect=changed):
            report = self.inspect()
        self.assertEqual(report["exit_code"], 2)
        self.assertEqual(report["counts"]["hashed_files"], 0)

    def test_missing_procfs_is_incomplete(self):
        self.write(self.source, "file")
        real_open = os.open
        def unavailable(path, *args, **kwargs):
            if str(path).startswith("/proc/self/fd/"):
                raise FileNotFoundError(errno.ENOENT, "procfs unavailable")
            return real_open(path, *args, **kwargs)
        with mock.patch.object(checker.os, "open", side_effect=unavailable):
            report = self.inspect()
        self.assertEqual(report["exit_code"], 2)
        self.assertEqual(report["counts"]["hashed_files"], 0)

    def test_source_change_after_destination_scan_invalidates_comparison(self):
        changed = self.write(self.source, "same")
        self.write(self.destination, "same")
        with self.changed_after_destination_scan(changed):
            report = self.inspect()
        self.assertEqual(report["coverage"]["inspection"], "incomplete")
        self.assertEqual(report["exit_code"], 2)
        self.assertNotIn("identical_content_duplication", self.kinds(report))
        self.assertEqual([e["tree"] for e in report["entries"] if "sha256" in e], ["destination"])

    def test_directory_change_invalidates_descendants_not_similar_prefixes(self):
        self.write(self.source, "group/child")
        self.write(self.source, "group2/child", b"unrelated")
        self.write(self.destination, "group/child")
        with self.changed_after_destination_scan(self.source / "group"):
            report = self.inspect()
        self.assertEqual(report["exit_code"], 2)
        self.assertNotIn("identical_content_duplication", self.kinds(report))
        retained = {(e["tree"], e["path"]) for e in report["entries"] if "sha256" in e}
        self.assertEqual(retained, {("source", "group2/child"), ("destination", "group/child")})

    def test_changed_root_discards_only_affected_tree_hashes(self):
        self.write(self.source, "same")
        self.write(self.destination, "same")
        for changed in (self.source, self.destination):
            with self.subTest(tree=changed.name), self.changed_after_destination_scan(changed):
                report = self.inspect()
            self.assertEqual(report["exit_code"], 2)
            self.assertNotIn("identical_content_duplication", self.kinds(report))
            retained = [e["tree"] for e in report["entries"] if "sha256" in e]
            self.assertEqual(retained, ["destination" if changed == self.source else "source"])

    def test_unavailable_root_locator_invalidates_hashes_and_checks_other_root(self):
        self.write(self.source, "same")
        self.write(self.destination, "same")
        real_pinned = checker.pinned
        openings = {str(self.source): 0, str(self.destination): 0}

        @contextmanager
        def unavailable(path, root=-100):
            if root == -100 and path in openings:
                openings[path] += 1
                if path == str(self.source) and openings[path] == 2:
                    raise FileNotFoundError(errno.ENOENT, "injected root locator loss")
            with real_pinned(path, root) as fd:
                yield fd

        with mock.patch.object(checker, "pinned", unavailable):
            report = self.inspect()
        self.assertEqual(report["exit_code"], 2)
        self.assertEqual(openings[str(self.destination)], 2)
        self.assertNotIn("identical_content_duplication", self.kinds(report))
        self.assertEqual([e["tree"] for e in report["entries"] if "sha256" in e], ["destination"])

    def test_incomplete_takes_precedence_over_conflicts(self):
        self.write(self.source, "Foo", b"left")
        self.write(self.destination, "foo", b"right")
        os.mkfifo(self.source / "pipe")
        report = self.inspect()
        self.assertIn("name_portability_collision", self.kinds(report))
        self.assertEqual(report["exit_code"], 2)

    def test_unverifiable_filename_bytes(self):
        path = os.fsencode(self.source) + b"/invalid_\xff"
        with open(path, "wb") as stream:
            stream.write(b"bytes")
        report = self.inspect()
        self.assertEqual(report["exit_code"], 2)
        serialized = json.loads(json.dumps(report))
        self.assertEqual(os.fsencode(serialized["entries"][0]["path"]), b"invalid_\xff")

    def test_large_synthetic_tree_measured_without_time_gate(self):
        for number in range(10000):
            self.write(self.source, f"group_{number // 100:03}/file_{number:05}.txt", f"entry {number}\n".encode())
        start = time.perf_counter()
        report = self.inspect()
        elapsed = time.perf_counter() - start
        self.assertEqual(report["exit_code"], 0)
        self.assertEqual(report["counts"]["hashed_files"], 10000)
        print(f"import preflight synthetic: 10000 files, {report['counts']['hashed_bytes']} bytes, "
              f"{elapsed:.3f}s including independent before/after inventories; no timing threshold")


class PortablePathTests(unittest.TestCase):
    def test_absolute_traversal_and_separator_forms(self):
        for path in ("/absolute", "C:drive_relative", "C:/absolute", "\\\\server\\share", "../up", "a/../b", "a//b", "a\\..\\b"):
            self.assertTrue(checker.path_issues(path), path)

    def test_length_diagnostics_and_valid_unicode_spaces(self):
        self.assertIn("component_length_risk", checker.path_issues("x" * 256))
        self.assertIn("relative_path_length_risk", checker.path_issues("segment/" * 40 + "file"))
        self.assertEqual(checker.path_issues("資料/with spaces.txt"), [])

    def test_unsupported_platform_fails_closed(self):
        with mock.patch.object(checker, "platform_supported", return_value=False):
            report = checker.inspect("/selected/source", "/selected/destination")
        self.assertEqual(report["exit_code"], 2)
        self.assertEqual(report["counts"]["entries"], 0)


if __name__ == "__main__":
    unittest.main()
