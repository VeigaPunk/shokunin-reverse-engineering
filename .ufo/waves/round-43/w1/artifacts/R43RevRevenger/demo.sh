#!/usr/bin/env bash
# R43RevRevenger wave-1 demonstration script (reproduces every cited number).
#
# Rebuild prerequisites (all outside the lane):
#   S=/fast/scratch/hyaku/kaidoku-r43/w1-R43RevRevenger
#   git -C <lane> show 6b9e64fe7e0de202d9383baad5792fbfe039a743:tools/round-42/heldout-gen-v4.py > $S/gen.py
#   cp <lane>/tools/round-39/gen-squashfs.py $S/writer.py
#   cp <lane>/tools/round-42/fixtures.json  $S/fixtures.json
#   patch -p0 < placement.patch   # or cp gen-r43.py (frozen port, sha256 below)
#
# Every command below is run from "$S"; TMPDIR is set per step so nothing lands
# in /tmp and unblob.log never lands in a cwd that matters.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
S=${S:-/fast/scratch/hyaku/kaidoku-r43/w1-R43RevRevenger}
SEED=d1681696dd63ca4f9b8a09ffa8fa3e2de5e2b51b
FX=$LANE/corpus/evidence/round-42/c2/fixtures
cd "$S" || exit 1

run() { echo; echo "\$ $*"; "$@"; echo "EXIT=$?"; }

echo "== generator identity =="
sha256sum gen.py gen-r43.py writer.py fixtures.json

echo
echo "== (a) FROZEN v4: --out with NO --run writes a manifest with zero envelopes =="
rm -rf demo-a; mkdir -p demo-tmp-a
run python3 -I -B gen.py --seed "$SEED" --out "$S/demo-a" --classes clean-le \
    --gen "$S/writer.py" --fixture-pins "$S/fixtures.json" --scratch "$S/demo-tmp-a" \
    --fixtures-dir "$FX"
echo "manifest present: $(test -f demo-a/manifest.json && echo yes || echo no)"
echo "envelopes written: $(ls demo-a/*/envelope.json 2>/dev/null | wc -l)"
sha256sum demo-a/manifest.json

echo
echo "== (b) PATCHED: --out with no --run refuses before building (exit 4) =="
rm -rf demo-b
run python3 -I -B gen-r43.py --seed "$SEED" --out "$S/demo-b" --classes clean-le \
    --gen "$S/writer.py" --fixture-pins "$S/fixtures.json" --scratch "$S/demo-tmp-a" \
    --fixtures-dir "$FX"
echo "out dir created: $(test -d demo-b && echo yes || echo no)"

echo
echo "== (c) PATCHED: --carriers-only builds carriers, never a manifest (exit 0) =="
rm -rf demo-c
run python3 -I -B gen-r43.py --seed "$SEED" --out "$S/demo-c" --classes clean-le --carriers-only \
    --gen "$S/writer.py" --fixture-pins "$S/fixtures.json" --scratch "$S/demo-tmp-a" \
    --fixtures-dir "$FX"
echo "manifest present: $(test -f demo-c/manifest.json && echo yes || echo no)"
sha256sum demo-c/H*/carrier.sqsh

echo
echo "== (d) PATCHED: full --run, refusal passes, manifest written LAST =="
rm -rf demo-d; mkdir -p demo-tmp-d
run python3 -I -B gen-r43.py --seed "$SEED" --out "$S/demo-d" --classes clean-le --run \
    --gen "$S/writer.py" --fixture-pins "$S/fixtures.json" --scratch "$S/demo-tmp-d" \
    --fixtures-dir "$FX"
python3 -c "import json;m=json.load(open('demo-d/manifest.json'));print('tuple_check.all_equal',m['generator']['tuple_check']['all_equal'],'checked',m['generator']['tuple_check']['carriers_checked'])"

echo
echo "== (e) MUTATION: one declared gap added for clean-le -> REFUSE, no manifest (exit 3) =="
sed "s/'clean-le': dict(handler='le', gaps=(), sr=False, failed=False,/'clean-le': dict(handler='le', gaps=('extractor-failure',), sr=False, failed=False,/" \
    gen-r43.py > demo-lie.py
rm -rf demo-e; mkdir -p demo-tmp-e
run python3 -I -B demo-lie.py --seed "$SEED" --out "$S/demo-e" --classes clean-le --run \
    --gen "$S/writer.py" --fixture-pins "$S/fixtures.json" --scratch "$S/demo-tmp-e" \
    --fixtures-dir "$FX"
echo "manifest present: $(test -f demo-e/manifest.json && echo yes || echo no)"

echo
echo "== (f) CTL-C1-2 RED: the patched generator's --tuple-check on the round-42 held-out set =="
run python3 -I -B gen-r43.py --tuple-check "$LANE/corpus/evidence/round-42/c2/heldout"

echo
echo "== (g) GREEN on the same 78 envelopes: C02's declared set to what its envelope shows =="
echo "    (control only, via the standalone prototype's --declared-from; a claim never uses it."
echo "     The generator-level green is step (d): the real run's own tuple check PASS.)"
run python3 -I -B "$HERE/tuple-check-proto.py" --dir "$LANE/corpus/evidence/round-42/c2/heldout" \
    --declared-from "$HERE/ctl-c1-2-green-declared.json" --json-out "$HERE/ctl-c1-2-green.json"

echo
echo "== (h) manifest delta: frozen v4 no-run manifest vs patched run manifest =="
run python3 -I -B "$HERE/manifest-delta.py" "$S/demo-a/manifest.json" "$S/demo-d/manifest.json"

echo
echo "== (i) patched --run --verify on the subset (pre-existing combo_unseen FAIL) =="
rm -rf demo-i; mkdir -p demo-tmp-i
run python3 -I -B gen-r43.py --seed "$SEED" --out "$S/demo-i" --classes clean-le --run --verify \
    --gen "$S/writer.py" --fixture-pins "$S/fixtures.json" --scratch "$S/demo-tmp-i" \
    --fixtures-dir "$FX"

echo
echo "== (j) frozen v4 --run --verify on the same subset: regen manifest == the no-run manifest =="
rm -rf demo-j; mkdir -p demo-tmp-j
run python3 -I -B gen.py --seed "$SEED" --out "$S/demo-j" --classes clean-le --run --verify \
    --gen "$S/writer.py" --fixture-pins "$S/fixtures.json" --scratch "$S/demo-tmp-j" \
    --fixtures-dir "$FX"
sha256sum demo-a/manifest.json demo-j/manifest.json

echo
echo "== (k) C02-shape incidence over 500 seeds (frozen combo_draw/combo_factors) =="
python3 -B "$HERE/c02-shape-sim.py" gen.py fixtures.json
