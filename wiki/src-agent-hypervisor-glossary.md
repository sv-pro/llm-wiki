---
tags: [source]
created: 2026-04-05
updated: 2026-04-05
sources: [agent-hypervisor-glossary]
---

# Agent Hypervisor — Glossary
> Authoritative term definitions derived from scenarios (primarily the ZombieAgent scenario).

**Source:** `raw/agent-hypervisor/GLOSSARY.md`

---

## Core Pipeline Terms

**Semantic Event** — A structured representation of an input, produced at the virtualization boundary. Never raw text. Always carries: `source`, `trust_level`, `tainted`, `sanitized_payload`. The agent only ever sees Semantic Events — never raw reality.

**Proposed Action** — A structured request from the agent to affect the world. The agent cannot act directly. It proposes. The [[agent-hypervisor|Hypervisor]] decides. Format: `action_type`, `parameters`, `provenance_chain`.

**Manifest Resolution** — The deterministic process of evaluating a Proposed Action against the [[world-manifest|World Manifest]]. Produces exactly one of: `ALLOW`, `DENY`, `ASK`. No LLM involved. Same input → same output, always. See [[manifest-resolution]].

---

## World Definition Terms

**[[world-manifest|World Manifest]]** — The formal specification of everything that exists in the agent's universe. Defines: trust channels, capabilities per trust level, permitted actions and their schemas, invariants, escalation conditions, provenance requirements. Not a config file — a *constitution*.

**Manifest Extension** — The act of adding a new explicit rule to the World Manifest in response to an ASK. Distinct from one-shot approval: extension changes the world permanently. Requires human review.

**Action Ontology** — The set of actions that *exist* in the agent's world, as defined by the World Manifest. Actions outside the ontology cannot be proposed — they do not exist.

---

## Trust & Taint Terms

**Trust Level** — A property of an input *channel*, not of content. Defined in the World Manifest per source: `trusted`, `untrusted`, `derived`. `derived` means trust is inherited from the provenance chain of source data.

**[[taint-propagation|Taint]]** — A property of data indicating it originated (directly or transitively) from an untrusted source. Taint is not a label that can be removed by the agent. It propagates through transformations.

**Provenance Chain** — The full lineage of a data object: original source, trust level at origin, all transformations applied, sessions crossed. Required on every memory write. The mechanism by which taint survives session boundaries.

---

## Capability Terms

**Capability** — A named permission class that must be present for an action to be allowed. Capabilities are granted per trust level, not per tool. Examples: `read`, `internal_write`, `memory_write`, `external_side_effects`. An action requiring a capability absent from the current trust context is denied — not filtered, but ontologically unavailable.

**Capability Matrix** — The mapping of trust levels to capability sets, defined in the World Manifest. Compiled into a static lookup table at manifest compilation time.

---

## Invariant Terms

**Invariant** — A physics law of the agent's world. Cannot be overridden by manifest rules. Always enforced *before* manifest lookup. Violation → immediate DENY.

**TaintContainmentLaw** — Invariant: tainted data cannot trigger `external_side_effects`. Enforcement: DENY regardless of manifest rules or user approval.

**ProvenanceLaw** — Invariant: `memory_write` requires provenance metadata. Unconditionally rejected without provenance.

**CapabilityBoundaryLaw** — Invariant: an action cannot execute without the required capability in the current trust context.

---

## Resolution Outcomes

**ALLOW** — Explicitly permitted by manifest; no invariant violations. Executes immediately, logged with full provenance.

**DENY** — Explicitly denied by manifest, or violates an invariant. Does not execute. Logged with specific rule triggered.

**ASK** — Not covered by manifest; no invariant violations. Available in interactive mode only. In background mode, uncovered actions resolve to DENY.

---

## Execution Modes

**Workflow Definition Mode** — Human defines and extends the agent's world. Produces or updates the World Manifest.

**Interactive Execution Mode** — Agent executes within the defined world, user present. Uncovered actions → ASK.

**Background Execution Mode** — Agent executes without user. Only explicitly allowed actions execute. Uncovered actions → DENY.

---

## Architecture Boundary Terms

**Core** — The hypervisor framework. Implements manifest loading, manifest resolution, [[taint-propagation|taint propagation]], provenance tracking, capability lookup, invariant enforcement. Zero dependency on Demo.

**Demo** — The scenario runner. Implements specific scenarios, user interaction, visualization. Depends on Core via defined interface.

---

## Related pages

[[agent-hypervisor]] · [[world-manifest]] · [[manifest-resolution]] · [[taint-propagation]] · [[four-layer-architecture]] · [[zombie-agent]]
