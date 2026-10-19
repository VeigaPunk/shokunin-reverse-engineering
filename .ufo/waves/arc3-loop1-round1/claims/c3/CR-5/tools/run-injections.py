#!/usr/bin/env python3
"""CR-5 injection harness: falsifiability probes against a census instrument.

Usage: python3 run-injections.py <census.py> <label>
Runs 6 injections on /dev/shm/cr5/root-before copies, each in its own case dir
under /dev/shm/cr5/cases-<label>/, captures stdout+exit per case.
"""
import os, shutil, subprocess, sys

BASE = "/dev/shm/cr5"
ROOT_BEFORE = os.path.join(BASE, "root-before")


def run_case(name, census, label, mutate=None, env_home=None, root_override=None):
    case = os.path.join(BASE, "cases-%s" % label, name)
    if os.path.exists(case):
        shutil.rmtree(case)
    shutil.copytree(ROOT_BEFORE, case)
    if mutate:
        mutate(case)
    env = dict(os.environ)
    if env_home:
        env["HOME"] = env_home
    root = root_override or case
    p = subprocess.run([sys.executable, census, "--root", root],
                       capture_output=True, text=True, env=env)
    out = p.stdout + p.stderr
    with open(os.path.join(BASE, "cases-%s" % label, name + ".out"), "w") as fh:
        fh.write(out + "\nEXIT=%d\n" % p.returncode)
    tail = [l for l in out.splitlines() if l.startswith(("VERDICT", "SCOPE-ERRORS", "ANCHOR-FAIL"))]
    print("[%s] exit=%d  %s" % (name, p.returncode, " | ".join(tail) or out.strip().splitlines()[-1:]))
    return p.returncode, out


def edit(path, old, new):
    txt = open(path, encoding="utf-8").read()
    assert old in txt, "needle %r not found in %s" % (old[:40], path)
    open(path, "w", encoding="utf-8").write(txt.replace(old, new, 1))


def t1(case):  # false current pin in SKILL.md CURRENT range (line 19 devin/omp pin)
    edit(os.path.join(case, "SKILL.md"), "rea-agents@6.5.0", "rea-agents@6.3.0")


def t2(case):  # undeclared stale locus appended beyond last declared line
    with open(os.path.join(case, "SCORECARD.md"), "a") as fh:
        fh.write("\nThe kimi client remains pinned to rea-agents@6.3.0 for the current round.\n")


def t3(case):  # strip a DATED marker (PROVINCE.md:40)
    edit(os.path.join(case, "PROVINCE.md"), "verified on this host 2026-10-13",
         "verified on this host [marker removed]")


def t4(case):  # anchor failure: empty HOME -> ANCHOR-FAIL exit 2
    pass


def t5(case):  # false current-claim planted inside a DATED range (shelter demo)
    # insert at line 800: inside DATED row 769-855, AFTER both marker lines
    # (704, 769) so the G15 marker assertions are not disturbed.
    lines = open(os.path.join(case, "SCORECARD.md"), encoding="utf-8").read().splitlines()
    lines.insert(800, "Current status: kimi runs rea-agents@6.3.0 as of this round.")
    open(os.path.join(case, "SCORECARD.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")


def t6(case):  # pointer needle outside declared range (ptr class, no pin/bare in unit)
    with open(os.path.join(case, "SCORECARD.md"), "a") as fh:
        fh.write("\nSee ~/.kimi-code/config.toml:9999 for the pointer class check.\n")


def main():
    census, label = sys.argv[1], sys.argv[2]
    os.makedirs(os.path.join(BASE, "cases-%s" % label), exist_ok=True)
    print("== instrument: %s (sha256 %s)" % (census, subprocess.run(
        ["sha256sum", census], capture_output=True, text=True).stdout.split()[0]))
    run_case("t0-baseline", census, label)
    run_case("t1-false-current-pin", census, label, t1)
    run_case("t2-undeclared-append", census, label, t2)
    run_case("t3-marker-strip", census, label, t3)
    run_case("t4-anchor-fail", census, label, t4,
             env_home=os.path.join(BASE, "fakehome"))
    run_case("t5-dated-shelter", census, label, t5)
    run_case("t6-ptr-out-of-range", census, label, t6)


if __name__ == "__main__":
    main()
