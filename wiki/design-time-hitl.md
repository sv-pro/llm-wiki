---
tags: [concept]
created: 2026-04-05
updated: 2026-04-05
sources: [agent-hypervisor-pub-missing-layer, agent-hypervisor-docs-concept]
---

# Design-Time Human-in-the-Loop
> Amortizing human judgment at design-time by reviewing World Manifests rather than individual runtime decisions — O(log n) cost instead of O(n).

**Primary sources:** [[src-agent-hypervisor-pub-missing-layer]] (Article 03), [[src-agent-hypervisor-docs-concept]]

---

## What It Is

Design-Time Human-in-the-Loop (Design-Time HITL) is the governance model used by [[agent-hypervisor]]: humans review and approve the [[world-manifest|World Manifest]] — which defines what actions exist, which inputs are trusted, and what the budget limits are — rather than reviewing individual runtime decisions.

**The economics argument:** Runtime HITL is O(n). Every decision costs the same human attention. One agent: manageable. A hundred agents processing thousands of requests: impossible.

Design-Time HITL is O(log n) per iteration covering *n* decisions. Each manifest review covers exponentially more runtime cases than a per-action review.

---

## The Constitution Analogy

A constitution is expensive to draft, but the cost amortizes across every citizen and every moment of governance. No one reviews every transaction against the full text of the law in real-time.

The World Manifest functions identically: one design-time review covers all runtime executions until the manifest is updated.

---

## The Scale Problem

Evidence:
- Enterprise SOC: 10,000 alerts/day; teams handle only 22%; 60%+ admit ignoring alerts that later proved critical.
- CrowdStrike: 51-second AI breakout times — runtime review is already too slow.
- Gartner: 40%+ of agentic AI projects predicted to be canceled by 2027 — not from technical failure, but inadequate governance at scale.
- Anthropic Opus 4.6: evades its own monitor 18% of the time in SHADE-Arena. Runtime monitoring has a ceiling.

---

## Three Modes of Human Oversight

| Mode | Role | Frequency |
|------|------|-----------|
| **Design-Time** | Reviews and approves World Manifests, taint rules, capability matrices | Once per manifest version |
| **Runtime Exception** | `require_approval` gate for actions not covered by manifest | Edge cases only; frequent firing = manifest underdefined |
| **Iteration-Time** | Analyzes runtime logs, approves LLM-generated manifest updates | Per improvement cycle |

Runtime `ASK` is a pressure-relief valve, not the primary oversight mechanism. If it fires frequently, the [[world-manifest|World Manifest]] is underdefined — that's feedback triggering a design-time iteration, not a governance process.

---

## The Four-Phase Cycle

```
DESIGN     → Human + LLM co-create the World Manifest
              Action schemas, trust policies, taint rules
              Human reviews and commits

COMPILE    → Manifest → deterministic artifacts
              Policy tables, validators, taint matrices
              No LLM survives. All unit-testable.

DEPLOY     → Pure deterministic runtime
              No LLM, no human. Reproducible and auditable.

LEARN      → Runtime logs reveal patterns:
              "47 escalations on rule X this week"
              "Zero bypasses on parser set Z"
              ↓
REDESIGN   → Human analyzes + LLM generates updated rules
              Tests run. Escalations drop. Loop continues.
```

---

## [[ai-aikido]] Connection

Design-Time HITL and [[ai-aikido]] are two sides of the same coin:
- AI Aikido describes *what* the LLM generates (deterministic artifacts from stochastic design-time intelligence).
- Design-Time HITL describes *how the human reviews* those artifacts (the four-phase cycle).

The human is not removed from the loop — they are placed at the *most leveraged point* in the loop.

---

## Contrast with Runtime HITL

**Runtime HITL (current industry default):**
- Human reviews individual tool calls before execution
- Cost: O(n) — proportional to agent activity
- Failure modes: approval fatigue, rubber-stamping, impractical at scale

**Design-Time HITL:**
- Human reviews the World Manifest
- Cost: O(log n) — amortized across all runtime sessions
- Failure modes: incomplete manifest coverage (bounded, detectable, fixable)

---

## Key concepts cross-referenced

- [[world-manifest]] — the artifact humans review at design-time
- [[ai-aikido]] — the LLM-powered generation phase
- [[manifest-resolution]] — the runtime decisions that design-time review governs
- [[four-layer-architecture]] — Layers 1–2 are the design-time artifacts
- [[crutch-workaround-bridge]] — Design-Time HITL is a Bridge-level approach
