#!/usr/bin/env bash
# SrcReopenAvmIndex (S244 re-open): fetch the 5 AVM download index bodies, receipt status/bytes/sha256/UTC.
# Read-only metadata pass; no image bodies are downloaded.
set -u
S=/fast/scratch/hyaku/kaidoku-r50/w3-SrcReopenAvmIndex
UA='kaidoku-r50-S244-reopen/1.0 (read-only index metadata check)'
UA2='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
echo "curl_version=$(curl --version | head -1)"
fetch() {
  name=$1; url=$2
  ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  w="$S/idx/$name.curlw"
  curl -sS --max-time 30 -A "$UA" -H 'Accept-Encoding: identity' \
    -o "$S/idx/$name.body" -D "$S/idx/$name.hdr" \
    -w 'code=%{http_code} dl=%{size_download} redirects=%{num_redirects} final=%{url_effective}' \
    "$url" > "$w" 2> "$S/idx/$name.err"
  rc=$?
  code=$(sed -n 's/.*code=\([0-9][0-9][0-9]\).*/\1/p' "$w")
  if [ "$rc" -ne 0 ] || [ "${code:-000}" = "403" ] || [ "${code:-000}" = "406" ]; then
    ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    curl -sS --max-time 30 -A "$UA2" -H 'Accept-Encoding: identity' \
      -o "$S/idx/$name.body" -D "$S/idx/$name.hdr" \
      -w 'code=%{http_code} dl=%{size_download} redirects=%{num_redirects} final=%{url_effective}' \
      "$url" > "$w" 2> "$S/idx/$name.err"
    rc=$?
    echo "RETRY-UA2 name=$name ts=$ts rc=$rc"
  fi
  bytes=$(stat -c %s "$S/idx/$name.body" 2>/dev/null || echo 0)
  sha=$(sha256sum "$S/idx/$name.body" 2>/dev/null | cut -d' ' -f1)
  echo "IDX ts=$ts name=$name rc=$rc $(cat "$w") bytes=$bytes sha256=$sha err=$(cat "$S/idx/$name.err" 2>/dev/null)"
}
fetch base                'https://download.avm.de/fritzbox/'
fetch fritzbox-7581       'https://download.avm.de/fritzbox/fritzbox-7581/other/fritz.os/'
fetch fritzbox-7582       'https://download.avm.de/fritzbox/fritzbox-7582/other/fritz.os/'
fetch fritzbox-6490-cable 'https://download.avm.de/fritzbox/fritzbox-6490-cable/deutschland/fritz.os/'
fetch fritzbox-6430-cable 'https://download.avm.de/fritzbox/fritzbox-6430-cable/deutschland/fritz.os/'
