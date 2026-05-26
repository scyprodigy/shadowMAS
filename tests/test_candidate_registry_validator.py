import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPO_ROOT / "tools" / "check_candidate_registry.py"


class CandidateRegistryValidatorTests(unittest.TestCase):
    def test_current_registry_passes(self):
        """Current tracked CANDIDATE-REGISTRY entries must all satisfy schema."""
        result = subprocess.run(
            [sys.executable, str(CHECKER)],
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

    def test_missing_required_field_is_caught(self):
        """A candidate missing any required field must trigger exit 1."""
        # Build a minimal in-memory registry mirroring the real shape,
        # but with one candidate that omits a required field.
        dirty_yaml = """\
candidate_entry_schema:
  required_fields:
    - candidate_id
    - title
    - status
candidates:
  - candidate_id: TEST-001
    title: complete entry for control
    status: candidate_for_human_review
  - candidate_id: TEST-002
    status: candidate_for_human_review
    # title is intentionally missing
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            registry_dir = tmpdir_path / "03_memory" / "registry"
            registry_dir.mkdir(parents=True)
            (registry_dir / "SHADOWMAS-CANDIDATE-REGISTRY.v0.yaml").write_text(
                dirty_yaml, encoding="utf-8"
            )
            tools_dir = tmpdir_path / "tools"
            tools_dir.mkdir(parents=True)
            (tools_dir / "check_candidate_registry.py").write_bytes(
                CHECKER.read_bytes()
            )

            result = subprocess.run(
                [sys.executable, str(tools_dir / "check_candidate_registry.py")],
                capture_output=True,
                text=True,
                cwd=tmpdir_path,
            )

        self.assertEqual(
            result.returncode,
            1,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertIn("REGISTRY DIRTY", result.stdout)
        self.assertIn("TEST-002", result.stdout)
        self.assertIn("title", result.stdout)


if __name__ == "__main__":
    unittest.main()
