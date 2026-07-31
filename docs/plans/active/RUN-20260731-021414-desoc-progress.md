# Run Plan: RUN-20260731-021414-desoc-progress

Status: active

## Formal Phase Packet

- Parent Run: `RUN-20260731-021414-repository-work-cycle-cai-hourly`
- Repo / workflow / mode / Lane: `desoc-publishing` / `system-runtime#repo-progress-run` / `system-canon#execute` / `1`
- Starting revision: `bb4424375fea`
- Write boundary: `src/local_experiment.py`, `scripts/build_local_experiment.py`,
  `tests/test_local_experiment.py`, `docs/product/phase-0-producer-preflight-question.md`,
  `docs/evaluations/phase-0-producer-preflight-evaluation.md`, `STATUS.md`,
  `LANE-STATE.yaml`, and this Run Plan.

## Objective

Make the offline portable-artifact contract usable from the producer side: a
local preflight must report every discovered artifact's structural readiness
and explain failures without deciding whether its research is admissible,
correct, or authored by its displayed producer.

## Purpose Connection and Intended Material Effect

The founding purpose requires that producers can publish simple research
artifacts without an institutional gatekeeper. The existing experiment proves
consumer orientation but gives a producer only a fail-fast generator error.
This slice will add a deterministic, offline preflight report that permits a
producer to see valid artifacts and all structural failures in one pass while
preserving the strict portable manifest contract and non-verification limits.

## Method, Constraints, and Done-When

- Treat this as Lane 1 solution design, implementation, and local product
  validation using only synthetic fixtures.
- Do not alter the manifest schema, create quality/admission thresholds,
  select a stack, accept submissions, launch a service, or use network data.
- Preflight must not write generated product output or mutate fixtures.
- The report must have stable lexical ordering, include valid artifact IDs,
  retain error detail for invalid artifact directories, and explicitly state
  that it verifies structure only.
- Tests must exercise a mixed valid/invalid fixture corpus and verify that
  generation remains fail-closed. Repository validation, unit tests, and
  `git diff --check` must pass before closeout.

## Execution Notes

Selected under active Lane 1 from the distinct producer-side gap left by the
2026-07-28 consumer-orientation evaluation. No recent active plan overlaps
this footprint. Required flows: `standard-run-safety-check`, `select-lane`,
`create-run-plan`, `revalidate-lane-selection`, and `append-run-receipt`.
Conditional flows anticipated: `classify-artifact-disposition`,
`rerank-next-work`, and `refresh-lane-state`.

## Receipt

Outcome: progressed

Material effect: the offline slice now exposes a deterministic producer-side
structural preflight. It reports each discovered artifact directory, preserves
valid entries in a mixed corpus, returns correction detail for malformed
directories, and explicitly rejects quality, admission, identity, authorship,
and priority inferences.

Validation: `python3 -m unittest discover -s tests -v` passed 12 tests;
`python3 scripts/build_local_experiment.py --preflight` reported all four
committed synthetic artifacts ready; `python3 scripts/validate_repository.py`
and `git diff --check` passed.

Required-flow attestation: `standard-run-safety-check`, `select-lane`,
`create-run-plan`, `revalidate-lane-selection`, and `append-run-receipt`.
Conditional flows invoked: `classify-artifact-disposition`,
`rerank-next-work`, and `refresh-lane-state`.

No non-GitHub external action occurred. Attention route: none. Next handoff:
identify a distinct producer-to-consumer gap; do not turn structural preflight
into a content-admission system.

Status: complete
