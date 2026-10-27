#!/usr/bin/env bash
# calibration-probes — the three checks the round-42 report routed forward.
#
#   P1 (round-42 finding F4): the map vocabulary cannot express what the
#      copies are.  Probe: add the proposed `encoding`/`members` keys to a map
#      entry and see whether the FROZEN gate still accepts it.
#   P2 (round-42 section 7 risk): `source_sha256` makes the gate watch a live
#      host container.  Probe: perturb the recorded source digest of the pacman
#      repository database and see how hard the gate goes red.
#   P3: the gate tool itself is byte-identical to the round-41 committed bytes.
#
# Usage: calibration-probes.sh <pack-dir> <scratch-dir> <receipts-dir>
set -u
P=${1:?pack dir}
S=${2:?scratch dir}
R=${3:?receipts dir}
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
GATE=$LANE/tools/round-41/local-source-gate.py
REV=6b9e64fe7e0de202d9383baad5792fbfe039a743
mkdir -p "$R"
D=$(mktemp -d "$S/fx.XXXX") || exit 1
git clone -q --shared "$LANE" "$D/lane" || exit 1
top=$(git -C "$D/lane" rev-parse --show-toplevel)
[ "$top" = "$D/lane" ] || { echo "clone toplevel mismatch: $top"; exit 1; }
cp -a "$P/corpus/." "$D/lane/corpus/" || exit 1
cd "$S" || exit 1

echo "### P1. map vocabulary: can the frozen gate accept encoding/members keys?"
python3 - "$D/lane/corpus/evidence/local-sources.json" "$D/map-enc.json" <<'PY'
import json, sys
doc = json.load(open(sys.argv[1]))
for k, v in doc["sources"].items():
    if k.endswith("/data/typeinfo/golang/go1.25.0.json"):
        v["encoding"] = "gzip"
    if k.endswith("/lib/Base-src.zip"):
        v["members"] = ["ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java"]
json.dump(doc, open(sys.argv[2], "w"), indent=2, sort_keys=True)
PY
cp "$D/lane/corpus/evidence/local-sources.json" "$D/map-orig.json"
cp "$D/map-enc.json" "$D/lane/corpus/evidence/local-sources.json"
python3 -I -B "$GATE" --root "$D/lane" --rev "$REV" --json > "$R/p1-encoding-keys.json" 2> "$R/p1-encoding-keys.err"
echo "encoding-keys exit=$?"
cp "$D/map-orig.json" "$D/lane/corpus/evidence/local-sources.json"

echo "### P1b. map vocabulary: a new kind value 'compressed'"
python3 - "$D/lane/corpus/evidence/local-sources.json" "$D/map-kind.json" <<'PY'
import json, sys
doc = json.load(open(sys.argv[1]))
for k, v in doc["sources"].items():
    if k.endswith("/data/typeinfo/golang/go1.25.0.json"):
        v["kind"] = "compressed"
json.dump(doc, open(sys.argv[2], "w"), indent=2, sort_keys=True)
PY
cp "$D/map-kind.json" "$D/lane/corpus/evidence/local-sources.json"
python3 -I -B "$GATE" --root "$D/lane" --rev "$REV" --json > "$R/p1b-new-kind.json" 2> "$R/p1b-new-kind.err"
echo "new-kind exit=$?"
cp "$D/map-orig.json" "$D/lane/corpus/evidence/local-sources.json"

echo "### P2. source_sha256 drift: perturb the recorded pacman-db source digest"
python3 - "$D/lane/corpus/evidence/local-sources.json" "$D/map-src.json" <<'PY'
import json, sys
doc = json.load(open(sys.argv[1]))
for k, v in doc["sources"].items():
    if k.endswith("/pacman/sync/extra.db"):
        v["source_sha256"] = "1" * 64
json.dump(doc, open(sys.argv[2], "w"), indent=2, sort_keys=True)
PY
cp "$D/map-src.json" "$D/lane/corpus/evidence/local-sources.json"
python3 -I -B "$GATE" --root "$D/lane" --rev "$REV" --json > "$R/p2-source-drift.json" 2> "$R/p2-source-drift.err"
echo "source-drift exit=$?"
cp "$D/map-orig.json" "$D/lane/corpus/evidence/local-sources.json"

echo "### P2b. source_sha256 dropped entirely: does the row stay green?"
python3 - "$D/lane/corpus/evidence/local-sources.json" "$D/map-nosrc.json" <<'PY'
import json, sys
doc = json.load(open(sys.argv[1]))
for k, v in doc["sources"].items():
    v.pop("source_sha256", None)
json.dump(doc, open(sys.argv[2], "w"), indent=2, sort_keys=True)
PY
cp "$D/map-nosrc.json" "$D/lane/corpus/evidence/local-sources.json"
python3 -I -B "$GATE" --root "$D/lane" --rev "$REV" --json > "$R/p2b-no-source.json" 2> "$R/p2b-no-source.err"
echo "no-source exit=$?"
cp "$D/map-orig.json" "$D/lane/corpus/evidence/local-sources.json"

echo "### P3. gate tool byte identity: working tree vs the round-41 committed bytes"
git -C "$LANE" show 6b9e64fe7e0de202d9383baad5792fbfe039a743:tools/round-41/local-source-gate.py > "$R/gate-at-base.py"
sha256sum "$R/gate-at-base.py" "$GATE" | tee "$R/gate-tool-sha256.txt"
cmp -s "$R/gate-at-base.py" "$GATE"; echo "gate-tool-cmp exit=$?"
git -C "$LANE" log --oneline -1 -- tools/round-41/local-source-gate.py | tee "$R/gate-tool-history.txt"

echo "### P4. the pack's map must be the round-41 map plus the 17 new entries"
python3 - "$D/lane/corpus/evidence/local-sources.json" > "$R/map-entries.txt" <<'PY'
import json, sys
doc = json.load(open(sys.argv[1]))
for k in sorted(doc["sources"]):
    print("%s\t%s\t%s" % (k, doc["sources"][k]["copy"], doc["sources"][k]["sha256"]))
PY
wc -l < "$R/map-entries.txt"

rm -rf "$D"
