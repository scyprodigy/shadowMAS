import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPO_ROOT / "tools" / "order_review_queue.py"

REVIEW_TEMPLATE = """\
packet_type: review_packet
packet_uid: {uid}
risk: {risk}
status: {status}
decision_needed: decide something
minimal_checks:
  must_read:
    - {must_read}
"""


class OrderReviewQueueTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        (self.repo / "queue").mkdir()
        (self.repo / "doc.md").write_text("word " * 50, encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def write_packet(self, name: str, uid: str, risk: str,
                     status: str = "ready_for_human", must_read: str = "doc.md"):
        (self.repo / "queue" / name).write_text(
            REVIEW_TEMPLATE.format(uid=uid, risk=risk, status=status, must_read=must_read),
            encoding="utf-8",
        )

    def run_tool(self, *extra: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(TOOL), "--repo", str(self.repo), "--root", "queue", *extra],
            capture_output=True,
            text=True,
        )

    def test_high_risk_ordered_before_low_risk_batch(self):
        self.write_packet("low.yaml", "uid-low", "r1_routine")
        self.write_packet("high.yaml", "uid-high", "r3_sensitive")
        result = self.run_tool()
        self.assertEqual(result.returncode, 0, msg=result.stdout)
        self.assertLess(result.stdout.index("uid-high"), result.stdout.index("uid-low"))
        self.assertIn("REVIEW FIRST", result.stdout)
        self.assertIn("BATCH TOGETHER", result.stdout)

    def test_non_pending_status_excluded_by_default(self):
        self.write_packet("closed.yaml", "uid-closed", "r2_guarded", status="approved")
        result = self.run_tool()
        self.assertEqual(result.returncode, 0, msg=result.stdout)
        self.assertIn("nothing pending", result.stdout)
        result_all = self.run_tool("--all-statuses")
        self.assertIn("uid-closed", result_all.stdout)

    def test_missing_must_read_is_warned_not_fatal(self):
        self.write_packet("gone.yaml", "uid-gone", "r2_guarded", must_read="missing.md")
        result = self.run_tool()
        self.assertEqual(result.returncode, 0, msg=result.stdout)
        self.assertIn("WARNING must_read missing: missing.md", result.stdout)


if __name__ == "__main__":
    unittest.main()
