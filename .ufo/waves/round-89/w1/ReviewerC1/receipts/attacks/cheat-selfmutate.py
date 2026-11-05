#!/usr/bin/env python3
"""Kill-rule attack: does the receipt pin the repair bytes?

A repair that rewrites its own source file during its first invocation.  The
battery hashes the repair file BEFORE the case loop, so the receipt's
`repair_sha256` records the pre-run bytes while later invocations run the
mutated file.  Score is incidental (this is the stored+8 cheat, red on N3);
the demonstration is the hash comparison after the run.
"""
import importlib.util
import os
import struct
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
R87 = os.path.join(LANE, "tools", "round-87", "upx-magic-repair.py")


def main() -> int:
    a = {}
    for i, x in enumerate(sys.argv):
        if x == "--in":
            a["in"] = sys.argv[i + 1]
        if x == "--out":
            a["out"] = sys.argv[i + 1]
    if "in" not in a or "out" not in a:
        return 2
    with open(__file__, "a") as fh:  # self-mutation, first invocation only
        fh.write(f"\n# mutated during invocation, in={a['in']}\n")
    with open(a["in"], "rb") as fh:
        d = fh.read()
    spec = importlib.util.spec_from_file_location("r87", R87)
    rep = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rep)
    try:
        ph_off, ph = rep.find_packheader(d)
        m, _s, _w = rep.find_linfo(d, ph_off, ph)
    except rep.Refused as exc:
        sys.stderr.write(f"refused: {exc}\n")
        return 3
    b0 = m + 20
    out = bytearray(d)
    stored = struct.unpack_from("<I", d, b0 + 4)[0]
    struct.pack_into("<I", out, b0 + 4, (stored + 8) & 0xFFFFFFFF)
    with open(a["out"], "wb") as fh:
        fh.write(bytes(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/invocations/inv-q7w36mpr/in

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/invocations/inv-sx8j4ihh/in

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/invocations/inv-dz16o9na/in

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/invocations/inv-zm1p4nrw/in

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/invocations/inv-rawe54ox/in

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/invocations/inv-wcicxpr2/in

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/invocations/inv-bdcndd9a/in

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/invocations/inv-0s29xx4q/in

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/invocations/inv-53_b2cdl/in

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/invocations/inv-brla1_x6/in

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/invocations/inv-ldj1y21x/in

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/invocations/inv-pu05vmr_/in

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/invocations/inv-8w70kzmj/in

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/invocations/inv-v7br_3je/in

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/invocations/inv-u_fvv_18/in

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/invocations/inv-ijz9zuuq/in

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/r88-battery-cbryis66/jq/orig

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/r88-battery-cbryis66/jq/packed

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/r88-battery-cbryis66/jq/chain.tampered

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/r88-battery-cbryis66/jq/n2.tampered

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/r88-battery-cbryis66/xxd/orig

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/r88-battery-cbryis66/xxd/packed

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/r88-battery-cbryis66/xxd/chain.tampered

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/r88-battery-cbryis66/xxd/n2.tampered

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/r88-battery-cbryis66/libz/orig

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/r88-battery-cbryis66/libz/packed

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/r88-battery-cbryis66/libz/chain.tampered

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/r88-battery-cbryis66/libz/n2.tampered

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/r88-battery-cbryis66/dinit/orig

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/r88-battery-cbryis66/dinit/packed

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/r88-battery-cbryis66/dinit/chain.tampered

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/r88-battery-cbryis66/dinit/n2.tampered

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/r88-battery-cbryis66/r87-battery-hcqaza57/jq/orig

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/r88-battery-cbryis66/r87-battery-hcqaza57/jq/packed

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/r88-battery-cbryis66/r87-battery-hcqaza57/jq/T1-zero.tampered

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/r88-battery-cbryis66/r87-battery-hcqaza57/jq/T2-foreign.tampered

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/r88-battery-cbryis66/r87-battery-hcqaza57/jq/n2.tampered

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/r88-battery-cbryis66/r87-battery-hcqaza57/xxd/orig

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/r88-battery-cbryis66/r87-battery-hcqaza57/xxd/packed

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/r88-battery-cbryis66/r87-battery-hcqaza57/xxd/T1-zero.tampered

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/r88-battery-cbryis66/r87-battery-hcqaza57/xxd/T2-foreign.tampered

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/r88-battery-cbryis66/r87-battery-hcqaza57/xxd/n2.tampered

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/r88-battery-cbryis66/r87-battery-hcqaza57/libz/orig

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/r88-battery-cbryis66/r87-battery-hcqaza57/libz/packed

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/r88-battery-cbryis66/r87-battery-hcqaza57/libz/T1-zero.tampered

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/r88-battery-cbryis66/r87-battery-hcqaza57/libz/T2-foreign.tampered

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/r88-battery-cbryis66/r87-battery-hcqaza57/libz/n2.tampered

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/r88-battery-cbryis66/r87-battery-hcqaza57/dinit/orig

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/r88-battery-cbryis66/r87-battery-hcqaza57/dinit/packed

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/r88-battery-cbryis66/r87-battery-hcqaza57/dinit/T1-zero.tampered

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/r88-battery-cbryis66/r87-battery-hcqaza57/dinit/T2-foreign.tampered

# mutated during invocation, in=/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/work/r89-battery-9miel6o3/r88-battery-cbryis66/r87-battery-hcqaza57/dinit/n2.tampered
