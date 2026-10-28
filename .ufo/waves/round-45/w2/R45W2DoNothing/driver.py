#!/usr/bin/env python3
"""R45W2DoNothing: build cheapest skip artefacts and score them with the frozen counters."""
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
FREEZE = "f762b7273e3f6ca3c710bb37d5de92a4a4417aec"
S = os.environ["S"]
REF = "corpus/lessons/round-44.md"
REF2 = "corpus/lessons/round-44-verifier-spotcheck.md"
REF3 = "corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md"


def show(path, rev=FREEZE):
    r = subprocess.run(["git", "-C", LANE, "show", f"{rev}:{path}"], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"cannot read {path}@{rev}: {r.stderr}")
    return r.stdout


def git(d, *args):
    return subprocess.run(["git", "-C", d, *args], capture_output=True, text=True)


def init_repo(name):
    d = tempfile.mkdtemp(dir=os.path.join(S, "fx"), prefix=name + "-")
    git(d, "init", "-q")
    git(d, "config", "user.email", "w2@do-nothing")
    git(d, "config", "user.name", "w2 do nothing")
    top = git(d, "rev-parse", "--show-toplevel").stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(d), (top, d)
    return d


def write(d, rel, text):
    full = os.path.join(d, rel)
    os.makedirs(os.path.dirname(full) or d, exist_ok=True)
    with open(full, "w") as fh:
        fh.write(text)


def commit(d, msg="fixture"):
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", msg)
    return git(d, "rev-parse", "HEAD").stdout.strip()


CRAFT_HEAD = "# SKILL\n\n## Queue-drain craft (fixture)\n\n"


def plain_blocks(n):
    return "".join(f"- **{i}. Plain rule {i}.** body text with no table.\n\n" for i in range(1, n + 1))


def triage_table_rows(limit=8):
    """Pull the largest existing table out of the real craft section and relabel it."""
    skill = show("SKILL.md")
    section = skill.split("## Queue-drain craft ", 1)[1].split("\n## ", 1)[0]
    tables, cur = [], []
    for line in section.splitlines():
        s = line.strip()
        if s.startswith("|"):
            cur.append(s)
        elif cur:
            tables.append(cur)
            cur = []
    if cur:
        tables.append(cur)
    tables = [t for t in tables if len(t) >= 4]
    big = max(tables, key=len)
    # first cell of each data row is the triage trigger; keep it, drop the rest
    header = big[0]
    data = [t for t in big[1:] if not re.fullmatch(r"\|[\s:|-]+\|", t)]
    rows = []
    for i, row in enumerate(data[:limit]):
        cells = [c.strip() for c in row.strip("|").split("|")]
        rows.append(f"| {cells[0]} | triage | {i % 3} | receipt-{i} |")
    return header, rows, len(big)


def build_c1(name, block_body, with_interpreter=True):
    d = init_repo(name)
    write(d, "SKILL.md", CRAFT_HEAD + plain_blocks(21) + block_body)
    if with_interpreter:
        write(d, "tools/round-45/frozen-path-preflight.py", show("tools/round-45/frozen-path-preflight.py"))
    write(d, "plans/round-45-claims.md", show("plans/round-45-claims.md"))
    for p in (REF, REF2, REF3):
        write(d, p, show(p))
    rev = commit(d)
    return d, rev


def score(tool, d, rev, out):
    cmd = [sys.executable, "-I", "-B", os.path.join(LANE, "tools/round-45", tool),
           "--root", d, "--freeze", rev, "--rev", rev, "--json-out", out]
    p = subprocess.run(cmd, capture_output=True, text=True,
                       env=dict(os.environ, TMPDIR=os.path.join(S, "tmp"), HYAKU_SCRATCH=os.path.join(S, "tmp")))
    return p.returncode, json.load(open(out)), " ".join(cmd)


def main():
    os.makedirs(os.path.join(S, "fx"), exist_ok=True)
    os.makedirs(os.path.join(S, "tmp"), exist_ok=True)
    results = {}

    hdr, rows, tlen = triage_table_rows(8)
    relabelled = (
        "- **22. Freeze integrity.** <!-- freeze-integrity-table v1 --> S140 "
        "tools/round-45/frozen-path-preflight.py\n\n"
        "  | trigger | arm | exit | receipt |\n  | --- | --- | --- | --- |\n  "
        + "\n  ".join(rows) + "\n\n"
        "  Refs: " + ", ".join(f"{p}:1" for p in (REF, REF2, REF3, "plans/round-45-claims.md")) + "\n\n"
    )
    d, rev = build_c1("c1-relabelled", relabelled)
    code, rec, cmd = score("c1-counter.py", d, rev, os.path.join(S, "c1-relabelled.json"))
    results["c1_relabelled_triage_22blocks"] = {
        "exit": code, "met_target": rec.get("met_target"), "failing": rec.get("failing"),
        "rule_blocks": rec.get("rule_blocks"), "rows": rec.get("block22_rows"),
        "refs": rec.get("block22_refs"), "table_source_len": tlen,
        "trigger_cell_sample": rows[0], "cmd": cmd, "fixture": d}

    # degenerate: 8 filler rows, no triage content at all
    filler = (
        "- **22. x.** <!-- freeze-integrity-table v1 --> S140 "
        "tools/round-45/frozen-path-preflight.py\n\n"
        "  | trigger | arm | exit | receipt |\n  | --- | --- | --- | --- |\n"
        + "".join(f"  | filler-{i} | filler | {i % 3} | filler |\n" for i in range(8))
        + "\n  Refs: " + ", ".join(f"{p}:1" for p in (REF, REF2, REF3, "plans/round-45-claims.md")) + "\n\n"
    )
    d2, rev2 = build_c1("c1-filler", filler)
    code2, rec2, cmd2 = score("c1-counter.py", d2, rev2, os.path.join(S, "c1-filler.json"))
    results["c1_filler_rows_22blocks"] = {
        "exit": code2, "met_target": rec2.get("met_target"), "failing": rec2.get("failing"),
        "rule_blocks": rec2.get("rule_blocks"), "cmd": cmd2, "fixture": d2}

    # C2(a): six rows naming tools that do not exist at the revision
    ghost = "".join(
        f"| `tools/round-99/ghost-{i}.py` | gate | `0` met; `1` not met; `2` unevaluable | `--selftest` |\n"
        for i in range(6))
    head = ("# SKILL\n\n### Round-45 instrument registry\n\n"
            "| tool | gate | exits | selftest |\n|---|---|---|---|\n")
    d3 = init_repo("c2-ghost")
    write(d3, "SKILL.md", head + ghost)
    write(d3, "tools/round-45/registry-scope.json", show("tools/round-45/registry-scope.json"))
    write(d3, "plans/round-45-claims.md", show("plans/round-45-claims.md"))
    rev3 = commit(d3)
    code3, rec3, cmd3 = score("c2-counter.py", d3, rev3, os.path.join(S, "c2-ghost.json"))
    results["c2_six_ghost_rows"] = {
        "exit": code3, "met_target": rec3.get("met_target"), "failing": rec3.get("failing"),
        "registry_rows": rec3.get("registry_rows"), "unregistered": rec3.get("unregistered"),
        "cmd": cmd3, "fixture": d3}

    # C2(b): six rows with the right paths but a vacuous exit cell and no gate content
    scope = json.loads(show("tools/round-45/registry-scope.json"))["paths"]
    vac = "".join(f"| `{p}` | x | 0 1 2 | x |\n" for p in scope)
    d4 = init_repo("c2-vacuous")
    write(d4, "SKILL.md", head + vac)
    write(d4, "tools/round-45/registry-scope.json", show("tools/round-45/registry-scope.json"))
    write(d4, "plans/round-45-claims.md", show("plans/round-45-claims.md"))
    rev4 = commit(d4)
    code4, rec4, cmd4 = score("c2-counter.py", d4, rev4, os.path.join(S, "c2-vacuous.json"))
    results["c2_six_vacuous_rows"] = {
        "exit": code4, "met_target": rec4.get("met_target"), "failing": rec4.get("failing"),
        "registered": rec4.get("registered"), "thin": rec4.get("thin"),
        "cmd": cmd4, "fixture": d4}

    print(json.dumps(results, indent=1, sort_keys=True))
    json.dump(results, open(os.path.join(S, "skip-results.json"), "w"), indent=1, sort_keys=True)


if __name__ == "__main__":
    main()
