import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPO_ROOT / "05_scripts" / "workspace" / "shadowmas_workspace.py"


def run_tool(*args, env_overrides=None):
    env = os.environ.copy()
    if env_overrides:
        env.update(env_overrides)
    return subprocess.run(
        [sys.executable, str(TOOL), *args],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        env=env,
    )


class WorkspaceListDestroyTests(unittest.TestCase):
    """Cover the list + destroy subcommands without touching the real workspace root."""

    def setUp(self):
        self._tmp_root = tempfile.TemporaryDirectory()
        self._tmp_project = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp_root.cleanup)
        self.addCleanup(self._tmp_project.cleanup)
        # Redirect local_data_root() to the temp dir via XDG_DATA_HOME.
        # On Linux/WSL CI, local_data_root() respects XDG_DATA_HOME.
        self.env = {"XDG_DATA_HOME": self._tmp_root.name}
        self.project_path = self._tmp_project.name

    def test_list_empty_root_returns_zero(self):
        result = run_tool("list", env_overrides=self.env)
        self.assertEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertIn("no workspaces", result.stdout)

    def test_list_shows_initialized_workspace(self):
        init = run_tool("init", "--project", self.project_path, env_overrides=self.env)
        self.assertEqual(init.returncode, 0, msg=init.stderr)

        ls = run_tool("list", env_overrides=self.env)
        self.assertEqual(ls.returncode, 0, msg=ls.stderr)
        self.assertIn(self.project_path, ls.stdout)
        self.assertIn("OK", ls.stdout)

    def test_destroy_requires_yes_flag(self):
        init = run_tool("init", "--project", self.project_path, env_overrides=self.env)
        self.assertEqual(init.returncode, 0, msg=init.stderr)

        d = run_tool("destroy", "--project", self.project_path, env_overrides=self.env)
        self.assertEqual(
            d.returncode,
            1,
            msg=f"destroy without --yes must return 1; stdout:\n{d.stdout}",
        )
        self.assertIn("would destroy", d.stdout)

        # workspace still exists
        ls = run_tool("list", env_overrides=self.env)
        self.assertIn(self.project_path, ls.stdout)

    def test_destroy_with_yes_removes_workspace(self):
        init = run_tool("init", "--project", self.project_path, env_overrides=self.env)
        self.assertEqual(init.returncode, 0, msg=init.stderr)

        d = run_tool(
            "destroy", "--project", self.project_path, "--yes", env_overrides=self.env
        )
        self.assertEqual(
            d.returncode,
            0,
            msg=f"destroy --yes must return 0; stdout:\n{d.stdout}\nstderr:\n{d.stderr}",
        )
        self.assertIn("destroyed", d.stdout)

        ls = run_tool("list", env_overrides=self.env)
        self.assertIn("no workspaces", ls.stdout)

    def test_destroy_idempotent_on_missing(self):
        # No init; destroy should still succeed (idempotent).
        d = run_tool(
            "destroy", "--project", self.project_path, "--yes", env_overrides=self.env
        )
        self.assertEqual(
            d.returncode,
            0,
            msg=f"destroy on missing workspace must return 0; stdout:\n{d.stdout}",
        )
        self.assertIn("does not exist", d.stdout)


if __name__ == "__main__":
    unittest.main()
