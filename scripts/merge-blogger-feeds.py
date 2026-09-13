#!/usr/bin/env python3
"""Merge overlapping paginated Blogger JSON feed responses."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("feeds", nargs="+", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    documents = [json.loads(path.read_text(encoding="utf-8")) for path in args.feeds]
    feed = documents[0]["feed"]
    entries = {}
    for document in documents:
        for entry in document["feed"].get("entry", []):
            entries[entry["id"]["$t"]] = entry
    feed["entry"] = sorted(entries.values(), key=lambda entry: entry["published"]["$t"], reverse=True)
    feed["openSearch$totalResults"]["$t"] = str(len(entries))
    args.output.write_text(json.dumps({"version": "1.0", "encoding": "UTF-8", "feed": feed}, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Merged {len(entries)} unique entries")


if __name__ == "__main__":
    main()
