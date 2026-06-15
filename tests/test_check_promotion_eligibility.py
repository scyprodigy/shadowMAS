import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPO_ROOT / "tools" / "check_promotion_eligibility.py"

ELIGIBLE = """\
packet_type: memory_packet
packet_uid: test-eligible-001
schema_version: v0
created_at: "2026-06-15T00:00:00Z"
created_by: t
owner: o
supervision_mode: human_available_delegate
risk: r1_routine
status: candidate
memory_kind: operational_heuristic
memory_scope: repo
summary: a candidate
structured_payload:
  k: v
source_refs:
  - source_type: file
    source_path: README.md
    relation: derived_from
invalidation_triggers:
  - the cited source changes
confidence: 0.7
promotion_candidate: "yes"
"""

INELIGIBLE_STATUS = ELIGIBLE.replace("status: candidate", "status: captured")
INELIGIBLE_NOT_CANDIDATE = ELIGIBLE.replace('promotion_candidate: "yes"', 'promotion_candidate: "no"')


class PromotionEligibilityTests(unittest.TestCase):
    def _run(self, body: str) -> subprocess.CompletedProcess:
        with tempfile.NamedTemporaryFile("w", suffix=".v0.yaml", dir=REPO_ROOT,
                                         delete=False) as fh:
            fh.write(body)
            path = Path(fh.name)
        try:
            return subprocess.run(
                [sys.executable, str(TOOL), str(path)],
                capture_output=True, text=True, cwd=REPO_ROOT,
            )
        finally:
            path.unlink()

    def test_real_candidate_is_eligible(self):
        result = subprocess.run(
            [sys.executable, str(TOOL),
             "07_working/drafts/memory_compiled_surface_discipline.v0.yaml"],
            capture_output=True, text=True, cwd=REPO_ROOT,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("ELIGIBLE FOR REVIEW", result.stdout)

    def test_eligible_fixture_passes(self):
        result = self._run(ELIGIBLE)
        self.assertEqual(result.returncode, 0, msg=result.stdout)

    def test_wrong_status_is_ineligible(self):
        result = self._run(INELIGIBLE_STATUS)
        self.assertEqual(result.returncode, 1, msg=result.stdout)
        self.assertIn("3 status is candidate", result.stdout)
        self.assertIn("NOT ELIGIBLE", result.stdout)

    def test_not_promotion_candidate_is_ineligible(self):
        result = self._run(INELIGIBLE_NOT_CANDIDATE)
        self.assertEqual(result.returncode, 1, msg=result.stdout)
        self.assertIn("NOT ELIGIBLE", result.stdout)


if __name__ == "__main__":
    unittest.main()
