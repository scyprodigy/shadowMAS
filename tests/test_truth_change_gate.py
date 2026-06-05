import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CHECKER = REPO / "tools" / "check_truth_change.py"

REVIEW_PACKET = """\
packet_uid: rp-test-001
packet_type: review_packet
schema_version: v0
created_at: "2026-06-05T00:00:00Z"
created_by: tester
owner: tester
supervision_mode: human_live_pair
risk: r2_guarded
status: ready_for_human
decision_needed: approve truth change
why_you_are_seeing_this: test
change_summary: test
risk_summary: test
recommendation: approve
promotion_snapshot:
  source_hashes:
    - {path: 01_truth/FOO.v0.en.md, hash: abc}
  snapshot_at: "2026-06-05T00:00:00Z"
source_refs:
  - source_type: truth_file
    source_path: 01_truth/FOO.v0.en.md
    relation: reviews
"""


def run(args):
    return subprocess.run([sys.executable, str(CHECKER), *args], capture_output=True, text=True)


class TestTruthChangeGate(unittest.TestCase):
    def test_no_truth_change_ok(self):
        result = run(["--changed", "README.md"])
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_truth_change_without_review_is_finding(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run(["--changed", "01_truth/FOO.v0.en.md", "--reviews-dir", tmp])
            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertIn("MISSING", result.stdout)

    def test_truth_change_with_review_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "rp.yaml").write_text(REVIEW_PACKET, encoding="utf-8")
            result = run(["--changed", "01_truth/FOO.v0.en.md", "--reviews-dir", tmp])
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertIn("covered", result.stdout)


if __name__ == "__main__":
    unittest.main()
