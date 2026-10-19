#!/usr/bin/env python3
"""RV-1 r3 — recompute a carrier's planted selector set from its SOURCE via
three independent keccak paths, and (optionally) reconcile against a planted
artifact, a runtime bytecode dump, and a raw-recorded probe/planted set.

Paths:
  A  keccak_slice.py            (from-spec slice formulation, derived constants)
  B  js_keccak.js               (js-sha3@0.8.0 from the receipted solc prefix)
  C  solc_methodids.js          (solc 0.8.37 compiler-internal keccak)

Usage:
  recompute.py --src TOKEN.sol [--planted FILE] [--runtime-hex FILE]
               [--runtime-bin FILE] [--optimize [--optimize-runs N]] [--label NAME]
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

TOOLS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS)
import keccak_slice as K  # noqa: E402

ENV = dict(os.environ, TMPDIR="/var/tmp/rv1-r3")


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, env=ENV, **kw)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_planted(path):
    """Accept: '0x<sel> sig ...', '<sel> sig', '<sel>@pc ...', or planted JSON
    (schemas seen: {functions:[{selector,sig}]}, {rows:[{selector,sig}]},
    {selectors:[...],signatures:[...]})."""
    out = {}
    if path.endswith(".json"):
        data = json.load(open(path))
        rows = data.get("functions") or data.get("rows") or data.get("entries") or []
        for fn in rows:
            sel = str(fn.get("selector", "")).replace("0x", "").lower()
            if sel:
                out[sel] = fn.get("sig", "")
        sels = data.get("selectors") or []
        sigs = data.get("signatures") or []
        for i, s in enumerate(sels):
            sel = str(s).replace("0x", "").lower()
            out.setdefault(sel, sigs[i] if i < len(sigs) else "")

        # nested schema (EX-08 style): {<contract>: {method_identifiers: {sig: sel}}}
        def walk(node):
            if isinstance(node, dict):
                mi = node.get("method_identifiers")
                if isinstance(mi, dict):
                    for sig, sel in mi.items():
                        out.setdefault(str(sel).replace("0x", "").lower(), sig)
                for v in node.values():
                    walk(v)
            elif isinstance(node, list):
                for v in node:
                    walk(v)
        walk(data)
        return out
    for raw in open(path):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        tok = line.split()[0]
        tok = tok.replace("0x", "")
        m = re.match(r"^[0-9a-fA-F]{8}$", tok)
        if not m:
            continue
        sig = ""
        rest = line.split()[1:]
        for r in rest:
            if re.match(r"^[A-Za-z_][A-Za-z0-9_]*\(", r):
                sig = r
                break
        out[tok.lower()] = sig
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--planted")
    ap.add_argument("--runtime-hex")
    ap.add_argument("--runtime-bin")
    ap.add_argument("--optimize", action="store_true")
    ap.add_argument("--optimize-runs", type=int, default=200)
    ap.add_argument("--label", default="")
    args = ap.parse_args()

    print(f"# RV-1 r3 recompute — label={args.label or args.src}")
    print(f"# source: {args.src}  sha256={sha256_file(args.src)}")

    # ---- path C: solc ----------------------------------------------------
    extra = ["--optimize", "--optimize-runs", str(args.optimize_runs)] if args.optimize else []
    r = run(["node", os.path.join(TOOLS, "solc_methodids.js"), args.src] + extra)
    if r.returncode != 0:
        print("SOLC_ERROR", r.stderr[:2000])
        sys.exit(1)
    solc_out = json.loads(r.stdout)
    print(f"# solc: {solc_out['solcVersion']} optimize={solc_out['optimize']} runs={solc_out['runs']}")
    contracts = solc_out["contracts"]
    planted_pre = parse_planted(args.planted) if args.planted else None

    # per-contract: path A + B + C (a source may declare a library + a contract)
    per_contract = {}
    for cname, c in contracts.items():
        pathC = {v.lower(): k for k, v in c["methodIdentifiers"].items()}  # sel -> sig
        sigs = sorted(c["abiFunctions"])
        sigfile = "/var/tmp/rv1-r3/out/_sigs.txt"
        with open(sigfile, "w") as f:
            f.write("\n".join(sigs) + "\n")
        pathA = {K.selector(s): s for s in sigs}
        rb = run(["node", os.path.join(TOOLS, "js_keccak.js"), sigfile])
        pathB = {}
        for line in rb.stdout.splitlines():
            if line.startswith("#") or not line.strip():
                continue
            sel, sig = line.split(None, 1)
            pathB[sel.lower()] = sig.strip()
        sigmap = {}
        for m in (pathA, pathB, pathC):
            for sel, sig in m.items():
                sigmap.setdefault(sel, set()).add(sig)
        bad = {s: v for s, v in sigmap.items() if len(v) > 1}
        per_contract[cname] = {
            "deployed": c["deployedBytecode"], "pathC": pathC,
            "setA": set(pathA), "setB": set(pathB), "sigmap": sigmap, "bad": bad,
        }
        print(f"# contract {cname}: K(A)={len(pathA)} K(B)={len(pathB)} K(C)={len(pathC)} "
              f"A==B={set(pathA) == set(pathB)} A==C={set(pathA) == set(pathC)} "
              f"sig_conflicts={len(bad)}"
              + (f"  planted_match={set(planted_pre) == set(pathA)}" if planted_pre is not None else ""))

    if planted_pre is not None:
        matching = [n for n, d in per_contract.items() if d["setA"] == set(planted_pre)]
        print(f"# contracts whose recomputed set == planted: {matching}")
    # target contract: the one whose set matches the planted artifact, else the largest
    if planted_pre is not None and matching:
        cname = matching[0]
    else:
        cname = max(per_contract, key=lambda n: len(per_contract[n]["setA"]))
    d = per_contract[cname]
    pathC, setA, setB, sigmap, bad = d["pathC"], d["setA"], d["setB"], d["sigmap"], d["bad"]
    c = contracts[cname]
    print(f"# target contract: {cname} (K={len(setA)})")
    print(f"# A==B: {setA == setB}   A==C: {setA == set(pathC)}   B==C: {setB == set(pathC)}")
    if setA != setB:
        print("  A\\B", sorted(setA - setB), " B\\A", sorted(setB - setA))
    if setA != set(pathC):
        print("  A\\C", sorted(setA - set(pathC)), " C\\A", sorted(set(pathC) - setA))
    print(f"# selector->signature conflicts across paths: {len(bad)} {bad if bad else ''}")

    # ---- compiled bytecode vs pinned runtime ----------------------------
    deployed_hex = c["deployedBytecode"]
    if not re.fullmatch(r"[0-9a-fA-F]*", deployed_hex or ""):
        import re as _re
        bad = sorted(set(_re.findall(r"[^0-9a-fA-F]+", deployed_hex)))
        print(f"# deployedBytecode contains unlinked library placeholders {bad}; byte-level compare skipped")
        deployed_hex = _re.sub(r"[^0-9a-fA-F]+", "", deployed_hex)
    deployed = bytes.fromhex(deployed_hex)
    print(f"# deployedBytecode sha256={hashlib.sha256(deployed).hexdigest()} len={len(deployed)}")
    for p in [args.runtime_bin, args.runtime_hex]:
        if not p:
            continue
        with open(p, "rb") as f:
            raw = f.read()
        text = raw.decode("ascii", "ignore").strip()
        if p.endswith(".hex") or (text and all(ch in "0123456789abcdefABCDEF" for ch in text)):
            rb_ = bytes.fromhex(text)
        else:
            rb_ = raw
        same = rb_ == deployed
        print(f"# runtime {p} sha256={hashlib.sha256(rb_).hexdigest()} len={len(rb_)} "
              f"compiled==file: {same}")
        if not same:
            for i in range(min(len(rb_), len(deployed))):
                if rb_[i] != deployed[i]:
                    print(f"  first diff at byte {i}: file={rb_[i]:02x} compiled={deployed[i]:02x}")
                    break

    # ---- reconcile with the planted artifact ----------------------------
    if args.planted:
        planted = parse_planted(args.planted)
        setP = set(planted)
        print(f"# planted: {args.planted} sha256={sha256_file(args.planted)} K={len(setP)}")
        print(f"# planted==A: {setP == setA}  planted==B: {setP == setB}  planted==C: {setP == set(pathC)}")
        miss = sorted(setP - setA)
        extra_ = sorted(setA - setP)
        print(f"# missing_from_recompute={miss}  extra_in_recompute={extra_}")
        for sel in sorted(setP & setA):
            ps = planted.get(sel, "")
            cs = pathC.get(sel, "")
            flag = "" if (not ps or not cs or ps == cs) else f"   SIG-DIFF planted='{ps}' solc='{cs}'"
            if flag:
                print(f"  {sel} {flag}")
    # ---- machine-readable summary ---------------------------------------
    print("# PLANTED_SET_JSON " + json.dumps({
        "source": args.src, "source_sha256": sha256_file(args.src),
        "contract": cname, "optimize": args.optimize,
        "deployed_sha256": hashlib.sha256(deployed).hexdigest(),
        "selectors": sorted(setA), "sigs": {k: sorted(v)[0] for k, v in sigmap.items()},
    }, sort_keys=True))


if __name__ == "__main__":
    main()