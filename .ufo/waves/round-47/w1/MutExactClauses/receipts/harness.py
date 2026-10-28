#!/usr/bin/env python3
"""MutExactClauses: delete one clause at a time from a SCRATCH COPY of
tools/round-47/exact.py and record which detectors go red.

Originals are never written. Every variant lives under $S/v/<name>/tools/...
with the sibling tools/round-46/gate.py copied byte-identically.
"""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = "/fast/scratch/hyaku/kaidoku-r47/MutExactClauses"
SRC = os.path.join(LANE, "tools/round-47/exact.py")
GATE = os.path.join(LANE, "tools/round-46/gate.py")

# --- the deletion edits: (sub-clause id, anchor, replacement) ---------------------

EDITS = {
 "1a-marker-unique": (
'''    if hard:
        if occurrences != 1:
            failing.append(f"marker_occurrences {occurrences} != 1")
        if len(marked) != 1:
            failing.append(f"marker_block_count {len(marked)} != 1")
    else:
        if not marked:
            failing.append("marker_block_count 0")
''',
'''    if not marked:
        failing.append("marker_block_count 0")
'''),
 "1b-block-is-last": (
'''    if hard and not receipt["block_is_last"]:
        failing.append("marker block is not the last craft block")
''', ""),
 "1c-title-24": (
'''    if hard and not block.startswith("24. "):
        failing.append("marker block title does not start with '24. '")
''', ""),
 "2-header": (
'''    if not header_ok:
        failing.append(f"header {header} != {HEADER}")
''', ""),
 "3-full": (
'''    if hard:
        if len(rows) != 4:
            failing.append(f"rows {len(rows)} != 4")
        if any(len(r) != 4 for r in rows):
            failing.append("a row does not have exactly 4 cells")
    elif len(rows) < 4:
        failing.append(f"rows {len(rows)} < 4")
    bad_exit = [r for r in rows if len(r) < 4 or r[3].strip("` ") not in {"0", "1", "2"}]
    if bad_exit:
        failing.append(f"exit cells outside {{0,1,2}}: {len(bad_exit)}")
''', ""),
 "3a-rows-count": (
'''        if len(rows) != 4:
            failing.append(f"rows {len(rows)} != 4")
''', ""),
 "3b-row-cells": (
'''        if any(len(r) != 4 for r in rows):
            failing.append("a row does not have exactly 4 cells")
''', ""),
 "3c-exit-cell": (
'''    bad_exit = [r for r in rows if len(r) < 4 or r[3].strip("` ") not in {"0", "1", "2"}]
    if bad_exit:
        failing.append(f"exit cells outside {{0,1,2}}: {len(bad_exit)}")
''', ""),
 "4-routed-ids": (
'''    if hard:
        multi = [n for n, ids in enumerate(per_row) if len(ids) != 1]
        if multi:
            failing.append(f"rows naming != 1 routed id: {multi}")
        if sorted(counts) != sorted(ROUTED) or set(counts.values()) != {1}:
            failing.append(f"routed cardinality {counts} != each of {ROUTED} exactly once")
    else:
        missing = [i for i in ROUTED if i not in counts]
        if missing:
            failing.append(f"routed ids not named by any row: {missing}")
''',
'''    missing = [i for i in ROUTED if i not in counts]
    if missing:
        failing.append(f"routed ids not named by any row: {missing}")
'''),
 "5-arm-token": (
'''    if hard:
        if any(a not in VOCAB for a in arm):
            failing.append(f"arm cells not exact vocabulary tokens: {arm}")
    else:
        if any(not any(t in a.lower() for t in VOCAB) for a in arm):
            failing.append("arm cells outside the vocabulary")
''',
'''    if any(not any(t in a.lower() for t in VOCAB) for a in arm):
        failing.append("arm cells outside the vocabulary")
'''),
 "6a-digest-pin": (
'''        m = MUT_PIN.search(block)
        receipt["mutations_sha256"] = m.group(1) if m else None
        receipt["mutations_sha256_expected"] = MUT_DIGEST
        if not m or m.group(1) != MUT_DIGEST:
            failing.append("mutations_sha256 does not match the counter's own mutation list")
''', ""),
 "6b-mutation-names": (
'''        names = [n for n, _ in MUTATIONS]
        unnamed = [n for n in names if n not in block]
        if unnamed:
            failing.append(f"mutation names not stated in the block: {unnamed}")
''', ""),
 "7-flag-order": (
'''        gtext = files(GATE46)
        if gtext is None:
            failing.append("gate.py absent at rev")
        else:
            n_ok, n_bad = gtext.count(ORDER), gtext.count(REVERSED)
            receipt["gate_order_literal"] = n_ok
            receipt["gate_order_reversed"] = n_bad
            if n_ok != 1 or n_bad != 0:
                failing.append(f"gate.py flag order: {n_ok} correct, {n_bad} reversed")
''', ""),
 "8-full": (
'''    if receipt["refs"] < 3:
        failing.append(f"refs {receipt['refs']} < 3")
    if bad_refs:
        failing.append(f"unresolved or unvalidated citations: {len(bad_refs)}")
    if hard and MUST_CITE not in cited:
        failing.append(f"does not cite {MUST_CITE}")
    if hard:
        m = SELF_PIN.search(block)
        body = files(SELF)
        want = hashlib.sha256(body.encode()).hexdigest() if body else None
        receipt["interpreter_sha256"] = m.group(1) if m else None
        receipt["interpreter_sha256_expected"] = want
        if want is None:
            failing.append("interpreter absent at rev")
        elif not m or m.group(1) != want:
            failing.append("interpreter sha256 pin does not match the bytes at rev")
''', ""),
 "8a-refs-floor": (
'''    if receipt["refs"] < 3:
        failing.append(f"refs {receipt['refs']} < 3")
''', ""),
 "8b-refs-resolve": (
'''    if bad_refs:
        failing.append(f"unresolved or unvalidated citations: {len(bad_refs)}")
''', ""),
 "8c-must-cite": (
'''    if hard and MUST_CITE not in cited:
        failing.append(f"does not cite {MUST_CITE}")
''', ""),
 "8d-interpreter-pin": (
'''    if hard:
        m = SELF_PIN.search(block)
        body = files(SELF)
        want = hashlib.sha256(body.encode()).hexdigest() if body else None
        receipt["interpreter_sha256"] = m.group(1) if m else None
        receipt["interpreter_sha256_expected"] = want
        if want is None:
            failing.append("interpreter absent at rev")
        elif not m or m.group(1) != want:
            failing.append("interpreter sha256 pin does not match the bytes at rev")
''', ""),
 "9-battery-thresholds": (
'''        for key, want in (("forgeries_total", 4), ("v2_green", 4), ("v3_green", 0),
                          ("genuine_green", 1), ("crash", 0)):
            if battery.get(key) != want:
                failing.append(f"battery {key} {battery.get(key)} != {want}")
''', ""),
}

# clause number -> its sub-clauses (the "delete clause N" variants the seat asked for)
CLAUSES = {
 "C1": ["1a-marker-unique", "1b-block-is-last", "1c-title-24"],
 "C2": ["2-header"],
 "C3": ["3-full"],
 "C4": ["4-routed-ids"],
 "C5": ["5-arm-token"],
 "C6": ["6a-digest-pin", "6b-mutation-names"],
 "C7": ["7-flag-order"],
 "C8": ["8-full"],
 "C9": ["9-battery-thresholds"],
}


EXTRA = {
 "4-both-profiles": (
'''    if hard:
        multi = [n for n, ids in enumerate(per_row) if len(ids) != 1]
        if multi:
            failing.append(f"rows naming != 1 routed id: {multi}")
        if sorted(counts) != sorted(ROUTED) or set(counts.values()) != {1}:
            failing.append(f"routed cardinality {counts} != each of {ROUTED} exactly once")
    else:
        missing = [i for i in ROUTED if i not in counts]
        if missing:
            failing.append(f"routed ids not named by any row: {missing}")
''', ""),
}


def build_variant(name, subs, src_text):
    text = src_text
    for sub in subs:
        anchor, repl = (EDITS | EXTRA)[sub]
        if text.count(anchor) != 1:
            raise SystemExit(f"{sub}: anchor occurs {text.count(anchor)} times")
        text = text.replace(anchor, repl, 1)
    import ast
    ast.parse(text)  # a variant that does not parse is a broken probe, not a survivor
    d = os.path.join(S, "v", name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(os.path.join(d, "tools/round-47"), exist_ok=True)
    os.makedirs(os.path.join(d, "tools/round-46"), exist_ok=True)
    path = os.path.join(d, "tools/round-47/exact.py")
    with open(path, "w") as fh:
        fh.write(text)
    shutil.copyfile(GATE, os.path.join(d, "tools/round-46/gate.py"))
    return path


def load(name, path):
    spec = importlib.util.spec_from_file_location("ex_" + name.replace("-", "_"), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_selftest(d, scratch):
    env = dict(os.environ, HYAKU_SCRATCH=scratch, TMPDIR=scratch)
    t = time.time()
    cp = subprocess.run([sys.executable, "-I", "-B",
                         os.path.join(d, "tools/round-47/exact.py"),
                         "--root", d, "--freeze", "selftest", "--rev", "selftest",
                         "--selftest"],
                        capture_output=True, text=True, env=env, cwd=d)
    out = cp.stdout
    i = out.find("{")
    try:
        data = json.loads(out[i:])
    except Exception:
        data = {"parse_error": out[-400:], "stderr": cp.stderr[-400:]}
    return {"exit": cp.returncode, "stdout_sha256": hashlib.sha256(out.encode()).hexdigest(),
            "stderr_tail": cp.stderr[-300:], "seconds": round(time.time() - t, 2),
            "cases": {c["case"]: {"expect": c["expect"], "got": c["got"], "ok": c["ok"],
                                  "failing": c["failing"]}
                      for c in data.get("cases", [])},
            "failures": data.get("failures"), "raw": data if "cases" not in data else None}


def probes(mod, scratch):
    """Artefact-level probes: one targeted defect each, scored with battery=None.

    A probe names the clause it is designed to trip; the interesting number is which
    deletion variants let it score 0 (survivor) instead of 1."""
    gate_body = open(os.path.join(os.path.dirname(mod.__file__), "..", "round-46",
                                  "gate.py")).read()
    base = {"plans/round-47-claims.md": mod.CLAIMS_BODY,
            "corpus/lessons/round-46.md": "lesson line\n" * 240,
            "tools/round-47/exact.py": open(mod.__file__).read(),
            "tools/round-46/gate.py": gate_body,
            "corpus/lessons/round-45.md": "lesson line\n" * 240}
    G = mod.GOOD_ROWS

    def sc(skill, extra=None, battery=None, profile="v3"):
        files = dict(base)
        files["SKILL.md"] = skill
        files.update(extra or {})
        code, rec = mod.score(skill, lambda p: files.get(p), profile, "probe-rev",
                              battery=battery)
        return code, (rec.get("failing") or rec.get("reason"))

    out = {}
    # not-last: a block after the marked one
    out["1b-block-is-last"] = sc(mod.skill_text(
        mod.good_block() + "- **25. A later plain rule.** body\n"))[0]
    out["1a-marker-unique"] = sc(mod.skill_text(mod.good_block(marker="")))[0]
    out["1c-title-24"] = sc(mod.skill_text(mod.good_block(
        title="An exact binding, unnumbered.")))[0]
    out["2-header"] = sc(mod.skill_text(mod.good_block(
        header="| trigger | v2 hole | arm | exit |")))[0]
    out["3a-rows-count"] = sc(mod.skill_text(mod.good_block(rows=G[:3])))[0]
    out["3b-row-cells"] = sc(mod.skill_text(mod.good_block(
        rows=[r + ("extra",) for r in G])))[0]
    out["3c-exit-cell"] = sc(mod.skill_text(mod.good_block(
        rows=[r[:3] + ("yes",) for r in G])))[0]
    out["4-routed-ids"] = sc(mod.skill_text(mod.good_block(
        rows=G[:3] + [("R46-CL2", "duplicate trigger", "order", "1")])))[0]
    # the ONLY shape clause 4 rejects alone: 4 rows, all four ids present, one row names two
    out["4-multi-id-row"] = sc(mod.skill_text(mod.good_block(rows=[
        ("R46-CL2 R46-CL3", "one cell names two routed ids", "symbol", "1"),
        G[2], G[3],
        ("R46-CL2", "and CL2 is the id counted twice", "once", "1")])))[0]
    out["5-arm-token"] = sc(mod.skill_text(mod.good_block(
        rows=[r[:2] + ("order-ish",) + r[3:] for r in G])))[0]
    out["6a-digest-pin"] = sc(mod.skill_text(mod.good_block(
        digest=hashlib.sha256(b"substring-arm").hexdigest())))[0]
    blk = mod.good_block()
    out["6b-mutation-names"] = sc(mod.skill_text(
        blk.replace("stale-mutations-digest, ", "")))[0]
    out["7-flag-order"] = sc(mod.skill_text(mod.good_block()),
                             extra={"tools/round-46/gate.py": gate_body.replace(
                                 mod.ORDER, mod.REVERSED, 1)})[0]
    two_refs = "`corpus/lessons/round-46.md:10-30`, `plans/round-47-claims.md:20`"
    out["8a-refs-floor"] = sc(mod.skill_text(mod.good_block(refs=two_refs)))[0]
    out["8b-refs-resolve"] = sc(mod.skill_text(mod.good_block(
        refs=mod.GOOD_REFS.replace("plans/round-47-claims.md:20",
                                   "corpus/lessons/round-46.md:9000"))))[0]
    out["8c-must-cite"] = sc(mod.skill_text(mod.good_block(
        refs="`corpus/lessons/round-45.md:10-30`, `corpus/lessons/round-45.md:40-60`, "
             "`plans/round-47-claims.md:20`")))[0]
    out["8d-interpreter-pin"] = sc(mod.skill_text(mod.good_block(pin="0" * 64)))[0]
    # calibration of clause 8's citation floor: HARD_REF also matches the block's own
    # `tools/round-47/exact.py` self-reference, which clause 8 exempts from the selector rule
    one = "`corpus/lessons/round-46.md:10-30`"
    two = "`corpus/lessons/round-46.md:10-30`, `plans/round-47-claims.md:20`"
    blk2 = mod.good_block(refs=two)
    # a second marker OUTSIDE the craft section: clause 1 counts over the whole document
    out["1-stray-marker"] = sc(mod.skill_text(mod.good_block()).replace(
        "## Next section", "a prose line " + mod.MARKER + "\n## Next section"))[0]
    out["8a-floor-1real"] = sc(mod.skill_text(mod.good_block(refs=one)))[0]
    out["8a-floor-2real"] = sc(mod.skill_text(blk2))[0]
    out["8a-floor-2real-noself"] = sc(mod.skill_text(
        blk2.replace("`tools/round-47/exact.py` ", "")))[0]
    out["8a-floor-2same"] = sc(mod.skill_text(mod.good_block(
        refs="`corpus/lessons/round-46.md:10-30`, `corpus/lessons/round-46.md:40-60`")))[0]
    out["9-battery-thresholds"] = sc(mod.skill_text(mod.good_block()), battery={
        "forgeries_total": 4, "v2_green": 4, "v3_green": 1, "genuine_green": 1,
        "crash": 0})[0]
    return out


def battery(mod, scratch):
    files = {"SKILL.md": mod.skill_text(mod.good_block()),
             "plans/round-47-claims.md": mod.CLAIMS_BODY,
             "corpus/lessons/round-46.md": "lesson line\n" * 240,
             "tools/round-47/exact.py": open(mod.__file__).read(),
             "tools/round-46/gate.py": open(os.path.join(
                 os.path.dirname(mod.__file__), "..", "round-46", "gate.py")).read()}
    d, rev = mod._repo(files, scratch, prefix="bat-")
    try:
        bat = mod.run_battery(d, rev, scratch)
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return {f["name"]: {"v2_exit": f.get("v2_exit"), "v3_exit": f.get("v3_exit"),
                        "v3_failing": f.get("v3_failing")}
            for f in bat.get("fixtures", [])} | {
        "_aggregate": {k: bat.get(k) for k in ("forgeries_total", "v2_green", "v3_green",
                                               "genuine_green", "crash", "genuine_exit")}}


def main():
    src_text = open(SRC).read()
    src_sha = hashlib.sha256(src_text.encode()).hexdigest()
    scratch = os.path.join(S, "tmp")
    os.makedirs(scratch, exist_ok=True)
    results = {}

    variants = [("pristine", [])]
    variants += [(c, subs) for c, subs in CLAUSES.items()]
    for sub in EDITS:
        if sub not in ("3-full", "8-full"):
            variants.append((sub, [sub]))
    variants.append(("4-both-profiles", ["4-both-profiles"]))
    variants.append(("3a+4-removed", ["3a-rows-count", "4-both-profiles"]))

    for name, subs in variants:
        path = build_variant(name, subs, src_text)
        d = os.path.dirname(os.path.dirname(os.path.dirname(path)))
        sub_scratch = os.path.join(scratch, name)
        os.makedirs(sub_scratch, exist_ok=True)
        mod = load(name, path)
        st = run_selftest(d, sub_scratch)
        pr = probes(mod, sub_scratch)
        bt = battery(mod, sub_scratch)
        results[name] = {"subs": subs, "sha256": hashlib.sha256(
            open(path, "rb").read()).hexdigest(), "selftest": st, "probes": pr,
            "battery": bt}
        print(f"{name:24s} selftest_exit={st['exit']} failures={st['failures']} "
              f"probes={sum(1 for v in pr.values() if v == 0)}/{len(pr)} green "
              f"v3_green={bt['_aggregate']['v3_green']}", flush=True)
    results["_meta"] = {"src": SRC, "src_sha256": src_sha,
                        "src_sha256_after": hashlib.sha256(
                            open(SRC, "rb").read()).hexdigest(),
                        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    with open(os.path.join(S, "results.json"), "w") as fh:
        json.dump(results, fh, indent=1, sort_keys=True)
    print("src sha before/after:", results["_meta"]["src_sha256"],
          results["_meta"]["src_sha256_after"])


if __name__ == "__main__":
    main()
