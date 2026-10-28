#!/usr/bin/env python3
"""C1Refs — end-to-end: run the FROZEN counter's own CLI on a two-commit fixture repo.

commit 1 = the lane's bytes at the freeze rev (SKILL.md still has 23 craft blocks)
commit 2 = the landing commit: SKILL.md with block 24 inserted at the end of the craft section
Then: python3 -I -B <lane>/tools/round-47/exact.py --root <fx> --freeze <c1> --rev <c2>
"""
import json
import os
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
REV = "5017e1f7299c3a812e87e7950148f54313dd279e"
SCRATCH = os.environ["HYAKU_SCRATCH"]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(LANE, "tools", "round-47"))
sys.path.insert(0, os.path.join(LANE, "tools", "round-46"))
import exact  # noqa: E402
import gate   # noqa: E402

from drive import BODY  # noqa: E402

_KNOW = gate.git(LANE, "ls-tree", "-r", "--name-only", REV, "--", "corpus/knowledge").stdout.split()
FILES = ["SKILL.md", exact.CLAIMS, exact.SELF, exact.GATE46, exact.MUST_CITE,
         "corpus/lessons/round-45.md", "corpus/README.md"] + _KNOW


def g(*args, cwd=None, check=True):
    r = subprocess.run(["git", "-C", cwd, *args], capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {args}: {r.stderr}")
    return r.stdout


def build(land_body):
    d = os.path.join(SCRATCH, "land-%d" % os.getpid())
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    g("init", "-q", cwd=d)
    g("config", "user.email", "fx@round47", cwd=d)
    g("config", "user.name", "round47 fixture", cwd=d)
    top = g("rev-parse", "--show-toplevel", cwd=d).strip()
    assert top == d, (top, d)
    files = {p: gate.show(LANE, REV, p) for p in FILES}
    for p, text in files.items():
        full = os.path.join(d, p)
        os.makedirs(os.path.dirname(full) or d, exist_ok=True)
        with open(full, "w") as fh:
            fh.write(text)
    g("add", "-A", cwd=d)
    g("commit", "-q", "-m", "freeze", cwd=d)
    c1 = g("rev-parse", "HEAD", cwd=d).strip()
    skill = files["SKILL.md"]
    blocks = exact.blocks_of(skill)
    assert len([b for b in blocks if exact.MARKER in b]) == 0, "fixture freeze already has a marker"
    skill = skill.replace(blocks[-1], blocks[-1] + "- **" + land_body, 1)
    with open(os.path.join(d, "SKILL.md"), "w") as fh:
        fh.write(skill)
    g("add", "-A", cwd=d)
    g("commit", "-q", "-m", "land block 24", cwd=d)
    c2 = g("rev-parse", "HEAD", cwd=d).strip()
    return d, c1, c2


def run(root, freeze, rev, profile="v3"):
    cmd = [sys.executable, "-I", "-B", os.path.join(LANE, "tools", "round-47", "exact.py"),
           "--root", root, "--freeze", freeze, "--rev", rev, "--profile", profile]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=SCRATCH)
    try:
        receipt = json.loads(r.stdout)
    except Exception:  # noqa: BLE001
        receipt = {"stdout_head": r.stdout[:400], "stderr_head": r.stderr[:400]}
    return {"cmd": " ".join(cmd), "exit": r.returncode,
            "failing": receipt.get("failing"), "met_target": receipt.get("met_target"),
            "refs": receipt.get("refs"),
            "battery": receipt.get("battery"),
            "frozen_path_changed": receipt.get("frozen_path_changed"),
            "rule_blocks": receipt.get("rule_blocks"),
            "stdout_sha256": __import__("hashlib").sha256(r.stdout.encode()).hexdigest()}


def main():
    out = {}
    for name, body in (("candidate", BODY),
                       ("candidate-plus-knowledge-cite", BODY.rstrip("\n") +
                        " , `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md:40-66`\n"),
                       ("clause8-green-others-red", BODY.replace(
                           "| R46-CL6 one flag reorder",
                           "| R46-CL2 a fifth row that repeats a routed id | duplicate | order | 1 |\n"
                           "| R46-CL6 one flag reorder"))):
        d, c1, c2 = build(body)
        try:
            ra = subprocess.run([sys.executable, "-I", "-B",
                                 os.path.join(os.path.dirname(os.path.abspath(__file__)), "recipeA.py"),
                                 d, c2], capture_output=True, text=True, cwd=SCRATCH)
            out[name] = {"fixture": d, "freeze": c1, "rev": c2,
                         "v3": run(d, c1, c2), "v2": run(d, c1, c2, "v2"),
                         "recipeA_exit": ra.returncode, "recipeA": ra.stdout.strip() or ra.stderr[:300]}
        finally:
            shutil.rmtree(d, ignore_errors=True)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
