#!/usr/bin/env bash
# R38-C1 harness (claim data generation; honours $HYAKU_SCRATCH).
#
#   c1-run.sh after CARRIER OUTDIR [SCRATCH]
#     Run REA extract-firmware (rea-agents 6.5.0, unblob 26.6.4) on CARRIER
#     with stock unblob (no external extractor needed for standard BE v4),
#     printing the envelope JSON to stdout and keeping the output tree in
#     OUTDIR. Uses REA_UNBLOB_COMMAND when set; never runs sasquatch.
#
#   c1-run.sh oracle CARRIER OUTDIR [SCRATCH]
#     Extract with ~/.local/bin/sasquatch-v4be -be into OUTDIR (cross-tool
#     oracle check; unsquashfs 4.7.5 refuses BE v4), printing a sha256 list
#     of every regular file found.
#
# Scratch for npx caches etc. lives under $SCRATCH (default
# $HYAKU_SCRATCH/kaidoku-r38/<seat>/); /tmp is only for files <50 MB.
set -euo pipefail
MODE="${1:?mode}"; CARRIER="${2:?carrier}"; OUT="${3:?outdir}"
S="${4:-${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kaidoku-r38/$(basename "$0" .sh)-$$}"
mkdir -p "$S"
trap 'rm -rf -- "$S"' EXIT
export TMPDIR="$S"
case "$MODE" in
  after)
    : "${REA_UNBLOB_COMMAND:?set REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob}"
    mkdir -p "$OUT"
    npx -y rea-agents@6.5.0 extract-firmware --format json "$CARRIER" "$OUT"
    ;;
  oracle)
    rm -rf "$OUT"; mkdir -p "$OUT"
    ~/.local/bin/sasquatch-v4be -be -d "$OUT" "$CARRIER" >/dev/null 2>&1 || {
      echo "sasquatch-v4be failed" >&2; exit 1; }
    find "$OUT" -type f -print0 | sort -z | while IFS= read -r -d '' f; do
      rel=${f#"$OUT"/}; sha=$(sha256sum "$f" | cut -d' ' -f1); sz=$(stat -c%s "$f")
      printf '%s\t%s\t%s\n' "$rel" "$sha" "$sz"
    done
    ;;
  *) echo "usage: $0 {after|oracle} CARRIER OUTDIR [SCRATCH]" >&2; exit 2 ;;
esac
