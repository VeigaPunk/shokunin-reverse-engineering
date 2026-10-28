#!/usr/bin/env python3
"""Mutation harness for R45W2CritC2Text: run the frozen c2-counter against
fixture repos that vary only the SKILL.md row shape. Read-only on the lane."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
COUNTER = os.path.join(LANE, "tools/round-45/c2-counter.py")
SCOPE = "tools/round-45/registry-scope.json"
CLAIMS = "plans/round-45-claims.md"
S = os.environ["S"]

PATHS = ["tools/round-44/a.py", "tools/round-44/b.sh", "tools/round-44/c.py",
         "tools/round-45/x.py", "tools/round-45/y.py", "tools/round-45/z.py"]

HEAD = "# SKILL\n\n### Round-44 instrument registry\n\n| tool | gate | exits | selftest | provenance | opts | lane |\n|---|---|---|---|---|---|---|\n"


def row(p, exits="`0` met; `1` not met; `2` unevaluable", first=None):
    return f"| {first or ('`' + p + '`')} | gate — test | {exits} | `--selftest` | src | opts | kaidoku |\n"


def rows(paths=None, exits="`0` met; `1` not met; `2` unevaluable"):
    return "".join(row(p, exits) for p in (paths or PATHS))


def git(d, *a):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True)


def make(d, skill, scope_paths=None, claims_text="claims\n" * 10):
    git(d, "init", "-q")
    git(d, "config", "user.email", "c2@selftest")
    git(d, "config", "user.name", "c2 selftest")
    top = git(d, "rev-parse", "--show-toplevel").stdout.strip()
    assert top == d, f"fixture toplevel {top!r} != {d!r}"
    files = {"SKILL.md": skill,
             SCOPE: json.dumps({"scope": "test", "paths": scope_paths or PATHS}, indent=1),
             CLAIMS: claims_text}
    for p, text in files.items():
        full = os.path.join(d, p)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as fh:
            fh.write(text)
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", "freeze")
    return git(d, "rev-parse", "HEAD").stdout.strip()


def run(skill, scope_paths=None):
    d = tempfile.mkdtemp(dir=os.path.join(S, "fx"))
    try:
        f = make(d, skill, scope_paths)
        r = subprocess.run([sys.executable, "-I", "-B", COUNTER, "--root", d,
                            "--freeze", f, "--rev", f],
                           capture_output=True, text=True, env={**os.environ, "TMPDIR": S})
        try:
            rec = json.loads(r.stdout)
        except ValueError:
            rec = {"raw": r.stdout[:200], "stderr": r.stderr[:200]}
        return r.returncode, rec
    finally:
        shutil.rmtree(d, ignore_errors=True)


CASES = {}


def case(name, expect, skill, scope_paths=None):
    CASES[name] = (expect, skill, scope_paths)


case("green-registry", 0, HEAD + rows())

case("decoy-heading-not-a-registry", 0,
     "# SKILL\n\n## Counting commands (not a registry)\n\n| tool | gate | exits | selftest | provenance | opts | lane |\n|---|---|---|---|---|---|---|\n" + rows())

case("fenced-code-block", 0,
     "# SKILL\n\n## Example\n\n```\n| tool | gate | exits | selftest | provenance | opts | lane |\n|---|---|---|---|---|---|---|\n" + rows() + "```\n")

case("duplicate-first-thin-second-full", 1,
     HEAD + row(PATHS[0], "`0` met; non-zero otherwise") + rows() + row(PATHS[0]))

case("duplicate-first-full-second-thin", 0,
     HEAD + rows() + row(PATHS[0], "`0` met; non-zero otherwise"))

case("negation-cell-names-0-1-2", 0,
     HEAD + row(PATHS[0], "never `0`; never `1`; never `2`") + rows(PATHS[1:]))

case("first-cell-extra-prose", 0,
     HEAD + row(PATHS[0], first="the `%s` gate" % PATHS[0]) + rows(PATHS[1:]))

case("mjs-scope-path", 1,
     HEAD + rows() + row("tools/round-27/xpin-attribute.mjs"),
     PATHS + ["tools/round-27/xpin-attribute.mjs"])

case("header-only-no-rows", 1, HEAD)

case("empty-exit-cell", 1,
     HEAD + row(PATHS[0], "``") + rows(PATHS[1:]))

case("exit-in-gate-column-only", 1,
     "# SKILL\n\n### Round-44 instrument registry\n\n| tool | gate | exits | selftest |\n|---|---|---|---|\n"
     + "| `%s` | gate names 0, 1 and 2 | non-zero | x |\n" % PATHS[0]
     + "".join("| `%s` | gate — test | `0` met; `1` not met; `2` unevaluable | x |\n" % p for p in PATHS[1:]))

if __name__ == "__main__":
    os.makedirs(os.path.join(S, "fx"), exist_ok=True)
    out = {}
    for name, (expect, skill, scope_paths) in CASES.items():
        code, rec = run(skill, scope_paths)
        digest = hashlib.sha256(json.dumps(rec, sort_keys=True).encode()).hexdigest()
        out[name] = {"expect": expect, "got": code,
                     "ok": code == expect,
                     "receipt_sha256": digest,
                     "unregistered": rec.get("unregistered"),
                     "thin": rec.get("thin"),
                     "scope_size": rec.get("scope_size"),
                     "registered": rec.get("registered"),
                     "reason": rec.get("reason")}
        print(json.dumps({"case": name, **out[name]}, sort_keys=True))
    json.dump(out, open(os.path.join(S, "mutations.json"), "w"), indent=1, sort_keys=True)
