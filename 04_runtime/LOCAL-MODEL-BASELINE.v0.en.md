# LOCAL-MODEL-BASELINE.v0.en.md

## Purpose
This file records the current local model baseline for shadowMAS v0.

Its goal is to define:
- which local models are currently selected
- what each model is used for
- where the preferred deployment side is
- what this baseline is not trying to do yet

## Current Model Baseline

### Text model
- `qwen3:8b`

Current intended use:
- low-cost text normalization
- extraction support
- context reduction support
- structured summarization
- simple governance-adjacent helper tasks
- not final human-authority decision making

### Embedding model
- `mxbai-embed-large`

Current intended use:
- semantic embedding generation
- retrieval support
- chunk recall
- memory candidate lookup
- code/document structure retrieval support

## Preferred Deployment Direction
Current preferred deployment side:
- Linux / WSL primary

## Why Linux / WSL primary
Current data gravity is on the Linux side:
- repo lives there
- Docker workloads live there
- database direction lives there
- future cloud/deployment direction is Linux-oriented

Therefore:
- prompt/rules/scripts/model service should stay as close to the data as possible
- avoid unnecessary cross-side path handling and file transport
- reduce complexity in codebase indexing and retrieval flows

## Windows Position
Windows is not currently the preferred long-term primary runtime side for shadowMAS local model service.

Windows may still be used for:
- human UI
- IDE hosts
- comparison/testing
- temporary convenience

But shadowMAS v0 baseline treats Linux / WSL as the primary side.

## Current Work Pattern
Preferred current flow:

1. read relevant repo/doc/runtime artifacts from Linux-side context
2. chunk/select relevant material
3. generate embeddings where needed
4. recall targeted chunks
5. pass reduced context to the text model
6. output normalized text or structured helper output
7. hand off to higher-level review, mergeback, or human decision

## Intended Model Roles

### `qwen3:8b`
Best suited for:
- cheap text cleanup
- paragraph-level summarization
- controlled extraction tasks
- sentence/paragraph scoring for compression
- helper-level transformation work

Not intended for:
- final governance authority
- blind whole-repo reasoning
- replacing project truth decisions
- replacing human approval

### `mxbai-embed-large`
Best suited for:
- embedding documents/chunks
- semantic retrieval
- memory candidate recall
- code/document proximity lookup
- index-assisted retrieval pipelines

Not intended for:
- truth arbitration
- direct decision authority
- replacing structured packet/registry discipline

## Compression Position
Compression is treated as a default optimization subsystem for selected lanes,
not as the foundational truth layer.

Use compression by default for:
- long natural-language background
- long history summary
- oversized RAG context
- pre-merge condensation
- pre-small-model context reduction

Do not use compression for:
- packet YAML
- JSON/YAML schema truth
- API contracts
- migrations
- field-level truth definitions
- code patches and diffs

Current preferred style:
- sentence-level filtering
- paragraph-level filtering
- inspectable/reversible compression
- learn from LLMLingua-like ideas without adopting the whole framework

## Retrieval Position
Retrieval may become strong, but retrieval is not the truth arbiter.

That means:
- embedding hit != approved truth
- vector similarity != promotion
- recalled chunk != canonical source

Repo-first truth still wins.

## Current Technology Bias
Prefer:
- Ollama as the local model serving direction
- local-first execution
- simple inspectable scripts
- structured chunk retrieval
- Chroma first for v0
- Qdrant later only if stronger filtering/scale is needed

Do not adopt early:
- heavyweight orchestration frameworks
- memory-first frameworks that obscure truth boundaries
- automatic prompt optimization frameworks as runtime dependency
- premature multi-provider abstraction layers

## AMD / GPU Position
GPU acceleration is not a prerequisite for shadowMAS v0.

v0 baseline must remain valid even if:
- GPU acceleration is unavailable
- Linux-side GPU support is incomplete
- CPU-only operation is slower

Performance improvement is secondary to correctness and inspectability.

## What This Baseline Is Not Yet
This file does not yet finalize:
- exact install steps
- exact Ollama runtime service management
- exact embedding pipeline implementation
- exact Chroma folder layout
- exact Linux-vs-Windows comparison benchmark
- exact adapter prompt behavior per host tool

## v0 Rule
For v0-min-landing-skeleton, the local model baseline only needs to do three things clearly:
1. record which models are selected
2. record what they are for
3. record which side is primary
<!-- SHADOWMAS_PRINCIPLES_PATCH:BEGIN -->
## Additional Routing and Normalization Rules

### Capability Routing Rule
Model selection must not be based on model name alone.

Routing must consider:
- task shape
- data shape
- output format requirements
- truth risk
- supervision mode
- acceptable latency/cost tradeoff

Examples:
- semantic lookup -> embedding lane
- small text cleanup -> local small text model lane
- schema validation -> rules/schema lane, not freeform text reasoning
- final governance decision -> human or high-authority review lane

### Prompt Compact Position
Prompt/context compaction is already part of the design direction.

It should be used where:
- long background must be reduced
- long history must be condensed
- oversized RAG context must be trimmed
- low-cost local helper lanes need smaller context

It should not rewrite:
- schema truth
- packet truth
- registry truth
- API/migration/field-level canonical definitions

### Prompt Cache Position
Prompt cache is acknowledged conceptually, but not yet formalized as a dedicated v0 artifact.

Current v0 rule:
- reuse and reduction are allowed
- cache must not outrank canonical truth
- cache design should remain subordinate to repo-first truth and invalidation rules

### Machine-First Rule
Machine-facing runtime files should prefer:
- minimal prose
- explicit field meaning
- stable format
- low ambiguity
- easy future normalization by Codex or validators
<!-- SHADOWMAS_PRINCIPLES_PATCH:END -->
