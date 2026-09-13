# TV Cabbage archive TODO

## Active: resolve the later Wayback publication

- [x] Preserve 101 early Blogspot posts and source snapshots.
- [x] Preserve the 25 readable posts recovered from the later Atom feed.
- [x] Inventory later article-like Wayback paths: 430 total, 25 locally matched.
- [x] Generate a durable recovery queue for the remaining 405 paths.
- [x] Fetch and inspect the first unresolved Wayback page (pipeline test).
- [x] Replace per-page shell fetching with the complete 430-entry public Blogger feed.
- [x] Extract readable title, body, publication date, labels, and media references.
- [x] Import all 405 previously unresolved source records (531 readable records total).
- [x] Begin duplicate comparison with exact normalized-body grouping.
- [ ] Record migrated/reposted pages as aliases rather than duplicate posts.
- [ ] Import genuinely new posts with capture provenance.
- [ ] Recover permitted images, audio, flyers, and downloads.
- [ ] Publish a coverage report: recovered, alias, unavailable, and pending.
- [ ] Rebuild, verify, commit, and publish the completed archive.

## Resume point

Run `python3 scripts/find-duplicate-posts.py`, review
`data/duplicate-candidates.json`, and convert verified migrated copies to aliases.

First test result: `/2009/02/1997-death-throws.html` was saved under
`data/recovered-pages/raw/`. Its capture is a Dynamic Views shell: the title and
Blogger post ID `851711165926836951` survive, but the body is not embedded.
The next extractor should query archived Blogger feed/API endpoints by post ID
and fall back to title-based alias matching against the early Blogspot corpus.
