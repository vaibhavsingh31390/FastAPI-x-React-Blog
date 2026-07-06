import markdown as markdown_lib
import bleach

from database.models.post import ContentMode


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


def render_post_content(content_mode: ContentMode, content: str) -> str | None:
    if content_mode == ContentMode.html:
        return _render_html(content)
    if content_mode == ContentMode.markdown:
        return _render_markdown(content)
    if content_mode == ContentMode.components:
        return None
    raise ValueError(f"Unsupported content mode: {content_mode}")
