# Status

Updated: 2026-07-24

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
- Offline experimental slice: mechanically verified; product revision required
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

The problem-shaping revision is now bounded in
`docs/product/phase-0-corpus-entry-and-version-comparison-revision.md`: add a
deterministic corpus entrypoint and derived immediate-predecessor comparison
without changing the portable source contract. Lane 1 may now implement that
ready, reversible slice and then reevaluate the generated traversal in its
validation phase.

The former shaping, delivery, and evaluation Lanes were consolidated on
2026-07-25 into phases of the same Lane 1 product lifecycle. Historical
receipts retain their original IDs.
Phase 0 remains active. The current implementation is an evaluated baseline,
not a production-stack choice or public launch.
