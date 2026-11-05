#!/usr/bin/env python3
"""self-assessment-audit.py - round-99 frozen counter for R99-C1 (calibration).

Counts mismatches between the lane's self-assessment and the committed repo
state at one revision (all inputs read with `git show <rev>:<path>`):

  A1 head-score    SCORECARD `## Owned axes` coverage head score equals the
                   round-66 stem recipe's score (tools/round-66/
                   coverage-selfcheck.py, imported by path): 1 mismatch if not.
  A2 head-fraction the head's `<m>/<n> knowledge files` equals the stem
                   recipe's [mapped, files]: 1 mismatch if not.
  A3 map-rows      every `corpus/knowledge/*.md` stem appears, backticked, in a
                   TABLE ROW of corpus/README.md `## Coverage map` (a line
                   starting `|` with >= 3 cells, not the separator) whose text,
                   with the row's matched stems, pipes, backticks, commas and
                   whitespace removed, keeps >= 20 characters: 1 mismatch per
                   stem that does not.  Stricter than the stem recipe, which
                   accepts any backticked token in the section (a prose line or
                   a stem-only row passes it).
  A4 registry      every `tools/round-97/*.py`, `tools/round-98/*.py` and
                   `tools/round-99/*.py` at the revision (direct children;
                   `controls/` and `forgeries/` fixtures excluded) has a row in
                   SKILL.md at or after `## Local round-evidence gate registry`
                   whose first cell is the backticked path and which has >= 5
                   cells: cell 2 starts with a kind word (counter, gate, probe,
                   tool, generator, helper) followed by ` — `; cell 3 declares
                   an exit map with `0=` and `1=` or `2=`; cell 4 has >= 10
                   characters; some cell carries the file's full sha256 at the
                   revision.  1 mismatch per tool without such a row.

Label: `mismatches M; head-score H; head-fraction F; map-rows R of N;
registry G of T`.  Frozen predicate (R99-C1): M == 0 at the measured revision
and exit 0 (the base revision scores M > 0, committed before any edit).
Exit 1 when M > 0; 2 usage / unreadable revision.  --selftest runs the
forgery fixtures in memory (no lane write).
"""
import argparse
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys

TOOL = "tools/round-99/self-assessment-audit.py"
HERE = os.path.dirname(os.path.abspath(__file__))
REG_HEAD = "## Local round-evidence gate registry"
TOOL_DIRS = ("tools/round-97", "tools/round-98", "tools/round-99")
KIND_RE = re.compile(r"^(counter|gate|probe|tool|generator|helper)\b[^|]*? — ")
HEX64 = re.compile(r"\b[0-9a-f]{64}\b")


def load_cs():
    p = os.path.join(HERE, "..", "round-66", "coverage-selfcheck.py")
    spec = importlib.util.spec_from_file_location("coverage_selfcheck", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def git(root, *argv, binary=False):
    return subprocess.check_output(["git", "-C", root, *argv], text=not binary)


def cells(line):
    parts = line.strip().split("|")
    return [c.strip() for c in parts[1:-1]] if line.strip().endswith("|") else [c.strip() for c in parts[1:]]


def map_rows(section, stems):
    want = set(stems)
    ok = set()
    for line in section.splitlines():
        if not line.startswith("|"):
            continue
        c = cells(line)
        if len(c) < 3 or set("".join(c[:3])) <= set("-: "):
            continue
        toks = set()
        for span in re.findall(r"`([^`]+)`", line):
            for part in span.split(","):
                toks.add(re.sub(r"\.md$", "", re.sub(r"^knowledge/", "", part.strip())))
        hit = toks & want
        if not hit:
            continue
        rest = line
        for t in hit:
            rest = rest.replace("knowledge/" + t, "").replace(t, "")
        rest = re.sub(r"[\s|`,]", "", rest)
        if len(rest) < 20:
            continue
        ok |= hit
    return sorted(want - ok)


def registry_missing(skill, tools):
    """tools: {path: sha256}. Returns sorted paths lacking a valid row."""
    if REG_HEAD not in skill:
        return sorted(tools)
    body = skill.split(REG_HEAD, 1)[1]
    good = set()
    for line in body.splitlines():
        if not line.startswith("| `tools/round-9"):
            continue
        c = cells(line)
        if len(c) < 5:
            continue
        m = re.fullmatch(r"`([^`]+)`", c[0])
        if not m or m.group(1) not in tools:
            continue
        path = m.group(1)
        if not KIND_RE.match(c[1]):
            continue
        if not (re.search(r"(?<![\w.])0\s*=", c[2]) and re.search(r"(?<![\w.])[12]\s*=", c[2])):
            continue
        if len(c[3]) < 10:
            continue
        if tools[path] not in HEX64.findall(line):
            continue
        good.add(path)
    return sorted(set(tools) - good)


def score(cs, stems, readme, scorecard, skill, tools):
    section = cs.map_section(readme)
    if section is None:
        raise ValueError("no coverage map section")
    stem = cs.recipe_stem(stems, section)
    stem_score = round(10 * stem["mapped"] / stem["knowledge_files"], 2)
    row = cs.coverage_row(scorecard)
    if row is None:
        raise ValueError("no coverage head row")
    parsed = cs.parse_row(row)
    a1 = int(parsed["head_score"] != stem_score)
    a2 = int([parsed["cited_mapped"], parsed["cited_files"]] != [stem["mapped"], stem["knowledge_files"]])
    a3 = map_rows(section, stems)
    a4 = registry_missing(skill, tools)
    m = a1 + a2 + len(a3) + len(a4)
    label = ("mismatches %d; head-score %s; head-fraction %s; map-rows %d of %d; registry %d of %d"
             % (m, "ok" if not a1 else "mismatch", "ok" if not a2 else "mismatch",
                len(stems) - len(a3), len(stems), len(tools) - len(a4), len(tools)))
    return {"mismatches": m, "label": label,
            "head": {"claimed_score": parsed["head_score"], "observed_score": stem_score,
                     "claimed_fraction": [parsed["cited_mapped"], parsed["cited_files"]],
                     "observed_fraction": [stem["mapped"], stem["knowledge_files"]]},
            "map_rows_missing": a3, "registry_missing": a4, "tools": tools,
            "stem_recipe_missing": stem["missing"]}


def read_rev(root, rev):
    stems = sorted(os.path.splitext(os.path.basename(p))[0]
                   for p in git(root, "ls-tree", "-r", "--name-only", rev, "--", "corpus/knowledge").splitlines()
                   if p.endswith(".md"))
    readme = git(root, "show", "%s:corpus/README.md" % rev)
    scorecard = git(root, "show", "%s:SCORECARD.md" % rev)
    skill = git(root, "show", "%s:SKILL.md" % rev)
    tools = {}
    for d in TOOL_DIRS:
        for p in git(root, "ls-tree", "--name-only", rev, "--", d + "/").splitlines():
            if p.endswith(".py"):
                tools[p] = hashlib.sha256(git(root, "show", "%s:%s" % (rev, p), binary=True)).hexdigest()
    return stems, readme, scorecard, skill, tools


def selftest(cs):
    fails = []
    stems = ["2026-01-01-a", "2026-01-02-b"]
    state = "held — a state cell that is long enough to pass the forty char floor"
    readme = ("x\n## Coverage map\n\n| section | entries | state |\n|---|---|---|\n"
              "| A | `2026-01-01-a` | %s |\n| B | `2026-01-02-b` | %s |\n\n## Knowledge\n" % (state, state))
    sc = ("## Owned axes\n\n| Axis | s | o | e | r |\n|---|---|---|---|---|\n"
          "| coverage | 1 → 10.0 | 2/2 knowledge files mapped | x | 99 |\n\nBaseline source revision: x\n")
    sha = "a" * 64
    good_row = ("| `tools/round-99/t.py` | counter — R99 thing | 0=met; 1=not met; 2=usage | "
                "`--selftest` cases 3 | sha256 %s | none |\n" % sha)
    skill = REG_HEAD + "\n\n" + good_row
    tools = {"tools/round-99/t.py": sha}

    def case(name, want, **kw):
        args = dict(stems=stems, readme=readme, scorecard=sc, skill=skill, tools=tools)
        args.update(kw)
        got = score(cs, **args)["mismatches"]
        if got != want:
            fails.append("%s: mismatches %d want %d" % (name, got, want))

    case("green", 0)
    case("F1-prose-token", 1, readme=readme.replace("| B | `2026-01-02-b` | %s |\n" % state,
                                                    "`2026-01-02-b` mentioned in prose\n"))
    case("F2-stem-only-row", 1, readme=readme.replace("| B | `2026-01-02-b` | %s |" % state,
                                                      "| B | `2026-01-02-b` | held |"))
    case("F3-head-stale", 1, scorecard=sc.replace("1 → 10.0 | 2/2", "1 → 10.0 | 1/1"))
    case("F4-path-only-row", 1, skill=REG_HEAD + "\n\n| `tools/round-99/t.py` | x | x | x | x |\n")
    case("F5-wrong-sha", 1, skill=REG_HEAD + "\n\n" + good_row.replace(sha, "b" * 64))
    case("F6-no-exit-map", 1, skill=REG_HEAD + "\n\n" + good_row.replace("0=met; 1=not met; 2=usage", "exits"))
    case("F7-row-outside-registry", 1, skill=good_row + "\n" + REG_HEAD + "\n")
    case("F8-unregistered-tool", 1, tools=dict(tools, **{"tools/round-99/u.py": "c" * 64}))
    print("SELFTEST cases=9 failures=%d" % len(fails))
    for f in fails:
        print("FAIL", f)
    return 0 if not fails else 1


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root")
    ap.add_argument("--rev")
    ap.add_argument("--json-out")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    cs = load_cs()
    if a.selftest:
        return selftest(cs)
    if not (a.root and a.rev and a.json_out):
        print("usage: --root --rev --json-out (or --selftest)", file=sys.stderr)
        return 2
    try:
        rev = git(a.root, "rev-parse", "--verify", a.rev + "^{commit}").strip()
        res = score(cs, *read_rev(a.root, rev))
    except (subprocess.CalledProcessError, ValueError) as e:
        print("could-not-evaluate: %s" % e, file=sys.stderr)
        return 2
    with open(os.path.abspath(__file__), "rb") as fh:
        res.update({"tool": TOOL, "rev": rev, "counter_sha256": hashlib.sha256(fh.read()).hexdigest(),
                    "exit": 0 if res["mismatches"] == 0 else 1, "met": res["mismatches"] == 0})
    tmp = a.json_out + ".partial"
    with open(tmp, "w") as fh:
        json.dump(res, fh, indent=1, sort_keys=True)
        fh.write("\n")
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, a.json_out)
    print(res["label"], "met", res["met"])
    return res["exit"]


if __name__ == "__main__":
    sys.exit(main())
