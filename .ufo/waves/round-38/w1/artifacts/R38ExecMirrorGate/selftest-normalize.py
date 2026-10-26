#!/usr/bin/env python3
"""selftest-normalize.py — falsifier battery for normalize-append.py (R38ExecMirrorGate).

Each case writes a one-row block, runs the normalizer, and checks the finding code and
exit status. Exit 0 only if every case is killed.
"""
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
NORM = os.path.join(HERE, "normalize-append.py")
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
SOURCES = os.path.join(LANE, "corpus/SOURCES.md")
ENTRY = "corpus/knowledge/2026-10-26-r38-squashfs-be-recursion.md"

CELLS = ["S120", "A row — https://example.invalid/a", "code", "A", "scope one",
         "anchor one", "A teaches cell long enough to pass.", "mined",
         "2026-10-26", "on-release", ENTRY]


def row(cells):
    return "| " + " | ".join(cells) + " |\n"


def first_mined_url_scope(path):
    """First mined Registry row's (source cell, scope cell) — the E04 collision target."""
    in_registry = False
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            s = line.rstrip("\n")
            t = s.lstrip(" ")
            ind = len(s) - len(t)
            if ind <= 3 and t.startswith("## "):
                in_registry = t[3:].strip() == "Registry"
                continue
            if not in_registry or ind > 3 or not t.startswith("|"):
                continue
            body = t[1:]
            if body.endswith("|"):
                body = body[:-1]
            c = [x.strip() for x in body.split("|")]
            if len(c) < 11 or c[0] == "id":
                continue
            if c[7] == "mined" and "http" in c[1]:
                return c[1], c[4]
    raise SystemExit("no mined registry row with a URL found")


DUP_URL, DUP_SCOPE = first_mined_url_scope(SOURCES)


def mutate(**kw):
    c = list(CELLS)
    for k, v in kw.items():
        c[int(k[1:])] = v
    return c


CASES = [
    ("G0-green", [row(CELLS), row(mutate(c0="S121", c1="B row — https://example.invalid/b"))],
     None, 0),
    ("G1-rejected-row", [row(mutate(c0="S122", c1="Rejected tool — https://example.invalid/7z",
                                     c6="Cannot open the image as archive, so the route is rejected.",
                                     c7="rejected", c10="\u2014"))], None, 0),
    ("R1-literal-pipe", [row(mutate(c4="scope|pipe"))], "N01", 1),
    ("R2-escaped-pipe", [row(mutate(c4="scope\\|pipe"))], "N01", 1),
    ("R3-id-collision", [row(mutate(c0="S106"))], "N03", 1),
    ("R4-dup-url-scope", [row(mutate(c1=DUP_URL, c4=DUP_SCOPE))], "N14", 1),
    ("R5-status-queued", [row(mutate(c7="queued"))], "N06", 1),
    ("R6-wrong-opened", [row(mutate(c8="2026-10-19"))], "N07", 1),
    ("R7-bad-recheck", [row(mutate(c9="bogus-cadence!!"))], "N08", 1),
    ("R8-usedby-not-admitted", [row(mutate(c10="corpus/knowledge/other.md"))], "N13", 1),
    ("R9-usedby-extra", [row(mutate(c10=ENTRY + ", corpus/lessons/round-38.md"))], "N13", 1),
    ("R10-bad-kind", [row(mutate(c2="blob"))], "N04", 1),
    ("R11-tierC-mined", [row(mutate(c3="C"))], "N09", 1),
    ("R12-empty-block", ["# no rows here\n"], None, 1),
    ("R13-bad-tier", [row(mutate(c3="D"))], "N05", 1),
    ("R14-thin-teaches", [row(mutate(c6="short"))], "N11", 1),
]

fail = 0
tmp = tempfile.mkdtemp(prefix="norm-selftest.")
for name, lines, want_code, want_rc in CASES:
    block = os.path.join(tmp, name + ".md")
    with open(block, "w", encoding="utf-8") as fh:
        fh.writelines(lines)
    out = os.path.join(tmp, name + ".out")
    p = subprocess.run([sys.executable, "-I", "-B", NORM, "--block", block,
                        "--sources", SOURCES, "--out", out, "--used-by", ENTRY],
                       capture_output=True, text=True)
    got_codes = {tok.split()[0] for tok in p.stdout.splitlines() if tok[:1] in "N"}
    code_ok = (want_code is None and not got_codes) or (want_code in got_codes)
    rc_ok = p.returncode == want_rc
    if code_ok and rc_ok:
        print(f"killed\t{name}\t{','.join(sorted(got_codes)) or 'clean'}\trc={p.returncode}")
    else:
        fail = 1
        print(f"SURVIVED\t{name}\twant={want_code}/rc{want_rc} got={sorted(got_codes)}/rc{p.returncode}")
        print("  stdout:", p.stdout.replace("\n", " | "))
        print("  stderr:", p.stderr.replace("\n", " | "))

import shutil
shutil.rmtree(tmp, ignore_errors=True)
print("selftest ok" if fail == 0 else "selftest FAILED")
sys.exit(0 if fail == 0 else 1)
