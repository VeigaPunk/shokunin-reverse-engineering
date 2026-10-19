#!/bin/bash
# EX-17 (kaidoku-shokunin arc3-loop1-round1, chain c2) tamper-injection runner.
# Usage: bash run-injections.sh <phase>    (phase = before | after)
# Tests ONLY copies under the scratch lab; the repo is read via git (read-only).
set -u
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
LAB=/dev/shm/ex17-c2-tamper
PHASE=${1:?usage: run-injections.sh <phase>}
BASE=${BASE:-$LAB/base}
OUT=$LAB/logs/$PHASE.txt
mkdir -p "$LAB/logs"
P=$BASE/citation-drift-probe.py
E=$BASE/expected.json
: > "$OUT"

echo "# phase=$PHASE date=$(date -u +%FT%TZ)" >> "$OUT"
echo "# repo HEAD: $(git -C "$REPO" rev-parse HEAD)" >> "$OUT"
echo "# base sha256 (probe / expected / table):" >> "$OUT"
sha256sum "$P" "$E" "$BASE/pointer-table.json" >> "$OUT"
echo >> "$OUT"

probe() { # probe <name> <table> [extra args...]
  local name=$1 table=$2; shift 2
  echo "## $name" >> "$OUT"
  echo "CMD: python3 citation-drift-probe.py --root $REPO --rev HEAD --table $table --expected $E $*" >> "$OUT"
  ( cd "$LAB" && python3 "$P" --root "$REPO" --rev HEAD --table "$table" --expected "$E" "$@" ) >> "$OUT" 2>&1
  echo "EXIT=$?" >> "$OUT"
  echo >> "$OUT"
}

tamper() { # tamper <py-snippet-file> <src> <dst> ; prints offset/byte/sha evidence
  local gen=$1 src=$2 dst=$3
  python3 "$gen" "$src" "$dst" >> "$OUT" 2>&1
  echo "sha256($(basename "$dst")) = $(sha256sum "$dst" | cut -d' ' -f1)" >> "$OUT"
}

# --- I0: baseline, pristine copied table ---
probe I0-clean "$BASE/pointer-table.json"
probe I0-clean-strict "$BASE/pointer-table.json" --strict

# --- I1: structural byte flip -> invalid JSON ---
cat > "$LAB/gen-i1.py" <<'PY'
import sys
src, dst = sys.argv[1], sys.argv[2]
b = bytearray(open(src, 'rb').read())
i = bytes(b).index(b'"entries": [')
before = b[i]
b[i] = 0x21  # '"' -> '!'
open(dst, 'wb').write(bytes(b))
print("I1: offset=%d byte 0x%02x -> 0x%02x" % (i, before, b[i]))
PY
tamper "$LAB/gen-i1.py" "$BASE/pointer-table.json" "$LAB/t1-invalid-json.json"
probe I1-invalid-json "$LAB/t1-invalid-json.json"

# --- I2: semantic byte flip, JSON stays valid: line 59 -> 69 ---
cat > "$LAB/gen-i2.py" <<'PY'
import sys
src, dst = sys.argv[1], sys.argv[2]
b = bytearray(open(src, 'rb').read())
i = bytes(b).index(b'"line": 59')
off = i + 8  # the '5' of 59
before = b[off]
b[off] = 0x36  # '5' -> '6'
open(dst, 'wb').write(bytes(b))
print("I2: offset=%d byte 0x%02x -> 0x%02x (line 59 -> 69 in sc59-stanza-key-anchor)" % (off, before, b[off]))
PY
tamper "$LAB/gen-i2.py" "$BASE/pointer-table.json" "$LAB/t2-lineflip.json"
python3 -c "import json;json.load(open('$LAB/t2-lineflip.json'));print('I2: tampered file still parses as JSON')" >> "$OUT" 2>&1
probe I2-lineflip "$LAB/t2-lineflip.json"
probe I2-lineflip-strict "$LAB/t2-lineflip.json" --strict

# --- I3: absent table ---
probe I3-absent "$LAB/t3-absent/pointer-table.json"

# --- I4: entries key renamed via byte flip -> all 31 entries silently skipped ---
cat > "$LAB/gen-i4.py" <<'PY'
import sys
src, dst = sys.argv[1], sys.argv[2]
b = bytearray(open(src, 'rb').read())
i = bytes(b).index(b'"entries": [')
off = i + 7  # last 's' of "entries"
before = b[off]
b[off] = 0x58  # 's' -> 'X'
open(dst, 'wb').write(bytes(b))
print("I4: offset=%d byte 0x%02x -> 0x%02x (\"entries\" -> \"entrieX\")" % (off, before, b[off]))
PY
tamper "$LAB/gen-i4.py" "$BASE/pointer-table.json" "$LAB/t4-keyrename.json"
python3 -c "import json;t=json.load(open('$LAB/t4-keyrename.json'));print('I4: parses OK; entries now =', len(t.get('entries',[])), 'quoted =', len(t.get('quoted',[])))" >> "$OUT" 2>&1
probe I4-keyrename "$LAB/t4-keyrename.json"
probe I4-keyrename-strict "$LAB/t4-keyrename.json" --strict

echo "# done phase=$PHASE $(date -u +%FT%TZ)" >> "$OUT"
