#!/usr/bin/env python3
"""R45-C1 counter: freeze-integrity decision table (SKILL rule block 22) and its arms.

Frozen target (plans/round-45-claims.md, R45-C1): at `--rev`,
  rule_blocks                     == 22 inside `## Queue-drain craft`
  block22_present                 == 1  (marker `<!-- freeze-integrity-table v1 -->`, exactly once)
  block22_rows                    >= 8  (table data rows, every exit cell in {0,1,2})
  block22_unresolved_citations    == 0  (every `path:line` ref resolves at --rev)
  block22_refs                    >= 4
  cites S140 and the interpreter path, both present at --rev
  preflight_selftest              exit 0 with cases>=11 failures=0, run from the bytes at --rev

Exit codes: 0 met; 1 not met (the reason list names each false clause); 2 could-not-evaluate
(unknown revision, freeze not an ancestor, SKILL.md absent, `frozen_path_changed` for a
commit inside FREEZE..REV touching the claims file or `tools/round-45/`).

Reads Git objects only; the interpreter's `--selftest` runs in a private directory under
$HYAKU_SCRATCH or $TMPDIR, which is removed before exit.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

MARKER = "<!-- freeze-integrity-table v1 -->"
PREFLIGHT = "tools/round-45/frozen-path-preflight.py"
CLAIMS = "plans/round-45-claims.md"
FROZEN = [CLAIMS, "tools/round-45"]
REF = re.compile(r"((?:corpus/(?:knowledge|lessons)|plans)/[A-Za-z0-9._-]+\.md)(?::(\d+)(?:-(\d+))?)?")


def git(root, *args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True, text=True)


def show(root, rev, path):
    r = git(root, "show", f"{rev}:{path}")
    return r.stdout if r.returncode == 0 else None


def scratch_dir():
    base = os.environ.get("HYAKU_SCRATCH") or os.environ.get("TMPDIR") or tempfile.gettempdir()
    root = os.path.join(base, "kaidoku-r45")
    os.makedirs(root, exist_ok=True)
    return tempfile.mkdtemp(dir=root, prefix="c1-")


def frozen_path_changed(root, freeze, rev):
    log = git(root, "log", "--name-only", "--format=", f"{freeze}..{rev}", "--", *FROZEN)
    if log.returncode != 0:
        return None
    return sorted({p for p in log.stdout.splitlines() if p.strip()})


def craft_blocks(skill):
    section = skill.split("## Queue-drain craft ", 1)[1].split("\n## ", 1)[0]
    return re.split(r"(?m)^- \*\*", section)[1:]


def block_table(block):
    """Return (header_cells, data_rows) of the first markdown table in the block."""
    lines = [l.strip() for l in block.splitlines() if l.strip().startswith("|")]
    if len(lines) < 3:
        return [], []
    header = [c.strip().strip("`").lower() for c in lines[0].strip("|").split("|")]
    rows = []
    for line in lines[1:]:
        if re.fullmatch(r"\|[\s:|-]+\|", line):
            continue
        rows.append([c.strip() for c in line.strip("|").split("|")])
    return header, rows


def unresolved_refs(root, rev, block, line_counts):
    missing = []
    total = 0
    for name, first, last in REF.findall(block):
        total += 1
        present = git(root, "cat-file", "-e", f"{rev}:{name}").returncode == 0
        if not present:
            missing.append(name)
            continue
        count = line_counts.get(name)
        if count is None:
            body = show(root, rev, name) or ""
            count = line_counts[name] = len(body.splitlines())
        end = int(last or first or 1)
        if not (1 <= int(first or 1) <= end <= count):
            missing.append(f"{name}:{first or 1}-{last or first or 1}")
    return total, missing


def run_preflight(root, rev, work):
    body = show(root, rev, PREFLIGHT)
    if body is None:
        return {"ok": False, "reason": "interpreter absent at rev"}
    path = os.path.join(work, "frozen-path-preflight.py")
    with open(path, "w") as fh:
        fh.write(body)
    env = dict(os.environ, TMPDIR=work, HYAKU_SCRATCH=work)
    env.pop("GIT_DIR", None)
    proc = subprocess.run([sys.executable, "-I", "-B", path, "--selftest"],
                          capture_output=True, text=True, env=env, timeout=300)
    m = re.search(r"PREFLIGHT_SELFTEST: cases=(\d+) failures=(\d+)", proc.stdout)
    cases = int(m.group(1)) if m else -1
    failures = int(m.group(2)) if m else -1
    ok = proc.returncode == 0 and cases >= 11 and failures == 0
    return {"ok": ok, "exit": proc.returncode, "cases": cases, "failures": failures}


def evaluate(root, freeze, rev, run_selftest=True):
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

    skill = show(root, tip, "SKILL.md")
    if skill is None:
        return 2, {"reason": "SKILL.md absent at rev"}

    blocks = craft_blocks(skill)
    rule_blocks = len(blocks)
    marked = [b for b in blocks if MARKER in b]
    block22_present = len(marked)
    rows, header, unresolved, refs = 0, [], [], 0
    bad_exit = []
    cites = {"S140": False, "interpreter": False}
    if block22_present == 1:
        block = marked[0]
        header, table_rows = block_table(block)
        rows = len(table_rows)
        exit_col = next((i for i, h in enumerate(header) if "exit" in h), None)
        for row in table_rows:
            if exit_col is None or exit_col >= len(row) or row[exit_col].strip("` ") not in {"0", "1", "2"}:
                bad_exit.append(row)
        refs, unresolved = unresolved_refs(root, tip, block, {})
        cites["S140"] = bool(re.search(r"\bS140\b", block))
        cites["interpreter"] = PREFLIGHT in block
    interpreter_present = git(root, "cat-file", "-e", f"{tip}:{PREFLIGHT}").returncode == 0

    selftest = {"ok": False, "skipped": True}
    if run_selftest and block22_present == 1:
        work = scratch_dir()
        try:
            selftest = run_preflight(root, tip, work)
        finally:
            shutil.rmtree(work, ignore_errors=True)

    header_ok = all(any(k in h for h in header) for k in ("trigger", "arm", "exit", "receipt"))
    reasons = []
    if rule_blocks < 22:
        reasons.append(f"rule_blocks {rule_blocks} != 22")
    if block22_present != 1:
        reasons.append(f"block22_present {block22_present} != 1")
    if rows < 8:
        reasons.append(f"block22_rows {rows} < 8")
    if not header_ok:
        reasons.append("block22 table header lacks trigger/arm/exit/receipt")
    if bad_exit:
        reasons.append(f"block22 exit cells outside {{0,1,2}}: {len(bad_exit)}")
    if unresolved:
        reasons.append(f"unresolved citations: {unresolved}")
    if refs < 4:
        reasons.append(f"block22_refs {refs} < 4")
    for key in ("S140", "interpreter"):
        if block22_present == 1 and not cites[key]:
            reasons.append(f"block22 does not cite {key}")
    if not interpreter_present:
        reasons.append("interpreter absent at rev")
    if block22_present == 1 and not selftest.get("ok"):
        reasons.append(f"preflight selftest {selftest}")

    receipt = {
        "counter": "round-45-c1",
        "freeze": base,
        "rev": tip,
        "rule_blocks": rule_blocks,
        "block22_present": block22_present,
        "block22_rows": rows,
        "block22_refs": refs,
        "block22_unresolved_citations": unresolved,
        "block22_cites": cites,
        "block22_header_ok": header_ok,
        "preflight_selftest": selftest,
        "interpreter_present": interpreter_present,
        "frozen_path_changed": [],
        "met_target": not reasons,
        "failing": reasons,
    }
    return (0 if not reasons else 1), receipt


# --- selftest ---------------------------------------------------------------

CRAFT_HEAD = "# SKILL\n\n## Queue-drain craft (test)\n\n"
GOOD_ROW = "| post-freeze commit touches a frozen path | commit arm | 1 | `--json-out` receipt |\n"
GOOD_HEADER = "| trigger | arm | exit | receipt |\n|---|---|---|---|\n"


def good_block(refs=("corpus/lessons/round-44.md:38", "plans/round-45-claims.md:1",
                     "corpus/lessons/round-44-verifier-spotcheck.md:12",
                     "corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:9")):
    body = "- **22. Freeze integrity.** " + MARKER + " S140 " + PREFLIGHT + "\n\n"
    body += GOOD_HEADER + GOOD_ROW * 8
    body += "\n  Refs: " + ", ".join(refs) + "\n\n"
    return body


def make_repo(d, skill, preflight_body, claims=True):
    git(d, "init", "-q")
    git(d, "config", "user.email", "c1@selftest")
    git(d, "config", "user.name", "c1 selftest")
    paths = {
        "SKILL.md": skill,
        "tools/round-45/frozen-path-preflight.py": preflight_body,
        "corpus/lessons/round-44.md": "l1\n" * 60,
        "corpus/lessons/round-44-verifier-spotcheck.md": "s1\n" * 40,
        "corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md": "k1\n" * 30,
    }
    if claims:
        paths["plans/round-45-claims.md"] = "claims\n" * 10
    for p, text in paths.items():
        full = os.path.join(d, p)
        os.makedirs(os.path.dirname(full) or d, exist_ok=True)
        with open(full, "w") as fh:
            fh.write(text)
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", "freeze")
    return git(d, "rev-parse", "HEAD").stdout.strip()


def skill_with(n_plain, block=""):
    text = CRAFT_HEAD
    for i in range(1, n_plain + 1):
        text += f"- **{i}. Plain rule {i}.** body\n"
    return text + block


STUB_OK = ("#!/usr/bin/env python3\n"
           "import sys\n"
           "print('PREFLIGHT_SELFTEST: cases=11 failures=0')\n"
           "sys.exit(0)\n")
STUB_RED = ("#!/usr/bin/env python3\n"
            "import sys\n"
            "print('PREFLIGHT_SELFTEST: cases=11 failures=1')\n"
            "sys.exit(1)\n")


def selftest():
    base = scratch_dir()
    cases = []

    def case(name, expect, fn):
        d = tempfile.mkdtemp(dir=base)
        try:
            code, receipt = fn(d)
        except Exception as exc:
            code, receipt = ("crash", {"error": f"{type(exc).__name__}: {exc}"})
        cases.append({"case": name, "expect": expect, "got": code, "ok": code == expect,
                      "receipt": receipt})

    def green(d):
        f = make_repo(d, skill_with(21, good_block()), STUB_OK)
        return evaluate(d, f, f)

    def relabelled(d):
        block = good_block().replace("22. Freeze integrity.", "20. Freeze integrity.")
        f = make_repo(d, skill_with(20, block), STUB_OK)
        return evaluate(d, f, f)

    def thin_table(d):
        block = good_block().replace(GOOD_ROW * 8, GOOD_ROW * 3)
        f = make_repo(d, skill_with(21, block), STUB_OK)
        return evaluate(d, f, f)

    def bad_citation(d):
        block = good_block(refs=("corpus/lessons/round-44.md:9999", "plans/round-45-claims.md:1",
                                 "corpus/lessons/round-44-verifier-spotcheck.md:12",
                                 "corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:9"))
        f = make_repo(d, skill_with(21, block), STUB_OK)
        return evaluate(d, f, f)

    def no_s140(d):
        block = good_block().replace(" S140 ", " ")
        f = make_repo(d, skill_with(21, block), STUB_OK)
        return evaluate(d, f, f)

    def interpreter_fails(d):
        f = make_repo(d, skill_with(21, good_block()), STUB_RED)
        return evaluate(d, f, f)

    def bad_exit_cell(d):
        block = good_block().replace("| 1 |", "| ok |")
        f = make_repo(d, skill_with(21, block), STUB_OK)
        return evaluate(d, f, f)

    def frozen_touched(d):
        f = make_repo(d, skill_with(21, good_block()), STUB_OK)
        with open(os.path.join(d, "plans/round-45-claims.md"), "a") as fh:
            fh.write("late edit\n")
        git(d, "add", "-A")
        git(d, "commit", "-q", "-m", "touch claims after freeze")
        r = git(d, "rev-parse", "HEAD").stdout.strip()
        return evaluate(d, f, r)

    def unknown_rev(d):
        f = make_repo(d, skill_with(21, good_block()), STUB_OK)
        return evaluate(d, f, "0" * 40)

    case("green", 0, green)
    case("red-relabelled-21-block", 1, relabelled)
    case("red-thin-table", 1, thin_table)
    case("red-bad-citation", 1, bad_citation)
    case("red-no-s140", 1, no_s140)
    case("red-interpreter-fails", 1, interpreter_fails)
    case("red-bad-exit-cell", 1, bad_exit_cell)
    case("red-frozen-touched-is-exit-2", 2, frozen_touched)
    case("red-unknown-rev", 2, unknown_rev)

    failures = [c for c in cases if not c["ok"]]
    for c in cases:
        print(json.dumps({"selftest": c["case"], "expect": c["expect"], "got": c["got"],
                          "ok": c["ok"]}, sort_keys=True))
    print("C1_SELFTEST: cases=%d failures=%d" % (len(cases), len(failures)))
    shutil.rmtree(base, ignore_errors=True)
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
        return selftest()
    if not (args.root and args.freeze and args.rev):
        print(json.dumps({"counter": "round-45-c1", "verdict": "could_not_evaluate",
                          "reason": "usage: --root --freeze --rev (or --selftest)"}))
        return 2
    code, receipt = evaluate(os.path.abspath(args.root), args.freeze, args.rev)
    if code == 2:
        receipt = {"counter": "round-45-c1", "verdict": "could_not_evaluate", **receipt}
    if args.json_out:
        with open(args.json_out, "w") as fh:
            json.dump(receipt, fh, indent=1, sort_keys=True)
    print(json.dumps(receipt, sort_keys=True))
    return code


if __name__ == "__main__":
    sys.exit(main())
