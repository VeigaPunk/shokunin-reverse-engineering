#!/usr/bin/env python3
"""R45W2C2Rerun: exact-equality attack on tools/round-45/c2-counter.py."""
import json
import os
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = "/fast/scratch/hyaku/kaidoku-r45/R45W2C2Rerun"
COUNTER = os.path.join(LANE, "tools/round-45/c2-counter.py")
SCOPE_REL = "tools/round-45/registry-scope.json"
CLAIMS_REL = "plans/round-45-claims.md"


def run(args, cwd=None):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)


def git(d, *a):
    return run(["git", "-C", d, *a])


def new_fixture(name):
    d = os.path.join(S, "fx-" + name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    r = git(d, "init", "-q")
    assert r.returncode == 0, r.stderr
    top = git(d, "rev-parse", "--show-toplevel").stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(d), (top, d)
    git(d, "config", "user.email", "w2c2@rerun")
    git(d, "config", "user.name", "w2c2 rerun")
    # byte-copy the lane artefacts the counter reads
    skill = open(os.path.join(LANE, "SKILL.md")).read()
    scope = open(os.path.join(LANE, SCOPE_REL)).read()
    claims = open(os.path.join(LANE, CLAIMS_REL)).read()
    for rel, text in (("SKILL.md", skill), (SCOPE_REL, scope), (CLAIMS_REL, claims)):
        full = os.path.join(d, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, "w").write(text)
    # tools/round-45/real files needed only if a case writes there
    os.makedirs(os.path.join(d, "tools/round-45"), exist_ok=True)
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", "freeze")
    f1 = git(d, "rev-parse", "HEAD").stdout.strip()
    return d, f1


def commit(d, msg):
    git(d, "add", "-A")
    r = git(d, "commit", "-q", "-m", msg)
    assert r.returncode == 0, r.stderr
    return git(d, "rev-parse", "HEAD").stdout.strip()


def write(d, rel, text):
    full = os.path.join(d, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w").write(text)


ROW_44C1 = "| `tools/round-44/c1-counter.py` |"
ROW_44C1_FULL = ("| `tools/round-44/c1-counter.py` | gate \u2014 R44-C1 coverage on four committed "
                 "unblob v1/v2 fixtures | `0` met; `1` not met; `2` could-not-evaluate | "
                 "`--selftest` | x | y | kaidoku |")


def score(d, f1, f2, tag):
    out = os.path.join(S, "score-" + tag + ".json")
    r = run([sys.executable, "-I", "-B", COUNTER, "--root", d, "--freeze", f1,
             "--rev", f2, "--json-out", out], cwd=S)
    rec = json.load(open(out)) if os.path.exists(out) else {}
    return {"tag": tag, "exit": r.returncode, "stdout_sha256":
            __import__("hashlib").sha256(r.stdout.encode()).hexdigest(),
            "stderr": r.stderr.strip()[:400],
            "registered": rec.get("registered"), "unregistered": rec.get("unregistered"),
            "thin": rec.get("thin"), "scope_size": rec.get("scope_size"),
            "registry_rows": rec.get("registry_rows"),
            "failing": rec.get("failing"),
            "verdict": rec.get("verdict"), "reason": rec.get("reason")}


def case(name, mutate, tag=None):
    d, f1 = new_fixture(name)
    mutate(d)
    f2 = commit(d, "mutate: " + name)
    return score(d, f1, f2, tag or name)


# --- cases -----------------------------------------------------------------
def suffix_only(d):
    """A1: first cell becomes the leaf suffix `c1-counter.py` (assignment's test)."""
    skill = open(os.path.join(d, "SKILL.md")).read()
    assert ROW_44C1 in skill
    skill = skill.replace(ROW_44C1, "| `c1-counter.py` |", 1)
    write(d, "SKILL.md", skill)


def suffix_underscore_prefix(d):
    """A2: suffix keeps a `tools/`-less dir: `round-44/c1-counter.py`."""
    skill = open(os.path.join(d, "SKILL.md")).read()
    skill = skill.replace(ROW_44C1, "| `round-44/c1-counter.py` |", 1)
    write(d, "SKILL.md", skill)


def superstring(d):
    """B: first cell is the scope path plus a `.bak` extension."""
    skill = open(os.path.join(d, "SKILL.md")).read()
    skill = skill.replace(ROW_44C1, "| `tools/round-44/c1-counter.py.bak` |", 1)
    write(d, "SKILL.md", skill)


def junk_prefix(d):
    """C: first cell is NOT the path: `x/tools/round-44/c1-counter.py`."""
    skill = open(os.path.join(d, "SKILL.md")).read()
    skill = skill.replace(ROW_44C1, "| `x/tools/round-44/c1-counter.py` |", 1)
    write(d, "SKILL.md", skill)


def absolute_prefix(d):
    """D: first cell is an absolute path ending in the scope path."""
    skill = open(os.path.join(d, "SKILL.md")).read()
    skill = skill.replace(ROW_44C1, "| `/repo/tools/round-44/c1-counter.py` |", 1)
    write(d, "SKILL.md", skill)


def deeper_dir(d):
    """E: same leaf name in a deeper dir: `tools/round-44/deep/c1-counter.py`."""
    skill = open(os.path.join(d, "SKILL.md")).read()
    skill = skill.replace(ROW_44C1, "| `tools/round-44/deep/c1-counter.py` |", 1)
    write(d, "SKILL.md", skill)


def duplicate_thin_after(d):
    """F: good row kept, a second row for the same path with a bare 'non-zero' cell added."""
    skill = open(os.path.join(d, "SKILL.md")).read()
    anchor = "| tools | gate or probe | verdict map (exit codes) | self-test command |"
    idx = skill.index(anchor)
    eol = skill.index("\n", idx) + 1
    # insert duplicate directly after the table header+separator block
    sep_eol = skill.index("\n", eol) + 1
    dup = ("| `tools/round-44/c1-counter.py` | gate \u2014 duplicate | non-zero on failure | "
           "none | x | y | kaidoku |\n")
    skill = skill[:sep_eol] + dup + skill[sep_eol:]
    write(d, "SKILL.md", skill)


def duplicate_thin_before(d):
    """G: the thin duplicate comes first; the good row stays after it."""
    skill = open(os.path.join(d, "SKILL.md")).read()
    anchor = "| tools | gate or probe | verdict map (exit codes) | self-test command |"
    idx = skill.index(anchor)
    eol = skill.index("\n", idx) + 1
    sep_eol = skill.index("\n", eol) + 1
    dup = ("| `tools/round-44/c1-counter.py` | gate \u2014 duplicate | non-zero on failure | "
           "none | x | y | kaidoku |\n")
    skill = skill[:sep_eol] + dup + skill[sep_eol:]
    # remove the original (good) row
    skill = skill.replace(ROW_44C1_FULL + "\n", "", 1)
    write(d, "SKILL.md", skill)


def row_outside_registry(d):
    """H: the row exists only in a non-registry table (under ## Sources)."""
    skill = open(os.path.join(d, "SKILL.md")).read()
    skill = skill.replace(ROW_44C1_FULL + "\n", "", 1)
    skill += ("\n## Sources\n\n| source | note |\n|---|---|\n"
              "| `tools/round-44/c1-counter.py` | `0` met; `1` not met; `2` unevaluable |\n")
    write(d, "SKILL.md", skill)


def touch_tools45_after_freeze(d):
    """I: a commit inside tools/round-45/ after the freeze (directory-freeze arm)."""
    write(d, "tools/round-45/new-instrument.py", "print('late')\n")


def touch_tools45_nested(d):
    """J: nested write inside tools/round-45/ after the freeze."""
    write(d, "tools/round-45/sub/deep.py", "print('late')\n")


def exit_cell_wrong_column(d):
    """K: a scope row moved into a 5-column legacy table where cells[2] is `command`."""
    skill = open(os.path.join(d, "SKILL.md")).read()
    skill = skill.replace(ROW_44C1_FULL + "\n", "", 1)
    legacy = ("\n| tool | purpose | command | exit codes | selftest |\n|---|---|---|---|---|\n"
              "| `tools/round-44/c1-counter.py` | gate | `python3 -I -B tools/round-44/"
              "c1-counter.py --selftest` | `0` met; `1` not met; `2` unevaluable | x |\n")
    skill += legacy
    write(d, "SKILL.md", skill)


CASES = [
    ("A1-suffix-leaf", suffix_only),
    ("A2-suffix-no-tools", suffix_underscore_prefix),
    ("B-superstring-bak", superstring),
    ("C-junk-prefix", junk_prefix),
    ("D-absolute-prefix", absolute_prefix),
    ("E-deeper-dir", deeper_dir),
    ("F-dup-thin-after", duplicate_thin_after),
    ("G-dup-thin-before", duplicate_thin_before),
    ("H-row-outside-registry", row_outside_registry),
    ("I-touch-tools45", touch_tools45_after_freeze),
    ("J-touch-tools45-nested", touch_tools45_nested),
    ("K-exit-cell-wrong-column", exit_cell_wrong_column),
]

results = []
for name, fn in CASES:
    try:
        results.append(case(name, fn))
    except Exception as exc:
        results.append({"tag": name, "error": "%s: %s" % (type(exc).__name__, exc)})
print(json.dumps(results, indent=1, sort_keys=True))
