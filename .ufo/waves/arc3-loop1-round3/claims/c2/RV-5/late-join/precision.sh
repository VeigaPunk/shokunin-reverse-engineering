#!/bin/bash
# RV-5 late-join precision attacks on the two new closures (D3 gate, write guard).
# usage: precision.sh <outdir>
set -u
TOOL=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/custody-pair/custody-pair.py
OUT="$1"; S=/var/tmp/rv5-late/scratch2
rm -rf "$S"; mkdir -p "$S" "$OUT"
export PYTHONDONTWRITEBYTECODE=1
PY=python3
LOG="$OUT/precision.log"; : >"$LOG"
r() { local n="$1"; shift; { echo "### $n"; echo "\$ $*"; } >>"$LOG"; { "$PY" "$TOOL" "$@"; echo "exit=$?"; echo "---"; } >>"$LOG" 2>&1; }
s() { local n="$1"; shift; { echo "### $n"; echo "\$ $*"; } >>"$LOG"; { bash -c "$*"; echo "exit=$?"; echo "---"; } >>"$LOG" 2>&1; }

sha256sum "$TOOL" >>"$LOG"; echo "date=$(date -Is)" >>"$LOG"

echo "== R-A: does the D3 gate count stanzas or distinct covered paths?" >>"$LOG"
printf 'dup\n' >"$S/dup.conf"
r RA1-capture-5-duplicate-stanzas capture --out "$S/dup5.txt" --paths "$S/dup.conf" "$S/dup.conf" "$S/dup.conf" "$S/dup.conf" "$S/dup.conf" --label dup5
s RA2-stanza-count "grep -c '^PATH:' $S/dup5.txt; grep '^PATH:' $S/dup5.txt | sort -u | wc -l"
r RA3-gate-require5 verify "$S/dup5.txt" --live --require-paths 5
r RA4-control-1-of-5 verify "$S/dup5.txt" --live --require-paths 6
# the same trick against the canonical custody set: 5 stanzas, one path
s RA5-canonical-dup "cp $HOME/.bashrc $S/b1 2>/dev/null; $PY $TOOL capture --out $S/canon5.txt --paths $HOME/.bashrc $HOME/.bashrc $HOME/.bashrc $HOME/.bashrc $HOME/.bashrc --label canon5"
r RA6-canonical-dup-gate verify "$S/canon5.txt" --live --require-paths 5

echo "== R-B: does the write guard cover the sidecar write target?" >>"$LOG"
printf 'measured bytes that must survive\n' >"$S/m.sha256"
sha256sum "$S/m.sha256" >>"$LOG"
r RB1-guard-out-is-measured capture --out "$S/m.sha256" --paths "$S/m.sha256" --label direct
sha256sum "$S/m.sha256" >>"$LOG"
r RB2-sidecar-clobber capture --out "$S/m" --paths "$S/m.sha256" --label sidecar
sha256sum "$S/m.sha256" >>"$LOG"
s RB3-after-state "ls -l $S/m $S/m.sha256 $S/m.sha256.sha256 2>&1; head -c 60 $S/m.sha256"
# custody-path variant: can the sidecar reach a custody path?
r RB4-custody-sidecar capture --out "$HOME/.bashr" --paths "$S/dup.conf" --label custside
s RB5-custody-unchanged "sha256sum $HOME/.bashrc; ls -l $HOME/.bashr $HOME/.bashr.sha256 2>&1 | head -3"

echo "== D6 extra arm: existing but unwritable scratch dir" >>"$LOG"
mkdir -p "$S/ro-scr"; chmod 500 "$S/ro-scr"
r RD1-readonly-scratch selftest --scratch "$S/ro-scr"
chmod 700 "$S/ro-scr"

echo "== D3 extra: huge N, non-integer N" >>"$LOG"
r RE1-require-99 verify "$S/dup5.txt" --live --require-paths 99
s RE2-require-nonint "$PY $TOOL verify $S/dup5.txt --live --require-paths five"

echo "== write-guard extra: out is an existing directory" >>"$LOG"
r RF1-out-is-dir capture --out "$S" --paths "$S/dup.conf" --label dirout

echo PRECISION-END >>"$LOG"; exit 0
