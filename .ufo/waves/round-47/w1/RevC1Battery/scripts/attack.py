#!/usr/bin/env python3
"""RevC1Battery — attack the C1 battery: is forgeries_total == 4 a real denominator?

Every lane is built from the FREEZE bytes at 5017e1f (claims, tools/, lessons) plus the
draft block 24 snapshotted from the lane worktree.  Each variant changes exactly one
thing in tools/round-47/exact.py, plus the mechanically re-derived interpreter_sha256
pin inside SKILL.md block 24 — the pin a forger recomputes over its own frozen bytes.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time

S = "/fast/scratch/hyaku/kaidoku-r47/RevC1Battery"
SRC = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
FREEZE = "5017e1f7299c3a812e87e7950148f54313dd279e"
OUT = os.path.join(S, "runs")
DRAFT = os.path.join(S, "draft-SKILL.md")
os.makedirs(OUT, exist_ok=True)

CLAIMS = "plans/round-47-claims.md"
SELF = "tools/round-47/exact.py"
MARK = "<!-- exactness-table v3 -->"
PIN = re.compile(r"interpreter_sha256:([0-9a-f]{64})")
MPIN = re.compile(r"mutations_sha256:([0-9a-f]{64})")


def run(args, cwd=None, env=None):
    t = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True, env=env)
    return {"cmd": args, "cwd": cwd, "utc": t, "exit": p.returncode,
            "stdout_sha256": hashlib.sha256(p.stdout.encode()).hexdigest(),
            "stdout": p.stdout, "stderr": p.stderr[-4000:]}


def show(rev, path):
    return subprocess.run(["git", "-C", SRC, "show", f"{rev}:{path}"],
                          capture_output=True, text=True).stdout


def block_of(skill):
    craft = skill.split("## Queue-drain craft ", 1)[1].split("\n## ", 1)[0]
    blocks = re.split(r"(?m)^- \*\*", craft)[1:]
    marked = [b for b in blocks if MARK in b]
    assert len(marked) == 1, f"marker blocks {len(marked)}"
    return marked[0]


def names_digest(names):
    return hashlib.sha256("\n".join(names).encode()).hexdigest()


def build_lane(tag, self_src, block=None, extra=None):
    lane = os.path.join(S, tag)
    shutil.rmtree(lane, ignore_errors=True)
    os.makedirs(lane)
    subprocess.run(f"git -C {SRC} archive {FREEZE} {CLAIMS} tools/round-47 "
                   f"tools/round-46 corpus/lessons/round-46.md "
                   f"corpus/lessons/round-45.md SKILL.md | tar -x -C {lane}",
                   shell=True, check=True)
    with open(os.path.join(lane, SELF), "w") as fh:
        fh.write(self_src)
    for path, text in (extra or {}).items():
        full = os.path.join(lane, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as fh:
            fh.write(text)
    g = lambda *a: subprocess.run(
        ["git", "-C", lane, "-c", "user.name=fx", "-c", "user.email=fx@r47", *a],
        check=True, capture_output=True, text=True)
    g("init", "-q")
    top = subprocess.run(["git", "-C", lane, "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True).stdout.strip()
    assert top == lane, (top, lane)
    g("add", "-A")
    g("commit", "-qm", "freeze: round-47 claims + tools")
    f1 = g("rev-parse", "HEAD").stdout.strip()
    with open(DRAFT) as fh:
        skill = fh.read()
    if block is not None:
        skill = skill.replace(block_of(skill), block, 1)
    want = hashlib.sha256(self_src.encode()).hexdigest()
    m = PIN.search(skill)
    skill = skill[:m.start(1)] + want + skill[m.end(1):]
    with open(os.path.join(lane, "SKILL.md"), "w") as fh:
        fh.write(skill)
    g("add", "SKILL.md")
    g("commit", "-qm", "land block 24")
    f2 = g("rev-parse", "HEAD").stdout.strip()
    return lane, f1, f2


def counter(tag, lane, f1, f2):
    env = dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S)
    jout = os.path.join(lane, ".ufo", "receipts", f"{tag}.json")
    os.makedirs(os.path.dirname(jout), exist_ok=True)
    rec = run([sys.executable, "-I", "-B", SELF, "--root", lane, "--freeze", f1,
               "--rev", f2, "--json-out", jout], cwd=lane, env=env)
    if os.path.exists(jout):
        with open(jout) as fh:
            rec["receipt"] = json.load(fh)
    rec["tag"] = tag
    with open(os.path.join(OUT, f"{tag}.json"), "w") as fh:
        json.dump(rec, fh, indent=1)
    return rec


def summary(rec):
    r = rec.get("receipt", {})
    b = r.get("battery", {}) or {}
    return {"tag": rec["tag"], "exit": rec["exit"], "met_target": r.get("met_target"),
            "failing": r.get("failing"), "reason": r.get("reason"),
            "battery": {k: b.get(k) for k in ("forgeries_total", "v2_green",
                                              "v3_green", "genuine_green", "crash")},
            "fixtures": [{k: f.get(k) for k in ("name", "error", "v2_exit", "v3_exit",
                                               "v3_failing")}
                         for f in b.get("fixtures", [])],
            "stdout_sha256": rec["stdout_sha256"], "utc": rec["utc"]}


def build_cases(base):
    c = {}
    c["T0-baseline"] = (base, None, {})
    t1 = base.replace(
        'def _m_substring_arm(block, spec):\n'
        '    rows = [r[:2] + ["order-ish"] + r[3:] for r in _rows(block)]\n'
        '    return rewrite_rows(block, rows), {}',
        'def _m_substring_arm(block, spec):\n    return block, {}')
    assert t1 != base
    c["T1-noop-mutation-body"] = (t1, None, {})
    t2 = base.replace('             ("flag-order-drift", _m_flag_order)]',
                      '             ("substring-arm", _m_substring_arm)]')
    assert t2 != base and 'flag-order-drift", _m_flag_order' not in t2
    nd = names_digest(["substring-arm", "duplicate-routed-id",
                       "stale-mutations-digest", "substring-arm"])
    c["T2-dup-name-4-entries"] = (t2, nd, {})
    t2b = t2.replace(
        '        gtext = files(GATE46)\n'
        '        if gtext is None:\n'
        '            failing.append("gate.py absent at rev")\n'
        '        else:\n'
        '            n_ok, n_bad = gtext.count(ORDER), gtext.count(REVERSED)\n'
        '            receipt["gate_order_literal"] = n_ok\n'
        '            receipt["gate_order_reversed"] = n_bad\n'
        '            if n_ok != 1 or n_bad != 0:\n'
        '                failing.append(f"gate.py flag order: {n_ok} correct, {n_bad} reversed")',
        '        pass  # clause 7 (flag order) deleted by the attacker')
    assert t2b != t2
    c["T2b-dup-name-clause7-deleted"] = (t2b, nd, {})
    whole = ('    if hard:\n'
             '        multi = [n for n, ids in enumerate(per_row) if len(ids) != 1]\n'
             '        if multi:\n'
             '            failing.append(f"rows naming != 1 routed id: {multi}")\n'
             '        if sorted(counts) != sorted(ROUTED) or set(counts.values()) != {1}:\n'
             '            failing.append(f"routed cardinality {counts} != each of {ROUTED} exactly once")\n'
             '    else:\n'
             '        missing = [i for i in ROUTED if i not in counts]\n'
             '        if missing:\n'
             '            failing.append(f"routed ids not named by any row: {missing}")\n')
    assert whole in base, "clause-4 block not found verbatim"
    t3 = base.replace(whole, '    # clause 4 (routed-id cardinality) deleted by the attacker\n')
    assert t3 != base
    c["T3-clause4-deleted"] = (t3, None, {})
    t4 = base.replace(
        'MUTATIONS = [("substring-arm", _m_substring_arm),\n'
        '             ("duplicate-routed-id", _m_duplicate_id),\n'
        '             ("stale-mutations-digest", _m_stale_digest),\n'
        '             ("flag-order-drift", _m_flag_order)]',
        'MUTATIONS = [("substring-arm", _m_substring_arm),\n'
        '             ("duplicate-routed-id", _m_duplicate_id),\n'
        '             ("stale-mutations-digest", _m_stale_digest)]')
    assert '("flag-order-drift"' not in t4, "T4 replace failed"
    nd4 = names_digest(["substring-arm", "duplicate-routed-id", "stale-mutations-digest"])
    c["T4-shrunk-3-mutations"] = (t4, nd4, {})
    c["T5-citation-outside-fixture-set"] = (
        base, None, {"corpus/knowledge/probe-r47.md":
                     "probe line one\nprobe line two\nprobe line three\n"},
        "`corpus/knowledge/probe-r47.md:2`")
    return c


if __name__ == "__main__":
    if not os.path.exists(DRAFT):
        shutil.copyfile(os.path.join(SRC, "SKILL.md"), DRAFT)
    draft_sha = hashlib.sha256(open(DRAFT, "rb").read()).hexdigest()
    base = show(FREEZE, SELF)
    out = {"draft_SKILL_sha256": draft_sha,
           "frozen_exact_sha256": hashlib.sha256(base.encode()).hexdigest(),
           "cases": {}}
    for tag, spec in build_cases(base).items():
        src, mdig, extra = spec[0], spec[1], spec[2]
        cite = spec[3] if len(spec) > 3 else None
        block = None
        if mdig or cite:
            block = block_of(open(DRAFT).read())
            if mdig:
                block = MPIN.sub(f"mutations_sha256:{mdig}", block, count=1)
            if cite:
                block = block.rstrip() + f"\n  Probe: {cite}.\n"
        lane, f1, f2 = build_lane(tag, src, block=block, extra=extra)
        rec = counter(tag, lane, f1, f2)
        out["cases"][tag] = summary(rec)
        s = out["cases"][tag]
        print(tag, "exit=%s" % s["exit"], "met=%s" % s["met_target"],
              "failing=%s" % (s["failing"] or s["reason"]), s["battery"], flush=True)
    with open(os.path.join(OUT, "summary.json"), "w") as fh:
        json.dump(out, fh, indent=1)
