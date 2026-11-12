import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPO_ROOT / "05_scripts" / "workspace" / "shadowmas_workspace.py"
VALIDATOR = REPO_ROOT / "05_scripts" / "validate" / "shadowmas_validate.py"
PACKET_TOOL = REPO_ROOT / "05_scripts" / "workspace" / "shadowmas_packet.py"
TASK_PACKET_EXAMPLE = REPO_ROOT / "examples" / "packets" / "task_packet.valid.v0.yaml"
REVIEW_PACKET_EXAMPLE = REPO_ROOT / "examples" / "packets" / "review_packet.valid.v0.yaml"


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


def run_validator(packet_path):
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(packet_path)],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )


def run_packet_writer(project_path, input_path, env_overrides):
    env = os.environ.copy()
    env.update(env_overrides)
    return subprocess.run(
        [sys.executable, str(PACKET_TOOL), "write", "--project", str(project_path),
         "--input", str(input_path)],
        capture_output=True, text=True, cwd=REPO_ROOT, env=env,
    )


class WorkspaceListDestroyTests(unittest.TestCase):
    """Cover the list + destroy subcommands without touching the real workspace root."""

    def setUp(self):
        self._tmp_root = tempfile.TemporaryDirectory()
        self._tmp_project = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp_root.cleanup)
        self.addCleanup(self._tmp_project.cleanup)
        # One project-specific override isolates tests on every host OS.
        self.env = {"SHADOWMAS_DATA_HOME": self._tmp_root.name}
        self.project_path = str(Path(self._tmp_project.name).resolve())

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

    def test_first_attach_and_review_flow_uses_external_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            project_path = tmp_path / "product-repo"
            project_path.mkdir()
            env = {"SHADOWMAS_DATA_HOME": str(tmp_path / "shadowmas-data")}

            init = run_tool("init", "--project", str(project_path), env_overrides=env)
            self.assertEqual(init.returncode, 0, msg=init.stderr)

            where = run_tool("where", "--project", str(project_path), env_overrides=env)
            self.assertEqual(where.returncode, 0, msg=where.stderr)
            workspace = Path(where.stdout.strip())
            self.assertTrue(
                workspace.is_relative_to(Path(env["SHADOWMAS_DATA_HOME"])),
                msg=f"workspace {workspace} is not under temp shadowMAS data root",
            )
            inspect = run_tool("inspect", "--project", str(project_path), env_overrides=env)
            self.assertEqual(
                inspect.returncode,
                0,
                msg=f"stdout:\n{inspect.stdout}\nstderr:\n{inspect.stderr}",
            )

            for name in ("packets", "reviews", "handoffs", "runs"):
                self.assertTrue((workspace / name).is_dir(), msg=f"missing {name}/")

            task_write = run_packet_writer(project_path, TASK_PACKET_EXAMPLE, env)
            review_write = run_packet_writer(project_path, REVIEW_PACKET_EXAMPLE, env)
            self.assertEqual(task_write.returncode, 0, task_write.stderr)
            self.assertEqual(review_write.returncode, 0, review_write.stderr)
            task_packet = Path(task_write.stdout.strip())
            review_packet = Path(review_write.stdout.strip())
            self.assertEqual(task_packet.parent, workspace / "packets")
            self.assertEqual(review_packet.parent, workspace / "reviews")

            task_result = run_validator(task_packet)
            self.assertEqual(
                task_result.returncode,
                0,
                msg=f"stdout:\n{task_result.stdout}\nstderr:\n{task_result.stderr}",
            )
            self.assertIn("checks: passed", task_result.stdout)

            review_result = run_validator(review_packet)
            self.assertEqual(
                review_result.returncode,
                0,
                msg=f"stdout:\n{review_result.stdout}\nstderr:\n{review_result.stderr}",
            )
            self.assertIn("checks: passed", review_result.stdout)

            self.assertTrue(project_path.is_dir())
            self.assertEqual(list(project_path.iterdir()), [])

    def test_shadowmas_data_home_overrides_host_specific_roots(self):
        with tempfile.TemporaryDirectory() as tmp:
            override = Path(tmp) / "portable-root"
            env = {
                "SHADOWMAS_DATA_HOME": str(override),
                "XDG_DATA_HOME": str(Path(tmp) / "wrong-xdg"),
                "LOCALAPPDATA": str(Path(tmp) / "wrong-local-app-data"),
            }
            result = run_tool("list", env_overrides=env)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(str(override / "workspaces"), result.stdout)

    def test_shadowmas_data_home_refuses_relative_path(self):
        result = run_tool(
            "list",
            env_overrides={"SHADOWMAS_DATA_HOME": "relative-data-root"},
        )
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("must be an absolute path", result.stderr)


if __name__ == "__main__":
    unittest.main()
