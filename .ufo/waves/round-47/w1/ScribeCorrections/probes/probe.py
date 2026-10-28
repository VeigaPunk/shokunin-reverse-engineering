#!/usr/bin/env python3
"""Probe the round-47 C2 corrections grammar: which landing shapes the frozen
parser accepts. Read-only on the lane; every variant is an in-memory card."""
import sys, os, json

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0, os.path.join(LANE, "tools", "round-47"))
sys.path.insert(0, os.path.join(LANE, "tools", "round-46"))
import record  # noqa: E402

REV = "3186f69b49798f2cc05727bbfd1604505fcee03b"
files = lambda p: record.gate.show(LANE, REV, p)  # noqa: E731
card0 = files("SCORECARD.md")

COV_OLD = "| coverage | 9.72 → 10.0 | 133/133 knowledge files mapped after the round-41 landing"
COV_NEW = ("| coverage | 9.72 → 10.0 | 138/138 knowledge files mapped at the round-47 landing "
           "(`git ls-tree -r --name-only <rev> corpus/knowledge | grep -c '\\.md$'` → 138; command A "
           "`mapped 138`, `missing []`, `dangling []`); 133/133 knowledge files mapped after the "
           "round-41 landing")
DEP_OLD = "| depth | 10 → 10 | 20/20 queue-drain rule blocks have resolvable file/range citations"
DEP_NEW = ("| depth | 10 → 10 | 23/23 queue-drain rule blocks have resolvable file/range citations "
           "at `3186f69b49798f2cc05727bbfd1604505fcee03b` (command A; the round-47 landing adds "
           "block 24 for 24/24); 20/20 queue-drain rule blocks have resolvable file/range citations")
WIN_OLD = "0425224..<tip>"
WIN_NARROW = "0425224..3ffbe0f8"
WIN_TIP = "332f4884..3186f69b"

CORR_HEAD = "## Record corrections — round 47"
SEATS = ("- corrects seats round-45: 2 waves, 76 seats total (dispatched: wave 1 40, wave 2 36; "
         "`.ufo/waves/round-45/w{1,2}-dispatch.json` `counts.spawn`; the same wave-2 file's "
         "`r45-w2-results.json` also records `seats 36`, so the superseded `wave 2: 32` matches "
         "no committed count)")
WIN = lambda pair: (f"- corrects window round-46: empty in {pair} -- tools/round-46 "
                    "plans/round-46-claims.md")
AXES_LINE = "- corrects axes coverage: 138/138"


def card(axes=True, window=WIN_NARROW, corr=(SEATS,), axes_line=False):
    t = card0
    if axes:
        t = t.replace(COV_OLD, COV_NEW, 1).replace(DEP_OLD, DEP_NEW, 1)
    if window:
        t = t.replace(WIN_OLD, window, 1)
    lines = [c if not callable(c) else c(window) for c in corr]
    if corr:
        t += "\n" + CORR_HEAD + "\n\n" + "\n".join(lines) + "\n"
    if axes_line:
        t = t.replace(CORR_HEAD + "\n\n", CORR_HEAD + "\n\n" + AXES_LINE + "\n", 1)
    return t


def show(name, text, battery=True):
    code, rec = record.evaluate_text(text, files, LANE, REV, battery=None)
    bat = None
    if battery and code in (0, 1):
        bat = record.run_battery(text, files, LANE, REV)
        code, rec = record.evaluate_text(text, files, LANE, REV, battery=bat)
    print(f"\n=== {name}: exit {code}")
    print("  failing:", rec.get("failing"))
    print("  mismatches:", [(m["class"], m["key"]) for m in rec.get("mismatches", [])])
    print("  exempted:", [(e["class"], e["key"]) for e in rec.get("exempted", [])])
    print("  corrections:", rec.get("corrections"),
          "bad:", [b["detail"] for b in rec.get("corrections_bad", [])])
    if bat:
        print("  battery:", bat["correction_forgeries"], "forgeries_green", bat["forgeries_green"])
        for f in bat["fixtures"]:
            print("    ", f.get("name"), "->", f.get("exit"), f.get("failing", f.get("error")))
    return code, rec


show("V0 committed card (control)", card0, battery=False)
show("V1 placeholder kept + concrete window correction (claims-file shape)",
     card(axes=True, window=None, corr=(SEATS, WIN)))
show("V2 in-place window = 332f4884..3186f69b (tip == rev)",
     card(axes=True, window=WIN_TIP, corr=(SEATS, WIN)))
show("V3 in-place window = 0425224..3ffbe0f8 (tip < F5)",
     card(axes=True, window=WIN_NARROW, corr=(SEATS, WIN)))
show("V4 axes rows left stale + '- corrects axes coverage: 138/138' line",
     card(axes=False, window=WIN_NARROW, corr=(SEATS, WIN), axes_line=True))
show("V5 V3 minus the window correction line (corrections=1)",
     card(axes=True, window=WIN_NARROW, corr=(SEATS,)))
show("V6 V3 with depth row at 24/24 while the rev has 23 blocks",
     card(axes=True, window=WIN_NARROW, corr=(SEATS, WIN)).replace(
         "23/23 queue-drain rule blocks", "24/24 queue-drain rule blocks", 1))
