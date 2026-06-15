# 03_memory/shared_memory/README | shared_memory memory plane: empty; one provisional placement was made and withdrawn 2026-06-15
# related: [03_memory, MEMORY-PLANE-HARNESS, SHADOWMAS-CURRENT-TRUTH, SHADOWMAS-FILE-STATUS-REGISTRY, PROMOTION-GATE-SEMANTICS, check_placement_provenance]
# phase: empty-after-withdrawal

# shared_memory

This directory is declared by the shadowMAS v0 memory-plane structure (see `03_memory/MEMORY-PLANE-HARNESS.v0.en.md` and the Memory Direction section of `01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md`). It currently holds no memory artifact.

On 2026-06-15 a first memory was provisionally promoted T4->T3 here and then **withdrawn the same day** after a negative audit (`07_working/drafts/rationale/NEGATIVE-AUDIT-SESSION-2026-06-15.v0.en.md`) found the promotion self-authored, self-executed, and self-approved on self-generated evidence. The candidate returned to candidate status; nothing remains placed.

Placement here does not make an artifact canonical truth (`approved_shared` is reusable memory below T2) and it does not happen by merely dropping a file in: every artifact in this folder must have an approved promotion review packet referencing it, now enforced in CI by `tools/check_placement_provenance.py`. Promotion also requires the eligibility preconditions (`tools/check_promotion_eligibility.py`), a promotion review packet, and — per the negative audit — independent validation when the same agent authored and would approve it. Placed artifacts remain subject to `tools/check_memory_validity.py`.
