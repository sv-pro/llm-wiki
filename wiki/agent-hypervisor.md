---
tags: [entity]
created: 2026-04-05
updated: 2026-04-05
sources: [agent-hypervisor-readme, agent-hypervisor-whitepaper, agent-hypervisor-changelog]
---

# Agent Hypervisor
> Deterministic execution governance layer for AI agents; enforces semantic-level isolation through ontological boundaries rather than probabilistic filtering.

**Repository:** [sv-pro/agent-hypervisor](https://github.com/sv-pro/agent-hypervisor)  
**Current version:** 0.4  
**Language:** Python ≥3.10  
**Status:** Proof-of-concept / early-stage research project

---

## What It Is

Agent Hypervisor (AH) is an architectural security layer that sits between any AI agent and the outside world. Rather than filtering dangerous behavior after the fact, AH changes what reality the agent inhabits.

**Core thesis:** AI agent vulnerabilities are architecturally predictable — not bugs — because agents operate with unmediated access to inputs, memory, and tools. The solution is not better detection; it is *safe reality by construction*.

**The key question AH asks:** "Does this action exist in the agent's universe?" — rather than "Can we stop this action?"

---

## How It Works

1. All external signals pass through a **virtualization boundary** before reaching the agent. Raw text is replaced with typed Semantic Events carrying `trust_level`, `taint`, and `sanitized_payload`.
2. The agent proposes **Intent Proposals** (structured JSON) rather than calling tools directly.
3. A **deterministic [[world-manifest|World Policy]]** — compiled from a YAML World Manifest — evaluates every proposal: `allow`, `deny`, or `ask` (pending human approval).
4. Every decision produces an **immutable trace entry** with full provenance.

No LLM appears on the enforcement path. Decisions are unit-testable and reproducible.

---

## Architecture

See [[four-layer-architecture]] for the full description:

| Layer | Name | Purpose |
|-------|------|---------|
| 0 | Execution Physics | Container/network isolation (planned) |
| 1 | Base Ontology | [[world-manifest]] schema & compiler |
| 2 | Dynamic Ontology | Capability DSL & policy presets |
| 3 | Execution Governance | IRBuilder, [[taint-propagation]], approvals |

---

## Key Capabilities (as of v0.4)

- Provenance-based policy enforcement across full derivation chains
- Three-way verdict system (`allow` / `deny` / `ask`)
- Persistent approval workflow — records survive process restarts
- Policy version history with hot-reload
- MCP adapter shim for Claude Desktop / Cursor
- 365 tests across 13 test files

---

## Benchmark Results

On the [[agentdojo-benchmark|AgentDojo]] benchmark (560 task-attack pairs):
- **0% Attack Success Rate** — no injection attack succeeded
- **80% utility** — legitimate tasks completed correctly under attack
- Outperforms all compared defenses (tool_filter, spotlighting, no-defense baseline)

See [[src-agent-hypervisor-benchmarks]] for full results.

---

## Key Distinctions

**vs. [[camel-defense|CaMeL]] (Google DeepMind):** AH uses no LLM on the critical security path; CaMeL uses a privileged LLM. AH enforces structural provenance constraints; CaMeL relies on the privileged model resisting influence from untrusted data.

**vs. guardrails:** A guardrail monitors after the fact. AH is a virtualization layer — the threat surface is never exposed.

**vs. policy engines:** Policy engines evaluate requests against rules (downstream of the compromise point). AH adds virtualization *before* any policy decision is needed.

---

## Source Pages

- [[src-agent-hypervisor-readme]] — entry point and navigation
- [[src-agent-hypervisor-whitepaper]] — full architectural thesis
- [[src-agent-hypervisor-glossary]] — authoritative term definitions
- [[src-agent-hypervisor-roadmap]] — development stages
- [[src-agent-hypervisor-changelog]] — version history
- [[src-agent-hypervisor-status]] — component maturity table
- [[src-agent-hypervisor-docs-concept]] — conceptual overview and FAQ
- [[src-agent-hypervisor-docs-architecture]] — threat model and technical spec
- [[src-agent-hypervisor-docs-research]] — vs. existing solutions, case studies
- [[src-agent-hypervisor-docs-positioning]] — Crutch/Workaround/Bridge classification
- [[src-agent-hypervisor-benchmarks]] — AgentDojo results
- [[src-agent-hypervisor-pub-missing-layer]] — "The Missing Layer" article series
- [[src-agent-hypervisor-docs-adr]] — architecture decision records
