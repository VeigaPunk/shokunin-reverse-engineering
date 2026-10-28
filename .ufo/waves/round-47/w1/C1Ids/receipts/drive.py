#!/usr/bin/env python3
"""Seat C1Ids — R47-C1 clause-4 fixtures over the frozen counter.

Builds one-commit fixture repos from the lane's bytes at HEAD (which still has 23 craft
blocks) plus a candidate block 24, then scores each with the frozen counter at v3.
Every git call names -C <fixture>; the fixture toplevel is asserted before the first commit.
"""
import hashlib
import json
import os
import subprocess
import sys
import time

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = "/fast/scratch/hyaku/kaidoku-r47/C1Ids"
REV = "3186f69b49798f2cc05727bbfd1604505fcee03b"   # HEAD: 23 craft blocks, frozen tools == freeze
FREEZE = "5017e1f7299c3a812e87e7950148f54313dd279e"
COUNTER = os.path.join(LANE, "tools/round-47/exact.py")
MUT = "19a2166e47c5231997063a7bc21a7224dda1aa0773bab9c6ffa80ea453d5a112"
PIN = "dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c"

HEADER = "| trigger | v2 hole | v3 arm | exit |"

INTRO = (
    "- **24. An instrument's binding is an equality, not a containment, and its denominator "
    "is pinned.** <!-- exactness-table v3 --> Block 23 stated what makes a freeze claim "
    "checkable; this one states what makes a *check* exact — one row per defect the round-46 "
    "non-author spot-check routed (`corpus/lessons/round-46.md:57-70`), the v2 binding that "
    "let a forgery pass it, and the v3 arm that fails the forgery. Interpreter pin: "
    "`tools/round-47/exact.py` `interpreter_sha256:%s`; the counter's own mutation list is "
    "pinned as `mutations_sha256:%s` over `substring-arm`, `duplicate-routed-id`, "
    "`stale-mutations-digest`, `flag-order-drift`." % (PIN, MUT))

ROWS = [
    ("R46-CL2 `blobberish` satisfies `blob` in the arm-vocabulary test",
     "the v2 test asks whether any vocabulary token is a substring of the lowercased cell, "
     "so every superstring passes", "symbol", "1"),
    ("R46-CL3 a row claims a routed id another row already addresses",
     "the v2 test asks whether the id appears in some row, so one row can claim a group it "
     "does not address", "once", "1"),
    ("R46-CL4 deleting a mutation changes the denominator the claim is judged on",
     "the v2 counter compares `forgeries_total` with a number it computes itself and pins "
     "nothing, so a deleted mutation passes", "digest", "1"),
    ("R46-CL6 one flag reorder prints a merge twice and blinds the history arm",
     "the v2 profile reads no flag order, so `-m --diff-merges=first-parent` and its "
     "reverse print differently and no clause notices", "order", "1"),
]

REFS = (
    "  Refs: `corpus/lessons/round-46.md:57-70` (the four routed instrument defects this "
    "matrix closes), `corpus/lessons/round-46.md:65-70` (R46-CL6: the flag order is a "
    "convention no clause reads), `corpus/lessons/round-46.md:27-31` (S142 grounds "
    "`-m --diff-merges=first-parent`), `plans/round-47-claims.md:74-75` (the routed-id "
    "cardinality clause this table must satisfy).")


def block(rows=None, header=HEADER, intro=INTRO, refs=REFS):
    rows = ROWS if rows is None else rows
    out = [intro, "", header, "|---|---|---|---|"]
    out += ["| " + " | ".join(r) + " |" for r in rows]
    out += ["", refs]
    return "\n".join(out)


def sub(rows, idx, cell, value):
    rows = [list(r) for r in rows]
    rows[idx][cell] = value
    return [tuple(r) for r in rows]


def landed_draft():
    wt = open(os.path.join(LANE, "SKILL.md")).read()
    head, rest = wt.split("\n## Config custody for live-probe rounds (SOP)", 1)
    body = head.rstrip("\n")
    start = body.rindex("\n- **24. ") + 1
    return body[start:]


def landed_with_rows(rows=None):
    """The worktree draft verbatim, except its four body rows replaced by `rows`."""
    rows = ROWS if rows is None else rows
    lines = landed_draft().splitlines()
    h = next(i for i, l in enumerate(lines) if l.strip() == HEADER)
    tail = lines[h + 6:]          # header, separator, four body rows
    body = ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join(lines[:h + 2] + body + tail)


def run(cmd, cwd=None, env=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=env)
    return r.returncode, r.stdout, r.stderr


def lane_bytes(path):
    code, out, err = run(["git", "-C", LANE, "show", "%s:%s" % (REV, path)])
    if code != 0:
        raise SystemExit("git show %s failed: %s" % (path, err))
    return out


def build(name, block_text):
    d = os.path.join(S, "fx", name)
    subprocess.run(["rm", "-rf", d], check=True)
    os.makedirs(d)
    code, out, err = run(["git", "-C", d, "init", "-q"])
    if code != 0:
        raise SystemExit("git init failed: " + err)
    for k, v in (("user.email", "fixture@round47"), ("user.name", "round47 fixture")):
        run(["git", "-C", d, "config", k, v])
    code, out, _ = run(["git", "-C", d, "rev-parse", "--show-toplevel"])
    if os.path.realpath(out.strip()) != os.path.realpath(d):
        raise SystemExit("fixture toplevel mismatch: %r vs %r" % (out.strip(), d))
    files = {"SKILL.md": lane_bytes("SKILL.md"),
             "plans/round-47-claims.md": lane_bytes("plans/round-47-claims.md"),
             "tools/round-47/exact.py": lane_bytes("tools/round-47/exact.py"),
             "tools/round-46/gate.py": lane_bytes("tools/round-46/gate.py"),
             "corpus/lessons/round-46.md": lane_bytes("corpus/lessons/round-46.md")}
    head, tail = files["SKILL.md"].split(
        "\n## Config custody for live-probe rounds (SOP)", 1)
    files["SKILL.md"] = (head.rstrip("\n") + "\n\n" + block_text + "\n\n## Config custody "
                         "for live-probe rounds (SOP)" + tail)
    for p, text in files.items():
        full = os.path.join(d, p)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as fh:
            fh.write(text)
    for step in (["add", "-A"], ["commit", "-q", "-m", "fixture " + name]):
        code, out, err = run(["git", "-C", d] + step)
        if code != 0:
            raise SystemExit("git %s failed: %s" % (step[0], err))
    code, out, _ = run(["git", "-C", d, "rev-parse", "HEAD"])
    os.makedirs(os.path.join(d, ".ufo"), exist_ok=True)
    return d, out.strip()


def score(name, d, rev):
    env = dict(os.environ, HYAKU_SCRATCH=os.path.join(S, "scratch"), TMPDIR=os.path.join(S, "scratch"))
    os.makedirs(env["HYAKU_SCRATCH"], exist_ok=True)
    out_rel = ".ufo/%s.json" % name
    cmd = [sys.executable, "-I", "-B", COUNTER, "--root", d, "--freeze", rev, "--rev", rev,
           "--json-out", out_rel]
    t = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    code, out, err = run(cmd, cwd=d, env=env)
    skill = lane_bytes_at(d, rev, "SKILL.md")
    rec = {"case": name, "fixture": d, "rev": rev, "utc": t,
           "block_sha256": hashlib.sha256(block_of(skill).encode()).hexdigest(),
           "skill_sha256": hashlib.sha256(skill.encode()).hexdigest(),
           "cmd": " ".join(cmd), "exit": code,
           "stdout_sha256": hashlib.sha256(out.encode()).hexdigest(),
           "stderr": err[-400:] if err else ""}
    try:
        rec.update(json.loads(out))
    except ValueError:
        rec["stdout_head"] = out[:400]
    return rec


def lane_bytes_at(root, rev, path):
    code, out, err = run(["git", "-C", root, "show", "%s:%s" % (rev, path)])
    if code != 0:
        raise SystemExit("git show %s failed: %s" % (path, err))
    return out


def block_of(skill):
    head, _ = skill.split("\n## Config custody for live-probe rounds (SOP)", 1)
    body = head.rstrip("\n")
    return body[body.rindex("\n- **24. ") + 1:]


def main():
    os.makedirs(os.path.join(S, "fx"), exist_ok=True)
    cases = {}
    cases["full"] = block()
    cases["partial-header-digest-ref"] = block(
        header="| trigger | v2 hole | arm | exit |",
        intro=INTRO.replace(MUT, hashlib.sha256(b"substring-arm").hexdigest()),
        refs=REFS.replace("`plans/round-47-claims.md:74-75`", "`corpus/QUALITY.md:3`"))
    cases["dup-id"] = block(rows=sub(ROWS, 1, 0, "R46-CL2 a duplicate trigger cell"))
    cases["multi-id-cell"] = block(rows=sub(ROWS, 1, 0, "R46-CL3 and R46-CL2 in one cell"))
    cases["id-in-hole-cell"] = block(rows=sub(sub(ROWS, 1, 0, "no id in this trigger cell"),
                                              1, 1, "the routed id R46-CL3 moved into the hole cell"))
    cases["permute-ids"] = block(rows=sub(sub(ROWS, 0, 0, ROWS[1][0]), 1, 0, ROWS[0][0]))
    cases["copyrow"] = block(rows=[ROWS[0], (ROWS[1][0], ROWS[0][1], ROWS[0][2], ROWS[0][3]),
                                   (ROWS[2][0], ROWS[0][1], ROWS[0][2], ROWS[0][3]),
                                   (ROWS[3][0], ROWS[0][1], ROWS[0][2], ROWS[0][3])])
    cases["dup-arm"] = block(rows=[r[:2] + ("order",) + r[3:] for r in ROWS])
    cases["one-hole-four-ids"] = block(
        rows=[(r[0], ROWS[0][1], r[2], r[3]) for r in ROWS])
    cases["cite-gate46"] = block(
        refs=REFS.replace("`tools/round-46/gate.py:99`", "") +
        " The order arm reads the argv literal in `tools/round-46/gate.py:99`.")
    cases["landed-worktree-draft"] = landed_draft()
    cases["landed-draft-plus-rows"] = landed_with_rows()

    out = []
    for name, text in cases.items():
        d, rev = build(name, text)
        rec = score(name, d, rev)
        out.append(rec)
        print("%-26s exit=%s failing=%s" % (name, rec["exit"],
              json.dumps(rec.get("failing"))[:300]))
    with open(os.path.join(S, "clause4-receipts.json"), "w") as fh:
        json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()
