#!/usr/bin/env python3
"""Build clause-7 fixtures from the lane's FROZEN bytes (read-only on the lane)."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = "/fast/scratch/hyaku/kaidoku-r47/C1Order"
FREEZE = "5017e1f7299c3a812e87e7950148f54313dd279e"
EXACT = os.path.join(LANE, "tools/round-47/exact.py")
ORDER = '"-m", "--diff-merges=first-parent"'
REVERSED = '"--diff-merges=first-parent", "-m"'

FILES = ["SKILL.md", "plans/round-47-claims.md", "tools/round-47/exact.py",
         "tools/round-46/gate.py", "corpus/lessons/round-46.md",
         "corpus/lessons/round-45.md"]

MUT_DIGEST = hashlib.sha256(
    "\n".join(["substring-arm", "duplicate-routed-id", "stale-mutations-digest",
               "flag-order-drift"]).encode()).hexdigest()


def show(path, rev=FREEZE):
    r = subprocess.run(["git", "-C", LANE, "show", f"{rev}:{path}"],
                       capture_output=True, text=True)
    assert r.returncode == 0, (path, r.stderr)
    return r.stdout


CANDIDATE = """- **24. An exactness binding is an equality, not a containment, and its denominator is pinned.** <!-- exactness-table v3 --> Block 23 stated what makes a freeze claim checkable; this one states what makes a *check* exact. Each row is a defect the round-46 non-author spot-check routed (R46-CL2, R46-CL3, R46-CL4, R46-CL6), the loose binding that let a forgery pass it, and the clause of the round-47 counter that now fails the same forgery. The counter's own mutation list is pinned as `mutations_sha256:%s` over `substring-arm`, `duplicate-routed-id`, `stale-mutations-digest`, `flag-order-drift`; the interpreter is pinned as `interpreter_sha256:%s`.

| trigger | v2 hole | v3 arm | exit |
|---|---|---|---|
| R46-CL2 `blobberish` satisfies `blob` in the arm-vocabulary test | containment over a lowercased cell, so any superstring passes | `symbol` | 1 |
| R46-CL3 a row claims a routed id that another row already addresses | the id check asks whether an id appears in some row, never how many times | `once` | 1 |
| R46-CL4 deleting a mutation changes the denominator the claim is judged on | the forgery count is compared with a number the code computes and nothing pins the list | `digest` | 1 |
| R46-CL6 one flag reorder (moving `-m` after `--diff-merges=first-parent`) prints a merge twice and restores the blindness R45-CL6 closed | the argument order is a convention no clause reads, so the reorder is silent | `order` | 1 |

  Refs: `corpus/lessons/round-46.md:65-70` (R46-CL6, the order-sensitive arm and its round-47 routing), `plans/round-47-claims.md:77-82` (clause 7: the literal present once and the reversed pair zero times), `tools/round-47/exact.py:258-264` (the two counts that fill `gate_order_literal` and `gate_order_reversed`). S142 grounds the arm (`corpus/lessons/round-46.md:29-32`).

""" % (MUT_DIGEST, hashlib.sha256(open(EXACT, "rb").read()).hexdigest())

INSERT_BEFORE = "## Config custody for live-probe rounds (SOP)"


def make_fixture(name, skill, gate_text):
    fx = os.path.join(S, name)
    shutil.rmtree(fx, ignore_errors=True)
    os.makedirs(fx)
    subprocess.run(["git", "-C", fx, "init", "-q"], check=True)
    for k, v in (("user.email", "c1order@round47"), ("user.name", "c1order fixture")):
        subprocess.run(["git", "-C", fx, "config", k, v], check=True)
    top = subprocess.run(["git", "-C", fx, "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True).stdout.strip()
    assert top == fx, (top, fx)
    for p in FILES:
        body = show(p)
        if p == "SKILL.md":
            body = skill
        elif p == "tools/round-46/gate.py":
            body = gate_text
        full = os.path.join(fx, p)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as fh:
            fh.write(body)
    subprocess.run(["git", "-C", fx, "add", "-A"], check=True)
    subprocess.run(["git", "-C", fx, "commit", "-q", "-m", "clause7 fixture"], check=True)
    rev = subprocess.run(["git", "-C", fx, "rev-parse", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    return fx, rev


def insert_block(skill, block):
    assert INSERT_BEFORE in skill, "insertion anchor absent"
    head, tail = skill.split(INSERT_BEFORE, 1)
    return head + block + INSERT_BEFORE + tail


def run(name, fx, rev, profile="v3"):
    out = os.path.join(fx, "receipt.json")
    t0 = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    r = subprocess.run([sys.executable, "-I", "-B", EXACT, "--root", fx,
                        "--freeze", rev, "--rev", rev, "--profile", profile,
                        "--json-out", out], capture_output=True, text=True,
                       cwd=fx, env=dict(os.environ, HYAKU_SCRATCH=S, TMPDIR=S))
    body = open(out).read() if os.path.exists(out) else r.stdout
    d = json.loads(body)
    return {"variant": name, "profile": profile, "exit": r.returncode,
            "utc": t0, "stdout_sha256": hashlib.sha256(r.stdout.encode()).hexdigest(),
            "failing": d.get("failing"), "receipt": d}


if __name__ == "__main__":
    base_skill = show("SKILL.md")
    gate_ok = show("tools/round-46/gate.py")
    assert gate_ok.count(ORDER) == 1 and gate_ok.count(REVERSED) == 0

    skill = insert_block(base_skill, CANDIDATE)
    results = []

    # V1 — candidate block, gate.py as frozen
    fx, rev = make_fixture("fx-v1", skill, gate_ok)
    results.append(run("v1-candidate-gate-clean", fx, rev))

    # V2 — clause 7's own red case: the exact literal swapped
    fx, rev = make_fixture("fx-v2", skill, gate_ok.replace(ORDER, REVERSED, 1))
    results.append(run("v2-gate-order-swapped", fx, rev))

    # V3 — forgery: live argv reversed under a different spacing, correct literal
    #      retained in a docstring line. Textual counts satisfied; argv reversed.
    forged = gate_ok.replace(
        '    r = git(root, "log", "-m", "--diff-merges=first-parent", '
        '"--name-status", "-z",',
        '    r = git(root, "log", "--diff-merges=first-parent","-m", '
        '"--name-status", "-z",', 1)
    assert forged != gate_ok
    forged = forged.replace(
        "Reads Git objects only; never writes inside the repo it measures.",
        'The history arm passes "-m", "--diff-merges=first-parent" so a merge '
        "shows its first-parent diff.\n\nReads Git objects only; never writes "
        "inside the repo it measures.", 1)
    assert forged.count(ORDER) == 1 and forged.count(REVERSED) == 0, (
        forged.count(ORDER), forged.count(REVERSED))
    fx, rev = make_fixture("fx-v3", skill, forged)
    results.append(run("v3-forged-order-in-comment-argv-reversed", fx, rev))

    # V4 — candidate that cites the file clause 7 measures (path outside ALLOW)
    extra = skill.replace(
        "  Refs: `corpus/lessons/round-46.md:65-70`",
        "  Refs: `tools/round-46/gate.py:99` (the arm clause 7 counts), "
        "`corpus/lessons/round-46.md:65-70`", 1)
    assert extra != skill
    fx, rev = make_fixture("fx-v4", extra, gate_ok)
    results.append(run("v4-cites-the-measured-file", fx, rev))

    # V5 — my own row with a substring arm cell, v3 vs v2
    bad = skill.replace("| `order` | 1 |", "| `order-ish` | 1 |", 1)
    assert bad != skill
    fx, rev = make_fixture("fx-v5", bad, gate_ok)
    results.append(run("v5-arm-substring-v3", fx, rev, "v3"))
    results.append(run("v5-arm-substring-v2", fx, rev, "v2"))

    with open(os.path.join(S, "variants.json"), "w") as fh:
        json.dump(results, fh, indent=1, sort_keys=True)
    for r in results:
        print("%-46s %-3s exit=%d failing=%s" % (r["variant"], r["profile"],
                                                 r["exit"], r["failing"]))
