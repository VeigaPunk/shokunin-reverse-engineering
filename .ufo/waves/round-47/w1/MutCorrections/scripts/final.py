#!/usr/bin/env python3
"""Re-run the surviving corrections mutants at the newest tip (insert-style where the
landed card no longer carries the old axes anchors)."""
import json
import os
import subprocess
import sys

S = "/fast/scratch/hyaku/kaidoku-r47/MutCorrections"
C = S + "/clone"
CARD = C + "/SCORECARD.md"
BASE = "b1a058f32c6908a6b92248052f151d0b0e2c76b1"

SEATS_NOW = "- corrects seats round-45: 2 waves, 76 seats total"
WIN46 = ("- corrects window round-46: empty in 332f4884..58eb04b6"
         " -- tools/round-46 plans/round-46-claims.md")
TAIL = "\n\n## Round 47 "


def insert_before_round(text, line):
    i = text.index(TAIL)
    return text[:i] + "\n" + line + text[i:]


MUT = {
    "cross-round-total": lambda t: t.replace(
        SEATS_NOW, "- corrects seats round-45: 2 waves, 80 seats total", 1),
    "wrong-round-historical-true": lambda t: t.replace(
        SEATS_NOW, "- corrects seats round-43: 2 waves, 64 seats total", 1),
    "window-pair-out-of-scope": lambda t: t.replace(
        WIN46, "- corrects window round-46: empty in 332f4884..332f4884"
               " -- tools/round-46 plans/round-46-claims.md", 1),
    "window-pair-real-other-commits": lambda t: t.replace(
        WIN46, "- corrects window round-46: empty in 1e2c310295..07d2894eab"
               " -- tools/round-47/exact.py", 1),
    "duplicate-correction": lambda t: t.replace(SEATS_NOW, SEATS_NOW + "\n" + SEATS_NOW, 1),
    "false-axes-correction": lambda t: insert_before_round(
        t, "- corrects axes coverage: 1/2"),
    "window-pair-atom-range": lambda t: t.replace(
        WIN46, "- corrects window round-46: empty in 0425224..58eb04b6"
               " -- tools/round-46 plans/round-46-claims.md", 1),
}

rows = []
for name, fn in MUT.items():
    subprocess.run(["git", "-C", C, "checkout", "-q", BASE, "--", "SCORECARD.md"],
                   check=True)
    text = open(CARD).read()
    out = fn(text)
    assert out != text, name + " no-op"
    open(CARD, "w").write(out)
    subprocess.run(["git", "-C", C, "add", "SCORECARD.md"], check=True)
    subprocess.run(["git", "-C", C, "commit", "-q", "-m", "mut2: " + name], check=True)
    rev = subprocess.run(["git", "-C", C, "rev-parse", "HEAD"], capture_output=True,
                         text=True).stdout.strip()
    for mode in ("no-battery", "battery"):
        extra = ["--no-battery"] if mode == "no-battery" else []
        r = subprocess.run(["python3", "-I", "-B", "tools/round-47/record.py",
                            "--root", C, "--rev", rev, *extra,
                            "--json-out", "receipts/%s.%s.json" % (name, mode)],
                           cwd=C, capture_output=True, text=True)
        rec = json.load(open("%s/receipts/%s.%s.json" % (C, name, mode)))
        rows.append({"mutation": name, "rev": rev, "mode": mode, "exit": r.returncode,
                     "failing": rec.get("failing"),
                     "corrections": rec.get("corrections"),
                     "corrections_bad": len(rec.get("corrections_bad") or []),
                     "exempted": len(rec.get("exempted") or []),
                     "atoms": rec.get("atoms"),
                     "forgeries_green": (rec.get("battery") or {}).get("forgeries_green")})
        print(name, mode, r.returncode, rec.get("failing"),
              "corrections", rec.get("corrections"), "atoms", rec.get("atoms"))

subprocess.run(["git", "-C", C, "reset", "-q", "--hard", BASE], check=True)
print("restored", subprocess.run(["git", "-C", C, "rev-parse", "HEAD"],
                                 capture_output=True, text=True).stdout.strip())
json.dump(rows, open(S + "/out/final-tip.json", "w"), indent=1)
