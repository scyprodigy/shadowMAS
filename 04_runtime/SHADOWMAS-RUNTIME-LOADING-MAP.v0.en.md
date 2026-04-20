# SHADOWMAS-RUNTIME-LOADING-MAP.v0.en.md

## Purpose
This file defines the minimum loading guidance for shadowMAS runtimes.

It exists to prevent:
- blind full-repo traversal
- loading too much too early
- runtime/source confusion
- treating tool state as canonical truth
- giant-prompt collapse

## Core Runtime Rule
Load by task shape.
Do not load everything by default.

A runtime should read the minimum useful source set,
then request more files only when the task actually requires them.

## What This File Covers
This file covers:
- minimum read sets
- task-shape-based loading
- runtime-side loading boundaries

This file does not replace:
- governance truth
- project execution truth
- operator onboarding guide
- tool-native config docs

Operator-facing explanation of canonical truth, working-only material, and tool/runtime state belongs in the operator guide.

## Minimum Read Sets By Task Shape

### A. Zero-memory calibration
Read:
- the exact current zero-memory intake pack defined in `01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md`

Use for:
- first contact
- role calibration
- repo understanding
- read-only orientation

### B. Governance review
Read zero-memory calibration pack, plus:
- `01_truth/SHADOWMAS-GOVERNANCE-MATRIX.v0.en.md`
- `01_truth/SHADOWMAS-TRANSLATION-POLICY.v0.en.md`
- any directly relevant truth file touched by the task

Use for:
- governance changes
- promotion/invalidation discussion
- source-boundary review

### C. Runtime / tooling discussion
Read zero-memory calibration pack, plus:
- `04_runtime/LOCAL-MODEL-BASELINE.v0.en.md`
- this file
- operator guide when human operation is involved

Use for:
- runtime adapter work
- tool placement
- loading boundary discussion
- local model flow discussion

### D. Packet / machine-contract work
Read zero-memory calibration pack, plus:
- `02_packets/PACKET-FIELD-DICTIONARY.v0.en.md`
- relevant packet schema files under `02_packets/`
- relevant registry files if packet touches memory or status

Use for:
- packet design
- machine-first artifact design
- review surface design

### E. Working-only / lessons / handoff work
Read zero-memory calibration pack, plus:
- relevant file(s) under `07_working/`
- operator guide if human review flow matters
- relevant canonical truth only when promotion or conflict appears

Use for:
- handoffs
- temporary merged notes
- lessons intake
- pre-promotion staging

## Runtime-Specific Minimum Guidance

### Codex
Default read order:
1. zero-memory calibration pack
2. this runtime loading map when runtime shaping matters
3. repo-local project execution entry files only if the task crosses into a project repo
4. additional files strictly on demand

Do not assume tool-private runtime state, for example under `~/.codex/`, is canonical truth.

### Claude Code
Default read order:
1. zero-memory calibration pack
2. this runtime loading map when runtime shaping matters
3. runtime-specific adapter file when available
4. additional files on demand

### Cursor
Default read order:
1. zero-memory calibration pack
2. local project execution entry files if the task is repo-local
3. runtime-specific adapter file when available
4. additional files on demand

### Local Ollama task runner
Default read order:
1. smallest relevant calibration subset
2. machine-first source files only when needed
3. compact task packet / review packet surfaces when available

Rule:
avoid large prose loads by default.

## Escalation Rule For More Reading
Ask for more files when:
- ownership is ambiguous
- a task touches canonical truth
- a task touches promotion/invalidation logic
- a task touches runtime boundaries
- a task touches write-back or mergeback safety
- current files are insufficient to determine scope safely

## Full-Repo Traversal Exception Rule
Full-repo traversal is not the default.

It may be justified only when:
- a human explicitly asks for repo-wide audit
- duplication detection requires broad inspection
- contamination review requires repo-wide read coverage
- structure drift cannot be resolved from the normal entry surfaces

Even then:
- traversal should still be bounded by purpose
- the runtime should report why broad traversal is needed

## Loading Philosophy
The goal is not to read less at all costs.
The goal is to read the smallest set that preserves correctness.

Quality and parseability come before token savings.
Compression is allowed only after truth identity remains safe.

## Companion Files
Use together with:
- `00_entry/SHADOWMAS-LAYERING-QUICKREF.v0.en.md`
- operator guide in `06_human_docs/` for human takeover and source-boundary interpretation
- runtime-specific adapter files when they are created
