# 03_memory/shared_memory/README | shared_memory memory plane: first placement made 2026-06-15
# related: [03_memory, MEMORY-PLANE-HARNESS, SHADOWMAS-CURRENT-TRUTH, SHADOWMAS-FILE-STATUS-REGISTRY, PROMOTION-GATE-SEMANTICS]
# phase: first-placement

# shared_memory

This directory is declared by the shadowMAS v0 memory-plane structure (see `03_memory/MEMORY-PLANE-HARNESS.v0.en.md` and the Memory Direction section of `01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md`).

It held no artifact until 2026-06-15, when the first memory was promoted T4->T3 under `07_working/drafts/PROMOTION-GATE-SEMANTICS.PROPOSAL.v0.en.md`: `MEMORY-COMPILED-SURFACE-DISCIPLINE.v0.yaml` (status `approved_shared`). The promotion-gate proposal itself is still working-only pending owner review; this first placement was made under owner-delegated authority and is recorded in the file-status registry.

No backend, schema, or contract for this plane is canonical yet. Placement here does not make an artifact canonical truth: `approved_shared` is reusable memory below T2. Promotion into this folder requires the eligibility preconditions (`tools/check_promotion_eligibility.py`), a promotion review packet, and a human or delegated decision; nothing becomes shared memory merely by being placed here. Placed artifacts remain subject to `tools/check_memory_validity.py`.
