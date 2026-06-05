#!/usr/bin/env python3
"""shadowmas run -- inspectable DRY-RUN of the packet flow (no real stage logic).

Logical command:  shadowmas run --dry <task_packet.yaml> [--workspace <ws> | --runs-dir <dir>]
Direct use:       python3 05_scripts/run/shadowmas_run.py --dry <task_packet.yaml> [...]

It walks a task_packet through the documented stage sequence WITHOUT executing any
stage. Only `validate` is implemented (it reuses the existing validator); every other
stage is a labelled NOT-IMPLEMENTED no-op. Each transition is appended to an
append-only, SHA-256 hash-chained run log (per SESSION-LOG-INTEGRITY).

Boundary: representation-valid is not authority-valid. This is dry-run only. It is not a
runner, not a daemon, not runtime enforcement, and writes nothing into a product repo.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # keep check_no_pollution green even without the env var

import argparse
import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


# (stage_name, implemented?) -- only `validate` is implemented in v0.
FLOW_STAGES = [
    ("runtime_inbox", False),
    ("packetize", False),
    ("validate", True),
    ("review_queue", False),
    ("approved_or_rejected", False),
    ("writeback", False),
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_validator() -> Any:
    vpath = repo_root() / "05_scripts" / "validate" / "shadowmas_validate.py"
    spec = importlib.util.spec_from_file_location("shadowmas_validate", vpath)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load validator at {vpath}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod  # required so the module's @dataclass can resolve its module
    spec.loader.exec_module(mod)
    return mod


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def compute_entry_hash(entry: dict[str, Any]) -> str:
    payload = {k: v for k, v in entry.items() if k != "entry_hash"}
    blob = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def make_entry(
    index: int, prev_hash: str, run_id: str, packet: str, stage: str,
    status: str, implemented: bool, note: str,
) -> dict[str, Any]:
    entry = {
        "entry_id": str(index),
        "prev_hash": prev_hash,
        "created_at": utc_now(),
        "payload": {
            "run_id": run_id,
            "packet": packet,
            "stage": stage,
            "status": status,
            "implemented": implemented,
            "dry_run": True,
            "note": note,
        },
    }
    entry["entry_hash"] = compute_entry_hash(entry)
    return entry


def resolve_runs_dir(workspace: str | None, runs_dir: str | None) -> Path | None:
    if runs_dir:
        return Path(runs_dir).expanduser().resolve()
    if workspace:
        ws = Path(workspace).expanduser().resolve()
        if not (ws / "workspace.json").exists():
            raise FileNotFoundError(
                f"--workspace has no workspace.json (not a shadowMAS external workspace): {ws}"
            )
        return ws / "runs"
    return None


def validate_stage(packet_path: Path) -> tuple[bool, str]:
    """Return (passed, note). Reuses the existing validator; no duplication."""
    validator = load_validator()
    data, code = validator.load_yaml(packet_path)
    if code != 0:
        return False, "packet failed to load/parse"
    errors, packet_type = validator.validate_packet(data, packet_path)
    if errors:
        return False, f"{len(errors)} validation error(s); first={errors[0].code}"
    if packet_type != "task_packet":
        return False, f"run expects task_packet, got {packet_type}"
    return True, "representation-valid task_packet (authority-valid NOT implied)"


def dry_run(packet: str, runs_dir: Path | None) -> int:
    packet_path = Path(packet).expanduser().resolve()
    run_id = f"{packet_path.stem}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')}"

    log_file: Path | None = None
    if runs_dir is not None:
        runs_dir.mkdir(parents=True, exist_ok=True)
        log_file = runs_dir / f"run_{run_id}.log.jsonl"

    print(f"shadowmas run --dry  (run_id={run_id})")
    print(f"packet: {packet_path}")
    print("flow (DRY-RUN; only 'validate' is implemented):")

    markers = {"PASS": "OK ", "SKIP": ".. ", "STOP": "XX "}
    prev_hash = "genesis"
    exit_code = 0
    for index, (stage, implemented) in enumerate(FLOW_STAGES):
        stopped = False
        if stage == "validate":
            passed, note = validate_stage(packet_path)
            status = "PASS" if passed else "STOP"
            if not passed:
                stopped = True
                exit_code = 1
        elif implemented:
            status, note = "PASS", "implemented"
        else:
            status, note = "SKIP", "NOT-IMPLEMENTED (dry-run no-op)"

        entry = make_entry(index, prev_hash, run_id, str(packet_path), stage,
                           status, implemented, note)
        prev_hash = entry["entry_hash"]

        print(f"  {markers[status]}{stage:22s} {status:4s} {note}")
        if log_file is not None:
            with log_file.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(entry, ensure_ascii=False) + "\n")

        if stopped:
            print(f"  -- stopped at {stage}: {note}")
            break

    if log_file is not None:
        print(f"run log (append-only, hash-chained): {log_file}")
    else:
        print("run log: not persisted (pass --workspace <ws> or --runs-dir <dir> to persist)")
    return exit_code


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspectable DRY-RUN of the shadowMAS packet flow (no real stage logic)."
    )
    parser.add_argument("--dry", action="store_true", required=True,
                        help="dry-run only; required (no non-dry mode exists in v0)")
    parser.add_argument("packet", help="task_packet YAML file")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--workspace", help="external shadowMAS workspace (writes log to <ws>/runs/)")
    group.add_argument("--runs-dir", help="explicit directory for the run log")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    try:
        args = parse_args(argv)
        runs_dir = resolve_runs_dir(args.workspace, args.runs_dir)
    except (FileNotFoundError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return dry_run(args.packet, runs_dir)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
