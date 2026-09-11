#!/usr/bin/env python3
"""Build readable, gated HTML pages from imported TV Cabbage Markdown records."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "content" / "posts"
OUTPUT_DIR = ROOT / "docs" / "posts"
CDX_FILE = ROOT / "data" / "wayback-cdx.json"


def linkify(value: str) -> str:
    escaped = html.escape(value)
    return re.sub(
        r"(https?://[^\s<]+)",
        r'<a href="\1" rel="noreferrer">\1</a>',
        escaped,
    )


def body_html(markdown: str) -> str:
    body = markdown.split("\n---\n\n", 1)[-1].strip()
    blocks = re.split(r"\n\s*\n", body)
    rendered: list[str] = []
    for block in blocks:
        lines = block.splitlines()
        if all(line.startswith("- ") for line in lines if line.strip()):
            items = "".join(f"<li>{linkify(line[2:])}</li>" for line in lines if line.strip())
            rendered.append(f"<ul>{items}</ul>")
            continue
        text = "<br>\n".join(linkify(line) for line in lines)
        rendered.append(f"<p>{text}</p>")
    return "\n".join(rendered)


def capture_timestamps() -> dict[str, str]:
  records = json.loads(CDX_FILE.read_text(encoding="utf-8"))[1:]
  timestamps: dict[str, str] = {}
  for timestamp, original, *_ in records:
    path = urlparse(original).path.rstrip("/") or "/"
    timestamps.setdefault(path, timestamp)
  return timestamps


def page(post: dict, body: str, timestamps: dict[str, str]) -> str:
    title = html.escape(post["title"])
    published = html.escape(post["published"] or "[unknown]")
    original_url = html.escape(post["original_url"] or "[unknown]", quote=True)
    source_url = html.escape(post["source_url"], quote=True)
    path = urlparse(post["original_url"]).path.rstrip("/") or "/"
    capture = timestamps.get(path)
    archive_url = f"https://web.archive.org/web/{capture}id_/{post['original_url']}" if capture else post["source_url"]
    return f'''<!doctype html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Archived TV Cabbage post: {title}">
  <title>{title} | TV Cabbage</title>
  <link rel="stylesheet" href="../styles.css">
</head>
<body class="post-page">
  <div class="password-gate" id="password-gate" role="dialog" aria-modal="true" aria-labelledby="gate-title">
    <div class="gate-panel">
      <p class="eyebrow">Private reconstruction</p>
      <h1 id="gate-title">TV Cabbage<br><em>archive access.</em></h1>
      <p>Enter the archive password to browse the reconstructed pages.</p>
      <form id="password-form">
        <label for="site-password">Password</label>
        <div class="gate-input"><input id="site-password" type="password" autocomplete="current-password" required><button class="button button-primary" type="submit">Enter</button></div>
        <p class="gate-error" id="password-error" role="alert" hidden>That password is not recognised.</p>
      </form>
      <a class="text-link" href="../page-list.html">View public page list <span aria-hidden="true">↗</span></a>
    </div>
  </div>
  <header class="site-header"><div class="header-inner"><a class="brand" href="../"><span class="brand-mark">TV</span><span><strong>TV Cabbage</strong><small>tVC Sound System / east Kent</small></span></a><nav class="site-nav" aria-label="Primary navigation"><a href="../#archive">Archive</a><a href="../page-list.html">Page list</a></nav></div></header>
  <main>
    <article class="post-content">
      <p class="eyebrow">Archive-derived post</p>
      <h1>{title}</h1>
      <div class="post-meta"><time>{published}</time><a href="{original_url}">{original_url}</a></div>
      <div class="post-body">{body}</div>
      <footer class="post-source"><p>Source capture: <a href="{source_url}" rel="noreferrer">archived Atom feed</a></p><p>Original page: <a href="{archive_url}" rel="noreferrer">Wayback capture ↗</a></p></footer>
    </article>
  </main>
  <footer class="site-footer"><p>TV Cabbage archive / local transcription</p><a href="../#archive">Back to archive ↗</a></footer>
  <script src="../post.js"></script>
</body>
</html>
'''


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    index = json.loads((SOURCE_DIR / "index.json").read_text(encoding="utf-8"))
    timestamps = capture_timestamps()
    for post in index:
        source = SOURCE_DIR / post["file"]
        output = OUTPUT_DIR / f"{source.stem}.html"
        output.write_text(page(post, body_html(source.read_text(encoding="utf-8")), timestamps), encoding="utf-8")
    print(f"Built {len(index)} HTML post pages in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
