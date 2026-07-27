# Phase 0 Question: Independent Artifact Corpus Navigation

Status: ready for Lane 1 implementation

Shaped: 2026-07-27

Evidence: `phase-0-corpus-entry-and-version-comparison-revision.md`; `../evaluations/phase-0-corpus-entry-and-version-comparison-evaluation.md`

## Product question

Starting from generated local output alone, can a consumer distinguish one
independent synthetic artifact from a version lineage, inspect each artifact's
declared provenance and relationships, and navigate the whole corpus without
treating deterministic navigation as a mandatory ranking?

The evaluated baseline contains only `synthetic-review-v1` and its successor
`synthetic-review-v2`. It proves corpus entry and immediate-predecessor
comparison, but not whether the entrypoint stays comprehensible when a
separate research artifact has no lineage relationship with that pair.

## Smallest slice

Add exactly one valid, independent synthetic artifact directory with the
existing portable `artifact.json` and `artifact.md` contract. It must declare
`supersedes: null` and use distinct artifact, claim, citation, and disagreement
IDs. Do not change the manifest schema, introduce a hand-maintained corpus
index, or add producer identity, priority, quality, admission, or ranking
state.

The existing generator must discover the new directory and include it in both
`index.html` and `index.json` under the current stable-artifact-ID ordering.
The corpus entrypoint must make clear that this is deterministic navigation,
not an endorsement or relevance ranking. The independent artifact's local
views must say that no predecessor is declared; no view may infer or display a
version relationship to either synthetic-review artifact.

## Behavioral acceptance

Lane 1 implementation is ready for validation when focused tests and a
generated traversal prove all of the following:

1. Adding the independent artifact requires editing only its two portable
   source files; no generator or index edit is needed.
2. Root `index.html` and `index.json` list all three artifacts in stable ID
   order and retain their synthetic/unverified and non-ranking disclosures.
3. A consumer can enter each artifact from the root, reach its local views,
   and return to the corpus entrypoint without knowing a directory name.
4. The v2-to-v1 comparison remains immediate-predecessor-only, while the
   independent artifact visibly declares no predecessor and exposes no false
   lineage link.
5. The generated JSON preserves equivalent source pointers, declared claims,
   citations, disagreements, and lineage for all three artifacts.
6. Generation remains byte-identical, source-preserving, symlink-safe, and
   offline; repository validation and focused tests pass.

## Delivery boundary

Lane 1 may change only the committed synthetic fixture pair, focused tests,
and the dependency-free generator if a real contract gap is found. Generated
output remains ignored under `_local/experiment/`. No production stack,
service, network request, live submission, account, identity verification,
reputation, payment, token, moderation, or deployment is in scope.

## Evaluation and disposition

Validation must start from generated `index.html` and inspect `index.json`;
it must record whether an unrelated artifact is legible as independent rather
than merely reachable. Passing mechanics are not evidence of real producer or
consumer usefulness. Keep, revise, revert, or reshape the slice from that
record without inferring a launch path.
