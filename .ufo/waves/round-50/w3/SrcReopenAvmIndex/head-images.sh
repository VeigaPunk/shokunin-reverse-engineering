#!/usr/bin/env bash
# SrcReopenAvmIndex: HTTP HEAD the four pinned carrier image URLs (no body download);
# record status / Content-Length / Last-Modified / ETag for pin comparison.
set -u
S=/fast/scratch/hyaku/kaidoku-r50/w3-SrcReopenAvmIndex
UA='kaidoku-r50-S244-reopen/1.0 (read-only metadata check)'
hd() {
  id=$1; url=$2
  ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  curl -sSI --max-time 25 -A "$UA" -D "$S/head/$id.hdr" -o /dev/null "$url" 2> "$S/head/$id.err"
  rc=$?
  mode=HEAD
  if [ "$rc" -ne 0 ] || [ ! -s "$S/head/$id.hdr" ]; then
    mode=RANGED-GET-0-0
    curl -sS --max-time 25 -A "$UA" -r 0-0 -D "$S/head/$id.hdr" -o "$S/head/$id.r0" "$url" 2>> "$S/head/$id.err"
    rc=$?
  fi
  lm=$(grep -i '^last-modified:' "$S/head/$id.hdr" 2>/dev/null | tail -1 | tr -d '\r')
  et=$(grep -i '^etag:'       "$S/head/$id.hdr" 2>/dev/null | tail -1 | tr -d '\r')
  cl=$(grep -i '^content-length:' "$S/head/$id.hdr" 2>/dev/null | tail -1 | tr -d '\r')
  ct=$(grep -i '^content-type:'   "$S/head/$id.hdr" 2>/dev/null | tail -1 | tr -d '\r')
  acc=$(grep -i '^accept-ranges:' "$S/head/$id.hdr" 2>/dev/null | tail -1 | tr -d '\r')
  code=$(awk 'NR==1{print $2}' "$S/head/$id.hdr" 2>/dev/null)
  echo "HEAD ts=$ts id=$id mode=$mode rc=$rc code=${code:-none} | $lm | $et | $cl | $ct | $acc | err=$(cat "$S/head/$id.err" 2>/dev/null)"
}
hd g7581 'https://download.avm.de/fritzbox/fritzbox-7581/other/fritz.os/FRITZ.Box_7581-07.18.image'
hd g7582 'https://download.avm.de/fritzbox/fritzbox-7582/other/fritz.os/FRITZ.Box_7582-07.18.image'
hd c6490 'https://download.avm.de/fritzbox/fritzbox-6490-cable/deutschland/fritz.os/FRITZ.Box_6490_Cable-07.57.image'
hd c6430 'https://download.avm.de/fritzbox/fritzbox-6430-cable/deutschland/fritz.os/FRITZ.Box_6430_Cable-07.30.image'
