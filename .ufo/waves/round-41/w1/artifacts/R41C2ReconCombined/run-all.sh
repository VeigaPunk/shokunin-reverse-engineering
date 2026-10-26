#!/usr/bin/env bash
# Reproduce every R41C2ReconCombined measurement.  Dev-only: all carriers are
# synthetic and land in scratch; no vendor byte is fetched, copied or needed.
#
#   S=<scratch> bash run-all.sh
#
# Needs: git (read-only), python3, unblob 26.6.4, sasquatch-v4be 4.5.1,
# npx/node (rea-agents 6.5.0 fetched into the npx cache), and a lane checkout at
# /home/vgpnk/Projects/shokunin/kaidoku-shokunin.
set -euo pipefail

S=${S:?set S to a scratch dir}
LANE=${LANE:-/home/vgpnk/Projects/shokunin/kaidoku-shokunin}
REV=${REV:-49096c7e6f226af0c750c4b003be58883cb6049f}
HERE=$(cd "$(dirname "$0")" && pwd)

mkdir -p "$S/frozen" "$S/dev" "$S/absorb" "$S/runs" "$S/direct"
cd "$S"
export TMPDIR="$S"

# --- frozen inputs (the round-40 tools and SKILL at the base revision) -------
for f in gen-squashfs.py heldout-gen-v2.py sqfs-triage-v2.py; do
  git -C "$LANE" show "$REV:tools/round-40/$f" > "$S/frozen/$f"
done
git -C "$LANE" show "$REV:SKILL.md" > "$S/frozen/SKILL.md"
sha256sum "$S"/frozen/*.py "$S"/frozen/SKILL.md

# --- round-40 partial recipe + symlinks, gzip and xz ------------------------
build() { python3 -I -B "$HERE/build-combined.py" --frozen "$S/frozen" --out "$S/dev" "$@"; }
build --name gzip-ff-intree      --comp gzip --fill ff --links in-tree
build --name gzip-ff-mixed       --comp gzip --fill ff --links escaping,in-tree
build --name gzip-ff-none        --comp gzip --fill ff --links ''
build --name gzip-00-intree      --comp gzip --fill 00 --links in-tree
build --name xz-ff-intree        --comp xz   --fill ff --links in-tree
build --name xz-00-intree        --comp xz   --fill 00 --links in-tree
build --name clean-mixed         --comp gzip --fill none --links escaping,in-tree
build --name gzip-semi-00-intree --comp gzip --fill 00 --links in-tree --content semi
build --name gzip-semi-ff-intree --comp gzip --fill ff --links in-tree --content semi
build --name xz-semi-00-intree   --comp xz   --fill 00 --links in-tree --content semi
build --name xz-semi-ff-intree   --comp xz   --fill ff --links in-tree --content semi

# --- compressed-length determinant probe (large damaged block) --------------
for spec in "gzip 00" "gzip ff" "xz 00" "xz ff"; do
  set -- $spec
  mkdir -p "$S/absorb/$1-$2"
  python3 -I -B "$HERE/absorb-probe.py" --frozen "$S/frozen" \
      --out "$S/absorb/$1-$2" --comp "$1" --fill "$2" \
      > "$S/absorb/$1-$2/probe.json"
done

# --- direct extractor (unblob's argv shape) ---------------------------------
for d in "$S"/absorb/*/; do
  n=$(basename "$d"); mkdir -p "$d/extract"
  sasquatch-v4be -be -no-exit-code -f -d "$d/extract" "$d/carrier.sqsh" \
      > "$d/stdout.txt" 2> "$d/stderr.txt" || true
  echo "$n published=$(find "$d/extract" -type f | wc -l) fatal=$(grep -c FATAL "$d/stderr.txt" || true)"
done

# --- REA 6.5.0 extract-firmware (one fresh outdir per run) ------------------
rea() {  # rea <input> <run-name> [extra argv...]
  local in=$1 rn=$2; shift 2
  local d="$S/runs/$rn"; mkdir -p "$d"
  ( cd "$d" && REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob \
      npx -y rea-agents@6.5.0 extract-firmware --format json --full-output \
      "$@" "$S/dev/$in/carrier.sqsh" "$d/out" > stdout.json 2> stderr.txt )
  echo "$rn exit=$?"
}
rea gzip-ff-intree    gzip-ff-intree       --max-depth 1
rea gzip-ff-intree    gzip-ff-intree-nod1
rea gzip-ff-intree    gzip-ff-intree-lite   --max-depth 1     # without --full-output
rea gzip-ff-mixed     gzip-ff-mixed        --max-depth 1
rea gzip-ff-mixed     gzip-ff-mixed-nod1
rea gzip-ff-none      gzip-ff-none         --max-depth 1
rea gzip-00-intree    gzip-00-intree-d1    --max-depth 1
rea xz-ff-intree      xz-ff-intree-d1      --max-depth 1
rea xz-00-intree      xz-00-intree-d1      --max-depth 1
rea clean-mixed       clean-mixed-d1       --max-depth 1
rea clean-mixed       clean-mixed-nod1

rea_abs() {  # same, for a carrier outside dev/
  local in=$1 rn=$2; shift 2
  local d="$S/runs/$rn"; mkdir -p "$d"
  ( cd "$d" && REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob \
      npx -y rea-agents@6.5.0 extract-firmware --format json --full-output \
      "$@" "$in" "$d/out" > stdout.json 2> stderr.txt )
  echo "$rn exit=$?"
}
rea_abs "$S/absorb/gzip-00/carrier.sqsh" absorb-gzip-00-d1 --max-depth 1
rea_abs "$S/absorb/xz-00/carrier.sqsh"   absorb-xz-00-d1   --max-depth 1
rea_abs "$S/absorb/gzip-00/carrier.sqsh" absorb-gzip-00-nod1

# --- features, v2 labels, draft-v3 precedence -------------------------------
runs=$(ls -d "$S"/runs/*/ | sed 's#/$##')
python3 -I -B "$HERE/feature-scan.py" --skill "$S/frozen/SKILL.md" $runs \
    > "$S/features.jsonl" 2> "$S/features.md"
envs=""; for r in $runs; do envs="$envs $r/stdout.json"; done
python3 -I -B "$HERE/v3-precedence.py" $envs > "$S/v3.jsonl"

# --- draft-v3 regression against the round-40 held-out labels ---------------
H="$LANE/corpus/evidence/round-40/c2/heldout"
python3 -I -B "$HERE/v3-precedence.py" "$H"/H*/envelope.json > "$S/v3-heldout.jsonl"
python3 - "$H/manifest.json" "$S/v3-heldout.jsonl" <<'PY'
import json, sys
man = {c['id']: c for c in json.load(open(sys.argv[1]))['carriers']}
bad = 0
for line in open(sys.argv[2]):
    r = json.loads(line); cid = r['path'].split('/')[-2]
    exp = (man[cid]['label'], man[cid]['action'])
    got = (r['label'], r['action'])
    bad += got != exp
    print(cid, man[cid]['class'], 'expected', exp, 'v3', got, 'rule', r['rule'],
          'OK' if got == exp else 'MISMATCH')
print('mismatches', bad)
PY
