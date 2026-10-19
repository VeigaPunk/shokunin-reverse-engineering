#!/usr/bin/env python3
import hashlib
import json
import pathlib
import sys

MASK = (1 << 64) - 1
ROUND_CONSTANTS = [
    0x0000000000000001, 0x0000000000008082, 0x800000000000808A,
    0x8000000080008000, 0x000000000000808B, 0x0000000080000001,
    0x8000000080008081, 0x8000000000008009, 0x000000000000008A,
    0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
    0x000000008000808B, 0x800000000000008B, 0x8000000000008089,
    0x8000000000008003, 0x8000000000008002, 0x8000000000000080,
    0x000000000000800A, 0x800000008000000A, 0x8000000080008081,
    0x8000000000008080, 0x0000000080000001, 0x8000000080008008,
]
ROTATION = [
    [0, 36, 3, 41, 18],
    [1, 44, 10, 45, 2],
    [62, 6, 43, 15, 61],
    [28, 55, 25, 21, 56],
    [27, 20, 39, 8, 14],
]
OPCODE_NAMES = {
    0x00: "STOP", 0x01: "ADD", 0x02: "MUL", 0x03: "SUB",
    0x04: "DIV", 0x05: "SDIV", 0x06: "MOD", 0x10: "LT",
    0x11: "GT", 0x14: "EQ", 0x15: "ISZERO", 0x16: "AND",
    0x17: "OR", 0x18: "XOR", 0x1B: "SHL", 0x1C: "SHR",
    0x34: "CALLVALUE", 0x35: "CALLDATALOAD", 0x36: "CALLDATASIZE",
    0x39: "CODECOPY", 0x51: "MLOAD", 0x56: "JUMP", 0x57: "JUMPI",
    0x61: "PUSH2", 0x63: "PUSH4",
    0x5B: "JUMPDEST", 0x5F: "PUSH0", 0x80: "DUP1", 0x81: "DUP2",
    0x82: "DUP3", 0xFD: "REVERT",
}


def rol(value, shift):
    if shift == 0:
        return value & MASK
    return ((value << shift) | (value >> (64 - shift))) & MASK


def keccak_f(state):
    for rc in ROUND_CONSTANTS:
        c = [state[x] ^ state[x + 5] ^ state[x + 10] ^ state[x + 15] ^ state[x + 20] for x in range(5)]
        d = [c[(x - 1) % 5] ^ rol(c[(x + 1) % 5], 1) for x in range(5)]
        for y in range(5):
            for x in range(5):
                state[x + 5 * y] ^= d[x]
        b = [0] * 25
        for y in range(5):
            for x in range(5):
                b[y + 5 * ((2 * x + 3 * y) % 5)] = rol(state[x + 5 * y], ROTATION[x][y])
        for y in range(5):
            for x in range(5):
                state[x + 5 * y] = b[x + 5 * y] ^ ((~b[(x + 1) % 5 + 5 * y]) & b[(x + 2) % 5 + 5 * y])
        state[0] ^= rc


def keccak256(data):
    rate = 136
    padded = bytearray(data)
    padded.append(0x01)
    while len(padded) % rate:
        padded.append(0)
    padded[-1] ^= 0x80
    state = [0] * 25
    for offset in range(0, len(padded), rate):
        block = padded[offset:offset + rate]
        for lane in range(rate // 8):
            state[lane] ^= int.from_bytes(block[lane * 8:lane * 8 + 8], "little")
        keccak_f(state)
    return b"".join(value.to_bytes(8, "little") for value in state)[:32]


def jump_table_data_start(code):
    pc = 0
    while pc < min(len(code), 128):
        op = code[pc]
        size = op - 0x5F if 0x60 <= op <= 0x7F else 0
        if op == 0x61 and code[pc + 3:pc + 7] == b"\x01\x60\x1e\x39":
            return int.from_bytes(code[pc + 1:pc + 3], "big")
        pc += 1 + size
    raise ValueError("no PUSH2/add/PUSH1 0x1e/CODECOPY table boundary in dispatcher prefix")


def decode(code):
    instructions = []
    pc = 0
    while pc < len(code):
        op = code[pc]
        size = op - 0x5F if 0x60 <= op <= 0x7F else 0
        immediate = code[pc + 1:pc + 1 + size]
        if len(immediate) != size:
            raise ValueError(f"truncated PUSH at 0x{pc:x}")
        instructions.append((pc, op, immediate))
        pc += 1 + size
    if pc != len(code):
        raise ValueError("instruction walk did not end at code boundary")
    return instructions


def function_signature(function):
    return function["name"] + "(" + ",".join(arg["type"] for arg in function["inputs"]) + ")"


def main(root):
    if keccak256(b"").hex() != "c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470":
        raise AssertionError("Keccak-256 empty-string vector failed")

    output = {
        "selector_hash": "Keccak-256 (Ethereum padding)",
        "keccak_empty_vector": keccak256(b"").hex(),
        "hardforks": [],
    }
    for evm in ("london", "paris", "shanghai", "cancun", "prague"):
        runtime_file = root / f"{evm}.runtime.hex"
        carrier_text = runtime_file.read_text().strip()
        if carrier_text.startswith("0x"):
            carrier_text = carrier_text[2:]
        code = bytes.fromhex(carrier_text)
        code_sha = hashlib.sha256(code).hexdigest()
        abi = json.loads((root / f"{evm}.abi.json").read_text())
        method_ids = json.loads((root / f"{evm}.methodids.json").read_text())
        settings = json.loads((root / f"{evm}.settings.json").read_text())
        probe = json.loads((root / f"{evm}.probe.json").read_text())
        functions = [item for item in abi if item.get("type") == "function"]
        signatures = {function_signature(item): item for item in functions}
        abi_selectors = {sig: keccak256(sig.encode()).hex()[:8] for sig in signatures}
        compiler_selectors = {sig: value.removeprefix("0x") for sig, value in method_ids.items()}
        if compiler_selectors != abi_selectors:
            raise AssertionError(f"{evm}: ABI and method_identifiers disagree")

        table_start = jump_table_data_start(code)
        if table_start >= len(code):
            raise AssertionError(f"{evm}: jump-table data start is outside runtime")
        decoded = decode(code[:table_start])
        push4_sites = [(index, ins[0], ins[2].hex()) for index, ins in enumerate(decoded) if ins[1] == 0x63]
        selector_set = set(abi_selectors.values())
        if {selector for _, _, selector in push4_sites} != selector_set:
            raise AssertionError(f"{evm}: opcode-boundary PUSH4 set differs from ABI selectors")
        if len(push4_sites) != len(selector_set):
            raise AssertionError(f"{evm}: duplicate or missing opcode-boundary PUSH4 selector")

        raw_functions = probe["raw_result"]["functions"]
        normalized_functions = probe["normalized_result"]["functions"]
        raw_selectors = {item["selector"].removeprefix("0x") for item in raw_functions}
        normalized_selectors = {item["selector"].removeprefix("0x") for item in normalized_functions}
        if raw_selectors != selector_set or normalized_selectors != selector_set:
            raise AssertionError(f"{evm}: REA selector set differs from ABI-derived selectors")
        if any(item["dispatch"] != "abi" for item in normalized_functions):
            raise AssertionError(f"{evm}: non-ABI dispatch result")
        bytecode = probe["normalized_result"]["bytecode"]
        if bytecode["sha256"] != code_sha or bytecode["bytes"] != len(code):
            raise AssertionError(f"{evm}: decoded REA bytecode identity differs")

        instruction_index_by_pc = {ins[0]: i for i, ins in enumerate(decoded)}
        selector_pc = {selector: pc for _, pc, selector in push4_sites}
        rows = []
        for item in normalized_functions:
            selector = item["selector"].removeprefix("0x")
            index = instruction_index_by_pc[selector_pc[selector]]
            pattern = [OPCODE_NAMES.get(decoded[j][1], f"OP_{decoded[j][1]:02x}") for j in range(index, index + 5)]
            rows.append({
                "selector": selector,
                "push4_pc": selector_pc[selector],
                "rea_offset": item["bytecode_offset"],
                "offset_is_push4_pc_plus_11": item["bytecode_offset"] == selector_pc[selector] + 11,
                "offset_byte_is_jumpdest": code[item["bytecode_offset"]] == 0x5B if item["bytecode_offset"] < len(code) else False,
                "compare_opcodes": pattern,
                "abi_mutability": signatures[next(sig for sig, value in abi_selectors.items() if value == selector)]["stateMutability"],
                "rea_mutability": item["inferred_state_mutability"],
            })

        raw_count = len(raw_functions)
        normalized_count = len(normalized_functions)
        payable_reads = sum(row["rea_mutability"] == "payable" and row["abi_mutability"] != "payable" for row in rows)
        prefix = code[:5].hex()
        output["hardforks"].append({
            "evm_version": evm,
            "settings": settings,
            "carrier_text_sha256": hashlib.sha256(runtime_file.read_bytes()).hexdigest(),
            "runtime_sha256": code_sha,
            "runtime_bytes": len(code),
            "runtime_prefix_5": prefix,
            "jump_table_data_start": table_start,
            "jump_table_tail_bytes": len(code) - table_start,
            "first_push4_pc": min(pc for _, pc, _ in push4_sites),
            "selector_count_abi_keccak": len(selector_set),
            "selector_count_method_identifiers": len(compiler_selectors),
            "selector_count_opcode_push4": len(push4_sites),
            "selector_count_rea_raw": raw_count,
            "selector_count_rea_normalized": normalized_count,
            "rea_evidence_id": probe["evidence_id"],
            "rea_decoded_sha256_matches": bytecode["sha256"] == code_sha,
            "rea_all_dispatch_abi": all(item["dispatch"] == "abi" for item in normalized_functions),
            "rea_result_inferred": probe["normalized_result"]["evidence_kind"] == "inferred" and probe["confidence"] == "inferred",
            "runtime_execution": probe["normalized_result"]["runtime_execution"],
            "opcode_push4_selector_set_matches": True,
            "all_compare_patterns_push4_dup2_xor_push2_jumpi": all(row["compare_opcodes"] == ["PUSH4", "DUP2", "XOR", "PUSH2", "JUMPI"] for row in rows),
            "offsets_push4_pc_plus_11": sum(row["offset_is_push4_pc_plus_11"] for row in rows),
            "offsets_on_jumpdest_byte": sum(row["offset_byte_is_jumpdest"] for row in rows),
            "rea_payable_reads_for_nonpayable_abi": payable_reads,
            "selectors": sorted(selector_set),
            "selector_rows": sorted(rows, key=lambda row: row["selector"]),
        })

    by_hash = {}
    for item in output["hardforks"]:
        by_hash.setdefault(item["runtime_sha256"], []).append(item["evm_version"])
    output["identical_runtime_groups"] = sorted(sorted(group) for group in by_hash.values())
    output["all_hardforks_selector_sets_equal"] = len({tuple(row["selectors"]) for row in output["hardforks"]}) == 1
    output["all_evm_settings_default_gas_nonexperimental"] = all(
        row["settings"] == {"optimize": "gas", "evm_version": row["evm_version"], "experimental_codegen": False}
        for row in output["hardforks"]
    )
    print(json.dumps(output, sort_keys=True, indent=2))


if __name__ == "__main__":
    main(pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve())
