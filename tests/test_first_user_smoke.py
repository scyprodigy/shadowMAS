import contextlib
import importlib.util
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SMOKE_SCRIPT = REPO_ROOT / "tools" / "first_user_smoke.py"


def load_smoke_module():
    spec = importlib.util.spec_from_file_location("first_user_smoke", SMOKE_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FirstUserSmokeTests(unittest.TestCase):
    def test_script_exists_and_imports(self):
        self.assertTrue(SMOKE_SCRIPT.is_file())
        module = load_smoke_module()
        self.assertTrue(hasattr(module, "run_smoke"))

    def test_help_output_contains_boundary_non_claim(self):
        result = subprocess.run(
            [sys.executable, str(SMOKE_SCRIPT), "--help"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn(
            "checks local representation and workspace mechanics only",
            result.stdout,
        )
        self.assertIn("does not prove production safety", result.stdout)
        self.assertIn("schema-valid packet", result.stdout)
        self.assertIn("authority-valid", result.stdout)

    def test_l1_negative_step_requires_nonzero_fail_signal(self):
        module = load_smoke_module()

        with contextlib.redirect_stdout(io.StringIO()):
            module.run_step(
                "expected negative",
                [sys.executable, "-c", "import sys; print('FAIL: expected'); sys.exit(1)"],
                cwd=REPO_ROOT,
                expect_l1_negative=True,
            )

        with contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(module.SmokeFailure):
                module.run_step(
                    "unexpected pass",
                    [sys.executable, "-c", "print('FAIL: but exited zero')"],
                    cwd=REPO_ROOT,
                    expect_l1_negative=True,
                )

        with contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(module.SmokeFailure):
                module.run_step(
                    "unexpected error",
                    [sys.executable, "-c", "import sys; print('runtime error'); sys.exit(1)"],
                    cwd=REPO_ROOT,
                    expect_l1_negative=True,
                )

    def test_fail_signal_helper_detects_fail_lines(self):
        module = load_smoke_module()
        result = subprocess.CompletedProcess(
            args=["demo"],
            returncode=1,
            stdout="FAIL: expected invariant\n",
            stderr="",
        )
        self.assertTrue(module.has_fail_signal(result))

    def test_is_under_helper_accepts_only_temp_child_paths(self):
        module = load_smoke_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            child = root / "xdg" / "shadowmas" / "workspaces" / "demo"
            child.mkdir(parents=True)
            outside = root.parent

            self.assertTrue(module.is_under(child, root))
            self.assertFalse(module.is_under(outside, child))


if __name__ == "__main__":
    unittest.main()
