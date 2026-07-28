# Phase 0 Question: Traversing a Declared Fork

Status: ready for Lane 1 implementation

Evidence: `phase-0-lineage-branching-evaluation.md`

## Product question

Can a consumer who starts at one declared successor learn about other declared
continuations of the same immediate predecessor without hidden corpus knowledge
or an implication that any sibling is better, canonical, merged, or adopted?

## Bounded revision

For an artifact with a declared predecessor, derive its sibling continuations
from that predecessor's existing reverse lineage. Render the context on the
artifact and versions views, and export equivalent predecessor and sibling IDs
in JSON. When no sibling exists, do not manufacture a relationship.

## Delivery boundary

Use only the existing synthetic fixtures and `supersedes` declarations. Do not
add ranking, graph scoring, identity verification, a production stack, network
behavior, live submissions, or launch behavior.

## Behavioral acceptance

1. Each fork successor identifies its shared declared predecessor and links to
   the other declared successor.
2. The context explicitly disclaims comparison, ranking, and selection.
3. JSON preserves the same predecessor and sibling IDs.
4. The output remains deterministic and source-preserving.
