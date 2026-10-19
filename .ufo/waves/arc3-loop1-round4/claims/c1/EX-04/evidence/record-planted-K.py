#!/usr/bin/env python3
"""EX-04 (arc3-loop1-round4, C1) — record the planted selector set K BEFORE any
compile or probe (the round's falsifiability requirement: planted-K recorded
pre-compile).

Derives selectors two ways from the same signature list, from independent
implementations (pure-Python keccak256.py and pure-JS keccak256.js), asserts
they agree, and writes planted-K.json with sha256s of the source and of both
derivation scripts.

Usage: python3 record-planted-K.py <CarrierV.vy> <out planted-K.json>
"""
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent

# The carrier's external surface, transcribed by hand from src/CarrierV.vy.
# `__init__` and `__default__` are excluded: neither is a dispatch selector.
SIGNATURES = [
    "owner()",
    "total_deposits()",
    "fee_bps()",
    "paused()",
    "balances(address)",
    "deposit()",
    "withdraw(uint256)",
    "set_fee(uint256)",
    "fee_on(uint256)",
    "fee_of(uint256,uint256)",
    "pause()",
    "unpause()",
    "balance_of(address)",
    "is_owner(address)",
    "fee_quote(uint256)",
]

# Eight ERC-20 selectors that must NOT appear in this carrier (non-ERC-20 shape).
ERC20_SIGNATURES = [
    "transfer(address,uint256)",
    "approve(address,uint256)",
    "transferFrom(address,address,uint256)",
    "balanceOf(address)",
    "allowance(address,address)",
    "totalSupply()",
    "name()",
    "symbol()",
]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def derive(script: Path, sigs, runner):
    out = subprocess.run(
        runner + [str(script)] + list(sigs),
        capture_output=True, text=True, check=True,
    ).stdout
    pairs = {}
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        sel, sig = line.split(None, 1)
        pairs[sig] = sel
    return pairs


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    src = Path(sys.argv[1]).resolve()
    out_path = Path(sys.argv[2]).resolve()

    py = derive(HERE / "keccak256.py", SIGNATURES + ERC20_SIGNATURES, [sys.executable])
    js = derive(HERE / "keccak256.js", SIGNATURES + ERC20_SIGNATURES, ["node"])
    if py != js:
        print("FATAL: the two independent keccak implementations disagree")
        for k in sorted(set(py) | set(js)):
            if py.get(k) != js.get(k):
                print(f"  {k}: python={py.get(k)} node={js.get(k)}")
        return 1

    planted = {sig: py[sig] for sig in SIGNATURES}
    erc20 = {sig: py[sig] for sig in ERC20_SIGNATURES}
    collisions = sorted(set(planted.values()) & set(erc20.values()))

    doc = {
        "seat": "EX-04",
        "wave": "arc3-loop1-round4",
        "chain": "c1",
        "carrier": "CarrierV",
        "recorded_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "note": "recorded PRE-COMPILE / PRE-PROBE; both derivations independent of the compiler",
        "source": {"path": str(src), "sha256": sha256_file(src)},
        "derivations": {
            "python": {"script": "keccak256.py", "sha256": sha256_file(HERE / "keccak256.py")},
            "node": {"script": "keccak256.js", "sha256": sha256_file(HERE / "keccak256.js")},
            "agree": True,
        },
        "K": len(planted),
        "planted_selectors": planted,
        "erc20_absent_check": {"count": len(erc20), "selectors": erc20, "collisions": collisions},
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(doc, indent=2, sort_keys=False) + "\n")
    print(json.dumps(doc, indent=2))
    print(f"wrote {out_path}  sha256={sha256_file(out_path)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
