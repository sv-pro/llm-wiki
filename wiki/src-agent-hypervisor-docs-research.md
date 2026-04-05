---
tags: [source]
created: 2026-04-05
updated: 2026-04-05
sources: [agent-hypervisor-docs-research]
---

# Agent Hypervisor — Research Docs
> Comparative analysis against existing solutions, vulnerability case studies, workarounds, references, and timeline.

**Sources:** `docs/research/vs-existing-solutions.md`, `docs/research/vulnerability-case-studies.md`, `docs/research/workarounds.md`, `docs/research/references.md`, `docs/research/timeline.md`, `docs/research/case_studies/MS_COPILOT_DLP_BYPASS.md`

---

## Summary

The research documentation establishes the architectural thesis through evidence: existing defenses fail structurally, real-world vulnerabilities are architecturally predictable, and practical workarounds can bridge the gap while AH matures.

---

## vs. Existing Solutions

All major current approaches are compared against AH across security model, failure mode, and determinism:

| Approach | Problem | Agent Hypervisor Response |
|----------|---------|--------------------------|
| System Prompts / Alignment | 78.5% bypass in multi-turn; LLM can't reliably distinguish instruction from data | Input virtualization — injections never enter the agent's world |
| Guardrails / Output Filtering | 95–99% bypass under adaptive attacks; encoding/semantic bypass | Virtualization replaces filtering entirely |
| Policy Engines | Operates at wrong abstraction level; confused deputy attacks | Ontological security — dangerous actions are absent, not forbidden |
| Sandboxing | Protects infrastructure, not semantics; prompt injection still works inside | Complementary — AH adds semantic isolation to infrastructure isolation |
| Monitoring / Detection | Reactive; data already exfiltrated by the time monitoring fires | Complementary — AH prevents; monitoring audits |

See [[crutch-workaround-bridge]] for the evaluation framework.

---

## Vulnerability Case Studies

Every major AI agent vulnerability follows the same structural pattern: agent in raw reality → attacker exploits direct access → probabilistic filter added → filter bypassed. **"We're surprised by gravity."**

Key cases:

- **[[zombie-agent]] (Radware, Jan 2026)** — Persistent memory poisoning via email. Root cause: no provenance on memory writes. AH fix: ProvenanceLaw + TaintContainmentLaw.
- **ShadowLeak (Radware, 2025)** — Single crafted email exfiltrates entire Gmail inbox. Root cause: no trust boundary, no [[taint-propagation]].
- **Prompt Injection (Universal)** — Hidden commands in processed text. OpenAI: "unlikely to ever be fully solved." AH: injection stripped at virtualization boundary.
- **Tool Exfiltration** — Sensitive data sent via whitelisted tool. Root cause: no data-flow taint tracking. AH: [[taint-propagation|TaintContainmentLaw]] blocks regardless of tool whitelist.

---

## MS Copilot DLP Bypass (Case Study)

For four weeks (January 2026), Microsoft 365 Copilot Chat read emails marked "Confidential" despite DLP policies. Tracked as CW1226324. Previously: EchoLeak (CVE-2025-32711) — a zero-click prompt injection bypassing Copilot's classifier.

Two incidents, two different vectors, same root cause: all security controls lived *inside* the same platform. When the platform broke, everything broke simultaneously.

Microsoft's own fix hint — Restricted Content Discovery (RCD): remove sensitive SharePoint sites from Copilot's retrieval pipeline entirely. This is a primitive form of Input Virtualization — the data doesn't exist in the agent's world, so there's nothing to bypass.

---

## Practical Workarounds

Six tactical patterns for immediate partial protection (20–80%), ordered by implementation effort:

1. **Input Classification** (30 min, 20–30%) — tag inputs with source and trust level at ingestion.
2. **Memory Provenance Tracking** (4 hrs, 40–50%) — record source of every memory write; forensic, not preventive.
3. **Read-Only Tool Wrappers** (15 min/tool) — eliminate accidental side effects during development.
4. **Segregated Memory** (4 hrs, 60–70%) — separate memory into trust-level zones.
5. **Taint Tracking** (1 day, 50–60%) — attach taint labels and check before external boundary crossings.
6. **Audit Logging** (1 day, reactive) — immutable append-only record of every agent action with provenance.

Maximum combined stack: ~75–80% against non-adaptive attacks. Each workaround maps directly to its AH equivalent (e.g., taint tracking → [[taint-propagation|TaintContainmentLaw]]).

---

## Timeline

Key industry milestones relevant to AH development:

- **Jan 8, 2026** — Radware ZombieAgent disclosure
- **Feb 13, 2026** — Dario Amodei: continuous learning breakthrough in 1–2 years (which makes memory attacks permanent)
- **Feb 14, 2026** — Agent Hypervisor public launch

---

## Key concepts cross-referenced

- [[zombie-agent]] — the ZombieAgent attack
- [[taint-propagation]] — TaintContainmentLaw
- [[crutch-workaround-bridge]] — the evaluation framework
- [[camel-defense]] — CaMeL comparison
- [[four-layer-architecture]] — the architectural response
