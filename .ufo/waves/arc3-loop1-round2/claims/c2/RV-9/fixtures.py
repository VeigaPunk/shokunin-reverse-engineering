#!/usr/bin/env python3
"""RV-9 independent fixture battery against the captured post-edit census
(/var/tmp/rv9-round2/c1-census-post.py, sha a4c16763… pinned by capture).
Every root is a /var/tmp copy; the repo tree is never a --root.
"""
import os
import re
import shutil
import subprocess
import sys

W = "/var/tmp/rv9-round2/fx"
REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
POST = "/var/tmp/rv9-round2/c1-census-post.py"
FILES = ["PROVINCE.md", "SKILL.md", "SCORECARD.md"]


def fresh(name):
    d = os.path.join(W, name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    for f in FILES:
        shutil.copy(os.path.join(REPO, f), d)
    return d


def run(case, census, root):
    p = subprocess.run([sys.executable, census, "--root", root],
                       capture_output=True, text=True)
    out = p.stdout + p.stderr
    open("/var/tmp/rv9-round2/fx-%s.out" % case, "w").write(out + "EXIT=%d\n" % p.returncode)
    keys = [l for l in out.splitlines()
            if l.startswith(("UNREADABLE", "G2 positive", "DECLARED", "VERDICT", "ANCHOR"))]
    print("[%s] exit=%d" % (case, p.returncode))
    for k in keys:
        print("    " + k)
    return p.returncode, out


def neuter(src, dst, which):
    txt = open(src, encoding="utf-8").read()
    subs = {
        "all": [('PIN = re.compile(r"rea-agents@(\\d+\\.\\d+\\.\\d+)", re.I)',
                 'PIN = re.compile(r"zzz-never@(\\d+\\.\\d+\\.\\d+)", re.I)'),
                ('VER = re.compile(r"(?<![\\d.])6\\.\\d+\\.\\d+")',
                 'VER = re.compile(r"zzz-never-6\\.\\d+\\.\\d+")'),
                ('PTR = re.compile(r"((?:~|/)[\\w./+-]+\\.(?:json|toml|ya?ml)):(\\d+)")',
                 'PTR = re.compile(r"zzz-never-ptr:(\\d+)")')],
        "pin": [('PIN = re.compile(r"rea-agents@(\\d+\\.\\d+\\.\\d+)", re.I)',
                 'PIN = re.compile(r"zzz-never@(\\d+\\.\\d+\\.\\d+)", re.I)')],
        "skill-only": [('VER = re.compile(r"(?<![\\d.])6\\.\\d+\\.\\d+")',
                        'VER = re.compile(r"(?<![\\d.])6\\.666\\.666")')],
    }[which]
    for old, new in subs:
        assert old in txt, old[:60]
        txt = txt.replace(old, new, 1)
    open(dst, "w", encoding="utf-8").write(txt)
    return dst


print("== control: ordinary fixture, all three files intact ==")
d = fresh("ctrl")
run("ctrl", POST, d)

print("== H1-a: SKILL.md absent ==")
d = fresh("h1-skill-absent")
os.remove(os.path.join(d, "SKILL.md"))
run("h1-skill-absent", POST, d)

print("== H1-b: PROVINCE.md absent ==")
d = fresh("h1-province-absent")
os.remove(os.path.join(d, "PROVINCE.md"))
run("h1-province-absent", POST, d)

print("== per-file collapse (my attack): SKILL.md replaced by 371 needle-free filler lines ==")
d = fresh("filler-skill")
with open(os.path.join(d, "SKILL.md"), "w") as fh:
    fh.write("\n".join("plain filler line %d" % i for i in range(1, 372)) + "\n")
run("filler-skill", POST, d)

print("== H3: all needles neutered (global blindness) ==")
d = fresh("blind-all")
neut = neuter(POST, "/var/tmp/rv9-round2/post-blind-all.py", "all")
run("blind-all", neut, d)

print("== H3-partial: PIN only neutered (named residual, expecting PASS) ==")
neut = neuter(POST, "/var/tmp/rv9-round2/post-blind-pin.py", "pin")
run("blind-pin", neut, d)

print("== H2 residual (named open): PROVINCE.md:44 pin -> rea-agents@6.4.0 with inline marker ==")
d = fresh("h2-marker")
p = os.path.join(d, "PROVINCE.md")
txt = open(p, encoding="utf-8").read().splitlines()
hit = False
for i, l in enumerate(txt):
    if "6.5.0" in l and i < 60:
        txt[i] = re.sub(r"6\.5\.0", "6.4.0", l) + "  (historical)"
        hit = True
        break
assert hit
open(p, "w").write("\n".join(txt) + "\n")
run("h2-marker", POST, d)
