# Phase 0 Question: Producer Structural Preflight Without Content Admission

Status: ready for Lane 1 implementation

Shaped: 2026-07-31

Evidence: `../evaluations/phase-0-consumer-orientation-walkthrough-evaluation.md`

## Product question

Can a producer preparing portable research artifacts identify every local
structural error in one offline pass without the product deciding whether an
artifact is publishable, correct, valuable, authored, or worthy of priority?

## Bounded revision

Add a dependency-free preflight command and library report. It must inspect
each discovered non-hidden artifact directory, retain valid results when other
directories fail, and list directories in stable lexical order. A valid entry
names its artifact ID; an invalid entry preserves the precise structural error.
The report must plainly limit itself to the portable experiment contract.

## Delivery boundary

This slice may change the local experiment loader, command, focused tests, and
the corresponding product/evaluation records. It must not modify the manifest
schema or fixture sources, rank or reject research, verify a person, establish
priority, select an application stack, accept a submission, or create a
network service.

## Behavioral acceptance

1. A mixed valid/invalid synthetic corpus returns one deterministic report.
2. Valid artifacts remain visible even when another directory needs correction.
3. The report identifies its structural-only and non-admission limit.
4. A malformed relationship remains a generator failure before output writes.
5. Preflight itself does not write output or mutate fixtures.
