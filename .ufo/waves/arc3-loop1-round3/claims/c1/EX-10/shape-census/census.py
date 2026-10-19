#!/usr/bin/env python3
"""Dispatch-shape census: how does solc 0.8.37 order its dispatcher as a
function of selector count and optimizer mode? EX-10 seat, arc3-loop1-round3."""
import pathlib, subprocess, sys, json
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from recon import analyze

PREFIX = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix'
OUT = pathlib.Path(__file__).parent
TMP = pathlib.Path('/var/tmp/ex10-r3/census'); TMP.mkdir(parents=True, exist_ok=True)

def source(k):
    fns = "\n".join(f"    function f{i}() external pure returns (uint256) {{ return {i}; }}" for i in range(k))
    return f"// SPDX-License-Identifier: MIT\npragma solidity 0.8.37;\ncontract C {{\n{fns}\n}}\n"

rows = []
for k in (4,5,6,7,8,9,10,11,13):
    src = TMP / f"C{k}.sol"; src.write_text(source(k))
    for mode, flag in (("nopt","0"), ("opt200","1")):
        binp = TMP / f"C{k}.{mode}.bin"
        sha = subprocess.check_output(["node", str(OUT/'compile-generic.js'), PREFIX, str(src), str(binp), flag], text=True).strip()
        code = binp.read_bytes()
        an, ops, _ = analyze(code)
        n_eq = sum(1 for e in an["entries"] if e["cmp"] == "EQ")
        n_nav = sum(1 for e in an["entries"] if e["cmp"] in ("GT","LT"))
        shape = "binsearch(GT/EQ)" if n_nav else "linear(EQ chain)"
        rows.append({"k": k, "mode": mode, "runtime_bytes": len(code), "sha256": sha,
                     "eq_entries": n_eq, "nav_entries": n_nav, "shape": shape,
                     "prologue_pc": an["prologues"], "head32": code[:32].hex()})
transcript = "\n".join(
    f"k={r['k']:2d} {r['mode']:6s} bytes={r['runtime_bytes']:4d} eq={r['eq_entries']:2d} nav={r['nav_entries']:2d} shape={r['shape']:18s} prologue_pc={r['prologue_pc']} sha256={r['sha256'][:16]}"
    for r in rows)
(OUT/'census-results.txt').write_text(transcript + "\n")
(OUT/'census-results.json').write_text(json.dumps(rows, indent=2) + "\n")
print(transcript)
