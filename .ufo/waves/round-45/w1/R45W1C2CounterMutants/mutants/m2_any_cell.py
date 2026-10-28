#!/usr/bin/env python3
"""R45-C2 counter: every claim-carrying instrument has a SKILL.md registry row.

Frozen target (plans/round-45-claims.md, R45-C2): over the scope committed in
`tools/round-45/registry-scope.json` — the instruments named by the round-44 and
round-45 frozen claim files —
  unregistered == []   every scope path is the first cell of a SKILL.md registry row
  thin         == []   that row's exit-code cell names 0, 1 and 2 (no bare "non-zero")
  scope_size   == 6    enumerated from the scope file, never from a count

Exit codes: 0 met; 1 not met; 2 could-not-evaluate (unknown revision, freeze not an
ancestor, SKILL.md or the scope file absent, `frozen_path_changed` for a commit inside
FREEZE..REV touching the claims file or `tools/round-45/`).

A row that names a different tool does not satisfy a scope path: the check is exact
path equality, so counting rows cannot reach the target (control: a scratch SKILL.md
with six rows for other paths still reports six unregistered).
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

CLAIMS = "plans/round-45-claims.md"
SCOPE = "tools/round-45/registry-scope.json"
FROZEN = [CLAIMS, "tools/round-45"]
ROW_TOOL = re.compile(r"`(tools/[A-Za-z0-9._/-]+\.(?:py|sh))`")


def git(root, *args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True, text=True)


def show(root, rev, path):
    r = git(root, "show", f"{rev}:{path}")
    return r.stdout if r.returncode == 0 else None


def parse_rows(skill):
    rows = []
    for line in skill.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) < 3:
            continue
        m = ROW_TOOL.search(cells[0])
        if not m:
            continue
        rows.append({"tool": m.group(1), "cells": cells, "line": s})
    return rows


def exits_ok(cell):
    return all(re.search(r"\b%d\b" % d, cell) for d in (0, 1, 2))


def frozen_path_changed(root, freeze, rev):
    log = git(root, "log", "--name-only", "--format=", f"{freeze}..{rev}", "--", *FROZEN)
    if log.returncode != 0:
        return None
    return sorted({p for p in log.stdout.splitlines() if p.strip()})


def evaluate(root, freeze, rev):
    for label, ref in (("freeze", freeze), ("rev", rev)):
        if git(root, "rev-parse", "--verify", ref + "^{commit}").returncode != 0:
            return 2, {"reason": f"unknown {label} revision"}
    base = git(root, "rev-parse", freeze + "^{commit}").stdout.strip()
    tip = git(root, "rev-parse", rev + "^{commit}").stdout.strip()
    if git(root, "merge-base", "--is-ancestor", base, tip).returncode != 0:
        return 2, {"reason": "freeze is not an ancestor of rev"}
    changed = frozen_path_changed(root, base, tip)
    if changed is None:
        return 2, {"reason": "git log failed"}
    if changed:
        return 2, {"reason": "frozen_path_changed", "frozen_path_changed": changed}

    scope_body = show(root, tip, SCOPE)
    if scope_body is None:
        return 2, {"reason": "scope file absent at rev"}
    try:
        scope = json.loads(scope_body)["paths"]
    except (ValueError, KeyError) as exc:
        return 2, {"reason": f"scope file unreadable: {exc}"}
    skill = show(root, tip, "SKILL.md")
    if skill is None:
        return 2, {"reason": "SKILL.md absent at rev"}

    rows = parse_rows(skill)
    by_tool = {}
    for row in rows:
        by_tool.setdefault(row["tool"], row)
    unregistered, thin, registered = [], [], []
    for path in scope:
        row = None  # MUTANT m2: any cell containing the path satisfies it
        for cand in rows:
            if any(path in c for c in cand["cells"]):
                row = cand
                break
        if row is None:
            unregistered.append(path)
            continue
        registered.append(path)
        # cells[2] is the "verdict map (exit codes)" column of the registry table
        if len(row["cells"]) < 3 or not exits_ok(row["cells"][2]):
            thin.append(path)

    reasons = []
    if len(scope) != 6:
        reasons.append(f"scope_size {len(scope)} != 6")
    if unregistered:
        reasons.append(f"unregistered: {unregistered}")
    if thin:
        reasons.append(f"thin exit-code cells: {thin}")

    receipt = {
        "counter": "round-45-c2",
        "freeze": base,
        "rev": tip,
        "scope_size": len(scope),
        "scope": scope,
        "registry_rows": len(rows),
        "registered": registered,
        "unregistered": unregistered,
        "thin": thin,
        "frozen_path_changed": [],
        "met_target": not reasons,
        "failing": reasons,
    }
    return (0 if not reasons else 1), receipt


# --- selftest ---------------------------------------------------------------

SCOPE_TEST = ["tools/round-44/a.py", "tools/round-44/b.sh", "tools/round-44/c.py",
              "tools/round-45/x.py", "tools/round-45/y.py", "tools/round-45/z.py"]


def good_rows():
    out = ""
    for p in SCOPE_TEST:
        out += f"| `{p}` | gate — test | `0` met; `1` not met; `2` unevaluable | `--selftest` |\n"
    return out


def make_repo(d, skill, scope=SCOPE_TEST, claims=True):
    git(d, "init", "-q")
    git(d, "config", "user.email", "c2@selftest")
    git(d, "config", "user.name", "c2 selftest")
    paths = {"SKILL.md": skill,
             SCOPE: json.dumps({"scope": "test", "paths": scope}, indent=1)}
    if claims:
        paths[CLAIMS] = "claims\n" * 10
    for p, text in paths.items():
        full = os.path.join(d, p)
        os.makedirs(os.path.dirname(full) or d, exist_ok=True)
        with open(full, "w") as fh:
            fh.write(text)
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", "freeze")
    return git(d, "rev-parse", "HEAD").stdout.strip()


HEAD = "# SKILL\n\n### Round-44 instrument registry\n\n| tool | gate | exits | selftest |\n|---|---|---|---|\n"


def selftest_scope():
    return SCOPE_TEST


def run_selftest():
    base = os.environ.get("HYAKU_SCRATCH") or os.environ.get("TMPDIR") or tempfile.gettempdir()
    root = os.path.join(base, "kaidoku-r45")
    os.makedirs(root, exist_ok=True)
    workroot = tempfile.mkdtemp(dir=root, prefix="c2-")
    cases = []

    def case(name, expect, fn):
        d = tempfile.mkdtemp(dir=workroot)
        try:
            code, receipt = fn(d)
        except Exception as exc:
            code, receipt = ("crash", {"error": f"{type(exc).__name__}: {exc}"})
        cases.append({"case": name, "expect": expect, "got": code, "ok": code == expect,
                      "receipt": receipt})

    def green(d):
        f = make_repo(d, HEAD + good_rows())
        return evaluate(d, f, f)

    def unregistered(d):
        skill = HEAD + good_rows().replace("| `tools/round-44/c.py` |", "| `tools/round-44/other.py` |")
        f = make_repo(d, skill)
        return evaluate(d, f, f)

    def wrong_path_row(d):
        rows = "".join(f"| `tools/round-40/c{i}.py` | gate | `0`; `1`; `2` | x |\n" for i in range(6))
        f = make_repo(d, HEAD + rows)
        return evaluate(d, f, f)

    def thin(d):
        skill = HEAD + good_rows().replace(
            "| `tools/round-45/y.py` | gate — test | `0` met; `1` not met; `2` unevaluable |",
            "| `tools/round-45/y.py` | gate — test | `0` met; non-zero otherwise |")
        f = make_repo(d, skill)
        return evaluate(d, f, f)

    def unknown_rev(d):
        f = make_repo(d, HEAD + good_rows())
        return evaluate(d, f, "0" * 40)

    def frozen_touched(d):
        f = make_repo(d, HEAD + good_rows())
        with open(os.path.join(d, "plans/round-45-claims.md"), "a") as fh:
            fh.write("late\n")
        git(d, "add", "-A")
        git(d, "commit", "-q", "-m", "post-freeze edit")
        return evaluate(d, f, git(d, "rev-parse", "HEAD").stdout.strip())

    def scope_size(d):
        f = make_repo(d, HEAD + good_rows(), scope=SCOPE_TEST[:5])
        return evaluate(d, f, f)

    case("green", 0, green)
    case("red-unregistered", 1, unregistered)
    case("red-wrong-path-rows", 1, wrong_path_row)
    case("red-thin-exit-cell", 1, thin)
    case("red-unknown-rev", 2, unknown_rev)
    case("red-frozen-touched", 2, frozen_touched)
    case("red-scope-size", 1, scope_size)

    failures = [c for c in cases if not c["ok"]]
    for c in cases:
        print(json.dumps({"selftest": c["case"], "expect": c["expect"], "got": c["got"],
                          "ok": c["ok"]}, sort_keys=True))
    print("C2_SELFTEST: cases=%d failures=%d" % (len(cases), len(failures)))
    shutil.rmtree(workroot, ignore_errors=True)
    return 0 if not failures else 1


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root")
    ap.add_argument("--freeze")
    ap.add_argument("--rev")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--json-out")
    args = ap.parse_args(argv)
    if args.selftest:
        return run_selftest()
    if not (args.root and args.freeze and args.rev):
        print(json.dumps({"counter": "round-45-c2", "verdict": "could_not_evaluate",
                          "reason": "usage: --root --freeze --rev (or --selftest)"}))
        return 2
    code, receipt = evaluate(os.path.abspath(args.root), args.freeze, args.rev)
    if code == 2:
        receipt = {"counter": "round-45-c2", "verdict": "could_not_evaluate", **receipt}
    if args.json_out:
        with open(args.json_out, "w") as fh:
            json.dump(receipt, fh, indent=1, sort_keys=True)
    print(json.dumps(receipt, sort_keys=True))
    return code


if __name__ == "__main__":
    sys.exit(main())
