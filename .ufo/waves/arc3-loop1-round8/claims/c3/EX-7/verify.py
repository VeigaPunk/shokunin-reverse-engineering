import hashlib
import json
import pathlib
import sys

from Crypto.Hash import keccak

base = pathlib.Path(sys.argv[1])
out_dir = base / "out" if (base / "out").is_dir() else base / "compiler" if (base / "compiler").is_dir() else base
probe_dir = base / "probe"
methodids = json.loads((out_dir / "noopt.method_identifiers").read_text())
expected = {value.removeprefix("0x").lower() for value in methodids.values()}
abi = json.loads((out_dir / "noopt.abi").read_text())
function_signatures = [
    f"{row['name']}({','.join(item['type'] for item in row['inputs'])})"
    for row in abi if row.get("type") == "function"
]
derived = set()
for signature in function_signatures:
    digest = keccak.new(digest_bits=256)
    digest.update(signature.encode())
    derived.add(digest.hexdigest()[:8])
assert len(methodids) == len(expected) == len(function_signatures) == len(derived) == 8
assert derived == expected
print(f"independent_keccak_signatures={len(function_signatures)} selectors_match_method_identifiers=True")
print("selector_set=" + ",".join(sorted(derived)))

for mode in ("gas", "noopt", "codesize"):
    code_text = (out_dir / f"{mode}.bytecode_runtime").read_text().strip()
    code = bytes.fromhex(code_text.removeprefix("0x"))
    code_sha = hashlib.sha256(code).hexdigest()
    mode_methodids = json.loads((out_dir / f"{mode}.method_identifiers").read_text())
    mode_expected = {value.removeprefix("0x").lower() for value in mode_methodids.values()}
    mode_abi = json.loads((out_dir / f"{mode}.abi").read_text())
    mode_signatures = [
        f"{row['name']}({','.join(item['type'] for item in row['inputs'])})"
        for row in mode_abi if row.get("type") == "function"
    ]
    mode_derived = set()
    for signature in mode_signatures:
        digest = keccak.new(digest_bits=256)
        digest.update(signature.encode())
        mode_derived.add(digest.hexdigest()[:8])
    assert len(mode_methodids) == len(mode_derived) == 8
    assert mode_expected == mode_derived == expected
    envelope = json.loads((probe_dir / f"{mode}-6.7.0.json").read_text())
    raw = envelope["raw_result"]["functions"]
    normalized_result = envelope["normalized_result"]
    normalized = normalized_result["functions"]
    raw_selectors = {row["selector"].removeprefix("0x").lower() for row in raw}
    normalized_selectors = {row["selector"].removeprefix("0x").lower() for row in normalized}
    decoded = normalized_result["bytecode"]
    assert len(raw) == len(normalized) == 8
    assert raw_selectors == normalized_selectors == mode_derived
    assert all(row["dispatch"] == "abi" for row in raw + normalized)
    assert decoded["bytes"] == len(code)
    assert decoded["sha256"] == code_sha
    assert envelope["provider"]["id"] == "evmole-interface"
    assert normalized_result["evidence_kind"] == "inferred"
    assert normalized_result["runtime_execution"] == "not-performed"
    offsets = sorted({row["bytecodeOffset"] for row in raw})
    print(f"{mode}: evidence_id={envelope['evidence_id']} selectors={len(raw_selectors)}/8 exact dispatch=abi decoded_sha256_match=True runtime_bytes={len(code)} runtime_sha256={code_sha} offsets={offsets}")
