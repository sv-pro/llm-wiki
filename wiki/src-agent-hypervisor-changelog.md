---
tags: [source]
created: 2026-04-05
updated: 2026-04-05
sources: [agent-hypervisor-changelog]
---

# Agent Hypervisor — Changelog
> Version history from v0.1 (concept) through v0.4 (auditable execution governance).

**Source:** `raw/agent-hypervisor/CHANGELOG.md`

---

## Summary

Four releases progressing from conceptual model to a full execution governance stack.

## v0.1 — Concept and Model

Initial release. Established the provenance data model, problem statement, and architectural framing. Defined the threat model covering prompt injection and data exfiltration.

## v0.2 — Provenance Firewall MVP

Introduced the core provenance model: `ValueRef`, derivation chains, and mixed provenance. Implemented `ProvenanceFirewall` with five structural rules (RULE-01 through RULE-05). Shipped an end-to-end firewall demo in three modes: unprotected, protected, and trusted source.

## v0.3 — Policy Engine and Gateway Infrastructure

Added a declarative YAML policy engine with hot-reload, a FastAPI gateway server with a full HTTP API, a Python client library (`GatewayClient`), storage layer (trace store, approval store, policy store), and a LangChain integration example.

## v0.4 — Auditable Execution Governance Showcase

The most complete release. Key additions:

- **Tool Gateway / Execution Switch** — a single enforcement point (`POST /tools/execute`) between the agent and external systems. Framework-agnostic.
- **Provenance-based policy enforcement** — every tool argument carries a provenance label; the policy engine evaluates the full derivation chain and produces a three-way verdict: `allow`, `deny`, or `ask`.
- **Approval workflow** — `ask` verdicts hold the tool pending human review. Approval records are persistent across restarts.
- **Persisted traces** — every decision produces an immutable entry in `.data/traces.jsonl`, linked to the exact policy version in force.
- **Policy version history** — every policy load is versioned; decisions are post-hoc auditable to the exact rules in force at decision time. Hot-reloadable via `POST /policy/reload`.
- **MCP adapter shim** — wraps the gateway as a Model Context Protocol server, allowing Claude Desktop and Cursor to delegate tool governance without code changes.
- **Showcase demo** — covers safe read (allow), prompt injection attempt (deny), and sensitive action requiring approval (ask → approve → execute).
- **365 tests** across 13 test files.

## Key concepts introduced

- [[four-layer-architecture]] — the layered execution model
- [[taint-propagation]] — provenance tracking across derivation chains
- [[manifest-resolution]] — the ALLOW / DENY / ASK decision rule
- [[world-manifest]] — the compiled policy artifact
