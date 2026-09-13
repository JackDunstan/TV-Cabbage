#!/usr/bin/env python3
"""Create/update the unresolved Wayback article recovery queue."""

from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CDX = ROOT / "data" / "wayback-cdx.json"
POSTS = ROOT / "content" / "posts" / "index.json"
QUEUE = ROOT / "data" / "recovery-queue.json"


def path(url: str) -> str:
    return urlparse(url).path.rstrip("/") or "/"


def main() -> None:
    records = json.loads(CDX.read_text(encoding="utf-8"))[1:]
    local_paths = {path(post["original_url"]) for post in json.loads(POSTS.read_text(encoding="utf-8"))}
    previous = {item["path"]: item for item in json.loads(QUEUE.read_text(encoding="utf-8"))} if QUEUE.exists() else {}
    captures: dict[str, tuple[str, str]] = {}
    for timestamp, original, *_ in records:
        article_path = path(original)
        parts = [part for part in article_path.split("/") if part]
        if article_path.endswith(".html") and len(parts) >= 3:
            captures.setdefault(article_path, (timestamp, original))
    queue = []
    for article_path, (timestamp, original) in sorted(captures.items()):
        if article_path in local_paths:
            continue
        item = previous.get(article_path, {})
        item.update({
            "path": article_path,
            "timestamp": timestamp,
            "original_url": original,
            "capture_url": f"https://web.archive.org/web/{timestamp}id_/{original}",
        })
        item.setdefault("status", "pending")
        item.setdefault("notes", "")
        queue.append(item)
    QUEUE.write_text(json.dumps(queue, indent=2) + "\n", encoding="utf-8")
    print(f"Recovery queue: {len(queue)} unresolved article paths")


if __name__ == "__main__":
    main()
