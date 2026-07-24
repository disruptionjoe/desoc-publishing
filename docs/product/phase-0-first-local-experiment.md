# Phase 0 first local experiment

Status: ready for local implementation

Selected: 2026-07-23

Boundary: synthetic fixtures only; no service launch or external action

## Decision

Build a dependency-free local reference generator that turns one portable
research artifact into three explainable consumer views:

1. the artifact as published;
2. a claim-and-support view; and
3. a version-and-disagreement view.

The experiment uses a Markdown body plus a JSON manifest, writes static local
HTML and a machine-readable JSON index, and operates only on committed
synthetic fixtures. It tests the smallest end-to-end product question:

> Can one producer publish a portable research artifact, and can a person or
> agent understand what it claims, what supports or contests it, and what
> changed, without an institutional admission gate or one mandatory ranking?

This is an experimental harness choice, not a production architecture,
identity system, priority proof, public launch, or decentralized-backend
decision.

## Approaches compared

| approach | useful evidence | main cost | disposition |
|---|---|---|---|
| Portable files plus static local views | Tests the producer/consumer loop, export, provenance, and plural views with minimal machinery | Omits multi-user and network behavior | Selected |
| Local database and web application | Tests richer interaction and queries | Commits early to application structure before the core artifact is proven | Defer |
| Content-addressed or decentralized prototype | Tests durability and location-independent retrieval | Adds identity, networking, and persistence assumptions unrelated to the first product question | Defer |

The selected approach is cheapest to reverse and exposes the data contract
before framework choices can hide it.

## Producer artifact

Each fixture is one directory:

```text
fixtures/<artifact-id>/
  artifact.json
  artifact.md
```

`artifact.json` contains:

- `schema_version`
- `artifact_id`
- `title`
- `producer_display` — an unverified display label, including a pseudonym
- `created_at` — a declared timestamp, not independently proven priority
- `version`
- `supersedes` — zero or one prior artifact version
- `claims` — stable IDs, concise claim text, and local citation IDs
- `citations` — IDs plus inspectable citation text or synthetic locator
- `disagreements` — target claim ID, position, rationale, and citation IDs

`artifact.md` contains the human-readable research body. The generator must
preserve the source files unchanged and treat the manifest as producer-supplied
claims, not verified truth.

## Consumer views

### Artifact view

Show the title, producer display, declared time, version lineage, Markdown
body, citations, and a plain statement that the fixture is synthetic and its
identity and priority are unverified.

### Claim-and-support view

List each stable claim with its cited support and contesting disagreements.
Do not collapse these into a score or admission verdict. Missing support is
visible as missing support.

### Version-and-disagreement view

Show what the current version supersedes and group disagreements by target
claim. Explain every ordering rule next to the view. Initial ordering is stable
artifact ID then claim ID; it is deterministic, not a quality ranking.

The generated JSON index must expose the same information so an agent can
inspect it without parsing HTML.

## Observable success

The experiment succeeds only when automated checks show all of the following:

1. A producer can add the complete synthetic artifact by editing only its two
   portable source files.
2. One command deterministically generates the three local views and JSON
   index from a clean checkout.
3. A consumer can locate the artifact's claims, citations, disagreements, and
   version lineage without consulting hidden state.
4. Every view states its ordering rule and exposes source pointers.
5. An agent can recover the same claim, citation, disagreement, and version
   relationships from the generated JSON.
6. Re-running the generator produces byte-identical output.
7. Repository and experiment tests pass without network access.

## Failure and reversal

Stop or return the slice to Lane 1 if any of these occur:

- generation requires hand-editing an index;
- the data model silently treats a display label as verified identity;
- a view hides unsupported or contesting evidence;
- one score becomes the required consumer view;
- adding an artifact requires changing generator code;
- Markdown or manifest content cannot be exported losslessly;
- deterministic offline generation cannot be achieved.

Reversal is deletion of the unshipped experimental implementation and
generated `_local/` output while retaining this packet and its negative
evidence. No migration or external rollback is required because no service,
account, or live data exists.

## Data and safety boundary

- Use committed synthetic fixtures only.
- No personal, participant, client, private, credential, or regulated data.
- No network calls, submissions, authentication, pseudonym verification,
  reputation, incentives, payments, tokens, moderation, or deployment.
- Suspected manipulation may appear only as explicit synthetic disagreement
  data; it never triggers removal.
- Generated output stays under `_local/` and is not committed.

## Implementation boundary

Use Python 3 standard-library code and plain HTML/CSS. Do not select a
production framework. The first implementation should add only:

```text
fixtures/
scripts/build_local_experiment.py
src/
tests/
```

The required local verification commands are:

```bash
python3 scripts/validate_repository.py
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/build_local_experiment.py --fixtures fixtures --output _local/experiment
git diff --check
```

Lane 2 owns implementation. Lane 3 must evaluate actual generated behavior
against the success and failure conditions above before any production-stack
or launch recommendation.
