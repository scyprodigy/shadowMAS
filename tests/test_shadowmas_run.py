import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RUN = REPO / "05_scripts" / "run" / "shadowmas_run.py"
CLI = REPO / "05_scripts" / "cli" / "shadowmas_cli.py"
VALID_TASK = REPO / "examples" / "packets" / "task_packet.valid.v0.yaml"


def run(args):
    return subprocess.run([sys.executable, *args], capture_output=True, text=True)


class TestShadowmasRunDry(unittest.TestCase):
    def test_valid_task_packet_dry_run_exits_zero(self):
        result = run([str(RUN), "--dry", str(VALID_TASK)])
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("validate", result.stdout)
        self.assertIn("PASS", result.stdout)

    def test_dry_flag_required(self):
        result = run([str(RUN), str(VALID_TASK)])
        self.assertNotEqual(result.returncode, 0)

    def test_persisted_run_log_is_hash_chained(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run([str(RUN), "--dry", str(VALID_TASK), "--runs-dir", tmp])
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            logs = list(Path(tmp).glob("run_*.log.jsonl"))
            self.assertEqual(len(logs), 1)
            entries = [json.loads(line) for line in logs[0].read_text().splitlines()]
            self.assertGreater(len(entries), 0)
            self.assertEqual(entries[0]["prev_hash"], "genesis")
            for prev, cur in zip(entries, entries[1:]):
                self.assertEqual(cur["prev_hash"], prev["entry_hash"])

    def test_invalid_packet_stops_at_validate(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.v0.yaml"
            bad.write_text("packet_type: task_packet\nschema_version: v0\n", encoding="utf-8")
            result = run([str(RUN), "--dry", str(bad)])
            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertIn("STOP", result.stdout)

    def test_cli_dispatch_run(self):
        result = run([str(CLI), "run", "--dry", str(VALID_TASK)])
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_cli_dispatch_validate(self):
        result = run([str(CLI), "validate", str(VALID_TASK)])
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_cli_unknown_command(self):
        result = run([str(CLI), "frobnicate"])
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
