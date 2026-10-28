#!/usr/bin/env python3
"""C2Corrections fixture driver: build card variants in a scratch clone and score them."""
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
COUNTER = os.path.join(LANE, "tools", "round-47", "record.py")
S = os.environ["HYAKU_SCRATCH"]
D = os.path.join(S, "repo")
BASE = "13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5"
LAND = "e856beb552080c03ede6000b96f1b58bde44c421"
CORR = "## Record corrections — round 47"


def g(*a, check=True):
    r = subprocess.run(["git", "-C", D, *a], capture_output=True, text=True)
    if check and r.returncode != 0:
        raise SystemExit("git %s failed: %s" % (a, r.stderr))
    return r


def show(rev, path):
    r = subprocess.run(["git", "-C", D, "show", "%s:%s" % (rev, path)],
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def fixture(label, base, card, skill=None):
    g("checkout", "-q", "-f", "-B", "fx-" + label, base)
    with open(os.path.join(D, "SCORECARD.md"), "w") as fh:
        fh.write(card)
    if skill is not None:
        with open(os.path.join(D, "SKILL.md"), "w") as fh:
            fh.write(skill)
    g("add", "-A")
    g("commit", "-q", "-m", "fixture " + label)
    return g("rev-parse", "HEAD").stdout.strip()


def score(label, rev, counter=COUNTER):
    out = os.path.join(D, ".ufo", "waves", "round-47", "w1", "fx", label + ".json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    env = dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S)
    r = subprocess.run([sys.executable, "-I", "-B", counter, "--root", D,
                        "--rev", rev, "--json-out", out],
                       capture_output=True, text=True, env=env)
    try:
        with open(out) as fh:
            rec = json.load(fh)
    except (OSError, ValueError):
        rec = {"reason": "no receipt", "stdout": r.stdout[-400:], "stderr": r.stderr[-400:]}
    return {"label": label, "rev": rev, "exit": r.returncode,
            "failing": rec.get("failing", rec.get("reason")),
            "mismatches": rec.get("mismatches"),
            "corrections": rec.get("corrections"),
            "corrections_bad": rec.get("corrections_bad"),
            "exempted": [e["atom"][:70] for e in rec.get("exempted", [])],
            "battery": rec.get("battery"),
            "atoms_by_class": rec.get("atoms_by_class")}


SEATS_LINE = "- corrects seats round-45: 2 waves, 76 seats total"
WIN_LINE = ("- corrects window round-46: empty in 58eb04b6..13a9e9e1 -- "
            "tools/round-46 plans/round-46-claims.md")
AX_C = "- corrects axes coverage: 138/138"
AX_D = "- corrects axes depth: 23/23"


def rows(card, cov="138/138", dep="23/23"):
    """Rewrite the leading fraction of the coverage/depth Owned-axes rows."""
    out = []
    for line in card.splitlines(True):
        if line.startswith("| coverage |"):
            line = line.replace("| 9.72 → 10.0 | ", "| 9.72 → 10.0 | " + cov + " ", 1)
            # drop any earlier leading fraction right after the score cell
            head, _, tail = line.partition(cov + " ")
            rest = tail.lstrip()
            line = head + cov + " " + rest if not rest.startswith("/") else line
        out.append(line)
    text = "".join(out)
    return text


def main():
    assert g("rev-parse", "--show-toplevel").stdout.strip() == D, "fixture root"
    res = []
    base_card = show(BASE, "SCORECARD.md")
    land_card = show(LAND, "SCORECARD.md")
    land_skill = show(LAND, "SKILL.md")

    # P1 landed card as-is
    res.append(score("p1-landed-asis", LAND))

    # P2 C2 reads the craft section: break block 24's citation in the landed SKILL.md
    broken = land_skill.replace("tools/round-47/exact.py", "tools/round-47/nonexistent.py", 1)
    tip = fixture("p2-craft-coupled", LAND, land_card, broken)
    res.append(score("p2-craft-coupled", tip))

    # P3 base + everything repaired in place + two no-op-but-true corrections
    c3 = base_card.replace("wave 2: 32 seats", "wave 2: 36 seats") \
                 .replace("0425224..<tip> -- tools/round-46 plans/round-46-claims.md` is empty",
                          "58eb04b6..13a9e9e1 -- tools/round-46 plans/round-46-claims.md` is empty") \
                 .replace("| coverage | 9.72 → 10.0 | ", "| coverage | 9.72 → 10.0 | 138/138 | ", 1) \
                 .replace("| depth | 10 → 10 | ", "| depth | 10 → 10 | 23/23 | ", 1)
    c3 += "\n" + CORR + "\n\n" + SEATS_LINE + "\n" + \
          "- corrects path .ufo/waves/round-46/w1-dispatch.json: present\n"
    res.append(score("p3-inplace-plus-noop-corrections", fixture("p3", BASE, c3)))

    # P4 base + window sentence deleted outright, zero window corrections
    c4 = base_card.replace(
        "`git log --name-status\n0425224..<tip> -- tools/round-46 plans/round-46-claims.md` is empty at every measurement above.",
        "The frozen round-46 paths are unchanged over the recorded measurements.")
    if c4 == base_card:
        c4 = base_card.replace(
            "0425224..<tip> -- tools/round-46 plans/round-46-claims.md` is empty at every measurement above.",
            "the frozen round-46 paths are unchanged over the recorded measurements.")
    c4 = c4.replace("wave 2: 32 seats", "wave 2: 36 seats") \
           .replace("| coverage | 9.72 → 10.0 | ", "| coverage | 9.72 → 10.0 | 138/138 | ", 1) \
           .replace("| depth | 10 → 10 | ", "| depth | 10 → 10 | 23/23 | ", 1)
    c4 += "\n" + CORR + "\n\n" + SEATS_LINE + "\n" + \
          "- corrects path .ufo/waves/round-46/w1-dispatch.json: present\n"
    res.append(score("p4-window-deleted-no-window-correction", fixture("p4", BASE, c4)))

    # P5 one window correction silences several placeholder window atoms
    c5 = base_card.replace(
        "0425224..<tip> -- tools/round-46 plans/round-46-claims.md` is empty at every measurement above.",
        "0425224..<tip> -- tools/round-46 plans/round-46-claims.md` is empty at every measurement above.\n"
        "`git log --name-status\n9f00..<tip> -- tools/round-46/attest.py` is empty.\n"
        "`git log --name-status\nbeef..<tip> -- corpus/lessons/round-46.md` is empty.")
    c5 = c5.replace("| coverage | 9.72 → 10.0 | ", "| coverage | 9.72 → 10.0 | 138/138 | ", 1) \
           .replace("| depth | 10 → 10 | ", "| depth | 10 → 10 | 23/23 | ", 1)
    c5 += "\n" + CORR + "\n\n" + WIN_LINE + "\n" + SEATS_LINE + "\n"
    res.append(score("p5-one-window-line-three-placeholders", fixture("p5", BASE, c5)))

    # P6 landed card + a false axes correction line (CORR does not accept `axes`)
    c6 = land_card + "\n" + "- corrects axes coverage: 999/999\n"
    res.append(score("p6-false-axes-line-invisible", fixture("p6", LAND, c6)))

    # P7 landed card + a *true-looking but unparseable* property: exempt cap probe
    c7 = land_card.replace("wave 2: 32 seats", "wave 2: 32 seats",
                           ) + ""
    res.append(score("p7-landed-plus-nothing", fixture("p7", LAND, c7)))

    # P8 v1 counter (frozen bytes) on the landed card
    v1 = os.path.join(S, "record-v1.py")
    with open(v1, "w") as fh:
        fh.write(show("5017e1f7299c3a812e87e7950148f54313dd279e", "tools/round-47/record.py"))
    os.chmod(v1, 0o755)
    res.append(score("p8-v1-counter-on-landed-card", LAND, counter=v1))

    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
