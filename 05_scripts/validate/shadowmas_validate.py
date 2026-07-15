#!/usr/bin/env python3
"""Minimal read-only shadowMAS packet validator.

Logical command shape: shadowmas validate <packet-file>
Direct use: python3 05_scripts/validate/shadowmas_validate.py <packet-file>
"""

from __future__ import annotations

import argparse
import math
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

TOOLS_DIR = Path(__file__).resolve().parents[2] / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from _shadowmas_readonly import UniqueKeyLoader  # noqa: E402


PACKET_TYPES = {"task_packet", "memory_packet", "review_packet"}

SHARED_REQUIRED = [
    "packet_uid",
    "packet_type",
    "schema_version",
    "created_at",
    "created_by",
    "owner",
    "supervision_mode",
    "risk",
    "status",
]

FAMILY_REQUIRED = {
    "task_packet": [
        "task_id",
        "goal",
        "scope",
        "out_of_scope",
        "truth_touchpoints",
        "worker_plan",
        "acceptance_criteria",
        "stop_conditions",
    ],
    "memory_packet": [
        "memory_kind",
        "memory_scope",
        "summary",
        "structured_payload",
        "source_refs",
        "invalidation_triggers",
        "confidence",
        "promotion_candidate",
    ],
    "review_packet": [
        "decision_needed",
        "why_you_are_seeing_this",
        "change_summary",
        "risk_summary",
        "recommendation",
    ],
}

STATUS_VALUES = {
    "task_packet": {
        "draft",
        "ready",
        "assigned",
        "in_progress",
        "blocked",
        "awaiting_review",
        "approved",
        "rejected",
        "done",
        "cancelled",
        "superseded",
    },
    "memory_packet": {
        "captured",
        "draft",
        "candidate",
        "approved_shared",
        "stale",
        "broken_reference",
        "rejected",
        "superseded",
        "archived",
    },
    "review_packet": {
        "draft",
        "ready_for_human",
        "under_review",
        "approved",
        "rejected",
        "needs_revision",
        "closed",
    },
}

REVIEW_RECOMMENDATION_VALUES = {"approve", "reject", "revise", "defer", "escalate", "unpromote"}
REVIEW_CONSENSUS_KIND_VALUES = {"unanimous", "majority", "first_to_decide"}

SUPERVISION_MODE_VALUES = {"human_live_pair", "human_available_delegate", "human_away_autonomous"}
RISK_VALUES = {"r0_trivial", "r1_routine", "r2_guarded", "r3_sensitive", "r4_human_only"}
RFC3339_UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
PROMOTION_CANDIDATE_VALUES = {"yes", "no"}
TRUST_CLASS_VALUES = {"trusted", "external", "adversarial_assumed"}
SOURCE_REF_STRING_FIELDS = {
    "source_type",
    "source_id",
    "source_path",
    "source_hash",
    "source_version",
    "section",
    "relation",
}

DEPRECATED_HANDOFF_FIELDS = {"next_owner", "handoff_reason"}
HANDOFF_REQUIRED_STRING_FIELDS = {"to_role", "needed_action", "reason"}
HANDOFF_REQUIRED_LIST_FIELDS = {"resume_from", "blockers"}
SHARED_NON_EMPTY_STRING_FIELDS = {
    "created_by",
    "owner",
    "packet_id",
    "task_id",
    "run_id",
    "session_id",
}
SHARED_STRING_LIST_FIELDS = {"writable_by", "related_packets", "tags"}
TASK_NON_EMPTY_STRING_FIELDS = {"goal", "why_now"}
TASK_STRING_LIST_FIELDS = {
    "scope",
    "out_of_scope",
    "truth_touchpoints",
    "acceptance_criteria",
    "stop_conditions",
    "deliverables",
    "constraints",
    "expected_outputs",
}
REVIEW_NON_EMPTY_STRING_FIELDS = {
    "decision_needed",
    "why_you_are_seeing_this",
    "change_summary",
    "risk_summary",
}
REVIEW_STRING_LIST_FIELDS = {"must_compare", "do_not_need_to_read"}


@dataclass
class ValidationError:
    code: str
    file: str
    field: str
    path: str
    message: str
    severity: str = "ERROR"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate one YAML packet file against the current shadowMAS v0 "
            "packet contract. Logical command: shadowmas validate <packet-file>."
        )
    )
    parser.add_argument("packet_file", help="YAML packet file to validate")
    return parser.parse_args(argv)


def print_error(error: ValidationError) -> None:
    print(f"ERROR {error.code}")
    print(f"file: {error.file}")
    print(f"field: {error.field}")
    print(f"path: {error.path}")
    print(f"severity: {error.severity}")
    print(f"message: {error.message}")


def print_errors(errors: list[ValidationError]) -> None:
    for index, error in enumerate(errors):
        if index:
            print()
        print_error(error)


def make_error(code: str, file: str, field: str, path: str, message: str) -> ValidationError:
    return ValidationError(code=code, file=file, field=field, path=path, message=message)


def load_yaml(path: Path) -> tuple[Any | None, int]:
    if not path.exists() or not path.is_file():
        print_error(
            make_error(
                "INPUT_FILE_ERROR",
                str(path),
                "<input>",
                "$",
                "input file does not exist or is not a file",
            )
        )
        return None, 2

    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        print_error(
            make_error("INPUT_FILE_ERROR", str(path), "<input>", "$", f"unable to read file: {exc}")
        )
        return None, 2

    try:
        return yaml.load(text, Loader=UniqueKeyLoader), 0
    except yaml.YAMLError as exc:
        print_error(make_error("YAML_PARSE_ERROR", str(path), "<yaml>", "$", str(exc)))
        return None, 2


def required_missing(data: dict[str, Any], field: str) -> bool:
    return field not in data or data[field] is None


def validate_non_empty_string_fields(
    data: dict[str, Any], fields: set[str], file_name: str, code: str
) -> list[ValidationError]:
    errors: list[ValidationError] = []
    for field in sorted(fields):
        if field not in data or data[field] is None:
            continue
        value = data[field]
        if not isinstance(value, str) or not value.strip():
            errors.append(
                make_error(
                    code,
                    file_name,
                    field,
                    f"$.{field}",
                    f"{field} must be a non-empty string",
                )
            )
    return errors


def validate_string_list_value(
    value: Any,
    file_name: str,
    field: str,
    path: str,
    code: str,
) -> list[ValidationError]:
    if not isinstance(value, list):
        return [
            make_error(code, file_name, field, path, f"{field} must be a list of strings")
        ]

    errors: list[ValidationError] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            errors.append(
                make_error(
                    code,
                    file_name,
                    field,
                    f"{path}[{index}]",
                    f"{field} items must be non-empty strings",
                )
            )
    return errors


def validate_string_list_fields(
    data: dict[str, Any], fields: set[str], file_name: str, code: str
) -> list[ValidationError]:
    errors: list[ValidationError] = []
    for field in sorted(fields):
        if field not in data or data[field] is None:
            continue
        errors.extend(
            validate_string_list_value(data[field], file_name, field, f"$.{field}", code)
        )
    return errors


def is_rfc3339_utc(value: Any) -> bool:
    if not isinstance(value, str) or not RFC3339_UTC_RE.fullmatch(value):
        return False
    try:
        datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return False
    return True


def schema_major(schema_version: Any) -> int | None:
    if schema_version == "v0":
        return 0
    return None


def filename_major(path: Path) -> int | None:
    match = re.search(r"\.v(\d+)(?:\.|$)", path.name)
    if not match:
        return None
    return int(match.group(1))


def validate_required(
    data: dict[str, Any], packet_type: str, file_name: str
) -> list[ValidationError]:
    errors: list[ValidationError] = []
    for field in SHARED_REQUIRED + FAMILY_REQUIRED[packet_type]:
        if required_missing(data, field):
            errors.append(
                make_error(
                    "REQUIRED_FIELD_MISSING",
                    file_name,
                    field,
                    f"$.{field}",
                    f"{packet_type} requires {field}",
                )
            )
    return errors


def validate_schema_version(data: dict[str, Any], path: Path) -> list[ValidationError]:
    errors: list[ValidationError] = []
    schema_version_value = data.get("schema_version")
    if schema_version_value is None:
        return errors

    major = schema_major(schema_version_value)
    if major is None:
        errors.append(
            make_error(
                "INVALID_SCHEMA_VERSION",
                str(path),
                "schema_version",
                "$.schema_version",
                "schema_version must be v0 for the MVP validator",
            )
        )
        return errors

    file_major = filename_major(path)
    if file_major is not None and file_major != major:
        errors.append(
            make_error(
                "SCHEMA_FILENAME_MAJOR_MISMATCH",
                str(path),
                "schema_version",
                "$.schema_version",
                f"filename major v{file_major} does not match schema_version major v{major}",
            )
        )
    return errors


def validate_status(data: dict[str, Any], packet_type: str, file_name: str) -> list[ValidationError]:
    status = data.get("status")
    if status is None:
        return []
    if not isinstance(status, str) or status not in STATUS_VALUES[packet_type]:
        allowed = ", ".join(sorted(STATUS_VALUES[packet_type]))
        return [
            make_error(
                "INVALID_STATUS",
                file_name,
                "status",
                "$.status",
                f'status "{status}" is not allowed for {packet_type}; allowed: {allowed}',
            )
        ]
    return []


def validate_review_recommendation(data: dict[str, Any], file_name: str) -> list[ValidationError]:
    recommendation = data.get("recommendation")
    if recommendation is None:
        return []
    if (
        not isinstance(recommendation, str)
        or recommendation not in REVIEW_RECOMMENDATION_VALUES
    ):
        allowed = ", ".join(sorted(REVIEW_RECOMMENDATION_VALUES))
        return [
            make_error(
                "INVALID_RECOMMENDATION",
                file_name,
                "recommendation",
                "$.recommendation",
                f'recommendation "{recommendation}" is not allowed for review_packet; allowed: {allowed}',
            )
        ]
    return []


def validate_review_multi_reviewer_fields(
    data: dict[str, Any], file_name: str
) -> list[ValidationError]:
    errors: list[ValidationError] = []
    reviewers_required = data.get("reviewers_required", 1)
    reviewers_required_valid = True

    if "reviewers_required" in data:
        if isinstance(reviewers_required, bool) or not isinstance(reviewers_required, int):
            reviewers_required_valid = False
            errors.append(
                make_error(
                    "INVALID_REVIEWERS_REQUIRED",
                    file_name,
                    "reviewers_required",
                    "$.reviewers_required",
                    "reviewers_required must be an integer greater than or equal to 1",
                )
            )
        elif reviewers_required < 1:
            reviewers_required_valid = False
            errors.append(
                make_error(
                    "INVALID_REVIEWERS_REQUIRED",
                    file_name,
                    "reviewers_required",
                    "$.reviewers_required",
                    "reviewers_required must be greater than or equal to 1",
                )
            )

    if "consensus_kind" in data:
        consensus_kind = data["consensus_kind"]
        if not isinstance(consensus_kind, str) or consensus_kind not in REVIEW_CONSENSUS_KIND_VALUES:
            allowed = ", ".join(sorted(REVIEW_CONSENSUS_KIND_VALUES))
            errors.append(
                make_error(
                    "INVALID_CONSENSUS_KIND",
                    file_name,
                    "consensus_kind",
                    "$.consensus_kind",
                    f"consensus_kind must be one of: {allowed}",
                )
            )

    has_consensus = "consensus_kind" in data and data["consensus_kind"] is not None
    if reviewers_required_valid and isinstance(reviewers_required, int):
        if reviewers_required > 1 and not has_consensus:
            errors.append(
                make_error(
                    "MISSING_CONSENSUS_KIND",
                    file_name,
                    "consensus_kind",
                    "$.consensus_kind",
                    "consensus_kind is required when reviewers_required is greater than 1",
                )
            )
        elif reviewers_required <= 1 and has_consensus:
            errors.append(
                make_error(
                    "UNEXPECTED_CONSENSUS_KIND",
                    file_name,
                    "consensus_kind",
                    "$.consensus_kind",
                    "consensus_kind applies only when reviewers_required is greater than 1",
                )
            )

    return errors


def validate_review_promotion_snapshot(
    data: dict[str, Any], file_name: str
) -> list[ValidationError]:
    if "promotion_snapshot" not in data:
        return []

    promotion_snapshot = data["promotion_snapshot"]
    if not isinstance(promotion_snapshot, dict):
        return [
            make_error(
                "INVALID_PROMOTION_SNAPSHOT",
                file_name,
                "promotion_snapshot",
                "$.promotion_snapshot",
                "promotion_snapshot must be an object when present",
            )
        ]

    errors: list[ValidationError] = []
    for field in ("source_hashes", "snapshot_at"):
        if field not in promotion_snapshot or promotion_snapshot[field] is None:
            errors.append(
                make_error(
                    "INVALID_PROMOTION_SNAPSHOT",
                    file_name,
                    field,
                    f"$.promotion_snapshot.{field}",
                    f"promotion_snapshot requires {field}",
                )
            )

    source_hashes = promotion_snapshot.get("source_hashes")
    if source_hashes is not None:
        if not isinstance(source_hashes, list):
            errors.append(
                make_error(
                    "INVALID_PROMOTION_SNAPSHOT",
                    file_name,
                    "source_hashes",
                    "$.promotion_snapshot.source_hashes",
                    "promotion_snapshot.source_hashes must be a list of objects",
                )
            )
        else:
            for index, item in enumerate(source_hashes):
                item_path = f"$.promotion_snapshot.source_hashes[{index}]"
                if not isinstance(item, dict):
                    errors.append(
                        make_error(
                            "INVALID_PROMOTION_SNAPSHOT",
                            file_name,
                            "source_hashes",
                            item_path,
                            "promotion_snapshot.source_hashes item must be an object",
                        )
                    )
                    continue
                for key, value in item.items():
                    if not isinstance(value, str):
                        errors.append(
                            make_error(
                                "INVALID_PROMOTION_SNAPSHOT",
                                file_name,
                                "source_hashes",
                                f"{item_path}.{key}",
                                "promotion_snapshot.source_hashes item values must be strings",
                            )
                        )

    snapshot_at = promotion_snapshot.get("snapshot_at")
    if snapshot_at is not None and not is_rfc3339_utc(snapshot_at):
        errors.append(
            make_error(
                "INVALID_PROMOTION_SNAPSHOT",
                file_name,
                "snapshot_at",
                "$.promotion_snapshot.snapshot_at",
                "promotion_snapshot.snapshot_at must be RFC3339 UTC with a Z suffix",
            )
        )

    return errors


def validate_source_refs(data: dict[str, Any], file_name: str) -> list[ValidationError]:
    if "source_refs" not in data:
        return []
    source_refs = data["source_refs"]
    if not isinstance(source_refs, list):
        return [
            make_error(
                "INVALID_REFERENCE_SHAPE",
                file_name,
                "source_refs",
                "$.source_refs",
                "source_refs must be a list when present",
            )
        ]

    errors: list[ValidationError] = []
    for index, item in enumerate(source_refs):
        item_path = f"$.source_refs[{index}]"
        if not isinstance(item, dict):
            errors.append(
                make_error(
                    "INVALID_REFERENCE_SHAPE",
                    file_name,
                    "source_refs",
                    item_path,
                    "source_refs item must be an object",
                )
            )
            continue

        for field in ("source_type", "relation"):
            if field not in item or item[field] is None:
                errors.append(
                    make_error(
                        "INVALID_REFERENCE_SHAPE",
                        file_name,
                        field,
                        f"{item_path}.{field}",
                        f"source_refs item requires {field}",
                    )
                )

        for field in SOURCE_REF_STRING_FIELDS:
            if field in item and item[field] is not None:
                value = item[field]
                if not isinstance(value, str) or not value.strip():
                    errors.append(
                        make_error(
                            "INVALID_REFERENCE_SHAPE",
                            file_name,
                            field,
                            f"{item_path}.{field}",
                            f"source_refs item {field} must be a non-empty string when present",
                        )
                    )

        source_path = item.get("source_path")
        source_id = item.get("source_id")
        has_source_path = isinstance(source_path, str) and bool(source_path.strip())
        has_source_id = isinstance(source_id, str) and bool(source_id.strip())
        if not has_source_path and not has_source_id:
            errors.append(
                make_error(
                    "INVALID_REFERENCE_SHAPE",
                    file_name,
                    "source_path",
                    item_path,
                    "source_refs item requires source_path or source_id",
                )
            )
    return errors


def validate_artifact_refs(data: dict[str, Any], file_name: str) -> list[ValidationError]:
    if "artifact_refs" not in data:
        return []
    artifact_refs = data["artifact_refs"]
    if not isinstance(artifact_refs, list):
        return [
            make_error(
                "INVALID_REFERENCE_SHAPE",
                file_name,
                "artifact_refs",
                "$.artifact_refs",
                "artifact_refs must be a list when present",
            )
        ]

    errors: list[ValidationError] = []
    for index, item in enumerate(artifact_refs):
        item_path = f"$.artifact_refs[{index}]"
        if not isinstance(item, dict):
            errors.append(
                make_error(
                    "INVALID_REFERENCE_SHAPE",
                    file_name,
                    "artifact_refs",
                    item_path,
                    "artifact_refs item must be an object",
                )
            )
            continue

        for field in ("artifact_type", "artifact_path", "change_kind"):
            if field not in item or item[field] is None:
                errors.append(
                    make_error(
                        "INVALID_REFERENCE_SHAPE",
                        file_name,
                        field,
                        f"{item_path}.{field}",
                        f"artifact_refs item requires {field}",
                    )
                )
            elif not isinstance(item[field], str) or not item[field].strip():
                errors.append(
                    make_error(
                        "INVALID_REFERENCE_SHAPE",
                        file_name,
                        field,
                        f"{item_path}.{field}",
                        f"artifact_refs item {field} must be a non-empty string",
                    )
                )

        if "exists" in item and not isinstance(item["exists"], bool):
            errors.append(
                make_error(
                    "INVALID_REFERENCE_SHAPE",
                    file_name,
                    "exists",
                    f"{item_path}.exists",
                    "artifact_refs item exists must be a boolean when present",
                )
            )
        for field in ("produced_by", "task_role"):
            if field in item and (
                not isinstance(item[field], str) or not item[field].strip()
            ):
                errors.append(
                    make_error(
                        "INVALID_REFERENCE_SHAPE",
                        file_name,
                        field,
                        f"{item_path}.{field}",
                        f"artifact_refs item {field} must be a non-empty string when present",
                    )
                )
    return errors


def validate_handoff(data: dict[str, Any], file_name: str) -> list[ValidationError]:
    if "handoff" not in data:
        return []
    handoff = data["handoff"]
    if not isinstance(handoff, dict):
        return [
            make_error(
                "INVALID_HANDOFF_SHAPE",
                file_name,
                "handoff",
                "$.handoff",
                "handoff must be an object when present",
            )
        ]

    errors: list[ValidationError] = []
    for field in HANDOFF_REQUIRED_STRING_FIELDS | HANDOFF_REQUIRED_LIST_FIELDS:
        if field not in handoff or handoff[field] is None:
            errors.append(
                make_error(
                    "INVALID_HANDOFF_SHAPE",
                    file_name,
                    field,
                    f"$.handoff.{field}",
                    f"handoff requires {field}",
                )
            )

    for field in HANDOFF_REQUIRED_STRING_FIELDS:
        if field in handoff and handoff[field] is not None:
            value = handoff[field]
            if not isinstance(value, str) or not value.strip():
                errors.append(
                    make_error(
                        "INVALID_HANDOFF_SHAPE",
                        file_name,
                        field,
                        f"$.handoff.{field}",
                        f"handoff.{field} must be a non-empty string",
                    )
                )

    for field in HANDOFF_REQUIRED_LIST_FIELDS:
        if field not in handoff or handoff[field] is None:
            continue
        value = handoff[field]
        if not isinstance(value, list):
            errors.append(
                make_error(
                    "INVALID_HANDOFF_SHAPE",
                    file_name,
                    field,
                    f"$.handoff.{field}",
                    f"handoff.{field} must be a list",
                )
            )
            continue
        for index, item in enumerate(value):
            if not isinstance(item, str) or not item.strip():
                errors.append(
                    make_error(
                        "INVALID_HANDOFF_SHAPE",
                        file_name,
                        field,
                        f"$.handoff.{field}[{index}]",
                        f"handoff.{field} items must be non-empty strings",
                    )
                )

    if "from_packet_ref" in handoff:
        value = handoff["from_packet_ref"]
        if not isinstance(value, str) or not value.strip():
            errors.append(
                make_error(
                    "INVALID_HANDOFF_SHAPE",
                    file_name,
                    "from_packet_ref",
                    "$.handoff.from_packet_ref",
                    "handoff.from_packet_ref must be a non-empty string when present",
                )
            )

    if "delegation_depth" in handoff:
        value = handoff["delegation_depth"]
        if isinstance(value, bool) or not isinstance(value, int):
            errors.append(
                make_error(
                    "INVALID_HANDOFF_SHAPE",
                    file_name,
                    "delegation_depth",
                    "$.handoff.delegation_depth",
                    "handoff.delegation_depth must be an integer when present",
                )
            )

    for field in DEPRECATED_HANDOFF_FIELDS:
        if field in handoff:
            errors.append(
                make_error(
                    "DEPRECATED_HANDOFF_FIELD",
                    file_name,
                    field,
                    f"$.handoff.{field}",
                    f"{field} is a deprecated/confusion-prone handoff field",
                )
            )
    return errors


def validate_supervision_mode(data: dict[str, Any], file_name: str) -> list[ValidationError]:
    value = data.get("supervision_mode")
    if value is None:
        return []
    if not isinstance(value, str) or value not in SUPERVISION_MODE_VALUES:
        allowed = ", ".join(sorted(SUPERVISION_MODE_VALUES))
        return [
            make_error(
                "INVALID_SUPERVISION_MODE",
                file_name,
                "supervision_mode",
                "$.supervision_mode",
                f'supervision_mode "{value}" is not allowed; allowed: {allowed}',
            )
        ]
    return []


def validate_risk(data: dict[str, Any], file_name: str) -> list[ValidationError]:
    value = data.get("risk")
    if value is None:
        return []
    if not isinstance(value, str) or value not in RISK_VALUES:
        allowed = ", ".join(sorted(RISK_VALUES))
        return [
            make_error(
                "INVALID_RISK",
                file_name,
                "risk",
                "$.risk",
                f'risk "{value}" is not allowed; allowed: {allowed}',
            )
        ]
    return []


def validate_created_at(data: dict[str, Any], file_name: str) -> list[ValidationError]:
    value = data.get("created_at")
    if value is None:
        return []
    if not is_rfc3339_utc(value):
        return [
            make_error(
                "INVALID_TIMESTAMP",
                file_name,
                "created_at",
                "$.created_at",
                f'created_at must be RFC3339 UTC with Z suffix (e.g. "2026-04-20T16:40:00Z"); got {value!r}',
            )
        ]
    return []


def validate_packet_uid(data: dict[str, Any], file_name: str) -> list[ValidationError]:
    value = data.get("packet_uid")
    if value is None:
        return []
    if not isinstance(value, str) or not value.strip():
        return [
            make_error(
                "INVALID_PACKET_UID",
                file_name,
                "packet_uid",
                "$.packet_uid",
                "packet_uid must be a non-empty string",
            )
        ]
    return []


def validate_payload_repr(data: dict[str, Any], file_name: str) -> list[ValidationError]:
    if "payload_repr" not in data:
        return []
    value = data["payload_repr"]
    if not isinstance(value, str):
        return [
            make_error(
                "INVALID_PAYLOAD_REPR",
                file_name,
                "payload_repr",
                "$.payload_repr",
                "payload_repr must be a string when present",
            )
        ]
    return []


def validate_cost_trace(data: dict[str, Any], file_name: str) -> list[ValidationError]:
    if "cost_trace" not in data:
        return []
    value = data["cost_trace"]
    if not isinstance(value, dict):
        return [
            make_error(
                "INVALID_COST_TRACE",
                file_name,
                "cost_trace",
                "$.cost_trace",
                "cost_trace must be an object when present",
            )
        ]
    return []


def validate_data_class(data: dict[str, Any], file_name: str) -> list[ValidationError]:
    if "data_class" not in data:
        return []
    value = data["data_class"]
    if not isinstance(value, str):
        return [
            make_error(
                "INVALID_DATA_CLASS",
                file_name,
                "data_class",
                "$.data_class",
                "data_class must be a string when present",
            )
        ]
    return []


def validate_shared_field_shapes(
    data: dict[str, Any], file_name: str
) -> list[ValidationError]:
    errors = validate_non_empty_string_fields(
        data,
        SHARED_NON_EMPTY_STRING_FIELDS,
        file_name,
        "INVALID_SHARED_FIELD",
    )
    errors.extend(
        validate_string_list_fields(
            data,
            SHARED_STRING_LIST_FIELDS,
            file_name,
            "INVALID_SHARED_FIELD",
        )
    )
    if "signed_by" in data and data["signed_by"] is not None:
        if not isinstance(data["signed_by"], dict):
            errors.append(
                make_error(
                    "INVALID_SHARED_FIELD",
                    file_name,
                    "signed_by",
                    "$.signed_by",
                    "signed_by must be an object when present",
                )
            )
    return errors


def validate_task_packet_fields(data: dict[str, Any], file_name: str) -> list[ValidationError]:
    errors = validate_non_empty_string_fields(
        data,
        TASK_NON_EMPTY_STRING_FIELDS,
        file_name,
        "INVALID_TASK_FIELD",
    )
    errors.extend(
        validate_string_list_fields(
            data,
            TASK_STRING_LIST_FIELDS,
            file_name,
            "INVALID_TASK_FIELD",
        )
    )

    worker_plan = data.get("worker_plan")
    if worker_plan is not None:
        if not isinstance(worker_plan, dict):
            errors.append(
                make_error(
                    "INVALID_WORKER_PLAN",
                    file_name,
                    "worker_plan",
                    "$.worker_plan",
                    "worker_plan must be an object",
                )
            )
        else:
            for field in ("preferred_worker", "fallback_worker"):
                if field in worker_plan and (
                    not isinstance(worker_plan[field], str)
                    or not worker_plan[field].strip()
                ):
                    errors.append(
                        make_error(
                            "INVALID_WORKER_PLAN",
                            file_name,
                            field,
                            f"$.worker_plan.{field}",
                            f"worker_plan.{field} must be a non-empty string when present",
                        )
                    )
            if "allow_fanout" in worker_plan and not isinstance(
                worker_plan["allow_fanout"], bool
            ):
                errors.append(
                    make_error(
                        "INVALID_WORKER_PLAN",
                        file_name,
                        "allow_fanout",
                        "$.worker_plan.allow_fanout",
                        "worker_plan.allow_fanout must be a boolean when present",
                    )
                )
            for field in ("fanout_limit", "retry_limit"):
                if field in worker_plan:
                    value = worker_plan[field]
                    if isinstance(value, bool) or not isinstance(value, int):
                        errors.append(
                            make_error(
                                "INVALID_WORKER_PLAN",
                                file_name,
                                field,
                                f"$.worker_plan.{field}",
                                f"worker_plan.{field} must be an integer when present",
                            )
                        )

    if "on_blocked" in data:
        on_blocked = data["on_blocked"]
        if not isinstance(on_blocked, dict):
            errors.append(
                make_error(
                    "INVALID_ON_BLOCKED",
                    file_name,
                    "on_blocked",
                    "$.on_blocked",
                    "on_blocked must be an object when present",
                )
            )
        else:
            if "action" in on_blocked and (
                not isinstance(on_blocked["action"], str)
                or not on_blocked["action"].strip()
            ):
                errors.append(
                    make_error(
                        "INVALID_ON_BLOCKED",
                        file_name,
                        "action",
                        "$.on_blocked.action",
                        "on_blocked.action must be a non-empty string when present",
                    )
                )
            if "next_allowed_work" in on_blocked:
                errors.extend(
                    validate_string_list_value(
                        on_blocked["next_allowed_work"],
                        file_name,
                        "next_allowed_work",
                        "$.on_blocked.next_allowed_work",
                        "INVALID_ON_BLOCKED",
                    )
                )

    if "inputs" not in data:
        return errors
    value = data["inputs"]
    if not isinstance(value, dict):
        errors.append(
            make_error(
                "INVALID_INPUTS",
                file_name,
                "inputs",
                "$.inputs",
                "inputs must be an object when present",
            )
        )
        return errors

    for field in ("required_context", "optional_context"):
        if field not in value:
            continue
        errors.extend(
            validate_string_list_value(
                value[field],
                file_name,
                field,
                f"$.inputs.{field}",
                "INVALID_INPUTS",
            )
        )
    if "trust_class" in value:
        trust_class = value["trust_class"]
        if not isinstance(trust_class, str) or trust_class not in TRUST_CLASS_VALUES:
            allowed = ", ".join(sorted(TRUST_CLASS_VALUES))
            errors.append(
                make_error(
                    "INVALID_INPUTS",
                    file_name,
                    "trust_class",
                    "$.inputs.trust_class",
                    f"inputs.trust_class must be one of: {allowed}",
                )
            )
    return errors


def validate_promotion_candidate(data: dict[str, Any], file_name: str) -> list[ValidationError]:
    value = data.get("promotion_candidate")
    if value is None:
        return []
    if not isinstance(value, str) or value not in PROMOTION_CANDIDATE_VALUES:
        return [
            make_error(
                "INVALID_PROMOTION_CANDIDATE",
                file_name,
                "promotion_candidate",
                "$.promotion_candidate",
                f'promotion_candidate must be the string "yes" or "no" (quoted; unquoted yes/no may be coerced to boolean by YAML 1.1 parsers); got {value!r}',
            )
        ]
    return []


def validate_review_packet_fields(
    data: dict[str, Any], file_name: str
) -> list[ValidationError]:
    errors = validate_non_empty_string_fields(
        data,
        REVIEW_NON_EMPTY_STRING_FIELDS,
        file_name,
        "INVALID_REVIEW_FIELD",
    )
    errors.extend(
        validate_string_list_fields(
            data,
            REVIEW_STRING_LIST_FIELDS,
            file_name,
            "INVALID_REVIEW_FIELD",
        )
    )

    if "minimal_checks" in data:
        minimal_checks = data["minimal_checks"]
        if not isinstance(minimal_checks, dict):
            errors.append(
                make_error(
                    "INVALID_REVIEW_FIELD",
                    file_name,
                    "minimal_checks",
                    "$.minimal_checks",
                    "minimal_checks must be an object when present",
                )
            )
        elif "must_read" in minimal_checks:
            errors.extend(
                validate_string_list_value(
                    minimal_checks["must_read"],
                    file_name,
                    "must_read",
                    "$.minimal_checks.must_read",
                    "INVALID_REVIEW_FIELD",
                )
            )
    return errors


def validate_memory_packet_fields(data: dict[str, Any], file_name: str) -> list[ValidationError]:
    errors: list[ValidationError] = []

    confidence = data.get("confidence")
    if confidence is not None:
        if isinstance(confidence, bool) or not isinstance(confidence, (int, float)):
            errors.append(
                make_error(
                    "INVALID_CONFIDENCE",
                    file_name,
                    "confidence",
                    "$.confidence",
                    "confidence must be a number between 0.0 and 1.0",
                )
            )
        elif not math.isfinite(confidence) or confidence < 0.0 or confidence > 1.0:
            errors.append(
                make_error(
                    "INVALID_CONFIDENCE",
                    file_name,
                    "confidence",
                    "$.confidence",
                    "confidence must be between 0.0 and 1.0 inclusive",
                )
            )

    memory_kind = data.get("memory_kind")
    if memory_kind is not None and (not isinstance(memory_kind, str) or not memory_kind.strip()):
        errors.append(
            make_error(
                "INVALID_MEMORY_KIND",
                file_name,
                "memory_kind",
                "$.memory_kind",
                "memory_kind must be a non-empty string",
            )
        )

    memory_scope = data.get("memory_scope")
    if memory_scope is not None and (
        not isinstance(memory_scope, str) or not memory_scope.strip()
    ):
        errors.append(
            make_error(
                "INVALID_MEMORY_SCOPE",
                file_name,
                "memory_scope",
                "$.memory_scope",
                "memory_scope must be a non-empty string",
            )
        )

    summary = data.get("summary")
    if summary is not None and (not isinstance(summary, str) or not summary.strip()):
        errors.append(
            make_error(
                "INVALID_MEMORY_SUMMARY",
                file_name,
                "summary",
                "$.summary",
                "summary must be a non-empty string",
            )
        )

    structured_payload = data.get("structured_payload")
    if structured_payload is not None and not isinstance(structured_payload, dict):
        errors.append(
            make_error(
                "INVALID_STRUCTURED_PAYLOAD",
                file_name,
                "structured_payload",
                "$.structured_payload",
                "structured_payload must be an object",
            )
        )

    if "invalidation_triggers" in data and data["invalidation_triggers"] is not None:
        errors.extend(
            validate_string_list_value(
                data["invalidation_triggers"],
                file_name,
                "invalidation_triggers",
                "$.invalidation_triggers",
                "INVALID_INVALIDATION_TRIGGERS",
            )
        )

    promotion_notes = data.get("promotion_notes")
    if promotion_notes is not None and (
        not isinstance(promotion_notes, str) or not promotion_notes.strip()
    ):
        errors.append(
            make_error(
                "INVALID_PROMOTION_NOTES",
                file_name,
                "promotion_notes",
                "$.promotion_notes",
                "promotion_notes must be a non-empty string when present",
            )
        )

    if "validity" in data:
        validity = data["validity"]
        if not isinstance(validity, dict):
            errors.append(
                make_error(
                    "INVALID_VALIDITY",
                    file_name,
                    "validity",
                    "$.validity",
                    "validity must be an object when present",
                )
            )
        else:
            applies_to = validity.get("applies_to")
            if applies_to is not None:
                # One existing v0 candidate stores this as a descriptive
                # string. Preserve that working-packet compatibility until a
                # human authority decision reconciles the packet and schema.
                if isinstance(applies_to, str) and applies_to.strip():
                    pass
                elif not isinstance(applies_to, dict):
                    errors.append(
                        make_error(
                            "INVALID_VALIDITY",
                            file_name,
                            "applies_to",
                            "$.validity.applies_to",
                            "validity.applies_to must be an object or a legacy "
                            "non-empty string when present",
                        )
                    )
                else:
                    for field in ("modules", "task_types"):
                        if field in applies_to:
                            errors.extend(
                                validate_string_list_value(
                                    applies_to[field],
                                    file_name,
                                    field,
                                    f"$.validity.applies_to.{field}",
                                    "INVALID_VALIDITY",
                                )
                            )
            if "stale_on" in validity:
                errors.extend(
                    validate_string_list_value(
                        validity["stale_on"],
                        file_name,
                        "stale_on",
                        "$.validity.stale_on",
                        "INVALID_VALIDITY",
                    )
                )
            for field in ("review_after", "runtime_generation"):
                if field in validity and (
                    not isinstance(validity[field], str) or not validity[field].strip()
                ):
                    errors.append(
                        make_error(
                            "INVALID_VALIDITY",
                            file_name,
                            field,
                            f"$.validity.{field}",
                            f"validity.{field} must be a non-empty string when present",
                        )
                    )

    if "invalidation" in data:
        invalidation = data["invalidation"]
        if not isinstance(invalidation, dict):
            errors.append(
                make_error(
                    "INVALID_INVALIDATION",
                    file_name,
                    "invalidation",
                    "$.invalidation",
                    "invalidation must be an object when present",
                )
            )
        elif "current_state" in invalidation and (
            not isinstance(invalidation["current_state"], str)
            or not invalidation["current_state"].strip()
        ):
            errors.append(
                make_error(
                    "INVALID_INVALIDATION",
                    file_name,
                    "current_state",
                    "$.invalidation.current_state",
                    "invalidation.current_state must be a non-empty string when present",
                )
            )

    return errors


def validate_packet(data: Any, path: Path) -> tuple[list[ValidationError], str | None]:
    file_name = str(path)
    if not isinstance(data, dict):
        return [
            make_error(
                "INPUT_NOT_MAPPING",
                file_name,
                "<root>",
                "$",
                "input must parse into one YAML mapping/object",
            )
        ], None

    packet_type = data.get("packet_type")
    if packet_type is None:
        return [
            make_error(
                "REQUIRED_FIELD_MISSING",
                file_name,
                "packet_type",
                "$.packet_type",
                "packet_type is required",
            )
        ], None

    if not isinstance(packet_type, str) or packet_type not in PACKET_TYPES:
        return [
            make_error(
                "UNKNOWN_PACKET_TYPE",
                file_name,
                "packet_type",
                "$.packet_type",
                f"unknown packet_type {packet_type!r}",
            )
        ], None

    errors: list[ValidationError] = []
    errors.extend(validate_required(data, packet_type, file_name))
    errors.extend(validate_schema_version(data, path))
    errors.extend(validate_status(data, packet_type, file_name))
    errors.extend(validate_supervision_mode(data, file_name))
    errors.extend(validate_risk(data, file_name))
    errors.extend(validate_created_at(data, file_name))
    errors.extend(validate_packet_uid(data, file_name))
    errors.extend(validate_shared_field_shapes(data, file_name))
    errors.extend(validate_payload_repr(data, file_name))
    errors.extend(validate_cost_trace(data, file_name))
    errors.extend(validate_data_class(data, file_name))
    if packet_type == "task_packet":
        errors.extend(validate_task_packet_fields(data, file_name))
    if packet_type == "review_packet":
        errors.extend(validate_review_packet_fields(data, file_name))
        errors.extend(validate_review_recommendation(data, file_name))
        errors.extend(validate_review_multi_reviewer_fields(data, file_name))
        errors.extend(validate_review_promotion_snapshot(data, file_name))
    if packet_type == "memory_packet":
        errors.extend(validate_memory_packet_fields(data, file_name))
        errors.extend(validate_promotion_candidate(data, file_name))
    errors.extend(validate_source_refs(data, file_name))
    errors.extend(validate_artifact_refs(data, file_name))
    errors.extend(validate_handoff(data, file_name))
    return errors, packet_type


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    path = Path(args.packet_file)
    data, load_exit = load_yaml(path)
    if load_exit:
        return load_exit

    errors, packet_type = validate_packet(data, path)
    if errors:
        print_errors(errors)
        return 1

    print(f"OK {path}")
    print(f"packet_type: {packet_type}")
    print(f"schema_version: {data.get('schema_version')}")
    print("checks: passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
