#!/usr/bin/env python3
"""Does reversing `-m --diff-merges=first-parent` change git log output at all?

Three merge shapes on a frozen path. Prints raw byte digests and parsed touched sets for
each order, then compares gate.history_touched (original) against a scratch copy whose
call site carries the reversed order.
"""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys

SCRATCH = sys.argv[1]
T46 = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-46"
ORIG = ['-m', '--diff-merges=first-parent']
REVE = ['--diff-merges=first-parent', '-m']

sys.path.insert(0, T46)
import gate  # noqa: E402


def git(d, *a):
    return subprocess.run(["git", "-C", d, *a], capture_output=True,
                          text=True, check=True)


def parse(out):
    tokens = out.decode("utf-8", "surrogateescape").split("\0")
    touched, i = set(), 0
    while i < len(tokens):
        if gate.STATUS.match(tokens[i].strip()) and i + 1 < len(tokens):
            if tokens[i + 1]:
                touched.add(tokens[i + 1])
            i += 2
            continue
        i += 1
    return sorted(touched)


def raw(d, base, tip, paths, order):
    return subprocess.run(
        ["git", "-C", d, "log", *order, "--name-status", "-z", "--format=",
         "%s..%s" % (base, tip), "--", *paths], capture_output=True).stdout


def build(d, resolution):
    git(d, "init", "-q")
    for k, v in (("user.email", "fx@r47"), ("user.name", "r47")):
        git(d, "config", k, v)
    open(os.path.join(d, "f.txt"), "w").write("base\n")   # frozen path
    open(os.path.join(d, "g.txt"), "w").write("g\n")
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", "base")
    base = git(d, "rev-parse", "HEAD").stdout.strip()
    git(d, "checkout", "-q", "-b", "side")
    open(os.path.join(d, "f.txt"), "w").write("side\n")
    open(os.path.join(d, "s.txt"), "w").write("s\n")
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", "side changes f")
    git(d, "checkout", "-q", "master")
    open(os.path.join(d, "g.txt"), "w").write("g2\n")
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", "main changes g")
    r = git(d, "merge", "--no-ff", "--no-commit", "side")
    assert r.returncode == 0 or True
    open(os.path.join(d, "f.txt"), "w").write(resolution + "\n")
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", "merge side")
    tip = git(d, "rev-parse", "HEAD").stdout.strip()
    parents = git(d, "rev-parse", "HEAD^1", "HEAD^2").stdout.split()
    return base, tip, parents


def load_reversed_gate():
    d = os.path.join(SCRATCH, "reversed-gate")
    os.makedirs(d, exist_ok=True)
    src = open(os.path.join(T46, "gate.py")).read()
    out = src.replace('"log", "-m", "--diff-merges=first-parent", "--name-status", "-z",',
                      '"log",\n            "--diff-merges=first-parent",\n            "-m", "--name-status", "-z",', 1)
    assert out != src
    p = os.path.join(d, "gate_rev.py")
    open(p, "w").write(out)
    spec = importlib.util.spec_from_file_location("gate_rev", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m, p, hashlib.sha256(out.encode()).hexdigest()


def main():
    rev_mod, rev_path, rev_sha = load_reversed_gate()
    results = []
    for label, resolution in (("third-state", "merged"), ("side-version", "side"),
                              ("first-parent-version", "base")):
        d = os.path.join(SCRATCH, "fx-" + label)
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
        env = dict(os.environ, GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_SYSTEM="/dev/null")
        os.environ.update({k: v for k, v in env.items() if k.startswith("GIT_CONFIG")})
        base, tip, parents = build(d, resolution)
        top = gate.git(d, "rev-parse", "--show-toplevel").stdout.strip()
        assert top == d, (top, d)
        raw_o = raw(d, base, tip, ["f.txt"], ORIG)
        raw_r = raw(d, base, tip, ["f.txt"], REVE)
        orig_touched, _ = gate.history_touched(d, base, tip, ["f.txt"])
        rev_touched, _ = rev_mod.history_touched(d, base, tip, ["f.txt"])
        full_o = raw(d, base, tip, ["f.txt", "g.txt", "s.txt"], ORIG)
        full_r = raw(d, base, tip, ["f.txt", "g.txt", "s.txt"], REVE)
        results.append({
            "shape": label,
            "merge_resolution_writes": resolution,
            "parents": parents,
            "f_scope_raw_sha_forward": hashlib.sha256(raw_o).hexdigest(),
            "f_scope_raw_sha_reversed": hashlib.sha256(raw_r).hexdigest(),
            "f_scope_raw_identical": raw_o == raw_r,
            "f_scope_touched_forward": parse(raw_o),
            "f_scope_touched_reversed": parse(raw_r),
            "history_touched_original": orig_touched,
            "history_touched_reversed": rev_touched,
            "history_touched_agree": orig_touched == rev_touched,
            "all_paths_raw_identical": full_o == full_r,
            "all_raw_forward_sha": hashlib.sha256(full_o).hexdigest(),
            "all_raw_reversed_sha": hashlib.sha256(full_r).hexdigest(),
            "all_touched_forward": parse(full_o),
            "all_touched_reversed": parse(full_r),
        })
        shutil.rmtree(d, ignore_errors=True)
    print(json.dumps({"reversed_gate_path": rev_path, "reversed_gate_sha256": rev_sha,
                      "git_version": subprocess.run(["git", "--version"],
                                                    capture_output=True, text=True).stdout.strip(),
                      "shapes": results}, indent=1))


if __name__ == "__main__":
    main()
