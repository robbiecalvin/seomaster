# SEO Master 2.0 — Phase 01

Local-first interface upgrade based on 1.0 RC1. Extract into a new folder. Stop the old server (Ctrl+C). In the new seo-master folder run:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python dashboard.py
```

Open http://127.0.0.1:8765. Choose New project, complete the three steps, then review the research plan. Analysis studio supports five form-based offline analyses. Supply actual evidence; no live discovery is performed. Other methods remain available via the existing CLI. Reports export JSON for machine use, not manual editing.

To retain old projects, stop both servers and copy the old workspace.sqlite into the new folder (back up both first), or start with `python dashboard.py --db /absolute/path/to/old/workspace.sqlite`. No database schema migration is needed. Do not expose this local server publicly.

This phase does not implement automatic research, full visual editors, live providers, or autonomous skill execution. Browser interaction has not been end-to-end tested; backend HTTP and JavaScript syntax checks are included in verification.
