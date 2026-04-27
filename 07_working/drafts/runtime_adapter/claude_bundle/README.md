> status: draft / source-evidence
> authority: none
> do not promote without governance review

# shadowMAS Claude Code Adapter v0 — Output Bundle

> Layer 4 Runtime Adapter design package for RideDispatch project under shadowMAS v0 governance.
> Produced as L2 planning output. To be merged by GPT head session.

## Files in this bundle

| # | File | Purpose | Format |
|---|---|---|---|
| 1 | `SHADOWMAS-CLAUDE-CODE-ADAPTER-PLAN.v0.md` | Main plan document, eight chapters with zh-TW narrative | Markdown |
| 2 | `MANIFESTO.md` | Positioning statement + Shadow Doctrine + Calibrated Trust philosophy | Markdown |
| 3 | `adapter-plan.v0.yaml` | Machine-stable self-description of the entire plan | YAML |
| 4 | `packet_common_shell.v0.yaml` | Fused packet shell (shadowMAS canonical + extensions for A2A future) | YAML |
| 5 | `shared_core.template.md` | 161-line Shared Core template for `~/.shadowmas-user/` | Markdown |
| 6 | `agents.template.yaml` | Agent registry template with three role-assignment modes | YAML |
| 7 | `claude-code-settings.template.json` | Hook configuration for `.claude/settings.json` | JSON |
| 8 | `bootstrap-prompt.md` | Paste-ready first-message prompt for new Claude Code session | Markdown |
| 9 | `RISKS-AND-UNRESOLVED.md` | Risks (R1-R7), Unresolved (U1-U7), Missing Decisions, mergeback note for GPT head | Markdown |

## Reading order

For a human reviewing this for the first time:

1. **MANIFESTO.md** — understand the positioning (5 min)
2. **SHADOWMAS-CLAUDE-CODE-ADAPTER-PLAN.v0.md** — full plan in zh-TW with eight chapters (20 min)
3. **RISKS-AND-UNRESOLVED.md** — see what is deferred and why (10 min)
4. Templates (4-7) — skim to confirm shape, deeper reading when implementing
5. **bootstrap-prompt.md** — when you actually start a Claude Code session

For an agent receiving this bundle:

1. `adapter-plan.v0.yaml` — machine-stable summary
2. `packet_common_shell.v0.yaml` — packet protocol
3. `shared_core.template.md` — behavioral baseline
4. `bootstrap-prompt.md` — operational entry

## What is in scope

- Claude Code prompt composition (file layering)
- Skills invocation policy (4 existing skills)
- Hooks policy (7 minimum + 3 lifecycle)
- Delegation routing (Claude Code → Cursor / Ollama)
- Session bootstrap protocol
- Week 1 phase guardrail
- Paste-ready bootstrap prompt
- Risk and unresolved log

## What is NOT in scope

- shadowMAS governance truth modifications
- RideDispatch business specifications
- Week 1 actual implementation code
- Memory plane runtime (deferred v0.5)
- Promotion gate automation (deferred)
- Trust scoring runtime (deferred v0.5)
- Cross-organization A2A endpoints

## Strategic position recap

**shadowMAS is not competing with A2A or Microsoft AGT.**

A2A handles enterprise inter-agent transport (HTTPS, OAuth, 150+ orgs).
Microsoft AGT handles enterprise agent fleet governance (DID, IATP, compliance).
shadowMAS handles **personal-scale workstation MAS governance** — one developer, multiple coding agents, own laptop, no vendor lock-in.

The packet shell is designed to be embeddable inside A2A Message Parts when a user later scales to enterprise. No rewrite needed.

## Three non-negotiable design choices

1. **Three-layer file separation** — shadowMAS core (read-only) / user layer (`~/.shadowmas-user/`) / project layer (`{project}/.shadowmas/`). Business logic never pollutes shadowMAS repo.

2. **AGENTS.md as universal entry** — distribute.sh produces one source, all AGENTS.md-aware tools read it. `~/.claude/CLAUDE.md` is a symlink to `~/AGENTS.md`. Single source of truth, multiple consumers.

3. **Hook three-tier check** — fixed gate (always trigger on event) + random audit (defeat rubber-stamping, v0.5) + forced block (absolute denial). Calibrated Trust framework as design backbone.

## Mergeback note for GPT head session

This bundle is a **proposal**, not a directive. GPT head retains dispatch authority. Items requiring human owner approval:

- Adoption of MANIFESTO positioning
- Switch from `mode: fixed` to `dynamic` or `self_claim` (defer decision)
- Open-source license choice
- Schedule for v0.5 features (memory plane, dynamic scoring, A2A wrapping)

If any conflict with shadowMAS canonical truth, this adapter plan defers.

---

End of bundle. The shadow takes the shape of whatever you cast.
