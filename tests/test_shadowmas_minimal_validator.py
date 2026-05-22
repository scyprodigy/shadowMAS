import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = REPO_ROOT / "tools" / "shadowmas_minimal_validator.py"
PACKET_VALIDATOR = REPO_ROOT / "05_scripts" / "validate" / "shadowmas_validate.py"
POSITIVE_FIXTURE = REPO_ROOT / "examples" / "demo_signal_governance.json"
NEGATIVE_FIXTURE = REPO_ROOT / "examples" / "demo_signal_governance_violation.json"
VALID_REVIEW_PACKET = REPO_ROOT / "examples" / "packets" / "review_packet.valid.v0.yaml"
VALID_TASK_PACKET = REPO_ROOT / "examples" / "packets" / "task_packet.valid.v0.yaml"
SINGLE_FLAG_DIR = REPO_ROOT / "examples" / "mutations" / "single_flag"
PARTIAL_COMPLIANCE_DIR = REPO_ROOT / "examples" / "mutations" / "partial_compliance"
L1_REPORT = REPO_ROOT / "07_working" / "drafts" / "rationale" / "l1_mutation_coverage_report.md"


# Mapping from short fixture filename (without .json) to full invariant name.
# Order mirrors the validator's invariant declaration order.
MUTATION_MAPPING = [
    ("truth_status",            "runtime_signal_truth_status_runtime_only"),
    ("truth_promotion",         "runtime_signal_cannot_promote_truth_directly"),
    ("memory_write",            "runtime_signal_cannot_write_memory_directly"),
    ("review_required",         "runtime_signal_requires_human_review_for_promotion"),
    ("layer_promotion",         "no_t4_t5_to_t2_t3_direct_promotion"),
    ("silent_memory_write",     "no_silent_memory_write"),
    ("audit_read_only",         "audit_projection_is_read_only"),
    ("audit_approval",          "audit_projection_has_no_approval_authority"),
    ("audit_truth",             "audit_projection_has_no_truth_authority"),
    ("action_advisory",         "recommended_action_is_advisory_only"),
    ("action_runtime_auth",     "recommended_action_cannot_authorize_runtime_action"),
    ("action_packet_auth",      "recommended_action_cannot_authorize_packet_change"),
    ("action_truth_promotion",  "recommended_action_cannot_promote_truth"),
    ("dashboard_authority",     "dashboard_does_not_become_authority"),
    ("human_authority",         "human_final_authority_preserved"),
]


def _parse_validator_output(stdout):
    fails = []
    passes = []
    for line in stdout.splitlines():
        if line.startswith("FAIL: "):
            fails.append(line.split("FAIL: ", 1)[1].split(" - ", 1)[0])
        elif line.startswith("PASS: "):
            passes.append(line.split("PASS: ", 1)[1].split(" - ", 1)[0])
    return fails, passes


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


def run_packet_validator(packet_path):
    return subprocess.run(
        [sys.executable, str(PACKET_VALIDATOR), str(packet_path)],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )


def write_temp_packet(text):
    fh = tempfile.NamedTemporaryFile(
        mode="w", suffix=".v0.yaml", delete=False, encoding="utf-8"
    )
    try:
        fh.write(text)
    finally:
        fh.close()
    return Path(fh.name)


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

    def test_non_object_json_root_fails_every_invariant(self):
        fh = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        )
        try:
            fh.write("[]")
        finally:
            fh.close()
        tmp_path = Path(fh.name)
        self.addCleanup(tmp_path.unlink, missing_ok=True)

        result = run_validator(tmp_path)
        fails, passes = _parse_validator_output(result.stdout)

        self.assertNotEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertEqual(
            len(fails),
            len(MUTATION_MAPPING),
            msg=f"expected every invariant to fail on non-object root; got fails={fails}",
        )
        self.assertEqual(
            passes,
            [],
            msg=f"expected no passes on non-object root; got passes={passes}",
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


class L1MutationCorpusTests(unittest.TestCase):
    def test_single_flag_mutation_corpus(self):
        fixtures = sorted(SINGLE_FLAG_DIR.glob("*.json"))
        short_names = {p.stem for p in fixtures}
        expected_short = {short for short, _ in MUTATION_MAPPING}

        self.assertEqual(len(fixtures), 15, "expected exactly 15 single_flag fixtures")
        self.assertEqual(short_names, expected_short, "single_flag corpus must cover every invariant exactly once")

        for short, invariant in MUTATION_MAPPING:
            fixture = SINGLE_FLAG_DIR / f"{short}.json"
            result = run_validator(fixture)
            fails, passes = _parse_validator_output(result.stdout)

            self.assertNotEqual(
                result.returncode, 0,
                msg=f"{fixture.name} should fail; stdout:\n{result.stdout}",
            )
            self.assertEqual(
                fails, [invariant],
                msg=f"{fixture.name} should fail exactly {invariant!r}; got fails={fails}",
            )
            self.assertEqual(
                len(passes), 14,
                msg=f"{fixture.name} should leave 14 invariants passing; got {len(passes)}",
            )

    def test_partial_compliance_traps(self):
        fixtures = sorted(PARTIAL_COMPLIANCE_DIR.glob("*.json"))
        short_names = {p.stem for p in fixtures}
        expected_short = {short for short, _ in MUTATION_MAPPING}

        self.assertEqual(len(fixtures), 15, "expected exactly 15 partial_compliance fixtures")
        self.assertEqual(short_names, expected_short, "partial_compliance corpus must cover every invariant exactly once")

        for short, invariant in MUTATION_MAPPING:
            fixture = PARTIAL_COMPLIANCE_DIR / f"{short}.json"
            result = run_validator(fixture)
            fails, _ = _parse_validator_output(result.stdout)

            self.assertNotEqual(
                result.returncode, 0,
                msg=f"{fixture.name} should fail; stdout:\n{result.stdout}",
            )
            self.assertEqual(
                fails, [invariant],
                msg=f"{fixture.name} should fail exactly {invariant!r}; got fails={fails}",
            )

    def test_l1_mutation_coverage_report_exists(self):
        self.assertTrue(L1_REPORT.exists(), f"L1 coverage report missing at {L1_REPORT}")
        text = L1_REPORT.read_text(encoding="utf-8")
        self.assertIn("mutation_detection_rate", text)
        self.assertIn("30/30", text)
        self.assertIn("partial_compliance_false_pass_rate", text)
        self.assertIn("0/15", text)
        for _, invariant in MUTATION_MAPPING:
            self.assertIn(invariant, text, f"report must mention invariant {invariant!r}")


class ShadowmasPacketValidatorTests(unittest.TestCase):
    def test_review_packet_recommendation_enum_values_pass(self):
        base_text = VALID_REVIEW_PACKET.read_text(encoding="utf-8")

        for recommendation in ("approve", "reject", "revise", "defer", "escalate"):
            with self.subTest(recommendation=recommendation):
                tmp_path = write_temp_packet(
                    base_text.replace("recommendation: defer", f"recommendation: {recommendation}")
                )
                self.addCleanup(tmp_path.unlink, missing_ok=True)

                result = run_packet_validator(tmp_path)

                self.assertEqual(
                    result.returncode,
                    0,
                    msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
                )

    def test_review_packet_invalid_recommendation_fails(self):
        base_text = VALID_REVIEW_PACKET.read_text(encoding="utf-8")
        tmp_path = write_temp_packet(
            base_text.replace("recommendation: defer", "recommendation: maybe")
        )
        self.addCleanup(tmp_path.unlink, missing_ok=True)

        result = run_packet_validator(tmp_path)

        self.assertEqual(
            result.returncode,
            1,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertIn("ERROR INVALID_RECOMMENDATION", result.stdout)
        self.assertIn("field: recommendation", result.stdout)
        self.assertIn("path: $.recommendation", result.stdout)

    def test_review_packet_missing_recommendation_still_uses_required_field_error(self):
        lines = [
            line
            for line in VALID_REVIEW_PACKET.read_text(encoding="utf-8").splitlines()
            if not line.startswith("recommendation:")
        ]
        tmp_path = write_temp_packet("\n".join(lines) + "\n")
        self.addCleanup(tmp_path.unlink, missing_ok=True)

        result = run_packet_validator(tmp_path)

        self.assertEqual(
            result.returncode,
            1,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertIn("ERROR REQUIRED_FIELD_MISSING", result.stdout)
        self.assertIn("field: recommendation", result.stdout)
        self.assertNotIn("ERROR INVALID_RECOMMENDATION", result.stdout)

    def test_task_packet_validation_is_unaffected_by_recommendation_enum(self):
        result = run_packet_validator(VALID_TASK_PACKET)

        self.assertEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )


if __name__ == "__main__":
    unittest.main()
