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
    # an approved review that reviewed candidate cand-001 (not the placed uid)
    REVIEWS = [
        {
            "packet_type": "review_packet",
            "packet_uid": "review-x-001",
            "status": "approved",
            "source_refs": [{"source_id": "cand-001"}],
            "related_packets": ["cand-001"],
        }
    ]

    def cover(self, uid, via, frm):
        return check_placement_provenance.review_covers(uid, via, frm, self.REVIEWS)

    def test_covered_by_direct_uid(self):
        # the placed artifact's own uid is referenced by the approved review
        self.assertTrue(self.cover("cand-001", None, None))

    def test_covered_by_via_review_when_review_covers_from_packet(self):
        # placed uid differs, but via_review names the review that reviewed
        # the from_packet candidate cand-001
        self.assertTrue(self.cover("placed-001", "review-x-001", "cand-001"))

    def test_forged_via_review_is_rejected(self):
        # via_review points at the approved review, but that review did NOT
        # review this artifact's from_packet (forgery) -> not covered
        self.assertFalse(self.cover("placed-001", "review-x-001", "unrelated-999"))

    def test_via_review_without_from_packet_is_rejected(self):
        # naming an approved review with no from_packet linkage is not enough
        self.assertFalse(self.cover("placed-001", "review-x-001", None))

    def test_uncovered_uid_fails(self):
        self.assertFalse(self.cover("mem-999", None, None))


if __name__ == "__main__":
    unittest.main()
