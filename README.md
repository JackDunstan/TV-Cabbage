# TV Cabbage archive

This is a closed preservation repository containing material recovered from the former TV Cabbage publications at `tvcabbage.blogspot.com` and `tvcabbage.co.uk`.

No further collection, reconstruction, maintenance, or development is planned by the repository holder. The files are retained in their current state so that the material remains findable and recoverable by its rights holder.

## Purpose

This repository is not presented as a new publication, authorised edition, or commercial use of TV Cabbage. It exists only as a preservation copy and discovery aid for content that was publicly available through Blogger and the Internet Archive.

The repository holder does **not** assert copyright ownership over the archived posts, comments, names, artwork, photographs, recordings, or other source material. Copyright and all related rights remain with their respective authors and rights holders. Inclusion here does not grant a licence to reuse third-party material.

A rights holder wishing to identify or recover material can use the source URLs and provenance records included with each post. A rights holder may also request correction, attribution, transfer, or removal through the repository's normal contact or issue channel.

## What is included

The repository currently contains:

- **531 readable post records** represented as Markdown source records and generated HTML pages.
- **101 posts** exposed by the earlier TV Cabbage Blogspot feed, published between 12 January 2005 and 10 September 2007.
- **430 post records** exposed by the later `tvcabbage.co.uk` Blogger feed. This set includes the 25 records originally recovered from an archived Atom feed.
- **One surviving public reader comment**, linked to its source post.
- A Wayback CDX inventory containing **535 HTML records across 531 unique URL paths**, including **430 article-like paths**.
- Public Blogger feed snapshots, a mobile-homepage snapshot, the recovered favicon, archive metadata, source URLs, timestamps, and evidence labels.
- A static browsing copy under [`docs/`](docs/) and repeatable import/build scripts under [`scripts/`](scripts/).

Some of the 531 records may be migrated or republished versions of earlier posts. Six exact-body duplicate groups covering 12 records were identified, but these have not been manually resolved into aliases. They remain separate source records so no evidence is discarded.

## What is not included

This is not a complete reproduction of either historical website. It does not include, except where a source snapshot happens to contain them:

- Most original photographs, flyers, illustrations, avatars, or other image assets.
- Audio, DJ mixes, video, downloadable files, or externally hosted embeds.
- Comments other than the single comment still exposed by the public comments feed.
- Deleted, private, draft, unindexed, or feed-excluded posts.
- Material from captures or backups that were never publicly indexed.
- The complete historical Blogger theme, client-side Dynamic Views behaviour, widgets, navigation state, analytics, or interactive services.
- Reliable category or label data where the surviving feeds did not expose it.
- Manual resolution of reposts, changed publication dates, aliases, broken external links, or conflicting metadata.

Additional material may still exist in Blogger account exports, the Internet Archive, search-engine caches, personal backups, old computers or drives, email attachments, social-media accounts, hosting accounts, or copies held by authors, photographers, contributors, event organisers, and readers. This repository makes no claim that such material has been exhausted or that the present collection is definitive.

## Provenance

Every readable record retains its original or archived source URL and an evidence label. The principal source sets are:

- The public feed for the earlier `tvcabbage.blogspot.com` publication.
- The public Blogger feed associated with the later `tvcabbage.co.uk` publication.
- [Internet Archive captures of `tvcabbage.co.uk`](https://web.archive.org/web/20260000000000*/http://www.tvcabbage.co.uk/).

Detailed provenance is recorded in [`data/archive-manifest.json`](data/archive-manifest.json), while [`content/source-site.md`](content/source-site.md) describes the earlier Blogspot publication.

## Repository map

- [`content/posts/`](content/posts/): readable post records.
- [`content/posts/index.json`](content/posts/index.json): merged 531-record post index.
- [`content/comments/index.json`](content/comments/index.json): the surviving comment record.
- [`data/archive-manifest.json`](data/archive-manifest.json): sources, collection dates, and archive scope.
- [`data/duplicate-candidates.json`](data/duplicate-candidates.json): unresolved exact-body duplicate groups.
- [`docs/`](docs/): generated static browsing copy.
- [`scripts/`](scripts/): preservation and build utilities retained for reproducibility.

## Status

**Archival work has ended.** The repository is preserved as-is. Its remaining scripts, queue, and TODO records document how the collection was produced and what remained unresolved; they are not a commitment to further work.

The static site's password prompt is only a client-side presentation gate. It is not security, and all committed source material remains publicly accessible.
