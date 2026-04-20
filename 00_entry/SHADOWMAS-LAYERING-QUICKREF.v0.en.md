# SHADOWMAS-LAYERING-QUICKREF.v0.en.md

## Purpose
This file is the shortest layer-to-source quick reference for shadowMAS v0.

It exists so that:
- a human or agent can enter the system fast
- layer ownership stays readable
- source-of-truth boundaries stay explicit
- runtime loading does not collapse into one giant prompt

This is a quick reference, not a replacement for canonical truth files.

## Core Entry Rule
Do not start with blind full-repo traversal.

Start from the smallest readable entry surface,
then load more files only when the task shape requires them.

## Layer Model At A Glance

### Layer 1: Shared Core
Meaning:
Cross-project reusable behavior floor.

What belongs here:
- discuss before acting
- minimal necessary change
- no blind full-repo traversal
- inspectability
- reversibility
- token discipline
- machine-first discipline when relevant

Current status:
- concept is formalized
- dedicated standalone source file is not yet finalized
- currently represented indirectly through current truth and related governance files

Current source surfaces:
- `01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md`
- `README.md`

### Layer 2: shadowMAS Governance
Meaning:
Global governance for truth, memory, promotion, invalidation, review, routing, and write-back boundaries.

Current source surfaces:
- `01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md`
- `01_truth/SHADOWMAS-PROMPT-LAYERING-CONTRACT.v0.en.md`
- `01_truth/SHADOWMAS-GOVERNANCE-MATRIX.v0.en.md`
- `01_truth/SHADOWMAS-CHANGE-IMPACT-MAP.v0.en.md`
- `01_truth/SHADOWMAS-TRANSLATION-POLICY.v0.en.md`

### Layer 3: Project Execution
Meaning:
Repo-local truth for one specific project.

Rule:
shadowMAS may read and interact with project-execution truth,
but project-domain truth remains local to that project repo.

Current source surface inside shadowMAS:
- no project repo is canonicalized here
- only governance-facing references, handoffs, or write-back boundaries may appear

### Layer 4: Runtime Adapter Prompt
Meaning:
Tool/runtime-specific execution shaping.

Examples:
- Codex
- Claude Code
- Cursor
- local Ollama task runner

Current source surfaces:
- `04_runtime/LOCAL-MODEL-BASELINE.v0.en.md`
- future runtime-specific adapter files
- `04_runtime/SHADOWMAS-RUNTIME-LOADING-MAP.v0.en.md`

### Layer 5: Host Native / Opaque Prompt
Meaning:
Provider/host-native prompt influence outside direct shadowMAS control.

Rule:
acknowledge it exists,
but do not treat it as maintainable source truth.

## Current Minimum Intake Pack
Use the exact current zero-memory intake pack defined in
`01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md`.

What this pack is for:
- first calibration
- read-only audit
- initial role separation
- basic navigation

What this pack is not for:
- autonomous patching
- blind moving of canon files
- ambiguous ownership decisions

## Source Category Quick Reference

### Canonical formal truth
Main homes:
- `01_truth/`
- machine-facing parts of `02_packets/`
- `03_memory/registry/`
- formal runtime baseline files in `04_runtime/`

### Human-facing explanation
Main homes:
- `06_human_docs/zh-TW/`
- `06_human_docs/en/`

### Working-only surfaces
Main home:
- `07_working/`

Rule:
working-only artifacts may support work,
but must not be mistaken for canonical truth.

## New Entry Design Rule
A new human or agent should not need to read the whole repo first.

A small set of direct, parseable, low-ambiguity entry files should be enough to tell them:
- what this system is
- which layer they are touching
- what to read next
- what not to treat as truth

## Non-Goals Of This File
This file does not:
- define full governance truth
- explain every runtime folder
- replace operator guidance
- define packet schemas
- define lessons handling

Use companion files for those.
