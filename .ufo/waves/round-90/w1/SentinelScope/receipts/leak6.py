#!/usr/bin/env python3
"""Six-cell blinded re-score with the sibling-box oracle.

Replicates the counter's per-carrier sequence (pack -> N3 -> P1 x 2 directions)
for the three P1 carriers, then scores the oracle in the *blinded* sandbox for
all six cells.  Nothing is derived: the oracle copies the 1-byte-different `out`
that the N3 control left in a sibling invocation box.
"""
import hashlib, importlib.util, json, os, shutil, subprocess, sys, tempfile

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = "/fast/scratch/hyaku/kaidoku-r90/SentinelScope"
WORK = os.path.join(S, "leakwork6")
CHEAT = os.path.join(S, "cheat-sibling-oracle.py")
REAL = os.path.join(LANE, "tools/round-90/upx-break-repair.py")


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def sha(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main():
    bat = load(os.path.join(LANE, "tools/round-90/upx-later-block-battery.py"), "bat")
    rep = load(os.path.join(LANE, "tools/round-87/upx-magic-repair.py"), "rep")
    r88 = load(os.path.join(LANE, "tools/round-88/upx-chain-repair.py"), "r88")
    shutil.rmtree(WORK, ignore_errors=True)
    os.makedirs(WORK)
    run_root = tempfile.mkdtemp(prefix="r90-battery-", dir=WORK)
    boxes = tempfile.mkdtemp(prefix="r90-boxes-", dir=WORK)
    env = bat.child_env(run_root)
    os.makedirs(env["HOME"])
    os.makedirs(env["TMPDIR"])
    decoy = os.path.join(boxes, "decoy")
    with open(decoy, "wb") as fh:
        fh.write(b"decoy-not-a-carrier\n" * 64)
    blind_paths = []
    for c in bat.CARRIERS:
        real = os.path.realpath(c["source"])
        if real not in blind_paths:
            blind_paths.append(real)
    blind = {"decoy": decoy, "hide": run_root, "paths": blind_paths}
    out = {"cells": [], "blind_ok": None}

    probe = subprocess.run(
        ["bwrap", "--dev-bind", "/", "/", "--tmpfs", run_root]
        + sum([["--bind", decoy, p] for p in blind_paths], [])
        + ["--", sys.executable, "-c",
           "import hashlib,sys;print(' '.join(hashlib.sha256(open(p,'rb').read())"
           ".hexdigest() for p in sys.argv[1:]))"] + blind_paths,
        capture_output=True, text=True, env=env, timeout=120)
    want = sha(decoy)
    seen = probe.stdout.split()
    out["blind_ok"] = probe.returncode == 0 and seen == [want] * len(blind_paths)
    out["probe"] = {"rc": probe.returncode, "seen": seen, "decoy_sha256": want}

    for c in bat.CARRIERS:
        if not c["p1"]:
            continue
        d = os.path.join(run_root, c["id"])
        os.makedirs(d)
        orig = os.path.join(d, "orig")
        shutil.copy2(c["source"], orig)
        packed = os.path.join(d, "packed")
        r = bat.run(["/usr/bin/upx", "--best", "-q", "-o", packed, orig], env)
        assert r["rc"] == 0, (c["id"], r)
        pbytes = open(packed, "rb").read()
        orig_sha = sha(orig)
        _b0, blocks = bat.layout(pbytes, rep, r88)
        blk = blocks[1]
        n3 = bat.invoke(REAL, pbytes, env, boxes)     # leaves out == pbytes
        assert n3["rc"] == 0 and n3.get("output") == pbytes, (c["id"], n3["rc"])
        for delta in bat.DIRECTIONS:
            value = blk["sz_cpr"] + delta
            if not (0 < value <= blk["sz_unc"]):
                continue
            t = bat.tamper(pbytes, blk, value)
            for label, cmd, bind in (("oracle-blinded", CHEAT, blind),
                                     ("oracle-unblinded", CHEAT, None)):
                row = bat.score_case(cmd, t, pbytes, {**blk, "sz_cpr": value},
                                     orig_sha, env, boxes, None, False, bind)
                out["cells"].append({"carrier": c["id"], "direction": delta,
                                     "mode": label, "rc": row["rc"],
                                     "recovered": row["recovered"],
                                     "box_after": row["box_after"],
                                     "arms": row["arms"]})
                print(c["id"], delta, label, "rc", row["rc"],
                      "recovered", row["recovered"], row["arms"])
    rec = sum(1 for x in out["cells"]
              if x["mode"] == "oracle-blinded" and x["recovered"])
    out["blinded_recovered"] = rec
    out["blinded_cells"] = sum(1 for x in out["cells"] if x["mode"] == "oracle-blinded")
    json.dump(out, open(os.path.join(S, "leak6.json"), "w"), indent=1, sort_keys=True)
    print(json.dumps({"blind_ok": out["blind_ok"],
                      "blinded_recovered": rec,
                      "blinded_cells": out["blinded_cells"]}))


main()
