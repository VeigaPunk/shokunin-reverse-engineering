#!/usr/bin/env bash
# ExecCensusMid — round-50 attempt-2 wave-3 SOURCES census driver.
# Runs the FROZEN manual census commands from /home/vgpnk/Projects/shokunin/CORPUS.md
# section "Census" verbatim against kaidoku-shokunin/corpus/SOURCES.md, cwd = lane root.
# Read-only: writes only into OUT.
set -u
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
OUT="$1"
mkdir -p "$OUT"
cd "$LANE" || exit 2

run() {
  local name="$1"; shift
  local cmd="$*"
  local rc=0
  local body="$OUT/$name.out"
  { eval "$cmd"; } >"$body" 2>&1 || rc=$?
  local sha
  sha=$(sha256sum "$body" | cut -d' ' -f1)
  local ts
  ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  {
    echo "### $name"
    echo "cwd: $LANE"
    echo "command: $cmd"
    echo "exit: $rc"
    echo "stdout_sha256: $sha"
    echo "utc: $ts"
    echo "--- output ---"
    cat "$body"
    echo "--- end output ---"
    echo
  } >>"$OUT/manual-census.txt"
  printf '%s\texit=%s\tsha256=%s\n' "$name" "$rc" "$sha"
}

: >"$OUT/manual-census.txt"

run rows \
  "grep -cE '^\\|[[:space:]]*S[0-9]{3,}[[:space:]]*\\|' corpus/SOURCES.md"

run malformed-rows \
  "awk -F'|' '/^\\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md"

run tier-histogram \
  "awk -F'|' '/^\\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\\|/ {t=\$5; gsub(/[[:space:]]/,\"\",t); n[t]++} END{for(k in n) printf \"%s=%d \", k, n[k]; print \"\"}' corpus/SOURCES.md"

run status-histogram \
  "awk -F'|' '/^\\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\\|/ {s=\$9; gsub(/[[:space:]]/,\"\",s); n[s]++} END{for(k in n) printf \"%s=%d \", k, n[k]; print \"\"}' corpus/SOURCES.md"

run duplicate-ids \
  "awk -F'|' '/^\\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\\|/ {i=\$2; gsub(/[[:space:]]/,\"\",i); print i}' corpus/SOURCES.md | sort | uniq -d"

run enum-violations \
  "awk -F'|' '/^\\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\\|/ && NF==13 {i=\$2;k=\$4;t=\$5;s=\$9; gsub(/[[:space:]]/,\"\",i); gsub(/[[:space:]]/,\"\",k); gsub(/[[:space:]]/,\"\",t); gsub(/[[:space:]]/,\"\",s); if (t !~ /^[ABC]\$/) print \"tier\", i, t; if (s !~ /^(queued|mined|rejected)\$/) print \"status\", i, s; if (k !~ /^(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)\$/) print \"kind\", i, k; if (t==\"A\" && k==\"community\") print \"tier-inflation\", i}' corpus/SOURCES.md"

run mined-used-by-missing \
  "awk -F'|' '/^\\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\\|/ && NF==13 {s=\$9; gsub(/[[:space:]]/,\"\",s); if (s==\"mined\") {n=split(\$12, a, /[,;]/); for (j=1;j<=n;j++) {p=a[j]; gsub(/^[[:space:]]+|[[:space:]]+\$/,\"\",p); if (p!=\"\" && p!=\"—\") print p}}}' corpus/SOURCES.md | while read -r p; do [ -e \"\$p\" ] || echo \"missing: \$p\"; done"

# The seat-spec row count (spacing-tolerant, 0-3 leading spaces) — the "before" number.
run rows-spacing-tolerant \
  "grep -cE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md"

echo "DONE"
