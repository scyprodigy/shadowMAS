"""External-workspace packet writes preserve identity and product boundaries."""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


REPO = Path(__file__).resolve().parents[1]
WORKSPACE_TOOL = REPO / "05_scripts" / "workspace" / "shadowmas_workspace.py"
PACKET_TOOL = REPO / "05_scripts" / "workspace" / "shadowmas_packet.py"
TASK = REPO / "examples" / "packets" / "task_packet.valid.v0.yaml"
REVIEW = REPO / "examples" / "packets" / "review_packet.valid.v0.yaml"


class WorkspacePacketTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.project = self.root / "product"
        self.project.mkdir()
        self.env = os.environ.copy()
        self.env["SHADOWMAS_DATA_HOME"] = str(self.root / "shadowmas-data")
        self.env["PYTHONDONTWRITEBYTECODE"] = "1"
        init = self.run_command(WORKSPACE_TOOL, "init", "--project", str(self.project))
        self.assertEqual(init.returncode, 0, init.stderr)
        self.workspace = Path(init.stdout.strip())

    def run_command(self, tool, *args):
        return subprocess.run(
            [sys.executable, str(tool), *args],
            cwd=REPO, env=self.env, capture_output=True, text=True,
        )

    def draft(self, fixture, name="draft.yaml", *, uid=None, omit_uid=False):
        source = fixture.read_text(encoding="utf-8")
        original_uid = yaml.safe_load(source)["packet_uid"]
        if omit_uid:
            source = source.replace(f"packet_uid: {original_uid}\n", "", 1)
        elif uid is not None:
            source = source.replace(original_uid, uid, 1)
        path = self.root / name
        path.write_text(source, encoding="utf-8")
        return path

    def write(self, source):
        return self.run_command(
            PACKET_TOOL, "write", "--project", str(self.project),
            "--input", str(source),
        )

    def test_write_uses_type_uid_and_version_without_touching_product(self):
        draft = self.draft(TASK)
        result = self.write(draft)
        self.assertEqual(result.returncode, 0, result.stderr)
        destination = self.workspace / "packets" / (
            "task_packet.example-task-packet-valid-v0-001.v0.yaml")
        self.assertEqual(Path(result.stdout.strip()), destination)
        self.assertEqual(destination.read_text(encoding="utf-8"),
                         draft.read_text(encoding="utf-8"))
        self.assertEqual(list(self.project.iterdir()), [])

        second = self.write(draft)
        self.assertEqual(second.returncode, 1)
        self.assertIn("packet_uid already exists", second.stderr)
        self.assertEqual(len(list((self.workspace / "packets").iterdir())), 1)

    def test_missing_uid_is_assigned_and_review_goes_to_reviews(self):
        draft = self.draft(REVIEW, omit_uid=True)
        result = self.write(draft)
        self.assertEqual(result.returncode, 0, result.stderr)
        destination = Path(result.stdout.strip())
        self.assertEqual(destination.parent, self.workspace / "reviews")
        data = yaml.safe_load(destination.read_text(encoding="utf-8"))
        self.assertEqual(destination.name,
                         f"review_packet.{data['packet_uid']}.v0.yaml")
        self.assertEqual(data["packet_type"], "review_packet")
        self.assertIn("# This is a non-canonical illustrative example.",
                      destination.read_text(encoding="utf-8"))

    def test_legacy_name_remains_readable_but_duplicate_uid_is_refused(self):
        legacy = self.workspace / "packets" / "old-agent-name.task.yml"
        legacy.write_text(TASK.read_text(encoding="utf-8"), encoding="utf-8")
        duplicate = self.write(self.draft(TASK))
        self.assertEqual(duplicate.returncode, 1)
        self.assertIn("packet_uid already exists", duplicate.stderr)
        self.assertTrue(legacy.is_file())

        new = self.write(self.draft(TASK, "new.yaml", uid="new-task-001"))
        self.assertEqual(new.returncode, 0, new.stderr)
        self.assertTrue(legacy.is_file())

    def test_invalid_packet_and_unsafe_uid_are_refused(self):
        invalid = self.draft(TASK)
        invalid.write_text(
            invalid.read_text(encoding="utf-8").replace("status: draft", "status: ready_after_dependency"),
            encoding="utf-8",
        )
        result = self.write(invalid)
        self.assertEqual(result.returncode, 1)
        self.assertIn("INVALID_STATUS", result.stderr)

        unsafe = self.write(self.draft(TASK, "unsafe.yaml", uid="name/with/slash"))
        self.assertEqual(unsafe.returncode, 2)
        self.assertIn("packet_uid must be", unsafe.stderr)
        self.assertEqual(list((self.workspace / "packets").iterdir()), [])

    def test_destination_symlink_into_product_is_refused(self):
        packets = self.workspace / "packets"
        packets.rmdir()
        try:
            packets.symlink_to(self.project, target_is_directory=True)
        except OSError as exc:
            self.skipTest(f"directory symlink unavailable: {exc}")
        result = self.write(self.draft(TASK))
        self.assertEqual(result.returncode, 2)
        self.assertIn("symlink", result.stderr)
        self.assertEqual(list(self.project.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
