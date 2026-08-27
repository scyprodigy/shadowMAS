import json
import os
import select
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from argparse import Namespace
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPO_ROOT / "tools" / "compose_review_brief.py"
METRICS_TOOL = REPO_ROOT / "tools" / "review_brief_metrics.py"
VALIDATOR = REPO_ROOT / "05_scripts" / "validate" / "shadowmas_validate.py"

sys.path.insert(0, str(REPO_ROOT / "tools"))
import compose_review_brief  # noqa: E402

REJECTION_TEMPLATE = """\
purpose: fixture rejection of wholesale framework adoption
rejected_claim: adopt giant orchestration framework wholesale
rejected_at: "2026-06-09"
rejection_class: feature_not_built
rejection_scope:
  applies_to: all fixture scopes
rejection_reasons:
  - first recorded reason for declining
reopen_conditions:
  - a real fixture unlock event occurs
anti_resurrection_note: fixture record for brief tests
"""

DEFERRED_TEMPLATE = """\
# deferred_state_inventory | fixture inventory
# related: [none]
# phase: working_draft

## Sample deferred surface
- unlock trigger: first real fixture need appears
"""

LESSONS_TEMPLATE = """\
version: v0
entries: []
"""

SECTION_HEADINGS = [
    "1. EVIDENCE AND COUNTER-EVIDENCE",
    "2. DECISION FRAME",
    "3. COVERAGE MANIFEST",
    "4. RISK AND REVERSIBILITY",
    "5. CHECKS (max seven, typed)",
    "6. HUMAN JUDGMENT",
    "7. COMPILER RECOMMENDATION",
]


def make_args(**overrides):
    base = dict(
        goal="add fixture widget", acceptance=["criterion holds"], path=[],
        risk="r1_routine", rollback="git revert HEAD", irreversible=False,
        source=[], history_limit=0, changed_loc=42, session_minutes=90,
        signoff_id="", created_by="compose_review_brief.v0",
        owner="human_owner", supervision_mode="human_live_pair",
    )
    base.update(overrides)
    return Namespace(**base)


class ComposeReviewBriefTests(unittest.TestCase):
    def setUp(self):
        self._repo_tmp = tempfile.TemporaryDirectory()
        self._ws_tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._repo_tmp.name)
        self.workspace = Path(self._ws_tmp.name)
        rationale = self.repo / "07_working" / "drafts" / "rationale"
        rationale.mkdir(parents=True)
        (self.repo / "07_working" / "drafts" /
         "SHADOWMAS-LESSONS-QUEUE.v0.yaml").write_text(
            LESSONS_TEMPLATE, encoding="utf-8")
        (rationale / "deferred_state_inventory.md").write_text(
            DEFERRED_TEMPLATE, encoding="utf-8")
        (rationale / "rejection_fixture_case.v0.yaml").write_text(
            REJECTION_TEMPLATE, encoding="utf-8")
        (self.workspace / "reviews").mkdir()
        (self.workspace / "runs").mkdir()

    def tearDown(self):
        self._repo_tmp.cleanup()
        self._ws_tmp.cleanup()

    def run_tool(self, *extra: str, detach: bool = False,
                 timeout: float | None = None) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(TOOL), "--repo", str(self.repo),
             "--workspace", str(self.workspace), *extra],
            capture_output=True, text=True,
            stdin=subprocess.DEVNULL, start_new_session=detach,
            timeout=timeout,
        )

    def run_tool_pty(self, extra, replies: str, timeout: float = 30.0):
        """Run the tool under a real controlling terminal, so /dev/tty
        resolves and the interactive receipt flow actually executes. A
        scripted pty is not a human; it is how the tool's own honesty about
        that (interaction_channel:tty, authentication:none) gets exercised."""
        pid, fd = os.forkpty()
        if pid == 0:  # child; never returns
            try:
                os.execv(sys.executable,
                         [sys.executable, str(TOOL), "--repo", str(self.repo),
                          "--workspace", str(self.workspace), *extra])
            finally:
                os._exit(127)
        os.write(fd, replies.encode())
        chunks: list[bytes] = []
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if not select.select([fd], [], [], 0.5)[0]:
                continue
            try:
                data = os.read(fd, 4096)
            except OSError:  # EIO once the child releases the pty
                break
            if not data:
                break
            chunks.append(data)
        else:
            os.close(fd)
            os.kill(pid, signal.SIGKILL)
            os.waitpid(pid, 0)
            self.fail("tool did not exit under a pseudo-terminal")
        os.close(fd)
        _, status = os.waitpid(pid, 0)
        return (os.waitstatus_to_exitcode(status),
                b"".join(chunks).decode("utf-8", "replace"))

    def base_args(self, *extra: str):
        return ("--goal", "add fixture widget", "--risk", "r1_routine",
                "--rollback", "git revert HEAD", "--changed-loc", "42", *extra)

    def last_run_record(self) -> dict:
        runs_file = self.workspace / "runs" / "review_brief_runs.v1.jsonl"
        lines = runs_file.read_text(encoding="utf-8").splitlines()
        return json.loads(lines[-1])

    def init_git(self):
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        subprocess.run(["git", "-C", str(self.repo), "-c",
                        "user.email=t@t", "-c", "user.name=t",
                        "commit", "-q", "--allow-empty", "-m", "init"],
                       check=True)

    def test_evidence_precedes_frame_and_recommendation_is_withheld(self):
        result = self.run_tool(*self.base_args())
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        evidence = result.stdout.index("1. EVIDENCE AND COUNTER-EVIDENCE")
        frame = result.stdout.index("2. DECISION FRAME")
        recommendation = result.stdout.index("7. COMPILER RECOMMENDATION")
        self.assertLess(evidence, frame)
        self.assertLess(frame, recommendation)
        self.assertIn("withheld until a human judgment", result.stdout)

    def test_counter_evidence_precedes_frame_and_recommendation_is_last(self):
        result = self.run_tool("--goal", "adopt an orchestration framework",
                               "--risk", "r1_routine", "--changed-loc", "42")
        out = result.stdout
        self.assertEqual(result.returncode, 1, msg=out + result.stderr)
        evidence = out.index("1. EVIDENCE AND COUNTER-EVIDENCE")
        blocking = out.index("BLOCKING FINDINGS")
        advisory = out.index("ADVISORY FINDINGS")
        frame = out.index("2. DECISION FRAME")
        judgment = out.index("6. HUMAN JUDGMENT")
        recommendation = out.index("7. COMPILER RECOMMENDATION")
        self.assertLess(evidence, blocking)
        self.assertLess(blocking, advisory)
        self.assertLess(advisory, frame)
        self.assertLess(frame, judgment)
        self.assertLess(judgment, recommendation)
        self.assertNotIn("FINDINGS", out[recommendation:],
                         msg="findings must not reappear after section 7")
        self.assertEqual(out.rindex("BLOCKING FINDINGS"), blocking)
        self.assertEqual(out.rindex("ADVISORY FINDINGS"), advisory)

    def test_guard_hit_is_advisory_evidence_with_exit_one(self):
        result = self.run_tool("--goal", "adopt an orchestration framework",
                               "--risk", "r1_routine",
                               "--rollback", "git revert HEAD",
                               "--changed-loc", "42")
        self.assertEqual(result.returncode, 1, msg=result.stdout + result.stderr)
        self.assertIn("DISCONFIRM", result.stdout)
        self.assertIn("ADVISORY FINDINGS", result.stdout)
        self.assertNotIn("BLOCKING FINDINGS", result.stdout)
        self.assertIn("withheld until a human judgment", result.stdout)

    def test_over_budget_is_blocking_with_units(self):
        result = self.run_tool(*self.base_args("--path", "src/widget.py"),
                               "--changed-loc", "500")
        self.assertEqual(result.returncode, 1, msg=result.stdout + result.stderr)
        self.assertIn("CHUNK SCHEDULE", result.stdout)
        self.assertIn("BLOCKING FINDINGS", result.stdout)
        self.assertIn("blocked:", result.stdout)

    def test_any_blocking_finding_refuses_receipt_before_terminal(self):
        cases = [
            self.base_args("--emit-receipt", "--owner", "h",
                           "--changed-loc", "500"),
            ("--goal", "add fixture widget", "--risk", "r1_routine",
             "--changed-loc", "42", "--emit-receipt", "--owner", "h"),
        ]
        for case in cases:
            result = self.run_tool(*case)
            self.assertEqual(result.returncode, 2,
                             msg=result.stdout + result.stderr)
            self.assertIn("blocking findings are open", result.stderr)
        self.assertEqual(list((self.workspace / "reviews").iterdir()), [])

    def test_negative_changed_loc_is_refused_before_composition(self):
        result = self.run_tool("--goal", "add fixture widget", "--risk",
                               "r2_guarded", "--rollback", "git revert HEAD",
                               "--changed-loc=-1")
        self.assertEqual(result.returncode, 2, msg=result.stdout + result.stderr)
        self.assertIn("must be zero or positive", result.stderr)
        self.assertNotIn("REVIEW BRIEF", result.stdout)
        self.assertFalse(
            (self.workspace / "runs" / "review_brief_runs.v1.jsonl").exists(),
            msg="a refused invocation must not enter the metrics record")

    def test_signoff_id_rejects_identity_or_authority_text(self):
        result = self.run_tool(
            *self.base_args("--signoff-id", "approver=alice@example.com"))
        self.assertEqual(result.returncode, 2,
                         msg=result.stdout + result.stderr)
        self.assertIn("--signoff-id must be", result.stderr)
        self.assertFalse(
            (self.workspace / "runs" / "review_brief_runs.v1.jsonl").exists())

    def test_task_path_refuses_repository_escape(self):
        for path in ("/", "/tmp/outside.py", "../outside.py", "."):
            with self.subTest(path=path):
                result = self.run_tool(*self.base_args("--path", path))
                self.assertEqual(result.returncode, 2,
                                 msg=result.stdout + result.stderr)
                self.assertIn("invalid task path", result.stderr)

    @unittest.skipUnless(hasattr(os, "forkpty"), "pty required")
    def test_pty_receipt_flow_writes_exactly_one_receipt(self):
        """Positive control: the pty harness really can produce a receipt, so
        'no receipt' in the negative tests below means something."""
        code, output = self.run_tool_pty(
            self.base_args("--emit-receipt", "--owner", "human_owner",
                           "--risk", "r2_guarded"),
            replies="\napprove\nadded_check\n")
        self.assertEqual(code, 0, msg=output)
        self.assertIn("receipt written:", output)
        self.assertEqual(len(list((self.workspace / "reviews").iterdir())), 1)
        record = self.last_run_record()
        self.assertEqual(record["record_kind"], "signoff")
        self.assertTrue(record["brief_consulted"])
        self.assertEqual(record["judgment"], "approve")
        self.assertEqual(record["observable_action"], "added_check")
        self.assertEqual(record["observable_action_source"],
                         "operator_declared_unauthenticated")
        self.assertEqual(record["interaction_channel"], "tty")
        self.assertEqual(record["authentication"], "none")
        self.assertEqual(record["consultation_claim"], "display_proxy_only")
        self.assertTrue(record["receipt"].startswith("reviews/"))
        self.assertNotIn(str(self.workspace), record["receipt"])
        metrics = subprocess.run(
            [sys.executable, str(METRICS_TOOL), "--workspace",
             str(self.workspace), "--format", "json"],
            capture_output=True, text=True)
        self.assertEqual(metrics.returncode, 3,
                         msg=metrics.stdout + metrics.stderr)
        report = json.loads(metrics.stdout)
        self.assertEqual(report["verdict"], "INSUFFICIENT_DATA")
        self.assertEqual(report["admissible"]["signoff"], 1,
                         msg=metrics.stdout)
        self.assertEqual(
            report["integrity"]["distinct_receipt_packet_uids"], 1)
        self.assertEqual(report["excluded"], {})

    @unittest.skipUnless(hasattr(os, "forkpty"), "pty required")
    def test_negative_changed_loc_yields_no_receipt_on_a_pty(self):
        code, output = self.run_tool_pty(
            ("--goal", "add fixture widget", "--risk", "r2_guarded",
             "--rollback", "git revert HEAD", "--changed-loc=-1",
             "--emit-receipt", "--owner", "human_owner"),
            replies="\napprove\nadded_check\n")
        self.assertEqual(code, 2, msg=output)
        self.assertIn("must be zero or positive", output)
        self.assertEqual(list((self.workspace / "reviews").iterdir()), [])

    def test_context_cap_overflow_blocks_receipt(self):
        sources = []
        for i in range(10):
            name = f"ctx_note_{i}.md"
            (self.repo / name).write_text("fixture context\n", encoding="utf-8")
            sources += ["--source", name]
        result = self.run_tool(*self.base_args(*sources, "--emit-receipt",
                                               "--owner", "h"))
        self.assertEqual(result.returncode, 2, msg=result.stdout + result.stderr)
        self.assertIn("blocking findings are open", result.stderr)
        self.assertIn("context-source cap reached", result.stderr)

    def test_unknown_changed_loc_is_blocking(self):
        result = self.run_tool("--goal", "add fixture widget",
                               "--risk", "r1_routine",
                               "--rollback", "git revert HEAD",
                               "--path", "src/widget.py")
        self.assertEqual(result.returncode, 1, msg=result.stdout + result.stderr)
        self.assertIn("changed lines unknown", result.stdout)
        self.assertIn("blocked:", result.stdout)

    def test_missing_rollback_is_blocking(self):
        result = self.run_tool("--goal", "add fixture widget",
                               "--risk", "r1_routine", "--changed-loc", "42")
        self.assertEqual(result.returncode, 1, msg=result.stdout + result.stderr)
        self.assertIn("rollback path missing", result.stdout)
        self.assertIn("BLOCKING FINDINGS", result.stdout)

    def test_checks_are_capped_at_seven_typed_items(self):
        acceptance = []
        for i in range(9):
            acceptance += ["--acceptance", f"criterion number {i} holds"]
        result = self.run_tool(*self.base_args(*acceptance))
        self.assertEqual(result.returncode, 1, msg=result.stdout + result.stderr)
        self.assertEqual(result.stdout.count("- [READ-DO]"), 6)
        self.assertEqual(result.stdout.count("- [DO-CONFIRM]"), 1)
        self.assertIn("check overflow", result.stdout)

    def test_word_cap_preserves_all_seven_headings(self):
        acceptance = []
        for i in range(12):
            acceptance += ["--acceptance",
                           f"very long acceptance criterion number {i} " +
                           "with many additional trailing words " * 8]
        result = self.run_tool(*self.base_args(*acceptance))
        self.assertLessEqual(len(result.stdout.split()), 600,
                             msg="brief exceeded the 600-word cap")
        for heading in SECTION_HEADINGS:
            self.assertIn(heading, result.stdout,
                          msg=f"heading lost under load: {heading}")

    def test_section_budget_drops_parent_and_children_atomically(self):
        groups = [
            ["1. EVIDENCE"],
            ["   retained finding"],
            ["   DISCONFIRM parent with enough words to exceed budget",
             "     reopen: child must never survive alone"],
        ]
        rendered = compose_review_brief.fit_section(groups, budget=15)
        self.assertIn("   retained finding", rendered)
        self.assertNotIn(
            "   DISCONFIRM parent with enough words to exceed budget",
            rendered)
        self.assertNotIn("     reopen: child must never survive alone",
                         rendered)
        self.assertIn("groups omitted", rendered[-1])

    def test_section_budget_preserves_finding_priority_as_prefix(self):
        groups = [
            ["1. EVIDENCE"],
            ["   DISCONFIRM [EXACT_PATH] rejection first"],
            ["   DISCONFIRM [EXACT_PATH] rejection second with detail",
             "     reopen: a condition that makes this group too large"],
            ["   DISCONFIRM [STRONG_KEYWORD] lesson short"],
        ]
        rendered = compose_review_brief.fit_section(groups, budget=20)
        joined = "\n".join(rendered)
        self.assertIn("rejection first", joined)
        self.assertNotIn("rejection second", joined)
        self.assertNotIn("lesson short", joined)
        self.assertIn("highest-tier=EXACT_PATH", rendered[-1])

    def test_trimmed_line_preserves_visual_nesting(self):
        text = "     reopen: " + "word " * 30
        self.assertTrue(compose_review_brief.trim_line(text).startswith(
            "     reopen:"))

    def test_ancestor_instruction_files_are_read_and_declared(self):
        (self.repo / "AGENTS.md").write_text("fixture agents guidance\n",
                                             encoding="utf-8")
        sub = self.repo / "src"
        sub.mkdir()
        (sub / "CLAUDE.md").write_text("fixture local guidance\n",
                                       encoding="utf-8")
        result = self.run_tool(*self.base_args("--path", "src/widget.py"),
                               "--changed-loc", "42")
        self.assertIn("task context read: AGENTS.md, src/CLAUDE.md",
                      result.stdout)
        self.assertIn("relevance query: goal + acceptance only", result.stdout)

    def test_instruction_text_does_not_overwhelm_task_relevance(self):
        (self.repo / "AGENTS.md").write_text(
            "adopt giant orchestration framework wholesale\n",
            encoding="utf-8",
        )
        result = self.run_tool(*self.base_args("--path", "src/widget.py"))
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertNotIn("ADVISORY FINDINGS", result.stdout)
        self.assertIn("relevance query: goal + acceptance only", result.stdout)

    def test_query_provenance_excludes_context_content(self):
        (self.repo / "AGENTS.md").write_text(
            "unique_context_token orchestration framework\n",
            encoding="utf-8",
        )
        args = make_args(path=["src/widget.py"])
        model, errors = compose_review_brief.compose(args, self.repo)
        self.assertEqual(errors, [])
        self.assertEqual(model["query_provenance"],
                         "goal_and_acceptance_only")
        self.assertNotIn("unique", model["query_tokens"])
        self.assertNotIn("context", model["query_tokens"])

    def test_broken_memory_evidence_is_scoped_and_rendered_stale(self):
        memory_dir = self.repo / "07_working" / "memory_fixture"
        memory_dir.mkdir()
        (memory_dir / "missing_source.v0.yaml").write_text(
            "packet_type: memory_packet\n"
            "packet_uid: fixture_missing_source\n"
            "source_refs:\n"
            "  - source_path: src/missing_widget.py\n",
            encoding="utf-8",
        )
        result = self.run_tool(*self.base_args(
            "--path", "src/missing_widget.py"))
        self.assertEqual(result.returncode, 1,
                         msg=result.stdout + result.stderr)
        self.assertIn("STALE fixture_missing_source: broken_reference",
                      result.stdout)

    def test_memory_path_substring_does_not_create_false_scope(self):
        memory_dir = self.repo / "07_working" / "memory_fixture"
        memory_dir.mkdir()
        (memory_dir / "similar_source.v0.yaml").write_text(
            "packet_type: memory_packet\n"
            "packet_uid: fixture_similar_source\n"
            "source_refs:\n"
            "  - source_path: src/widget_backup.py\n",
            encoding="utf-8",
        )
        args = make_args(path=["src/widget.py"])
        model, errors = compose_review_brief.compose(args, self.repo)
        self.assertEqual(errors, [])
        self.assertEqual(model["memory_findings"], [])
        self.assertEqual(model["memory_out_of_scope"], 1)

    def test_markdown_links_are_followed_one_hop_only(self):
        (self.repo / "start.md").write_text("see [hop1](hop_one.md)\n",
                                            encoding="utf-8")
        (self.repo / "hop_one.md").write_text("see [hop2](hop_two.md)\n",
                                              encoding="utf-8")
        (self.repo / "hop_two.md").write_text("too far\n", encoding="utf-8")
        result = self.run_tool(*self.base_args("--source", "start.md"))
        self.assertIn("hop_one.md", result.stdout)
        self.assertNotIn("hop_two.md", result.stdout)

    def test_emit_receipt_without_terminal_refuses_and_writes_nothing(self):
        result = self.run_tool(*self.base_args("--emit-receipt",
                                               "--owner", "human_owner"),
                               detach=True)
        self.assertEqual(result.returncode, 2, msg=result.stdout + result.stderr)
        self.assertIn("refuses non-interactive execution", result.stderr)
        self.assertEqual(list((self.workspace / "reviews").iterdir()), [])

    def test_json_mode_withholds_recommendation(self):
        result = self.run_tool(*self.base_args("--format", "json"))
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertNotIn("recommendation", payload)
        self.assertTrue(payload["recommendation_withheld"])

    def test_refused_json_receipt_does_not_create_signoff_salt(self):
        result = self.run_tool(*self.base_args(
            "--format", "json", "--emit-receipt", "--owner", "human_owner",
            "--signoff-id", "ticket-4417"))
        self.assertEqual(result.returncode, 2,
                         msg=result.stdout + result.stderr)
        self.assertFalse((self.workspace / ".signoff_salt").exists())

    def test_workspace_inside_repo_is_rejected(self):
        inner = self.repo / "workspace"
        (inner / "reviews").mkdir(parents=True)
        (inner / "runs").mkdir()
        result = subprocess.run(
            [sys.executable, str(TOOL), "--repo", str(self.repo),
             "--workspace", str(inner), *self.base_args()],
            capture_output=True, text=True, stdin=subprocess.DEVNULL,
        )
        self.assertEqual(result.returncode, 2, msg=result.stdout + result.stderr)
        self.assertIn("outside the repository", result.stderr)

    def test_run_record_carries_all_kill_condition_fields(self):
        self.run_tool(*self.base_args("--signoff-id", "signoff-42"))
        record = self.last_run_record()
        for field in ("record_kind", "run_id", "signoff_id",
                      "eligible_signoff", "brief_consulted", "judgment",
                      "observable_action", "compose_ms", "triage_ms",
                      "brief_displayed", "interaction_channel",
                      "authentication", "judgment_source",
                      "observable_action_source", "exit_code"):
            self.assertIn(field, record)
        self.assertEqual(record["record_kind"], "preview")
        self.assertEqual(record["record_version"], "review_brief_run.v1")
        salt_path = self.workspace / ".signoff_salt"
        salt = salt_path.read_bytes()
        self.assertEqual(
            record["signoff_id"],
            compose_review_brief.opaque_signoff_id(
                "signoff-42", "unused", salt))
        self.assertNotIn("signoff-42", record["signoff_id"])
        self.assertEqual(len(salt), 32)
        self.assertEqual(salt_path.stat().st_mode & 0o077, 0)
        self.assertFalse(record["eligible_signoff"])  # r1 is not eligible
        self.assertEqual(record["judgment"], "none")
        self.assertEqual(record["observable_action"], "not_applicable")
        self.assertEqual(record["interaction_channel"], "stdout")
        self.assertEqual(record["authentication"], "none")

    def test_declared_signoff_id_is_stable_only_within_one_workspace(self):
        first_salt = compose_review_brief.load_or_create_signoff_salt(
            self.workspace)
        first = compose_review_brief.opaque_signoff_id(
            "ticket-4417", "unused", first_salt)
        repeated = compose_review_brief.opaque_signoff_id(
            "ticket-4417", "unused", first_salt)
        with tempfile.TemporaryDirectory() as other_tmp:
            other = Path(other_tmp)
            second_salt = compose_review_brief.load_or_create_signoff_salt(
                other)
            second = compose_review_brief.opaque_signoff_id(
                "ticket-4417", "unused", second_salt)
        self.assertEqual(first, repeated)
        self.assertNotEqual(first, second)
        self.assertNotIn(b"ticket-4417", first_salt)

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO support required")
    def test_fifo_signoff_salt_is_rejected_without_blocking(self):
        os.mkfifo(self.workspace / ".signoff_salt", 0o600)
        result = self.run_tool(
            *self.base_args("--signoff-id", "ticket-4417"), timeout=3)
        self.assertEqual(result.returncode, 2,
                         msg=result.stdout + result.stderr)
        self.assertIn("not a regular file", result.stderr)

    def test_refused_receipt_attempts_never_claim_brief_consultation(self):
        """A refusal is not a sign-off and is not a consultation; recording it
        as either corrupts both sides of the kill-condition ratio."""
        blocked = self.run_tool(*self.base_args("--emit-receipt", "--owner",
                                                "h", "--changed-loc", "500"))
        self.assertEqual(blocked.returncode, 2,
                         msg=blocked.stdout + blocked.stderr)
        record = self.last_run_record()
        self.assertEqual(record["record_kind"], "signoff_attempt")
        self.assertFalse(record["brief_consulted"])
        self.assertEqual(record["judgment"], "none")

        headless = self.run_tool(*self.base_args("--emit-receipt", "--owner",
                                                 "h"), detach=True)
        self.assertEqual(headless.returncode, 2,
                         msg=headless.stdout + headless.stderr)
        record = self.last_run_record()
        self.assertEqual(record["record_kind"], "signoff_attempt")
        self.assertFalse(record["brief_consulted"])
        self.assertEqual(record["judgment"], "none")
        self.assertEqual(list((self.workspace / "reviews").iterdir()), [])

    @unittest.skipUnless(hasattr(os, "forkpty"), "pty required")
    def test_cancelled_judgment_records_consultation_but_no_signoff(self):
        code, output = self.run_tool_pty(
            self.base_args("--emit-receipt", "--owner", "human_owner"),
            replies="\n\n")
        self.assertEqual(code, 0, msg=output)
        self.assertIn("cancelled; no receipt written", output)
        self.assertEqual(list((self.workspace / "reviews").iterdir()), [])
        record = self.last_run_record()
        self.assertEqual(record["record_kind"], "signoff_attempt")
        self.assertTrue(record["brief_consulted"])
        self.assertEqual(record["judgment"], "cancelled")
        self.assertEqual(record["interaction_channel"], "tty")
        self.assertEqual(record["authentication"], "none")

    def test_record_skip_logs_eligible_signoff_without_consultation(self):
        result = self.run_tool("--record-skip", "--risk", "r2_guarded")
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        record = self.last_run_record()
        self.assertEqual(record["record_kind"], "skip")
        self.assertTrue(record["eligible_signoff"])
        self.assertFalse(record["brief_consulted"])

    def test_receipt_rejects_unknown_selected_finding_ids(self):
        args = make_args()
        model, errors = compose_review_brief.compose(args, self.repo)
        self.assertEqual(errors, [])
        with self.assertRaises(ValueError):
            compose_review_brief.build_receipt(
                model, args, "approve", ["fake-finding-id"],
                compose_review_brief.utc_now(), self.repo)

    def test_receipt_rejects_unconfirmed_weak_match_as_judgment_basis(self):
        args = make_args(goal="improve framework docs")
        model, errors = compose_review_brief.compose(args, self.repo)
        self.assertEqual(errors, [])
        self.assertTrue(model["guard_weak"])
        weak_id = model["guard_weak"][0]["record_id"]
        with self.assertRaises(ValueError):
            compose_review_brief.build_receipt(
                model, args, "approve", [weak_id],
                compose_review_brief.utc_now(), self.repo)

    def test_receipt_is_honest_validator_clean_and_collision_safe(self):
        (self.repo / "widget.py").write_text("print('fixture')\n",
                                             encoding="utf-8")
        args = make_args(path=["widget.py"])
        model, errors = compose_review_brief.compose(args, self.repo)
        self.assertEqual(errors, [])
        receipt = compose_review_brief.build_receipt(
            model, args, "approve", [], compose_review_brief.utc_now(),
            self.repo)
        self.assertEqual(receipt["status"], "approved")
        self.assertIn("interaction_channel:tty", receipt["tags"])
        self.assertIn("authentication:none", receipt["tags"])
        self.assertNotIn("review_mode:direct_human_evaluation", receipt["tags"])
        self.assertNotIn("signed_by", receipt)
        hash_refs = [r for r in receipt["source_refs"]
                     if r.get("relation") == "reviewed_bytes"]
        self.assertEqual(len(hash_refs[0]["source_hash"]), 64)
        path1, error1 = compose_review_brief.finalize_receipt(
            receipt, self.workspace)
        self.assertIsNone(error1, msg=error1)
        path2, error2 = compose_review_brief.finalize_receipt(
            receipt, self.workspace)
        self.assertIsNone(path2)
        self.assertIn("collision refused", error2)
        self.assertEqual(len(list((self.workspace / "reviews").iterdir())), 1)

    @unittest.skipUnless(shutil.which("git"), "git not available")
    def test_untracked_directory_files_count_toward_the_budget(self):
        self.init_git()
        newdir = self.repo / "newdir"
        newdir.mkdir()
        (newdir / "big_new_file.py").write_text("x = 1\n" * 450,
                                                encoding="utf-8")
        result = self.run_tool("--goal", "add fixture widget",
                               "--risk", "r1_routine",
                               "--rollback", "git revert HEAD",
                               "--path", "newdir")
        self.assertEqual(result.returncode, 1, msg=result.stdout + result.stderr)
        self.assertIn("over budget: 450", result.stdout)

    @unittest.skipUnless(shutil.which("git"), "git not available")
    def test_tracked_binary_modification_is_blocking_not_zero(self):
        self.init_git()
        blob = self.repo / "asset.bin"
        blob.write_bytes(b"\x00\x01\x02\x03")
        subprocess.run(["git", "-C", str(self.repo), "add", "asset.bin"],
                       check=True)
        subprocess.run(["git", "-C", str(self.repo), "-c", "user.email=t@t",
                        "-c", "user.name=t", "commit", "-q", "-m", "bin"],
                       check=True)
        blob.write_bytes(b"\x00\x01\x02\x03\x04\x05")
        result = self.run_tool("--goal", "add fixture widget",
                               "--risk", "r1_routine",
                               "--rollback", "git revert HEAD",
                               "--path", "asset.bin")
        self.assertEqual(result.returncode, 1, msg=result.stdout + result.stderr)
        self.assertIn("binary change blocks the unit", result.stdout)
        self.assertIn("blocked:", result.stdout)


if __name__ == "__main__":
    unittest.main()
