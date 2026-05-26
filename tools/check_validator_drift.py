#!/usr/bin/env python3
"""Compare validator hardcoded constants against packet yaml schemas.

The validator (05_scripts/validate/shadowmas_validate.py) hardcodes
Python sets/lists that mirror what the packet yaml schemas declare.
The two surfaces are maintained by hand. This checker catches when
they drift apart.

Checked surfaces:
  - PACKET_TYPES                    <-> packet_common_shell.packet_type.allowed
  - SHARED_REQUIRED                 <-> packet_common_shell.required_shared_fields keys
  - FAMILY_REQUIRED[family]         <-> {task,memory,review}_packet.required_fields keys
  - STATUS_VALUES[family]           <-> {task,memory,review}_packet.allowed_status_values
  - SUPERVISION_MODE_VALUES         <-> packet_common_shell.supervision_mode.allowed
  - RISK_VALUES                     <-> packet_common_shell.risk.allowed
  - REVIEW_RECOMMENDATION_VALUES    <-> review_packet.recommendation.allowed
  - PROMOTION_CANDIDATE_VALUES      <-> memory_packet.promotion_candidate.allowed

Exit codes:
  0  no drift
  1  drift detected on one or more surfaces
  2  usage / file / parse error

Usage:
  python3 tools/check_validator_drift.py
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent
VALIDATOR_PATH = REPO_ROOT / "05_scripts" / "validate" / "shadowmas_validate.py"
SHELL_PATH = REPO_ROOT / "02_packets" / "packet_common_shell.v0.yaml"
TASK_PATH = REPO_ROOT / "02_packets" / "task_packet.v0.yaml"
MEMORY_PATH = REPO_ROOT / "02_packets" / "memory_packet.v0.yaml"
REVIEW_PATH = REPO_ROOT / "02_packets" / "review_packet.v0.yaml"


def load_validator():
    module_name = "shadowmas_validator_drift_import"
    spec = importlib.util.spec_from_file_location(module_name, VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    # Register before exec so @dataclass can resolve cls.__module__ via sys.modules.
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def load_yaml_file(path: Path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def compare_sets(label, validator_set, yaml_set, findings):
    only_in_validator = set(validator_set) - set(yaml_set)
    only_in_yaml = set(yaml_set) - set(validator_set)
    if only_in_validator or only_in_yaml:
        findings.append(
            {
                "surface": label,
                "only_in_validator": sorted(only_in_validator),
                "only_in_yaml": sorted(only_in_yaml),
            }
        )


def safe_get(d, keys, label, findings):
    cur = d
    for k in keys:
        if not isinstance(cur, dict) or k not in cur:
            findings.append({"surface": label, "error": f"yaml path missing: {keys}"})
            return None
        cur = cur[k]
    return cur


def main() -> int:
    for p in [VALIDATOR_PATH, SHELL_PATH, TASK_PATH, MEMORY_PATH, REVIEW_PATH]:
        if not p.is_file():
            print(f"ERROR: missing {p}", file=sys.stderr)
            return 2

    try:
        v = load_validator()
        shell = load_yaml_file(SHELL_PATH)
        task = load_yaml_file(TASK_PATH)
        memory = load_yaml_file(MEMORY_PATH)
        review = load_yaml_file(REVIEW_PATH)
    except Exception as exc:
        print(
            f"ERROR: load failed: {exc.__class__.__name__}: {exc}",
            file=sys.stderr,
        )
        return 2

    findings = []

    yaml_packet_types = safe_get(
        shell, ["required_shared_fields", "packet_type", "allowed"], "PACKET_TYPES", findings
    )
    if yaml_packet_types is not None:
        compare_sets("PACKET_TYPES", v.PACKET_TYPES, yaml_packet_types, findings)

    shared = safe_get(shell, ["required_shared_fields"], "SHARED_REQUIRED", findings)
    if isinstance(shared, dict):
        compare_sets("SHARED_REQUIRED", v.SHARED_REQUIRED, shared.keys(), findings)

    families = {"task_packet": task, "memory_packet": memory, "review_packet": review}
    for fname, fyaml in families.items():
        rf = safe_get(fyaml, ["required_fields"], f"FAMILY_REQUIRED[{fname}]", findings)
        if isinstance(rf, dict):
            compare_sets(
                f"FAMILY_REQUIRED[{fname}]",
                v.FAMILY_REQUIRED[fname],
                rf.keys(),
                findings,
            )

        sv = safe_get(fyaml, ["allowed_status_values"], f"STATUS_VALUES[{fname}]", findings)
        if isinstance(sv, list):
            compare_sets(
                f"STATUS_VALUES[{fname}]",
                v.STATUS_VALUES[fname],
                sv,
                findings,
            )

    sup = safe_get(
        shell,
        ["required_shared_fields", "supervision_mode", "allowed"],
        "SUPERVISION_MODE_VALUES",
        findings,
    )
    if sup is not None:
        compare_sets("SUPERVISION_MODE_VALUES", v.SUPERVISION_MODE_VALUES, sup, findings)

    risk = safe_get(
        shell,
        ["required_shared_fields", "risk", "allowed"],
        "RISK_VALUES",
        findings,
    )
    if risk is not None:
        compare_sets("RISK_VALUES", v.RISK_VALUES, risk, findings)

    rec = safe_get(
        review,
        ["required_fields", "recommendation", "allowed"],
        "REVIEW_RECOMMENDATION_VALUES",
        findings,
    )
    if rec is not None:
        compare_sets(
            "REVIEW_RECOMMENDATION_VALUES",
            v.REVIEW_RECOMMENDATION_VALUES,
            rec,
            findings,
        )

    promo = safe_get(
        memory,
        ["required_fields", "promotion_candidate", "allowed"],
        "PROMOTION_CANDIDATE_VALUES",
        findings,
    )
    if promo is not None:
        compare_sets(
            "PROMOTION_CANDIDATE_VALUES",
            v.PROMOTION_CANDIDATE_VALUES,
            promo,
            findings,
        )

    if findings:
        print(f"DRIFT FOUND: {len(findings)} surface(s) disagree")
        for f in findings:
            print(f"  surface: {f['surface']}")
            if "error" in f:
                print(f"    error: {f['error']}")
            else:
                if f["only_in_validator"]:
                    print(f"    only in validator: {f['only_in_validator']}")
                if f["only_in_yaml"]:
                    print(f"    only in yaml: {f['only_in_yaml']}")
        return 1

    print("OK validator constants and yaml schemas agree on all checked surfaces")
    return 0


if __name__ == "__main__":
    sys.exit(main())
