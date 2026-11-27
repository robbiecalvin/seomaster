---
name: seo-regression-testing
description: Compare baseline and candidate URL snapshots for lost titles, new noindex and changed canonicals.
---
# Seo Regression Testing

## Inputs
Project scope, upstream release-gate findings, dated evidence and relevant URLs or records.

## Procedure
Compare baseline and candidate URL snapshots for lost titles, new noindex and changed canonicals.
Run `python offline.py regressions INPUT.json` with the contract in OFFLINE.md.

## Deliverable
Regression findings
Include evidence IDs, affected scope, priority, owner and acceptance test. Mark missing inputs unavailable.

## Acceptance
Verify findings against source records, distinguish estimates from measurements, and obtain approval before changes. Never promise rankings or fabricate results.
