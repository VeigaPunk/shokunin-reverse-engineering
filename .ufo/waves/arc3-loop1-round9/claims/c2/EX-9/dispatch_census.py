#!/usr/bin/env python3
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent / "evidence"
raw = (HERE / "noopt.runtime.hex").read_text(encoding="ascii").strip()
if raw.startswith("0x"):
    raw = raw[2:]
code = bytes.fromhex(raw)
method_ids = json.loads((HERE / "noopt.methodids.json").read_text())
expected = {value.removeprefix("0x").lower() for value in method_ids.values()}

instructions = []
pc = 0
while pc < len(code):
    op = code[pc]
    width = op - 0x5f if 0x60 <= op <= 0x7f else 0
    end = pc + 1 + width
    if end > len(code):
        raise ValueError(f"truncated PUSH at {pc:#x}")
    instructions.append((pc, op, code[pc + 1:end]))
    pc = end

counts = {op: sum(item[1] == op for item in instructions) for op in (0x63, 0x14, 0x15, 0x81, 0x61, 0x57, 0x06, 0x1b, 0x39)}
legs = []
for index in range(len(instructions) - 5):
    window = instructions[index:index + 6]
    if [item[1] for item in window] == [0x63, 0x81, 0x14, 0x15, 0x61, 0x57]:
        selector = window[0][2].hex()
        target = int.from_bytes(window[4][2], "big")
        legs.append((window[0][0], selector, target))

selectors = {selector for _, selector, _ in legs}
assert len(legs) == len(expected) == 8
assert selectors == expected
assert counts[0x63] == counts[0x14] == 8
assert all(code[target] == 0x5b for _, _, target in legs)

print(f"runtime_bytes={len(code)}")
print("opcode_boundary_counts=" + ",".join(f"{name}:{counts[op]}" for op, name in ((0x63, "PUSH4"), (0x14, "EQ"), (0x15, "ISZERO"), (0x81, "DUP2"), (0x61, "PUSH2"), (0x57, "JUMPI"), (0x06, "MOD"), (0x1b, "SHL"), (0x39, "CODECOPY"))))
print(f"compare_legs={len(legs)}; distinct_selectors={len(selectors)}; method_identifier_set_match={selectors == expected}")
print("legs=" + ",".join(f"pc:{pc:#x}/selector:{selector}/target:{target:#x}" for pc, selector, target in legs))
print("all_targets_are_JUMPDEST=" + str(all(code[target] == 0x5b for _, _, target in legs)))
