#!/usr/bin/env python3
"""Seventh batch: a coherent crash control/mutant pair on green fixtures at the lane HEAD."""
import json, os, re, shutil, sys
sys.path.insert(0, "/fast/scratch/hyaku/kaidoku-r47/MutExitCodes")
import drive2 as D
from drive2 import sh, repo, put, commit, S, run, LANE, lane_show, green_c2

HEAD = sh(["git", "-C", LANE, "rev-parse", "HEAD"]).stdout.strip()
REF = re.compile(r"((?:corpus|plans|tools)/[A-Za-z0-9._/-]+)(?::(\d+)(?:-(\d+))?)?")

def c1_green():
    skill = lane_show(HEAD, "SKILL.md")
    files = {"SKILL.md": skill,
             "plans/round-47-claims.md": lane_show(HEAD, "plans/round-47-claims.md"),
             "tools/round-47/exact.py": lane_show(HEAD, "tools/round-47/exact.py"),
             "tools/round-46/gate.py": lane_show(HEAD, "tools/round-46/gate.py")}
    craft = skill.split("## Queue-drain craft ", 1)[1].split("\n## ", 1)[0]
    for name, _, _ in REF.findall(craft):
        if name not in files and os.path.isfile(os.path.join(LANE, name)):
            body = lane_show(HEAD, name)
            if body is not None:
                files[name] = body
    d = repo("g1green", files)
    rev = commit(d, "green c1 fixture")
    return d, rev

def main():
    d, rev = c1_green()
    C1 = os.path.join(d, "tools/round-47/exact.py")
    base = run("c1-crash-control-HEAD", ["python3", "-I", "-B", C1, "--root", d,
                                        "--freeze", rev, "--rev", rev, "--no-battery"], 0,
               "green fixture, unmutated counter (rev=%s)" % rev[:8])
    # mutants run from OUTSIDE the frozen dir, with freeze == rev, so the frozen-path arm
    # cannot pre-empt the crash (the executed file need not live under --root).
    mut = os.path.join(S, "mut")
    os.makedirs(os.path.join(mut, "tools/round-47"), exist_ok=True)
    os.makedirs(os.path.join(mut, "tools/round-46"), exist_ok=True)
    shutil.copy(os.path.join(LANE, "tools/round-46/gate.py"),
                os.path.join(mut, "tools/round-46/gate.py"))
    original = open(os.path.join(d, "tools/round-47/exact.py")).read()
    for name, mutate, expect, note in (
        ("score-runtimeerror",
         lambda b: b.replace("def score(skill, files, profile, rev, battery=None):\n",
                            "def score(skill, files, profile, rev, battery=None):\n"
                            '    raise RuntimeError("injected-crash")\n', 1), 2,
         "Exception inside the scored path"),
        ("score-memoryerror",
         lambda b: b.replace("def score(skill, files, profile, rev, battery=None):\n",
                            "def score(skill, files, profile, rev, battery=None):\n"
                            '    raise MemoryError("injected")\n', 1), 2,
         "an Exception subclass the guard must catch"),
        ("keyboardinterrupt",
         lambda b: b.replace("def score(skill, files, profile, rev, battery=None):\n",
                            "def score(skill, files, profile, rev, battery=None):\n"
                            '    raise KeyboardInterrupt("injected")\n', 1), 2,
         "BaseException: outside main_guard's except Exception"),
        ("emit-unserialisable",
         lambda b: b.replace('    gate.emit(receipt, out)\n',
                            '    receipt["unserialisable"] = {1, 2}\n'
                            '    gate.emit(receipt, out)\n', 1), 2,
         "crash after main_guard, inside gate.emit"),
    ):
        body = mutate(original)
        assert body != original, name
        target = os.path.join(mut, "tools/round-47/exact.py")
        open(target, "w").write(body)
        run("c1-crash-" + name, ["python3", "-I", "-B", target, "--root", d,
                                 "--freeze", rev, "--rev", rev, "--no-battery"], expect, note)

    d2, base2, land2 = green_c2()
    C2 = os.path.join(d2, "tools/round-47/record.py")
    run("c2-crash-control-green", ["python3", "-I", "-B", C2, "--root", d2, "--rev", land2,
                                   "--no-battery"], 0, "green fixture, unmutated counter")
    for name, needle, repl, expect, note in (
        ("evaluate-text-runtimeerror", "def evaluate_text(card, files, root, rev, battery=None):\n",
         "def evaluate_text(card, files, root, rev, battery=None):\n"
         '    raise RuntimeError("injected-crash")\n', 2, "Exception inside the scored path"),
        ("post-guard-emit", None, None, 2, "crash after main_guard, inside gate.emit"),
    ):
        dd = os.path.join(S, "g2c-" + name + "-" + os.urandom(3).hex())
        os.makedirs(dd)
        sh(["git", "-C", dd, "clone", "-q", d2, "."], check=True)
        for k, v in (("user.email", "fx@round47"), ("user.name", "r47 fixture")):
            sh(["git", "-C", dd, "config", k, v], check=True)
        body = open(os.path.join(dd, "tools/round-47/record.py")).read()
        if needle:
            body = body.replace(needle, repl, 1)
        else:
            body = body.replace('    receipt["rev"] = tip\n',
                                '    receipt["rev"] = tip\n    receipt["bad"] = {1, 2}\n', 1)
        put(dd, {"tools/round-47/record.py": body})
        r = commit(dd, "mutant " + name)
        run("c2-crash-" + name, ["python3", "-I", "-B",
                                 os.path.join(dd, "tools/round-47/record.py"), "--root", dd,
                                 "--rev", r, "--no-battery"], expect, note)

main()

with open(os.path.join(S, "receipts7.jsonl"), "w") as fh:
    for x in D.OUT:
        fh.write(json.dumps(x) + "\n")
