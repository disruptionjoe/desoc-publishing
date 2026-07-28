# Status

Updated: 2026-07-27

## Current phase

**Phase 0 — product definition and local proving**

The public sovereign repository and founding operating system are established.
Agents may research, compare product hypotheses, select a smallest useful
experiment, scaffold a local application, and iterate with synthetic or
explicitly approved public fixtures.

## Current truth

- Repository: public and active
- Governance: Joe holds constitutional authority
- Automation: active through the existing `cai_directed` Repository Work Cycle
- Experimental harness: dependency-free Python and static local output selected
- Production application stack: not selected
- Offline experimental slice: evaluated baseline for an independent artifact, a two-version lineage, and one declared lineage fork
- Generated output: ignored under `_local/experiment/`
- Production application: not yet implemented
- User-facing launch: not authorized
- Live submissions or participant data: not authorized
- Production deployment: not authorized
- Decentralized backend: future option, not a requirement

## Verified local behavior and product evidence

The reversible first local experiment in
`docs/product/phase-0-first-local-experiment.md` now:

1. discovers strict synthetic Markdown and JSON artifact pairs without a
   hand-maintained index;
2. generates explainable artifact, claim/support, and version/disagreement
   views plus an equivalent JSON index;
3. exposes missing support, disagreements, source pointers, synthetic status,
   unverified identity and priority, and deterministic ordering;
4. preserves fixture bytes and produces byte-identical output on repeated
   runs; and
5. passes repository validation and six offline unit tests.

The first product-validation evaluation nevertheless found a product-level failure. The
generated tree has no human-readable corpus entrypoint, so a person must know
an artifact directory and filename before entering the product. Its version
view names a predecessor but does not link to it or derive which stable claims,
support relationships, or disagreements changed. Mechanical success therefore
does not yet establish a usable producer-to-consumer loop.

## Immediate objective

The corpus-entry and immediate-predecessor revision is an evaluated baseline:
the generated root `index.html` reaches both artifacts and their three local
views, while the v2 view derives its declared difference from v1. The evidence
is recorded in
`docs/evaluations/phase-0-corpus-entry-and-version-comparison-evaluation.md`.

The independent-artifact corpus question is now an evaluated baseline. The
generated entrypoint keeps source pointers, identity limits, lineage, and
deterministic navigation legible across one independent artifact and the
two-version lineage without a mandatory ranking or hidden source knowledge.
See `docs/evaluations/phase-0-independent-artifact-corpus-evaluation.md`.
The next bounded question is whether reverse lineage makes multiple declared
successors discoverable without implying a canonical branch. Its contract is
`docs/product/phase-0-lineage-branching-question.md`. It retains the portable
source contract, offline boundary, and absence of a production-stack decision.

That lineage-branching slice is now evaluated. A shared predecessor visibly
links to each lexically ordered declared successor, and the equivalent JSON
index exposes the same paths while disclaiming canonicality, preference,
replacement, or quality. The evidence is recorded in
`docs/evaluations/phase-0-lineage-branching-evaluation.md`. The next earned
question is whether a bounded consumer traversal can make that plurality
comprehensible without hidden corpus knowledge.

The former shaping, delivery, and evaluation Lanes were consolidated on
2026-07-25 into phases of the same Lane 1 product lifecycle. Historical
receipts retain their original IDs.
Phase 0 remains active. The current implementation is an evaluated baseline,
not a production-stack choice or public launch.
