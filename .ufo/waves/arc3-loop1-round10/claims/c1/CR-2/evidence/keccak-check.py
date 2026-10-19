import json
import pathlib
import sys
from Crypto.Hash import keccak

compile_dir = pathlib.Path(sys.argv[1])

def selector(signature):
    digest = keccak.new(digest_bits=256)
    digest.update(signature.encode())
    return digest.hexdigest()[:8]

assert selector("transfer(address,uint256)") == "a9059cbb"
print("KECCAK_KNOWN_VECTOR=transfer(address,uint256):a9059cbb PASS")
results = {}
for target in ("prague", "london"):
    abi = json.loads((compile_dir / f"{target}.abi.json").read_text())
    methods = json.loads((compile_dir / f"{target}.method_identifiers.json").read_text())
    functions = [row for row in abi if row.get("type") == "function"]
    signatures = sorted(f"{row['name']}({','.join(arg['type'] for arg in row.get('inputs', []))})" for row in functions)
    selectors = {selector(signature) for signature in signatures}
    method_selectors = {value.lower().removeprefix("0x") for value in methods.values()}
    assert len(functions) == len(methods) == len(signatures) == len(selectors) == 8
    assert selectors == method_selectors
    results[target] = selectors
    print(f"{target.upper()}_SIGNATURES={','.join(signatures)}")
    print(f"{target.upper()}_KECCAK_SELECTORS={','.join(sorted(selectors))}")
    print(f"{target.upper()}_ABI_METHOD_IDS_MATCH=True")
assert results["prague"] == results["london"]
print("CROSS_TARGET_KECCAK_SELECTORS_IDENTICAL=True")
