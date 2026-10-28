#!/usr/bin/env python3
"""R45-C1 satisfiability preflight: build fixture repos, score each with the frozen counter.

Read-only on the lane tree; every fixture lives under S and is removed by the caller.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = "/fast/scratch/hyaku/kaidoku-r45/R45W1C1Satisfy"
OUT = os.path.join(REPO, ".ufo/waves/round-45/w1/R45W1C1Satisfy")
RECEIPTS = os.path.join(OUT, "receipts")
FREEZE = "f762b7273e3f6ca3c710bb37d5de92a4a4417aec"

CANON_ROWS = [
    "| no commit in FREEZE..REV touches a frozen path | commit | 0 | `verdict: clean` (corpus/lessons/round-44.md:18) |",
    "| post-freeze commit touches a frozen path | commit | 1 | `frozen_path_changed` (corpus/lessons/round-44.md:63) |",
    "| path touched then restored to its FREEZE bytes | restored | 1 | `restored: [...]` (corpus/lessons/round-44-verifier-spotcheck.md:89-92) |",
    "| worktree dirty under the frozen pathspec | dirty | 1 | `dirty: [...]` (corpus/lessons/round-44.md:88) |",
    "| directory freeze scored without --pathspec | pathspec | 2 | `pathspec_required` (plans/round-45-claims.md:1) |",
    "| freeze revision unknown to the repo | commit | 2 | `unknown freeze revision` (plans/round-45-claims.md:20) |",
    "| freeze is not an ancestor of rev | commit | 2 | `freeze is not an ancestor of rev` (plans/round-45-claims.md:24) |",
    "| bulk sweep commits frozen fixtures with unrelated paths | commit | 1 | `touched: [...]` (corpus/lessons/round-44.md:63) |",
]
CANON_HEADER = "| trigger | arm | exit | receipt |"
CANON_SEP = "|---|---|---|---|"


def git(root, *args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True, text=True)


def utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def write(root, path, text):
    full = os.path.join(root, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as fh:
        fh.write(text)


def commit(root, msg):
    git(root, "add", "-A")
    r = git(root, "commit", "-q", "-m", msg)
    assert r.returncode == 0, r.stderr
    return git(root, "rev-parse", "HEAD").stdout.strip()


def block(header=CANON_HEADER, sep=CANON_SEP, rows=None, marker=True, s140=True,
          interp=True, lead="- **22. Freeze integrity: decide from the arm, not the tip.** "):
    rows = CANON_ROWS if rows is None else rows
    head = lead + ("<!-- freeze-integrity-table v1 --> " if marker else "")
    if s140:
        head += "S140 (git-status porcelain v1) fixes the dirty arm's parse; "
    if interp:
        head += "the gate is `tools/round-45/frozen-path-preflight.py`.\n"
    out = head + "\n"
    out += "  " + header + "\n"
    out += "  " + sep + "\n"
    for r in rows:
        out += "  " + r + "\n"
    return out


def base_sources():
    skill = subprocess.run(["git", "-C", REPO, "show", FREEZE + ":SKILL.md"],
                           capture_output=True, text=True, check=True).stdout
    claims = subprocess.run(["git", "-C", REPO, "show", FREEZE + ":plans/round-45-claims.md"],
                            capture_output=True, text=True, check=True).stdout
    pre = subprocess.run(["git", "-C", REPO, "show", FREEZE + ":tools/round-45/frozen-path-preflight.py"],
                         capture_output=True, text=True, check=True).stdout
    cnt = subprocess.run(["git", "-C", REPO, "show", FREEZE + ":tools/round-45/c1-counter.py"],
                         capture_output=True, text=True, check=True).stdout
    corpus = {}
    for name in ("corpus/lessons/round-44.md", "corpus/lessons/round-44-verifier-spotcheck.md"):
        r = subprocess.run(["git", "-C", REPO, "show", f"{FREEZE}:{name}"],
                           capture_output=True, text=True)
        if r.returncode != 0:
            raise SystemExit(f"missing {name} at freeze")
        corpus[name] = r.stdout
    return skill, claims, pre, cnt, corpus


ANCHOR = "\n## Config custody for live-probe rounds (SOP)"


def craft_count(skill):
    sec = skill.split("## Queue-drain craft ", 1)[1].split("\n## ", 1)[0]
    return len(re.split(r"(?m)^- \*\*", sec)[1:])


def build(d, skill_base, block_text, claims, pre, cnt, corpus, skill_transform=None,
          frozen_touch=False):
    os.makedirs(d, exist_ok=True)
    git(d, "init", "-q")
    assert os.path.realpath(git(d, "rev-parse", "--show-toplevel").stdout.strip()) == os.path.realpath(d)
    git(d, "config", "user.email", "r45w1c1@fixture")
    git(d, "config", "user.name", "r45w1c1 fixture")
    assert craft_count(skill_base) == 21, craft_count(skill_base)
    write(d, "SKILL.md", skill_base)
    write(d, "plans/round-45-claims.md", claims)
    write(d, "tools/round-45/frozen-path-preflight.py", pre)
    write(d, "tools/round-45/c1-counter.py", cnt)
    for name, text in corpus.items():
        write(d, name, text)
    f = commit(d, "freeze")
    assert ANCHOR in skill_base
    landed = skill_base.replace(ANCHOR, "\n" + block_text + ANCHOR, 1)
    if skill_transform:
        landed = skill_transform(landed)
    write(d, "SKILL.md", landed)
    r = commit(d, "land block 22")
    if frozen_touch:
        with open(os.path.join(d, "plans/round-45-claims.md"), "a") as fh:
            fh.write("late edit after the landing\n")
        r = commit(d, "touch a frozen path after the landing")
    return f, r, landed


VARIANTS = []


def variant(name, expect, note, block_text=None, transform=None, skill_transform=None):
    VARIANTS.append({"name": name, "expect": expect, "note": note,
                     "block": block_text, "transform": transform,
                     "skill_transform": skill_transform, "frozen_touch": False})


def t_indent(bt):
    return "\n".join(("    " + l[2:]) if l.startswith("  |") else l for l in bt.split("\n"))


def t_split(bt):
    lines = bt.split("\n")
    return "\n".join(lines[:3] + ["", "  These arms are ordered by when they fire.", ""] + lines[3:])


def t_split_header(bt):
    lines = bt.split("\n")
    return "\n".join(lines[:3] + ["", "  These arms are ordered by when they fire.", "",
                                  "  " + CANON_HEADER, "  " + CANON_SEP, ""] + lines[3:])


def _cells(row):
    return [c for c in row.strip().strip("|").split("|")]


def _row(cells):
    return "  | " + " | ".join(c.strip() for c in cells) + " |"


def t_backtick_exit(bt):
    out = []
    for l in bt.split("\n"):
        if l.startswith("  |") and not l.startswith("  |---") and "trigger" not in l:
            c = _cells(l)
            c[2] = "`" + c[2] + "`"
            l = _row(c)
        out.append(l)
    return "\n".join(out)


def t_drop_sep(bt):
    return "\n".join(l for l in bt.split("\n") if l.strip() != CANON_SEP)


def t_table_first(bt):
    lines = bt.split("\n")
    return "\n".join(lines[2:] + [lines[0]])


def t_marker_twice(bt):
    lines = bt.split("\n")
    lines[0] = lines[0] + " <!-- freeze-integrity-table v1 -->"
    return "\n".join(lines)


def t_nested_bullet(bt):
    return bt.rstrip("\n") + "\n  - **note:** the arms are ordered by when they fire.\n"


def t_indent_head(bt):
    lines = bt.split("\n")
    lines[0] = "  " + lines[0]
    return "\n".join(lines)


def t_exit_second(bt):
    out = []
    for l in bt.split("\n"):
        if l.startswith("  |") and "trigger" in l:
            l = "  | trigger | exit | arm | receipt |"
        elif l.startswith("  |") and not l.startswith("  |---"):
            c = _cells(l)
            c = [c[0], c[2], c[1], c[3]]
            l = _row(c)
        out.append(l)
    return "\n".join(out)


def t_header_backticked(bt):
    return bt.replace("  " + CANON_HEADER, "  | `trigger` | `arm` | `exit` | `receipt` |")


def t_fenced(bt):
    lines = bt.split("\n")
    return "\n".join(lines[:2] + ["  ```"] + lines[2:11] + ["  ```"] + lines[11:])


def t_no_lead_pipe(bt):
    return "\n".join(("  " + l.strip()[1:].strip()) if l.startswith("  |") else l
                     for l in bt.split("\n"))


def t_bold_exit(bt):
    out = []
    for l in bt.split("\n"):
        if l.startswith("  |") and not l.startswith("  |---") and "trigger" not in l:
            c = _cells(l)
            c[2] = "**" + c[2] + "**"
            l = _row(c)
        out.append(l)
    return "\n".join(out)


def t_second_marked_block(bt):
    return bt.rstrip("\n") + ("\n- **23. Another freeze rule.** <!-- freeze-integrity-table v1 -->"
                              " S140 tools/round-45/frozen-path-preflight.py\n\n"
                              "  | trigger | arm | exit | receipt |\n  |---|---|---|---|\n")


def rows_only_n(n, mutate=None):
    rows = []
    for i, r in enumerate(CANON_ROWS):
        c = _cells(r)
        if i >= n:
            c[3] = c[3].split(" (")[0]
        rows.append(_row(c))
    if mutate:
        rows = mutate(rows)
    return rows



def patch_rows(rows, idx, new):
    rows = list(rows)
    rows[idx] = new
    return rows


def t_heading_bare(skill):
    return skill.replace("## Queue-drain craft (rounds 5-12, distilled in round 13)",
                         "## Queue-drain craft", 1)


def t_block_outside_section(skill):
    sec = "## Queue-drain craft "
    i = skill.index(sec)
    head, tail = skill[:i], skill[i:]
    cut = tail.index("\n## ")
    block_part = tail[:cut]
    # remove the inserted block from the section and re-emit it under a new heading
    marker = "<!-- freeze-integrity-table v1 -->"
    start = block_part.index("- **22. Freeze integrity")
    end = len(block_part)
    moved = block_part[start:end]
    sec_only = block_part[:start]
    rest = tail[cut:]
    return head + sec_only + rest + "\n## Appendix\n\n" + moved


variant("v20-heading-without-trailing-space", 1, "renamed craft heading (no trailing space)",
        skill_transform=t_heading_bare)
variant("v21-exit-cell-with-annotation", 1, "exit cell '0 (clean)'",
        block_text=block(rows=patch_rows(CANON_ROWS, 0,
            "| no commit in FREEZE..REV touches a frozen path | commit | 0 (clean) | `verdict: clean` (corpus/lessons/round-44.md:18) |")))
variant("v22-header-exit-code", 0, "header cell 'exit code'",
        block_text=block(header="| trigger | arm | exit code | receipt |"))
variant("v23-literal-pipe-in-arm-cell", 1, "a bare pipe inside one arm cell",
        block_text=block(rows=patch_rows(CANON_ROWS, 1,
            "| post-freeze commit touches a frozen path | commit|blob | 1 | `frozen_path_changed` (corpus/lessons/round-44.md:63) |")))
variant("v24-block-outside-craft-section", 1, "block moved below a later ## heading",
        skill_transform=t_block_outside_section)


# canonical
variant("v00-canonical", 0, "the spec-shaped block")
# the three asked-for syntax variations
variant("v01-table-indented", 0, "every table line prefixed with two spaces", transform=t_indent)
variant("v02-table-split-by-paragraph", 0, "table halves separated by a prose line", transform=t_split)
variant("v03-split-plus-second-header", 1, "split table with a repeated header row", transform=t_split_header)
variant("v04-exit-cell-backticked", 0, "exit cells written as `0`/`1`/`2`", transform=t_backtick_exit)
# further parser probes
variant("v05-no-separator-row", 1, "table without the |---| separator row", transform=t_drop_sep)
variant("v06-table-before-block-line", 1, "table placed above the - **22. line", transform=t_table_first)
variant("v07-marker-twice-same-block", 0, "marker repeated inside block 22", transform=t_marker_twice)
variant("v08-nested-bold-bullet", 1, "a '  - **note:**' sub-bullet inside block 22", transform=t_nested_bullet)
variant("v09-block-line-indented", 1, "the - **22. line itself indented", transform=t_indent_head)
variant("v10-exit-column-second", 0, "header columns trigger|exit|arm|receipt", transform=t_exit_second)
variant("v11-header-cells-backticked", 0, "header cells wrapped in backticks", transform=t_header_backticked)
variant("v12-table-fenced", 0, "table inside a ``` fence", transform=t_fenced)
variant("v13-only-three-citations", 1, "three resolvable citations",
        block_text=block(rows=rows_only_n(3)))
variant("v14-citation-past-eof", 1, "one citation line past EOF",
        block_text=block(rows=patch_rows(CANON_ROWS, 0,
                                    "| no commit in FREEZE..REV touches a frozen path | commit | 0 | `verdict: clean` (corpus/lessons/round-44.md:9999) |")))
variant("v15-s140-hyphenated", 1, "S-140 instead of S140",
        block_text=block(s140=False).replace("the gate is", "See S-140. The gate is", 1))
variant("v16-citation-without-line", 0, "a citation with no :line",
        block_text=block(rows=patch_rows(CANON_ROWS, 0,
                                    "| no commit in FREEZE..REV touches a frozen path | commit | 0 | `verdict: clean` (corpus/lessons/round-44.md) |")))
variant("v17-rows-no-leading-pipe", 1, "table rows without a leading pipe", transform=t_no_lead_pipe)
variant("v18-bold-exit-cell", 1, "exit cell written as **0**", transform=t_bold_exit)
variant("v19-two-marked-blocks", 1, "marker in block 22 and in a 23rd block", transform=t_second_marked_block)
variant("v25-canonical-then-frozen-touch", 2, "canonical block, then a post-landing commit edits the claims file")


def main():
    os.makedirs(RECEIPTS, exist_ok=True)
    os.makedirs(os.path.join(S, "runner"), exist_ok=True)
    runner = os.path.join(S, "runner", "c1-counter.py")
    pre_path = os.path.join(S, "runner", "frozen-path-preflight.py")
    skill, claims, pre, cnt, corpus = base_sources()
    with open(runner, "w") as fh:
        fh.write(cnt)
    with open(pre_path, "w") as fh:
        fh.write(pre)

    results = []
    for v in VARIANTS:
        if v["name"].startswith("v25"):
            v["frozen_touch"] = True
        bt = v["block"] if v["block"] is not None else block()
        if v["transform"]:
            bt = v["transform"](bt)
        d = tempfile.mkdtemp(dir=S, prefix="fx-")
        try:
            f, r, landed = build(d, skill, bt, claims, pre, cnt, corpus, v["skill_transform"],
                                 v["frozen_touch"])
            run = os.path.join(S, "runner", "work-" + v["name"])
            os.makedirs(run, exist_ok=True)
            cmd = [sys.executable, "-I", "-B", runner, "--root", d, "--freeze", f, "--rev", r,
                   "--json-out", os.path.join(RECEIPTS, v["name"] + ".json")]
            env = dict(os.environ, TMPDIR=run, HYAKU_SCRATCH=run)
            env.pop("GIT_DIR", None)
            t0 = utc()
            p = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=600)
            t1 = utc()
            sha = hashlib.sha256(p.stdout.encode()).hexdigest()
            try:
                receipt = json.loads(p.stdout)
            except Exception:
                receipt = {"stdout_unparsed": p.stdout[-2000:]}
            rec = {"variant": v["name"], "note": v["note"], "expect": v["expect"],
                   "exit": p.returncode, "stdout_sha256": sha, "utc_start": t0, "utc_end": t1,
                   "command": " ".join(cmd), "fixture": d, "freeze": f, "rev": r,
                   "receipt": receipt, "stderr_tail": p.stderr[-800:]}
            with open(os.path.join(RECEIPTS, v["name"] + ".json"), "w") as fh:
                json.dump(rec, fh, indent=1, sort_keys=True)
            results.append(rec)
            print(json.dumps({"variant": v["name"], "exit": p.returncode,
                              "expect": v["expect"], "failing": receipt.get("failing"),
                              "rows": receipt.get("block22_rows"),
                              "refs": receipt.get("block22_refs"),
                              "blocks": receipt.get("rule_blocks"),
                              "present": receipt.get("block22_present"),
                              "selftest": receipt.get("preflight_selftest")}, sort_keys=True))
        finally:
            shutil.rmtree(d, ignore_errors=True)
            shutil.rmtree(os.path.join(S, "runner", "work-" + v["name"]), ignore_errors=True)
    with open(os.path.join(OUT, "summary.json"), "w") as fh:
        json.dump(results, fh, indent=1, sort_keys=True)
    mism = [r["variant"] for r in results if r["exit"] != r["expect"]]
    print("EXPECT_MISMATCH:", mism)
    return 0


if __name__ == "__main__":
    sys.exit(main())
