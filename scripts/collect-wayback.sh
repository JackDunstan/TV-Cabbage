#!/usr/bin/env sh
set -eu

site_url="${1:-www.tvcabbage.co.uk/*}"
out_file="${2:-data/wayback-cdx.json}"

mkdir -p "$(dirname "$out_file")"

curl --fail --location --silent --show-error \
  --get 'https://web.archive.org/cdx/search/cdx' \
  --data-urlencode "url=$site_url" \
  --data-urlencode 'output=json' \
  --data-urlencode 'fl=timestamp,original,statuscode,mimetype,digest' \
  --data-urlencode 'filter=statuscode:200' \
  --data-urlencode 'collapse=urlkey' \
  > "$out_file"

printf 'Saved Wayback CDX response for %s to %s\n' "$site_url" "$out_file"
