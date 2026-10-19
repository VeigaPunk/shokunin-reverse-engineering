import hashlib
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
compile_dir = root / "compile"
probe_dir = root / "probe"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def runtime(mode):
    text = (compile_dir / f"{mode}.runtime.hex").read_text().strip()
    if text.startswith("0x"):
        text = text[2:]
    return bytes.fromhex(text)


def load_json(path):
    return json.loads(path.read_text())


def function_payload(probe):
    return sorted(
        (
            item.get("selector", "").lower().removeprefix("0x"),
            item.get("bytecode_offset"),
            item.get("dispatch"),
            item.get("inferred_arguments"),
            item.get("inferred_state_mutability"),
        )
        for item in probe["normalized_result"]["functions"]
    )


def selector_set(probe):
    return sorted(item[0] for item in function_payload(probe))


modes = ("noopt", "none")
runtimes = {mode: runtime(mode) for mode in modes}
probes = {mode: load_json(probe_dir / f"{mode}.json") for mode in modes}
abis = {mode: load_json(compile_dir / f"{mode}.abi.json") for mode in modes}
methodids = {mode: load_json(compile_dir / f"{mode}.methodids.json") for mode in modes}
settings = {mode: load_json(compile_dir / f"{mode}.settings.json") for mode in modes}

for mode in modes:
    normalized = probes[mode]["normalized_result"]
    decoded = normalized["bytecode"]
    raw_functions = probes[mode]["raw_result"]["functions"]
    assert decoded["sha256"] == digest(runtimes[mode])
    assert decoded["bytes"] == len(runtimes[mode])
    assert len(normalized["functions"]) == len(raw_functions)

assert runtimes["noopt"] == runtimes["none"]
assert abis["noopt"] == abis["none"]
assert methodids["noopt"] == methodids["none"]
assert settings["noopt"] == settings["none"]
assert function_payload(probes["noopt"]) == function_payload(probes["none"])
assert probes["noopt"]["raw_result"]["functions"] == probes["none"]["raw_result"]["functions"]

compiled_selectors = {
    value.lower().removeprefix("0x")
    for value in methodids["noopt"].values()
}
for mode in modes:
    assert set(selector_set(probes[mode])) == compiled_selectors
    assert probes[mode]["provider"]["id"] == "evmole-interface"
    assert probes[mode]["normalized_result"]["runtime_execution"] == "not-performed"

identity = (root / "identity.txt").read_text().splitlines()
source_path = next(line.split("=", 1)[1] for line in identity if line.startswith("source_path="))
compiler_path = next(line.split("=", 1)[1] for line in identity if line.startswith("compiler_path="))
source_hash = next(line.split()[0] for line in identity if line.split()[-1] == source_path)
compiler_hash = next(line.split()[0] for line in identity if line.split()[-1] == compiler_path)
compiler_version = next(line for line in identity if "+commit." in line)

print(f"SOURCE_SHA256={source_hash}")
print(f"VYPER_LAUNCHER_SHA256={compiler_hash}")
print(f"VYPER_VERSION={compiler_version}")
for mode in modes:
    print(f"{mode.upper()}_RUNTIME_BYTES={len(runtimes[mode])} DECODED_SHA256={digest(runtimes[mode])}")
    print(f"{mode.upper()}_ABI_FUNCTIONS={sum(item.get('type') == 'function' for item in abis[mode])}")
    print(f"{mode.upper()}_METHOD_IDENTIFIERS={len(methodids[mode])}")
    print(f"{mode.upper()}_SETTINGS={json.dumps(settings[mode], sort_keys=True, separators=(',', ':'))}")
    print(f"{mode.upper()}_REA_EVIDENCE_ID={probes[mode]['evidence_id']}")
    print(f"{mode.upper()}_REA_PROVIDER={probes[mode]['provider']['id']} VERSION={probes[mode]['provider']['version']}")
    print(f"{mode.upper()}_REA_ROWS={len(probes[mode]['normalized_result']['functions'])} RAW_ROWS={len(probes[mode]['raw_result']['functions'])}")
    print(f"{mode.upper()}_REA_DECODED_SHA_MATCH={probes[mode]['normalized_result']['bytecode']['sha256'] == digest(runtimes[mode])}")
    print(f"{mode.upper()}_REA_SELECTOR_METHODID_MATCH={set(selector_set(probes[mode])) == compiled_selectors}")
    print(f"{mode.upper()}_REA_CONFIDENCE={probes[mode]['confidence']} AUTHORITY={probes[mode]['authority']} RUNTIME_EXECUTION={probes[mode]['normalized_result']['runtime_execution']}")
print(f"RUNTIME_BYTE_IDENTICAL={runtimes['noopt'] == runtimes['none']}")
print(f"ABI_IDENTICAL={abis['noopt'] == abis['none']}")
print(f"METHOD_IDENTIFIERS_IDENTICAL={methodids['noopt'] == methodids['none']}")
print(f"SETTINGS_IDENTICAL={settings['noopt'] == settings['none']}")
print(f"REA_FUNCTION_PAYLOAD_IDENTICAL={function_payload(probes['noopt']) == function_payload(probes['none'])}")
print(f"REA_RAW_FUNCTIONS_IDENTICAL={probes['noopt']['raw_result']['functions'] == probes['none']['raw_result']['functions']}")
print(f"REA_SELECTORS={','.join(selector_set(probes['noopt']))}")
print("SCOPE=synthetic K8.vy bytes; Vyper 0.4.3 CLI launcher/version recorded; REA static inference, no execution")
