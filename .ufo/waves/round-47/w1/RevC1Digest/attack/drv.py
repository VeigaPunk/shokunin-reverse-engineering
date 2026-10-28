#!/usr/bin/env python3
"""Drive clause-6 attacks on R47-C1's mutation digest. Writes receipts under $S/receipts."""
import hashlib, json, os, re, shutil, subprocess, sys, time

S = "/fast/scratch/hyaku/kaidoku-r47/RevC1Digest"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
REV = os.environ.get("REV", "1e2c3102952dc636650095643c1963c833859019")
os.makedirs(f"{S}/receipts", exist_ok=True)
os.makedirs(f"{S}/counters", exist_ok=True)
os.makedirs(f"{S}/round-46", exist_ok=True)
os.environ["HYAKU_SCRATCH"] = S
os.environ["TMPDIR"] = S


def git(d, *a, **kw):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True, **kw)


def lane_show(path):
    r = git(LANE, "show", f"{REV}:{path}")
    assert r.returncode == 0, (path, r.stderr)
    return r.stdout


FILES = ["SKILL.md", "plans/round-47-claims.md", "tools/round-47/exact.py",
         "tools/round-46/gate.py", "corpus/lessons/round-46.md",
         "corpus/lessons/round-45.md"]
BASE = {p: lane_show(p) for p in FILES}

EXACT = BASE["tools/round-47/exact.py"]
open(f"{S}/round-46/gate.py", "w").write(BASE["tools/round-46/gate.py"])
open(f"{S}/counters/orig.py", "w").write(EXACT)

NAMES = ["substring-arm", "duplicate-routed-id", "stale-mutations-digest", "flag-order-drift"]
LIST_TEXT = """MUTATIONS = [("substring-arm", _m_substring_arm),
             ("duplicate-routed-id", _m_duplicate_id),
             ("stale-mutations-digest", _m_stale_digest),
             ("flag-order-drift", _m_flag_order)]"""

variants = {}
# (1) reversed order, same bodies
variants["reorder"] = EXACT.replace(LIST_TEXT, """MUTATIONS = [("flag-order-drift", _m_flag_order),
             ("stale-mutations-digest", _m_stale_digest),
             ("duplicate-routed-id", _m_duplicate_id),
             ("substring-arm", _m_substring_arm)]""")
# (2) names unchanged, bodies swapped: digest MUST be identical
variants["bodycam"] = EXACT.replace(LIST_TEXT, """MUTATIONS = [("substring-arm", _m_duplicate_id),
             ("duplicate-routed-id", _m_substring_arm),
             ("stale-mutations-digest", _m_stale_digest),
             ("flag-order-drift", _m_flag_order)]""")
# (3) one body neutralised to a no-op; names + order unchanged
variants["noop"] = EXACT.replace(
    '("duplicate-routed-id", _m_duplicate_id)',
    '("duplicate-routed-id", lambda block, spec: (block, {}))')

for k, v in variants.items():
    assert v != EXACT, k
    assert LIST_TEXT in EXACT
    open(f"{S}/counters/{k}.py", "w").write(v)

digest = lambda ns: hashlib.sha256("\n".join(ns).encode()).hexdigest()
sha = lambda t: hashlib.sha256(t.encode()).hexdigest()
REV_NAMES = list(reversed(NAMES))


def build_fixture(tag, counter_text, interp_pin, mut_pin):
    d = subprocess.run(["mktemp", "-d", "-p", S], capture_output=True, text=True).stdout.strip()
    git(d, "init", "-q")
    for k, v in (("user.email", "fx@round47"), ("user.name", "r47 fixture")):
        git(d, "config", k, v)
    top = git(d, "rev-parse", "--show-toplevel").stdout.strip()
    assert top == d, (top, d)
    files = dict(BASE)
    files["tools/round-47/exact.py"] = counter_text
    skill = BASE["SKILL.md"]
    skill = re.sub(r"interpreter_sha256:[0-9a-f]{64}", f"interpreter_sha256:{interp_pin}", skill)
    skill = re.sub(r"mutations_sha256:[0-9a-f]{64}", f"mutations_sha256:{mut_pin}", skill)
    files["SKILL.md"] = skill
    for p, text in files.items():
        full = os.path.join(d, p)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, "w").write(text)
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", "fixture " + tag)
    rev = git(d, "rev-parse", "HEAD").stdout.strip()
    return d, rev


RECEIPTS = []


def run(tag, counter, root, freeze, rev, note):
    out = f"{S}/receipts/{tag}.json"
    cmd = [sys.executable, "-I", "-B", counter, "--root", root, "--freeze", freeze,
           "--rev", rev]
    t0 = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=S)
    open(out, "w").write(r.stdout)
    rec = json.loads(r.stdout) if r.stdout.strip() else {}
    bat = rec.get("battery", {})
    row = {"tag": tag, "note": note, "utc": t0, "argv": cmd, "exit": r.returncode,
           "stdout_sha256": hashlib.sha256(r.stdout.encode()).hexdigest(),
           "stdout_path": f"receipts/{tag}.json",
           "failure_mode": rec.get("failing") or rec.get("reason"),
           "battery": {k: bat.get(k) for k in
                       ("forgeries_total", "v2_green", "v3_green", "genuine_green",
                        "crash", "skipped", "error")},
           "mut_pin_seen": rec.get("mutations_sha256"),
           "mut_pin_expected": rec.get("mutations_sha256_expected"),
           "interp_seen": rec.get("interpreter_sha256"),
           "interp_expected": rec.get("interpreter_sha256_expected")}
    if isinstance(bat, dict) and bat.get("fixtures"):
        row["fixtures"] = [{k: f.get(k) for k in
                            ("name", "v2_exit", "v3_exit", "v3_failing", "error")}
                           for f in bat["fixtures"]]
    RECEIPTS.append(row)
    print(json.dumps({k: row[k] for k in ("tag", "exit", "failure_mode", "battery")}))
    return row


print("== executed-counter hashes ==")
for k in ("orig", "reorder", "bodycam", "noop"):
    print(k, sha(open(f"{S}/counters/{k}.py").read()))
print("digest orig-order ", digest(NAMES), " reversed-order", digest(REV_NAMES))
print("bodycam digest unchanged:", digest(NAMES) == digest(
    ["substring-arm", "duplicate-routed-id", "stale-mutations-digest", "flag-order-drift"]))

# R0: lane baseline at the declared freeze and at the stale prompt freeze
run("R0-lane-declared-freeze", f"{LANE}/tools/round-47/exact.py", LANE,
    "9018c53b16503c8d06d398b75503406508119946", REV, "baseline at A1 freeze")
run("R0b-lane-prompt-freeze", f"{LANE}/tools/round-47/exact.py", LANE,
    "5017e1f7299c3a812e87e7950148f54313dd279e", REV, "baseline at the prompt's freeze 5017e1f")

# fixture with the honest bytes and the honest pins
D0, R0 = build_fixture("honest", EXACT, sha(EXACT), digest(NAMES))
run("R1-fixture-honest", f"{S}/counters/orig.py", D0, R0, R0, "fixture floor")

# R2: reordered counter, block pin left stale (freeze==rev, so no drift clause can fire)
run("R2-reorder-stale-pin", f"{S}/counters/reorder.py", D0, R0, R0,
    "prompt's experiment: reorder MUTATIONS, keep the block's pin")

# R3: reorder + re-pin both pins (a legitimate re-freeze)
D3, R3 = build_fixture("reorder-repinned", variants["reorder"],
                       sha(variants["reorder"]), digest(REV_NAMES))
run("R3-reorder-repinned", f"{S}/counters/reorder.py", D3, R3, R3,
    "reorder is undetectable once the block is re-pinned")

# R4: names unchanged, bodies swapped, only the interpreter pin refreshed
D4, R4 = build_fixture("bodycam", variants["bodycam"], sha(variants["bodycam"]), digest(NAMES))
run("R4-body-swap", f"{S}/counters/bodycam.py", D4, R4, R4,
    "digest over names cannot see which body a name denotes")

# R5: one mutation neutralised to a no-op, interpreter pin refreshed, digest untouched
D5, R5 = build_fixture("noop", variants["noop"], sha(variants["noop"]), digest(NAMES))
run("R5-noop-body", f"{S}/counters/noop.py", D5, R5, R5,
    "a vanished forgery is scored as v2_green")

# R6: executed counter bytes differ from the pinned interpreter on purpose
run("R6-executed-unpinned", f"{S}/counters/bodycam.py", D0, R0, R0,
    "executed bytes != fixture exact.py; receipt has no field for them")

json.dump({"rev": REV, "receipts": RECEIPTS}, open(f"{S}/receipts/index.json", "w"), indent=1)
print("wrote", f"{S}/receipts/index.json")
