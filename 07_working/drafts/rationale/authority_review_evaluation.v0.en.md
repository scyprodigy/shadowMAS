# authority_review_evaluation.v0.en | working evaluation plan for authority boundaries and evidence-preserving review
# related: [DECISION-review-brief-primary-direction, RATIONALE-attention-budget-review, l1_mutation_coverage_report, external_paradigm_references]
# phase: draft_non_canonical

# Authority and Review Evaluation

This working note collects reusable evaluation questions. It does not change
project identity, packet schemas, runtime contracts, or promotion authority.
It reports no new experiment or human-review benefit.

## Information must retain its authority

Test whether a runtime signal becomes truth, a retrieval result becomes
approved memory, an audit projection becomes approval, or a recommendation
becomes permission to act without the required promotion path. A summary must
preserve source status, unresolved uncertainty, and invalidation conditions.
Fluent wording and valid structure alone do not establish those properties.

Use the existing named invariants and fixtures before proposing new fields.
Each evaluated case needs a source rule, expected result, and evidence location.
This adapts the repository's authority-layer and information-flow references
to an evaluation plan; it adds no enforcement mechanism.

## Separate evidence levels

| Evaluation | Comparison and measurements | Limit on the conclusion |
|---|---|---|
| Designed fixtures | Positive cases, single-target mutations, partial-compliance traps; compare always-pass, always-fail, and structure-only validators; report detection and false passes | Tests the authored corpus, not deployment safety |
| Multi-step traces | Locate the first unauthorized transition and subsequent consequences; measure detection and step attribution against labelled breakpoints | Correct final classification can still conceal an incorrect explanation |
| Independent cases | Cases and labels produced independently of the checker; use held-out cases and report precision, recall, disagreement, and sample sizes | Self-authored cases are not independent validation |
| Human review | Compare the existing review workflow with a brief, using matched tasks and recorded decisions; report errors, total review time, and uncertainty | Shorter output is not evidence of better oversight |
| Generalization | Held-out tasks and independently coded outcomes | Construct and predictive validity require separate evidence |

The existing fixture report remains the owner of its counts and results.
Do not copy historical test totals into a new claim about the current suite.
No calendar, funding programme, or external submission is needed to use this
sequence; advance when the previous evidence and required review are available.

## Review compression must preserve checkable evidence

The existing task-scoped brief is the implementation surface. Evaluate it
against a full diff and the current manual review process rather than adding
a parallel review-card command.

- Count input lines, output lines, preparation time, and verification time
  separately. A line-count ratio measures size, not comprehension or quality.
- Label relevant risk locations independently. Report missed locations as
  well as false flags; a heuristic cannot measure its own recall.
- Keep source paths and line locations so a reviewer can check each selection.
  Record coverage limits and missing inputs beside the selected evidence.
- Compare changed paths with the declared task scope. Treat an unexpected
  path as a review question, not proof of a violation or permission to delete.
- Group repeated flags for readability while retaining their locations and
  counts. Deduplication must not make omitted locations disappear.
- Distinguish executable changes from comments and data, but retain sensitive
  material checks in all text. Blanket comment or string exclusion can hide
  credentials, embedded code, and authority-bearing configuration.
- Keep any task-specific concern terms local and explicit. A no-match result
  only describes the inspected inputs; it is not an all-clear conclusion.

These are methodological lessons from exploratory keyword filtering, not a
precision or oversight result. Evaluate thresholds on independent examples
before using them to make adoption claims.

## Public reproduction and claim limits

Use synthetic or deliberately generalized examples. Preserve source-rule
links and expected outcomes without publishing contacts, private proposals,
local paths, account identifiers, or reversibly encoded substitutes. Public
artifacts must be reviewed independently of their private source material.

Passing fixtures does not prove runtime safety, real-world collusion or memory
poisoning detection, human-review improvement, construct validity, or predictive
validity. Recommendations and compiler output remain advisory; human approval
must not be inferred from a successful check.
