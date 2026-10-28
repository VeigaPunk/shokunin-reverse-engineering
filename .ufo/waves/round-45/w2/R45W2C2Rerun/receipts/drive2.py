#!/usr/bin/env python3
"""Round 2: duplicate-row, table-scope and column-position attacks on c2-counter."""
import hashlib
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
TARGET = "tools/round-44/c1-counter.py"


def run(args, cwd=None):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)


def git(d, *a):
    return run(["git", "-C", d, *a])


class Fixture:
    def __init__(self, name):
        self.d = os.path.join(S, "fx2-" + name)
        shutil.rmtree(self.d, ignore_errors=True)
        os.makedirs(self.d)
        self.d = os.path.realpath(self.d)
        assert git(self.d, "init", "-q").returncode == 0
        top = git(self.d, "rev-parse", "--show-toplevel").stdout.strip()
        assert os.path.realpath(top) == self.d, (top, self.d)
        git(self.d, "config", "user.email", "w2c2@rerun")
        git(self.d, "config", "user.name", "w2c2 rerun")
        for rel in ("SKILL.md", SCOPE_REL, CLAIMS_REL):
            full = os.path.join(self.d, rel)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            open(full, "w").write(open(os.path.join(LANE, rel)).read())
        os.makedirs(os.path.join(self.d, "tools/round-45"), exist_ok=True)
        git(self.d, "add", "-A")
        git(self.d, "commit", "-q", "-m", "freeze")
        self.f1 = git(self.d, "rev-parse", "HEAD").stdout.strip()
        self.skill = open(os.path.join(self.d, "SKILL.md")).read()

    def target_line(self):
        for line in self.skill.splitlines():
            if line.startswith("| `" + TARGET + "` |"):
                return line
        raise SystemExit("target row not found")

    def write(self, text):
        open(os.path.join(self.d, "SKILL.md"), "w").write(text)

    def commit(self):
        git(self.d, "add", "-A")
        r = git(self.d, "commit", "-q", "-m", "mutate")
        assert r.returncode == 0, r.stderr
        return git(self.d, "rev-parse", "HEAD").stdout.strip()

    def score(self, tag):
        out = os.path.join(S, "score2-" + tag + ".json")
        r = run([sys.executable, "-I", "-B", COUNTER, "--root", self.d, "--freeze",
                 self.f1, "--rev", self.commit(), "--json-out", out], cwd=S)
        rec = json.load(open(out)) if os.path.exists(out) else {}
        return {"tag": tag, "exit": r.returncode,
                "stdout_sha256": hashlib.sha256(r.stdout.encode()).hexdigest(),
                "registered": rec.get("registered"), "unregistered": rec.get("unregistered"),
                "thin": rec.get("thin"), "registry_rows": rec.get("registry_rows"),
                "failing": rec.get("failing"), "reason": rec.get("reason"),
                "verdict": rec.get("verdict"), "stderr": r.stderr.strip()[:300]}


def thin_variant(line):
    cells = [c for c in line.strip().strip("|").split("|")]
    cells[2] = " non-zero on any failure "
    return "|" + "|".join(cells) + "|"


def exitless_variant(line):
    cells = [c for c in line.strip().strip("|").split("|")]
    cells[2] = " `0` met; `1` not met "
    return "|" + "|".join(cells) + "|"


def embedded_numbers(line):
    cells = [c for c in line.strip().strip("|").split("|")]
    cells[2] = " `10` met; `11` not met; `12` unevaluable "
    return "|" + "|".join(cells) + "|"


results = []

# F: good row first, bare-non-zero duplicate second.
fx = Fixture("F-dup-thin-after")
line = fx.target_line()
fx.write(fx.skill.replace(line + "\n", line + "\n" + thin_variant(line) + "\n", 1))
results.append(fx.score("F-dup-thin-after"))

# G: thin duplicate FIRST, good row after.
fx = Fixture("G-dup-thin-before")
line = fx.target_line()
fx.write(fx.skill.replace(line + "\n", thin_variant(line) + "\n" + line + "\n", 1))
results.append(fx.score("G-dup-thin-before"))

# H: the row lives only in a non-registry table under ## Sources (7 cells kept).
fx = Fixture("H-row-under-sources")
line = fx.target_line()
text = fx.skill.replace(line + "\n", "", 1)
text += ("\n## Sources\n\n| tool | gate or probe | verdict map (exit codes) | self-test | "
         "pin | scope | owner |\n|---|---|---|---|---|---|---|\n" + line + "\n")
fx.write(text)
results.append(fx.score("H-row-under-sources"))

# H2: the row lives only inside a fenced code block.
fx = Fixture("H2-row-in-codeblock")
line = fx.target_line()
text = fx.skill.replace(line + "\n", "", 1)
text += "\n```\n" + line + "\n```\n"
fx.write(text)
results.append(fx.score("H2-row-in-codeblock"))

# K: legacy 5-column table; cells[2] is `command` (with 0/1/2), cells[3] is the exit map (bare).
fx = Fixture("K-column-shift-false-pass")
line = fx.target_line()
cells = [c for c in line.strip().strip("|").split("|")]
legacy = ("| " + cells[0] + " | gate | `--mode 0 --retry 1 --code 2` | non-zero on any "
          "failure | none |")
text = fx.skill.replace(line + "\n", "", 1)
text += ("\n| tool | purpose | command | exit codes | selftest |\n|---|---|---|---|---|\n"
         + legacy + "\n")
fx.write(text)
results.append(fx.score("K-column-shift-false-pass"))

# K2: legacy table where the exit cell names 0/1/2 but the command cell does not -> false thin.
fx = Fixture("K2-column-shift-false-thin")
line = fx.target_line()
cells = [c for c in line.strip().strip("|").split("|")]
legacy = ("| " + cells[0] + " | gate | `python3 -I -B " + TARGET + " --selftest` | "
          "`0` met; `1` not met; `2` unevaluable | x |")
text = fx.skill.replace(line + "\n", "", 1)
text += ("\n| tool | purpose | command | exit codes | selftest |\n|---|---|---|---|---|\n"
         + legacy + "\n")
fx.write(text)
results.append(fx.score("K2-column-shift-false-thin"))

# L: exit cell names 0 and 1 but not 2.
fx = Fixture("L-exit-cell-missing-2")
line = fx.target_line()
fx.write(fx.skill.replace(line + "\n", exitless_variant(line) + "\n", 1))
results.append(fx.score("L-exit-cell-missing-2"))

# M: exit cell names only 10/11/12 (no bare 0/1/2).
fx = Fixture("M-embedded-numbers")
line = fx.target_line()
fx.write(fx.skill.replace(line + "\n", embedded_numbers(line) + "\n", 1))
results.append(fx.score("M-embedded-numbers"))

print(json.dumps(results, indent=1, sort_keys=True))
