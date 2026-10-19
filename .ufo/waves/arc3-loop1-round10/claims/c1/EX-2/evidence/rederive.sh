#!/usr/bin/env bash
set -euo pipefail
ART=$(cd "$(dirname "$0")/.." && pwd)
ROOT=$(git -C "$ART" rev-parse --show-toplevel)
SCRATCH=$(mktemp -d /var/tmp/kaidoku-ex2-r10-recheck.XXXXXX)
mkdir -p "$SCRATCH/tmp" "$SCRATCH/package" "$SCRATCH/src" "$SCRATCH/out" "$SCRATCH/out-repeat" "$SCRATCH/out-0837"
cp "$ART/evidence/ViaIrVault.sol" "$SCRATCH/src/ViaIrVault.sol"
TMPDIR="$SCRATCH/tmp" npm pack solc@0.8.28 --silent --offline --cache "$HOME/.npm" --pack-destination "$SCRATCH" > "$SCRATCH/npm-pack.stdout"
tar -xzf "$SCRATCH/solc-0.8.28.tgz" -C "$SCRATCH/package"
SOLC_0837="$ROOT/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/solc"
NODE_PATH="$ROOT/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules" node "$ART/evidence/compile.js" "$SCRATCH/package/package" "$SCRATCH/src/ViaIrVault.sol" "$SCRATCH/out"
NODE_PATH="$ROOT/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules" node "$ART/evidence/compile.js" "$SCRATCH/package/package" "$SCRATCH/src/ViaIrVault.sol" "$SCRATCH/out-repeat"
NODE_PATH="$ROOT/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules" node "$ART/evidence/compile.js" "$SOLC_0837" "$SCRATCH/src/ViaIrVault.sol" "$SCRATCH/out-0837"
REA=/home/vgpnk/.npm/_npx/9b9809298fe40d2c/node_modules/rea-agents/scripts/rea.mjs
for LEG in viair-opt200 std-opt200; do
  TMPDIR="$SCRATCH/tmp" node "$REA" inspect-evm-interface "$SCRATCH/out/$LEG/runtime.hex" hex --format json > "$SCRATCH/probe-028-$LEG.json" 2> "$SCRATCH/probe-028-$LEG.stderr"
done
TMPDIR="$SCRATCH/tmp" node "$REA" inspect-evm-interface "$SCRATCH/out-0837/viair-opt200/runtime.hex" hex --format json > "$SCRATCH/probe-0837-viair-opt200.json" 2> "$SCRATCH/probe-0837-viair-opt200.stderr"
python3 - "$SCRATCH" <<'PY'
import hashlib, json, pathlib, sys
root = pathlib.Path(sys.argv[1])
checks = []
for leg in ("viair-opt200", "std-opt200"):
    for name in ("runtime.bin", "creation.bin", "abi.json", "method-identifiers.json"):
        left = (root / "out" / leg / name).read_bytes()
        right = (root / "out-repeat" / leg / name).read_bytes()
        checks.append({"leg": leg, "file": name, "equal": left == right,
                       "sha256": hashlib.sha256(left).hexdigest()})
if not all(row["equal"] for row in checks):
    raise SystemExit("repeat compilation mismatch")
print("repeat_compile_comparisons=" + json.dumps(checks, sort_keys=True, separators=(",", ":")))
PY
python3 "$ART/evidence/dispatch-census.py" "$SCRATCH"
printf 'scratch=%s\n' "$SCRATCH"
printf 'source_sha256='; sha256sum "$SCRATCH/src/ViaIrVault.sol"
printf 'solc_0_8_28_tgz_sha256='; sha256sum "$SCRATCH/solc-0.8.28.tgz"
printf 'soljson_0_8_28_sha256='; sha256sum "$SCRATCH/package/package/soljson.js"
printf 'soljson_0_8_37_sha256='; sha256sum "$SOLC_0837/soljson.js"
