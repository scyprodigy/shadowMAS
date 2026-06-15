import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPO_ROOT / "tools" / "import_memory_candidate.py"

EXTERNAL_MEMORY = """\
packet_type: memory_packet
packet_uid: ext-memory-001
owner: someone_else
status: approved_shared
confidence: 0.95
promotion_candidate: "yes"
summary: externally trusted heuristic
invalidation_triggers:
  - source truth changed
"""

NOT_MEMORY = """\
packet_type: task_packet
packet_uid: ext-task-001
"""


class ImportMemoryCandidateTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.source = self.root / "external.yaml"
        self.source.write_text(EXTERNAL_MEMORY, encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def test_import_downgrades_status_and_caps_confidence(self):
        out = self.root / "imported.yaml"
        result = subprocess.run(
            [sys.executable, str(TOOL), str(self.source), "--out", str(out),
             "--importer", "test_owner"],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        data = yaml.safe_load(out.read_text(encoding="utf-8"))
        self.assertEqual(data["status"], "candidate")
        self.assertEqual(data["owner"], "test_owner")
        self.assertLessEqual(data["confidence"], 0.5)
        self.assertEqual(data["import_provenance"]["original_status"], "approved_shared")
        self.assertEqual(data["import_provenance"]["original_confidence"], 0.95)
        self.assertTrue(any("re-validated" in t for t in data["invalidation_triggers"]))
        # source file untouched
        self.assertEqual(self.source.read_text(encoding="utf-8"), EXTERNAL_MEMORY)

    def test_non_memory_packet_refused(self):
        bad = self.root / "task.yaml"
        bad.write_text(NOT_MEMORY, encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(TOOL), str(bad)],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("REFUSED", result.stdout)


if __name__ == "__main__":
    unittest.main()
