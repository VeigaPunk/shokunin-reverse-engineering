#!/usr/bin/env bash
# sandbox-gate — exercise the prepared copies inside a throwaway clone of the lane.
#
# Seat R42LocalSrc. No git mutation: the clone is only cloned and copied into,
# never committed. Every git call names -C explicitly and the clone's top level
# is asserted before anything touches it.
#
# Usage: sandbox-gate.sh <artifacts-dir> <scratch-dir> <receipts-dir>
set -u

A=${1:?artifacts dir}
S=${2:?scratch dir}
R=${3:?receipts dir}
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
GATE=$LANE/tools/round-41/local-source-gate.py
REV=c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c
mkdir -p "$R"
D=$(mktemp -d "$S/fx.XXXX") || exit 1
D2=$(mktemp -d "$S/fx.XXXX") || exit 1

git clone -q --shared "$LANE" "$D/lane" || exit 1
top=$(git -C "$D/lane" rev-parse --show-toplevel)
[ "$top" = "$D/lane" ] || { echo "clone toplevel mismatch: $top"; exit 1; }

git clone -q --shared "$LANE" "$D2/lane" || exit 1
top2=$(git -C "$D2/lane" rev-parse --show-toplevel)
[ "$top2" = "$D2/lane" ] || { echo "pristine toplevel mismatch: $top2"; exit 1; }

cp -a "$A/corpus/." "$D/lane/corpus/" || exit 1

cd "$S" || exit 1
echo "### A. gate in the unmodified clone (no copies) — negative control"
python3 -I -B "$GATE" --root "$D2/lane" --rev "$REV" --json > "$R/gate-pristine.json" 2> "$R/gate-pristine.err"
echo "pristine exit=$?"

echo "### B. gate in the clone with the prepared copies, pinned rev"
python3 -I -B "$GATE" --root "$D/lane" --rev "$REV" --json > "$R/gate-with-copies.json" 2> "$R/gate-with-copies.err"
echo "with-copies (rev) exit=$?"

echo "### C. gate in the clone with the prepared copies, working tree"
python3 -I -B "$GATE" --root "$D/lane" > "$R/gate-with-copies.txt" 2> "$R/gate-with-copies-text.err"
echo "with-copies (tree) exit=$?"

echo "### D. verify-copies against the clone"
TARGS=()
[ -f "$S/dl/rea6.7.0.tgz" ] && TARGS=(--tarball "$S/dl/rea6.7.0.tgz")
python3 -I -B "$A/build/verify-copies.py" --root "$D/lane" "${TARGS[@]}" > "$R/verify-clone.tsv" 2>&1
echo "verify exit=$?"

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

echo "### G. restored clone must be green again"
python3 -I -B "$GATE" --root "$D/lane" --rev "$REV" --json > "$R/gate-restored.json" 2>&1
echo "restored exit=$?"

rm -rf "$D" "$D2"
