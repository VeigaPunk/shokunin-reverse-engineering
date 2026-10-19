#!/usr/bin/env python3
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent / "evidence"
text = (HERE / "noopt.runtime.hex").read_text(encoding="ascii").strip()
if text.startswith("0x"):
    text = text[2:]
code = bytes.fromhex(text)
probe = json.loads((HERE / "noopt.probe.json").read_text())
rows = {row["selector"].removeprefix("0x").lower(): row["bytecode_offset"] for row in probe["normalized_result"]["functions"]}

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

push4_pcs = {}
for index in range(len(instructions) - 5):
    window = instructions[index:index + 6]
    if [item[1] for item in window] == [0x63, 0x81, 0x14, 0x15, 0x61, 0x57]:
        push4_pcs[window[0][2].hex()] = window[0][0]

assert set(rows) == set(push4_pcs) and len(rows) == 8
results = []
for selector, offset in sorted(rows.items()):
    push4_pc = push4_pcs[selector]
    opcode = code[offset]
    results.append((selector, push4_pc, offset, offset - push4_pc, opcode))
assert all(delta == 12 and opcode == 0x34 for _, _, _, delta, opcode in results)

print(f"rows={len(results)}")
print("all_REA_offsets_equal_PUSH4_pc_plus_12=True")
print("all_REA_offsets_point_to_CALLVALUE_not_JUMPDEST=True")
print("rows=" + ",".join(f"{selector}:push4_pc={push4_pc:#x}:rea_offset={offset:#x}:delta={delta}:opcode=CALLVALUE" for selector, push4_pc, offset, delta, opcode in results))
