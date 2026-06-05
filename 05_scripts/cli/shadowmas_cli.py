#!/usr/bin/env python3
"""shadowmas -- thin dispatcher routing to existing shadowMAS script surfaces.

  python3 05_scripts/cli/shadowmas_cli.py validate <packet-file>
  python3 05_scripts/cli/shadowmas_cli.py workspace <init|where|inspect|list|destroy> [...]
  python3 05_scripts/cli/shadowmas_cli.py run --dry <task_packet> [--workspace <ws> | --runs-dir <dir>]

A router, not a framework. Each subcommand delegates to its existing module unchanged;
this makes the documented `shadowmas <verb>` logical command real without duplicating logic.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # keep check_no_pollution green even without the env var

import importlib.util
from pathlib import Path
from typing import Any


ROUTES = {
    "validate": ("validate", "shadowmas_validate.py"),
    "workspace": ("workspace", "shadowmas_workspace.py"),
    "run": ("run", "shadowmas_run.py"),
}

USAGE = (
    "usage: shadowmas <command> [args]\n"
    "commands:\n"
    "  validate <packet-file>\n"
    "  workspace <init|where|inspect|list|destroy> [...]\n"
    "  run --dry <task_packet> [--workspace <ws> | --runs-dir <dir>]\n"
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_module(subdir: str, filename: str) -> Any:
    path = repo_root() / "05_scripts" / subdir / filename
    spec = importlib.util.spec_from_file_location(filename[:-3], path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # required so a loaded module's @dataclass can resolve itself
    spec.loader.exec_module(module)
    return module


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(USAGE)
        return 0 if argv else 2
    command, rest = argv[0], argv[1:]
    if command not in ROUTES:
        print(f"ERROR: unknown command {command!r}\n\n{USAGE}", file=sys.stderr)
        return 2
    subdir, filename = ROUTES[command]
    return load_module(subdir, filename).main(rest)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
