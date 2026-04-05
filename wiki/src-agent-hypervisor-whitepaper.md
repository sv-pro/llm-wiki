---
tags: [source]
created: 2026-04-05
updated: 2026-04-05
sources: [agent-hypervisor-whitepaper]
---

# Agent Hypervisor — Whitepaper
> Formal architecture document: four-layer model, AI Aikido, World Manifest Compiler, Design-Time HITL.

**Source:** `raw/agent-hypervisor/WHITEPAPER.md`

---

## Origin Insight

A GitHub Copilot demo using Playwright MCP to test a web application raises the key question: *Can another prompt capture all test operations as a deterministic Playwright script, bypassing the LLM entirely?* The answer is yes — and this is the thesis:

> Every time an LLM generates code that is compiled and executed, a stochastic process has produced a deterministic artifact.

[[ai-aikido]]: use the LLM's capability to *build* the deterministic cage in which agents safely operate. Intelligence designs the physics; it does not govern the physics at runtime.

---

## Part I — Core Architecture

### The Problem

Standard defenses (guardrails, prompt filters, output classifiers) operate *after* the agent has perceived dangerous input. Evidence:
- Adaptive attacks: **90–100% bypass rates** (Yi et al., 2025)
- OpenAI: prompt injection "unlikely to ever be fully solved" at behavioral layer
- [[zombie-agent]]: persistent memory poisoning with **90% data leakage** (Radware, Jan 2026)

### The Thesis

> **"Does action Y exist in agent X's universe?"**

Not permission-based — **construction-based**. Dangerous actions are absent from the world the agent inhabits.

### [[four-layer-architecture]]

| Layer | Name | Role |
|---|---|---|
| 0 | Execution Physics | Infrastructure isolation — makes actions physically impossible |
| 1 | Base Ontology | Design-time vocabulary of actions that exist |
| 2 | Dynamic Ontology Projection | Context-dependent subset visible to the actor now |
| 3 | Execution Governance | Deterministic allow/deny/ask/simulate — no LLM |

### Manifest Resolution Law

```
proposed action
  ├── explicit allow in manifest     → ALLOW
  ├── explicit deny in manifest      → DENY
  ├── invariant violation            → DENY
  └── not covered by manifest
        ├── interactive mode         → ASK
        └── background mode         → DENY
```

---

## Part II — The Semantic Gap (Honest Weakness)

The boundary layer needs intelligence to understand input, but intelligence is stochastic. Three tensions:

1. **Parsing requires understanding** — semantic ambiguity ("forward to Alex") requires a model
2. **Taint propagation breaks on transformations** — classic overtainting/undertainting problem (Denning, 1976)
3. **Ontology design is hard** — too narrow = useless; too wide = nominal security

**Honest claim:** bounded, measurable security — not perfect, not probabilistic, but deterministic within explicitly defined boundaries.

---

## Part III — [[ai-aikido]]

Resolution via temporal separation: stochastic intelligence operates at **design-time** to generate deterministic artifacts. Runtime executes only those artifacts.

Applications:
- Parser/canonicalizer generation from real input corpora
- Automated [[world-manifest]] creation
- Adversarial red-teaming of parsers (generate → attack → patch → re-attack)
- Context-aware [[taint-propagation]] rule generation

---

## Part IV — [[world-manifest-compiler]]

Compilation pipeline:

```
Human intent + LLM semantic modeling
              ↓
     World Manifest (reviewed & committed)
              ↓
     Compilation phase
              ↓
     Deterministic runtime artifacts
              ↓
     Runtime enforcement (LLM-free)
```

The [[world-manifest]] defines: base ontology (L1), trust model (L1), capability matrix (L2), taint propagation rules (L3), escalation conditions (L3), provenance schema (L3).

---

## Part V — [[design-time-hitl]]

> Human judgment is necessary, but must be amortized through design-time rather than expended at runtime.

Three modes:
- **Design-time** (scales) — one decision amortizes across thousands of runtime decisions
- **Runtime** (exception, not rule) — `require_approval` is the pressure relief valve; frequent firing signals an underdefined manifest
- **Iteration-time** — logs reveal patterns → LLM regenerates rules → coverage expands

Economics: `O(n)` per runtime decision (traditional) → `O(log n)` per design iteration (Agent Hypervisor).

---

## Part VIII — Honest Constraints

- Manifest completeness is finite — novel attacks require redesign
- Semantic ambiguity is resolved by policy, not eliminated
- Adaptation is not instantaneous (redesign → recompile → redeploy gap)
- Human responsibility remains — a poorly designed manifest produces a poorly secured world

---

## Key concepts

[[agent-hypervisor]] · [[four-layer-architecture]] · [[world-manifest]] · [[world-manifest-compiler]] · [[ai-aikido]] · [[taint-propagation]] · [[design-time-hitl]] · [[manifest-resolution]] · [[zombie-agent]] · [[camel-defense]]
