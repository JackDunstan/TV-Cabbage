# TV Cabbage archive

A source-led repository for preserving and rebuilding the former `tvcabbage.co.uk` website.

## What is verified

The Internet Archive records 71 captures of the homepage between 22 May 2017 and 3 January 2026. The latest successfully inspected HTML identifies the site as a Blogger publication:

- Title: **TV Cabbage**
- Description: `tVC Sound System provide free parties, playing deep dubbed out house and techno music, to the people of east Kent...`
- Platform: Blogger
- Template: Blogger Dynamic Views
- Initial view: `timeslide`
- Layout: 960px content frame with a 310px right rail
- Canonical URL: `http://www.tvcabbage.co.uk/`

The archived HTML is structurally sparse because Blogger Dynamic Views populated the page with client-side requests. Missing post text, media, and navigation labels are therefore marked as unknown instead of being invented.

## Repository layout

- [`content/homepage.md`](content/homepage.md): verified homepage transcription and observations.
- [`content/posts/`](content/posts/): 25 readable posts recovered from the archived Atom feed.
- [`data/archive-manifest.json`](data/archive-manifest.json): capture provenance and known archive endpoints.
- [`docs/information-architecture.md`](docs/information-architecture.md): reconstructed content model and navigation hypotheses.
- [`prompts/rebuild-website.md`](prompts/rebuild-website.md): prompts for rebuilding the site in stages.
- [`scripts/collect-wayback.sh`](scripts/collect-wayback.sh): repeatable CDX collection script for when the archive is available.

## GitHub Pages publication

The publishable site lives in [`docs/index.html`](docs/index.html). A public route directory is available at [`docs/page-list.html`](docs/page-list.html). The archive presentation uses the password `tvcabbage`.

GitHub Pages is a static host and cannot provide real password protection. The gate is client-side presentation access only; source files, JavaScript, and the CDX data remain publicly fetchable. Do not put private or sensitive material in this repository.

## Research source

Primary source: [Wayback Machine wildcard](https://web.archive.org/web/20260000000000*/http://www.tvcabbage.co.uk/)

The source URL is retained exactly as supplied because it is part of the provenance. Do not treat the proposed IA as a complete historical crawl until the URL inventory has been collected and reviewed.

## Suggested next collection pass

```sh
./scripts/collect-wayback.sh
```

The script writes a raw CDX JSON response to `data/wayback-cdx.json`. Review each discovered URL, then add page or post transcriptions under `content/` with its capture timestamp and source URL.

## Rebuild principles

1. Preserve the archive's language and uncertainty.
2. Keep source captures separate from reconstructed presentation.
3. Recreate the publication's music and free-party context without inventing event dates or artist information.
4. Prefer a searchable chronological archive plus category/label navigation over a generic marketing homepage.
5. Keep media rights and provenance attached to every imported asset.
