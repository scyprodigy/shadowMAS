import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPO_ROOT / "tools" / "check_packet_refs.py"

TASK = """\
packet_type: task_packet
packet_uid: t-real-001
"""

REVIEW_CLEAN = """\
packet_type: review_packet
packet_uid: r-clean-001
source_refs:
  - source_type: task_packet
    source_id: t-real-001
    relation: reviews
  - source_type: file
    source_path: evidence.md
    relation: derived_from
related_packets:
  - t-real-001
minimal_checks:
  must_read:
    - evidence.md
"""

REVIEW_DANGLING = """\
packet_type: review_packet
packet_uid: r-bad-001
source_refs:
  - source_type: task_packet
    source_id: t-ghost-999
    relation: reviews
  - source_type: file
    source_path: gone/missing.md
    relation: derived_from
related_packets:
  - t-ghost-999
"""


class PacketRefsCurrentStateTests(unittest.TestCase):
    def test_current_repo_has_no_dangling_refs(self):
        """Every committed packet's reference edges must resolve at HEAD."""
        result = subprocess.run(
            [sys.executable, str(TOOL)],
            capture_output=True, text=True, cwd=REPO_ROOT,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("OK", result.stdout)


class PacketRefsUnitTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        (self.repo / "packets").mkdir()
        (self.repo / "evidence.md").write_text("evidence\n", encoding="utf-8")
        (self.repo / "packets" / "task.yaml").write_text(TASK, encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def run_tool(self):
        return subprocess.run(
            [sys.executable, str(TOOL), "--repo", str(self.repo), "--root", "packets"],
            capture_output=True, text=True,
        )

    def test_clean_references_pass(self):
        (self.repo / "packets" / "review.yaml").write_text(REVIEW_CLEAN, encoding="utf-8")
        result = self.run_tool()
        self.assertEqual(result.returncode, 0, msg=result.stdout)

    def test_dangling_id_path_and_related_are_found(self):
        (self.repo / "packets" / "review.yaml").write_text(REVIEW_DANGLING, encoding="utf-8")
        result = self.run_tool()
        self.assertEqual(result.returncode, 1, msg=result.stdout)
        self.assertIn("dangling source_id (no such packet): t-ghost-999", result.stdout)
        self.assertIn("dangling source_path (no such file): gone/missing.md", result.stdout)
        self.assertIn("dangling related_packet (no such packet): t-ghost-999", result.stdout)

    def test_malformed_yaml_is_a_setup_error_not_a_silent_skip(self):
        (self.repo / "packets" / "broken.yaml").write_text(
            "packet_type: [\n", encoding="utf-8"
        )

        result = self.run_tool()

        self.assertEqual(result.returncode, 2, msg=result.stdout + result.stderr)
        self.assertIn("unable to parse YAML file", result.stderr)

    def test_duplicate_packet_uid_is_an_integrity_finding(self):
        (self.repo / "packets" / "duplicate.yaml").write_text(TASK, encoding="utf-8")

        result = self.run_tool()

        self.assertEqual(result.returncode, 1, msg=result.stdout + result.stderr)
        self.assertIn("duplicate packet_uid t-real-001", result.stdout)

    def test_packet_family_document_without_uid_is_a_finding(self):
        (self.repo / "packets" / "missing-uid.yaml").write_text(
            "packet_type: task_packet\n", encoding="utf-8"
        )

        result = self.run_tool()

        self.assertEqual(result.returncode, 1, msg=result.stdout + result.stderr)
        self.assertIn("invalid packet_uid", result.stdout)

    def test_repository_path_escape_is_rejected_without_following_it(self):
        review = """\
packet_type: review_packet
packet_uid: r-escape-001
source_refs:
  - source_type: file
    source_path: ../outside.md
    relation: derived_from
"""
        (self.repo / "packets" / "escape.yaml").write_text(review, encoding="utf-8")

        result = self.run_tool()

        self.assertEqual(result.returncode, 1, msg=result.stdout + result.stderr)
        self.assertIn("invalid source_path", result.stdout)
        self.assertIn("parent traversal is not allowed", result.stdout)


if __name__ == "__main__":
    unittest.main()
