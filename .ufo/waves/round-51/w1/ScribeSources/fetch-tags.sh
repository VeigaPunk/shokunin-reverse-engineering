#!/usr/bin/env bash
# round-51 seat ScribeSources — tag-pinned fetch (4.7.5, the host tool version)
set -u
S=/fast/scratch/hyaku/kaidoku-r51/w1-ScribeSources
export TMPDIR="$S"
mkdir -p "$S/body" "$S/receipts"
TSV="$S/receipts/receipts-tags.tsv"
: > "$TSV"
printf 'url\tutc_time\thttp_status\tbytes\tsha256\tcurl_exit\tbody_file\n' >> "$TSV"

fetch() {
  local url="$1" name="$2"
  local body="$S/body/$name" hdr="$S/body/$name.headers"
  local t; t=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  local code rc sz sha
  code=$(curl -sSL -o "$body" -D "$hdr" -w '%{http_code}' --max-time 120 "$url" 2>/dev/null)
  rc=$?
  sz=$(stat -c %s "$body" 2>/dev/null || echo 0)
  sha=$(sha256sum "$body" 2>/dev/null | cut -d' ' -f1)
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$url" "$t" "$code" "$sz" "$sha" "$rc" "$body" >> "$TSV"
  grep -iE '^(content-type|content-length|last-modified|etag):' "$hdr" > "$body.meta" 2>/dev/null || true
  rm -f "$hdr"
  printf '%s  %s  %s  %sB  rc=%s\n' "$t" "$code" "$sz" "$sha" "$rc"
}

fetch 'https://raw.githubusercontent.com/plougher/squashfs-tools/4.7.5/squashfs-tools/unsquashfs.c' 'unsquashfs-4.7.5.c'
fetch 'https://raw.githubusercontent.com/plougher/squashfs-tools/4.7.5/squashfs-tools/mksquashfs.c' 'mksquashfs-4.7.5.c'
fetch 'https://raw.githubusercontent.com/plougher/squashfs-tools/db038ef265ed00bb17aaf695a72f9b0c3489eb20/squashfs-tools/unsquashfs.c' 'unsquashfs-headpin.c'
fetch 'https://raw.githubusercontent.com/plougher/squashfs-tools/db038ef265ed00bb17aaf695a72f9b0c3489eb20/squashfs-tools/mksquashfs.c' 'mksquashfs-headpin.c'
