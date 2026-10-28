#!/usr/bin/env python3
"""Targeted detectors for each surviving registry.py mutant.

The frozen `--selftest` is the detector of record; where it reports `failures=0` for
a mutant, this harness asks the separate question the seat needs answered: is the
mutated defect *observable* on an input the selftest does not contain?  Each probe
scores one hand-built artefact with `registry.score()` (the same function the
counter calls), once on the pristine bytes and once on the mutant, in-process.
"""
import hashlib
import importlib.util
import json
import os
import sys

S = "/fast/scratch/hyaku/kaidoku-r46/R46W1MutC2Checks"
REP = ("/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/"
       "round-46/w1/R46W1MutC2Checks")
CENSUS = "tools/round-46/census.json"


def load(dirpath, tag):
    sys.modules.pop("gate", None)
    sys.path.insert(0, dirpath)
    try:
        spec = importlib.util.spec_from_file_location(
            "reg_" + tag, os.path.join(dirpath, "registry.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    finally:
        sys.path.remove(dirpath)
    return mod


P = load(os.path.join(S, "pristine"), "pristine")
HEAD, TAIL, HOUSE = P.HEAD, P.TAIL, P.HOUSE
HDR = "| " + " | ".join(HOUSE) + " |"
SEP = "|" + "---|" * len(HOUSE)
GOOD_EXITS = "0=met; 1=not met; 2=could-not-evaluate"
THIN_EXITS = "non-zero on failure"
TWO = ["tools/round-46/a.py", "tools/round-46/b.py"]


def row(path, exits=GOOD_EXITS):
    return f"| `{path}` | gate | {exits} | `--selftest` | none | repo | kaidoku |"


def table(paths=TWO, exits=GOOD_EXITS):
    return HDR + "\n" + SEP + "\n" + "\n".join(row(p, exits) for p in paths) + "\n"


def files_for(scope, present=None):
    present = scope if present is None else present

    def files(p):
        if p == CENSUS:
            return json.dumps({"paths": scope})
        if p == "SKILL.md":
            return None
        return "#!/usr/bin/env python3\n" if p in present else None
    return files


PROBES = [
    ("P1-fence-with-house-header", "m2-fence-blind-parse", ["head", "frozen"],
     "\n### R\n\n" + HEAD + "\n\n```\n" + table() + "```\n" + TAIL + "\n",
     TWO, None, "v2", None),
    ("P2-table-entirely-outside-section", "m6-rows-outside-section", ["head", "frozen"],
     "\n### R\n\n" + table() + "\n" + HEAD + "\n\n" + TAIL + "\n",
     TWO, None, "v2", None),
    ("P3-two-open-markers", "m10-duplicate-markers-allowed", ["head", "frozen"],
     "\n### R\n\n" + HEAD + "\n\n" + HEAD + "\n\n" + table() + "\n" + TAIL + "\n",
     TWO, None, "v2", None),
    ("P4-census-names-nothing", "m11-empty-scope-accepted", ["head", "frozen"],
     "\n### R\n\n" + HEAD + "\n\n" + table([]) + "\n" + TAIL + "\n",
     [], None, "v2", None),
    ("P5-duplicate-row-good-last", "m8-last-row-wins", ["head", "frozen"],
     "\n### R\n\n" + HEAD + "\n\n" + HDR + "\n" + SEP + "\n"
     + row(TWO[0], THIN_EXITS) + "\n" + row(TWO[0]) + "\n" + row(TWO[1]) + "\n"
     + "\n" + TAIL + "\n", TWO, None, "v2", None),
    ("P6-duplicate-row-thin-last", "m8-last-row-wins", ["head", "frozen"],
     "\n### R\n\n" + HEAD + "\n\n" + HDR + "\n" + SEP + "\n"
     + row(TWO[0]) + "\n" + row(TWO[0], THIN_EXITS) + "\n" + row(TWO[1]) + "\n"
     + "\n" + TAIL + "\n", TWO, None, "v2", None),
    ("P7-battery-accepted-all-forgeries", "m9b-battery-check-neutered", ["head", "frozen"],
     "\n### R\n\n" + HEAD + "\n\n" + table() + "\n" + TAIL + "\n", TWO, None, "v2",
     {"forgeries_total": 7, "v1_green": 7, "v2_green": 7, "genuine_green": 1}),
    ("P8-close-marker-before-open", "m7-close-before-open-allowed", ["head", "frozen"],
     "\n" + TAIL + "\n\n" + table() + "\n" + HEAD + "\n", TWO, None, "v2", None),
    ("P9-v1-substring-cell", None, ["head", "frozen"],
     "\n### R\n\n" + HEAD + "\n\n" + HDR + "\n" + SEP + "\n"
     + f"| see `{TWO[0]}` (wrapper) | gate | {GOOD_EXITS} | `--selftest` | none "
       "| repo | kaidoku |\n" + row(TWO[1]) + "\n" + TAIL + "\n", TWO, None, "v1", None),
    ("P10-v1-registered-path-absent", None, ["head", "frozen"],
     "\n### R\n\n" + HEAD + "\n\n" + table() + "\n" + TAIL + "\n",
     TWO, TWO[:1], "v1", None),
    ("P11-v1-fenced-single-letter", None, ["head", "frozen"],
     "\n### R\n\n" + HEAD + "\n\n" + HDR + "\n" + SEP + "\n"
     + f"| `{TWO[0]}` | gate | 0 1 2 | x | y | z | kaidoku |\n"
     + f"| `{TWO[1]}` | gate | 0 1 2 | x | y | z | kaidoku |\n" + TAIL + "\n",
     TWO, None, "v1", None),
]

bases = {"head": os.path.join(S, "pristine"),
         "frozen": os.path.join(S, "frozen")}
mods = {}


def module_for(base, mutant):
    key = (base, mutant)
    if key not in mods:
        d = os.path.join(S, "mut-%s-%s" % (base, mutant)) if mutant else bases[base]
        mods[key] = load(d, "%s_%s" % (base, (mutant or "pristine").replace("-", "_")))
    return mods[key]


receipts = []
for pid, mutant, base_list, skill, scope, present, profile, battery in PROBES:
    for base in base_list:
        pr = module_for(base, None)
        mu = module_for(base, mutant) if mutant else None
        out = {"probe": pid, "base": base, "profile": profile,
               "mutant_name": mutant}
        for label, mod in (("pristine", pr), ("mutant", mu)):
            if mod is None:
                continue
            code, rec = mod.score(skill, files_for(scope, present), "r46", profile,
                                  "probe-rev", battery=battery)
            out[label] = {"exit": code, "met_target": rec.get("met_target"),
                          "failing": rec.get("failing"),
                          "reason": rec.get("reason"),
                          "unregistered": rec.get("unregistered"),
                          "thin": rec.get("thin")}
        out["defect_observable"] = (
            (out.get("mutant") or {}).get("exit") != out["pristine"]["exit"])
        receipts.append(out)
        print("%-34s %-7s pristine=%s mutant=%s observable=%s" % (
            pid, base, out["pristine"]["exit"],
            (out.get("mutant") or {}).get("exit"), out["defect_observable"]))
        if out.get("mutant") is None:
            print("   (single-base probe)")

# m4 does not apply to the freeze bytes with the head anchor: its own anchor there.
d = os.path.join(S, "mut-frozen-m4-drop-absent-at-rev")
if os.path.isdir(d):
    print("frozen m4 dir present")

os.makedirs(REP, exist_ok=True)
with open(os.path.join(REP, "probes.json"), "w") as fh:
    json.dump({"probes": receipts,
               "module_shas": {b: hashlib.sha256(open(
                   os.path.join(p, "registry.py"), "rb").read()).hexdigest()
                   for b, p in bases.items()}}, fh, indent=1)
print("wrote", os.path.join(REP, "probes.json"))
