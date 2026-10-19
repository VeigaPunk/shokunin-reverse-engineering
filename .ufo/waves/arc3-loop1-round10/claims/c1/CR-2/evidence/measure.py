import hashlib
import json
import pathlib
import sys

compile_dir = pathlib.Path(sys.argv[1])
probe_dir = pathlib.Path(sys.argv[2])

def read_json(path):
    return json.loads(path.read_text())

def decode(path):
    text = path.read_text().strip().removeprefix("0x")
    code = bytes.fromhex(text)
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
            pc += size
        instructions.append((start, opcode, immediate))
    return code, instructions

results = {}
for target in ("prague", "london"):
    code, instructions = decode(compile_dir / f"{target}.runtime.hex")
    digest = hashlib.sha256(code).hexdigest()
    settings = read_json(compile_dir / f"{target}.settings.json")
    abi = read_json(compile_dir / f"{target}.abi.json")
    methods = read_json(compile_dir / f"{target}.method_identifiers.json")
    functions = [row for row in abi if row.get("type") == "function"]
    method_selectors = {value.lower().removeprefix("0x") for value in methods.values()}
    probe = read_json(probe_dir / f"{target}.json")
    normalized = probe["normalized_result"]
    raw_rows = probe["raw_result"]["functions"]
    normalized_rows = normalized["functions"]
    raw_selectors = {row["selector"].lower().removeprefix("0x") for row in raw_rows}
    normalized_selectors = {row["selector"].lower().removeprefix("0x") for row in normalized_rows}
    sites = [(index, pc, immediate.hex()) for index, (pc, opcode, immediate) in enumerate(instructions)
             if opcode == 0x63 and immediate.hex() in method_selectors]
    assert settings["evm_version"] == target
    assert settings["optimize"] == "gas"
    assert len(functions) == len(methods) == len(raw_rows) == len(normalized_rows) == 8
    assert method_selectors == raw_selectors == normalized_selectors
    assert normalized["bytecode"]["sha256"] == digest
    assert len(sites) == 8 and {selector for _, _, selector in sites} == method_selectors
    dispatch_abi_rows = sum(row.get("dispatch") == "abi" for row in normalized_rows)
    assert dispatch_abi_rows == 8
    for index, _, _ in sites:
        assert [row[1] for row in instructions[index + 1:index + 5]] == [0x81, 0x18, 0x61, 0x57]
    mod_index = next(index for index, row in enumerate(instructions) if row[1] == 0x06)
    entry_bytes = int.from_bytes(instructions[mod_index - 3][2], "big")
    bucket_count = int.from_bytes(instructions[mod_index - 2][2], "big")
    assert instructions[mod_index - 3][1] == 0x60 and entry_bytes == 2
    assert instructions[mod_index - 2][1] == 0x60 and bucket_count == 9
    assert instructions[mod_index - 1][1] == 0x82
    assert instructions[mod_index + 1][1] == 0x60 and instructions[mod_index + 1][2] == b"\x01"
    assert instructions[mod_index + 2][1] == 0x1b
    table_push = mod_index + 3
    assert instructions[table_push][1] == 0x61
    table_start = int.from_bytes(instructions[table_push][2], "big")
    assert instructions[mod_index + 4][1] == 0x01
    assert instructions[mod_index + 5][1] == 0x60 and instructions[mod_index + 5][2] == b"\x1e"
    assert instructions[mod_index + 6][1] == 0x39
    assert instructions[mod_index + 8][1] == 0x51 and instructions[mod_index + 9][1] == 0x56
    table = code[table_start:table_start + entry_bytes * bucket_count]
    table_entries = [int.from_bytes(table[index:index + entry_bytes], "big") for index in range(0, len(table), entry_bytes)]
    assert len(table) == 18 and len(table_entries) == bucket_count
    assert all(target_pc < len(code) and code[target_pc] == 0x5b for target_pc in table_entries)
    results[target] = (code, method_selectors, table_start, table, table_entries, probe)
    print(f"{target.upper()}_SETTINGS={json.dumps(settings, sort_keys=True)}")
    print(f"{target.upper()}_RUNTIME_BYTES={len(code)} SHA256={digest}")
    print(f"{target.upper()}_ABI_FUNCTIONS={len(functions)} METHOD_ID_ENTRIES={len(methods)}")
    print(f"{target.upper()}_SELECTORS={','.join(sorted(method_selectors))}")
    print(f"{target.upper()}_REA_RAW_ROWS={len(raw_rows)} NORMALIZED_ROWS={len(normalized_rows)} DISPATCH_ABI_ROWS={dispatch_abi_rows} SELECTORS_MATCH=True DECODED_SHA_MATCH=True")
    print(f"{target.upper()}_EVIDENCE_ID={probe['evidence_id']} PROVIDER={probe['provider']['id']}@{probe['provider']['version']}")
    print(f"{target.upper()}_CONFIDENCE={probe['confidence']} AUTHORITY={probe['authority']} COMPLETENESS={normalized['discovery_completeness']} RUNTIME_EXECUTION={normalized['runtime_execution']}")
    print(f"{target.upper()}_DISPATCH_MOD_DIVISOR={bucket_count} TABLE_ENTRY_BYTES={entry_bytes} CODECOPY_DEST=0x1e THEN_MLOAD_JUMP=True")
    print(f"{target.upper()}_DISPATCH_TABLE_START={table_start:#x} ENTRIES={len(table_entries)} BYTES={table.hex()}")
    print(f"{target.upper()}_TABLE_TARGETS={','.join(f'{value:#06x}' for value in table_entries)} ALL_JUMPDESTS=True")
    print(f"{target.upper()}_SELECTOR_PUSH4_SITES={','.join(f'{selector}@{pc:#x}' for _, pc, selector in sites)}")
    print(f"{target.upper()}_SELECTOR_BUCKETS={','.join(f'{int(selector, 16) % bucket_count}:{selector}' for selector in sorted(method_selectors))}")

assert results["prague"][1] == results["london"][1]
assert results["prague"][0] != results["london"][0]
print("CROSS_TARGET_SELECTORS_IDENTICAL=True")
print("CROSS_TARGET_RUNTIME_BYTES_IDENTICAL=False")
