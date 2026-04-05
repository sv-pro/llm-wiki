---
tags: [concept]
created: 2026-04-05
updated: 2026-04-05
sources: [agent-hypervisor-whitepaper, agent-hypervisor-zombie-scenario, agent-hypervisor-docs-architecture]
---

# Manifest Resolution
> The deterministic decision rule that evaluates every Intent Proposal against the World Manifest, producing one of three verdicts: ALLOW, DENY, or ASK.

**Primary sources:** [[src-agent-hypervisor-docs-architecture]], [[src-agent-hypervisor-zombie-agent-scenario]], [[src-agent-hypervisor-whitepaper]]

---

## What It Is

Manifest Resolution is the policy evaluation step in [[agent-hypervisor]]'s enforcement pipeline. Every proposed action passes through this deterministic rule, which evaluates: the action type, trust level of source data, [[taint-propagation|taint status]], reversibility, budget limits, and explicit manifest rules.

**Key property:** Same input, same output, always. There is no LLM on this path.

---

## The Decision Rule

```
proposed action
  │
  ├── explicit ALLOW in manifest          → ALLOW
  ├── explicit DENY in manifest           → DENY
  ├── invariant violation                 → DENY
  │     (TaintContainmentLaw,
  │      CapabilityBoundaryLaw, etc.)
  └── not covered by manifest
        ├── interactive mode              → ASK
        │     ├── one-shot approval       → execute once (no manifest change)
        │     └── manifest extension      → update [[world-manifest]], then execute
        └── background mode              → DENY
```

**"The world is closed-for-execution, open-for-extension."**

---

## The Three Verdicts

### ALLOW
The action is explicitly permitted by the manifest and passes all invariant checks. The tool executes and a trace entry is written.

### DENY
One of:
- An explicit deny rule in the manifest.
- An invariant violation (most commonly the [[taint-propagation|TaintContainmentLaw]]: tainted data attempting to trigger external side effects).
- The CapabilityBoundaryLaw: the action requires a capability not present at the current trust level.
- The ProvenanceLaw: a memory write attempted without required provenance metadata.
- Background mode and the action is not covered.

All denials produce an immutable trace entry with the rule that fired.

### ASK
The action is not covered by the manifest and the agent is running in interactive mode. The system presents the proposal to the human reviewer with full provenance context and offers:
- **One-shot approval** — execute this instance only; the manifest is unchanged.
- **Manifest extension** — add a rule to the [[world-manifest|World Manifest]] to cover this class of actions going forward; then execute.
- **Deny** — reject this specific instance.

Frequent `ASK` verdicts are a signal that the manifest is underdefined — see [[design-time-hitl]].

---

## Enforcement Invariants

| Law | Rule | Enforcement |
|-----|------|-------------|
| **TaintContainmentLaw** | Tainted data cannot trigger `external_side_effects` | DENY |
| **CapabilityBoundaryLaw** | Action requires capability absent at current trust level | DENY |
| **ProvenanceLaw** | Memory write requires provenance metadata | DENY |

These are physics laws, not configuration options. They apply regardless of what the [[world-manifest|World Manifest]] says — they are structural invariants of the architecture.

---

## The Enforcement Pipeline (Detailed)

From [[src-agent-hypervisor-docs-architecture]]:

```
Raw input
  → [Layer 1] Trust classification + taint assignment + injection stripping
  → Semantic Event
  → [Layer 3] Agent perceives → produces Intent Proposal (structured JSON)
  → [Layer 4] Deterministic World Policy evaluation:
      - Is the action in the World Manifest?
      - Is the trust level sufficient?
      - Is the data tainted?
      - Is the action reversible?
      - Is the budget exhausted?
  → decision: allow | deny | require_approval | simulate
  → [Layer 5] If allowed: tool invocation + immutable audit log
```

---

## Three Execution Modes

| Mode | Uncovered action | Tainted action |
|------|-----------------|----------------|
| Interactive | ASK | DENY (or ASK if manifest includes `required_if_tainted`) |
| Background | DENY | DENY |
| Simulation | Record only, no execution | Record only |

---

## Determinism Property

The manifest resolution is the "acid test" for [[agent-hypervisor]]: can you write a deterministic unit test for your agent's safety? If same manifest + same input always produces same decision, the answer is yes.

This property makes the system auditable, reproducible, and improvable — unlike probabilistic runtime filters whose failure modes are open-ended.

---

## Key concepts cross-referenced

- [[world-manifest]] — the specification evaluated during resolution
- [[taint-propagation]] — the TaintContainmentLaw that drives most DENY verdicts
- [[four-layer-architecture]] — Layer 3 runs the enforcement
- [[design-time-hitl]] — the ASK → manifest-extension pathway
- [[zombie-agent]] — the scenario demonstrating cross-session resolution
- [[agentdojo-benchmark]] — empirical validation of 0% ASR with 80% utility
