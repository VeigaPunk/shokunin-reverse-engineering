#!/usr/bin/env bash
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
ART="$ROOT/.ufo/waves/arc3-loop1-round9/claims/c2/EX-8"
PREFIX="$ROOT/.ufo/waves/arc3-loop1-round1/tools/solc-prefix"
REA_ROOT="/home/vgpnk/.npm/_npx/9b9809298fe40d2c/node_modules/rea-agents"
RUN="$(mktemp -d /var/tmp/kaidoku-ex8-r9.XXXXXX)"
mkdir -p "$RUN/tmp"
{
  printf 'measurement_utc='; date -u +%Y-%m-%dT%H:%M:%SZ
  printf 'repo_head='; git rev-parse HEAD
  printf 'node='; node --version
  printf 'scratch=%s\nTMPDIR=%s\n' "$RUN" "$RUN/tmp"
  printf 'compiler_version='
  node -e "process.stdout.write(require('$PREFIX/node_modules/solc').version() + '\\n')"
  printf 'REA_package_version='
  node -e "process.stdout.write(require('$REA_ROOT/package.json').version + '\\n')"
  sha256sum "$PREFIX/node_modules/solc/soljson.js" "$REA_ROOT/package.json" "$REA_ROOT/scripts/rea.mjs" "$ART/evidence/source/ViaIrVault.no-fallback.sol" "$ART/evidence/source/ViaIrVault.fallback.sol"
} > "$ART/evidence/identity.txt"
TMPDIR="$RUN/tmp" node "$ART/evidence/compile.js" "$PREFIX" "$ART/evidence/source" "$ART/evidence/compile" | tee "$ART/evidence/compile/compile-summary.json"
for mode in no-fallback payable-fallback; do
  TMPDIR="$RUN/tmp" node "$REA_ROOT/scripts/rea.mjs" inspect-evm-interface "$ART/evidence/compile/$mode/runtime.hex" hex --format json > "$ART/evidence/probe/$mode.json" 2> "$ART/evidence/probe/$mode.stderr"
  printf '%s exit=0 json_bytes=%s stderr_bytes=%s\n' "$mode" "$(wc -c < "$ART/evidence/probe/$mode.json")" "$(wc -c < "$ART/evidence/probe/$mode.stderr")"
done | tee "$ART/evidence/probe/calls.txt"
python3 "$ART/evidence/walk.py" "$ART/evidence/compile" | tee "$ART/evidence/compile/dispatch-walk.txt"
python3 - "$ART" <<'PY' | tee "$ART/evidence/probe/verification.txt"
import hashlib, json, pathlib, sys
art = pathlib.Path(sys.argv[1])
for mode in ('no-fallback', 'payable-fallback'):
    root = art / 'evidence'
    abi = json.loads((root / 'compile' / mode / 'abi.json').read_text())
    method_ids = json.loads((root / 'compile' / mode / 'method-identifiers.json').read_text())
    probe = json.loads((root / 'probe' / f'{mode}.json').read_text())
    functions = [item for item in abi if item.get('type') == 'function']
    expected = {value.lower().removeprefix('0x') for value in method_ids.values()}
    normalized = probe['normalized_result']
    raw_functions = probe['raw_result']['functions']
    selectors = {row['selector'].lower().removeprefix('0x') for row in normalized['functions']}
    raw_selectors = {row['selector'].lower().removeprefix('0x') for row in raw_functions}
    runtime = (root / 'compile' / mode / 'runtime.bin').read_bytes()
    actual_sha = hashlib.sha256(runtime).hexdigest()
    assert len(functions) == len(method_ids) == len(normalized['functions']) == len(raw_functions) == 15
    assert expected == selectors == raw_selectors
    assert normalized['bytecode']['sha256'] == actual_sha
    print(f"{mode}: ABI_FUNCTIONS={len(functions)} METHOD_IDS={len(method_ids)} NORMALIZED={len(selectors)} RAW={len(raw_selectors)} SELECTORS_MATCH=True DECODED_SHA_MATCH={actual_sha} EVIDENCE_ID={probe.get('evidence_id')}")
    print(f"{mode}: FALLBACK_ABI={sum(item.get('type') == 'fallback' for item in abi)} RECEIVE_ABI={sum(item.get('type') == 'receive' for item in abi)} PROVIDER={probe.get('provider', {}).get('id')} VERSION={probe.get('provider', {}).get('version')}")
PY
