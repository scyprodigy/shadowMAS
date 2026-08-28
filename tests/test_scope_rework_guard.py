import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPO_ROOT / "tools" / "scope_rework_guard.py"

sys.path.insert(0, str(REPO_ROOT / "tools"))
import scope_rework_guard  # noqa: E402

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
        self.write_rejection(applies_to="exact file src/parser.py")
        result = self.run_tool("--goal", "touch nothing related", "--path",
                               "src/parser.py")
        self.assertEqual(result.returncode, 1, msg=result.stdout + result.stderr)
        self.assertIn("EXACT_PATH", result.stdout)
        self.assertIn("matched path: src/parser.py", result.stdout)

    def test_nested_declared_directory_is_a_path_scope_finding(self):
        self.write_rejection(applies_to="all files below src/parser/")
        result = self.run_tool("--goal", "unrelated words", "--path",
                               "src/parser/widget.py")
        self.assertEqual(result.returncode, 1, msg=result.stdout + result.stderr)
        self.assertIn("PATH_SCOPE", result.stdout)
        self.assertIn("matched path: src/parser/", result.stdout)

    def test_declared_directory_matches_its_own_normalized_path(self):
        self.write_rejection(applies_to="deferred `03_memory/session_log/`")
        for query in ("03_memory/session_log", "03_memory/session_log/"):
            with self.subTest(query=query):
                result = self.run_tool("--goal", "unrelated words", "--path",
                                       query)
                self.assertEqual(result.returncode, 1,
                                 msg=result.stdout + result.stderr)
                self.assertIn("EXACT_PATH", result.stdout)
                self.assertIn("matched path: 03_memory/session_log/",
                              result.stdout)

    def test_suffix_of_declared_path_is_not_exact(self):
        scope = "07_working/drafts/rationale/policy_filename_memo.md"
        for query in ("drafts/rationale/policy_filename_memo.md",
                      "rationale/policy_filename_memo.md"):
            with self.subTest(query=query):
                tier, hit = scope_rework_guard.declared_path_match(scope, query)
                self.assertIsNone(tier)
                self.assertIsNone(hit)

    def test_normalize_paths_removes_prefix_not_character_set(self):
        self.assertEqual(
            scope_rework_guard.normalize_paths(
                ["./src/widget.py", ".../foo.py", "./.hidden"]),
            ["src/widget.py", ".../foo.py", ".hidden"],
        )

    def test_normalize_paths_collapses_dot_segments_and_duplicate_slashes(self):
        self.assertEqual(
            scope_rework_guard.normalize_paths([
                "03_memory/./session_log",
                "03_memory//session_log",
            ]),
            ["03_memory/session_log", "03_memory/session_log"],
        )

    def test_absolute_and_parent_paths_are_refused(self):
        for query in ("/", "/tmp/outside.py", "../outside.py", "."):
            with self.subTest(query=query):
                result = self.run_tool("--goal", "unrelated", "--path", query)
                self.assertEqual(result.returncode, 2,
                                 msg=result.stdout + result.stderr)
                self.assertIn("invalid --path", result.stderr)

    def test_incidental_top_level_parent_is_not_an_exact_path_match(self):
        decision = self.rationale / "DECISION-incidental-path.v0.en.md"
        decision.write_text(
            "# DECISION-incidental-path.v0.en | unrelated fixture decision\n"
            "\nThis mentions `tools/other_tool.py` incidentally.\n",
            encoding="utf-8",
        )
        result = self.run_tool("--goal", "zzzz qqqq wwww", "--path",
                               "tools/nonexistent_probe.py")
        self.assertEqual(result.returncode, 0,
                         msg=result.stdout + result.stderr)
        self.assertNotIn("EXACT_PATH", result.stdout)

    def test_strong_keyword_match_requires_two_primary_tokens(self):
        self.write_rejection()
        result = self.run_tool("--goal", "adopt an orchestration framework")
        self.assertEqual(result.returncode, 1, msg=result.stdout + result.stderr)
        self.assertIn("STRONG_KEYWORD", result.stdout)

    def test_reopen_conditions_are_printed_with_the_finding(self):
        self.write_rejection()
        result = self.run_tool("--goal", "adopt an orchestration framework")
        self.assertIn("reopen: a real fixture unlock event occurs", result.stdout)

    def test_decision_reopen_conditions_come_from_its_own_section(self):
        decision = self.rationale / "DECISION-reopen-probe.v0.en.md"
        decision.write_text(
            "# DECISION-reopen-probe.v0.en | reject widget alpha redesign\n"
            "\n# Decision\nDo not redesign.\n"
            "\n# Reopen conditions\n\n- owner supplies new evidence\n"
            "- fixture constraint changes\n\n# Anti-resurrection note\nStop.\n",
            encoding="utf-8",
        )
        result = self.run_tool("--goal", "widget alpha redesign")
        self.assertEqual(result.returncode, 1, msg=result.stdout + result.stderr)
        self.assertIn("reopen: owner supplies new evidence", result.stdout)
        self.assertIn("reopen: fixture constraint changes", result.stdout)

    def test_rejected_reopen_heading_is_not_live(self):
        text = (
            "# Rejected reopen conditions\n\n"
            "- rejected condition\n\n"
            "# Reopen conditions\n\n"
            "- live condition\n")
        self.assertEqual(
            scope_rework_guard.markdown_list_section(text,
                                                     "reopen conditions"),
            ["live condition"],
        )

    def test_fenced_heading_does_not_end_reopen_section(self):
        text = (
            "# Reopen conditions\n\n"
            "- live condition\n\n"
            "```markdown\n# Not a real heading\n```\n"
            "  continued detail\n\n# Next section\n")
        self.assertEqual(
            scope_rework_guard.markdown_list_section(text,
                                                     "reopen conditions"),
            ["live condition continued detail"],
        )

    def test_common_decorated_reopen_headings_are_recognized(self):
        for heading in ("## Reopen conditions:",
                        "## **Reopen conditions**",
                        "## _Reopen conditions_:"):
            with self.subTest(heading=heading):
                self.assertEqual(
                    scope_rework_guard.markdown_list_section(
                        f"{heading}\n\n- live condition\n",
                        "reopen conditions"),
                    ["live condition"],
                )

    def test_unclosed_fence_is_refused(self):
        text = "```markdown\n# Reopen conditions\n- hidden condition\n"
        with self.assertRaisesRegex(ValueError, "unclosed Markdown fence"):
            scope_rework_guard.markdown_list_section(
                text, "reopen conditions")

    def test_nested_condition_remains_qualified_by_parent(self):
        text = ("# Reopen conditions\n\n- parent condition\n"
                "  - nested qualification\n")
        self.assertEqual(
            scope_rework_guard.markdown_list_section(
                text, "reopen conditions"),
            ["parent condition — nested: nested qualification"],
        )

    def test_setext_reopen_heading_is_recognized(self):
        text = "Reopen conditions\n-----------------\n\n- live condition\n"
        self.assertEqual(
            scope_rework_guard.markdown_list_section(
                text, "reopen conditions"),
            ["live condition"],
        )

    def test_thematic_break_after_list_item_is_not_a_setext_heading(self):
        text = "# Reopen conditions\n\n- first\n---\n- second\n"
        self.assertEqual(
            scope_rework_guard.markdown_list_section(
                text, "reopen conditions"),
            ["first", "second"],
        )

    def test_thematic_break_after_wrapped_item_is_not_a_setext_heading(self):
        text = (
            "# Reopen conditions\n\n- first\n"
            "  wrapped text\n---\n- second\n"
        )
        self.assertEqual(
            scope_rework_guard.markdown_list_section(
                text, "reopen conditions"),
            ["first wrapped text", "second"],
        )

    def test_thematic_break_after_lazy_continuation_preserves_items(self):
        text = (
            "# Reopen conditions\n\n- first\n"
            "lazy text\n---\n- second\n"
        )
        self.assertEqual(
            scope_rework_guard.markdown_list_section(
                text, "reopen conditions"),
            ["first lazy text", "second"],
        )

    def test_equals_after_lazy_continuation_remains_condition_text(self):
        text = (
            "# Reopen conditions\n\n- first\n"
            "lazy text\n===\n- second\n"
        )
        self.assertEqual(
            scope_rework_guard.markdown_list_section(
                text, "reopen conditions"),
            ["first lazy text ===", "second"],
        )

    def test_spaced_thematic_break_does_not_become_a_condition(self):
        for rule in ("- - -", "  * * *", "    _ _ _"):
            with self.subTest(rule=rule):
                text = (
                    "# Reopen conditions\n\n- first\n"
                    f"{rule}\n- second\n"
                )
                self.assertEqual(
                    scope_rework_guard.markdown_list_section(
                        text, "reopen conditions"),
                    ["first", "second"],
                )

    def test_indented_code_block_is_not_condition_text(self):
        text = (
            "# Reopen conditions\n\n- first\n\n"
            "      code sample\n"
            "      - code-looking line\n"
            "      more code\n"
            "- second\n"
        )
        self.assertEqual(
            scope_rework_guard.markdown_list_section(
                text, "reopen conditions"),
            ["first", "second"],
        )

    def test_indented_paragraph_remains_condition_text(self):
        text = (
            "# Reopen conditions\n\n- first\n\n"
            "    wrapped paragraph\n"
            "- second\n"
        )
        self.assertEqual(
            scope_rework_guard.markdown_list_section(
                text, "reopen conditions"),
            ["first wrapped paragraph", "second"],
        )

    def test_setext_heading_after_blank_terminates_live_section(self):
        text = (
            "# Reopen conditions\n\n- first\n\n"
            "Next section\n------------\n- hidden\n"
        )
        self.assertEqual(
            scope_rework_guard.markdown_list_section(
                text, "reopen conditions"),
            ["first"],
        )

    def test_block_quote_is_not_lazy_condition_text(self):
        text = (
            "# Reopen conditions\n\n- first\n"
            "> quoted note\n"
            "lazy quote continuation\n"
            "- second\n"
        )
        self.assertEqual(
            scope_rework_guard.markdown_list_section(
                text, "reopen conditions"),
            ["first", "second"],
        )

    def test_lazy_block_quote_text_is_not_a_setext_heading(self):
        text = (
            "# Reopen conditions\n\n- first\n"
            "> quoted note\n"
            "heading-like quote continuation\n"
            "---\n"
            "- second\n"
        )
        self.assertEqual(
            scope_rework_guard.markdown_list_section(
                text, "reopen conditions"),
            ["first", "second"],
        )

    def test_interrupting_html_block_is_not_lazy_condition_text(self):
        for html in (
                "<!-- editorial note -->",
                "<?review note?>",
                "<!REVIEW note>",
                "<![CDATA[note]]>",
                "<script>note</script>"):
            with self.subTest(html=html):
                text = (
                    "# Reopen conditions\n\n- first\n"
                    f"{html}\n- second\n"
                )
                self.assertEqual(
                    scope_rework_guard.markdown_list_section(
                        text, "reopen conditions"),
                    ["first", "second"],
                )

    def test_multiline_html_block_is_not_condition_text(self):
        text = (
            "# Reopen conditions\n\n- first\n"
            "<!--\neditorial note\n-->\n"
            "- second\n"
        )
        self.assertEqual(
            scope_rework_guard.markdown_list_section(
                text, "reopen conditions"),
            ["first", "second"],
        )

    def test_inline_html_remains_lazy_condition_text(self):
        text = (
            "# Reopen conditions\n\n- first\n"
            "<span>inline note</span>\n"
            "- second\n"
        )
        self.assertEqual(
            scope_rework_guard.markdown_list_section(
                text, "reopen conditions"),
            ["first <span>inline note</span>", "second"],
        )

    def test_paragraph_outside_list_is_not_condition_text(self):
        text = (
            "# Reopen conditions\n\n- first\n\n"
            "outside paragraph one\n"
            "outside paragraph two\n"
            "- second\n"
        )
        self.assertEqual(
            scope_rework_guard.markdown_list_section(
                text, "reopen conditions"),
            ["first", "second"],
        )

    def test_common_markdown_list_markers_are_recognized(self):
        for item in ("* asterisk condition", "+ plus condition",
                     "1. ordered condition", "2) ordered-paren condition"):
            with self.subTest(item=item):
                self.assertEqual(
                    scope_rework_guard.markdown_list_section(
                        f"# Reopen conditions\n\n{item}\n",
                        "reopen conditions"),
                    [item.split(maxsplit=1)[1]],
                )

    def test_multiple_live_reopen_sections_are_refused(self):
        decision = self.rationale / "DECISION-ambiguous.v0.en.md"
        decision.write_text(
            "# DECISION-ambiguous.v0.en | ambiguous widget decision\n\n"
            "# Reopen conditions\n\n- first\n\n"
            "# v-future Reopen Conditions\n\n- second\n",
            encoding="utf-8",
        )
        result = self.run_tool("--goal", "ambiguous widget decision")
        self.assertEqual(result.returncode, 2,
                         msg=result.stdout + result.stderr)
        self.assertIn("ambiguous decision record", result.stderr)

    def test_real_corpus_nonsense_task_has_no_path_false_positive(self):
        result = subprocess.run(
            [sys.executable, str(TOOL), "--repo", str(REPO_ROOT),
             "--goal", "zzzz qqqq wwww", "--path",
             "tools/nonexistent_review_probe.py"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0,
                         msg=result.stdout + result.stderr)
        self.assertIn("no hit within bounded coverage", result.stdout)
        self.assertNotIn("EXACT_PATH", result.stdout)

    def test_single_token_overlap_is_weak_and_exit_zero(self):
        self.write_rejection()
        result = self.run_tool("--goal", "improve the framework docs")
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("MANUAL CONFIRMATION REQUIRED", result.stdout)
        self.assertIn(
            "no exact, path-scope, or strong hit within bounded coverage",
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
