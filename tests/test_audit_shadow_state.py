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
        for label in ("anchor drift", "memory validity", "packet reference integrity"):
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


if __name__ == "__main__":
    unittest.main()
