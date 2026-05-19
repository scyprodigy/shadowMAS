import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CLI = REPO_ROOT / "tools" / "inspect_l2_fixture.py"
VALID_FIXTURE = (
    REPO_ROOT / "examples" / "traces" / "l2_handoff" / "ephemeral_handoff_memory_promotion.json"
)


def run_cli(arg):
    return subprocess.run(
        [sys.executable, str(CLI), str(arg)],
        capture_output=True,
        text=True,
    )


class InspectL2FixtureCLITests(unittest.TestCase):
    def test_valid_fixture_returns_pass_and_exit_zero(self):
        result = run_cli(VALID_FIXTURE)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "pass")
        self.assertEqual(payload["violations"], [])
        self.assertEqual(payload["fixture_id"], "l2_handoff_ephemeral_memory_promotion")

    def test_cli_output_is_valid_json(self):
        result = run_cli(VALID_FIXTURE)
        json.loads(result.stdout)

    def test_malformed_fixture_missing_key_returns_fail_and_exit_one(self):
        fixture = json.loads(VALID_FIXTURE.read_text(encoding="utf-8"))
        del fixture["non_claims"]

        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".json", delete=False, encoding="utf-8"
            ) as fh:
                json.dump(fixture, fh)
                tmp_path = fh.name

            result = run_cli(tmp_path)
        finally:
            if tmp_path is not None:
                Path(tmp_path).unlink(missing_ok=True)

        self.assertEqual(result.returncode, 1, msg=result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "fail")
        self.assertTrue(
            any("missing_required_keys" in v for v in payload["violations"]),
            payload["violations"],
        )


if __name__ == "__main__":
    unittest.main()
