#!/usr/bin/env python3
"""Verify the drafted corrections section against the live frozen parser."""
import sys, os, json
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0, os.path.join(LANE, "tools", "round-47"))
sys.path.insert(0, os.path.join(LANE, "tools", "round-46"))
import record  # noqa: E402

REV = sys.argv[1] if len(sys.argv) > 1 else "2e4ae43463aabdae707f8c8a4daa41441ad67a71"
DRAFT = os.path.join(LANE, ".ufo/waves/round-47/w1/ScribeCorrections/corrections.md")
files = lambda p: record.gate.show(LANE, REV, p)  # noqa: E731
card = files("SCORECARD.md")
draft = open(DRAFT, encoding="utf-8").read().rstrip("\n") + "\n"

HEAD = "## Record corrections — round 47"
assert HEAD in card
live = card.split(HEAD, 1)[1]
live = live.split("\n## ", 1)[0]          # the landed body, up to the next heading
swapped = card.replace(HEAD + live, draft, 1)
print("card bytes:", len(card), "-> swapped:", len(swapped), "changed:", swapped != card)

# what the parser actually reads out of the draft
corr, body = record.corrections(swapped)
print("\nparsed correction entries:")
for c in corr:
    print("  class=%s key=%s" % (c["class"], c["key"]))
    print("    statement:", c["statement"][:120])
print("  count:", len(corr))

cache = {}
def spawns(rnd):
    return record.dispatch_counts(files, str(rnd))
print("\nper-line re-derivation:")
for c in corr:
    ok, detail = record.corrects(c, files, LANE, REV, spawns)
    print("  %s/%s -> %s %s" % (c["class"], c["key"], ok, json.dumps(detail)))

code, rec = record.evaluate_text(swapped, files, LANE, REV, battery=None)
bat = record.run_battery(swapped, files, LANE, REV)
code, rec = record.evaluate_text(swapped, files, LANE, REV, battery=bat)
print("\n=== DRAFTED CARD: exit", code)
print("  sections:", rec["sections"])
print("  atoms:", rec["atoms"], "verified:", rec["verified"],
      "exempted:", [e["class"] + "/" + str(e["key"]) for e in rec["exempted"]])
print("  mismatches:", [(m["class"], m["key"]) for m in rec["mismatches"]])
print("  corrections:", rec["corrections"],
      "bad:", [b["detail"] for b in rec["corrections_bad"]])
print("  battery:", bat["correction_forgeries"], "forgeries_green", bat["forgeries_green"])
for f in bat["fixtures"]:
    print("    ", f.get("name"), "->", f.get("exit"), f.get("failing", f.get("error")))
print("  failing:", rec["failing"])
