# Wiki Index

Master catalog of all pages in this wiki. Updated by the LLM on every ingest.

---

## Sources

### sv-pro/agent-hypervisor — Root Sources
- [[src-agent-hypervisor-readme]] — Entry point and navigation guide for the repository. (2026-04-05)
- [[src-agent-hypervisor-whitepaper]] — Full architectural thesis: the five-layer virtualization model and formal guarantees. (2026-04-05)
- [[src-agent-hypervisor-glossary]] — Authoritative term definitions for all AH concepts. (2026-04-05)
- [[src-agent-hypervisor-roadmap]] — Development stages and versioned plans. (2026-04-05)
- [[src-agent-hypervisor-changelog]] — Version history v0.1 (concept) through v0.4 (auditable execution governance). (2026-04-05)
- [[src-agent-hypervisor-claude]] — Developer guide: repo structure, four layers, dev setup, key conventions. (2026-04-05)
- [[src-agent-hypervisor-contributing]] — Contribution guide: what's welcome, design principles. (2026-04-05)
- [[src-agent-hypervisor-status]] — Component maturity model and classification table. (2026-04-05)

### sv-pro/agent-hypervisor — Scenarios
- [[src-agent-hypervisor-zombie-agent-scenario]] — ZombieAgent attack and how AH breaks it at three independent boundaries. (2026-04-05)

### sv-pro/agent-hypervisor — Concept Docs
- [[src-agent-hypervisor-docs-concept]] — Overview, core concepts, and FAQ objection-handling. (2026-04-05)

### sv-pro/agent-hypervisor — Research Docs
- [[src-agent-hypervisor-docs-research]] — vs. existing solutions, vulnerability case studies, workarounds, MS Copilot DLP case study. (2026-04-05)

### sv-pro/agent-hypervisor — Architecture Docs
- [[src-agent-hypervisor-docs-architecture]] — Threat model, execution governance, provenance model, technical spec. (2026-04-05)

### sv-pro/agent-hypervisor — Positioning Docs
- [[src-agent-hypervisor-docs-positioning]] — Crutch/Workaround/Bridge framework and security comparison table. (2026-04-05)

### sv-pro/agent-hypervisor — Architecture Decision Records
- [[src-agent-hypervisor-docs-adr]] — All six ADRs: schema versioning, simulation fidelity, policy IR, policy language, program layer, economic constraints. (2026-04-05)

### sv-pro/agent-hypervisor — Publications
- [[src-agent-hypervisor-pub-missing-layer]] — "The Missing Layer" article series (articles 01–04). (2026-04-05)

### sv-pro/agent-hypervisor — Benchmarks
- [[src-agent-hypervisor-benchmarks]] — AgentDojo benchmark: 0% ASR, 80% utility across 560 pairs. (2026-04-05)

---

## Entities

- [[agent-hypervisor]] — Deterministic execution governance layer for AI agents; enforces semantic-level isolation through ontological boundaries.
- [[camel-defense]] — CaMeL (Google DeepMind, 2025): dual-LLM capability-based defense; closest prior work to AH.

---

## Concepts

- [[world-manifest]] — Formal specification of an AI agent's universe: actions, trust channels, capabilities, taint rules, budgets.
- [[four-layer-architecture]] — The four deterministic layers: Execution Physics (L0), Base Ontology (L1), Dynamic Ontology (L2), Execution Governance (L3).
- [[ai-aikido]] — Using LLM stochastically at design-time to generate deterministic runtime artifacts.
- [[taint-propagation]] — How data contamination spreads through derivation chains; the TaintContainmentLaw.
- [[manifest-resolution]] — The deterministic ALLOW / DENY / ASK decision rule evaluated at runtime.
- [[design-time-hitl]] — Design-time Human-in-the-Loop: amortizing human judgment across all runtime decisions.
- [[zombie-agent]] — The ZombieAgent attack (Radware, Jan 2026): persistent memory poisoning, cross-session taint, 90% data leakage.
- [[crutch-workaround-bridge]] — Evaluation framework: Crutch (band-aid), Workaround (functional bypass), Bridge (architectural solution).
- [[agentdojo-benchmark]] — AgentDojo adversarial benchmark: what it tests, AH results (0% ASR, 80% utility), methodology.

---

## Comparisons

*(none yet)*

---

## Syntheses

*(none yet)*

---

## Queries

*(none yet)*
