---
tags: [concept]
created: 2026-04-05
updated: 2026-04-05
sources: [agent-hypervisor-whitepaper, agent-hypervisor-docs-architecture, agent-hypervisor-changelog]
---

# Taint Propagation
> The mechanism by which data contamination from untrusted sources spreads through all derived values, enforced by the TaintContainmentLaw which prevents tainted data from triggering external side effects.

**Primary sources:** [[src-agent-hypervisor-docs-architecture]], [[src-agent-hypervisor-whitepaper]], [[src-agent-hypervisor-zombie-agent-scenario]]

---

## What It Is

Taint propagation is the core data-flow security mechanism of [[agent-hypervisor]]. Every value that enters the system from an untrusted source is marked "tainted," and that taint label propagates monotonically through all derived values — it can never be removed except through an explicit sanitization gate defined in the [[world-manifest|World Manifest]].

**Key invariant:** Taint is monotonically joined. A derived value inherits the *least-trusted* provenance class among all its parents. Wrapping an external value does not launder it.

---

## The ValueRef Model

Every value in the system is wrapped in a `ValueRef`:

```python
@dataclass
class ValueRef:
    id: str                         # unique identifier
    value: Any                      # the actual value
    provenance: ProvenanceClass     # where it came from
    roles: list[Role]               # intended use in the task
    parents: list[str]              # ids of parent ValueRefs
    source_label: str               # human-readable origin
```

Agents never work with raw strings for values used in tool arguments. Every such value is a `ValueRef`.

---

## Provenance Classes (Least → Most Trusted)

| Class | Meaning |
|-------|---------|
| `external_document` | Content from files, emails, web pages, API responses |
| `derived` | Computed or extracted from parent values (inherits least-trusted parent) |
| `user_declared` | Explicitly declared by the operator in the task manifest |
| `system` | Hardcoded by the system — no user influence possible |

**Key invariant:** Provenance can only flow from less trusted to more trusted through *explicit operator declaration*, not through computation.

---

## Derivation DAG and Chain Resolution

Parent relationships form a **directed acyclic graph (DAG)**. `resolve_chain(ref, registry)` returns all ancestors of a `ValueRef` in BFS order. The chain is used to:
1. Detect untrusted ancestry — does any ancestor have `external_document`?
2. Find declared sources — does any ancestor have `user_declared` with the required role?
3. Compute effective trust — the least-trusted ancestor dominates (RULE-03).

---

## The TaintContainmentLaw

> Tainted data cannot reach Layer 5 (the Execution Boundary) without an explicit sanitization gate defined in the World Manifest.

This is enforced as a **physics law**, not a policy check — the route from tainted data to external action does not exist in the architecture. It is the primary defense against data exfiltration attacks (e.g., [[zombie-agent]]).

---

## Mixed Provenance and Anti-Laundering (RULE-03)

A value has **mixed provenance** when its chain contains ancestors from more than one provenance class. The less-trusted source always dominates.

**Recipient laundering attempt (blocked):**
```
doc_ref (external_document) → addr_extracted (derived, external_document ancestor)
contacts_ref (user_declared) → combined (derived, parents=[addr_extracted, contacts_ref])
```
Even though `contacts_ref` is trusted, the `external_document` ancestor dominates. RULE-01 fires: deny. The combination does not produce a trusted value.

---

## Overtainting vs. Undertainting Problem

Two failure modes:
- **Overtainting** — marking values as tainted when they're not (e.g., tainting all tool outputs unconditionally). Reduces utility (false positives block legitimate actions). Fixed in [[src-agent-hypervisor-benchmarks|AgentDojo refactor]] by switching to detection-driven taint seeding.
- **Undertainting** — failing to propagate taint through a transformation. Creates exfiltration paths.

The refactored implementation seeds taint only when injection patterns are detected, and propagates taint to specific argument values (not globally to all calls).

---

## Trace Output

Decision traces show the full provenance chain:

```
tool: send_email
arg [to] provenance: derived:extracted from malicious_doc.txt <- external_document:malicious_doc.txt
verdict: deny
reason: Recipient traces to external_document — cannot authorize outbound email
rules: RULE-01, RULE-02
```

---

## Cross-Session Taint ([[zombie-agent]] Scenario)

Taint metadata is preserved in memory records. A memory object written from an `UNTRUSTED` source carries that taint into every future session that reads it. When Session 2 loads memory written from an untrusted email in Session 1, the provenance chain is intact: `action derived from memory[taint=true, origin=untrusted_email, written=session_1] → DENY`.

---

## Key concepts cross-referenced

- [[world-manifest]] — defines the taint rules and sanitization gates
- [[manifest-resolution]] — the ALLOW/DENY/ASK verdict derived from taint state
- [[zombie-agent]] — the primary scenario demonstrating cross-session taint
- [[four-layer-architecture]] — Layer 3 enforces taint; Layer 1 assigns initial taint
- [[agentdojo-benchmark]] — benchmark measuring taint effectiveness
