import contextlib
import io
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPO_ROOT / "tools" / "audit_shadow_state.py"

sys.path.insert(0, str(REPO_ROOT / "tools"))

import audit_shadow_state  # noqa: E402


class AuditShadowStateTests(unittest.TestCase):
    def test_current_repo_is_clean(self):
        """The consolidated health snapshot must be clean at HEAD."""
        result = subprocess.run(
            [sys.executable, str(TOOL)],
            capture_output=True, text=True, cwd=REPO_ROOT,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("shapes consistent", result.stdout)
        # the snapshot must disclose what it does not verify, not imply health
        self.assertIn("representation consistency only", result.stdout)
        # every underlying check should be represented as a row
        for label in (
            "anchor drift",
            "rationale index freshness",
            "do-not-redo freshness",
            "memory validity",
            "packet reference integrity",
            "rejection record contract",
            "shared-memory provenance",
        ):
            self.assertIn(label, result.stdout)

    def test_setup_error_summary_prefers_stderr(self):
        completed = subprocess.CompletedProcess(
            args=["probe"], returncode=2, stdout="misleading normal output\n", stderr="fatal scan error\n"
        )
        with patch.object(audit_shadow_state.subprocess, "run", return_value=completed):
            label, code, summary = audit_shadow_state.run_check("probe", ["probe"])

        self.assertEqual(label, "probe")
        self.assertEqual(code, 2)
        self.assertEqual(summary, "fatal scan error")

    def test_main_propagates_child_finding_and_setup_error(self):
        agenda = subprocess.CompletedProcess(
            args=["agenda"], returncode=0,
            stdout="review agenda: 0 pending packet(s)\n", stderr="",
        )
        for child_code, expected_code, expected_result in (
            (1, 1, "RESULT: FINDINGS"),
            (2, 2, "RESULT: ERROR"),
        ):
            with self.subTest(child_code=child_code):
                def fake_run_check(label, command):
                    code = child_code if label == "memory validity" else 0
                    return label, code, f"{label} probe"

                stdout = io.StringIO()
                with (
                    patch.object(
                        audit_shadow_state, "run_check", side_effect=fake_run_check
                    ),
                    patch.object(
                        audit_shadow_state.subprocess, "run", return_value=agenda
                    ),
                    contextlib.redirect_stdout(stdout),
                ):
                    code = audit_shadow_state.main([])

                self.assertEqual(code, expected_code, msg=stdout.getvalue())
                self.assertIn(expected_result, stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
