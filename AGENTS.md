# AGENTS | public repo instructions for AI coding agents working on shadowMAS
# related: [README, SHADOWMAS-LAYERING-QUICKREF, SHADOWMAS-CURRENT-TRUTH, policy_filename_memo]
# phase: public_working_guidance

# AGENTS.md

## Purpose

This file gives public-safe instructions for AI coding agents and human contributors working in the shadowMAS repository. It does not define canonical truth and does not override files under `01_truth/`, packet schemas, registries, or human review. If a task description and a rule in this file conflict, ask for human clarification before acting.

## Reading order before non-trivial work

1. `README.md` for project identity and first-run commands.
2. `00_entry/SHADOWMAS-LAYERING-QUICKREF.v0.en.md` for the layer model.
3. `01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md` for the current minimum truth.
4. Other files under `01_truth/` only if the task touches authority-boundary policy, prompt layering, change impact, or translation policy.

Do not perform blind full-repo traversal. Load files on demand by task shape.

## Authority boundaries

- `01_truth/` contains canonical project truth surfaces. Do not edit unless the task explicitly allows truth-surface changes.
- `02_packets/` contains packet schemas and packet documentation. Do not edit packet schemas unless explicitly allowed.
- `03_memory/` contains registry and memory-plane surfaces. Do not edit registries unless explicitly allowed.
- `04_runtime/` contains runtime-facing design surfaces. Do not change runtime contracts unless explicitly allowed.
- `00_entry/`, `06_human_docs/`: established entry and human-facing surfaces. Treat as semi-canonical.
- `05_scripts/`, `tools/`, `tests/`, `examples/`: machine-facing surfaces. Keep names and structure stable.
- `07_working/` contains drafts, rationale, proposals, and working material. Inclusion in `07_working/` does not make a file canonical truth. Promotion to a higher layer requires explicit human authority-boundary review.

## Public/private boundary

- Do not add private proposal, outreach, partnership, or correspondence material to public `main`.
- Do not add secrets, credentials, access tokens, local machine paths, or private account data.
- Do not track generated PDF, DOCX, or PPTX exports. These belong in gitignored `exports/` directories or outside the repository.
- Keep source formats diffable: Markdown, YAML, JSON, Python, or other plain-text formats unless the task explicitly requires otherwise.
- If a task may expose private material, stop and ask for human review before continuing.

## Editing discipline

- Keep changes atomic and path-scoped. One task should usually touch one logical surface.
- Before changing a file, identify its path layer (above) and authority level.
- Do not mix unrelated changes in one task.
- Prefer minimal diffs over broad rewrites.
- Preserve existing public-safe wording unless a task explicitly asks for a rewrite.
- Do not rename files without checking references and the path policy below.
- For markdown and YAML files, preserve any existing 3-line header convention (line 1 name/responsibility, line 2 related list, line 3 phase) unless the task is explicitly to revise those headers.

## Naming and generated files

- Follow the path-sensitive filename policy at `07_working/drafts/rationale/policy_filename_memo.md` when it is present.
- Keep machine-facing surfaces (tools, tests, examples, packets, registries) predictable.
- Keep human-facing drafts under `07_working/drafts/` readable: prefer lowercase snake_case multi-word names with semantic version suffixes such as `v2_1`. Avoid compressed tokens like `v21` representing `v2.1`.
- Do not track generated `exports/`, `.pdf`, `.docx`, or `.pptx` files.
- Do not create large binary artifacts in the repo.

## Validation

Run only validation commands relevant to the paths touched.

- `git status --short` to confirm the worktree state.
- `git diff -- <paths>` to inspect the specific diff.
- `python3 -m unittest discover tests` to run the test suite.
- `python3 tools/shadowmas_minimal_validator.py examples/demo_signal_governance.json` to validate the positive fixture.
- `python3 tools/shadowmas_minimal_validator.py examples/demo_signal_governance_violation.json` to validate the negative fixture.

Validation commands should be read-only with respect to the repository.

## Git rules

- Do not run `git add`, `git commit`, or `git push` unless the human explicitly asks.
- If asked to prepare a commit, report the exact paths changed and a suggested commit message; let the human review and execute.
- If a task touches multiple unrelated surfaces, propose splitting into separate commits.
- Do not force-push, rebase published history, or rewrite shared branches.

## Safety and non-claims

- Do not claim shadowMAS proves runtime safety.
- Do not claim empirical human-oversight improvement.
- Do not claim construct validity or predictive validity unless such evidence exists in the repository.
- Do not present runtime signals, dashboards, recommendations, or working drafts as human approval or canonical truth.
- Treat retrieval hits, cache hits, and confidence scores as evidence, not as authority.

## When the task is unclear

- When ambiguity would materially affect scope, safety, or public/private boundaries, ask one focused clarifying question before changing files.
- Prefer a read-only audit and a written summary over speculative edits.
- If you discover an authority-boundary risk, surface it in the response rather than working around it.
- If a path or rule appears in this file but contradicts a more specific rule in a task description, prefer the task description and report the conflict.

## Reporting expectations

When a task is complete, the report should usually include:

- the exact list of paths that were modified, created, or deleted;
- the validation commands that were run and their outcomes;
- any boundary that the agent declined to cross and the reason;
- a one-sentence statement of what is left for human review;
- if appropriate, a suggested commit message for the human to use.

Avoid trailing summaries of what every paragraph of the diff says. The diff itself is the artifact; the report should add only the context the diff cannot show on its own.

## Style and tone

- Write in plain English. Define jargon inline when first used.
- Prefer short sections with clear headers over long undifferentiated prose.
- Keep file headers, comments, and commit messages factual and minimal.
- Do not embed marketing language in source files.
- Avoid emojis in tracked source unless the user explicitly asks.

## Cross-references

- Treat path references inside files as load-bearing. If you rename a file, search for references to its old path and either update them or stop and ask.
- Treat the contents of `01_truth/SHADOWMAS-CHANGE-IMPACT-MAP.v0.en.md` as the authoritative guide to which surfaces must be reviewed when a particular kind of change is made.

## Out of scope for this file

This file does not:

- define canonical truth;
- replace `01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md` or any other formal surface;
- describe local hook implementations or contributor machine configuration;
- specify branch strategy beyond the public/private boundary stated above;
- enumerate every validation command; the per-task command set depends on the paths touched.

For deeper authority-boundary and packet semantics, follow the reading order at the top of this file and the change-impact map referenced above.
