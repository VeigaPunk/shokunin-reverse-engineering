#!/usr/bin/env python3
import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])
OPCODES = {
    0x03: "SUB", 0x10: "LT", 0x11: "GT", 0x14: "EQ", 0x15: "ISZERO",
    0x1c: "SHR", 0x35: "CALLDATALOAD", 0x36: "CALLDATASIZE",
    0x57: "JUMPI", 0x5b: "JUMPDEST", 0x80: "DUP1", 0xfd: "REVERT",
}


def decode(data):
    ins = []
    pc = 0
    while pc < len(data):
        start = pc
        op = data[pc]
        pc += 1
        if op == 0x5f:
            name, immediate = "PUSH0", None
        elif 0x60 <= op <= 0x7f:
            width = op - 0x5f
            immediate = data[pc:pc + width]
            if len(immediate) != width:
                raise ValueError(f"truncated PUSH{width} at pc={start}")
            name = f"PUSH{width}"
            pc += width
        else:
            name, immediate = OPCODES.get(op, f"OP_{op:02X}"), None
        ins.append((start, name, int.from_bytes(immediate, "big") if immediate is not None else None))
    return ins


def sha(data):
    return hashlib.sha256(data).hexdigest()


def census(folder, probe_path):
    code = (folder / "runtime.bin").read_bytes()
    abi = json.loads((folder / "abi.json").read_text())
    method_ids = json.loads((folder / "method-identifiers.json").read_text())
    derived = json.loads((folder / "selectors-derived.json").read_text())
    abi_funcs = [entry for entry in abi if entry.get("type") == "function"]
    derived_pairs = {selector for _signature, selector in derived}
    method_set = set(method_ids.values())
    meta_len = int.from_bytes(code[-2:], "big")
    meta_start = len(code) - meta_len - 2
    instructions = decode(code[:meta_start])
    names = [entry[1] for entry in instructions]
    prologue = next((i for i in range(len(instructions) - 3)
                     if names[i:i + 4] == ["PUSH0", "CALLDATALOAD", "PUSH1", "SHR"]
                     and instructions[i + 2][2] == 0xe0), None)
    if prologue is None:
        raise ValueError(f"selector prologue absent: {folder}")
    comparisons = []
    for i in range(prologue + 4, len(instructions) - 3):
        a, b, c, d = instructions[i:i + 4]
        if a[1] == "PUSH4" and b[1] in {"EQ", "GT", "SUB"} and c[1] == "PUSH2" and d[1] == "JUMPI":
            comparisons.append({"pc": a[0], "selector": f"{a[2]:08x}", "compare": b[1], "target": c[2]})
    guard_patterns = []
    for i in range(len(instructions) - 5):
        window = instructions[i:i + 6]
        if (window[0][1] == "PUSH1" and window[0][2] == 4
                and [item[1] for item in window[1:4]] == ["CALLDATASIZE", "LT", "ISZERO"]
                and window[4][1] == "PUSH2" and window[5][1] == "JUMPI"):
            guard_patterns.append({"pc": window[0][0], "kind": "LT;ISZERO"})
        if (window[0][1] == "PUSH1" and window[0][2] == 4
                and [item[1] for item in window[1:3]] == ["CALLDATASIZE", "LT"]
                and window[3][1] == "PUSH2" and window[4][1] == "JUMPI"):
            guard_patterns.append({"pc": window[0][0], "kind": "LT"})
    selectors = [item["selector"] for item in comparisons]
    probe = json.loads(probe_path.read_text()) if probe_path else None
    record = {
        "runtime_bytes": len(code),
        "runtime_sha256": sha(code),
        "metadata_start": meta_start,
        "metadata_length": meta_len,
        "metadata_and_length_sha256": sha(code[meta_start:]),
        "pre_metadata_sha256": sha(code[:meta_start]),
        "prologue_pc": instructions[prologue][0],
        "guard_patterns": guard_patterns,
        "abi_functions": len(abi_funcs),
        "method_identifier_count": len(method_ids),
        "derived_selector_count": len(derived_pairs),
        "derived_equals_method_ids": derived_pairs == method_set,
        "dispatch_compare_counts": {name: sum(item["compare"] == name for item in comparisons)
                                     for name in sorted({item["compare"] for item in comparisons})},
        "dispatch_comparison_sites": len(comparisons),
        "dispatch_distinct_selectors": len(set(selectors)),
        "dispatch_selectors_sorted": selectors == sorted(selectors),
        "dispatch_equals_method_ids": set(selectors) == method_set,
        "dispatch_rows": comparisons,
    }
    if probe is not None:
        normalized = probe.get("normalized_result", {})
        rows = normalized.get("functions", [])
        found = {row.get("selector", "").removeprefix("0x") for row in rows}
        record["rea"] = {
            "evidence_id": probe.get("evidence_id"),
            "provider": probe.get("provider"),
            "confidence": probe.get("confidence"),
            "authority": probe.get("authority"),
            "function_count": len(rows),
            "selectors_equal_method_ids": found == method_set,
            "decoded_sha256": normalized.get("bytecode", {}).get("sha256"),
            "decoded_sha_equals_runtime": normalized.get("bytecode", {}).get("sha256") == sha(code),
            "runtime_execution": normalized.get("runtime_execution"),
        }
    return record


legs = {
    "solc_0_8_28_viaIR": (ROOT / "out" / "viair-opt200", ROOT / "probe-028-viair-opt200.json"),
    "solc_0_8_28_standard": (ROOT / "out" / "std-opt200", ROOT / "probe-028-std-opt200.json"),
    "solc_0_8_37_viaIR": (ROOT / "out-0837" / "viair-opt200", ROOT / "probe-0837-viair-opt200.json"),
}
results = {name: census(folder, probe) for name, (folder, probe) in legs.items()}
a = legs["solc_0_8_28_viaIR"][0] / "runtime.bin"
b = legs["solc_0_8_37_viaIR"][0] / "runtime.bin"
code_a, code_b = a.read_bytes(), b.read_bytes()
ra, rb = results["solc_0_8_28_viaIR"], results["solc_0_8_37_viaIR"]
sa, sb = ra["metadata_start"], rb["metadata_start"]
results["cross_version_viaIR"] = {
    "source_sha256": sha((ROOT / "src" / "ViaIrVault.sol").read_bytes()),
    "runtime_lengths_equal": len(code_a) == len(code_b),
    "metadata_starts_equal": sa == sb,
    "pre_metadata_byte_equal": code_a[:sa] == code_b[:sb],
    "first_pre_metadata_difference": next((i for i, (x, y) in enumerate(zip(code_a[:sa], code_b[:sb])) if x != y), None),
}
print(json.dumps(results, sort_keys=True, indent=2))
