# SHADOWMAS-TRANSLATION-POLICY.v0.en.md

## Purpose
This file defines the bilingual and translation policy for shadowMAS.

Its goal is to keep:
- English canonical execution truth stable
- Chinese human-facing explanation useful
- bilingual scope controlled
- maintenance cost bounded
- agent readability and human readability both preserved

## Core Direction
- English is the canonical language for agent-facing formal truth.
- zh-TW is the primary companion language for human-facing navigation, rationale, onboarding, and design explanation.
- Not every file should have a bilingual mirror.
- Only high-value human-critical files should normally receive Chinese companion treatment.

## Why this exists
If every file is mirrored in two languages:
- maintenance explodes
- drift increases
- humans get overwhelmed
- agents may not know which copy is canonical
- translation quality becomes a burden instead of a help

Therefore:
- canonical truth stays minimal and English-first
- human comprehension stays strong through selective zh-TW companion documents

## Language Roles

### English
Use English for:
- formal truth files
- packet definitions
- registry definitions
- agent-facing rule files
- machine-stable schemas
- CLI/runtime/governance technical contracts

### zh-TW
Use zh-TW for:
- single-source human entry
- onboarding
- design rationale
- decision explanation
- reference notes
- diagrams and interpretation guides
- technical intention and tradeoff explanation for humans

## Canonical Rule
If a file exists in both English and zh-TW:
- the English formal file is canonical
- the zh-TW file is companion, not the source of truth
- the zh-TW file must not silently redefine the English formal truth

## Translation Scope Categories

### Category A: Always bilingual-critical
These files normally require a zh-TW companion or zh-TW explanation path.

Examples:
- current truth summary for humans
- field dictionary summaries
- ERD summaries
- DTO / OpenAPI summaries
- core process documentation
- navigation / onboarding docs
- major governance rationale

### Category B: Selective bilingual
These files may receive zh-TW support when the human value is high.

Examples:
- governance matrix summary
- memory-plane explanation
- local model baseline explanation
- important change-impact explanation
- important write-back safety explanation

### Category C: English-only by default
These files should usually remain English-only unless a strong human need appears.

Examples:
- packet YAML schemas
- registry YAML files
- machine-stable shell schemas
- runtime adapter technical contracts
- detailed validator specs
- low-level automation docs
- temporary working technical drafts

## Current shadowMAS v0 policy

### Must exist in English formal form
- `01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md`
- `01_truth/SHADOWMAS-PROMPT-LAYERING-CONTRACT.v0.en.md`
- `01_truth/SHADOWMAS-GOVERNANCE-MATRIX.v0.en.md`
- `01_truth/SHADOWMAS-CHANGE-IMPACT-MAP.v0.en.md`
- `01_truth/SHADOWMAS-TRANSLATION-POLICY.v0.en.md`
- `02_packets/*` machine-facing packet files
- `03_memory/*` machine-facing harness/registry files
- `04_runtime/*` formal runtime baseline files

### Must exist in zh-TW human-facing form
- `06_human_docs/zh-TW/SHADOWMAS-SINGLE-SOURCE.v0.zh-TW.md`

### Likely to need zh-TW companion later
- governance overview
- packet explanation
- memory-plane rationale
- local model rationale
- project decoupling explanation
- compression rationale
- design references / why-not choices

## Sync Rule

### When an English formal file changes
Ask:
1. Is this change visible to human operators/designers?
2. Is this change important for onboarding or future understanding?
3. Is this change part of high-value bilingual scope?

If yes:
- update the relevant zh-TW human-facing document
- at minimum, update the single-source navigation brain if the change is foundational

If no:
- no zh-TW update is required

### When a zh-TW file changes
Ask:
1. Did the actual governance/truth change?
2. Or is this only explanation/clarification?

If only explanation changed:
- do not update formal English truth files

If actual truth changed:
- update English canonical truth first
- then update the zh-TW companion

## Single-Source Rule
The zh-TW single-source file is the primary human navigation brain.

It should:
- summarize the current design
- explain why key decisions were made
- point humans to deeper docs
- record design intention and tradeoffs

It should not:
- silently create new formal truth
- replace English formal files
- become a giant unsynchronized shadow copy of the whole repo

## Translation Style Rule
zh-TW companion docs should:
- optimize readability
- preserve technical precision
- allow English technical terms where they help clarity
- explain design intention, not just translate literally

The goal is:
- comprehension first
- traceability second
- low drift third

Literal full-mirror translation is not the goal.

## Naming Rule
English formal files should keep consistent machine-friendly names.

zh-TW companion docs may:
- use zh-TW content
- still keep stable filenames
- remain grouped under `06_human_docs/zh-TW/`

Do not create mixed canonical naming chaos across both languages.

## Anti-Explosion Rule
Do not mirror every English file into zh-TW by default.

New zh-TW files require justification such as:
- onboarding value
- governance explanation value
- high confusion risk without human explanation
- major decision rationale value

## Human-Facing Depth Rule
Human-facing zh-TW documents may be longer and richer than English formal files.

They may include:
- why this was chosen
- what alternatives were rejected
- what references influenced the decision
- historical reasoning
- operational interpretation
- learning notes for future maintainers

This is allowed because zh-TW human docs are not the canonical execution truth layer.

## Agent Rule
Agents should:
- default to English formal files for execution truth
- use zh-TW docs for human-context support only when relevant
- never assume a zh-TW companion overrides English canonical truth

## Still Not Final
The following may refine later:
- exact file list for bilingual-critical scope
- automatic translation sync triggers
- milestone-based zh-TW summary generation rules
- future external/public documentation language strategy
