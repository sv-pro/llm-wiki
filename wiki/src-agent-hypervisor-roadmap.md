---
tags: [source]
created: 2026-04-05
updated: 2026-04-05
sources: [agent-hypervisor-roadmap]
---

# Agent Hypervisor — Roadmap
> Development plan from architectural concept to working code, organized in stages and versioned milestones.

**Source:** `raw/agent-hypervisor/ROADMAP.md`

---

## The Development Cycle

```
Design ──▶ Compile ──▶ Deploy ──▶ Learn ──▶ Redesign
```

LLM participates only in **Design**. Phases 2–4 are fully deterministic and LLM-free.

---

## Three Maturity Stages

### Stage 1 — Proof of Concept ✅ Complete

`src/hypervisor.py` (~200 lines, PyYAML only) proves:
- Deterministic policy evaluation with no LLM on the critical path
- Tool whitelisting as ontological boundary
- Cumulative state limits (budget enforcement)
- Unit-testable safety properties

### Stage 2 — Executable Proof ✅ Complete

Three milestones:

**M2 — Core Engine** — World Manifest schema v1, compiler CLI, taint rule compiler, Semantic Event model, Intent Proposal API, provenance graph, reversibility classification.

**M3 — Tool Boundary** — MCP proxy skeleton, tools as virtualized devices, capability matrix enforcement, taint-aware egress control.

**M4 — Proof** — Benchmarks and demos. Results: **0.0% Attack Success Rate** and **80.0% utility** under attack on 560-pair AgentDojo workspace benchmark (gpt-4o-mini-2024-07-18), matching [[camel-defense|CaMeL]]'s ASR with no LLM on the security path.

### Stage 3 — Beta Product 🟠 In Progress

| Deliverable | Status |
|---|---|
| Docker local stack | Present |
| Web UI | Pending (#32) |
| Hello-world tutorial | Complete |
| Positioning and comparisons | Complete |

---

## Versioned Roadmap (v0.2 → v0.4)

### v0.2 — High-Resolution World Manifest

**Theme:** From coarse action ontology to precise world modeling.

New [[world-manifest]] schema v2 adds: `Entity`, `Actor`, `DataClass`, `TrustZone`, `SideEffectSurface`, `TransitionPolicy`, `ConfirmationClass`, `ObservabilitySpec` types. Enables data-flow policies, not just action-level permissions.

### v0.3 — World Manifest Designer / Compiler / Tuner

**Theme:** From manual YAML authoring to a HITL toolchain.

New CLI commands: `ahc validate`, `ahc simulate`, `ahc diff`, `ahc coverage`, `ahc tune`, `ahc draft` (LLM-assisted manifest drafting). Closes the Design → Compile → Learn → Redesign loop without editing source code.

### v0.4 — Policy Language Experimentation

**Theme:** From hand-written YAML rules to a principled rule-engine foundation.

Evaluates Datalog, Rego (OPA), and Cedar as policy language backends. **Recommendation: Datalog first** — taint propagation maps naturally to recursive Datalog rules; manifest = extensional database; 7-step validation = derivation.

| Property | Datalog | Rego | Cedar |
|---|---|---|---|
| Taint propagation | Excellent | Good | Limited |
| Provenance-aware policy | Excellent | Good | Weak |
| AH concepts fit | Highest | High | Medium |

---

## Program Layer Evolution

The Program Layer is an optional execution abstraction above the World Kernel for task execution via structured programs. Key constraint: programs define *how* tasks execute; the World Kernel always defines *what* is possible.

Phases: 0 (Locked Core ✅), 1 (Minimal Task Compiler Scaffold ✅), further phases planned.

---

## Related pages

[[agent-hypervisor]] · [[world-manifest]] · [[world-manifest-compiler]] · [[four-layer-architecture]] · [[camel-defense]] · [[taint-propagation]] · [[design-time-hitl]]
