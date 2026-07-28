# Phase 0 Evaluation: Declared Lineage Branching

Evaluated: 2026-07-28

## Question

Can a consumer beginning at a declared predecessor discover every declared
successor without the local product implying that any continuation is canonical,
preferred, correct, adopted, merged, or a replacement?

## Observed result

The dependency-free generator now derives reverse lineage solely from each
fixture's existing `supersedes` declaration. `synthetic-review-v1` exposes the
lexically ordered successors `synthetic-review-branch-a` and
`synthetic-review-v2` on its artifact and versions views. The generated JSON
exports the identical successor IDs plus artifact and versions paths.

The branch fixture shares only `synthetic-review-v1` as its immediate
predecessor. It makes no claim that either sibling defeats, invalidates, merges
with, or outranks the other. Artifacts without successors visibly say so.

## Checks

| Check | Result | Evidence |
| --- | --- | --- |
| Predecessor exposes both branches in lexical order | pass | Focused successor-navigation test |
| Navigation rejects a canonicality inference | pass | Required disclosure in artifact and versions views |
| Successors retain only their immediate predecessor | pass | Existing predecessor-link and comparison tests |
| JSON has HTML-equivalent successor paths | pass | `declared_successors` assertion |
| Output stays deterministic and source-preserving | pass | Determinism test |

## Boundary

This is offline synthetic product evidence. It does not establish human value,
identity, authorship, priority, ranking, adoption, a production stack, live
submission, or launch readiness.

## Next earned state

Use a bounded traversal evaluation to determine whether the declared plurality
is comprehensible to a consumer without hidden corpus knowledge. Do not add
ranking, graph scoring, identity verification, or network behavior.
