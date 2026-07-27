# Run Plan: Bound the Corpus Entry and Version Comparison Revision

Status: complete

Run ID: `RUN-20260725-070927-desoc-progress`

Parent Run: `RUN-20260725-070927-repository-work-cycle-cai-hourly`

## Target

- Owner: `desoc-publishing`
- Repository: `repos/public/desoc-publishing`
- Starting revision: `edec337ccc4152aa25d7eded5d2d98bee918f9c0`
- Working tree: clean
- Run mode: scheduled/non-interactive
- Write boundary: this repository's product, current-status, Lane-state, and
  run-plan records only

## Run Family

- Phase: Progress
- Workflow: `system-runtime#repo-progress-run`
- Workflow graph revision: `sha256:09ceebd5cdcb21090c418dd504a529b7bd10a906f5709a709a70f14d9adc918c`
- Orchestration workflow: `system-runtime#repository-work-cycle`
- Orchestration revision: `sha256:ca14ff3517db01c5b0decfed879b44f6646b4ba910ea0582e605ae863eb7c499`
- Mode: `system-canon#execute`

## Lane Selection

- Lane: `1` (`Product opportunity and shaping`)
- Manifest revision: `1`; definition ordinal: `1`; control revision: `1`
- Control state and in-flight policy: `active`, `continue_current`
- Manifest SHA-256: `1cf6003f389a6c844c7a2c6f30ef72e144592013f5c93b2c88305ba8a8131e7c`
- Emergency entries: none; emergency-revocation digest unchanged from the
  preceding closed run
- Selection basis: the preceding Lane 3 evaluation and current Lane state both
  require this bounded shape before implementation can resume.

## Objective

Specify the smallest deterministic corpus-entry and immediate-predecessor
comparison revision that lets a human enter the synthetic corpus and answer
what changed without source inspection.

## Context And Constraints

Read the root and CAI authority, steward overlay, repository Constitution,
status, Lanes, Lane state, preceding evaluation/plan, product packet, and the
progress workflow and required flows. Preserve the portable two-file producer
contract, synthetic/offline/dependency-free boundary, deterministic ordering,
and absence of a quality/admission score. Do not change Lane 2 implementation,
select a production stack, launch, use real data, or perform an external action
other than ordinary authorized GitHub versioning.

The session-sync start check attempted its required fetch but could not resolve
`github.com`; local branch state was clean and no writer lock existed. This
does not prevent owner-local shaping; it does prevent claiming a fresh remote
sync or a successful push until connectivity returns.

## Expected Writable Surfaces

- `docs/product/phase-0-corpus-entry-and-version-comparison-revision.md`
- `docs/product/phase-0-first-local-experiment.md`
- `STATUS.md`
- `LANE-STATE.yaml`
- this run plan

## Recent Run Collision Check

The immediately preceding related plan, `RUN-20260724-221205`, is complete
and selected this distinct Lane 1 shaping work. No plan modified in the last
hour, live writer, shared-index activity, or `capacityos-writer.lock` was
found. The tree was clean at `HEAD` before this plan.

## Plan

1. Define the generated corpus entrypoint, links, deterministic ordering, and
   source disclosures.
2. Define exact immediate-predecessor comparison semantics for stable claims,
   support, and disagreement relationships, including absence and edge cases.
3. State implementation boundaries and behavioral acceptance checks that make
   the Lane 2 slice executable and Lane 3 reevaluable.
4. Revalidate the Lane immediately before owner effects, update owner truth,
   rerank the next work, validate, append the receipt, then commit/push if the
   network permits.

## Execution Notes

Plan created after formal packet, Lane, authority, clean-tree, and writer-lock
checks. No owner content effect has occurred yet.

- Revalidated immediately before the owner effects: `HEAD` stayed at
  `edec337ccc4152aa25d7eded5d2d98bee918f9c0`, Lane 1 remained active with
  `continue_current`, the manifest and workflow digests matched the packet,
  and no writer lock or emergency revocation appeared.
- Created the delivery-ready product contract. It specifies the root
  `index.html` traversal, deterministic entry contents and ordering,
  predecessor links, immediate-predecessor-only comparison scope, exact stable
  claim/support/disagreement matching rules, and testable behavioral outcomes.
- Kept the portable source schema and the held Lane 2 implementation intact.
  The contract explicitly prohibits derived state in producer manifests,
  implicit scores, stack selection, and external interaction.
- Updated current product, status, and Lane truth so Lane 2 is ready to
  implement the bounded revision and Lane 3 has an exact reevaluation entry.

## Next-Work Handoff

- current work: corpus-entry and version-comparison shaping
- current disposition: ENDPOINT_POSITIVE
- durable priority owner: desoc-publishing
- recommendation status: provisionally selectable under local rules

| rank | eligible lane or work item | why now | dependencies / gates |
|---:|---|---|---|
| 1 | Lane 2: implement corpus entry and derived comparison | The accepted local contract removes the semantic delivery gate while preserving the safe baseline. | Synthetic/offline only; keep generated output ignored and run stated behavioral checks. |
| 2 | Lane 3: reevaluate revised traversal | It directly tests the repaired consumer loop. | Ineligible until Lane 2 implements and validates the contract. |

- recommended next: Lane 2 bounded local delivery
- switch signal: Lane 1 specified reproducible entry and comparison behavior
- strongest alternative: Lane 3 reevaluation, lower because it would only
  reproduce the known negative endpoint before implementation
- overturning evidence: a contract inconsistency with the portable source
  model or a delivery test that proves the stated behavior cannot be generated
  safely
- steward reconciliation needed: no; owner status and Lane state are updated

## Validation

- `python3 scripts/validate_repository.py` — passed.
- `python3 -m unittest discover -s tests -p 'test_*.py'` — six tests passed.
- `python3 scripts/build_local_experiment.py --fixtures fixtures --output
  _local/experiment` — passed offline; retained the evaluated baseline output.
- `git diff --check` — passed.
- Product-contract inspection — confirmed a root entrypoint, predecessor-link,
  stable-claim/support/disagreement comparison, and behavioral-test contract
  with no production-stack or external-action expansion.

## Receipt

- Result: `progressed`.
- Owner/Lane: `desoc-publishing`, Lane `1`; manifest revision `1`, definition
  ordinal `1`, control revision `1`, `continue_current`.
- Material effect: a delivery-ready contract now makes the failed human
  traversal executable as a deterministic local Lane 2 revision and gives
  Lane 3 observable re-evaluation checks.
- Actual footprint:
  - `LANE-STATE.yaml`
  - `STATUS.md`
  - `docs/plans/active/RUN-20260725-070927-desoc-progress.md`
  - `docs/product/phase-0-corpus-entry-and-version-comparison-revision.md`
  - `docs/product/phase-0-first-local-experiment.md`
- Revalidation: owner, active Lane 1 control, pinned `HEAD`, manifest and
  workflow digests, no writer lock, and no emergency revocation matched before
  the content effects.
- Required flows attested: `standard-run-safety-check`, `select-lane`,
  `create-run-plan`, `revalidate-lane-selection`, `append-run-receipt`.
- Conditional flows invoked: `refresh-lane-state`, `rerank-next-work`,
  `classify-artifact-disposition`.
- Flow exceptions: none. Method refs: `[]`; method effect: `null`.
- External actions: none. GitHub versioning is authorized, but the required
  session sync fetch failed because DNS could not resolve `github.com`; push
  will be attempted only after the coherent local commit.
- Current-work disposition: `ENDPOINT_POSITIVE`. Next: Lane 2 local delivery.
- Joe attention: none.
