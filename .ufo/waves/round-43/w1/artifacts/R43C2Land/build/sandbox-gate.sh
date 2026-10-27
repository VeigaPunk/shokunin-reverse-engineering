#!/usr/bin/env bash
# sandbox-gate — exercise the R43-C2 landing pack inside throwaway clones.
#
# Seat R43C2Land, round 43 wave 1.  No git mutation of the lane: the clones are
# only cloned and copied into, never committed.  Every git call names -C
# explicitly and each clone's top level is asserted before anything touches it.
#
# Usage: sandbox-gate.sh <pack-dir> <scratch-dir> <receipts-dir>
set -u

P=${1:?pack dir}
S=${2:?scratch dir}
R=${3:?receipts dir}
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
GATE=$LANE/tools/round-41/local-source-gate.py
REV=6b9e64fe7e0de202d9383baad5792fbfe039a743
mkdir -p "$R"
D=$(mktemp -d "$S/fx.XXXX") || exit 1
D2=$(mktemp -d "$S/fx.XXXX") || exit 1

git clone -q --shared "$LANE" "$D/lane" || exit 1
top=$(git -C "$D/lane" rev-parse --show-toplevel)
[ "$top" = "$D/lane" ] || { echo "clone toplevel mismatch: $top"; exit 1; }

git clone -q --shared "$LANE" "$D2/lane" || exit 1
top2=$(git -C "$D2/lane" rev-parse --show-toplevel)
[ "$top2" = "$D2/lane" ] || { echo "pristine toplevel mismatch: $top2"; exit 1; }

cp -a "$P/corpus/." "$D/lane/corpus/" || exit 1

cd "$S" || exit 1

echo "### A. gate in the unmodified clone (no copies) — negative control"
python3 -I -B "$GATE" --root "$D2/lane" --rev "$REV" --json > "$R/gate-pristine.json" 2> "$R/gate-pristine.err"
echo "pristine exit=$?"

echo "### B. gate in the clone with the pack, pinned rev $REV"
python3 -I -B "$GATE" --root "$D/lane" --rev "$REV" --json > "$R/gate-with-copies.json" 2> "$R/gate-with-copies.err"
echo "with-copies (rev) exit=$?"

echo "### C. gate in the clone with the pack, working tree"
python3 -I -B "$GATE" --root "$D/lane" > "$R/gate-with-copies.txt" 2> "$R/gate-with-copies-text.err"
echo "with-copies (tree) exit=$?"

echo "### D. gate selftest (tool health)"
python3 -I -B "$GATE" --selftest > "$R/gate-selftest.txt" 2>&1
echo "selftest exit=$?"

echo "### E. control: one corrupted copy must turn the gate red"
cp "$D/lane/corpus/evidence/round-42/local-sources/S056/cliCommandNames.js" "$D/keep.js"
printf 'x' >> "$D/lane/corpus/evidence/round-42/local-sources/S056/cliCommandNames.js"
python3 -I -B "$GATE" --root "$D/lane" --rev "$REV" --json > "$R/gate-corrupt.json" 2>&1
echo "corrupt exit=$?"
cp "$D/keep.js" "$D/lane/corpus/evidence/round-42/local-sources/S056/cliCommandNames.js"

echo "### F. control: dropping one map entry must turn the gate red"
python3 - "$D/lane/corpus/evidence/local-sources.json" "$D/map-full.json" <<'PY'
import json, sys
doc = json.load(open(sys.argv[1]))
cp = dict(doc)
cp["sources"] = {k: v for k, v in doc["sources"].items()
                 if not k.endswith("/ghidra_12.1.4_PUBLIC/docs/ChangeHistory.md")}
json.dump(cp, open(sys.argv[2], "w"), indent=2, sort_keys=True)
PY
cp "$D/lane/corpus/evidence/local-sources.json" "$D/map-orig.json"
cp "$D/map-full.json" "$D/lane/corpus/evidence/local-sources.json"
python3 -I -B "$GATE" --root "$D/lane" --rev "$REV" --json > "$R/gate-dropped-entry.json" 2>&1
echo "dropped-entry exit=$?"
cp "$D/map-orig.json" "$D/lane/corpus/evidence/local-sources.json"

echo "### G. control: a copy whose digest does not match the map must turn the gate red"
python3 - "$D/lane/corpus/evidence/local-sources.json" "$D/map-bad.json" <<'PY'
import json, sys
doc = json.load(open(sys.argv[1]))
for k, v in doc["sources"].items():
    if k.endswith("/dist/cliCommandNames.js"):
        v["sha256"] = "0" * 64
json.dump(doc, open(sys.argv[2], "w"), indent=2, sort_keys=True)
PY
cp "$D/map-bad.json" "$D/lane/corpus/evidence/local-sources.json"
python3 -I -B "$GATE" --root "$D/lane" --rev "$REV" --json > "$R/gate-bad-digest.json" 2>&1
echo "bad-digest exit=$?"
cp "$D/map-orig.json" "$D/lane/corpus/evidence/local-sources.json"

echo "### H. restored clone must be green again"
python3 -I -B "$GATE" --root "$D/lane" --rev "$REV" --json > "$R/gate-restored.json" 2>&1
echo "restored exit=$?"

rm -rf "$D" "$D2"
