#!/usr/bin/env python3
"""Demonstrate that four minimal clause changes close the verified holes, and that the
landed block still scores met under them."""
import hashlib, json, os, re, shutil, subprocess, sys, time

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = "/fast/scratch/hyaku/kaidoku-r47/CritC1Sizing"
EXACT = os.path.join(LANE, "tools/round-47/exact.py")
SRC = open(EXACT).read()
SKILL = open(os.path.join(LANE, "SKILL.md")).read()

import importlib.util
spec = importlib.util.spec_from_file_location("ex", EXACT)
ex = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ex)
BLOCK = [b for b in ex.blocks_of(SKILL) if ex.MARKER in b][0]

# --- the four proposed clauses -------------------------------------------------
FIXES = [
    # (label, old, new)
    ("noop-is-red",
     '            out["fixtures"].append({"name": name, "error": "mutation was a no-op"})\n'
     '            out["forgeries_total"] += 1\n'
     '            out["v2_green"] += 1\n'
     '            continue',
     '            out["fixtures"].append({"name": name, "error": "mutation was a no-op"})\n'
     '            out["forgeries_total"] += 1\n'
     '            out["crash"] += 1\n'
     '            continue'),
    ("arm-bijection",
     '    if hard:\n        if any(a not in VOCAB for a in arm):\n'
     '            failing.append(f"arm cells not exact vocabulary tokens: {arm}")',
     '    if hard:\n        if any(a not in VOCAB for a in arm):\n'
     '            failing.append(f"arm cells not exact vocabulary tokens: {arm}")\n'
     '        if sorted(arm) != sorted(VOCAB):\n'
     '            failing.append(f"arm cells are not the four tokens once each: {arm}")'),
    ("exit-means-an-arm",
     '    bad_exit = [r for r in rows if len(r) < 4 or r[3].strip("` ") not in {"0", "1", "2"}]',
     '    allowed_exit = {"0", "1", "2"} if not hard else {"1", "2"}\n'
     '    bad_exit = [r for r in rows if len(r) < 4 or r[3].strip("` ") not in allowed_exit]'),
]


def patched(base, with_dead):
    src = base
    for _, old, new in FIXES:
        assert old in src, old[:50]
        src = src.replace(old, new, 1)
    # refs: gate on selector-bearing citations, not on every match
    old = '    if hard and MUST_CITE not in cited:'
    new = ('    if hard:\n'
           '        sel = len([m for m in HARD_REF.findall(block) if m[1]])\n'
           '        if sel < 3:\n'
           '            failing.append(f"selectored citations {sel} < 3")\n'
           '    if hard and MUST_CITE not in cited:')
    assert old in src
    src = src.replace(old, new, 1)
    if with_dead:
        for old, new in DEAD:
            assert old in src
            src = src.replace(old, new, 1)
    return src


DEAD = [
    ('def _m_substring_arm(block, spec):\n'
     '    rows = [r[:2] + ["order-ish"] + r[3:] for r in _rows(block)]\n'
     '    return rewrite_rows(block, rows), {}',
     'def _m_substring_arm(block, spec):\n    return block, {}'),
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

ATTACKS = {
    "ctrl-genuine": BLOCK,
    "exit-all-zero": ex.rewrite_rows(BLOCK, [r[:3] + ["0"] for r in ex.table(BLOCK)[1]]),
    "arm-all-order": ex.rewrite_rows(BLOCK, [r[:2] + ["order"] + r[3:] for r in ex.table(BLOCK)[1]]),
    "arm-permuted": ex.rewrite_rows(BLOCK, [r[:2] + [p] + r[3:] for r, p in
                                            zip(ex.table(BLOCK)[1],
                                                ["order", "digest", "once", "symbol"])]),
    "refs-minimal": re.sub(r"(?m)^  Refs: .*$", "  Refs: `corpus/lessons/round-46.md:57-66`.",
                           BLOCK, count=1),
}

RESULTS = []


def build(name, skill_text, counter_src):
    d = os.path.join(S, "px-" + name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    subprocess.run(["git", "-C", d, "config", "user.email", "fx@round47"], check=True)
    subprocess.run(["git", "-C", d, "config", "user.name", "fx"], check=True)
    assert subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                          capture_output=True, text=True).stdout.strip() == os.path.realpath(d)
    files = {"SKILL.md": skill_text,
             "plans/round-47-claims.md": open(os.path.join(LANE, "plans/round-47-claims.md")).read(),
             "tools/round-47/exact.py": counter_src,
             "tools/round-46/gate.py": open(os.path.join(LANE, "tools/round-46/gate.py")).read()}
    for nm, _, _ in ex.HARD_REF.findall(BLOCK):
        full = os.path.join(LANE, nm)
        if os.path.isfile(full):
            files.setdefault(nm, open(full).read())
    for p, t in files.items():
        full = os.path.join(d, p)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, "w").write(t)
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "commit", "-q", "-m", "fixture"], check=True)
    return d, subprocess.run(["git", "-C", d, "rev-parse", "HEAD"],
                             capture_output=True, text=True).stdout.strip()


def run(label, block, counter_src):
    sha = hashlib.sha256(counter_src.encode()).hexdigest()
    blk = re.sub(r"interpreter_sha256:[0-9a-f]{64}", "interpreter_sha256:" + sha, block, count=1)
    d, rev = build(label, SKILL.replace(BLOCK, blk, 1), counter_src)
    cmd = [sys.executable, "-I", "-B", os.path.join(d, "tools/round-47/exact.py"),
           "--root", d, "--freeze", rev, "--rev", rev]
    r = subprocess.run(cmd, capture_output=True, text=True,
                       env=dict(os.environ, HYAKU_SCRATCH=S, TMPDIR=S))
    rec = {"case": label, "exit": r.returncode,
           "stdout_sha256": hashlib.sha256(r.stdout.encode()).hexdigest(),
           "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    try:
        j = json.loads(r.stdout)
        rec.update(failing=j.get("failing"), met_target=j.get("met_target"),
                   battery=j.get("battery"), refs=j.get("refs"),
                   refs_selector=j.get("refs_selector"))
    except Exception:
        rec["tail"] = (r.stdout + r.stderr)[-800:]
    RESULTS.append(rec)
    print(label, "exit", rec["exit"], "failing", rec.get("failing"))
    return rec


fixed = patched(SRC, with_dead=False)
for k, v in ATTACKS.items():
    run("fixed-" + k, v, fixed)

dead_fixed = patched(SRC, with_dead=True)
run("fixed-dead-all", BLOCK, dead_fixed)

open(os.path.join(S, "fixdemo.json"), "w").write(json.dumps(RESULTS, indent=1))
