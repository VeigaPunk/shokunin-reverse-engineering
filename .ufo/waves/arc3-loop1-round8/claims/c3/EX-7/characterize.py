import hashlib
import json
import pathlib
import sys

base = pathlib.Path(sys.argv[1])
input_dir = base / "out" if (base / "out").is_dir() else base / "compiler" if (base / "compiler").is_dir() else base
op_names = {
    0x00: "STOP", 0x01: "ADD", 0x02: "MUL", 0x03: "SUB", 0x06: "MOD",
    0x10: "LT", 0x11: "GT", 0x14: "EQ", 0x15: "ISZERO", 0x16: "AND",
    0x18: "XOR", 0x1b: "SHL", 0x1c: "SHR", 0x20: "KECCAK256",
    0x35: "CALLDATALOAD", 0x36: "CALLDATASIZE", 0x39: "CODECOPY",
    0x50: "POP", 0x51: "MLOAD", 0x52: "MSTORE", 0x56: "JUMP",
    0x57: "JUMPI", 0x5b: "JUMPDEST", 0x5f: "PUSH0", 0x80: "DUP1",
    0x81: "DUP2", 0x82: "DUP3", 0x90: "SWAP1", 0xf3: "RETURN",
    0xfd: "REVERT",
}
for code in range(0x60, 0x80):
    op_names[code] = f"PUSH{code - 0x5f}"


def bytecode(mode):
    text = (input_dir / f"{mode}.bytecode_runtime").read_text().strip()
    return bytes.fromhex(text.removeprefix("0x"))


def decode(data):
    instructions = []
    pc = 0
    while pc < len(data):
        start = pc
        opcode = data[pc]
        pc += 1
        width = opcode - 0x5f if 0x60 <= opcode <= 0x7f else 0
        immediate = data[pc:pc + width]
        pc += width
        instructions.append((start, opcode, immediate))
    return instructions


def name(instruction):
    return op_names.get(instruction[1], f"OP_{instruction[1]:02x}")


selectors = json.loads((input_dir / "noopt.method_identifiers").read_text())
expected = {value.removeprefix("0x").lower() for value in selectors.values()}
print(f"abi_method_identifiers={len(selectors)} distinct_selectors={len(expected)}")
print("selector_set=" + ",".join(sorted(expected)))

for mode in ("gas", "noopt", "codesize"):
    data = bytecode(mode)
    instructions = decode(data)
    names = [name(item) for item in instructions]
    digest = hashlib.sha256(data).hexdigest()
    print(f"{mode}: runtime_bytes={len(data)} runtime_sha256={digest} instruction_count={len(instructions)}")
    counts = {opcode: names.count(opcode) for opcode in ("PUSH4", "EQ", "XOR", "MOD", "CODECOPY", "JUMPI", "JUMPDEST")}
    print(f"{mode}: opcode_counts={json.dumps(counts, sort_keys=True)}")
    if mode in ("gas", "noopt"):
        opcode_chain = ("PUSH4", "DUP2", "XOR", "PUSH2", "JUMPI") if mode == "gas" else ("PUSH4", "DUP2", "EQ", "ISZERO", "PUSH2", "JUMPI")
        windows = []
        for index, item in enumerate(instructions):
            if names[index:index + len(opcode_chain)] == list(opcode_chain):
                selector = item[2].hex()
                chain_end = item[0] + sum(1 + len(part[2]) for part in instructions[index:index + len(opcode_chain)])
                windows.append((item[0], chain_end, selector))
        print(f"{mode}: selector_compare_windows={len(windows)} sites=" + ";".join(f"pc={pc}:selector={selector}" for pc, _, selector in windows))
        print(f"{mode}: expected_selector_matches={set(selector for _, _, selector in windows) == expected}")
        print(f"{mode}: derived_post_chain_offsets=" + ",".join(str(offset) for _, offset, _ in windows))
        if mode == "noopt":
            print(f"{mode}: selector_push4_pcs=" + ",".join(str(pc) for pc, _, _ in windows))
            print(f"{mode}: bytes_at_derived_offsets=" + ",".join(f"0x{data[offset]:02x}" for _, offset, _ in windows))
    else:
        push4_pcs = [item[0] for item in instructions if name(item) == "PUSH4"]
        copy_index = next(index for index, item in enumerate(instructions) if name(item) == "CODECOPY")
        copy_operands = instructions[copy_index - 3:copy_index]
        assert len(copy_operands) == 3 and all(name(item).startswith("PUSH") for item in copy_operands)
        header_length = int.from_bytes(copy_operands[0][2], "big")
        table_offset = int.from_bytes(copy_operands[1][2], "big")
        copy_destination = int.from_bytes(copy_operands[2][2], "big")
        tail = data[table_offset:]
        header = tail[:header_length]
        selector_width = len(next(iter(expected))) // 2
        record_size, remainder = divmod(len(tail) - len(header), len(expected))
        assert remainder == 0 and record_size > selector_width + 1
        target_width = record_size - selector_width - 1
        records = [tail[header_length + index * record_size:header_length + (index + 1) * record_size] for index in range(len(expected))]
        decoded = [(record[:selector_width].hex(), int.from_bytes(record[selector_width:selector_width + target_width], "big"), record[-1]) for record in records]
        print(f"codesize: opcode_boundary_push4_pcs={push4_pcs}")
        print(f"codesize: first_codecopy_src=0x{table_offset:x} header_length={header_length} copy_destination={copy_destination}")
        print(f"codesize: tail_offset=0x{table_offset:x} tail_bytes={len(tail)} header={header.hex()} record_width={record_size} records={len(records)}")
        print("codesize: records=" + ";".join(f"selector={selector}:target=0x{target:04x}:tag={tag}" for selector, target, tag in decoded))
        decoded_selectors = {selector for selector, _, _ in decoded}
        print(f"codesize: record_selectors_match_expected={decoded_selectors == expected}")
        print(f"codesize: record_targets_are_jumpdest={all(target < len(data) and data[target] == 0x5b for _, target, _ in decoded)}")
        print(f"codesize: tail_selector_bytes_present={all(selector in tail.hex() for selector in expected)}")
        candidate_excerpt = bytes.fromhex("01c3013008d7b7913b00a6259adbf6910074252ae1431c005b259b")
        print(f"codesize: compared_excerpt_bytes={len(candidate_excerpt)} matches_tail_prefix={tail.startswith(candidate_excerpt)} excerpt={candidate_excerpt.hex()}")
