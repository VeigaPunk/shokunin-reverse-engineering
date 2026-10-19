#!/usr/bin/env python3
"""EX-04 (arc3-loop1-round4, C1) — independent verification of the compiled
CarrierV artifacts, with no compiler in the loop:

  * runtime hex -> bytes -> re-hex round-trip (the "extract runtime bytes" step)
  * creation code ends with the runtime code (locate the runtime as a suffix of
    the creation blob; constructor args, if any, would sit after it)
  * the recovered dispatch table matches the planted-K set derived pre-compile:
    every planted selector occurs in the runtime bytes, no ERC-20 selector does
  * `vyper -f method_identifiers` agrees with the planted-K set, and the ABI's
    own signature list hashes (keccak256, independent implementation) to the
    same selectors
  * JUMPDEST landing check on Vyper's dispatcher immediates (a Vyper dispatch
    shape reading; reported, not asserted as a Vyper invariant)

Usage: python3 verify-artifacts.py <work-dir> <planted-K.json>
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from keccak256 import keccak256  # noqa: E402  (local independent implementation)


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    work = Path(sys.argv[1]).resolve()
    planted_path = Path(sys.argv[2]).resolve()
    planted = json.loads(planted_path.read_text())
    K = planted["planted_selectors"]

    report = {"seat": "EX-04", "work_dir": str(work), "checks": {}, "findings": []}
    C = report["checks"]

    creation_hex = (work / "creation.hex").read_text().strip()
    runtime_hex = (work / "runtime.hex").read_text().strip()
    runtime_bin = (work / "runtime.bin").read_bytes()
    creation_bin = (work / "creation.bin").read_bytes()

    C["runtime_hex_chars"] = len(runtime_hex)
    C["runtime_bytes"] = len(runtime_bin)
    C["creation_hex_chars"] = len(creation_hex)
    C["creation_bytes"] = len(creation_bin)
    C["runtime_hex_even"] = len(runtime_hex) % 2 == 0
    C["runtime_bin_matches_hex"] = runtime_bin.hex() == runtime_hex.lower()
    C["runtime_sha256"] = sha256_file(work / "runtime.bin")
    C["runtime_hex_file_sha256"] = sha256_file(work / "runtime.hex")
    C["creation_sha256"] = sha256_file(work / "creation.bin")
    C["runtime_hex_sha256_of_bytes"] = hashlib.sha256(bytes.fromhex(runtime_hex)).hexdigest()

    # creation = constructor prologue + runtime (+ args); locate runtime as suffix
    idx = creation_hex.lower().rfind(runtime_hex.lower())
    C["runtime_found_in_creation"] = idx >= 0
    C["runtime_offset_in_creation_bytes"] = idx // 2 if idx >= 0 else None
    C["creation_tail_equals_runtime"] = creation_hex.lower().endswith(runtime_hex.lower())
    C["bytes_after_runtime_in_creation"] = (
        (len(creation_hex) - idx - len(runtime_hex)) // 2 if idx >= 0 else None
    )

    # selector membership in the runtime bytes (PUSH4 immediates)
    rt = bytes.fromhex(runtime_hex)
    C["planted_k"] = len(K)
    C["planted_present"] = sorted(s for s in K.values() if bytes.fromhex(s) in rt)
    C["planted_missing"] = sorted(s for s in K.values() if bytes.fromhex(s) not in rt)
    erc20 = planted["erc20_absent_check"]["selectors"]
    C["erc20_present_in_runtime"] = sorted(s for s in erc20.values() if bytes.fromhex(s) in rt)

    # independent ABI -> signature -> selector derivation
    abi = json.loads((work / "abi.json").read_text())
    sigs = []
    for item in abi:
        if item.get("type") != "function":
            continue
        ins = ",".join(i["type"] for i in item.get("inputs", []))
        sigs.append(f"{item['name']}({ins})")
    abi_sel = {f"{s}": keccak256(s.encode()).hex()[:8] for s in sigs}
    C["abi_function_count"] = len(sigs)
    C["abi_selector_set"] = sorted(abi_sel.values())
    C["abi_set_equals_planted"] = sorted(abi_sel.values()) == sorted(K.values())
    C["abi_minus_planted"] = sorted(set(abi_sel.values()) - set(K.values()))
    C["planted_minus_abi"] = sorted(set(K.values()) - set(abi_sel.values()))
    C["abi_nonfunction_items"] = sorted(
        {i.get("type") for i in abi if i.get("type") != "function"}
    )

    # vyper -f method_identifiers agreement
    mid = json.loads((work / "method-identifiers.json").read_text())
    C["method_identifiers"] = mid
    C["method_identifiers_match_abi"] = {
        k: v for k, v in mid.items()
    } == {k: v for k, v in abi_sel.items()} if set(mid) == set(abi_sel) else False
    C["method_identifiers_key_diff"] = {
        "only_in_method_identifiers": sorted(set(mid) - set(abi_sel)),
        "only_in_abi": sorted(set(abi_sel) - set(mid)),
    }

    # JUMPDEST landing on dispatcher immediates (Vyper shape reading)
    jumps = []
    for m in re.finditer(rb"\x61(..)\x14", rt):  # PUSH2 <imm> EQ
        jumps.append(int.from_bytes(m.group(1), "big"))
    landings = {hex(o): (o < len(rt) and rt[o] == 0x5B) for o in jumps}
    C["push2_eq_targets"] = {hex(o): landings[hex(o)] for o in jumps}
    C["all_push2_eq_targets_jumpdest"] = all(landings.values()) if jumps else None

    if C["planted_missing"]:
        report["findings"].append(f"planted selectors absent from runtime: {C['planted_missing']}")
    if C["erc20_present_in_runtime"]:
        report["findings"].append(f"ERC-20 selectors present: {C['erc20_present_in_runtime']}")
    if not C["abi_set_equals_planted"]:
        report["findings"].append("ABI-derived selector set != planted-K set")
    if not C["runtime_bin_matches_hex"]:
        report["findings"].append("runtime.bin does not match runtime.hex")
    if not C["runtime_found_in_creation"]:
        report["findings"].append("runtime code not found inside creation code")

    out = work / "verify-report.json"
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    print(f"wrote {out} sha256={sha256_file(out)}")
    return 1 if report["findings"] else 0


if __name__ == "__main__":
    sys.exit(main())
