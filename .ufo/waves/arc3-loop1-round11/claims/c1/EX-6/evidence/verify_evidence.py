import hashlib
import json
from collections import Counter
from pathlib import Path

root = Path(__file__).resolve().parent

def read_runtime(fork):
    return bytes.fromhex((root / "compiled" / f"BlobFork-{fork}.runtime.hex").read_text().strip().removeprefix("0x"))

def decode_code(raw):
    pc = 0
    first_push2_value = None
    first_push2_pc = None
    while pc < len(raw):
        opcode = raw[pc]
        size = opcode - 0x5f if 0x60 <= opcode <= 0x7f else 0
        immediate = raw[pc + 1:pc + 1 + size]
        if len(immediate) != size:
            raise ValueError(f"truncated PUSH at pc={pc}")
        if opcode == 0x61 and first_push2_value is None:
            first_push2_pc = pc
            first_push2_value = int.from_bytes(immediate, "big")
            break
        pc += 1 + size
    if first_push2_value is None or first_push2_value >= len(raw):
        raise ValueError("missing in-range first PUSH2 immediate")
    code = raw[:first_push2_value]
    pc = 0
    counts = Counter()
    push4 = []
    while pc < len(code):
        opcode = code[pc]
        size = opcode - 0x5f if 0x60 <= opcode <= 0x7f else 0
        immediate = code[pc + 1:pc + 1 + size]
        if len(immediate) != size:
            raise ValueError(f"truncated PUSH at pc={pc}")
        counts[opcode] += 1
        if opcode == 0x63:
            push4.append((pc, immediate.hex()))
        pc += 1 + size
    if pc != first_push2_value:
        raise ValueError("opcode walk did not end at the PUSH2-provided boundary")
    return first_push2_pc, first_push2_value, counts, push4

records = {}
for fork in ("cancun", "prague"):
    stem = root / "compiled" / f"BlobFork-{fork}"
    raw = read_runtime(fork)
    repeated = bytes.fromhex((root / "compiled" / f"BlobFork-{fork}.runtime.repeat.hex").read_text().strip().removeprefix("0x"))
    abi = json.loads((root / "compiled" / f"BlobFork-{fork}.abi").read_text())
    method_ids = json.loads((root / "compiled" / f"BlobFork-{fork}.method_identifiers").read_text())
    settings = json.loads((root / "compiled" / f"BlobFork-{fork}.settings").read_text())
    rea = json.loads((root / f"probe-{fork}.json").read_text())
    first_push2_pc, base, counts, push4 = decode_code(raw)
    expected = {value.removeprefix("0x").lower() for value in method_ids.values()}
    actual = {selector for _, selector in push4}
    observed = {row["selector"].lower() for row in rea["raw_result"]["functions"]}
    decoded = rea["normalized_result"]["bytecode"]
    if raw != repeated or settings.get("evm_version") != fork:
        raise AssertionError(f"compile identity mismatch for {fork}")
    if len(abi) != len(method_ids) or actual != expected or observed != expected:
        raise AssertionError(f"selector/ABI mismatch for {fork}")
    if decoded.get("sha256") != hashlib.sha256(raw).hexdigest() or decoded.get("bytes") != len(raw):
        raise AssertionError(f"REA decoded identity mismatch for {fork}")
    records[fork] = {
        "raw": raw,
        "expected": expected,
        "abi": abi,
        "rea": rea,
        "first_push2_pc": first_push2_pc,
        "copy_base": base,
        "suffix_hex": raw[base:].hex(),
        "push4": push4,
        "counts": counts,
    }
    print(f"{fork}: runtime_bytes={len(raw)} runtime_sha256={hashlib.sha256(raw).hexdigest()} repeated_identical={raw == repeated}")
    print(f"{fork}: settings={json.dumps(settings, sort_keys=True)} abi_functions={len(abi)} selectors_match_push4_and_rea=True")
    print(f"{fork}: push2_pc={first_push2_pc} copy_base=0x{base:04x} suffix_bytes={len(raw[base:])} suffix_hex={raw[base:].hex()}")
    print(f"{fork}: opcode_counts PUSH4={counts[0x63]} XOR={counts[0x18]} AND={counts[0x16]} MOD={counts[0x06]} BLOBHASH={counts[0x49]} BLOBBASEFEE={counts[0x4a]}")
    print(f"{fork}: push4_sites={json.dumps(push4)} REA_id={rea['evidence_id']} rea_function_count={len(observed)} rea_decoded_sha256={decoded['sha256']}")

if records["cancun"]["raw"] != records["prague"]["raw"]:
    raise AssertionError("Cancun and Prague runtime bytes differ")
print("cancun_prague_runtime_identical=True")
for fork, record in records.items():
    abi_by_name = {item["name"]: item for item in record["abi"]}
    rea_by_selector = {item["selector"].lower(): item for item in record["rea"]["raw_result"]["functions"]}
    selector = next(value.removeprefix("0x").lower() for key, value in json.loads((root / "compiled" / f"BlobFork-{fork}.method_identifiers").read_text()).items() if key == "blob_hash(uint256)")
    print(f"{fork}: blob_hash_abi_mutability={abi_by_name['blob_hash']['stateMutability']} rea_inferred_mutability={rea_by_selector[selector]['stateMutability']} selector={selector}")
    normalized = record["rea"]["normalized_result"]
    print(f"{fork}: discovery_completeness={normalized['discovery_completeness']} runtime_execution={normalized['runtime_execution']} tool_hardfork={normalized['bytecode']['hardfork']}")
