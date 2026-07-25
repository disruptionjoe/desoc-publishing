# Phase 0 Revision: Corpus Entry and Version Comparison

Status: ready for Lane 2 local delivery

Shaped: 2026-07-25

Evidence: `../evaluations/phase-0-first-local-experiment-evaluation.md`

## Product question

Starting from generated local output alone, can a person locate every
synthetic artifact and inspect exactly how a version differs from its direct
predecessor without treating producer prose, identity, or priority as verified
truth?

This is a bounded revision to the existing offline experiment. It neither
changes the portable producer contract nor selects a production stack,
identity system, ranking, admission rule, network service, or launch.

## Consumer traversal

The generator must write `index.html` at the output root. It is the single
human corpus entrypoint and links to every discovered artifact's `artifact.html`.
Each entry shows only declared, inspectable fields: title, artifact ID,
producer display, declared time, version, and links to the artifact, claims,
and versions views. It also displays the synthetic/unverified notice, the
deterministic ordering rule, and the portable source pointer for each entry.

Entries sort by stable artifact ID. This order is deterministic navigation,
not an endorsement, quality ranking, priority proof, or admission decision.
The JSON index remains agent-legible and must expose `index.html` plus the
same per-artifact view paths; it need not duplicate rendered HTML.

Every artifact page keeps its local three-view navigation and adds a visible
link back to the corpus entrypoint. When `supersedes` is non-null, the artifact
and versions pages link to the predecessor's generated artifact and versions
views. A first version instead says that no predecessor is declared. The
generator continues to reject an unresolved predecessor rather than emitting a
broken link.

## Derived comparison contract

The versions view compares an artifact only with its declared immediate
predecessor. It must label the comparison as generator-derived and separate it
from any producer-authored Markdown revision note. No inferred intent,
quality, correctness, or priority conclusion is permitted.

For stable claim IDs, derive and show these ordered sets:

| category | exact rule |
|---|---|
| added claims | ID exists only in the current manifest |
| removed claims | ID exists only in the predecessor manifest |
| text-changed claims | ID exists in both and its `text` differs byte-for-byte |
| unchanged claims | ID exists in both and its `text` is identical |
| support changes | for each shared claim ID, report citation IDs added to and removed from `citation_ids`; an empty pair is not rendered as a change |
| disagreement changes | for each shared claim ID, compare declared disagreement relationships targeting that claim by `disagreement_id`; report added and removed IDs, and report a changed ID when its `position`, `rationale`, or citation-ID set differs |

For a claim added or removed with the version, show its complete declared
support and target disagreements under that claim's category rather than
pretending a paired relationship exists. Sort claim IDs and disagreement IDs
lexically. Within every displayed citation-ID set, sort lexically. Explain
these rules beside the comparison so a reader can reproduce the view from the
two portable manifests.

The existing fixtures must demonstrate at least one text change, a support
change, and a disagreement added or removed/changed. A focused test fixture may
be added only if the current pair cannot cover one required category; it must
remain a valid synthetic two-file artifact and must not become a hand-maintained
corpus index.

## Delivery boundary

Lane 2 may change only the dependency-free generator, its focused tests, and
the existing synthetic fixtures when needed to exercise the contract. Generated
output stays ignored under `_local/experiment/`. Preserve byte-identical
generation, source preservation, symlink safety, exact manifest validation,
and the absence of network calls or third-party dependencies.

Do not alter the artifact manifest schema merely to encode derived comparison
state; the comparison is calculated from existing declared relationships. Do
not add scores, quality thresholds, identity verification, public submission,
or external services.

## Behavioral acceptance

The Lane 2 change is ready for Lane 3 evaluation only when automated checks
prove all of the following:

1. Root `index.html` is generated deterministically and links to both current
   synthetic artifacts without prior directory knowledge.
2. A corpus-entry traversal reaches each artifact's three local views and each
   view returns to the entrypoint.
3. A declared predecessor renders as links to the predecessor artifact and
   versions views; a first version renders no false predecessor link.
4. The current `synthetic-review-v2` comparison visibly identifies the
   `claim-trust` text and support changes and the changed/additional
   disagreement relationship for `claim-access`.
5. The comparison labels itself as derived, exposes its ordering/matching
   rules, and does not substitute the producer's Markdown revision note for
   derived output.
6. JSON still provides equivalent source pointers, lineage, views, and
   declared relationships; the build remains byte-identical and offline.

Lane 3 should traverse from `index.html`, answer what changed using generated
output alone, and reevaluate every original observable success condition. It
must record any mismatch between the specified comparison and actual rendered
behavior rather than treating passing mechanics as product success.
