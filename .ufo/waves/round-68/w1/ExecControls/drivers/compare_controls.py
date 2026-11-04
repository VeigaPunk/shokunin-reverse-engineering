#!/usr/bin/env python3
"""compare_controls.py - field-for-field comparison of the rerun controls payload
against the L1's pre-integration receipt. Nothing is normalised away: key sets,
list lengths, element order and scalar values all count.
"""
from __future__ import annotations

import json
import os
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
PRE = os.path.join(LANE, ".ufo", "waves", "round-68", "l1", "pre",
                   "controls-at-base.json")
CUR = os.path.join(LANE, ".ufo", "waves", "round-68", "w1", "ExecControls",
                   "controls-rerun.json")
OUT = os.path.join(LANE, ".ufo", "waves", "round-68", "w1", "ExecControls",
                   "controls-compare.json")


def diff(x, y, path: str = "") -> list[dict]:
    out: list[dict] = []
    here = path or "$"
    if type(x) is not type(y):
        return [{"path": here, "kind": "type", "pre": type(x).__name__,
                 "rerun": type(y).__name__}]
    if isinstance(x, dict):
        for key in sorted(set(x) | set(y)):
            sub = f"{here}.{key}"
            if key not in x:
                out.append({"path": sub, "kind": "only-in-rerun", "rerun": y[key]})
            elif key not in y:
                out.append({"path": sub, "kind": "only-in-pre", "pre": x[key]})
            else:
                out.extend(diff(x[key], y[key], sub))
    elif isinstance(x, list):
        if len(x) != len(y):
            out.append({"path": here, "kind": "length", "pre": len(x),
                        "rerun": len(y)})
        for i, (xi, yi) in enumerate(zip(x, y)):
            out.extend(diff(xi, yi, f"{here}[{i}]"))
    elif x != y:
        out.append({"path": here, "kind": "value", "pre": x, "rerun": y})
    return out


def main() -> int:
    with open(PRE, encoding="utf-8") as fh:
        pre = json.load(fh)
    with open(CUR, encoding="utf-8") as fh:
        cur = json.load(fh)
    differences = diff(pre, cur)
    pre_arms = [a["id"] for a in pre.get("arms", [])]
    cur_arms = [a["id"] for a in cur.get("arms", [])]
    per_arm = {}
    for ident in sorted(set(pre_arms) | set(cur_arms)):
        pa = next((a for a in pre["arms"] if a["id"] == ident), None)
        ca = next((a for a in cur["arms"] if a["id"] == ident), None)
        per_arm[ident] = {"present_in_pre": pa is not None,
                          "present_in_rerun": ca is not None,
                          "equal": pa == ca}
    payload = {
        "schema": "kaidoku-r68-controls-compare-v1",
        "pre": os.path.relpath(PRE, LANE),
        "rerun": os.path.relpath(CUR, LANE),
        "equal": not differences,
        "differences": differences,
        "arm_order_equal": pre_arms == cur_arms,
        "arms": per_arm,
        "counts": {"pre_arms": len(pre_arms), "rerun_arms": len(cur_arms),
                   "pre_green": len(pre.get("green", [])),
                   "rerun_green": len(cur.get("green", [])),
                   "pre_ok": pre.get("ok"), "rerun_ok": cur.get("ok")},
        "by_id_equal": sorted(pre_arms) == sorted(cur_arms) and all(
            v["equal"] for v in per_arm.values()),
    }
    text = json.dumps(payload, indent=1, sort_keys=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text + "\n")
    print(text)
    return 0 if payload["equal"] and payload["by_id_equal"] else 1


if __name__ == "__main__":
    sys.exit(main())
