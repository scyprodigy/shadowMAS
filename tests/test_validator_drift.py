import contextlib
import io
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPO_ROOT / "tools" / "check_validator_drift.py"

sys.path.insert(0, str(REPO_ROOT / "tools"))

import check_validator_drift  # noqa: E402


class ValidatorSchemaDriftTests(unittest.TestCase):
    def test_no_drift_on_current_state(self):
        """Validator constants must match packet yaml schemas across every checked surface."""
        result = subprocess.run(
            [sys.executable, str(CHECKER)],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        )
        self.assertEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertIn("OK", result.stdout)

    def test_each_compared_surface_detects_schema_only_drift(self):
        cases = [
            ("PACKET_TYPES", "SHELL_PATH", ("required_shared_fields", "packet_type", "allowed"), "list"),
            ("SHARED_REQUIRED", "SHELL_PATH", ("required_shared_fields",), "mapping"),
            ("FAMILY_REQUIRED[task_packet]", "TASK_PATH", ("required_fields",), "mapping"),
            ("FAMILY_REQUIRED[memory_packet]", "MEMORY_PATH", ("required_fields",), "mapping"),
            ("FAMILY_REQUIRED[review_packet]", "REVIEW_PATH", ("required_fields",), "mapping"),
            ("STATUS_VALUES[task_packet]", "TASK_PATH", ("allowed_status_values",), "list"),
            ("STATUS_VALUES[memory_packet]", "MEMORY_PATH", ("allowed_status_values",), "list"),
            ("STATUS_VALUES[review_packet]", "REVIEW_PATH", ("allowed_status_values",), "list"),
            ("SUPERVISION_MODE_VALUES", "SHELL_PATH", ("required_shared_fields", "supervision_mode", "allowed"), "list"),
            ("RISK_VALUES", "SHELL_PATH", ("required_shared_fields", "risk", "allowed"), "list"),
            ("REVIEW_RECOMMENDATION_VALUES", "REVIEW_PATH", ("required_fields", "recommendation", "allowed"), "list"),
            ("PROMOTION_CANDIDATE_VALUES", "MEMORY_PATH", ("required_fields", "promotion_candidate", "allowed"), "list"),
        ]

        for surface, path_attr, yaml_path, container_kind in cases:
            with self.subTest(surface=surface), tempfile.TemporaryDirectory() as tmp:
                source = getattr(check_validator_drift, path_attr)
                data = yaml.safe_load(source.read_text(encoding="utf-8"))
                target = data
                for key in yaml_path:
                    target = target[key]
                if container_kind == "list":
                    target.append("__mutation_probe__")
                else:
                    target["__mutation_probe__"] = {"type": "string"}

                mutated = Path(tmp) / source.name
                mutated.write_text(
                    yaml.safe_dump(data, sort_keys=False), encoding="utf-8"
                )
                stdout = io.StringIO()
                with patch.object(check_validator_drift, path_attr, mutated):
                    with contextlib.redirect_stdout(stdout):
                        code = check_validator_drift.main()

                output = stdout.getvalue()
                self.assertEqual(code, 1, msg=output)
                self.assertIn(f"surface: {surface}", output)

    def test_validator_side_only_drift_is_detected(self):
        """Pairs with the schema-side test above so the contract is symmetric:
        a value the validator gained and the schema never declared is drift
        too. Without this, a checker that only reports yaml-side additions
        looks healthy."""
        with tempfile.TemporaryDirectory() as tmp:
            # mirror the repo layout: the validator resolves its tools/ import
            # relative to its own __file__, so a bare copy would not load
            root = Path(tmp)
            validate_dir = root / "05_scripts" / "validate"
            tools_dir = root / "tools"
            validate_dir.mkdir(parents=True)
            tools_dir.mkdir()
            shutil.copyfile(REPO_ROOT / "tools" / "_shadowmas_readonly.py",
                            tools_dir / "_shadowmas_readonly.py")

            source = check_validator_drift.VALIDATOR_PATH
            mutated = validate_dir / source.name
            mutated.write_text(
                source.read_text(encoding="utf-8")
                + '\nRISK_VALUES = RISK_VALUES | {"r_probe_validator_only"}\n',
                encoding="utf-8",
            )

            stdout = io.StringIO()
            with (
                patch.object(check_validator_drift, "VALIDATOR_PATH", mutated),
                contextlib.redirect_stdout(stdout),
            ):
                code = check_validator_drift.main()

        output = stdout.getvalue()
        self.assertEqual(code, 1, msg=output)
        self.assertIn("surface: RISK_VALUES", output)

    def test_missing_schema_path_fails_closed(self):
        """A compared path that disappears from a schema must be reported. If
        it is silently skipped, that surface stops being checked at all and
        the tool still exits 0."""
        with tempfile.TemporaryDirectory() as tmp:
            source = check_validator_drift.REVIEW_PATH
            data = yaml.safe_load(source.read_text(encoding="utf-8"))
            del data["required_fields"]["recommendation"]["allowed"]

            mutated = Path(tmp) / source.name
            mutated.write_text(
                yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

            stdout = io.StringIO()
            with (
                patch.object(check_validator_drift, "REVIEW_PATH", mutated),
                contextlib.redirect_stdout(stdout),
            ):
                code = check_validator_drift.main()

        output = stdout.getvalue()
        self.assertEqual(code, 1, msg=output)
        self.assertIn("surface: REVIEW_RECOMMENDATION_VALUES", output)


if __name__ == "__main__":
    unittest.main()
