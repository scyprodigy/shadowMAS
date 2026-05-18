# examples_readme | index for public example fixtures and validator first-run usage
# related: [shadowmas_minimal_validator, demo_signal_governance, mutations_corpus, l2_handoff_traces]
# phase: public_examples_index

# shadowMAS Examples

## Purpose
Files under `examples/` are non-canonical illustrative examples for first-run validator usage.

They help a cold user run the current read-only packet validator without inventing a packet from scratch.

## Available examples
- `examples/packets/task_packet.valid.v0.yaml`: minimal valid `task_packet` example for a harmless illustrative documentation task.
- `examples/mutations/`: L1 mutation fixtures are available under `examples/mutations/`. These examples are fixture material, not validation results.
- `examples/traces/l2_handoff/`: L2 multi-step handoff trace fixture skeletons are available under `examples/traces/l2_handoff/`. These examples are fixture material, not validation results.

## Run the validator
Run commands from the repository root.

Validate the current example with:

```bash
python3 05_scripts/validate/shadowmas_validate.py examples/packets/task_packet.valid.v0.yaml
```

Expected success output:

```text
OK examples/packets/task_packet.valid.v0.yaml
packet_type: task_packet
schema_version: v0
checks: passed
```

## Boundary
Example files are not truth files.

They are not packet schemas.

They are not required for product repos.

They are not recommended real tasks, hidden fixtures, or a test suite.

The validator checks packet shape and contract rules. It does not execute tasks, run agents, write back changes, or promote packet contents into truth.

Do not copy examples into product repos as product truth.
