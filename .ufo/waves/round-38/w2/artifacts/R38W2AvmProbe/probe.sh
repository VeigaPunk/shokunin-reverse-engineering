#!/bin/sh
# Reproduce the R38W2AvmProbe frontier probe (round 38, attempt 2, wave 2).
# Assumes: unblob 26.6.4 at ~/.local/bin/unblob (uv tool), rea-agents 6.5.0 via npx,
#          sasquatch-v4be 4.5.1 at ~/.local/bin/sasquatch-v4be,
#          lane root = kaidoku-shokunin checkout.
# Scratch only: run inside a throwaway dir; nothing here writes to the lane.
set -eu
LANE=${LANE:-/home/vgpnk/Projects/shokunin/kaidoku-shokunin}
S=${S:-$(mktemp -d)}
mkdir -p "$S/input"
cp "$LANE/corpus/evidence/round-37/c1/K1/carrier.sqsh" "$S/input/k1-orig.sqsh"
python3 "$(dirname "$0")/make-avm-copy.py" "$S/input/k1-orig.sqsh" "$S/input/k1-avm.sqsh"

# sasquatch matrix (subshell: a failing sasquatch-v4be can take the caller shell down with it)
for mode in noflag beflag; do
  for img in k1-orig k1-avm; do
    flag=""; [ "$mode" = beflag ] && flag=-be
    out="$S/sq-$img-$mode"; mkdir -p "$out"
    ( ~/.local/bin/sasquatch-v4be $flag -no-exit-code -f -d "$out" "$S/input/$img.sqsh" \
        > "$out/stdout.txt" 2> "$out/stderr.txt" ) || true
    echo "$img $mode files=$(find "$out" -type f ! -name 'stdout.txt' ! -name 'stderr.txt' | wc -l)"
  done
done

# unblob direct (verbose log shows the exact extractor argv)
PATH="$HOME/.local/bin:$PATH" ~/.local/bin/unblob -v -e "$S/ub-avm" "$S/input/k1-avm.sqsh" > "$S/ub-avm.log" 2>&1
grep -E "Running extract command|Extract command failed" "$S/ub-avm.log" || true

# REA envelope (OUTDIR must not exist)
export REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob
npx -y rea-agents@6.5.0 extract-firmware "$S/input/k1-avm.sqsh" "$S/rea-avm" --format json --full-output
echo "scratch: $S"
