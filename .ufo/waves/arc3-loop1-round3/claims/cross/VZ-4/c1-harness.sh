#!/bin/bash
# VZ-4 C1 cross-check — independent optimizer-enabled carrier, compiled with the
# receipted wave solc prefix (reuse verified: receipt pins tarball sha256
# 0e1a1ab6…575a51; prefix tree byte-identical to the ambient install,
# soljson.js 221d7a66…).
#
# Shape deliberately outside r1's probed class: payable receive() + payable
# fallback() + mixed mutability + a library-bound call — compiled via
# standard-JSON with optimizer enabled, runs=200. Planted selector set is
# derived from the compiled ABI BEFORE any probe run.
set -u
PREFIX=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix
SOLC="$PREFIX/node_modules/.bin/solcjs"
W=/var/tmp/vz4r3/c1
OUT="${1:-/var/tmp/vz4r3/c1-results.txt}"
export TMPDIR=$W/tmp; mkdir -p "$TMPDIR" "$W/src" "$W/out" "$W/scr"
: > "$OUT"
say() { printf '%s\n' "$*" | tee -a "$OUT"; }

cat > "$W/src/VzPayable.sol" <<'SOL'
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

library MathLib {
    function add(uint256 a, uint256 b) internal pure returns (uint256) { return a + b; }
}

contract VzPayable {
    address public owner;
    mapping(address => uint256) private balances;
    uint256 public totalDeposited;
    event Deposited(address indexed who, uint256 amount);

    constructor() payable { owner = msg.sender; }

    function balanceOf(address who) external view returns (uint256) { return balances[who]; }
    function deposit() external payable { balances[msg.sender] = MathLib.add(balances[msg.sender], msg.value); totalDeposited += msg.value; emit Deposited(msg.sender, msg.value); }
    function setLimit(uint256 x) public returns (uint256) { return x; }
    function getLimit() public view returns (uint256) { return totalDeposited; }
    function tag() external pure returns (bytes32) { return keccak256("vz4"); }
    function withdraw(uint256 amount) external { require(balances[msg.sender] >= amount, "insufficient"); balances[msg.sender] -= amount; payable(msg.sender).transfer(amount); }
    function sweep() external { require(msg.sender == owner, "owner only"); payable(owner).transfer(address(this).balance); }

    receive() external payable { totalDeposited += msg.value; }
    fallback() external payable { totalDeposited += 1; }
}
SOL

say "== VZ-4 C1 optimizer-shape cross-check =="
say "solcjs=$SOLC"
say "solcjs version: $("$SOLC" --version 2>&1)"
say "soljson.js sha256=$(sha256sum "$(dirname "$(readlink -f "$SOLC")")/soljson.js" | cut -d' ' -f1)"
say "utc=$(date -u +%FT%TZ)"

# standard-JSON input, optimizer on runs=200
python3 - "$W/src/VzPayable.sol" "$W/in.json" <<'PY'
import json, sys
src = open(sys.argv[1]).read()
inp = {"language": "Solidity", "sources": {"VzPayable.sol": {"content": src}},
       "settings": {"optimizer": {"enabled": True, "runs": 200},
                    "outputSelection": {"*": {"*": ["abi", "evm.deployedBytecode.object", "evm.bytecode.object"]}}}}
json.dump(inp, open(sys.argv[2], "w"))
PY
say "-- compile (standard-json, optimizer enabled, runs=200) --"
"$SOLC" --standard-json < "$W/in.json" > "$W/stdout.json" 2>"$W/stdout.err"
say "compile exit=$? stderr=$(head -c 200 "$W/stdout.err")"

python3 - "$W/stdout.json" "$W" <<'PY'
import json, sys
raw = open(sys.argv[1]).read()
out = json.loads(raw[raw.index('{'):]); w = sys.argv[2]
c = out['contracts']['VzPayable.sol']['VzPayable']
rt = c['evm']['deployedBytecode']['object']
open(w + '/VzPayable.runtime.hex', 'w').write(rt)
json.dump(c['abi'], open(w + '/VzPayable.abi.json', 'w'), indent=1)
print('runtime hex bytes:', len(rt))
PY

say "-- planted selectors (keccak256(sig)[0:4] over the compiled ABI) --"
node - "$W/VzPayable.abi.json" "$PREFIX/node_modules" > "$W/planted-K.txt" <<'JS'
const fs = require('fs');
const [abiPath, modDir] = process.argv.slice(2);
const { keccak256 } = require(modDir + '/js-sha3');
const abi = JSON.parse(fs.readFileSync(abiPath, 'utf8'));
const rows = [];
for (const it of abi) {
  if (it.type !== 'function') continue;
  const sig = `${it.name}(${(it.inputs||[]).map(i=>i.type).join(',')})`;
  rows.push(keccak256(sig).slice(0, 8) + ': ' + sig);
}
rows.sort();
console.log(rows.join('\n'));
JS
cat "$W/planted-K.txt" | tee -a "$OUT"
K=$(grep -c . "$W/planted-K.txt"); say "planted K=$K"
say "runtime hex carrier: bytes=$(wc -c < "$W/VzPayable.runtime.hex") sha256=$(sha256sum "$W/VzPayable.runtime.hex" | cut -d' ' -f1)"

for PIN in "${PINS:-6.4.0}"; do
  say "-- probe rea-agents@$PIN (hex carrier) --"
  if timeout 170 npx -y "rea-agents@$PIN" inspect-evm-interface "$W/VzPayable.runtime.hex" hex \
      --format json > "$W/probe-$PIN.json" 2>"$W/probe-$PIN.err"; then
    python3 - "$W/probe-$PIN.json" "$W/planted-K.txt" "$PIN" <<'PY' | tee -a "$OUT"
import json, sys
env = json.load(open(sys.argv[1]))
planted = {l.split(':')[0].strip() for l in open(sys.argv[2]) if ':' in l}
nr = env.get('normalized_result') or {}
fns = nr.get('functions') or []
got = set()
for f in fns:
    s = f.get('selector') or f.get('signature') or ''
    if s.startswith('0x'): s = s[2:]
    got.add(s[:8])
k = len(planted)
print(f"pin=rea-agents@{sys.argv[3]} evidence_id={env.get('evidence_id')}")
print(f"functions_reported={len(fns)} planted_K={k}")
print(f"missing={sorted(planted-got)} extra={sorted(got-planted)}")
print(f"K/K={'YES' if planted==got else 'NO'}")
print(f"dispatch_kinds={sorted({f.get('dispatch') for f in fns})}")
print(f"mutability={sorted({f.get('inferred_state_mutability') for f in fns})}")
print(f"bytecode_sha={((env.get('normalized_result') or {}).get('bytecode') or {}).get('sha256')}")
PY
  else
    say "PROBE FAILED pin=$PIN (err tail follows)"; tail -5 "$W/probe-$PIN.err" | tee -a "$OUT"
  fi
done
say "== end $(date -u +%FT%TZ) =="