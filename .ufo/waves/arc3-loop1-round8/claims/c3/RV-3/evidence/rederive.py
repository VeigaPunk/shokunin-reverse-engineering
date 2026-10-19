import hashlib
import json
from pathlib import Path

from Crypto.Hash import keccak

EVIDENCE = Path(__file__).resolve().parent
REPO = EVIDENCE.parents[6]
SOURCE = REPO / ".ufo/waves/arc3-loop1-round4/claims/c1/CR-1/vy/K8.vy"


def decode(code):
    out = []
    pc = 0
    while pc < len(code):
        start = pc
        op = code[pc]
        pc += 1
        size = op - 0x5F if 0x60 <= op <= 0x7F else 0
        immediate = code[pc:pc + size]
        pc += size
        name = f"PUSH{size}" if size else {
            0x06: "MOD", 0x14: "EQ", 0x15: "ISZERO", 0x34: "CALLVALUE",
            0x39: "CODECOPY", 0x57: "JUMPI", 0x5B: "JUMPDEST",
            0x80: "DUP1", 0x81: "DUP2", 0x18: "XOR",
        }.get(op, f"0x{op:02x}")
        out.append((start, op, name, immediate))
    return out


def read_code(mode):
    text = (EVIDENCE / f"{mode}.runtime.hex").read_text().strip()
    return bytes.fromhex(text.removeprefix("0x"))


abi = json.loads((EVIDENCE / "noopt.abi.json").read_text())
method_ids = json.loads((EVIDENCE / "noopt.methodids.json").read_text())
signatures = {}
abi_mutability = {}
for item in abi:
    if item.get("type") != "function":
        continue
    signature = item["name"] + "(" + ",".join(arg["type"] for arg in item.get("inputs", [])) + ")"
    digest = keccak.new(digest_bits=256)
    digest.update(signature.encode("utf-8"))
    signatures[signature] = digest.hexdigest()[:8]
    abi_mutability[signature] = item["stateMutability"]
normalized_method_ids = {key: value.removeprefix("0x").lower() for key, value in method_ids.items()}
assert signatures == normalized_method_ids
noopt_settings = json.loads((EVIDENCE / "noopt.settings.json").read_text())
none_settings = json.loads((EVIDENCE / "none.settings.json").read_text())
noopt_code = read_code("noopt")
none_code = read_code("none")
assert noopt_settings["optimize"] == none_settings["optimize"] == "none"
assert noopt_code == none_code
abi_mutability_by_selector = {signatures[signature]: value for signature, value in abi_mutability.items()}

result = {
    "source": str(SOURCE),
    "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    "abi_functions": len(signatures),
    "method_identifiers": len(normalized_method_ids),
    "signatures_and_selectors": signatures,
    "compiler_method_identifiers_match_independent_keccak": True,
    "abi_mutability": sorted(set(abi_mutability.values())),
    "noopt_and_O_none": {
        "settings": noopt_settings,
        "identical_runtime_hex_bytes": True,
        "runtime_bytes": len(none_code),
        "runtime_sha256": hashlib.sha256(none_code).hexdigest(),
    },
    "forms": {},
}

for mode in ("noopt", "codesize"):
    code = read_code(mode)
    instructions = decode(code)
    envelope = json.loads((EVIDENCE / f"rea-{mode}.json").read_text())
    normalized = envelope["normalized_result"]
    functions = normalized["functions"]
    raw_functions = envelope["raw_result"]["functions"]
    actual_selectors = {item["selector"].removeprefix("0x").lower() for item in functions}
    code_sha = hashlib.sha256(code).hexdigest()
    carrier_sha = hashlib.sha256((EVIDENCE / f"{mode}.runtime.hex").read_bytes()).hexdigest()
    assert normalized["bytecode"]["sha256"] == code_sha
    assert normalized["bytecode"]["bytes"] == len(code)
    assert envelope["subject"]["digest"]["sha256"] == carrier_sha
    assert len(raw_functions) == len(functions) == len(signatures)
    assert actual_selectors == set(signatures.values())
    assert {item["dispatch"] for item in functions} == {"abi"}
    inferred_mutability = {item["selector"].removeprefix("0x"): item["inferred_state_mutability"] for item in functions}
    mutability_agreement = sum(abi_mutability_by_selector[selector] == inferred for selector, inferred in inferred_mutability.items())

    op_counts = {name: sum(item[2] == name for item in instructions) for name in ("PUSH4", "EQ", "ISZERO", "XOR", "MOD", "CODECOPY")}
    detail = {
        "runtime_bytes": len(code),
        "runtime_sha256": code_sha,
        "hex_carrier_sha256": carrier_sha,
        "opcode_counts": op_counts,
        "rea_evidence_id": envelope["evidence_id"],
        "rea_provider": envelope["provider"],
        "rea_raw_normalized_function_counts": [len(raw_functions), len(functions)],
        "rea_selectors_match_independent_keccak": True,
        "rea_dispatch": "abi",
        "rea_inferred_mutability": sorted({item["inferred_state_mutability"] for item in functions}),
        "abi_vs_rea_mutability_agreement": [mutability_agreement, len(functions)],
        "rea_bytecode_offsets": {item["selector"].removeprefix("0x"): item["bytecode_offset"] for item in functions},
        "confidence": envelope["confidence"],
        "authority": envelope["authority"],
        "discovery_completeness": normalized["discovery_completeness"],
        "runtime_execution": normalized["runtime_execution"],
    }
    if mode == "noopt":
        legs = []
        for index, item in enumerate(instructions):
            if item[2] == "PUSH4" and [entry[2] for entry in instructions[index + 1:index + 6]] == ["DUP2", "EQ", "ISZERO", "PUSH2", "JUMPI"]:
                selector = item[3].hex()
                offset = detail["rea_bytecode_offsets"][selector]
                legs.append({"selector": selector, "push4_pc": item[0], "rea_offset": offset, "opcode_at_offset": f"0x{code[offset]:02x}"})
        detail["eq_iszero_chain_legs"] = legs
        assert len(legs) == 8
        assert all(row["rea_offset"] == row["push4_pc"] + 12 and row["opcode_at_offset"] == "0x34" for row in legs)
    else:
        copy_index = next(index for index, item in enumerate(instructions) if item[2] == "CODECOPY")
        copy_window = instructions[copy_index - 3:copy_index + 1]
        assert [item[2] for item in copy_window] == ["PUSH1", "PUSH2", "PUSH1", "CODECOPY"]
        assert [int.from_bytes(item[3], "big") for item in copy_window[:3]] == [5, 0x12B, 0x1B]
        detail["first_CODECOPY"] = {
            "pc": f"0x{instructions[copy_index][0]:x}",
            "push_immediates_in_order": [f"0x{int.from_bytes(item[3], 'big'):x}" for item in copy_window[:3]],
            "code_bytes_copied": 5,
            "source_offset": "0x12b",
            "memory_offset": "0x1b",
        }
        start = 0x12B
        tail = code[start:]
        records = []
        for index in range(5, len(tail), 7):
            record = tail[index:index + 7]
            if len(record) == 7:
                records.append({
                    "selector": record[:4].hex(),
                    "target": int.from_bytes(record[4:6], "big"),
                    "marker": f"0x{record[6]:02x}",
                })
        detail["table"] = {
            "start": f"0x{start:x}",
            "bytes": len(tail),
            "end_exclusive": f"0x{start + len(tail):x}",
            "header": tail[:5].hex(),
            "first_27_bytes_hex": tail[:27].hex(),
            "records": records,
            "all_record_targets_are_jumpdest": all(code[row["target"]] == 0x5B for row in records),
        }
        assert len(tail) == 61 and len(records) == 8
        assert detail["table"]["header"] == "01c3013008"
        assert {row["selector"] for row in records} == set(signatures.values())
        assert all(row["marker"] == "0x25" for row in records)
        assert detail["table"]["all_record_targets_are_jumpdest"]
        assert all(item["bytecode_offset"] == 65 for item in functions)
        assert all(code[item["bytecode_offset"]] == 0x80 for item in functions)
    result["forms"][mode] = detail

print(json.dumps(result, sort_keys=True, separators=(",", ":")))
