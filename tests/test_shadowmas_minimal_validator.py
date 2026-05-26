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
    def _review_packet_with_lines(self, *lines):
        base_text = VALID_REVIEW_PACKET.read_text(encoding="utf-8")
        return base_text.replace("recommendation: defer", "recommendation: defer\n" + "\n".join(lines))

    def test_review_packet_recommendation_enum_values_pass(self):
        base_text = VALID_REVIEW_PACKET.read_text(encoding="utf-8")

        for recommendation in ("approve", "reject", "revise", "defer", "escalate", "unpromote"):
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

    def test_review_packet_reviewers_required_valid_values_pass(self):
        for reviewers_required in (1, 2):
            with self.subTest(reviewers_required=reviewers_required):
                tmp_path = write_temp_packet(
                    self._review_packet_with_lines(f"reviewers_required: {reviewers_required}")
                )
                self.addCleanup(tmp_path.unlink, missing_ok=True)

                result = run_packet_validator(tmp_path)

                self.assertEqual(
                    result.returncode,
                    0,
                    msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
                )

    def test_review_packet_reviewers_required_invalid_values_fail(self):
        cases = {
            "zero": "0",
            "negative": "-1",
            "string": '"2"',
            "boolean": "true",
            "float": "1.5",
            "list": "[]",
            "map": "{}",
        }
        for name, value in cases.items():
            with self.subTest(name=name):
                tmp_path = write_temp_packet(
                    self._review_packet_with_lines(f"reviewers_required: {value}")
                )
                self.addCleanup(tmp_path.unlink, missing_ok=True)

                result = run_packet_validator(tmp_path)

                self.assertEqual(
                    result.returncode,
                    1,
                    msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
                )
                self.assertIn("ERROR INVALID_REVIEWERS_REQUIRED", result.stdout)
                self.assertIn("field: reviewers_required", result.stdout)
                self.assertIn("path: $.reviewers_required", result.stdout)

    def test_review_packet_consensus_kind_valid_values_pass(self):
        for consensus_kind in ("unanimous", "majority", "first_to_decide"):
            with self.subTest(consensus_kind=consensus_kind):
                tmp_path = write_temp_packet(
                    self._review_packet_with_lines(f"consensus_kind: {consensus_kind}")
                )
                self.addCleanup(tmp_path.unlink, missing_ok=True)

                result = run_packet_validator(tmp_path)

                self.assertEqual(
                    result.returncode,
                    0,
                    msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
                )

    def test_review_packet_consensus_kind_invalid_values_fail(self):
        cases = {
            "unknown": "quorum",
            "integer": "2",
            "boolean": "true",
            "list": "[]",
        }
        for name, value in cases.items():
            with self.subTest(name=name):
                tmp_path = write_temp_packet(
                    self._review_packet_with_lines(f"consensus_kind: {value}")
                )
                self.addCleanup(tmp_path.unlink, missing_ok=True)

                result = run_packet_validator(tmp_path)

                self.assertEqual(
                    result.returncode,
                    1,
                    msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
                )
                self.assertIn("ERROR INVALID_CONSENSUS_KIND", result.stdout)
                self.assertIn("field: consensus_kind", result.stdout)
                self.assertIn("path: $.consensus_kind", result.stdout)

    def test_review_packet_promotion_snapshot_valid_values_pass(self):
        cases = {
            "one_source_hash": [
                "promotion_snapshot:",
                "  source_hashes:",
                "    - source_path: 01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md",
                "      hash: sha256:example-current-truth",
                "  snapshot_at: \"2026-05-22T00:00:00Z\"",
            ],
            "multiple_source_hashes": [
                "promotion_snapshot:",
                "  source_hashes:",
                "    - source_path: 01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md",
                "      hash: sha256:example-current-truth",
                "    - source_path: 00_entry/SHADOWMAS-LAYERING-QUICKREF.v0.en.md",
                "      hash: sha256:example-quickref",
                "  snapshot_at: \"2026-05-22T00:00:00Z\"",
            ],
        }
        for name, lines in cases.items():
            with self.subTest(name=name):
                tmp_path = write_temp_packet(self._review_packet_with_lines(*lines))
                self.addCleanup(tmp_path.unlink, missing_ok=True)

                result = run_packet_validator(tmp_path)

                self.assertEqual(
                    result.returncode,
                    0,
                    msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
                )

    def test_review_packet_promotion_snapshot_invalid_shapes_fail(self):
        cases = {
            "string": ["promotion_snapshot: not-a-snapshot"],
            "list": ["promotion_snapshot: []"],
            "boolean": ["promotion_snapshot: true"],
            "missing_source_hashes": [
                "promotion_snapshot:",
                "  snapshot_at: \"2026-05-22T00:00:00Z\"",
            ],
            "missing_snapshot_at": [
                "promotion_snapshot:",
                "  source_hashes:",
                "    - source_path: 01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md",
                "      hash: sha256:example-current-truth",
            ],
        }
        for name, lines in cases.items():
            with self.subTest(name=name):
                tmp_path = write_temp_packet(self._review_packet_with_lines(*lines))
                self.addCleanup(tmp_path.unlink, missing_ok=True)

                result = run_packet_validator(tmp_path)

                self.assertEqual(
                    result.returncode,
                    1,
                    msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
                )
                self.assertIn("ERROR INVALID_PROMOTION_SNAPSHOT", result.stdout)

    def test_review_packet_promotion_snapshot_invalid_source_hashes_fail(self):
        cases = {
            "source_hashes_string": [
                "promotion_snapshot:",
                "  source_hashes: not-a-list",
                "  snapshot_at: \"2026-05-22T00:00:00Z\"",
            ],
            "source_hashes_list_scalar_item": [
                "promotion_snapshot:",
                "  source_hashes:",
                "    - not-an-object",
                "  snapshot_at: \"2026-05-22T00:00:00Z\"",
            ],
            "source_hashes_non_string_value": [
                "promotion_snapshot:",
                "  source_hashes:",
                "    - source_path: 01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md",
                "      hash: 12345",
                "  snapshot_at: \"2026-05-22T00:00:00Z\"",
            ],
        }
        for name, lines in cases.items():
            with self.subTest(name=name):
                tmp_path = write_temp_packet(self._review_packet_with_lines(*lines))
                self.addCleanup(tmp_path.unlink, missing_ok=True)

                result = run_packet_validator(tmp_path)

                self.assertEqual(
                    result.returncode,
                    1,
                    msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
                )
                self.assertIn("ERROR INVALID_PROMOTION_SNAPSHOT", result.stdout)
                self.assertIn("field: source_hashes", result.stdout)
                self.assertIn("$.promotion_snapshot.source_hashes", result.stdout)

    def test_review_packet_promotion_snapshot_invalid_snapshot_at_fails(self):
        tmp_path = write_temp_packet(
            self._review_packet_with_lines(
                "promotion_snapshot:",
                "  source_hashes:",
                "    - source_path: 01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md",
                "      hash: sha256:example-current-truth",
                "  snapshot_at: 20260522",
            )
        )
        self.addCleanup(tmp_path.unlink, missing_ok=True)

        result = run_packet_validator(tmp_path)

        self.assertEqual(
            result.returncode,
            1,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertIn("ERROR INVALID_PROMOTION_SNAPSHOT", result.stdout)
        self.assertIn("field: snapshot_at", result.stdout)
        self.assertIn("path: $.promotion_snapshot.snapshot_at", result.stdout)

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

    def test_task_packet_validation_is_unaffected_by_multi_reviewer_fields(self):
        base_text = VALID_TASK_PACKET.read_text(encoding="utf-8")
        tmp_path = write_temp_packet(
            base_text + "\nreviewers_required: true\nconsensus_kind: quorum\n"
        )
        self.addCleanup(tmp_path.unlink, missing_ok=True)

        result = run_packet_validator(tmp_path)

        self.assertEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_task_packet_validation_is_unaffected_by_promotion_snapshot(self):
        base_text = VALID_TASK_PACKET.read_text(encoding="utf-8")
        tmp_path = write_temp_packet(
            base_text + "\npromotion_snapshot: invalid-for-review-packet\n"
        )
        self.addCleanup(tmp_path.unlink, missing_ok=True)

        result = run_packet_validator(tmp_path)

        self.assertEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_memory_packet_validation_is_unaffected_by_multi_reviewer_fields(self):
        memory_packet = """\
packet_uid: example-memory-packet-valid-v0-001
packet_type: memory_packet
schema_version: v0
created_at: "2026-05-22T00:00:00Z"
created_by: example_author
owner: example_owner
supervision_mode: human_available_delegate
risk: r0_trivial
status: candidate
memory_kind: tooling_note
memory_scope: session_local
summary: Example memory packet for validator scope testing.
structured_payload:
  note: Multi-reviewer fields are not memory_packet fields.
source_refs:
  - source_type: file
    source_path: examples/packets/review_packet.valid.v0.yaml
    relation: read_from
invalidation_triggers:
  - source file changes
confidence: 0.5
promotion_candidate: "no"
reviewers_required: true
consensus_kind: quorum
"""
        tmp_path = write_temp_packet(memory_packet)
        self.addCleanup(tmp_path.unlink, missing_ok=True)

        result = run_packet_validator(tmp_path)

        self.assertEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_memory_packet_validation_is_unaffected_by_promotion_snapshot(self):
        memory_packet = """\
packet_uid: example-memory-packet-valid-v0-001
packet_type: memory_packet
schema_version: v0
created_at: "2026-05-22T00:00:00Z"
created_by: example_author
owner: example_owner
supervision_mode: human_available_delegate
risk: r0_trivial
status: candidate
memory_kind: tooling_note
memory_scope: session_local
summary: Example memory packet for validator scope testing.
structured_payload:
  note: promotion_snapshot is not a memory_packet field.
source_refs:
  - source_type: file
    source_path: examples/packets/review_packet.valid.v0.yaml
    relation: read_from
invalidation_triggers:
  - source file changes
confidence: 0.5
promotion_candidate: "no"
promotion_snapshot: invalid-for-review-packet
"""
        tmp_path = write_temp_packet(memory_packet)
        self.addCleanup(tmp_path.unlink, missing_ok=True)

        result = run_packet_validator(tmp_path)

        self.assertEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_invalid_supervision_mode_fails(self):
        base_text = VALID_TASK_PACKET.read_text(encoding="utf-8")
        tmp_path = write_temp_packet(
            base_text.replace(
                "supervision_mode: human_available_delegate",
                "supervision_mode: not_a_real_mode",
            )
        )
        self.addCleanup(tmp_path.unlink, missing_ok=True)

        result = run_packet_validator(tmp_path)

        self.assertEqual(
            result.returncode,
            1,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertIn("INVALID_SUPERVISION_MODE", result.stdout)

    def test_invalid_risk_fails(self):
        base_text = VALID_TASK_PACKET.read_text(encoding="utf-8")
        tmp_path = write_temp_packet(
            base_text.replace(
                "risk: r0_trivial",
                "risk: not_a_real_tier",
            )
        )
        self.addCleanup(tmp_path.unlink, missing_ok=True)

        result = run_packet_validator(tmp_path)

        self.assertEqual(
            result.returncode,
            1,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertIn("INVALID_RISK", result.stdout)

    def test_invalid_created_at_fails(self):
        base_text = VALID_TASK_PACKET.read_text(encoding="utf-8")
        tmp_path = write_temp_packet(
            base_text.replace(
                'created_at: "2026-05-06T00:00:00Z"',
                'created_at: "not a timestamp"',
            )
        )
        self.addCleanup(tmp_path.unlink, missing_ok=True)

        result = run_packet_validator(tmp_path)

        self.assertEqual(
            result.returncode,
            1,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertIn("INVALID_TIMESTAMP", result.stdout)

    def test_empty_packet_uid_fails(self):
        base_text = VALID_TASK_PACKET.read_text(encoding="utf-8")
        tmp_path = write_temp_packet(
            base_text.replace(
                "packet_uid: example-task-packet-valid-v0-001",
                'packet_uid: ""',
            )
        )
        self.addCleanup(tmp_path.unlink, missing_ok=True)

        result = run_packet_validator(tmp_path)

        self.assertEqual(
            result.returncode,
            1,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertIn("INVALID_PACKET_UID", result.stdout)


if __name__ == "__main__":
    unittest.main()
