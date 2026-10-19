#!/usr/bin/env python3
"""RV-1 LATE-JOIN — recompute both planted selector sets from the carrier
SOURCES with keccak path D (keccak_bits.py, byte-string state, derived RC/RHO),
and reconcile against: the planted files, the landed solc ABI artifacts, and
the runtime bytecode's PUSH4 dispatch immediates.

Sources of truth are the .sol files themselves; nothing is taken from the
planted artifacts except the comparison target.

Usage: recompute_carriers.py
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import keccak_bits as KD  # noqa: E402

REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
C1 = os.path.join(REPO, ".ufo/waves/arc3-loop1-round3/claims/c1")
OUT = "/var/tmp/rv1-latejoin/out"

CANON = {
    "uint": "uint256", "int": "int256",
    "fixed": "fixed128x18", "ufixed": "ufixed128x18",
}


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def canon_type(t):
    t = t.strip()
    t = re.sub(r"\s+(memory|calldata|storage|payable|indexed)\b", "", t)
    t = re.sub(r"^(address|contract)\s*$", "address", t)
    if t in CANON:
        return CANON[t]
    m = re.fullmatch(r"(u?int)(\d*)", t)
    if m:
        return m.group(1) + (m.group(2) or "256")
    if t.endswith("[]"):
        return canon_type(t[:-2]) + "[]"
    if t.startswith("mapping"):
        return t
    return t


def split_params(s):
    """Split a Solidity parameter list at top-level commas."""
    out, depth, cur = [], 0, ""
    for ch in s:
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        if ch == "," and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    if cur.strip():
        out.append(cur)
    return out


def sig_from_params(s):
    types = []
    for p in split_params(s):
        p = p.strip()
        if not p:
            continue
        # drop the parameter NAME: last identifier token, unless the whole thing
        # is a bare type
        parts = p.split()
        # walk backwards to find the type portion: types may be multi-token
        # (e.g. "uint256[] memory" already stripped by canon_type)
        ty = " ".join(parts[:-1]) if len(parts) > 1 else parts[0]
        if not ty:
            ty = parts[0]
        types.append(canon_type(ty))
    return "(" + ",".join(types) + ")"


FUNC_RE = re.compile(
    r"\bfunction\s+([A-Za-z_$][A-Za-z0-9_$]*)\s*\(([^;{]*?)\)"
    r"((?:\s*(?:external|public|internal|private|view|pure|payable|virtual|override|returns\s*\([^)]*\)))*)",
    re.S,
)


# public state variables generate getters on the ABI; they are NOT `function`
# declarations, so they need their own rule.  Two extractor bugs were caught by
# this audit itself: (a) the first pass missed auto-getters entirely, and (b)
# consuming the trailing `;` as part of the match swallowed the separator the
# NEXT declaration needed, so consecutive declarations matched only the first.
# The semicolon is now a lookahead, not consumed.
VAR_RE = re.compile(
    r"(?:^|[;{}]\s*)([A-Za-z_$][A-Za-z0-9_$]*(?:\[\])?(?:\s+[A-Za-z_$][A-Za-z0-9_$]*)?)"
    r"\s+public\s+(?:constant\s+|immutable\s+)?([A-Za-z_$][A-Za-z0-9_$]*(?:\s*=\s*[^;]*)?)\s*(?=;)",
    re.S,
)


def extract(src_text, contract):
    """Return list of dicts for external/public functions of `contract`."""
    body = extract_contract_body(src_text, contract)
    fns = []
    for m in VAR_RE.finditer(body):
        ty, decl = m.group(1).strip(), m.group(2).strip()
        ty = " ".join(ty.split())
        name = decl.split("=")[0].strip()
        if " " in name or not re.fullmatch(r"[A-Za-z_$][A-Za-z0-9_$]*", name):
            continue
        if name in ("memory", "calldata", "storage"):
            continue
        fns.append({
            "sig": name + "()",
            "name": name,
            "params_raw": "",
            "mutability": "view",
            "from": "public-state-var",
        })
    for m in FUNC_RE.finditer(body):
        name, params, quals = m.group(1), m.group(2), m.group(3) or ""
        quals_norm = re.sub(r"\s+", " ", quals)
        if not re.search(r"\b(external|public)\b", quals_norm):
            continue
        mut = "nonpayable"
        if re.search(r"\bpayable\b", quals_norm):
            mut = "payable"
        elif re.search(r"\bview\b", quals_norm):
            mut = "view"
        elif re.search(r"\bpure\b", quals_norm):
            mut = "pure"
        fns.append({
            "sig": name + sig_from_params(params),
            "name": name,
            "params_raw": " ".join(params.split()),
            "mutability": mut,
            "from": "function-decl",
        })
    return fns


def extract_contract_body(text, contract):
    m = re.search(r"\bcontract\s+" + re.escape(contract) + r"\b", text)
    if not m:
        raise SystemExit(f"contract {contract} not found")
    i = text.index("{", m.end())
    depth, j = 0, i
    while j < len(text):
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
            if depth == 0:
                return text[i:j + 1]
        j += 1
    raise SystemExit("unbalanced braces")


def parse_planted(path):
    out = []
    for raw in open(path):
        line = raw.strip()
        m = re.match(r"^(0x)?([0-9a-fA-F]{8})\s+(\S+)\s+\[(\w+)\]", line)
        if m:
            out.append({"selector": m.group(2).lower(), "sig": m.group(3),
                        "mutability": m.group(4)})
    return out


def abi_functions(path):
    abi = json.load(open(path))
    out = []
    for e in abi:
        if e.get("type") != "function":
            continue
        sig = e["name"] + "(" + ",".join(i["type"] for i in e.get("inputs", [])) + ")"
        out.append({"sig": sig, "mutability": e.get("stateMutability", "nonpayable")})
    return out


def push4_sites(code):
    """Return list of (pc, imm_hex) for every PUSH4 immediate."""
    sites = []
    pc = 0
    n = len(code)
    while pc < n:
        op = code[pc]
        if 0x60 <= op <= 0x7f:
            k = op - 0x5f
            imm = code[pc + 1:pc + 1 + k]
            if k == 4 and len(imm) == 4:
                sites.append((pc, imm.hex()))
            pc += 1 + k
        else:
            pc += 1
    return sites


def diff(a, b):
    return sorted(set(a) - set(b)), sorted(set(b) - set(a))


def run(label, sol_path, contract, planted_path, abi_path, runtime_path):
    res = {"label": label, "contract": contract, "sol": sol_path}
    src = open(sol_path).read()
    res["source_sha256"] = sha256_file(sol_path)
    res["planted_sha256"] = sha256_file(planted_path)

    fns = extract(src, contract)
    for f in fns:
        f["selector"] = KD.selector(f["sig"])
    res["n_extracted"] = len(fns)
    res["source_sigs"] = {f["sig"]: f["selector"] for f in fns}
    res["source_mutability"] = {f["sig"]: f["mutability"] for f in fns}

    planted = parse_planted(planted_path)
    res["n_planted"] = len(planted)
    res["planted_sigs"] = {p["sig"]: p["selector"] for p in planted}
    res["planted_mutability"] = {p["sig"]: p["mutability"] for p in planted}

    # 1. selector agreement for shared sigs
    both = sorted(set(res["source_sigs"]) & set(res["planted_sigs"]))
    res["selector_mismatches"] = [
        {"sig": s, "source_path_D": res["source_sigs"][s], "planted": res["planted_sigs"][s]}
        for s in both if res["source_sigs"][s] != res["planted_sigs"][s]
    ]
    res["sig_missing_in_planted"] = sorted(set(res["source_sigs"]) - set(res["planted_sigs"]))
    res["sig_extra_in_planted"] = sorted(set(res["planted_sigs"]) - set(res["source_sigs"]))
    res["mutability_mismatches"] = [
        {"sig": s, "source": res["source_mutability"][s], "planted": res["planted_mutability"][s]}
        for s in both if res["source_mutability"][s] != res["planted_mutability"][s]
    ]
    res["set_equal"] = (not res["selector_mismatches"] and not res["sig_missing_in_planted"]
                        and not res["sig_extra_in_planted"])

    # 2. ABI cross-check (solc's own view of the same source)
    if abi_path and os.path.exists(abi_path):
        abi = abi_functions(abi_path)
        res["abi_sha256"] = sha256_file(abi_path)
        abi_sigs = {a["sig"]: KD.selector(a["sig"]) for a in abi}
        res["abi_sigs"] = abi_sigs
        miss, extra = diff(res["source_sigs"], abi_sigs)
        res["abi_missing"] = miss
        res["abi_extra"] = extra
        res["abi_selector_mismatch"] = [s for s in set(res["source_sigs"]) & set(abi_sigs)
                                        if res["source_sigs"][s] != abi_sigs[s]]

    # 3. runtime bytecode PUSH4 presence (byte-level, independent of any table)
    if runtime_path and os.path.exists(runtime_path):
        txt = open(runtime_path).read().strip()
        code = bytes.fromhex(txt[2:] if txt.startswith("0x") else txt)
        res["runtime_text_sha256"] = sha256_file(runtime_path)
        res["runtime_sha256"] = hashlib.sha256(code).hexdigest()
        res["runtime_len"] = len(code)
        sites = push4_sites(code)
        res["push4_sites"] = [[pc, imm] for pc, imm in sites]
        present = {imm for _, imm in sites}
        sel_set = set(res["source_sigs"].values())
        res["selectors_absent_from_code"] = sorted(sel_set - present)
        res["code_push4_not_selectors"] = sorted(present - sel_set)

    return res


def main():
    jobs = [
        dict(label="carrierA-EX-02-opt200", contract="CarrierA",
             sol_path=os.path.join(C1, "EX-02/carrierA.sol"),
             planted_path=os.path.join(C1, "EX-02/planted-A.txt"),
             abi_path=os.path.join(C1, "EX-02/evidence/carrierA.abi.json"),
             runtime_path=os.path.join(C1, "EX-02/evidence/carrierA.runtime.hex")),
        dict(label="carrierB-EX-04-opt200", contract="VaultB",
             sol_path=os.path.join(C1, "EX-04/carrierB.sol"),
             planted_path=os.path.join(C1, "EX-04/planted-B.txt"),
             abi_path=os.path.join(C1, "EX-04/evidence/carrierB.abi-opt200.json"),
             runtime_path=os.path.join(C1, "EX-04/evidence/carrierB.runtime-opt200.hex")),
        dict(label="carrierB-EX-04-noopt", contract="VaultB",
             sol_path=os.path.join(C1, "EX-04/carrierB.sol"),
             planted_path=os.path.join(C1, "EX-04/planted-B.txt"),
             abi_path=os.path.join(C1, "EX-04/evidence/carrierB.abi-noopt.json"),
             runtime_path=os.path.join(C1, "EX-04/evidence/carrierB.runtime-noopt.hex")),
    ]
    os.makedirs(OUT, exist_ok=True)
    allres = []
    for j in jobs:
        r = run(**j)
        allres.append(r)
        lines = []
        lines.append(f"# RV-1 LATE-JOIN recompute — {r['label']}")
        lines.append(f"# keccak path D = {os.path.join(HERE, 'keccak_bits.py')} "
                     f"(byte-string state, derived RC/RHO)")
        lines.append(f"# source {r['sol']}")
        lines.append(f"#   sha256={r['source_sha256']}")
        lines.append(f"# contract {r['contract']}: extracted K={r['n_extracted']}  planted K={r['n_planted']}")
        lines.append(f"# SET_EQUAL={r['set_equal']}  selector_mismatches={len(r['selector_mismatches'])}")
        lines.append(f"# sig_missing_in_planted={r['sig_missing_in_planted']}")
        lines.append(f"# sig_extra_in_planted={r['sig_extra_in_planted']}")
        lines.append(f"# mutability_mismatches={r['mutability_mismatches']}")
        if "abi_missing" in r:
            lines.append(f"# ABI ({r.get('abi_sha256','')[:16]}…): missing={r['abi_missing']} "
                         f"extra={r['abi_extra']} selmismatch={r['abi_selector_mismatch']}")
        if "runtime_sha256" in r:
            lines.append(f"# runtime {r['runtime_sha256']} len={r['runtime_len']}")
            lines.append(f"# selectors_absent_from_code={r['selectors_absent_from_code']}")
            lines.append(f"# code_push4_not_selectors={r['code_push4_not_selectors']}")
        lines.append("")
        lines.append("| sig | path-D selector | planted | ABI-derived | mut(src) | mut(planted) |")
        lines.append("|---|---|---|---|---|---|")
        for s in sorted(r["source_sigs"]):
            lines.append("| {} | {} | {} | {} | {} | {} |".format(
                s, r["source_sigs"][s],
                r["planted_sigs"].get(s, "-"),
                r.get("abi_sigs", {}).get(s, "-"),
                r["source_mutability"][s], r["planted_mutability"].get(s, "-")))
        txt = "\n".join(lines) + "\n"
        p = os.path.join(OUT, f"recompute-{r['label']}.txt")
        open(p, "w").write(txt)
        print(txt)
    json.dump(allres, open(os.path.join(OUT, "recompute-c1-rv1-latejoin.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
