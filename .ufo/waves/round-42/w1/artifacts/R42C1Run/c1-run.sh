#!/usr/bin/env bash
# R42-C1 run harness (kaidoku round 42; ported from tools/round-41/c1-run.sh).
# Two arms, one carrier each; receipts land in corpus/evidence/round-42/c1/<id>/.
#
#   c1-run.sh after  CARRIER OUTDIR|ID [SCRATCH]
#     REA extract-firmware (rea-agents@6.5.0, --format json --full-output
#     --max-depth 1) via `npx -y`, run with cwd = a private scratch dir,
#     REA_UNBLOB_COMMAND (MUST be absolute) defaulting to
#     $HOME/.local/bin/unblob. The child PATH is the inherited PATH and MUST
#     resolve plain `sasquatch` (the R42-C1 extractor; unblob 26.6.4 runs
#     `sasquatch -be|-le` for every v1-v3 chunk). `sasquatch-v4be` is not the
#     arm's extractor and is never required or used here (exit 2 when plain
#     sasquatch does not resolve).
#     The extraction root is `$SCRATCH/extract` (REA refuses an existing root,
#     so it is never pre-created) and is deleted with the scratch on exit.
#       writes OUTDIR/after.json  = the envelope's `data` object (the REA
#                                   evidence object the counter reads), only
#                                   when REA exits 0 with ok=true
#       writes OUTDIR/run.json    = argv, UTC start/end + duration, exit
#                                   codes, plain-sasquatch path/sha256/version,
#                                   rea + unblob versions, carrier pin +
#                                   superblock summary (v1-v3 packed layout and
#                                   v4), envelope digest, receipt digest
#       C1_KEEP_ENVELOPE=1 additionally keeps the raw {ok,data,meta}
#                                   envelope as OUTDIR/after.envelope.json
#
#   c1-run.sh oracle CARRIER OUTDIR|ID [SCRATCH]
#     Independent-oracle arm for a carved SquashFS v1-v3 image (any of the v3
#     vendor magics). It runs ONE tool, `sqfs3-oracle.py` (C1_ORACLE; default
#     <script dir>/sqfs3-oracle.py = tools/round-42/ once installed), which is
#     itself the two-producer oracle: `unsquashfs` 4.7.5 and 7-Zip `7z`, neither
#     of them sasquatch. Contract (validated from --help before the run):
#         python3 -I sqfs3-oracle.py --work DIR --files OUT.tsv
#                       --nonregular OUT.tsv --json OUT.json IMAGE
#     exit 0 ok, 2 unreadable/unsupported image, 3 producer disagreement.
#     The harness re-validates the two tables (3 fields, sha256 hex,
#     bytewise-sorted unique relpaths, closed kind vocabulary, no path overlap)
#     so a malformed table cannot be frozen, and writes:
#       -> OUTDIR/oracle.tsv       relpath TAB sha256 TAB size (regular files)
#       -> OUTDIR/nonregular.tsv   relpath TAB kind TAB detail
#       -> OUTDIR/oracle-inner.json the tool's own oracle-run.json (digested)
#       -> OUTDIR/oracle-run.json  argv, tool pins, exit code, output digests,
#                                  table counts, the tool's cross-check verdict
#                                  and first 20 mismatches, the superblock.
#     C1_ORACLE_CROSSCHECK=1 additionally extracts with plain `sasquatch`
#     (the -be/-le argv unblob 26.6.4 picks) and records whether that extractor
#     agrees with the oracle on every regular relpath/sha256/size. It is
#     advisory evidence only (sasquatch is the extractor under test, never an
#     oracle) and does not change the exit status.
#
# OUTDIR is either a path or a bare id: a value without a `/` that is not an
# existing directory resolves to $C1_EVIDENCE_ROOT/<id>, where
# C1_EVIDENCE_ROOT defaults to <lane>/corpus/evidence/round-42/c1. A path
# outside that root is refused (exit 2) unless C1_ALLOW_FOREIGN_OUTDIR=1; the
# receipt records outdir_under_evidence_root either way.
#
# A non-default SCRATCH must contain a /kaidoku-r42/ path segment: the
# extraction root recorded in the receipt (parameters.output_directory) is what
# proves the run happened this round, so the harness refuses (exit 2) a scratch
# that cannot carry the round-42 provenance marker.
# C1_ALLOW_FOREIGN_SCRATCH=1 downgrades that refusal to a warning and records
# run_provenance_segment_ok:false (development runs only).
#
# Scratch lives under $HYAKU_SCRATCH (default /fast/scratch/hyaku) in
# kaidoku-r42/, or at the explicit SCRATCH argument; either way it is removed
# on exit. TMPDIR points into it so REA staging, unblob.log and the oracle
# tool's producer roots land there.
#
# R41-CL2 fix: the envelope-data summary and the receipt are written to files
# under the scratch and read by jq via --slurpfile ($summary[0], $receipt[0]).
# No receipt-sized value ever travels through argv (Linux MAX_ARG_STRLEN is
# 131072 bytes; a rootfs summary is larger).
#
# Exit: 0 ok, 2 usage/environment error, 3 tool failure.
set -euo pipefail

PROG=$(basename "$0")
SCRIPT_DIR=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd -P)

usage() {
  cat >&2 <<'EOF'
usage: c1-run.sh after  CARRIER OUTDIR|ID [SCRATCH]
       c1-run.sh oracle CARRIER OUTDIR|ID [SCRATCH]
  after   REA extract-firmware (rea-agents@6.5.0 + unblob 26.6.4, plain
          `sasquatch` on PATH) -> OUTDIR/after.json (the `data` object)
          + OUTDIR/run.json
  oracle  independent two-producer oracle (sqfs3-oracle.py: unsquashfs 4.7.5 +
          7-Zip) -> OUTDIR/oracle.tsv, OUTDIR/nonregular.tsv,
          OUTDIR/oracle-inner.json, OUTDIR/oracle-run.json
  env     HYAKU_SCRATCH (default /fast/scratch/hyaku), REA_UNBLOB_COMMAND
          (absolute; default $HOME/.local/bin/unblob), C1_ORACLE (default
          <script dir>/sqfs3-oracle.py), C1_EVIDENCE_ROOT (default
          <lane>/corpus/evidence/round-42/c1), C1_REA_TIMEOUT (default 900 s),
          C1_KEEP_ENVELOPE=1 (after arm only), C1_ORACLE_CROSSCHECK=1 (oracle
          arm only), C1_ALLOW_FOREIGN_SCRATCH=1, C1_ALLOW_FOREIGN_OUTDIR=1
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

# Lane root: nearest ancestor of the script holding corpus/evidence and plans/.
lane_root() {
  local d=$SCRIPT_DIR
  local _
  for _ in 0 1 2 3 4 5; do
    if [[ -d $d/corpus/evidence && -d $d/plans ]]; then
      printf '%s\n' "$d"
      return 0
    fi
    d=$(dirname -- "$d")
  done
  printf '%s\n' "$SCRIPT_DIR/../.."
}
lane=$(realpath -m -- "$(lane_root)")
evidence_root=$(realpath -m -- "${C1_EVIDENCE_ROOT:-$lane/corpus/evidence/round-42/c1}")

# OUTDIR: a bare id resolves under the round-42 evidence root.
if [[ $outdir_in != */* && ! -d $outdir_in ]]; then
  outdir_target=$evidence_root/$outdir_in
else
  outdir_target=$outdir_in
fi
mkdir -p "$outdir_target" || err "cannot create OUTDIR: $outdir_target"
outdir=$(realpath -- "$outdir_target")
outdir_id=$(basename -- "$outdir")
outdir_under_evidence_root=false
case "$outdir/" in
  "$evidence_root"/*) outdir_under_evidence_root=true ;;
esac
if [[ $outdir_under_evidence_root != true ]]; then
  if [[ ${C1_ALLOW_FOREIGN_OUTDIR:-0} == 1 ]]; then
    echo "$PROG: warning: OUTDIR $outdir is outside the round-42 evidence root"\
         "$evidence_root (development run); receipts frozen from it will not sit"\
         "under corpus/evidence/round-42/c1/<id>" >&2
  else
    err "OUTDIR $outdir is outside the round-42 evidence root $evidence_root;"\
        "pass a bare id (e.g. V1), an in-root path, or C1_ALLOW_FOREIGN_OUTDIR=1"\
        "for a development run"
  fi
fi

scratch_root=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kaidoku-r42
mkdir -p "$scratch_root" || err "cannot create scratch root: $scratch_root"
prov_segment_ok=true
if [[ -n $scratch_arg ]]; then
  scratch=$(realpath -m -- "$scratch_arg")
  case "$scratch/" in
    */kaidoku-r42/*) ;;
    *)
      if [[ ${C1_ALLOW_FOREIGN_SCRATCH:-0} == 1 ]]; then
        prov_segment_ok=false
        echo "$PROG: warning: SCRATCH $scratch lacks a /kaidoku-r42/ segment; the R42-C1"\
             "run-provenance clause (receipt parameters.output_directory) will not match" >&2
      else
        err "SCRATCH $scratch lacks a /kaidoku-r42/ segment: a receipt written from it fails"\
            "the R42-C1 run-provenance clause (parameters.output_directory is hashed into the"\
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

# Plain `sasquatch` pin (R42-C1 extractor): path, sha256, version line, version.
sq_pin() {
  sq=$(command -v sasquatch || true)
  [[ -n $sq ]] || err "plain sasquatch is not resolvable on PATH (the R42-C1 extractor;"\
                      "sasquatch-v4be is NOT a substitute)"
  sq=$(realpath -- "$sq")
  sq_sha=$(sha256sum "$sq" | cut -d' ' -f1)
  sq_line=$("$sq" -version 2>&1 | sed -n 1p || true)
  sq_ver=$(printf '%s' "$sq_line" | sed -nE 's/.*[Vv]ersion ([0-9][0-9A-Za-z.]*).*/\1/p')
  [[ -n $sq_ver ]] || sq_ver=unknown
}

# SquashFS magic families (unblob 26.6.4 squashfs_v1..v4 handlers).
#   standard    hsqs / sqsh      little / big
#   ddwrt v3    hsqt / tqsh      little / big
#   broadcom v3 shsq / qshs      little / big
#   nonstandard v3 zlqs / sqlz   little / big
# magic_scan prints: "<magic> <offset> <byte_order> <family> <n_hits>" for the
# earliest magic in the first 1 MiB; every hit is also recorded by the caller's
# superblock summary (see superblock_summary).
magic_scan() {
  python3 -I - "$carrier" <<'PY'
import json, sys

TOKENS = (
    (b'sqsh', 'big', 'standard'),
    (b'hsqs', 'little', 'standard'),
    (b'tqsh', 'big', 'ddwrt'),
    (b'hsqt', 'little', 'ddwrt'),
    (b'qshs', 'big', 'broadcom'),
    (b'shsq', 'little', 'broadcom'),
    (b'sqlz', 'big', 'nonstandard'),
    (b'zlqs', 'little', 'nonstandard'),
)
raw = open(sys.argv[1], 'rb').read(1 << 20)
hits = []
for tok, order, family in TOKENS:
    start = 0
    while True:
        i = raw.find(tok, start)
        if i < 0:
            break
        hits.append({'magic': tok.decode('ascii'), 'offset': i,
                     'byte_order': order, 'family': family})
        start = i + 1
hits.sort(key=lambda h: h['offset'])
first = hits[0] if hits else {'magic': 'none', 'offset': -1,
                              'byte_order': '', 'family': ''}
print(json.dumps({'first': first, 'hits': hits}))
PY
}

# Superblock summary. v1-v3 packed layout (unblob SquashFSv3Handler
# C_DEFINITIONS) and v4; endianness from the magic, version from s_major.
superblock_summary() {
  python3 -I - "$carrier" "$1" <<'PY'
import json, struct, sys

carrier, scan_json = sys.argv[1], json.loads(sys.argv[2])
first = scan_json['first']
magic = first['magic']
if magic == 'none':
    print('null')
    raise SystemExit(0)
e = '>' if first['byte_order'] == 'big' else '<'
off = first['offset']
raw = open(carrier, 'rb').read(off + 128)
if len(raw) < off + 4:
    print('null')
    raise SystemExit(0)

def u8(o):
    return raw[off + o]

def u16(o):
    return struct.unpack_from(e + 'H', raw, off + o)[0]

def u32(o):
    return struct.unpack_from(e + 'I', raw, off + o)[0]

def u64(o):
    return struct.unpack_from(e + 'Q', raw, off + o)[0]

if len(raw) < off + 32:
    print('null')
    raise SystemExit(0)
major = u16(28)
minor = u16(30)
# A truncated carrier must not crash the arm: emit null instead of a traceback.
need = 48 if major == 4 else (52 if major in (1, 2) else 120)
if len(raw) < off + need:
    print('null')
    raise SystemExit(0)
out = {
    'magic': magic,
    'magic_offset': off,
    'byte_order': first['byte_order'],
    'family': first['family'],
    'magic_hits': len(scan_json['hits']),
    's_major': major,
    's_minor': minor,
    'version': '%d.%d' % (major, minor),
}
if major == 4:
    # squashfs4_super_block (all fields endian-following the magic).
    out.update({
        'layout': 'v4',
        'inodes': u32(4),
        'mkfs_time': u32(8),
        'block_size': u32(12),
        'fragments': u32(16),
        'compression_id': u16(20),
        'block_log': u16(22),
        'flags': u16(24),
        'no_ids': u16(26),
        'root_inode': u64(32),
        'bytes_used': u64(40),
    })
    out['compression'] = {1: 'gzip', 2: 'lzma', 3: 'lzo', 4: 'xz',
                          5: 'lz4', 6: 'zstd'}.get(out['compression_id'])
elif major == 3:
    # squashfs3_super_block, packed (unblob 26.6.4 C_DEFINITIONS); vendor
    # variants share the layout and change only magic+endianness.
    out.update({
        'layout': 'v3',
        'inodes': u32(4),
        'mkfs_time': u32(39),
        'root_inode': u64(43),
        'block_size': u32(51),
        'fragments': u32(55),
        'bytes_used': u64(63),
        'block_log': u16(34),
        'flags': u8(36),
        'no_uids': u8(37),
        'no_guids': u8(38),
        # v3 has no compression id: gzip/LZMA is implied by the payload, the
        # superblock carries no compressor field.
        # v3 superblocks carry no compressor id; the actual method is a
        # property of the payload (the oracle records 7z's Method).
        'compression': None,
        'compression_note': 'v3 superblock has no compressor field',
        'compression_id': None,
    })
else:
    # v1/v2: same packed prefix as v3 up to root_inode; the tail (block_size,
    # bytes_used, tables) is not at the v3 offsets, so it is not reported.
    # v1/v2 are out of R42-C1 scope (v3 family only).
    out.update({
        'layout': 'v1' if major == 1 else 'v2',
        'inodes': u32(4),
        'mkfs_time': u32(39),
        'root_inode': u64(43),
        'block_size': None,
        'fragments': None,
        'bytes_used': None,
        'block_log': u16(34),
        'flags': u8(36),
        'no_uids': u8(37),
        'no_guids': u8(38),
        'compression': None,
        'compression_id': None,
        'layout_note': 'v1/v2 tail fields are not at the v3 offsets; out of R42-C1 scope',
    })
print(json.dumps(out))
PY
}

# Compressor of the payload, for the receipt's superblock summary. A v1-v3
# superblock carries no compressor field: the method is a property of the block
# stream. 7z names it ("Method = ZLIB") on a 4-byte-magic-normalized copy (7z
# does not accept the vendor magic words), the same normalization the oracle
# tool uses. Empty output = not measured (7z absent or unreadable); the field
# stays null and compression_note says so.
compression_probe() {
  command -v 7z >/dev/null 2>&1 || return 1
  local dest=$scratch/compression-probe.sqfs
  python3 -I - "$carrier" "$offset" "$byte_order" "$dest" <<'PY'
import shutil, sys

src, off, order, dest = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
shutil.copyfile(src, dest)
with open(dest, 'r+b') as fh:
    fh.seek(off)
    fh.write(b'sqsh' if order == 'big' else b'hsqs')
PY
  [[ -f $dest ]] || return 1
  7z l -slt "$dest" 2>/dev/null | sed -nE 's/^Method = (.*)$/\1/p' | sed -n 1p
}

# ---------------------------------------------------------------- oracle arm
if [[ $mode == oracle ]]; then
  oracle_in=${C1_ORACLE:-$SCRIPT_DIR/sqfs3-oracle.py}
  [[ -f $oracle_in ]] || err "oracle tool not found: $oracle_in (set C1_ORACLE to the"\
                             "installed tools/round-42/sqfs3-oracle.py)"
  [[ -r $oracle_in ]] || err "oracle tool is not readable: $oracle_in"
  oracle=$(realpath -- "$oracle_in")
  oracle_sha=$(sha256sum "$oracle" | cut -d' ' -f1)
  py_bin=python3
  oracle_help=$("$py_bin" -I -- "$oracle" --help 2>&1) \
    || err "oracle --help failed: $oracle"
  for flag in --work --files --nonregular --json; do
    grep -q -- "$flag" <<<"$oracle_help" \
      || err "oracle does not advertise $flag in --help: $oracle"
  done

  # A failed run must never leave a previous run's tables in the evidence dir:
  # digest them as previous_outputs, then remove them before this run starts.
  previous_outputs=$( { for f in oracle.tsv nonregular.tsv oracle-inner.json; do
      if [[ -f $outdir/$f ]]; then
        printf '%s %s\n' "$(sha256sum "$outdir/$f" | cut -d' ' -f1)" "$f"
      fi
    done; } | jq -R -s 'split("\n") | map(select(length > 0) | split(" ")) | map({path: .[1], sha256: .[0]})')
  rm -f -- "$outdir/oracle.tsv" "$outdir/nonregular.tsv" "$outdir/oracle-inner.json"

  scan=$(magic_scan)
  read -r magic offset byte_order family <<<"$(jq -r '.first | "\(.magic) \(.offset) \(.byte_order) \(.family)"' <<<"$scan")"
  [[ $magic != none ]] || err "no SquashFS magic (hsqs|sqsh|hsqt|tqsh|shsq|qshs|zlqs|sqlz)"\
                              "in the first 1 MiB of $carrier"
  superblock=$(superblock_summary "$scan")
  if [[ $superblock != null && ${C1_COMPRESSION_PROBE:-1} == 1 ]] \
     && jq -e '.layout != "v4"' <<<"$superblock" >/dev/null 2>&1; then
    if comp=$(compression_probe) && [[ -n $comp ]]; then
      superblock=$(jq -c --arg c "$comp" \
        '.compression = $c | .compression_source = "7z l -slt on a 4-byte-magic-normalized copy"' \
        <<<"$superblock")
    fi
  fi

  # Tool pins for the receipt (versions only; the oracle tool owns its argv).
  unsquashfs_path=$(command -v unsquashfs || true)
  unsquashfs_ver=''
  [[ -n $unsquashfs_path ]] && unsquashfs_ver=$(unsquashfs -version 2>&1 | sed -n 1p || true)
  sevenz_path=$(command -v 7z || true)
  sevenz_ver=''
  [[ -n $sevenz_path ]] && sevenz_ver=$(7z 2>&1 | sed -n 2p || true)

  mkdir -p "$scratch/oracle-work"
  oracle_argv=("$py_bin" -I -- "$oracle" \
               --work "$scratch/oracle-work" \
               --files "$scratch/oracle.tsv" \
               --nonregular "$scratch/nonregular.tsv" \
               --json "$scratch/oracle-inner.json")
  if [[ $offset -ne 0 ]]; then
    grep -q -- '--offset' <<<"$oracle_help" \
      || err "squashfs magic sits at offset $offset but the oracle tool does not"\
             "advertise --offset: carve the chunk at offset 0 first"
    oracle_argv+=(--offset "$offset")
  fi
  oracle_argv+=("$carrier")
  oracle_argv_json=$(arr_json "${oracle_argv[@]}")

  start=$(date -u +%FT%TZ); start_ms=$(date +%s%3N)
  set +e
  ( cd "$scratch" && timeout "${C1_ORACLE_TIMEOUT:-900}" "${oracle_argv[@]}" ) \
    > "$scratch/oracle.stdout" 2> "$scratch/oracle.err"
  oracle_rc=$?
  set -e
  end=$(date -u +%FT%TZ); end_ms=$(date +%s%3N); dur=$((end_ms - start_ms))
  oracle_err_head=$(sed -n '1,20p' "$scratch/oracle.err" 2>/dev/null | cut -c1-400 || true)

  inner_sha=''
  inner_bytes=0
  cross_ok=null
  cross_mismatch_count=null
  printf 'null\n' > "$scratch/inner.json"
  if [[ -f $scratch/oracle-inner.json ]] && jq -e . "$scratch/oracle-inner.json" >/dev/null 2>&1; then
    jq -c . "$scratch/oracle-inner.json" > "$scratch/inner.json"
    inner_sha=$(sha256sum "$scratch/oracle-inner.json" | cut -d' ' -f1)
    inner_bytes=$(stat -c%s "$scratch/oracle-inner.json")
    cross_ok=$(jq -c 'if (.cross_check | type) == "object" then (.cross_check.verdict == "agree")
                      elif (.crosscheck | type) == "object" then (.crosscheck.files_equal // null)
                      elif (.producers_equal | type) == "boolean" then .producers_equal
                      else null end' "$scratch/oracle-inner.json")
    cross_mismatch_count=$(jq -c 'if (.cross_check.mismatch_count | type) == "number" then .cross_check.mismatch_count
                                  elif (.crosscheck.mismatches | type) == "array" then (.crosscheck.mismatches | length)
                                  else null end' "$scratch/oracle-inner.json")
  fi

  table_error=null
  tables=null
  tables_copied=false
  if [[ -f $scratch/oracle.tsv && -f $scratch/nonregular.tsv ]]; then
    if tables=$(python3 -I - "$scratch/oracle.tsv" "$scratch/nonregular.tsv" <<'PY'
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
    ); then
      if [[ $oracle_rc -eq 0 ]]; then
        cp -f "$scratch/oracle.tsv" "$outdir/oracle.tsv"
        cp -f "$scratch/nonregular.tsv" "$outdir/nonregular.tsv"
        tables_copied=true
      fi
    else
      tables=null
      table_error="oracle tables failed validation (see message above)"
    fi
  elif [[ $oracle_rc -eq 0 ]]; then
    table_error="oracle wrote no oracle.tsv/nonregular.tsv"
  fi
  if [[ -n $inner_sha ]]; then
    cp -f "$scratch/oracle-inner.json" "$outdir/oracle-inner.json"
  fi

  # Advisory: does the extractor under test (plain sasquatch) agree with the
  # oracle? Never part of the exit status (sasquatch is not an oracle).
  crosscheck=null
  if [[ ${C1_ORACLE_CROSSCHECK:-0} == 1 && $oracle_rc -eq 0 && $tables_copied == true ]]; then
    sq_pin
    sq_argv=("$sq" "-$( [[ $byte_order == big ]] && printf be || printf le )" \
             -f -no-exit-code -n)
    [[ $offset -ne 0 ]] && sq_argv+=(-o "$offset")
    mkdir -p "$scratch/sasq-root"
    sq_argv+=(-d "$scratch/sasq-root" "$carrier")
    set +e
    ( cd "$scratch" && "${sq_argv[@]}" ) > "$scratch/sasq.log" 2>&1
    sq_rc=$?
    set -e
    crosscheck=$(python3 -I - "$scratch/sasq-root" "$scratch/oracle.tsv" "$sq_rc" <<'PY'
import hashlib, json, os, sys

root, oracle_tsv, sq_rc = sys.argv[1], sys.argv[2], int(sys.argv[3])


def load_oracle(path):
    rows = []
    with open(path, encoding='utf-8', errors='surrogateescape') as fh:
        for line in fh.read().splitlines():
            if line:
                rel, sha, size = line.split('\t')
                rows.append((rel, sha, int(size)))
    return rows


check = []
for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
    for name in dirnames + filenames:
        p = os.path.join(dirpath, name)
        rel = os.path.relpath(p, root).replace(os.sep, '/')
        if os.path.islink(p) or not os.path.isfile(p):
            continue
        h = hashlib.sha256()
        with open(p, 'rb') as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b''):
                h.update(chunk)
        check.append((rel, h.hexdigest(), os.path.getsize(p)))
check.sort(key=lambda r: r[0].encode('utf-8', 'surrogateescape'))

omap = {r[0]: (r[1], r[2]) for r in load_oracle(oracle_tsv)}
cmap = {r[0]: (r[1], r[2]) for r in check}
mismatches = []
for rel in sorted(set(omap) | set(cmap)):
    o, c = omap.get(rel), cmap.get(rel)
    if o == c:
        continue
    if c is None:
        mismatches.append({'relpath': rel, 'kind': 'missing_from_extract', 'oracle': o})
    elif o is None:
        mismatches.append({'relpath': rel, 'kind': 'extra_in_extract', 'check': c})
    else:
        mismatches.append({'relpath': rel,
                           'kind': 'sha256' if o[0] != c[0] else 'size',
                           'oracle': o, 'check': c})
print(json.dumps({
    'extractor': 'sasquatch (advisory only; never an oracle)',
    'extract_exit': sq_rc,
    'files_equal': not mismatches,
    'check_files': len(check),
    'mismatch_count': len(mismatches),
    'mismatches': mismatches[:20],
}))
PY
    ) || crosscheck=null
  fi

  jq -n \
    --arg schema kaidoku-r42-c1-run-v1 \
    --arg mode oracle \
    --arg claim R42-C1 \
    --arg carrier "$carrier" --arg carrier_sha "$carrier_sha" --argjson carrier_size "$carrier_size" \
    --arg outdir "$outdir" --arg outdir_id "$outdir_id" \
    --argjson outdir_under_evidence_root "$outdir_under_evidence_root" \
    --arg evidence_root "$evidence_root" \
    --argjson prov_segment "$prov_segment_ok" --arg scratch_root "$scratch_root" \
    --arg magic "$magic" --arg byte_order "$byte_order" --arg family "$family" \
    --argjson offset "$offset" --argjson superblock "$superblock" \
    --arg oracle "$oracle" --arg oracle_sha "$oracle_sha" --argjson oracle_argv "$oracle_argv_json" \
    --arg start "$start" --arg end "$end" --argjson duration_ms "$dur" \
    --argjson oracle_exit "$oracle_rc" --arg oracle_stderr "$oracle_err_head" \
    --arg unsquashfs_path "$unsquashfs_path" --arg unsquashfs_version "$unsquashfs_ver" \
    --arg sevenz_path "$sevenz_path" --arg sevenz_version "$sevenz_ver" \
    --argjson tables "$tables" --arg table_error "$table_error" \
    --argjson previous_outputs "$previous_outputs" \
    --argjson tables_copied "$tables_copied" \
    --argjson cross_ok "$cross_ok" --argjson cross_mismatch_count "$cross_mismatch_count" \
    --argjson crosscheck "$crosscheck" \
    --arg inner_sha "$inner_sha" --argjson inner_bytes "$inner_bytes" \
    --slurpfile inner "$scratch/inner.json" \
    --arg files_sha "$( [[ -f $outdir/oracle.tsv ]] && sha256sum "$outdir/oracle.tsv" | cut -d' ' -f1 || true)" \
    --argjson files_bytes "$( [[ -f $outdir/oracle.tsv ]] && stat -c%s "$outdir/oracle.tsv" || echo 0)" \
    --arg nr_sha "$( [[ -f $outdir/nonregular.tsv ]] && sha256sum "$outdir/nonregular.tsv" | cut -d' ' -f1 || true)" \
    --argjson nr_bytes "$( [[ -f $outdir/nonregular.tsv ]] && stat -c%s "$outdir/nonregular.tsv" || echo 0)" \
    '{
      schema: $schema, mode: $mode, claim: $claim,
      carrier: {path: $carrier, sha256: $carrier_sha, size_bytes: $carrier_size,
                magic: $magic, magic_offset: $offset, byte_order: $byte_order,
                magic_family: $family, superblock: $superblock},
      outdir: $outdir, outdir_id: $outdir_id,
      outdir_under_evidence_root: $outdir_under_evidence_root,
      evidence_root: $evidence_root,
      run_provenance_segment_ok: $prov_segment, scratch_root: $scratch_root,
      oracle: {path: $oracle, sha256: $oracle_sha, argv: $oracle_argv,
               start_utc: $start, end_utc: $end, duration_ms: $duration_ms,
               exit: $oracle_exit, stderr_head: $oracle_stderr},
      producers: {
        unsquashfs: {path: $unsquashfs_path, version_line: $unsquashfs_version},
        seven_zip: {path: $sevenz_path, version_line: $sevenz_version}
      },
      previous_outputs: $previous_outputs,
      tables: $tables, tables_copied: $tables_copied,
      table_error: (if $table_error == "null" then null else $table_error end),
      crosscheck: {producers_equal: $cross_ok, mismatch_count: $cross_mismatch_count,
                   tool_report: $inner[0]},
      extractor_crosscheck: $crosscheck,
      outputs: {
        oracle_tsv: {path: "oracle.tsv", sha256: $files_sha, bytes: $files_bytes},
        nonregular_tsv: {path: "nonregular.tsv", sha256: $nr_sha, bytes: $nr_bytes},
        oracle_inner_json: {path: "oracle-inner.json", sha256: $inner_sha, bytes: $inner_bytes}
      }
    }' > "$outdir/oracle-run.json"

  if [[ $oracle_rc -eq 2 ]]; then
    err "oracle could not read the carrier (exit 2; see $outdir/oracle-run.json):"\
        "a producer rejects the image, so it cannot become a frozen carrier"
  elif [[ $oracle_rc -ne 0 ]]; then
    fail "oracle exited $oracle_rc (see $outdir/oracle-run.json)"
  fi
  if [[ $table_error != null ]]; then
    fail "oracle tables unusable (see $outdir/oracle-run.json)"
  fi
  exit 0
fi

# ----------------------------------------------------------------- after arm
command -v npx >/dev/null || err "npx not found on PATH"
sq_pin

unblob_env=${REA_UNBLOB_COMMAND:-$HOME/.local/bin/unblob}
case "$unblob_env" in
  /*) ;;
  *) err "REA_UNBLOB_COMMAND must be an absolute path (got: $unblob_env)" ;;
esac
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

scan=$(magic_scan)
superblock=$(superblock_summary "$scan")
read -r offset byte_order <<<"$(jq -r '.first | "\(.offset) \(.byte_order)"' <<<"$scan")"
if [[ $superblock != null && ${C1_COMPRESSION_PROBE:-1} == 1 ]] \
   && jq -e '.layout != "v4"' <<<"$superblock" >/dev/null 2>&1; then
  if comp=$(compression_probe) && [[ -n $comp ]]; then
    superblock=$(jq -c --arg c "$comp" \
      '.compression = $c | .compression_source = "7z l -slt on a 4-byte-magic-normalized copy"' \
      <<<"$superblock")
  fi
fi

prev_after_sha=''
[[ -f $outdir/after.json ]] && prev_after_sha=$(sha256sum "$outdir/after.json" | cut -d' ' -f1)

extract_root=$scratch/extract
# Frozen round-42 parameter (carried from round 41, R40C1ReconGaps §6): vendor
# members exceed the 10000 staged-entry budget at the default depth (nested
# filesystem_core.squashfs), so every C1 carrier runs at depth 1.
argv=(npx -y "$rea_pin" extract-firmware --format json --full-output --max-depth 1 "$carrier" "$extract_root")
argv_json=$(arr_json "${argv[@]}")

start=$(date -u +%FT%TZ); start_ms=$(date +%s%3N)
set +e
( cd "$scratch" && timeout "${C1_REA_TIMEOUT:-900}" "${argv[@]}" ) > "$scratch/envelope.json" 2> "$scratch/rea.err"
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

# R41-CL2: the summary and the receipt travel through FILES, never argv.
# Pre-seed both so the final jq always has a slurpfile to read.
printf 'null\n' > "$scratch/summary.json"
printf 'null\n' > "$scratch/receipt.json"
receipt_written=false
summary_error=null
receipt_error=null
depth_ok=null
if [[ $have_data == true ]]; then
  jq -c '.data' "$scratch/envelope.json" > "$scratch/after.json"
  if ! jq -c '
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
      chunks: [((.normalized_result.chunks // [])[]) | {
        provider_id: (.provider_id // null), handler: (.handler // null),
        offset: (.range.offset // null), length: (.range.length // null),
        encrypted: (.encrypted | if . == null then null else . end),
        extraction_failed: (.extraction_failed | if . == null then null else . end)}],
      files: ((.normalized_result.files // []) | length),
      published_bytes: (.normalized_result.published_bytes // null),
      gaps: ((.normalized_result.extraction_gaps // []) | length),
      gaps_detail: [((.normalized_result.extraction_gaps // [])[]) | {kind, relative_path: (.relative_path // null), handler: (.handler // null), dependencies: (.dependencies // [])}],
      diagnostics: [((.normalized_result.diagnostics // [])[]) | {
        typename: (.report.__typename__ // .kind // null),
        severity: (.report.severity // null),
        link: (.report.link // null),
        target: (.report.target // null)}],
      depth_limited_paths: ((.normalized_result.depth_limited_paths // []) | length),
      unpublished_entries: [((.normalized_result.unpublished_entries // [])[]) | {relative_path: (.relative_path // null), kind: (.kind // null), link_target: (.link_target // null)}],
      selection_sha256: (.normalized_result.selection.sha256 // null),
      subject_sha256: (.subject.digest.sha256 // null),
      max_depth: (.parameters.max_depth // null),
      output_directory: (.normalized_result.output_directory // null)
    }' "$scratch/after.json" > "$scratch/summary.json" 2> "$scratch/summary.err"; then
    printf 'null\n' > "$scratch/summary.json"
    summary_error=$(sed -n '1p' "$scratch/summary.err" 2>/dev/null | cut -c1-400)
  fi

  depth_ok=$(jq -c '.parameters.max_depth == 1' "$scratch/after.json")
  if [[ $rc -eq 0 && $envelope_ok == true && $summary_error == null && $depth_ok == true ]]; then
    mv -f "$scratch/after.json" "$outdir/after.json"
    receipt_written=true
    if ! jq -n \
      --arg sha "$(sha256sum "$outdir/after.json" | cut -d' ' -f1)" \
      --argjson bytes "$(stat -c%s "$outdir/after.json")" \
      --slurpfile summary "$scratch/summary.json" \
      '{path: "after.json", sha256: $sha, bytes: $bytes} + $summary[0]' \
      > "$scratch/receipt.json" 2> "$scratch/receipt.err"; then
      printf 'null\n' > "$scratch/receipt.json"
      receipt_written=false
      receipt_error=$(sed -n '1p' "$scratch/receipt.err" 2>/dev/null | cut -c1-400)
    fi
  elif [[ $depth_ok != true ]]; then
    receipt_written=false
    receipt_error="receipt parameters.max_depth is not 1 (the R42-C1 depth binding)"
  fi
fi

if [[ ${C1_KEEP_ENVELOPE:-0} == 1 ]]; then
  cp -f "$scratch/envelope.json" "$outdir/after.envelope.json"
fi

stderr_head=$({ grep -v 'npm warn' "$scratch/rea.err" 2>/dev/null || true; } | sed -n '1,20p' | cut -c1-400)

jq -n \
  --arg schema kaidoku-r42-c1-run-v1 \
  --arg mode after \
  --arg claim R42-C1 \
  --arg carrier "$carrier" --arg carrier_sha "$carrier_sha" --argjson carrier_size "$carrier_size" \
  --arg outdir "$outdir" --arg outdir_id "$outdir_id" \
  --argjson outdir_under_evidence_root "$outdir_under_evidence_root" \
  --arg evidence_root "$evidence_root" \
  --argjson prov_segment "$prov_segment_ok" \
  --arg extract_root "$extract_root" --arg cwd "$scratch" \
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
  --arg summary_error "$summary_error" --arg receipt_error "$receipt_error" \
  --argjson depth_ok "$depth_ok" \
  --slurpfile receipt "$scratch/receipt.json" \
  --slurpfile summary "$scratch/summary.json" \
  --arg prev_after "$prev_after_sha" \
  --arg stderr_head "$stderr_head" \
  '{
    schema: $schema, mode: $mode, claim: $claim,
    carrier: {path: $carrier, sha256: $carrier_sha, size_bytes: $carrier_size,
              superblock: $superblock},
    outdir: $outdir, outdir_id: $outdir_id,
    outdir_under_evidence_root: $outdir_under_evidence_root,
    evidence_root: $evidence_root,
    argv: $argv, argv_shell: $argv_shell, cwd: $cwd,
    run_provenance_segment_ok: $prov_segment,
    extraction_root: $extract_root,
    start_utc: $start, end_utc: $end, duration_ms: $duration_ms, exit: $exit,
    rea: {pin: $rea_pin, version: $rea_ver, package_root: $rea_root},
    unblob: {env_value: $unblob_env, command_env: $unblob, sha256: $unblob_sha, version: $unblob_ver},
    sasquatch: {path: $sq, sha256: $sq_sha, version: $sq_ver, version_line: $sq_line,
                role: "extractor under test (plain sasquatch; v3 argv -be|-le)"},
    child_path: $path,
    envelope: {parseable: $env_parseable, ok: $env_ok, sha256: $env_sha, bytes: $env_bytes,
               error: $env_error},
    data_extracted: $have_data,
    receipt_written: $receipt_written,
    depth_ok: $depth_ok,
    summary_error: (if $summary_error == "null" then null else $summary_error end),
    receipt_error: (if $receipt_error == "null" then null else $receipt_error end),
    receipt: $receipt[0],
    envelope_data_summary: $summary[0],
    previous_after_json_sha256: (if $prev_after == "" then null else $prev_after end),
    stderr_head: $stderr_head
  }' > "$outdir/run.json"

if [[ $receipt_written != true ]]; then
  echo "$PROG: no receipt written (rea exit $rc, envelope ok=$envelope_ok, data=$have_data); see $outdir/run.json" >&2
  exit 3
fi
exit 0
