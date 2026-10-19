import hashlib
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
names = {
    0x00: "STOP", 0x01: "ADD", 0x02: "MUL", 0x03: "SUB", 0x04: "DIV",
    0x06: "MOD", 0x10: "LT", 0x11: "GT", 0x14: "EQ", 0x15: "ISZERO",
    0x16: "AND", 0x17: "OR", 0x18: "XOR", 0x19: "NOT", 0x1b: "SHL",
    0x1c: "SHR", 0x35: "CALLDATALOAD", 0x36: "CALLDATASIZE",
    0x37: "CALLDATACOPY", 0x39: "CODECOPY", 0x51: "MLOAD", 0x52: "MSTORE",
    0x54: "SLOAD", 0x55: "SSTORE", 0x56: "JUMP", 0x57: "JUMPI",
    0x5b: "JUMPDEST", 0x5f: "PUSH0", 0xf3: "RETURN", 0xfd: "REVERT",
}
for op in range(0x80, 0x90):
    names[op] = f"DUP{op - 0x7f}"
for op in range(0x90, 0xa0):
    names[op] = f"SWAP{op - 0x8f}"
for op in range(0x60, 0x80):
    names[op] = f"PUSH{op - 0x5f}"


def decode(code):
    out = []
    pc = 0
    while pc < len(code):
        start = pc
        op = code[pc]
        pc += 1
        if 0x60 <= op <= 0x7f:
            width = op - 0x5f
            imm = code[pc:pc + width]
            pc += width
            name = names[op]
            value = imm.hex()
        else:
            name = names.get(op, f"0x{op:02x}")
            value = ""
        out.append((start, name, value, pc))
    return out


for variant in ("gas", "noopt", "codesize"):
    code = bytes.fromhex((root / f"{variant}.runtime.hex").read_text().strip().removeprefix("0x"))
    method_ids = json.loads((root / f"{variant}.methodids.json").read_text())
    oracle = {value.removeprefix("0x") for value in method_ids.values()}
    instructions = decode(code)
    by_pc = {row[0]: index for index, row in enumerate(instructions)}
    push4 = [(pc, imm) for pc, name, imm, _ in instructions if name == "PUSH4"]
    occurrences = {}
    for selector in sorted(oracle):
        needle = bytes.fromhex(selector)
        positions = []
        cursor = 0
        while (cursor := code.find(needle, cursor)) >= 0:
            positions.append(cursor)
            cursor += 1
        occurrences[selector] = positions
    after = lambda pc, count: [instructions[by_pc[pc] + i][1] for i in range(1, count + 1)]
    noopt_legs = [(pc, imm) for pc, imm in push4 if after(pc, 5) == ["DUP2", "EQ", "ISZERO", "PUSH2", "JUMPI"]]
    gas_legs = [(pc, imm) for pc, imm in push4 if after(pc, 4) == ["DUP2", "XOR", "PUSH2", "JUMPI"]]
    copy_windows = []
    for i in range(len(instructions) - 3):
        window = instructions[i:i + 4]
        if [(x[1], x[2]) for x in window] == [
            ("PUSH1", "05"), ("PUSH2", "012b"), ("PUSH1", "1b"), ("CODECOPY", "")
        ]:
            copy_windows.append([x[0] for x in window])
    probe = json.loads((root / f"probe-{variant}-6.4.0.json").read_text())
    probe = probe.get("data", probe)
    functions = probe["normalized_result"]["functions"]
    recovered = {row["selector"].removeprefix("0x") for row in functions}
    push4_by_selector = {imm: pc for pc, imm in push4}
    probe_offsets = []
    for row in functions:
        selector = row["selector"].removeprefix("0x")
        offset = row["bytecode_offset"]
        instruction = instructions[by_pc[offset]] if offset in by_pc else None
        push_pc = push4_by_selector.get(selector)
        probe_offsets.append({
            "selector": selector,
            "offset": offset,
            "opcode_at_offset": instruction[1] if instruction else None,
            "push4_pc": push_pc,
            "offset_minus_push4_pc": offset - push_pc if push_pc is not None else None,
        })
    print(json.dumps({
        "variant": variant,
        "runtime_bytes": len(code),
        "runtime_sha256": hashlib.sha256(code).hexdigest(),
        "compiler_method_ids": len(oracle),
        "push4_count": len(push4),
        "push4_loci": push4,
        "noopt_eq_legs": noopt_legs,
        "gas_xor_legs": gas_legs,
        "codesize_copy_window_pcs": copy_windows,
        "selector_byte_offsets": occurrences,
        "all_selector_bytes_in_codesize_tail": (
            all(offset >= 0x12b for values in occurrences.values() for offset in values)
            if variant == "codesize" else None
        ),
        "probe_evidence_id": probe.get("evidence_id"),
        "probe_bytecode_sha256": probe["normalized_result"]["bytecode"]["sha256"],
        "probe_function_rows": len(functions),
        "probe_unique_selectors": len(recovered),
        "missing": sorted(oracle - recovered),
        "extra": sorted(recovered - oracle),
        "dispatch_values": sorted({row["dispatch"] for row in functions}),
        "probe_offsets": probe_offsets,
    }, sort_keys=True))
