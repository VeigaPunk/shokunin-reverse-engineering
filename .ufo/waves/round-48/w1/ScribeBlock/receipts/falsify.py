#!/usr/bin/env python3
"""Falsification probes against tools/round-48/meanings.py v3 on the simulated
landing. Each probe weakens the artefact or the counter and checks whether the
clause still scores met."""
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0, LANE + "/tools/round-48")
sys.path.insert(0, LANE + "/tools/round-46")
import meanings  # noqa: E402

sim = open("/fast/scratch/hyaku/kaidoku-r48/ScribeBlock/skill-landed.md").read()

def files(p):
    try:
        return open(LANE + "/" + p).read()
    except OSError:
        return None

def verdict(text, label):
    code, rec = meanings.score(text, files, "v3", "SIM", battery=None)
    print(f"{label}: exit {code} failing={rec['failing'][:2]}")
    return code

# --- Probe P1: minimal-vocabulary verdict map (tautological meanings) --------
# R46-CL7's fix reduces to a vocabulary test: a map that names ONLY the class
# token per segment is contentless yet green.
p1 = sim.replace(
    "0=met, all three bindings true, or a selftest in which every case passes; "
    "1=not met, a binding false, or at least one selftest case fails;",
    "0=met; 1=not met;", 1)
assert p1 != sim
verdict(p1, "P1 bare-token verdict map (0=met;1=not met;2=unevaluable)")

# --- Probe P2: cross-labeled segments — seg1 carries unevaluable text --------
p2 = sim.replace(
    "1=not met, a control reaches n/n so the kill rule fires, or an uncaught "
    "crash; 2=argparse usage error, nothing evaluated",
    "1=not met or could-not-evaluate, a control reaches n/n; "
    "2=unevaluable or a violation, nothing evaluated", 1)
assert p2 != sim
verdict(p2, "P2 cross-labeled seg1/seg2 (polarity checked on seg0 only)")

# --- Probe P3: duplicate citations pad the refs count ------------------------
marked = [b for b in meanings.blocks_of(sim) if meanings.MARKER in b][0]
dup_ref = "`corpus/lessons/round-46.md:1`"
p3 = sim.replace(marked, marked.replace(
    "`plans/round-48-claims.md:24-37`",
    dup_ref + ", " + dup_ref + ", " + dup_ref + ", `plans/round-48-claims.md:24-37`"), 1)
assert p3 != sim
verdict(p3, "P3 refs count padded with duplicate citations")

# --- Probe P4: helper gut -> mutations become no-ops, battery still 4/4/0/1/0
orig = meanings._rewrite_registry
meanings._rewrite_registry = lambda skill_, fn: skill_
try:
    import inspect
    digest = meanings._mut_digest()
    print("P4 digest-with-gutted-helper == pinned digest:", digest == meanings.MUT_DIGEST)
    out = {"forgeries_total": 0, "v2_green": 0, "v3_green": 0,
           "genuine_green": 0, "crash": 0, "noop": 0}
    code, _ = meanings.score(sim, files, "v3", "SIM", battery=None)
    out["genuine_green"] = 1 if code == 0 else 0
    for name, fn in meanings.MUTATIONS:
        text, _ = fn(sim, None)
        if text == sim:
            out["noop"] += 1
            out["forgeries_total"] += 1
            out["v2_green"] += 1
            continue
        fx = lambda p: (text if p == "SKILL.md" else files(p))
        c2, _ = meanings.score(text, fx, "v2", "SIM", battery=None)
        c3, _ = meanings.score(text, fx, "v3", "SIM", battery=None)
        out["forgeries_total"] += 1
        out["v2_green"] += c2 == 0
        out["v3_green"] += c3 == 0
        out["crash"] += c3 == 2
    print("P4 battery with gutted helper:", out)
    want = {"forgeries_total": 4, "v2_green": 4, "v3_green": 0,
            "genuine_green": 1, "crash": 0}
    print("P4 battery still on-target:", all(out[k] == want[k] for k in want),
          "no-op mutations:", out["noop"])
finally:
    meanings._rewrite_registry = orig

# --- Probe P5: routed id hidden outside the trigger cell ---------------------
p5 = sim.replace(
    "the three segments were bound only by their digits' presence",
    "the three segments were bound only by their digits' presence, R47-CL10", 1)
assert p5 != sim
verdict(p5, "P5 second routed id smuggled into a v1-hole cell")

# --- Probe P6: seg2 given NOTMET text (cross-class text, no polarity guard) --
p6 = sim.replace(
    "2=argparse usage error, nothing evaluated",
    "2=unevaluable, an argparse usage error or a violation, nothing evaluated", 1)
assert p6 != sim
verdict(p6, "P6 seg2 carrying both unevaluable and not-met tokens")
