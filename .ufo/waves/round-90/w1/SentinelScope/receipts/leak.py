#!/usr/bin/env python3
"""Round-90 sentinel: does the carrier-blind arm bound *provenance*?

Two oracles are exercised against the counter's own machinery
(tools/round-90/upx-later-block-battery.py: child_env, invoke, score_case and
the same bwrap argv), on the jq P1 cell (block 1, sz_cpr stored - 7):

  O1 sibling box   a repair that copies a 14036-byte `out` from a sibling
                   invocation box (N3 leaves the intact packed bytes there)
  O2 /proc root    a repair that reads the run root through a host process's
                   /proc/<pid>/root (the sandbox does not unshare the PID ns)

and the real repair is re-scored in the same sandbox as the control that the
sandbox is not simply broken.
"""
import hashlib, importlib.util, json, os, shutil, struct, subprocess, sys, tempfile

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = "/fast/scratch/hyaku/kaidoku-r90/SentinelScope"
WORK = os.path.join(S, "leakwork")
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
    pkg = os.path.expanduser("~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents")
    if not os.path.isdir(pkg):
        pkg = os.path.expanduser("~/.local/share/rea-agents/6.5.0")
    decoy = os.path.join(boxes, "decoy")
    with open(decoy, "wb") as fh:
        fh.write(b"decoy-not-a-carrier\n" * 64)
    blind_paths = []
    for c in bat.CARRIERS:
        real = os.path.realpath(c["source"])
        if real not in blind_paths:
            blind_paths.append(real)
    blind = {"decoy": decoy, "hide": run_root, "paths": blind_paths}

    d = os.path.join(run_root, "jq")
    os.makedirs(d)
    orig = os.path.join(d, "orig")
    shutil.copy2("/usr/bin/jq", orig)
    packed = os.path.join(d, "packed")
    r = bat.run(["/usr/bin/upx", "--best", "-q", "-o", packed, orig], env)
    assert r["rc"] == 0, r
    pbytes = open(packed, "rb").read()
    orig_sha = sha(orig)
    _b0, blocks = bat.layout(pbytes, rep, r88)
    blk = blocks[1]
    value = blk["sz_cpr"] - 7
    t = bat.tamper(pbytes, blk, value)
    win = {**blk, "sz_cpr": value}
    out = {"pkg": pkg, "box_count_before": None, "rows": {}}

    # the counter's own N3 control runs first and leaves out == packed
    n3 = bat.invoke(REAL, pbytes, env, boxes)
    out["N3"] = {"rc": n3["rc"], "identical": n3.get("output") == pbytes,
                 "box_after": n3["box_after"]}
    out["box_count_after_N3"] = len(os.listdir(boxes))

    for label, cmd in (("real-unblinded", REAL), ("real-blinded", REAL),
                       ("sibling-oracle-unblinded", CHEAT),
                       ("sibling-oracle-blinded", CHEAT)):
        blind_arg = blind if label.endswith("blinded") else None
        row = bat.score_case(cmd, t, pbytes, win, orig_sha, env, boxes, pkg,
                             False, blind_arg)
        out["rows"][label] = {"rc": row["rc"], "arms": row["arms"],
                              "recovered": row["recovered"],
                              "box_after": row["box_after"]}
        print(label, json.dumps({"rc": row["rc"], "recovered": row["recovered"],
                                 "arms": row["arms"]}, sort_keys=True))

    # O2: /proc/<host pid>/root from inside the counter's sandbox argv
    payload = (
        "import os,sys\n"
        "h=sys.argv[1]\n"
        "hits=[]\n"
        "for pid in os.listdir('/proc'):\n"
        "    if not pid.isdigit():\n"
        "        continue\n"
        "    r='/proc/%s/root%s'%(pid,h)\n"
        "    try:\n"
        "        if os.path.isdir(r):\n"
        "            hits.append((pid, sorted(os.listdir(r))[:4]))\n"
        "    except OSError:\n"
        "        pass\n"
        "print('HITS', hits[:6])\n"
        "print('n_hits', len(hits))\n")
    argv = ["bwrap", "--dev-bind", "/", "/", "--tmpfs", run_root]
    for p in blind_paths:
        argv += ["--bind", decoy, p]
    argv += ["--", sys.executable, "-c", payload, run_root]
    pr = subprocess.run(argv, capture_output=True, text=True, env=env, timeout=120)
    out["proc_root"] = {"rc": pr.returncode, "stdout": pr.stdout.strip(),
                        "stderr": pr.stderr.strip()[-300:], "hide": run_root}
    print("proc-root rc", pr.returncode, pr.stdout.strip().replace("\n", " | "))

    json.dump(out, open(os.path.join(S, "leak.json"), "w"), indent=1, sort_keys=True)


main()
