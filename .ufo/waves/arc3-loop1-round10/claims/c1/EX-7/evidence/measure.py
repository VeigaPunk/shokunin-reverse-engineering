#!/usr/bin/env python3
import hashlib
import json
import pathlib
import sys
from collections import Counter

root = pathlib.Path(sys.argv[1])
code = bytes.fromhex(root.joinpath("paris.runtime.hex").read_text().strip().removeprefix("0x"))
abi = json.loads(root.joinpath("paris.abi.json").read_text())
method_ids = json.loads(root.joinpath("paris.method-identifiers.json").read_text())
probe = json.loads(root.joinpath("paris.rea.json").read_text())
normalized = probe["normalized_result"]
raw_functions = probe["raw_result"]["functions"]
functions = normalized["functions"]

def sel(value):
    return str(value).lower().removeprefix("0x")

def as_int(value):
    return value if isinstance(value, int) else int(str(value), 0)

opcode_names = {
    0x00: "STOP", 0x01: "ADD", 0x02: "MUL", 0x03: "SUB", 0x04: "DIV",
    0x06: "MOD", 0x10: "LT", 0x11: "GT", 0x14: "EQ", 0x15: "ISZERO",
    0x16: "AND", 0x17: "OR", 0x18: "XOR", 0x1B: "SHL", 0x1C: "SHR",
    0x34: "CALLVALUE", 0x35: "CALLDATALOAD", 0x36: "CALLDATASIZE",
    0x37: "CALLDATACOPY", 0x38: "CODESIZE", 0x39: "CODECOPY",
    0x50: "POP", 0x51: "MLOAD", 0x52: "MSTORE", 0x54: "SLOAD",
    0x55: "SSTORE", 0x56: "JUMP", 0x57: "JUMPI", 0x5B: "JUMPDEST",
    0x5F: "PUSH0", 0xF3: "RETURN", 0xFD: "REVERT",
}
for op in range(0x60, 0x80):
    opcode_names[op] = f"PUSH{op - 0x5F}"
for op in range(0x80, 0x90):
    opcode_names[op] = f"DUP{op - 0x7F}"
for op in range(0x90, 0xA0):
    opcode_names[op] = f"SWAP{op - 0x8F}"

instructions = []
pc = 0
while pc < len(code):
    start = pc
    op = code[pc]
    pc += 1
    width = op - 0x5F if 0x60 <= op <= 0x7F else 0
    immediate = code[pc:pc + width]
    pc += width
    instructions.append((start, opcode_names.get(op, f"0x{op:02x}"), immediate))

abi_functions = [entry for entry in abi if entry.get("type") == "function"]
abi_selectors = {sel(value) for value in method_ids.values()}
rea_selectors = {sel(row["selector"]) for row in functions}
raw_selectors = {sel(row["selector"]) for row in raw_functions}
push4 = [(at, data.hex()) for at, name, data in instructions if name == "PUSH4"]
counts = Counter(name for _, name, _ in instructions)
sha = hashlib.sha256(code).hexdigest()
assert len(abi_functions) == len(method_ids) == len(functions) == len(raw_functions) == 8
assert abi_selectors == rea_selectors == raw_selectors
assert {value for _, value in push4} == abi_selectors
assert normalized["bytecode"]["sha256"] == sha

offset_by_selector = {sel(row["selector"]): as_int(row["bytecode_offset"]) for row in functions}
opcode_by_pc = {at: name for at, name, _ in instructions}

def render_instruction(at, name, immediate):
    suffix = f" 0x{immediate.hex()}" if immediate else ""
    return f"{at:#06x} {name}{suffix}"

print(f"SOURCE_SHA256={hashlib.sha256(root.joinpath('K8.vy').read_bytes()).hexdigest()}")
print(f"RUNTIME_BYTES={len(code)} RUNTIME_SHA256={sha}")
print(f"ABI_FUNCTIONS={len(abi_functions)} METHOD_IDENTIFIERS={len(method_ids)}")
print(f"ABI_METHODID_REA_NORMALIZED_REA_RAW_SELECTOR_SETS_EQUAL={abi_selectors == rea_selectors == raw_selectors}")
print("SELECTORS=" + ",".join(sorted(abi_selectors)))
print(f"PUSH4_SITES={len(push4)} PUSH4_SELECTORS_ONLY={set(value for _, value in push4) == abi_selectors}")
print("OPCODE_COUNTS=" + " ".join(
    f"{name}:{counts[name]}" for name in (
        "PUSH0", "PUSH1", "CALLDATALOAD", "SHR", "MOD", "SHL", "CODECOPY",
        "MLOAD", "DUP2", "XOR", "EQ", "ISZERO", "JUMPI", "JUMPDEST"
    )
))
print(f"REA_ROWS={len(functions)} RAW_ROWS={len(raw_functions)} DISPATCH={dict(Counter(row.get('dispatch') for row in functions))}")
print(f"REA_DECODED_SHA256_MATCH={normalized['bytecode']['sha256'] == sha}")
print(f"EVIDENCE_ID={probe.get('evidence_id', 'not-present')}")
provider = probe.get("provider", {})
print(f"PROVIDER={provider.get('id', 'not-present')} VERSION={provider.get('version', 'not-present')}")
print("SELECTOR_BYTECODE_OFFSETS=" + ",".join(
    f"{key}:{offset:#x}/{opcode_by_pc.get(offset, 'not-opcode-boundary')}"
    for key, offset in sorted(offset_by_selector.items())
))
print("HEAD_INSTRUCTIONS=")
for row in instructions[:45]:
    print(render_instruction(*row))

instruction_index = {row[0]: index for index, row in enumerate(instructions)}
codecopy_index = next(index for index, row in enumerate(instructions) if row[1] == "CODECOPY")
table_source = instructions[codecopy_index - 3]
assert table_source[1] == "PUSH2"
table_offset = int.from_bytes(table_source[2], "big")
table = code[table_offset:]
assert len(table) % 2 == 0
bucket_targets = [int.from_bytes(table[index:index + 2], "big") for index in range(0, len(table), 2)]

def is_compare_head(offset):
    index = instruction_index.get(offset)
    return index is not None and instructions[index][1] == "JUMPDEST" and [
        row[1] for row in instructions[index + 1:index + 6]
    ] == ["PUSH4", "DUP2", "XOR", "PUSH2", "JUMPI"]

bucket_chains = []
terminal_targets = []
for bucket, target in enumerate(bucket_targets):
    chain = []
    offset = target
    visited = set()
    while offset not in visited and is_compare_head(offset):
        visited.add(offset)
        index = instruction_index[offset]
        selector = instructions[index + 1][2].hex()
        next_offset = int.from_bytes(instructions[index + 4][2], "big")
        chain.append(selector)
        offset = next_offset
    expected_bucket = {selector for selector in abi_selectors if int(selector, 16) % len(bucket_targets) == bucket}
    assert set(chain) == expected_bucket
    bucket_chains.append(chain)
    terminal_targets.append(offset)
assert sum(map(len, bucket_chains)) == len(abi_selectors)
assert len(set(terminal_targets)) == 1
miss_target = terminal_targets[0]
miss_index = instruction_index[miss_target]
assert [row[1] for row in instructions[miss_index:miss_index + 4]] == ["JUMPDEST", "PUSH1", "PUSH1", "REVERT"]
for index, (at, name, immediate) in enumerate(instructions):
    if name == "PUSH4":
        selector = immediate.hex()
        assert [row[1] for row in instructions[index + 1:index + 5]] == ["DUP2", "XOR", "PUSH2", "JUMPI"]
        handler_offset = instructions[index + 5][0]
        assert offset_by_selector[selector] == handler_offset
        assert opcode_by_pc[handler_offset] == "PUSH1"
print(f"TABLE_OFFSET={table_offset:#x} TABLE_BYTES={len(table)} BUCKETS={len(bucket_targets)} TABLE_HEX={table.hex()}")
for bucket, (target, chain) in enumerate(zip(bucket_targets, bucket_chains)):
    print(f"BUCKET_{bucket}={target:#x} SELECTORS={','.join(chain) if chain else '<empty>'}")
print(f"BUCKETS_MATCH_SELECTOR_MODULO=True EMPTY_BUCKETS={sum(not chain for chain in bucket_chains)}")
print(f"CHAINS_TERMINATE_AT_REVERT=True MISS_TARGET={miss_target:#x}")
print("REA_OFFSETS_EQUAL_COMPARE_FALLTHROUGH=True HANDLER_OPCODE=PUSH1")
