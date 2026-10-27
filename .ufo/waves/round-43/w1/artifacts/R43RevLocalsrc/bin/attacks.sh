#!/usr/bin/env bash
set -u
D=$(cat /fast/scratch/hyaku/kaidoku-r43/w1-R43RevLocalsrc/attackdir.txt)
LANE=$D/lane
GATE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-41/local-source-gate.py
REV=c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c
MAP=$LANE/corpus/evidence/local-sources.json
ORIG_MAP=$(cat "$MAP")
OUT=/fast/scratch/hyaku/kaidoku-r43/w1-R43RevLocalsrc/receipts/attacks
mkdir -p "$OUT"

gate() {  # $1 name; runs gate, records exit + failed rows + per-path reasons
  local name=$1
  python3 -I -B "$GATE" --root "$LANE" --rev "$REV" --json > "$OUT/$name.json" 2> "$OUT/$name.err"
  local ex=$?
  python3 - "$OUT/$name.json" "$name" "$ex" <<'PY'
import json, sys
try:
    d = json.load(open(sys.argv[1]))
    reasons = {}
    for rec in d["records"]:
        for p in rec["paths"]:
            if not p["ok"]:
                reasons.setdefault(p["reason"], []).append(rec["id"])
    print("%-28s exit=%s failed=%s reasons=%s" % (sys.argv[2], sys.argv[3], d["rows_failed"], reasons))
except Exception as e:
    print("%-28s exit=%s  (unparseable: %s)" % (sys.argv[2], sys.argv[3], open(sys.argv[1]).read()[:200]))
PY
}

restore() {
  printf '%s' "$ORIG_MAP" > "$MAP"
  git -C "$LANE" checkout -- corpus/evidence/round-42/local-sources 2>/dev/null
}

cp -a /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-42/w1/artifacts/R42LocalSrc/corpus/. "$LANE/corpus/"

echo "== baseline =="
gate 00-baseline

echo "== A. non-existent copy (S007 entry copy deleted from map path) =="
rm "$LANE/corpus/evidence/round-42/local-sources/S007/ChangeHistory.md"
gate 01-A-nonexistent
git -C "$LANE" checkout -- corpus/evidence/round-42/local-sources 2>/dev/null || cp -a /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-42/w1/artifacts/R42LocalSrc/corpus/evidence/round-42/local-sources/S007/ChangeHistory.md "$LANE/corpus/evidence/round-42/local-sources/S007/ChangeHistory.md"
[ -f "$LANE/corpus/evidence/round-42/local-sources/S007/ChangeHistory.md" ] || cp -a /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-42/w1/artifacts/R42LocalSrc/corpus/evidence/round-42/local-sources/S007/ChangeHistory.md "$LANE/corpus/evidence/round-42/local-sources/S007/ChangeHistory.md"

echo "== B1. copy is a symlink to another in-lane file =="
TGT=$LANE/corpus/evidence/round-42/local-sources/S007/ChangeHistory.md
mv "$TGT" "$TGT.real"
ln -s "S006/BSimTutorial_Intro.md" "$LANE/corpus/evidence/round-42/local-sources/S007/ChangeHistory.md" 2>/dev/null || true
# relative symlink within same dir:
rm "$LANE/corpus/evidence/round-42/local-sources/S007/ChangeHistory.md"
ln -s "../S006/BSimTutorial_Intro.md" "$LANE/corpus/evidence/round-42/local-sources/S007/ChangeHistory.md"
gate 02-B1-symlink-inlane-wrongdigest
echo "== B2. symlink to in-lane file with correct digest (self-link) =="
rm "$LANE/corpus/evidence/round-42/local-sources/S007/ChangeHistory.md"
ln -s "ChangeHistory.md.real" "$LANE/corpus/evidence/round-42/local-sources/S007/ChangeHistory.md"
gate 03-B2-symlink-rightdigest
echo "== B3. symlink OUT of lane to host file (digest matches) =="
rm "$LANE/corpus/evidence/round-42/local-sources/S007/ChangeHistory.md"
ln -s "/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/ChangeHistory.md" "$LANE/corpus/evidence/round-42/local-sources/S007/ChangeHistory.md"
gate 04-B3-symlink-outoflane
echo "== B4. dangling symlink =="
rm "$LANE/corpus/evidence/round-42/local-sources/S007/ChangeHistory.md"
ln -s "/nonexistent/nothing.md" "$LANE/corpus/evidence/round-42/local-sources/S007/ChangeHistory.md"
gate 05-B4-dangling-symlink
rm "$LANE/corpus/evidence/round-42/local-sources/S007/ChangeHistory.md"
mv "$TGT.real" "$TGT" 2>/dev/null || cp -a /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-42/w1/artifacts/R42LocalSrc/corpus/evidence/round-42/local-sources/S007/ChangeHistory.md "$TGT"

echo "== C1. copy outside stated dir but inside lane (tools/stub.bin, right bytes) =="
mkdir -p "$LANE/tools"
cp "$LANE/corpus/evidence/round-42/local-sources/S007/ChangeHistory.md" "$LANE/tools/stub-copy.bin"
python3 - "$MAP" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
k = "/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/ChangeHistory.md"
d["sources"][k]["copy"] = "tools/stub-copy.bin"
json.dump(d, open(sys.argv[1], "w"), indent=2, sort_keys=True)
PY
gate 06-C1-copy-tools-dir
echo "== C2. copy inside .git =="
cp "$LANE/corpus/evidence/round-42/local-sources/S007/ChangeHistory.md" "$LANE/.git/stub-copy.bin"
python3 - "$MAP" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
k = "/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/ChangeHistory.md"
d["sources"][k]["copy"] = ".git/stub-copy.bin"
json.dump(d, open(sys.argv[1], "w"), indent=2, sort_keys=True)
PY
gate 07-C2-copy-inside-dotgit
printf '%s' "$ORIG_MAP" > "$MAP"

echo "== D1. row-pinned S126: map keeps row digest, copy stubbed =="
printf 'stub-bytes-not-the-tsv' > "$LANE/corpus/evidence/round-41/s126/lead1-avm-image.tsv"
gate 08-D1-pinned-stub-copy
git -C "$LANE" checkout -- corpus/evidence/round-41/s126/lead1-avm-image.tsv
echo "== D2. row-pinned S126: map sha set to stub's digest =="
printf 'stub-bytes-not-the-tsv' > "$LANE/corpus/evidence/round-41/s126/lead1-avm-image.tsv"
STUBSHA=$(sha256sum "$LANE/corpus/evidence/round-41/s126/lead1-avm-image.tsv" | cut -d' ' -f1)
python3 - "$MAP" "$STUBSHA" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
k = "/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/lead1-avm-image.tsv"
d["sources"][k]["sha256"] = sys.argv[2]
json.dump(d, open(sys.argv[1], "w"), indent=2, sort_keys=True)
PY
gate 09-D2-pinned-stub-digest
git -C "$LANE" checkout -- corpus/evidence/round-41/s126/lead1-avm-image.tsv
printf '%s' "$ORIG_MAP" > "$MAP"

echo "== D3. UNPINNED row S007: stub copy + map sha = stub digest =="
printf 'i am a stub, not ChangeHistory' > "$LANE/corpus/evidence/round-42/local-sources/S007/ChangeHistory.md"
STUBSHA=$(sha256sum "$LANE/corpus/evidence/round-42/local-sources/S007/ChangeHistory.md" | cut -d' ' -f1)
python3 - "$MAP" "$STUBSHA" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
k = "/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/ChangeHistory.md"
d["sources"][k]["sha256"] = sys.argv[2]
json.dump(d, open(sys.argv[1], "w"), indent=2, sort_keys=True)
PY
gate 10-D3-unpinned-stub
printf '%s' "$ORIG_MAP" > "$MAP"
cp -a /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-42/w1/artifacts/R42LocalSrc/corpus/evidence/round-42/local-sources/S007/ChangeHistory.md "$LANE/corpus/evidence/round-42/local-sources/S007/ChangeHistory.md"

echo "== E. alias: S040 entry points at S056's copy + digest =="
python3 - "$MAP" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
src = "/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/cliCommandNames.js"
tgt = "/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/cli/artifactCommands.js"
d["sources"][tgt]["copy"] = d["sources"][src]["copy"]
d["sources"][tgt]["sha256"] = d["sources"][src]["sha256"]
json.dump(d, open(sys.argv[1], "w"), indent=2, sort_keys=True)
PY
gate 11-E-alias
printf '%s' "$ORIG_MAP" > "$MAP"

echo "== F. duplicate JSON key (S007 entry textually twice; first = stub) =="
python3 - "$MAP" <<'PY'
import json, sys
txt = open(sys.argv[1]).read()
d = json.loads(txt)
k = "/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/ChangeHistory.md"
stub = json.dumps({k: {"copy": "corpus/evidence/round-42/local-sources/S006/BSimTutorial_Intro.md",
                       "sha256": "0"*64, "kind": "file"}}, sort_keys=True)[1:-1]
good = json.dumps({k: d["sources"][k]}, sort_keys=True)[1:-1]
# inject stub first, then the real entry again, inside "sources"
marker = '"sources": {'
i = txt.index(marker) + len(marker)
txt2 = txt[:i] + "\n" + stub + ",\n" + good + "," + txt[i:]
open(sys.argv[1], "w").write(txt2)
PY
gate 12-F-dup-key-stub-first
printf '%s' "$ORIG_MAP" > "$MAP"

echo "== G. copy is a directory =="
python3 - "$MAP" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
k = "/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/ChangeHistory.md"
d["sources"][k]["copy"] = "corpus/evidence/round-42/local-sources/S007"
json.dump(d, open(sys.argv[1], "w"), indent=2, sort_keys=True)
PY
gate 13-G-copy-is-dir
printf '%s' "$ORIG_MAP" > "$MAP"

echo "== H1. copy path escapes root via .. =="
python3 - "$MAP" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
k = "/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/ChangeHistory.md"
d["sources"][k]["copy"] = "../../etc/hostname"
json.dump(d, open(sys.argv[1], "w"), indent=2, sort_keys=True)
PY
gate 14-H1-dotdot-escape
echo "== H2. absolute copy =="
python3 - "$MAP" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
k = "/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/ChangeHistory.md"
d["sources"][k]["copy"] = "/etc/hostname"
json.dump(d, open(sys.argv[1], "w"), indent=2, sort_keys=True)
PY
gate 15-H2-absolute-copy
echo "== H3. copy is the external path itself =="
python3 - "$MAP" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
k = "/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/ChangeHistory.md"
d["sources"][k]["copy"] = k
json.dump(d, open(sys.argv[1], "w"), indent=2, sort_keys=True)
PY
gate 16-H3-copy-is-external
printf '%s' "$ORIG_MAP" > "$MAP"

echo "== I1. extra entry key not referenced by any row (harmless?) =="
python3 - "$MAP" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
d["sources"]["/nonexistent/orphan/path.bin"] = {"copy": "corpus/evidence/round-42/local-sources/S006/BSimTutorial_Intro.md", "sha256": "a23562a3175409a66e12e5ba47bd19e218cd7868b03bc3210c4ae7e0d296c33e", "kind": "file"}
json.dump(d, open(sys.argv[1], "w"), indent=2, sort_keys=True)
PY
gate 17-I1-orphan-entry
printf '%s' "$ORIG_MAP" > "$MAP"

echo "== I2. unknown key inside an entry =="
python3 - "$MAP" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
k = "/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/ChangeHistory.md"
d["sources"][k]["comment"] = "sneaky"
json.dump(d, open(sys.argv[1], "w"), indent=2, sort_keys=True)
PY
gate 18-I2-unknown-key
printf '%s' "$ORIG_MAP" > "$MAP"

echo "== I3. map absent entirely =="
mv "$MAP" "$MAP.gone"
gate 19-I3-map-absent
mv "$MAP.gone" "$MAP"

echo "== final restore check =="
gate 99-restored
