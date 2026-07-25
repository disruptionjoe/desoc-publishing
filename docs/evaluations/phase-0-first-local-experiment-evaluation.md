# Evaluation: Phase 0 First Local Experiment

Status: complete

Evaluated: 2026-07-24

Run: `RUN-20260724-221205-desoc-progress`

Disposition: revise and return to Lane 1 problem shaping

## Bottom line

The dependency-free generator is a sound mechanical baseline, but the current
slice does not yet answer its central product question for a human consumer.
It generates no corpus-level HTML entrypoint, and its version view names a
predecessor without linking to it or explaining claim-level changes. A person
therefore needs hidden filesystem knowledge to enter the corpus and must
manually compare source or generated files to understand what changed.

The experiment requires every observable success condition to pass. This
consumer-navigation and change-legibility failure makes the current evaluation
a negative product endpoint even though generation and all six automated tests
pass.

## Evaluation boundary

- Inputs: the two committed synthetic portable artifacts
- Generated output: ignored `_local/experiment/`
- Network, accounts, deployment, live participation, and real data: none
- Production-stack decision: out of scope
- Evaluation method: generate from source, inventory every output, traverse
  available human links, inspect the JSON relationship index, rerun the unit
  and repository checks, and compare observed behavior with each stated
  condition

## Observable success results

| # | condition | result | evidence |
|---:|---|---|---|
| 1 | Add a complete artifact using only its two portable source files | pass | `test_fixture_discovery_needs_no_hand_maintained_index` adds a copied third fixture without generator changes |
| 2 | One command generates three views and JSON deterministically | pass | The build command generated six HTML files plus `index.json`; repeated-tree equality is tested |
| 3 | A consumer can locate claims, citations, disagreements, and lineage without hidden state | **fail** | There is no generated `index.html`; the only root entry is agent-oriented JSON, and artifact pages are reachable only when their directory names are already known |
| 4 | Every view states ordering and exposes source pointers | pass | All six generated HTML views contain the ordering disclosure and portable source path; `index.json` exposes both globally and per artifact |
| 5 | An agent can recover equivalent relationships from JSON | pass | The parity test compares generated claims, disagreements, lineage, and lossless Markdown with loaded source |
| 6 | Re-running generation is byte-identical | pass | `test_generation_is_deterministic_and_preserves_sources` compares two complete output trees |
| 7 | Repository and experiment tests pass offline | pass | Six unit tests and repository validation pass without a network dependency |

Because condition 3 fails, the experiment does not satisfy its all-conditions
success rule.

## Central-question traversal

### Producer

The producer path works at the experimental boundary. Each artifact is a
portable Markdown/JSON pair, discovery is automatic, invalid relationships
fail closed, and generation preserves source bytes.

### Human consumer

The generated tree has no discoverable HTML starting point. Once a person is
given an artifact page directly, local navigation among its artifact, claims,
and versions views works. That success is conditional on knowledge outside the
product: the artifact directory and initial filename.

The version view says, for example, that version 2 supersedes
`synthetic-review-v1`, but the identifier is plain text. The view neither links
to the predecessor nor derives which stable claims, support relationships, or
disagreements changed. The fixture's prose happens to contain a revision note,
but that producer-authored note is not an independently inspectable
relationship view.

### Agent consumer

The JSON index is complete and lossless for the declared data. It exposes
source pointers, views, claims, citations, disagreements, and the direct
`supersedes` edge. An agent can recover the relationships, but must still
compute a version comparison itself. The current slice is therefore stronger
for an agent than for a person, contrary to the commitment that human use
remain clear and deliberately designed.

## Failure and reversal checks

The implementation does not require a hand-maintained index, treat display
labels as verified identity, hide missing support in the claim view, impose a
score, require generator changes for new valid artifacts, lose source
Markdown, or break deterministic offline generation.

Full deletion is not earned: the implementation is reversible, safe, and
provides a useful mechanical base. The negative evidence instead earns a
targeted revision before further stack or launch discussion.

## Earned reshape requirements

Lane 1 problem shaping should define the smallest revision that:

1. generates a deterministic human-readable corpus entrypoint;
2. makes every artifact reachable from that entrypoint without knowing an
   artifact ID or filesystem path;
3. turns valid predecessor relationships into navigable version links;
4. derives an explicit comparison over stable claim IDs, including added,
   removed, and text-changed claims plus changed support and disagreement
   relationships;
5. distinguishes producer-authored revision notes from generator-derived
   comparisons; and
6. adds behavioral checks that begin at the corpus entrypoint and answer
   "what changed?" without direct source inspection.

These requirements remain synthetic, local, framework-free, and reversible.
They do not select a production stack or authorize launch.

## Decision

Keep the current code as an evaluated baseline, mark the first experiment as
needing revision, and return next work to Lane 1. Implementation should not
extend the slice until problem shaping bounds the repair; Lane 1 validation
should reevaluate the
revised traversal rather than treating mechanical test success as product
success.
