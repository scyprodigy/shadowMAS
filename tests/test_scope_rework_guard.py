import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPO_ROOT / "tools" / "scope_rework_guard.py"

REJECTION_TEMPLATE = """\
purpose: {purpose}
rejected_claim: {claim}
rejected_at: "2026-06-09"
rejection_class: feature_not_built
rejection_scope:
  applies_to: {applies_to}
rejection_reasons:
  - first recorded reason for declining
reopen_conditions:
  - {reopen}
source_refs:
  - 07_working/drafts/rationale/DECISION-sample-record.v0.en.md
anti_resurrection_note: fixture record for guard tests
"""

DEFERRED_TEMPLATE = """\
# deferred_state_inventory | fixture inventory
# related: [none]
# phase: working_draft

# Deferred State Inventory

## Purpose
Fixture purpose section that the parser must skip.

## Sample deferred surface
- declared purpose: fixture deferred surface
- unlock trigger: first real fixture need appears
"""

LESSONS_TEMPLATE = """\
version: v0
entries:
  - lesson_id: lesson_9001
    date: "2026-06-15"
    trigger_type: rework_or_wrong_edit_risk
    short_summary: "bulk staging swept an unauthored file into a commit"
    impact: medium
    repeat_count: 1
    suggested_sink: execution_patch
    human_decision:
      status: pending
      note: "stage explicit paths only"
"""


class ScopeReworkGuardTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        self.rationale = self.repo / "07_working" / "drafts" / "rationale"
        self.rationale.mkdir(parents=True)
        (self.repo / "07_working" / "drafts").joinpath(
            "SHADOWMAS-LESSONS-QUEUE.v0.yaml"
        ).write_text(LESSONS_TEMPLATE, encoding="utf-8")
        (self.rationale / "deferred_state_inventory.md").write_text(
            DEFERRED_TEMPLATE, encoding="utf-8"
        )
        (self.rationale / "DECISION-sample-record.v0.en.md").write_text(
            "# DECISION-sample-record.v0.en | decision record: no giant "
            "orchestration framework adoption\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self._tmp.cleanup()

    def write_rejection(self, name="rejection_fixture_case.v0.yaml",
                        purpose="fixture rejection of wholesale framework adoption",
                        claim="adopt giant orchestration framework wholesale",
                        applies_to="all fixture scopes including src/parser/ tree",
                        reopen="a real fixture unlock event occurs"):
        (self.rationale / name).write_text(
            REJECTION_TEMPLATE.format(
                purpose=purpose, claim=claim, applies_to=applies_to, reopen=reopen
            ),
            encoding="utf-8",
        )

    def run_tool(self, *extra: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(TOOL), "--repo", str(self.repo), *extra],
            capture_output=True,
            text=True,
        )

    def test_exact_path_match_is_a_finding_with_exit_one(self):
        self.write_rejection()
        result = self.run_tool("--goal", "touch nothing related", "--path",
                               "src/parser.py")
        self.assertEqual(result.returncode, 1, msg=result.stdout + result.stderr)
        self.assertIn("EXACT_PATH", result.stdout)
        self.assertIn("matched path: src/parser.py", result.stdout)

    def test_strong_keyword_match_requires_two_primary_tokens(self):
        self.write_rejection()
        result = self.run_tool("--goal", "adopt an orchestration framework")
        self.assertEqual(result.returncode, 1, msg=result.stdout + result.stderr)
        self.assertIn("STRONG_KEYWORD", result.stdout)

    def test_reopen_conditions_are_printed_with_the_finding(self):
        self.write_rejection()
        result = self.run_tool("--goal", "adopt an orchestration framework")
        self.assertIn("reopen: a real fixture unlock event occurs", result.stdout)

    def test_single_token_overlap_is_weak_and_exit_zero(self):
        self.write_rejection()
        result = self.run_tool("--goal", "improve the framework docs")
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("MANUAL CONFIRMATION REQUIRED", result.stdout)
        self.assertIn("no exact or strong hit within bounded coverage",
                      result.stdout)

    def test_no_hit_uses_bounded_coverage_phrase(self):
        self.write_rejection()
        result = self.run_tool("--goal", "unrelated topic entirely zzz")
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("no hit within bounded coverage", result.stdout)
        self.assertIn("COVERAGE: scanned", result.stdout)

    def test_rejection_ordered_before_lesson_at_same_tier(self):
        self.write_rejection(claim="bulk staging swept files wholesale",
                             purpose="fixture rejection about bulk staging sweep")
        result = self.run_tool("--goal", "bulk staging swept")
        self.assertEqual(result.returncode, 1, msg=result.stdout + result.stderr)
        self.assertLess(result.stdout.index("rejection_fixture_case"),
                        result.stdout.index("lesson_9001"))

    def test_malformed_rejection_yaml_fails_closed(self):
        (self.rationale / "rejection_broken_case.v0.yaml").write_text(
            "purpose: [\n", encoding="utf-8"
        )
        result = self.run_tool("--goal", "anything at all")
        self.assertEqual(result.returncode, 2, msg=result.stdout + result.stderr)
        self.assertIn("unable to parse YAML file", result.stderr)

    def test_no_query_subjects_is_a_usage_error(self):
        result = self.run_tool()
        self.assertEqual(result.returncode, 2, msg=result.stdout + result.stderr)
        self.assertIn("no query subjects", result.stderr)

    def test_findings_beyond_max_sources_are_suppressed_with_notice(self):
        for i in range(12):
            self.write_rejection(
                name=f"rejection_case_{i:02d}.v0.yaml",
                purpose=f"fixture number {i} about widget alpha adoption",
                claim=f"widget alpha adoption case {i}")
        result = self.run_tool("--goal", "widget alpha adoption")
        self.assertEqual(result.returncode, 1, msg=result.stdout + result.stderr)
        self.assertIn("suppressed by the 8-source cap", result.stdout)
        self.assertEqual(result.stdout.count("[STRONG_KEYWORD] rejection"), 8)

    def test_max_sources_ceiling_cannot_be_raised(self):
        for i in range(12):
            self.write_rejection(
                name=f"rejection_case_{i:02d}.v0.yaml",
                purpose=f"fixture number {i} about widget alpha adoption",
                claim=f"widget alpha adoption case {i}")
        result = self.run_tool("--goal", "widget alpha adoption",
                               "--max-sources", "99")
        self.assertEqual(result.returncode, 1, msg=result.stdout + result.stderr)
        self.assertEqual(result.stdout.count("[STRONG_KEYWORD] rejection"), 8)
        self.assertIn("suppressed by the 8-source cap", result.stdout)

    def test_weak_matches_are_capped_with_notice(self):
        for i in range(12):
            self.write_rejection(
                name=f"rejection_weak_{i:02d}.v0.yaml",
                purpose=f"fixture number {i} about gadget item",
                claim=f"gadget item case {i}")
        result = self.run_tool("--goal", "gadget probe")
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertEqual(result.stdout.count("[WEAK] rejection"), 8)
        self.assertIn("more weak matches suppressed", result.stdout)

    def test_missing_sources_are_a_setup_error(self):
        (self.repo / "07_working" / "drafts" /
         "SHADOWMAS-LESSONS-QUEUE.v0.yaml").unlink()
        result = self.run_tool("--goal", "anything at all")
        self.assertEqual(result.returncode, 2, msg=result.stdout + result.stderr)
        self.assertIn("missing source", result.stderr)


if __name__ == "__main__":
    unittest.main()
