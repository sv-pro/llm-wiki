---
tags: [source]
created: 2026-04-05
updated: 2026-04-05
sources: [agent-hypervisor-status]
---

# Agent Hypervisor — STATUS.md
> Component maturity model and classification table for every major system component.

**Source:** `raw/agent-hypervisor/STATUS.md`  
*Updated: March 2026*

---

## Summary

STATUS.md is the authoritative reference for what is production-ready, in progress, experimental, or archived in [[agent-hypervisor]].

---

## Maturity Classification

| Symbol | Label | Meaning |
|--------|-------|---------|
| ✅ | **Canonical** | Stable, production-quality or publication-ready |
| 🔵 | **Supported** | Working, maintained, but may evolve |
| 🟡 | **Experimental** | PoC or draft quality; not relied on by other components |
| 🟠 | **In Progress** | Being actively developed |
| ⬜ | **Planned** | Specified but not yet implemented |
| 🗄️ | **Archived** | Superseded; preserved for reference only |

---

## Notable Status Entries

### Architecture Documentation
All core documentation (whitepaper, threat model, FAQ, glossary, evaluation framework) is ✅ Canonical.

### Publication Series — *The Missing Layer*
Articles 01–04 are ✅ Published. Articles 05–07 and a 3-article taint series are ⬜ Planned.

### Layer 0: Execution Physics
Container/network isolation and OS-level sandboxing are ⬜ Planned. The `Dockerfile` exists but the isolation layer is not implemented.

### Layer 1: Base Ontology (World Manifest + Compiler)
Core components (World Manifest schema v1, manifest loader, capability profiler/renderer, `awc` CLI, enforcer) are ✅ Canonical. Schema v2 and additional `ahc` commands (`validate`, `simulate`, `diff`, `coverage`, `tune`, `draft`) are ⬜ Planned for v0.2–v0.3.

### Layer 2: Dynamic Ontology
Capability DSL, named policy presets, MCP integration wrapper, and audit/event logger are 🔵 Supported. Dynamic context projection is 🟠 In Progress.

### Layer 3: Execution Governance
`IRBuilder`, `TaintContext`, `SafeMCPProxy`, `Executor`, `Channel`, and `compile_world()` are ✅ Canonical. Approval gate is 🟡 Experimental. Reversibility classification is 🟠 In Progress.

### Research
AgentDojo benchmark integration is 🟠 In Progress (M4 deliverable). See [[agentdojo-benchmark]] and [[src-agent-hypervisor-benchmarks]].

### ADRs
ADR-001 through ADR-004 are 🟡 Open (decisions pending). ADR-005 is Accepted.

---

## Key concepts cross-referenced

- [[four-layer-architecture]] — the layers tracked in this status document
- [[world-manifest]] — Layer 1 core artifact
- [[taint-propagation]] — Layer 3 core mechanism
- [[agentdojo-benchmark]] — benchmark research tracked here
- [[src-agent-hypervisor-docs-adr]] — ADR summaries
