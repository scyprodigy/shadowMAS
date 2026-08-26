import datetime as dt
import json
import subprocess
import sys
import tempfile
import unittest
import uuid
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPO_ROOT / "tools" / "review_brief_metrics.py"


class ReviewBriefMetricsTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.workspace = Path(self._tmp.name)
        (self.workspace / "runs").mkdir()
        (self.workspace / "reviews").mkdir()
        self.run_file = self.workspace / "runs" / "review_brief_runs.v1.jsonl"

    def tearDown(self):
        self._tmp.cleanup()

    def record(self, kind: str, signoff_id: str, *, action: str = "none",
               action_source: str = "operator_declared_unauthenticated",
               authentication: str = "none", **extra) -> dict:
        signoff = kind == "signoff"
        base = {
            "record_version": "review_brief_run.v1",
            "record_kind": kind,
            "run_id": self.opaque(f"run:{signoff_id}:{kind}"),
            "signoff_id": self.opaque(f"signoff:{signoff_id}"),
            "at": "2026-08-13T00:00:00Z",
            "risk": "r2_guarded",
            "eligible_signoff": True,
            "brief_displayed": signoff,
            "brief_consulted": signoff,
            "consultation_claim": "display_proxy_only",
            "interaction_channel": "tty" if signoff else "none",
            "authentication": authentication,
            "judgment": "approve" if signoff else "none",
            "judgment_source": ("operator_input_unauthenticated"
                                if signoff else "none"),
            "observable_action": action if signoff else "not_applicable",
            "observable_action_source": action_source if signoff else "none",
            "changed_loc": 10,
            "blocking_findings": 0,
            "advisory_findings": 0,
            "guard_hits": 0,
            "receipt": (f"reviews/review-{signoff_id}.v0.yaml"
                        if signoff else None),
            "compose_ms": 500,
            "triage_ms": 500 if signoff else 0,
            "exit_code": 0,
        }
        base.update(extra)
        return base

    @staticmethod
    def opaque(label: str) -> str:
        return str(uuid.uuid5(uuid.NAMESPACE_URL,
                              f"shadowmas-test:{label}"))

    @staticmethod
    def receipt_text(packet_uid: str) -> str:
        return (
            f"packet_uid: {packet_uid}\n"
            "packet_type: review_packet\n"
            "schema_version: v0\n"
            "created_at: '2026-01-01T00:00:00Z'\n"
            "created_by: review_brief_test\n"
            "owner: fixture_owner\n"
            "supervision_mode: human_live_pair\n"
            "risk: r2_guarded\n"
            "status: approved\n"
            "decision_needed: fixture decision\n"
            "why_you_are_seeing_this: fixture evidence\n"
            "change_summary: fixture change\n"
            "risk_summary: fixture risk\n"
            "recommendation: approve\n"
        )

    def write(self, records: list[dict]) -> None:
        receipt_uids: dict[str, str] = {}
        for record in records:
            receipt = record.get("receipt")
            if (record.get("record_kind") == "signoff"
                    and isinstance(receipt, str)
                    and receipt.startswith("reviews/")
                    and receipt.count("/") == 1
                    and receipt.endswith(".v0.yaml")):
                packet_uid = receipt_uids.setdefault(
                    receipt, f"packet-{len(receipt_uids)}")
                (self.workspace / receipt).write_text(
                    self.receipt_text(packet_uid),
                    encoding="utf-8")
        self.write_jsonl(records)

    def write_jsonl(self, records: list[dict]) -> None:
        self.run_file.write_text(
            "".join(json.dumps(record) + "\n" for record in records),
            encoding="utf-8",
        )

    def spanning(self, records: list[dict]) -> list[dict]:
        start = dt.datetime(2026, 1, 1, tzinfo=dt.timezone.utc)
        for index, record in enumerate(records):
            at = start + dt.timedelta(days=index * 7)
            record["at"] = at.strftime("%Y-%m-%dT%H:%M:%SZ")
        return records

    def run_tool(self, *extra: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(TOOL), "--workspace", str(self.workspace),
             "--format", "json", *extra],
            capture_output=True,
            text=True,
        )

    def test_missing_run_data_is_insufficient_not_success(self):
        result = self.run_tool()
        self.assertEqual(result.returncode, 3, msg=result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["verdict"], "INSUFFICIENT_DATA")
        self.assertEqual(report["claim_ceiling"],
                         "recorded_workflow_proxy_only")

    def test_two_thresholds_produce_proxy_kill_signal(self):
        records = [self.record("skip", f"skip-{i}") for i in range(20)]
        records += [self.record("signoff", f"signoff-{i}") for i in range(10)]
        self.write(self.spanning(records))
        result = self.run_tool()
        self.assertEqual(result.returncode, 1, msg=result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["verdict"], "PROXY_KILL_SIGNAL")
        self.assertAlmostEqual(
            report["criteria"]["consult_rate_proxy"]["value"], 1 / 3)
        self.assertEqual(
            report["criteria"]["declared_action_rate_proxy"]["value"], 0.0)

    def test_good_proxy_rates_do_not_claim_product_success(self):
        self.write(self.spanning([
            self.record("signoff", f"signoff-{i}", action="added_check")
            for i in range(30)
        ]))
        result = self.run_tool()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["verdict"], "NO_PROXY_KILL_SIGNAL")
        self.assertEqual(
            report["integrity"]["distinct_receipt_packet_uids"], 30)
        self.assertIn("not human authentication", report["advisory"])
        self.assertNotIn("SUCCESS", result.stdout)

    def test_malformed_jsonl_fails_closed_without_partial_verdict(self):
        self.run_file.write_text('{"record_version":\n', encoding="utf-8")
        result = self.run_tool()
        self.assertEqual(result.returncode, 2, msg=result.stdout + result.stderr)
        self.assertIn("malformed JSONL", result.stderr)
        self.assertEqual(result.stdout, "")

    def test_forged_authentication_is_excluded_not_trusted(self):
        self.write([self.record("signoff", "forged", authentication="signed")])
        result = self.run_tool()
        self.assertEqual(result.returncode, 3, msg=result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["excluded"]["unsupported_authentication"], 1)
        self.assertEqual(report["admissible"]["signoff"], 0)

    def test_legacy_record_version_is_excluded_not_upgraded(self):
        self.write([self.record("signoff", "legacy",
                                record_version="review_brief_run.v0")])
        result = self.run_tool()
        self.assertEqual(result.returncode, 3, msg=result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["excluded"]["unknown_record_version"], 1)

    def test_eligible_flag_must_agree_with_risk(self):
        self.write([self.record("signoff", "forged-risk",
                                risk="r1_routine")])
        result = self.run_tool()
        self.assertEqual(result.returncode, 3, msg=result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["excluded"]["eligible_risk_mismatch"], 1)

    def test_signoff_requires_receipt_reference(self):
        self.write([self.record("signoff", "missing-receipt", receipt=None)])
        result = self.run_tool()
        self.assertEqual(result.returncode, 3, msg=result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(
            report["excluded"]["signoff_without_receipt_reference"], 1)

    def test_forbidden_learning_signal_is_excluded(self):
        self.write([self.record("signoff", "poisoned",
                                model_confidence_score=0.99)])
        result = self.run_tool()
        self.assertEqual(result.returncode, 3, msg=result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(
            report["excluded"]["forbidden_key:model_confidence_score"], 1)

    def test_unknown_v1_field_is_excluded(self):
        self.write([self.record("signoff", "unknown",
                                claimed_human_identity="operator")])
        result = self.run_tool()
        self.assertEqual(result.returncode, 3, msg=result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(
            report["excluded"]["unknown_field:claimed_human_identity"], 1)

    def test_nonstandard_json_number_is_malformed(self):
        record = self.record("signoff", "nan")
        record["compose_ms"] = float("nan")
        self.run_file.write_text(json.dumps(record) + "\n", encoding="utf-8")
        result = self.run_tool()
        self.assertEqual(result.returncode, 2, msg=result.stdout + result.stderr)
        self.assertIn("non-standard JSON constant", result.stderr)

    def test_poisoned_record_prevents_verdict_even_with_enough_clean_data(self):
        records = self.spanning([
            self.record("signoff", f"signoff-{i}", action="added_check")
            for i in range(30)
        ])
        records.append(self.record("signoff", "poisoned", raw_logs="secret"))
        self.write(records)
        result = self.run_tool()
        self.assertEqual(result.returncode, 3, msg=result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["verdict"], "PARTIAL_DATA")
        self.assertEqual(report["excluded"]["forbidden_key:raw_logs"], 1)

    def test_derived_action_is_not_counted_as_observed_change(self):
        self.write(self.spanning([
            self.record("signoff", f"signoff-{i}", action="revision",
                        action_source="derived_from_judgment")
            for i in range(30)
        ]))
        result = self.run_tool()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(
            report["criteria"]["declared_action_rate_proxy"]["value"], 0.0)
        self.assertEqual(report["limitations"]["derived_actions_not_counted"],
                         30)

    def test_duplicate_terminal_records_are_excluded(self):
        self.write([
            self.record("signoff", "same"),
            self.record("skip", "same"),
        ])
        result = self.run_tool()
        self.assertEqual(result.returncode, 3, msg=result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["excluded"]["ambiguous_terminal_records"], 2)
        self.assertEqual(report["admissible"]["eligible_signoff_units"], 0)

    def test_replayed_run_id_cannot_inflate_denominator(self):
        records = [
            self.record("signoff", f"signoff-{i}", action="added_check",
                        run_id=self.opaque("one-replayed-run"))
            for i in range(30)
        ]
        self.write(records)
        result = self.run_tool()
        self.assertEqual(result.returncode, 3, msg=result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["verdict"], "PARTIAL_DATA")
        self.assertEqual(report["excluded"]["duplicate_run_id"], 29)
        self.assertEqual(report["admissible"]["eligible_signoff_units"], 1)

    def test_reused_receipt_cannot_inflate_denominator(self):
        records = [
            self.record("signoff", f"signoff-{i}", action="added_check",
                        receipt="reviews/review-shared.v0.yaml")
            for i in range(30)
        ]
        self.write(records)
        result = self.run_tool()
        self.assertEqual(result.returncode, 3, msg=result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(
            report["excluded"]["duplicate_receipt_reference"], 29)
        self.assertEqual(report["admissible"]["eligible_signoff_units"], 1)

    def test_symlinked_receipts_cannot_satisfy_gate(self):
        real = self.workspace / "reviews" / "real.v0.yaml"
        real.write_text(
            self.receipt_text("real"), encoding="utf-8")
        records = self.spanning([
            self.record("signoff", f"signoff-{i}", action="added_check",
                        receipt=f"reviews/copy-{i}.v0.yaml")
            for i in range(30)
        ])
        for i in range(30):
            (self.workspace / "reviews" / f"copy-{i}.v0.yaml").symlink_to(
                "real.v0.yaml")
        self.write_jsonl(records)
        result = self.run_tool()
        self.assertEqual(result.returncode, 3, msg=result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["verdict"], "PARTIAL_DATA")
        self.assertEqual(report["excluded"]["receipt_is_symlink"], 30)
        self.assertEqual(report["admissible"]["eligible_signoff_units"], 0)

    def test_copied_packet_uid_cannot_satisfy_gate(self):
        records = self.spanning([
            self.record("signoff", f"signoff-{i}", action="added_check")
            for i in range(30)
        ])
        self.write(records)
        for record in records:
            (self.workspace / record["receipt"]).write_text(
                self.receipt_text("copied-packet"),
                encoding="utf-8")
        result = self.run_tool()
        self.assertEqual(result.returncode, 3, msg=result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["verdict"], "PARTIAL_DATA")
        self.assertEqual(
            report["excluded"]["duplicate_receipt_packet_uid"], 29)
        self.assertEqual(report["admissible"]["eligible_signoff_units"], 1)

    def test_missing_receipt_file_is_excluded(self):
        record = self.record("signoff", "missing-file")
        self.write([record])
        (self.workspace / record["receipt"]).unlink()
        result = self.run_tool()
        self.assertEqual(result.returncode, 3, msg=result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["excluded"]["receipt_missing"], 1)

    def test_since_excludes_earlier_valid_records(self):
        old = self.record("signoff", "old", at="2026-08-12T00:00:00Z")
        self.write([old])
        result = self.run_tool("--since", "2026-08-13T00:00:00Z")
        self.assertEqual(result.returncode, 3, msg=result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["admissible"]["signoff"], 0)
        self.assertEqual(report["window"]["since"],
                         "2026-08-13T00:00:00+00:00")
        self.assertEqual(report["window"]["valid_records_before_window"], 1)

    def test_since_excludes_earlier_poisoned_record_from_window(self):
        old = self.record("signoff", "old-poisoned",
                          at="2026-08-12T00:00:00Z", raw_logs="secret")
        self.write([old])
        result = self.run_tool("--since", "2026-08-13T00:00:00Z")
        self.assertEqual(result.returncode, 3, msg=result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["verdict"], "PARTIAL_DATA")
        self.assertEqual(report["excluded"]["forbidden_key:raw_logs"], 1)

    def test_since_cannot_launder_poison_into_clean_verdict(self):
        records = self.spanning([
            self.record("signoff", f"signoff-{i}", action="added_check")
            for i in range(30)
        ])
        records.append(self.record(
            "signoff", "old-poisoned", at="2025-01-01T00:00:00Z",
            record_version="review_brief_run.v0"))
        self.write(records)
        result = self.run_tool("--since", "2026-01-01T00:00:00Z")
        self.assertEqual(result.returncode, 3, msg=result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["verdict"], "PARTIAL_DATA")
        self.assertEqual(report["excluded"]["unknown_record_version"], 1)

    def test_thirty_units_in_one_session_are_insufficient(self):
        self.write([
            self.record("signoff", f"signoff-{i}", action="added_check")
            for i in range(30)
        ])
        result = self.run_tool()
        self.assertEqual(result.returncode, 3, msg=result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["verdict"], "INSUFFICIENT_DATA")
        self.assertFalse(report["window"]["observation_span_ready"])
        self.assertEqual(
            report["criteria"]["consult_rate_proxy"]["reason"],
            "observation_span<6_calendar_months")

    def test_backdated_endpoint_cannot_counterfeit_distributed_dogfood(self):
        records = [
            self.record("signoff", f"signoff-{i}", action="added_check",
                        at="2026-08-01T00:00:00Z")
            for i in range(29)
        ]
        records.append(self.record(
            "signoff", "backdated", action="added_check",
            at="2026-02-01T00:00:00Z"))
        self.write(records)
        result = self.run_tool()
        self.assertEqual(result.returncode, 3,
                         msg=result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["verdict"], "INSUFFICIENT_DATA")
        self.assertEqual(report["window"]["distinct_observation_months"], 2)
        self.assertTrue(report["window"]["observation_span_ready"])
        self.assertFalse(
            report["window"]["distinct_observation_months_ready"])
        self.assertFalse(report["window"]["observation_gate_ready"])
        self.assertEqual(
            report["criteria"]["consult_rate_proxy"]["reason"],
            "observation_distribution<6_distinct_calendar_months")

    def test_action_and_overhead_require_ten_signoffs(self):
        records = [self.record("skip", f"skip-{i}") for i in range(29)]
        records.append(self.record("signoff", "only-signoff"))
        self.write(self.spanning(records))
        result = self.run_tool()
        self.assertEqual(result.returncode, 3,
                         msg=result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["verdict"], "INSUFFICIENT_DATA")
        self.assertTrue(report["criteria"]["consult_rate_proxy"]["fires"])
        self.assertFalse(report["admissible"]["signoff_sample_ready"])
        for name in ("declared_action_rate_proxy",
                     "median_compose_plus_triage_seconds"):
            self.assertIsNone(report["criteria"][name]["value"])
            self.assertEqual(report["criteria"][name]["reason"],
                             "signoff_sample_too_small")

    def test_future_timestamp_is_excluded(self):
        self.write([self.record("signoff", "future",
                                at="2099-01-01T00:00:00Z")])
        result = self.run_tool()
        self.assertEqual(result.returncode, 3, msg=result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["excluded"]["timestamp_in_future"], 1)

    def test_sensitive_identifier_content_is_rejected(self):
        record = self.record("signoff", "clean")
        record["signoff_id"] = "approver=alice@example.com|authority=final"
        self.write([record])
        result = self.run_tool()
        self.assertEqual(result.returncode, 3, msg=result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["excluded"]["invalid_signoff_id"], 1)

    def test_sensitive_receipt_value_is_rejected(self):
        record = self.record("signoff", "clean")
        record["receipt"] = (
            "reviews/r.yaml;RAW_LOG=secret;model_confidence=0.98")
        self.write([record])
        result = self.run_tool()
        self.assertEqual(result.returncode, 3, msg=result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(
            report["excluded"]["signoff_without_receipt_reference"], 1)

    def test_unbounded_judgment_value_is_rejected(self):
        record = self.record("signoff", "clean")
        record["judgment"] = "approver=alice|authority=final"
        self.write([record])
        result = self.run_tool()
        self.assertEqual(result.returncode, 3, msg=result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["excluded"]["invalid_judgment"], 1)

    def test_default_text_discloses_window_and_limitations(self):
        result = subprocess.run(
            [sys.executable, str(TOOL), "--workspace", str(self.workspace)],
            capture_output=True, text=True)
        self.assertEqual(result.returncode, 3,
                         msg=result.stdout + result.stderr)
        self.assertIn("window: since=none", result.stdout)
        self.assertIn("distinct_observation_months=0", result.stdout)
        self.assertIn("distinct_targets=0/0 signoffs", result.stdout)
        self.assertIn("authentication=none", result.stdout)
        self.assertIn("causality=none", result.stdout)

    def test_since_requires_timezone(self):
        result = self.run_tool("--since", "2026-08-13T00:00:00")
        self.assertEqual(result.returncode, 2, msg=result.stdout + result.stderr)
        self.assertIn("timezone-aware", result.stderr)

    def test_evaluator_writes_no_workspace_artifacts(self):
        before = sorted(path.relative_to(self.workspace)
                        for path in self.workspace.rglob("*"))
        self.run_tool()
        after = sorted(path.relative_to(self.workspace)
                       for path in self.workspace.rglob("*"))
        self.assertEqual(after, before)


if __name__ == "__main__":
    unittest.main()
