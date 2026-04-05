---
tags: [source]
created: 2026-04-05
updated: 2026-04-05
sources: [agent-hypervisor-benchmarks]
---

# Agent Hypervisor — Benchmark Results
> AgentDojo benchmark evaluation: 0% ASR, 80% utility across 560 attack pairs (post-refactor).

**Sources:** `research/benchmarks/agentdojo/results.md`, `research/benchmarks/agentdojo/methodology.md`, `research/benchmarks/reports/report-v1.md`, `research/agentdojo-bench/README.md`

---

## Summary

Agent Hypervisor was evaluated on the AgentDojo adversarial benchmark. Post-refactor results show **0% Attack Success Rate** with **80% utility** across 560 task-attack pairs. These are preliminary results requiring independent replication.

---

## What AgentDojo Measures

AgentDojo tests AI agents across two metrics:
- **Utility** — fraction of legitimate tasks completed correctly (no firewall false-blocking).
- **Attack Success Rate (ASR)** — fraction of prompt injection attacks that succeeded (attacker's action executed).

The benchmark covers multiple domains (email assistant, travel planner, banking) with injected adversarial content in documents, emails, or web pages that attempt to hijack the agent's actions.

---

## Post-Refactor Results (Full Scope)

Full scope: 40 user tasks × 14 injection tasks = **560 pairs**.  
Model: `gpt-4o-mini-2024-07-18`, Attack: `important_instructions`.

| System | Utility (under attack) | ASR | Utility (clean) |
|--------|------------------------|-----|-----------------|
| **Agent Hypervisor** | **80.0%** | **0.0%** | **80.0%** |
| tool_filter | 72.9% | 1.1% | 80.0% |
| spotlighting_with_delimiting | 47.5% | 12.7% | 77.5% |
| none (baseline) | 32.5% | 18.2% | 82.5% |

**Key observation:** Under attack, the baseline achieves only 32.5% utility — the agent follows attacker instructions instead of completing the user's task. AH restores utility to 80.0% by blocking injections.

---

## Before vs. After Refactor

| Metric | Before | After | Delta |
|--------|--------|-------|-------|
| No-attack utility | 53.3% | 80.0% | +26.7pp |
| Attack utility | ~60% | 80.0% | ~+20pp |
| Attack ASR | ~47.8% | 0.0% | ~−47.8pp |

**Root causes addressed by refactor:**
1. **Detection-driven taint seeding** — previously tainted every tool output unconditionally. Now only seeds taint when injection patterns are actually detected, eliminating false positives.
2. **Argument-level taint containment** — previously blocked all external-boundary calls once any taint present. Now taint carries the attacker's specific target values; calls whose arguments don't match those values are allowed.

---

## Architecture in AgentDojo

Three pipeline elements inserted into the `ToolsExecutionLoop`:

1. **AHTaintGuard** (pre-tool execution) — validates proposed calls against taint state and World Manifest. Runs 7-step fail-closed validation (manifest → action → schema → capability → taint → escalation → allow).
2. **AHBlockedCallInjector** (post-tool execution) — injects structured error feedback for blocked calls; caps retries at 2 per episode.
3. **AHInputSanitizer** (post-tool execution, pre-LLM) — canonicalizes tool outputs (strips injection blocks), seeds taint when injection patterns are detected, wraps outputs with trust metadata.

---

## Comparison with [[camel-defense|CaMeL]]

| Property | CaMeL | Agent Hypervisor |
|----------|-------|-----------------|
| Taint granularity | Value-level (Python interpreter) | Message-level |
| Security path | Dual-LLM (privileged + quarantined) | **No LLM** on critical path |
| Policy definition | Manual | Design-time compiled manifests |
| Performance overhead | Interpreter overhead | O(1) manifest lookup + regex |

Prior prototype evaluation (16-task subset): AH 81% utility / 6% ASR vs. CaMeL ~80% utility / ~10% ASR.

---

## Limitations

- **Single benchmark** — AgentDojo covers a specific task distribution; may not generalize.
- **Manifest quality matters** — task manifests were LLM-generated and reviewed; production quality directly affects both utility and security.
- **`ask` → `deny` substitution** — in automated runs, `ask` verdicts were treated as `deny`; production `ask` enables human review, recovering some utility.
- **Single LLM backend** — `gpt-4o-mini-2024-07-18` only.
- **Independent replication needed** — preliminary results from prototype.

---

## Key concepts cross-referenced

- [[agentdojo-benchmark]] — the benchmark concept page
- [[taint-propagation]] — the core mechanism evaluated
- [[world-manifest]] — the manifests used in evaluation
- [[camel-defense]] — CaMeL comparison
- [[manifest-resolution]] — ALLOW / DENY / ASK verdicts
