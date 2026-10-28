#!/usr/bin/env python3
"""Second round: amendment-flow attack (freeze == tip) + receipt forensics."""
import hashlib, json, os, re, shutil, subprocess, sys, time

S = "/fast/scratch/hyaku/kaidoku-r47/RevC1Digest"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
REV = os.environ["REV"]
os.environ["HYAKU_SCRATCH"] = S
os.environ["TMPDIR"] = S


def git(d, *a):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True)


def lane_show(path):
    r = git(LANE, "show", f"{REV}:{path}")
    assert r.returncode == 0, (path, r.stderr)
    return r.stdout


FILES = ["SKILL.md", "plans/round-47-claims.md", "tools/round-47/exact.py",
         "tools/round-46/gate.py", "corpus/lessons/round-46.md",
         "corpus/lessons/round-45.md"]
BASE = {p: lane_show(p) for p in FILES}
EXACT = BASE["tools/round-47/exact.py"]
sha = lambda t: hashlib.sha256(t.encode()).hexdigest()
digest = lambda ns: hashlib.sha256("\n".join(ns).encode()).hexdigest()
NAMES = ["substring-arm", "duplicate-routed-id", "stale-mutations-digest", "flag-order-drift"]

NOOP = EXACT.replace('("duplicate-routed-id", _m_duplicate_id)',
                     '("duplicate-routed-id", lambda block, spec: (block, {}))')
assert NOOP != EXACT


def pins(skill, interp, mutp):
    skill = re.sub(r"interpreter_sha256:[0-9a-f]{64}", f"interpreter_sha256:{interp}", skill)
    return re.sub(r"mutations_sha256:[0-9a-f]{64}", f"mutations_sha256:{mutp}", skill)


def commit(d, files, msg):
    for p, text in files.items():
        full = os.path.join(d, p)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, "w").write(text)
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", msg)
    return git(d, "rev-parse", "HEAD").stdout.strip()


OUT = []


def run(tag, counter, root, freeze, rev, note):
    path = f"{S}/receipts/{tag}.json"
    cmd = [sys.executable, "-I", "-B", counter, "--root", root, "--freeze", freeze, "--rev", rev]
    utc = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=S)
    open(path, "w").write(r.stdout)
    rec = json.loads(r.stdout)
    bat = rec.get("battery", {})
    row = {"tag": tag, "note": note, "utc": utc, "argv": cmd, "exit": r.returncode,
           "receipt": f"receipts/{tag}.json",
           "stdout_sha256": hashlib.sha256(r.stdout.encode()).hexdigest(),
           "failing": rec.get("failing") or rec.get("reason"),
           "battery": bat if len(json.dumps(bat)) < 900 else
           {k: bat.get(k) for k in ("forgeries_total", "v2_green", "v3_green",
                                    "genuine_green", "crash", "skipped", "error")},
           "freeze_field": rec.get("freeze"), "frozen_path_changed": rec.get("frozen_path_changed"),
           "touched": rec.get("touched"), "restored": rec.get("restored"),
           "interp_expected": rec.get("interpreter_sha256_expected"),
           "mut_expected": rec.get("mutations_sha256_expected")}
    OUT.append(row)
    print(json.dumps({k: row[k] for k in ("tag", "exit", "failing", "freeze_field",
                                          "frozen_path_changed", "touched")})[:600])
    return row


# --- lane at freeze == rev == declared freeze (what the L1's re-measure does) ---
run("R7-lane-freeze-eq-rev", f"{LANE}/tools/round-47/exact.py", LANE, REV, REV,
    "freeze re-derives to the tip after the A1/A2/A3/A4 amendments")
run("R7b-lane-a1-freeze", f"{LANE}/tools/round-47/exact.py", LANE,
    "9018c53b16503c8d06d398b75503406508119946", REV, "A1 freeze")

# --- the same flow on a fixture: honest commit -> amendment commit that no-ops a mutation ---
d = subprocess.run(["mktemp", "-d", "-p", S], capture_output=True, text=True).stdout.strip()
git(d, "init", "-q")
git(d, "config", "user.email", "fx@round47")
git(d, "config", "user.name", "r47 fixture")
assert git(d, "rev-parse", "--show-toplevel").stdout.strip() == d
c1 = commit(d, dict(BASE, **{"SKILL.md": pins(BASE["SKILL.md"], sha(EXACT), digest(NAMES))}),
            "c1 honest freeze")
# amendment: neutralise one mutation, refresh only the interpreter pin
c2 = commit(d, {"tools/round-47/exact.py": NOOP,
                "SKILL.md": pins(BASE["SKILL.md"], sha(NOOP), digest(NAMES))},
            "c2 amendment: no-op one mutation")
open(f"{S}/counters/noop.py", "w").write(NOOP)
run("R8-amendment-freeze-old", f"{S}/counters/noop.py", d, c1, c2,
    "freeze pinned at c1: the tool edit is a frozen_path_changed")
run("R8b-amendment-freeze-tip", f"{S}/counters/noop.py", d, c2, c2,
    "amendment declared 'the freeze', exactly as A1/A2 did: green with 3 real forgeries")

# --- receipt forensics on the earlier runs ---
for tag in ("R1-fixture-honest", "R4-body-swap", "R5-noop-body", "R6-executed-unpinned"):
    rec = json.load(open(f"{S}/receipts/{tag}.json"))
    bat = rec.get("battery", {})
    print("\n##", tag, "exit-battery", {k: bat.get(k) for k in
          ("forgeries_total", "v2_green", "v3_green", "genuine_green", "crash")})
    for f in bat.get("fixtures", []):
        print("  ", json.dumps(f)[:400])
    print("   receipt keys:", sorted(rec))
    print("   any field naming the executed counter's sha?:",
          [k for k in rec if "sha" in k.lower()])

json.dump({"rev": REV, "runs": OUT}, open(f"{S}/receipts/index2.json", "w"), indent=1)
print("\nwrote", f"{S}/receipts/index2.json", "fixture", d)
