#!/usr/bin/env python3
"""Consolidated C2Corrections probe suite: writes probes.json into the seat dir."""
import hashlib
import json
import os
import subprocess
import sys
import datetime

S = os.environ["HYAKU_SCRATCH"]
D = os.path.join(S, "repo")
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
COUNTER = os.path.join(LANE, "tools/round-47/record.py")
SEAT = os.path.join(LANE, ".ufo/waves/round-47/w1/C2Corrections")
BASE = "13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5"
CORR = "## Record corrections — round 47"
WIN = ("- corrects window round-46: empty in 332f4884..58eb04b6 -- "
       "tools/round-46 plans/round-46-claims.md")


def g(*a, check=True):
    r = subprocess.run(["git", "-C", D, *a], capture_output=True, text=True)
    if check and r.returncode != 0:
        raise SystemExit("git %s: %s" % (a, r.stderr))
    return r


def show(rev, p):
    return subprocess.run(["git", "-C", D, "show", "%s:%s" % (rev, p)],
                          capture_output=True, text=True).stdout


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fx(label, base, card, skill=None):
    g("checkout", "-q", "-f", "-B", "probe-" + label, base)
    open(os.path.join(D, "SCORECARD.md"), "w").write(card)
    if skill is not None:
        open(os.path.join(D, "SKILL.md"), "w").write(skill)
    g("add", "-A")
    g("commit", "-q", "-m", "probe " + label)
    return g("rev-parse", "HEAD").stdout.strip()


def sc(label, rev, note):
    out = os.path.join(D, ".ufo", "waves", "round-47", "w1", "probes", label + ".json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    cmd = [sys.executable, "-I", "-B", COUNTER, "--root", D, "--rev", rev,
           "--json-out", out]
    r = subprocess.run(cmd, capture_output=True, text=True,
                       env=dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S))
    raw = open(out).read() if os.path.exists(out) else ""
    if raw:
        dest = os.path.join(SEAT, "probe-receipts", label + ".json")
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, "w").write(raw)
    rec = json.loads(raw) if raw else {}
    return {"probe": label, "note": note, "rev": rev, "exit": r.returncode,
            "failing": rec.get("failing"), "atoms": rec.get("atoms"),
            "sections": rec.get("sections"), "corrections": rec.get("corrections"),
            "corrections_bad": rec.get("corrections_bad"),
            "mismatches": [{"class": m["class"], "key": m["key"], "derived": m.get("derived")}
                           for m in rec.get("mismatches", [])],
            "exempted": [{"class": e["class"], "key": e["key"]} for e in rec.get("exempted", [])],
            "battery": {k: v for k, v in (rec.get("battery") or {}).items() if k != "fixtures"},
            "receipt_sha256": hashlib.sha256(raw.encode()).hexdigest(), "utc": now()}


def insert(card, line):
    i = card.index(CORR) + len(CORR)
    return card[:i] + "\n" + line + card[i:]


def main():
    assert g("rev-parse", "--show-toplevel").stdout.strip() == D
    g("fetch", "-q", "origin")
    pin = g("rev-parse", "origin/main").stdout.strip()
    base = show(BASE, "SCORECARD.md")
    head = show(pin, "SCORECARD.md")
    head_skill = show(pin, "SKILL.md")
    draft = open(os.path.join(S, "draft-section.md")).read()
    rows = base.replace("| coverage | 9.72 → 10.0 | ",
                        "| coverage | 9.72 → 10.0 | 138/138 | ", 1) \
               .replace("| depth | 10 → 10 | ", "| depth | 10 → 10 | 23/23 | ", 1)
    rows_win = rows.replace(
        "0425224..<tip> -- tools/round-46 plans/round-46-claims.md` is empty",
        "332f4884..58eb04b6 -- tools/round-46 plans/round-46-claims.md` is empty")
    out = []
    out.append(sc("P0-lane-pin-asis", pin, "the lane's card as committed at the pin"))
    broken = head_skill.replace("`tools/round-47/exact.py` `interpreter_sha256",
                                "`tools/round-47/missing.py` `interpreter_sha256", 1)
    out.append(sc("P1-craft-citation-broken",
                  fx("p1", pin, head, broken),
                  "block 24's interpreter citation renamed: C2 must go red on the depth head"))
    out.append(sc("P2-draft-plus-rows", fx("p2", BASE, rows_win + "\n" + draft),
                  "my draft section on the base card with both axis heads repaired in place"))
    out.append(sc("P3-draft-no-row-repair", fx("p3", BASE, base + "\n" + draft),
                  "my draft section alone: the two exemption lines fire, the axes heads cannot be exempted"))
    out.append(sc("P4-rows-and-corrections-exempt-nothing",
                  fx("p4", BASE, rows_win.replace("wave 2: 32 seats", "wave 2: 36 seats")
                     + "\n" + CORR + "\n\n- corrects seats round-45: 2 waves, 76 seats total\n"
                     + WIN + "\n"),
                  "every atom repaired in place: two true corrections, zero exemptions"))
    no_win = rows.replace(
        "`git log --name-status\n0425224..<tip> -- tools/round-46 plans/round-46-claims.md`"
        " is empty at every measurement above.",
        "the frozen round-46 paths are unchanged over the recorded measurements.")
    if no_win == rows:
        no_win = rows.replace(
            "0425224..<tip> -- tools/round-46 plans/round-46-claims.md` is empty at every"
            " measurement above.",
            "the frozen round-46 paths are unchanged over the recorded measurements.")
    out.append(sc("P5-window-sentence-deleted",
                  fx("p5", BASE, no_win.replace("wave 2: 32 seats", "wave 2: 36 seats")
                     + "\n" + CORR + "\n\n- corrects seats round-45: 2 waves, 76 seats total\n"),
                  "repair by deleting the unverifiable sentence: clause 2 (class coverage) must refuse"))
    two = rows.replace(
        "0425224..<tip> -- tools/round-46 plans/round-46-claims.md` is empty at every"
        " measurement above.",
        "0425224..<tip> -- tools/round-46 plans/round-46-claims.md` is empty at every"
        " measurement above.\n`git log 332f4884..<tip> -- tools/round-46/attest.py` is empty.")
    out.append(sc("P6-one-line-two-placeholders",
                  fx("p6", BASE, two + "\n" + CORR + "\n\n"
                     + "- corrects seats round-45: 2 waves, 76 seats total\n" + WIN + "\n"),
                  "one window correction silences two placeholder atoms with different subjects"))
    out.append(sc("P7-false-axes-line", fx("p7", pin, insert(head, "- corrects axes coverage: 999/999")),
                  "a false axes correction: is it parsed at all?"))
    out.append(sc("P8-unrelated-pathspec-window",
                  fx("p8", pin, insert(head, "- corrects window round-46: empty in 332f4884..58eb04b6"
                                       " -- corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-"
                                       "replay-gate-stop.md")),
                  "an empty window over an unrelated path supersedes the round-46 frozen-path claim"))
    out.append(sc("P9-plausible-nonempty-window",
                  fx("p9", pin, insert(head, "- corrects window round-46: empty in 0425224..58eb04b6"
                                       " -- tools/round-46 plans/round-46-claims.md")),
                  "the record's original window, concretised: must stay red"))
    out.append(sc("P10-false-seats-total",
                  fx("p10", pin, insert(head, "- corrects seats round-46: 2 waves, 79 seats total")),
                  "a seats total the dispatch files contradict"))
    out.append(sc("P11-ghost-path",
                  fx("p11", pin, insert(head, "- corrects path does/not/exist.md: never")),
                  "an exemption naming a path that does not exist"))
    out.append(sc("P12-historical-round-44",
                  fx("p12", pin, insert(head, "- corrects seats round-44: 2 waves, 79 seats total")),
                  "a correction for a round the card never mentions"))
    open(os.path.join(SEAT, "probes.json"), "w").write(
        json.dumps({"pin": pin, "counter_sha256": hashlib.sha256(
            open(COUNTER, "rb").read()).hexdigest(), "probes": out}, indent=1))
    for p in out:
        print(p["probe"], "exit", p["exit"], "|", (p["failing"] or "clean"),
              "| corr", p["corrections"], "bad", len(p["corrections_bad"] or []),
              "exempted", len(p["exempted"]))


if __name__ == "__main__":
    main()
