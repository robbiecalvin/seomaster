---
name: knowledge-graph
description: Knowledge graph engineering for SEO research and implementation planning.
---
# Knowledge graph engineering

## Method
Validate entity references in supplied triples; review relationship accuracy.

1. Read project scope, market, language and relevant upstream evidence.
2. Record source, collection date, classification and confidence for each observation.
3. Run `python offline.py graph_references INPUT.json` using the contract in OFFLINE.md.
4. Produce findings with affected URLs or entities, evidence IDs, priority, proposed action and acceptance test. Mark missing evidence unavailable.
5. Obtain approval before production changes or outreach.

## Acceptance
Each recommendation is traceable, reproducible where possible, and reviewed for search policy compliance. No invented metrics or guaranteed rankings.
