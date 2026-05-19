import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = REPO_ROOT / "examples" / "traces" / "l2_handoff"
INDEX = TRACE_DIR / "index.json"

REQUIRED_KEYS = {
    "fixture_id",
    "title",
    "level",
    "authority_layers_involved",
    "trace_steps",
    "expected_boundary_violation",
    "expected_safe_behavior",
    "non_claims",
}

REQUIRED_NON_CLAIMS = {
    "not_a_validation_result",
    "not_runtime_behavior",
    "not_runtime_enforcement",
    "not_construct_validity_evidence",
    "not_predictive_validity_evidence",
}


class L2HandoffTraceFixtureTests(unittest.TestCase):
    def test_index_lists_three_l2_handoff_fixtures(self):
        data = json.loads(INDEX.read_text(encoding="utf-8"))
        fixtures = data["fixtures"]

        self.assertEqual(data["level"], "L2")
        self.assertEqual(len(fixtures), 3)
        for item in fixtures:
            self.assertTrue((TRACE_DIR / item["file"]).exists(), item)

    def test_l2_trace_fixtures_have_required_skeleton_shape(self):
        data = json.loads(INDEX.read_text(encoding="utf-8"))

        for item in data["fixtures"]:
            path = TRACE_DIR / item["file"]
            fixture = json.loads(path.read_text(encoding="utf-8"))

            self.assertTrue(REQUIRED_KEYS.issubset(fixture), path.name)
            self.assertEqual(fixture["level"], "L2", path.name)
            self.assertGreaterEqual(len(fixture["trace_steps"]), 2, path.name)
            self.assertTrue(REQUIRED_NON_CLAIMS.issubset(fixture["non_claims"]), path.name)
            self.assertIn("unsafe_transition", fixture["expected_boundary_violation"], path.name)

    def test_l2_trace_fixture_authority_layer_consistency(self):
        data = json.loads(INDEX.read_text(encoding="utf-8"))

        for item in data["fixtures"]:
            path = TRACE_DIR / item["file"]
            fixture = json.loads(path.read_text(encoding="utf-8"))

            declared = set(fixture["authority_layers_involved"])
            step_layers = {step["authority_layer"] for step in fixture["trace_steps"]}

            self.assertTrue(
                step_layers.issubset(declared),
                f"{path.name}: trace step layers {step_layers - declared} missing from authority_layers_involved",
            )
            self.assertTrue(
                declared.issubset(step_layers),
                f"{path.name}: authority_layers_involved {declared - step_layers} not present in any trace step",
            )


if __name__ == "__main__":
    unittest.main()
