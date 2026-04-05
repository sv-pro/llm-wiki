---
tags: [concept]
created: 2026-04-05
updated: 2026-04-05
sources: [agent-hypervisor-pub-missing-layer, agent-hypervisor-docs-concept]
---

# AI Aikido
> Using the LLM's own stochastic capability at design-time to generate deterministic runtime artifacts — intelligence designs the physics, it does not govern individual actions at runtime.

**Primary sources:** [[src-agent-hypervisor-pub-missing-layer]] (Article 02), [[src-agent-hypervisor-docs-concept]]

---

## What It Is

AI Aikido is the central technique of [[agent-hypervisor]]: the boundary between stochastic and deterministic processing does not run between systems — it runs between *phases*. LLM intelligence is used at design-time; the runtime is deterministic.

The name references judo/aikido: redirecting the opponent's force. The LLM's own capability is used to build the deterministic structure that makes the LLM safe to deploy.

---

## The Pattern Hidden in Plain Sight

Every software developer already practices AI Aikido daily:
- GitHub Copilot (stochastic) generates code that executes deterministically in production.
- ChatGPT generates a SQL query that runs deterministically.
- Claude generates Terraform config that provisions infrastructure identically every time.

A stochastic process produces a deterministic artifact. The LLM participates in the *generation* phase; the generated artifact executes without it. The entire industry practices this without naming it.

---

## Applied to Agent Security

| Design-time (stochastic) | Runtime artifact (deterministic) |
|--------------------------|----------------------------------|
| LLM analyzes real inputs and generates injection detection patterns | Regular expressions, PEG grammars, JSON Schema validators |
| LLM generates [[world-manifest|World Manifests]] from business process descriptions | Compiled capability tables, taint state machines |
| LLM proposes taint propagation rules ("if source is email and transformation is summarize, taint is preserved") | Deterministic taint rules; human reviews and approves |

The same LLM then *attacks* the generated artifacts — adversarial inputs, edge cases, semantic ambiguity — at design-time. Generate → attack → patch → re-attack. Only the survivors are deployed.

---

## The World Manifest Compiler Pipeline

```
Human intent + LLM semantic modeling
       ↓
World Manifest (reviewed and committed by human)
       ↓
Compilation phase
       ↓
Deterministic runtime artifacts:
  - Policy lookup tables
  - JSON Schema validators
  - Taint state machines
  - Capability engines
       ↓
LLM-free enforcement
```

No LLM survives the compilation phase. Every artifact is unit-testable. Every decision reproducible.

---

## Industry Convergence Evidence

Four domains independently arrived at the same pattern:

1. **SOC bounded autonomy** — AI handles triage automatically; design-time boundary decisions amortize across all future alerts.
2. **Enterprise voice AI** — modular architecture wins over native speech-to-speech ("black box"); the text layer between transcription and synthesis enables deterministic policy.
3. **Cloudflare Moltworker** — ephemeral containers for isolated agent execution; primitive world definition.
4. **Meta's Rule of Two** — "Guardrails must live outside the LLM. Kill switches for tool calls cannot depend on model behavior alone."

---

## What AI Aikido Does NOT Solve

AI Aikido handles the design phase. It does not eliminate:
- **The semantic gap** — the LLM used at design-time to generate security parsers may miss genuinely ambiguous injections.
- **Manifest authoring errors** — a poorly generated (or reviewed) manifest produces poor security.
- **Continuous improvement** — new attack patterns require returning to the design-time phase.

---

## Connection to Design-Time HITL

AI Aikido and [[design-time-hitl]] are complementary:
- AI Aikido describes *what* the LLM generates (deterministic artifacts).
- Design-Time HITL describes *how the human reviews* those artifacts (the four-phase cycle).

Together they form the Design → Compile → Deploy → Learn → Redesign loop.

---

## Key concepts cross-referenced

- [[world-manifest]] — the primary artifact generated via AI Aikido
- [[design-time-hitl]] — the human review phase of the cycle
- [[four-layer-architecture]] — the layers that AI Aikido artifacts populate
- [[taint-propagation]] — taint rules are a compiled AI Aikido artifact
- [[manifest-resolution]] — the deterministic policy evaluation at runtime
