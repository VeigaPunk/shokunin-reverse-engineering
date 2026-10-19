import sys, json, subprocess
sys.path.insert(0, '/var/tmp/rv1')
import keccak_ref as K

PREFIX = sys.argv[1]
# battery: real signatures + rate-boundary lengths + empty
sigs = ["transfer(address,uint256)", "balanceOf(address)", "approve(address,uint256)",
        "totalSupply()", "transferFrom(address,address,uint256)", "deposit()", "get()",
        "set(uint256)", "withdraw(uint256)", "", "abc", "x"*135, "y"*136, "z"*137,
        "w"*271, "v"*272, "u"*273]
node_js = """
const sha3 = require(process.argv[1]);
const inps = JSON.parse(process.argv[2]);
console.log(JSON.stringify(inps.map(s => sha3.keccak256(s))));
"""
out = subprocess.run(['node','-e',node_js, f"{PREFIX}/node_modules/js-sha3", json.dumps(sigs)],
                     capture_output=True, text=True, check=True).stdout.strip()
js = json.loads(out)
print("=== RV-1 from-spec keccak-256  vs  js-sha3@0.8.0 (EX-03's likely path) ===")
allok = True
for s, want in zip(sigs, js):
    got = K.keccak_256(s.encode()).hex()
    ok = got == want
    allok &= ok
    label = s if len(s) <= 42 else f"<{len(s)} bytes>"
    print(f"{'OK  ' if ok else 'FAIL'} {label:<42} {got[:16]}... {'==' if ok else '!='} {want[:16]}...")
print("XCHECK_ALL_MATCH:", allok, f"({len(sigs)} inputs)")
sys.exit(0 if allok else 1)
