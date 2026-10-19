#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
EVID="$ROOT/.ufo/waves/arc3-loop1-round10/claims/c1/EX-1/evidence/vyper"
SRC="$EVID/source/K8.vy"
VYPER="$ROOT/.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper"
RUN="/var/tmp/kaidoku-ex1-vyper-r10"

mkdir -p "$RUN/tmp" "$RUN/out" "$EVID/compile"
for target in cancun paris; do
  for pass in 1 2; do
    env TMPDIR="$RUN/tmp" "$VYPER" --evm-version "$target" -O gas --no-bytecode-metadata -f bytecode_runtime "$SRC" > "$RUN/out/$target.no-metadata.$pass.runtime.hex"
  done
  cmp "$RUN/out/$target.no-metadata.1.runtime.hex" "$RUN/out/$target.no-metadata.2.runtime.hex"
  cp "$RUN/out/$target.no-metadata.1.runtime.hex" "$EVID/compile/$target.no-metadata.runtime.hex"
done
printf 'exit=0; both targets repeated byte-identically\n' > "$EVID/no-metadata-run-status.txt"
