# EXTERNAL-RESEARCH-DRAFT-ENTRY-RULE.v0.en.md

> Status: working draft / drafts intake rule
> Nature: human-facing convergence rule, **not** canonical truth, **not** packet schema, **not** runtime contract.
> Purpose: give later sessions a minimum but executable rule for deciding when an external-research artifact is worth writing into `07_working/drafts/`, and when it should stay out.

---

## 1. One-sentence rule

An external-research artifact should enter `drafts/` only when it has moved beyond a temporary idea, scattered links, or one-off chat notes, and is **likely to be cited, compared, converged, or reused as design-discussion input in later sessions**.

Conversely, the following should **not** go into `drafts/` first:
- a single link
- an unstructured idea
- a lesson still waiting for human sink selection
- or a conclusion that is already ready to update formal truth / schema / contract directly

---

## 2. When an artifact should enter `drafts/`

A `drafts` artifact is recommended only when most of the following are true.

### A. The topic has converged into one theme
- The research topic is explicit and singular.
- It is not a giant survey.
- It is not mixing multiple decision questions.
- A later session can answer, in one sentence, what the draft is about.

### B. It already contains reusable conclusions
- It is no longer only source collection.
- It already contains:
  - problem restatement
  - source summary
  - actionable principles or candidate criteria
  - explicitly unresolved areas
- Even if later rejected, it is still useful as a comparison baseline.

### C. It is explicitly not formal truth
The file must directly state that it is something like:
- working draft
- external research memo
- rationale draft

It must also explicitly state that it is:
- **not** canonical truth
- **not** packet schema
- **not** product spec
- **not** runtime contract

This prevents later sessions from treating `drafts/` as if it were formal law.

### D. It is likely to be cited again later
One or more of the following is enough:
- the same topic will likely be revisited more than once
- the conclusions will be used to compare alternative designs
- the material helps human design understanding but is not yet ready for formalization
- the original sources are scattered enough that not organizing them now would create expensive rework later

### E. It has a companion references file
If the artifact depends on external papers, heuristics, case studies, or research sources, it should keep a companion references file.

That references file should preserve at least:
- citation
- DOI / URL
- claim supported
- evidence strength
- why it matters here

Rule of thumb:
**the memo carries human-readable convergence; the references file preserves external-link detail.**

---

## 3. When an artifact should not enter `drafts/`

### A. It is really a lesson / failure / repeated pitfall
That should go to a queue first, not to `drafts/`.

Typical queue-shaped traits:
- repeated_same_failure
- rework_or_wrong_edit_risk
- needs_patch_downshift
- still waiting for human sink selection (execution patch / project patch / governance candidate / no action)

This kind of artifact is a lesson awaiting routing, not a converged external-research draft.

### B. It is still one-off session collection
- no problem restatement yet
- no reusable conclusion yet
- only URLs, quotes, copied fragments, or partial notes
- no articulation of why the sources matter to shadowMAS

In that state it should stay in session context or a temporary working area, not in `drafts/`.

### C. It is already ready to update formal files directly
If the conclusion has already converged to the point where it should directly update:
- `01_truth/`
- `02_packets/`
- runtime / adapter contract files

then a separate `drafts` layer is unnecessary unless the research itself still has independent human-facing rationale value.

### D. It is only a large storage dump
A references file is not a literature warehouse.
If it is only “store as many papers as possible” without grouping them into reusable principle clusters or claim clusters, it should not enter `drafts/`.

---

## 4. Minimum retention unit for `drafts/`

A retained external-research topic should normally contain two things.

### 1) Human-readable memo
Suggested minimum contents:
- problem restatement
- scope boundary
- source summary
- distilled principles / findings
- anti-patterns or misuse risks
- unresolved parts that must not be promoted directly

### 2) Companion references file
Suggested minimum contents:
- principle cluster / claim cluster
- reference_id
- source citation
- DOI / URL
- evidence strength
- why it matters here

If the second item is missing, external-link detail is likely to disappear in later discussion rounds.

---

## 5. Minimum decision flow

Later sessions can use this order directly.

### Step 1
Is this an **external research artifact** or a **lesson queue item**?
- If it is a routed lesson / error / rework risk, keep it in queue first.
- If it is a topic-shaped research artifact, continue.

### Step 2
Has it already become a **single-theme reusable memo**?
- If no, do not place it in `drafts/`.
- If yes, continue.

### Step 3
Does it explicitly mark itself as **not canonical truth**, **not schema**, and **not product/runtime law**?
- If no, add boundary/status language first.
- If yes, continue.

### Step 4
Does it have companion references / source support that preserves external-link detail?
- If no, add the supporting references material first.
- If yes, it is suitable for `drafts/`.

---

## 6. Naming and placement suggestions

### Suitable names under `07_working/drafts/`
- `TOPIC-RESEARCH-MEMO.v0.en.md`
- `TOPIC-RATIONALE-DRAFT.v0.en.md`
- `TOPIC-REFERENCES.v0.yaml`

### Names to avoid
- `notes.md`
- `tmp.md`
- `misc-research.md`
- `links.yaml`

Rule:
the filename should expose the artifact’s role directly, rather than forcing later sessions to infer it.

---

## 7. Boundary against formal truth

External research in `drafts/` may serve as:
- design-discussion input
- rationale candidate material
- human-facing explanation basis
- pre-decision memo input

External research in `drafts/` must not be treated as:
- canonical truth
- packet contract
- registry law
- runtime law
- auto-promotion basis

Any move from `drafts/` into a formal layer requires a separate convergence and review step.
It must not be copied upward automatically.

---

## 8. Concrete reading of the current three artifacts

### `FAST-REVIEW-FORM-RESEARCH-MEMO.v0.zh-TW.md`
Should be kept in `drafts/`.

Why:
- clear single theme
- reusable conclusions already present
- explicitly marked as non-canonical research input
- suitable for later design discussion reuse

### `FAST-REVIEW-FORM-REFERENCES.v0.yaml`
Should be retained together with the memo above as its companion file.

Why:
- preserves DOI / URL / claim / evidence strength / relevance
- prevents later sessions from retaining only slogans without source detail

### `SHADOWMAS-LESSONS-QUEUE.v0.yaml`
Does not belong to the `drafts/` retention rule.

Why:
- it is a queue, not a research memo
- its role is working-only intake with later human sink selection
- it belongs to queue / registry logic, not to external-research draft logic

---

## 9. Minimum conclusion

An external-research artifact is worth writing into `07_working/drafts/` only when all of the following are true:

1. the topic is singular
2. reusable convergence already exists, not only raw collection
3. the artifact explicitly marks itself as non-canonical
4. companion references / source support preserve external-link detail
5. later sessions are likely to cite or reuse it again

If the material is only a routed lesson, a pending sink decision, or leftover one-off session residue, it should remain in queue or session context rather than entering `drafts/`.
