#!/usr/bin/env python3
"""Minimal external shadowMAS workspace helper.

Direct use:
  python3 05_scripts/workspace/shadowmas_workspace.py init --project <project-path>
  python3 05_scripts/workspace/shadowmas_workspace.py where --project <project-path>
  python3 05_scripts/workspace/shadowmas_workspace.py inspect --project <project-path>
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


WORKSPACE_SUBDIRS = ["packets", "reviews", "handoffs", "runs"]
REQUIRED_METADATA_FIELDS = [
    "schema_version",
    "workspace_kind",
    "project_id",
    "project_path",
    "workspace_path",
    "created_at",
    "created_by",
    "boundary",
]
REQUIRED_BOUNDARY_FIELDS = ["writes_product_repo", "governance_artifacts_external"]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create or locate an external shadowMAS workspace for a product repo "
            "without writing into the product repo."
        )
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name in ("init", "where", "inspect"):
        command = subparsers.add_parser(name)
        command.add_argument("--project", required=True, help="Product project directory path")

    destroy_cmd = subparsers.add_parser("destroy")
    destroy_cmd.add_argument("--project", required=True, help="Product project directory path")
    destroy_cmd.add_argument(
        "--yes",
        action="store_true",
        help="confirm destructive action; required for destroy to actually remove the workspace",
    )

    subparsers.add_parser("list")

    return parser.parse_args(argv)


def print_error(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)


def print_workspace_error(
    code: str,
    workspace: Path | None,
    field: str | None,
    message: str,
) -> None:
    print(f"ERROR {code}")
    if workspace is not None:
        print(f"workspace: {workspace}")
    if field is not None:
        print(f"field: {field}")
    print(f"message: {message}")


def resolve_project(path_text: str) -> Path:
    return Path(path_text).expanduser().resolve(strict=False)


def validate_project(path: Path) -> bool:
    return path.exists() and path.is_dir()


def local_data_root() -> Path:
    system = platform.system()
    if system == "Darwin":
        return Path.home() / "Library" / "Application Support" / "shadowmas" / "workspaces"
    if system == "Windows":
        local_app_data = os.environ.get("LOCALAPPDATA")
        if local_app_data:
            return Path(local_app_data) / "shadowmas" / "workspaces"
        return Path.home() / "AppData" / "Local" / "shadowmas" / "workspaces"

    xdg_data_home = os.environ.get("XDG_DATA_HOME")
    if xdg_data_home:
        return Path(xdg_data_home) / "shadowmas" / "workspaces"
    return Path.home() / ".local" / "share" / "shadowmas" / "workspaces"


def slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip()).strip("-._")
    return slug.lower() or "project"


def project_id(project_path: Path) -> str:
    readable = slugify(project_path.name)
    digest = hashlib.sha256(str(project_path).encode("utf-8")).hexdigest()[:8]
    return f"{readable}-{digest}"


def workspace_path(project_path: Path) -> Path:
    return local_data_root() / project_id(project_path)


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def workspace_metadata(project_path: Path, workspace: Path) -> dict[str, object]:
    return {
        "schema_version": "v0",
        "workspace_kind": "external_workspace",
        "project_id": project_id(project_path),
        "project_path": str(project_path),
        "workspace_path": str(workspace),
        "created_at": utc_timestamp(),
        "created_by": "shadowmas_workspace.py",
        "boundary": {
            "writes_product_repo": False,
            "governance_artifacts_external": True,
        },
    }


def init_workspace(project_path: Path) -> int:
    if not validate_project(project_path):
        print_error(f"project path must exist and be a directory: {project_path}")
        return 1

    workspace = workspace_path(project_path)
    metadata_path = workspace / "workspace.json"

    if metadata_path.exists():
        print(f"workspace already exists: {workspace}")
        return 0

    try:
        workspace.mkdir(parents=True, exist_ok=True)
        for name in WORKSPACE_SUBDIRS:
            (workspace / name).mkdir(exist_ok=True)
        metadata_path.write_text(
            json.dumps(workspace_metadata(project_path, workspace), indent=2, sort_keys=True)
            + "\n",
            encoding="utf-8",
        )
    except OSError as exc:
        print_error(f"unable to create workspace: {exc}")
        return 2

    print(workspace)
    return 0


def where_workspace(project_path: Path) -> int:
    if not validate_project(project_path):
        print_error(f"project path must exist and be a directory: {project_path}")
        return 1

    workspace = workspace_path(project_path)
    if not workspace.exists():
        print_error(f"workspace does not exist: {workspace}")
        return 1

    print(workspace)
    return 0


def inspect_project_error(project_path: Path) -> int:
    if not project_path.exists():
        print_workspace_error(
            "PROJECT_NOT_FOUND",
            None,
            "project_path",
            f"project path does not exist: {project_path}",
        )
        return 1
    if not project_path.is_dir():
        print_workspace_error(
            "PROJECT_NOT_DIRECTORY",
            None,
            "project_path",
            f"project path is not a directory: {project_path}",
        )
        return 1
    return 0


def metadata_field(data: dict[str, object], field_path: str) -> object:
    current: object = data
    for part in field_path.split("."):
        if not isinstance(current, dict) or part not in current:
            raise KeyError(field_path)
        current = current[part]
    return current


def inspect_workspace(project_path: Path) -> int:
    project_error = inspect_project_error(project_path)
    if project_error:
        return project_error

    workspace = workspace_path(project_path)
    if not workspace.exists():
        print_workspace_error(
            "WORKSPACE_NOT_FOUND",
            workspace,
            None,
            f"workspace does not exist: {workspace}",
        )
        return 1
    if not workspace.is_dir():
        print_workspace_error(
            "WORKSPACE_NOT_DIRECTORY",
            workspace,
            None,
            f"workspace path is not a directory: {workspace}",
        )
        return 1

    metadata_path = workspace / "workspace.json"
    if not metadata_path.exists():
        print_workspace_error(
            "WORKSPACE_METADATA_MISSING",
            workspace,
            "workspace.json",
            "workspace metadata file is missing",
        )
        return 1

    try:
        data = json.loads(metadata_path.read_text(encoding="utf-8"))
    except OSError as exc:
        print_workspace_error(
            "WORKSPACE_METADATA_UNREADABLE",
            workspace,
            "workspace.json",
            f"unable to read workspace metadata: {exc}",
        )
        return 2
    except json.JSONDecodeError as exc:
        print_workspace_error(
            "WORKSPACE_METADATA_PARSE_ERROR",
            workspace,
            "workspace.json",
            f"unable to parse workspace metadata as JSON: {exc}",
        )
        return 2

    if not isinstance(data, dict):
        print_workspace_error(
            "WORKSPACE_METADATA_NOT_OBJECT",
            workspace,
            "workspace.json",
            "workspace metadata root must be an object",
        )
        return 1

    for field in REQUIRED_METADATA_FIELDS:
        if field not in data:
            print_workspace_error(
                "WORKSPACE_METADATA_FIELD_MISSING",
                workspace,
                field,
                f"workspace metadata requires {field}",
            )
            return 1

    boundary = data.get("boundary")
    if not isinstance(boundary, dict):
        print_workspace_error(
            "WORKSPACE_METADATA_VALUE_MISMATCH",
            workspace,
            "boundary",
            "workspace metadata boundary must be an object",
        )
        return 1

    for field in REQUIRED_BOUNDARY_FIELDS:
        field_path = f"boundary.{field}"
        if field not in boundary:
            print_workspace_error(
                "WORKSPACE_METADATA_FIELD_MISSING",
                workspace,
                field_path,
                f"workspace metadata requires {field_path}",
            )
            return 1

    expected_values: dict[str, object] = {
        "schema_version": "v0",
        "workspace_kind": "external_workspace",
        "boundary.writes_product_repo": False,
        "boundary.governance_artifacts_external": True,
    }
    for field_path, expected in expected_values.items():
        try:
            actual = metadata_field(data, field_path)
        except KeyError:
            print_workspace_error(
                "WORKSPACE_METADATA_FIELD_MISSING",
                workspace,
                field_path,
                f"workspace metadata requires {field_path}",
            )
            return 1
        if actual != expected:
            print_workspace_error(
                "WORKSPACE_METADATA_VALUE_MISMATCH",
                workspace,
                field_path,
                f"expected {field_path} to be {expected!r}, got {actual!r}",
            )
            return 1

    expected_paths = {
        "workspace_path": str(workspace),
        "project_path": str(project_path),
    }
    for field, expected in expected_paths.items():
        actual = data.get(field)
        if actual != expected:
            print_workspace_error(
                "WORKSPACE_METADATA_PATH_MISMATCH",
                workspace,
                field,
                f"expected {field} to be {expected!r}, got {actual!r}",
            )
            return 1

    expected_project_id = project_id(project_path)
    actual_project_id = data.get("project_id")
    if actual_project_id != expected_project_id:
        print_workspace_error(
            "WORKSPACE_METADATA_PROJECT_ID_MISMATCH",
            workspace,
            "project_id",
            f"expected project_id to be {expected_project_id!r}, got {actual_project_id!r}",
        )
        return 1

    print("OK workspace metadata valid")
    print(f"workspace: {workspace}")
    print(f"project_id: {expected_project_id}")
    print("schema_version: v0")
    return 0


def list_workspaces() -> int:
    root = local_data_root()
    if not root.exists():
        print(f"no workspaces (root does not exist: {root})")
        return 0
    workspaces = sorted([d for d in root.iterdir() if d.is_dir()])
    if not workspaces:
        print(f"no workspaces under {root}")
        return 0
    print(f"workspaces under {root}:")
    for w in workspaces:
        meta = w / "workspace.json"
        if not meta.exists():
            print(f"  {w.name}  <no workspace.json>  INVALID")
            continue
        try:
            data = json.loads(meta.read_text(encoding="utf-8"))
            project = data.get("project_path", "<unknown>")
            print(f"  {w.name}  project={project}  OK")
        except (OSError, json.JSONDecodeError):
            print(f"  {w.name}  <unreadable>  INVALID")
    return 0


def destroy_workspace(project_path: Path, confirm: bool) -> int:
    workspace = workspace_path(project_path)
    if not workspace.exists():
        print(f"workspace does not exist: {workspace}")
        return 0  # idempotent: already gone
    if not workspace.is_dir():
        print_error(f"workspace path is not a directory: {workspace}")
        return 1
    meta = workspace / "workspace.json"
    if not meta.exists():
        print_error(f"refusing to destroy: workspace.json missing at {workspace}")
        return 1
    try:
        data = json.loads(meta.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print_error(f"refusing to destroy: workspace.json unreadable: {exc}")
        return 1
    if data.get("workspace_path") != str(workspace):
        print_error(
            "refusing to destroy: workspace.json workspace_path mismatch "
            f"(expected {workspace}, got {data.get('workspace_path')})"
        )
        return 1
    if not confirm:
        print(f"would destroy: {workspace}")
        print("re-run with --yes to actually destroy.")
        return 1
    shutil.rmtree(workspace)
    print(f"destroyed: {workspace}")
    return 0


def main(argv: list[str]) -> int:
    try:
        args = parse_args(argv)
        if args.command == "list":
            return list_workspaces()
        project_path = resolve_project(args.project)
        if args.command == "init":
            return init_workspace(project_path)
        if args.command == "where":
            return where_workspace(project_path)
        if args.command == "inspect":
            return inspect_workspace(project_path)
        if args.command == "destroy":
            return destroy_workspace(project_path, args.yes)
        print_error(f"unknown command: {args.command}")
        return 2
    except Exception as exc:  # Defensive boundary for unexpected CLI failures.
        print_error(f"unexpected failure: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
