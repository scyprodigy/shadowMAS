#!/usr/bin/env python3
"""One-command snapshot of shadowMAS authority-boundary health.

Read-only. ADVISORY. This is a thin orchestrator: it runs the existing
read-only checkers and presents a single consolidated view, so an owner or
agent can see the shadow's trust state in one screen instead of running each
tool by hand. It owns no check logic; each underlying tool remains the source
of truth, and CI keeps running them as separate gated steps with clearer
per-step failures.

It reports, in one place:
- anchor drift (landing-file consistency)
- compiled-surface freshness (rationale index, DO-NOT-REDO)
- memory validity (ghost-dependency findings)
- packet reference integrity (dangling edges)
- the pending review agenda (informational, never a finding)

Usage:
  python3 tools/audit_shadow_state.py
  python3 tools/audit_shadow_state.py --generation <id>   # also flag generation staleness

Exit: 0 = no advisory findings; 1 = at least one check reported findings;
      2 = a check could not run.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def last_meaningful_line(text: str) -> str:
    lines = [ln for ln in text.splitlines() if ln.strip()]
    return lines[-1] if lines else "(no output)"


def run_check(label: str, command: list[str]) -> tuple[str, int, str]:
    proc = subprocess.run(command, cwd=REPO, capture_output=True, text=True)
    summary = last_meaningful_line(proc.stdout) or last_meaningful_line(proc.stderr)
    return label, proc.returncode, summary


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Consolidated shadowMAS authority-boundary health snapshot.")
    parser.add_argument("--generation", help="current model/runtime generation id for staleness check")
    args = parser.parse_args(argv)

    py = sys.executable
    memory_cmd = [py, "tools/check_memory_validity.py"]
    if args.generation:
        memory_cmd += ["--generation", args.generation]

    checks = [
        run_check("anchor drift", [py, "tools/check_anchor_drift.py"]),
        run_check("rationale index freshness", [py, "tools/build_rationale_index.py", "--check"]),
        run_check("do-not-redo freshness", [py, "tools/build_rework_guard.py", "--check"]),
        run_check("memory validity", memory_cmd),
        run_check("packet reference integrity", [py, "tools/check_packet_refs.py"]),
    ]

    setup_error = any(code == 2 for _, code, _ in checks)
    findings = any(code == 1 for _, code, _ in checks)

    print("shadowMAS authority-boundary health\n")
    width = max(len(label) for label, _, _ in checks)
    for label, code, summary in checks:
        mark = {0: "PASS", 1: "FINDING", 2: "ERROR"}.get(code, "?")
        print(f"  [{mark:7}] {label:<{width}}  {summary}")

    # review agenda is informational context, not a pass/fail signal;
    # its summary is the first line ("review agenda: N pending ...")
    agenda = subprocess.run([py, "tools/order_review_queue.py"], cwd=REPO,
                            capture_output=True, text=True)
    agenda_lines = [ln for ln in agenda.stdout.splitlines() if ln.strip()]
    agenda_summary = agenda_lines[0] if agenda_lines else "(no output)"
    print(f"\n  review queue: {agenda_summary}")
    print("  (run tools/order_review_queue.py for the full agenda)")

    print()
    if setup_error:
        print("RESULT: ERROR — a check could not run")
        return 2
    if findings:
        print("RESULT: FINDINGS — see the FINDING rows above; human review decides")
        return 1
    print("RESULT: OK — no authority-boundary findings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
