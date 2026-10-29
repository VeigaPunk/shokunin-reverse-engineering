#!/usr/bin/env bash
# ExecCensusMid — drift comparison driver (attempt-2 start receipt vs re-run).
set -u
D=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-50/w3/ExecCensusMid
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-50/l1
OUT="$D/drift.txt"
: >"$OUT"

emit() { echo "$@" >>"$OUT"; }

run() {
  local name="$1"; shift
  local cmd="$*"
  local rc=0
  local body; body=$(mktemp "$D/.drift.XXXXXX")
  { eval "$cmd"; } >"$body" 2>&1 || rc=$?
  local sha; sha=$(sha256sum "$body" | cut -d' ' -f1)
  local ts; ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  {
    echo "### $name"
    echo "command: $cmd"
    echo "exit: $rc"
    echo "stdout_sha256: $sha"
    echo "utc: $ts"
    echo "--- output ---"
    cat "$body"
    echo "--- end output ---"
    echo
  } >>"$OUT"
  rm -f "$body"
  printf '%s\texit=%s\tsha256=%s\n' "$name" "$rc" "$sha"
}

run drift-diff-attempt2-start \
  "diff '$L/sources-census-start-attempt2.txt' '$D/validate-attempt2.out'"
run drift-cmp-attempt2-start \
  "cmp '$L/sources-census-start-attempt2.txt' '$D/validate-attempt2.out'"
run w04-count-attempt2-start \
  "grep -c 'W04' '$L/sources-census-start-attempt2.txt'"
run w04-count-rerun \
  "grep -c 'W04' '$D/validate-attempt2.out'"
run ecode-count-rerun \
  "grep -cE '\\tE[0-9]{2}\\t' '$D/validate-attempt2.out'"
run ok-line-rerun \
  "tail -1 '$D/validate-attempt2.out'"
run attempt1-start-w04-count \
  "grep -c 'W04' '$L/sources-census-start.txt'"
run attempt1-end-w04-count \
  "grep -c 'W04' '$L/sources-census-end.txt'"
run diff-attempt1-start-vs-attempt2-start \
  "diff '$L/sources-census-start.txt' '$L/sources-census-start-attempt2.txt'"
run sha256-start-attempt2 \
  "sha256sum '$L/sources-census-start-attempt2.txt'"
run sha256-validate-rerun \
  "sha256sum '$D/validate-attempt2.out'"
run sha256-sources-md-worktree \
  "sha256sum /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md"
run sha256-sources-md-at-base \
  "cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && git show f890bbead20ca2c549487167f56876ae47f1e1a4:corpus/SOURCES.md | sha256sum"
run sha256-sources-md-at-head \
  "cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && git show HEAD:corpus/SOURCES.md | sha256sum"
run used-by-candidate-count \
  "cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && awk -F'|' '/^\\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\\|/ && NF==13 {s=\$9; gsub(/[[:space:]]/,\"\",s); if (s==\"mined\") {n=split(\$12, a, /[,;]/); for (j=1;j<=n;j++) {p=a[j]; gsub(/^[[:space:]]+|[[:space:]]+\$/,\"\",p); if (p!=\"\" && p!=\"—\") c++}}} END{print c+0}' corpus/SOURCES.md"
echo DONE
