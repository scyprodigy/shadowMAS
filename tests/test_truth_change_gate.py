import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CHECKER = REPO / "tools" / "check_truth_change.py"

REVIEW_PACKET = """\
packet_uid: rp-test-001
packet_type: review_packet
schema_version: v0
created_at: "2026-06-05T00:00:00Z"
created_by: tester
owner: tester
supervision_mode: human_live_pair
risk: r2_guarded
status: ready_for_human
decision_needed: approve truth change
why_you_are_seeing_this: test
change_summary: test
risk_summary: test
recommendation: approve
promotion_snapshot:
  source_hashes:
    - {path: 01_truth/FOO.v0.en.md, hash: abc}
  snapshot_at: "2026-06-05T00:00:00Z"
source_refs:
  - source_type: truth_file
    source_path: 01_truth/FOO.v0.en.md
    relation: reviews
"""


def run(args):
    return subprocess.run([sys.executable, str(CHECKER), *args], capture_output=True, text=True)


class TestTruthChangeGate(unittest.TestCase):
    def test_no_truth_change_ok(self):
        result = run(["--changed", "README.md"])
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_truth_change_without_review_is_finding(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run(["--changed", "01_truth/FOO.v0.en.md", "--reviews-dir", tmp])
            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertIn("MISSING", result.stdout)

    def test_truth_change_with_review_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "rp.yaml").write_text(REVIEW_PACKET, encoding="utf-8")
            result = run(["--changed", "01_truth/FOO.v0.en.md", "--reviews-dir", tmp])
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertIn("covered", result.stdout)

    def test_malformed_review_yaml_is_a_setup_error_not_a_silent_skip(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "broken.yaml").write_text("packet_type: [\n", encoding="utf-8")

            result = run(
                ["--changed", "01_truth/FOO.v0.en.md", "--reviews-dir", tmp]
            )

            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn("unable to parse YAML file", result.stderr)

    def test_invalid_git_base_is_a_setup_error_not_no_change(self):
        result = run(["--base", "refs/heads/__shadowmas_missing_base__"])

        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("git diff failed", result.stderr)
        self.assertNotIn("OK no 01_truth/ changes", result.stdout)

    def test_source_id_substring_does_not_cover_a_truth_path(self):
        source_id_only = REVIEW_PACKET.replace(
            "source_refs:\n"
            "  - source_type: truth_file\n"
            "    source_path: 01_truth/FOO.v0.en.md",
            "source_refs:\n"
            "  - source_type: truth_file\n"
            "    source_id: FOO",
        )
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "rp.yaml").write_text(source_id_only, encoding="utf-8")

            result = run(
                ["--changed", "01_truth/FOO.v0.en.md", "--reviews-dir", tmp]
            )

            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("MISSING", result.stdout)

    def test_review_without_packet_uid_does_not_cover_truth(self):
        missing_uid = REVIEW_PACKET.replace("packet_uid: rp-test-001\n", "")
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "rp.yaml").write_text(missing_uid, encoding="utf-8")

            result = run(
                ["--changed", "01_truth/FOO.v0.en.md", "--reviews-dir", tmp]
            )

            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("MISSING", result.stdout)

    def test_snapshot_must_cover_the_same_truth_path(self):
        unrelated_snapshot = REVIEW_PACKET.replace(
            "{path: 01_truth/FOO.v0.en.md, hash: abc}",
            "{path: 01_truth/BAR.v0.en.md, hash: abc}",
        )
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "rp.yaml").write_text(unrelated_snapshot, encoding="utf-8")

            result = run(
                ["--changed", "01_truth/FOO.v0.en.md", "--reviews-dir", tmp]
            )

            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("MISSING", result.stdout)

    def test_snapshot_requires_a_hash_and_valid_utc_timestamp(self):
        cases = {
            "missing_hash": REVIEW_PACKET.replace(
                "{path: 01_truth/FOO.v0.en.md, hash: abc}",
                "{path: 01_truth/FOO.v0.en.md}",
            ),
            "invalid_timestamp": REVIEW_PACKET.replace(
                'snapshot_at: "2026-06-05T00:00:00Z"',
                'snapshot_at: "2026-02-30T00:00:00Z"',
            ),
        }
        for name, packet in cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                (Path(tmp) / "rp.yaml").write_text(packet, encoding="utf-8")

                result = run(
                    ["--changed", "01_truth/FOO.v0.en.md", "--reviews-dir", tmp]
                )

                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("MISSING", result.stdout)


if __name__ == "__main__":
    unittest.main()
