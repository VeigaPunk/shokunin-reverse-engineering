#!/usr/bin/env bash
set -euo pipefail
root=$(git rev-parse --show-toplevel)
seat="$root/.ufo/waves/arc3-loop1-round10/claims/c1/EX-3"
scratch=$(mktemp -d /var/tmp/kaidoku-ex3-r10.XXXXXX)
mkdir -p "$scratch/tmp"
export TMPDIR="$scratch/tmp"
compiler="$root/.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper"
source="$seat/evidence/K8.vy"
printf 'scratch=%s\n' "$scratch"
printf 'source_sha256='
sha256sum "$source"
printf 'compiler_sha256='
sha256sum "$compiler"
printf 'compiler_version='
"$compiler" --version
cp "$source" "$scratch/K8.vy"
cd "$scratch"
for fork in paris cancun prague; do
  for pass in 1 2; do
    "$compiler" --evm-version "$fork" -f bytecode_runtime K8.vy > "$fork.runtime.$pass.hex"
  done
  cmp -s "$fork.runtime.1.hex" "$fork.runtime.2.hex"
  printf '%s_determinism=PASS\n' "$fork"
  "$compiler" --evm-version "$fork" -f abi K8.vy > "$fork.abi.json"
  "$compiler" --evm-version "$fork" -f method_identifiers K8.vy > "$fork.method-identifiers.json"
  "$compiler" --evm-version "$fork" -f opcodes_runtime K8.vy > "$fork.opcodes.txt"
  "$compiler" --evm-version "$fork" -f settings K8.vy > "$fork.settings.json"
  npx -y rea-agents@6.7.0 inspect-evm-interface "$scratch/$fork.runtime.1.hex" hex --format json > "$fork.probe.json" 2> "$fork.probe.stderr"
done
python3 - "$scratch" <<'PY'
import collections, json, pathlib, sys
p = pathlib.Path(sys.argv[1])
for fork in ('paris', 'cancun', 'prague'):
    env = json.loads((p / f'{fork}.probe.json').read_text())
    compiled = json.loads((p / f'{fork}.method-identifiers.json').read_text())
    abi = json.loads((p / f'{fork}.abi.json').read_text())
    opcodes = (p / f'{fork}.opcodes.txt').read_text().split()
    expected = {v.lower().removeprefix('0x') for v in compiled.values()}
    result = {x['selector'].lower().removeprefix('0x') for x in env['normalized_result']['functions']}
    bytecode = env['normalized_result']['bytecode']
    if len(expected) != 8 or len(result) != 8 or expected != result:
        raise SystemExit(f'{fork}: selector reconciliation failed: expected={sorted(expected)} result={sorted(result)}')
    if sum(x.get('type') == 'function' for x in abi) != 8:
        raise SystemExit(f'{fork}: ABI function count mismatch')
    if {x['dispatch'] for x in env['normalized_result']['functions']} != {'abi'}:
        raise SystemExit(f'{fork}: unexpected dispatch class')
    push4_positions = [i for i, token in enumerate(opcodes) if token == 'PUSH4']
    selector_legs = sum(
        len(opcodes[i:i+7]) == 7 and opcodes[i+2:i+4] == ['DUP2', 'XOR']
        and opcodes[i+4] == 'PUSH2' and opcodes[i+6] == 'JUMPI'
        for i in push4_positions
    )
    if len(push4_positions) != 8 or selector_legs != 8:
        raise SystemExit(f'{fork}: dispatcher census mismatch: PUSH4={len(push4_positions)} legs={selector_legs}')
    counts = collections.Counter(zip(opcodes, opcodes[1:]))
    print(f"{fork}: settings={json.loads((p / f'{fork}.settings.json').read_text())}; ABI-functions=8; compiled-ids=8; REA-functions=8; selectors=8/8; missing=[]; extra=[]; dispatch=abi x8; runtime-bytes={bytecode['bytes']}; decoded-sha256={bytecode['sha256']}; artifact-sha256={env['subject']['digest']['sha256']}; PUSH4={len(push4_positions)}; selector-legs={selector_legs}; MOD={opcodes.count('MOD')}; CODECOPY={opcodes.count('CODECOPY')}; PUSH0={opcodes.count('PUSH0')}; PUSH1_00={counts[('PUSH1', '0x00')]}; provider={env['provider']['id']}@{env['provider']['version']}; evidence_id={env['evidence_id']}")
    if env['normalized_result'].get('runtime_execution') != 'not-performed':
        raise SystemExit(f'{fork}: unexpected runtime-execution status')
for a, b in (('paris', 'prague'), ('cancun', 'prague'), ('paris', 'cancun')):
    runtime_equal = (p / f'{a}.runtime.1.hex').read_bytes() == (p / f'{b}.runtime.1.hex').read_bytes()
    abi_equal = (p / f'{a}.abi.json').read_bytes() == (p / f'{b}.abi.json').read_bytes()
    ids_equal = (p / f'{a}.method-identifiers.json').read_bytes() == (p / f'{b}.method-identifiers.json').read_bytes()
    print(f'{a}_vs_{b}: runtime_identical={runtime_equal}; ABI_identical={abi_equal}; method_identifiers_identical={ids_equal}')
if (p / 'paris.runtime.1.hex').read_bytes() == (p / 'prague.runtime.1.hex').read_bytes():
    raise SystemExit('Paris and Prague runtime bytes unexpectedly identical')
if (p / 'cancun.runtime.1.hex').read_bytes() != (p / 'prague.runtime.1.hex').read_bytes():
    raise SystemExit('Cancun and Prague runtime bytes differ')
for fork in ('paris', 'cancun', 'prague'):
    if (p / f'{fork}.abi.json').read_bytes() != (p / 'prague.abi.json').read_bytes():
        raise SystemExit(f'{fork}: ABI differs across forks')
    if (p / f'{fork}.method-identifiers.json').read_bytes() != (p / 'prague.method-identifiers.json').read_bytes():
        raise SystemExit(f'{fork}: method identifiers differ across forks')
PY
printf 'scratch=%s\n' "$scratch"
