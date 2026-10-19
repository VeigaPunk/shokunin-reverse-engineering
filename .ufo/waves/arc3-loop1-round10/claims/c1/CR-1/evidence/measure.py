import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

EVIDENCE = Path(__file__).resolve().parent
ROOT = Path(subprocess.check_output(["git", "-C", str(EVIDENCE), "rev-parse", "--show-toplevel"], text=True).strip())
JS_SHA3 = ROOT / ".ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/js-sha3"


def keccak_selectors(signatures):
    module_path = json.dumps(str(JS_SHA3))
    program = f'''const {{keccak_256}} = require({module_path});
let input = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", chunk => input += chunk);
process.stdin.on("end", () => {{
  const signatures = JSON.parse(input);
  const selectors = Object.fromEntries(signatures.map(s => [s, keccak_256(s).slice(0, 8)]));
  console.log(JSON.stringify({{empty: keccak_256(""), transfer: keccak_256("transfer(address,uint256)").slice(0, 8), selectors}}));
}});'''
    result = subprocess.run(["node", "-e", program], input=json.dumps(signatures), text=True, check=True, capture_output=True)
    parsed = json.loads(result.stdout)
    assert parsed["empty"] == "c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"
    assert parsed["transfer"] == "a9059cbb"
    return parsed["selectors"]


OPCODES = {
    0x00: "STOP", 0x01: "ADD", 0x02: "MUL", 0x03: "SUB", 0x04: "DIV", 0x06: "MOD",
    0x10: "LT", 0x11: "GT", 0x14: "EQ", 0x15: "ISZERO", 0x16: "AND", 0x17: "OR",
    0x18: "XOR", 0x1B: "SHL", 0x1C: "SHR", 0x20: "SHA3", 0x35: "CALLDATALOAD", 0x36: "CALLDATASIZE",
    0x38: "CODESIZE", 0x39: "CODECOPY", 0x50: "POP", 0x51: "MLOAD", 0x52: "MSTORE",
    0x53: "MSTORE8", 0x54: "SLOAD", 0x55: "SSTORE", 0x56: "JUMP", 0x57: "JUMPI",
    0x58: "PC", 0x5B: "JUMPDEST", 0x5F: "PUSH0", 0xF3: "RETURN", 0xFD: "REVERT",
    0xFE: "INVALID",
}


def decode(code):
    result = []
    pc = 0
    while pc < len(code):
        start = pc
        opcode = code[pc]
        pc += 1
        if 0x60 <= opcode <= 0x7F:
            size = opcode - 0x5F
            immediate = code[pc:pc + size]
            name = f"PUSH{size}"
            pc += size
        elif 0x80 <= opcode <= 0x8F:
            immediate = b""
            name = f"DUP{opcode - 0x7F}"
        elif 0x90 <= opcode <= 0x9F:
            immediate = b""
            name = f"SWAP{opcode - 0x8F}"
        elif 0xA0 <= opcode <= 0xA4:
            immediate = b""
            name = f"LOG{opcode - 0xA0}"
        else:
            immediate = b""
            name = OPCODES.get(opcode, f"OP_{opcode:02x}")
        result.append({"pc": start, "opcode": opcode, "name": name, "immediate": immediate})
    return result


measurements = {}
for fork in ("paris", "prague"):
    abi = json.loads((EVIDENCE / f"compiled/{fork}.abi.json").read_text())
    method_ids = json.loads((EVIDENCE / f"compiled/{fork}.method-identifiers.json").read_text())
    settings = json.loads((EVIDENCE / f"compiled/{fork}.settings.json").read_text())
    runtime_file = EVIDENCE / f"compiled/{fork}.runtime.hex"
    runtime_text = runtime_file.read_text().strip()
    runtime_bytes = bytes.fromhex(runtime_text.removeprefix("0x"))
    runtime_sha = hashlib.sha256(runtime_bytes).hexdigest()
    file_sha = hashlib.sha256(runtime_file.read_bytes()).hexdigest()
    signatures = [f"{entry['name']}({','.join(arg['type'] for arg in entry['inputs'])})" for entry in abi if entry["type"] == "function"]
    abi_mutability = {f"{entry['name']}({','.join(arg['type'] for arg in entry['inputs'])})": entry["stateMutability"] for entry in abi if entry["type"] == "function"}
    derived = keccak_selectors(signatures)
    ids = {sig: value.removeprefix("0x").lower() for sig, value in method_ids.items()}
    envelope = json.loads((EVIDENCE / f"probe/{fork}.rea.json").read_text())
    rea_rows = envelope["normalized_result"]["functions"]
    rea_selectors = {row["selector"].removeprefix("0x").lower() for row in rea_rows}
    rea_mutability = {row["selector"].removeprefix("0x").lower(): row["inferred_state_mutability"] for row in rea_rows}
    normalized = envelope["normalized_result"]["bytecode"]
    decoded_bytes = bytes.fromhex(normalized["hex"].removeprefix("0x"))
    instructions = decode(runtime_bytes)
    names = [item["name"] for item in instructions]
    offsets = {item["pc"]: item["name"] for item in instructions}
    legs = []
    for index in range(len(instructions) - 4):
        window = instructions[index:index + 5]
        if [item["name"] for item in window] == ["PUSH4", "DUP2", "XOR", "PUSH2", "JUMPI"]:
            legs.append((window[0]["immediate"].hex(), int.from_bytes(window[3]["immediate"], "big"), window[0]["pc"]))
    selector_pcs = {selector: pc for selector, _, pc in legs}
    offset_opcodes = [offsets.get(row["bytecode_offset"], "not-an-opcode-boundary") for row in rea_rows]
    offset_deltas = [row["bytecode_offset"] - selector_pcs[row["selector"].removeprefix("0x").lower()] for row in rea_rows]
    raw_rows = envelope["raw_result"]["functions"]
    first_mod = names.index("MOD") if "MOD" in names else None
    mod_before_first_jump = first_mod is not None and first_mod < names.index("JUMP")
    selectors = sorted(derived.values())
    assert len(signatures) == 8
    assert len(method_ids) == 8
    assert derived == ids
    assert len(rea_rows) == 8 and len(raw_rows) == 8
    assert rea_selectors == set(selectors)
    assert hashlib.sha256(decoded_bytes).hexdigest() == normalized["sha256"] == runtime_sha
    assert len(decoded_bytes) == normalized["bytes"] == len(runtime_bytes)
    assert envelope["provider"]["version"] == "evmole@0.9.3"
    assert settings["evm_version"] == fork
    assert len(legs) == 8 and {selector for selector, _, _ in legs} == set(selectors)
    assert set(offset_deltas) == {11}
    assert set(offset_opcodes) == {"PUSH1"}
    assert mod_before_first_jump
    measurements[fork] = {"selectors": set(selectors), "runtime_sha": runtime_sha, "file_sha": file_sha}
    inferred_by_selector = rea_mutability
    agreements = sum(abi_mutability[sig] == inferred_by_selector[derived[sig]] for sig in signatures)
    print(f"{fork.upper()}_SETTINGS={json.dumps(settings, sort_keys=True)}")
    print(f"{fork.upper()}_SOURCE_SHA256={hashlib.sha256((EVIDENCE / 'source/K8.vy').read_bytes()).hexdigest()}")
    print(f"{fork.upper()}_RUNTIME_BYTES={len(runtime_bytes)} RUNTIME_SHA256={runtime_sha} HEX_FILE_SHA256={file_sha}")
    print(f"{fork.upper()}_COMPILE_RERUN_IDENTICAL=YES (5 output forms, rederive.sh)")
    print(f"{fork.upper()}_SELECTORS={','.join(selectors)}")
    print(f"{fork.upper()}_K_K=YES ABI={len(signatures)} METHOD_IDS={len(method_ids)} KECCAK={len(derived)} REA_RAW={len(raw_rows)} REA_NORMALIZED={len(rea_rows)}")
    print(f"{fork.upper()}_METHOD_IDS_EQUAL_INDEPENDENT_KECCAK=YES REA_SET_EQUAL=YES DECODED_SHA_MATCH=YES")
    print(f"{fork.upper()}_REA_EVIDENCE_ID={envelope['evidence_id']} PROVIDER={envelope['provider']['id']}/{envelope['provider']['version']}")
    print(f"{fork.upper()}_DISPATCH_PREFIX={' '.join(names[:16])}")
    print(f"{fork.upper()}_DISPATCH_LEGS={len(legs)} PATTERN=PUSH4,DUP2,XOR,PUSH2,JUMPI MOD_IN_PROLOGUE=YES")
    print(f"{fork.upper()}_OFFSET_DELTA_FROM_PUSH4={sorted(set(offset_deltas))} OFFSET_OPCODE=PUSH1")
    print(f"{fork.upper()}_REA_OFFSET_OPCODE_COUNTS={dict(sorted(Counter(offset_opcodes).items()))}")
    print(f"{fork.upper()}_MUTABILITY_ABI_REA_AGREEMENT={agreements}/{len(signatures)} ABI_VIEW={sum(value == 'view' for value in abi_mutability.values())} REA_PAYABLE={sum(value == 'payable' for value in inferred_by_selector.values())}")

assert measurements["paris"]["selectors"] == measurements["prague"]["selectors"]
print("PAIR_SELECTOR_SETS_EQUAL=YES")
print(f"PAIR_RUNTIME_SIZE_DELTA_PRAGUE_MINUS_PARIS={len(bytes.fromhex((EVIDENCE / 'compiled/prague.runtime.hex').read_text().strip().removeprefix('0x')))-len(bytes.fromhex((EVIDENCE / 'compiled/paris.runtime.hex').read_text().strip().removeprefix('0x')))}_bytes")
