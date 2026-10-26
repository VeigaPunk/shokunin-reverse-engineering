#!/usr/bin/env bash
# registry-immutable.sh LANE BASE REV
# CORPUS.md SOURCES rule 2 (append-only): for every registry row present at BASE,
# only status, recheck and used-by may differ at REV. Prints each row whose other
# cells changed (id, column numbers) and exits 1; exits 0 when none changed.
# Round-38 mistake M38-8: the S110 scope cell was widened in place at 3b960fe5.
set -euo pipefail
lane=$1 base=$2 rev=$3
rows() { git -C "$lane" show "$1:corpus/SOURCES.md" | grep -E '^ {0,3}\| *S[0-9]{3,} *\|'; }
# columns (awk -F'|'): 2 id, 3 source, 4 kind, 5 tier, 6 scope, 7 anchor, 8 teaches, 9 status, 10 opened, 11 recheck, 12 used-by
awk -F'|' 'NR==FNR { id=$2; gsub(/ /,"",id); b[id]=$0; next }
  { id=$2; gsub(/ /,"",id); if (!(id in b)) next
    n=split(b[id], o, "|"); bad=""
    for (c=2; c<=12; c++) if (c!=9 && c!=11 && c!=12 && o[c]!=$c) bad=bad " " c
    if (bad!="") { print id, "changed columns:" bad; hit=1 } }
  END { exit hit ? 1 : 0 }' <(rows "$base") <(rows "$rev")
