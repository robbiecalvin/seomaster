---
name: seo-documentation-manager
description: Maintain evidence-linked decisions and verify required release checks.
---
# Seo Documentation Manager

## Inputs
Project scope, upstream release-gate findings, dated evidence and relevant URLs or records.

## Procedure
Maintain evidence-linked decisions and verify required release checks.
Run `python offline.py release_checks INPUT.json` with the contract in OFFLINE.md.

## Deliverable
Release checklist
Include evidence IDs, affected scope, priority, owner and acceptance test. Mark missing inputs unavailable.

## Acceptance
Verify findings against source records, distinguish estimates from measurements, and obtain approval before changes. Never promise rankings or fabricate results.
