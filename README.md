# SEO Master — v1.0.0-rc.1
Python 3.10+, standard library only. No network calls, deployment or credentials required.

Run `python -m unittest discover -s tests -v`, then `python seo_master.py plan examples/project.json` from this directory. To register a future skill, add its manifest to registry.json and its instructions under skills/. Plans are deterministic and never execute skills. Copy skills/seo-master into your Codex skills directory or explicitly instruct Codex to read it alongside this repository. The competitor kit is retained as a reference framework, not an automated integration.

## Workflow
Discover project → select applicable skills → resolve dependencies → collect evidence → approve recommendations → implement → verify → monitor. This release implements selection, dependency ordering and basic evidence validation only. Future skills are marked planned and blocked from execution. No live SEO research has been performed.

## Section 02
Offline research commands: see OFFLINE.md. Original competitor kit remains in competitor-reference.zip. Skills are manual Codex workflows with offline helpers, not autonomous agents.

## Section 03
Technical snapshot analysis is available through offline.py. See OFFLINE.md for input contracts and limitations. No network requests or production writes.

## Section 4
13 specialist workflows; 4 offline helpers. Other skills require manual review. See OFFLINE.md.

## Section 5
8 specialist workflows; 3 offline helpers. Other skills require manual review. See OFFLINE.md.

## Section 6
7 specialist workflows; 3 offline helpers. Other skills require manual review. See OFFLINE.md.

## Section 7
See OFFLINE.md for new contracts; no live execution.

## Section 8
See OFFLINE.md for new contracts; no live execution.

## Section 9
See OFFLINE.md for new contracts; no live execution.

## Sections 10–11
See INTEGRATIONS.md for opt-in provider adapters. Launch the local single-user dashboard with `python dashboard.py`, then open http://127.0.0.1:8765. Projects and offline analysis history are stored in workspace.sqlite. Use OFFLINE.md for method-specific JSON inputs. Export produces project, plan and run history JSON. Do not expose the local server to a network; it has no multi-user authentication. Provider calls are not wired into the dashboard.

## Section 12 — Release candidate
Install `requirements.txt` before launching the dashboard or running the full suite. Earlier offline CLI commands remain standard-library only. See RELEASE.md for installation, backup, security boundaries and outstanding production gates. Project and evidence schemas are enforced in the workspace. The local installer copies skill definitions without overwriting existing folders. This is a local release candidate, not a production-hosted service.

## Latest update
See PHASES_02_04.md for the combined research release and setup.

## Phases 05–07
See [PHASES_05_07.md](PHASES_05_07.md) for new workspaces.

## Phases 08–09
See [integration and execution guide](PHASES_08_09.md).

See [Phases 10–12](PHASES_10_12.md) for architecture, implementation and export workflows.
