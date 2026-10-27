#!/bin/sh
# R43W2AssimFlip fresh-bytes fetch (read-only network checks)
# Lane tip at run time: 5856614ac4bf7f2363bbcd1956644474a82108e5 ; freeze f3f8db389416d094b1ddeb1215ddcf914bfc0d1c
set -u
cd /fast/scratch/hyaku/kaidoku-r43/w2/R43W2AssimFlip || exit 9
: > fetch-transcript.txt
run() {
  echo "== $*" >> fetch-transcript.txt
  date -u +%FT%TZ >> fetch-transcript.txt
  "$@" >> fetch-transcript.txt 2>&1
  ec=$?
  echo "exit=$ec" >> fetch-transcript.txt
  echo >> fetch-transcript.txt
  return $ec
}

# 1. Releases API (default page)
curl -fsSL -w '\nHTTP_STATUS=%{http_code}\n' -o rel-r43w2.json https://api.github.com/repos/onekey-sec/sasquatch/releases
run sha256sum rel-r43w2.json
run wc -c rel-r43w2.json

# 2. Releases API page 2 (ninth-release probe)
curl -fsSL -w '\nHTTP_STATUS=%{http_code}\n' -o rel-r43w2-page2.json 'https://api.github.com/repos/onekey-sec/sasquatch/releases?per_page=100&page=2'
run sha256sum rel-r43w2-page2.json
run wc -c rel-r43w2-page2.json

# 3. Tags endpoint (ninth-release probe, alternate route)
curl -fsSL -w '\nHTTP_STATUS=%{http_code}\n' -o tags-r43w2.json 'https://api.github.com/repos/onekey-sec/sasquatch/tags?per_page=100'
run sha256sum tags-r43w2.json
run wc -c tags-r43w2.json

# 4. Rendered releases page
curl -fsSL -w '\nHTTP_STATUS=%{http_code}\n' -o sasq-releases-r43w2.html https://github.com/onekey-sec/sasquatch/releases
run sha256sum sasq-releases-r43w2.html
run wc -c sasq-releases-r43w2.html
