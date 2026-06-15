import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPO_ROOT / "tools" / "trace_packet_chain.py"

TASK = """\
packet_type: task_packet
packet_uid: t-001
status: done
"""

REVIEW = """\
packet_type: review_packet
packet_uid: r-001
status: approved
source_refs:
  - source_type: task_packet
    source_id: t-001
    relation: reviews
  - source_type: file
    source_path: evidence.md
    relation: derived_from
related_packets:
  - t-001
"""


class TracePacketChainTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        (self.repo / "packets").mkdir()
        (self.repo / "packets" / "task.yaml").write_text(TASK, encoding="utf-8")
        (self.repo / "packets" / "review.yaml").write_text(REVIEW, encoding="utf-8")
        (self.repo / "evidence.md").write_text("evidence\n", encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def run_tool(self, uid: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(TOOL), uid, "--repo", str(self.repo), "--root", "packets"],
            capture_output=True,
            text=True,
        )

    def test_inbound_reference_is_reconstructed(self):
        result = self.run_tool("t-001")
        self.assertEqual(result.returncode, 0, msg=result.stdout)
        self.assertIn("<- r-001", result.stdout)

    def test_outbound_and_evidence_files_listed(self):
        result = self.run_tool("r-001")
        self.assertEqual(result.returncode, 0, msg=result.stdout)
        self.assertIn("-> t-001", result.stdout)
        self.assertIn("[ok] evidence.md", result.stdout)

    def test_missing_evidence_file_marked(self):
        (self.repo / "evidence.md").unlink()
        result = self.run_tool("r-001")
        self.assertIn("[MISSING] evidence.md", result.stdout)

    def test_unknown_uid_exits_one(self):
        result = self.run_tool("nope-999")
        self.assertEqual(result.returncode, 1)
        self.assertIn("NOT FOUND", result.stdout)


if __name__ == "__main__":
    unittest.main()
