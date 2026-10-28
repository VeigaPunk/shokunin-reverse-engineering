#!/usr/bin/env python3
"""Fixture: a craft block that cites only the counter scores as a resolved
depth block under `record.depth_pair` and as unresolved under SCORECARD recipe A.

Builds a one-commit git fixture under the scratch root, proves the top level,
then measures both derivations at the fixture's HEAD.

Usage: python3 -I -B fixture_selfcite.py --scratch <dir>
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

SKILL = """# fixture

## Queue-drain craft (fixture)

- **24. A block that cites the counter itself.** <!-- exactness-table v3 --> The
  only citation is `tools/round-47/exact.py`, which exists at this revision.
"""


def git(root, *args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True, text=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", required=True)
    args = ap.parse_args()
    d = tempfile.mkdtemp(dir=args.scratch, prefix="selfcite-fixture-")
    commands = [f"git -C {d} init -q"]
    git(d, "init", "-q")
    top = git(d, "rev-parse", "--show-toplevel").stdout.strip()
    if top != os.path.realpath(d):
        print(json.dumps({"reason": "fixture toplevel mismatch", "top": top, "dir": d}))
        return 2
    os.makedirs(os.path.join(d, "tools", "round-47"))
    with open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8") as fh:
        fh.write(SKILL)
    with open(os.path.join(d, "tools", "round-47", "exact.py"), "w", encoding="utf-8") as fh:
        fh.write("# fixture stub\n")
    commands.append(f"git -C {d} add SKILL.md tools/round-47/exact.py")
    git(d, "add", "SKILL.md", "tools/round-47/exact.py")
    commands.append(f"git -C {d} -c user.name=fixture -c user.email=fixture@invalid "
                    f"commit -q -m fixture")
    c = git(d, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
            "commit", "-q", "-m", "fixture")
    if c.returncode != 0:
        print(json.dumps({"reason": "fixture commit failed", "stderr": c.stderr}))
        return 2
    rev = git(d, "rev-parse", "HEAD").stdout.strip()

    lane = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
    sys.path.insert(0, os.path.join(lane, "tools", "round-47"))
    sys.path.insert(0, os.path.join(lane, "tools", "round-46"))
    import gate  # noqa: PLC0415
    import record  # noqa: PLC0415
    files = lambda p: gate.show(d, rev, p)  # noqa: E731
    depth = list(record.depth_pair(files))

    # recipe A's knowledge-only pattern over the same fixture
    import pathlib
    import re
    craft = files("SKILL.md").split("## Queue-drain craft ", 1)[1].split("\n## ", 1)[0]
    rules = re.split(r"(?m)^- \*\*", craft)[1:]
    pattern = r"corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?"
    recipe = sum(1 for rule in rules if re.findall(pattern, rule))

    print(json.dumps({
        "fixture": d, "rev": rev, "commands": commands,
        "skill_sha256": __import__("hashlib").sha256(SKILL.encode()).hexdigest(),
        "record_depth_pair": depth,
        "recipe_a_resolved_rules": recipe,
        "rule_blocks": len(rules),
        "record_fraction": "%d/%d" % tuple(depth),
        "recipe_a_fraction": "%d/%d" % (recipe, len(rules)),
        "divergence": depth[0] != recipe,
    }, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
