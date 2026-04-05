# Wiki Log

Append-only chronological record of all operations. Never delete or edit past entries.

Each entry header format: `## [YYYY-MM-DD] <operation> | <title>`

Grep the last 5 entries: `grep "^## \[" wiki/log.md | tail -5`

---

## [2026-04-05] edit | Initial wiki created

- Wiki initialized with empty index and log.
- Schema defined in `AGENTS.md`.
