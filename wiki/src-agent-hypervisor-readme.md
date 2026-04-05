---
tags: [source]
created: 2026-04-05
updated: 2026-04-05
sources: [agent-hypervisor-readme]
---

# Agent Hypervisor — README
> Entry point and navigation guide for the sv-pro/agent-hypervisor repository.

**Source:** `raw/agent-hypervisor/README.md`  
**Repo:** [sv-pro/agent-hypervisor](https://github.com/sv-pro/agent-hypervisor)

---

## Summary

[[agent-hypervisor]] is a deterministic virtualization layer for AI agents. The core claim: AI agent vulnerabilities are architecturally predictable — not bugs — because agents operate with unmediated access to inputs, memory, and tools.

The standard defense is behavioral (detect bad actions, filter bad inputs). Agent Hypervisor asks a different question: **"Does this action exist in the agent's universe?"** Dangerous actions are not prohibited — they are *absent* from the [[world-manifest|World Manifest]]-defined world.

## Architecture overview

```
[ Raw Reality ]
      ↓
┌─────────────────────────────────────┐
│  Layer 0: Execution Physics         │
│  Layer 1: Base Ontology             │
│  Layer 2: Dynamic Ontology          │
│  Layer 3: Execution Governance      │
└─────────────────────────────────────┘
      ↓
[ Agent — virtualized world ]
```

See [[four-layer-architecture]] for the full description.

## Key distinction from CaMeL

| | [[camel-defense\|CaMeL]] | [[agent-hypervisor\|Agent Hypervisor]] |
|---|---|---|
| LLM role | Extracts control flow at **runtime** | Generates policy artifacts at **design-time** |
| Runtime enforcement | LLM on critical path | Deterministic lookup tables only |

## Status (at time of source)

- Core execution model defined
- ZombieAgent scenario and World Manifest documented
- Core framework (`src/core/hypervisor.py`) — 8/8 tests pass
- Manifest authoring tooling not yet built

## Key concepts mentioned

- [[world-manifest]] — constitution of the agent's world
- [[manifest-resolution]] — the deterministic decision rule
- [[four-layer-architecture]] — the layered defense model
- [[camel-defense]] — related work (Google DeepMind, 2025)
- [[zombie-agent]] — primary attack scenario
