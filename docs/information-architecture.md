# Information architecture reconstruction

This is a working reconstruction, not a claim that every section existed in every capture.

## Confirmed publication model

TV Cabbage behaved like a chronological Blogger publication. The strongest evidence is the Atom/RSS feed metadata and the Dynamic Views `timeslide` configuration. The primary unit is therefore a post or media item, not a brochure-style page.

## Proposed top-level structure

```text
TV Cabbage
├── Home / latest activity
├── Archive / timeline
│   └── individual post
├── Labels / themes
├── Events / free parties
├── Music / mixes and recordings
├── About TV Cabbage
└── Contact / links
```

Only `Home / latest activity`, `Archive / timeline`, and the existence of feed endpoints are supported directly by the inspected shell. The remaining branches are reconstruction targets inferred from the homepage description and the likely Blogger content model; they must be confirmed against captures.

## Content types

### Post

- title
- published date
- body
- excerpt
- labels
- source capture timestamp
- original permalink
- media references

### Event

- event name
- date and time
- place
- location details
- lineup or sound system details
- access or cost notes
- source capture timestamp

### Media item

- title
- media type: image, audio, video, flyer
- creator or rights holder
- original URL
- archive URL
- local preservation status
- caption and alt text

### Link

- label
- destination
- relationship: social, booking, collaborator, venue, archive
- source capture timestamp

## Navigation behavior to reproduce

1. Make the latest posts immediately visible.
2. Provide a chronological timeline or archive index.
3. Allow labels to filter the archive.
4. Keep each post addressable by a stable URL.
5. Expose RSS or Atom for the reconstructed publication.
6. Retain the compact, utilitarian right-rail role suggested by the original 310px sidebar.

## Evidence levels

Use one of these labels in content records:

- `verified`: visible in an inspected capture.
- `archive-derived`: recovered from a Wayback URL or feed response.
- `inferred`: a useful rebuild hypothesis not yet confirmed.
- `unknown`: a field that should remain empty until evidence is found.
