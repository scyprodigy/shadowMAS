#!/usr/bin/env python3
"""Minimal shadowMAS governance validator. This is a demo, not a runtime engine."""

import json
import sys


_MISSING = object()


def get_path(data, path):
    current = data
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return _MISSING
        current = current[key]
    return current


def build_invariants(data):
    return [
        {
            "invariant_name": "runtime_signal_truth_status_runtime_only",
            "human_readable_summary": "runtime signal truth_status remains runtime_signal_only",
            "predicate": lambda: get_path(data, ["runtime_signal", "truth_status"]) == "runtime_signal_only",
        },
        {
            "invariant_name": "runtime_signal_cannot_promote_truth_directly",
            "human_readable_summary": "runtime signal cannot promote truth directly",
            "predicate": lambda: get_path(data, ["runtime_signal", "may_promote_to_truth_directly"]) is False,
        },
        {
            "invariant_name": "runtime_signal_cannot_write_memory_directly",
            "human_readable_summary": "runtime signal cannot write memory directly",
            "predicate": lambda: get_path(data, ["runtime_signal", "may_write_to_memory_directly"]) is False,
        },
        {
            "invariant_name": "runtime_signal_requires_human_review_for_promotion",
            "human_readable_summary": "runtime signal requires human review for promotion",
            "predicate": lambda: get_path(data, ["runtime_signal", "requires_human_review_for_promotion"]) is True,
        },
        {
            "invariant_name": "no_t4_t5_to_t2_t3_direct_promotion",
            "human_readable_summary": "T4/T5 signals cannot directly promote into T2/T3",
            "predicate": lambda: get_path(data, ["expected_boundary", "no_t4_t5_to_t2_t3_direct_promotion"]) is True,
        },
        {
            "invariant_name": "no_silent_memory_write",
            "human_readable_summary": "runtime signals cannot silently write memory",
            "predicate": lambda: get_path(data, ["expected_boundary", "no_silent_memory_write"]) is True,
        },
        {
            "invariant_name": "audit_projection_is_read_only",
            "human_readable_summary": "audit projection is read-only",
            "predicate": lambda: get_path(data, ["audit_projection", "read_only"]) is True,
        },
        {
            "invariant_name": "audit_projection_has_no_approval_authority",
            "human_readable_summary": "audit projection has no approval authority",
            "predicate": lambda: get_path(data, ["audit_projection", "approval_authority"]) is False,
        },
        {
            "invariant_name": "audit_projection_has_no_truth_authority",
            "human_readable_summary": "audit projection has no truth authority",
            "predicate": lambda: get_path(data, ["audit_projection", "truth_authority"]) is False,
        },
        {
            "invariant_name": "recommended_action_is_advisory_only",
            "human_readable_summary": "recommended_action is advisory only",
            "predicate": lambda: get_path(data, ["audit_projection", "recommended_action", "advisory_only"]) is True,
        },
        {
            "invariant_name": "recommended_action_cannot_authorize_runtime_action",
            "human_readable_summary": "recommended_action cannot authorize runtime action",
            "predicate": lambda: get_path(data, ["audit_projection", "recommended_action", "may_authorize_runtime_action_by_itself"]) is False,
        },
        {
            "invariant_name": "recommended_action_cannot_authorize_packet_change",
            "human_readable_summary": "recommended_action cannot authorize packet change",
            "predicate": lambda: get_path(data, ["audit_projection", "recommended_action", "may_authorize_packet_change"]) is False,
        },
        {
            "invariant_name": "recommended_action_cannot_promote_truth",
            "human_readable_summary": "recommended_action cannot promote truth",
            "predicate": lambda: get_path(data, ["audit_projection", "recommended_action", "may_promote_truth"]) is False,
        },
        {
            "invariant_name": "dashboard_does_not_become_authority",
            "human_readable_summary": "dashboard does not become authority",
            "predicate": lambda: get_path(data, ["expected_boundary", "no_dashboard_authority"]) is True,
        },
        {
            "invariant_name": "human_final_authority_preserved",
            "human_readable_summary": "human final authority is preserved",
            "predicate": lambda: get_path(data, ["expected_boundary", "human_final_authority_preserved"]) is True,
        },
    ]


def check(invariant):
    line = f"{invariant['invariant_name']} - {invariant['human_readable_summary']}"
    if invariant["predicate"]():
        print(f"PASS: {line}")
        return True
    print(f"FAIL: {line}")
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

    results = [check(invariant) for invariant in build_invariants(data)]

    return 0 if all(results) else 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: shadowmas_minimal_validator.py <demo.json>")
        sys.exit(1)
    sys.exit(main(sys.argv[1]))
