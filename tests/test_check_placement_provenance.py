import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPO_ROOT / "tools" / "check_placement_provenance.py"

sys.path.insert(0, str(REPO_ROOT / "tools"))

import check_placement_provenance  # noqa: E402


class PlacementProvenanceCurrentStateTests(unittest.TestCase):
    def test_current_repo_passes(self):
        """shared_memory is empty after the withdrawal; the gate must pass."""
        result = subprocess.run(
            [sys.executable, str(TOOL)],
            capture_output=True, text=True, cwd=REPO_ROOT,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("OK", result.stdout)


class ReviewCoversUnitTests(unittest.TestCase):
    REVIEWS = [
        {
            "packet_type": "review_packet",
            "packet_uid": "review-x-001",
            "status": "approved",
            "source_refs": [{"source_id": "mem-001"}],
            "related_packets": ["mem-001"],
        }
    ]

    def test_covered_by_source_id(self):
        self.assertTrue(check_placement_provenance.review_covers("mem-001", None, self.REVIEWS))

    def test_covered_by_via_review(self):
        self.assertTrue(
            check_placement_provenance.review_covers("other", "review-x-001", self.REVIEWS))

    def test_uncovered_uid_fails(self):
        self.assertFalse(check_placement_provenance.review_covers("mem-999", None, self.REVIEWS))

    def test_closed_review_does_not_count(self):
        # load_approved_reviews only collects status == approved, so a closed
        # (withdrawn) review is never passed in; an artifact relying on it is uncovered
        closed = [dict(self.REVIEWS[0], status="closed")]
        approved_only = [r for r in closed if r["status"] == "approved"]
        self.assertFalse(
            check_placement_provenance.review_covers("mem-001", None, approved_only))


if __name__ == "__main__":
    unittest.main()
