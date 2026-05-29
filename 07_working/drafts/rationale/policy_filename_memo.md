# policy_filename_memo | path-sensitive filename policy memo for shadowMAS source surfaces
# related: [check_naming_hook, check_lang_hook, session_gate_hook, source_tree_policy]
# phase: working_draft

# Filename Policy Memo

> Status: working draft, non-canonical, public-safe, not grant-specific.
> Local hooks under `~/.claude/hooks/` are runtime tooling and must implement policy, not create policy.
> This memo lives in `07_working/drafts/rationale/` as a working policy proposal.
> It is not canonical truth.
> Local hooks do not authorize truth, memory, approval, or repository policy by themselves.
> Machine-facing zones remain strict.
> Human and research draft zones allow readable semantic names.
> Generated binary exports are not source.

## Purpose

Define a path-sensitive filename convention for the shadowMAS public repository, and clarify the operational boundary between filename policy (this memo, repo-side) and filename enforcement (local Claude Code hooks, runtime-side). The hooks implement policy; they do not establish it.

## Authority boundary statement

The local Claude Code hooks at `~/.claude/hooks/check_naming.sh`, `~/.claude/hooks/check_lang.sh`, and `~/.claude/hooks/session_gate.sh` are T5 runtime tooling under the project's own T0–T5 layering (see `01_truth/SHADOWMAS-GOVERNANCE-MATRIX.v0.en.md`). They are not under `01_truth/`, not listed in `03_memory/registry/SHADOWMAS-FILE-STATUS-REGISTRY.v0.yaml`, and not part of any approved governance surface. This memo provides a working-draft written policy proposal that the local hooks currently implement for practical consistency. Promotion to T3 approved shared memory requires a separate human decision.

## Principles

1. **`filename_is_metadata`** — A filename is an ambient metadata header for the file's identity. Filenames should encode this metadata; they should not be arbitrary scratch tokens.
2. **`filename_is_authority_surface`** — Path + filename together declare authority. A filename should not promote itself past the path's authority layer.
3. **`filename_is_low_token_semantic_index`** — Filenames are scanned by humans, by `grep`, and by language models. Compressed tokens cost more cognitive and token effort to parse than full word boundaries.
4. **`path_carries_authority_layer`** — Path prefixes (`00_`, `01_`, ..., `07_`) already encode authority and audience. Filename conventions compose with the path; they should not duplicate or override it.
5. **`machine_surfaces_need_stable_identifiers`** — For Python modules, JSON fixtures, packet schemas, and registry YAML, stable predictable identifiers serve parsers and reproducibility.
6. **`human_research_drafts_need_readable_semantic_names`** — Descriptive multi-word identifiers reduce comprehension time relative to abbreviated identifiers; the same logic applies to filenames in human-read zones.
7. **`version_suffixes_must_be_semantic`** — `v2_1` (representing v2.1) preserves major/minor distinction; `v21` collapses it. Semantic version syntax conveys compatibility intent.
8. **`generated_binary_exports_are_not_source`** — PDFs, DOCX, PPTX, and similar are derived outputs; they live in gitignored `exports/` directories and never enter the source tree.
9. **`hook_must_enforce_policy_not_create_policy`** — A runtime hook is T5 tooling. It implements a written policy that lives at T2 / T3 / working-draft. The hook does not itself authorize what the policy is.
10. **`language_hooks_must_respect_declared_translation_zones`** — A global English-only block conflicts with `01_truth/SHADOWMAS-TRANSLATION-POLICY.v0.en.md`, which permits zh-TW companion docs for high-value human navigation. Language hooks must exempt declared bilingual zones (currently `06_human_docs/zh-TW/`) and continue enforcing English-first discipline elsewhere.
11. **`session_gates_must_reference_existing_entry_surfaces`** — Session-start reminders that point to non-existent files train operators to ignore the gate. The reminder must reference real entry surfaces: `00_entry/SHADOWMAS-LAYERING-QUICKREF.v0.en.md` and the intake pack defined in `01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md`.

## Path policy table

### `00_entry/` — structured_semantic
- Allowed examples: `SHADOWMAS-LAYERING-QUICKREF.v0.en.md`.
- Disallowed examples: `quick-ref.md`, `entry_v1.md`.
- Rationale: canonical entry surface; UPPERCASE-WITH-HYPHENS-AND-DOTS preserves consistency with `01_truth/`.
- Hook enforcement: enforce. Hook accepts the structured_semantic pattern explicitly.

### `01_truth/` — structured_semantic
- Allowed examples: `SHADOWMAS-CURRENT-TRUTH.v0.en.md`, `SHADOWMAS-GOVERNANCE-MATRIX.v0.en.md`.
- Disallowed examples: `current_truth_v1.md`.
- Rationale: canonical truth; established UPPERCASE convention.
- Hook enforcement: enforce.

### `02_packets/` — strict_machine
- Allowed examples: `task_packet.v0.yaml`, `memory_packet.v0.yaml`, `review_packet.v0.yaml`, `PACKET-FIELD-DICTIONARY.v0.en.md`.
- Disallowed examples: freeform names.
- Rationale: machine-parsed schema layer.
- Hook enforcement: enforce.

### `03_memory/` — structured_semantic
- Allowed examples: `MEMORY-PLANE-HARNESS.v0.en.md`, `registry/SHADOWMAS-CANDIDATE-REGISTRY.v0.yaml`.
- Disallowed examples: `candidates.yaml`.
- Rationale: mixed machine + governance role.
- Hook enforcement: enforce.

### `04_runtime/` — structured_semantic
- Allowed examples: `LOCAL-MODEL-BASELINE.v0.en.md`, `SHADOWMAS-RUNTIME-LOADING-MAP.v0.en.md`.
- Disallowed examples: `runtime_notes.md`.
- Rationale: same as `01_truth/`.
- Hook enforcement: enforce.

### `05_scripts/` — strict_machine_with_subpath_context
- Allowed examples: `validate/shadowmas_validate.py`, `workspace/shadowmas_workspace.py`, `validate/README.md`, `workspace/README.md`.
- Disallowed examples: spaces; TitleCase script names.
- Rationale: subpath (`validate/`, `workspace/`) carries the module role, so two-segment script names (`shadowmas_validate.py`, `shadowmas_workspace.py`) are acceptable here. README.md uses the universal uppercase exemption.
- Hook enforcement: enforce. Hook accepts 2-or-3-segment lowercase Python names under `05_scripts/**` plus README.

### `tools/` — strict_machine
- Allowed examples: `shadowmas_minimal_validator.py`.
- Disallowed examples: `Tool With Spaces.py`, 1-letter or 2-letter abbreviated module names.
- Rationale: Python module-naming domain.
- Hook enforcement: enforce strict 3-segment.

### `tests/` — strict_machine_with_python_idiom_exceptions
- Allowed examples: `test_shadowmas_minimal_validator.py`, `__init__.py`.
- Disallowed examples: `TestSuite.py`, `checks.py`.
- Rationale: pytest/unittest discovery requires the `test_` prefix; `__init__.py` is the standard Python package init idiom.
- Hook enforcement: enforce. Hook accepts `test_*.py` (any subsegment count), `__init__.py`, plus 3-segment fallback.

### `examples/` — strict_machine_fixture
- Allowed examples: `demo_signal_governance.json`, `demo_signal_governance_violation.json`, `packets/task_packet.valid.v0.yaml`, `README.md`.
- Disallowed examples: `Example One.json`, freeform names.
- Rationale: machine-readable fixtures; subpath `packets/` mirrors the `02_packets/` shape; the 4-segment `_violation` form pairs with the 3-segment positive fixture for L1 testing.
- Hook enforcement: enforce. Hook accepts the existing fixture filenames explicitly.

### `06_human_docs/` — structured_semantic
- Allowed examples: `SHADOWMAS-OPERATOR-GUIDE.v0.en.md`, `SHADOWMAS-SINGLE-SOURCE.v0.zh-TW.md`, `SHADOWMAS-OPERATOR-GUIDE.v0.zh-TW.md`.
- Disallowed examples: lowercase scratch names.
- Note: zh-TW companion docs are valid human-doc surfaces when explicitly under `06_human_docs/zh-TW/`. The language hook must exempt that path; English-first remains the default elsewhere.
- Hook enforcement: enforce structured_semantic; language hook exempts `06_human_docs/zh-TW/` for CJK content.

### `07_working/` — structured_semantic_or_flexible_research
- Allowed examples at root: `DRAFT-ENTRY-RULE.v0.en.md`.
- Disallowed examples: scratch names.
- Rationale: working-area intake rules can use either legacy UPPERCASE-WITH-HYPHENS-AND-DOTS or new lowercase snake_case.
- Hook enforcement: accept both shapes at the root of `07_working/`.

### `07_working/drafts/**` — flexible_research_with_legacy_structured_semantic
- Allowed examples:
  - lowercase snake_case descriptive names (e.g., `active_design_ledger.yaml`, `policy_filename_memo.md`)
  - UPPERCASE-WITH-HYPHENS legacy working docs (e.g., `CONTRACT-VERSIONING-VALIDATOR-CI-PREP.v0.en.md`, `AGENT-JOIN-CONTRACT.v0.en.md`)
  - working markers (dotted-mixed shapes), abstract examples:
    - `<base>.PROPOSAL.v0.yaml`
    - `<base>.DRAFT.v0.md`
    - `<base>.template.PROPOSAL.yaml`
- Disallowed examples:
  - lowercase generic standalone scratch names: `scratch.md`, `tmp.md`, `temp.md`, `notes.md`, `final.md`
  - spaces or TitleCase: `Final Draft.md`, `MyProposal.md`
- Rationale: research drafts and runtime-adapter working artifacts span legacy and new conventions; the working zone needs to admit both without inviting scratch-file pollution.
- Hook enforcement: apply flexible_research recursively to all of `07_working/drafts/**`, accept legacy UPPERCASE shapes, accept `.PROPOSAL` / `.DRAFT` / `.CLAUDE-CODE` / `.template` markers, reject lowercase generic scratch names.

### `07_working/private/` — ignored_private
- Allowed examples: any lowercase snake_case name.
- Disallowed examples: filenames that would shadow tracked files.
- Rationale: gitignored; not source-tracked.
- Hook enforcement: exempt (full path-prefix exemption).

### Root `README.md`, `LICENSE` — standard project exemptions
- Allowed examples: `README.md`, `LICENSE`.
- Rationale: standard convention; uppercase exemption already applies.
- Hook enforcement: existing universal uppercase exemption covers these.

## Forbidden generic scratch tokens (lowercase only)

In `flexible_research` paths, the hook rejects lowercase filenames whose name part contains any segment from: `scratch`, `tmp`, `temp`, `notes`, `final`. The token `draft` is NOT in the lowercase blocklist because the established working-adapter bundle includes legitimate `.DRAFT` and `.draft` markers; the hook discriminates by case (the uppercase `.DRAFT` marker stays allowed under existing working bundles, while a lowercase standalone `draft.md` is still rejected by the 2–6 segment minimum and lowercase blocklist).

## Out of scope

- No mass rename of existing grandfathered files. The hook is PreToolUse only; existing files coexist with the new rules.
- No canonical truth promotion. This memo remains non-canonical working draft.
- No registry changes.
- No private-branch or outreach content on public main.
- No binary exports tracked in Git. Generated PDFs / DOCX / PPTX are gitignored.

## Companion hook responsibilities

- `~/.claude/hooks/check_naming.sh` — implements the path policy table above.
- `~/.claude/hooks/check_header.sh` — enforces 3-line header on `.md` / `.yaml` / `.yml` writes; not modified by this memo.
- `~/.claude/hooks/check_lang.sh` — implements principle 10: English-first in machine-facing zones, exempt `06_human_docs/zh-TW/`.
- `~/.claude/hooks/session_gate.sh` — implements principle 11: reminder references real entry files.

## Promotion path

This memo is non-canonical working draft. Promotion to T3 approved shared memory requires a separate human governance decision. Until then, the local hooks are anchored to this memo by reference; this memo is anchored to the project's own authority-boundary construct by the "Authority boundary statement" section above.
