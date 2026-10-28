#!/usr/bin/env bash
# Census-shaped checks from /home/vgpnk/Projects/shokunin/CORPUS.md section SOURCES.
# Read-only against the lane; the edited registry lives only in scratch.
S=/fast/scratch/hyaku/kaidoku-r49/C1ScribeSources
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
TREE=$S/tree2
USEDBY='{s=$9; gsub(/[[:space:]]/,"",s); if (s=="mined") {n=split($12, a, /[,;]/); for (j=1;j<=n;j++) {p=a[j]; gsub(/^[[:space:]]+|[[:space:]]+$/,"",p); if (p!="" && p!="—") print p}}}'

run() { # label, registry file, cwd
  local label=$1 reg=$2 cwd=$3
  echo "=== $label"
  echo "registry sha256: $(sha256sum "$reg" | cut -c1-64)  cwd: $cwd"
  echo "rows: $(grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' "$reg")"
  echo "malformed (NF!=13, must be 0): $(awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' "$reg")"
  echo "NF of S138/S139 rows: $(awk -F'|' '/^\| *S13[89] *\|/ {printf "%s:NF=%d ", $2, NF}' "$reg")"
  echo "duplicate ids (must be empty): [$(awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' "$reg" | sort | uniq -d | tr '\n' ' ')]"
  (cd "$cwd" && awk -F'|' "/^\\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\\|/ {$USEDBY}" "$reg" | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done)
  echo "missing-scan exit (pipeline status of last test; 0 = scan ran)  rc=$?"
}

run "V0 lane root, BASE registry (expect no missing)" "$S/SOURCES.base.md" "$L"
run "V1 lane root, EDITED registry, R49 entry absent (expect 2 missing: the entry lands with the registry)" "$S/SOURCES.edit.md" "$L"
run "V2 scratch tree, EDITED registry, R49 entry present (expect no missing)" "$TREE/corpus/SOURCES.md" "$TREE"
echo "=== S138/S139 opened column"
awk -F'|' '/^\| *S13[89] *\|/ {print $2, "opened=[" $10 "]"}' "$S/SOURCES.edit.md"
