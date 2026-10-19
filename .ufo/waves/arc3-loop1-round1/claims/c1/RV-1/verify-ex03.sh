#!/usr/bin/env bash
# RV-1 primary-target verification — EX-03 token.sol (arc3-loop1-round1, chain c1)
#
# Independently recomputes the planted selector set from EX-03/token.sol with
# RV-1's own from-spec Keccak-256 and verifies every stated EX-03 claim that is
# checkable without EX-03's scratch compile: artifact hashes, selector set,
# canonicalization guardrails, event topic0 hashes, and a full independent
# recompile of token.sol with the authorized solc 0.8.37.
#
# usage: verify-ex03.sh            (run from claims/c1/)
set -u
C1="$(cd "$(dirname "$0")/.." && pwd)"
RV1="$C1/RV-1"
EX03="$C1/EX-03"
PREFIX="$C1/../../tools/solc-prefix"
SOLC="$PREFIX/node_modules/solc"
W="$(mktemp -d -p /var/tmp rv1-ex03.XXXXXX)" || exit 2
export TMPDIR="$W"
trap 'rm -rf "$W"' EXIT

echo "=== RV-1 primary-target verification: EX-03 token.sol ==="
echo "date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo

echo "-- [1] EX-03 stated artifact hashes --"
sha256sum "$EX03/token.sol" "$EX03/keccak256.py"
stat -c '   %n  %s bytes' "$EX03/token.sol" "$EX03/keccak256.py"
echo "   claimed: token.sol 497d70f2ed055b56a0b2e2bf826f704f11ee8a1ba4ec664dae0ddb6a0ac76a6f (2417 B)"
echo "            keccak256.py 7a58534b5cdd7798b11bb2931f7ce6afdb8ba073ead1d76e5b0443b5da6f9427 (3812 B)"
echo

echo "-- [2] RV-1 recompute from source (from-spec keccak) --"
python3 "$RV1/recompute.py" sol "$EX03/token.sol"
echo

echo "-- [3] selector-set comparison (8-hex-char tokens only) --"
python3 - "$EX03/planted-selectors.txt" "$RV1/ex03-rv1-recompute.txt" <<'PY'
import sys
def load8(p):
    s = set()
    for l in open(p):
        l = l.strip()
        if not l or l.startswith('#') or l.startswith('K='):
            continue
        t = l.split()[0].lower().removeprefix('0x')
        if len(t) == 8:
            s.add(t)
    return s
a, b = load8(sys.argv[1]), load8(sys.argv[2])
print(f"   EX-03 planted selectors: {len(a)}   RV-1 recomputed: {len(b)}")
print(f"   missing_vs_planted={sorted(a - b)}")
print(f"   extra_vs_planted={sorted(b - a)}")
print("   VERDICT:", "MATCH 9/9" if a == b else "MISMATCH")
sys.exit(0 if a == b else 1)
PY
echo

echo "-- [4] EX-03 canonicalization guardrails, RV-1 recompute --"
python3 - <<'PY'
import sys, hashlib
sys.path.insert(0, __import__('os').environ['RV1DIR'])
import keccak_ref as K
for sig, want in [("transfer(address,uint256)", "a9059cbb"), ("transfer(address, uint256)", "9d61d234"),
                  ("transfer(address,uint)", "6cb927d8"), ("TRANSFER(address,uint256)", "d51e217e")]:
    got = K.selector(sig)
    print(f"   {'OK  ' if got == want else 'FAIL'} {sig!r:<32} rv1={got} claimed={want}")
h = hashlib.sha3_256(b"transfer(address,uint256)").hexdigest()[:8]
print(f"   {'OK  ' if h == '4b40e901' else 'FAIL'} NIST sha3-256('transfer(address,uint256)')[:4] = {h} claimed=4b40e901")
PY
echo

echo "-- [5] event topic0 full hashes, RV-1 recompute --"
python3 - <<'PY'
import sys, os
sys.path.insert(0, os.environ['RV1DIR'])
import keccak_ref as K
for sig, want in [("Transfer(address,address,uint256)", "ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"),
                  ("Approval(address,address,uint256)", "8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925")]:
    got = K.keccak_256(sig.encode()).hex()
    print(f"   {'OK  ' if got == want else 'FAIL'} {sig:<38} {got}")
PY
echo

echo "-- [6] independent recompile of token.sol with authorized solc --"
cp "$EX03/token.sol" "$W/token.sol"
( cd "$W" && node -e "
const solc=require('$SOLC'),fs=require('fs');
const i={language:'Solidity',sources:{'token.sol':{content:fs.readFileSync('token.sol','utf8')}},settings:{outputSelection:{'*':{'*':['abi','evm.bytecode.object','evm.deployedBytecode.object']}}}};
const o=JSON.parse(solc.compile(JSON.stringify(i)));
if(o.errors) for(const e of o.errors) if(e.severity==='error'){console.error('SOLC ERROR:',e.formattedMessage);process.exit(1);}
const c=o.contracts['token.sol'].KdkToken;
fs.writeFileSync('runtime.hex',c.evm.deployedBytecode.object);
fs.writeFileSync('abi.json',JSON.stringify(c.abi));
console.log('   solc:',solc.version());
" )
python3 - "$W" "$EX03/planted-selectors.txt" <<'PY'
import sys, json, hashlib, os
W, planted_path = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.environ['RV1DIR'])
import keccak_ref as K
code = bytes.fromhex(open(f"{W}/runtime.hex").read().strip())
chk = lambda got, want, lbl: print(f"   {'MATCH   ' if got == want else 'MISMATCH'} {lbl}: {got}" + ("" if got == want else f"  (claimed {want})"))
chk(len(code), 3457, "runtime bytes")
chk(hashlib.sha256(code).hexdigest(), "46ccaae1554a9b887e6c715622a9b8f9c17faee9f23d905b41fd7b344f1d395e", "sha256(runtime)")
chk(K.keccak_256(code).hex(), "42e54374d8c183a19af27c29d498c0cea90e75f7d358e87ef98f86f540dcfd89", "keccak256 code hash (RV-1 keccak)")
sels = []; i = 0
while i < len(code):
    op = code[i]
    if 0x60 <= op <= 0x7f:
        ln = op - 0x5f
        if op == 0x63:
            sels.append(code[i+1:i+5].hex())
        i += 1 + ln
    else:
        i += 1
planted = set()
for l in open(planted_path):
    l = l.strip()
    if not l or l.startswith('#') or l.startswith('K='):
        continue
    t = l.split()[0].lower().removeprefix('0x')
    if len(t) == 8:
        planted.add(t)
inv = set(sels)
print(f"\n   PUSH4 constants: {len(sels)} occurrences, {len(inv)} distinct")
print(f"   missing_vs_planted={sorted(planted - inv)}")
print(f"   EXTRA PUSH4 not planted={sorted(inv - planted)}")
print("   VERDICT:", "9/9 with ZERO extras" if inv == planted else "MISMATCH")
abi = json.load(open(f"{W}/abi.json"))
sigs = sorted({e['name'] + '(' + ','.join(x['type'] for x in e.get('inputs', [])) + ')' for e in abi if e.get('type') == 'function'})
abisel = set(K.selector(s) for s in sigs)
print(f"   ABI-derived {len(sigs)} functions -> {sorted(abisel)}")
print("   ABI vs planted:", "MATCH" if abisel == planted else "MISMATCH")
PY
echo
echo "=== END RV-1 primary-target verification ==="
