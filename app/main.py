"""LLM Wiki — FastAPI web application."""
from __future__ import annotations

import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from pygments.formatters import HtmlFormatter

from . import llm, wiki as w

WIKI_DIR = Path(os.environ.get("WIKI_DIR", "wiki"))
BASE_DIR = Path(__file__).parent

_PYGMENTS_CSS = (
    HtmlFormatter(style="github-dark").get_style_defs(".highlight")
    + "\n"
    + HtmlFormatter(style="default").get_style_defs(".highlight-light")
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.wiki_dir = WIKI_DIR
    app.state.pages = w.get_all_pages(WIKI_DIR)
    app.state.sidebar = w.group_pages(app.state.pages)
    app.state.llm_enabled = llm.is_configured()
    yield


app = FastAPI(title="LLM Wiki", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


def _ctx(request: Request, **kwargs) -> dict:
    return {
        "sidebar_groups": request.app.state.sidebar,
        "llm_enabled": request.app.state.llm_enabled,
        **kwargs,
    }


# ── Static assets ─────────────────────────────────────────────────────────────

@app.get("/pygments.css", include_in_schema=False)
async def pygments_css():
    return Response(content=_PYGMENTS_CSS, media_type="text/css")


# ── Pages ─────────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def home():
    return RedirectResponse(url="/wiki/index")


@app.get("/pages", response_class=HTMLResponse)
async def list_pages(request: Request):
    return templates.TemplateResponse(
        request, "list.html",
        context=_ctx(request, title="All Pages", pages=request.app.state.pages, current_slug=None),
    )


@app.get("/wiki/{slug}", response_class=HTMLResponse)
async def page(request: Request, slug: str):
    try:
        meta, html = w.render_page(slug, request.app.state.wiki_dir)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Page '{slug}' not found")
    return templates.TemplateResponse(
        request, "page.html",
        context=_ctx(request, title=meta.title, meta=meta, html=html, current_slug=slug),
    )


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, q: str = ""):
    results = (
        w.search_pages(q, request.app.state.pages, request.app.state.wiki_dir) if q else []
    )
    return templates.TemplateResponse(
        request, "search.html",
        context=_ctx(
            request,
            title=f"Search: {q}" if q else "Search",
            query=q,
            results=results,
            current_slug=None,
        ),
    )


# ── LLM query ─────────────────────────────────────────────────────────────────

@app.get("/ask", response_class=HTMLResponse)
async def ask_form(request: Request):
    if not request.app.state.llm_enabled:
        raise HTTPException(status_code=404, detail="LLM not configured")
    return templates.TemplateResponse(
        request, "query.html",
        context=_ctx(request, title="Ask the Wiki", current_slug=None),
    )


class QueryRequest(BaseModel):
    question: str


@app.post("/api/ask")
async def api_ask(req: QueryRequest, request: Request):
    if not request.app.state.llm_enabled:
        raise HTTPException(status_code=503, detail="LLM not configured")

    wiki_dir = request.app.state.wiki_dir
    pages = request.app.state.pages

    # Find most relevant pages; always include index for orientation
    results = w.search_pages(req.question, pages, wiki_dir)
    relevant = [r.meta.slug for r in results[:6]]
    if "index" not in relevant:
        relevant.insert(0, "index")

    context = w.read_pages_for_context(relevant, wiki_dir)
    system = (
        "You are an assistant for an LLM-maintained markdown wiki. "
        "Answer the user's question using only the wiki pages provided. "
        "Cite pages by name when you reference them, e.g. [[page-slug]]. "
        "Be concise and accurate.\n\n"
        f"WIKI PAGES:\n{context}"
    )
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": req.question},
    ]

    async def generate():
        try:
            async for chunk in llm.stream_query(messages):
                # Escape any SSE control characters in the chunk
                safe = chunk.replace("\n", "\\n")
                yield f"data: {safe}\n\n"
        except Exception as exc:
            yield f"data: [ERROR] {exc}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@app.get("/api/llm-status")
async def llm_status():
    ok, message = await llm.health_check()
    return {"ok": ok, "message": message}
