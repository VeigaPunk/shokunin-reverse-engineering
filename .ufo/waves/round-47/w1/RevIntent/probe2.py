#!/usr/bin/env python3
"""RevIntent probe 2 — gate verdicts for the same variants, on a tamper+restore merge
where the history arm is the ONLY witness (blob arm clean at both ends)."""
import hashlib
import importlib.util
import json
import os
import shutil
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


GATE_BODY = open(GATE).read()
CALL = '"log", "-m", "--diff-merges=first-parent", "--name-status", "-z",\n            "--format=", f"{base}..{tip}", "--", *paths, binary=True)'
assert GATE_BODY.count(CALL) == 1

DISABLED = CALL.replace("binary=True)", "binary=True)\n    return [], None  # arm short-circuited")

VARIANTS = {
    "genuine": GATE_BODY,
    "reversed": GATE_BODY.replace(
        '"log", "-m", "--diff-merges=first-parent", "--name-status", "-z",',
        '"log", "--diff-merges=first-parent", "-m", "--name-status", "-z",'),
    "forge_slice": GATE_BODY.replace(
        '"log", "-m", "--diff-merges=first-parent", "--name-status", "-z",',
        '"log", *MERGE_ARGS[::-1], "--name-status", "-z",').replace(
        'STATUS = re.compile(r"^[ACDMRTUXB][0-9]*$")',
        'STATUS = re.compile(r"^[ACDMRTUXB][0-9]*$")\n'
        'MERGE_ARGS = ("-m", "--diff-merges=first-parent")'),
    "arm_disabled": GATE_BODY.replace(CALL, DISABLED),
}
for name, body in VARIANTS.items():
    p = os.path.join(S, "gatev_%s.py" % name)
    open(p, "w").write(body)
    VARIANTS[name] = (p, body)

ORDER = '"-m", "--diff-merges=first-parent"'
REVERSED = '"--diff-merges=first-parent", "-m"'
CLAIMS = "plans/round-46-claims.md"
CLAIMS_BODY = ("# claims\n\nfiller\n" * 20 +
               "\n## Frozen paths (exact)\n\n- `frozen.txt`\n\n"
               "## After\n\ntail\n")


def git(d, *a, **kw):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True, **kw)


def build(d):
    open(os.path.join(d, "frozen.txt"), "w").write("a\n")
    open(os.path.join(d, "other.txt"), "w").write("x\n")
    os.makedirs(os.path.join(d, "plans"))
    open(os.path.join(d, CLAIMS), "w").write(CLAIMS_BODY)
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", "base")
    base = git(d, "rev-parse", "HEAD").stdout.strip()
    git(d, "branch", "-M", "main")
    git(d, "checkout", "-q", "-b", "side")
    open(os.path.join(d, "side.txt"), "w").write("s\n")
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", "side add")
    git(d, "checkout", "-q", "main")
    open(os.path.join(d, "frozen.txt"), "w").write("tampered\n")
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", "tamper frozen")
    subprocess.run(["git", "-C", d, "merge", "--no-ff", "side", "-m", "merge"],
                   capture_output=True)
    open(os.path.join(d, "frozen.txt"), "w").write("a\n")   # restore inside the merge
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", "merge: restore frozen")
    tip = git(d, "rev-parse", "HEAD").stdout.strip()
    return base, tip


d = os.path.join(S, "fx-restore-merge")
shutil.rmtree(d, ignore_errors=True)
subprocess.run(["git", "init", "-q", d], check=True)
assert git(d, "rev-parse", "--show-toplevel").stdout.strip() == d
git(d, "config", "user.email", "fx@r47")
git(d, "config", "user.name", "fx")
base, tip = build(d)

print("fixture %s\nbase=%s\ntip=%s" % (d, base, tip))
print("trees identical at both ends for frozen.txt:",
      git(d, "rev-parse", "%s:frozen.txt" % base).stdout.strip() ==
      git(d, "rev-parse", "%s:frozen.txt" % tip).stdout.strip())
print("parents of tip:", git(d, "rev-list", "--parents", "-1", tip).stdout.split()[1:])
print()

out = {}
for name, (path, body) in VARIANTS.items():
    mod = load("gv_" + name, path)
    code, rec = mod.freeze_state(d, base, tip, claims=CLAIMS)
    out[name] = {"exit": code, "reason": rec.get("reason"),
                 "touched": rec.get("touched"), "restored": rec.get("restored"),
                 "blob_changed": rec.get("blob_changed"),
                 "clause7_literal": body.count(ORDER),
                 "clause7_reversed": body.count(REVERSED)}
    print("%-14s freeze_state exit=%s reason=%-20s touched=%s literal=%d reversed=%d"
          % (name, code, rec.get("reason"), rec.get("touched"),
             body.count(ORDER), body.count(REVERSED)))

# exact.py clause 7 verdict for the same bytes
exact = load("exact47b", EXACT)
gate_mod = sys.modules["gate"]
skill = exact.skill_text(exact.good_block())
base_files = {"SKILL.md": skill, "plans/round-47-claims.md": exact.CLAIMS_BODY,
              "corpus/lessons/round-46.md": "lesson line\n" * 240,
              "tools/round-47/exact.py": open(EXACT).read()}
print("\nexact.py score(profile=v3) on the same four gate.py bytes:")
for name, (path, body) in VARIANTS.items():
    files = dict(base_files, **{"tools/round-46/gate.py": body})
    fx, rev = exact._repo(files, S, prefix="fxv-%s-" % name)
    try:
        code, rec = exact.score(files["SKILL.md"], lambda p: gate_mod.show(fx, rev, p),
                                "v3", rev, battery=None)
    finally:
        shutil.rmtree(fx, ignore_errors=True)
    out[name]["exact_exit"] = code
    out[name]["exact_failing"] = rec.get("failing")
    print("  %-14s exit=%s failing=%s" % (name, code, rec.get("failing")))

json.dump(out, open(os.path.join(S, "probe2.json"), "w"), indent=1, sort_keys=True)

# ---- fuzz: is the reversed arm ever NARROWER than the frozen arm? -----------------
import random
rng = random.Random(47)
stats = {"equal": 0, "reversed_wider": 0, "reversed_narrower": 0, "other": 0}
examples = []
gen = load("gv_genuine_fuzz", VARIANTS["genuine"][0])
rev_mod = load("gv_reversed_fuzz", VARIANTS["reversed"][0])
for i in range(24):
    fd = os.path.join(S, "fz-%02d" % i)
    shutil.rmtree(fd, ignore_errors=True)
    subprocess.run(["git", "init", "-q", fd], check=True)
    assert git(fd, "rev-parse", "--show-toplevel").stdout.strip() == fd
    git(fd, "config", "user.email", "fx@r47")
    git(fd, "config", "user.name", "fx")
    names = ["f%d.txt" % k for k in range(rng.randint(1, 4))]
    for n in names:
        open(os.path.join(fd, n), "w").write("0\n")
    git(fd, "add", "-A")
    git(fd, "commit", "-q", "-m", "base")
    git(fd, "branch", "-M", "main")
    b = git(fd, "rev-parse", "HEAD").stdout.strip()
    git(fd, "checkout", "-q", "-b", "side")
    for n in rng.sample(names, rng.randint(0, len(names))):
        open(os.path.join(fd, n), "w").write("side\n")
    git(fd, "add", "-A")
    git(fd, "commit", "-q", "-m", "side")
    git(fd, "checkout", "-q", "main")
    for n in rng.sample(names, rng.randint(0, len(names))):
        open(os.path.join(fd, n), "w").write("main\n")
    git(fd, "add", "-A")
    git(fd, "commit", "-q", "-m", "main")
    subprocess.run(["git", "-C", fd, "merge", "--no-ff", "side", "-m", "m"],
                   capture_output=True)
    for n in rng.sample(names, rng.randint(0, len(names))):
        open(os.path.join(fd, n), "w").write("resolved\n")
    git(fd, "add", "-A")
    git(fd, "commit", "-q", "-m", "merge resolution")
    t = git(fd, "rev-parse", "HEAD").stdout.strip()
    a = gen.history_touched(fd, b, t, names)[0]
    z = rev_mod.history_touched(fd, b, t, names)[0]
    if set(a) == set(z):
        stats["equal"] += 1
    elif set(a) < set(z):
        stats["reversed_wider"] += 1
        examples.append({"i": i, "frozen_arm": a, "reversed": z})
    elif set(z) < set(a):
        stats["reversed_narrower"] += 1
        examples.append({"i": i, "frozen_arm": a, "reversed": z})
    else:
        stats["other"] += 1
print("\nfuzz over 24 random merge fixtures:", stats)
print("strict examples:", examples[:5])
json.dump({"stats": stats, "examples": examples},
          open(os.path.join(S, "fuzz.json"), "w"), indent=1)
