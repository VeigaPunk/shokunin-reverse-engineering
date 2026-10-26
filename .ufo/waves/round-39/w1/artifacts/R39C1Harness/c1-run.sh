#!/usr/bin/env bash
# R39-C1 run harness (kaidoku round 39). Two arms, one carrier each.
#
#   c1-run.sh after  CARRIER OUTDIR [SCRATCH]
#     REA extract-firmware (rea-agents@6.5.0, --format json --full-output) via
#     `npx -y`, run with cwd = a private scratch dir, REA_UNBLOB_COMMAND
#     defaulting to ~/.local/bin/unblob. The child PATH is the inherited PATH
#     and MUST resolve sasquatch-v4be (that is the arm's precondition; the
#     harness exits 2 when it does not). The extraction root is
#     `$SCRATCH/extract` (REA refuses an existing root, so it is never
#     pre-created) and is deleted with the scratch on exit.
#       writes OUTDIR/after.json  = the envelope's `data` object (the REA
#                                   evidence object the counter reads), only
#                                   when REA exits 0 with ok=true
#       writes OUTDIR/run.json    = argv, UTC start/end + duration, exit
#                                   codes, sasquatch-v4be path/sha256/version,
#                                   rea + unblob versions, carrier pin,
#                                   envelope digest, receipt digest
#       C1_KEEP_ENVELOPE=1 additionally keeps the raw {ok,data,meta}
#                                   envelope as OUTDIR/after.envelope.json
#
#   A non-default SCRATCH must contain a /kaidoku-r39/ path segment: the receipt's
#   hashed parameters.output_directory is what proves the run happened this round,
#   so the harness refuses (exit 2) a scratch that cannot satisfy the R39-C1
#   counter's run_provenance_ok clause. C1_ALLOW_FOREIGN_SCRATCH=1 downgrades that
#   refusal to a warning and records run_provenance_segment_ok:false (dev runs).
#
#   c1-run.sh oracle CARRIER OUTDIR [SCRATCH]
#     Independent cross-tool oracle: sasquatch-v4be -be extraction into
#     $SCRATCH/root, then a listing computed by the harness itself (lstat, no
#     symlink following).
#       writes OUTDIR/oracle-check.tsv            relpath TAB sha256 TAB size
#                                                 (regular files, sorted)
#       writes OUTDIR/oracle-symlinks-check.tsv   relpath TAB target TAB
#                                                 in-tree|escaping
#       writes OUTDIR/oracle-run.json             offset, sasquatch pin, counts
#     The oracle-check.tsv grammar is byte-compatible with the frozen
#     corpus oracle.tsv, so `diff` is the cross-check. A symlink resolves
#     POSIX-style against the link's own directory with the extraction root as
#     `/`; it is `in-tree` when the normalised result stays at or below the
#     root and `escaping` otherwise (absolute targets are resolved from `/`).
#
# Scratch lives under $HYAKU_SCRATCH (default /fast/scratch/hyaku) in
# kaidoku-r39/, or at the explicit SCRATCH argument; either way it is removed
# on exit. TMPDIR points into it so REA staging and unblob.log land there.
#
# Exit: 0 ok, 2 usage/environment error, 3 tool failure.
set -euo pipefail

PROG=$(basename "$0")

usage() {
  cat >&2 <<'EOF'
usage: c1-run.sh after  CARRIER OUTDIR [SCRATCH]
       c1-run.sh oracle CARRIER OUTDIR [SCRATCH]
  after   REA extract-firmware (rea-agents@6.5.0 + unblob 26.6.4, sasquatch-v4be
          on PATH) -> OUTDIR/after.json (the `data` object) + OUTDIR/run.json
  oracle  independent sasquatch-v4be -be extraction -> OUTDIR/oracle-check.tsv,
          OUTDIR/oracle-symlinks-check.tsv + OUTDIR/oracle-run.json
  env     HYAKU_SCRATCH (default /fast/scratch/hyaku), REA_UNBLOB_COMMAND
          (default $HOME/.local/bin/unblob), C1_KEEP_ENVELOPE=1 (after arm only),
          C1_ALLOW_FOREIGN_SCRATCH=1 (permit a SCRATCH without a /kaidoku-r39/ segment)
EOF
  exit 2
}

err() { echo "$PROG: $*" >&2; exit 2; }

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

carrier=$(realpath "$carrier_in")
carrier_sha=$(sha256sum "$carrier" | cut -d' ' -f1)
carrier_size=$(stat -c%s "$carrier")

mkdir -p "$outdir_in" || err "cannot create OUTDIR: $outdir_in"
outdir=$(realpath "$outdir_in")

scratch_root=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kaidoku-r39
mkdir -p "$scratch_root" || err "cannot create scratch root: $scratch_root"
prov_segment_ok=true
if [[ -n $scratch_arg ]]; then
  scratch=$(realpath -m "$scratch_arg")
  case "$scratch/" in
    */kaidoku-r39/*) ;;
    *)
      if [[ ${C1_ALLOW_FOREIGN_SCRATCH:-0} == 1 ]]; then
        prov_segment_ok=false
        echo "$PROG: warning: SCRATCH $scratch lacks a /kaidoku-r39/ segment; the R39-C1"\
             "counter's run_provenance_ok clause (receipt parameters.output_directory) will not match" >&2
      else
        err "SCRATCH $scratch lacks a /kaidoku-r39/ segment: a receipt written from it fails the"\
            "R39-C1 counter's run_provenance_ok clause (parameters.output_directory is hashed into the"\
            "evidence id). Use the default scratch, or set C1_ALLOW_FOREIGN_SCRATCH=1 for a dev run."
      fi ;;
  esac
  mkdir -p "$scratch" || err "cannot create SCRATCH: $scratch"
else
  scratch=$(mktemp -d "$scratch_root/c1-run.XXXXXX")
  scratch=$(realpath "$scratch")
fi
trap 'rm -rf -- "$scratch"' EXIT
export TMPDIR=$scratch

# ---------------------------------------------------------------- oracle arm
if [[ $mode == oracle ]]; then
  sq=$(command -v sasquatch-v4be || true)
  [[ -n $sq ]] || err "sasquatch-v4be not resolvable on PATH"
  sq=$(realpath "$sq")
  sq_sha=$(sha256sum "$sq" | cut -d' ' -f1)
  sq_line=$("$sq" -version 2>&1 | sed -n 1p || true)
  sq_ver=$(printf '%s' "$sq_line" | sed -nE 's/.*[Vv]ersion ([0-9][0-9A-Za-z.]*).*/\1/p')
  [[ -n $sq_ver ]] || sq_ver=unknown

  offset=$(python3 -I - "$carrier" <<'PY'
import sys
raw = open(sys.argv[1], 'rb').read(1 << 20)
hits = [i for i in (raw.find(b'sqsh'), raw.find(b'hsqs')) if i >= 0]
if not hits:
    sys.exit(1)
print(min(hits))
PY
  ) || err "no squashfs magic (sqsh|hsqs) in the first 1 MiB of $carrier"

  mkdir -p "$scratch/root"
  start=$(date -u +%FT%TZ); start_ms=$(date +%s%3N)
  set +e
  "$sq" -be -n -o "$offset" -d "$scratch/root" "$carrier" > "$scratch/sasq.log" 2>&1
  rc=$?
  set -e
  end=$(date -u +%FT%TZ); end_ms=$(date +%s%3N); dur=$((end_ms - start_ms))

  counts=$(python3 -I - "$scratch/root" "$outdir/oracle-check.tsv" "$outdir/oracle-symlinks-check.tsv" <<'PY'
import hashlib, json, os, posixpath, sys

root, files_out, links_out = sys.argv[1:4]
files, links, dangling = [], [], 0


def classify(rel, target):
    """Resolve a link target against the image root (root == `/`).

    An absolute target escapes: it addresses the host root, not the image root
    (same call as R39-C1's symlink rule and the round-39 counter's resolve_kind).
    """
    if target.startswith('/'):
        return 'escaping', target
    resolved = posixpath.normpath(posixpath.join(posixpath.dirname(rel), target))
    if resolved in ('', '.'):
        return 'in-tree', resolved
    inside = not (resolved == '..' or resolved.startswith('../'))
    return ('in-tree' if inside else 'escaping'), resolved


for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
    # A symlink to a directory is reported in dirnames and is not descended
    # (followlinks=False); a symlink to a file is reported in filenames.
    for name in dirnames + filenames:
        p = os.path.join(dirpath, name)
        rel = os.path.relpath(p, root).replace(os.sep, '/')
        if os.path.islink(p):
            target = os.readlink(p)
            kind, resolved = classify(rel, target)
            if kind == 'in-tree' and not os.path.exists(os.path.join(root, resolved)):
                dangling += 1
            links.append((rel, target, kind))
        elif os.path.isfile(p):
            h = hashlib.sha256()
            with open(p, 'rb') as fh:
                for chunk in iter(lambda: fh.read(1 << 20), b''):
                    h.update(chunk)
            files.append((rel, h.hexdigest(), os.path.getsize(p)))

files.sort(key=lambda r: r[0].encode())
links.sort(key=lambda r: r[0].encode())
with open(files_out, 'w', encoding='utf-8', newline='\n') as fh:
    for rel, sha, size in files:
        fh.write(f'{rel}\t{sha}\t{size}\n')
with open(links_out, 'w', encoding='utf-8', newline='\n') as fh:
    for rel, target, kind in links:
        fh.write(f'{rel}\t{target}\t{kind}\n')
print(json.dumps({
    'regular_files': len(files),
    'symlinks': len(links),
    'symlinks_in_tree': sum(1 for r in links if r[2] == 'in-tree'),
    'symlinks_escaping': sum(1 for r in links if r[2] == 'escaping'),
    'dangling_in_tree': dangling,
}))
PY
  )

  jq -n \
    --arg schema kaidoku-r39-c1-run-v1 \
    --arg mode oracle \
    --arg claim R39-C1 \
    --arg carrier "$carrier" --arg carrier_sha "$carrier_sha" --argjson carrier_size "$carrier_size" \
    --arg outdir "$outdir" \
    --argjson offset "$offset" \
    --arg start "$start" --arg end "$end" --argjson duration_ms "$dur" --argjson exit "$rc" \
    --arg sq "$sq" --arg sq_sha "$sq_sha" --arg sq_ver "$sq_ver" --arg sq_line "$sq_line" \
    --arg scratch_root "$scratch_root" \
    --argjson counts "$counts" \
    --arg files_sha "$(sha256sum "$outdir/oracle-check.tsv" | cut -d' ' -f1)" \
    --arg links_sha "$(sha256sum "$outdir/oracle-symlinks-check.tsv" | cut -d' ' -f1)" \
    --arg log "$(sed -n '1,20p' "$scratch/sasq.log" | cut -c1-400)" \
    --arg argv "$PROG oracle $carrier $outdir" \
    '{
      schema: $schema, mode: $mode, claim: $claim, argv: $argv,
      carrier: {path: $carrier, sha256: $carrier_sha, size_bytes: $carrier_size},
      outdir: $outdir,
      squashfs_offset: $offset,
      start_utc: $start, end_utc: $end, duration_ms: $duration_ms, exit: $exit,
      sasquatch_v4be: {path: $sq, sha256: $sq_sha, version: $sq_ver, version_line: $sq_line},
      extractor: "sasquatch-v4be -be (independent of REA and unblob)",
      scratch_root: $scratch_root,
      outputs: {
        oracle_check_tsv: {path: "oracle-check.tsv", sha256: $files_sha},
        oracle_symlinks_check_tsv: {path: "oracle-symlinks-check.tsv", sha256: $links_sha}
      },
      counts: $counts,
      extractor_log_head: $log
    }' > "$outdir/oracle-run.json"

  [[ $rc -eq 0 ]] || { echo "$PROG: sasquatch-v4be exited $rc (see oracle-run.json)" >&2; exit 3; }
  exit 0
fi

# ----------------------------------------------------------------- after arm
command -v npx >/dev/null || err "npx not found on PATH"
sq=$(command -v sasquatch-v4be || true)
[[ -n $sq ]] || err "sasquatch-v4be not resolvable on PATH (the after arm requires the BE extractor)"
sq=$(realpath "$sq")
sq_sha=$(sha256sum "$sq" | cut -d' ' -f1)
sq_line=$("$sq" -version 2>&1 | sed -n 1p || true)
sq_ver=$(printf '%s' "$sq_line" | sed -nE 's/.*[Vv]ersion ([0-9][0-9A-Za-z.]*).*/\1/p')
[[ -n $sq_ver ]] || sq_ver=unknown

unblob_env=${REA_UNBLOB_COMMAND:-$HOME/.local/bin/unblob}
[[ -x $unblob_env ]] || err "REA_UNBLOB_COMMAND is missing or not executable: $unblob_env"
unblob=$(realpath "$unblob_env")
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

prev_after_sha=''
[[ -f $outdir/after.json ]] && prev_after_sha=$(sha256sum "$outdir/after.json" | cut -d' ' -f1)

extract_root=$scratch/extract
argv=(npx -y "$rea_pin" extract-firmware --format json --full-output "$carrier" "$extract_root")
argv_json=$(printf '%s\n' "${argv[@]}" | jq -R . | jq -s -c .)

start=$(date -u +%FT%TZ); start_ms=$(date +%s%3N)
set +e
( cd "$scratch" && timeout 900 "${argv[@]}" ) > "$scratch/envelope.json" 2> "$scratch/rea.err"
rc=$?
set -e
end=$(date -u +%FT%TZ); end_ms=$(date +%s%3N); dur=$((end_ms - start_ms))

envelope_parseable=false
envelope_ok=false
have_data=false
if jq -e 'type == "object"' "$scratch/envelope.json" >/dev/null 2>&1; then
  envelope_parseable=true
  [[ $(jq -r '.ok == true' "$scratch/envelope.json") == true ]] && envelope_ok=true
  if [[ $envelope_ok == true ]] && jq -e '(.data | type) == "object"' "$scratch/envelope.json" >/dev/null 2>&1; then
    have_data=true
  fi
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
  --arg schema kaidoku-r39-c1-run-v1 \
  --arg mode after \
  --arg claim R39-C1 \
  --arg carrier "$carrier" --arg carrier_sha "$carrier_sha" --argjson carrier_size "$carrier_size" \
  --arg outdir "$outdir" --arg extract_root "$extract_root" --arg cwd "$scratch" \
  --argjson prov_segment "$prov_segment_ok" \
  --argjson argv "$argv_json" \
  --arg argv_shell "REA_UNBLOB_COMMAND=$unblob ${argv[*]}" \
  --arg start "$start" --arg end "$end" --argjson duration_ms "$dur" --argjson exit "$rc" \
  --arg rea_pin "$rea_pin" --arg rea_ver "$rea_ver" --arg rea_root "$rea_root" \
  --arg unblob_env "$unblob_env" --arg unblob "$unblob" --arg unblob_sha "$unblob_sha" --arg unblob_ver "$unblob_ver" \
  --arg sq "$sq" --arg sq_sha "$sq_sha" --arg sq_ver "$sq_ver" --arg sq_line "$sq_line" \
  --arg path "$PATH" \
  --argjson env_parseable "$envelope_parseable" --argjson env_ok "$envelope_ok" \
  --arg env_sha "$(sha256sum "$scratch/envelope.json" | cut -d' ' -f1)" \
  --argjson env_bytes "$(stat -c%s "$scratch/envelope.json")" \
  --argjson have_data "$have_data" --argjson receipt_written "$receipt_written" \
  --argjson receipt "$receipt" --argjson summary "$summary" \
  --arg prev_after "$prev_after_sha" \
  --arg stderr_head "$stderr_head" \
  '{
    schema: $schema, mode: $mode, claim: $claim,
    carrier: {path: $carrier, sha256: $carrier_sha, size_bytes: $carrier_size},
    outdir: $outdir,
    argv: $argv, argv_shell: $argv_shell, cwd: $cwd,
    run_provenance_segment_ok: $prov_segment,
    extraction_root: $extract_root,
    start_utc: $start, end_utc: $end, duration_ms: $duration_ms, exit: $exit,
    rea: {pin: $rea_pin, version: $rea_ver, package_root: $rea_root},
    unblob: {env_value: $unblob_env, command_env: $unblob, sha256: $unblob_sha, version: $unblob_ver},
    sasquatch_v4be: {path: $sq, sha256: $sq_sha, version: $sq_ver, version_line: $sq_line},
    child_path: $path,
    envelope: {parseable: $env_parseable, ok: $env_ok, sha256: $env_sha, bytes: $env_bytes},
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
