#!/usr/bin/env bash
set -euo pipefail
base=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
runtime="$base/runtime/squashfs-root"
if [[ ! -x "$runtime/usr/bin/sigrok-cli" ]]; then
  printf '%s\n' 'Run tools/setup-sigrok.py first; no implicit tool acquisition.' >&2
  exit 2
fi
# The 2019 bundle contains an old libgmodule, while its missing libgio resolves
# to this host. Preload the matching host gmodule instead of mixing those ABIs.
export LD_LIBRARY_PATH="$runtime/usr/lib"
export LD_PRELOAD=/usr/lib/libgmodule-2.0.so.0
export PYTHONPATH="$runtime/usr/share/pyshared"
export SIGROKDECODE_DIR="$runtime/usr/share/libsigrokdecode/decoders"
exec "$runtime/usr/bin/sigrok-cli" "$@"
