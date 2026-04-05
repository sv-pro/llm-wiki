---
tags: [source]
created: 2026-04-05
updated: 2026-04-05
sources: [agent-hypervisor-contributing]
---

# Agent Hypervisor — CONTRIBUTING.md
> Contribution guide: what's welcome, what's not, and the four core design principles.

**Source:** `raw/agent-hypervisor/CONTRIBUTING.md`

---

## Summary

[[agent-hypervisor]] is an early-stage proof-of-concept. At this stage, **conceptual feedback is the most valuable contribution**. The project is not yet seeking production-readiness improvements or enterprise feature requests.

---

## Types of Contributions Welcome

| Type | How |
|------|-----|
| **Conceptual feedback** (most valuable) | GitHub Discussions — Is the abstraction compelling? Are there fundamental flaws? What attack vectors are missed? |
| **Documentation improvements** | Pull Request — clarifications, examples, analogies, diagrams, typo fixes |
| **Code examples** | Pull Request into `examples/` — integrations with agent frameworks, additional demo scenarios, physics law implementations |
| **Real-world use cases** | GitHub Issue with `use-case` label — what this would solve, what it doesn't address |

---

## Not Looking For (Yet)

- Production-readiness improvements (it's a PoC)
- Enterprise feature requests
- Performance optimizations

Focus: **validating the architectural approach**.

---

## Development Setup

```bash
git clone https://github.com/sv-pro/agent-hypervisor.git
cd agent-hypervisor
pip install pyyaml pytest
pytest
python3 demo_scenarios.py
```

---

## Code Style

- Python 3.8+, type hints on all public APIs
- Docstrings that explain **why**, not just what
- Every safety property expressible as a deterministic unit test
- Keep it minimal — this is a PoC, not a framework

---

## Core Design Principles

1. **Deterministic** — no LLM calls or probabilistic logic in the evaluation path
2. **Educational** — code should teach the concept to a new reader
3. **Testable** — every Hypervisor decision must be reproducible in a unit test
4. **Minimal** — resist abstractions not needed for the current proof-of-concept

These principles directly support the architecture described in [[four-layer-architecture]] and the [[ai-aikido]] philosophy: stochastic intelligence at design-time, deterministic enforcement at runtime.
