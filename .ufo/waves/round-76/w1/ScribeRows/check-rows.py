#!/usr/bin/env python3
"""Mechanical checks on the three draft rows against their pinned snapshots."""
import hashlib
import html
import re
import sys
from pathlib import Path

S = Path("/fast/scratch/hyaku/kaidoku-r76/ScribeRows")
rows = [l.rstrip("\n") for l in (S / "rows-draft.md").read_text().splitlines() if l.strip()]
fail = []


def check(cond, msg):
    print(("ok   " if cond else "FAIL ") + msg)
    if not cond:
        fail.append(msg)


def cells(row):
    return [c.strip() for c in row.split("|")[1:-1]]


check(len(rows) == 3, f"three draft rows (got {len(rows)})")
parsed = []
for row in rows:
    cs = cells(row)
    parsed.append(cs)
    check(len(cs) == 11, f"{cs[0]}: 11 cells (got {len(cs)})")
    check("\\|" not in row, f"{cs[0]}: no escaped pipe in the row")
    check(all("|" not in c for c in cs), f"{cs[0]}: no literal pipe inside a cell")
    check(cs[0] in {"S286", "S287", "S288"}, f"{cs[0]}: id in the frozen set")
    check(cs[2] == "docs", f"{cs[0]}: kind docs")
    check(cs[3] in {"A", "C"}, f"{cs[0]}: tier A or C")
    check(cs[7] in {"mined", "rejected"}, f"{cs[0]}: status mined or rejected")
    check(cs[8] == "2026-11-04", f"{cs[0]}: opened 2026-11-04")
    check(re.fullmatch(r"\d+d|[A-Za-z][A-Za-z0-9 _-]*", cs[9]) is not None,
          f"{cs[0]}: recheck cadence {cs[9]!r}")

snap = {
    "shlex": S / "shlex.html",
    "argparse": S / "argparse.html",
    "sh1": S / "sh1.html",
}
digest = {k: hashlib.sha256(p.read_bytes()).hexdigest() for k, p in snap.items()}
size = {k: len(p.read_bytes()) for k, p in snap.items()}
lines = {k: p.read_text(errors="replace").splitlines() for k, p in snap.items()}

# (key, line span of the quote, rendered quote, expected word count, line of the heading)
quotes = [
    ("shlex", (229, 229), "Split the string s using shell-like syntax.", 7, 218,
     "Simple lexical analysis"),
    ("argparse", (2417, 2418),
     "This method prints a usage message, including the message, to sys.stderr "
     "and terminates the program with a status code of 2.", 21, 2398,
     "Exiting methods"),
    ("sh1", (6, 6), "The requested URL was not found on this server.", 9, 3,
     "404 Not Found"),
]

def strip(line):
    return html.unescape(re.sub(r"<[^>]+>", "", line))

for key, (a, b), quote, words, hline, heading in quotes:
    joined = " ".join(strip(l) for l in lines[key][a - 1:b])
    joined = re.sub(r"\s+", " ", joined).strip()
    check(quote in joined, f"{key}: quote is contiguous in rendered lines {a}-{b}")
    check(len(quote.split()) == words, f"{key}: quote word count {len(quote.split())} == {words}")
    check(words <= 25, f"{key}: quote <= 25 words")
    check(heading in lines[key][hline - 1], f"{key}: heading at line {hline} is {heading!r}")

# sha256 and byte-count claims inside the anchor cells
anch = {cs[0]: cs[5] for cs in parsed}
check(digest["shlex"] in anch["S286"] and "66 497" in anch["S286"], "S286: anchor pins shlex digest and size")
check(digest["argparse"] in anch["S287"] and "334 994" in anch["S287"], "S287: anchor pins argparse digest and size")
check(digest["sh1"] in anch["S288"] and "196" in anch["S288"], "S288: anchor pins 404 digest and size")
check(lines["shlex"][226].startswith('<dt class="sig sig-object py" id="shlex.split">'),
      "S286: dt at line 227 is the shlex.split entry")
check('id="argparse.ArgumentParser.error"' in lines["argparse"][2414],
      "S287: dt at line 2415 is the ArgumentParser.error entry")
check('id="argparse.ArgumentParser.exit"' in lines["argparse"][2399],
      "S287: exit entry dt at line 2400")
check("SYNOPSIS" not in "\n".join(lines["sh1"]) and "DESCRIPTION" not in "\n".join(lines["sh1"]),
      "S288: the 404 body carries no SYNOPSIS/DESCRIPTION")

# reject row grammar: reason + flip, three words each
teach = {cs[0]: cs[6] for cs in parsed}
m = re.search(r"REJECTED: (.+?)\. Flip: (.+?)\.?$", teach["S288"])
check(m is not None, "S288: teaches carries `REJECTED: ... Flip: ...`")
if m:
    check(len(m.group(1).split()) >= 3, "S288: reason >= 3 words")
    check(len(m.group(2).split()) >= 3, "S288: flip >= 3 words")
check("grep -c 'shell=True' tools/round-76/plan-command.py" in teach["S288"],
      "S288: teaches records the consumer search")

print()
print("FAILURES:", len(fail))
sys.exit(1 if fail else 0)
