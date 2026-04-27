> status: draft / source-evidence
> authority: none
> do not promote without governance review
>
> Draft runtime-adapter evidence only.
> Must not write back into product repos or redefine project-local truth.
> Runtime-adapter intake does not preempt the current version-governance lane.

# SHADOWMAS-RUNTIME-ADAPTER-MERGEBACK.v0

> Mergeback review for Claude `files.zip` bundle.  
> Branch scope: L2 planning + Layer 4 Runtime Adapter design.  
> Target: return this branch back to main HEAD after this mergeback is accepted.

---

## 0. Decision Summary

The Claude bundle is useful and should be preserved as a **runtime adapter draft bundle**, not promoted directly into canonical shadowMAS truth.

Primary decision:

- **Accept as working/draft material** for Claude Code adapter design.
- **Do not canonicalize** MANIFESTO, packet shell, hook config, agent registry, or shared core template yet.
- **Use the bundle to create follow-up draft files** for hot-join agents, project intake, legacy intake normalization, packet compatibility, and runtime adapter contract.
- **No more Claude reply is required** for this branch. Claude has provided enough material for GPT head merge review.

Return condition to main HEAD:

- This file is the branch mergeback artifact.
- After owner review, this branch can return to main HEAD with the merge message in section 12.

---

## 1. Source Bundle Reviewed

Bundle: `files.zip`

Extracted files:

| File | Role in bundle | Merge disposition |
|---|---|---|
| `README.md` | Bundle index and reading order | Keep as source evidence only |
| `MANIFESTO.md` | Positioning / doctrine / philosophy | Keep as rationale candidate; do not canonicalize |
| `SHADOWMAS-CLAUDE-CODE-ADAPTER-PLAN.v0.md` | Main Layer 4 adapter plan | Keep as high-value draft source |
| `adapter-plan.v0.yaml` | Machine-readable adapter summary | Keep as draft proposal; validate later |
| `packet_common_shell.v0.yaml` | Packet common shell proposal | Keep as packet-shell proposal only; do not replace canonical packet rules |
| `shared_core.template.md` | Cross-project behavior template | Keep as template candidate; must be decontaminated before use |
| `agents.template.yaml` | Agent registry / assignment modes | Keep as proposal; dynamic/self-claim deferred |
| `claude-code-settings.template.json` | Claude Code hook settings template | Keep as hook template; not production config |
| `bootstrap-prompt.md` | Paste-ready Claude Code bootstrap prompt | Keep as operational draft |
| `RISKS-AND-UNRESOLVED.md` | Risk register and unresolved decisions | Keep; must be preserved with main plan |

---

## 2. What This Branch Was Supposed To Do

This branch is not the main HEAD session.

This branch's job:

1. Absorb Claude's Layer 4 runtime adapter design output.
2. Decide what can be merged back safely.
3. Prevent Claude output from being promoted directly into shadowMAS canonical truth.
4. Extract the real missing contracts:
   - agent hot-join
   - project hot-intake
   - legacy / non-packet intake normalization
   - packet compatibility layer
   - runtime adapter contract
5. Produce a mergeback package for the main HEAD session.

This branch is now complete enough to return to main HEAD after this artifact is accepted.

---

## 3. Governance Judgment

Claude's bundle is broadly aligned with shadowMAS v0 direction, but it is not canonical.

Reasons:

- It correctly treats Claude Code as a runtime adapter lane, not as final truth.
- It correctly separates GPT head, Claude Code, Cursor, Ollama, hooks, skills, project docs, and shadowMAS docs by authority level.
- It correctly treats hooks as runtime guards rather than truth sources.
- It correctly keeps Week 1 RideDispatch scope narrow.
- It correctly identifies unresolved risks instead of pretending the adapter is complete.

However, it also introduces several claims that require explicit promotion review:

- MANIFESTO positioning language.
- `packet_common_shell.v0.yaml` as “canonical minimal envelope.”
- AGENTS.md / CLAUDE.md symlink strategy.
- `distribute.sh` / `install.sh` implied workflow.
- dynamic / fixed / self_claim role-assignment model.
- A2A embedding route.
- hook event model and specific Claude Code settings.

Therefore:

> Treat the bundle as **T4 execution/planning feed** and **T3 candidate material**, not T2 approved truth.

---

## 4. Merge Decision by File

### 4.1 `README.md`

Decision: **Keep as bundle index only.**

Use:

- Helps human and agent understand bundle layout.
- Good reading order.
- Correctly states proposal status.

Do not:

- Promote into shadowMAS repo root README directly.
- Treat strategic recap as approved positioning.

Recommended landing:

```txt
07_working/drafts/runtime_adapter/claude_bundle/README.md
```

---

### 4.2 `MANIFESTO.md`

Decision: **Keep as rationale candidate; do not canonicalize.**

High-value content:

- “shadowMAS is a governance protocol, not a framework.”
- personal-scale workstation MAS governance positioning.
- calibrated trust / rubber-stamping concern.
- “not another A2A” framing.

Risks:

- Strong philosophical language may overstate current v0 maturity.
- External claims about A2A / AGT / ecosystem standards require fact-checking before public use.
- zh-TW doctrine content conflicts with the current English-canonical policy if treated as canonical.
- “Packet is the smallest unit, also the whole” may be too strong unless legacy/non-packet intake is formalized.

Recommended landing:

```txt
07_working/drafts/rationale/SHADOWMAS-MANIFESTO-DRAFT.v0.md
```

Required before promotion:

- Convert into English canonical positioning if used formally.
- Preserve zh-TW as companion/rationale if human-facing value remains high.
- Verify external claims or remove them.
- Align with Current Truth wording.

---

### 4.3 `SHADOWMAS-CLAUDE-CODE-ADAPTER-PLAN.v0.md`

Decision: **Keep as main Runtime Adapter working draft.**

High-value content:

- Layer mapping table.
- Prompt composition plan.
- Claude Code session bootstrap.
- Skills invocation policy.
- Hooks policy.
- Agent delegation routing.
- Week 1 phase guardrail.
- Explicit statement that the plan does not modify shadowMAS truth or RideDispatch business specs.

Risks:

- Some file paths are proposed, not approved.
- Some hooks imply future scripts that do not exist yet.
- Some adapter rules may be too Claude-specific and must not leak into Cursor/Codex.
- “AGENTS.md as universal entry” is a promising direction but needs host/tool compatibility validation.

Recommended landing:

```txt
07_working/drafts/runtime_adapter/SHADOWMAS-CLAUDE-CODE-ADAPTER-PLAN.v0.md
```

Promotion target later:

```txt
04_runtime/adapters/CLAUDE-CODE-RUNTIME-ADAPTER.v0.en.md
```

Only after:

- path policy is approved,
- hook capability is validated,
- source-of-truth relationship is clarified,
- runtime adapter contract exists.

---

### 4.4 `adapter-plan.v0.yaml`

Decision: **Keep as machine-readable draft; validate later.**

Use:

- Good candidate for adapter registry / adapter manifest.
- Useful for future tooling.

Risks:

- YAML schema is not approved.
- Some fields likely overlap with future runtime adapter contract.
- Could accidentally become a second source of truth.

Recommended landing:

```txt
07_working/drafts/runtime_adapter/adapter-plan.v0.yaml
```

Required before promotion:

- Define schema ownership.
- Define whether this is a generated manifest or hand-maintained truth.
- Add validation rules.

---

### 4.5 `packet_common_shell.v0.yaml`

Decision: **Keep as proposal only; do not replace packet canonical direction.**

High-value content:

- Clear shell fields.
- Extension region concept.
- task / memory / review payload examples.
- Future A2A wrapping fields kept in extension zone.

Risks:

- It calls itself canonical, but canonical status has not been granted.
- `agent_id: null if self-claim` assumes self-claim mode, which is not approved.
- A2A wrapping fields should remain future extension only.
- It does not yet handle legacy/non-packet intake.

Recommended landing:

```txt
07_working/drafts/packet/packet_common_shell.PROPOSAL.v0.yaml
```

Follow-up required:

- Create `PACKET-COMPATIBILITY-LAYER.v0.en.md`.
- Add raw intake / wrapped artifact / native packet distinction.
- Add loss accounting fields for legacy conversion.

---

### 4.6 `shared_core.template.md`

Decision: **Keep as template candidate; do not install directly.**

High-value content:

- Discuss before implementing.
- Undefined is not decided.
- Minimum necessary change.
- No blind full-repo traversal.
- Packet discipline.
- Role awareness.
- Session discipline.
- Hard constraints.

Risks:

- It says “No packet, no delegation,” which is acceptable for inter-agent delegation but too strict if applied to raw intake/import.
- It has operational file path assumptions.
- It includes user-specific behavior choices that should not become global Shared Core automatically.

Recommended landing:

```txt
07_working/drafts/templates/shared_core.template.DRAFT.md
```

Required before promotion:

- Split global shared-core rules from user-local preferences.
- Clarify that raw legacy input may enter via intake adapter even if not packet-native.
- Remove path assumptions unless formally approved.

---

### 4.7 `agents.template.yaml`

Decision: **Keep as proposal; use fixed mode only for v0.**

High-value content:

- Agent capability declaration.
- Provider / host / capability mapping.
- Role assignment modes.
- Explicit note that dynamic/self_claim are disabled in v0.

Risks:

- dynamic scoring requires memory plane and persistent metrics.
- self_claim requires packet transport, optimistic locking, and claim conflict handling.
- role assignment changes need human approval and rollback plan.

Recommended landing:

```txt
07_working/drafts/runtime_adapter/agents.template.PROPOSAL.yaml
```

v0 decision:

```yaml
role_assignment:
  mode: fixed
  dynamic:
    enabled: false
  self_claim:
    enabled: false
```

---

### 4.8 `claude-code-settings.template.json`

Decision: **Keep as hook config template; not executable policy yet.**

High-value content:

- SessionStart / PreCompact / Stop lifecycle hooks.
- PreToolUse hard blocks.
- PostToolUse report guard.
- Clear hook identifiers.

Risks:

- Actual Claude Code hook API may vary by version.
- Matching strings may be bypassed.
- Hook scripts do not exist in this bundle.
- Hook blocking behavior must be tested in a real local workspace.

Recommended landing:

```txt
07_working/drafts/runtime_adapter/claude-code-settings.template.PROPOSAL.json
```

Required before promotion:

- Validate hook schema against actual Claude Code environment.
- Write hook scripts.
- Add bypass tests.
- Decide advisory vs hard-block behavior per hook.

---

### 4.9 `bootstrap-prompt.md`

Decision: **Keep as paste-ready Claude Code bootstrap draft.**

High-value content:

- Smallest necessary truth pack.
- No repo walk.
- Decided / Pending / Undefined structure.
- Week 1 guardrail.
- zh-TW to human, English to files/agents.
- hard constraints.

Risks:

- Assumes local files exist at specific paths.
- May need project-specific path substitution.
- Should be generated from source layers later, not maintained manually forever.

Recommended landing:

```txt
07_working/drafts/runtime_adapter/bootstrap-prompt.CLAUDE-CODE.v0.md
```

---

### 4.10 `RISKS-AND-UNRESOLVED.md`

Decision: **Keep with high priority.**

This file should not be separated from the adapter plan.

High-value risks:

- Silent rule dropout.
- Hook bypass via creative shell syntax.
- distribute.sh sync failure.
- Claude-only instruction leakage into Cursor.
- Ollama output over-trust.
- Phase guardrail bypass.
- Hook performance overhead.

High-value unresolved items:

- Ollama transport.
- packet storage location.
- Codex hook equivalent.
- dynamic scoring persistence.
- A2A nesting schema.
- install.sh vs distribute.sh boundary.
- multi-project distribute conflicts.

Recommended landing:

```txt
07_working/drafts/runtime_adapter/RISKS-AND-UNRESOLVED.v0.md
```

---

## 5. Answer to Owner's “files.zip: What Should Be Deleted?”

### 5.1 Do not delete these from the source bundle archive

Keep the original `files.zip` as source evidence until the branch is merged back.

Reason:

- It preserves raw provenance.
- It lets main HEAD re-check whether mergeback summarized correctly.
- It avoids losing bundle context before promotion decisions.

### 5.2 After mergeback, do not copy all files into canonical locations

Do not place the entire extracted bundle into formal canonical folders.

Instead, copy selected files into draft/source-evidence locations.

Recommended handling:

| Item | Keep? | Delete from canonical target? | Reason |
|---|---:|---:|---|
| Original `files.zip` | Yes, temporarily | N/A | raw source evidence |
| Extracted temporary folder | No after merge | Yes | only workspace temp |
| `README.md` | Yes as source | Yes from canonical root | bundle index only |
| `MANIFESTO.md` | Yes as rationale draft | Yes from canonical truth | not approved positioning |
| Adapter plan | Yes | No, but only under drafts | high-value runtime adapter draft |
| YAML adapter manifest | Yes | Yes from canonical truth | schema unapproved |
| Packet shell | Yes | Yes from canonical packet truth | proposal only |
| Shared core template | Yes | Yes from approved shared core | needs decontamination |
| Agents template | Yes | Yes from approved registry | dynamic/self-claim unapproved |
| Claude settings template | Yes | Yes from production config | not tested |
| Bootstrap prompt | Yes | Yes from canonical truth | operational draft only |
| Risks file | Yes | No, under draft with plan | must accompany adapter draft |

### 5.3 Practical cleanup rule

After this mergeback file is accepted:

- Keep `files.zip` until main HEAD confirms it has absorbed the mergeback.
- Keep only the selected draft copies in repo.
- Delete the extracted temp folder.
- Do not delete the source archive before main HEAD returns confirmation.

Suggested local cleanup after main HEAD confirms:

```bash
rm -rf files_unzipped/
```

Do **not** delete `files.zip` until the branch merge is complete or the archive is stored elsewhere.

---

## 6. Core Issue Found: Hot-Join and Hot-Intake Are Real Missing Contracts

The owner's question was correct:

> Can shadowMAS allow many agents to join anytime and any project to attach anytime?

Answer:

- Yes, but not as naked entry.
- The current v0 direction supports the concept, but does not fully formalize the intake contract.
- Without intake normalization, non-packet work can lose authority, scope, timing, rationale, and trace.

This is not proof that shadowMAS is bad.

It means shadowMAS v0 needs one missing compatibility layer:

```txt
Raw / Legacy / External Input
  -> intake quarantine
  -> adapter wrapping
  -> packet candidate
  -> review
  -> promotion gate
```

Without this layer, “packet-first” becomes too brittle.

With this layer, shadowMAS can support arbitrary agents and arbitrary projects without pretending everything was packet-native from day one.

---

## 7. Required New Draft Files

This branch should recommend the following new draft documents.

### 7.1 `AGENT-JOIN-CONTRACT.v0.en.md`

Purpose:

Define how a new agent joins shadowMAS.

Minimum contents:

- agent identity
- runtime / host
- capability declaration
- intended L-layer
- allowed T-layer outputs
- writable locations
- forbidden actions
- required intake files
- packet output requirements
- stop / escalation conditions

Key rule:

> Agents may join dynamically, but no agent joins with undefined authority.

Recommended landing:

```txt
07_working/drafts/runtime_adapter/AGENT-JOIN-CONTRACT.v0.en.md
```

---

### 7.2 `PROJECT-INTAKE-CONTRACT.v0.en.md`

Purpose:

Define how an arbitrary project attaches to shadowMAS.

Minimum contents:

- project identity
- project truth priority
- current phase
- allowed scope
- forbidden scope
- repo traversal policy
- source docs / entry docs
- existing artifacts
- hot-intake status
- write-back boundary

Key rule:

> shadowMAS may assist any project, but project-domain truth remains project-local.

Recommended landing:

```txt
07_working/drafts/runtime_adapter/PROJECT-INTAKE-CONTRACT.v0.en.md
```

---

### 7.3 `LEGACY-INTAKE-NORMALIZATION.v0.en.md`

Purpose:

Define how non-packet history, chat, docs, task sheets, screenshots, Claude/Cursor/Codex outputs, or pre-shadow work enters the system.

Minimum contents:

- source kind
- original source preservation
- capture timestamp
- original author / claimed authority
- extraction method
- converted packet candidate
- confidence
- loss notes
- unresolved authority claims
- human confirmation requirements

Key rule:

> Non-packet material may enter shadowMAS, but it enters as evidence or candidate, not approved truth.

Recommended landing:

```txt
07_working/drafts/runtime_adapter/LEGACY-INTAKE-NORMALIZATION.v0.en.md
```

---

### 7.4 `PACKET-COMPATIBILITY-LAYER.v0.en.md`

Purpose:

Define compatibility levels between native shadowMAS packets and non-native inputs.

Minimum model:

| Level | Name | Meaning | May route? | May promote? |
|---|---|---|---:|---:|
| L0 | raw_intake_evidence | raw chat/doc/output/source | No direct routing | No |
| L1 | adapter_wrapped_artifact | raw source plus metadata | Limited | No |
| L2 | packet_candidate | normalized packet-shaped object | Yes, after review | No direct |
| L3 | approved_packet | reviewed packet | Yes | only through promotion gate |

Key rule:

> Packet compatibility is not binary. It must preserve uncertainty and loss.

Recommended landing:

```txt
07_working/drafts/packet/PACKET-COMPATIBILITY-LAYER.v0.en.md
```

---

### 7.5 `RUNTIME-ADAPTER-CONTRACT.v0.en.md`

Purpose:

Define the general contract for Claude Code, Cursor, Codex, Ollama, hooks, and skills.

Minimum contents:

- runtime identity
- host constraints
- prompt delivery method
- tool capability boundary
- hook support
- skill support
- delegation input / output contract
- protected actions
- audit/logging expectations
- adapter-specific non-truth rule

Key rule:

> A runtime adapter adapts execution. It does not redefine truth.

Recommended landing:

```txt
07_working/drafts/runtime_adapter/RUNTIME-ADAPTER-CONTRACT.v0.en.md
```

---

## 8. RideDispatch Phase Guardrail to Preserve

The current commercial project phase remains narrow.

Allowed Week 1 focus:

- `/dashboard`
- `/orders/create`
- `/no-access`
- API client skeleton
- mock / real switch
- typecheck / build
- backend `/health`
- backend `POST /orders`
- backend `POST /orders/force-create` or stable contract
- stable response / error format
- stable geofence blocked response
- development CORS / base URL rules

Forbidden for Week 1:

- Dispatch
- Station
- Chat
- Audit Center
- Management CRUD
- permission persistence
- CTI integration
- formal Auth
- formal Audit
- Wallet
- schema / migration expansion beyond approved need
- first-level directory changes

Any adapter, hook, prompt, or task packet that pushes implementation beyond this scope should be blocked or deferred.

---

## 9. Proposed Landing Structure

Recommended repo landing if this is merged as draft work:

```txt
07_working/drafts/runtime_adapter/
├── SHADOWMAS-RUNTIME-ADAPTER-MERGEBACK.v0.md
├── claude_bundle/
│   ├── README.md
│   ├── SHADOWMAS-CLAUDE-CODE-ADAPTER-PLAN.v0.md
│   ├── adapter-plan.v0.yaml
│   ├── agents.template.PROPOSAL.yaml
│   ├── bootstrap-prompt.CLAUDE-CODE.v0.md
│   ├── claude-code-settings.template.PROPOSAL.json
│   ├── shared_core.template.DRAFT.md
│   └── RISKS-AND-UNRESOLVED.v0.md
├── AGENT-JOIN-CONTRACT.v0.en.md                 # follow-up draft
├── PROJECT-INTAKE-CONTRACT.v0.en.md             # follow-up draft
├── LEGACY-INTAKE-NORMALIZATION.v0.en.md         # follow-up draft
└── RUNTIME-ADAPTER-CONTRACT.v0.en.md            # follow-up draft

07_working/drafts/packet/
├── packet_common_shell.PROPOSAL.v0.yaml
└── PACKET-COMPATIBILITY-LAYER.v0.en.md          # follow-up draft

07_working/drafts/rationale/
└── SHADOWMAS-MANIFESTO-DRAFT.v0.md
```

Do not put these directly into:

```txt
01_truth/
02_packets/
03_memory/
04_runtime/
```

until promotion review is complete.

---

## 10. Open Decisions for Main HEAD

Main HEAD / human owner must decide:

1. Should `MANIFESTO.md` become a human-facing rationale doc, a README positioning section, or remain private draft?
2. Should AGENTS.md become the cross-tool entry convention for shadowMAS local workflows?
3. Should `~/.claude/CLAUDE.md` symlink to `~/AGENTS.md`, or should Claude maintain a separate adapter file?
4. Where should packets physically live?
5. Should `packet_common_shell.v0.yaml` be promoted, revised, or replaced by a stricter packet schema?
6. Should `role_assignment.mode` remain fixed for v0? Recommended answer: yes.
7. How should non-packet legacy work be normalized?
8. Should install/distribute scripts be part of v0, or deferred until after adapter contract?
9. Should hook templates be implemented now, or first documented as non-executable policy?
10. How to sync ChatGPT Custom Instructions given host-native manual limitation?

---

## 11. Recommended Next Task Packet for Main HEAD

```yaml
task_packet:
  goal: "Merge Claude runtime adapter bundle into shadowMAS working drafts without promoting it to canonical truth."
  scope:
    - "Create draft landing paths under 07_working/drafts/runtime_adapter/"
    - "Preserve Claude adapter plan and risks file as source draft material"
    - "Create or request follow-up drafts for agent join, project intake, legacy intake normalization, packet compatibility, and runtime adapter contract"
  out_of_scope:
    - "Do not modify 01_truth canonical files"
    - "Do not replace existing packet truth"
    - "Do not implement hooks"
    - "Do not change RideDispatch Week 1 business scope"
    - "Do not introduce Dispatch/Station/Chat/Audit/Auth/CTI tasks"
  truth_touchpoints:
    - "SHADOWMAS-CURRENT-TRUTH.v0.en.md"
    - "SHADOWMAS-PROMPT-LAYERING-CONTRACT.v0.en.md"
    - "SHADOWMAS-GOVERNANCE-MATRIX.v0.en.md"
    - "SHADOWMAS-CHANGE-IMPACT-MAP.v0.en.md"
    - "WEEK1_BACKEND_NEEDS_v2.md"
    - "backend_roadmap.md"
  worker_plan:
    - "Land Claude bundle files only under draft/source-evidence paths"
    - "Mark packet shell as proposal, not canonical"
    - "Preserve risks and unresolved decisions"
    - "Create follow-up task list for missing contracts"
    - "Report deferred files and intentional non-promotions"
  acceptance_criteria:
    - "No canonical truth files are changed"
    - "All Claude bundle files are either preserved as draft evidence or intentionally excluded"
    - "Hot-join and hot-intake gaps are explicitly documented"
    - "Week 1 RideDispatch guardrail remains unchanged"
    - "Main HEAD receives mergeback summary and unresolved decisions"
  stop_conditions:
    - "Need to change 01_truth or 02_packets canonical files"
    - "Need to decide public positioning or license"
    - "Need to implement executable hooks"
    - "Need to change project business scope"
```

---

## 12. Merge Message to Main HEAD

```txt
Claude adapter branch mergeback ready.

I reviewed files.zip from Claude. The bundle is valuable but should be treated as Layer 4 runtime-adapter draft material, not canonical shadowMAS truth.

Recommended merge:
- Preserve SHADOWMAS-CLAUDE-CODE-ADAPTER-PLAN.v0.md and RISKS-AND-UNRESOLVED.md under 07_working/drafts/runtime_adapter/.
- Preserve packet_common_shell.v0.yaml only as packet shell proposal, not as canonical packet replacement.
- Preserve MANIFESTO.md only as rationale/positioning draft, not canonical truth.
- Keep shared_core.template.md, agents.template.yaml, claude-code-settings.template.json, and bootstrap-prompt.md as draft templates only.

Main finding:
shadowMAS can support multi-agent hot-join and arbitrary project hot-intake, but v0 still needs explicit contracts for:
1. AGENT-JOIN-CONTRACT
2. PROJECT-INTAKE-CONTRACT
3. LEGACY-INTAKE-NORMALIZATION
4. PACKET-COMPATIBILITY-LAYER
5. RUNTIME-ADAPTER-CONTRACT

No more Claude reply is required for this branch.
The branch can return to main HEAD after this mergeback artifact is accepted.
```

---

## 13. Final Branch Status

```txt
branch: claude-runtime-adapter-mergeback
status: ready_to_return_to_main_head
claude_reply_needed: false
canonical_truth_change: false
draft_material_created: true
hot_join_gap_identified: true
hot_intake_gap_identified: true
legacy_packet_gap_identified: true
week1_scope_preserved: true
```

---

## 14. Short Answer to Owner

Yes, after producing this file, this branch can go back to main HEAD.

`files.zip` should not be blindly deleted before main HEAD confirms mergeback. Keep the original archive as source evidence. Delete only temporary extracted folders after merge. Preserve selected files as draft material, not canonical truth.

---

## 15. Follow-Up Drafts Authored Later

The five follow-up gaps identified by this mergeback were later authored as working drafts only:

- `07_working/drafts/runtime_adapter/AGENT-JOIN-CONTRACT.v0.en.md`
- `07_working/drafts/runtime_adapter/PROJECT-INTAKE-CONTRACT.v0.en.md`
- `07_working/drafts/runtime_adapter/LEGACY-INTAKE-NORMALIZATION.v0.en.md`
- `07_working/drafts/packet/PACKET-COMPATIBILITY-LAYER.v0.en.md`
- `07_working/drafts/runtime_adapter/RUNTIME-ADAPTER-CONTRACT.v0.en.md`

These drafts remain non-canonical runtime-adapter support material and do not promote Claude bundle content into approved truth.
