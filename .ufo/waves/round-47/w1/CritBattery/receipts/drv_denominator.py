#!/usr/bin/env python3
"""CritBattery: a freeze==rev co-forgery of the C1 denominator.

Builds a two-commit lane-shaped fixture in scratch:
  c1 = genuine exact.py (4 mutations) + the landed block 24, pins recomputed
  c2 = exact.py whose mutation list REPLACES `flag-order-drift` with a second
       `substring-arm` (4 entries, so forgeries_total stays 4) + the block re-pinned
Then runs the fixture's own exact.py at --freeze c2 --rev c2 and also c1..c2.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
REV = sys.argv[1] if len(sys.argv) > 1 else "31b092d1"
S = os.environ["HYAKU_SCRATCH"]
sys.path.insert(0, LANE + "/tools/round-47")
sys.path.insert(0, LANE + "/tools/round-46")
import gate  # noqa: E402
import exact  # noqa: E402

tip = gate.resolve(LANE, REV)
skill = gate.show(LANE, tip, "SKILL.md")
block = [b for b in exact.blocks_of(skill) if exact.MARKER in b][0]

GENUINE = gate.show(LANE, tip, "tools/round-47/exact.py")
names4 = [n for n, _ in exact.MUTATIONS]
digest4 = hashlib.sha256("\n".join(names4).encode()).hexdigest()
assert digest4 == exact.MUT_DIGEST

# --- the tampered counter: same four count, one class removed -------------------
TAMPERED = GENUINE.replace('             ("flag-order-drift", _m_flag_order)]',
                           '             ("substring-arm", _m_substring_arm)]')
assert TAMPERED != GENUINE
names_t = ["substring-arm", "duplicate-routed-id", "stale-mutations-digest", "substring-arm"]
digest_t = hashlib.sha256("\n".join(names_t).encode()).hexdigest()
sha_t = hashlib.sha256(TAMPERED.encode()).hexdigest()

# the block states a names list; keep the text, repin both digests
pinned = block.replace(exact.MUT_DIGEST, digest_t, 1)
src_pin = exact.SELF_PIN.search(block).group(1)
pinned = pinned.replace(src_pin, sha_t, 1)
assert pinned != block

# --- fixture files -------------------------------------------------------------
files = {"SKILL.md": skill.replace(block, pinned, 1),
         "tools/round-47/exact.py": TAMPERED}
for name, _, _ in exact.HARD_REF.findall(pinned):
    body = gate.show(LANE, tip, name)
    if body is not None:
        files[name] = body
for p in (exact.CLAIMS, exact.GATE46, exact.MUST_CITE):
    body = gate.show(LANE, tip, p)
    if body is not None:
        files[p] = body


def commit(d, msg, contents):
    for p, text in contents.items():
        full = os.path.join(d, p)
        os.makedirs(os.path.dirname(full) or d, exist_ok=True)
        with open(full, "w") as fh:
            fh.write(text)
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "commit", "-q", "-m", msg], check=True)
    return subprocess.run(["git", "-C", d, "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()


d = tempfile.mkdtemp(dir=S, prefix="denominator-")
subprocess.run(["git", "-C", d, "init", "-q"], check=True)
for k, v in (("user.email", "fx@round47"), ("user.name", "round47 fixture")):
    subprocess.run(["git", "-C", d, "config", k, v], check=True)
top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                     capture_output=True, text=True).stdout.strip()
assert top == d, (top, d)

gen = dict(files)
gen["tools/round-47/exact.py"] = GENUINE
gen["SKILL.md"] = skill          # the genuine block, pins as landed
c1 = commit(d, "genuine counter + landed block", gen)
c2 = commit(d, "denominator substitution: flag-order-drift -> a second substring-arm",
            {"tools/round-47/exact.py": TAMPERED, "SKILL.md": files["SKILL.md"]})

# the fixture's own counter, run against the fixture
counter = os.path.join(d, "tools/round-47/exact.py")
out = {}
for label, args in (("freeze=c1 rev=c2", ["--freeze", c1, "--rev", c2]),
                    ("freeze=c2 rev=c2", ["--freeze", c2, "--rev", c2])):
    r = subprocess.run([sys.executable, "-I", "-B", counter, "--root", d] + args,
                       capture_output=True, text=True)
    rec = {}
    try:
        rec = json.loads(r.stdout)
    except ValueError:
        rec = {"stdout": r.stdout[:200], "stderr": r.stderr[:200]}
    out[label] = {"exit": r.returncode,
                  "reason": rec.get("reason"),
                  "failing": rec.get("failing"),
                  "battery": rec.get("battery") and {
                      k: v for k, v in rec["battery"].items() if k != "fixtures"},
                  "fixtures": [f.get("name") for f in (rec.get("battery") or {}).get("fixtures", [])]}
print(json.dumps({"rev": tip, "c1": c1, "c2": c2, "genuine_digest": digest4,
                  "tampered_digest": digest_t, "tampered_sha": sha_t,
                  "results": out}, indent=1))
shutil.copy(os.path.join(d, "tools/round-47/exact.py"),
            os.path.join(LANE, ".ufo/waves/round-47/w1/CritBattery/receipts",
                         "tampered-exact.py"))
shutil.rmtree(d, ignore_errors=True)
