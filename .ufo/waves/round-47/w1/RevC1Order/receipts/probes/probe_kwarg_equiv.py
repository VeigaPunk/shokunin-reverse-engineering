#!/usr/bin/env python3
"""The kwarg/helper rewrite clause 7 rejects: does it compute the same `touched` set?"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys

SCRATCH = sys.argv[1]
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
T46 = os.path.join(LANE, "tools", "round-46")
sys.path.insert(0, T46)
import gate  # noqa: E402

GATE_BODY = open(os.path.join(T46, "gate.py")).read()
ORIG_CALL = ('    r = git(root, "log", "-m", "--diff-merges=first-parent", "--name-status", "-z",\n'
             '            "--format=", f"{base}..{tip}", "--", *paths, binary=True)\n')
KWARG_CALL = ('    r = git(root, "log", "--name-status", "-z",\n'
              '            "--format=", f"{base}..{tip}", "--", *paths, binary=True,\n'
              '            merges="first-parent")\n')
ORIG_SIG = ('def git(root, *args, binary=False, timeout=120):\n'
            '    return subprocess.run(["git", "-C", root, *args], capture_output=True,\n'
            '                          text=not binary, timeout=timeout)\n')
KWARG_SIG = ('def git(root, *args, binary=False, timeout=120, merges=None):\n'
             '    if merges:\n'
             '        args = (args[0], "-m", "--diff-merges=" + merges) + tuple(args[1:])\n'
             '    return subprocess.run(["git", "-C", root, *args], capture_output=True,\n'
             '                          text=not binary, timeout=timeout)\n')
FLAGS_AFTER_PATHSPEC_CALL = ('    r = git(root, "log", "--name-status", "-z",\n'
                             '            "--format=", f"{base}..{tip}", "--", *paths,\n'
                             '            "-m", "--diff-merges=first-parent", binary=True)\n')
assert ORIG_CALL in GATE_BODY and ORIG_SIG in GATE_BODY


def git(d, *a, check=True):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True, check=check)


def merge_repo(d):
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    git(d, "init", "-q")
    for k, v in (("user.email", "fx@r47"), ("user.name", "r47")):
        git(d, "config", k, v)
    for n in ("f.txt", "y.txt", "z.txt"):
        open(os.path.join(d, n), "w").write("base\n")
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", "base")
    base = git(d, "rev-parse", "HEAD").stdout.strip()
    trunk = git(d, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    git(d, "checkout", "-q", "-b", "side")
    open(os.path.join(d, "y.txt"), "w").write("side\n")
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", "side")
    git(d, "checkout", "-q", trunk)
    open(os.path.join(d, "z.txt"), "w").write("main\n")
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", "main")
    git(d, "merge", "--no-ff", "--no-commit", "side", check=False)
    open(os.path.join(d, "f.txt"), "w").write("resolved-in-merge\n")
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", "merge")
    tip = git(d, "rev-parse", "HEAD").stdout.strip()
    assert gate.git(d, "rev-parse", "--show-toplevel").stdout.strip() == d
    return base, tip


def load(name, text):
    d = os.path.join(SCRATCH, "equiv")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, name + ".py")
    open(p, "w").write(text)
    spec = importlib.util.spec_from_file_location(name, p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m, p


def main():
    repo = os.path.join(SCRATCH, "equiv-merge")
    base, tip = merge_repo(repo)
    out = {"repo": repo, "base": base, "tip": tip, "scopes": {}}
    scopes = {"f.txt": ["f.txt"], "all": ["f.txt", "y.txt", "z.txt"]}
    variants = (("original", GATE_BODY),
                ("kwarg-helper-correct-argv", GATE_BODY.replace(ORIG_SIG, KWARG_SIG)
                 .replace(ORIG_CALL, KWARG_CALL)),
                ("flags-after-pathspec", GATE_BODY.replace(ORIG_CALL, FLAGS_AFTER_PATHSPEC_CALL)))
    for label, text in variants:
        mod, p = load(label.replace("-", "_"), text)
        row = {"module": p}
        for sname, paths in scopes.items():
            touched, err = mod.history_touched(repo, base, tip, paths)
            row[sname] = {"touched": touched, "err": err}
        out["scopes"][label] = row
    base_all = out["scopes"]["original"]["all"]["touched"]
    out["agree"] = {k: out["scopes"][k]["all"]["touched"] == base_all
                    for k in out["scopes"] if k != "original"}
    shutil.rmtree(repo, ignore_errors=True)
    shutil.rmtree(os.path.join(SCRATCH, "equiv"), ignore_errors=True)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
