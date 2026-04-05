---
tags: [concept]
created: 2026-04-05
updated: 2026-04-05
sources: [agent-hypervisor-benchmarks]
---

# AgentDojo Benchmark
> An adversarial benchmark for AI agents measuring utility (task completion rate) and Attack Success Rate (ASR) across prompt injection attacks; Agent Hypervisor achieves 0% ASR and 80% utility.

**Primary sources:** [[src-agent-hypervisor-benchmarks]], `research/benchmarks/agentdojo/`

---

## What It Is

AgentDojo is an adversarial benchmark developed at ETH Zurich for evaluating AI agent defenses. It tests two competing objectives:

- **Utility** — fraction of legitimate tasks the agent completes correctly (without the defense blocking normal operation).
- **Attack Success Rate (ASR)** — fraction of prompt injection attacks that succeeded (attacker's intended action executed).

A good defense minimizes ASR without significantly reducing utility. The hardest challenge: utility and security are in tension — overly aggressive defenses block legitimate actions.

---

## Test Design

AgentDojo pairs each user task with one or more adversarial variants where attacker-controlled content (injected into documents, emails, or web pages) attempts to hijack the agent's actions — specifically outbound side-effect calls like `send_email`, HTTP requests, and file writes.

**Full scope evaluation:** 40 user tasks × 14 injection tasks = **560 task-attack pairs**  
**Domains covered:** workspace (email), travel, banking, slack

---

## Agent Hypervisor Results (Post-Refactor)

Model: `gpt-4o-mini-2024-07-18`, Attack: `important_instructions`

| System | Utility (under attack) | ASR | Utility (clean) |
|--------|------------------------|-----|-----------------|
| **Agent Hypervisor** | **80.0%** | **0.0%** | **80.0%** |
| tool_filter | 72.9% | 1.1% | 80.0% |
| spotlighting_with_delimiting | 47.5% | 12.7% | 77.5% |
| none (baseline) | 32.5% | 18.2% | 82.5% |

**Key finding:** Under attack, the no-defense baseline achieves only 32.5% utility — the agent follows attacker instructions instead of completing the user's task. AH restores utility to 80.0% by blocking injections and returning control to the legitimate task.

---

## Why the Results Hold

Agent Hypervisor's 0% ASR is structural, not probabilistic. The provenance check is:

```yaml
# Block any outbound email where the recipient traces to external content
- id: deny-email-external-recipient
  tool: send_email
  argument: to
  provenance: external_document
  verdict: deny
```

This rule fires regardless of how the injection is phrased — it checks the *structure* of the derivation DAG, not the content of the instruction. There are no strings to match, no classifiers to fool.

---

## The Refactor: Before vs. After

| Metric | Before | After |
|--------|--------|-------|
| No-attack utility | 53.3% | 80.0% |
| Attack ASR | ~47.8% | 0.0% |

**Two root causes fixed:**
1. Detection-driven taint seeding (was: taint all tool outputs blindly → too many false positives)
2. Argument-level taint containment (was: block any call when any taint present → too aggressive)

---

## Implementation Architecture in AgentDojo

Three `BasePipelineElement` subclasses inserted into the agent's `ToolsExecutionLoop`:

1. **AHTaintGuard** — pre-execution validation via 7-step fail-closed pipeline
2. **AHBlockedCallInjector** — structured error feedback + retry cap (2 blocks per episode)
3. **AHInputSanitizer** — detection-driven taint seeding, injection pattern stripping

---

## Comparison with [[camel-defense|CaMeL]]

| | CaMeL | Agent Hypervisor |
|--|-------|-----------------|
| Security path | Dual-LLM | No LLM |
| Taint granularity | Value-level | Argument-level |
| Utility | ~80% | 80.0% |
| ASR | ~10% | **0.0%** |

---

## Limitations

- Single benchmark — may not generalize to all agent deployment patterns.
- `ask` verdicts treated as `deny` in automated runs (production `ask` enables human review).
- Single LLM backend (`gpt-4o-mini`).
- **Independent replication needed** — preliminary results from a prototype.

---

## Key concepts cross-referenced

- [[taint-propagation]] — the core enforcement mechanism evaluated
- [[world-manifest]] — task manifests used in evaluation
- [[manifest-resolution]] — ALLOW/DENY/ASK verdicts
- [[camel-defense]] — closest published prior work
- [[src-agent-hypervisor-benchmarks]] — full results page
