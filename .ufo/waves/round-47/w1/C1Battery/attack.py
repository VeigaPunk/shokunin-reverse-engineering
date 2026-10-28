#!/usr/bin/env python3
"""C1Battery — independent build and score of the four R47-C1 forgery classes.

This harness does NOT import tools/round-47/exact.py. It
  1. captures the candidate block 24 from the lane worktree (read-only),
  2. builds one-commit git fixtures in scratch, each carrying exactly one defect class,
  3. scores every fixture with the frozen counter under --profile v2 and --profile v3,
  4. re-derives the claimed clauses from the fixture bytes with its own reader,
  5. records command / exit / stdout sha256 / UTC for every run.

Adds three escape probes and two controls beyond the four named classes.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
FREEZE = "5017e1f7299c3a812e87e7950148f54313dd279e"
S = "/fast/scratch/hyaku/kaidoku-r47/C1Battery"
GEN = os.path.join(S, "gen")
OUT = os.path.join(S, "out")
COUNTER = os.path.join(LANE, "tools/round-47/exact.py")
SKILL_CAP = os.path.join(GEN, "SKILL.candidate.md")

# The twenty-one vocabularies/constants the counter uses, restated here from the CLAIMS
# FILE text (plans/round-47-claims.md R47-C1 predicate), not imported from exact.py.
VOCAB = ("symbol", "once", "digest", "order")
ROUTED = ["R46-CL2", "R46-CL3", "R46-CL4", "R46-CL6"]
HEADER = ["trigger", "v2 hole", "v3 arm", "exit"]
MARKER = "<!-- exactness-table v3 -->"
ORDER = '"-m", "--diff-merges=first-parent"'
REVERSED = '"--diff-merges=first-parent", "-m"'
REF = re.compile(r"((?:corpus|plans|tools)/[A-Za-z0-9._/-]+)(?::(\d+)(?:-(\d+))?)?")
SELF = "tools/round-47/exact.py"
MUST_CITE = "corpus/lessons/round-46.md"
MUT_NAMES = ["substring-arm", "duplicate-routed-id", "stale-mutations-digest",
             "flag-order-drift"]
MUT_DIGEST = hashlib.sha256("\n".join(MUT_NAMES).encode()).hexdigest()
FIXTURE_PATHS = ("plans/round-47-claims.md", "tools/round-47/exact.py",
                 "tools/round-46/gate.py", "corpus/lessons/round-46.md",
                 "corpus/lessons/round-45.md")


def utc():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def git(root, *args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True, text=True)


def show(rev, path):
    r = git(LANE, "show", f"{rev}:{path}")
    return r.stdout if r.returncode == 0 else None


# --- block extraction / table editing -------------------------------------------

def extract_block(skill, num="24. "):
    lines = skill.splitlines(keepends=True)
    start = next(i for i, l in enumerate(lines) if l.startswith("- **" + num))
    end = start
    while end + 1 < len(lines) and not lines[end + 1].startswith("- **") \
            and not lines[end + 1].startswith("## "):
        end += 1
    while lines[end].strip() == "":
        end -= 1
    return "".join(lines[start:end + 1])


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def table_span(block):
    lines = block.splitlines()
    idx = [i for i, l in enumerate(lines) if l.strip().startswith("|")]
    return lines, idx[0], idx[-1]


def map_rows(block, fn):
    lines, start, end = table_span(block)
    data = fn([cells(l) for l in lines[start + 2:end + 1]])
    body = [lines[start], lines[start + 1]] + ["| " + " | ".join(r) + " |" for r in data]
    return "\n".join(lines[:start] + body + lines[end + 1:])


# --- the mutations, written here, independently of exact.py ---------------------

def m_substring_arm(block):
    """Every arm cell is a superstring of a vocabulary token, never equal to one."""
    sup = {"symbol": "symbols", "once": "once-over", "digest": "digest-pin",
           "order": "ordering"}
    return map_rows(block, lambda rows: [r[:2] + [sup[r[2].strip("` ")]] + r[3:]
                                         for r in rows])


def m_duplicate_routed_id(block):
    """Five rows; R46-CL3 named twice; all four ids still present."""
    def fn(rows):
        return rows + [["R46-CL3", "a second row claiming the once defect",
                        "once", "1"]]
    return map_rows(block, fn)


def m_stale_mutations_digest(block):
    """The pin is a digest over three of the four names (a different three from the
    counter's own slice, to prove the check is not keyed to its arithmetic)."""
    stale = hashlib.sha256("\n".join([MUT_NAMES[0], MUT_NAMES[1], MUT_NAMES[3]])
                           .encode()).hexdigest()
    assert stale != MUT_DIGEST
    return re.sub(r"mutations_sha256:[0-9a-f]{64}", "mutations_sha256:" + stale,
                  block, count=1)


def m_blobberish_arm(block):
    """The claims file's kill-rule literal: `blobberish` in a v3-arm cell."""
    return map_rows(block, lambda rows: [r[:2] + ["blobberish"] + r[3:]
                                         for r in rows[:1]] + rows[1:])


def m_arm_permutation(block):
    """Same four tokens, rotated one row: every cell is a vocabulary member, no cell is
    the arm its own trigger row requires."""
    perms = ["`digest`", "`symbol`", "`order`", "`once`"]
    return map_rows(block, lambda rows: [r[:2] + [perms[i]] + r[3:]
                                        for i, r in enumerate(rows)])


def m_citation_vacuity(block):
    """Every citation replaced by the same two-line span of the must-cite lesson."""
    return re.sub(r"((?:corpus|plans)/[A-Za-z0-9._/-]+:\d+(?:-\d+)?)",
                  "corpus/lessons/round-46.md:1-2", block)


def m_digest_reorder(block):
    """Control: the same four names in a different order must break the pin."""
    other = hashlib.sha256("\n".join(reversed(MUT_NAMES)).encode()).hexdigest()
    assert other != MUT_DIGEST
    return re.sub(r"mutations_sha256:[0-9a-f]{64}", "mutations_sha256:" + other,
                  block, count=1)


MUTATIONS = [
    ("substring-arm", "block", m_substring_arm),
    ("duplicate-routed-id", "block", m_duplicate_routed_id),
    ("stale-mutations-digest", "block", m_stale_mutations_digest),
    ("flag-order-drift", "gate", None),
    ("blobberish-arm", "block", m_blobberish_arm),
    ("arm-permutation", "block", m_arm_permutation),
    ("citation-vacuity", "block", m_citation_vacuity),
    ("cardinality-only", "block",
     lambda b: map_rows(b, lambda rows: [(["R46-CL2"] + r[1:]) if i == 1 else r
                                         for i, r in enumerate(rows)])),
    ("digest-reorder", "block", m_digest_reorder),
    ("mutations-name-removed", "block",
     lambda b: b.replace("`flag-order-drift`", "the fourth class", 1)),
    # controls: a change that is NOT the defect must leave v3 green
    ("block-prose-control", "block",
     lambda b: b.replace("Block 23 stated what makes a freeze claim checkable",
                         "Block 23 stated what makes a freeze claim inspectable", 1)),
    ("gate-comment-control", "gate_comment", None),
]


# --- independent clause reader --------------------------------------------------

def read_clauses(fx, block):
    """Re-derive the R47-C1 clauses from the fixture's own bytes."""
    lines = [l for l in block.splitlines() if l.strip().startswith("|")]
    header, rows = None, []
    for line in lines:
        c = cells(line)
        if all(re.fullmatch(r":?-{2,}:?", x) or x == "" for x in c):
            continue
        if header is None:
            header = c
        else:
            rows.append(c)
    ids = [[m for m in re.findall(r"R46-CL\d+", r[0])] for r in rows]
    counts = {}
    for lst in ids:
        for i in lst:
            counts[i] = counts.get(i, 0) + 1
    arms = [r[2].strip("` ") if len(r) > 2 else None for r in rows]
    gate = open(os.path.join(fx, "tools/round-46/gate.py")).read()
    interp = hashlib.sha256(open(os.path.join(fx, SELF), "rb").read()).hexdigest()
    mpin = re.search(r"mutations_sha256:([0-9a-f]{64})", block)
    ipin = re.search(r"interpreter_sha256:([0-9a-f]{64})", block)
    skills = open(os.path.join(fx, "SKILL.md")).read()
    refs = REF.findall(block)
    bad = []
    for name, first, last in refs:
        if name == SELF:
            continue
        if not name.startswith(("corpus/lessons/", "corpus/knowledge/", "plans/",
                               "tools/round-47/")):
            bad.append(name + ": outside the path set")
            continue
        p = os.path.join(fx, name)
        if not os.path.exists(p):
            bad.append(name + ": absent")
            continue
        n = len(open(p).read().splitlines())
        if not first:
            bad.append(name + ": no selector")
        elif not (1 <= int(first) <= int(last or first) <= n):
            bad.append(f"{name}: {first}-{last or first} outside 1..{n}")
    out = {
        "marker_occurrences": skills.count(MARKER),
        "header": header, "rows": len(rows),
        "row_cells": [len(r) for r in rows],
        "exits": [r[3].strip("` ") if len(r) > 3 else None for r in rows],
        "routed_counts": counts, "ids_per_row": [len(x) for x in ids],
        "arm_tokens": arms, "arms_all_vocab": all(a in VOCAB for a in arms),
        "mutations_sha256": mpin.group(1) if mpin else None,
        "mutations_sha256_expected": MUT_DIGEST,
        "mutations_ok": bool(mpin) and mpin.group(1) == MUT_DIGEST,
        "names_stated": [n for n in MUT_NAMES if n in block],
        "gate_order": gate.count(ORDER), "gate_reversed": gate.count(REVERSED),
        "interpreter_sha256": ipin.group(1) if ipin else None,
        "interpreter_expected": interp,
        "interpreter_ok": bool(ipin) and ipin.group(1) == interp,
        "refs": len(refs), "bad_refs": bad,
        "must_cite": MUST_CITE in [r[0] for r in refs],
    }
    f = []
    if out["marker_occurrences"] != 1:
        f.append("c1-marker")
    if out["header"] != HEADER:
        f.append("c2-header")
    if out["rows"] != 4 or any(n != 4 for n in out["row_cells"]):
        f.append("c3-rows")
    if any(x not in {"0", "1", "2"} for x in out["exits"]):
        f.append("c3-exit")
    if any(n != 1 for n in out["ids_per_row"]):
        f.append("c4-row-id-arity")
    if sorted(counts) != sorted(ROUTED) or set(counts.values()) != {1}:
        f.append("c4-cardinality")
    if not out["arms_all_vocab"]:
        f.append("c5-arm-equality")
    if not out["mutations_ok"]:
        f.append("c6-digest")
    if len(out["names_stated"]) != 4:
        f.append("c6-names")
    if out["gate_order"] != 1 or out["gate_reversed"] != 0:
        f.append("c7-flag-order")
    if out["refs"] < 3 or out["bad_refs"] or not out["must_cite"]:
        f.append("c8-citations")
    if not out["interpreter_ok"]:
        f.append("c8-interpreter-pin")
    out["my_failing"] = f
    return out


# --- fixture construction -------------------------------------------------------

def build(name, skill_text, gate_text):
    d = tempfile.mkdtemp(dir=GEN, prefix="fx-")
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    for k, v in (("user.email", "c1battery@round47"), ("user.name", "C1Battery fixture")):
        subprocess.run(["git", "-C", d, "config", k, v], check=True)
    top = git(d, "rev-parse", "--show-toplevel").stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(d), (top, d)
    files = {"SKILL.md": skill_text}
    for p in FIXTURE_PATHS:
        if p == "tools/round-46/gate.py":
            files[p] = gate_text
        else:
            body = show(FREEZE, p)
            assert body is not None, p
            files[p] = body
    for p, text in files.items():
        full = os.path.join(d, p)
        os.makedirs(os.path.dirname(full) or d, exist_ok=True)
        with open(full, "w") as fh:
            fh.write(text)
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "commit", "-q", "-m", name], check=True)
    rev = git(d, "rev-parse", "HEAD").stdout.strip()
    return d, rev


def run_counter(fx, rev, profile, battery):
    cmd = ["python3", "-I", "-B", COUNTER, "--root", fx, "--freeze", rev, "--rev", rev,
           "--profile", profile]
    if not battery:
        cmd.append("--no-battery")
    env = dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S)
    t = utc()
    r = subprocess.run(cmd, capture_output=True, text=True, env=env)
    sha = hashlib.sha256(r.stdout.encode()).hexdigest()
    tag = f"{os.path.basename(fx)}-{profile}-{'bat' if battery else 'nobat'}"
    path = os.path.join(OUT, tag + ".json")
    with open(path, "w") as fh:
        fh.write(r.stdout)
    rec = {"cmd": " ".join(cmd), "exit": r.returncode, "stdout_sha256": sha,
           "stdout_bytes": len(r.stdout), "stderr": r.stderr[-400:], "utc": t,
           "receipt_path": path}
    try:
        rec["receipt"] = json.loads(r.stdout)
    except ValueError:
        rec["receipt"] = {"unparsable": r.stdout[:400]}
    return rec


def main():
    os.makedirs(OUT, exist_ok=True)
    skill0 = open(SKILL_CAP).read()
    block0 = extract_block(skill0)
    gate0 = show(FREEZE, "tools/round-46/gate.py")
    runs = {"utc": utc(), "freeze": FREEZE, "counter": COUNTER,
            "skill_capture_sha256": hashlib.sha256(skill0.encode()).hexdigest(),
            "block_sha256": hashlib.sha256(block0.encode()).hexdigest(),
            "mutations_sha256": MUT_DIGEST, "fixtures": {}}

    # genuine control: v2, v3 (no battery) and v3 (with the counter's own battery)
    d, rev = build("genuine", skill0, gate0)
    g = {"rev": rev, "dir": d, "clauses": read_clauses(d, block0)}
    g["v2"] = run_counter(d, rev, "v2", False)
    g["v3"] = run_counter(d, rev, "v3", False)
    g["v3_battery"] = run_counter(d, rev, "v3", True)
    runs["fixtures"]["genuine"] = g
    keep = os.path.join(GEN, "keep-genuine")
    os.makedirs(os.path.join(keep, "tools/round-46"), exist_ok=True)
    shutil.copyfile(os.path.join(d, "SKILL.md"), os.path.join(keep, "SKILL.md"))
    shutil.copyfile(os.path.join(d, "tools/round-46/gate.py"),
                    os.path.join(keep, "tools/round-46/gate.py"))

    for name, target, fn in MUTATIONS:
        block, gate = block0, gate0
        if target == "block":
            block = fn(block0)
            skill = skill0.replace(block0, block, 1)
            assert skill != skill0
        elif target == "gate":
            assert gate0.count(ORDER) == 1 and gate0.count(REVERSED) == 0
            gate = gate0.replace(ORDER, REVERSED, 1)
            skill = skill0
        else:
            assert gate0.count(ORDER) == 1
            gate = gate0 + "\n# a control change that is not the flag order\n"
            skill = skill0
        d, rev = build(name, skill, gate)
        entry = {"rev": rev, "dir": d, "block_changed": block != block0,
                 "gate_changed": gate != gate0,
                 "clauses": read_clauses(d, block)}
        entry["v2"] = run_counter(d, rev, "v2", False)
        entry["v3"] = run_counter(d, rev, "v3", False)
        if name in ("substring-arm", "duplicate-routed-id", "stale-mutations-digest",
                    "flag-order-drift", "arm-permutation", "citation-vacuity",
                    "mutations-name-removed"):
            entry["v3_battery"] = run_counter(d, rev, "v3", True)
        # byte-level isolation evidence
        bdiff = subprocess.run(["diff", "-u", os.path.join(GEN, "keep-genuine", "SKILL.md"),
                                os.path.join(d, "SKILL.md")], capture_output=True,
                               text=True).stdout
        gdiff = subprocess.run(["diff", "-u",
                                os.path.join(GEN, "keep-genuine", "tools/round-46/gate.py"),
                                os.path.join(d, "tools/round-46/gate.py")],
                               capture_output=True, text=True).stdout
        entry["skill_diff_lines"] = len([l for l in bdiff.splitlines()
                                         if l[:1] in "+-" and not l.startswith(("+++", "---"))])
        entry["gate_diff_lines"] = len([l for l in gdiff.splitlines()
                                        if l[:1] in "+-" and not l.startswith(("+++", "---"))])
        open(os.path.join(OUT, f"diff-{name}.skill.diff"), "w").write(bdiff)
        open(os.path.join(OUT, f"diff-{name}.gate.diff"), "w").write(gdiff)
        runs["fixtures"][name] = entry

    # kill-rule case: block 23's table relabelled `24. ` with the marker appended
    b23 = extract_block(skill0, "23. ")
    relabelled = b23.replace("- **23. ", "- **24. ", 1)
    relabelled = relabelled.replace("<!-- freeze-integrity-table v2 -->",
                                    MARKER, 1)
    d, rev = build("block23-relabelled", skill0.replace(block0, relabelled, 1), gate0)
    e = {"rev": rev, "dir": d, "block_changed": True, "gate_changed": False,
         "clauses": read_clauses(d, relabelled)}
    e["v2"] = run_counter(d, rev, "v2", False)
    e["v3"] = run_counter(d, rev, "v3", False)
    runs["fixtures"]["block23-relabelled"] = e

    with open(os.path.join(OUT, "runs.json"), "w") as fh:
        json.dump(runs, fh, indent=1, sort_keys=True)

    print("class | v2 | v3 | my_failing | counter_v3_failing")
    for name, e in runs["fixtures"].items():
        c3 = e["v3"].get("receipt", {})
        print("%-24s | %s | %s | %s | %s | bat=%s" % (
            name, e["v2"]["exit"], e["v3"]["exit"], e["clauses"]["my_failing"],
            c3.get("failing"), e.get("v3_battery", {}).get("exit")))
    print("genuine v3-with-battery exit:", runs["fixtures"]["genuine"]["v3_battery"]["exit"])
    print("genuine battery:", json.dumps(
        runs["fixtures"]["genuine"]["v3_battery"]["receipt"].get("battery"), indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
