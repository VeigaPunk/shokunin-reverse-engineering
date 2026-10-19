import hashlib
import json
import re
from pathlib import Path
from Crypto.Hash import keccak

ROOT = Path(__file__).parent
COMPILE = ROOT / "compile"
PROBE = ROOT / "probe"
results = {}

for target in ("prague", "london"):
    abi = json.loads((COMPILE / f"{target}.abi.json").read_text())
    methods = json.loads((COMPILE / f"{target}.method-identifiers.json").read_text())
    functions = [item for item in abi if item.get("type") == "function"]
    signatures = {
        item["name"] + "(" + ",".join(arg["type"] for arg in item["inputs"]) + ")"
        for item in functions
    }
    derived = {}
    for signature in signatures:
        digest = keccak.new(digest_bits=256)
        digest.update(signature.encode())
        derived[signature] = "0x" + digest.hexdigest()[:8]
    compiler_ids = {name: value.lower() for name, value in methods.items()}
    assert compiler_ids == derived, (target, "compiler IDs differ from Keccak")

    probe = json.loads((PROBE / f"{target}.json").read_text())
    expected = set(derived.values())
    raw = {"0x" + item["selector"].lower().removeprefix("0x") for item in probe["raw_result"]["functions"]}
    normalized = {item["selector"].lower() for item in probe["normalized_result"]["functions"]}
    assert raw == expected, (target, "raw selector set differs")
    assert normalized == expected, (target, "normalized selector set differs")
    assert len(probe["raw_result"]["functions"]) == len(expected)
    assert len(probe["normalized_result"]["functions"]) == len(expected)

    opcode_text = (COMPILE / f"{target}.opcodes.txt").read_text()
    push4 = ["0x" + value.lower() for value in re.findall(r"\bPUSH4 0x([0-9A-Fa-f]{8})\b", opcode_text)]
    assert len(push4) == len(expected), (target, "unexpected PUSH4 count", push4)
    assert set(push4) == expected, (target, "PUSH4 selector set differs")
    assert opcode_text.count("DUP2 XOR") == len(expected)
    assert opcode_text.count(" MOD ") == 1
    assert opcode_text.count(" CODECOPY ") == 1

    runtime = bytes.fromhex((COMPILE / f"{target}.runtime.hex").read_text().strip().removeprefix("0x"))
    settings = json.loads((COMPILE / f"{target}.settings.json").read_text())
    offsets = sorted(item["bytecode_offset"] for item in probe["normalized_result"]["functions"])
    results[target] = {
        "settings": settings,
        "functions": len(functions),
        "compiler_keccak_equals": True,
        "rea_raw": len(raw),
        "rea_normalized": len(normalized),
        "rea_selectors_match": True,
        "opcode_push4": len(push4),
        "opcode_xor_comparisons": opcode_text.count("DUP2 XOR"),
        "opcode_mod": opcode_text.count(" MOD "),
        "opcode_codecopy": opcode_text.count(" CODECOPY "),
        "runtime_bytes": len(runtime),
        "runtime_sha256": hashlib.sha256(runtime).hexdigest(),
        "runtime_hex_prefix": runtime[:5].hex(),
        "rea_offsets": offsets,
        "evidence_id": probe["evidence_id"],
    }

assert set(derived.values()) == set(json.loads((COMPILE / "london.method-identifiers.json").read_text()).values())
print(json.dumps({"target_results": results, "same_selector_set_across_targets": True}, sort_keys=True))
