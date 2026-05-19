# l2_handoff_trace_fixtures | public L2 multi-step handoff trace fixture skeletons
# related: [examples_index, mutations_corpus, l2_trace_fixture_schema]
# phase: public_fixture_skeletons

# L2 Handoff Trace Fixtures

## Purpose

This directory contains public-safe L2 multi-step trace fixture skeletons for shadowMAS authority-boundary evaluation work.

L2 traces model how an information object can drift across more than one handoff step. They are intended to complement the L1 mutation fixtures under `examples/mutations/`, which isolate single-field invariant failures.

## Difference From L1

L1 mutation fixtures change one field at a time and are meant to exercise one named invariant directly.

L2 trace fixtures describe short sequences. Each step records how a signal, summary, projection, or recommendation is carried forward and where a stronger authority layer is incorrectly implied.

## Boundary Modeled

The core boundary is that T4/T5 information must not become T2/T3 unless a governed validation or promotion path exists.

These traces focus on handoff failure shapes such as:

- ephemeral context being treated as durable memory
- an execution-feed observation being treated as canonical truth
- a compliant-looking summary hiding an authority-boundary failure across steps

## Non-Claims

These files are fixture skeletons only.

They are not validation results. They do not show runtime behavior, runtime enforcement, formal validation, construct validity, predictive validity, or production safety.

They do not modify validator logic and do not prove that a future validator detects these patterns.
