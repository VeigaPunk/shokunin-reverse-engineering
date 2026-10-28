#!/usr/bin/env python3
"""Build one-commit fixture repos in scratch holding the lane's round-46 refs.

Usage: build.py <fixture-name> <mode: attest|registry|raw> [--drop PATH]...
Writes $S/fx/<name> (git repo, one commit) and prints the commit id.
Mutation of SKILL.md is done by the caller through the `transform` hook file
$S/fx/<name>.py, which must define transform(skill_text) -> str.
"""
import json
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = os.environ["HYAKU_SCRATCH"]
HARD = re.compile(r"((?:corpus|plans|tools)/[A-Za-z0-9._/-]+)(?::(\d+)(?:-(\d+))?)?")


def git(*args, cwd=None, check=False):
    return subprocess.run(["git", *args], capture_output=True, text=True, cwd=cwd, check=check)


def lane_show(path, rev="HEAD"):
    r = git("-C", LANE, "show", f"{rev}:{path}")
    return r.stdout if r.returncode == 0 else None


def main(name, mode, drops):
    d = os.path.join(S, "fx", name)
    subprocess.run(["rm", "-rf", d], check=True)
    os.makedirs(d)
    git("-C", d, "init", "-q", check=True)
    for k, v in (("user.email", "fx@round46"), ("user.name", "round46 fixture")):
        git("-C", d, "config", k, v, check=True)
    top = git("-C", d, "rev-parse", "--show-toplevel").stdout.strip()
    if top != d:
        sys.exit(f"FIXTURE TOPLEVEL MISMATCH: {top} != {d}")

    skill = lane_show("SKILL.md")
    block_start = skill.index("- **23. ")
    block_end = skill.index("\n## ", block_start + 10)
    block = skill[block_start:block_end]
    refs = [m[0] for m in HARD.findall(block)]

    paths = {"SKILL.md", "plans/round-46-claims.md", "tools/round-46/attest.py",
             "tools/round-46/registry.py", "tools/round-46/gate.py",
             "tools/round-46/census.json", "tools/round-46/census.py"} | set(refs)
    if mode == "registry":
        census = json.loads(lane_show("tools/round-46/census.json"))
        paths |= set(census["paths"])
    paths -= set(drops)

    for p in sorted(paths):
        body = lane_show(p)
        if body is None:
            print(f"MISS {p}")
            continue
        full = os.path.join(d, p)
        os.makedirs(os.path.dirname(full) or d, exist_ok=True)
        with open(full, "w", encoding="utf-8", newline="") as fh:
            fh.write(body)

    hook = os.path.join(S, "fx", name + ".py")
    if os.path.exists(hook):
        ns = {}
        exec(compile(open(hook).read(), hook, "exec"), ns)
        skill = ns["transform"](skill)
    with open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8", newline="") as fh:
        fh.write(skill)

    git("-C", d, "add", "-A", check=True)
    git("-C", d, "commit", "-q", "-m", "fixture", check=True)
    rev = git("-C", d, "rev-parse", "HEAD").stdout.strip()
    print(json.dumps({"fixture": d, "rev": rev, "files": len(paths),
                      "block_start": block_start, "block_end": block_end,
                      "refs": len(refs)}))


if __name__ == "__main__":
    drops = [a.split("=", 1)[1] for a in sys.argv if a.startswith("--drop=")]
    main(sys.argv[1], sys.argv[2], drops)
