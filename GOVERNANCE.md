# Governance

Joe is the current constitutional governor. Agents are delegated broad
authority to research, design, build, test, evaluate, and improve the
repository within the Constitution.

## Decision classes

- **Constitutional:** reserved to Joe.
- **Canon:** durable product, architecture, or process rules. Agents may change
  these with evidence, a recorded decision, and migration or reversal notes.
- **Runtime:** current plans, queue state, experiments, and Lane state. Agents
  may update these through normal work.
- **Observation:** feedback, source notes, metrics, and hypotheses. These inform
  decisions but do not command them.

## Governance gates

Joe's explicit authorization is required before:

- people can use or edit a deployed application;
- the repository accepts live submissions or non-synthetic personal data;
- work creates consequences outside the repository and ordinary authorized
  application development;
- any constitutional authority is transferred.

Passing tests, completing Phase 0, or preparing a release packet does not cross
one of these gates. It returns a recommendation and evidence to Joe.

## Change discipline

Material canon decisions belong in `DECISIONS.md` or `docs/decisions/`.
Experiments must state the question, boundary, success and failure signals, and
reversal path. When product evidence conflicts with a preferred process or
feature, record the conflict and favor the product evidence unless the
Constitution says otherwise.

