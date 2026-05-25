#!/usr/bin/env python3
"""Minimal read-only shadowMAS packet validator.

Logical command shape: shadowmas validate <packet-file>
Direct use: python3 05_scripts/validate/shadowmas_validate.py <packet-file>
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


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

DEPRECATED_HANDOFF_FIELDS = {"next_owner", "handoff_reason"}


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
    except OSError as exc:
        print_error(
            make_error("INPUT_FILE_ERROR", str(path), "<input>", "$", f"unable to read file: {exc}")
        )
        return None, 2

    try:
        return yaml.safe_load(text), 0
    except yaml.YAMLError as exc:
        print_error(make_error("YAML_PARSE_ERROR", str(path), "<yaml>", "$", str(exc)))
        return None, 2


def required_missing(data: dict[str, Any], field: str) -> bool:
    return field not in data or data[field] is None


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
    if status not in STATUS_VALUES[packet_type]:
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
    if recommendation not in REVIEW_RECOMMENDATION_VALUES:
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
        if not item.get("source_path") and not item.get("source_id"):
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
    for field in ("to_role", "needed_action", "reason", "resume_from", "blockers"):
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

    if "resume_from" in handoff and not isinstance(handoff["resume_from"], list):
        errors.append(
            make_error(
                "INVALID_HANDOFF_SHAPE",
                file_name,
                "resume_from",
                "$.handoff.resume_from",
                "handoff.resume_from must be a list",
            )
        )
    if "blockers" in handoff and not isinstance(handoff["blockers"], list):
        errors.append(
            make_error(
                "INVALID_HANDOFF_SHAPE",
                file_name,
                "blockers",
                "$.handoff.blockers",
                "handoff.blockers must be a list",
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

    if packet_type not in PACKET_TYPES:
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
    if packet_type == "review_packet":
        errors.extend(validate_review_recommendation(data, file_name))
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
