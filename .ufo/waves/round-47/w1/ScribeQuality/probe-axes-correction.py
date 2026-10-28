#!/usr/bin/env python3
"""ScribeQuality probe — is a false `- corrects axes …` line ever evaluated?

`tools/round-47/record.py:50` parses correction lines with
    CORR = re.compile(r"^- corrects (seats|window|path|rev) (\\S+):\\s*(.+)$")
so an `axes` line never becomes an entry: `corrections()` returns only the seats/window/path/rev
lines it recognises. `corrects()` has an `axes` branch (record.py:280) that no caller can reach.

The probe reads the card at --rev, replaces the landing's true axes fraction with a false one,
and re-evaluates. Nothing on the lane is written.
"""
import argparse
import json
import os
import subprocess
import sys

LANE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(LANE, "tools", "round-47"))
import record  # noqa: E402
import gate  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", required=True)
    ap.add_argument("--json-out")
    a = ap.parse_args()
    card = gate.show(LANE, a.rev, "SCORECARD.md")
    files = lambda p: gate.show(LANE, a.rev, p)  # noqa: E731
    body = card.split("## Record corrections — round 47", 1)[1].split("\n## ", 1)[0]
    lines = [l.strip() for l in body.splitlines() if l.strip().startswith("- corrects")]
    parsed, _ = record.corrections(card)
    out = {"rev": a.rev,
           "correction_lines_in_card": len(lines),
           "correction_lines_parsed": len(parsed),
           "parsed": [{"class": c["class"], "key": c["key"]} for c in parsed],
           "unparsed": [l[:80] for l in lines
                        if not any(l.startswith(x["text"]) for x in parsed)]}
    true_frac = "138/138"
    assert ("- corrects axes coverage: " + true_frac) in card, "landing line not found"
    forged = card.replace("- corrects axes coverage: " + true_frac,
                          "- corrects axes coverage: 999/999", 1)
    c0, r0 = record.evaluate_text(card, files, LANE, a.rev, battery=None)
    c1, r1 = record.evaluate_text(forged, files, LANE, a.rev, battery=None)
    out["truth"] = {"exit": c0, "corrections": r0.get("corrections"),
                    "corrections_bad": r0.get("corrections_bad"),
                    "met_target": r0.get("met_target")}
    out["forged_axes_999_of_999"] = {"exit": c1, "corrections": r1.get("corrections"),
                                     "corrections_bad": r1.get("corrections_bad"),
                                     "mismatches": len(r1.get("mismatches", [])),
                                     "met_target": r1.get("met_target"),
                                     "failing": r1.get("failing")}
    print(json.dumps(out, indent=1))
    if a.json_out:
        with open(a.json_out, "w") as fh:
            json.dump(out, fh, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
