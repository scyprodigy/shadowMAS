import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ANCHOR_CHECKER = REPO_ROOT / "tools" / "check_anchor_drift.py"
INDEX_BUILDER = REPO_ROOT / "tools" / "build_rationale_index.py"

sys.path.insert(0, str(REPO_ROOT / "tools"))

import check_anchor_drift  # noqa: E402


class AnchorDriftCurrentStateTests(unittest.TestCase):
    def test_no_anchor_drift_on_current_state(self):
        """Landing files must not drift from canonical anchors at HEAD."""
        result = subprocess.run(
            [sys.executable, str(ANCHOR_CHECKER)],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        )
        self.assertEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertIn("OK", result.stdout)


class AnchorDriftUnitTests(unittest.TestCase):
    def test_count_claim_mismatch_detected(self):
        lines = [
            "shadowMAS exists to reduce five recurring failure modes:",
            "",
            "- a",
            "- b",
            "- c",
        ]
        self.assertEqual(check_anchor_drift.bullets_after(lines, 0), 3)

    def test_bullets_stop_at_non_bullet(self):
        lines = [
            "reduce two failure modes:",
            "- a",
            "- b",
            "prose resumes here",
            "- not counted",
        ]
        self.assertEqual(check_anchor_drift.bullets_after(lines, 0), 2)

    def test_intake_pack_extracted_from_owner(self):
        pack = check_anchor_drift.intake_pack_paths()
        self.assertGreaterEqual(len(pack), 3)
        self.assertTrue(any("SHADOWMAS-CURRENT-TRUTH" in p for p in pack))


class ReworkGuardCompiledTests(unittest.TestCase):
    def test_do_not_redo_surface_is_up_to_date(self):
        """00_entry/DO-NOT-REDO.compiled.v0.en.md must match its compiled form at HEAD."""
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "tools" / "build_rework_guard.py"), "--check"],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        )
        self.assertEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )


class RationaleIndexCompiledTests(unittest.TestCase):
    def test_index_is_up_to_date(self):
        """rationale_index.md must match its compiled form at HEAD."""
        result = subprocess.run(
            [sys.executable, str(INDEX_BUILDER), "--check"],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        )
        self.assertEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )


if __name__ == "__main__":
    unittest.main()
