#!/usr/bin/env bash
# R38-C1 harness (claim data generation; honours $HYAKU_SCRATCH).
#
#   c1-run.sh before CARRIER OUTDIR [SCRATCH]
#     REA extract-firmware (rea-agents 6.5.0, unblob 26.6.4) with
#     sasquatch-v4be unavailable: strip $HOME/.local/bin from PATH for the
#     child while keeping REA_UNBLOB_COMMAND absolute (it runs from its own
#     venv). Expected envelope: chunks handler squashfs_v4_be with
#     missing-extractor-dependency [sasquatch-v4be] and 0 published files.
#
#   c1-run.sh after CARRIER OUTDIR [SCRATCH]
#     Same run with sasquatch-v4be available (default PATH). Expected: every
#     oracle file published, no gaps.
#
#   c1-run.sh oracle CARRIER OUTDIR [SCRATCH]
#     Extract with ~/.local/bin/sasquatch-v4be -be into OUTDIR (cross-tool
#     oracle check; unsquashfs 4.7.5 refuses BE v4), printing a sha256 list
#     of every regular file found.
#
# OUTDIR must not exist; REA creates it. Scratch for npx caches etc. lives
# under $SCRATCH (default $HYAKU_SCRATCH/kaidoku-r38/<seat>/); /tmp is only
# for files <50 MB.
set -euo pipefail
MODE="${1:?mode}"; CARRIER="${2:?carrier}"; OUT="${3:?outdir}"
S="${4:-${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kaidoku-r38/$(basename "$0" .sh)-$$}"
mkdir -p "$S"
trap 'rm -rf -- "$S"' EXIT
export TMPDIR="$S"
case "$MODE" in
  before|after)
    : "${REA_UNBLOB_COMMAND:?set REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob}"
    rm -rf "$OUT"          # REA refuses an existing extraction root; it creates $OUT itself
    if [ "$MODE" = before ]; then
      STRIP="$(printf '%s' "$PATH" | tr ':' '\n' | grep -v -F "$HOME/.local/bin" | paste -sd:)"
      PATH="$STRIP" npx -y rea-agents@6.5.0 extract-firmware --format json "$CARRIER" "$OUT"
    else
      npx -y rea-agents@6.5.0 extract-firmware --format json "$CARRIER" "$OUT"
    fi
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
  *) echo "usage: $0 {before|after|oracle} CARRIER OUTDIR [SCRATCH]" >&2; exit 2 ;;
esac
