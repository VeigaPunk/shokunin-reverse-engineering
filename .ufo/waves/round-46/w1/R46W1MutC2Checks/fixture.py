#!/usr/bin/env python3
"""End-to-end detectors: `registry.evaluate()` on real one- and two-commit fixtures.

Each forgery is committed into its own fixture repo (the instrument is scored through
its own entry point, gate.freeze_state included), so a mutant that the selftest cannot
see is still shown to change the counter's exit code.
"""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

S = "/fast/scratch/hyaku/kaidoku-r46/R46W1MutC2Checks"
REP = ("/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/"
       "round-46/w1/R46W1MutC2Checks")
CLAIMS = ("# claims\n\n## Frozen paths (exact)\n\n"
          "- `plans/round-46-claims.md`\n- `tools/round-46/`\n")
CENSUS = "tools/round-46/census.json"
TWO = ["tools/round-46/a.py", "tools/round-46/b.py"]


def load(dirpath, tag):
    sys.modules.pop("gate", None)
    sys.path.insert(0, dirpath)
    try:
        spec = importlib.util.spec_from_file_location(
            "reg_e2e_" + tag, os.path.join(dirpath, "registry.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    finally:
        sys.path.remove(dirpath)
    return mod


P = load(os.path.join(S, "pristine"), "pristine")
HEAD, TAIL, HOUSE = P.HEAD, P.TAIL, P.HOUSE
HDR = "| " + " | ".join(HOUSE) + " |"
SEP = "|" + "---|" * len(HOUSE)


def row(path, exits="0=met; 1=not met; 2=could-not-evaluate"):
    return f"| `{path}` | gate | {exits} | `--selftest` | none | repo | kaidoku |"


def good_table():
    return HDR + "\n" + SEP + "\n" + "\n".join(row(p) for p in TWO)


def g(d, *args):
    return subprocess.run(["git", "-C", d, *args], capture_output=True, text=True,
                          check=True)


def mkfixture(skill, scope=TWO, extra=()):
    d = tempfile.mkdtemp(dir=S, prefix="fx-")
    g(d, "init", "-q")
    toplevel = g(d, "rev-parse", "--show-toplevel").stdout.strip()
    if os.path.realpath(toplevel) != os.path.realpath(d):
        raise SystemExit("fixture toplevel mismatch: %r != %r" % (toplevel, d))
    g(d, "config", "user.email", "fx@round46")
    g(d, "config", "user.name", "round46 fixture")
    base = {"SKILL.md": skill, CLAIMS: CLAIMS if False else CLAIMS,
            "plans/round-46-claims.md": CLAIMS,
            CENSUS: json.dumps({"paths": scope})}
    for p in scope:
        base[p] = "#!/usr/bin/env python3\n"
    for p, body in base.items():
        full = os.path.join(d, p)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as fh:
            fh.write(body)
    g(d, "add", "-A")
    g(d, "commit", "-q", "-m", "freeze")
    revs = [g(d, "rev-parse", "HEAD").stdout.strip()]
    for n, changes in enumerate(extra, 1):
        for p, body in changes.items():
            full = os.path.join(d, p)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, "w") as fh:
                fh.write(body)
        g(d, "add", "-A")
        g(d, "commit", "-q", "-m", "step%d" % n)
        revs.append(g(d, "rev-parse", "HEAD").stdout.strip())
    return d, revs


CASES = [
    ("F1-fenced-table-with-house-header", "head", "m2-fence-blind-parse",
     "\n### R\n\n" + HEAD + "\n\n```\n" + good_table() + "\n```\n" + TAIL + "\n", ()),
    ("F2-table-outside-section", "head", "m6-rows-outside-section",
     "\n### R\n\n" + good_table() + "\n\n" + HEAD + "\n\n" + TAIL + "\n", ()),
    ("F3-frozen-dir-touched", "head", "m12-frozen-arm-ignored",
     "\n### R\n\n" + HEAD + "\n\n" + good_table() + "\n" + TAIL + "\n",
     ({"tools/round-46/a.py": "#!/usr/bin/env python3\n# tampered\n"},)),
    ("F4-frozen-dir-touched-then-restored", "head", None,
     "\n### R\n\n" + HEAD + "\n\n" + good_table() + "\n" + TAIL + "\n",
     ({"tools/round-46/a.py": "#!/usr/bin/env python3\n# tampered\n"},
      {"tools/round-46/a.py": "#!/usr/bin/env python3\n"})),
]

receipts = []
for name, base, mutant, skill, extra in CASES:
    pr = load(os.path.join(S, "pristine"), "pristine")
    mu = (load(os.path.join(S, "mut-%s-%s" % (base, mutant)), mutant)
          if mutant else None)
    d, revs = mkfixture(skill, extra=extra)
    out = {"case": name, "base": base, "mutant": mutant, "fixture": d,
           "revs": revs, "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    try:
        for label, mod in (("pristine", pr), ("mutant", mu)):
            if mod is None:
                continue
            code, rec = mod.evaluate(d, revs[0], revs[-1], "r46", "v2",
                                     with_battery=False)
            out[label] = {"exit": code, "met_target": rec.get("met_target"),
                          "failing": rec.get("failing"),
                          "reason": rec.get("reason"),
                          "frozen_path_changed": rec.get("frozen_path_changed"),
                          "restored": rec.get("restored"),
                          "touched": rec.get("touched")}
        out["defect_observable"] = ((out.get("mutant") or {}).get("exit")
                                    != out["pristine"]["exit"])
        out["git_status_porcelain"] = g(d, "status", "--porcelain").stdout
    finally:
        shutil.rmtree(d, ignore_errors=True)
    receipts.append(out)
    print("%-40s pristine=%s mutant=%s observable=%s" % (
        name, out["pristine"]["exit"], (out.get("mutant") or {}).get("exit"),
        out["defect_observable"]))
    if out["pristine"]["exit"] == 2:
        print("   pristine:", out["pristine"].get("reason"),
              "restored=", out["pristine"].get("restored"))

os.makedirs(REP, exist_ok=True)
with open(os.path.join(REP, "fixtures.json"), "w") as fh:
    json.dump({"cases": receipts,
               "module_shas": {
                   "pristine": hashlib.sha256(open(
                       os.path.join(S, "pristine", "registry.py"), "rb").read()).hexdigest(),
                   "mutants": {m: hashlib.sha256(open(
                       os.path.join(S, "mut-head-" + m, "registry.py"), "rb").read()
                   ).hexdigest() for _, _, m, _, _ in CASES if m}}}, fh, indent=1)
print("wrote", os.path.join(REP, "fixtures.json"))
