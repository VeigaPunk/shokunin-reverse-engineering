#!/usr/bin/env bash
# ConnSiblings w3 sibling-overlap scan — receipt-grade grep driver.
# Every result row: surface, token, exit_code (grep semantics: 0=match, 1=no match, 2=error), match count, output file, sha256 of output, UTC timestamp.
set -u
S=/fast/scratch/hyaku/kaidoku-r50/w3-ConnSiblings
OUT="$S/scan-results"
mkdir -p "$OUT"
RECEIPT="$OUT/receipt.tsv"
: > "$RECEIPT"
printf 'surface\ttoken\texit_code\tmatches\toutput_file\toutput_sha256\tutc\n' >> "$RECEIPT"

TOKENS=('squashfs_v2_nonstandard' 'squashfs_v3_broadcom' 'squashfs_v3_nonstandard' 'hsqs' 'sqfs-triage' 'FRITZ' 'AVM')

scan() {
  local surface="$1"; shift
  local desc="$1"; shift
  # remaining args: paths to search
  local paths=("$@")
  local token f n sha utc rc
  for token in "${TOKENS[@]}"; do
    f="$OUT/${surface}__${token}.txt"
    utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    grep -rIn --binary-files=without-match -e "$token" "${paths[@]}" > "$f" 2> "$f.err"
    rc=$?
    if [ -s "$f.err" ]; then rc=2; fi
    n=$(wc -l < "$f")
    sha=$(sha256sum "$f" | awk '{print $1}')
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$surface" "$token" "$rc" "$n" "$f" "$sha" "$utc" >> "$RECEIPT"
  done
}

# Surface A: sibling lanes' PROVINCE.md + SKILL.md (skip kaidoku)
A_PATHS=()
for d in /home/vgpnk/Projects/shokunin/*-shokunin; do
  case "$d" in
    */kaidoku-shokunin) continue ;;
  esac
  [ -f "$d/PROVINCE.md" ] && A_PATHS+=("$d/PROVINCE.md")
  [ -f "$d/SKILL.md" ] && A_PATHS+=("$d/SKILL.md")
done
scan A_sibling_province_skill "sibling PROVINCE+SKILL" "${A_PATHS[@]}"

# Surface B: sibling lanes' corpus/knowledge trees (skip kaidoku)
B_PATHS=()
for d in /home/vgpnk/Projects/shokunin/*-shokunin; do
  case "$d" in
    */kaidoku-shokunin) continue ;;
  esac
  [ -d "$d/corpus/knowledge" ] && B_PATHS+=("$d/corpus/knowledge")
done
if [ "${#B_PATHS[@]}" -gt 0 ]; then
  scan B_sibling_knowledge "sibling corpus/knowledge" "${B_PATHS[@]}"
else
  printf 'B_sibling_knowledge\tALL\t2\t0\tNONE\tno-corpus-knowledge-dirs\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$RECEIPT"
fi

# Surface C: shokuknow merge knowledge (all lanes; kaidoku rows annotated self in report)
C_PATHS=(/home/vgpnk/Projects/shokuknow/merge/*/knowledge)
scan C_shokuknow_merge "shokuknow merge knowledge" "${C_PATHS[@]}"

sha256sum "$RECEIPT" | awk '{print $1}' > "$OUT/receipt.tsv.sha256"
echo "SCAN-DONE receipt=$RECEIPT sha256=$(cat "$OUT/receipt.tsv.sha256")"
