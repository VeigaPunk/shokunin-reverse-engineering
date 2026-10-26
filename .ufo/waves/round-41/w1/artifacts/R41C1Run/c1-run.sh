#!/usr/bin/env bash
# R41-C1 run harness (kaidoku round 41; ported from tools/round-40/c1-run.sh).
# Two arms, one carrier each; output goes to corpus/evidence/round-41/c1/<id>/.
#
#   c1-run.sh after  CARRIER OUTDIR [SCRATCH]
#     REA extract-firmware (rea-agents@6.5.0, --format json --full-output) via
#     `npx -y`, run with cwd = a private scratch dir, REA_UNBLOB_COMMAND
#     defaulting to ~/.local/bin/unblob. The child PATH is the inherited PATH
#     and MUST resolve sasquatch-v4be (the arm's precondition; exit 2 when it
#     does not). The extraction root is `$SCRATCH/extract` (REA refuses an
#     existing root, so it is never pre-created) and is deleted with the
#     scratch on exit.
#       writes OUTDIR/after.json  = the envelope's `data` object (the REA
#                                   evidence object the counter reads), only
#                                   when REA exits 0 with ok=true
#       writes OUTDIR/run.json    = argv, UTC start/end + duration, exit
#                                   codes, sasquatch-v4be path/sha256/version,
#                                   rea + unblob versions, carrier pin +
#                                   big-endian superblock marker summary,
#                                   envelope digest, receipt digest
#       C1_KEEP_ENVELOPE=1 additionally keeps the raw {ok,data,meta}
#                                   envelope as OUTDIR/after.envelope.json
#
#   c1-run.sh oracle CARRIER OUTDIR [SCRATCH]
#     AVM-layout oracle arm. Two independent producers, one frozen grammar:
#       1. the independent reader (carried from round 40; stdlib only; --layout avm = BE
#          superblock/inode fields with LITTLE-endian metadata block-length
#          headers). Default path: sqfs-list.py in this script's directory
#          (tools/round-41/sqfs-list.py once frozen); C1_READER overrides.
#          The harness requires the reader's --help to advertise --layout,
#          --files and --nonregular, and runs exactly
#            python3 -I sqfs-list.py --layout avm --files … --nonregular …
#                                     --inspect CARRIER
#          -> OUTDIR/oracle.tsv     relpath TAB sha256 TAB size (regular files)
#          -> OUTDIR/nonregular.tsv relpath TAB kind TAB detail
#                                   kind: dir|symlink|char-device|block-device|
#                                   fifo|socket; detail = link target (symlink),
#                                   decimal major:minor (devices), else empty
#          -> oracle.tsv / nonregular.tsv are validated here (3 fields, sha256
#             hex, bytewise-sorted unique relpaths, closed kind vocabulary, no
#             path overlap) so a malformed table cannot be frozen.
#       2. the cross-check extractor: `sasquatch-v4be` WITHOUT -be (the AVM
#          argv unblob 26.6.4 picks when mkfs_time == bytes_used), forced with
#          -f and -no-exit-code (unprivileged runs cannot create device nodes;
#          that must not fail an otherwise complete extraction), into
#          $SCRATCH/root -> OUTDIR/oracle-check.tsv, same regular-file grammar
#          as oracle.tsv. A cross-check disagreement (any relpath,
#          sha256 or size) is a tool failure (exit 3): the arm is meant to
#          prove two independent producers agree before the carrier is frozen.
#       writes OUTDIR/oracle-run.json = argv, pins, both exit codes, output
#          digests, table counts, cross-check verdict + first 20 mismatches,
#          the reader's --inspect JSON.
#
#   The oracle arm is for genuine AVM-layout BIG-ENDIAN images (`sqsh` magic).
#   An `hsqs` carrier is rejected with exit 2: LE images are out of this arm's
#   scope and `-layout avm` semantics do not apply to them.
#
# A non-default SCRATCH must contain a /kaidoku-r41/ path segment: the
# extraction root recorded in the receipt (parameters.output_directory) is what
# proves the run happened this round, so the harness refuses (exit 2) a
# scratch that cannot carry the round-41 provenance marker.
# C1_ALLOW_FOREIGN_SCRATCH=1 downgrades that refusal to a warning and records
# run_provenance_segment_ok:false (development runs only).
#
# Scratch lives under $HYAKU_SCRATCH (default /fast/scratch/hyaku) in
# kaidoku-r41/, or at the explicit SCRATCH argument; either way it is removed
# on exit. TMPDIR points into it so REA staging and unblob.log land there.
#
# Exit: 0 ok, 2 usage/environment error, 3 tool failure.
set -euo pipefail

PROG=$(basename "$0")
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)

usage() {
  cat >&2 <<'EOF'
usage: c1-run.sh after  CARRIER OUTDIR [SCRATCH]
       c1-run.sh oracle CARRIER OUTDIR [SCRATCH]
  after   REA extract-firmware (rea-agents@6.5.0 + unblob 26.6.4, sasquatch-v4be
          on PATH) -> OUTDIR/after.json (the `data` object) + OUTDIR/run.json
  oracle  AVM-layout independent oracle (round-41 sqfs-list.py --layout avm)
          + sasquatch-v4be -f (NO -be) cross-check -> OUTDIR/oracle.tsv,
          OUTDIR/nonregular.tsv, OUTDIR/oracle-check.tsv, OUTDIR/oracle-run.json
  env     HYAKU_SCRATCH (default /fast/scratch/hyaku), REA_UNBLOB_COMMAND
          (default $HOME/.local/bin/unblob), C1_READER (default
          <script dir>/sqfs-list.py), C1_KEEP_ENVELOPE=1 (after arm only),
          C1_ALLOW_FOREIGN_SCRATCH=1 (permit a SCRATCH without a /kaidoku-r41/
          segment)
EOF
  exit 2
}

err() { echo "$PROG: $*" >&2; exit 2; }
fail() { echo "$PROG: $*" >&2; exit 3; }

mode=${1:-}
carrier_in=${2:-}
outdir_in=${3:-}
scratch_arg=${4:-}
case "$mode" in
  after|oracle) ;;
  *) usage ;;
esac
[[ $# -ge 3 && $# -le 4 && -n $carrier_in && -n $outdir_in ]] || usage
[[ -f $carrier_in ]] || err "carrier is not a regular file: $carrier_in"
[[ -r $carrier_in ]] || err "carrier is not readable: $carrier_in"
command -v python3 >/dev/null || err "python3 not found on PATH"
command -v jq >/dev/null || err "jq not found on PATH"

carrier=$(realpath -- "$carrier_in")
carrier_sha=$(sha256sum "$carrier" | cut -d' ' -f1)
carrier_size=$(stat -c%s "$carrier")

mkdir -p "$outdir_in" || err "cannot create OUTDIR: $outdir_in"
outdir=$(realpath -- "$outdir_in")

scratch_root=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kaidoku-r41
mkdir -p "$scratch_root" || err "cannot create scratch root: $scratch_root"
prov_segment_ok=true
if [[ -n $scratch_arg ]]; then
  scratch=$(realpath -m -- "$scratch_arg")
  case "$scratch/" in
    */kaidoku-r41/*) ;;
    *)
      if [[ ${C1_ALLOW_FOREIGN_SCRATCH:-0} == 1 ]]; then
        prov_segment_ok=false
        echo "$PROG: warning: SCRATCH $scratch lacks a /kaidoku-r41/ segment; the R41-C1"\
             "run-provenance clause (receipt parameters.output_directory) will not match" >&2
      else
        err "SCRATCH $scratch lacks a /kaidoku-r41/ segment: a receipt written from it fails"\
            "the R41-C1 run-provenance clause (parameters.output_directory is hashed into the"\
            "evidence id). Use the default scratch, or set C1_ALLOW_FOREIGN_SCRATCH=1 for a dev run."
      fi ;;
  esac
  mkdir -p "$scratch" || err "cannot create SCRATCH: $scratch"
else
  scratch=$(mktemp -d "$scratch_root/c1-run.XXXXXX")
  scratch=$(realpath -- "$scratch")
fi
trap 'rm -rf -- "$scratch"' EXIT
export TMPDIR=$scratch

# JSON array from shell arguments (empty input -> []).
arr_json() { printf '%s\n' "$@" | jq -R . | jq -s -c .; }

# sasquatch-v4be pin: path, sha256, version line, version.
sq_pin() {
  sq=$(command -v sasquatch-v4be || true)
  [[ -n $sq ]] || err "sasquatch-v4be not resolvable on PATH (the arm requires the BE extractor)"
  sq=$(realpath -- "$sq")
  sq_sha=$(sha256sum "$sq" | cut -d' ' -f1)
  sq_line=$("$sq" -version 2>&1 | sed -n 1p || true)
  sq_ver=$(printf '%s' "$sq_line" | sed -nE 's/.*[Vv]ersion ([0-9][0-9A-Za-z.]*).*/\1/p')
  [[ -n $sq_ver ]] || sq_ver=unknown
}

# First 1 MiB carries either magic; report which and where.
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

# ---------------------------------------------------------------- oracle arm
if [[ $mode == oracle ]]; then
  reader_in=${C1_READER:-$SCRIPT_DIR/sqfs-list.py}
  [[ -f $reader_in ]] || err "round-41 reader not found: $reader_in (set C1_READER)"
  [[ -r $reader_in ]] || err "round-41 reader is not readable: $reader_in"
  reader=$(realpath -- "$reader_in")
  reader_sha=$(sha256sum "$reader" | cut -d' ' -f1)
  py_bin=python3
  reader_help=$("$py_bin" -I -- "$reader" --help 2>&1) \
    || err "reader --help failed: $reader"
  for flag in --layout --files --nonregular; do
    grep -q -- "$flag" <<<"$reader_help" \
      || err "reader does not advertise $flag in --help: $reader"
  done

  read -r magic offset <<<"$(magic_scan)"
  case "$magic" in
    sqsh) ;;
    hsqs) err "oracle arm is for AVM-layout BIG-ENDIAN images (sqsh); $carrier has hsqs at $offset" ;;
    *)    err "no squashfs magic (sqsh|hsqs) in the first 1 MiB of $carrier" ;;
  esac

  sq_pin
  reader_argv=("$py_bin" -I -- "$reader" --layout avm \
               --files "$scratch/oracle.tsv" --nonregular "$scratch/nonregular.tsv" \
               --inspect "$carrier")
  reader_argv_json=$(arr_json "${reader_argv[@]}")

  start=$(date -u +%FT%TZ); start_ms=$(date +%s%3N)
  set +e
  ( cd "$scratch" && "${reader_argv[@]}" ) \
    > "$scratch/reader.inspect.json" 2> "$scratch/reader.err"
  reader_rc=$?
  set -e
  end=$(date -u +%FT%TZ); end_ms=$(date +%s%3N); dur=$((end_ms - start_ms))
  reader_err_head=$(sed -n '1,20p' "$scratch/reader.err" 2>/dev/null | cut -c1-400 || true)

  if [[ $reader_rc -ne 0 ]]; then
    jq -n --arg schema kaidoku-r41-c1-run-v1 --arg mode oracle --arg claim R41-C1 \
      --arg carrier "$carrier" --arg carrier_sha "$carrier_sha" --argjson carrier_size "$carrier_size" \
      --arg outdir "$outdir" --argjson prov_segment "$prov_segment_ok" \
      --arg reader "$reader" --arg reader_sha "$reader_sha" --argjson reader_argv "$reader_argv_json" \
      --arg start "$start" --arg end "$end" --argjson duration_ms "$dur" \
      --argjson reader_exit "$reader_rc" --arg reader_stderr "$reader_err_head" \
      --arg scratch_root "$scratch_root" \
      '{schema: $schema, mode: $mode, claim: $claim,
        carrier: {path: $carrier, sha256: $carrier_sha, size_bytes: $carrier_size},
        outdir: $outdir, layout: "avm", run_provenance_segment_ok: $prov_segment,
        reader: {path: $reader, sha256: $reader_sha, argv: $reader_argv},
        start_utc: $start, end_utc: $end, duration_ms: $duration_ms,
        reader_exit: $reader_exit, reader_stderr_head: $reader_stderr,
        scratch_root: $scratch_root, error: "reader_failed"}' > "$outdir/oracle-run.json"
    fail "reader exited $reader_rc (see $outdir/oracle-run.json)"
  fi
  [[ -f $scratch/oracle.tsv ]] || fail "reader wrote no oracle.tsv"
  [[ -f $scratch/nonregular.tsv ]] || fail "reader wrote no nonregular.tsv"

  # Validate both tables (grammar, closed kind vocabulary, ordering, overlap).
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


def key(f):
    return f[0].encode('utf-8', 'surrogateescape')


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
  # -no-exit-code is what unblob 26.6.4 passes to sasquatch-v4be: an
  # unprivileged extraction cannot create device nodes, and that must not turn
  # a complete regular-file extraction into a tool failure. The file/sha256
  # cross-check below is the real gate.
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

  # Cross-check listing (regular files only; lstat, no symlink following).
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

  # --inspect must be JSON; null is recorded but is a tool failure.
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
    --arg outdir "$outdir" --argjson prov_segment "$prov_segment_ok" \
    --arg scratch_root "$scratch_root" \
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
      run_provenance_segment_ok: $prov_segment, scratch_root: $scratch_root,
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
fi

# ----------------------------------------------------------------- after arm
command -v npx >/dev/null || err "npx not found on PATH"
sq_pin

unblob_env=${REA_UNBLOB_COMMAND:-$HOME/.local/bin/unblob}
[[ -x $unblob_env ]] || err "REA_UNBLOB_COMMAND is missing or not executable: $unblob_env"
unblob=$(realpath -- "$unblob_env")
unblob_sha=$(sha256sum "$unblob" | cut -d' ' -f1)
unblob_ver=$("$unblob" --version 2>&1 | sed -n 1p || true)
[[ -n $unblob_ver ]] || unblob_ver=unknown
export REA_UNBLOB_COMMAND=$unblob

rea_pin=rea-agents@6.5.0
rea_ver=$(timeout 120 npx -y "$rea_pin" --version 2>/dev/null | sed -n '$p' || true)
[[ -n $rea_ver ]] || rea_ver=unknown
rea_root=$(find "${npm_config_cache:-$HOME/.npm}/_npx" -maxdepth 5 \
  -path '*/node_modules/rea-agents/package.json' -print 2>/dev/null \
  | while IFS= read -r p; do
      [[ $(jq -r '.version' "$p" 2>/dev/null) == "${rea_pin#rea-agents@}" ]] && printf '%s\n' "${p%/package.json}"
    done | sed -n '$p' || true)
[[ -n $rea_root ]] || rea_root=unknown

# Big-endian superblock summary (marker = mkfs_time == bytes_used). Read-only.
superblock=$(python3 -I - "$carrier" <<'PY'
import json, struct, sys
raw = open(sys.argv[1], 'rb').read(48)
magic = raw[:4]
if magic == b'sqsh':
    e = '>'
elif magic == b'hsqs':
    e = '<'
else:
    print('null')
    raise SystemExit(0)
if len(raw) < 48:
    print('null')
    raise SystemExit(0)
mkfs, = struct.unpack(e + 'I', raw[8:12])
used, = struct.unpack(e + 'Q', raw[40:48])
print(json.dumps({'magic': magic.decode('ascii'), 'byte_order': 'big' if e == '>' else 'little',
                  'mkfs_time': mkfs, 'bytes_used': used, 'avm_marker': mkfs == used}))
PY
)

prev_after_sha=''
[[ -f $outdir/after.json ]] && prev_after_sha=$(sha256sum "$outdir/after.json" | cut -d' ' -f1)

extract_root=$scratch/extract
# Frozen round-41 parameter (carried from round 40, R40C1ReconGaps §6): vendor AVM members exceed
# the 10000 staged-entry budget at the default depth (nested filesystem_core.squashfs), so every
# C1 carrier runs at depth 1.
argv=(npx -y "$rea_pin" extract-firmware --format json --full-output --max-depth 1 "$carrier" "$extract_root")
argv_json=$(arr_json "${argv[@]}")

start=$(date -u +%FT%TZ); start_ms=$(date +%s%3N)
set +e
( cd "$scratch" && timeout 900 "${argv[@]}" ) > "$scratch/envelope.json" 2> "$scratch/rea.err"
rc=$?
set -e
end=$(date -u +%FT%TZ); end_ms=$(date +%s%3N); dur=$((end_ms - start_ms))

envelope_parseable=false
envelope_ok=false
have_data=false
envelope_error=null
if jq -e 'type == "object"' "$scratch/envelope.json" >/dev/null 2>&1; then
  envelope_parseable=true
  [[ $(jq -r '.ok == true' "$scratch/envelope.json") == true ]] && envelope_ok=true
  if [[ $envelope_ok == true ]] && jq -e '(.data | type) == "object"' "$scratch/envelope.json" >/dev/null 2>&1; then
    have_data=true
  fi
  # A failed envelope's structured reason (REA exit 1) is the diagnosis the
  # recon needs: surface it instead of only the envelope digest.
  envelope_error=$(jq -c 'if .ok == true then null else (.error // null) end' "$scratch/envelope.json")
fi

summary=null
receipt=null
if [[ $have_data == true ]]; then
  jq -c '.data' "$scratch/envelope.json" > "$scratch/after.json"
  summary=$(jq -c '
    {
      evidence_id: .evidence_id,
      operation: .operation,
      provider: {id: (.provider.id // null), version: (.provider.version // null)},
      engine: {name: (.normalized_result.engine.name // null),
               version: (.normalized_result.engine.version // null),
               executable_path: (.normalized_result.engine.executable_path // null),
               executable_sha256: (.normalized_result.engine.executable_sha256 // null)},
      coverage: (.normalized_result.coverage // null),
      handlers: [((.normalized_result.chunks // [])[].handler) | select(. != null)] | unique,
      files: ((.normalized_result.files // []) | length),
      published_bytes: (.normalized_result.published_bytes // null),
      gaps: ((.normalized_result.extraction_gaps // []) | length),
      gaps_detail: [((.normalized_result.extraction_gaps // [])[]) | {kind, relative_path: (.relative_path // null), handler: (.handler // null), dependencies: (.dependencies // [])}],
      unpublished_entries: [((.normalized_result.unpublished_entries // [])[]) | {relative_path: (.relative_path // null), kind: (.kind // null), link_target: (.link_target // null)}],
      selection_sha256: (.normalized_result.selection.sha256 // null),
      subject_sha256: (.subject.digest.sha256 // null),
      output_directory: (.normalized_result.output_directory // null)
    }' "$scratch/after.json")
fi

receipt_written=false
if [[ $rc -eq 0 && $envelope_ok == true && $have_data == true ]]; then
  mv -f "$scratch/after.json" "$outdir/after.json"
  receipt_written=true
  receipt=$(jq -n \
    --arg sha "$(sha256sum "$outdir/after.json" | cut -d' ' -f1)" \
    --argjson bytes "$(stat -c%s "$outdir/after.json")" \
    --argjson summary "$summary" \
    '{path: "after.json", sha256: $sha, bytes: $bytes} + $summary')
fi

if [[ ${C1_KEEP_ENVELOPE:-0} == 1 ]]; then
  cp -f "$scratch/envelope.json" "$outdir/after.envelope.json"
fi

stderr_head=$({ grep -v 'npm warn' "$scratch/rea.err" 2>/dev/null || true; } | sed -n '1,20p' | cut -c1-400)

jq -n \
  --arg schema kaidoku-r41-c1-run-v1 \
  --arg mode after \
  --arg claim R41-C1 \
  --arg carrier "$carrier" --arg carrier_sha "$carrier_sha" --argjson carrier_size "$carrier_size" \
  --arg outdir "$outdir" --arg extract_root "$extract_root" --arg cwd "$scratch" \
  --argjson prov_segment "$prov_segment_ok" \
  --argjson argv "$argv_json" \
  --arg argv_shell "REA_UNBLOB_COMMAND=$unblob ${argv[*]}" \
  --arg start "$start" --arg end "$end" --argjson duration_ms "$dur" --argjson exit "$rc" \
  --arg rea_pin "$rea_pin" --arg rea_ver "$rea_ver" --arg rea_root "$rea_root" \
  --arg unblob_env "$unblob_env" --arg unblob "$unblob" --arg unblob_sha "$unblob_sha" --arg unblob_ver "$unblob_ver" \
  --arg sq "$sq" --arg sq_sha "$sq_sha" --arg sq_ver "$sq_ver" --arg sq_line "$sq_line" \
  --argjson superblock "$superblock" \
  --arg path "$PATH" \
  --argjson env_parseable "$envelope_parseable" --argjson env_ok "$envelope_ok" \
  --argjson env_error "$envelope_error" \
  --arg env_sha "$(sha256sum "$scratch/envelope.json" | cut -d' ' -f1)" \
  --argjson env_bytes "$(stat -c%s "$scratch/envelope.json")" \
  --argjson have_data "$have_data" --argjson receipt_written "$receipt_written" \
  --argjson receipt "$receipt" --argjson summary "$summary" \
  --arg prev_after "$prev_after_sha" \
  --arg stderr_head "$stderr_head" \
  '{
    schema: $schema, mode: $mode, claim: $claim,
    carrier: {path: $carrier, sha256: $carrier_sha, size_bytes: $carrier_size,
              superblock: $superblock},
    outdir: $outdir,
    argv: $argv, argv_shell: $argv_shell, cwd: $cwd,
    run_provenance_segment_ok: $prov_segment,
    extraction_root: $extract_root,
    start_utc: $start, end_utc: $end, duration_ms: $duration_ms, exit: $exit,
    rea: {pin: $rea_pin, version: $rea_ver, package_root: $rea_root},
    unblob: {env_value: $unblob_env, command_env: $unblob, sha256: $unblob_sha, version: $unblob_ver},
    sasquatch_v4be: {path: $sq, sha256: $sq_sha, version: $sq_ver, version_line: $sq_line},
    child_path: $path,
    envelope: {parseable: $env_parseable, ok: $env_ok, sha256: $env_sha, bytes: $env_bytes,
               error: $env_error},
    data_extracted: $have_data,
    receipt_written: $receipt_written,
    receipt: $receipt,
    envelope_data_summary: $summary,
    previous_after_json_sha256: (if $prev_after == "" then null else $prev_after end),
    stderr_head: $stderr_head
  }' > "$outdir/run.json"

if [[ $receipt_written != true ]]; then
  echo "$PROG: no receipt written (rea exit $rc, envelope ok=$envelope_ok, data=$have_data); see $outdir/run.json" >&2
  exit 3
fi
exit 0
