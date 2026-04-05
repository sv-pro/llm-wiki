# LLM Wiki — Agent Schema

This document is the schema for the LLM Wiki. It tells you (the LLM agent) how this wiki is structured, what the conventions are, and exactly what to do when ingesting sources, answering queries, or maintaining the wiki.

Read this file at the start of every session.

---

## Directory layout

```
raw/            # Immutable source documents — never modify these
raw/assets/     # Images and attachments referenced by raw sources
wiki/           # You own this directory — create, update, delete pages freely
wiki/index.md   # Master content catalog — update on every ingest
wiki/log.md     # Append-only chronological log — append on every operation
```

---

## Wiki page conventions

- All wiki pages are **markdown** (`.md`).
- Use `[[WikiLink]]` syntax for internal links (Obsidian-compatible).
- Add YAML frontmatter to every page you create:

  ```yaml
  ---
  tags: [entity | concept | source | comparison | synthesis | query]
  created: YYYY-MM-DD
  updated: YYYY-MM-DD
  sources: [source-slug-1, source-slug-2]
  ---
  ```

- Page filenames: lowercase, hyphen-separated (e.g. `neural-scaling-laws.md`).
- Keep pages focused — one entity or concept per page. Prefer many small pages over a few large ones.
- Always add a one-line summary at the top of each page, just below the H1 title, as a blockquote:

  ```markdown
  # Neural Scaling Laws
  > Power-law relationships between model performance, dataset size, and compute.
  ```

---

## Page types

| Type | Purpose | Naming convention |
|------|---------|-------------------|
| `source` | Summary of a single raw source | `src-<slug>.md` |
| `entity` | A person, organization, product, or dataset | `<name>.md` |
| `concept` | An idea, technique, or topic | `<concept>.md` |
| `comparison` | Side-by-side analysis of related items | `cmp-<a>-vs-<b>.md` |
| `synthesis` | Cross-cutting analysis or thesis | `syn-<topic>.md` |
| `query` | A notable Q&A filed back into the wiki | `q-<slug>.md` |

---

## index.md format

`wiki/index.md` is the master catalog. Keep it organized by page type. Format each entry as:

```markdown
## Sources
- [[src-slug]] — One-line summary. (YYYY-MM-DD)

## Entities
- [[entity-name]] — One-line summary.

## Concepts
- [[concept-name]] — One-line summary.

## Comparisons
- [[cmp-a-vs-b]] — One-line summary.

## Syntheses
- [[syn-topic]] — One-line summary.

## Queries
- [[q-slug]] — One-line summary. (YYYY-MM-DD)
```

When answering a query, read `wiki/index.md` first to identify relevant pages, then drill into them.

---

## log.md format

`wiki/log.md` is append-only. **Never delete or edit past entries.** Each entry header must follow this exact format so it is grep-parseable:

```
## [YYYY-MM-DD] <operation> | <title>
```

Where `<operation>` is one of: `ingest`, `query`, `lint`, `edit`.

Example:

```markdown
## [2026-04-05] ingest | Attention Is All You Need

- Source: `raw/attention-is-all-you-need.pdf`
- Pages created: [[src-attention-is-all-you-need]], [[transformer]], [[multi-head-attention]], [[positional-encoding]]
- Pages updated: [[index]], [[deep-learning]]
- Key takeaways: Introduced the Transformer architecture; replaced RNNs with self-attention.
```

---

## Ingest workflow

When the user says "ingest `raw/<file>`":

1. **Read** the source file (and any referenced images if needed).
2. **Discuss** key takeaways with the user if they are present; otherwise proceed.
3. **Create** a `src-<slug>.md` summary page in `wiki/`.
4. **Create or update** entity and concept pages touched by the source.
5. **Note contradictions**: if the source contradicts an existing page, add a `> ⚠️ Contradiction:` callout to both pages.
6. **Update** `wiki/index.md` with all new and modified pages.
7. **Append** an entry to `wiki/log.md`.

A single source may touch 10–15 wiki pages. That's expected and desirable.

---

## Query workflow

When the user asks a question:

1. Read `wiki/index.md` to identify relevant pages.
2. Read the relevant pages.
3. Synthesize an answer with `[[WikiLink]]` citations.
4. **Ask the user** whether to file the answer back as a `query` page in the wiki. If yes, create `wiki/q-<slug>.md` and update the index and log.

---

## Lint workflow

When the user asks for a lint / health check:

1. Read all pages in `wiki/`.
2. Report:
   - **Contradictions** between pages.
   - **Stale claims** likely superseded by newer sources.
   - **Orphan pages** with no inbound `[[links]]`.
   - **Missing pages** — concepts mentioned but lacking their own page.
   - **Missing cross-references** — pages that should link to each other but don't.
   - **Data gaps** that a web search could fill.
3. For each issue, propose a fix and ask the user whether to apply it.
4. Append a lint entry to `wiki/log.md`.

---

## General rules

- **Never modify files in `raw/`.**
- **Never truncate `wiki/log.md`** — it is append-only.
- Keep `wiki/index.md` complete and up to date — it is the LLM's navigation tool.
- Prefer updating existing pages over creating new ones when the content is closely related.
- Use consistent terminology across pages — introduce redirects (short pages that just link elsewhere) when the same concept appears under multiple names.
- If unsure whether to create a new page or update an existing one, ask the user.
