# Evaluation: Corpus Entry and Version Comparison

Status: complete

Evaluated: 2026-07-26

## Boundary and method

Generated the committed synthetic fixtures locally, began at the generated
`index.html`, traversed each artifact's artifact/claims/versions views, then
checked the JSON index and the immediate-predecessor comparison. No network,
accounts, live data, deployment, or human participants were used.

## Result

The entrypoint lists both artifacts deterministically and reaches all three
views without filesystem knowledge. The v2 versions view links to v1 and
derives added, removed, changed, and unchanged stable claim IDs, plus support
and disagreement deltas. The generated notices preserve that these are
synthetic fixtures and that ordering is not a quality ranking.

The seven focused tests and repository validation pass. This is evidence that
the bounded offline navigation revision satisfies its stated synthetic
traversal conditions; it is not evidence of product usefulness with real
producers or consumers, and it does not authorize a stack, deployment, or
participation.

## Disposition

Lane 1's current local corpus slice is accepted as an evaluated baseline.
The next product question requires separately authorized human-use evidence or
another bounded synthetic product question; do not infer a launch path.
