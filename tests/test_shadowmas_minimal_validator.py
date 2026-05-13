import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = REPO_ROOT / "tools" / "shadowmas_minimal_validator.py"
POSITIVE_FIXTURE = REPO_ROOT / "examples" / "demo_signal_governance.json"
NEGATIVE_FIXTURE = REPO_ROOT / "examples" / "demo_signal_governance_violation.json"


PASS_INVARIANTS = [
    "PASS: runtime_signal_truth_status_runtime_only",
    "PASS: runtime_signal_cannot_promote_truth_directly",
    "PASS: runtime_signal_cannot_write_memory_directly",
    "PASS: runtime_signal_requires_human_review_for_promotion",
    "PASS: no_t4_t5_to_t2_t3_direct_promotion",
    "PASS: no_silent_memory_write",
    "PASS: audit_projection_is_read_only",
    "PASS: audit_projection_has_no_approval_authority",
    "PASS: audit_projection_has_no_truth_authority",
    "PASS: recommended_action_is_advisory_only",
    "PASS: recommended_action_cannot_authorize_runtime_action",
    "PASS: recommended_action_cannot_authorize_packet_change",
    "PASS: recommended_action_cannot_promote_truth",
    "PASS: dashboard_does_not_become_authority",
    "PASS: human_final_authority_preserved",
]

NEGATIVE_EXPECTED_LINES = [
    "PASS: runtime_signal_truth_status_runtime_only",
    "FAIL: runtime_signal_cannot_promote_truth_directly",
    "FAIL: runtime_signal_cannot_write_memory_directly",
    "FAIL: runtime_signal_requires_human_review_for_promotion",
    "FAIL: no_t4_t5_to_t2_t3_direct_promotion",
    "FAIL: no_silent_memory_write",
    "FAIL: audit_projection_is_read_only",
    "FAIL: audit_projection_has_no_approval_authority",
    "FAIL: audit_projection_has_no_truth_authority",
    "FAIL: recommended_action_is_advisory_only",
    "FAIL: recommended_action_cannot_authorize_runtime_action",
    "FAIL: recommended_action_cannot_authorize_packet_change",
    "FAIL: recommended_action_cannot_promote_truth",
    "FAIL: dashboard_does_not_become_authority",
    "FAIL: human_final_authority_preserved",
]


def run_validator(fixture_path):
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(fixture_path)],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )


class ShadowmasMinimalValidatorTests(unittest.TestCase):
    def test_positive_fixture_passes(self):
        result = run_validator(POSITIVE_FIXTURE)

        self.assertEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        for expected in PASS_INVARIANTS:
            self.assertIn(
                expected,
                result.stdout,
                msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
        self.assertNotIn(
            "FAIL:",
            result.stdout,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_negative_fixture_fails(self):
        result = run_validator(NEGATIVE_FIXTURE)

        self.assertEqual(
            result.returncode,
            1,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        for expected in NEGATIVE_EXPECTED_LINES:
            self.assertIn(
                expected,
                result.stdout,
                msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )

    def test_validator_missing_file_fails(self):
        missing_fixture = REPO_ROOT / "tests" / "definitely_missing_validator_fixture.json"
        result = run_validator(missing_fixture)
        combined_output = result.stdout + result.stderr

        self.assertNotEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertTrue(
            any(signal in combined_output for signal in ["No such file", "not found", "error", "Error"]),
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )


if __name__ == "__main__":
    unittest.main()
