#!/usr/bin/env python3
"""verify-probe.py — seat EX-05 (chain c1, arc3-loop1-round4).

Re-derives planted-vs-probe.txt: compares this seat's planted selector set
against the carrierV probe envelopes copied byte-identical into probe-pins/
(from RV-2's own legs). Writes planted-vs-probe.txt and probe-ids.txt.
"""
import glob
import hashlib
import json

SEAT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round4/claims/c1/EX-05"


def main():
    full = json.load(open(f"{SEAT}/planted-full.json"))
    planted = {e["selector"][2:] for e in full["entries"]}

    lines = ["== planted-vs-probe (RV-2 carrierV legs, copied byte-identical into probe-pins/) =="]
    lines.append(f"planted-full.json sha256 {hashlib.sha256(open(f'{SEAT}/planted-full.json','rb').read()).hexdigest()}")
    lines.append(f"planted K = {len(planted)}")
    ids = ["== probe evidence ids (from probe-pins/, copied byte-identical) =="]
    for p in sorted(glob.glob(f"{SEAT}/probe-pins/*.json")):
        d = json.load(open(p))
        fns = d.get("normalized_result", {}).get("functions", [])
        got = {f["selector"][2:] for f in fns}
        sha = hashlib.sha256(open(p, "rb").read()).hexdigest()
        lines.append("")
        lines.append(f"file: {p.split('/')[-1]}  sha256 {sha}")
        lines.append(f"  functions: {len(fns)} | dispatch set: {sorted(set(f.get('dispatch') for f in fns))}")
        lines.append(f"  missing (planted - recovered): {sorted(planted - got) or 'none'}")
        lines.append(f"  extra   (recovered - planted): {sorted(got - planted) or 'none'}")
        lines.append(f"  decoded bytecode sha256: {d.get('normalized_result',{}).get('bytecode',{}).get('sha256')}")
        ids.append(f"{p.split('/')[-1]}")
        ids.append(f"  evidence_id: {d.get('evidence_id')}")
        ids.append(f"  operation: {d.get('operation')} | predicate_type: {d.get('predicate_type')} | authority: {d.get('authority')}")
        ids.append(f"  provider: {d.get('provider',{}).get('id')} {d.get('provider',{}).get('version')}")
        ids.append(f"  confidence: {d.get('confidence')}")

    open(f"{SEAT}/planted-vs-probe.txt", "w").write("\n".join(lines) + "\n")
    open(f"{SEAT}/probe-ids.txt", "w").write("\n".join(ids) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
