#!/usr/bin/env python3
"""Probe 2: the placeholder-exemption guard and the last-two-section scope slide."""
import sys, os
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0, os.path.join(LANE, "tools", "round-47"))
sys.path.insert(0, os.path.join(LANE, "tools", "round-46"))
import record  # noqa: E402

REV = "3186f69b49798f2cc05727bbfd1604505fcee03b"
files = lambda p: record.gate.show(LANE, REV, p)  # noqa: E731
card0 = files("SCORECARD.md")

COV_OLD = "| coverage | 9.72 → 10.0 | 133/133 knowledge files mapped after the round-41 landing"
COV_NEW = "| coverage | 9.72 → 10.0 | 138/138 knowledge files mapped at the round-47 landing; 133/133 knowledge files mapped after the round-41 landing"
DEP_OLD = "| depth | 10 → 10 | 20/20 queue-drain rule blocks have resolvable file/range citations"
DEP_NEW = "| depth | 10 → 10 | 23/23 queue-drain rule blocks have resolvable file/range citations at `3186f69b`; 20/20 queue-drain rule blocks have resolvable file/range citations"

H = "## Record corrections — round 47"
SEATS = "- corrects seats round-45: 2 waves, 76 seats total"
WIN = ("- corrects window round-46: empty in 0425224..3ffbe0f8 -- tools/round-46 "
       "plans/round-46-claims.md")
R47 = """

## Round 47 — the exactness matrix and the self-assessment re-derivation

Base `13a9e9e1`. Freeze `5017e1f7`. Waves: 75 seats (`.ufo/waves/round-47/w1-dispatch.json`).
"""


def base(axes=True, window="0425224..3ffbe0f8", corr=(SEATS, WIN), tail=""):
    t = card0
    if axes:
        t = t.replace(COV_OLD, COV_NEW, 1).replace(DEP_OLD, DEP_NEW, 1)
    if window:
        t = t.replace("0425224..<tip>", window, 1)
    t += "\n" + H + "\n\n" + "\n".join(corr) + "\n" + tail
    return t


def show(name, text, battery=False):
    code, rec = record.evaluate_text(text, files, LANE, REV, battery=None)
    bat = None
    if battery and code in (0, 1):
        bat = record.run_battery(text, files, LANE, REV)
        code, rec = record.evaluate_text(text, files, LANE, REV, battery=bat)
    print(f"\n=== {name}: exit {code}")
    print("  sections:", rec.get("sections"))
    print("  failing:", rec.get("failing"))
    print("  mismatches:", [(m["class"], m["key"]) for m in rec.get("mismatches", [])])
    print("  exempted:", [(e["class"], e["key"]) for e in rec.get("exempted", [])])
    print("  corrections:", rec.get("corrections"),
          "bad:", [b["detail"] for b in rec.get("corrections_bad", [])])
    if bat:
        print("  battery:", bat["correction_forgeries"], "green", bat["forgeries_green"])


show("V1-fixed: placeholder '<tip>' kept + concrete window correction",
     base(window=None, corr=(SEATS, WIN)))
show("V3 (reference, green shape)", base(), battery=True)
show("V7: V3 + a '## Round 47' section appended after the corrections",
     base(tail=R47), battery=True)
show("V8: V7 with the seats correction dropped (window only)",
     base(corr=(WIN,), tail=R47))
show("V9: V7 with a vacuous 'rev' correction on an already-resolving sha",
     base(corr=(WIN, "- corrects rev 3186f69b: resolves, already green"), tail=R47))
