#!/usr/bin/env python3
"""C1 attack driver: forge block 24 / the battery and score with the frozen counter."""
import hashlib, importlib.util, json, os, re, shutil, subprocess, sys, time

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = "/fast/scratch/hyaku/kaidoku-r47/CritC1Sizing"
EXACT = os.path.join(LANE, "tools/round-47/exact.py")

spec = importlib.util.spec_from_file_location("exact_lane", EXACT)
ex = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ex)

SKILL = open(os.path.join(LANE, "SKILL.md")).read()
BLOCK = [b for b in ex.blocks_of(SKILL) if ex.MARKER in b][0]
TABLE_ROWS = ex.table(BLOCK)[1]

RECEIPTS = []
PROV = {"lane_rev": subprocess.run(["git", "-C", LANE, "rev-parse", "HEAD"],
                                    capture_output=True, text=True).stdout.strip(),
        "exact_sha256": hashlib.sha256(open(EXACT, "rb").read()).hexdigest(),
        "skill_sha256": hashlib.sha256(SKILL.encode()).hexdigest()}
print("provenance", PROV)


def git(d, *a, **kw):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True, **kw)


def build(name, skill_text, extra=None):
    d = os.path.join(S, "fx-" + name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    r = git(d, "init", "-q")
    assert r.returncode == 0
    git(d, "config", "user.email", "fx@round47")
    git(d, "config", "user.name", "round47 fixture")
    top = git(d, "rev-parse", "--show-toplevel").stdout.strip()
    assert top == os.path.realpath(d), (top, d)
    files = {"SKILL.md": skill_text,
             "plans/round-47-claims.md": open(os.path.join(LANE, "plans/round-47-claims.md")).read(),
             "tools/round-47/exact.py": open(EXACT).read(),
             "tools/round-46/gate.py": open(os.path.join(LANE, "tools/round-46/gate.py")).read()}
    for name, _, _ in ex.HARD_REF.findall(BLOCK):
        full = os.path.join(LANE, name)
        if os.path.isfile(full):
            files.setdefault(name, open(full).read())
    files.update(extra or {})
    for p, t in files.items():
        full = os.path.join(d, p)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, "w").write(t)
    git(d, "add", "-A")
    c = git(d, "commit", "-q", "-m", "fixture")
    assert c.returncode == 0, c.stderr
    return d, git(d, "rev-parse", "HEAD").stdout.strip()


def mutate_rows(rows):
    return ex.rewrite_rows(BLOCK, rows)


def score_fixture(name, block, counter=EXACT, extra=None):
    d, rev = build(name, SKILL.replace(BLOCK, block, 1), extra=extra)
    cmd = [sys.executable, "-I", "-B", counter, "--root", d, "--freeze", rev, "--rev", rev]
    t0 = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    r = subprocess.run(cmd, capture_output=True, text=True,
                       env=dict(os.environ, HYAKU_SCRATCH=S, TMPDIR=S))
    t1 = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    out = r.stdout
    rec = {"attack": name, "provenance": PROV, "cmd": " ".join(cmd), "exit": r.returncode,
           "stdout_sha256": hashlib.sha256(out.encode()).hexdigest(),
           "t0": t0, "t1": t1,
           "failing": None, "battery": None, "reason": None}
    try:
        j = json.loads(out)
        rec["failing"] = j.get("failing")
        rec["battery"] = j.get("battery")
        rec["reason"] = j.get("reason")
        rec["rows"] = j.get("rows")
        rec["arm_tokens"] = j.get("arm_tokens")
        rec["refs"] = j.get("refs")
        rec["met_target"] = j.get("met_target")
    except Exception:
        rec["stdout_tail"] = out[-2000:]
        rec["stderr_tail"] = r.stderr[-1000:]
    open(os.path.join(S, name + ".json"), "w").write(json.dumps(rec, indent=1))
    RECEIPTS.append(rec)
    print(name, "exit", rec["exit"], "failing", rec["failing"],
          "battery", {k: (v if not isinstance(v, list) else len(v))
                      for k, v in (rec["battery"] or {}).items() if k != "fixtures"})
    return rec


# ---- control: genuine block, real counter -------------------------------------
score_fixture("ctrl-genuine", BLOCK)

# ---- A1: every exit cell says 0 (no defect is claimed to be caught) -----------
rows = [r[:3] + ["0"] for r in TABLE_ROWS]
score_fixture("exit-all-zero", mutate_rows(rows))

# ---- A2: every v2-hole cell is junk ------------------------------------------
rows = [r[:1] + ["x"] + r[2:] for r in TABLE_ROWS]
score_fixture("v2hole-junk", mutate_rows(rows))

# ---- A3: arm tokens permuted across the rows (bijection, wrong pairing) -------
perm = ["order", "digest", "once", "symbol"]
rows = [r[:2] + [p] + r[3:] for r, p in zip(TABLE_ROWS, perm)]
score_fixture("arm-permuted", mutate_rows(rows))

# ---- A4: every arm cell the same valid token (not a matrix) ------------------
rows = [r[:2] + ["order"] + r[3:] for r in TABLE_ROWS]
score_fixture("arm-all-order", mutate_rows(rows))

# ---- A5: isolating R46-CL3 forgery: 4 rows, one id duplicated ----------------
ids = ["R46-CL2", "R46-CL2", "R46-CL4", "R46-CL6"]
rows = [[ids[i]] + TABLE_ROWS[i][1:] for i in range(4)]
score_fixture("dup-id-isolating", mutate_rows(rows))

# ---- A7: only ONE selectored citation; refs>=3 filled by SELF mentions -------
blk = re.sub(r"(?m)^  Refs: .*$", "  Refs: `corpus/lessons/round-46.md:57-66`.",
             BLOCK, count=1)
score_fixture("refs-minimal", blk)

# ---- A6: dead battery. Neuter one / all mutation functions, re-pin the block --
orig = open(EXACT).read()
SUB = ('def _m_substring_arm(block, spec):\n'
       '    rows = [r[:2] + ["order-ish"] + r[3:] for r in _rows(block)]\n'
       '    return rewrite_rows(block, rows), {}')
DEAD_SUB = 'def _m_substring_arm(block, spec):\n    return block, {}'
assert SUB in orig

# dead-one: neuter substring-arm only
mod = orig.replace(SUB, DEAD_SUB, 1)
sha = hashlib.sha256(mod.encode()).hexdigest()
blk = re.sub(r"interpreter_sha256:[0-9a-f]{64}", "interpreter_sha256:" + sha, BLOCK, count=1)
score_fixture("dead-one", blk,
              counter=os.path.join(S, "counter-dead-one.py"),
              extra=None) if False else None

# write modified counters into per-attack repos because --root must contain them
def dead_counter_repo(label, transforms):
    src = orig
    for a, b in transforms:
        assert a in src, (label, a[:40])
        src = src.replace(a, b, 1)
    sha = hashlib.sha256(src.encode()).hexdigest()
    blk = re.sub(r"interpreter_sha256:[0-9a-f]{64}", "interpreter_sha256:" + sha, BLOCK, count=1)
    d, rev = build("cx-" + label, SKILL.replace(BLOCK, blk, 1),
                   extra={"tools/round-47/exact.py": src})
    cmd = [sys.executable, "-I", "-B", os.path.join(d, "tools/round-47/exact.py"),
           "--root", d, "--freeze", rev, "--rev", rev]
    t0 = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    r = subprocess.run(cmd, capture_output=True, text=True,
                       env=dict(os.environ, HYAKU_SCRATCH=S, TMPDIR=S))
    t1 = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    rec = {"attack": "dead-" + label, "provenance": PROV, "cmd": " ".join(cmd), "exit": r.returncode,
           "stdout_sha256": hashlib.sha256(r.stdout.encode()).hexdigest(),
           "t0": t0, "t1": t1, "interpreter_sha256": sha}
    try:
        j = json.loads(r.stdout)
        rec.update(failing=j.get("failing"), battery=j.get("battery"),
                   reason=j.get("reason"), met_target=j.get("met_target"))
    except Exception:
        rec["stdout_tail"] = r.stdout[-3000:]
        rec["stderr_tail"] = r.stderr[-1500:]
    open(os.path.join(S, "dead-" + label + ".json"), "w").write(json.dumps(rec, indent=1))
    RECEIPTS.append(rec)
    print("dead-" + label, "exit", rec["exit"], "failing", rec["failing"],
          "forgeries_total", (rec.get("battery") or {}).get("forgeries_total"),
          "v2_green", (rec.get("battery") or {}).get("v2_green"),
          "v3_green", (rec.get("battery") or {}).get("v3_green"))
    return rec


dead_counter_repo("one", [(SUB, DEAD_SUB)])

ALL_DEAD = [
    (SUB, DEAD_SUB),
    ('def _m_duplicate_id(block, spec):\n'
     '    rows = [r[:] for r in _rows(block)]\n'
     '    rows.insert(2, ["R46-CL2", "a duplicate trigger cell", "order", "1"])\n'
     '    return rewrite_rows(block, rows), {}',
     'def _m_duplicate_id(block, spec):\n    return block, {}'),
    ('def _m_stale_digest(block, spec):\n'
     '    m = MUT_PIN.search(block)\n'
     '    if not m:\n'
     '        raise ValueError("block carries no mutations_sha256 to stale")\n'
     '    stale = hashlib.sha256("\\n".join(n for n, _ in MUTATIONS[:3]).encode()).hexdigest()\n'
     '    return block.replace(m.group(1), stale, 1), {}',
     'def _m_stale_digest(block, spec):\n    return block, {}'),
    ('def _m_flag_order(block, spec):\n    return block, {GATE46: ("gate_order_swapped", None)}',
     'def _m_flag_order(block, spec):\n    return block, {}'),
]
dead_counter_repo("all", ALL_DEAD)

open(os.path.join(S, "attacks.jsonl"), "w").write(
    "\n".join(json.dumps(r) for r in RECEIPTS) + "\n")
print("WROTE", len(RECEIPTS), "receipts")
