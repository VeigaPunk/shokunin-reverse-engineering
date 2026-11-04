#!/usr/bin/env python3
"""Preflight variants: tool-tuple order and version fallback."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys

SCRATCH = "/fast/scratch/hyaku/kaidoku-r69/MutBattery"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
REA = "/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents"
PY = sys.executable


def parse(rec):
    for text in (rec.stdout, rec.stderr):
        for chunk in [text] + text.splitlines()[::-1]:
            chunk = chunk.strip()
            if not chunk.startswith("{"):
                continue
            try:
                cand = json.loads(chunk)
            except json.JSONDecodeError:
                continue
            if isinstance(cand, dict) and "unevaluable" in cand:
                return cand["unevaluable"]
    return None


def run(argv, env):
    p = subprocess.run(argv, capture_output=True, text=True, timeout=300, env=env)
    return {"rc": p.returncode, "unevaluable": parse(p),
            "stderr_tail": p.stderr[-300:]}


def main():
    work = os.path.join(SCRATCH, "work")
    no_git = os.path.join(SCRATCH, "pathbin-nogit")
    os.makedirs(no_git, exist_ok=True)
    for t in ("readelf", "upx"):
        found = shutil.which(t)
        link = os.path.join(no_git, t)
        if found and not os.path.exists(link):
            os.symlink(found, link)
    silent = os.path.join(SCRATCH, "upx-silent")
    with open(silent, "w", encoding="utf-8") as fh:
        fh.write('#!/bin/sh\nif [ "$1" = "--version" ]; then exit 0; fi\nexit 3\n')
    os.chmod(silent, 0o755)
    env_nogit = {"PATH": no_git, "HOME": os.environ.get("HOME", "/root"), "LANG": "C"}
    env_normal = {"PATH": os.environ.get("PATH", "/usr/bin"),
                  "HOME": os.environ.get("HOME", "/root"), "LANG": "C"}
    out = {}
    for mid in ("pristine", "MB09_preflight_tool_order", "MB20_version_fallback"):
        path = (os.path.join(SCRATCH, "pristine-packed-elf.py") if mid == "pristine"
                else os.path.join(SCRATCH, mid + "-packed-elf.py"))
        base = [PY, "-I", "-B", path, "--root", LANE, "--rev",
                "f15998102f1ce3569e61faa2ac6f286bc414538e", "--pkg", REA, "--work", work]
        out[mid] = {
            "path_missing_node_and_git": run(base, env_nogit),
            "silent_version_packer": run(base + ["--upx", silent], env_normal),
        }
    print(json.dumps(out, indent=1, sort_keys=True))
    with open(os.path.join(SCRATCH, "preflight-variants.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")


if __name__ == "__main__":
    main()
