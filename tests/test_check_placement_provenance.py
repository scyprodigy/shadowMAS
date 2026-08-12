import contextlib
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

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


class PlacementProvenanceScannerTests(unittest.TestCase):
    def run_gate(self, artifact: str, review: str | None = None):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shared = root / "shared_memory"
            reviews = root / "reviews"
            shared.mkdir()
            reviews.mkdir()
            (shared / "memory.v0.yaml").write_text(artifact, encoding="utf-8")
            if review is not None:
                (reviews / "review.v0.yaml").write_text(review, encoding="utf-8")

            stdout = io.StringIO()
            stderr = io.StringIO()
            with (
                patch.object(check_placement_provenance, "SHARED", shared),
                patch.object(check_placement_provenance, "REVIEW_ROOTS", [reviews]),
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(stderr),
            ):
                code = check_placement_provenance.main()
        return code, stdout.getvalue(), stderr.getvalue()

    def test_nonempty_unreviewed_placement_is_rejected(self):
        artifact = """\
packet_type: memory_packet
packet_uid: mem-unreviewed-001
"""
        code, stdout, stderr = self.run_gate(artifact)
        self.assertEqual(code, 1, msg=stdout + stderr)
        self.assertIn("checked 1 shared_memory artifact(s)", stdout)
        self.assertIn("no approved promotion review_packet", stdout)

    def test_nonempty_reviewed_placement_passes(self):
        artifact = """\
packet_type: memory_packet
packet_uid: mem-reviewed-001
"""
        review = """\
packet_type: review_packet
packet_uid: review-placement-001
status: approved
source_refs:
  - source_id: mem-reviewed-001
"""
        code, stdout, stderr = self.run_gate(artifact, review)
        self.assertEqual(code, 0, msg=stdout + stderr)
        self.assertIn(
            "checked 1 shared_memory artifact(s) against 1 approved review packet(s)",
            stdout,
        )


    def test_missing_shared_memory_directory_is_a_setup_error(self):
        """This checker declares itself real enforcement that fails the build.
        An absent provenance root must not be read as an empty one: exit 0
        would mean 'every artifact has provenance' about a directory that was
        never scanned."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            reviews = root / "reviews"
            reviews.mkdir()
            absent = root / "shared_memory"  # deliberately never created

            stdout = io.StringIO()
            stderr = io.StringIO()
            with (
                patch.object(check_placement_provenance, "SHARED", absent),
                patch.object(check_placement_provenance, "REVIEW_ROOTS", [reviews]),
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(stderr),
            ):
                code = check_placement_provenance.main()

        self.assertEqual(code, 2, msg=stdout.getvalue() + stderr.getvalue())
        self.assertTrue(stderr.getvalue().strip(),
                        msg="a setup error must report something on stderr")


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


class ApprovedReviewLoadTests(unittest.TestCase):
    def test_malformed_review_yaml_is_not_silently_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "broken.yaml").write_text("packet_type: [\n", encoding="utf-8")
            with patch.object(check_placement_provenance, "REVIEW_ROOTS", [root]):
                reviews, errors = check_placement_provenance.load_approved_reviews()

        self.assertEqual(reviews, [])
        self.assertTrue(errors)
        self.assertIn("unable to parse YAML file", errors[0])

    def test_duplicate_approved_review_uid_is_a_scan_error(self):
        review = """\
packet_type: review_packet
packet_uid: review-duplicate-001
status: approved
source_refs: []
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "one.yaml").write_text(review, encoding="utf-8")
            (root / "two.yaml").write_text(review, encoding="utf-8")
            with patch.object(check_placement_provenance, "REVIEW_ROOTS", [root]):
                reviews, errors = check_placement_provenance.load_approved_reviews()

        self.assertEqual(len(reviews), 1)
        self.assertTrue(any("duplicate approved review packet_uid" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
