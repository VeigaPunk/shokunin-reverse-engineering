#!/usr/bin/env python3
"""Two discriminating probes of the FROZEN attest.py v2 clause set.

P1: an extra table row whose trigger is not a routed `R45-CL<n>` id (the claims'
    clause 4 sentence: 'every row's trigger names a routed R45-CL<n> id').
P2: the Refs paragraph cut to one citation repeated six times (the claims'
    clause 5 sentence: 'at least six citations carry a line selector and resolve').

Each probe builds a one-commit fixture repo under $HYAKU_SCRATCH, commits the
mutated SKILL.md plus every file its citations name, and scores it with the
FROZEN counter bytes copied from `git show <FREEZE>:tools/round-46/`.
Read-only on the lane tree: `git show` only.
"""
import os
import re
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
FROZEN = "/fast/scratch/hyaku/kaidoku-r46/R46W1ScribeLesson/frozen"
SEAT = os.path.join(LANE, ".ufo/waves/round-46/w1/R46W1ScribeLesson")
FREEZE = "65678df0f1666e83cdeea7233bfb31ffe73ec709"
REV = sys.argv[1] if len(sys.argv) > 1 else "0425224756791b414454df28a9abf93dcdf154ce"
REF = re.compile(r"((?:corpus|plans|tools)/[A-Za-z0-9._/-]+)(?::(\d+)(?:-(\d+))?)?")


def git(*args, cwd=LANE):
    return subprocess.run(["git", "-C", cwd, *args], capture_output=True, text=True)


def show(path, rev=REV):
    r = git("show", f"{rev}:{path}")
    return r.stdout if r.returncode == 0 else None


def write(path, text, base):
    full = os.path.join(base, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as fh:
        fh.write(text)


def fixture(name, skill, block):
    d = os.path.join(os.environ["HYAKU_SCRATCH"], "probe-" + name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    subprocess.run(["git", "-C", d, "config", "user.email", "p@round46"], check=True)
    subprocess.run(["git", "-C", d, "config", "user.name", "probe"], check=True)
    top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True).stdout.strip()
    assert top == d, (top, d)
    write("SKILL.md", skill, d)
    need = {"plans/round-46-claims.md", "tools/round-46/attest.py",
            "tools/round-46/gate.py", "corpus/lessons/round-45.md"}
    need |= {m.group(1) for m in REF.finditer(block)}
    for p in sorted(need):
        kind = git("cat-file", "-t", f"{REV}:{p}").stdout.strip()
        if kind != "blob":
            print("   (skip, not a blob at rev:", kind or "absent", ")", p)
            continue
        body = show(p)
        if body is None:
            print("   (skip, absent at rev)", p)
            continue
        write(p, body, d)
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "commit", "-q", "-m", "probe"], check=True)
    return d, subprocess.run(["git", "-C", d, "rev-parse", "HEAD"],
                             capture_output=True, text=True).stdout.strip()


def run(name, d, rev, battery):
    # out_path() scopes --json-out to the MEASURED root, so the receipt lands in
    # the fixture and is copied into the seat dir afterwards.
    out = os.path.join(d, "receipt.json")
    args = [sys.executable, "-I", "-B", os.path.join(FROZEN, "attest.py"),
            "--root", d, "--freeze", rev, "--rev", rev, "--json-out", out]
    if not battery:
        args.append("--no-battery")
    r = subprocess.run(args, capture_output=True, text=True)
    print(f"   {name}: exit={r.returncode}")
    if os.path.exists(out):
        shutil.copyfile(out, os.path.join(SEAT, name + ".json"))
    else:
        print("   stdout:", r.stdout[:400])
    return r.returncode, out


skill = show("SKILL.md")
assert skill, "SKILL.md absent at rev"
start = skill.index("## Queue-drain craft ") + len("## Queue-drain craft ")
sec = skill[start:].split("\n## ", 1)[0]
block = sec.split("\n- **", 1)[1]
block = "- **" + block
assert "<!-- freeze-integrity-table v2 -->" in block, "no v2 marker in the block"

# --- P1: append a row whose trigger is not a routed id -------------------------
row = "| scratch note, no routed id | nothing routed | pin | 0 |"
p1 = skill.replace(block, block.rstrip("\n") + "\n" + row + "\n", 1)
assert p1 != skill

# --- P2: one citation, six times ----------------------------------------------
lines = block.splitlines()
tail = [i for i, l in enumerate(lines) if l.strip().startswith("Refs:")]
assert tail, "no Refs paragraph"
same = "`corpus/lessons/round-45.md:12-30`"
lines[tail[0]] = ("  Refs: " + ", ".join([same] * 6))
p2block = "\n".join(lines) + "\n"
p2 = skill.replace(block, p2block, 1)
assert p2 != skill

for name, text, blk, batt in (("P1-junk-trigger-row", p1, block, True),
                              ("P2-six-identical-refs", p2, p2block, False)):
    print("==", name)
    d, rev = fixture(name, text, blk)
    try:
        code, out = run(name, d, rev, batt)
    finally:
        shutil.rmtree(d, ignore_errors=True)
