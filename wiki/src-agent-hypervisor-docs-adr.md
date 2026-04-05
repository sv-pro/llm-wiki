---
tags: [source]
created: 2026-04-05
updated: 2026-04-05
sources: [agent-hypervisor-docs-adr]
---

# Agent Hypervisor — Architecture Decision Records
> Summaries of all six ADRs covering schema versioning, simulation fidelity, policy IR, policy language, program layer, and economic constraints.

**Sources:** `docs/adr/ADR-001` through `docs/adr/ADR-006`

---

## Summary

Six ADRs document the architectural decisions and open questions for [[agent-hypervisor]]. ADR-005 is Accepted; the rest are Open and awaiting prototype or implementation evidence.

---

## ADR-001 — Manifest Schema Versioning (v1 → v2)

**Status:** Open · **Phase:** v0.2

**Question:** Should the v2 [[world-manifest|World Manifest]] schema be a strict superset of v1 (additive, backward-compatible) or a clean break requiring explicit migration?

**Options:** A) Additive superset (v1 manifests remain valid), B) Clean break with `ahc migrate`, C) Versioned coexistence (compiler selects by `version:` field).

**Current lean:** Option B (clean break), conditional on benchmark report confirming v2 expressiveness is needed to fix specific attack categories.

---

## ADR-002 — `ahc simulate` Fidelity Model

**Status:** Open · **Phase:** v0.3

**Question:** Should `ahc simulate` execute against compiled runtime artifacts (binary fidelity) or re-interpret YAML directly (source fidelity)?

**Options:** A) Compiled artifact fidelity (true fidelity, slower iteration), B) Source/YAML fidelity (faster authoring, risk of divergence), C) Compiled with hot-reload (best of both, complex).

**Current lean:** Option A for v0.3, with a fidelity regression test in CI. Option B deferred to v0.4 if compilation latency is a friction point.

---

## ADR-003 — Policy IR: Internal vs. Stable External Interface

**Status:** Open · **Phase:** v0.4

**Question:** Should the Policy Intermediate Representation (between manifest compiler and policy backends) be treated as an internal compiler detail or stabilized as a public interface with semver guarantees?

**Options:** A) Internal (opaque), B) Stable external (semver, documented), C) Internal now, stabilize at v0.5.

**Current lean:** Option C — treat as internal during v0.4 prototype work; publish IR stability RFC alongside ADR-004 resolution.

---

## ADR-004 — Policy Language Backend: Datalog vs. Rego vs. Cedar

**Status:** Open · **Phase:** v0.4

**Question:** Which policy language should replace hand-written Python predicate tables as the primary backend for the [[world-manifest|World Policy]] engine?

**Assessment summary:**

| Language | Taint Propagation | Provenance-Aware Policy | Runtime Performance | Fit with AH |
|----------|------------------|------------------------|--------------------|----|
| Datalog | Excellent (recursive facts) | Excellent | Good (Souffle) | Highest |
| Rego (OPA) | Good | Good | Good (Wasm) | High |
| Cedar | Limited | Weak | Excellent | Medium |

**Secondary question:** Use Cedar for actor/capability authorization subset even if Datalog handles taint reasoning? (Hybrid deferred to post-v0.4.)

**Current lean:** Prototype Datalog first. If latency constraint met and no fundamental fit problems, Datalog becomes the recommendation. Rego is fallback.

---

## ADR-005 — Program Layer as Optional Execution Abstraction

**Status:** Accepted · **Phase:** v0.2 (scaffolding) → v0.3+ (implementation)

**Decision:** Introduce the Program Layer as an optional execution abstraction between policy enforcement and tool execution. Key statement: *"Programs may define how tasks are executed, but never what is possible — that remains defined by the World Kernel."*

Phase 1 introduces `ExecutionPlan` hierarchy, clean interfaces (`TaskCompiler`, `Executor` protocols), and an `ExecutionRouter` switch in the gateway. The `plan_type: "direct"` default produces byte-for-byte identical execution to the pre-extension state. `plan_type: "program"` raises `NotImplementedError` (loud by design).

**Not introduced:** sandbox implementation, LLM at runtime, `ProgramRegistry` storage, changes to `runtime/` modules.

---

## ADR-006 — Economic Constraint Integration

**Status:** Open · **Phase:** Economic Execution Control Phase 1 & 2

Three open sub-decisions:

1. **Token estimation** — heuristic (4 chars ≈ 1 token, current) vs. real tokenizer (e.g., `tiktoken`). Lean: heuristic for Phase 1; revisit at Phase 3 with empirical billing data.
2. **Session budget accumulator** — in-process (current) vs. persistent store (Redis/DB). Lean: in-process for Phase 1; persistent store deferred to Stage 3 (Beta Product).
3. **REPLAN verdict signalling** — exception-based (`BudgetExceeded` subclassing `ConstructionError`) vs. structured return (`EnforcementResult` union). Lean: exception-based for Phase 1, consistent with existing `ApprovalRequired` and `TaintViolation` patterns.

---

## Key concepts cross-referenced

- [[world-manifest]] — the manifest schema central to ADR-001 through ADR-004
- [[four-layer-architecture]] — the layers these ADRs govern
- [[taint-propagation]] — the propagation model Datalog would formalize (ADR-004)
- [[manifest-resolution]] — the Policy IR output (ADR-003)
