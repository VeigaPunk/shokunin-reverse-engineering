#!/usr/bin/env python3
"""R8: serves ONLY the round-87 magic class (composed r87 repair, no geometry).

Isolates the regression arm: if the battery's regression arm is met while the
main T3-chain-szcpr cases all fail, the regression arm alone carries no
chain-geometry information.
"""
import sys

sys.path.insert(0, "/fast/scratch/hyaku/kaidoku-r88/ReviewerC1")
import vcommon as V  # noqa: E402


def repair_r87_only(rule: str, d: bytes):
    if d[:4] != b"\x7fELF" or len(d) < 64 or d[5] != 1:
        raise V.Refused("not a little-endian ELF")
    rep = V.load_r87()
    try:
        out, info = rep.repair(d)
    except rep.Refused as exc:
        raise V.Refused(f"r87-only: {exc}")
    info["class"] = "anchor" if not info.get("intact") else "intact"
    return out, info


V.repair = repair_r87_only  # noqa: SLF001 - scratch probe override
raise SystemExit(V.main("R8-r87-only"))
