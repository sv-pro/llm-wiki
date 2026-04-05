---
tags: [source]
created: 2026-04-05
updated: 2026-04-05
sources: [agent-hypervisor-docs-architecture]
---

# Agent Hypervisor — Architecture Docs
> Technical architecture: threat model, execution governance, provenance model, and formal specifications.

**Sources:** `docs/architecture/threat-model.md`, `docs/architecture/execution_governance.md`, `docs/architecture/provenance_model.md`, `docs/architecture/architecture.md`, `docs/architecture/hello-world.md`, `docs/architecture/one_pager.md`, `docs/architecture/technical-spec.md`

---

## Summary

The architecture documentation covers the full technical specification of [[agent-hypervisor]]: where the virtualization boundary is, how trust is assigned, how provenance is tracked, how the enforcement pipeline operates, and what the formal guarantees are.

---

## Threat Model

The virtualization boundary is the single point through which all external signals must pass before reaching the agent. Key properties:

- Everything passes through it — no raw input reaches the agent.
- It is deterministic — same input produces the same Semantic Event, always.
- It is the only place taint is assigned. Once assigned, [[taint-propagation|taint propagates]] automatically.
- It contains no LLM.

**Trust channels** define what inputs are trusted at the *channel* level, not content level:

| Channel | Trust Level | Notes |
|---------|------------|-------|
| `user` | TRUSTED | Highest trust by default |
| `email` | UNTRUSTED | Fully attacker-controlled |
| `web` | UNTRUSTED | Includes scraped data |
| `file` | SEMI_TRUSTED | Depends on provenance |
| `MCP` | SEMI_TRUSTED | Tool-specific, see manifest |
| `agent-to-agent` | UNTRUSTED | No transitive trust escalation |

Trust level cannot be upgraded by the agent — only the [[world-manifest|World Manifest]] can define trust levels.

**In-scope threats:** prompt injection, tainted egress (data exfiltration), tool abuse, poisoned tool outputs (MCP injection), memory poisoning.

**Out-of-scope:** semantic ambiguity at boundary, finite manifest completeness, host system compromise, World Manifest design errors, LLM model vulnerabilities.

---

## Execution Governance

The enforcement pipeline (from `execution_governance.md`):

```
Agent / LLM Runtime
  → POST /tools/execute {tool, arguments with provenance}
  ↓
Agent Hypervisor Gateway
  1. Resolve provenance chains (full derivation DAG)
  2. PolicyEngine.evaluate() (declarative YAML rules)
  3. ProvenanceFirewall.check() (structural rules)
  4. Combine verdicts: deny > ask > allow
  5. Write TraceEntry (always — all verdicts)
  ↓
deny (403) | ask (approval_id) | allow (execute adapter)
  ↓
TraceStore / ApprovalStore / PolicyStore
```

**Provenance classes** (trust order, least → most):
- `external_document` — files, emails, web pages (untrusted)
- `derived` — computed from parents (inherits least-trusted parent)
- `user_declared` — declared by operator in task (trusted)
- `system` — hardcoded, no user influence (most trusted)

**Three-way verdict:** `allow` (execute), `deny` (block + trace), `ask` (hold for human review). All three produce immutable trace entries.

---

## Provenance Model

See [[taint-propagation]] for the full concept page. Key structures:

**ValueRef** — every value carries: unique id, actual value, provenance class, roles, parent ids, and source label. Agents never work with raw strings for tool arguments.

**Sticky provenance (RULE-03):** a derived value inherits the least-trusted provenance class among its parents. Wrapping an external value does not launder it.

**Recipient laundering example:** combining an attacker-embedded address (`external_document`) with a trusted contacts file (`user_declared`) produces a derived value with `external_document` ancestry — the combination is denied.

**Trace output format:** `tool: send_email | arg [to] provenance: derived:extracted from malicious_doc.txt <- external_document:malicious_doc.txt | verdict: deny`

---

## Critical Path (No LLM)

```
Raw input → [L1] Trust classification + taint + injection stripping
  → Semantic Event → [L3] Agent perceives → Agent produces Intent Proposal
  → [L4] Deterministic World Policy evaluation
  → allow | deny | require_approval | simulate
  → [L5] If allowed: tool invocation + immutable audit log
```

No LLM appears on this path. The critical path is unit-testable end-to-end without mocking the agent.

---

## Bounded Security Claim

AH does not claim perfect security. It claims **bounded, measurable security**: the attack surface has an explicit shape, both contact points (Layer 1 and Layer 5) are auditable and improvable, and failure modes are engineering debt (incomplete manifest) rather than probabilistic drift (unknown bypass rates).

---

## Key concepts cross-referenced

- [[world-manifest]] — the manifest artifact driving compilation
- [[taint-propagation]] — the provenance model and TaintContainmentLaw
- [[manifest-resolution]] — the three-way verdict
- [[four-layer-architecture]] — the layered defense
- [[zombie-agent]] — primary threat scenario
- [[design-time-hitl]] — human review at design time
