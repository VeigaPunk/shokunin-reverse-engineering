#!/usr/bin/env python3
"""R45-C1 falsification harness. Runs the FROZEN c1-counter.py (byte-identical copy)
against fixture repos that vary one clause at a time."""
import hashlib
import json
import os
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/kaidoku-r45/R45W1CritC1"
COUNTER = os.path.join(S, "counter.py")
REAL_PREFLIGHT = open(os.path.join(S, "preflight-real.py")).read()
STUB = ("#!/usr/bin/env python3\n"
        "import sys\n"
        "print('PREFLIGHT_SELFTEST: cases=11 failures=0')\n"
        "sys.exit(0)\n")
MARK = "<!-- freeze-integrity-table v1 -->"
PRE = "tools/round-45/frozen-path-preflight.py"
HEAD = "# SKILL\n\n## Queue-drain craft (test)\n\n"
HDR = "| trigger | arm | exit | receipt |\n|---|---|---|---|\n"
GOOD_ROW = "| post-freeze commit touches a frozen path | commit arm | 1 | `--json-out` receipt |\n"
GARBAGE_ROWS = "".join("| lorem %d | ipsum | %d | dolor |\n" % (i, i % 3) for i in range(8))
REFS4 = ("\n  Refs: corpus/lessons/round-44.md, plans/round-45-claims.md, "
         "corpus/lessons/round-44-verifier-spotcheck.md, "
         "corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md\n\n")


def git(d, *a):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True)


def commit(d, msg):
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", msg)
    return git(d, "rev-parse", "HEAD").stdout.strip()


def write(d, p, t):
    full = os.path.join(d, p)
    os.makedirs(os.path.dirname(full) or d, exist_ok=True)
    with open(full, "w") as fh:
        fh.write(t)


def plain(n):
    return "".join("- **%d. Plain rule %d.** body\n" % (i, i) for i in range(1, n + 1))


def block(rows, refs=REFS4, marker=True, label="22"):
    b = "- **%s. Freeze integrity.** %s S140 %s\n\n" % (label, MARK if marker else "", PRE)
    b += HDR + rows + refs
    return b


def repo(d, skill, preflight=REAL_PREFLIGHT, heading="## Queue-drain craft (test)", extra=None):
    git(d, "init", "-q")
    git(d, "config", "user.email", "a@fixture")
    git(d, "config", "user.name", "fixture")
    if heading:
        skill = skill.replace("## Queue-drain craft (test)", heading)
    write(d, "SKILL.md", skill)
    write(d, PRE, preflight)
    write(d, "corpus/lessons/round-44.md", "l1\n" * 60)
    write(d, "corpus/lessons/round-44-verifier-spotcheck.md", "s1\n" * 40)
    write(d, "corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md", "k1\n" * 30)
    write(d, "plans/round-45-claims.md", "claims\n" * 10)
    if extra:
        for p, t in extra.items():
            write(d, p, t)
    return commit(d, "freeze")


def score(d, freeze, rev):
    env = dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S)
    p = subprocess.run([sys.executable, "-I", "-B", COUNTER, "--root", d,
                        "--freeze", freeze, "--rev", rev],
                       capture_output=True, text=True, env=env, timeout=600)
    out = p.stdout.strip()
    try:
        r = json.loads(out.splitlines()[-1]) if out else {}
    except Exception:
        r = {}
    return p.returncode, r, p.stderr.strip().splitlines()[-3:]


RESULTS = []


def record(name, expect, d, code, r, err, note=""):
    RESULTS.append({
        "attack": name,
        "expected_if_sound": expect,
        "observed_exit": code,
        "met_target": r.get("met_target"),
        "rule_blocks": r.get("rule_blocks"),
        "block22_present": r.get("block22_present"),
        "block22_rows": r.get("block22_rows"),
        "block22_refs": r.get("block22_refs"),
        "unresolved": r.get("block22_unresolved_citations"),
        "header_ok": r.get("block22_header_ok"),
        "selftest": r.get("preflight_selftest"),
        "failing": r.get("failing"),
        "stderr_tail": err,
        "note": note,
    })
    print(json.dumps(RESULTS[-1], sort_keys=True))


def run(name, expect, fn):
    d = os.path.join(S, "fx-" + name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    try:
        code, r, err = fn(d)
    except Exception as exc:
        code, r, err = "harnes-crash", {"e": repr(exc)}, []
    record(name, expect, d, code, r, err)


# 1 do-nothing SKILL.md
def a1(d):
    f = repo(d, HEAD + plain(21))
    return score(d, f, f)


# 2 garbage dataframe rows that answer nothing
def a2(d):
    f = repo(d, HEAD + plain(21) + block(GARBAGE_ROWS))
    return score(d, f, f)


# 3a label/number irrelevant + unrelated bullets make the count
def a3a(d):
    txt = HEAD + plain(20) + "- **scratch note.** unrelated bullet\n" + block(GOOD_ROW * 8, label="7") + "- **another note.** also unrelated\n"
    f = repo(d, txt)
    return score(d, f, f)


# 3b header substring cheat
def a3b(d):
    b = ("- **22. Freeze integrity.** " + MARK + " S140 " + PRE + "\n\n"
         "| triggered | harm | exits | receipts |\n|---|---|---|---|\n" + GARBAGE_ROWS + REFS4)
    f = repo(d, HEAD + plain(21) + b)
    return score(d, f, f)


# 3c inflation of the denominator breaks a genuine block
def a3c(d):
    f = repo(d, HEAD + plain(22) + block(GOOD_ROW * 8))
    return score(d, f, f)


# 4 four refs that resolve but say nothing about freeze integrity
def a4(d):
    refs = ("\n  Refs: corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:1-2, "
            "corpus/lessons/round-44.md:1-1, corpus/lessons/round-44-verifier-spotcheck.md:39, "
            "plans/round-45-claims.md:2-3\n\n")
    f = repo(d, HEAD + plain(21) + block(GOOD_ROW * 8, refs=refs))
    return score(d, f, f)


# 4b citation loop: four self-references to the claims file
def a4b(d):
    refs = ("\n  Refs: plans/round-45-claims.md:1, plans/round-45-claims.md:2, "
            "plans/round-45-claims.md:3, plans/round-45-claims.md:4\n\n")
    f = repo(d, HEAD + plain(21) + block(GOOD_ROW * 8, refs=refs))
    return score(d, f, f)


# 5 stub interpreter that prints the expected line
def a5(d):
    f = repo(d, HEAD + plain(21) + block(GOOD_ROW * 8), preflight=STUB)
    return score(d, f, f)


# 6 cheapest green artefact: garbage rows + unrelated refs + stub interpreter
def a6(d):
    refs = ("\n  Refs: corpus/lessons/round-44.md:1, plans/round-45-claims.md:1, "
            "corpus/lessons/round-44-verifier-spotcheck.md:1, "
            "corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:1\n\n")
    f = repo(d, HEAD + plain(21) + block(GARBAGE_ROWS, refs=refs), preflight=STUB)
    return score(d, f, f)


# 7 frozen path touched only by an evil merge commit
def a7(d):
    f = repo(d, HEAD + plain(21) + block(GOOD_ROW * 8))
    write(d, "other.txt", "one\n")
    commit(d, "unrelated")
    git(d, "checkout", "-q", "-b", "side", f)
    write(d, "side.txt", "side\n")
    commit(d, "side change")
    git(d, "checkout", "-q", "master")
    m = git(d, "merge", "--no-ff", "--no-commit", "side")
    with open(os.path.join(d, "tools/round-45/frozen-path-preflight.py"), "a") as fh:
        fh.write("# evil merge append\n")
    with open(os.path.join(d, "plans/round-45-claims.md"), "a") as fh:
        fh.write("evil merge append\n")
    merge_rev = commit(d, "merge side")
    visible = git(d, "log", "--name-only", "--format=", f + ".." + merge_rev,
                  "--", "plans/round-45-claims.md", "tools/round-45")
    code, r, err = score(d, f, merge_rev)
    r["_counter_git_log_sees"] = visible.stdout.strip()
    r["_preflight_first_parent"] = subprocess.run(
        [sys.executable, "-I", "-B", os.path.join(d, PRE), "--root", d, "--freeze", f,
         "--rev", merge_rev, "--pathspec", "tools/round-45/",
         "--freeze-path", "tools/round-45", "--require-pathspec"],
        capture_output=True, text=True, env=dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S)).returncode
    return code, r, err


# 8 heading variant -> uncaught exception
def a8(d):
    f = repo(d, HEAD + plain(21) + block(GOOD_ROW * 8),
             heading="## Queue-drain craft")
    return score(d, f, f)


run("a1-do-nothing", 1, a1)
run("a2-garbage-rows", 1, a2)
run("a3a-unrelated-bullets", 1, a3a)
run("a3b-header-substring", 1, a3b)
run("a3c-inflated-denominator", 0, a3c)
run("a4-irrelevant-refs", 1, a4)
run("a4b-self-citation", 1, a4b)
run("a5-stub-interpreter", 1, a5)
run("a6-cheapest-green", 1, a6)
run("a7-evil-merge", 2, a7)
run("a8-heading-crash", 2, a8)

with open(os.path.join(S, "attacks-results.json"), "w") as fh:
    json.dump(RESULTS, fh, indent=1, sort_keys=True)
print("\nSUM", sum(1 for r in RESULTS if r["observed_exit"] == r["expected_if_sound"]), "/", len(RESULTS))
