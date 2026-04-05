# Wiki Log

Append-only chronological record of all operations. Never delete or edit past entries.

Each entry header format: `## [YYYY-MM-DD] <operation> | <title>`

Grep the last 5 entries: `grep "^## \[" wiki/log.md | tail -5`

---

## [2026-04-05] edit | Initial wiki created

- Wiki initialized with empty index and log.
- Schema defined in `AGENTS.md`.

## [2026-04-05] ingest | sv-pro/agent-hypervisor — Full Repository Ingest (Session 2)

### Sources ingested
- `raw/agent-hypervisor/CHANGELOG.md` — version history v0.1–v0.4
- `raw/agent-hypervisor/CLAUDE.md` — developer guide, four-layer architecture, conventions
- `raw/agent-hypervisor/CONTRIBUTING.md` — contribution guide, design principles
- `raw/agent-hypervisor/STATUS.md` — component maturity model and classification table
- `raw/agent-hypervisor/scenarios/zombie-agent/SCENARIO.md` — ZombieAgent attack scenario
- `raw/agent-hypervisor/docs/concept/overview.md`, `concepts.md`, `faq.md` — core concepts and FAQ
- `raw/agent-hypervisor/docs/research/vs-existing-solutions.md`, `vulnerability-case-studies.md`, `workarounds.md`, `timeline.md`, `references.md`, `case_studies/MS_COPILOT_DLP_BYPASS.md`
- `raw/agent-hypervisor/docs/architecture/threat-model.md`, `execution_governance.md`, `provenance_model.md`
- `raw/agent-hypervisor/docs/positioning/crutch_workaround_bridge.md`, `security_comparison.md`
- `raw/agent-hypervisor/docs/adr/ADR-001` through `ADR-006`
- `raw/agent-hypervisor/docs/pub/the-missing-layer/00-series-overview.md` and articles 01–04
- `raw/agent-hypervisor/research/benchmarks/agentdojo/results.md`, `methodology.md`
- `raw/agent-hypervisor/research/benchmarks/reports/report-v1.md`
- `raw/agent-hypervisor/research/agentdojo-bench/README.md`

### Source pages created
- [[src-agent-hypervisor-changelog]]
- [[src-agent-hypervisor-claude]]
- [[src-agent-hypervisor-contributing]]
- [[src-agent-hypervisor-status]]
- [[src-agent-hypervisor-zombie-agent-scenario]]
- [[src-agent-hypervisor-docs-concept]]
- [[src-agent-hypervisor-docs-research]]
- [[src-agent-hypervisor-docs-architecture]]
- [[src-agent-hypervisor-docs-adr]]
- [[src-agent-hypervisor-pub-missing-layer]]
- [[src-agent-hypervisor-benchmarks]]
- [[src-agent-hypervisor-docs-positioning]]

### Entity pages created
- [[agent-hypervisor]] — main entity page; what it is, current version (0.4), status, key links
- [[camel-defense]] — Google DeepMind CaMeL, 2025; dual-LLM defense; comparison with AH

### Concept pages created
- [[world-manifest]] — formal spec of the agent's universe; constitution metaphor; compilation pipeline
- [[ai-aikido]] — stochastic design-time → deterministic runtime; the central technique
- [[taint-propagation]] — ValueRef model, TaintContainmentLaw, overtainting/undertainting, cross-session taint
- [[four-layer-architecture]] — L0 Execution Physics, L1 Base Ontology, L2 Dynamic Ontology, L3 Execution Governance
- [[design-time-hitl]] — amortizing human judgment; O(n) vs O(log n) economics; four-phase cycle
- [[manifest-resolution]] — ALLOW / DENY / ASK; three execution modes; enforcement invariants
- [[zombie-agent]] — ZombieAgent attack; 90% data leakage; three AH boundaries that break it
- [[crutch-workaround-bridge]] — evaluation framework; Crutch/Workaround/Bridge definitions; permission vs ontological security
- [[agentdojo-benchmark]] — benchmark design; 0% ASR / 80% utility results; CaMeL comparison

### Pages updated
- [[index]] — fully populated with all pages from session 1 and session 2

### Key takeaways
- AH achieves 0% ASR with 80% utility on 560 AgentDojo pairs (post-refactor, preliminary)
- The ZombieAgent scenario demonstrates cross-session taint propagation as a structural defense
- The Crutch/Workaround/Bridge framework positions AH as a Bridge toward ontological security
- "The Missing Layer" article series (articles 01–04 published) provides the public argument
- ADR-005 (Program Layer) is Accepted; ADR-001–004, ADR-006 are Open
- Core runtime components (IRBuilder, TaintContext, SafeMCPProxy, Executor) are ✅ Canonical
