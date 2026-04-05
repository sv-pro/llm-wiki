---
tags: [entity]
created: 2026-04-05
updated: 2026-04-05
sources: [agent-hypervisor-docs-research, agent-hypervisor-benchmarks]
---

# CaMeL Defense
> CaMeL (Capability-based Memory and Labeling), a dual-LLM defense system from Google DeepMind (2025) that separates trusted and untrusted LLM instances to resist prompt injection.

**Organization:** Google DeepMind  
**Published:** 2025  
**Paper:** Debenedetti et al., 2025

---

## What It Is

CaMeL is a capability-based defense for AI agents that addresses prompt injection by separating agent execution into two LLM instances:
- A **privileged model** that interprets instructions and has access to tools.
- An **unprivileged (quarantined) model** that handles untrusted data.

The privileged model is intended to resist influence from untrusted data that the unprivileged model processes.

---

## How It Works

```
Trusted instructions → Privileged LLM → Tool calls
Untrusted data      → Unprivileged LLM → Results (with taint labels)
                                          ↓
                        Privileged LLM evaluates whether to use result
```

Taint is tracked at the *value level* using a Python interpreter within the unprivileged model's sandbox.

---

## Results on AgentDojo

From the [[agentdojo-benchmark]] evaluation (approximate, from published paper):

| System | Utility | ASR |
|--------|---------|-----|
| No defense | 100% | ~70% |
| CaMeL | ~80% | ~10% |
| [[agent-hypervisor]] (post-refactor) | 80.0% | **0.0%** |

---

## Comparison with Agent Hypervisor

| Property | CaMeL | [[agent-hypervisor|Agent Hypervisor]] |
|----------|-------|---------------------------------------|
| Security path | Dual-LLM (privileged + quarantined) | **No LLM** on critical path |
| Taint granularity | Value-level (Python interpreter) | Message-level + argument-level |
| Policy definition | Manual | Design-time compiled [[world-manifest|manifests]] |
| Performance overhead | Interpreter overhead | O(1) manifest lookup + regex |
| Failure mode | Privileged model may be influenced; LLMs share failure modes | Engineering errors in World Manifest (different failure class) |
| Provable correctness | With Python interpreter | Deterministic (same inputs → same block) |

**Key architectural distinction:** CaMeL relies on the privileged LLM resisting influence from untrusted data — which remains a probabilistic guarantee. Agent Hypervisor enforces structural provenance constraints at the tool boundary with no LLM on the enforcement path — making bypass require defeating a structural property rather than bypassing a model.

---

## The Correlated Failure Mode Argument

From [[src-agent-hypervisor-docs-architecture]] (threat model):

> "A stochastic system cannot reliably constrain another stochastic system with the same failure modes."

Both models in CaMeL share the same architecture, training methodology, and class of failure modes. An adversarial input that bypasses one LLM is statistically likely to bypass another LLM of the same family. The supervisor is not independent — it is a correlated copy.

Agent Hypervisor addresses this by placing a deterministic system (with fundamentally different failure modes) between the agent and external effects.

---

## Positioning in [[crutch-workaround-bridge]] Framework

CaMeL is classified as a **partial Bridge** — it is better than Workarounds (it introduces structural thinking about trust separation) but still relies on a probabilistic component (the privileged LLM) on the security path.

---

## Key concepts cross-referenced

- [[agentdojo-benchmark]] — comparative benchmark results
- [[taint-propagation]] — the mechanism where AH and CaMeL take different approaches
- [[agent-hypervisor]] — the primary comparison point
- [[crutch-workaround-bridge]] — evaluation framework
- [[src-agent-hypervisor-docs-research]] — detailed comparison
