#!/bin/bash
# Reproduce the R40C2ReconEmpty zero-regular-file recon from nothing.
#   usage: ./build.sh WORKDIR
# Every build/run is a development input: fresh trees authored here, never a
# C1 carrier and never a C2 held-out carrier.  TMPDIR is pointed at WORKDIR;
# nothing is written under /tmp.
set -eu
ROOT=${1:?usage: build.sh WORKDIR}
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
HERE=$(cd "$(dirname "$0")" && pwd)
WRITER="$LANE/tools/round-39/gen-squashfs.py"
READER="$LANE/tools/round-39/sqfs-list.py"
V1="$LANE/tools/round-39/sqfs-triage.py"
export TMPDIR="$ROOT"
export R40_WORK="$ROOT"
mkdir -p "$ROOT"/{trees,carriers,envelopes,runs,oracle,logs,synthetic}

# ---- trees (see trees.json) -------------------------------------------------
mkdir -p "$ROOT/trees/T1/onlydir"
mkdir -p "$ROOT/trees/T2/a/b" "$ROOT/trees/T2/c"
mkdir -p "$ROOT/trees/T3/linkdir" "$ROOT/trees/T3/other"
ln -s ../ghost "$ROOT/trees/T3/linkdir/rel"
ln -s ghost2 "$ROOT/trees/T3/top"
mkdir -p "$ROOT/trees/T4"                                    # childless root: degenerate control
mkdir -p "$ROOT/trees/T5/a/b/c/d" "$ROOT/trees/T5/日本語" "$ROOT/trees/T5/ümlaut/empty"
mkdir -p "$ROOT/trees/T6/keep"
ln -s ../ghost "$ROOT/trees/T6/esc"
ln -s ../../deep/ghost "$ROOT/trees/T6/keep/esc2"

# ---- carriers (lane writer, unmodified) -------------------------------------
for t in T1 T2 T3 T5; do
  for e in le be; do
    for c in gzip xz; do
      python3 -B "$WRITER" "$ROOT/trees/$t" "$ROOT/carriers/$t-$e-$c.sqsh" --endian "$e" --comp "$c"
    done
  done
done
# T4 (childless-root control) and T6 (escaping-only) are gzip only
for e in le be; do
  python3 -B "$WRITER" "$ROOT/trees/T4" "$ROOT/carriers/T4-$e-gzip.sqsh" --endian "$e" --comp gzip
  python3 -B "$WRITER" "$ROOT/trees/T6" "$ROOT/carriers/T6-$e-gzip.sqsh" --endian "$e" --comp gzip
done
python3 -B "$WRITER" "$ROOT/trees/T1" "$ROOT/carriers/T1-avm-gzip.sqsh" --endian avm --comp gzip
python3 -B "$WRITER" "$ROOT/trees/T2" "$ROOT/carriers/T2-avm-xz.sqsh" --endian avm --comp xz
printf 'not a squashfs image at all\n' > "$ROOT/carriers/NOTSQFS-gzip.bin"

# ---- independent reads ------------------------------------------------------
: > "$ROOT/logs/sqfs-list.txt"
for f in "$ROOT"/carriers/T{1,2,3,4,5,6}-*.sqsh; do
  b=$(basename "$f" .sqsh)
  { echo "== $b sqfs-list"
    python3 -I -B "$READER" "$f" --files "$ROOT/oracle/$b.files.tsv" \
        --symlinks "$ROOT/oracle/$b.symlinks.tsv" --inspect
    echo "rc=$?"; } >> "$ROOT/logs/sqfs-list.txt"
done
: > "$ROOT/logs/direct-reads.txt"
for f in "$ROOT"/carriers/*; do
  b=$(basename "$f")
  case "$b" in
    *-be-*) bin=sasquatch-v4be; flag=-be ;;
    *-le-*) bin=sasquatch; flag= ;;
    *avm*) bin=sasquatch-v4be; flag= ;;
    *) bin=sasquatch; flag= ;;
  esac
  d="$ROOT/sasq/$b"; mkdir -p "$d"
  { echo "== $b bin=$bin flag=${flag:-none}"; "$bin" $flag -f -d "$d" "$f" 2>&1; echo "rc=$?"; } \
      >> "$ROOT/logs/direct-reads.txt"
done

# ---- REA 6.5.0 extract-firmware over every carrier --------------------------
python3 -B "$HERE/rea_driver.py"

# ---- feature tables and v1 labels ------------------------------------------
python3 -B "$HERE/extract.py" > "$ROOT/features.tsv"
printf 'run\tlabel\trule\n' > "$ROOT/v1-labels.tsv"
for f in "$ROOT"/envelopes/*.full.json; do
  b=$(basename "$f" .full.json)
  python3 -I -B "$V1" --skill "$LANE/SKILL.md" --json "$f" \
    | jq -r --arg b "$b" '"\($b)\t\(.results[0].label)\t\(.results[0].rule // "none")"' \
    >> "$ROOT/v1-labels.tsv"
done

# ---- domain-guard variants and the v2 grammar probe ------------------------
jq '.data | .operation = "analyze"'  "$ROOT/envelopes/T1-le-gzip.full.json" > "$ROOT/synthetic/T1-le-gzip-OP-analyze.json"
jq '.data | .provider.id = "binwalk" | .provider.name = "Binwalk"' "$ROOT/envelopes/T1-le-gzip.full.json" > "$ROOT/synthetic/T1-le-gzip-PV-binwalk.json"
jq '.data | .provider.name = "NotUnblob"' "$ROOT/envelopes/T1-le-gzip.full.json" > "$ROOT/synthetic/T1-le-gzip-PV-name-only.json"
jq '.data | .operation = "decompile"' "$ROOT/envelopes/T3-le-gzip.full.json" > "$ROOT/synthetic/T3-le-gzip-OP-decompile.json"
python3 -I -B "$HERE/probe-v2-rows.py" --table "$HERE/candidate-triage-v2.md" \
  --json "$ROOT/probe-v2-labels.tsv" "$ROOT"/envelopes/*.full.json "$ROOT"/synthetic/*.json
echo "done: $ROOT"
