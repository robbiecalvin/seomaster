# SEO Master 2.0 — phases 02–04 initial combined release

Run `python dashboard.py` after installing requirements. Existing workspace.sqlite is compatible; stop servers and back up the database before copying it.

## Competitor research
Set `BRAVE_SEARCH_API_KEY` in your shell before starting the server. Use the Competitor research page, enter a relevant search query and authorize the request. Search results are candidate domains, not verified competitors or Google rankings. Provider charges may apply. No live provider verification has been performed.

## Website crawler
Enter a public HTTPS URL and select 1–10 pages. The crawler checks robots.txt, follows same-origin links without query strings, pins validated public IPs, verifies TLS and reports redirects without following them. It inspects static HTML only. No JavaScript rendering, sitemap discovery, redirect traversal or confirmed indexing. Requests are synchronous; the local interface may wait during a crawl. Do not expose the server publicly. Crawl-delay can lengthen a run. Network behavior has only been tested using fixtures.

## Keyword intelligence
Enter keywords or upload a CSV with headers `keyword,volume,difficulty`. Supply market, language and source. Missing metrics remain unavailable; intent is heuristic. Imports append snapshots; duplicate keywords within an import are collapsed. Filter saved rows and download CSV. No live keyword volume API or editing/deletion workflow yet.

## Verification
Run `python -m unittest discover -s tests -v`. The five new tests exercise fixture-based discovery, crawl behavior, URL restrictions and keyword parsing. Browser interaction and live network tests remain pending.
