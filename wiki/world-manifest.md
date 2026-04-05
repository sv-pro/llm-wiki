---
tags: [concept]
created: 2026-04-05
updated: 2026-04-05
sources: [agent-hypervisor-whitepaper, agent-hypervisor-readme, agent-hypervisor-docs-concept]
---

# World Manifest
> The formal specification of an AI agent's universe — what actions exist, which inputs are trusted, how data contamination propagates, and what the budget limits are.

**Primary sources:** [[src-agent-hypervisor-whitepaper]], [[src-agent-hypervisor-docs-concept]], [[src-agent-hypervisor-docs-architecture]]

---

## What It Is

The World Manifest is a YAML document that defines everything in an [[agent-hypervisor|Agent Hypervisor]]-governed agent's world. It is analogous to a **constitution**: expensive to draft, but the cost amortizes across every runtime decision.

The key security insight: tools and actions not defined in the manifest do not exist in the agent's world — they are not forbidden, they are *absent*.

---

## What a Manifest Defines

| Section | Purpose |
|---------|---------|
| **Action Ontology** | Complete set of permitted actions (tools the agent can call) |
| **Trust Model** | Trust channels (`user`, `email`, `web`, `MCP`, etc.) and their trust levels |
| **Capability Matrix** | Which capabilities are available at which trust levels |
| **Taint Rules** | How contamination propagates through data transformations |
| **Escalation Conditions** | When to `ask` vs. automatically `allow` or `deny` |
| **Provenance Schema** | Origin tracking rules for memory and data |
| **Budgets** | Cost / token / operation limits |

---

## The Constitution Metaphor

The World Manifest functions like a legal constitution: humans review and commit it at design-time. Every runtime session executes deterministically within that reviewed boundary. This is the core of [[design-time-hitl|Design-Time HITL]] — human judgment is amortized, not repeated per-action.

A poorly designed manifest produces a poorly secured world. **Security is a property of the manifest, not of the runtime alone.**

---

## Compilation

The manifest is compiled by the **World Manifest Compiler** (CLI: `awc compile`, `ahc compile`) into deterministic runtime artifacts:
- Lookup tables (capability matrix)
- JSON Schema validators (typed action schemas)
- Taint state machines ([[taint-propagation]])
- Policy tables (for [[manifest-resolution]])

This compilation step is the heart of [[ai-aikido]]: LLM intelligence is used at design-time to author the manifest; the compiled artifacts contain no LLM.

---

## Closed-for-Execution, Open-for-Extension

The World Manifest defines a **closed action space** at runtime. Novel situations not covered by the manifest trigger:
- **Interactive mode:** an `ASK` verdict — human reviews and chooses one-shot approval or manifest extension.
- **Background mode:** automatic `DENY`.

This is the "closed-for-execution, open-for-extension" property: the world is finite and safe by construction, but can grow through explicit, reviewed extension.

---

## Minimal Viable Semantic (MVS)

The manifest encodes only what the agent legitimately needs. Everything else does not exist. The smaller the defined world, the smaller the attack surface.

---

## Example (ZombieAgent scenario)

```yaml
version: "1.0"
name: "email-assistant"

trust_channels:
  user:   trusted
  email:  untrusted
  memory: derived  # trust inherited from source provenance

capabilities:
  trusted:   [read, internal_write, memory_write, external_side_effects]
  untrusted: [read]
  tainted:   []

actions:
  send_email:
    requires: [external_side_effects]
    approval: required_if_tainted

invariants:
  TaintContainmentLaw:
    rule: tainted_data cannot trigger external_side_effects
    enforcement: deny
```

See [[src-agent-hypervisor-zombie-agent-scenario]] for the full scenario manifest.

---

## Key concepts cross-referenced

- [[four-layer-architecture]] — the manifest governs Layers 1–3
- [[ai-aikido]] — LLM-assisted manifest authoring
- [[design-time-hitl]] — human review of the manifest
- [[taint-propagation]] — the taint rules section
- [[manifest-resolution]] — how the manifest is evaluated at runtime
- [[zombie-agent]] — the primary motivating scenario
