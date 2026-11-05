#!/usr/bin/env python3
"""Isolated probes for the SentinelWrite seat. Operates only under SCR (scratch)."""
import importlib.util
import json
import os
import shutil
import subprocess
import sys

SCR = "/fast/scratch/hyaku/kaidoku-r96/SentinelWrite"
TREE = os.path.join(SCR, "tree")
out = {}


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def reset(d):
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    return d


def write_probe(mod, label):
    """(a) planted <path>.tmp, (b) planted at path, for one write_receipt."""
    base = reset(os.path.join(SCR, "wp-" + label))
    victim = os.path.join(base, "victim.txt")
    with open(victim, "w") as fh:
        fh.write("PLANTED\n")
    res = {}
    # (a) symlink at <path>.tmp
    tgt = os.path.join(base, "a", "receipt.json")
    os.makedirs(os.path.dirname(tgt))
    os.symlink(victim, tgt + ".tmp")
    mod.write_receipt(tgt, {"x": 1, "label": "a"})
    res["a_victim_intact"] = open(victim).read() == "PLANTED\n"
    res["a_target_regular"] = not os.path.islink(tgt)
    res["a_target_json_ok"] = json.load(open(tgt))["x"] == 1
    res["a_tmp_left"] = sorted(n for n in os.listdir(os.path.dirname(tgt))
                               if n.endswith(".tmp"))
    # (b) symlink AT the json-out path
    tgt2 = os.path.join(base, "b", "receipt.json")
    os.makedirs(os.path.dirname(tgt2))
    os.symlink(victim, tgt2)
    mod.write_receipt(tgt2, {"x": 2})
    res["b_victim_intact"] = open(victim).read() == "PLANTED\n"
    res["b_target_regular"] = not os.path.islink(tgt2)
    res["b_target_json_ok"] = json.load(open(tgt2))["x"] == 2
    # mode + flags
    st = os.stat(tgt2)
    res["mode_octal"] = oct(st.st_mode & 0o777)
    # dangling link at target
    tgt3 = os.path.join(base, "c", "receipt.json")
    os.makedirs(os.path.dirname(tgt3))
    os.symlink(os.path.join(base, "nonexistent-dir", "z"), tgt3)
    mod.write_receipt(tgt3, {"x": 3})
    res["c_dangling_replaced"] = (not os.path.islink(tgt3)) and json.load(open(tgt3))["x"] == 3
    # unknown-type failure leaves no temp or target
    tgt4 = os.path.join(base, "d", "receipt.json")
    os.makedirs(os.path.dirname(tgt4))
    try:
        mod.write_receipt(tgt4, {"x": object()})
        res["d_raised"] = False
    except TypeError:
        res["d_raised"] = True
    res["d_residue"] = os.listdir(os.path.dirname(tgt4))
    return res


out["v6_write_receipt"] = write_probe(
    load(os.path.join(TREE, "tools/round-96/stop-boundary-repair-battery-v6.py"), "p_v6"), "v6")
out["probe2_write_receipt"] = write_probe(
    load(os.path.join(TREE, "tools/round-96/symlink-probe-v2.py"), "p_probe2"), "probe2")
out["kill2_write_receipt"] = write_probe(
    load(os.path.join(TREE, "tools/round-96/kill-rule-v2.py"), "p_kill2"), "kill2")

# (g) kill-rule build_copy with a pre-planted mut-<name> symlink
kill = load(os.path.join(TREE, "tools/round-96/kill-rule-v2.py"), "p_kill2b")
mutants = json.load(open(os.path.join(TREE, ".ufo/waves/round-96/mutants.json")))
m1 = [m for m in mutants["mutants"] if m["name"] == "M1"][0]
work = reset(os.path.join(SCR, "kr-work"))
mutdir = os.path.join(work, "mut")
os.makedirs(mutdir)
victim_dir = reset(os.path.join(SCR, "kr-victim"))
# precious pre-existing file at the path the mutant copy would occupy inside the victim
precious_rel = m1["file"]
os.makedirs(os.path.dirname(os.path.join(victim_dir, precious_rel)))
with open(os.path.join(victim_dir, precious_rel), "w") as fh:
    fh.write("PRECIOUS\n")
os.symlink(victim_dir, os.path.join(mutdir, "mut-M1"))
g = {}
try:
    d = kill.build_copy("M1", m1, TREE, mutdir, [])
    g["returned"] = d
except Exception as exc:  # noqa: BLE001
    g["exception"] = "%s: %s" % (type(exc).__name__, exc)
g["mut_M1_still_symlink"] = os.path.islink(os.path.join(mutdir, "mut-M1"))
g["victim_precious_now"] = open(os.path.join(victim_dir, precious_rel)).read()
g["victim_overwritten"] = g["victim_precious_now"] != "PRECIOUS\n"
g["victim_deps_written"] = sorted(os.listdir(os.path.join(victim_dir, "tools")))
out["kill2_build_copy_symlink"] = g

# (g2) pre-planted mut-<name> as a regular file -> rmtree ignored, makedirs fails
work2 = reset(os.path.join(SCR, "kr-work2"))
mutdir2 = os.path.join(work2, "mut")
os.makedirs(mutdir2)
with open(os.path.join(mutdir2, "mut-M1"), "w") as fh:
    fh.write("junk")
g2 = {}
try:
    kill.build_copy("M1", m1, TREE, mutdir2, [])
    g2["exception"] = None
except Exception as exc:  # noqa: BLE001
    g2["exception"] = "%s: %s" % (type(exc).__name__, exc)
out["kill2_build_copy_file_planted"] = g2

# (f) probe stale receipt: a writer that exits 1 without writing leaves verdict hardened
probe = os.path.join(TREE, "tools/round-96/symlink-probe-v2.py")
good = os.path.join(SCR, "fake_writer_good.py")
bad = os.path.join(SCR, "fake_writer_bad.py")
with open(good, "w") as fh:
    fh.write("import argparse,json\n"
             "ap=argparse.ArgumentParser();ap.add_argument('--json-out');"
             "ap.add_argument('--work');ap.add_argument('--root');ap.add_argument('--repair-cmd');"
             "ap.add_argument('--rev');ap.add_argument('--expect');a=ap.parse_args()\n"
             "open(a.json_out,'w').write(json.dumps({'label':a.expect,'met_target':False}))\n")
with open(bad, "w") as fh:
    fh.write("import sys\nsys.stderr.write('boom\\n')\nsys.exit(1)\n")
pw = os.path.join(SCR, "probe-stale")
shutil.rmtree(pw, ignore_errors=True)
os.makedirs(pw)
rec_out1 = os.path.join(pw, "probe-1.json")
rec_out2 = os.path.join(pw, "probe-2.json")


def run_probe(writer, rec_out):
    cmd = [sys.executable, "-I", "-B", probe, "--root", TREE, "--writer", writer,
           "--repair-cmd", ".ufo/waves/round-93/controls/identity_noop.py",
           "--work", os.path.join(pw, "work"), "--rev", "HEAD",
           "--expect", "x", "--json-out", rec_out]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    return p.returncode, json.load(open(rec_out))


rc1, r1 = run_probe(good, rec_out1)
rc2, r2 = run_probe(bad, rec_out2)
out["probe_stale_receipt"] = {
    "run1_rc": rc1, "run1_verdict": r1["verdict"], "run1_writer_rc": r1["writer_rc"],
    "run2_rc": rc2, "run2_verdict": r2["verdict"], "run2_writer_rc": r2["writer_rc"],
    "run2_receipt_valid": r2["receipt_valid"], "run2_victim_intact": r2["victim_intact"],
    "run2_met": r2["met"],
}

print(json.dumps(out, indent=1, sort_keys=True, default=str))
