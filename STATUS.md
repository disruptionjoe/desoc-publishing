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
- Offline experimental slice: implemented and locally verified
- Generated output: ignored under `_local/experiment/`
- Production application: not yet implemented
- User-facing launch: not authorized
- Live submissions or participant data: not authorized
- Production deployment: not authorized
- Decentralized backend: future option, not a requirement

## Verified local behavior

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
5. passes repository validation and five offline unit tests.

## Immediate objective

Evaluate the generated behavior in Lane 3 against the experiment's observable
success and failure conditions. Phase 0 remains active. This implementation is
an experimental harness, not a production-stack choice or public launch.
