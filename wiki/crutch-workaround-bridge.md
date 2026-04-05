---
tags: [concept]
created: 2026-04-05
updated: 2026-04-05
sources: [agent-hypervisor-docs-positioning]
---

# Crutch / Workaround / Bridge
> A classification framework for AI security approaches: Crutch (treats symptoms), Workaround (solves immediate problem without fixing root cause), Bridge (introduces the correct architectural direction).

**Primary sources:** [[src-agent-hypervisor-docs-positioning]], [[src-agent-hypervisor-pub-missing-layer]]

---

## What It Is

The Crutch/Workaround/Bridge framework is the evaluation lens used by [[agent-hypervisor]] to classify AI security approaches. The core question:

> Does this system **block attacks** — or **redefine the agent's world**?

These are not the same thing. A system that blocks attacks operates inside an unsafe architecture and tries to intercept what escapes. A system that redefines the world changes what can be expressed at all.

---

## 🔴 Crutch

**Definition:** Treats symptoms rather than cause.

- Probabilistic — works most of the time, not all of the time
- Bypassable — adaptive attacks circumvent it by design
- Post-perception — operates after unsafe inputs have already entered the pipeline
- Maintenance cost scales with attack sophistication
- **Failure mode:** a new attack variant bypasses it; the fix is a new rule — permanent treadmill

**Examples:** Regex and keyword filters, prompt injection classifiers, LLM-as-judge safety checks, output content scanners.

---

## 🟡 Workaround

**Definition:** Solves an immediate problem without fixing the root cause.

- Solves specific attack classes at the point of application
- Partial protection — bounded scope, uncovered flanks
- Production-usable — real reduction in risk
- Still operates inside an architecturally unsafe pipeline
- **Failure mode:** guarantees end exactly where explicit rules end; uncovered = unprotected

**Examples:** LangChain security layers, runtime monitoring, tool allow/deny lists, LLM firewalls with structured rule sets.

---

## 🟢 Bridge

**Definition:** Introduces the correct architectural direction.

- Changes what can *exist*, not what is *permitted*
- Structural — guarantees hold by construction, not configuration
- Composable — works with and strengthens other approaches
- Reduces attack surface before the agent encounters it
- Cost does not scale with attack sophistication
- **Failure mode:** bounded and explicit — you can state exactly what it does not cover

**Examples:** Capability-based security systems, ontology-based action scoping, [[agent-hypervisor]].

---

## The Permission Security Trap

Most AI security operates in **permission security mode:**
```
Agent → proposes action → policy checks → allow or deny
```

Two structural problems:
1. The policy must anticipate every dangerous action. Attackers need to find one it missed. Asymmetric cost.
2. The policy operates on the *output* of an LLM that was already compromised.

**Ontological security** changes the order:
```
Design-time: define what actions exist
Runtime:     agent can only propose actions that exist
             policy evaluates within that bounded space
```

Dangerous actions never defined cannot be proposed, expressed, or evaluated — they are absent.

---

## Why Workarounds Don't Scale

A Workaround's coverage is proportional to its enumeration of threats. As agents become more capable, the action space expands. A Workaround that covers today's threat model has fixed coverage against an expanding attack surface.

A Bridge's coverage is proportional to the World Manifest's definition of the agent's world. As the manifest grows, so does coverage — linearly. New capabilities enter the governed space automatically.

---

## Pipeline Position Map

```
Input arrives
      │
[🔴 Crutch]     — post-input canonicalization, filtering, sanitization
      │           Operates after perception. Input has already entered.
      ▼
Agent processes
      │
[🟡 Workaround] — policy enforcement, execution gate
      │           Dangerous action was expressed; trying to catch it.
      ▼
Execution

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[🟢 Bridge]     — design-time world compilation
                  Operates before the agent exists.
                  Dangerous actions are not blocked — they are absent.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Agent Hypervisor Classification

- **NOT a Crutch** — does not filter outputs or classify prompts
- **NOT a Workaround** — does not add rules to an unsafe pipeline
- **A Bridge toward Ontological Security** — actions are constructed, not filtered; capabilities are rendered, not granted; unsafe actions are impossible, not denied

---

## Honest Limitations

Agent Hypervisor is a Bridge, not a complete solution. A Bridge does not solve:
- **The semantic gap** — the manifest must be correct.
- **Manifest authoring quality** — bad manifest = bad security.
- **LLM reasoning errors** within a correctly defined world.

A Bridge is the correct foundation for building the rest.

---

## Key concepts cross-referenced

- [[world-manifest]] — the Bridge artifact
- [[ai-aikido]] — how Bridge artifacts are generated
- [[design-time-hitl]] — the human review enabling the Bridge
- [[four-layer-architecture]] — the Bridge architecture
- [[agentdojo-benchmark]] — empirical evidence for Bridge effectiveness
- [[camel-defense]] — CaMeL as a partial Bridge
