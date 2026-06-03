#!/usr/bin/env python3
"""Run the controlled-alpha first-user smoke path.

This is an evaluator convenience wrapper around existing local checks. It is
not a runtime engine and does not make authority or production-safety claims.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


BOUNDARY_TEXT = (
    "This smoke script checks local representation and workspace mechanics only.\n"
    "It does not prove production safety, runtime authority enforcement, "
    "automatic correctness, or product-repo approval.\n"
    "A schema-valid packet is not necessarily authority-valid."
)


class SmokeFailure(RuntimeError):
    """Raised when one smoke step fails."""


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the shadowMAS controlled local first-user smoke path.",
        epilog=BOUNDARY_TEXT,
    )
    parser.add_argument(
        "--skip-unit-tests",
        action="store_true",
        help="skip python3 -m unittest discover tests",
    )
    return parser.parse_args(argv)


def has_fail_signal(result: subprocess.CompletedProcess[str]) -> bool:
    return "FAIL:" in f"{result.stdout}\n{result.stderr}"


def print_failure_output(result: subprocess.CompletedProcess[str]) -> None:
    print(f"  exit: {result.returncode}")
    if result.stdout:
        print("  stdout:")
        print(result.stdout.rstrip())
    if result.stderr:
        print("  stderr:")
        print(result.stderr.rstrip())


def run_step(
    name: str,
    command: list[str],
    *,
    cwd: Path,
    env: dict[str, str] | None = None,
    expect_l1_negative: bool = False,
) -> subprocess.CompletedProcess[str]:
    print(f"[smoke] {name}")
    result = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
    )

    if expect_l1_negative:
        if result.returncode != 0 and has_fail_signal(result):
            print("  OK expected negative fixture failed")
            return result
        print_failure_output(result)
        raise SmokeFailure(f"{name} did not show expected negative behavior")

    if result.returncode == 0:
        print("  OK")
        return result

    print_failure_output(result)
    raise SmokeFailure(f"{name} failed")


def is_under(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
    except ValueError:
        return False
    return True


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SmokeFailure(message)


def run_temp_workspace_flow(root: Path) -> None:
    print("[smoke] temp-only workspace attach/review flow")
    tmp_path: Path | None = None
    with tempfile.TemporaryDirectory(prefix="shadowmas-first-user-smoke-") as tmp:
        tmp_path = Path(tmp)
        project_path = tmp_path / "product-repo"
        project_path.mkdir()
        xdg_root = tmp_path / "xdg"
        env = os.environ.copy()
        env["XDG_DATA_HOME"] = str(xdg_root)

        workspace_tool = root / "05_scripts" / "workspace" / "shadowmas_workspace.py"
        validator = root / "05_scripts" / "validate" / "shadowmas_validate.py"

        run_step(
            "workspace init",
            [sys.executable, str(workspace_tool), "init", "--project", str(project_path)],
            cwd=root,
            env=env,
        )
        where = run_step(
            "workspace where",
            [sys.executable, str(workspace_tool), "where", "--project", str(project_path)],
            cwd=root,
            env=env,
        )
        workspace = Path(where.stdout.strip())
        require(is_under(workspace, xdg_root), f"workspace is outside temp XDG root: {workspace}")

        run_step(
            "workspace inspect",
            [sys.executable, str(workspace_tool), "inspect", "--project", str(project_path)],
            cwd=root,
            env=env,
        )

        for name in ("packets", "reviews", "handoffs", "runs"):
            require((workspace / name).is_dir(), f"missing workspace directory: {name}/")

        task_packet = workspace / "packets" / "first_attach_packet.v0.yaml"
        review_packet = workspace / "reviews" / "first_review_packet.v0.yaml"
        shutil.copyfile(root / "examples" / "packets" / "task_packet.valid.v0.yaml", task_packet)
        shutil.copyfile(
            root / "examples" / "packets" / "review_packet.valid.v0.yaml",
            review_packet,
        )

        run_step("copied task packet validator", [sys.executable, str(validator), str(task_packet)], cwd=root)
        run_step(
            "copied review packet validator",
            [sys.executable, str(validator), str(review_packet)],
            cwd=root,
        )

        require(project_path.is_dir(), "temp product path no longer exists")
        require(list(project_path.iterdir()) == [], "temp product path was polluted")
        print("  OK")

    if tmp_path is not None:
        require(not tmp_path.exists(), f"temp directory was not cleaned up: {tmp_path}")


def run_smoke(*, skip_unit_tests: bool = False) -> int:
    root = repo_root()
    print(BOUNDARY_TEXT)

    if not skip_unit_tests:
        run_step(
            "unit tests",
            [sys.executable, "-m", "unittest", "discover", "tests"],
            cwd=root,
        )

    validator = root / "05_scripts" / "validate" / "shadowmas_validate.py"
    run_step(
        "task packet validator",
        [sys.executable, str(validator), "examples/packets/task_packet.valid.v0.yaml"],
        cwd=root,
    )
    run_step(
        "review packet validator",
        [sys.executable, str(validator), "examples/packets/review_packet.valid.v0.yaml"],
        cwd=root,
    )
    run_step(
        "memory packet validator",
        [sys.executable, str(validator), "examples/packets/memory_packet.valid.v0.yaml"],
        cwd=root,
    )
    run_step(
        "candidate registry checker",
        [sys.executable, "tools/check_candidate_registry.py"],
        cwd=root,
    )
    run_step(
        "L1 positive fixture",
        [sys.executable, "tools/shadowmas_minimal_validator.py", "examples/demo_signal_governance.json"],
        cwd=root,
    )
    run_step(
        "L1 negative fixture",
        [
            sys.executable,
            "tools/shadowmas_minimal_validator.py",
            "examples/demo_signal_governance_violation.json",
        ],
        cwd=root,
        expect_l1_negative=True,
    )
    run_step(
        "L2 inspector smoke",
        [
            sys.executable,
            "tools/inspect_l2_fixture.py",
            "examples/traces/l2_handoff/ephemeral_handoff_memory_promotion.json",
        ],
        cwd=root,
    )
    run_temp_workspace_flow(root)
    print("[smoke] OK controlled local evaluation smoke completed")
    return 0


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        return run_smoke(skip_unit_tests=args.skip_unit_tests)
    except SmokeFailure as exc:
        print(f"[smoke] FAIL {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
