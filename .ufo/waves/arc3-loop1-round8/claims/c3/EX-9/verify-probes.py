from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()


def instructions(code: bytes) -> list[tuple[int, int, bytes]]:
    rows = []
    pc = 0
    while pc < len(code):
        start = pc
        opcode = code[pc]
        pc += 1
        immediate = b""
        if 0x60 <= opcode <= 0x7F:
            width = opcode - 0x5F
            immediate = code[pc : pc + width]
            pc += width
        rows.append((start, opcode, immediate))
    return rows


def runtime(form: str) -> bytes:
    return bytes.fromhex((ROOT / f"{form}.runtime.hex").read_text().strip().removeprefix("0x"))


for form in ("gas", "noopt", "codesize"):
    code = runtime(form)
    expected = {value.removeprefix("0x").lower() for value in json.loads((ROOT / f"{form}.methodids.json").read_text()).values()}
    probe = json.loads((ROOT / f"probe-{form}.json").read_text())
    result = probe["normalized_result"]
    rows = result["functions"]
    observed = {row["selector"].removeprefix("0x").lower() for row in rows}
    raw = {row["selector"].removeprefix("0x").lower() for row in probe["raw_result"]["functions"]}
    normalized = result["bytecode"]
    assert probe["operation"] == "inspect_evm_interface"
    assert probe["provider"]["id"] == "evmole-interface"
    assert probe["provider"]["version"] == "evmole@0.9.3"
    assert result["evidence_kind"] == "inferred" and probe["authority"] == "shipped-artifact"
    assert result["runtime_execution"] == "not-performed" and result["discovery_completeness"] == "unknown"
    assert len(rows) == len(observed) == 8 and observed == expected and raw == expected
    assert normalized["sha256"] == hashlib.sha256(code).hexdigest()
    assert normalized["bytes"] == len(code)
    assert all(row["dispatch"] == "abi" for row in rows)
    offsets = {row["selector"].removeprefix("0x").lower(): row["bytecode_offset"] for row in rows}
    opcode_rows = instructions(code)
    if form in ("gas", "noopt"):
        push4_sites = {immediate.hex(): pc for pc, opcode, immediate in opcode_rows if opcode == 0x63}
        delta = 11 if form == "gas" else 12
        assert set(push4_sites) == expected
        assert all(offsets[selector] == pc + delta for selector, pc in push4_sites.items())
        expected_byte = 0x60 if form == "gas" else 0x34
        assert all(code[offsets[selector]] == expected_byte for selector in expected)
        print(f"{form}: evidence_id={probe['evidence_id']} functions={len(rows)} selector_set=8/8 decoded_sha_match=True offsets=push4_pc+{delta} offset_opcode=0x{expected_byte:02x}")
        print("  selector_offsets=" + ",".join(f"{selector}:{offsets[selector]}" for selector in sorted(expected)))
    else:
        unique_offsets = set(offsets.values())
        copy_index = next(i for i, (_, opcode, _) in enumerate(opcode_rows) if opcode == 0x39 and i >= 3 and opcode_rows[i - 1][1] == 0x60 and opcode_rows[i - 1][2] == b"\x1b" and opcode_rows[i - 2][1] == 0x61 and opcode_rows[i - 3][1] == 0x60 and opcode_rows[i - 3][2] == b"\x05")
        base = int.from_bytes(opcode_rows[copy_index - 2][2], "big")
        tail = code[base:]
        table_records = [tail[5 + index * 7 : 5 + (index + 1) * 7] for index in range((len(tail) - 5) // 7)]
        targets = {int.from_bytes(record[4:6], "big") for record in table_records}
        assert unique_offsets == {65} and code[65] == 0x80
        assert len(table_records) == 8 and {record[:4].hex() for record in table_records} == expected
        assert 65 not in targets
        print(f"{form}: evidence_id={probe['evidence_id']} functions={len(rows)} selector_set=8/8 decoded_sha_match=True shared_offsets={sorted(unique_offsets)} opcode_at_65=0x{code[65]:02x} table_base=0x{base:x} table_targets={sorted(targets)} offset_is_handler_target=False")
    print(f"  confidence={probe['confidence']} authority={probe['authority']} execution={result['runtime_execution']} completeness={result['discovery_completeness']}")
