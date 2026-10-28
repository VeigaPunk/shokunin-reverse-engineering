#!/usr/bin/env python3
"""Decisive clause-7 forgery: the literal lives in a comment, the live arm drops the flags.

For each gate.py variant print (a) exact.py --profile v3's verdict on a genuine block 24,
and (b) what gate.history_touched actually returns on a repo whose only edit to a frozen
path is a merge resolution (parents never touch it).
"""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys

SCRATCH = sys.argv[1]
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
T47 = os.path.join(LANE, "tools", "round-47")
T46 = os.path.join(LANE, "tools", "round-46")
sys.path.insert(0, T47)
sys.path.insert(0, T46)
import gate          # noqa: E402
import exact         # noqa: E402

GATE_BODY = open(os.path.join(T46, "gate.py")).read()
EXACT_BODY = open(os.path.join(T47, "exact.py")).read()
ORIG_CALL = ('    r = git(root, "log", "-m", "--diff-merges=first-parent", "--name-status", "-z",\n'
             '            "--format=", f"{base}..{tip}", "--", *paths, binary=True)\n')
assert ORIG_CALL in GATE_BODY


def git(d, *a, check=True):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True, check=check)


def tamper_repo(d):
    """Only the merge commit touches the frozen path f.txt; neither parent does."""
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    git(d, "init", "-q")
    for k, v in (("user.email", "fx@r47"), ("user.name", "r47")):
        git(d, "config", k, v)
    for name in ("f.txt", "x.txt", "y.txt", "z.txt"):
        open(os.path.join(d, name), "w").write("base\n")
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", "base")
    base = git(d, "rev-parse", "HEAD").stdout.strip()
    trunk = git(d, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    git(d, "checkout", "-q", "-b", "side")
    open(os.path.join(d, "y.txt"), "w").write("side\n")
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", "side touches y only")
    git(d, "checkout", "-q", trunk)
    open(os.path.join(d, "z.txt"), "w").write("main\n")
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", "main touches z only")
    git(d, "merge", "--no-ff", "--no-commit", "side", check=False)
    open(os.path.join(d, "f.txt"), "w").write("resolved-in-merge\n")   # the resolution edit
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", "merge side")
    tip = git(d, "rev-parse", "HEAD").stdout.strip()
    top = gate.git(d, "rev-parse", "--show-toplevel").stdout.strip()
    assert top == d, (top, d)
    return base, tip


VARIANTS = {}


def add(name, call_text, comment=False):
    body = GATE_BODY.replace(ORIG_CALL, call_text, 1)
    if comment:
        body = body.replace('TEMP_PARTITIONS = ("/tmp", "/var/tmp")\n',
                            'TEMP_PARTITIONS = ("/tmp", "/var/tmp")\n' + COMMENT, 1)
        assert COMMENT in body
    VARIANTS[name] = body


COMMENT = ('# The history arm must be evaluated as "-m", "--diff-merges=first-parent"; the order\n'
           '# is load-bearing (round-46 R46-CL6).\n')


def commented(text):
    return text.replace('TEMP_PARTITIONS = ("/tmp", "/var/tmp")\n',
                        'TEMP_PARTITIONS = ("/tmp", "/var/tmp")\n' + COMMENT, 1)


add("original",
    ORIG_CALL)
add("comment-only-literal-flags-dropped",
    '    r = git(root, "log", "--name-status", "-z",\n'
    '            "--format=", f"{base}..{tip}", "--", *paths, binary=True)\n', comment=True)
add("comment-only-literal-reversed-across-lines",
    '    r = git(root, "log",\n'
    '            "--diff-merges=first-parent",\n'
    '            "-m", "--name-status", "-z",\n'
    '            "--format=", f"{base}..{tip}", "--", *paths, binary=True)\n', comment=True)
add("comment-only-literal-flags-dropped-and-black-wrapped",
    '    r = git(root, "log",\n'
    '            "--name-status",\n'
    '            "-z",\n'
    '            "--format=", f"{base}..{tip}", "--", *paths, binary=True)\n', comment=True)
add("comment-forward-live-call-reversed-one-line",
    ORIG_CALL.replace('"-m", "--diff-merges=first-parent"',
                      '"--diff-merges=first-parent", "-m"'), comment=True)
add("flags-after-pathspec-order-kept",
    '    r = git(root, "log", "--name-status", "-z",\n'
    '            "--format=", f"{base}..{tip}", "--", *paths,\n'
    '            "-m", "--diff-merges=first-parent", binary=True)\n')
ORIG_SIG = ('def git(root, *args, binary=False, timeout=120):\n'
            '    return subprocess.run(["git", "-C", root, *args], capture_output=True,\n'
            '                          text=not binary, timeout=timeout)\n')
KWARG_SIG = ('def git(root, *args, binary=False, timeout=120, merges=None):\n'
             '    if merges:\n'
             '        args = (args[0], "-m", "--diff-merges=" + merges) + tuple(args[1:])\n'
             '    return subprocess.run(["git", "-C", root, *args], capture_output=True,\n'
             '                          text=not binary, timeout=timeout)\n')
KWARG_CALL = ('    r = git(root, "log", "--name-status", "-z",\n'
              '            "--format=", f"{base}..{tip}", "--", *paths, binary=True,\n'
              '            merges="first-parent")\n')
assert ORIG_SIG in GATE_BODY
VARIANTS["kwarg-helper-correct-argv"] = (
    GATE_BODY.replace(ORIG_SIG, KWARG_SIG).replace(ORIG_CALL, KWARG_CALL, 1))


def score_variant(name, gate_text):
    files = {
        "SKILL.md": exact.skill_text(exact.good_block()),
        "plans/round-47-claims.md": exact.CLAIMS_BODY,
        "corpus/lessons/round-46.md": "lesson line\n" * 240,
        exact.SELF: EXACT_BODY,
        exact.GATE46: gate_text,
    }
    d, rev = exact._repo(files, SCRATCH, prefix="dec-")
    try:
        top = gate.git(d, "rev-parse", "--show-toplevel").stdout.strip()
        assert top == d
        f = lambda p: gate.show(d, rev, p)  # noqa: E731
        c3, r3 = exact.score(files["SKILL.md"], f, "v3", rev, battery=None)
        c2, _ = exact.score(files["SKILL.md"], f, "v2", rev, battery=None)
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return c3, c2, r3.get("failing"), r3.get("gate_order_literal"), r3.get("gate_order_reversed")


def import_variant(name, gate_text):
    d = os.path.join(SCRATCH, "variants")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, name.replace("-", "_") + ".py")
    open(p, "w").write(gate_text)
    spec = importlib.util.spec_from_file_location("g_" + name.replace("-", "_"), p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m, p


def main():
    repo = os.path.join(SCRATCH, "tamper-merge")
    base, tip = tamper_repo(repo)
    rows = []
    for name, text in VARIANTS.items():
        c3, c2, failing, n_ok, n_bad = score_variant(name, text)
        try:
            mod, p = import_variant(name, text)
            touched, err = mod.history_touched(repo, base, tip, ["f.txt"])
            err = err
        except Exception as exc:  # noqa: BLE001
            touched, err, p = None, "%s: %s" % (type(exc).__name__, exc), None
        raw = subprocess.run(["git", "-C", repo, "log", "--name-status", "-z", "--format=",
                              "%s..%s" % (base, tip)], capture_output=True).stdout
        rows.append({
            "variant": name,
            "gate_sha256": hashlib.sha256(text.encode()).hexdigest(),
            "v3_exit": c3, "v2_exit": c2,
            "v3_failing": failing,
            "receipt_gate_order_literal": n_ok,
            "receipt_gate_order_reversed": n_bad,
            "history_touched_f_txt": touched,
            "tamper_seen": bool(touched),
            "module": p,
        })
        shutil.rmtree(os.path.dirname(p), ignore_errors=True) if False else None
    # independent ground truth: what does git itself say about f.txt in base..tip?
    rows.append({"ground_truth_git_log_name_status": raw.decode("utf-8", "replace")})
    shutil.rmtree(repo, ignore_errors=True)
    print(json.dumps({"repo_base": base, "repo_tip": tip, "rows": rows}, indent=1))


if __name__ == "__main__":
    main()
