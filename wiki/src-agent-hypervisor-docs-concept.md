---
tags: [source]
created: 2026-04-05
updated: 2026-04-05
sources: [agent-hypervisor-docs-concept]
---

# Agent Hypervisor — Concept Docs
> Core conceptual documentation: overview, key concepts, and FAQ objection-handling.

**Sources:** `docs/concept/overview.md`, `docs/concept/concepts.md`, `docs/concept/faq.md`

---

## Summary

Three documents that form the entry point to the [[agent-hypervisor]] architectural thesis. Together they cover: the problem (agents in raw reality), the solution (perception-bounded worlds), the core concepts, and the hardest objections.

---

## The Problem (from overview.md)

Modern AI agents operate in raw reality — they receive unstructured text regardless of whether it comes from a trusted colleague or an attacker's prompt injection. Three failure modes are architecturally inevitable:

- **Unmediated input** — no structural distinction between trusted instructions and untrusted data.
- **Direct memory access** — no provenance tracking on writes.
- **Immediate tool execution** — no staging or reversibility analysis.

---

## The Solution: Perception-Bounded Worlds

The agent is not filtered — its *world* is redesigned. The agent operates inside a constructed universe where:

- Input arrives as typed Semantic Events (with `trust_level`, `taint`, `sanitized_payload`), never as raw text.
- Actions are Intent Proposals evaluated by a deterministic World Policy.
- Dangerous capabilities simply do not exist in the agent's world.

The distinction is **ontological, not behavioral**. A guardrail says "you are not allowed to do X." The hypervisor says "X does not exist in this world."

---

## Core Concepts (from concepts.md)

| Concept | Description |
|---------|-------------|
| [[world-manifest]] | Formal specification of the agent's universe — actions, trust channels, capabilities, taint rules |
| [[four-layer-architecture]] | The four layers from Execution Physics (L0) to Execution Governance (L3) |
| [[taint-propagation]] | Monotonic taint propagation; the TaintContainmentLaw |
| [[manifest-resolution]] | Deterministic ALLOW / DENY / ASK decision rule |
| [[ai-aikido]] | LLM at design-time generates deterministic runtime artifacts |
| [[design-time-hitl]] | Human reviews the World Manifest, not individual runtime decisions |

---

## FAQ — Key Objections (from faq.md)

**"Isn't this just a guardrail?"**
No. A guardrail monitors after the fact. The hypervisor is a virtualization layer — the threat surface is never exposed.

**"Isn't this just a policy engine?"**
Partially. Policy engines evaluate requests against rules — bypassable if the input is ambiguous. AH adds the virtualization layer before the policy engine ever sees input.

**"Isn't this just a sandbox?"**
A sandbox restricts what the agent can *do*. AH also restricts what the agent can *perceive* — raw text is replaced with Semantic Events.

**"Isn't this just an MCP proxy?"**
An MCP proxy intercepts at the output boundary. AH enforces at both input (Layer 1) and output (Layer 5), with [[taint-propagation]] bridging the gap.

**"The semantic gap means Layer 1 needs intelligence — doesn't that reintroduce probabilistic components?"**
Yes, and it's acknowledged. The architecture handles this through *isolation* (Layer 1 failure doesn't cascade) and *tunable conservatism* (stricter policy = smaller attack surface). The failure mode is bounded and explicit, unlike runtime LLM guardrails.

**"Why Design-Time HITL instead of runtime?"**
Runtime HITL doesn't scale. [[design-time-hitl]] amortizes human judgment once across all runtime executions. Runtime `ASK` is a pressure-relief valve for edge cases, not the primary oversight mechanism.

**What is guaranteed:**
- Same intent proposal → same decision (determinism).
- Tainted data cannot reach Layer 5 without an explicit sanitization gate.
- Tools not in the World Manifest cannot be invoked.
- Every effect on external reality passes through an immutable audit log.

**What remains unsolved:**
- Semantically ambiguous injections that pass Layer 1 undetected.
- World Manifest design errors (bad spec → bad security).
- Novel attack patterns not anticipated at design time.
