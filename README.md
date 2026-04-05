# llm-wiki

A pattern for building personal knowledge bases using LLMs.

*Inspired by [Andrej Karpathy's LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).*

## The core idea

Most people's experience with LLMs and documents looks like RAG: you upload a collection of files, the LLM retrieves relevant chunks at query time, and generates an answer. This works, but the LLM is rediscovering knowledge from scratch on every question. There's no accumulation.

The idea here is different. Instead of just retrieving from raw documents at query time, the LLM **incrementally builds and maintains a persistent wiki** — a structured, interlinked collection of markdown files that sits between you and the raw sources. When you add a new source, the LLM reads it, extracts the key information, and integrates it into the existing wiki — updating entity pages, revising topic summaries, noting where new data contradicts old claims, strengthening or challenging the evolving synthesis. The knowledge is compiled once and then *kept current*, not re-derived on every query.

**The wiki is a persistent, compounding artifact.** The cross-references are already there. The contradictions have already been flagged. The synthesis already reflects everything you've read.

You never (or rarely) write the wiki yourself — the LLM writes and maintains all of it. You're in charge of sourcing, exploration, and asking the right questions.

## Architecture

```
llm-wiki/
├── README.md       # This file
├── AGENTS.md       # Schema: tells the LLM how to maintain this wiki
├── raw/            # Your curated source documents (immutable)
│   └── assets/     # Images and attachments referenced by sources
└── wiki/           # LLM-generated markdown files
    ├── index.md    # Content catalog — updated on every ingest
    └── log.md      # Append-only chronological log of all operations
```

**Raw sources** (`raw/`) — your curated collection of source documents: articles, papers, images, data files. These are immutable — the LLM reads from them but never modifies them.

**The wiki** (`wiki/`) — a directory of LLM-generated markdown files: summaries, entity pages, concept pages, comparisons, an overview, a synthesis. The LLM owns this layer entirely.

**The schema** (`AGENTS.md`) — tells the LLM how the wiki is structured, what the conventions are, and what workflows to follow when ingesting sources, answering questions, or maintaining the wiki.

## Operations

**Ingest.** Drop a new source into `raw/` and tell the LLM to process it. The LLM reads the source, discusses key takeaways, writes a summary page in the wiki, updates `wiki/index.md`, updates relevant entity and concept pages, and appends an entry to `wiki/log.md`.

**Query.** Ask questions against the wiki. The LLM reads `wiki/index.md` first to find relevant pages, drills into them, and synthesizes an answer with citations. Good answers can be filed back into the wiki as new pages — explorations compound in the knowledge base just like ingested sources do.

**Lint.** Periodically ask the LLM to health-check the wiki: look for contradictions, stale claims, orphan pages, missing cross-references, and data gaps.

## Getting started

1. Clone this repo and open it in [Obsidian](https://obsidian.md) (the wiki folder makes a great vault).
2. Open your LLM agent (Claude Code, OpenAI Codex, etc.) in the repo directory — it will read `AGENTS.md` automatically.
3. Drop a source file into `raw/` and tell the agent: *"Ingest `raw/<filename>`"*.
4. Browse the results in Obsidian, follow the links, check the graph view.

## Tips

- **Obsidian Web Clipper** converts web articles to markdown — great for quickly getting sources into `raw/`.
- **Obsidian graph view** shows what's connected to what, which pages are hubs, and which are orphans.
- The wiki is just a git repo of markdown files — you get version history, branching, and collaboration for free.
- For larger wikis, [qmd](https://github.com/tobi/qmd) provides local hybrid BM25/vector search over markdown files with an MCP server interface.
- **Marp** (Obsidian plugin) renders markdown as slide decks — useful for generating presentations from wiki content.