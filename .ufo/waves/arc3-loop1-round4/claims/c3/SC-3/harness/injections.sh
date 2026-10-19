#!/usr/bin/env bash
# SC-3 (chain c3, scribe) round-4 injection harness — the four named residuals.
# Usage: injections.sh <tool-copy.py> <workdir> <tag>
# All fixtures are scratch; no custody path is ever opened for writing.
set -u
TOOL="$1"; WORK="$2"; TAG="$3"
mkdir -p "$WORK"
run() {  # run <id> <cwd> <args...>
  local id="$1"; shift
  local cwd="$1"; shift
  ( cd "$cwd" && python3 "$TOOL" "$@" ) > "$WORK/$TAG-$id.out" 2>&1
  echo "$?" > "$WORK/$TAG-$id.rc"
  printf '%-28s rc=%s  %s\n' "$id" "$(cat "$WORK/$TAG-$id.rc")" "$(head -c 160 "$WORK/$TAG-$id.out" | tr '\n' '|')"
}

F="$WORK/fixtures"; rm -rf "$F"; mkdir -p "$F"

# ---- (a) sidecar path not scope-checked ---------------------------------- #
printf 'alpha\n' > "$F/vic.sha256"          # the measured path
run a1 "$F" capture --paths "$F/vic.sha256" --out "$F/vic" --label a1
sha256sum "$F/vic.sha256" | sed 's/^/  vic.sha256 after: /'
grep -c '^# custody-pair receipt' "$F/vic.sha256" 2>/dev/null | sed 's/^/  vic.sha256 receipt-lines: /'

# ---- (b) out.parent.mkdir outside the guarded try ------------------------ #
printf 'plain\n' > "$F/notadir"
run b1 "$F" capture --paths "$F/vic.sha256" --out "$F/notadir/sub/r.txt" --label b1
run b2 "$F" capture --paths "$F/vic.sha256" --out "" --label b2

# ---- (c) coverage gate counts stanzas, not distinct paths ---------------- #
printf 'beta\n' > "$F/one.conf"
run c0 "$F" capture --paths "$F/one.conf" --out "$F/r1.txt" --label c0
run c1 "$F" verify "$F/r1.txt" --live --require-paths 5
run c2 "$F" capture --paths "$F/one.conf" "$F/one.conf" "$F/one.conf" "$F/one.conf" "$F/one.conf" --out "$F/dupe5.txt" --label c2
grep -c '^PATH ' "$F/dupe5.txt" | sed 's/^/  dupe5.txt PATH stanzas: /'
run c3 "$F" verify "$F/dupe5.txt" --live --require-paths 5
run c4 "$F" verify "$F/dupe5.txt" --live
# v1 sums shape: 5 duplicate rows for the same path
D=$(sha256sum "$F/one.conf" | cut -d' ' -f1)
{ for i in 1 2 3 4 5; do printf '%s  %s\n' "$D" "$F/one.conf"; done; } > "$F/sums-dupe5.txt"
run c5 "$F" verify "$F/sums-dupe5.txt" --live --require-paths 5
# 5 distinct non-canonical scratch paths (control)
for i in 1 2 3 4 5; do printf 'p%s\n' "$i" > "$F/p$i.conf"; done
run c6 "$F" capture --paths "$F/p1.conf" "$F/p2.conf" "$F/p3.conf" "$F/p4.conf" "$F/p5.conf" --out "$F/five.txt" --label c6
run c7 "$F" verify "$F/five.txt" --live --require-paths 5

# ---- (d) both-sides-absent MATCH semantics ------------------------------- #
run d1 "$F" capture --paths "$F/ghost.conf" --out "$F/ghost-receipt.txt" --label d1
run d2 "$F" verify "$F/ghost-receipt.txt" --live
run d3 "$F" verify "$F/ghost-receipt.txt" "$F/ghost-receipt.txt"

# ---- controls ------------------------------------------------------------ #
run k1 "$F" selftest --scratch "$WORK"
run k2 "$F" paths
echo "TAG=$TAG tool=$(sha256sum "$TOOL" | cut -d' ' -f1) lines=$(wc -l < "$TOOL")"
