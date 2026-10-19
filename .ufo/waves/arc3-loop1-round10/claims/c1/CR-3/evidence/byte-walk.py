import hashlib
import json
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])
rea_version = (root / "rea-version.txt").read_text().strip()
for target in ("london", "prague"):
    out = root / "out" / target
    code_text = (out / "runtime.hex").read_text().strip()
    if code_text.startswith("0x"):
        code_text = code_text[2:]
    code = bytes.fromhex(code_text)
    abi = json.loads((out / "abi.json").read_text())
    method_ids = json.loads((out / "method-identifiers.json").read_text())
    settings = json.loads((out / "settings.json").read_text())
    selectors = {value.removeprefix("0x").lower() for value in method_ids.values()}
    abi_selectors = len([item for item in abi if item.get("type") == "function"])
    table_match = re.search(rb"\x61(.{2})\x01\x60\x1e\x39", code[:48])
    bucket_match = re.search(rb"\x60\x02\x60([\x01-\x7f])\x82\x06", code[:32])
    if table_match is None or bucket_match is None:
        raise SystemExit(f"{target}: dispatch table pattern not found")
    table_start = int.from_bytes(table_match.group(1), "big")
    bucket_count = bucket_match.group(1)[0]
    table_end = table_start + 2 * bucket_count
    if table_end != len(code):
        raise SystemExit(f"{target}: table range {table_start}:{table_end} does not end at {len(code)}")
    entries = [int.from_bytes(code[i:i + 2], "big") for i in range(table_start, table_end, 2)]
    push4_sites = []
    pc = 0
    while pc < table_start:
        opcode_pc = pc
        opcode = code[pc]
        pc += 1
        if 0x60 <= opcode <= 0x7f:
            width = opcode - 0x5f
            immediate = code[pc:pc + width]
            if len(immediate) != width:
                raise SystemExit(f"{target}: truncated PUSH at {opcode_pc}")
            if opcode == 0x63:
                push4_sites.append((opcode_pc, immediate.hex(), code[pc + width:pc + width + 5].hex()))
            pc += width
    push4_selectors = {selector for _, selector, _ in push4_sites}
    push4_pcs = {selector: pc for pc, selector, _ in push4_sites}
    selector_bucket = {}
    for selector in sorted(selectors):
        bucket = int(selector, 16) % bucket_count
        selector_bucket[selector] = {
            "bucket": bucket,
            "entry": entries[bucket],
            "entry_is_jumpdest": code[entries[bucket]] == 0x5b,
        }
    rea = json.loads((root / "probe" / f"{target}.json").read_text())
    raw_functions = rea["raw_result"]["functions"]
    rea_selectors = {fn["selector"].removeprefix("0x").lower() for fn in raw_functions}
    rea_offsets = {fn["selector"].removeprefix("0x").lower(): fn["bytecodeOffset"] for fn in raw_functions}
    offset_map = {
        selector: {
            "push4_pc": push4_pcs[selector],
            "REA_bytecodeOffset": rea_offsets[selector],
            "push4_pc_plus_11": push4_pcs[selector] + 11,
        }
        for selector in sorted(selectors)
    }
    bytecode = rea["normalized_result"]["bytecode"]
    occupied_buckets = sorted({item["bucket"] for item in selector_bucket.values()})
    table_entries_are_jumpdests = all(code[target_pc] == 0x5b for target_pc in entries)
    xor_compare_sites = all(after.startswith("811861") for _, _, after in push4_sites)
    print(json.dumps({
        "target": target,
        "settings": settings,
        "runtime_bytes": len(code),
        "runtime_sha256": hashlib.sha256(code).hexdigest(),
        "abi_functions": abi_selectors,
        "method_identifiers": len(selectors),
        "REA_version": rea_version,
        "REA_evidence_id": rea["evidence_id"],
        "REA_provider": rea["provider"]["id"],
        "REA_provider_version": rea["provider"]["version"],
        "REA_rows": len(raw_functions),
        "REA_selector_set_matches_compiler": rea_selectors == selectors,
        "REA_decoded_sha256_matches_compiler": bytecode["sha256"] == hashlib.sha256(code).hexdigest(),
        "REA_discovery_completeness": rea["normalized_result"].get("discovery_completeness"),
        "REA_runtime_execution": rea["normalized_result"].get("runtime_execution"),
        "prefix_hex": code[:26].hex(),
        "table_start": table_start,
        "table_buckets": bucket_count,
        "table_bytes": code[table_start:table_end].hex(),
        "table_entries": entries,
        "table_entries_are_jumpdests": table_entries_are_jumpdests,
        "occupied_buckets": occupied_buckets,
        "empty_buckets": [index for index in range(bucket_count) if index not in occupied_buckets],
        "push4_sites_before_table": push4_sites,
        "xor_compare_sites": xor_compare_sites,
        "push4_selector_set_matches_compiler": push4_selectors == selectors,
        "REA_offsets_equal_push4_pc_plus_11": all(item["REA_bytecodeOffset"] == item["push4_pc_plus_11"] for item in offset_map.values()),
        "offset_map": offset_map,
        "selector_bucket_map": selector_bucket,
    }, sort_keys=True))
