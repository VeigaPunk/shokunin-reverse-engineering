#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent / "evidence"
MODES = ("noopt", "none")


def read(name):
    return (HERE / name).read_bytes()


def decode_hex(name):
    text = read(name).decode("ascii").strip()
    if text.startswith("0x"):
        text = text[2:]
    return bytes.fromhex(text)


def load_json(name):
    return json.loads(read(name))


runtimes = {mode: read(f"{mode}.runtime.hex") for mode in MODES}
bytecode = {mode: decode_hex(f"{mode}.runtime.hex") for mode in MODES}
abis = {mode: read(f"{mode}.abi.json") for mode in MODES}
method_files = {mode: read(f"{mode}.methodids.json") for mode in MODES}
settings_files = {mode: read(f"{mode}.settings.json") for mode in MODES}
probes = {mode: load_json(f"{mode}.probe.json") for mode in MODES}
method_ids = {mode: load_json(f"{mode}.methodids.json") for mode in MODES}
abis_json = {mode: load_json(f"{mode}.abi.json") for mode in MODES}

assert runtimes["noopt"] == runtimes["none"]
assert bytecode["noopt"] == bytecode["none"]
assert abis["noopt"] == abis["none"]
assert method_files["noopt"] == method_files["none"]
assert settings_files["noopt"] == settings_files["none"]
assert all(json.loads(settings_files[mode])["optimize"] == "none" for mode in MODES)

expected = {value.removeprefix("0x").lower() for value in method_ids["noopt"].values()}
abi_signatures = {
    entry["name"] + "(" + ",".join(arg["type"] for arg in entry["inputs"]) + ")"
    for entry in abis_json["noopt"]
    if entry.get("type") == "function"
}
assert len(abi_signatures) == len(abis_json["noopt"]) == len(expected) == 8
assert method_ids["none"] == method_ids["noopt"]

result_rows = {}
for mode in MODES:
    probe = probes[mode]
    normalized = probe["normalized_result"]
    raw_functions = probe["raw_result"]["functions"]
    functions = normalized["functions"]
    selectors = {item["selector"].removeprefix("0x").lower() for item in functions}
    raw_selectors = {item["selector"].lower() for item in raw_functions}
    assert len(functions) == len(raw_functions) == 8
    assert selectors == raw_selectors == expected
    assert all(item["dispatch"] == "abi" for item in functions)
    assert normalized["bytecode"]["sha256"] == hashlib.sha256(bytecode[mode]).hexdigest()
    assert normalized["bytecode"]["bytes"] == len(bytecode[mode])
    result_rows[mode] = {
        "evidence_id": probe["evidence_id"],
        "provider": probe["provider"]["id"],
        "provider_version": probe["provider"]["version"],
        "raw_functions": raw_functions,
        "functions": functions,
        "bytecode_sha256": normalized["bytecode"]["sha256"],
        "bytecode_bytes": normalized["bytecode"]["bytes"],
        "runtime_execution": normalized["runtime_execution"],
        "confidence": probe["confidence"],
        "authority": probe["authority"],
    }

assert result_rows["noopt"]["raw_functions"] == result_rows["none"]["raw_functions"]
assert result_rows["noopt"]["functions"] == result_rows["none"]["functions"]
assert result_rows["noopt"]["bytecode_sha256"] == result_rows["none"]["bytecode_sha256"]

print("fixture=K8.vy (8 external functions), source_sha256=" + hashlib.sha256(read("K8.vy")).hexdigest())
print("compiler=Vyper 0.4.3+commit.bff19ea2; compiler_sha256=615f792c6bc1bdf87cbc4612420a331ec108246d9debadbb3f3b9efa8209dd10")
for mode in MODES:
    print(f"{mode}_settings={json.loads(settings_files[mode])}")
    print(f"{mode}_runtime_hex_file_sha256={hashlib.sha256(runtimes[mode]).hexdigest()}")
    print(f"{mode}_runtime_decoded_bytes={len(bytecode[mode])}")
    print(f"{mode}_runtime_decoded_sha256={hashlib.sha256(bytecode[mode]).hexdigest()}")
    row = result_rows[mode]
    print(f"{mode}_REA={row['provider']} {row['provider_version']} id={row['evidence_id']}")
    print(f"{mode}_REA_rows={len(row['raw_functions'])}/{len(row['functions'])}; selectors_match_compiler={set(item['selector'].removeprefix('0x').lower() for item in row['functions']) == expected}; all_dispatch_abi={all(item['dispatch'] == 'abi' for item in row['functions'])}")
    print(f"{mode}_REA_decoded_sha256={row['bytecode_sha256']} bytes={row['bytecode_bytes']}; confidence={row['confidence']}; authority={row['authority']}; runtime_execution={row['runtime_execution']}")
print("ABI_function_count=8; method_identifier_count=8; compiler_selector_set=" + ",".join(sorted(expected)))
print("byte_exact_equal_runtime_abi_methodids_settings=True")
print("byte_exact_equal_REA_function_payloads=True")
print("inference_note=all 8 ABI mutabilities are view; REA infers payable for all 8; static inference only")
