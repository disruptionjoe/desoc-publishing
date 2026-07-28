# Phase 0 Question: Lineage Branches Without False Canonicality

Status: ready for Lane 1 implementation

Shaped: 2026-07-27

Evidence: `phase-0-independent-artifact-corpus-evaluation.md`

## Product question

When two or more portable artifacts declare the same immediate predecessor, can
a consumer discover every declared successor from generated output without the
product implying that one successor is canonical, preferred, or a replacement
for the others?

The current local baseline makes backward lineage visible: a successor links to
its declared predecessor. It does not make a fork visible from the predecessor
page. That leaves a consumer who starts at an earlier artifact unable to learn
that multiple declared continuations exist without prior directory knowledge.

## Bounded revision

The dependency-free generator must derive reverse lineage only from existing
`supersedes` declarations. Each artifact and versions view must show either no
declared successors, one linked declared successor, or multiple linked declared
successors listed by stable artifact ID. The branch list must say it is a
navigation aid, not a verdict about identity, authorship, priority, correctness,
adoption, merge, replacement, or quality; the generator does not select a
canonical branch.

The JSON index must expose the same declared-successor IDs and view paths. IDs
and links must sort lexically. A malformed corpus with a duplicate artifact ID
or unresolved `supersedes` target must continue to fail before output is written.

## Focused synthetic fixture

Add one valid synthetic artifact that declares `synthetic-review-v1` as its
immediate predecessor while remaining distinct from `synthetic-review-v2`. It
must preserve the portable manifest contract, synthetic/unverified disclosures,
and absence of a hand-maintained corpus index. It must not imply either
successor wins, merges, invalidates, or supersedes the other.

## Delivery boundary

Lane 1 implementation may change only the dependency-free generator, focused
tests, the one synthetic branch fixture, and product/evaluation records needed
to report the observed result. Generated output remains ignored under
`_local/experiment/`.

Do not change the manifest schema, add graph ranking, choose a production
stack, verify identities, accept live submissions, expose a network service,
or make a launch claim.

## Behavioral acceptance

1. `synthetic-review-v1` visibly links to both declared successors in stable
   lexical order with a non-canonical-branch disclosure.
2. Each successor links only to its own immediate predecessor; no comparison
   claims to compare sibling branches.
3. Artifacts with no successor visibly say so and render no false link.
4. JSON exposes the same successor IDs and artifact/versions paths as HTML.
5. Generation remains byte-identical, offline, source-preserving, and free of
   a hand-maintained corpus index.

Evaluation should traverse the fork from the predecessor and record whether a
consumer can discover declared plurality without a canonicality inference.
