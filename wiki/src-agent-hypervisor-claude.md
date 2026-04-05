---
tags: [source]
created: 2026-04-05
updated: 2026-04-05
sources: [agent-hypervisor-claude]
---

# Agent Hypervisor — CLAUDE.md (Dev Guide)
> Developer reference: repo structure, four-layer architecture, setup, and key conventions.

**Source:** `raw/agent-hypervisor/CLAUDE.md`

---

## Summary

The dev guide for working in the Agent Hypervisor codebase. Primary audience: AI coding assistants and contributors. The core thesis: AI agent security should be addressed at the architecture level through deterministic enforcement, not probabilistic guardrails.

**Current version:** 0.2.0 · **Python:** ≥3.10

---

## Repository Structure

| Directory | Purpose |
|-----------|---------|
| `src/agent_hypervisor/runtime/` | Layer 3: Execution governance kernel |
| `src/agent_hypervisor/compiler/` | Layer 1: World Manifest compiler & CLI |
| `src/agent_hypervisor/authoring/` | Layer 2: Capability DSL and policy presets |
| `src/agent_hypervisor/hypervisor/` | Hypervisor PoC, gateway, policy engine |
| `src/agent_hypervisor/program_layer/` | Optional: task compilation & workflow |
| `src/agent_hypervisor/economic/` | Economic constraints (cost/budget enforcement) |
| `docs/` | Architecture docs, whitepapers, ADRs |
| `examples/` | Runnable demonstrations |
| `research/` | AgentDojo benchmarks, traces, reports |
| `archive/`, `lab/` | Historical/experimental — do not modify |

---

## Four-Layer Architecture

See [[four-layer-architecture]] for the full concept page.

| Layer | Name | Location | Purpose |
|-------|------|----------|---------|
| 0 | Execution Physics | (planned) | Container/network isolation |
| 1 | Base Ontology | `compiler/` | World Manifest schema & compiler |
| 2 | Dynamic Ontology | `authoring/` | Capability DSL & policy presets |
| 3 | Execution Governance | `runtime/` | IRBuilder, taint, provenance, approvals |

**Execution flow:** `world_manifest.yaml` → `compile_world()` → `CompiledPolicy` (frozen) → `Channel` → `IRBuilder` → `Executor` → worker subprocess.

---

## Core Safety Mechanisms

- **IntentIR** — sealed object; cannot be constructed outside `IRBuilder`.
- **IRBuilder.build()** — all constraints checked at construction time.
- **TaintedValue** — every value is tainted; taint is monotonically joined, never removed. See [[taint-propagation]].
- **Process boundary** — handlers run in a separate subprocess; policy evaluation in the main process.
- **SafeMCPProxy** — in-path enforcement for all MCP tool calls.
- **PolicyEngine** — evaluates provenance firewall rules from `default_policy.yaml`.

---

## Development Setup & Tests

```bash
pip install -e .
pytest                          # all tests
pytest tests/runtime/           # layer-specific
```

Test configuration is in `pyproject.toml`. Import path quirk: `pythonpath = ["src/agent_hypervisor"]`, so tests import submodules directly (e.g., `from runtime.ir import IRBuilder`).

---

## CLI Tools

Two entry points (same `compiler/cli.py`): `awc` (Agent World Compiler) and `ahc` (Agent Hypervisor Compiler).

```bash
awc run --scenario safe
awc compile --manifest path/to/manifest.yaml
awc profile --trace path/to/trace.json
awc render --manifest path/to/manifest.yaml
```

---

## Key Conventions

- No LLM on the execution path — compile-time decisions only.
- Enforce at construction time (`IRBuilder.build()`), not at call time.
- Taint is never dropped. Removing taint propagation is a security regression.
- `CompiledPolicy` is immutable once created.
- Process boundary is a hard invariant.

---

## What NOT to Do

- Do not add LLM calls to `runtime/`.
- Do not bypass `IRBuilder` to construct `IntentIR` directly.
- Do not remove or weaken taint propagation without an ADR.
- Do not modify `archive/` or `lab/`.
- Do not add probabilistic filtering to the runtime layer.

---

## Key concepts cross-referenced

- [[world-manifest]] — the World Manifest compilation pipeline
- [[taint-propagation]] — how taint is maintained
- [[four-layer-architecture]] — the layered design
- [[ai-aikido]] — design-time LLM for deterministic runtime artifacts
- [[design-time-hitl]] — human review at design time
