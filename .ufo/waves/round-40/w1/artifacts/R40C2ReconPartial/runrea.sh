#!/bin/sh
# runrea.sh NAME INPUT ENVELOPE_OUT [--stripped]
#
# One REA 6.5.0 extract-firmware run, exactly the CLI the lane freezes:
#   REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 \
#       extract-firmware --format json --full-output INPUT FRESH_OUTDIR
# Unblob writes unblob.log into its cwd and REA refuses a pre-existing outdir,
# so each run gets its own cwd under $S/run/NAME and a fresh out/ inside it.
#
# --stripped removes $HOME/.local/bin from the child PATH (sasquatch * and
# unblob unreachable by name) and keeps every command absolute.
set -eu
S=${S:-/fast/scratch/hyaku/kaidoku-r40/R40C2ReconPartial}
name=$1
input=$2
envout=$3
mode=${4:-full}
rundir=$S/run/$name
rm -rf "$rundir"
mkdir -p "$rundir"
outdir=$rundir/out
if [ "$mode" = "--stripped" ]; then
  child_path=/usr/local/bin:/usr/bin:/bin
else
  child_path=$PATH
fi
cd "$rundir"
set +e
env PATH="$child_path" REA_UNBLOB_COMMAND="$HOME/.local/bin/unblob" \
  npx -y rea-agents@6.5.0 extract-firmware --format json --full-output \
  "$input" "$outdir" > "$envout" 2> "$rundir/stderr.log"
rc=$?
set -e
printf '%s exit=%s envelope=%s bytes=%s\n' "$name" "$rc" "$envout" \
  "$(wc -c < "$envout")" >> "$S/run/status.log"
exit 0
