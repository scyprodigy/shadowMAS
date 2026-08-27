#!/usr/bin/env python3
"""Evaluate review-brief dogfood metrics as unauthenticated workflow proxies.

Read-only against both repository and workspace. This tool evaluates the three
thresholds recorded in DECISION-review-brief-primary-direction from local
``review_brief_runs.v1.jsonl`` data. It never authenticates a human and never
claims attention, competence, approval quality, causality, or improved
oversight. A threshold result is a proxy signal for human review, not an
automatic product decision.

Evaluation requires at least 30 eligible terminal units distributed across at
least six distinct UTC calendar months and spanning six calendar months end to
end after timestamp normalization to UTC. Action-rate and overhead proxies
additionally require at least ten admissible sign-offs. A sign-off is counted
only when its workspace-relative
receipt is a non-symlink v0 review_packet with a distinct resolved target and
packet_uid. These integrity checks do not authenticate the operator or the
timestamps.

Exit: 0 = enough admissible data and fewer than two proxy thresholds fire;
1 = two or more proxy thresholds fire (human review required);
2 = usage/setup/malformed-input error; 3 = insufficient or partial data.
"""

from __future__ import annotations

import argparse
import calendar
import datetime as dt
import json
import re
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

from _shadowmas_readonly import UniqueKeyLoader


REPO = Path(__file__).resolve().parents[1]
VALIDATOR_DIR = REPO / "05_scripts" / "validate"
if str(VALIDATOR_DIR) not in sys.path:
    sys.path.insert(0, str(VALIDATOR_DIR))
import shadowmas_validate as packet_validator  # noqa: E402

RUN_FILE = Path("runs/review_brief_runs.v1.jsonl")
RECORD_VERSION = "review_brief_run.v1"
MIN_ELIGIBLE_SIGNOFFS = 30
MIN_OBSERVATION_MONTHS = 6
MIN_SIGNOFF_SAMPLE = 10
CONSULT_RATE_FLOOR = 0.40
ACTION_RATE_FLOOR = 0.10
OVERHEAD_CEILING_SECONDS = 120.0
MAX_LINE_BYTES = 65536
MAX_RECEIPT_BYTES = 65536
MAX_FUTURE_SKEW = dt.timedelta(minutes=5)
UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-"
    r"[0-9a-f]{12}$")
PACKET_UID_RE = re.compile(r"^[A-Za-z0-9_.:-]{1,128}$")
RECEIPT_RE = re.compile(r"^reviews/[A-Za-z0-9_.:-]{1,180}\.ya?ml$")

RECORD_KINDS = {"preview", "signoff", "signoff_attempt", "skip"}
RISK_TIERS = {"r0_trivial", "r1_routine", "r2_guarded", "r3_sensitive",
              "r4_human_only"}
ELIGIBLE_RISKS = {"r2_guarded", "r3_sensitive", "r4_human_only"}
JUDGMENTS = {"approve", "reject", "revise"}
ALL_JUDGMENTS = JUDGMENTS | {"none", "cancelled"}
JUDGMENT_SOURCES = {"none", "operator_input_unauthenticated"}
OBSERVABLE_ACTIONS = {"none", "added_check", "revision", "rejection", "reopen"}
ACTION_SOURCES = {
    "none", "operator_declared_unauthenticated", "derived_from_judgment"
}
FORBIDDEN_KEYS = {
    "cache_hit", "confidence", "model_confidence_score", "private_memory",
    "private_memory_content", "raw_log", "raw_logs", "raw_memory",
    "retrieval_hit",
}
RECORD_FIELDS = {
    "record_version", "record_kind", "run_id", "signoff_id", "at", "risk",
    "eligible_signoff", "brief_displayed", "brief_consulted",
    "consultation_claim", "interaction_channel", "authentication", "judgment",
    "judgment_source", "observable_action", "observable_action_source",
    "changed_loc", "blocking_findings", "advisory_findings", "guard_hits",
    "receipt", "compose_ms", "triage_ms", "exit_code",
}


def workspace_error(workspace: Path, repo: Path) -> str | None:
    if not workspace.is_dir():
        return f"workspace is not a directory: {workspace}"
    try:
        workspace.resolve().relative_to(repo.resolve())
        return "workspace must resolve outside the repository"
    except ValueError:
        pass
    for subdirectory in ("runs", "reviews"):
        if not (workspace / subdirectory).is_dir():
            return ("workspace is missing required subdirectory: "
                    f"{subdirectory}/")
    return None


def forbidden_key(value: object) -> str | None:
    if isinstance(value, dict):
        for key, item in value.items():
            key_text = str(key)
            if key_text in FORBIDDEN_KEYS or key_text.startswith("raw_"):
                return key_text
            nested = forbidden_key(item)
            if nested:
                return nested
    elif isinstance(value, list):
        for item in value:
            nested = forbidden_key(item)
            if nested:
                return nested
    return None


def valid_timestamp(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def parse_timestamp(value: str) -> dt.datetime:
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


def add_calendar_months(value: dt.datetime, months: int) -> dt.datetime:
    month_index = value.month - 1 + months
    year = value.year + month_index // 12
    month = month_index % 12 + 1
    day = min(value.day, calendar.monthrange(year, month)[1])
    return value.replace(year=year, month=month, day=day)


def validate_record(record: object) -> str | None:
    if not isinstance(record, dict):
        return "record_not_object"
    poisoned = forbidden_key(record)
    if poisoned:
        return f"forbidden_key:{poisoned}"
    unknown = sorted(set(record) - RECORD_FIELDS)
    if unknown:
        return f"unknown_field:{unknown[0]}"
    if record.get("record_version") != RECORD_VERSION:
        return "unknown_record_version"
    if record.get("record_kind") not in RECORD_KINDS:
        return "unknown_record_kind"
    if (not isinstance(record.get("run_id"), str)
            or not UUID_RE.fullmatch(record["run_id"])):
        return "invalid_run_id"
    if (not isinstance(record.get("signoff_id"), str)
            or not UUID_RE.fullmatch(record["signoff_id"])):
        return "invalid_signoff_id"
    if not valid_timestamp(record.get("at")):
        return "invalid_timestamp"
    if not isinstance(record.get("eligible_signoff"), bool):
        return "invalid_eligible_signoff"
    if record.get("risk") not in RISK_TIERS:
        return "invalid_risk"
    if record["eligible_signoff"] != (record["risk"] in ELIGIBLE_RISKS):
        return "eligible_risk_mismatch"
    if not isinstance(record.get("brief_displayed"), bool):
        return "legacy_missing_display_provenance"
    if record.get("brief_consulted") != record["brief_displayed"]:
        return "display_alias_mismatch"
    if record.get("consultation_claim") != "display_proxy_only":
        return "unsupported_consultation_claim"
    if record.get("authentication") != "none":
        return "unsupported_authentication"
    if record.get("interaction_channel") not in {"none", "stdout", "tty"}:
        return "invalid_interaction_channel"
    if record.get("judgment") not in ALL_JUDGMENTS:
        return "invalid_judgment"
    if record.get("judgment_source") not in JUDGMENT_SOURCES:
        return "invalid_judgment_source"
    if record.get("observable_action_source") not in ACTION_SOURCES:
        return "invalid_observable_action_source"
    if record.get("observable_action") not in OBSERVABLE_ACTIONS | {"not_applicable"}:
        return "invalid_observable_action"
    for field in ("compose_ms", "triage_ms", "exit_code"):
        value = record.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            return f"invalid_{field}"
    if record["exit_code"] not in {0, 1, 2}:
        return "invalid_exit_code"
    changed_loc = record.get("changed_loc")
    if (changed_loc is not None
            and (not isinstance(changed_loc, int)
                 or isinstance(changed_loc, bool) or changed_loc < 0)):
        return "invalid_changed_loc"
    for field in ("blocking_findings", "advisory_findings", "guard_hits"):
        value = record.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            return f"invalid_{field}"
    receipt = record.get("receipt")
    if receipt is not None and not isinstance(receipt, str):
        return "invalid_receipt_reference"

    kind = record["record_kind"]
    if kind == "signoff":
        if record.get("judgment") not in JUDGMENTS:
            return "signoff_without_judgment"
        if record.get("judgment_source") != "operator_input_unauthenticated":
            return "signoff_without_judgment_provenance"
        if record.get("interaction_channel") != "tty" or not record["brief_displayed"]:
            return "signoff_without_tty_display"
        if record.get("observable_action_source") == "none":
            return "signoff_without_action_provenance"
        if (not isinstance(receipt, str)
                or not RECEIPT_RE.fullmatch(receipt)):
            return "signoff_without_receipt_reference"
    elif kind == "skip":
        if record["brief_displayed"] or record.get("interaction_channel") != "none":
            return "skip_with_display"
        if (record.get("judgment") != "none"
                or record.get("judgment_source") != "none"
                or record.get("observable_action") != "not_applicable"
                or record.get("observable_action_source") != "none"
                or receipt is not None):
            return "skip_with_judgment_or_action"
    elif kind == "preview":
        if (not record["brief_displayed"]
                or record.get("interaction_channel") != "stdout"
                or record.get("judgment") != "none"
                or record.get("judgment_source") != "none"
                or record.get("observable_action") != "not_applicable"
                or record.get("observable_action_source") != "none"
                or receipt is not None):
            return "invalid_preview_provenance"
    else:  # signoff_attempt
        if receipt is not None:
            return "signoff_attempt_with_receipt_reference"
        if record["brief_displayed"]:
            if record.get("interaction_channel") != "tty":
                return "displayed_attempt_without_tty"
            if record.get("judgment") in JUDGMENTS:
                if (record.get("judgment_source")
                        != "operator_input_unauthenticated"
                        or record.get("observable_action_source") == "none"):
                    return "judged_attempt_without_provenance"
            elif (record.get("judgment") != "cancelled"
                  or record.get("judgment_source") != "none"
                  or record.get("observable_action") != "none"
                  or record.get("observable_action_source") != "none"):
                return "invalid_cancelled_attempt"
        elif (record.get("interaction_channel") != "none"
              or record.get("judgment") != "none"
              or record.get("judgment_source") != "none"
              or record.get("observable_action") != "not_applicable"
              or record.get("observable_action_source") != "none"):
            return "invalid_undisplayed_attempt"
    return None


def reject_json_constant(value: str) -> None:
    raise ValueError(f"non-standard JSON constant {value}")


def load_records(path: Path) -> tuple[list[dict], Counter, str | None]:
    if not path.exists():
        return [], Counter(), None
    records: list[dict] = []
    excluded: Counter = Counter()
    future_limit = dt.datetime.now(dt.timezone.utc) + MAX_FUTURE_SKEW
    try:
        lines = path.read_bytes().splitlines()
    except OSError as exc:
        return [], excluded, f"unable to read run data: {exc}"
    for line_number, raw in enumerate(lines, start=1):
        if not raw.strip():
            continue
        if len(raw) > MAX_LINE_BYTES:
            excluded["line_too_large"] += 1
            continue
        try:
            record = json.loads(raw, parse_constant=reject_json_constant)
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
            return [], excluded, f"malformed JSONL at line {line_number}: {exc}"
        reason = validate_record(record)
        if reason:
            excluded[reason] += 1
        elif parse_timestamp(record["at"]) > future_limit:
            excluded["timestamp_in_future"] += 1
        else:
            records.append(record)
    return records, excluded, None


def criterion(value: float | None, fires: bool | None,
              reason: str | None = None) -> dict:
    return {"value": value, "fires": fires, "reason": reason}


def load_receipt_identity(
    workspace: Path, receipt: str
) -> tuple[Path | None, str | None, str | None]:
    reviews = (workspace / "reviews").resolve()
    declared = workspace / receipt
    if (workspace / "reviews").is_symlink() or declared.is_symlink():
        return None, None, "receipt_is_symlink"
    target = declared.resolve()
    try:
        target.relative_to(reviews)
    except ValueError:
        return None, None, "receipt_outside_reviews"
    if not target.is_file():
        return None, None, "receipt_missing"
    try:
        if target.stat().st_size > MAX_RECEIPT_BYTES:
            return None, None, "receipt_too_large"
        data = yaml.load(target.read_text(encoding="utf-8"),
                         Loader=UniqueKeyLoader)
    except (OSError, UnicodeError, yaml.YAMLError):
        return None, None, "receipt_unreadable_or_malformed"
    if not isinstance(data, dict) or data.get("packet_type") != "review_packet":
        return None, None, "receipt_not_review_packet"
    if data.get("schema_version") != "v0":
        return None, None, "receipt_unknown_schema_version"
    validation_errors, packet_type = packet_validator.validate_packet(
        data, target)
    if validation_errors or packet_type != "review_packet":
        return None, None, "receipt_packet_invalid"
    packet_uid = data.get("packet_uid")
    if (not isinstance(packet_uid, str)
            or not PACKET_UID_RE.fullmatch(packet_uid)):
        return None, None, "receipt_invalid_packet_uid"
    return target, packet_uid, None


def measured_receipt_integrity(
    signoffs: list[dict], identities: dict[str, tuple[Path, str]]
) -> dict:
    """Measure receipt cardinality independently of the dedup controls."""
    measured = [identities[record["run_id"]] for record in signoffs
                if record["run_id"] in identities]
    return {
        "distinct_receipt_targets": len({target for target, _uid in measured}),
        "distinct_receipt_packet_uids": len({
            uid for _target, uid in measured}),
        "signoffs_with_measured_receipt_identity": len(measured),
        "signoff_denominator": len(signoffs),
        "receipt_symlinks_allowed": False,
    }


def evaluate(records: list[dict], excluded: Counter, workspace: Path,
             since: dt.datetime | None = None) -> tuple[dict, int]:
    unique: list[dict] = []
    seen_run_ids: set[str] = set()
    seen_receipt_targets: set[Path] = set()
    seen_receipt_packet_uids: set[str] = set()
    receipt_identities: dict[str, tuple[Path, str]] = {}
    for record in records:
        if record["run_id"] in seen_run_ids:
            excluded["duplicate_run_id"] += 1
            continue
        seen_run_ids.add(record["run_id"])
        if record["record_kind"] == "signoff":
            receipt = record["receipt"]
            target, packet_uid, error = load_receipt_identity(
                workspace, receipt)
            if error:
                excluded[error] += 1
                continue
            if target is None or packet_uid is None:
                excluded["receipt_identity_unavailable"] += 1
                continue
            if target in seen_receipt_targets:
                excluded["duplicate_receipt_reference"] += 1
                continue
            seen_receipt_targets.add(target)
            if packet_uid in seen_receipt_packet_uids:
                excluded["duplicate_receipt_packet_uid"] += 1
                continue
            seen_receipt_packet_uids.add(packet_uid)
            receipt_identities[record["run_id"]] = (target, packet_uid)
        unique.append(record)

    groups: dict[str, list[dict]] = defaultdict(list)
    for record in unique:
        groups[record["signoff_id"]].append(record)

    globally_admissible: list[dict] = []
    for group in groups.values():
        candidates = [r for r in group
                      if r["record_kind"] in {"signoff", "skip"}
                      and r["eligible_signoff"]]
        if len(candidates) > 1:
            excluded["ambiguous_terminal_records"] += len(candidates)
            candidate_ids = {r["run_id"] for r in candidates}
            globally_admissible.extend(
                r for r in group if r["run_id"] not in candidate_ids)
        else:
            globally_admissible.extend(group)

    if since is None:
        records = globally_admissible
        window_dropped = 0
    else:
        records = [r for r in globally_admissible
                   if parse_timestamp(r["at"]) >= since]
        window_dropped = len(globally_admissible) - len(records)

    terminals = [r for r in records
                 if r["record_kind"] in {"signoff", "skip"}
                 and r["eligible_signoff"]]

    signoffs = [r for r in terminals if r["record_kind"] == "signoff"]
    skips = [r for r in terminals if r["record_kind"] == "skip"]
    eligible_count = len(terminals)
    preview_count = sum(r["record_kind"] == "preview" for r in records)
    attempt_count = sum(r["record_kind"] == "signoff_attempt" for r in records)

    integrity = measured_receipt_integrity(signoffs, receipt_identities)
    missing_identities = (
        len(signoffs) - integrity["signoffs_with_measured_receipt_identity"])
    measured_identities = integrity["signoffs_with_measured_receipt_identity"]
    duplicate_targets = (
        measured_identities - integrity["distinct_receipt_targets"])
    duplicate_packet_uids = (
        measured_identities - integrity["distinct_receipt_packet_uids"])
    if missing_identities:
        excluded["receipt_identity_measurement_gap"] += missing_identities
    if duplicate_targets:
        excluded["receipt_target_cardinality_mismatch"] += duplicate_targets
    if duplicate_packet_uids:
        excluded["receipt_packet_uid_cardinality_mismatch"] += \
            duplicate_packet_uids

    terminal_times = sorted(
        parse_timestamp(r["at"]).astimezone(dt.timezone.utc)
        for r in terminals)
    observation_start = terminal_times[0] if terminal_times else None
    observation_end = terminal_times[-1] if terminal_times else None
    observation_span_days = (
        (observation_end - observation_start).total_seconds() / 86400
        if observation_start is not None and observation_end is not None
        else None
    )
    observation_months = {(item.year, item.month) for item in terminal_times}
    observation_month_counts = Counter(
        item.strftime("%Y-%m") for item in terminal_times)
    observation_day_counts = Counter(
        item.strftime("%Y-%m-%d") for item in terminal_times)
    distinct_observation_months = len(observation_months)
    max_units_in_one_utc_day = max(observation_day_counts.values(), default=0)
    max_single_utc_day_share = (
        max_units_in_one_utc_day / eligible_count if eligible_count else None)
    end_to_end_span_ready = bool(
        observation_start is not None and observation_end is not None
        and observation_end >= add_calendar_months(
            observation_start, MIN_OBSERVATION_MONTHS)
    )
    distinct_months_ready = (
        distinct_observation_months >= MIN_OBSERVATION_MONTHS)
    observation_gate_ready = end_to_end_span_ready and distinct_months_ready
    count_ready = eligible_count >= MIN_ELIGIBLE_SIGNOFFS
    evaluation_ready = count_ready and observation_gate_ready
    if not count_ready:
        readiness_reason = f"eligible_signoffs<{MIN_ELIGIBLE_SIGNOFFS}"
    elif not end_to_end_span_ready:
        readiness_reason = (
            f"observation_span<{MIN_OBSERVATION_MONTHS}_calendar_months")
    elif not distinct_months_ready:
        readiness_reason = (
            f"observation_distribution<{MIN_OBSERVATION_MONTHS}_"
            "distinct_calendar_months")
    else:
        readiness_reason = None

    if evaluation_ready:
        consult_rate = len(signoffs) / eligible_count
        consult = criterion(consult_rate,
                            consult_rate < CONSULT_RATE_FLOOR)
    else:
        consult = criterion(None, None, readiness_reason)

    declared_actions = [
        r for r in signoffs
        if r["observable_action_source"] == "operator_declared_unauthenticated"
        and r["observable_action"] != "none"
    ]
    signoff_sample_ready = len(signoffs) >= MIN_SIGNOFF_SAMPLE
    if evaluation_ready and signoff_sample_ready:
        action_rate = len(declared_actions) / len(signoffs)
        action = criterion(action_rate, action_rate < ACTION_RATE_FLOOR)
        overhead_seconds = statistics.median(
            (r["compose_ms"] + r["triage_ms"]) / 1000 for r in signoffs)
        overhead = criterion(overhead_seconds,
                             overhead_seconds > OVERHEAD_CEILING_SECONDS)
    else:
        reason = ("signoff_sample_too_small" if evaluation_ready
                  else readiness_reason)
        action = criterion(None, None, reason)
        overhead = criterion(None, None, reason)

    criteria = {
        "consult_rate_proxy": consult,
        "declared_action_rate_proxy": action,
        "median_compose_plus_triage_seconds": overhead,
    }
    defined = [item for item in criteria.values() if item["fires"] is not None]
    fired = sum(item["fires"] is True for item in defined)
    if excluded:
        verdict = "PARTIAL_DATA"
        exit_code = 3
    elif not evaluation_ready or len(defined) < 3:
        verdict = "INSUFFICIENT_DATA"
        exit_code = 3
    elif fired >= 2:
        verdict = "PROXY_KILL_SIGNAL"
        exit_code = 1
    else:
        verdict = "NO_PROXY_KILL_SIGNAL"
        exit_code = 0

    first_record = min(records, key=lambda r: parse_timestamp(r["at"])) \
        if records else None
    last_record = max(records, key=lambda r: parse_timestamp(r["at"])) \
        if records else None
    derived_actions = sum(
        r["record_kind"] == "signoff"
        and r["observable_action_source"] == "derived_from_judgment"
        for r in records
    )
    report = {
        "advisory": "recorded workflow proxies only; not human authentication or oversight quality",
        "window": {
            "since": since.isoformat() if since else None,
            "valid_records_before_window": window_dropped,
            "first_record_at": first_record["at"] if first_record else None,
            "last_record_at": last_record["at"] if last_record else None,
            "observation_start_utc": (
                observation_start.isoformat() if observation_start else None),
            "observation_end_utc": (
                observation_end.isoformat() if observation_end else None),
            "observation_span_days": observation_span_days,
            "minimum_observation_span": "6_calendar_months",
            "distinct_observation_months": distinct_observation_months,
            "minimum_distinct_observation_months": MIN_OBSERVATION_MONTHS,
            "units_by_utc_month": dict(sorted(observation_month_counts.items())),
            "max_units_in_one_utc_day": max_units_in_one_utc_day,
            "max_single_utc_day_share": max_single_utc_day_share,
            "observation_span_ready": end_to_end_span_ready,
            "distinct_observation_months_ready": distinct_months_ready,
            "observation_gate_ready": observation_gate_ready,
        },
        "admissible": {
            "eligible_signoff_units": eligible_count,
            "signoff": len(signoffs),
            "minimum_signoff_sample": MIN_SIGNOFF_SAMPLE,
            "signoff_sample_ready": signoff_sample_ready,
            "skip": len(skips),
            "preview": preview_count,
            "signoff_attempt": attempt_count,
        },
        "integrity": integrity,
        "excluded": dict(sorted(excluded.items())),
        "criteria": criteria,
        "limitations": {
            "authentication": "none",
            "timestamp_authentication": "none",
            "receipt_authentication": "none",
            "unauthenticated_tty_signoffs": len(signoffs),
            "derived_actions_not_counted": derived_actions,
            "causality_claim": "none",
        },
        "verdict": verdict,
        "claim_ceiling": "recorded_workflow_proxy_only",
    }
    return report, exit_code


def render_text(report: dict) -> str:
    span = report["window"]["observation_span_days"]
    span_text = str(span) if span is not None else "undefined"
    day_share = report["window"]["max_single_utc_day_share"]
    day_share_text = str(day_share) if day_share is not None else "undefined"
    month_counts = report["window"]["units_by_utc_month"]
    month_counts_text = ",".join(
        f"{month}:{count}" for month, count in month_counts.items()) or "none"
    lines = [
        "REVIEW BRIEF METRICS (ADVISORY)",
        report["advisory"],
        f"verdict: {report['verdict']}",
        f"eligible units: {report['admissible']['eligible_signoff_units']} "
        f"(signoff={report['admissible']['signoff']} "
        f"skip={report['admissible']['skip']})",
        f"receipt integrity: distinct_targets="
        f"{report['integrity']['distinct_receipt_targets']}/"
        f"{report['integrity']['signoff_denominator']} signoffs "
        f"distinct_packet_uids="
        f"{report['integrity']['distinct_receipt_packet_uids']}/"
        f"{report['integrity']['signoff_denominator']} signoffs "
        "symlinks_allowed=false",
        f"window: since={report['window']['since'] or 'none'} "
        f"first={report['window']['first_record_at'] or 'none'} "
        f"last={report['window']['last_record_at'] or 'none'} "
        f"valid_before_window={report['window']['valid_records_before_window']} "
        f"observation_start_utc="
        f"{report['window']['observation_start_utc'] or 'none'} "
        f"observation_end_utc="
        f"{report['window']['observation_end_utc'] or 'none'} "
        f"observation_span_days={span_text} "
        f"distinct_observation_months="
        f"{report['window']['distinct_observation_months']} "
        f"units_by_utc_month={month_counts_text} "
        f"max_units_in_one_utc_day="
        f"{report['window']['max_units_in_one_utc_day']} "
        f"max_single_utc_day_share="
        f"{day_share_text} "
        f"span_ready={report['window']['observation_span_ready']} "
        f"distinct_months_ready="
        f"{report['window']['distinct_observation_months_ready']} "
        f"observation_gate_ready="
        f"{report['window']['observation_gate_ready']}",
    ]
    for name, item in report["criteria"].items():
        value = "undefined" if item["value"] is None else f"{item['value']:.4f}"
        lines.append(f"{name}: {value}; fires={item['fires']}; "
                     f"reason={item['reason'] or 'none'}")
    if report["excluded"]:
        lines.append("excluded: " + ", ".join(
            f"{key}={value}" for key, value in report["excluded"].items()))
    limitations = report["limitations"]
    lines.append(
        "limitations: authentication=none; timestamp_authentication=none; "
        "receipt_authentication=none; causality=none; "
        f"unauthenticated_tty_signoffs="
        f"{limitations['unauthenticated_tty_signoffs']}; "
        f"derived_actions_not_counted="
        f"{limitations['derived_actions_not_counted']}")
    lines.append("claim ceiling: recorded_workflow_proxy_only")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate unauthenticated review-brief workflow proxies "
                    "against the recorded dogfood thresholds (read-only)."
    )
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--since",
                        help="include valid records at or after this timezone-"
                             "aware ISO-8601 timestamp")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)

    workspace = Path(args.workspace)
    error = workspace_error(workspace, REPO)
    if error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    since = None
    if args.since:
        if not valid_timestamp(args.since):
            print("ERROR: --since must be a timezone-aware ISO-8601 "
                  "timestamp", file=sys.stderr)
            return 2
        since = parse_timestamp(args.since)
    records, excluded, error = load_records(workspace / RUN_FILE)
    if error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    report, exit_code = evaluate(records, excluded, workspace, since)
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(render_text(report))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
