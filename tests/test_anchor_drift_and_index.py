import contextlib
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[1]
ANCHOR_CHECKER = REPO_ROOT / "tools" / "check_anchor_drift.py"
INDEX_BUILDER = REPO_ROOT / "tools" / "build_rationale_index.py"

sys.path.insert(0, str(REPO_ROOT / "tools"))

import check_anchor_drift  # noqa: E402
import build_rationale_index  # noqa: E402
import build_rework_guard  # noqa: E402


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
    BASE_TRUTH = """\
# current truth fixture

shadowMAS exists to reduce three recurring failure modes:
- a
- b
- c

### Current v0 Intake Pack
1. `one.md`
2. `two.md`
3. `three.md`
"""

    def run_main_with(self, truth_text: str, *other_docs: str):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            truth = root / "CURRENT-TRUTH.md"
            truth.write_text(truth_text, encoding="utf-8")
            paths = [truth]
            for index, body in enumerate(other_docs):
                path = root / f"other-{index}.md"
                path.write_text(body, encoding="utf-8")
                paths.append(path)

            stdout = io.StringIO()
            with (
                patch.object(check_anchor_drift, "REPO", root),
                patch.object(check_anchor_drift, "CURRENT_TRUTH", truth),
                patch.object(check_anchor_drift, "COUNT_CLAIM_FILES", [truth]),
                patch.object(check_anchor_drift, "scannable_md_files", return_value=paths),
                contextlib.redirect_stdout(stdout),
            ):
                code = check_anchor_drift.main()
        return code, stdout.getvalue()

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

    def test_main_reports_count_claim_mismatch(self):
        dirty = self.BASE_TRUTH.replace("reduce three", "reduce five")
        code, output = self.run_main_with(dirty)
        self.assertEqual(code, 1, msg=output)
        self.assertIn("claims 5 failure modes but lists 3 bullets", output)

    def test_main_reports_full_intake_pack_duplication(self):
        duplicate = "\n".join(("`one.md`", "`two.md`", "`three.md`"))
        code, output = self.run_main_with(self.BASE_TRUTH, duplicate)
        self.assertEqual(code, 1, msg=output)
        self.assertIn("repeats the full v0 intake pack list", output)

    def test_main_reports_deprecated_vocabulary(self):
        code, output = self.run_main_with(
            self.BASE_TRUTH, "Coordination / Governance Shadow"
        )
        self.assertEqual(code, 1, msg=output)
        self.assertIn("deprecated term", output)


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

    def test_check_rejects_stale_compiled_surface(self):
        with tempfile.TemporaryDirectory() as tmp:
            stale = Path(tmp) / "DO-NOT-REDO.compiled.v0.en.md"
            stale.write_text("stale\n", encoding="utf-8")
            stdout = io.StringIO()
            with (
                patch.object(build_rework_guard, "OUTPUT", stale),
                contextlib.redirect_stdout(stdout),
            ):
                code = build_rework_guard.main(["--check"])

        self.assertEqual(code, 1, msg=stdout.getvalue())
        self.assertIn("surface is stale", stdout.getvalue())


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

    def test_check_rejects_stale_rationale_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            rationale = Path(tmp)
            (rationale / "DECISION-probe.v0.en.md").write_text(
                "# DECISION-probe | mutation probe\n"
                "# related: []\n"
                "# phase: test\n",
                encoding="utf-8",
            )
            (rationale / "rationale_index.md").write_text(
                "stale\n", encoding="utf-8"
            )
            stdout = io.StringIO()
            with (
                patch.object(build_rationale_index, "RATIONALE_DIR", rationale),
                contextlib.redirect_stdout(stdout),
            ):
                code = build_rationale_index.main(["--check"])

        self.assertEqual(code, 1, msg=stdout.getvalue())
        self.assertIn("rationale_index.md is stale", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
