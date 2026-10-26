#!/usr/bin/env bash
# run-matrix.sh - reproduce the R42C1Oracle validation matrix.
#
#   ./run-matrix.sh <fixtures-dir> <runs-dir> <matrix.tsv> [extra-image ...]
#
# <fixtures-dir> holds the unblob 26.6.4 SquashFS fixtures (see
# fixtures/MANIFEST.tsv for the sha256 of every input and its source URL).
# Every fixture is run in FULL mode; fixtures under a v4/ path get
# --dev-allow-v4 so the listing parsers are exercised on a real tree (v4 is
# never part of the C1 contract).  Extra images (OpenWrt chunks, round-41
# carriers) are appended to the matrix with their own full-mode run.
#
# Scratch layout: work roots live under $TMPDIR (or $PWD/work when TMPDIR is
# unset) - never /tmp - and are kept so the run record matches the tree.
set -u
FIX=${1:?fixtures dir}; RUNS=${2:?runs dir}; MATRIX=${3:?matrix tsv}
shift 3 || true
ORACLE=$(cd "$(dirname "$0")" && pwd)/sqfs3-oracle.py
export TMPDIR=${TMPDIR:-$PWD/work}
mkdir -p "$TMPDIR" "$RUNS" "$(dirname "$MATRIX")"
printf 'input\tmagic\tversion\tbh_kind\tbh_total\tbh_complete\tz_total\tz_complete\tverdict\texit\treason\tregular_rows\tnonregular_rows\n' > "$MATRIX"

run_one() {
  local img=$1 tag=$2 extra=""
  case "$img" in */v4/*) extra="--dev-allow-v4" ;; esac
  local w="$TMPDIR/work.$(echo "$tag" | tr '/' '_')"
  local out="$RUNS/$tag"; mkdir -p "$out"
  python3 -I "$ORACLE" $extra --work "$w" --files "$out/oracle.tsv" \
      --nonregular "$out/nonregular.tsv" --json "$out/oracle-run.json" "$img" \
      >/dev/null 2>"$out/stderr.txt"
  local rc=$?
  python3 - "$out/oracle-run.json" "$rc" "$tag" "$MATRIX" <<'PY'
import json, sys
path, rc, tag, matrix = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
try:
    d = json.load(open(path))
except Exception as exc:                       # noqa: BLE001
    open(matrix, 'a').write('%s\tmissing-json\t\t\t\t\t\t\t\t%s\t%s\t\t\n'
                            % (tag, rc, exc))
    raise SystemExit(0)
lay = d.get('layout') or {}
b = (d.get('producers') or {}).get('backhand') or {}
u = (d.get('producers') or {}).get('unsquashfs') or {}
z = (d.get('producers') or {}).get('7z') or {}
cc = d.get('cross_check') or {}
t = d.get('tables') or {}
open(matrix, 'a').write(
    '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (
        tag, lay.get('magic', ''), lay.get('version', ''),
        b.get('kind', ''), (b.get('counts') or {}).get('total', ''),
        b.get('complete', ''),
        (z.get('counts') or {}).get('total', ''), z.get('complete', ''),
        cc.get('verdict', ''), rc, d.get('reason') or '',
        t.get('regular_rows', ''), t.get('nonregular_rows', '')))
PY
}

cd "$FIX" || exit 1
for f in $(find . -name '*.bin' -o -name '*.squashfs' | sed 's|^\./||' | sort); do
  run_one "$FIX/$f" "${f%/*}/${f##*/}"
done
for img in "$@"; do
  run_one "$img" "external/$(basename "$(dirname "$img")")__$(basename "$img")"
done
wc -l "$MATRIX"
