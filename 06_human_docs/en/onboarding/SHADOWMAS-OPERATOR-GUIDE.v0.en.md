# SHADOWMAS-OPERATOR-GUIDE.v0.en.md

## Purpose
This is the shortest human operator guide for shadowMAS.

Its job is not to explain the whole worldview.
Its job is to help a new operator quickly tell:
- what is canonical truth
- what is tool/runtime state
- what is working-only material
- what to read first
- what not to treat as source truth

## One-Sentence Positioning
shadowMAS is a human-AI governance system.

Its goal is not to flatten everything into one giant prompt.
Its goal is to keep truth, memory, review, runtime, and write-back boundaries clear,
so humans and agents can take over work with minimal reading.

## Read These First
Start here for human takeover:

1. this operator guide
2. `01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md`
3. the exact current intake-pack section in `01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md` when you need the formal 4-file zero-memory entry set
4. `00_entry/SHADOWMAS-LAYERING-QUICKREF.v0.en.md` when layer/source mapping is needed
5. `04_runtime/SHADOWMAS-RUNTIME-LOADING-MAP.v0.en.md` when runtime-side loading rules matter

## Folder Reading Rule
You do not need a full folder-by-folder explanation to take over safely.

Use:
- `01_truth/` for formal canonical truth
- `06_human_docs/` for human onboarding and explanation
- `07_working/` for working-only materials that support work but are not canonical truth

## What Counts As Tool Runtime State
Some files belong to the tool runtime, not to canonical shadowMAS truth.

Examples:
- auth state
- cache
- history
- sessions
- logs
- sqlite state files
- shell snapshots

These may help the tool operate,
but they are not formal source-of-truth artifacts.

## Who May Perform Git Actions
Constitution-level rule:
- remote push may only be triggered by a human
- final merge may only be triggered by a human
- promotion to a public branch may only be triggered by a human

An agent may at most perform:
- local branch work
- local commit
- local diff
- review packet preparation

Even after long automation chains,
a human must still review and release the result.

## What Machine-First Actually Means
Machine-first does not mean reducing tokens at any cost.

The real rule is:
according to data shape and error cost,
preserve quality and parseability first,
then compress when safe.

That means:
- structure when structure is needed
- keep enums explicit when ambiguity is risky
- do not rely on guessing for high-risk fields
- do not force every artifact into the smallest possible form

## What Working-Only Means
Working-only material exists for:
- current workflow
- temporary organization
- human review staging
- pre-promotion evaluation

It may be read,
and it may support decisions,
but it must not be treated directly as:
- canonical truth
- approved shared memory

Examples:
- lessons queue
- incoming handoffs
- merged audit drafts
- pre-promotion notes

## Minimal Takeover Rule
Do not begin by reading the whole repo.

Start from the smallest entry surface,
then determine:
- which layer you are touching
- where the canonical truth lives
- what is only working or runtime state
- whether runtime-side loading rules are needed from `04_runtime/SHADOWMAS-RUNTIME-LOADING-MAP.v0.en.md`

This is the shadowMAS goal:
small, direct, and strong enough for correct takeover.
