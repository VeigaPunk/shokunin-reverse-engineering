#!/usr/bin/env python3
"""EX-09 independent verifier — third-party re-derivation of the recon-A.md facts.

Written by the late-join EX-09 seat. Deliberately does NOT import or call
ex09-recon.py: it re-implements the disassembly walk and the keccak sponge
(flat-lane indexing) from scratch, and cross-checks the keccak against
js-sha3 and EX-04's node keccak.js.

Checks per carrier:
  C1  target bytes hash-match the upstream pin recorded by the authoring seat
  C2  planted set re-derived from signatures by an independent keccak
  C3  planted file on disk == that re-derivation (set equality)
  C4  every frozen probe leg: set / offsets / decoded digest / encoding form
  C5  every probe offset lands on a JUMPDEST byte (per carrier class)

Usage: python3 verify-independent.py <out-prefix>
"""
import hashlib
import json
import os
import subprocess
import sys

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
D = f"{ROOT}/.ufo/waves/arc3-loop1-round3/claims/c1/EX-09"

# ---------------------------------------------------------------- keccak (flat)
RC = [0x0000000000000001, 0x0000000000008082, 0x800000000000808A,
      0x8000000080008000, 0x000000000000808B, 0x0000000080000001,
      0x8000000080008081, 0x8000000000008009, 0x000000000000008A,
      0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
      0x000000008000808B, 0x800000000000008B, 0x8000000000008089,
      0x8000000000008003, 0x8000000000008002, 0x8000000000000080,
      0x000000000000800A, 0x800000008000000A, 0x8000000080008081,
      0x8000000000008080, 0x0000000080000001, 0x8000000080008008]
R = [[0, 36, 3, 41, 18], [1, 44, 10, 45, 2], [62, 6, 43, 15, 61],
     [28, 55, 25, 21, 56], [27, 20, 39, 8, 14]]
M = (1 << 64) - 1


def rot(v, n):
    n %= 64
    return ((v << n) | (v >> (64 - n))) & M if n else v


def _f(A):
    for rc in RC:
        C = [A[x] ^ A[x + 5] ^ A[x + 10] ^ A[x + 15] ^ A[x + 20] for x in range(5)]
        Dv = [C[(x + 4) % 5] ^ rot(C[(x + 1) % 5], 1) for x in range(5)]
        for x in range(5):
            for y in range(5):
                A[x + 5 * y] ^= Dv[x]
        B = [0] * 25
        for x in range(5):
            for y in range(5):
                B[y + 5 * ((2 * x + 3 * y) % 5)] = rot(A[x + 5 * y], R[x][y])
        for x in range(5):
            for y in range(5):
                A[x + 5 * y] = B[x + 5 * y] ^ ((~B[(x + 1) % 5 + 5 * y] & M)
                                               & B[(x + 2) % 5 + 5 * y])
        A[0] ^= rc


def keccak256(data):
    rate, A = 136, [0] * 25
    pad = rate - (len(data) % rate)
    p = data + (b"\x81" if pad == 1 else b"\x01" + b"\x00" * (pad - 2) + b"\x80")
    for o in range(0, len(p), rate):
        for i in range(rate // 8):
            A[i] ^= int.from_bytes(p[o + i * 8:o + i * 8 + 8], "little")
        _f(A)
    return b"".join(A[i].to_bytes(8, "little") for i in range(4))


def sel(sig):
    return keccak256(sig.encode())[:4].hex()


# ------------------------------------------------------------- disassembly
def walk(code):
    """Own linear sweep: (offset, opcode, immediate)."""
    i, n, out = 0, len(code), []
    while i < n:
        op = code[i]
        ln = op - 0x5F if 0x60 <= op <= 0x7F else 0
        out.append((i, op, code[i + 1:i + 1 + ln]))
        i += 1 + ln
    return out


def eq_table(code):
    """Own dispatcher walk: PUSH4 <sel> EQ PUSH1|PUSH2 <dest> JUMPI nodes.

    Returns {selector: (dest, cmp_offset, dest_width)}. Independent of
    ex09-recon.py's window scan: walks instruction-by-instruction.
    """
    ins = walk(code)
    table = {}
    for idx, (o, op, imm) in enumerate(ins):
        if op != 0x63 or len(imm) != 4:
            continue
        if idx + 4 >= len(ins):
            continue
        (o1, op1, _), (o2, op2, i2), (o3, op3, _) = ins[idx + 1], ins[idx + 2], ins[idx + 3]
        if op1 != 0x14 or op2 not in (0x60, 0x61) or op3 != 0x57:
            continue
        dest = int.from_bytes(i2, "big")
        table[imm.hex()] = (dest, o1, op2 - 0x5F)
    return table


def load_probe(path):
    d = json.load(open(path))
    if isinstance(d, dict) and "evidence_bundle" in d:
        d = d["evidence_bundle"]["records"][0]
    if isinstance(d, dict) and "data" in d and isinstance(d["data"], dict) \
            and "raw_result" in d["data"]:
        d = d["data"]
    return d


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


CARRIERS = [
    {
        "id": "A/2",
        "name": "carrierA-r3 (EX-02/EX-03 authored, optimizer runs=200)",
        "hexfile": f"{D}/target-carrierA-r3.runtime.hex",
        "binfile": f"{D}/target-carrierA-r3.runtime.bin",
        "upstream": [(".ufo/waves/arc3-loop1-round3/claims/c1/EX-03/"
                      "carrier-A-EX02/carrierA.runtime.bin",
                      "9f7392acccea72cd42bdd8095a8578cab0727766f218b5399da22bc21d23741a")],
        "planted": f"{D}/planted-carrierA-r3.copy.txt",
        "legs": f"{D}/legs-carrierA-r3.txt",
        "expect_jumpdest": True,
        "sigs": ["sweep(address)", "totalCredited()", "withdraw(uint256)",
                 "rotate(address)", "isSolvent()", "creditOf(address)",
                 "owner()", "stamp()", "deposit()"],
    },
    {
        "id": "A/3",
        "name": "OptVault (PL-1 plan carrier, optimizer runs=200)",
        "hexfile": f"{D}/target-OptVault.runtime.hex",
        "binfile": f"{D}/target-OptVault.runtime.bin",
        "upstream": [(".ufo/waves/arc3-loop1-round3/claims/c1/EX-03/"
                      "carrier-A-plan-prototype-OptVault/OptVault.runtime.bin",
                      "544469b7bebfda4e5c9dedc7a11af69fc77d917f1d4258a53d1aa5ed95dfde7f")],
        "planted": f"{D}/planted-OptVault.copy.txt",
        "legs": f"{D}/legs-OptVault.txt",
        "expect_jumpdest": True,
        "sigs": ["setPaused(bool)", "withdraw(uint256)", "paused()",
                 "creditOf(address)", "deposit()"],
    },
    {
        "id": "A/1",
        "name": "legacy control carrier-A.hex (r1 CR-1 hand-assembled)",
        "hexfile": f"{D}/target-carrier-A-control.hex",
        "binfile": f"{D}/target-carrier-A-control.bin",
        "upstream": [(".ufo/waves/arc3-loop1-round1/claims/c1/CR-1/evidence/"
                      "carrier-A.hex",
                      "36dc82468c5846a93273970483253e63f5b0bef673f0bd355d3c41db01b9b3d2")],
        "planted": f"{D}/planted-A-control.json",
        "legs": f"{D}/legs-control.txt",
        "expect_jumpdest": False,
        "sigs": ["transfer(address,uint256)", "balanceOf(address)",
                 "approve(address,uint256)"],
    },
]


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "/var/tmp/ex09v/verify"
    report = {"keccak_selftest": None, "carriers": [], "verdict": None}
    ok = True

    # keccak self-test
    v = [("", "c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"),
         ("abc", "4e03657aea45a94fc7d47ba826c8d667c0d1e6e33a64a036ec44f58fa12d6c45")]
    st = all(keccak256(m.encode()).hex() == e for m, e in v)
    report["keccak_selftest"] = "PASS" if st else "FAIL"
    ok &= st

    # cross-implementation: js-sha3 via node, and EX-04's node keccak.js
    xchecks = {}
    for label, mod in [("js-sha3", "js-sha3"), ("EX-04 keccak.js", "ex04")]:
        if mod == "js-sha3":
            script = (f"const s=require('{ROOT}/.ufo/waves/arc3-loop1-round1/"
                      "tools/solc-prefix/node_modules/js-sha3');"
                      "for(const x of JSON.parse(process.argv[1]))"
                      "console.log(s.keccak256(x).slice(0,8))")
        else:
            script = ("const k=require('/var/tmp/ex09v/keccak-js-independent.js');"
                      "for(const x of JSON.parse(process.argv[1]))"
                      "console.log(k.selector(x))")
        sigs = sorted({s for c in CARRIERS for s in c["sigs"]})
        try:
            r = subprocess.run(["node", "-e", script, json.dumps(sigs)],
                               capture_output=True, text=True, timeout=60)
            got = r.stdout.split()
            want = [sel(s) for s in sigs]
            xchecks[label] = "PASS" if got == want else f"MISMATCH {got} != {want}"
            ok &= got == want
        except Exception as e:  # noqa: BLE001
            xchecks[label] = f"ERROR {e}"
            ok = False
    report["keccak_crossimpl"] = xchecks

    for c in CARRIERS:
        cr = {"id": c["id"], "name": c["name"], "checks": {}, "legs": []}
        code = bytes.fromhex(open(c["hexfile"]).read().strip())
        code_sha = hashlib.sha256(code).hexdigest()
        cr["decoded_sha256"] = code_sha
        cr["decoded_bytes"] = len(code)

        # C1 upstream pin
        ups = []
        for path, want in c["upstream"]:
            got = sha(f"{ROOT}/{path}")
            ups.append({"path": path, "want": want, "got": got,
                        "match": got == want})
            ok &= got == want
        cr["checks"]["C1_upstream_pin"] = ups

        # C2 planted re-derived from signatures
        derived = {sel(s): s for s in c["sigs"]}
        cr["checks"]["C2_derived_from_sigs"] = derived

        # C3 planted file == derivation (text table or EX-09's planted-A-control.json)
        if c["planted"].endswith(".json"):
            doc = json.load(open(c["planted"]))
            planted = {e["selector"].lower().removeprefix("0x"): e.get("sig", "")
                       for e in doc["entries"]}
        else:
            planted = {e.split()[0].lower().removeprefix("0x"): e.split()[1]
                       for e in open(c["planted"]) if e.strip()
                       and not e.startswith("#") and e.split()[0].startswith("0x")}
        same = set(planted) == set(derived)
        ok &= same
        cr["checks"]["C3_planted_matches_derivation"] = {
            "planted_K": len(planted), "derived_K": len(derived),
            "match": same,
            "missing": sorted(set(derived) - set(planted)),
            "extra": sorted(set(planted) - set(derived))}

        # own dispatcher parse
        table = eq_table(code)
        cr["eq_table_K"] = len(table)
        cr["checks"]["eq_table"] = {s: {"dest": d, "cmp_offset": o, "width": w}
                                    for s, (d, o, w) in sorted(table.items())}

        legs = [l.strip() for l in open(c["legs"])
                if l.strip() and not l.startswith("#")]
        cr["legs_frozen"] = len(legs)
        leg_fail = 0
        for lp in legs:
            d = load_probe(f"{ROOT}/{lp}")
            fns = d["raw_result"].get("functions") or []
            n = d["normalized_result"]
            got = {f["selector"].lower().removeprefix("0x"): f.get("bytecodeOffset")
                   for f in fns}
            set_ok = set(got) == set(derived)
            off_ok = all(table.get(s, (None,))[0] == o for s, o in got.items())
            dig_ok = n["bytecode"]["sha256"] == code_sha
            art = n["artifact"]
            if art["encoding"] == "hex":
                form_ok = 2 * len(code) <= art["bytes"] <= 2 * len(code) + 4
            else:
                form_ok = (art["bytes"] == len(code)
                           and d["subject"]["digest"]["sha256"] == code_sha)
            land_bad = [s for s, o in got.items()
                        if not (0 <= o < len(code) and code[o] == 0x5b)]
            row = {"leg": os.path.basename(lp), "n": len(fns), "set_ok": set_ok,
                   "offsets_ok": off_ok, "digest_ok": dig_ok, "form_ok": form_ok,
                   "non_jumpdest_offsets": sorted(land_bad)}
            if not (set_ok and off_ok and dig_ok and form_ok):
                leg_fail += 1
            cr["legs"].append(row)
        cr["leg_failures"] = leg_fail
        # C5: on solc carriers every offset must be a JUMPDEST; on the control
        #     none may be (its dests are declared immediates 2 bytes early)
        if c["expect_jumpdest"]:
            c5 = all(not r["non_jumpdest_offsets"] for r in cr["legs"])
        else:
            c5 = all(r["non_jumpdest_offsets"] == sorted(r["non_jumpdest_offsets"])
                     and len(r["non_jumpdest_offsets"]) == r["n"] for r in cr["legs"])
        cr["checks"]["C5_landing_expectation_holds"] = c5
        ok &= leg_fail == 0 and c5
        report["carriers"].append(cr)

    report["verdict"] = "ALL INDEPENDENT CHECKS PASS" if ok else "FAILURES PRESENT"
    txt = json.dumps(report, indent=2)
    open(f"{out}.json", "w").write(txt + "\n")
    # human summary
    lines = [f"keccak self-test: {report['keccak_selftest']}",
             f"keccak cross-impl: {report['keccak_crossimpl']}", ""]
    for cr in report["carriers"]:
        lines.append(f"--- {cr['id']}  {cr['name']}")
        lines.append(f"    decoded {cr['decoded_sha256']} ({cr['decoded_bytes']} B)")
        for u in cr["checks"]["C1_upstream_pin"]:
            lines.append(f"    C1 upstream pin {'OK  ' if u['match'] else 'FAIL'} {u['path']}")
        p = cr["checks"]["C3_planted_matches_derivation"]
        lines.append(f"    C2/C3 planted K={p['planted_K']} derived K={p['derived_K']} "
                     f"{'MATCH' if p['match'] else 'MISMATCH'}")
        lines.append(f"    own EQ-table K={cr['eq_table_K']}")
        lines.append(f"    legs frozen={cr['legs_frozen']}  failures={cr['leg_failures']}  "
                     f"C5={cr['checks']['C5_landing_expectation_holds']}")
        bad = [r for r in cr["legs"] if r["non_jumpdest_offsets"]]
        if bad:
            lines.append(f"    legs with non-JUMPDEST offsets: {len(bad)} "
                         f"(all {bad[0]['non_jumpdest_offsets']})")
        lines.append("")
    lines.append(f"VERDICT: {report['verdict']}")
    open(f"{out}.txt", "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
