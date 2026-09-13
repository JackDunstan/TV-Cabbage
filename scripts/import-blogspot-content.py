#!/usr/bin/env python3
"""Import readable posts from the live TV Cabbage Blogspot JSON feed."""

from __future__ import annotations

import argparse
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path

DEFAULT_FEED = "https://tvcabbage.blogspot.com/feeds/posts/default?alt=json&max-results=500"


class ReadableText(HTMLParser):
    """Reduce Blogger HTML to readable, Markdown-friendly plain text."""

    BLOCK_TAGS = {"address", "article", "br", "div", "h1", "h2", "h3", "h4", "li", "p", "pre", "section"}

    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "li":
            self.parts.append("\n- ")
        elif tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def text(self) -> str:
        value = "".join(self.parts).replace("\xa0", " ")
        value = re.sub(r"[ \t]+", " ", value)
        value = re.sub(r"\n[ \t]+", "\n", value)
        value = re.sub(r"\n{3,}", "\n\n", value)
        return value.strip()


def slugify(value: str) -> str:
    value = value.lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "untitled"


def value(record: dict, key: str) -> str:
    return record.get(key, {}).get("$t", "").strip()


def alternate_link(entry: dict) -> str:
    return next((link["href"] for link in entry.get("link", []) if link.get("rel") == "alternate"), "")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("feed", type=Path, help="Downloaded Blogger JSON feed")
    parser.add_argument("--source-url", default=DEFAULT_FEED)
    parser.add_argument("--output", type=Path, default=Path("content/posts"))
    parser.add_argument("--index", type=Path, default=Path("content/posts/index.json"))
    args = parser.parse_args()

    feed = json.loads(args.feed.read_text(encoding="utf-8"))["feed"]
    expected = int(value(feed, "openSearch$totalResults") or 0)
    entries = feed.get("entry", [])
    if expected and len(entries) != expected:
        raise SystemExit(f"Feed declared {expected} posts but supplied {len(entries)}")

    args.output.mkdir(parents=True, exist_ok=True)
    existing = json.loads(args.index.read_text(encoding="utf-8")) if args.index.exists() else []
    by_url = {post["original_url"]: post for post in existing}

    for entry in entries:
        title = value(entry, "title") or "Untitled post"
        published = value(entry, "published") or value(entry, "updated")
        original_url = alternate_link(entry)
        if original_url in by_url and by_url[original_url].get("evidence") == "archive-derived":
            continue
        content = value(entry, "content") or value(entry, "summary")
        reader = ReadableText()
        reader.feed(html.unescape(content))
        body = reader.text() or "[No readable body was present in the source feed.]"
        url_slug = Path(original_url.split("?", 1)[0]).stem
        filename_slug = url_slug if title == "Untitled post" else slugify(title)
        filename = f"{published[:10] or 'undated'}-{filename_slug}.md"
        page = (
            f"# {title}\n\n"
            f"> Imported from the public TV Cabbage Blogspot feed.\n\n"
            f"- Published: `{published or '[unknown]'}`\n"
            f"- Original URL: {original_url or '[unknown]'}\n"
            f"- Source: {args.source_url}\n"
            f"- Evidence: `source-derived`\n\n"
            f"---\n\n{body}\n"
        )
        (args.output / filename).write_text(page, encoding="utf-8")
        by_url[original_url] = {
            "title": title,
            "published": published,
            "original_url": original_url,
            "source_url": args.source_url,
            "file": filename,
            "evidence": "source-derived",
        }

    merged = sorted(by_url.values(), key=lambda post: post["published"], reverse=True)
    args.index.write_text(json.dumps(merged, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Processed {len(entries)} Blogspot posts; merged index contains {len(merged)} posts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
