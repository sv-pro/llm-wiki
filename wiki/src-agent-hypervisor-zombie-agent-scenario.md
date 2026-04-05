---
tags: [source]
created: 2026-04-05
updated: 2026-04-05
sources: [agent-hypervisor-zombie-scenario]
---

# Agent Hypervisor — ZombieAgent Scenario
> Canonical reference for how AH breaks the ZombieAgent cross-session memory-poisoning attack at three independent boundaries.

**Source:** `raw/agent-hypervisor/scenarios/zombie-agent/SCENARIO.md`

---

## Summary

[[zombie-agent]] (Radware, January 2026) is a multi-step, cross-session attack where malicious instructions enter agent memory through untrusted input and survive across sessions, turning the agent into a persistent threat actor.

Agent Hypervisor breaks this attack at **three independent boundaries**:

1. **Input Virtualization** — untrusted input never reaches the agent as raw text.
2. **Provenance-gated Memory Write** — tainted data cannot enter persistent memory.
3. **Taint Propagation across sessions** — memory written from tainted sources carries taint into every future session.

No single boundary needs to be perfect. Together they make the attack **structurally impossible** — not probabilistically unlikely.

---

## Attack Chain (Without Agent Hypervisor)

```
Session 1: email arrives → agent reads raw email containing hidden instruction
  → agent writes instruction to persistent memory (no provenance check)
Session 2+: agent loads memory → malicious instruction loaded as trusted context
  → agent forwards user data to attacker → no anomaly detected
```

Root causes: no trust tagging, no provenance on memory write, no cross-session taint propagation, unrestricted exfiltration path.

---

## Three Evolutionary Steps

### Step 1 — Single Session: Prompt Injection → DENY
The hidden email instruction proposes `send_email` to an external address. AH identifies the source as untrusted, applies the [[taint-propagation|TaintContainmentLaw]], and returns **DENY** — the `external_side_effects` capability is absent for untrusted sources.

### Step 2 — Memory Write: Provenance-Gated Persistence
Data derived from untrusted email carries taint. The manifest rule forbids tainted data being written to persistent memory without explicit user approval. In interactive mode: **ASK** with one-shot vs. manifest-extension choice. In background mode: **DENY**.

### Step 3 — Cross-Session: Taint Survives in Memory
Assume Step 2 was approved as one-shot, with taint metadata preserved in the memory record. Session 2 loads the memory. The loaded record carries `taint: true, source: untrusted_email, session: 1`. Any proposed `send_email` derived from this memory gets **DENY** — the cross-session provenance chain is explicit in the trace.

---

## Manifest Resolution (Applied to This Scenario)

```
proposed action
  ├── explicit allow in manifest          → ALLOW
  ├── explicit deny in manifest           → DENY
  ├── invariant violation                 → DENY (TaintContainmentLaw, etc.)
  └── not covered by manifest
        ├── interactive mode              → ASK → one-shot or manifest extension
        └── background mode              → DENY
```

See [[manifest-resolution]] for the full ALLOW / DENY / ASK framework.

---

## Success Criteria (Unit Tests)

| Test | Expected |
|------|---------|
| untrusted_email → proposed `send_email` | DENY (TaintContainmentLaw) |
| untrusted_email → proposed `write_memory` | ASK (interactive) / DENY (background) |
| memory[taint=true] → proposed `send_email` | DENY (cross-session) |
| trusted_user → proposed `send_email` | ALLOW |
| same manifest + same input | same decision (determinism) |
| action not in manifest | ASK / DENY |

All six tests run without an LLM. All decisions are reproducible.

---

## Key concepts cross-referenced

- [[zombie-agent]] — the attack itself
- [[taint-propagation]] — TaintContainmentLaw enforcement
- [[manifest-resolution]] — the ALLOW / DENY / ASK decision rule
- [[world-manifest]] — the scenario manifest structure
- [[design-time-hitl]] — the ASK → manifest-extension workflow
