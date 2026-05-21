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


def run_cli(*args):
    return subprocess.run(
        [sys.executable, str(CLI), *[str(a) for a in args]],
        capture_output=True,
        text=True,
    )


class InspectL2FixtureCLITests(unittest.TestCase):
    _EXPECTED_ENVELOPE_KEYS = {
        "fixture_id",
        "title",
        "status",
        "checked_rules",
        "violations",
        "transition",
        "human_summary_en",
        "human_summary_zh",
    }

    def _write_tmp(self, payload, *, suffix=".json"):
        fh = tempfile.NamedTemporaryFile(
            mode="w", suffix=suffix, delete=False, encoding="utf-8"
        )
        try:
            if isinstance(payload, str):
                fh.write(payload)
            else:
                json.dump(payload, fh)
        finally:
            fh.close()
        tmp_path = Path(fh.name)
        self.addCleanup(tmp_path.unlink, missing_ok=True)
        return tmp_path

    def _load_valid_fixture_copy(self):
        return json.loads(VALID_FIXTURE.read_text(encoding="utf-8"))

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
        fixture = self._load_valid_fixture_copy()
        del fixture["non_claims"]
        tmp_path = self._write_tmp(fixture)

        result = run_cli(tmp_path)

        self.assertEqual(result.returncode, 1, msg=result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "fail")
        self.assertTrue(
            any("missing_required_keys" in v for v in payload["violations"]),
            payload["violations"],
        )

    def test_invalid_json_file_returns_fail(self):
        tmp_path = self._write_tmp("not valid json {{{")

        result = run_cli(tmp_path)

        self.assertEqual(result.returncode, 1, msg=result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "fail")
        self.assertTrue(
            any(v.startswith("invalid_json") for v in payload["violations"]),
            payload["violations"],
        )

    def test_missing_file_path_returns_fail(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=True) as fh:
            missing_path = fh.name
        # The file is now deleted; we keep the path as a definitely nonexistent target.
        self.assertFalse(
            Path(missing_path).exists(),
            f"sanity: expected {missing_path} to be absent",
        )

        result = run_cli(missing_path)

        self.assertEqual(result.returncode, 1, msg=result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "fail")
        self.assertTrue(
            any(v.startswith("file_unreadable") for v in payload["violations"]),
            payload["violations"],
        )

    def test_no_argv_returns_usage_fail(self):
        result = subprocess.run(
            [sys.executable, str(CLI)],
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 1, msg=result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "fail")
        self.assertIn("usage", payload["checked_rules"])
        self.assertTrue(
            any(v.startswith("usage:") for v in payload["violations"]),
            payload["violations"],
        )

    def test_wrong_relation_returns_fail(self):
        fixture = self._load_valid_fixture_copy()
        fixture["expected_boundary_violation"]["unsafe_transition"]["relation"] = (
            "governed_promotion_candidate"
        )
        tmp_path = self._write_tmp(fixture)

        result = run_cli(tmp_path)

        self.assertEqual(result.returncode, 1, msg=result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "fail")
        self.assertTrue(
            any(
                v.startswith("relation_must_be_unsafe_promotion")
                for v in payload["violations"]
            ),
            payload["violations"],
        )

    def test_same_source_and_target_returns_fail(self):
        fixture = self._load_valid_fixture_copy()
        transition = fixture["expected_boundary_violation"]["unsafe_transition"]
        transition["target_layer"] = transition["source_layer"]
        tmp_path = self._write_tmp(fixture)

        result = run_cli(tmp_path)

        self.assertEqual(result.returncode, 1, msg=result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "fail")
        self.assertTrue(
            any(
                v.startswith("source_and_target_layers_must_differ")
                for v in payload["violations"]
            ),
            payload["violations"],
        )

    def test_pass_report_envelope_shape(self):
        result = run_cli(VALID_FIXTURE)

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        payload = json.loads(result.stdout)

        self.assertEqual(set(payload.keys()), self._EXPECTED_ENVELOPE_KEYS)
        self.assertEqual(payload["status"], "pass")
        self.assertEqual(payload["violations"], [])
        self.assertIsInstance(payload["checked_rules"], list)
        self.assertGreater(len(payload["checked_rules"]), 0)
        self.assertIsInstance(payload["transition"], dict)
        self.assertIsInstance(payload["human_summary_en"], str)
        self.assertGreater(len(payload["human_summary_en"]), 0)
        self.assertIsInstance(payload["human_summary_zh"], str)
        self.assertGreater(len(payload["human_summary_zh"]), 0)

    def test_fail_report_envelope_shape(self):
        fixture = self._load_valid_fixture_copy()
        del fixture["non_claims"]
        tmp_path = self._write_tmp(fixture)

        result = run_cli(tmp_path)

        self.assertEqual(result.returncode, 1, msg=result.stderr)
        payload = json.loads(result.stdout)

        self.assertEqual(set(payload.keys()), self._EXPECTED_ENVELOPE_KEYS)
        self.assertEqual(payload["status"], "fail")
        self.assertIsInstance(payload["violations"], list)
        self.assertGreater(len(payload["violations"]), 0)
        self.assertIsInstance(payload["checked_rules"], list)
        self.assertIsInstance(payload["human_summary_en"], str)
        self.assertGreater(len(payload["human_summary_en"]), 0)
        self.assertIsInstance(payload["human_summary_zh"], str)
        self.assertGreater(len(payload["human_summary_zh"]), 0)


if __name__ == "__main__":
    unittest.main()
