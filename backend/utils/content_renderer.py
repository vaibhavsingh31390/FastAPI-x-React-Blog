import html
import subprocess
from pathlib import Path

import bleach
import markdown as markdown_lib

from database.models.post import ContentMode
from database.schema.content_blocks import ContentBlock, parse_blocks_content

SSR_DIR = Path(__file__).resolve().parent.parent / "ssr"

ALLOWED_HTML_TAGS = frozenset(
    {
        "a",
        "blockquote",
        "br",
        "code",
        "em",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "hr",
        "img",
        "li",
        "ol",
        "p",
        "pre",
        "strong",
        "ul",
    }
)
ALLOWED_HTML_ATTRIBUTES = {
    "a": ["href", "title", "target", "rel", "class"],
    "img": ["src", "alt", "title", "loading", "width", "height"],
}


def _render_html(content: str) -> str:
    return bleach.clean(
        content,
        tags=ALLOWED_HTML_TAGS,
        attributes=ALLOWED_HTML_ATTRIBUTES,
        strip=True,
    )


def _render_markdown(content: str) -> str:
    return markdown_lib.markdown(content, extensions=["extra", "sane_lists"])


def _render_block_fallback(block: ContentBlock) -> str:
    props = block.props
    if block.type == "heading":
        level = max(1, min(6, int(props.get("level", 2))))
        text = html.escape(str(props.get("text", "")))
        return f"<h{level}>{text}</h{level}>"
    if block.type == "paragraph":
        text = html.escape(str(props.get("text", "")))
        return f"<p>{text}</p>"
    if block.type == "cta":
        label = html.escape(str(props.get("label", "")))
        href = html.escape(str(props.get("href", "#")))
        return f'<a href="{href}" class="content-cta">{label}</a>'
    if block.type == "image":
        src = html.escape(str(props.get("src", "")))
        alt = html.escape(str(props.get("alt", "")))
        return f'<img src="{src}" alt="{alt}" loading="lazy">'
    raise ValueError(f"Unsupported block type: {block.type}")


def _render_blocks_fallback(content: str) -> str:
    blocks = parse_blocks_content(content)
    return "".join(_render_block_fallback(block) for block in blocks)


def _render_blocks_node(content: str) -> str:
    result = subprocess.run(
        ["node", str(SSR_DIR / "render.mjs")],
        input=content,
        capture_output=True,
        text=True,
        cwd=SSR_DIR,
        check=False,
    )
    if result.returncode != 0:
        message = result.stderr.strip() or "Node SSR failed"
        raise RuntimeError(message)
    return result.stdout


def render_post_content(
    content_mode: ContentMode,
    content: str,
    *,
    use_node_ssr: bool = True,
) -> str:
    if content_mode == ContentMode.html:
        return _render_html(content)
    if content_mode == ContentMode.markdown:
        return _render_markdown(content)
    if content_mode == ContentMode.blocks:
        if use_node_ssr:
            return _render_blocks_node(content)
        return _render_blocks_fallback(content)
    raise ValueError(f"Unsupported content mode: {content_mode}")
