import json, os, importlib.util, io, contextlib, shutil
S = os.environ["HYAKU_SCRATCH"]
LANE = S + "/lane"
base = json.load(open(S + "/attacks/base/honest-at-head.json"))
HEAD = base["head"]
OLD = "e4d1f7de9deae83e6d5f78d2d7f0157196002af0"


def go(path, name, rev):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    orig = m.v3.score

    def fake(args):
        return 0, {"class": "x", "label": base["expect"], "met_target": True, "exit": 0,
                   "counts": base["counts"], "revision": args.rev, "fresh_cells": []}
    m.v3.score = fake
    out = S + "/rev-scenario-%s.json" % name
    shutil.rmtree(S + "/rw-%s" % name, ignore_errors=True)
    bo, be = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(bo), contextlib.redirect_stderr(be):
        code = m.main(["--root", LANE, "--work", S + "/rw-%s" % name, "--rev", rev,
                       "--expect", base["expect"], "--json-out", out])
    m.v3.score = orig
    rec = json.load(open(out))
    return {"exit": code, "head": rec["head"], "revision": rec["revision"],
            "stderr": be.getvalue().strip().splitlines()}


out = {
    "honest-counter --rev OLD": go(LANE + "/tools/round-96/stop-boundary-repair-battery-v6.py", "honest-old", OLD),
    "M11-mutant --rev OLD": go(S + "/kr-attack-work/M11/mut-M11/tools/round-96/stop-boundary-repair-battery-v6.py", "m11-old", OLD),
    "honest-counter --rev HEAD": go(LANE + "/tools/round-96/stop-boundary-repair-battery-v6.py", "honest-head", HEAD),
}
print(json.dumps(out, indent=1, sort_keys=True))
