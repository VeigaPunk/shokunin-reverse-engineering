#!/usr/bin/env python3
"""Third round: block-text forgeries against the digest clause."""
import hashlib, json, os, re, subprocess, sys, time

S = "/fast/scratch/hyaku/kaidoku-r47/RevC1Digest"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
REV = os.environ["REV"]
os.environ["HYAKU_SCRATCH"] = S
os.environ["TMPDIR"] = S
git = lambda d, *a: subprocess.run(["git", "-C", d, *a], capture_output=True, text=True)
show = lambda p: git(LANE, "show", f"{REV}:{p}").stdout
FILES = ["SKILL.md", "plans/round-47-claims.md", "tools/round-47/exact.py",
         "tools/round-46/gate.py", "corpus/lessons/round-46.md", "corpus/lessons/round-45.md"]
BASE = {p: show(p) for p in FILES}
sha = lambda t: hashlib.sha256(t.encode()).hexdigest()
digest = lambda ns: hashlib.sha256("\n".join(ns).encode()).hexdigest()
NAMES = ["substring-arm", "duplicate-routed-id", "stale-mutations-digest", "flag-order-drift"]
GOOD = digest(NAMES)
OUT = []


def fixture(tag, skill):
    d = subprocess.run(["mktemp", "-d", "-p", S], capture_output=True, text=True).stdout.strip()
    git(d, "init", "-q")
    git(d, "config", "user.email", "fx@round47")
    git(d, "config", "user.name", "r47 fixture")
    assert git(d, "rev-parse", "--show-toplevel").stdout.strip() == d
    files = dict(BASE, **{"SKILL.md": skill})
    for p, t in files.items():
        full = os.path.join(d, p)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, "w").write(t)
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", tag)
    return d, git(d, "rev-parse", "HEAD").stdout.strip()


def run(tag, counter, root, freeze, rev, note):
    cmd = [sys.executable, "-I", "-B", counter, "--root", root, "--freeze", freeze, "--rev", rev]
    utc = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=S)
    open(f"{S}/receipts/{tag}.json", "w").write(r.stdout)
    rec = json.loads(r.stdout)
    bat = rec.get("battery", {})
    row = {"tag": tag, "note": note, "utc": utc, "argv": cmd, "exit": r.returncode,
           "stdout_sha256": hashlib.sha256(r.stdout.encode()).hexdigest(),
           "receipt": f"receipts/{tag}.json",
           "failing": rec.get("failing") or rec.get("reason"),
           "battery": {k: bat.get(k) for k in ("forgeries_total", "v2_green", "v3_green",
                                               "genuine_green", "crash")} if bat else None,
           "mut_seen": rec.get("mutations_sha256"),
           "mut_expected": rec.get("mutations_sha256_expected")}
    OUT.append(row)
    print(json.dumps({k: row[k] for k in ("tag", "exit", "failing", "battery")})[:500])
    return row


SK = BASE["SKILL.md"]
block_line = [l for l in SK.splitlines() if "exactness-table v3" in l][0]

# R9: a second, wrong mutations_sha256 appended inside the block, after the correct one
v9 = SK.replace(block_line, block_line + f" A second, stale pin reads mutations_sha256:{'0'*64}.", 1)
assert v9 != SK
d9, r9 = fixture("dup-pin", v9)
run("R9-second-pin-ignored", f"{S}/counters/orig.py", d9, r9, r9,
    "a wrong pin printed after the correct one is never read")

# R10: the four names appear only in a negated clause inside the block
v10 = SK
for n in NAMES:
    v10 = v10.replace(f"`{n}`", f"`not-{n}-honest`")
assert v10 != SK
d10, r10 = fixture("negated-names", v10)
run("R10-superstring-names", f"{S}/counters/orig.py", d10, r10, r10,
    "'names' is a substring test: not-substring-arm-honest satisfies substring-arm")

json.dump({"rev": REV, "runs": OUT}, open(f"{S}/receipts/index3.json", "w"), indent=1)
print("wrote index3.json")
