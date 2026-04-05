"""Wiki page loading, WikiLink rendering, search."""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import frontmatter
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.toc import TocExtension

WIKI_DIR = Path(os.environ.get("WIKI_DIR", "wiki"))
WIKILINK_RE = re.compile(r"\[\[([^\|\]]+?)(?:\|([^\]]+?))?\]\]")

TAG_ORDER = ["entity", "concept", "source", "comparison", "synthesis", "query"]


@dataclass
class PageMeta:
    slug: str
    title: str
    tag: str
    summary: str
    updated: str
    tags: list[str] = field(default_factory=list)
    sources: list[str] = field(default_factory=list)
    created: str = ""


@dataclass
class SearchResult:
    meta: PageMeta
    score: int
    excerpt: str


def _wikilink_to_md(m: re.Match) -> str:
    target = m.group(1).strip()
    label = (m.group(2) or m.group(1)).strip()
    return f"[{label}](/wiki/{target})"


def _make_md() -> markdown.Markdown:
    return markdown.Markdown(
        extensions=[
            FencedCodeExtension(),
            CodeHiliteExtension(css_class="highlight", guess_lang=False, noclasses=False),
            TocExtension(permalink=True, toc_depth="2-4"),
            "tables",
            "admonition",
            "attr_list",
            "def_list",
        ],
    )


def _extract_title(content: str) -> str:
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return ""


def _extract_summary(content: str) -> str:
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("> "):
            return stripped[2:].strip()
    return ""


def _parse_tags(raw) -> list[str]:
    if isinstance(raw, list):
        return [str(t) for t in raw]
    if isinstance(raw, str):
        return [raw]
    return []


def load_page_meta(path: Path) -> Optional[PageMeta]:
    try:
        post = frontmatter.load(str(path))
        slug = path.stem
        title = _extract_title(post.content) or slug.replace("-", " ").title()
        summary = _extract_summary(post.content)
        tags = _parse_tags(post.get("tags", []))
        tag = next((t for t in tags if t in TAG_ORDER), tags[0] if tags else "other")
        sources = _parse_tags(post.get("sources", []))
        updated = str(post.get("updated", post.get("created", "")))
        created = str(post.get("created", ""))
        return PageMeta(
            slug=slug,
            title=title,
            tag=tag,
            summary=summary,
            updated=updated,
            tags=tags,
            sources=sources,
            created=created,
        )
    except Exception:
        return None


def get_all_pages(wiki_dir: Path = WIKI_DIR) -> list[PageMeta]:
    pages = []
    for path in sorted(wiki_dir.glob("*.md")):
        meta = load_page_meta(path)
        if meta:
            pages.append(meta)
    return pages


def group_pages(pages: list[PageMeta]) -> dict[str, list[PageMeta]]:
    groups: dict[str, list[PageMeta]] = {}
    for p in sorted(pages, key=lambda x: x.title.lower()):
        g = p.tag if p.tag in TAG_ORDER else "other"
        groups.setdefault(g, []).append(p)
    ordered = {k: groups[k] for k in TAG_ORDER if k in groups}
    if "other" in groups:
        ordered["other"] = groups["other"]
    return ordered


def render_page(slug: str, wiki_dir: Path = WIKI_DIR) -> tuple[PageMeta, str]:
    path = wiki_dir / f"{slug}.md"
    if not path.exists():
        raise FileNotFoundError(f"Page not found: {slug}")
    post = frontmatter.load(str(path))
    body = WIKILINK_RE.sub(_wikilink_to_md, post.content)
    md = _make_md()
    html = md.convert(body)
    meta = load_page_meta(path)
    if not meta:
        raise ValueError(f"Failed to parse page: {slug}")
    return meta, html


def search_pages(
    query: str, pages: list[PageMeta], wiki_dir: Path = WIKI_DIR
) -> list[SearchResult]:
    q = query.lower()
    results = []
    for meta in pages:
        path = wiki_dir / f"{meta.slug}.md"
        try:
            post = frontmatter.load(str(path))
            text = post.content
            score = 0
            if q in meta.title.lower():
                score += 10
            if q in meta.summary.lower():
                score += 5
            if q in text.lower():
                score += 1
            if score:
                idx = text.lower().find(q)
                start = max(0, idx - 80)
                end = min(len(text), idx + 200)
                lead = "…" if start > 0 else ""
                tail = "…" if end < len(text) else ""
                excerpt = lead + text[start:end].replace("\n", " ") + tail
                results.append(SearchResult(meta=meta, score=score, excerpt=excerpt))
        except Exception:
            continue
    return sorted(results, key=lambda r: -r.score)


def read_pages_for_context(
    slugs: list[str], wiki_dir: Path = WIKI_DIR, max_chars: int = 24_000
) -> str:
    parts = []
    total = 0
    for slug in slugs:
        path = wiki_dir / f"{slug}.md"
        try:
            text = path.read_text(encoding="utf-8")
            if total + len(text) > max_chars:
                text = text[: max_chars - total]
            parts.append(f"=== {slug}.md ===\n{text}")
            total += len(text)
            if total >= max_chars:
                break
        except Exception:
            continue
    return "\n\n".join(parts)
