import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPO_ROOT / "tools" / "check_memory_validity.py"

sys.path.insert(0, str(REPO_ROOT / "tools"))

import check_memory_validity  # noqa: E402


def write_packet(root: Path, name: str, body: str) -> Path:
    path = root / name
    path.write_text(body, encoding="utf-8")
    return path


CLEAN_PACKET = """\
packet_type: memory_packet
packet_uid: test-memory-clean-001
source_refs:
  - source_type: file
    source_path: existing_source.md
    relation: derived_from
"""

BROKEN_PACKET = """\
packet_type: memory_packet
packet_uid: test-memory-broken-001
source_refs:
  - source_type: file
    source_path: gone/missing_source.md
    relation: derived_from
"""

HASHED_PACKET_TEMPLATE = """\
packet_type: memory_packet
packet_uid: test-memory-hashed-001
source_refs: []
invalidation:
  source_hashes:
    - source_path: existing_source.md
      sha256: {sha}
validity:
  stale_on:
    - model or runtime generation changed
"""


class MemoryValidityCurrentStateTests(unittest.TestCase):
    def test_current_repo_is_clean(self):
        """All committed memory packets must resolve their cited sources at HEAD."""
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


class MemoryValidityUnitTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        (self.repo / "packets").mkdir()
        (self.repo / "existing_source.md").write_text("source body\n", encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def run_checker(self) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(CHECKER), "--repo", str(self.repo), "--root", "packets"],
            capture_output=True,
            text=True,
        )

    def test_clean_packet_passes(self):
        write_packet(self.repo / "packets", "clean.v0.yaml", CLEAN_PACKET)
        result = self.run_checker()
        self.assertEqual(result.returncode, 0, msg=result.stdout)
        self.assertIn("checked 1 memory packet(s)", result.stdout)

    def test_missing_source_is_broken_reference(self):
        write_packet(self.repo / "packets", "broken.v0.yaml", BROKEN_PACKET)
        result = self.run_checker()
        self.assertEqual(result.returncode, 1, msg=result.stdout)
        self.assertIn("broken_reference", result.stdout)
        self.assertIn("gone/missing_source.md", result.stdout)

    def test_hash_drift_is_stale_and_stale_on_is_noted(self):
        sha = check_memory_validity.sha256_of(self.repo / "existing_source.md")
        write_packet(self.repo / "packets", "hashed.v0.yaml",
                     HASHED_PACKET_TEMPLATE.format(sha=sha))
        result = self.run_checker()
        self.assertEqual(result.returncode, 0, msg=result.stdout)
        self.assertIn("NOTE declared stale_on condition", result.stdout)

        (self.repo / "existing_source.md").write_text("drifted body\n", encoding="utf-8")
        result = self.run_checker()
        self.assertEqual(result.returncode, 1, msg=result.stdout)
        self.assertIn("stale: source content drifted", result.stdout)


if __name__ == "__main__":
    unittest.main()
