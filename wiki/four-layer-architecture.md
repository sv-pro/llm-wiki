---
tags: [concept]
created: 2026-04-05
updated: 2026-04-05
sources: [agent-hypervisor-readme, agent-hypervisor-claude, agent-hypervisor-whitepaper]
---

# Four-Layer Architecture
> The four deterministic layers of Agent Hypervisor: Execution Physics (L0), Base Ontology (L1), Dynamic Ontology (L2), and Execution Governance (L3).

**Primary sources:** [[src-agent-hypervisor-readme]], [[src-agent-hypervisor-claude]], [[src-agent-hypervisor-whitepaper]]

---

## Overview

[[agent-hypervisor]] is organized into four deterministic layers. Together they transform raw reality into a safe, bounded world for the AI agent. The LLM operates *inside* this world; it never touches raw reality directly.

```
[ Raw Reality — emails, files, APIs, other agents ]
        ↓
Layer 0: Execution Physics    (container/network isolation)
        ↓
Layer 1: Base Ontology        (World Manifest schema & compiler)
        ↓
Layer 2: Dynamic Ontology     (Capability DSL & policy presets)
        ↓
Layer 3: Execution Governance (IRBuilder, taint, provenance, approvals)
        ↓
[ Agent — virtualized world ]
        ↓
[ External effects — audited, traced, governed ]
```

---

## Layer 0 — Execution Physics

**Purpose:** Container and network isolation.  
**Status:** ⬜ Planned. `Dockerfile` exists but the isolation layer is not yet implemented.

The infrastructure isolation layer. In the full architecture, every agent session runs in an isolated container with defined network egress. This prevents filesystem and network escapes entirely — complementary to the semantic isolation of Layers 1–3.

---

## Layer 1 — Base Ontology

**Purpose:** World Manifest schema and compiler.  
**Location:** `src/agent_hypervisor/compiler/`  
**Status:** ✅ Canonical (core components).

This layer defines what the agent's world *is*. The [[world-manifest|World Manifest]] declares the complete set of actions, trust channels, capabilities, taint rules, escalation conditions, provenance schema, and budgets.

The compiler (`awc compile` / `ahc compile`) transforms the manifest into deterministic runtime artifacts: policy tables, JSON Schema validators, taint state machines, capability engines. No LLM survives compilation.

Key components: World Manifest schema v1, manifest loader, capability profiler, capability renderer, `awc`/`ahc` CLI, enforcer (ALLOW/DENY decisions).

---

## Layer 2 — Dynamic Ontology

**Purpose:** Capability DSL and policy presets.  
**Location:** `src/agent_hypervisor/authoring/`  
**Status:** 🔵 Supported.

This layer provides tools for *authoring* the world definition. The Capability DSL (YAML) lets operators define capabilities declaratively. Named policy presets (worlds) like `base` and `email_safe` provide reusable starting points. The MCP integration wrapper enables [[agent-hypervisor]] to intercept MCP tool calls.

Also includes the audit/event logger — one-line JSON event logger for all decisions.

---

## Layer 3 — Execution Governance

**Purpose:** IRBuilder, taint propagation, provenance, approvals.  
**Location:** `src/agent_hypervisor/runtime/`  
**Status:** ✅ Canonical (core components).

The enforcement kernel. This layer:
- **IRBuilder.build()** — validates all constraints at construction time, producing a sealed `IntentIR` object. Cannot be constructed outside `IRBuilder`.
- **TaintContext** — monotonic [[taint-propagation]]; taint is never dropped.
- **SafeMCPProxy** — in-path enforcement for all MCP tool calls.
- **Executor / Sandbox** — executes validated `IntentIR` in a separate subprocess.
- **Channel** — trust level resolution for input sources.
- **compile_world()** — transforms a World Manifest into a `CompiledPolicy` (frozen, immutable).

The process boundary is a hard security invariant: handler code never has direct access to policy state.

---

## Execution Flow

```
world_manifest.yaml
    ↓ compile_world() [runtime/runtime.py]
CompiledPolicy (frozen, metadata only)
    ↓
Channel → IRBuilder → Executor → worker subprocess
```

---

## No LLM on the Critical Path

A key architectural property: no LLM appears anywhere in the enforcement path (Layers 1–3). The agent (LLM) operates exclusively in Layer 3 from the perspective of *perceiving* Semantic Events and *proposing* intents. All policy evaluation, taint checking, and execution decisions are deterministic.

---

## Key concepts cross-referenced

- [[world-manifest]] — the Layer 1 artifact
- [[taint-propagation]] — the Layer 3 enforcement mechanism
- [[manifest-resolution]] — the three-way verdict produced by Layer 3
- [[ai-aikido]] — LLM-assisted authoring at Layers 1–2
- [[design-time-hitl]] — human review of Layer 1–2 artifacts
- [[zombie-agent]] — the scenario that motivated the architecture
