# Offline runner
Run `python offline.py METHOD input.json`. Envelope: `{"evidence":[...foundation evidence records...],"data":...}`. Evidence applies to the supplied dataset; record-level provenance must be reviewed manually.

| Method | data shape |
|---|---|
| keywords / markets | array of keyword, market, language, optional numeric volume |
| intent | query string |
| competitors | own_keywords array; competitors array of records with keywords array |
| serp | array of domain and type records from one SERP |
| changes | before_scope, after_scope (equal); before and after arrays of id and numeric or null value |
| gaps | own and competitor arrays of keyword records |
| score | demand, difficulty, relevance, commercial, weakness, effort (0–10) |

Missing coverage is not proof of absence. Use comparable market, device, date and provider scopes. No live retrieval or automatic implementation.

## Technical methods
| Method | data shape |
|---|---|
| audit, indexability, schema, canonical, mobile | url, html, optional status and x_robots_tag |
| graph | array of url and html records |
| performance | lcp_ms, inp_ms, cls (numeric or null); use comparable field p75 data |
| rendering | url, before_html, after_html |
| sitemap | XML string |
| redirects | object mapping source URL to target URL |
| hreflang | array of url and alternates (language-to-URL object) |
| migration | old and new URL arrays, mapping object |

These are snapshot checks, not a live crawler, browser renderer, schema eligibility validator, security scanner or proof of indexing. Graph coverage is limited to supplied pages. Review robots.txt, HTTP headers, rendering, accessibility, redirect status codes and search engine reports separately.

## Section 4
Synthetic input examples (wrap each in the existing evidence/data envelope). Results are candidate findings, not live measurements.

- `coverage`: `{"required": ["a", "b"], "covered": ["a"]}` → `["b"]`

- `metadata`: `[{"url": "a", "title": "X"}, {"url": "b", "title": "x"}]` → `[{"url": "a", "missing": ["description"], "duplicate_title": true}, {"url": "b", "missing": ["description"], "duplicate_title": true}]`

- `cannibalization`: `[{"keyword": "x", "market": "CA", "language": "en", "url": "a"}, {"keyword": "x", "market": "CA", "language": "en", "url": "b"}]` → `[{"keyword": "x", "market": "CA", "language": "en", "urls": ["a", "b"]}]`

- `refresh`: `[{"url": "a", "current": 1, "previous": 0}]` → `[{"url": "a", "change": null}]`

## Section 5
Synthetic input examples (wrap each in the existing evidence/data envelope). Results are candidate findings, not live measurements.

- `visibility`: `[{"engine": "test", "mentioned": true, "cited": false}]` → `{"test": {"samples": 1, "mention_rate": 1.0, "citation_rate": 0.0}}`

- `claim_sources`: `[{"id": "a", "source_ids": []}]` → `["a"]`

- `graph_references`: `{"entities": ["a"], "triples": [{"subject": "a", "object": "b"}]}` → `[{"subject": "a", "object": "b"}]`

## Section 6
Synthetic input examples (wrap each in the existing evidence/data envelope). Results are candidate findings, not live measurements.

- `backlinks`: `[{"source": "https://a.test/x", "target": "b"}, {"source": "https://a.test/y", "target": "b"}]` → `{"unique_hosts": 1, "target_hosts": {"b": 1}}`

- `listings`: `{"canonical": {"name": "A"}, "listings": [{"source": "x", "name": "B"}]}` → `[{"source": "x", "differences": ["name"]}]`

- `prospects`: `[{"url": "a", "editorial_relevance": true, "paid_link": true, "spam": false}]` → `[]`

## Section 7
`catalog_checks`: array of url, title, optional item_count. `media_checks`: array of url, type (image/video), optional decorative, alt, transcript. These are limited snapshot checks, not indexability or accessibility certification.

## Section 8
`metrics`: array of clicks, impressions, sessions, conversions (nonnegative numbers). `compare_metrics`: baseline and current arrays of same scope and duration; relative changes are fractions, null for undefined. `forecast`: array of name, sessions, conversion_rate (0–1), value_per_conversion; scenario only. Do not combine incompatible segments or currencies.

## Section 9
`regressions`: baseline and candidate arrays of url, title, noindex (boolean), canonical. `release_checks`: checks array with id, status, evidence_ids; required IDs technical, content, evidence, regression, approval. A passing checklist is not deployment authorization; evidence references require independent review.
