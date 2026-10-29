#!/usr/bin/env bash
# R50-C1 run harness (kaidoku round 50; ported from tools/round-41/c1-run.sh, hardened
# with the round-49 data-run guard and fixed child PATH).
#
# DATA procedure for genuine AVM-marker LITTLE-ENDIAN SquashFS v4 (`hsqs`) members of
# public FRITZ!OS images. The L1 runs it AFTER the freeze, one carrier at a time;
# seats never run an `after` arm into the lane evidence root (a pre-freeze receipt is
# not a receipt: the counter's first-add-after-freeze clause could never hold).
#
#   c1-run.sh after  --id ID --carrier FILE --data-run [--outdir DIR] ...
#     REA 6.5.0 `extract-firmware` via `npx -y rea-agents@6.5.0`, argv
#       npx -y rea-agents@6.5.0 extract-firmware --format json --full-output \
#           --max-depth 1 CARRIER $SCRATCH/extract
#     (the exact round-41 flags; depth 1 because vendor members exceed the 10000
#     staged-entry budget at the default depth). cwd = a private scratch dir,
#     TMPDIR = that dir, REA_UNBLOB_COMMAND = ~/.local/bin/unblob (26.6.4).
#     Precondition (exit 2): `sasquatch` (NOT sasquatch-v4be) resolves on the child
#     PATH; the LE handler `squashfs_v4_le` needs no -be binary. The child PATH is
#     fixed (see FIXED_PATH) so the run and the counter's rerun resolve the same
#     binaries; C1_CHILD_PATH overrides it and is recorded.
#       writes OUTDIR/after.json  = the envelope's `data` object (what the counter
#                                   reads), only when REA exits 0 with ok=true
#       writes OUTDIR/run.json    = argv, UTC start/end, duration, exit codes, tool
#                                   pins (sasquatch/unblob/rea), carrier pin +
#                                   LE superblock summary, envelope digest, receipt
#                                   digest, the handler list, subject-digest and
#                                   output-directory-prefix verdicts
#       C1_KEEP_ENVELOPE=1 additionally keeps the raw {ok,data,meta} envelope.
#     The extraction tree is never committed and is deleted with the scratch.
#
#   c1-run.sh oracle --id ID --carrier FILE [--outdir DIR] ...
#     LE-AVM oracle arm; THREE independent producers, one frozen grammar, any
#     disagreement is exit 3:
#       1. the pure-Python reader tools/round-41/sqfs-list.py
#            --layout auto  (primary: `auto` and `le` both parse an LE xz member;
#                            `avm` is the BIG-endian-AVM layout and is NOT used)
#            --layout le    (run again; its tables must be byte-identical to auto)
#          -> OUTDIR/oracle.tsv      relpath TAB sha256 TAB size (regular files)
#          -> OUTDIR/nonregular.tsv  relpath TAB kind TAB detail
#             kind: dir|symlink|char-device|block-device|fifo|socket
#       2. /usr/bin/unsquashfs 4.7.5 -no-xattrs -f -no-exit-code (the plan's named
#          independent oracle): extraction tree walked + hashed, plus the
#          `-lln` listing for device/fifo/socket entries
#          -> OUTDIR/oracle-unsquashfs.tsv  (regular files, same grammar)
#       3. the cross-check extractor `sasquatch -le -f -no-exit-code` (the argv
#          unblob 26.6.4 uses for an LE image)
#          -> OUTDIR/oracle-check.tsv       (regular files, same grammar)
#     Compared: regular files across all three (relpath, sha256, size); dir/symlink
#     rows of nonregular.tsv against both extraction trees; device/fifo/socket rows
#     against the `-lln` listing (an unprivileged extraction cannot create them).
#       writes OUTDIR/oracle-run.json = argv, pins, exit codes, output digests,
#          table counts, comparison verdicts + first 20 mismatches, the reader's
#          --inspect JSON.
#     Precondition (exit 2): the carrier superblock is `hsqs` at offset 0, v4.0,
#     compression 4 (xz), mkfs_time == bytes_used (the AVM marker), and the reader's
#     --inspect agrees (little endian, xz, avm_marker true). C1_ALLOW_NONAVM=1
#     waives it (control carriers only) and records the waiver.
#
# Scratch (both arms): `$HYAKU_SCRATCH/kaidoku-r50` (default /fast/scratch/hyaku) or the
# --scratch BASE; BASE MUST carry a /kaidoku-r50/ path segment (the receipt's
# parameters.output_directory is hashed into the evidence id and the counter requires it
# to start with /fast/scratch/hyaku/kaidoku-r50/). A private `c1-run.XXXXXX` directory is
# made INSIDE the base and only that directory is removed on exit (--keep-scratch keeps
# it). C1_ALLOW_FOREIGN_SCRATCH=1 downgrades the segment refusal to a warning and
# records run_provenance_segment_ok:false (development only).
#
# Data-run guard: `after` always requires --data-run (or KAIDOKU_C1_DATA_RUN=1); `oracle`
# requires it only when OUTDIR lies under .../corpus/evidence/round-50/. --dry-run
# prints the resolved plan and writes nothing. An existing after.json (after arm) or
# oracle.tsv (oracle arm) in OUTDIR is an occupied slot: exit 2 unless --force.
#
# Pins (exit 2 on drift unless C1_ALLOW_PIN_DRIFT=1): unblob 26.6.4, sasquatch 4.5.1,
# unsquashfs 4.7.5, rea-agents 6.5.0.
#
# Exit: 0 ok, 2 usage/environment/precondition error (could not evaluate), 3 tool
# failure or producer disagreement. (1 is unused: nothing here "does not meet" a claim;
# the counter judges.)
set -euo pipefail

PROG=$(basename "$0")
SCRIPT_DIR=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd -P)

REA_PIN=rea-agents@6.5.0
UNBLOB_PIN=26.6.4
SASQUATCH_PIN=4.5.1
UNSQUASHFS_PIN=4.7.5
ROUND_SEGMENT=kaidoku-r50
SCRATCH_PREFIX=/fast/scratch/hyaku/kaidoku-r50/
EVIDENCE_SEGMENT=/corpus/evidence/round-50/
# Identical to the round-42/49 FIXED_PATH so the extractor that resolves (`sasquatch`)
# is the same binary in the run and in a counter rerun.
FIXED_PATH="/usr/local/bin:/usr/bin:/bin:$HOME/.local/bin:$HOME/.local/share/fnm/node-versions/v24.21.0/installation/bin"

err() { echo "$PROG: $*" >&2; exit 2; }
fail() { echo "$PROG: $*" >&2; exit 3; }

usage() {
  cat >&2 <<'EOF'
usage: c1-run.sh after  --id ID --carrier FILE --data-run [OPTIONS]
       c1-run.sh oracle --id ID --carrier FILE [OPTIONS]
  OPTIONS
    --outdir DIR      output directory (default <lane>/corpus/evidence/round-50/c1/ID,
                      lane = this script's grandparent directory; needs corpus/evidence)
    --scratch BASE    scratch base; MUST contain a /kaidoku-r50/ segment
                      (default ${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kaidoku-r50)
    --pin SHA256      assert the carrier sha256 (exit 2 on mismatch)
    --data-run        state that the freeze is in place (or KAIDOKU_C1_DATA_RUN=1)
    --force           replace an occupied after.json / oracle.tsv slot
    --keep-scratch    keep the private scratch directory
    --dry-run         print the resolved plan; write nothing
  env  HYAKU_SCRATCH, REA_UNBLOB_COMMAND (default ~/.local/bin/unblob), C1_READER
       (default <repo>/tools/round-41/sqfs-list.py, else the script directory),
       C1_UNSQUASHFS (default /usr/bin/unsquashfs), C1_CHILD_PATH, C1_KEEP_ENVELOPE=1,
       C1_ALLOW_FOREIGN_SCRATCH=1, C1_ALLOW_NONAVM=1, C1_ALLOW_PIN_DRIFT=1,
       C1_ALLOW_NO_SASQUATCH=1 (after arm: waive the sasquatch precondition; ONLY for
       the CTL-C1-3 control, recorded in run.json)
EOF
  exit 2
}

# ------------------------------------------------------------------ arguments
mode=${1:-}
case "$mode" in after|oracle) shift ;; -h|--help) usage ;; *) usage ;; esac
cid=''; carrier_in=''; outdir_in=''; scratch_base_in=''; pin_in=''
data_run=${KAIDOKU_C1_DATA_RUN:-0}; [[ $data_run == 1 ]] || data_run=0
force=0; keep_scratch=0; dry_run=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --id)       [[ $# -ge 2 ]] || usage; cid=$2; shift 2 ;;
    --carrier)  [[ $# -ge 2 ]] || usage; carrier_in=$2; shift 2 ;;
    --outdir)   [[ $# -ge 2 ]] || usage; outdir_in=$2; shift 2 ;;
    --scratch)  [[ $# -ge 2 ]] || usage; scratch_base_in=$2; shift 2 ;;
    --pin)      [[ $# -ge 2 ]] || usage; pin_in=$2; shift 2 ;;
    --data-run) data_run=1; shift ;;
    --force)    force=1; shift ;;
    --keep-scratch) keep_scratch=1; shift ;;
    --dry-run)  dry_run=1; shift ;;
    -h|--help)  usage ;;
    *) echo "$PROG: unknown argument: $1" >&2; usage ;;
  esac
done
[[ $cid =~ ^[a-z0-9][a-z0-9_-]{0,31}$ ]] || err "--id must match ^[a-z0-9][a-z0-9_-]{0,31}\$ (got '$cid')"
[[ -n $carrier_in ]] || err "--carrier is required"
[[ -z $pin_in || $pin_in =~ ^[0-9a-f]{64}$ ]] || err "--pin is not 64 lowercase hex"

if [[ -n ${C1_CHILD_PATH:-} ]]; then child_path=$C1_CHILD_PATH; child_path_override=true
else child_path=$FIXED_PATH; child_path_override=false; fi
export PATH="$child_path"
command -v python3 >/dev/null || err "python3 not found on the child PATH $child_path"
command -v jq >/dev/null || err "jq not found on the child PATH $child_path"

[[ -f $carrier_in ]] || err "carrier is not a regular file: $carrier_in"
[[ -r $carrier_in ]] || err "carrier is not readable: $carrier_in"
carrier=$(realpath -- "$carrier_in")

lane_root=$(CDPATH='' cd -- "$SCRIPT_DIR/../.." && pwd -P)
if [[ -n $outdir_in ]]; then
  outdir=$(realpath -m -- "$outdir_in")
else
  [[ -d $lane_root/corpus/evidence ]] \
    || err "default OUTDIR needs the lane root two levels above $SCRIPT_DIR (no corpus/evidence there); pass --outdir"
  outdir=$lane_root/corpus/evidence/round-50/c1/$cid
fi

# Data-run guard.
under_evidence=false
case "$outdir/" in *"$EVIDENCE_SEGMENT"*) under_evidence=true ;; esac
if [[ $mode == after && $data_run != 1 ]]; then
  err "the after arm refuses without --data-run (or KAIDOKU_C1_DATA_RUN=1): it is the post-freeze data procedure, run by the L1 only"
fi
if [[ $mode == oracle && $under_evidence == true && $data_run != 1 ]]; then
  err "OUTDIR $outdir lies under $EVIDENCE_SEGMENT: refusing without --data-run (post-freeze, L1 only)"
fi

# Scratch base: must carry /kaidoku-r50/.
if [[ -n $scratch_base_in ]]; then scratch_base=$(realpath -m -- "$scratch_base_in")
else scratch_base=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/$ROUND_SEGMENT; fi
prov_segment_ok=true
case "$scratch_base/" in
  */"$ROUND_SEGMENT"/*) ;;
  *)
    if [[ ${C1_ALLOW_FOREIGN_SCRATCH:-0} == 1 ]]; then
      prov_segment_ok=false
      echo "$PROG: warning: scratch $scratch_base lacks a /$ROUND_SEGMENT/ segment; the R50-C1 output_directory clause will not hold" >&2
    else
      err "scratch $scratch_base lacks a /$ROUND_SEGMENT/ segment: a receipt written from it fails the R50-C1 run-provenance clause (parameters.output_directory is hashed into the evidence id). C1_ALLOW_FOREIGN_SCRATCH=1 permits a dev run."
    fi ;;
esac
# The counter requires output_directory to start with the canonical prefix.
prefix_ok=false
case "$scratch_base/" in "$SCRATCH_PREFIX"*) prefix_ok=true ;; esac
if [[ $mode == after && $prefix_ok != true && ${C1_ALLOW_FOREIGN_SCRATCH:-0} != 1 ]]; then
  err "scratch $scratch_base does not start with $SCRATCH_PREFIX: the receipt's output_directory would fail the counter's prefix test (HYAKU_SCRATCH must be /fast/scratch/hyaku)"
fi

slot=$([[ $mode == after ]] && echo after.json || echo oracle.tsv)
if [[ -e $outdir/$slot && $force != 1 ]]; then
  err "occupied slot: $outdir/$slot exists (use --force to replace)"
fi

reader_default=$SCRIPT_DIR/../round-41/sqfs-list.py
[[ -f $reader_default ]] || reader_default=$SCRIPT_DIR/sqfs-list.py
reader_in=${C1_READER:-$reader_default}
unsq_in=${C1_UNSQUASHFS:-/usr/bin/unsquashfs}
rea_timeout=900
max_output_bytes=${C1_MAX_OUTPUT_BYTES-536870912}
max_output_files=${C1_MAX_OUTPUT_FILES-100000}

if [[ $dry_run == 1 ]]; then
  echo "$PROG --dry-run: mode=$mode id=$cid"
  echo "  carrier=$carrier  pin=${pin_in:-none}"
  echo "  outdir=$outdir  under_evidence=$under_evidence  data_run=$data_run force=$force"
  echo "  scratch_base=$scratch_base  prov_segment_ok=$prov_segment_ok  prefix_ok=$prefix_ok"
  echo "  child_path=$child_path  override=$child_path_override"
  if [[ $mode == after ]]; then
    echo "  REA_UNBLOB_COMMAND=${REA_UNBLOB_COMMAND:-$HOME/.local/bin/unblob}"
    echo "  cwd=<scratch>/c1-run.XXXXXX  TMPDIR=<scratch>/c1-run.XXXXXX"
    echo "  timeout $rea_timeout npx -y $REA_PIN extract-firmware --format json --full-output --max-depth 1 ${max_output_bytes:+--max-output-bytes $max_output_bytes} ${max_output_files:+--max-output-files $max_output_files} $carrier <scratch>/c1-run.XXXXXX/extract"
    echo "  precondition: sasquatch (not sasquatch-v4be) on the child PATH"
  else
    echo "  reader: python3 -I -- $reader_in --layout auto|le --files … --nonregular … --inspect $carrier"
    echo "  unsquashfs: $unsq_in -no-xattrs -f -no-exit-code -d <scratch>/usq/root $carrier ; $unsq_in -lln $carrier"
    echo "  sasquatch: sasquatch -le -f -no-exit-code -n -d <scratch>/sq/root $carrier"
  fi
  exit 0
fi

# ------------------------------------------------------------- common helpers
carrier_sha=$(sha256sum "$carrier" | cut -d' ' -f1)
carrier_size=$(stat -c%s "$carrier")
if [[ -n $pin_in && $pin_in != "$carrier_sha" ]]; then
  err "carrier sha256 $carrier_sha != --pin $pin_in"
fi


arr_json() { printf '%s\n' "$@" | jq -R . | jq -s -c .; }
pin_drift_ok() { [[ ${C1_ALLOW_PIN_DRIFT:-0} == 1 ]]; }

# Tool pins: path, sha256, version line, version. `$1` = binary name or path.
tool_pin() { # sets: t_path t_sha t_line t_ver
  local bin=$1 flag=$2 p
  p=$(command -v -- "$bin" || true)
  [[ -n $p ]] || return 1
  t_path=$(realpath -- "$p")
  t_sha=$(sha256sum "$t_path" | cut -d' ' -f1)
  t_line=$("$t_path" "$flag" 2>&1 | sed -n 1p || true)
  t_ver=$(printf '%s' "$t_line" | sed -nE 's/.*[Vv]ersion ([0-9][0-9A-Za-z.]*).*/\1/p')
  [[ -n $t_ver ]] || t_ver=unknown
  return 0
}

# Superblock summary (LE). Prints JSON; `null` when the first 48 bytes carry no magic.
superblock=$(python3 -I - "$carrier" <<'PY'
import json, struct, sys
raw = open(sys.argv[1], 'rb').read(96)
magic = raw[:4]
if magic not in (b'hsqs', b'sqsh') or len(raw) < 48:
    print('null')
    raise SystemExit(0)
e = '<' if magic == b'hsqs' else '>'
mkfs, = struct.unpack(e + 'I', raw[8:12])
block_size, = struct.unpack(e + 'I', raw[12:16])
comp, = struct.unpack(e + 'H', raw[20:22])
major, minor = struct.unpack(e + 'HH', raw[28:32])
used, = struct.unpack(e + 'Q', raw[40:48])
print(json.dumps({'magic': magic.decode('ascii'),
                  'byte_order': 'little' if e == '<' else 'big',
                  'version': '%d.%d' % (major, minor), 'compression_id': comp,
                  'block_size': block_size, 'mkfs_time': mkfs, 'bytes_used': used,
                  'avm_marker': mkfs == used}))
PY
)
sb_ok=$(jq -r '. != null and .magic == "hsqs" and .version == "4.0" and .compression_id == 4 and .avm_marker == true' <<<"$superblock")
sb_waived=false
if [[ $sb_ok != true ]]; then
  if [[ ${C1_ALLOW_NONAVM:-0} == 1 ]]; then
    sb_waived=true
    echo "$PROG: warning: superblock is not LE hsqs v4.0 xz with mkfs_time == bytes_used; waived by C1_ALLOW_NONAVM=1: $superblock" >&2
  else
    err "carrier superblock is not little-endian hsqs v4.0, compression 4, mkfs_time == bytes_used (the AVM marker): $superblock"
  fi
fi
if [[ $superblock != null ]]; then
  [[ $(jq -r '.bytes_used <= '"$carrier_size" <<<"$superblock") == true ]] \
    || err "superblock bytes_used exceeds the carrier size $carrier_size: $superblock"
fi
mkdir -p "$outdir" || err "cannot create OUTDIR: $outdir"
mkdir -p "$scratch_base" || err "cannot create scratch base: $scratch_base"
scratch=$(mktemp -d "$scratch_base/c1-run.XXXXXX")
scratch=$(realpath -- "$scratch")
if [[ $keep_scratch == 1 ]]; then
  trap 'echo "$PROG: scratch kept: $scratch" >&2' EXIT
else
  trap 'chmod -R u+rwX -- "$scratch" 2>/dev/null || true; rm -rf -- "$scratch"' EXIT
fi
export TMPDIR=$scratch

# ---------------------------------------------------------------- oracle arm
if [[ $mode == oracle ]]; then
  [[ -f $reader_in && -r $reader_in ]] || err "reader not found/readable: $reader_in (set C1_READER)"
  reader=$(realpath -- "$reader_in")
  reader_sha=$(sha256sum "$reader" | cut -d' ' -f1)
  reader_help=$(python3 -I -- "$reader" --help 2>&1) || err "reader --help failed: $reader"
  for flag in --layout --files --nonregular --inspect; do
    grep -q -- "$flag" <<<"$reader_help" || err "reader does not advertise $flag in --help: $reader"
  done

  [[ -x $unsq_in ]] || err "unsquashfs not executable: $unsq_in"
  tool_pin "$unsq_in" -version || err "cannot pin unsquashfs"
  unsq=$t_path; unsq_sha=$t_sha; unsq_line=$t_line; unsq_ver=$t_ver
  [[ $unsq_ver == "$UNSQUASHFS_PIN" ]] || pin_drift_ok || err "unsquashfs is $unsq_ver, pin is $UNSQUASHFS_PIN"
  tool_pin sasquatch -version || err "sasquatch not resolvable on the child PATH $child_path (the cross-check extractor)"
  sq=$t_path; sq_sha=$t_sha; sq_line=$t_line; sq_ver=$t_ver
  [[ $sq_ver == "$SASQUATCH_PIN" ]] || pin_drift_ok || err "sasquatch is $sq_ver, pin is $SASQUATCH_PIN"

  # 1. reader, layouts auto (primary) and le (must agree byte for byte).
  run_reader() { # $1 layout, $2 prefix
    local rc
    reader_argv=(python3 -I -- "$reader" --layout "$1" \
                 --files "$scratch/$2.oracle.tsv" --nonregular "$scratch/$2.nonregular.tsv" \
                 --inspect "$carrier")
    set +e
    ( cd "$scratch" && "${reader_argv[@]}" ) > "$scratch/$2.inspect.json" 2> "$scratch/$2.err"
    rc=$?
    set -e
    return $rc
  }
  start=$(date -u +%FT%TZ); start_ms=$(date +%s%3N)
  run_reader auto ra && reader_rc=0 || reader_rc=$?
  reader_argv_json=$(arr_json "${reader_argv[@]}")
  end=$(date -u +%FT%TZ); dur=$(( $(date +%s%3N) - start_ms ))
  reader_err_head=$(sed -n '1,20p' "$scratch/ra.err" 2>/dev/null | cut -c1-400 || true)
  fail_run_json() { # $1 error key
    jq -n --arg schema kaidoku-r50-c1-run-v1 --arg mode oracle --arg claim R50-C1 --arg id "$cid" \
      --arg carrier "$carrier" --arg carrier_sha "$carrier_sha" --argjson carrier_size "$carrier_size" \
      --arg outdir "$outdir" --argjson prov_segment "$prov_segment_ok" \
      --arg reader "$reader" --arg reader_sha "$reader_sha" --argjson reader_argv "$reader_argv_json" \
      --arg start "$start" --arg end "$end" --argjson duration_ms "$dur" \
      --argjson reader_exit "$reader_rc" --arg reader_stderr "$reader_err_head" --arg error "$1" \
      '{schema: $schema, mode: $mode, claim: $claim, id: $id,
        carrier: {path: $carrier, sha256: $carrier_sha, size_bytes: $carrier_size},
        outdir: $outdir, run_provenance_segment_ok: $prov_segment,
        reader: {path: $reader, sha256: $reader_sha, argv: $reader_argv},
        start_utc: $start, end_utc: $end, duration_ms: $duration_ms,
        reader_exit: $reader_exit, reader_stderr_head: $reader_stderr, error: $error}' \
      > "$outdir/oracle-run.json"
  }
  if [[ $reader_rc -ne 0 ]]; then
    fail_run_json reader_failed
    fail "reader (auto) exited $reader_rc (see $outdir/oracle-run.json)"
  fi
  reader_argv_auto_json=$reader_argv_json
  run_reader le rl && rl_rc=0 || rl_rc=$?
  reader_argv_le_json=$(arr_json "${reader_argv[@]}")
  [[ $rl_rc -eq 0 ]] || fail "reader (le) exited $rl_rc: $(sed -n 1p "$scratch/rl.err")"
  layouts_equal=false
  if cmp -s "$scratch/ra.oracle.tsv" "$scratch/rl.oracle.tsv" \
     && cmp -s "$scratch/ra.nonregular.tsv" "$scratch/rl.nonregular.tsv"; then layouts_equal=true; fi
  [[ $layouts_equal == true ]] || fail "reader --layout auto and --layout le tables differ"
  [[ -f $scratch/ra.oracle.tsv && -f $scratch/ra.nonregular.tsv ]] || fail "reader wrote no tables"
  cp -f "$scratch/ra.oracle.tsv" "$scratch/oracle.tsv"
  cp -f "$scratch/ra.nonregular.tsv" "$scratch/nonregular.tsv"
  jq -e . "$scratch/ra.inspect.json" >/dev/null 2>&1 || fail "reader --inspect did not print JSON"
  inspect_json=$(jq -c . "$scratch/ra.inspect.json")
  inspect_ok=$(jq -r '.endian == "little" and .compression == "xz" and .avm_marker == true' <<<"$inspect_json")
  if [[ $inspect_ok != true && $sb_waived != true ]]; then
    fail "reader --inspect disagrees with the LE-AVM claim (endian/compression/avm_marker): $inspect_json"
  fi

  # Validate the reader tables (grammar, closed kind vocabulary, ordering, overlap).
  tables=$(python3 -I - "$scratch/oracle.tsv" "$scratch/nonregular.tsv" <<'PY'
import json, re, sys

KINDS = {'dir', 'symlink', 'char-device', 'block-device', 'fifo', 'socket'}
HEX = re.compile(r'[0-9a-f]{64}\Z')


def load(path):
    rows = []
    with open(path, encoding='utf-8', errors='surrogateescape') as fh:
        for n, line in enumerate(fh.read().split('\n'), 1):
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

  # 2. unsquashfs (the plan's named oracle): extraction tree + -lln listing.
  mkdir -p "$scratch/usq"
  usq_argv=("$unsq" -no-xattrs -no-progress -f -no-exit-code -d "$scratch/usq/root" "$carrier")
  usq_argv_json=$(arr_json "${usq_argv[@]}")
  usq_start=$(date -u +%FT%TZ); usq_start_ms=$(date +%s%3N)
  set +e
  ( cd "$scratch" && "${usq_argv[@]}" ) > "$scratch/usq.log" 2>&1
  usq_rc=$?
  set -e
  usq_end=$(date -u +%FT%TZ); usq_dur=$(( $(date +%s%3N) - usq_start_ms ))
  usq_log_head=$(sed -n '1,20p' "$scratch/usq.log" 2>/dev/null | cut -c1-400 || true)
  "$unsq" -lln "$carrier" > "$scratch/usq.listing" 2> "$scratch/usq.listing.err" \
    || fail "unsquashfs -lln exited $?: $(sed -n 1p "$scratch/usq.listing.err")"

  # 3. sasquatch -le cross-check extraction.
  mkdir -p "$scratch/sq"
  sq_argv=("$sq" -le -f -no-exit-code -n -d "$scratch/sq/root" "$carrier")
  sq_argv_json=$(arr_json "${sq_argv[@]}")
  sq_start=$(date -u +%FT%TZ); sq_start_ms=$(date +%s%3N)
  set +e
  ( cd "$scratch" && "${sq_argv[@]}" ) > "$scratch/sasq.log" 2>&1
  sq_rc=$?
  set -e
  sq_end=$(date -u +%FT%TZ); sq_dur=$(( $(date +%s%3N) - sq_start_ms ))
  sq_log_head=$(sed -n '1,20p' "$scratch/sasq.log" 2>/dev/null | cut -c1-400 || true)

  # Compare: write oracle-unsquashfs.tsv / oracle-check.tsv, print the verdict JSON.
  cross=$(python3 -I - "$scratch/usq/root" "$scratch/sq/root" "$scratch/usq.listing" \
                "$scratch/oracle.tsv" "$scratch/nonregular.tsv" \
                "$scratch/oracle-unsquashfs.tsv" "$scratch/oracle-check.tsv" <<'PY'
import hashlib, json, os, re, stat, sys

usq_root, sq_root, listing, oracle_tsv, nonreg_tsv, out_usq, out_chk = sys.argv[1:8]
E = 'utf-8'


def b2s(b):
    return b.decode(E, 'surrogateescape')


def load(path, nfields=3):
    rows = []
    with open(path, 'rb') as fh:
        for line in fh.read().split(b'\n'):
            if line:
                rows.append(line.split(b'\t'))
    return rows


def hash_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def walk(root):
    """(regular {rel: (sha, size)}, nonregular {rel: (kind, detail)}, unsafe [rel]).
    lstat only, no symlink following; the root itself is not listed."""
    root = os.fsencode(root)
    if not os.path.isdir(root):
        return None, None, []
    # an unprivileged extraction may leave unreadable directory modes
    for dp, dns, fns in os.walk(root, followlinks=False):
        for n in dns:
            q = os.path.join(dp, n)
            if not os.path.islink(q):
                os.chmod(q, os.lstat(q).st_mode | 0o700)
    reg, non, unsafe = {}, {}, []
    for dp, dns, fns in os.walk(root, followlinks=False):
        for n in dns + fns:
            p = os.path.join(dp, n)
            rel = os.path.relpath(p, root).replace(os.sep.encode(), b'/')
            if any(c in rel for c in (b'\t', b'\n', b'\r')):
                unsafe.append(b2s(rel))
            m = os.lstat(p).st_mode
            if stat.S_ISLNK(m):
                non[rel] = ('symlink', os.readlink(p))
            elif stat.S_ISDIR(m):
                non[rel] = ('dir', b'')
            elif stat.S_ISREG(m):
                if not (m & 0o400):
                    os.chmod(p, m | 0o400)
                reg[rel] = (hash_file(p), os.lstat(p).st_size)
            else:
                non[rel] = ('other', b'')
    return reg, non, unsafe


def write_tsv(path, reg):
    with open(path, 'wb') as fh:
        for rel in sorted(reg):
            sha, size = reg[rel]
            fh.write(rel + b'\t' + sha.encode() + b'\t' + str(size).encode() + b'\n')


oracle = {r[0]: (r[1].decode(), int(r[2])) for r in load(oracle_tsv)}
onon = {r[0]: (r[1].decode(), r[2]) for r in load(nonreg_tsv)}
usq_reg, usq_non, usq_unsafe = walk(usq_root)
sq_reg, sq_non, sq_unsafe = walk(sq_root)
if usq_reg is None or sq_reg is None:
    print(json.dumps({'error': 'extraction root missing', 'usq': usq_reg is not None,
                      'sasquatch': sq_reg is not None}))
    raise SystemExit(0)
write_tsv(out_usq, usq_reg)
write_tsv(out_chk, sq_reg)

# special entries (c/b/p/s) from the unsquashfs -lln listing
# `<mode> <uid>/<gid> [<major>, <minor> | <size>] <date> <time> squashfs-root/<path>`
special = {}
rx_dev = re.compile(rb'^([cb])\S{9}\s+\S+\s+(\d+),\s*(\d+)\s+\d{4}-\d\d-\d\d \d\d:\d\d(?::\d\d)?\s(.*)$')
rx_pf = re.compile(rb'^([ps])\S{9}\s+\S+\s+\d+\s+\d{4}-\d\d-\d\d \d\d:\d\d(?::\d\d)?\s(.*)$')
with open(listing, 'rb') as fh:
    for line in fh.read().split(b'\n'):
        m = rx_dev.match(line)
        if m:
            kind = 'char-device' if m.group(1) == b'c' else 'block-device'
            name, detail = m.group(4), b'%s:%s' % (m.group(2), m.group(3))
        else:
            m = rx_pf.match(line)
            if not m:
                continue
            kind = 'fifo' if m.group(1) == b'p' else 'socket'
            name, detail = m.group(2), b''
        if name.startswith(b'squashfs-root/'):
            name = name[len(b'squashfs-root/'):]
        special[name] = (kind, detail)

mismatches = []


def cmp_reg(label, other):
    for rel in sorted(set(oracle) | set(other)):
        o, c = oracle.get(rel), other.get(rel)
        if o == c:
            continue
        if c is None:
            mismatches.append({'against': label, 'relpath': b2s(rel), 'kind': 'missing', 'oracle': o})
        elif o is None:
            mismatches.append({'against': label, 'relpath': b2s(rel), 'kind': 'extra', 'other': c})
        else:
            mismatches.append({'against': label, 'relpath': b2s(rel),
                               'kind': 'sha256' if o[0] != c[0] else 'size', 'oracle': o, 'other': c})


cmp_reg('unsquashfs', usq_reg)
cmp_reg('sasquatch-le', sq_reg)

# dir/symlink rows against both extraction trees
want = {rel: v for rel, v in onon.items() if v[0] in ('dir', 'symlink')}
for label, tree in (('unsquashfs', usq_non), ('sasquatch-le', sq_non)):
    have = {rel: (k, b2s(d) if k == 'symlink' else '') for rel, (k, d) in tree.items()
            if k in ('dir', 'symlink')}
    wantd = {rel: (k, b2s(d) if k == 'symlink' else '') for rel, (k, d) in want.items()}
    # the extraction can also hold device/fifo placeholders only if privileged
    for rel in sorted(set(wantd) | set(have)):
        if wantd.get(rel) != have.get(rel):
            mismatches.append({'against': label + ':nonregular', 'relpath': b2s(rel),
                               'kind': 'nonregular', 'oracle': wantd.get(rel), 'other': have.get(rel)})
# device/fifo/socket rows against the -lln listing
wsp = {rel: (k, b2s(d)) for rel, (k, d) in onon.items() if k not in ('dir', 'symlink')}
hsp = {rel: (k, b2s(d)) for rel, (k, d) in special.items()}
for rel in sorted(set(wsp) | set(hsp)):
    if wsp.get(rel) != hsp.get(rel):
        mismatches.append({'against': 'unsquashfs:-lln', 'relpath': b2s(rel),
                           'kind': 'special', 'oracle': wsp.get(rel), 'other': hsp.get(rel)})
for label, tree in (('unsquashfs', usq_non), ('sasquatch-le', sq_non)):
    for rel, (k, d) in tree.items():
        if k == 'other':
            mismatches.append({'against': label, 'relpath': b2s(rel), 'kind': 'unexpected-special-in-tree'})
unsafe = sorted(set(usq_unsafe) | set(sq_unsafe) | {b2s(k) for k in oracle if any(c in k for c in (b'\t', b'\n', b'\r'))})
print(json.dumps({
    'all_equal': not mismatches and not unsafe,
    'unsquashfs_files': len(usq_reg), 'sasquatch_files': len(sq_reg),
    'unsquashfs_nonregular_in_tree': len(usq_non), 'sasquatch_nonregular_in_tree': len(sq_non),
    'special_in_listing': len(special),
    'tsv_unsafe_paths': unsafe[:20],
    'mismatch_count': len(mismatches), 'mismatches': mismatches[:20],
}))
PY
  ) || fail "comparison listing failed"
  jq -e 'has("error") | not' <<<"$cross" >/dev/null || fail "extraction root missing: $cross"

  cp -f "$scratch/oracle.tsv" "$outdir/oracle.tsv"
  cp -f "$scratch/nonregular.tsv" "$outdir/nonregular.tsv"
  cp -f "$scratch/oracle-unsquashfs.tsv" "$outdir/oracle-unsquashfs.tsv"
  cp -f "$scratch/oracle-check.tsv" "$outdir/oracle-check.tsv"
  cross_ok=$(jq -r '.all_equal' <<<"$cross")

  jq -n \
    --arg schema kaidoku-r50-c1-run-v1 --arg mode oracle --arg claim R50-C1 --arg id "$cid" \
    --arg carrier "$carrier" --arg carrier_sha "$carrier_sha" --argjson carrier_size "$carrier_size" \
    --argjson superblock "$superblock" --argjson sb_waived "$sb_waived" \
    --arg outdir "$outdir" --argjson prov_segment "$prov_segment_ok" \
    --arg scratch_base "$scratch_base" --arg child_path "$child_path" \
    --arg reader "$reader" --arg reader_sha "$reader_sha" \
    --argjson reader_argv_auto "$reader_argv_auto_json" --argjson reader_argv_le "$reader_argv_le_json" \
    --argjson layouts_equal "$layouts_equal" \
    --arg start "$start" --arg end "$end" --argjson duration_ms "$dur" \
    --argjson reader_exit "$reader_rc" --arg reader_stderr "$reader_err_head" \
    --arg unsq "$unsq" --arg unsq_sha "$unsq_sha" --arg unsq_ver "$unsq_ver" --arg unsq_line "$unsq_line" \
    --argjson usq_argv "$usq_argv_json" --arg usq_start "$usq_start" --arg usq_end "$usq_end" \
    --argjson usq_duration_ms "$usq_dur" --argjson usq_exit "$usq_rc" --arg usq_log "$usq_log_head" \
    --arg sq "$sq" --arg sq_sha "$sq_sha" --arg sq_ver "$sq_ver" --arg sq_line "$sq_line" \
    --argjson sq_argv "$sq_argv_json" --arg sq_start "$sq_start" --arg sq_end "$sq_end" \
    --argjson sq_duration_ms "$sq_dur" --argjson sq_exit "$sq_rc" --arg sq_log "$sq_log_head" \
    --argjson tables "$tables" --argjson cross "$cross" --argjson inspect "$inspect_json" \
    --arg f1 "$(sha256sum "$outdir/oracle.tsv" | cut -d' ' -f1)" --argjson b1 "$(stat -c%s "$outdir/oracle.tsv")" \
    --arg f2 "$(sha256sum "$outdir/nonregular.tsv" | cut -d' ' -f1)" --argjson b2 "$(stat -c%s "$outdir/nonregular.tsv")" \
    --arg f3 "$(sha256sum "$outdir/oracle-unsquashfs.tsv" | cut -d' ' -f1)" --argjson b3 "$(stat -c%s "$outdir/oracle-unsquashfs.tsv")" \
    --arg f4 "$(sha256sum "$outdir/oracle-check.tsv" | cut -d' ' -f1)" --argjson b4 "$(stat -c%s "$outdir/oracle-check.tsv")" \
    '{
      schema: $schema, mode: $mode, claim: $claim, id: $id,
      carrier: {path: $carrier, sha256: $carrier_sha, size_bytes: $carrier_size,
                superblock: $superblock, superblock_precondition_waived: $sb_waived},
      outdir: $outdir, layout: "auto+le", squashfs_offset: 0,
      run_provenance_segment_ok: $prov_segment, scratch_base: $scratch_base, child_path: $child_path,
      reader: {path: $reader, sha256: $reader_sha, argv_auto: $reader_argv_auto, argv_le: $reader_argv_le,
               auto_le_tables_equal: $layouts_equal, start_utc: $start, end_utc: $end,
               duration_ms: $duration_ms, exit: $reader_exit, stderr_head: $reader_stderr},
      unsquashfs: {path: $unsq, sha256: $unsq_sha, version: $unsq_ver, version_line: $unsq_line,
                   argv: $usq_argv, start_utc: $usq_start, end_utc: $usq_end,
                   duration_ms: $usq_duration_ms, exit: $usq_exit, log_head: $usq_log},
      sasquatch: {path: $sq, sha256: $sq_sha, version: $sq_ver, version_line: $sq_line,
                  argv: $sq_argv, start_utc: $sq_start, end_utc: $sq_end,
                  duration_ms: $sq_duration_ms, exit: $sq_exit, log_head: $sq_log},
      tables: $tables,
      outputs: {
        oracle_tsv: {path: "oracle.tsv", sha256: $f1, bytes: $b1},
        nonregular_tsv: {path: "nonregular.tsv", sha256: $f2, bytes: $b2},
        oracle_unsquashfs_tsv: {path: "oracle-unsquashfs.tsv", sha256: $f3, bytes: $b3},
        oracle_check_tsv: {path: "oracle-check.tsv", sha256: $f4, bytes: $b4}
      },
      crosscheck: $cross,
      reader_inspect: $inspect
    }' > "$outdir/oracle-run.json"

  [[ $usq_rc -eq 0 ]] || fail "unsquashfs exited $usq_rc (see $outdir/oracle-run.json)"
  [[ $sq_rc -eq 0 ]] || fail "sasquatch exited $sq_rc (see $outdir/oracle-run.json)"
  [[ $cross_ok == true ]] || fail "producers disagree ($(jq -r '.mismatch_count' <<<"$cross") rows, unsafe paths $(jq -c '.tsv_unsafe_paths' <<<"$cross"); see $outdir/oracle-run.json)"
  exit 0
fi

# ----------------------------------------------------------------- after arm
command -v npx >/dev/null || err "npx not found on the child PATH $child_path"
sasq_waived=false
if ! tool_pin sasquatch -version; then
  if [[ ${C1_ALLOW_NO_SASQUATCH:-0} == 1 ]]; then
    sasq_waived=true; t_path=''; t_sha=''; t_line=''; t_ver=''
    echo "$PROG: warning: sasquatch absent from the child PATH; waived by C1_ALLOW_NO_SASQUATCH=1 (CTL-C1-3 control only)" >&2
  else
    err "sasquatch not resolvable on the child PATH $child_path (the after arm's precondition; sasquatch-v4be does not satisfy it)"
  fi
elif [[ $t_ver != "$SASQUATCH_PIN" ]] && ! pin_drift_ok; then
  err "sasquatch is $t_ver, pin is $SASQUATCH_PIN"
fi
sq=$t_path; sq_sha=$t_sha; sq_line=$t_line; sq_ver=$t_ver

unblob_env=${REA_UNBLOB_COMMAND:-$HOME/.local/bin/unblob}
[[ -x $unblob_env ]] || err "REA_UNBLOB_COMMAND is missing or not executable: $unblob_env"
unblob=$(realpath -- "$unblob_env")
unblob_sha=$(sha256sum "$unblob" | cut -d' ' -f1)
unblob_ver=$("$unblob" --version 2>&1 | sed -n 1p || true)
[[ -n $unblob_ver ]] || unblob_ver=unknown
[[ $unblob_ver == "$UNBLOB_PIN" ]] || pin_drift_ok || err "unblob is $unblob_ver, pin is $UNBLOB_PIN"
export REA_UNBLOB_COMMAND=$unblob

rea_ver=$(timeout 120 npx -y "$REA_PIN" --version 2>/dev/null | sed -n '$p' || true)
[[ -n $rea_ver ]] || rea_ver=unknown
rea_root=$(find "${npm_config_cache:-$HOME/.npm}/_npx" -maxdepth 5 \
  -path '*/node_modules/rea-agents/package.json' -print 2>/dev/null \
  | while IFS= read -r p; do
      [[ $(jq -r '.version' "$p" 2>/dev/null) == "${REA_PIN#rea-agents@}" ]] && printf '%s\n' "${p%/package.json}"
    done | sed -n '$p' || true)
[[ -n $rea_root ]] || rea_root=unknown
[[ $rea_ver == "${REA_PIN#rea-agents@}" ]] || pin_drift_ok || err "rea-agents reports $rea_ver, pin is ${REA_PIN#rea-agents@}"

prev_after_sha=''
[[ -f $outdir/after.json ]] && prev_after_sha=$(sha256sum "$outdir/after.json" | cut -d' ' -f1)

extract_root=$scratch/extract   # REA refuses an existing root: never pre-created
argv=(npx -y "$REA_PIN" extract-firmware --format json --full-output --max-depth 1)
# REA 6.5.0 on the a7530 member (15150 inodes, 172 MB) fails at the default budgets
# ("Staging entry budget exceeded (10000)"); both limits below are the schema maxima and
# are the frozen REA parameters for every carrier (the counter replays them from the receipt).
[[ -n $max_output_bytes ]] && argv+=(--max-output-bytes "$max_output_bytes")
[[ -n $max_output_files ]] && argv+=(--max-output-files "$max_output_files")
argv+=("$carrier" "$extract_root")
argv_json=$(arr_json "${argv[@]}")

start=$(date -u +%FT%TZ); start_ms=$(date +%s%3N)
set +e
( cd "$scratch" && timeout "$rea_timeout" "${argv[@]}" ) > "$scratch/envelope.json" 2> "$scratch/rea.err"
rc=$?
set -e
end=$(date -u +%FT%TZ); dur=$(( $(date +%s%3N) - start_ms ))

envelope_parseable=false; envelope_ok=false; have_data=false; envelope_error=null
if jq -e 'type == "object"' "$scratch/envelope.json" >/dev/null 2>&1; then
  envelope_parseable=true
  [[ $(jq -r '.ok == true' "$scratch/envelope.json") == true ]] && envelope_ok=true
  if [[ $envelope_ok == true ]] && jq -e '(.data | type) == "object"' "$scratch/envelope.json" >/dev/null 2>&1; then
    have_data=true
  fi
  envelope_error=$(jq -c 'if .ok == true then null else (.error // null) end' "$scratch/envelope.json")
fi

summary=null; receipt=null
subject_ok=null; outdir_prefix_ok=null; handler_le=null; no_failed_chunk=null
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
      chunks: ((.normalized_result.chunks // []) | length),
      chunks_detail: [((.normalized_result.chunks // [])[]) | {handler, range, extraction_failed}],
      files: ((.normalized_result.files // []) | length),
      published_bytes: (.normalized_result.published_bytes // null),
      gaps: ((.normalized_result.extraction_gaps // []) | length),
      gaps_detail: [((.normalized_result.extraction_gaps // [])[:20][]) | {kind, relative_path: (.relative_path // null), handler: (.handler // null), dependencies: (.dependencies // [])}],
      unpublished_entries: ((.normalized_result.unpublished_entries // []) | length),
      unpublished_entries_by_kind: ([(.normalized_result.unpublished_entries // [])[] | (.kind // "unknown")] | group_by(.) | map({key: .[0], value: length}) | from_entries),
      unpublished_entries_head: [((.normalized_result.unpublished_entries // [])[:20][]) | {relative_path: (.relative_path // null), kind: (.kind // null), link_target: (.link_target // null)}],
      parameters: (.parameters // null),
      selection_sha256: (.normalized_result.selection.sha256 // null),
      subject_sha256: (.subject.digest.sha256 // null),
      output_directory: (.normalized_result.output_directory // null),
      parameters_output_directory: (.parameters.output_directory // null)
    }' "$scratch/after.json")
  subject_ok=$([[ $(jq -r '.subject_sha256' <<<"$summary") == "$carrier_sha" ]] && echo true || echo false)
  outdir_prefix_ok=$(jq -r --arg pre "$SCRATCH_PREFIX" \
    '((.parameters_output_directory // .output_directory // "") | (startswith($pre) and (contains("..") | not)))' <<<"$summary")
  handler_le=$(jq -r '.handlers | index("squashfs_v4_le") != null' <<<"$summary")
  no_failed_chunk=$(jq -r '[(.normalized_result.chunks // [])[] | select(.extraction_failed != false)] | length == 0' "$scratch/after.json")
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
[[ ${C1_KEEP_ENVELOPE:-0} == 1 ]] && cp -f "$scratch/envelope.json" "$outdir/after.envelope.json"

stderr_head=$({ grep -v 'npm warn' "$scratch/rea.err" 2>/dev/null || true; } | sed -n '1,20p' | cut -c1-400)

jq -n \
  --arg schema kaidoku-r50-c1-run-v1 --arg mode after --arg claim R50-C1 --arg id "$cid" \
  --arg carrier "$carrier" --arg carrier_sha "$carrier_sha" --argjson carrier_size "$carrier_size" \
  --argjson superblock "$superblock" --argjson sb_waived "$sb_waived" \
  --arg outdir "$outdir" --arg extract_root "$extract_root" --arg cwd "$scratch" \
  --argjson prov_segment "$prov_segment_ok" --argjson prefix_ok "$prefix_ok" \
  --argjson argv "$argv_json" \
  --arg argv_shell "REA_UNBLOB_COMMAND=$unblob ${argv[*]}" \
  --arg start "$start" --arg end "$end" --argjson duration_ms "$dur" --argjson exit "$rc" \
  --arg rea_pin "$REA_PIN" --arg rea_ver "$rea_ver" --arg rea_root "$rea_root" \
  --arg unblob_env "$unblob_env" --arg unblob "$unblob" --arg unblob_sha "$unblob_sha" --arg unblob_ver "$unblob_ver" \
  --arg sq "$sq" --arg sq_sha "$sq_sha" --arg sq_ver "$sq_ver" --arg sq_line "$sq_line" \
  --argjson sasq_waived "$sasq_waived" \
  --arg path "$PATH" --argjson path_override "$child_path_override" \
  --argjson env_parseable "$envelope_parseable" --argjson env_ok "$envelope_ok" \
  --argjson env_error "$envelope_error" \
  --arg env_sha "$(sha256sum "$scratch/envelope.json" | cut -d' ' -f1)" \
  --argjson env_bytes "$(stat -c%s "$scratch/envelope.json")" \
  --argjson have_data "$have_data" --argjson receipt_written "$receipt_written" \
  --argjson receipt "$receipt" --argjson summary "$summary" \
  --argjson subject_ok "$subject_ok" --argjson outdir_prefix_ok "$outdir_prefix_ok" \
  --argjson handler_le "$handler_le" --argjson no_failed_chunk "$no_failed_chunk" \
  --arg prev_after "$prev_after_sha" --arg stderr_head "$stderr_head" \
  '{
    schema: $schema, mode: $mode, claim: $claim, id: $id,
    carrier: {path: $carrier, sha256: $carrier_sha, size_bytes: $carrier_size,
              superblock: $superblock, superblock_precondition_waived: $sb_waived},
    outdir: $outdir,
    argv: $argv, argv_shell: $argv_shell, cwd: $cwd,
    run_provenance_segment_ok: $prov_segment, output_directory_prefix_ok: $prefix_ok,
    extraction_root: $extract_root,
    start_utc: $start, end_utc: $end, duration_ms: $duration_ms, exit: $exit,
    rea: {pin: $rea_pin, version: $rea_ver, package_root: $rea_root},
    unblob: {env_value: $unblob_env, command_env: $unblob, sha256: $unblob_sha, version: $unblob_ver},
    sasquatch: {path: $sq, sha256: $sq_sha, version: $sq_ver, version_line: $sq_line,
                precondition_waived: $sasq_waived},
    child_path: $path, child_path_override: $path_override,
    envelope: {parseable: $env_parseable, ok: $env_ok, sha256: $env_sha, bytes: $env_bytes,
               error: $env_error},
    data_extracted: $have_data,
    receipt_written: $receipt_written,
    receipt: $receipt,
    envelope_data_summary: $summary,
    harness_observations: {subject_digest_equals_carrier: $subject_ok,
                           receipt_output_directory_prefix_ok: $outdir_prefix_ok,
                           handler_squashfs_v4_le_named: $handler_le,
                           no_failed_chunk: $no_failed_chunk},
    previous_after_json_sha256: (if $prev_after == "" then null else $prev_after end),
    stderr_head: $stderr_head
  }' > "$outdir/run.json"

if [[ $receipt_written != true ]]; then
  echo "$PROG: no receipt written (rea exit $rc, envelope ok=$envelope_ok, data=$have_data); see $outdir/run.json" >&2
  exit 3
fi
if [[ $no_failed_chunk != true ]]; then
  echo "$PROG: note: a chunk reports extraction_failed (recorded as a negative; the counter judges): gaps $(jq -c '[.gaps_detail[].kind]' <<<"$summary")" >&2
fi
if [[ $handler_le != true ]]; then
  echo "$PROG: note: the receipt does not name squashfs_v4_le (recorded; the counter judges): handlers $(jq -c '.handlers' <<<"$summary")" >&2
fi
if [[ $subject_ok != true ]]; then
  echo "$PROG: receipt subject digest != carrier sha256; see $outdir/run.json" >&2
  exit 3
fi
exit 0
