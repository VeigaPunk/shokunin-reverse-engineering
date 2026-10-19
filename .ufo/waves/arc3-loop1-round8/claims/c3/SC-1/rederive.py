from collections import Counter
from Crypto.Hash import keccak
import hashlib
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
expected_builds = {
    "gas": (418, "72e5d886da7ccaf633b957738456323e22043275092e001fbc06847b57b06814"),
    "noopt": (617, "1a7bf2cdc83e171f0a8485c894286ea59289de9bd45f1c124e1ed6888ef14ffc"),
    "codesize": (360, "bf5afe485f0aa298c488ba7101dfe99f8ab372174cee605ffec4a4d796ca2ba5"),
}
assert hashlib.sha256((root / "K8.vy").read_bytes()).hexdigest() == (
    "62549f79b9efb6677e5b24769296e812ec321914816cb5e78699091fdfe6ea7d"
)
names = {
    0x03: "SUB",
    0x06: "MOD",
    0x14: "EQ",
    0x15: "ISZERO",
    0x34: "CALLVALUE",
    0x39: "CODECOPY",
    0x57: "JUMPI",
    0x5b: "JUMPDEST",
    0x61: "PUSH2",
    0x63: "PUSH4",
    0x80: "DUP1",
    0x81: "DUP2",
}


def decode(code):
    instructions = []
    pc = 0
    while pc < len(code):
        start = pc
        opcode = code[pc]
        pc += 1
        immediate = b""
        if 0x60 <= opcode <= 0x7f:
            size = opcode - 0x5f
            immediate = code[pc:pc + size]
            if len(immediate) != size:
                raise ValueError(f"truncated PUSH at {start:#x}")
            pc += size
        instructions.append((start, opcode, immediate))
    return instructions


def selector_map(abi):
    result = {}
    mutability = {}
    for function in abi:
        if function.get("type") != "function":
            continue
        signature = (
            function["name"] + "(" + ",".join(
                item["type"] for item in function.get("inputs", [])
            ) + ")"
        )
        digest = keccak.new(digest_bits=256)
        digest.update(signature.encode())
        selector = digest.hexdigest()[:8]
        result[signature] = selector
        mutability[selector] = function.get("stateMutability")
    return result, mutability


def code_hash(code):
    return hashlib.sha256(code).hexdigest()


results = {}
for mode in ("gas", "noopt", "codesize"):
    text = (root / f"{mode}.runtime.hex").read_text().strip().removeprefix("0x")
    code = bytes.fromhex(text)
    assert (len(code), code_hash(code)) == expected_builds[mode]
    abi = json.loads((root / f"{mode}.abi.json").read_text())
    method_ids = json.loads((root / f"{mode}.methodids.json").read_text())
    settings = json.loads((root / f"{mode}.settings.json").read_text())
    selectors, abi_mutability = selector_map(abi)
    expected = set(selectors.values())
    compiler_ids = {value.removeprefix("0x") for value in method_ids.values()}
    assert len(selectors) == len(expected) == 8
    assert expected == compiler_ids
    results[mode] = (code, expected, abi_mutability)
    print(
        f"{mode}: settings={json.dumps(settings, sort_keys=True)} "
        f"bytes={len(code)} sha256={code_hash(code)} "
        f"abi_functions={sum(item.get('type') == 'function' for item in abi)} "
        f"method_ids={len(method_ids)} independent_keccak={len(selectors)} "
        f"selector_sets_equal=True"
    )
    print("  selectors=" + ",".join(f"{sig}:{value}" for sig, value in selectors.items()))

for mode in ("noopt", "codesize"):
    code, expected, abi_mutability = results[mode]
    envelope = json.loads((root / f"rea-{mode}.json").read_text())
    provider = envelope["provider"]
    normalized = envelope["normalized_result"]
    raw = envelope["raw_result"]
    normalized_functions = normalized["functions"]
    raw_functions = raw["functions"]
    normalized_selectors = {
        item["selector"].removeprefix("0x") for item in normalized_functions
    }
    raw_selectors = {
        item["selector"].removeprefix("0x") for item in raw_functions
    }
    assert envelope["operation"] == "inspect_evm_interface"
    assert provider["id"] == "evmole-interface"
    assert provider["version"] == "evmole@0.9.3"
    assert envelope["confidence"] == "inferred"
    assert envelope["authority"] == "shipped-artifact"
    assert len(normalized_functions) == len(raw_functions) == 8
    assert normalized_selectors == raw_selectors == expected
    assert all(item["dispatch"] == "abi" for item in normalized_functions)
    assert normalized["bytecode"]["bytes"] == len(code)
    assert normalized["bytecode"]["sha256"] == code_hash(code)
    print(
        f"  REA id={envelope['evidence_id']} operation={envelope['operation']} "
        f"provider={provider['id']} version={provider['version']} "
        f"normalized={len(normalized_functions)} raw={len(raw_functions)} "
        f"K/K=True byte_count={normalized['bytecode']['bytes']} "
        f"decoded_sha256_match=True discovery_completeness="
        f"{normalized['discovery_completeness']}"
    )
    agreement = sum(
        abi_mutability[item["selector"][2:]] == item["inferred_state_mutability"]
        for item in normalized_functions
    )
    inference_counts = Counter(
        item["inferred_state_mutability"] for item in normalized_functions
    )
    print(
        f"  REA mutability_vs_ABI={agreement}/8 "
        f"inferred={json.dumps(dict(inference_counts), sort_keys=True)}"
    )
    offsets = {item["selector"][2:]: item["bytecode_offset"] for item in normalized_functions}
    print(
        "  REA offsets=" + ",".join(
            f"{selector}:{offsets[selector]}" for selector in sorted(offsets)
        )
    )
    instructions = decode(code)
    if mode == "noopt":
        legs = []
        for index, (pc, opcode, immediate) in enumerate(instructions):
            following = [item[1] for item in instructions[index + 1:index + 6]]
            if opcode == 0x63 and following == [0x81, 0x14, 0x15, 0x61, 0x57]:
                legs.append((pc, immediate.hex()))
        assert len(legs) == 8
        assert {selector for _, selector in legs} == expected
        assert all(offsets[selector] == pc + 12 for pc, selector in legs)
        assert all(code[offsets[selector]] == 0x34 for selector in expected)
        print(
            "  noopt opcode-boundary PUSH4/EQ chain legs=" + str(len(legs)) + " "
            + ",".join(f"{pc}:{selector}" for pc, selector in legs)
        )
        print(
            "  noopt reported offsets are PUSH4_pc+12 at CALLVALUE (0x34)=True"
        )
    else:
        table_start = len(code) - 61
        table = code[table_start:]
        assert table_start == 0x12b
        assert table[:5].hex() == "01c3013008"
        records = []
        for offset in range(table_start + 5, len(code), 7):
            selector = code[offset:offset + 4].hex()
            target = int.from_bytes(code[offset + 4:offset + 6], "big")
            marker = code[offset + 6]
            target_opcode = code[target] if target < len(code) else None
            records.append((selector, target, marker, target_opcode))
        assert len(records) == 8
        assert {selector for selector, _, _, _ in records} == expected
        assert all(marker == 0x25 and opcode == 0x5b for _, _, marker, opcode in records)
        executable = decode(code[:table_start])
        counts = Counter(opcode for _, opcode, _ in executable)
        codecopy_pcs = [pc for pc, opcode, _ in executable if opcode == 0x39]
        assert counts[0x63] == 0
        assert counts[0x14] == 1
        assert counts[0x06] == 1
        assert codecopy_pcs == [12, 45]
        assert {item["bytecode_offset"] for item in normalized_functions} == {65}
        assert code[65] == 0x80
        print(
            f"  codesize executable_prefix_bytes={table_start} "
            f"opcode_counts=PUSH4:{counts[0x63]},EQ:{counts[0x14]},"
            f"MOD:{counts[0x06]},CODECOPY:{counts[0x39]} "
            f"CODECOPY_PCs={codecopy_pcs}"
        )
        print(
            f"  codesize packed_table=offset:{table_start:#x},bytes:{len(table)},"
            f"header:{table[:5].hex()},records:{len(records)}"
        )
        print(
            "  codesize selector-to-target=" + ",".join(
                f"{selector}->{target:#06x}" for selector, target, _, _ in records
            )
        )
        print("  all table markers=0x25 and target opcodes=JUMPDEST (0x5b)=True")
        print("  codesize REA offset 65 is DUP1 (0x80), shared by all eight=True")
