#!/usr/bin/env python3
"""Minimal shadowMAS governance validator. This is a demo, not a runtime engine."""

import json
import sys


def check(label, condition, fail_reason):
    if condition:
        print(f"PASS: {label}")
        return True
    print(f"FAIL: {fail_reason}")
    return False


def main(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        print(f"FAIL: demo file not found: {path}")
        return 1
    except json.JSONDecodeError as exc:
        print(f"FAIL: invalid JSON ({exc})")
        return 1

    rs = data.get("runtime_signal", {})
    ap = data.get("audit_projection", {})
    ra = ap.get("recommended_action", {})
    eb = data.get("expected_boundary", {})

    results = []

    results.append(check(
        "runtime signal remains non-authoritative",
        rs.get("truth_status") == "runtime_signal_only"
        and rs.get("may_promote_to_truth_directly") is False
        and rs.get("may_write_to_memory_directly") is False
        and rs.get("requires_human_review_for_promotion") is True,
        "runtime_signal authority flags do not match non-authoritative contract",
    ))

    results.append(check(
        "no T4/T5 to T2/T3 promotion",
        eb.get("no_t4_t5_to_t2_t3_direct_promotion") is True,
        "expected_boundary.no_t4_t5_to_t2_t3_direct_promotion is not True",
    ))

    results.append(check(
        "no silent memory write",
        eb.get("no_silent_memory_write") is True,
        "expected_boundary.no_silent_memory_write is not True",
    ))

    results.append(check(
        "audit projection has no approval authority",
        ap.get("read_only") is True
        and ap.get("approval_authority") is False
        and ap.get("truth_authority") is False,
        "audit_projection authority flags do not match read-only contract",
    ))

    results.append(check(
        "recommended_action is advisory only",
        ra.get("advisory_only") is True
        and ra.get("may_authorize_runtime_action_by_itself") is False
        and ra.get("may_authorize_packet_change") is False
        and ra.get("may_promote_truth") is False,
        "recommended_action carries authority beyond advisory",
    ))

    results.append(check(
        "human final authority preserved",
        eb.get("human_final_authority_preserved") is True
        and eb.get("no_dashboard_authority") is True,
        "human final authority or no_dashboard_authority not preserved",
    ))

    return 0 if all(results) else 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: shadowmas_minimal_validator.py <demo.json>")
        sys.exit(1)
    sys.exit(main(sys.argv[1]))
