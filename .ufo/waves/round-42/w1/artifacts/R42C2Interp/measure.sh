#!/usr/bin/env bash
# measure.sh -- R42C2Interp reproduction driver.
#
# Runs the v4 interpreter selftest, then the cross-checks this seat's report cites:
#   1. selftest                                    (expect 113/113, exit 0)
#   2. probe-table parse                           (expect 13 rules, exit 0)
#   3. real legacy REA envelopes, v3 vs v4         (R41-CL4: unclassified -> step 6/8)
#   4. 52 round-41 held-out envelopes, v3 vs v4    (expect 52/52 identical pairs)
#   5. 4 round-41 C1 after.json receipts, v3 vs v4 (expect 4/4 identical pairs)
#
# Usage:  WORK=/fast/scratch/... ./measure.sh
#   LANE  lane root   (default /home/vgpnk/Projects/shokunin/kaidoku-shokunin)
#   WORK  scratch dir for outputs (must exist; honour TMPDIR, never hardcode /tmp)
#
# The v3 control interpreter is read from the base commit, never from the working
# tree:  git -C "$LANE" show c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c:tools/round-41/sqfs-triage-v3.py
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
LANE=${LANE:-/home/vgpnk/Projects/shokunin/kaidoku-shokunin}
WORK=${WORK:?set WORK to a scratch directory}
BASE=c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c
V4="$HERE/sqfs-triage-v4.py"
TABLE="$HERE/probe-table-v4.md"
V3="$WORK/sqfs-triage-v3.py"
mkdir -p "$WORK"
export TMPDIR="$WORK"

echo "== 1. selftest"
python3 -I -B "$V4" --selftest | tail -1
echo "selftest exit=${PIPESTATUS[0]}"

echo "== 2. probe table"
python3 -I -B "$V4" --skill "$TABLE" --table-only | head -2
echo "table-only exit=${PIPESTATUS[0]}"

echo "== control interpreter from $BASE"
git -C "$LANE" show "$BASE:tools/round-41/sqfs-triage-v3.py" > "$V3"
sha256sum "$V3"

echo "== 3. real legacy REA envelopes (evidence/envelopes/*)"
mapfile -t REAL < <(ls -1 "$HERE"/envelopes/*.json)
python3 -I -B "$V3" --skill "$LANE/SKILL.md" "${REAL[@]}" > "$WORK/v3-real.tsv"
echo "v3 exit=$?"
python3 -I -B "$V4" --skill "$TABLE" "${REAL[@]}" > "$WORK/v4-real.tsv"
echo "v4 exit=$?"
paste "$WORK/v3-real.tsv" "$WORK/v4-real.tsv" | awk -F'\t' '{printf "%-34s v3=%-22s v4=%-22s\n", $1, $2"/"$3, $5"/"$6}'

echo "== 4. round-41 held-out envelopes"
mapfile -t HELD < <(ls -1 "$LANE"/corpus/evidence/round-41/c2/heldout/*/envelope.json)
python3 -I -B "$V3" --skill "$LANE/SKILL.md" "${HELD[@]}" > "$WORK/v3-heldout.tsv"
echo "v3 exit=$? envelopes=${#HELD[@]}"
python3 -I -B "$V4" --skill "$TABLE" "${HELD[@]}" > "$WORK/v4-heldout.tsv"
echo "v4 exit=$?"
python3 - "$WORK/v3-heldout.tsv" "$WORK/v4-heldout.tsv" <<'PY'
import os, sys
def load(path):
    out = {}
    for line in open(path, encoding='utf-8'):
        line = line.rstrip('\n')
        if not line:
            continue
        p, label, action = line.split('\t')
        out[os.path.basename(os.path.dirname(p))] = (label, action)
    return out
a, b = load(sys.argv[1]), load(sys.argv[2])
keys = sorted(set(a) | set(b))
diff = [(k, a.get(k), b.get(k)) for k in keys if a.get(k) != b.get(k)]
print('heldout compared=%d identical=%d' % (len(keys), len(keys) - len(diff)))
for row in diff:
    print('DIFF', row)
PY

echo "== 5. round-41 C1 carriers (after.json receipts)"
mapfile -t C1 < <(ls -1 "$LANE"/corpus/evidence/round-41/c1/*/after.json)
python3 -I -B "$V3" --skill "$LANE/SKILL.md" "${C1[@]}" > "$WORK/v3-c1.tsv"
echo "v3 exit=$?"
python3 -I -B "$V4" --skill "$TABLE" "${C1[@]}" > "$WORK/v4-c1.tsv"
echo "v4 exit=$?"
paste "$WORK/v3-c1.tsv" "$WORK/v4-c1.tsv" | awk -F'\t' '{printf "%-16s v3=%-24s v4=%-24s\n", $1, $2"/"$3, $5"/"$6}'

echo "== 6. the base SKILL.md must be refused by the v4 interpreter"
python3 -I -B "$V4" --skill "$LANE/SKILL.md" --table-only
echo "base-skill exit=$? (expect 2 + a refused v3 marker)"
