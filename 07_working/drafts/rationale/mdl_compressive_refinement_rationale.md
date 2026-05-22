# mdl_compressive_refinement_rationale | draft rationale for minimum-description and net-effect refinement principles
# related: [rationale_evaluation_drift, l2_handoff_traces, inspect_l2_fixture, task_atomicity]
# phase: draft_rationale

# Rationale: MDL, Compressive Refinement, and Net-Effect Parsimony

## Purpose

This memo records a draft rationale for three working primitives the project owner has identified as useful for future shadowMAS design decisions:

- minimum-description-length (MDL) reasoning,
- compressive refinement,
- parsimony / net-effect criterion.

It is a draft rationale only. It is not canonical truth, not a schema, not validator logic, not a runtime claim, and not a recommendation for any specific code change. It exists so future tasks can reach for a shared vocabulary when deciding whether a proposed refinement is worth its cost.

## Concept summary

### Minimum description length

A rough framing of MDL as it is used here:

L(model semantics) ≈ L(explanation) + L(corrections needed)

- *Complexity*: how long, how nested, or how branched the explanation is — how much structure a reader or downstream consumer has to load to follow it.
- *Faithfulness cost*: how much of the underlying reality the explanation omits and will later need to be patched, corrected, or extended.

The useful framing is **not** "make every explanation shorter." It is "minimize complexity subject to a faithfulness threshold." A short explanation that needs many later corrections is not cheap; it has merely pushed cost into the future. A long explanation that exhausts a hidden distinction is not wasteful; it has paid the cost up front.

### Compressive refinement

Compressive refinement is rewriting a structure so its surface becomes smaller, simpler, or more inspectable *while preserving the original semantics*. The aim is not deletion; it is exposure. Hidden semantics that were carried implicitly in prose, in a delimiter convention, or in a single overloaded string get re-encoded as explicit structure that can be read, queried, or checked.

Three small intuitions:

- a string with a custom delimiter scheme becomes an object with named fields.
- a long narrative log becomes a smaller rationale memo that names the load-bearing claim.
- a vague task becomes an atomic mission with explicit allowed-edit and constraint lists.

In each case the same meaning is preserved but more of it is now inspectable.

### Parsimony / net-effect criterion

A refinement is better only if the reduction in ambiguity, correction load, or hidden semantics outweighs the added structure or reviewer burden. This is the brake that prevents compressive refinement from collapsing into elegant-but-unreadable abstraction.

Two failure modes the criterion guards against:

- *under-refinement*: leaving meaning implicit because it "feels obvious," and paying for it later in repeated corrections.
- *over-refinement*: lifting every implicit convention into formal structure, so the reader has to load a vocabulary before reading anything else.

## shadowMAS interpretation

These three primitives map onto concrete shadowMAS design areas without becoming rules:

- **atomic task design**: a task spec that names its allowed files, forbidden files, and exit conditions trades narrative compactness for inspectability — typically a positive net effect when several agents or humans share the task.
- **fixture design**: a fixture whose authority boundary is encoded as an explicit `source_layer` / `target_layer` / `relation` triple makes hidden authority promotion visible to a checker, a reader, and a diff tool at once.
- **schema refinement**: when a single string starts carrying two or more independent meanings, splitting it into named fields is usually a positive net effect; collapsing two fields whose meanings always co-vary is usually neutral or positive.
- **mega-log extraction**: pulling a load-bearing rationale paragraph out of a long historical log into a small named memo (this file, and its neighbours) is a compressive refinement: the semantics survive, the surface shrinks, and the rationale becomes citable.
- **hook profile refinement**: the recent change to `.claude/hooks/check_header.sh` — accepting both 3-line metadata headers and legacy canonical filename-H1 lines — is a small example of reducing exception sprawl. The hook now describes one explicit two-profile contract instead of an implicit set of one-off allowances.

The pattern across these examples is the same: each refinement was worth it because the resulting surface was easier to read and check, not because it was shorter.

## Non-goals

This memo deliberately does **not**:

- define a mathematical scoring system, a cost metric, or a refinement-acceptance formula.
- create a validator rule, a CLI check, or a test.
- create a semantic vocabulary registry.
- introduce a new field, schema, or invariant.
- claim formal validation, construct validity, or predictive validity for any shadowMAS surface.
- claim runtime safety or production safety for any shadowMAS surface.
- replace human judgement about whether a specific refinement is worth its cost.

It is a draft vocabulary for human and agent reviewers, nothing more.

## Practical heuristics

A short, qualitative list. None of these are rules; all of them are prompts for a reviewer.

- shorter is not automatically better; cheaper-to-maintain is the actual target.
- structure is useful only if it reduces future ambiguity or correction load.
- do not harden speculative layers; over-formalising a design that is still moving costs more than it saves.
- expose hidden semantics when repeated correction shows they are real, not on first suspicion.
- keep human-readable and machine-readable forms aligned but not identical; redundant exact mirroring usually pays its cost twice.
- a refinement that reduces surface but increases the vocabulary a reader must already know is not a net win.

## Examples from current repo

These public, current-repo examples illustrate the rationale. None of them is offered as proof of anything beyond itself.

- `examples/traces/l2_handoff/*.json` encode unsafe-transition as an explicit `{source_layer, target_layer, relation}` object instead of a single sentence. The hidden authority promotion is now a structured claim a checker can read.
- `tests/test_inspect_l2_fixture.py` pins the L2 inspector's JSON output envelope and the inspector's violation-accumulation behaviour. These tests expose contracts that were previously implicit in code.
- `tests/test_shadowmas_minimal_validator.py::test_partial_compliance_traps` was tightened from "target invariant *in* fails" to "fails == [target_invariant]". The contract documented in `examples/mutations/README.md` was previously stricter than the test; the test now matches the documented promise.
- `.claude/hooks/check_header.sh` declares one two-profile contract (3-line metadata header *or* legacy canonical filename-H1) instead of an implicit pile of file-by-file exceptions.
- The README and onboarding-guide framing sweeps moved shadowMAS self-positioning from "governance system" to "dynamic packetized shadow layer." That change is compressive in the parsimony sense: it removed an overclaim while keeping the description of what the repo actually is.

None of these examples shows that the refinement principles are correct in general. They show only that, in these specific cases, the resulting surface was easier to read or check.

## Future promotion conditions

This rationale should be considered for promotion to a more canonical form only if all of the following continue to hold:

- it has been useful as a shared vocabulary across multiple concrete tasks, not only the one that produced it.
- using it has not increased reviewer burden — that is, reviewers cite the rationale to make decisions faster, not to debate the rationale itself.
- the heuristics here have survived contact with real refactors without needing repeated patching.
- no part of it has drifted into being treated as a validator rule, a schema constraint, or a runtime claim.

Until those conditions are met, this file stays in `07_working/drafts/rationale/` as working rationale, non-canonical, public-safe.

## Non-claims

- not canonical truth.
- not a schema, validator rule, or CLI behaviour.
- not a runtime safeguard.
- not formal validation, construct validity, or predictive validity evidence.
- not a guarantee that any specific refinement is correct.
- not a replacement for human review of individual design changes.
