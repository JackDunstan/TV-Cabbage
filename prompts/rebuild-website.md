# Prompts for rebuilding TV Cabbage

Use these prompts with a coding agent after adding more captured content. Each prompt assumes the source files in this repository are authoritative and that unknown values must remain unknown.

## 1. Build the content model

> Read `README.md`, `content/`, `data/archive-manifest.json`, and `docs/information-architecture.md`. Create a typed content model for archived posts, events, media items, and links. Every record must retain its original URL, Wayback capture timestamp, evidence level, and media provenance. Do not invent missing fields or content. Add focused tests for parsing and validation.

## 2. Import a capture set

> Inspect `data/wayback-cdx.json` and the archived URLs it lists. Extract only content that is present in the captures. Create one source record per post or page under `content/`, preserve original wording, and attach the exact capture URL. Report inaccessible captures and leave their records marked `unknown` rather than filling gaps from speculation.

## 3. Recreate the information architecture

> Using the verified content records and `docs/information-architecture.md`, build a chronological TV Cabbage archive with Home, Archive, Labels, Events, Music, About, and Contact routes only where the source evidence supports them. Make every post addressable, searchable, and filterable by label. Clearly mark inferred sections in the code or data model.

## 4. Reproduce the visual language

> Rebuild the observed Blogger Dynamic Views character without copying proprietary Blogger code. Preserve the timeslide-inspired chronological browsing pattern, a restrained 960px reading frame, and a compact right rail. Use the archived colors and typography as evidence, but make the layout responsive for modern screens. Do not add invented hero copy, event claims, or generic music imagery.

## 5. Add media responsibly

> For every archived image, flyer, audio file, or video, record its source URL, Wayback URL, capture date, rights status, and alt text before displaying it. If the asset cannot be recovered or its rights are unclear, show a text placeholder and retain the provenance record. Do not hotlink third-party assets in production.

## 6. Quality review

> Review the rebuilt site against the archive manifest. Check that every visible factual claim has a source record, every unknown is represented honestly, every archive link includes a timestamp, and the navigation matches the reconstructed information architecture. Test mobile layout, keyboard navigation, feed output, broken media handling, and deep links.

## 7. Editorial cleanup

> Copyedit only for clarity and accessibility while preserving the original voice and factual meaning. Never normalize names, dates, venues, or music descriptions without a source. Keep the original text in a source field and the edited text in a separate presentation field.
