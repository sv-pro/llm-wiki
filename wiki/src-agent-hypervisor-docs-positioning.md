---
tags: [source]
created: 2026-04-05
updated: 2026-04-05
sources: [agent-hypervisor-docs-positioning]
---

# Agent Hypervisor — Positioning Docs
> The Crutch/Workaround/Bridge framework and security comparison table.

**Sources:** `docs/positioning/crutch_workaround_bridge.md`, `docs/positioning/security_comparison.md`

---

## Summary

Two positioning documents that define a classification framework for evaluating AI security approaches and apply it to compare Agent Hypervisor against the current landscape.

---

## The Crutch / Workaround / Bridge Framework

See [[crutch-workaround-bridge]] for the full concept page.

**Core question:** Does this system block attacks, or redefine the agent's world?

### 🔴 Crutch
Treats symptoms, not cause. Probabilistic, bypassable, operates after unsafe inputs have already entered the pipeline. Maintenance cost scales with attack sophistication.
- Examples: regex/keyword filters, prompt injection classifiers, LLM-as-judge safety checks, output content scanners.

### 🟡 Workaround
Solves a specific immediate problem without fixing root cause. Production-usable, real risk reduction, bounded scope. Coverage degrades as agent capabilities expand.
- Examples: LangChain security layers, runtime monitoring, tool allow/deny lists, LLM firewalls.

### 🟢 Bridge
Introduces the correct architectural direction. Changes what can *exist*, not what is *permitted*. Structural guarantees that hold by construction, not configuration. Cost does not scale with attack sophistication.
- Examples: capability-based security systems, ontology-based action scoping, [[agent-hypervisor]].

**The key distinction:**
- Crutch/Workaround: "Can we stop this attack?" (reactive)
- Bridge: "Can this action exist in this world?" (generative)

**The permission security trap:** most AI security operates as `agent → proposes action → policy checks → allow/deny`. The policy must anticipate every dangerous action; attackers need to find one it missed. Asymmetric cost.

Ontological security: define what actions exist at design-time. The agent can only propose actions that exist. Dangerous actions that were never defined cannot be expressed.

**Why Workarounds don't scale:** as agents become more capable, the action space expands. Workaround coverage is proportional to threat enumeration — a fixed amount against an expanding attack surface. Bridge coverage is proportional to manifest definition — linear growth with the governed space.

---

## Security Comparison Table

See [[crutch-workaround-bridge]] for the full framework. Summary of key approaches:

| Approach | Type | Determinism | Bypass Risk | Scales |
|----------|------|-------------|-------------|--------|
| Regex / keyword filters | 🔴 Crutch | Deterministic | High | No |
| Prompt injection classifiers | 🔴 Crutch | Probabilistic | High | No |
| LLM-as-judge safety | 🔴 Crutch | Probabilistic | High | No |
| Output content scanners | 🔴 Crutch | Mixed | Medium | No |
| LangChain security layers | 🟡 Workaround | Mixed | Medium | Partial |
| Tool allow/deny lists | 🟡 Workaround | Deterministic | Medium | Partial |
| Runtime monitoring | 🟡 Workaround | Probabilistic | Medium | Partial |
| LLM firewall (rule-based) | 🟡 Workaround | Mixed | Medium | Partial |
| [[agent-hypervisor]] | 🟢 Bridge | Deterministic | Low† | Yes |

†Bypass risk for AH is bounded by the semantic gap: if the World Manifest incorrectly defines the agent's world, the system correctly enforces an incorrect world. This is a *known, explicit, bounded* risk.

**Key observations:**
- Determinism alone is not sufficient — tool allow/deny lists are deterministic but are a Workaround (they control which tools exist, not what arguments are passed).
- Probabilistic components break audit chains — you cannot explain a decision if it depended on a model's hidden state.
- AH's enforcement path is fully deterministic from IRBuilder through execution.

---

## Honest Limitations

AH is a Bridge, not a complete solution. A Bridge does not solve:
- The **semantic gap** — the manifest must be correct.
- **Manifest authoring quality** — bad manifest = bad security.
- **LLM reasoning errors** within a correctly defined world.

A Bridge is not the end of security — it is the correct foundation.

---

## Key concepts cross-referenced

- [[crutch-workaround-bridge]] — the framework detailed here
- [[world-manifest]] — the Bridge artifact
- [[four-layer-architecture]] — the architectural layers
- [[camel-defense]] — CaMeL is a partial Bridge
- [[ai-aikido]] — design-time intelligence enabling the Bridge
