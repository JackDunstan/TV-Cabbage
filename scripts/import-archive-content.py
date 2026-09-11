#!/usr/bin/env python3
"""Import readable TV Cabbage posts from an archived Blogger Atom feed."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen
from xml.etree import ElementTree

ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}
DEFAULT_FEED = "https://web.archive.org/web/20251206205736id_/https://www.tvcabbage.co.uk/atom.xml"


class ReadableText(HTMLParser):
    """Reduce feed HTML to readable Markdown-friendly plain text."""

    BLOCK_TAGS = {"address", "article", "br", "div", "h1", "h2", "h3", "h4", "li", "p", "pre", "section"}

    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.list_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "li":
            self.list_depth += 1
            self.parts.append("\n- ")
        elif tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag == "li":
            self.list_depth = max(0, self.list_depth - 1)
        elif tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def text(self) -> str:
        value = "".join(self.parts).replace("\xa0", " ")
        value = re.sub(r"[ \t]+", " ", value)
        value = re.sub(r"\n[ \t]+", "\n", value)
        value = re.sub(r"\n{3,}", "\n\n", value)
        return value.strip()


@dataclass
class ImportedPost:
    title: str
    published: str
    original_url: str
    source_url: str
    filename: str
    body: str


def fetch(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": "TV-Cabbage-archive-import/1.0"})
    with urlopen(request, timeout=60) as response:
        return response.read()


def slugify(value: str) -> str:
    value = value.lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "untitled"


def entry_link(entry: ElementTree.Element) -> str:
    for link in entry.findall("atom:link", ATOM_NS):
        if link.attrib.get("rel", "alternate") == "alternate" and link.attrib.get("href"):
            return link.attrib["href"]
    return ""


def text_field(entry: ElementTree.Element, name: str) -> str:
    return entry.findtext(f"atom:{name}", "", ATOM_NS).strip()


def import_feed(feed_url: str, output_dir: Path) -> list[ImportedPost]:
    root = ElementTree.fromstring(fetch(feed_url))
    output_dir.mkdir(parents=True, exist_ok=True)
    imported: list[ImportedPost] = []

    for entry in root.findall("atom:entry", ATOM_NS):
        title = text_field(entry, "title") or "Untitled post"
        original_url = entry_link(entry)
        published = text_field(entry, "published") or text_field(entry, "updated")
        content = text_field(entry, "content")
        if not content:
            content = text_field(entry, "summary")
        parser = ReadableText()
        parser.feed(html.unescape(content))
        body = parser.text()
        if not body:
            body = "[No readable body was present in the archived feed.]"
        timestamp = published[:10] or "undated"
        filename = f"{timestamp}-{slugify(title)}.md"
        source_url = feed_url
        page = (
            f"# {title}\n\n"
            f"> Imported from an archived Blogger Atom feed.\n\n"
            f"- Published: `{published or '[unknown]'}`\n"
            f"- Original URL: {original_url or '[unknown]'}\n"
            f"- Archive source: {source_url}\n"
            f"- Evidence: `archive-derived`\n\n"
            f"---\n\n{body}\n"
        )
        (output_dir / filename).write_text(page, encoding="utf-8")
        imported.append(ImportedPost(title, published, original_url, source_url, filename, body))
    return imported


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--feed-url", default=DEFAULT_FEED)
    parser.add_argument("--output", type=Path, default=Path("content/posts"))
    args = parser.parse_args()

    try:
        posts = import_feed(args.feed_url, args.output)
    except Exception as error:  # noqa: BLE001 - report network/parser failures clearly
        print(f"Could not import archive feed: {error}", file=sys.stderr)
        return 1

    index = [
        {
            "title": post.title,
            "published": post.published,
            "original_url": post.original_url,
            "source_url": post.source_url,
            "file": post.filename,
            "evidence": "archive-derived",
        }
        for post in posts
    ]
    (args.output / "index.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    print(f"Imported {len(posts)} readable posts to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
