#!/usr/bin/env bash
# ScribeRowsSources — round-50 attempt-2 source re-open fetcher (seat-local).
# Re-fetches the four SOURCES rows' sources into the seat scratch, records
# exact command, UTC time, HTTP status, byte count, sha256 and curl exit code.
# No vendor firmware image is fetched: only index pages and text files.
# Set-Cookie headers are stripped before any header is kept.
set -u
S="${S:-/fast/scratch/hyaku/kaidoku-r50/w3-ScribeRowsSources}"
OUT="$S/receipts"
SRC="$S/src"
mkdir -p "$OUT" "$SRC"
UA='Mozilla/5.0 (X11; Linux x86_64) kaidoku-round50-source-scribe'
RCFILE="$OUT/receipts.tsv"
: > "$RCFILE"

emit() { # id url outfile
  local id="$1" url="$2" out="$3"
  local hdr="$OUT/$id.hdr" t0 t1 code rc n sha
  t0=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  code=$(curl -sS -A "$UA" -D "$hdr.raw" -o "$out" -w '%{http_code}' "$url")
  rc=$?
  t1=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  # strip Set-Cookie / cookie-bearing headers before keeping them
  grep -iv '^set-cookie:' "$hdr.raw" | grep -iv '^cookie:' > "$hdr"
  rm -f "$hdr.raw"
  n=$(stat -c%s "$out" 2>/dev/null || echo 0)
  sha=$(sha256sum "$out" 2>/dev/null | cut -d' ' -f1)
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$id" "$url" "$t0" "$t1" "$rc" "$code" "$n" "$sha" >> "$RCFILE"
  printf 'FETCH id=%s rc=%s http=%s bytes=%s sha256=%s\n' "$id" "$rc" "$code" "$n" "$sha"
}

emit S243 'https://raw.githubusercontent.com/Freetz/freetz/master/tools/make/squashfs4-host-be/patches/101-TARGET_FORMAT__AVM_BE_AVM_LE_symbols_only.patch' "$SRC/S243-freetz-101.patch"
emit S244root 'https://download.avm.de/fritzbox/' "$SRC/S244-root-index.html"
emit S244_7581 'https://download.avm.de/fritzbox/fritzbox-7581/other/fritz.os/' "$SRC/S244-7581-index.html"
emit S244_7582 'https://download.avm.de/fritzbox/fritzbox-7582/other/fritz.os/' "$SRC/S244-7582-index.html"
emit S244_6490 'https://download.avm.de/fritzbox/fritzbox-6490-cable/deutschland/fritz.os/' "$SRC/S244-6490-index.html"
emit S244_6430 'https://download.avm.de/fritzbox/fritzbox-6430-cable/deutschland/fritz.os/' "$SRC/S244-6430-index.html"
emit S245 'https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py' "$SRC/S245-unblob-squashfs.py"
emit S249 'https://download.avm.de/fritzbox/fritzbox-6490-cable/deutschland/fritz.os/info_en.txt' "$SRC/S249-info_en.txt"

echo "receipts: $RCFILE"
