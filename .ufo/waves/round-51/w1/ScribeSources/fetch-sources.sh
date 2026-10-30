#!/usr/bin/env bash
# round-51 seat ScribeSources — source fetch driver
# Records for each fetch: exact URL, UTC time, HTTP status, bytes, sha256, curl exit.
# Saves bodies under $S/body/ and a receipts TSV under $S/receipts/.
set -u
S=/fast/scratch/hyaku/kaidoku-r51/w1-ScribeSources
export TMPDIR="$S"
mkdir -p "$S/body" "$S/receipts"
TSV="$S/receipts/receipts.tsv"
: > "$TSV"
printf 'url\tutc_time\thttp_status\tbytes\tsha256\tcurl_exit\tbody_file\n' >> "$TSV"

fetch() {
  local url="$1" name="$2"
  local body="$S/body/$name"
  local hdr="$S/body/$name.headers"
  local t; t=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  local code rc sz sha
  code=$(curl -sSL -o "$body" -D "$hdr" -w '%{http_code}' --max-time 120 "$url" 2>"$S/body/$name.err")
  rc=$?
  sz=$(stat -c %s "$body" 2>/dev/null || echo 0)
  sha=$(sha256sum "$body" 2>/dev/null | cut -d' ' -f1)
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$url" "$t" "$code" "$sz" "$sha" "$rc" "$body" >> "$TSV"
  # header scrub: only content-type/last-modified kept, set-cookie/cookie dropped
  grep -iE '^(content-type|content-length|last-modified|etag):' "$hdr" > "$body.meta" 2>/dev/null || true
  rm -f "$hdr"
  printf '%s  %s  %s  %sB  rc=%s\n' "$t" "$code" "$sz" "$sha" "$rc"
}

fetch 'https://raw.githubusercontent.com/plougher/squashfs-tools/master/squashfs-tools/unsquashfs.c' 'unsquashfs-master.c'
fetch 'https://raw.githubusercontent.com/plougher/squashfs-tools/master/squashfs-tools/mksquashfs.c' 'mksquashfs-master.c'
