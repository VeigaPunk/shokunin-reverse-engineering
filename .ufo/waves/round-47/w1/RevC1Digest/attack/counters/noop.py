#!/usr/bin/env python3
"""Round-47 C1 counter — exactness bindings over SKILL.md craft rule block 24.

Profiles:
  v3 (default) — exact tokens, exactly-once routed ids, a pinned mutation digest and a
                 flag-order clause over tools/round-46/gate.py.
  v2           — the round-46 semantics ported (substring arm vocabulary, at-least-once ids,
                 no digest clause, no flag-order clause), used only to score the round's own
                 forgeries against the hole it measures.

Exit codes: 0 met; 1 not met; 2 could-not-evaluate.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "round-46"))
import gate  # noqa: E402

SELF = "tools/round-47/exact.py"
CLAIMS = "plans/round-47-claims.md"
GATE46 = "tools/round-46/gate.py"
CRAFT = "## Queue-drain craft "
MALFORMED = "## Queue-drain craft\n"
MARKER = "<!-- exactness-table v3 -->"
HEADER = ["trigger", "v2 hole", "v3 arm", "exit"]
ROUTED = ["R46-CL2", "R46-CL3", "R46-CL4", "R46-CL6"]
VOCAB = ("symbol", "once", "digest", "order")
ALLOW = ("corpus/lessons/", "corpus/knowledge/", "plans/", "tools/round-47/")
MUST_CITE = "corpus/lessons/round-46.md"
ORDER = '"-m", "--diff-merges=first-parent"'
REVERSED = '"--diff-merges=first-parent", "-m"'
HARD_REF = re.compile(r"((?:corpus|plans|tools)/[A-Za-z0-9._/-]+)(?::(\d+)(?:-(\d+))?)?")
MUT_PIN = re.compile(r"mutations_sha256:([0-9a-f]{64})")
SELF_PIN = re.compile(r"interpreter_sha256:([0-9a-f]{64})")
ID = re.compile(r"R46-CL\d+")


class Malformed(Exception):
    pass


# --- the mutation list, and the digest the block must pin -------------------------

def _table_span(block):
    lines = block.splitlines()
    idx = [i for i, l in enumerate(lines) if l.strip().startswith("|")]
    if not idx:
        raise ValueError("no table in the block")
    return lines, idx[0], idx[-1]


def rewrite_rows(block, rows):
    lines, start, end = _table_span(block)
    header, _ = table(block)
    body = ["| " + " | ".join(header) + " |",
            "|" + "|".join(["---"] * len(header)) + "|"]
    body += ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join(lines[:start] + body + lines[end + 1:])


def _m_substring_arm(block, spec):
    rows = [r[:2] + ["order-ish"] + r[3:] for r in _rows(block)]
    return rewrite_rows(block, rows), {}


def _m_duplicate_id(block, spec):
    rows = [r[:] for r in _rows(block)]
    rows.insert(2, ["R46-CL2", "a duplicate trigger cell", "order", "1"])
    return rewrite_rows(block, rows), {}


def _m_stale_digest(block, spec):
    m = MUT_PIN.search(block)
    if not m:
        raise ValueError("block carries no mutations_sha256 to stale")
    stale = hashlib.sha256("\n".join(n for n, _ in MUTATIONS[:3]).encode()).hexdigest()
    return block.replace(m.group(1), stale, 1), {}


def _m_flag_order(block, spec):
    return block, {GATE46: ("gate_order_swapped", None)}


MUTATIONS = [("substring-arm", _m_substring_arm),
             ("duplicate-routed-id", lambda block, spec: (block, {})),
             ("stale-mutations-digest", _m_stale_digest),
             ("flag-order-drift", _m_flag_order)]
MUT_DIGEST = hashlib.sha256("\n".join(n for n, _ in MUTATIONS).encode()).hexdigest()


# --- parse helpers ----------------------------------------------------------------

def craft_section(skill):
    if CRAFT not in skill:
        if MALFORMED in skill:
            raise Malformed("craft heading lacks its trailing space")
        raise Malformed("no `## Queue-drain craft ` section")
    return skill.split(CRAFT, 1)[1].split("\n## ", 1)[0]


def blocks_of(skill):
    return re.split(r"(?m)^- \*\*", craft_section(skill))[1:]


def table(block):
    lines = [l.strip() for l in block.splitlines() if l.strip().startswith("|")]
    if len(lines) < 2:
        return [], []
    rows, header = [], None
    for line in lines:
        cells = _cells(line)
        if all(re.fullmatch(r":?-{2,}:?", c) or c == "" for c in cells):
            continue
        if header is None:
            header = cells
            continue
        rows.append(cells)
    return header or [], rows


def _cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _rows(block):
    return table(block)[1]


def line_count(files, path):
    body = files(path)
    return None if body is None else len(body.splitlines())


def check_refs(block, files, hard):
    bad, cited = [], set()
    for name, first, last in HARD_REF.findall(block):
        if not name.startswith(ALLOW):
            bad.append(f"{name}: outside the validated path set")
            continue
        cited.add(name)
        if name == SELF:
            continue  # identified by its own sha256 pin, not by a line selector
        if hard and not first:
            bad.append(f"{name}: no line selector")
            continue
        count = line_count(files, name)
        if count is None:
            bad.append(f"{name}: absent at rev")
            continue
        start, end = int(first or 1), int(last or first or 1)
        if not (1 <= start <= end <= count):
            bad.append(f"{name}:{start}-{end} outside 1..{count}")
    return bad, cited


# --- score ------------------------------------------------------------------------

def score(skill, files, profile, rev, battery=None):
    hard = profile == "v3"
    try:
        blocks = blocks_of(skill)
    except Malformed as exc:
        return 2, {"reason": str(exc)}
    occurrences = skill.count(MARKER)
    marked = [b for b in blocks if MARKER in b]
    receipt = {"counter": "round-47-c1", "profile": profile, "rev": rev,
               "rule_blocks": len(blocks), "marker_occurrences": occurrences,
               "block_present": len(marked)}
    failing = []
    if hard:
        if occurrences != 1:
            failing.append(f"marker_occurrences {occurrences} != 1")
        if len(marked) != 1:
            failing.append(f"marker_block_count {len(marked)} != 1")
    else:
        if not marked:
            failing.append("marker_block_count 0")
    if not marked:
        receipt.update(met_target=False, failing=failing)
        return 1, receipt
    block = marked[0]
    header, rows = table(block)
    receipt.update({"block_is_last": blocks[-1] is block,
                    "block_title": block.split("**", 1)[0][:24],
                    "header": header, "rows": len(rows)})
    if hard and not receipt["block_is_last"]:
        failing.append("marker block is not the last craft block")
    if hard and not block.startswith("24. "):
        failing.append("marker block title does not start with '24. '")
    if hard:
        header_ok = header == HEADER
    else:
        header_ok = all(any(t in h.lower() for h in header) for t in
                        (x.lower() for x in HEADER))
    receipt["header_ok"] = header_ok
    if not header_ok:
        failing.append(f"header {header} != {HEADER}")
    if hard:
        if len(rows) != 4:
            failing.append(f"rows {len(rows)} != 4")
        if any(len(r) != 4 for r in rows):
            failing.append("a row does not have exactly 4 cells")
    elif len(rows) < 4:
        failing.append(f"rows {len(rows)} < 4")
    bad_exit = [r for r in rows if len(r) < 4 or r[3].strip("` ") not in {"0", "1", "2"}]
    if bad_exit:
        failing.append(f"exit cells outside {{0,1,2}}: {len(bad_exit)}")

    # clause 4: routed-id cardinality -------------------------------------------------
    per_row = [ID.findall(r[0]) if r else [] for r in rows]
    counts = {}
    for ids in per_row:
        for i in ids:
            counts[i] = counts.get(i, 0) + 1
    receipt["routed_counts"] = counts
    if hard:
        multi = [n for n, ids in enumerate(per_row) if len(ids) != 1]
        if multi:
            failing.append(f"rows naming != 1 routed id: {multi}")
        if sorted(counts) != sorted(ROUTED) or set(counts.values()) != {1}:
            failing.append(f"routed cardinality {counts} != each of {ROUTED} exactly once")
    else:
        missing = [i for i in ROUTED if i not in counts]
        if missing:
            failing.append(f"routed ids not named by any row: {missing}")

    # clause 5: arm token, exactly ------------------------------------------------
    arm = [r[2].strip("` ") if len(r) > 2 else "" for r in rows]
    receipt["arm_tokens"] = arm
    if hard:
        if any(a not in VOCAB for a in arm):
            failing.append(f"arm cells not exact vocabulary tokens: {arm}")
    else:
        if any(not any(t in a.lower() for t in VOCAB) for a in arm):
            failing.append("arm cells outside the vocabulary")

    # clause 6 + 7: digest pin and flag order --------------------------------------
    if hard:
        m = MUT_PIN.search(block)
        receipt["mutations_sha256"] = m.group(1) if m else None
        receipt["mutations_sha256_expected"] = MUT_DIGEST
        if not m or m.group(1) != MUT_DIGEST:
            failing.append("mutations_sha256 does not match the counter's own mutation list")
        names = [n for n, _ in MUTATIONS]
        unnamed = [n for n in names if n not in block]
        if unnamed:
            failing.append(f"mutation names not stated in the block: {unnamed}")
        gtext = files(GATE46)
        if gtext is None:
            failing.append("gate.py absent at rev")
        else:
            n_ok, n_bad = gtext.count(ORDER), gtext.count(REVERSED)
            receipt["gate_order_literal"] = n_ok
            receipt["gate_order_reversed"] = n_bad
            if n_ok != 1 or n_bad != 0:
                failing.append(f"gate.py flag order: {n_ok} correct, {n_bad} reversed")

    # clause 8: citations and pins ------------------------------------------------
    bad_refs, cited = check_refs(block, files, hard)
    receipt["refs"] = len(HARD_REF.findall(block))
    receipt["cited"] = sorted(cited)
    receipt["unresolved_citations"] = bad_refs
    if receipt["refs"] < 3:
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

    if battery is not None:
        receipt["battery"] = battery
        for key, want in (("forgeries_total", 4), ("v2_green", 4), ("v3_green", 0),
                          ("genuine_green", 1), ("crash", 0)):
            if battery.get(key) != want:
                failing.append(f"battery {key} {battery.get(key)} != {want}")
    receipt["met_target"] = not failing
    receipt["failing"] = failing
    return (0 if not failing else 1), receipt


# --- battery ----------------------------------------------------------------------

def _repo(files, scratch_root, prefix="fx-"):
    d = tempfile.mkdtemp(dir=scratch_root, prefix=prefix)
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    for k, v in (("user.email", "fx@round47"), ("user.name", "round47 fixture")):
        subprocess.run(["git", "-C", d, "config", k, v], check=True)
    top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True).stdout.strip()
    if top != d:
        raise RuntimeError("fixture toplevel mismatch")
    for p, text in files.items():
        full = os.path.join(d, p)
        os.makedirs(os.path.dirname(full) or d, exist_ok=True)
        with open(full, "w") as fh:
            fh.write(text)
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "commit", "-q", "-m", "fixture"], check=True)
    rev = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    return d, rev


def _fixture_files(root, rev):
    """The real repo's bytes for every file a block-24 fixture needs."""
    skill = gate.show(root, rev, "SKILL.md")
    out = {"SKILL.md": skill}
    for p in (CLAIMS, SELF, GATE46, MUST_CITE, "corpus/lessons/round-45.md"):
        body = gate.show(root, rev, p)
        if body is not None:
            out[p] = body
    return out


def run_battery(root, rev, scratch_root):
    skill = gate.show(root, rev, "SKILL.md")
    if skill is None:
        return {"error": "SKILL.md absent at rev"}
    blocks = blocks_of(skill)
    marked = [b for b in blocks if MARKER in b]
    if len(marked) != 1:
        return {"error": f"cannot build a battery: marker blocks {len(marked)}"}
    block = marked[0]
    base = _fixture_files(root, rev)
    files_at = lambda d, r: (lambda p: gate.show(d, r, p))  # noqa: E731
    out = {"fixtures": [], "forgeries_total": 0, "v2_green": 0, "v3_green": 0,
           "genuine_green": 0, "crash": 0, "mutations_sha256": MUT_DIGEST}
    code, _ = score(skill, lambda p: base.get(p), "v3", rev, battery=None)
    out["genuine_green"] = 1 if code == 0 else 0
    out["genuine_exit"] = code
    if code == 2:
        out["crash"] += 1
    for name, fn in MUTATIONS:
        text, overrides = fn(block, None)
        if text == block and not overrides:
            out["fixtures"].append({"name": name, "error": "mutation was a no-op"})
            out["forgeries_total"] += 1
            out["v2_green"] += 1
            continue
        files = dict(base)
        files["SKILL.md"] = skill.replace(block, text, 1)
        for path, (kind, _) in overrides.items():
            body = files.get(path)
            if body is None:
                body = gate.show(root, rev, path)
            if kind == "gate_order_swapped" and body:
                files[path] = body.replace(ORDER, REVERSED, 1)
        d, frev = _repo(files, scratch_root)
        try:
            f = files_at(d, frev)
            c2, r2 = score(files["SKILL.md"], f, "v2", frev, battery=None)
            c3, r3 = score(files["SKILL.md"], f, "v3", frev, battery=None)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        out["forgeries_total"] += 1
        out["v2_green"] += 1 if c2 == 0 else 0
        out["v3_green"] += 1 if c3 == 0 else 0
        out["crash"] += 1 if c3 == 2 else 0
        out["fixtures"].append({"name": name, "v2_exit": c2, "v3_exit": c3,
                                "v2_failing": r2.get("failing", r2.get("reason")),
                                "v3_failing": r3.get("failing", r3.get("reason"))})
    return out


# --- CLI --------------------------------------------------------------------------

def evaluate(root, freeze, rev, profile="v3", with_battery=True):
    flat, fs = gate.freeze_state(root, freeze, rev, CLAIMS)
    if flat == 2:
        return 2, dict(fs, counter="round-47-c1", profile=profile)
    skill = gate.show(root, rev, "SKILL.md")
    if skill is None:
        return 2, {"reason": "SKILL.md absent at rev", "counter": "round-47-c1"}
    files = lambda p: gate.show(root, rev, p)  # noqa: E731
    code, receipt = score(skill, files, profile, rev, battery=None)
    if with_battery and code == 0:
        scratch_root, err = gate.scratch("kaidoku-r47-battery-")
        if err:
            return 2, {"reason": err, "counter": "round-47-c1"}
        try:
            battery = run_battery(root, rev, scratch_root)
        finally:
            shutil.rmtree(scratch_root, ignore_errors=True)
        if "error" in battery:
            return 2, {"reason": "battery: " + battery["error"], "counter": "round-47-c1"}
        code, receipt = score(skill, files, profile, rev, battery=battery)
    elif with_battery:
        receipt["battery"] = {"skipped": "artefact fails a structural clause first"}
    receipt.update({"freeze": fs["freeze"], "frozen_derived": fs["frozen_derived"],
                    "frozen_path_changed": fs["frozen_path_changed"],
                    "touched": len(fs["touched"]), "restored": fs["restored"]})
    return code, receipt


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", required=True)
    ap.add_argument("--freeze", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--profile", default="v3", choices=("v2", "v3"))
    ap.add_argument("--no-battery", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--json-out")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    out, err = gate.out_path(args.root, args.json_out)
    if err:
        print(json.dumps({"reason": err}))
        return 2
    code, receipt = gate.main_guard(
        lambda: evaluate(args.root, args.freeze, args.rev, args.profile,
                         not args.no_battery))
    gate.emit(receipt, out)
    return code


# --- selftest ---------------------------------------------------------------------

GOOD_ROWS = [("R46-CL2", "`order-ish` satisfies `order`", "symbol", "1"),
             ("R46-CL3", "an id in some row, not once", "once", "1"),
             ("R46-CL4", "the mutation list has no digest", "digest", "1"),
             ("R46-CL6", "one argument reorder blinds the merge arm", "order", "1")]
GOOD_REFS = ("`corpus/lessons/round-46.md:10-30`, `corpus/lessons/round-46.md:40-60`, "
             "`plans/round-47-claims.md:20`")
CLAIMS_BODY = ("# claims\n\n" + "filler line\n" * 60 +
               "\n## Frozen paths (exact)\n\n- `plans/round-47-claims.md`\n"
               "- `tools/round-47/`\n\n## After\n\ntail\n")


def good_block(rows=None, header="| trigger | v2 hole | v3 arm | exit |",
               refs=GOOD_REFS, digest=None, pin=None, marker=MARKER,
               title="24. An exact binding is an equality, not a containment."):
    rows = GOOD_ROWS if rows is None else rows
    digest = digest or MUT_DIGEST
    pin = pin or hashlib.sha256(open(__file__, "rb").read()).hexdigest()
    body = (f"- **{title}** {marker} `tools/round-47/exact.py` interpreter_sha256:{pin} "
            f"mutations_sha256:{digest} names substring-arm, duplicate-routed-id, "
            f"stale-mutations-digest, flag-order-drift. Source S143.\n\n"
            f"{header}\n|---|---|---|---|\n")
    for r in rows:
        body += "| " + " | ".join(r) + " |\n"
    return body + f"\n  Refs: {refs}\n"


def skill_text(block, before=23, heading="## Queue-drain craft (test) "):
    text = "# SKILL\n\nintro\n\n" + heading + "\n\n"
    for i in range(1, before + 1):
        text += f"- **{i}. Plain rule {i}.** body text\n"
    return text + block + "\n## Next section\n\ntail\n"


def selftest():
    root, err = gate.scratch("kaidoku-r47-selftest-")
    if err:
        print(json.dumps({"reason": err}))
        return 2
    cases = []

    def run(name, expect, skill, overrides=None, profile="v3"):
        files = {"SKILL.md": skill, "plans/round-47-claims.md": CLAIMS_BODY,
                 "corpus/lessons/round-46.md": "lesson line\n" * 240,
                 "tools/round-47/exact.py": open(__file__).read(),
                 "tools/round-46/gate.py": open(
                     os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  "..", "round-46", "gate.py")).read()}
        files.update(overrides or {})
        d = None
        try:
            d, rev = _repo(files, root, prefix="self-")
            got, rec = score(files["SKILL.md"], lambda p: gate.show(d, rev, p),
                             profile, rev, battery=None)
        except Exception as exc:  # noqa: BLE001
            got, rec = "crash", {"reason": f"{type(exc).__name__}: {exc}"}
        finally:
            if d:
                shutil.rmtree(d, ignore_errors=True)
        cases.append({"case": name, "expect": expect, "got": got, "ok": got == expect,
                      "failing": rec.get("failing") or rec.get("reason")})
        return got

    run("green", 0, skill_text(good_block()))
    run("red-marker-missing", 1, skill_text(good_block(marker="")))
    run("red-two-markers", 1, skill_text(good_block(
        marker=MARKER + " " + MARKER)))
    run("red-title-unnumbered", 1, skill_text(good_block(
        title="An exact binding, unnumbered.")))
    run("red-header-inexact", 1, skill_text(good_block(
        header="| trigger | v2 hole | arm | exit |")))
    run("red-rows-not-four", 1, skill_text(good_block(rows=GOOD_ROWS[:3])))
    run("red-duplicate-routed-id", 1, skill_text(good_block(
        rows=GOOD_ROWS[:3] + [("R46-CL2", "duplicate trigger", "order", "1")])))
    run("red-arm-substring", 1, skill_text(good_block(
        rows=[r[:2] + ("order-ish",) + r[3:] for r in GOOD_ROWS])))
    run("red-digest-stale", 1, skill_text(good_block(
        digest=hashlib.sha256(b"substring-arm").hexdigest())))
    run("red-ref-no-selector", 1, skill_text(good_block(
        refs=GOOD_REFS.replace(":20", ""))))
    run("red-ref-outside-allowlist", 1, skill_text(good_block(
        refs=GOOD_REFS.replace("plans/round-47-claims.md:20", "corpus/QUALITY.md:3"))))
    run("red-pin-mismatch", 1, skill_text(good_block(pin="0" * 64)))
    run("red-malformed-heading-is-exit-2", 2, skill_text(
        good_block(), heading="## Queue-drain craft"))
    gate_body = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "..", "round-46", "gate.py")).read()
    swapped = gate_body.replace(ORDER, REVERSED, 1)
    run("red-flag-order-swapped", 1, skill_text(good_block()),
        overrides={"tools/round-46/gate.py": swapped})
    run("red-battery-green-forgery", 1, skill_text(good_block(
        rows=[r[:2] + ("order-ish",) + r[3:] for r in GOOD_ROWS])))

    # the battery itself, on the genuine block: 4 forgeries, v2 green on all, v3 red on all
    files = {"SKILL.md": skill_text(good_block()),
             "plans/round-47-claims.md": CLAIMS_BODY,
             "corpus/lessons/round-46.md": "lesson line\n" * 240,
             "tools/round-47/exact.py": open(__file__).read(),
             "tools/round-46/gate.py": open(os.path.join(
                 os.path.dirname(os.path.abspath(__file__)), "..", "round-46",
                 "gate.py")).read()}
    d = None
    try:
        d, rev = _repo(files, root, prefix="battery-")
        bat = run_battery(d, rev, root)
        ok = (bat.get("forgeries_total") == 4 and bat.get("v2_green") == 4
              and bat.get("v3_green") == 0 and bat.get("genuine_green") == 1
              and bat.get("crash") == 0)
    except Exception as exc:  # noqa: BLE001
        ok, bat = False, {"error": f"{type(exc).__name__}: {exc}"}
    finally:
        if d:
            shutil.rmtree(d, ignore_errors=True)
    cases.append({"case": "battery-discriminates", "expect": True, "got": bool(ok),
                  "ok": bool(ok), "failing": None if ok else bat})

    failures = [c for c in cases if not c["ok"]]
    print("EXACT_SELFTEST: cases=%d failures=%d" % (len(cases), len(failures)))
    print(json.dumps({"cases": cases, "failures": len(failures)}, indent=1))
    shutil.rmtree(root, ignore_errors=True)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
