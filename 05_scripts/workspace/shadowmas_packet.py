#!/usr/bin/env python3
"""Validate and place one new packet in an existing external workspace."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import uuid
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools"))
sys.path.insert(0, str(REPO / "05_scripts" / "validate"))

from _shadowmas_packet_naming import PACKET_DIRECTORIES, workspace_packet_name  # noqa: E402
from _shadowmas_readonly import UniqueKeyLoader  # noqa: E402
from shadowmas_validate import validate_packet  # noqa: E402
from shadowmas_workspace import project_id, resolve_project, workspace_path  # noqa: E402


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    write = subparsers.add_parser("write", help="validate and place one packet")
    write.add_argument("--project", required=True, help="existing product project directory")
    write.add_argument("--input", required=True, help="YAML draft to place")
    return parser.parse_args(argv)


def checked_workspace(project: Path) -> Path:
    if not project.is_dir():
        raise ValueError(f"project path must exist and be a directory: {project}")
    workspace = workspace_path(project)
    metadata_file = workspace / "workspace.json"
    if not metadata_file.is_file():
        raise ValueError(f"workspace is not initialized: {workspace}")
    metadata = json.loads(metadata_file.read_text(encoding="utf-8"))
    boundary = metadata.get("boundary") if isinstance(metadata, dict) else None
    if (not isinstance(metadata, dict)
            or metadata.get("schema_version") != "v0"
            or metadata.get("workspace_kind") != "external_workspace"
            or metadata.get("project_id") != project_id(project)
            or metadata.get("project_path") != str(project)
            or metadata.get("workspace_path") != str(workspace)
            or not isinstance(boundary, dict)
            or boundary.get("writes_product_repo") is not False
            or boundary.get("governance_artifacts_external") is not True):
        raise ValueError(f"workspace metadata does not match this project: {workspace}")
    if workspace.resolve().is_relative_to(project.resolve()):
        raise ValueError("workspace resolves inside the product project")
    return workspace


def load_draft(path: Path) -> tuple[dict, str]:
    original = path.read_text(encoding="utf-8")
    data = yaml.load(original, Loader=UniqueKeyLoader)
    if not isinstance(data, dict):
        raise ValueError("input must contain one YAML mapping")
    if "packet_uid" not in data:
        uid = str(uuid.uuid4())
        data["packet_uid"] = uid
        with_uid = f"packet_uid: {uid}\n{original}"
        try:
            if yaml.load(with_uid, Loader=UniqueKeyLoader) == data:
                return data, with_uid
        except yaml.YAMLError:
            pass
        return data, yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
    return data, original


def uid_collision(workspace: Path, uid: str) -> Path | None:
    for directory in ("packets", "reviews", "handoffs", "runs"):
        root = workspace / directory
        if not root.is_dir():
            continue
        for path in sorted((*root.glob("*.yaml"), *root.glob("*.yml"))):
            if path.is_symlink():
                raise ValueError(f"cannot inspect symlinked packet: {path}")
            data = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
            if isinstance(data, dict) and data.get("packet_uid") == uid:
                return path
    return None


def write_packet(project: Path, input_path: Path) -> int:
    workspace = checked_workspace(project)
    data, content = load_draft(input_path)
    packet_type = data.get("packet_type")
    uid = data.get("packet_uid")
    version = data.get("schema_version")
    name = workspace_packet_name(packet_type, uid, version)
    directory = workspace / PACKET_DIRECTORIES[packet_type]
    if not directory.is_dir() or directory.is_symlink():
        raise ValueError(f"packet destination is missing or is a symlink: {directory}")
    if directory.resolve().parent != workspace.resolve():
        raise ValueError("packet destination escapes the workspace")
    destination = directory / name
    errors, _ = validate_packet(data, destination)
    if errors:
        for error in errors:
            print(f"ERROR {error.code}: {error.field}: {error.message}", file=sys.stderr)
        return 1
    collision = uid_collision(workspace, uid)
    if collision is not None:
        print(f"ERROR packet_uid already exists: {collision}", file=sys.stderr)
        return 1

    temporary: Path | None = None
    try:
        fd, temp_name = tempfile.mkstemp(prefix=".pending-", suffix=".yaml", dir=directory)
        temporary = Path(temp_name)
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as output:
            output.write(content)
            output.flush()
            os.fsync(output.fileno())
        os.link(temporary, destination)
    except FileExistsError:
        print(f"ERROR packet filename already exists: {destination}", file=sys.stderr)
        return 1
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    print(destination)
    return 0


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        return write_packet(resolve_project(args.project), Path(args.input))
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError, yaml.YAMLError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
