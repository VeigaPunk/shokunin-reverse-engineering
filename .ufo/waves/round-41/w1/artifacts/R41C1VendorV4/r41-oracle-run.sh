#!/usr/bin/env bash
# R41-C1 oracle arm, round-41 port of tools/round-40/c1-run.sh `oracle` mode.
#
#   r41-oracle-run.sh CARRIER OUTDIR WORK
#
# Two independent producers, one frozen grammar (identical to round 40):
#   1. tools/round-40/sqfs-list.py --layout avm  (BE structural fields,
#      LITTLE-endian metadata/data block-length headers)
#      -> OUTDIR/oracle.tsv      relpath TAB sha256 TAB size   (regular files)
#      -> OUTDIR/nonregular.tsv  relpath TAB kind TAB detail
#   2. sasquatch-v4be WITHOUT -be (the argv unblob 26.6.4 picks when
#      mkfs_time == bytes_used), forced with -f -no-exit-code (an unprivileged
#      run cannot create device nodes) -> OUTDIR/oracle-check.tsv.
#   A disagreement on any relpath/sha256/size is a tool failure (exit 3).
#
# WORK is required (no hardcoded /tmp); TMPDIR points inside the private
# scratch, which is removed on exit. WORK must carry a /kaidoku-r41/ segment:
# the recorded scratch_root proves the run happened this round.
#
# Differences from the round-40 arm: CLAIM/schema are round-41, and the
# provenance segment is /kaidoku-r41/ instead of /kaidoku-r40/. Everything the
# frozen grammar defines (table formats, validation, cross-check) is unchanged.
#
# Exit: 0 ok, 2 usage/environment error, 3 tool failure.
set -euo pipefail

PROG=$(basename "$0")
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin

usage() {
  cat >&2 <<'EOF'
usage: r41-oracle-run.sh CARRIER OUTDIR WORK
  CARRIER  AVM-layout big-endian SquashFS v4 image (sqsh magic)
  OUTDIR   existing or creatable output directory for the tables
  WORK     scratch directory (required; must contain /kaidoku-r41/)
  env      C1_READER (default <lane>/tools/round-40/sqfs-list.py)
EOF
  exit 2
}

err() { echo "$PROG: $*" >&2; exit 2; }
fail() { echo "$PROG: $*" >&2; exit 3; }

[[ $# -eq 3 ]] || usage
carrier_in=$1 outdir_in=$2 work_in=$3
[[ -f $carrier_in ]] || err "carrier is not a regular file: $carrier_in"
[[ -r $carrier_in ]] || err "carrier is not readable: $carrier_in"
command -v python3 >/dev/null || err "python3 not found on PATH"
command -v jq >/dev/null || err "jq not found on PATH"

work=$(realpath -m -- "$work_in")
case "$work/" in
  */kaidoku-r41/*) ;;
  *) err "WORK $work lacks a /kaidoku-r41/ segment (round-41 run provenance)" ;;
esac
mkdir -p "$work" || err "cannot create WORK: $work"

carrier=$(realpath -- "$carrier_in")
carrier_sha=$(sha256sum "$carrier" | cut -d' ' -f1)
carrier_size=$(stat -c%s "$carrier")

mkdir -p "$outdir_in" || err "cannot create OUTDIR: $outdir_in"
outdir=$(realpath -- "$outdir_in")

scratch=$(mktemp -d "$work/oracle.XXXXXX")
scratch=$(realpath -- "$scratch")
trap 'rm -rf -- "$scratch"' EXIT
export TMPDIR=$scratch

arr_json() { printf '%s\n' "$@" | jq -R . | jq -s -c .; }

sq_pin() {
  sq=$(command -v sasquatch-v4be || true)
  [[ -n $sq ]] || err "sasquatch-v4be not resolvable on PATH (the arm requires the BE extractor)"
  sq=$(realpath -- "$sq")
  sq_sha=$(sha256sum "$sq" | cut -d' ' -f1)
  sq_line=$("$sq" -version 2>&1 | sed -n 1p || true)
  sq_ver=$(printf '%s' "$sq_line" | sed -nE 's/.*[Vv]ersion ([0-9][0-9A-Za-z.]*).*/\1/p')
  [[ -n $sq_ver ]] || sq_ver=unknown
}

magic_scan() {
  python3 -I - "$carrier" <<'PY'
import sys
raw = open(sys.argv[1], 'rb').read(1 << 20)
be = raw.find(b'sqsh')
le = raw.find(b'hsqs')
if be >= 0 and (le < 0 or be <= le):
    print('sqsh', be)
elif le >= 0:
    print('hsqs', le)
else:
    print('none', -1)
PY
}

reader_in=${C1_READER:-$LANE/tools/round-40/sqfs-list.py}
[[ -f $reader_in ]] || err "reader not found: $reader_in (set C1_READER)"
[[ -r $reader_in ]] || err "reader is not readable: $reader_in"
reader=$(realpath -- "$reader_in")
reader_sha=$(sha256sum "$reader" | cut -d' ' -f1)
reader_help=$(python3 -I -- "$reader" --help 2>&1) || err "reader --help failed: $reader"
for flag in --layout --files --nonregular; do
  grep -q -- "$flag" <<<"$reader_help" || err "reader does not advertise $flag: $reader"
done

read -r magic offset <<<"$(magic_scan)"
case "$magic" in
  sqsh) ;;
  hsqs) err "oracle arm is for AVM-layout BIG-ENDIAN images (sqsh); $carrier has hsqs at $offset" ;;
  *)    err "no squashfs magic (sqsh|hsqs) in the first 1 MiB of $carrier" ;;
esac

sq_pin
reader_argv=(python3 -I -- "$reader" --layout avm \
             --files "$scratch/oracle.tsv" --nonregular "$scratch/nonregular.tsv" \
             --inspect "$carrier")
reader_argv_json=$(arr_json "${reader_argv[@]}")

start=$(date -u +%FT%TZ); start_ms=$(date +%s%3N)
set +e
( cd "$scratch" && "${reader_argv[@]}" ) > "$scratch/reader.inspect.json" 2> "$scratch/reader.err"
reader_rc=$?
set -e
end=$(date -u +%FT%TZ); end_ms=$(date +%s%3N); dur=$((end_ms - start_ms))
reader_err_head=$(sed -n '1,20p' "$scratch/reader.err" 2>/dev/null | cut -c1-400 || true)

if [[ $reader_rc -ne 0 ]]; then
  jq -n --arg schema kaidoku-r41-c1-run-v1 --arg mode oracle --arg claim R41-C1 \
    --arg carrier "$carrier" --arg carrier_sha "$carrier_sha" --argjson carrier_size "$carrier_size" \
    --arg outdir "$outdir" --arg scratch_root "$work" --arg scratch "$scratch" \
    --arg reader "$reader" --arg reader_sha "$reader_sha" --argjson reader_argv "$reader_argv_json" \
    --arg start "$start" --arg end "$end" --argjson duration_ms "$dur" \
    --argjson reader_exit "$reader_rc" --arg reader_stderr "$reader_err_head" \
    '{schema: $schema, mode: $mode, claim: $claim,
      carrier: {path: $carrier, sha256: $carrier_sha, size_bytes: $carrier_size},
      outdir: $outdir, layout: "avm", run_provenance_segment_ok: true,
      scratch_root: $scratch_root, scratch: $scratch,
      reader: {path: $reader, sha256: $reader_sha, argv: $reader_argv},
      start_utc: $start, end_utc: $end, duration_ms: $duration_ms,
      reader_exit: $reader_exit, reader_stderr_head: $reader_stderr,
      error: "reader_failed"}' > "$outdir/oracle-run.json"
  fail "reader exited $reader_rc (see $outdir/oracle-run.json)"
fi
[[ -f $scratch/oracle.tsv ]] || fail "reader wrote no oracle.tsv"
[[ -f $scratch/nonregular.tsv ]] || fail "reader wrote no nonregular.tsv"

tables=$(python3 -I - "$scratch/oracle.tsv" "$scratch/nonregular.tsv" <<'PY'
import json, re, sys

KINDS = {'dir', 'symlink', 'char-device', 'block-device', 'fifo', 'socket'}
HEX = re.compile(r'[0-9a-f]{64}\Z')


def load(path):
    rows = []
    with open(path, encoding='utf-8', errors='surrogateescape') as fh:
        for n, line in enumerate(fh.read().splitlines(), 1):
            if not line:
                continue
            f = line.split('\t')
            if len(f) != 3:
                raise SystemExit('%s:%d: want 3 tab fields, got %d' % (path, n, len(f)))
            rows.append(f)
    return rows


orows = load(sys.argv[1])
nrows = load(sys.argv[2])
if not orows:
    raise SystemExit('oracle.tsv: no regular-file rows')
keys = []
for rel, sha, size in orows:
    if not rel or rel.startswith('/'):
        raise SystemExit('oracle.tsv: relpath not relative: %r' % rel)
    if not HEX.match(sha):
        raise SystemExit('oracle.tsv: sha256 is not 64 lowercase hex for %r' % rel)
    if not size.isdigit():
        raise SystemExit('oracle.tsv: size is not a non-negative integer for %r' % rel)
    keys.append(rel.encode('utf-8', 'surrogateescape'))
if keys != sorted(keys) or len(set(keys)) != len(keys):
    raise SystemExit('oracle.tsv: relpaths are not bytewise-sorted and unique')
kinds = {}
nkeys = []
for rel, kind, detail in nrows:
    if not rel or rel.startswith('/'):
        raise SystemExit('nonregular.tsv: relpath not relative: %r' % rel)
    if kind not in KINDS:
        raise SystemExit('nonregular.tsv: kind %r not in closed vocabulary' % kind)
    if kind == 'symlink' and not detail:
        raise SystemExit('nonregular.tsv: symlink %r has an empty target' % rel)
    if kind in ('char-device', 'block-device') and not re.match(r'^[0-9]+:[0-9]+$', detail):
        raise SystemExit('nonregular.tsv: device %r detail is not major:minor' % rel)
    if kind in ('dir', 'fifo', 'socket') and detail:
        raise SystemExit('nonregular.tsv: %s %r carries a detail' % (kind, rel))
    kinds[kind] = kinds.get(kind, 0) + 1
    nkeys.append(rel.encode('utf-8', 'surrogateescape'))
if nkeys != sorted(nkeys) or len(set(nkeys)) != len(nkeys):
    raise SystemExit('nonregular.tsv: relpaths are not bytewise-sorted and unique')
if set(keys) & set(nkeys):
    raise SystemExit('nonregular.tsv: path(s) also listed as regular files')
print(json.dumps({'oracle_files': len(orows),
                  'nonregular_entries': len(nrows),
                  'nonregular_by_kind': kinds}))
PY
) || fail "reader tables failed validation (see message above)"

mkdir -p "$scratch/root"
sq_argv=("$sq" -f -no-exit-code -n)
[[ $offset -ne 0 ]] && sq_argv+=(-o "$offset")
sq_argv+=(-d "$scratch/root" "$carrier")
sq_argv_json=$(arr_json "${sq_argv[@]}")
sq_start=$(date -u +%FT%TZ); sq_start_ms=$(date +%s%3N)
set +e
( cd "$scratch" && "${sq_argv[@]}" ) > "$scratch/sasq.log" 2>&1
sq_rc=$?
set -e
sq_end=$(date -u +%FT%TZ); sq_end_ms=$(date +%s%3N); sq_dur=$((sq_end_ms - sq_start_ms))
sq_log_head=$(sed -n '1,20p' "$scratch/sasq.log" 2>/dev/null | cut -c1-400 || true)

cross=$(python3 -I - "$scratch/root" "$scratch/oracle.tsv" "$scratch/oracle-check.tsv" <<'PY'
import hashlib, json, os, sys

root, oracle_tsv, out_tsv = sys.argv[1:4]


def load_oracle(path):
    rows = []
    with open(path, encoding='utf-8', errors='surrogateescape') as fh:
        for line in fh.read().splitlines():
            if line:
                rel, sha, size = line.split('\t')
                rows.append((rel, sha, int(size)))
    return rows


check = []
symlinks = 0
for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
    for name in dirnames + filenames:
        p = os.path.join(dirpath, name)
        rel = os.path.relpath(p, root).replace(os.sep, '/')
        if os.path.islink(p):
            symlinks += 1
            continue
        if not os.path.isfile(p):
            continue
        h = hashlib.sha256()
        with open(p, 'rb') as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b''):
                h.update(chunk)
        check.append((rel, h.hexdigest(), os.path.getsize(p)))
check.sort(key=lambda r: r[0].encode('utf-8', 'surrogateescape'))
with open(out_tsv, 'w', encoding='utf-8', newline='\n') as fh:
    for rel, sha, size in check:
        fh.write('%s\t%s\t%d\n' % (rel, sha, size))

oracle = load_oracle(oracle_tsv)
omap = {r[0]: (r[1], r[2]) for r in oracle}
cmap = {r[0]: (r[1], r[2]) for r in check}
mismatches = []
for rel in sorted(set(omap) | set(cmap)):
    o = omap.get(rel)
    c = cmap.get(rel)
    if o == c:
        continue
    if c is None:
        mismatches.append({'relpath': rel, 'kind': 'missing_from_extract', 'oracle': o})
    elif o is None:
        mismatches.append({'relpath': rel, 'kind': 'extra_in_extract', 'check': c})
    else:
        kind = 'sha256' if o[0] != c[0] else 'size'
        mismatches.append({'relpath': rel, 'kind': kind, 'oracle': o, 'check': c})
print(json.dumps({
    'files_equal': not mismatches,
    'check_files': len(check),
    'check_symlinks': symlinks,
    'mismatch_count': len(mismatches),
    'mismatches': mismatches[:20],
}))
PY
) || fail "cross-check listing failed"

cp -f "$scratch/oracle.tsv" "$outdir/oracle.tsv"
cp -f "$scratch/nonregular.tsv" "$outdir/nonregular.tsv"
cp -f "$scratch/oracle-check.tsv" "$outdir/oracle-check.tsv"

inspect_json=null
if jq -e . "$scratch/reader.inspect.json" >/dev/null 2>&1; then
  inspect_json=$(jq -c . "$scratch/reader.inspect.json")
fi
cross_ok=$(jq -r '.files_equal' <<<"$cross")

jq -n \
  --arg schema kaidoku-r41-c1-run-v1 \
  --arg mode oracle \
  --arg claim R41-C1 \
  --arg carrier "$carrier" --arg carrier_sha "$carrier_sha" --argjson carrier_size "$carrier_size" \
  --arg outdir "$outdir" --arg scratch_root "$work" --arg scratch "$scratch" \
  --arg reader "$reader" --arg reader_sha "$reader_sha" --argjson reader_argv "$reader_argv_json" \
  --arg start "$start" --arg end "$end" --argjson duration_ms "$dur" \
  --argjson reader_exit "$reader_rc" --arg reader_stderr "$reader_err_head" \
  --arg layout avm --arg magic sqsh --argjson offset "$offset" \
  --arg sq "$sq" --arg sq_sha "$sq_sha" --arg sq_ver "$sq_ver" --arg sq_line "$sq_line" \
  --argjson sq_argv "$sq_argv_json" \
  --arg sq_start "$sq_start" --arg sq_end "$sq_end" --argjson sq_duration_ms "$sq_dur" \
  --argjson sq_exit "$sq_rc" --arg sq_log "$sq_log_head" \
  --argjson tables "$tables" --argjson cross "$cross" --argjson inspect "$inspect_json" \
  --arg files_sha "$(sha256sum "$outdir/oracle.tsv" | cut -d' ' -f1)" \
  --argjson files_bytes "$(stat -c%s "$outdir/oracle.tsv")" \
  --arg nr_sha "$(sha256sum "$outdir/nonregular.tsv" | cut -d' ' -f1)" \
  --argjson nr_bytes "$(stat -c%s "$outdir/nonregular.tsv")" \
  --arg chk_sha "$(sha256sum "$outdir/oracle-check.tsv" | cut -d' ' -f1)" \
  --argjson chk_bytes "$(stat -c%s "$outdir/oracle-check.tsv")" \
  '{
    schema: $schema, mode: $mode, claim: $claim,
    carrier: {path: $carrier, sha256: $carrier_sha, size_bytes: $carrier_size},
    outdir: $outdir, layout: $layout, magic: $magic, squashfs_offset: $offset,
    run_provenance_segment_ok: true, scratch_root: $scratch_root, scratch: $scratch,
    reader: {path: $reader, sha256: $reader_sha, argv: $reader_argv,
             start_utc: $start, end_utc: $end, duration_ms: $duration_ms,
             exit: $reader_exit, stderr_head: $reader_stderr},
    extractor: "sasquatch-v4be -f -no-exit-code (NO -be; the AVM argv unblob 26.6.4 picks when the marker holds)",
    sasquatch_v4be: {path: $sq, sha256: $sq_sha, version: $sq_ver, version_line: $sq_line,
                     argv: $sq_argv, start_utc: $sq_start, end_utc: $sq_end,
                     duration_ms: $sq_duration_ms, exit: $sq_exit, log_head: $sq_log},
    tables: $tables,
    outputs: {
      oracle_tsv: {path: "oracle.tsv", sha256: $files_sha, bytes: $files_bytes},
      nonregular_tsv: {path: "nonregular.tsv", sha256: $nr_sha, bytes: $nr_bytes},
      oracle_check_tsv: {path: "oracle-check.tsv", sha256: $chk_sha, bytes: $chk_bytes}
    },
    crosscheck: $cross,
    reader_inspect: $inspect
  }' > "$outdir/oracle-run.json"

[[ $sq_rc -eq 0 ]] || fail "sasquatch-v4be exited $sq_rc (see $outdir/oracle-run.json)"
[[ $cross_ok == true ]] || fail "cross-check disagrees ($(jq -r '.mismatch_count' <<<"$cross") rows; see $outdir/oracle-run.json)"
[[ $inspect_json != null ]] || fail "reader --inspect did not print JSON"
exit 0
