#!/usr/bin/env python3
"""Find exact-body duplicate posts that should become URL aliases."""
import hashlib, json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
posts = json.loads((ROOT/'content/posts/index.json').read_text())
groups = {}
for post in posts:
    text = (ROOT/'content/posts'/post['file']).read_text().split('\n---\n\n',1)[-1]
    normalized = re.sub(r'\s+', ' ', text).strip().casefold()
    if len(normalized) >= 80:
        groups.setdefault(hashlib.sha256(normalized.encode()).hexdigest(), []).append(post)
duplicates = [items for items in groups.values() if len(items) > 1]
(ROOT/'data/duplicate-candidates.json').write_text(json.dumps(duplicates, indent=2, ensure_ascii=False)+'\n')
print(f'{len(duplicates)} exact-body groups covering {sum(map(len, duplicates))} records')
