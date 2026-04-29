#!/usr/bin/env python3
"""Minimal external shadowMAS workspace helper.

Direct use:
  python3 05_scripts/workspace/shadowmas_workspace.py init --project <project-path>
  python3 05_scripts/workspace/shadowmas_workspace.py where --project <project-path>
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


WORKSPACE_SUBDIRS = ["packets", "reviews", "handoffs", "runs"]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create or locate an external shadowMAS workspace for a product repo "
            "without writing into the product repo."
        )
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name in ("init", "where"):
        command = subparsers.add_parser(name)
        command.add_argument("--project", required=True, help="Product project directory path")

    return parser.parse_args(argv)


def print_error(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)


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


def main(argv: list[str]) -> int:
    try:
        args = parse_args(argv)
        project_path = resolve_project(args.project)
        if args.command == "init":
            return init_workspace(project_path)
        if args.command == "where":
            return where_workspace(project_path)
        print_error(f"unknown command: {args.command}")
        return 2
    except Exception as exc:  # Defensive boundary for unexpected CLI failures.
        print_error(f"unexpected failure: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
