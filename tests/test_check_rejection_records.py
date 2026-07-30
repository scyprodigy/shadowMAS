import contextlib
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPO_ROOT / "tools" / "check_rejection_records.py"

sys.path.insert(0, str(REPO_ROOT / "tools"))

import check_rejection_records  # noqa: E402

VALID = """\
purpose: a thing was rejected
rejected_claim: build the thing
rejection_scope:
  applies_to: this scope
  exceptions:
    - one allowed case
rejection_reasons:
  - a durable reason
reopen_conditions:
  - some condition
source_refs:
  - some/owner.md
anti_resurrection_note: why this record exists
"""

MISSING_FIELDS = """\
purpose: incomplete record
rejected_claim: build the thing
rejection_scope:
  exceptions:
    - one case
rejection_reasons: []
"""


class RejectionRecordsCurrentStateTests(unittest.TestCase):
    def test_current_instances_satisfy_contract(self):
        result = subprocess.run(
            [sys.executable, str(TOOL)],
            capture_output=True, text=True, cwd=REPO_ROOT,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("OK", result.stdout)


class RejectionRecordsUnitTests(unittest.TestCase):
    def setUp(self):
        self.required = check_rejection_records.load_contract()

    def _check(self, body: str) -> list[str]:
        with tempfile.NamedTemporaryFile("w", suffix=".v0.yaml", delete=False) as fh:
            fh.write(body)
            path = Path(fh.name)
        try:
            return check_rejection_records.check_instance(path, self.required)
        finally:
            path.unlink()

    def test_valid_instance_has_no_findings(self):
        self.assertEqual(self._check(VALID), [])

    def test_missing_and_empty_fields_are_found(self):
        findings = self._check(MISSING_FIELDS)
        joined = "\n".join(findings)
        self.assertIn("reopen_conditions", joined)
        self.assertIn("source_refs", joined)
        self.assertIn("anti_resurrection_note", joined)
        self.assertIn("rejection_reasons", joined)  # empty list counts as missing
        self.assertIn("applies_to", joined)

    def test_contract_loaded_from_proposal(self):
        self.assertIn("rejected_claim", self.required)
        self.assertIn("reopen_conditions", self.required)

    def test_main_discovers_and_rejects_invalid_instance(self):
        proposal_body = """\
required_fields:
  rejected_claim: {}
  reopen_conditions: {}
"""
        invalid_body = """\
purpose: discovered but invalid
"""
        with tempfile.TemporaryDirectory() as tmp:
            rationale = Path(tmp)
            proposal = rationale / "rejection_record.PROPOSAL.v0.yaml"
            proposal.write_text(proposal_body, encoding="utf-8")
            (rationale / "rejection_probe.v0.yaml").write_text(
                invalid_body, encoding="utf-8"
            )
            stdout = io.StringIO()
            with (
                patch.object(
                    check_rejection_records, "RATIONALE_DIR", rationale
                ),
                patch.object(
                    check_rejection_records, "PROPOSAL", proposal
                ),
                contextlib.redirect_stdout(stdout),
            ):
                code = check_rejection_records.main()

        output = stdout.getvalue()
        self.assertEqual(code, 1, msg=output)
        self.assertIn("checked 1 rejection_record instance(s)", output)
        self.assertIn("missing or empty required field", output)


if __name__ == "__main__":
    unittest.main()
