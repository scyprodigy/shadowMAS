#!/usr/bin/env python3
"""Minimal shadowMAS L2 handoff fixture inspector. This is a fixture schema check, not a runtime engine."""

import json
import sys
from pathlib import Path


REQUIRED_TOP_KEYS = (
    "fixture_id",
    "title",
    "level",
    "authority_layers_involved",
    "trace_steps",
    "expected_boundary_violation",
    "expected_safe_behavior",
    "non_claims",
)
REQUIRED_TRANSITION_KEYS = ("source_layer", "target_layer", "relation")

HUMAN_SUMMARY_EN_PASS = "fixture inspection passed"
HUMAN_SUMMARY_EN_FAIL = "fixture inspection failed"
# zh-TW summaries are assembled from explicit codepoints so this machine-facing
# source file stays ASCII-only per repository language policy. They render as
# readable zh-TW characters at runtime through json.dumps(..., ensure_ascii=False).
HUMAN_SUMMARY_ZH_PASS = "fixture " + "".join(
    chr(c) for c in (0x6AA2, 0x8996, 0x901A, 0x904E)
)
HUMAN_SUMMARY_ZH_FAIL = "fixture " + "".join(
    chr(c) for c in (0x6AA2, 0x8996, 0x5931, 0x6557)
)


def _fail_envelope(violations, *, checked_rules=None, fixture_id=None, title=None):
    return {
        "fixture_id": fixture_id,
        "title": title,
        "status": "fail",
        "checked_rules": list(checked_rules or []),
        "violations": list(violations),
        "transition": None,
        "human_summary_en": HUMAN_SUMMARY_EN_FAIL,
        "human_summary_zh": HUMAN_SUMMARY_ZH_FAIL,
    }


def inspect_l2_fixture(path):
    """Inspect one L2 handoff fixture JSON file and return a report dict."""
    try:
        raw = Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        return _fail_envelope(
            [f"file_unreadable: {exc.__class__.__name__}"],
            checked_rules=["load_json"],
        )

    try:
        fixture = json.loads(raw)
    except json.JSONDecodeError as exc:
        return _fail_envelope(
            [f"invalid_json: {exc.msg} at line {exc.lineno} column {exc.colno}"],
            checked_rules=["load_json"],
        )

    if not isinstance(fixture, dict):
        return _fail_envelope(
            ["fixture_root_must_be_object"],
            checked_rules=["load_json"],
        )

    fixture_id = fixture.get("fixture_id")
    title = fixture.get("title")
    violations = []
    checked_rules = ["load_json"]

    checked_rules.append("required_top_level_keys")
    missing = [k for k in REQUIRED_TOP_KEYS if k not in fixture]
    if missing:
        violations.append(f"missing_required_keys: {sorted(missing)}")

    checked_rules.append("level_is_L2")
    if fixture.get("level") != "L2":
        violations.append(f"level_must_be_L2: got {fixture.get('level')!r}")

    checked_rules.append("authority_layers_match_trace_step_layers")
    declared = set(fixture.get("authority_layers_involved") or [])
    raw_steps = fixture.get("trace_steps") or []
    step_layers = {
        step.get("authority_layer")
        for step in raw_steps
        if isinstance(step, dict)
    }
    if declared != step_layers:
        violations.append(
            "authority_layer_set_mismatch: "
            f"in_steps_not_declared={sorted(step_layers - declared)}, "
            f"declared_not_in_steps={sorted(declared - step_layers)}"
        )

    checked_rules.append("unsafe_transition_object_shape")
    violation_obj = fixture.get("expected_boundary_violation")
    transition_raw = (
        violation_obj.get("unsafe_transition")
        if isinstance(violation_obj, dict)
        else None
    )

    transition = None
    if not isinstance(transition_raw, dict):
        violations.append("unsafe_transition_must_be_object")
    else:
        keyset = set(transition_raw.keys())
        expected = set(REQUIRED_TRANSITION_KEYS)
        if keyset != expected:
            violations.append(
                "unsafe_transition_keys_must_be_exactly: "
                f"expected={sorted(expected)}, got={sorted(keyset)}"
            )

        checked_rules.append("relation_is_unsafe_promotion")
        if transition_raw.get("relation") != "unsafe_promotion":
            violations.append(
                f"relation_must_be_unsafe_promotion: got {transition_raw.get('relation')!r}"
            )

        source_layer = transition_raw.get("source_layer")
        target_layer = transition_raw.get("target_layer")

        checked_rules.append("transition_layers_in_trace_steps")
        if source_layer not in step_layers:
            violations.append(f"source_layer_not_in_trace_steps: {source_layer!r}")
        if target_layer not in step_layers:
            violations.append(f"target_layer_not_in_trace_steps: {target_layer!r}")

        checked_rules.append("transition_source_differs_from_target")
        if source_layer == target_layer:
            violations.append(f"source_and_target_layers_must_differ: {source_layer!r}")

        transition = {
            "source_layer": source_layer,
            "target_layer": target_layer,
            "relation": transition_raw.get("relation"),
        }

    if violations:
        return _fail_envelope(
            violations,
            checked_rules=checked_rules,
            fixture_id=fixture_id,
            title=title,
        )

    return {
        "fixture_id": fixture_id,
        "title": title,
        "status": "pass",
        "checked_rules": checked_rules,
        "violations": [],
        "transition": transition,
        "human_summary_en": HUMAN_SUMMARY_EN_PASS,
        "human_summary_zh": HUMAN_SUMMARY_ZH_PASS,
    }


def main(argv):
    if len(argv) != 2:
        report = _fail_envelope(
            ["usage: inspect_l2_fixture.py <path_to_l2_fixture.json>"],
            checked_rules=["usage"],
        )
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 1

    report = inspect_l2_fixture(argv[1])
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
