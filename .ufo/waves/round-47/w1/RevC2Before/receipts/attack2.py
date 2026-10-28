#!/usr/bin/env python3
"""C2 attack harness, second batch: the fence escape, the battery's window trap, the trigger word."""
import json, os, shutil, subprocess, sys, hashlib

S = os.path.dirname(os.path.abspath(__file__))
FX0 = os.path.join(S, "fx0")
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
COUNTER = os.path.join(LANE, "tools/round-47/record.py")
CORR = "## Record corrections — round 47"
TIP = "13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5"


def sh(*a, cwd=None):
    r = subprocess.run(a, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("FAILED %s: %s %s" % (" ".join(a), r.stdout, r.stderr))
    return r


def fresh(name):
    d = os.path.join(S, "fx-" + name)
    if os.path.exists(d):
        subprocess.run(["rm", "-rf", d], check=True)
    sh("git", "clone", "-q", FX0, d)
    sh("git", "-C", d, "config", "user.email", "st@r47")
    sh("git", "-C", d, "config", "user.name", "r47 fixture")
    assert sh("git", "-C", d, "rev-parse", "--show-toplevel").stdout.strip() == d
    return d


def commit(d):
    sh("git", "-C", d, "add", "-A")
    sh("git", "-C", d, "commit", "-q", "-m", "mutate card")
    return sh("git", "-C", d, "rev-parse", "HEAD").stdout.strip()


def card_path(d):
    return os.path.join(d, "SCORECARD.md")


def write(d, text):
    p = card_path(d)
    old = open(p, encoding="utf-8").read()
    assert text != old, "MUTATION WAS A NO-OP"
    open(p, "w", encoding="utf-8").write(text)
    return commit(d)


def run(d, rev, battery=True):
    out = os.path.join(d, "receipt.json")
    cmd = ["python3", "-I", "-B", COUNTER, "--root", d, "--rev", rev,
           "--json-out", out] + ([] if battery else ["--no-battery"])
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=S,
                       env=dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S))
    rec = json.load(open(out)) if os.path.exists(out) else {}
    if os.path.exists(out):
        os.unlink(out)
    return {"exit": r.returncode, "cmd": " ".join(cmd),
            "stdout_sha256": hashlib.sha256(r.stdout.encode()).hexdigest(),
            "sections": rec.get("sections"), "atoms": rec.get("atoms"),
            "atoms_by_class": rec.get("atoms_by_class"),
            "corrections": rec.get("corrections"),
            "corrections_bad": rec.get("corrections_bad"),
            "exempted": [e["class"] + "/" + str(e["key"]) for e in rec.get("exempted") or []],
            "mismatches": [(m["class"], str(m["key"]), m["atom"][:80])
                           for m in rec.get("mismatches") or []],
            "failing": rec.get("failing"),
            "battery": {k: v for k, v in (rec.get("battery") or {}).items() if k != "fixtures"},
            "battery_fixtures": (rec.get("battery") or {}).get("fixtures")}


HIDE_45 = ("## Round 45 — the freeze rule becomes an instrument with four red arms; "
           "the registry names the six claim-carrying instruments")
DECOY = "\n```\n## Round 99 — a sample heading shown to the reader\n```\n"


def axes_fix(t):
    t = t.replace("| coverage | 9.72 → 10.0 | 133/133", "| coverage | 9.72 → 10.0 | 138/138")
    return t.replace("| depth | 10 → 10 | 20/20", "| depth | 10 → 10 | 23/23")


def corr(win):
    return ("\n%s\n\n" % CORR +
            "- corrects seats round-46: 2 waves, 80 seats total\n"
            "- corrects window round-46: %s\n" % win)


C = {}
C["c10_fence_hides_round45_body"] = dict(
    mut=lambda t: axes_fix(t).replace(
        HIDE_45, HIDE_45 + "\n```\n## note: everything below is background\n```\n", 1)
        + corr("empty in 22fd0d6..22fd0d6 -- corpus/lessons/round-46-verifier-spotcheck.md"),
    note="a fenced `## note` line right after the round-45 heading; the false "
         "`wave 2: 32 seats` sentence is still in the card")
C["c10b_fence_hides_round45_no_axesfix"] = dict(
    mut=lambda t: t.replace(
        HIDE_45, HIDE_45 + "\n```\n## note: everything below is background\n```\n", 1),
    note="same fence, axes untouched: shows exactly which atoms survive")
C["c11_battery_window_ends_at_rev"] = dict(
    mut=lambda t: axes_fix(t).replace(
        HIDE_45, HIDE_45 + "\n```\n## note: everything below is background\n```\n", 1)
        + corr("empty in 13a9e9e..13a9e9e -- corpus/lessons/round-46-verifier-spotcheck.md"),
    note="a TRUE tautological window ending at --rev")
C["c12_battery_window_path_after_rev"] = dict(
    mut=lambda t: axes_fix(t).replace(
        HIDE_45, HIDE_45 + "\n```\n## note: everything below is background\n```\n", 1)
        + corr("empty in f762b72..13a9e9e -- tools/round-47/"),
    note="a TRUE non-tautological window: tools/round-47/ did not exist at rev, so the "
         "window is empty, and base..rev is empty too")
C["c13_decoy_section_core_only"] = dict(
    mut=lambda t: axes_fix(t) + DECOY + corr(
        "empty in 22fd0d6..22fd0d6 -- corpus/lessons/round-46-verifier-spotcheck.md"),
    note="a fenced `## Round 99` heading replaces the real round-47 section in the "
         "last-two window; the false round-45 seats sentence is never read")
C["c14_rephrase_trigger_word"] = dict(
    mut=lambda t: t.replace(
        "0425224..<tip> -- tools/round-46 plans/round-46-claims.md` is empty at every "
        "measurement above",
        "0425224..<tip> -- tools/round-46 plans/round-46-claims.md` was empty at every "
        "measurement above")
        + "\n`git log 22fd0d6..22fd0d6 -- SCORECARD.md` is empty.\n",
    note="the false claim rephrased off the literal `is empty` trigger while a second, "
         "true window sentence keeps the class populated")


def main(only):
    rows = []
    for name, spec in C.items():
        if only and name not in only:
            continue
        d = fresh(name)
        tip = write(d, spec["mut"](open(card_path(d), encoding="utf-8").read()))
        raw = open(card_path(d), encoding="utf-8").read()
        rec = {"case": name, "fixture": d, "tip": tip, "note": spec["note"],
               "false_sentence_present": "wave 2: 32 seats" in raw,
               "with_battery": run(d, tip, True), "no_battery": run(d, tip, False)}
        rows.append(rec)
        print(json.dumps(rec, indent=1))
        print("-" * 70)
    json.dump(rows, open(os.path.join(S, "attack2-results.json"), "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1:])
