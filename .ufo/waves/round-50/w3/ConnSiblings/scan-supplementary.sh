#!/usr/bin/env bash
# ConnSiblings w3 supplementary adjacency scan — generic firmware-extraction tokens.
set -u
S=/fast/scratch/hyaku/kaidoku-r50/w3-ConnSiblings
OUT="$S/scan-results"
RECEIPT="$OUT/receipt-supplementary.tsv"
: > "$RECEIPT"
printf 'surface\ttoken\texit_code\tmatches\toutput_file\toutput_sha256\tutc\n' >> "$RECEIPT"
TOKENS=('squashfs' 'sasquatch' 'unblob')

scan() {
  local surface="$1"; shift
  local token f n sha utc rc
  for token in "${TOKENS[@]}"; do
    f="$OUT/${surface}__${token}.txt"
    utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    grep -rIn --binary-files=without-match -e "$token" "$@" > "$f" 2> "$f.err"
    rc=$?
    if [ -s "$f.err" ]; then rc=2; fi
    n=$(wc -l < "$f")
    sha=$(sha256sum "$f" | awk '{print $1}')
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$surface" "$token" "$rc" "$n" "$f" "$sha" "$utc" >> "$RECEIPT"
  done
}

A_PATHS=()
B_PATHS=()
for d in /home/vgpnk/Projects/shokunin/*-shokunin; do
  case "$d" in
    */kaidoku-shokunin) continue ;;
  esac
  [ -f "$d/PROVINCE.md" ] && A_PATHS+=("$d/PROVINCE.md")
  [ -f "$d/SKILL.md" ] && A_PATHS+=("$d/SKILL.md")
  [ -d "$d/corpus/knowledge" ] && B_PATHS+=("$d/corpus/knowledge")
done
scan A_sibling_province_skill "${A_PATHS[@]}"
scan B_sibling_knowledge "${B_PATHS[@]}"

sha256sum "$RECEIPT" | awk '{print $1}' > "$OUT/receipt-supplementary.tsv.sha256"
echo "SUP-DONE receipt=$RECEIPT sha256=$(cat "$OUT/receipt-supplementary.tsv.sha256")"
