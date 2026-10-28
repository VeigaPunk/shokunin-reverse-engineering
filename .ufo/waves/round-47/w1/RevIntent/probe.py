#!/usr/bin/env python3
"""RevIntent probe: does R47-C1 clause 7 protect the arm R46-CL6 describes, or its spelling?

Everything runs against the REAL frozen bytes (read-only) plus scratch fixtures.
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = os.environ["S"]
EXACT = os.path.join(ROOT, "tools/round-47/exact.py")
GATE = os.path.join(ROOT, "tools/round-46/gate.py")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


GATE_BODY = open(GATE).read()
CALL = '"log", "-m", "--diff-merges=first-parent", "--name-status", "-z",'
assert GATE_BODY.count(CALL) == 1, GATE_BODY.count(CALL)

VARIANTS = {
    # arm exactly as frozen
    "genuine": GATE_BODY,
    # arm reordered: later flag wins -> per-parent (separate) diffs
    "reversed": GATE_BODY.replace(
        CALL, '"log", "--diff-merges=first-parent", "-m", "--name-status", "-z",'),
    # `-m` dropped: documented as redundant for this arm by the round-46 seat (F4)
    "fp_only": GATE_BODY.replace(
        CALL, '"log", "--diff-merges=first-parent", "--name-status", "-z",'),
    # the long form of the same value (S142/F6: first-parent and 1 share a <dd>)
    "fp_one": GATE_BODY.replace(
        CALL, '"log", "-m", "--diff-merges=1", "--name-status", "-z",'),
    # FORGERY A: the pinned pair sits in a comment; the executable call passes the
    # mode through a name, in the reversed order. Behavior: separate diffs.
    "forge_comment_var": GATE_BODY.replace(
        CALL, '"log", MERGE_MODE, "-m", "--name-status", "-z",').replace(
        'STATUS = re.compile(r"^[ACDMRTUXB][0-9]*$")',
        'STATUS = re.compile(r"^[ACDMRTUXB][0-9]*$")\n'
        '# pinned order (R46-CL6): "-m", "--diff-merges=first-parent"\n'
        'MERGE_MODE = "--diff-merges=first-parent"'),
    # FORGERY B: the pinned pair is stored once, then applied in reverse at the call.
    "forge_slice": GATE_BODY.replace(
        CALL, '"log", *MERGE_ARGS[::-1], "--name-status", "-z",').replace(
        'STATUS = re.compile(r"^[ACDMRTUXB][0-9]*$")',
        'STATUS = re.compile(r"^[ACDMRTUXB][0-9]*$")\n'
        'MERGE_ARGS = ("-m", "--diff-merges=first-parent")'),
    # BRITTLENESS: an arm-correct file whose docstring quotes the pinned pair
    "doc_quoted": GATE_BODY.replace(
        "  history arm is `git log -m --diff-merges=first-parent --name-status -z`, and a",
        '  history arm is `git log "-m", "--diff-merges=first-parent" --name-status -z`, and a'),
}

for name, body in VARIANTS.items():
    path = os.path.join(S, "gate_%s.py" % name)
    with open(path, "w") as fh:
        fh.write(body)
    VARIANTS[name] = (path, body)

ORDER = '"-m", "--diff-merges=first-parent"'
REVERSED = '"--diff-merges=first-parent", "-m"'
print("== clause-7 literal counts (exact.py's own test) ==")
for name, (path, body) in VARIANTS.items():
    print("%-20s order=%d reversed=%d" % (name, body.count(ORDER), body.count(REVERSED)))

# ---------------------------------------------------------------- clause-7 scoring
exact = load("exact47", EXACT)
gate = sys.modules["gate"]  # imported by exact from tools/round-46

skill = exact.skill_text(exact.good_block())
BASE_FILES = {
    "SKILL.md": skill,
    "plans/round-47-claims.md": exact.CLAIMS_BODY,
    "corpus/lessons/round-46.md": "lesson line\n" * 240,
    "tools/round-47/exact.py": open(EXACT).read(),
}

print("\n== exact.py score(profile=v3) per gate.py variant ==")
scores = {}
for name, (path, body) in VARIANTS.items():
    files = dict(BASE_FILES, **{"tools/round-46/gate.py": body})
    d, rev = exact._repo(files, S, prefix="fx-%s-" % name)
    try:
        code, rec = exact.score(files["SKILL.md"], lambda p: gate.show(d, rev, p),
                                "v3", rev, battery=None)
    finally:
        import shutil
        shutil.rmtree(d, ignore_errors=True)
    scores[name] = {"exit": code,
                    "gate_order_literal": rec.get("gate_order_literal"),
                    "gate_order_reversed": rec.get("gate_order_reversed"),
                    "failing": rec.get("failing")}
    print("%-20s exit=%s literal=%s reversed=%s failing=%s"
          % (name, code, rec.get("gate_order_literal"),
             rec.get("gate_order_reversed"), rec.get("failing")))

# ------------------------------------------------- behavior through history_touched
print("\n== history_touched under each variant ==")


def touched(variant, root, base, tip, paths):
    mod = load("g_" + variant, VARIANTS[variant][0])
    return mod.history_touched(root, base, tip, paths)


def git(d, *a, **kw):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True, **kw)


def fixture(name, build):
    d = os.path.join(S, name)
    subprocess.run(["rm", "-rf", d])
    subprocess.run(["git", "init", "-q", d], check=True)
    top = git(d, "rev-parse", "--show-toplevel").stdout.strip()
    assert top == d, (top, d)
    git(d, "config", "user.email", "fx@r47")
    git(d, "config", "user.name", "fx")
    return d, build(d)


def commit(d, msg):
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", msg)
    return git(d, "rev-parse", "HEAD").stdout.strip()


def build_evil(d):
    open(os.path.join(d, "frozen.txt"), "w").write("a\n")
    open(os.path.join(d, "other.txt"), "w").write("x\n")
    commit(d, "base")
    git(d, "branch", "-M", "main")
    git(d, "checkout", "-q", "-b", "side")
    open(os.path.join(d, "frozen.txt"), "w").write("side\n")
    commit(d, "side")
    git(d, "checkout", "-q", "main")
    open(os.path.join(d, "frozen.txt"), "w").write("main\n")
    commit(d, "main")
    subprocess.run(["git", "-C", d, "merge", "--no-ff", "side", "-m", "merge"],
                   capture_output=True)
    open(os.path.join(d, "frozen.txt"), "w").write("merged\n")
    commit(d, "merge with resolution")
    m = git(d, "rev-parse", "HEAD").stdout.strip()
    base = git(d, "rev-parse", "HEAD^1").stdout.strip()
    return base, m


def build_oldbranch(d):
    """p2 forked before the freeze; main changed frozen.txt BEFORE the freeze."""
    open(os.path.join(d, "frozen.txt"), "w").write("a\n")
    open(os.path.join(d, "other.txt"), "w").write("x\n")
    commit(d, "fork")
    git(d, "branch", "-M", "main")
    git(d, "checkout", "-q", "-b", "side")
    open(os.path.join(d, "side.txt"), "w").write("s\n")
    commit(d, "side add")
    git(d, "checkout", "-q", "main")
    open(os.path.join(d, "frozen.txt"), "w").write("main-pre-freeze\n")
    commit(d, "main edits frozen BEFORE freeze")
    base = git(d, "rev-parse", "HEAD").stdout.strip()   # the freeze
    open(os.path.join(d, "other.txt"), "w").write("y\n")
    commit(d, "post-freeze unfrozen edit")
    subprocess.run(["git", "-C", d, "merge", "--no-ff", "side", "-m", "merge"],
                   capture_output=True)
    m = git(d, "rev-parse", "HEAD").stdout.strip()
    return base, m


cases = {}
for fxname, build in (("fx-evil", build_evil), ("fx-oldbranch", build_oldbranch)):
    d, (base, tip) = fixture(fxname, build)
    cases[fxname] = {"repo": d, "base": base, "tip": tip, "paths": ["frozen.txt", "other.txt"]}
    print("\n-- %s base=%s tip=%s" % (fxname, base[:8], tip[:8]))
    print("   commits in base..tip:",
          git(d, "log", "--format=%s", "%s..%s" % (base, tip)).stdout.split())
    for variant in ("genuine", "reversed", "fp_only", "forge_comment_var", "forge_slice"):
        t, err = touched(variant, d, base, tip, cases[fxname]["paths"])
        print("   %-20s touched=%s err=%s" % (variant, t, err))

# config dependence of `-m`
d = cases["fx-evil"]["repo"]
git(d, "config", "log.diffMerges", "combined")
print("\n-- log.diffMerges=combined on fx-evil")
for variant in ("genuine", "reversed"):
    t, err = touched(variant, d, cases["fx-evil"]["base"], cases["fx-evil"]["tip"],
                     cases["fx-evil"]["paths"])
    print("   %-20s touched=%s err=%s" % (variant, t, err))
git(d, "config", "--unset", "log.diffMerges")

# ------------------------------------------------------------- merge semantics raw
print("\n== raw git-log entries per merge, fx-evil ==")
d, (base, tip) = cases["fx-evil"]["repo"], (cases["fx-evil"]["base"], cases["fx-evil"]["tip"])
for label, args in (("gate order", ["-m", "--diff-merges=first-parent"]),
                    ("reversed", ["--diff-merges=first-parent", "-m"]),
                    ("fp only", ["--diff-merges=first-parent"])):
    r = git(d, "log", *args, "--name-status", "-z", "--format=",
            "%s..%s" % (base, tip), "--", "frozen.txt", "other.txt")
    toks = r.stdout.split("\0")
    print("%-12s exit=%s tokens=%d sha256=%s" %
          (label, r.returncode, len(toks) - 1, sha(r.stdout)))

json.dump({"scores": scores,
           "counts": {n: [b.count(ORDER), b.count(REVERSED)]
                      for n, (p, b) in VARIANTS.items()}},
          open(os.path.join(S, "probe.json"), "w"), indent=1, sort_keys=True)
print("\nwrote", os.path.join(S, "probe.json"))
