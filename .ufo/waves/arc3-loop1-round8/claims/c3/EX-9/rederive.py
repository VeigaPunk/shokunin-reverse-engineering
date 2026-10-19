from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
ROT = (
    (0, 36, 3, 41, 18),
    (1, 44, 10, 45, 2),
    (62, 6, 43, 15, 61),
    (28, 55, 25, 21, 56),
    (27, 20, 39, 8, 14),
)
ROUND_CONSTANTS = (
    0x0000000000000001, 0x0000000000008082, 0x800000000000808A,
    0x8000000080008000, 0x000000000000808B, 0x0000000080000001,
    0x8000000080008081, 0x8000000000008009, 0x000000000000008A,
    0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
    0x000000008000808B, 0x800000000000008B, 0x8000000000008089,
    0x8000000000008003, 0x8000000000008002, 0x8000000000000080,
    0x000000000000800A, 0x800000008000000A, 0x8000000080008081,
    0x8000000000008080, 0x0000000080000001, 0x8000000080008008,
)
MASK64 = (1 << 64) - 1


def rol(value: int, count: int) -> int:
    if count == 0:
        return value
    return ((value << count) | (value >> (64 - count))) & MASK64


def keccak_f(state: list[int]) -> None:
    for constant in ROUND_CONSTANTS:
        columns = [state[x] ^ state[x + 5] ^ state[x + 10] ^ state[x + 15] ^ state[x + 20] for x in range(5)]
        delta = [columns[(x - 1) % 5] ^ rol(columns[(x + 1) % 5], 1) for x in range(5)]
        for y in range(5):
            for x in range(5):
                state[x + 5 * y] ^= delta[x]
        moved = [0] * 25
        for y in range(5):
            for x in range(5):
                moved[y + 5 * ((2 * x + 3 * y) % 5)] = rol(state[x + 5 * y], ROT[x][y])
        for y in range(5):
            for x in range(5):
                state[x + 5 * y] = moved[x + 5 * y] ^ ((~moved[(x + 1) % 5 + 5 * y]) & moved[(x + 2) % 5 + 5 * y])
        state[0] ^= constant


def keccak256(data: bytes) -> bytes:
    rate = 136
    padded = bytearray(data)
    padded.append(0x01)
    padded.extend(b"\x00" * ((rate - len(padded) % rate - 1) % rate))
    padded.append(0x80)
    state = [0] * 25
    for start in range(0, len(padded), rate):
        block = padded[start : start + rate]
        for index, value in enumerate(block):
            state[index // 8] ^= value << (8 * (index % 8))
        keccak_f(state)
    return b"".join(lane.to_bytes(8, "little") for lane in state)[:32]


OPCODE_NAMES = {
    0x00: "STOP", 0x01: "ADD", 0x02: "MUL", 0x03: "SUB", 0x04: "DIV",
    0x05: "SDIV", 0x06: "MOD", 0x07: "SMOD", 0x08: "ADDMOD", 0x09: "MULMOD",
    0x0A: "EXP", 0x0B: "SIGNEXTEND", 0x10: "LT", 0x11: "GT", 0x12: "SLT",
    0x13: "SGT", 0x14: "EQ", 0x15: "ISZERO", 0x16: "AND", 0x17: "OR",
    0x18: "XOR", 0x19: "NOT", 0x1A: "BYTE", 0x1B: "SHL", 0x1C: "SHR",
    0x1D: "SAR", 0x20: "KECCAK256", 0x30: "ADDRESS", 0x31: "BALANCE",
    0x32: "ORIGIN", 0x33: "CALLER", 0x34: "CALLVALUE", 0x35: "CALLDATALOAD",
    0x36: "CALLDATASIZE", 0x37: "CALLDATACOPY", 0x38: "CODESIZE", 0x39: "CODECOPY",
    0x3A: "GASPRICE", 0x3B: "EXTCODESIZE", 0x3C: "EXTCODECOPY", 0x3D: "RETURNDATASIZE",
    0x3E: "RETURNDATACOPY", 0x40: "BLOCKHASH", 0x41: "COINBASE", 0x42: "TIMESTAMP",
    0x43: "NUMBER", 0x44: "PREVRANDAO", 0x45: "GASLIMIT", 0x46: "CHAINID",
    0x47: "SELFBALANCE", 0x48: "BASEFEE", 0x50: "POP", 0x51: "MLOAD",
    0x52: "MSTORE", 0x53: "MSTORE8", 0x54: "SLOAD", 0x55: "SSTORE",
    0x56: "JUMP", 0x57: "JUMPI", 0x58: "PC", 0x59: "MSIZE", 0x5A: "GAS",
    0x5B: "JUMPDEST", 0x5F: "PUSH0", 0xF0: "CREATE", 0xF1: "CALL",
    0xF2: "CALLCODE", 0xF3: "RETURN", 0xF4: "DELEGATECALL", 0xF5: "CREATE2",
    0xFA: "STATICCALL", 0xFD: "REVERT", 0xFE: "INVALID", 0xFF: "SELFDESTRUCT",
}
for index in range(1, 33):
    OPCODE_NAMES[0x5F + index] = f"PUSH{index}"
for index in range(1, 17):
    OPCODE_NAMES[0x7F + index] = f"DUP{index}"
    OPCODE_NAMES[0x8F + index] = f"SWAP{index}"
for index in range(0, 5):
    OPCODE_NAMES[0xA0 + index] = f"LOG{index}"


def executable_region(code: bytes) -> tuple[bytes, int]:
    if len(code) >= 2:
        trailer_size = int.from_bytes(code[-2:], "big")
        trailer_start = len(code) - 2 - trailer_size
        if trailer_start >= 0 and code[trailer_start] >> 5 == 5 and b"vyper" in code[trailer_start:-2]:
            return code[:trailer_start], trailer_start
    return code, len(code)


def disassemble(code: bytes) -> list[tuple[int, str, bytes]]:
    code, _ = executable_region(code)
    rows = []
    pc = 0
    while pc < len(code):
        start = pc
        opcode = code[pc]
        pc += 1
        name = OPCODE_NAMES.get(opcode, f"0x{opcode:02x}")
        immediate = b""
        if 0x60 <= opcode <= 0x7F:
            width = opcode - 0x5F
            immediate = code[pc : pc + width]
            pc += width
        rows.append((start, name, immediate))
    return rows


assert keccak256(b"").hex() == "c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"
assert keccak256(b"transfer(address,uint256)")[:4].hex() == "a9059cbb"
print("keccak_vectors=2/2")
print(f"source_sha256={hashlib.sha256((ROOT / 'K8.vy').read_bytes()).hexdigest()}")

forms = ("gas", "noopt", "none", "codesize")
compiled = {}
for form in forms:
    path = ROOT / f"{form}.runtime.hex"
    carrier = path.read_bytes()
    code = bytes.fromhex(carrier.decode().strip().removeprefix("0x"))
    compiled[form] = code
    abi = json.loads((ROOT / f"{form}.abi.json").read_text())
    method_ids = json.loads((ROOT / f"{form}.methodids.json").read_text())
    signatures = [
        item["name"] + "(" + ",".join(arg["type"] for arg in item["inputs"]) + ")"
        for item in abi if item.get("type") == "function"
    ]
    selectors = {keccak256(signature.encode())[:4].hex() for signature in signatures}
    compiler_selectors = {value.removeprefix("0x").lower() for value in method_ids.values()}
    executable, executable_bytes = executable_region(code)
    rows = disassemble(code)
    counts = {name: sum(row[1] == name for row in rows) for name in ("PUSH4", "EQ", "XOR", "MOD", "CODECOPY", "JUMPI", "JUMPDEST")}
    push4 = [(pc, immediate.hex()) for pc, name, immediate in rows if name == "PUSH4"]
    partial_pushes = [(pc, name, len(immediate), int(name[4:])) for pc, name, immediate in rows if name.startswith("PUSH") and name[4:].isdigit() and len(immediate) < int(name[4:])]
    print(f"[{form}] bytes={len(code)} executable_bytes={executable_bytes} metadata_bytes={len(code) - executable_bytes} decoded_sha256={hashlib.sha256(code).hexdigest()} carrier_sha256={hashlib.sha256(carrier).hexdigest()}")
    print(f"partial_push_at_eof={partial_pushes}")
    print(f"abi_functions={len(signatures)} method_ids={len(method_ids)} distinct_abi_selectors={len(selectors)} set_equals_method_ids={selectors == compiler_selectors}")
    print("selectors=" + ",".join(sorted(selectors)))
    print("opcode_counts=" + ",".join(f"{name}:{value}" for name, value in counts.items()))
    if form in ("gas", "noopt"):
        print("PUSH4_sites=" + ",".join(f"0x{pc:x}:{selector}" for pc, selector in push4))
        for pc, selector in push4:
            index = next(i for i, row in enumerate(rows) if row[0] == pc)
            window = rows[index : index + 6]
            print("window=" + " ".join(f"0x{offset:x}:{name}" + (f" {immediate.hex()}" if immediate else "") for offset, name, immediate in window))
    if form == "codesize":
        table_call = None
        for index, row in enumerate(rows):
            if row[1] == "CODECOPY" and index >= 3 and rows[index - 1][1] == "PUSH1" and rows[index - 1][2] == b"\x1b" and rows[index - 2][1] == "PUSH2" and rows[index - 3][1] == "PUSH1" and rows[index - 3][2] == b"\x05":
                table_call = index
                break
        if table_call is None:
            raise ValueError("table CODECOPY prelude not found")
        data_base = int.from_bytes(rows[table_call - 2][2], "big")
        data = code[data_base:]
        header, records = data[:5], data[5:]
        if len(records) % 7:
            raise ValueError(f"selector table record tail is not divisible by 7: {len(records)}")
        decoded_records = []
        for index in range(0, len(records), 7):
            item = records[index : index + 7]
            selector = item[:4].hex()
            target = int.from_bytes(item[4:6], "big")
            marker = item[6]
            decoded_records.append((selector, target, marker, code[target] if target < len(code) else None))
        print(f"table_copy_pc=0x{rows[table_call][0]:x} table_base=0x{data_base:x} table_tail_bytes={len(data)} header={header.hex()} record_count={len(decoded_records)}")
        print("table_records=" + ",".join(f"{sel}->0x{dst:04x}/marker-0x{marker:02x}/target-byte-{target_byte:02x}" for sel, dst, marker, target_byte in decoded_records))
        table_selectors = {item[0] for item in decoded_records}
        print(f"table_selector_set_equals_abi={table_selectors == selectors} all_targets_jumpdest={all(item[3] == 0x5b for item in decoded_records)} all_markers_0x25={all(item[2] == 0x25 for item in decoded_records)}")

print(f"noopt_equals_none={compiled['noopt'] == compiled['none']}")
