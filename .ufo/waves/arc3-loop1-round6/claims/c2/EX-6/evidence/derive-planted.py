#!/usr/bin/env python3
"""EX-6 seat: derive the planted selector set pre-compile/pre-probe."""
import json, sys, datetime
sys.path.insert(0, ".")
from keccak import selector

SIGS = [
    "owner()", "feeBps()", "scaleUnits()", "pausedFlag()", "totalHeld()",
    "heldBy(address)", "computeFee(uint256)", "halve(uint256)",
    "setFee(uint256)", "depositFor(address)", "pauseSwitch(bool)",
    "transferOwnership(address)",
]
ERC20 = ["transfer(address,uint256)", "transferFrom(address,address,uint256)",
         "approve(address,uint256)", "balanceOf(address)", "totalSupply()",
         "allowance(address,address)", "name()", "symbol()"]
erc20_sel = {s: selector(s) for s in ERC20}
sel = {s: selector(s) for s in SIGS}
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
doc = {
    "recorded_utc": now,
    "contract": "ViaIRVault",
    "phase": "pre-compile pre-probe",
    "derivation": "pure-Python keccak256 (evidence/keccak.py, VECTORS PASS; copied from .ufo/waves/arc3-loop1-round3/claims/c1/EX-10/keccak.py)",
    "planted": [{"signature": s, "selector_hex4": sel[s]} for s in SIGS],
    "K": len(SIGS),
    "non_selector_abi_entries": ["receive()", "fallback()"],
    "erc20_absence": {
        "checked_selectors": erc20_sel,
        "collisions_with_planted": sorted(set(erc20_sel.values()) & set(sel.values())),
    },
}
open("planted-K.json", "w").write(json.dumps(doc, indent=2) + "\n")
with open("planted.txt", "w") as f:
    for s in SIGS:
        f.write(f"{sel[s]}  {s}\n")
print("recorded_utc:", now, "K:", len(SIGS))
for s in SIGS:
    print(f"{sel[s]}  {s}")
print("erc20 collisions:", doc["erc20_absence"]["collisions_with_planted"])
