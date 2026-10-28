#!/usr/bin/env python3
"""RevC2Before final receipt capture: every decisive probe with command, exit, stdout sha256, UTC."""
import datetime, hashlib, json, os, shutil, subprocess, sys

S = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
COUNTER = os.path.join(LANE, "tools/round-47/record.py")
FROZEN = os.path.join(S, "frozen/tools/round-47/record.py")
BASE = "13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5"
CORR = "## Record corrections — round 47"
HIDE_45 = ("## Round 45 — the freeze rule becomes an instrument with four red arms; "
           "the registry names the six claim-carrying instruments")
PATH_ATOM = ".ufo/waves/round-45/controls/ctl-c1-0-do-nothing.json"
ENV = dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S)


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sh(*a, cwd=None):
    r = subprocess.run(a, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("FAILED %s: %s %s" % (" ".join(a), r.stdout, r.stderr))
    return r


def counter(script, root, rev, battery=True):
    out = os.path.join(root, "receipt.json")
    cmd = ["python3", "-I", "-B", script, "--root", root, "--rev", rev,
           "--json-out", out] + ([] if battery else ["--no-battery"])
    t = utc()
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=S, env=ENV)
    rec = json.load(open(out)) if os.path.exists(out) else {}
    if os.path.exists(out):
        os.unlink(out)
    return {"utc": t, "cmd": " ".join(cmd).replace(S, "$S"), "exit": r.returncode,
            "stdout_sha256": hashlib.sha256(r.stdout.encode()).hexdigest(),
            "sections": rec.get("sections"), "atoms": rec.get("atoms"),
            "atoms_by_class": rec.get("atoms_by_class"),
            "corrections": rec.get("corrections"),
            "corrections_bad": rec.get("corrections_bad"),
            "exempted": [e["class"] + "/" + str(e["key"]) for e in rec.get("exempted") or []],
            "mismatches": [(m["class"], str(m["key"]), m["atom"][:100])
                           for m in rec.get("mismatches") or []],
            "failing": rec.get("failing"),
            "battery": {k: v for k, v in (rec.get("battery") or {}).items()
                        if k != "fixtures"},
            "battery_fixtures": (rec.get("battery") or {}).get("fixtures")}


def fixture(name, mut, source=None):
    d = os.path.join(S, "fx-" + name)
    if os.path.exists(d):
        shutil.rmtree(d)
    sh("git", "clone", "-q", source or os.path.join(S, "fx0"), d)
    sh("git", "-C", d, "config", "user.email", "st@r47")
    sh("git", "-C", d, "config", "user.name", "r47 fixture")
    assert sh("git", "-C", d, "rev-parse", "--show-toplevel").stdout.strip() == d
    p = os.path.join(d, "SCORECARD.md")
    text = mut(open(p, encoding="utf-8").read())
    assert text != open(p, encoding="utf-8").read(), "no-op mutation"
    open(p, "w", encoding="utf-8").write(text)
    sh("git", "-C", d, "add", "-A")
    sh("git", "-C", d, "commit", "-q", "-m", name)
    return d, sh("git", "-C", d, "rev-parse", "HEAD").stdout.strip()


def axes_fix(t):
    t = t.replace("| coverage | 9.72 → 10.0 | 133/133", "| coverage | 9.72 → 10.0 | 138/138")
    return t.replace("| depth | 10 → 10 | 20/20", "| depth | 10 → 10 | 23/23")


LANDED = sh("git", "-C", LANE, "rev-parse", "HEAD").stdout.strip()
FALSE = "\nWaves: 9 + 9 = 99 seats. The round dispatched eighteen seats.\n"
FENCE = "\n```\n## note: everything below this line is background\n```\n"

probes = {}

# P1 — the before-state, at the base, with the counter as landed at LANDED
probes["P1_before_state_at_base"] = counter(COUNTER, LANE, BASE)

# P2/P3 — a false seat atom in the landed round-47 section: detected, then hidden by one fence line
d, tip = fixture("p2_false_seats_visible", lambda t: t + FALSE, LANE)
probes["P2_false_seats_visible"] = dict(counter(COUNTER, d, tip), fixture="$S/fx-p2_false_seats_visible",
                                        tip=tip, mutation="append a false `Waves:` sentence to the "
                                                          "landed round-47 section")
def hide(t):
    i = t.index("## Round 47 —")
    j = t.index("\n", i) + 1
    return t[:j] + FENCE + t[j:] + FALSE
d, tip = fixture("p3_false_seats_fence_hidden", hide, LANE)
probes["P3_false_seats_fence_hidden"] = dict(counter(COUNTER, d, tip), fixture="$S/fx-p3_false_seats_fence_hidden",
                                             tip=tip, mutation="the same sentence, with a fenced "
                                                               "`## note:` line after the round-47 heading")

# P4/P5 — the frozen bytes at 5017e1f: A1's "unreachable" premise, and the clause A1 deleted
def f4(t):
    t = axes_fix(t)
    t = t.replace("0425224..<tip> -- tools/round-46 plans/round-46-claims.md",
                  "0425224..0425224 -- tools/round-46")
    return t + ("\n" + CORR + "\n\n- corrects seats round-45: 2 waves, 76 seats total\n"
                f"- corrects path {PATH_ATOM}: landed\n"
                "- corrects window round-46: empty in 0425224..0425224 -- tools/round-46\n")
d, tip = fixture("p4_frozen_reachable", f4)
probes["P4_frozen_bytes_reachable"] = dict(
    frozen=counter(FROZEN, d, tip), current=counter(COUNTER, d, tip),
    fixture="$S/fx-p4_frozen_reachable", tip=tip,
    mutation="the round-46 window sentence restated as a concrete pair, two corrections")

def f2(t):
    return axes_fix(t) + ("\n" + CORR + "\n\n- corrects seats round-45: 2 waves, 76 seats total\n"
                          f"- corrects path {PATH_ATOM}: landed\n"
                          "- corrects window round-46: empty in 22fd0d6..22fd0d6 -- "
                          "corpus/lessons/round-46-verifier-spotcheck.md\n")
d, tip = fixture("p5_unrelated_window", f2)
probes["P5_unrelated_window_exemption"] = dict(
    frozen=counter(FROZEN, d, tip), current=counter(COUNTER, d, tip),
    fixture="$S/fx-p5_unrelated_window", tip=tip,
    mutation="the placeholder window atom exempted by a true window over an unrelated path")

# P6 — an false `- corrects axes` line on the landed card
def p6(t):
    return t.replace("- corrects axes depth: 24/24", "- corrects axes depth: 99/99")
d, tip = fixture("p6_axes_correction", p6, LANE)
probes["P6_axes_correction_unparsed"] = dict(counter(COUNTER, d, tip),
                                             fixture="$S/fx-p6_axes_correction", tip=tip,
                                             mutation="the landed `- corrects axes depth: 24/24` "
                                                      "changed to 99/99")

# P7 — a section with zero atoms
def p7(t):
    return axes_fix(t) + ("\n" + CORR + "\n\n- corrects seats round-46: 2 waves, 80 seats total\n"
                          "- corrects window round-46: empty in 22fd0d6..22fd0d6 -- "
                          "corpus/lessons/round-46-verifier-spotcheck.md\n"
                          "\n## Round 47 — nothing measured this round\n\nNo counter was run.\n")
d, tip = fixture("p7_empty_newest_section", p7)
probes["P7_empty_newest_section"] = dict(counter(COUNTER, d, tip),
                                         fixture="$S/fx-p7_empty_newest_section", tip=tip,
                                         mutation="the newest section carries no atom")

out = {"seat": "RevC2Before", "lane": LANE, "base": BASE, "freeze": "5017e1f7299c3a812e87e7950148f54313dd279e",
       "measured_at_lane_head": LANDED,
       "frozen_counter_sha256": hashlib.sha256(open(FROZEN, "rb").read()).hexdigest(),
       "landed_counter_sha256": hashlib.sha256(open(COUNTER, "rb").read()).hexdigest(),
       "landed_counter_blob_at_head": sh("git", "-C", LANE, "rev-parse", f"{LANDED}:tools/round-47/record.py").stdout.strip(),
       "probes": probes}
json.dump(out, open(os.path.join(S, "revc2-probes.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
