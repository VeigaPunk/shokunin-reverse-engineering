"""Read-only quote-binding check against a pinned lane revision.

Calls tools/round-48/record2.score on the committed SCORECARD. One variant
inserts a citation of c2-at-A4.json into the round-47 section. One variant
appends a round-48 section that cites a record2-shaped object supplied only
by the files() wrapper (not written into the lane).
"""
import json
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path[:0] = [f"{LANE}/tools/round-48", f"{LANE}/tools/round-46"]
import gate  # noqa: E402
import record2  # noqa: E402

REV = subprocess.check_output(["git", "-C", LANE, "rev-parse", "HEAD"], text=True).strip()
BLOB = subprocess.check_output(
    ["git", "-C", LANE, "rev-parse", f"{REV}:tools/round-48/record2.py"], text=True
).strip()
WORK = subprocess.check_output(
    ["git", "-C", LANE, "hash-object", "tools/round-48/record2.py"], text=True
).strip()


def show(path):
    return gate.show(LANE, REV, path)


def section(card, n):
    key = f"## Round {n}"
    i = card.find(key)
    j = card.find("\n## ", i + 1)
    return card[i:j if j >= 0 else len(card)]


def brief(code, rec):
    oracle = rec.get("oracle") or {}
    return {
        "exit": code,
        "quotes_checked": rec.get("quotes_checked"),
        "quotes_bad": rec.get("quotes_bad"),
        "oracle_atoms": oracle.get("atoms"),
        "oracle_met": oracle.get("met_target"),
        "oracle_mismatches": len(oracle.get("mismatches") or []),
        "failing": rec.get("failing"),
    }


card = show("SCORECARD.md")
files = lambda p: show(p)  # noqa: E731
print("rev", REV)
print("record2_blob", BLOB)
print("record2_worktree", WORK)
print("round47_quotes", record2.QUOTE.findall(section(card, 47)))
print("round47_receipts", sorted(set(record2.RECEIPT.findall(section(card, 47)))))

code, rec = record2.score(card, files, LANE, REV, "v3", battery=None)
print("BASELINE", json.dumps(brief(code, rec)))

old = ".ufo/waves/round-47/l1/scores/c2-at-A7.json"
extra = ".ufo/waves/round-47/l1/scores/c2-at-A4.json"
i = card.find("## Round 47")
j = card.find("\n## ", i + 1)
sec = card[i:j].replace(old, old + "`, `" + extra, 1)
card_a4 = card[:i] + sec + card[j:]
code, rec = record2.score(card_a4, files, LANE, REV, "v3", battery=None)
print("CITE_A4", json.dumps(brief(code, rec)))
print("cite_a4_receipts", sorted(set(record2.RECEIPT.findall(section(card_a4, 47)))))

synth_path = ".ufo/waves/round-48/l1/scores/c2-at-LANDING.json"
synth = {
    "counter": "round-48-c2",
    "corrections": 2,
    "oracle": {"atoms": 44, "corrections": 2, "exempted": [{}], "mismatches": []},
}


def files_synth(p):
    if p == synth_path:
        return json.dumps(synth)
    return show(p)


addon = (
    "\n\n## Round 48 — probe\n\n"
    "exit 0, `atoms 44`, `exempted 1`, `corrections 2`, `mismatches 0` "
    f"(`{synth_path}`).\n"
)
code, rec = record2.score(card + addon, files_synth, LANE, REV, "v3", battery=None)
print("SYNTH", json.dumps(brief(code, rec)))
for key in ("atoms", "exempted", "corrections", "mismatches"):
    print(f"quote_value {key}", record2.quote_value(synth, key))
print("quote_value oracle.atoms", record2.quote_value(synth["oracle"], "atoms"))

r3 = json.loads(show(".ufo/waves/round-47/l1/scores/c1-at-R3.json"))
for fx in r3["battery"]["fixtures"]:
    v2 = fx.get("v2_failing") or []
    print("R3", fx["name"], "v2_exit", fx["v2_exit"], "v2_fail", (v2[0][:160] if v2 else ""))
