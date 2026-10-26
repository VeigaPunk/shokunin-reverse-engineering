#!/bin/sh
# R41C2Gen — reproduce the round-41 v3 held-out dev proof exactly.
#
#   TMPDIR=/fast/scratch/hyaku/kaidoku-r41/R41C2Gen sh run-dev.sh
#
# Every lane path is absolute; all writes go to $TMPDIR, never to /tmp and never
# into the lane.  Nothing here touches vendor firmware bytes: the carriers are
# built from the lane's own writer.  REA runs only through its CLI, only on
# carriers this script builds.
set -eu
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
A=$LANE/.ufo/waves/round-41/w1/artifacts/R41C2Gen
GEN=$A/heldout-gen-v3.py
WRITER=$LANE/tools/round-40/gen-squashfs.py
BASE=49096c7e6f226af0c750c4b003be58883cb6049f
SEED=c9e30c103fab83c4a703aec5927cb26187cf67f18f6bc6ec29352f09097fe31b  # sha256("dev41")
S=${TMPDIR:?set TMPDIR to a scratch directory}
mkdir -p "$S"
cd "$S"
export TMPDIR="$S" HYAKU_SCRATCH=/fast/scratch/hyaku

echo "== 0. inputs =="
sha256sum "$GEN" "$WRITER"

echo "== 1. determinism selftest (no REA) =="
python3 -I -B "$GEN" --seed "$SEED" --selftest --scratch "$S" --gen "$WRITER"

echo "== 2. full dev set: build + one REA run per carrier + verify =="
python3 -I -B "$GEN" --seed "$SEED" --out "$S/dev" --run --verify \
        --scratch "$S" --gen "$WRITER"

echo "== 3. depth control: the same depth-limited carriers at --max-depth 3 =="
for id in H31 H33; do
    mkdir -p "$S/depthctl/$id"
    ( cd "$S/depthctl/$id"
      REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob \
        npx -y rea-agents@6.5.0 extract-firmware --format json --full-output \
            --max-depth 3 "$S/dev/$id/carrier.sqsh" "$S/depthctl/$id/out" \
        > env.json 2> err.txt
      echo "  $id depth-3 exit=$?" )
    python3 - "$S/depthctl/$id/env.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))['data']['normalized_result']
print('   handlers', sorted({c['handler'] for c in d['chunks'] if c.get('handler')}),
      '| gaps', sorted({g['kind'] for g in d['extraction_gaps']}),
      '| depth_limited_paths', len(d.get('depth_limited_paths') or []),
      '| files', len(d.get('files') or []))
PY
done

echo "== 4. lineage: rebuild the 13 v2 classes with the round-40 v2 generator =="
git -C "$LANE" show "$BASE:tools/round-40/heldout-gen-v2.py" > "$S/heldout-gen-v2.py"
python3 -I -B "$S/heldout-gen-v2.py" --seed "$SEED" --out "$S/v2dev" \
        --classes clean-be,clean-le,clean-empty,escaping-symlink-removed,\
in-tree-symlink-metadata,mixed-symlinks,dep-missing-be,dep-missing-le,\
avm-marker-be-dropped,body-extractor-failure,partial-body-failure,\
no-squashfs-chunk,out-of-domain --gen "$WRITER"
python3 - "$S/v2dev/manifest.json" "$S/dev/manifest.json" <<'PY'
import json, sys
a = {c['id']: (c['class'], c['sha256'], c['compression'])
     for c in json.load(open(sys.argv[1]))['carriers']}
b = {c['id']: (c['class'], c['sha256'], c['compression'])
     for c in json.load(open(sys.argv[2]))['carriers']}
same = [i for i in sorted(a) if a[i][1] == b[i][1]]
diff = [i for i in sorted(a) if a[i][1] != b[i][1]]
print('   byte-identical v2 -> v3:', len(same), 'of', len(a))
for i in diff:
    print('   differs:', i, a[i][0], a[i][2], '->', b[i][2])
PY

echo "== 5. action vocabulary bind: red on the round-40 line, green on a v3 line =="
printf 'probe\n<!-- sqfs-triage-actions: none confirm-empty expect-link-absent count-gap audit-symlinks install-extractor-be install-extractor-le wrap-extractor-be preserve-failure salvage-partial extract-nested inspect-input -->\n' > "$S/v3-actions.md"
set +e
python3 -I -B "$GEN" --seed "$SEED" --out "$S/act-red" --classes clean-be \
        --actions-set interp --actions-file "$LANE/SKILL.md" --gen "$WRITER"
echo "   round-40 SKILL line exit=$? (expect 1: 'extract-nested' undeclared)"
python3 -I -B "$GEN" --seed "$SEED" --out "$S/act-green" --classes clean-be \
        --actions-set interp --actions-file "$S/v3-actions.md" --gen "$WRITER" \
        >/dev/null
echo "   v3-shaped line exit=$? (expect 0)"
set -e

echo "== 6. combo family: factor draws and how many are outside the named tuples =="
python3 - "$S/dev/manifest.json" <<'PY'
import json, sys
m = json.load(open(sys.argv[1]))
named = {c['id']: c for c in m['carriers'] if c['class'] != 'combo'}
combos = [c for c in m['carriers'] if c['class'] == 'combo']
named_tuples = {json.dumps(c['declared'], sort_keys=True) for c in named.values()}
outside = 0
print('   id   endian in_tree escaping partial comp   depth | declared G / be / sr / P | inside named set')
for c in combos:
    f = c['factors']
    d = c['declared']
    hit = json.dumps(d, sort_keys=True) in named_tuples
    outside += 0 if hit else 1
    print('   %s  %-6s %-7d %-8d %-7d %-6s %-5d | %-40s %-3s %-5s %-8s | %s'
          % (c['id'], f['endian'], f['in_tree'], f['escaping'], f['partial'],
             f['comp'], f['max_depth'], ','.join(d['gap_kinds']) or '-',
             d['be_argv'], d['symlink_removed'], d['published'],
             'yes' if hit else 'NO'))
print('   %d of %d combos fall OUTSIDE the named class tuples' % (outside, len(combos)))
PY
