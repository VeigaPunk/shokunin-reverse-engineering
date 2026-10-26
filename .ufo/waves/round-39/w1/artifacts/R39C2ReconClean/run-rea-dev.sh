#!/bin/sh
# R39C2ReconClean — the exact after-arm REA invocation used for every development carrier.
# sasquatch AND sasquatch-v4be reachable on the child PATH (~/.local/bin is on it); unblob
# pinned by absolute path so the provider cannot drift.
# Usage: sh run-rea-dev.sh <SCRATCH>   (carriers + trees must already exist under <SCRATCH>)
set -eu
S=${1:?scratch dir}
cd "$S"                     # unblob writes unblob.log into its cwd
mkdir -p env out
for c in a1 a2 b1 b2 c1 c2 d1 d2 e1 f1 f2 be-body-damaged be-meta-damaged; do
  REA_UNBLOB_COMMAND="$HOME/.local/bin/unblob" \
    npx -y rea-agents@6.5.0 extract-firmware --format json --full-output \
    "$S/carriers/$c.sqsh" "$S/out/$c" > "$S/env/$c.json" 2> "$S/env/$c.err"
  echo "$c exit=$?"
done
