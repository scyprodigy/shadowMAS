> status: working draft / disposition board
> authority: none
> not canonical truth
> not product specification
> not packet schema law
> not runtime implementation
> not a product repo patch
> source basis: DISPATCH-DEV-MAS-MERGE-DOSSIER.v1.en.md.txt and merge-dossier.md.txt

# DISPATCH-MAS-CLEANUP-DISPOSITION-BOARD.v0

## Purpose
Preserve useful shadow-side concepts recovered from dispatch-dev MAS cleanup without treating dispatch-dev as shadowMAS truth.

This board is a bounded disposition record. It does not reopen commercial repo cleanup, does not patch a product repo, and does not promote dossier content into canonical shadowMAS truth.

## Cleanup Boundary
- dispatch-dev cleanup is treated as complete enough for this board.
- This patch must not touch the commercial repo.
- Product-domain truth remains product-local.
- shadowMAS may learn governance concepts from cleanup, but must not import product-specific assumptions as truth.
- Dossier content is source evidence and classification input, not current shadowMAS authority.

## Already Represented / Safe To Stop Tracking As Raw Dispatch Residue
- Hard separation between shadowMAS and product repos appears represented in current shadowMAS truth and layering language.
- L/T/R or equivalent separation appears represented in current governance vocabulary.
- Read-order / truth-priority discipline appears represented through no-blind-traversal, layered reading, and source-artifact discipline.
- Working/formal/archive style governance appears represented as a mature repo-local governance pattern, even if not a shadowMAS-specific invention.
- Memory is not truth, cache is not authority, and promotion gates are required appears represented in the current memory and governance direction.

## Promote Candidates For Future Narrow Patches

### MAS vs Product Boundary
Why it matters:
- prevents product-domain truth pollution
- keeps product repos independently operable
- keeps shadowMAS governance from becoming product-local authority

Likely target files:
- `01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md`
- `01_truth/SHADOWMAS-PROMPT-LAYERING-CONTRACT.v0.en.md`
- future write-back or project-intake contracts if created

Blocked by:
- decision on whether existing boundary wording is sufficient or needs a narrow audit patch

Do not implement now.

### Memory / Promotion / Invalidation Governance
Why it matters:
- cleanup highlighted stale retrieval, summary drift, cache poisoning, precedence inversion, shared-memory contamination, and promotion without invalidation
- these are shadow-relevant governance risks, not product-domain facts

Likely target files:
- `03_memory/MEMORY-PLANE-HARNESS.v0.en.md`
- `03_memory/registry/SHADOWMAS-FILE-STATUS-REGISTRY.v0.yaml`
- future invalidation policy if created

Blocked by:
- decision on whether current memory harness and registry wording already covers the cleanup-derived risks sufficiently

Do not implement now.

### Cleanup-Derived Quality Gaps
Why it matters:
- citation artifact contamination, ADR lifecycle, project-state wording precision, external governance boundary wording, and frozen truth-priority need are reusable quality concerns
- these can become review checklist material without importing product specifics

Likely target files:
- future quality checklist or review-surface draft
- `01_truth/SHADOWMAS-CHANGE-IMPACT-MAP.v0.en.md` only if formal change-impact meaning changes

Blocked by:
- decision on whether these belong in a checklist, rationale note, review packet guidance, or formal truth patch

Do not implement now.

### Working / Formal / Archive Governance
Why it matters:
- cleanup showed the pattern can reduce active-path contamination
- it may be useful as general file-status / workspace hygiene guidance

Likely target files:
- `03_memory/registry/SHADOWMAS-FILE-STATUS-REGISTRY.v0.yaml`
- `07_working/DRAFT-ENTRY-RULE.v0.en.md`
- future repo-structure guidance if created

Blocked by:
- decision on whether current registry and working-area handling already cover the pattern well enough

Do not implement now.

## Rationale-Only Concepts
- Packet system concept recovered from dispatch-dev remains rationale only; it does not supply concrete schema truth.
- Review surface discipline remains rationale only: bounded review/output preference, changed files, summary, unresolved items, risks, temporary assumptions, next decisions, and human final review.
- Planner / worker / reviewer role split remains rationale only when expressed without model-brand binding.
- Runtime / tooling boundary principle remains rationale only; exclude product-specific Windows, WSL, Docker, host, and repo placement details.
- Still-valuable cleanup gaps may serve as checklist material unless later promoted through a separate governed patch.

## Discard / Do Not Carry Forward
- Product repo as MAS global entry surface.
- Product formal layer as MAS governance host.
- Product data layer as packet entry layer.
- Product architecture layer as T/O/R or L/T/R governance host.
- Model-brand routing such as Claude as planner / MiniMax as worker.
- Single-indexer constitution as general truth.
- Archive-era wording that treats old docs as active global truth.
- Any guidance depending on deleted or nonexistent MAS files inside the product repo.

## Future Patch Queue

| Order | Queue item | Candidate target file(s) | Why it matters | Blocked by what decision | Safe to patch independently? |
|---|---|---|---|---|---|
| 1 | product-repo hard boundary wording audit | current truth, prompt layering, future write-back/project-intake contracts | prevents product truth contamination | whether existing boundary wording is sufficient | Yes |
| 2 | memory / promotion / invalidation clarification if gaps remain | memory harness, registry, future invalidation policy | prevents stale retrieval and memory authority leakage | whether current memory governance already covers cleanup-derived risks | Yes, with memory-surface review |
| 3 | cleanup-derived quality checklist | future checklist or review-surface draft | turns cleanup lessons into reusable review prompts | checklist vs formal truth vs review packet guidance | Yes |
| 4 | rationale note for planner/worker/reviewer role split without model binding | future rationale/operator note | preserves useful collaboration pattern without tool lock-in | whether role split needs formal contract or rationale only | Yes |
| 5 | runtime boundary rationale note without product-specific host assumptions | future operator/runtime rationale | preserves runtime-boundary principle without importing product host facts | whether runtime boundary belongs in rationale or adapter contract | No, may interact with runtime-adapter decisions |

## External File Deletion Condition
After this board is committed and reviewed, the owner may delete:
- `DISPATCH-DEV-MAS-MERGE-DOSSIER.v1.en.md.txt`
- `merge-dossier.md.txt`

## Do Not Promote Yet
This board is working evidence only. It classifies cleanup-derived concepts so later work can decide what to patch, keep as rationale, or discard.

No canonical truth, packet schema, memory registry, runtime file, product repo file, validator, CI, or implementation is changed by this board.
