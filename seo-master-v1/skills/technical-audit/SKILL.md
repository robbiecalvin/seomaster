---
name: technical-audit
description: Inspect HTML title, description, headings and index directives.
---
# technical-audit

Inspect HTML title, description, headings and index directives.

## Workflow
1. Inspect project scope, market, and existing evidence.
2. Collect the inputs described in the offline runner documentation. Preserve source, date and scope; validate evidence using the foundation validator.
3. Run `audit` through the offline runner. Treat outputs as candidates, not verified live findings.
4. Review each finding against original evidence; document missing data and confidence.
5. Produce prioritized recommendations with affected URLs or keyword IDs, evidence references and acceptance tests.
6. Obtain approval before changing production.

## Acceptance
Reproducible input and output, no invented metrics, explicit limitations, no unauthorized changes.
