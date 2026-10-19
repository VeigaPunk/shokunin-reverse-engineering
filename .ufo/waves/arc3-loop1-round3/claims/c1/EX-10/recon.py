#!/usr/bin/env python3
"""EX-10 seat (arc3-loop1-round3, chain c1): carrier-B independent reconciliation.

Own linear-sweep disassembler + dispatch parser (linear chain and GT/EQ
binary-search shapes) + keccak scan, reconciled against the planted set, the
solc ABI, and any probe envelopes passed on the command line.

Usage:
  recon.py <runtime.bin> <planted-K.json> <abi.json> [probe.json ...]
Writes JSON to stdout.
"""
import hashlib
import json
import sys

from keccak import keccak256

CMP = {0x10: "LT", 0x11: "GT", 0x14: "EQ"}


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def disasm(code: bytes):
    ops = []
    pc = 0
    while pc < len(code):
        op = code[pc]
        if 0x60 <= op <= 0x7F:
            n = op - 0x5F
            imm = code[pc + 1:pc + 1 + n]
            ops.append((pc, op, imm, int.from_bytes(imm, "big") if len(imm) == n else None))
            pc += 1 + n
        else:
            ops.append((pc, op, b"", None))
            pc += 1
    return ops


def analyze(code: bytes):
    ops = disasm(code)
    out = {"prologues": [], "entries": [], "push4_constants": set()}
    prologues = []
    for i in range(len(ops) - 3):
        if (ops[i][1] == 0x5F and ops[i + 1][1] == 0x35 and ops[i + 2][1] == 0x60
                and ops[i + 2][3] == 0xE0 and ops[i + 3][1] == 0x1C):
            prologues.append(ops[i][0])
    out["prologues"] = prologues
    for i in range(len(ops)):
        pc, op, imm, val = ops[i]
        if op == 0x63:  # PUSH4
            out["push4_constants"].add(imm.hex())
    for i in range(len(ops) - 4):
        pc, op, imm, val = ops[i]
        if op == 0x80 and ops[i + 1][1] == 0x63:  # DUP1 PUSH4 <sel>
            sel = ops[i + 1][2].hex()
            nxt = ops[i + 2][1]
            if nxt in CMP:
                kind = CMP[nxt]
                rec = {"push4_site": pc, "selector": sel, "cmp": kind}
                if ops[i + 3][1] == 0x61 and ops[i + 4][1] == 0x57:  # PUSH2 <t> JUMPI
                    rec["jumpi_target"] = ops[i + 3][3]
                    rec["target_is_jumpdest"] = code[ops[i + 3][3]] == 0x5B if ops[i + 3][3] < len(code) else None
                out["entries"].append(rec)
    out["push4_constants"] = sorted(out["push4_constants"])
    return out, ops, code


def keccak_scan(code: bytes, selectors):
    res = []
    for sel in selectors:
        b = bytes.fromhex(sel)
        offs = []
        start = 0
        while True:
            j = code.find(b, start)
            if j < 0:
                break
            offs.append({"offset": j, "preceded_by_push4_opcode": j > 0 and code[j - 1] == 0x63})
            start = j + 1
        res.append({"selector": sel, "occurrences": offs})
    return res


def abi_selectors(abi_path):
    abi = json.load(open(abi_path))
    sigs, sels = [], []
    for item in abi:
        if item.get("type") != "function":
            continue
        ins = ",".join(t["type"] for t in item.get("inputs", []))
        sig = f"{item['name']}({ins})"
        sigs.append(sig)
        sels.append({"sig": sig, "selector": keccak256(sig.encode()).hex()[:8]})
    return sigs, sels


def probe_leg(path, code_sha256):
    d = json.load(open(path))
    fn = d.get("normalized_result", {}).get("functions", []) or d.get("raw_result", {}).get("functions", [])
    funcs = [{"selector": f["selector"].removeprefix("0x"),
              "bytecode_offset": f.get("bytecode_offset", f.get("bytecodeOffset")),
              "dispatch": f.get("dispatch"),
              "inferred_arguments": f.get("inferred_arguments", f.get("arguments")),
              "inferred_state_mutability": f.get("inferred_state_mutability", f.get("stateMutability"))}
             for f in fn]
    br = d.get("normalized_result", {}).get("bytecode", {})
    return {
        "path": path,
        "evidence_id": d.get("evidence_id"),
        "provider_version": d.get("provider", {}).get("version"),
        "file_sha256": d.get("subject", {}).get("digest", {}).get("sha256"),
        "file_bytes": d.get("normalized_result", {}).get("artifact", {}).get("bytes"),
        "decoded_bytecode_sha256": br.get("sha256"),
        "decoded_bytecode_bytes": br.get("bytes"),
        "decoded_matches_runtime": br.get("sha256") == code_sha256,
        "kind": br.get("kind"),
        "functions": funcs,
    }


def main():
    bin_path, planted_path, abi_path = sys.argv[1], sys.argv[2], sys.argv[3]
    probe_paths = sys.argv[4:]
    code = open(bin_path, "rb").read()
    csha = sha256(code)
    planted = json.load(open(planted_path))
    planted_sels = sorted(e["selector"] for e in planted["entries"])
    sigs, abi_sels = abi_selectors(abi_path)
    abi_set = sorted(s["selector"] for s in abi_sels)
    an, ops, _ = analyze(code)
    eq_dests = sorted({(e["selector"], e["jumpi_target"]) for e in an["entries"] if e["cmp"] == "EQ"})
    eq_set = sorted(s for s, _ in eq_dests)
    gt_labels = sorted({(e["selector"], e["jumpi_target"]) for e in an["entries"] if e["cmp"] in ("GT", "LT")})
    scan = keccak_scan(code, planted_sels)
    scan_found = sorted(s["selector"] for s in scan if s["occurrences"])
    non_dispatch_push4 = sorted(set(an["push4_constants"]) - set(planted_sels))

    legs = [probe_leg(p, csha) for p in probe_paths]
    leg_report = []
    for leg in legs:
        leg_sels = sorted(f["selector"] for f in leg["functions"])
        offmap = {f["selector"]: f["bytecode_offset"] for f in leg["functions"]}
        myoff = dict(eq_dests)
        mism_off = {s: {"probe": offmap[s], "mine": myoff.get(s)} for s in leg_sels if myoff.get(s) != offmap[s]}
        leg_report.append({
            **leg,
            "K": len(leg_sels),
            "set_equal_planted": leg_sels == planted_sels,
            "missing_vs_planted": sorted(set(planted_sels) - set(leg_sels)),
            "extra_vs_planted": sorted(set(leg_sels) - set(planted_sels)),
            "offset_map_output_mismatches": mism_off,
        })

    report = {
        "runtime_bin": bin_path,
        "runtime_sha256": csha,
        "runtime_bytes": len(code),
        "dispatcher_prologues_pc": an["prologues"],
        "planted_K": len(planted_sels),
        "planted_selectors_sha256": hashlib.sha256(json.dumps(planted_sels).encode()).hexdigest(),
        "abi_selectors_K": len(abi_set),
        "abi_set_equals_planted": abi_set == planted_sels,
        "abi_only_differing": sorted(set(abi_set) ^ set(planted_sels)),
        "dispatch_eq_K": len(eq_set),
        "dispatch_eq_equals_planted": eq_set == planted_sels,
        "dispatch_eq_only_differing": sorted(set(eq_set) ^ set(planted_sels)),
        "dispatch_eq_dests": [{"selector": s, "dest": t} for s, t in eq_dests],
        "dispatch_eq_targets_all_jumpdest": all(code[t] == 0x5B for _, t in eq_dests),
        "dispatch_gt_lt_labels": [{"selector": s, "target": t} for s, t in gt_labels],
        "keccak_scan_found": scan_found,
        "keccak_scan_equals_planted": scan_found == planted_sels,
        "keccak_scan_detail": scan,
        "push4_constants_total": len(an["push4_constants"]),
        "non_dispatch_push4_constants": non_dispatch_push4,
        "probe_legs": leg_report,
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()