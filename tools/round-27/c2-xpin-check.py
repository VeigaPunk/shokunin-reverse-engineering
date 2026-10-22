#!/usr/bin/env python3
"""R27-C2 checker: cross-pin evidence-ID attribution capability (rea-agents 6.5.0 vs 6.7.0).

Committed before the capability tool exists. It counts four things at REV:

  A. r26_rows_ok  — the tool at REV (tools/round-27/xpin-attribute.mjs, run with node) is fed
     the 24 committed round-26 envelopes. A row is ok when the tool prints the stored id, an
     id65 equal to this checker's 6.5.0 recompute, an id67 equal to this checker's 6.7.0
     recompute, and the attribution derived from those three. Target 24/24.
  B. red_ok       — three generated red envelopes (one byte of normalized_result changed ->
     none; relationship_coverage null with the id re-minted under the 6.7.0 rule -> 6.7.0;
     relationship_coverage set and the id re-minted -> both). Target 3/3.
  C. capability_row — SCORECARD.md `## Capabilities` has a table row naming the tool path.
  D. source_row   — SOURCES.md has a row that is new since BASE, status mined, opened
     2026-10-22, whose source cell names the installed 6.7.0 package root, and whose id
     appears as a table row in corpus/lessons/round-27.md `## Gate`.

This checker's own recompute is independent of the tool: the 6.5.0 rule comes from
tools/round-26/recompute-ids.py at REV (standard library); the 6.7.0 rule is the same
projection with relationship_coverage always present (evidence.js:178 in the 6.7.0 package,
sha256 a3fb9f02..., against :175-177 in 6.5.0). The checker also verifies the two installed
package files it relies on still carry their frozen sha256 values.

Usage:
  c2-xpin-check.py --root LANE --rev REV [--base BASE] [--tool-cmd CMD]
  c2-xpin-check.py --selftest
Exit 0 when A=24/24, B=3/3, C=1, D=1; 1 otherwise; 2 on input error.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile

TOOL_PATH = "tools/round-27/xpin-attribute.mjs"
RECOMPUTE_PATH = "tools/round-26/recompute-ids.py"
R26_ENVELOPES = "corpus/evidence/round-26/c1/envelopes"
SCORECARD = "SCORECARD.md"
SOURCES = "corpus/SOURCES.md"
LESSON = "corpus/lessons/round-27.md"
BASE = "cd32264f7ee356a9c0f48bd8e3fcdac222db22a0"
OPENED = "2026-10-22"
PKG65 = "/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents"
PKG67 = "/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents"
PKG67_MARK = "a1722018f28f9df2"
FROZEN_FILES = {
    PKG65 + "/package.json": "a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c",
    PKG65 + "/dist/domain/evidence.js": "f992d93eaf228bf8d7c6bc3bf566f4ff4554b53299f35cd7ff29e3b18a78dcff",
    PKG67 + "/package.json": "3f6c47fb12c8388f291a21e7f99a876495d03aee671b3b6a0708dd12d6ebb570",
    PKG67 + "/dist/domain/evidence.js": "a3fb9f028e04e3a14f4c2269048e194ad2a8acb884b0e403212bb977d329c0fb",
}
R26_TOTAL = 24
ATTRIBUTIONS = ("6.5.0", "6.7.0", "both", "none")


class InputError(Exception):
    pass


def git(root, *args):
    proc = subprocess.run(["git", "-C", root, *args], capture_output=True)
    if proc.returncode != 0:
        raise InputError("git %s failed: %s" % (" ".join(args), proc.stderr.decode(errors="replace").strip()))
    return proc.stdout.decode()


def show(root, rev, path):
    proc = subprocess.run(["git", "-C", root, "show", "%s:%s" % (rev, path)], capture_output=True)
    return proc.stdout if proc.returncode == 0 else None


def load_module(raw, name):
    tmp = tempfile.mkdtemp(prefix="r27c2-")
    path = os.path.join(tmp, name + ".py")
    with open(path, "wb") as handle:
        handle.write(raw)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    shutil.rmtree(tmp, ignore_errors=True)
    return module


def ids_for(recompute, data):
    """Return (id under the 6.5.0 rule, id under the 6.7.0 rule). Canonical JSON orders keys."""
    id65 = recompute.compute_evidence_id(data)
    projection = recompute.semantic_projection(data)
    projection["relationship_coverage"] = data.get("relationship_coverage")
    id67 = "ev_" + recompute.digest_canonical_value(projection)
    return id65, id67


def attribution(stored, id65, id67):
    if stored == id65 and stored == id67:
        return "both"
    if stored == id65:
        return "6.5.0"
    if stored == id67:
        return "6.7.0"
    return "none"


def run_tool(tool_cmd, files):
    proc = subprocess.run(tool_cmd + ["--pkg65", PKG65, "--pkg67", PKG67, *files], capture_output=True, timeout=600)
    rows = {}
    for line in proc.stdout.decode("utf-8", errors="replace").split("\n"):
        cells = line.split("\t")
        if len(cells) == 5 and cells[0] in files:
            rows.setdefault(cells[0], []).append(cells[1:])
    return proc.returncode, rows, proc.stderr.decode("utf-8", errors="replace")[-800:]


def check_rows(recompute, tool_cmd, cases, workdir):
    """cases: list of (name, envelope_dict, expected_attribution or None). Returns ok count and reasons."""
    files, expected = [], {}
    for name, env, want in cases:
        path = os.path.join(workdir, name)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(env, handle)
        data = env["data"]
        id65, id67 = ids_for(recompute, data)
        stored = data.get("evidence_id")
        derived = attribution(stored, id65, id67)
        if want is not None and derived != want:
            raise InputError("fixture %s derives %s, expected %s" % (name, derived, want))
        files.append(path)
        expected[path] = [stored, id65, id67, derived]
    code, rows, stderr = run_tool(tool_cmd, files)
    ok, reasons = 0, []
    if code != 0:
        reasons.append("tool exit %d: %s" % (code, stderr.strip()[:300]))
    for path in files:
        got = rows.get(path)
        if got is None or len(got) != 1:
            reasons.append("%s: tool printed %d lines" % (os.path.basename(path), 0 if got is None else len(got)))
            continue
        if got[0] != expected[path]:
            reasons.append("%s: tool %s, checker %s" % (os.path.basename(path), got[0][3:], expected[path][3:]))
            continue
        ok += 1
    return ok, reasons, expected


def red_cases(recompute, envelopes):
    """Build the three red envelopes from round-26 envelopes."""
    null_cov = next(e for e in envelopes if e["data"].get("relationship_coverage") is None)
    reds = []
    one = copy.deepcopy(null_cov)
    nr = one["data"]["normalized_result"]
    one["data"]["normalized_result"] = {"tampered": True, "was": nr}
    reds.append(("red-tampered.json", one, "none"))
    two = copy.deepcopy(null_cov)
    two["data"]["evidence_id"] = ids_for(recompute, two["data"])[1]
    reds.append(("red-minted-67.json", two, "6.7.0"))
    three = copy.deepcopy(null_cov)
    three["data"]["relationship_coverage"] = {"status": "selftest", "edges": 0}
    three["data"]["evidence_id"] = ids_for(recompute, three["data"])[0]
    reds.append(("red-coverage-set.json", three, "both"))
    return reds


def section_lines(text, heading):
    out, inside = [], False
    for line in text.split("\n"):
        if line.startswith("## "):
            if inside:
                break
            inside = line.strip() == heading
            continue
        if inside:
            out.append(line)
    return out


def sources_rows(text):
    rows = {}
    for line in text.split("\n"):
        match = re.match(r"^\| (S\d{3}) \|", line)
        if match:
            rows[match.group(1)] = [cell.strip() for cell in line.strip().strip("|").split("|")]
    return rows


def capability_row(root, rev):
    raw = show(root, rev, SCORECARD)
    if raw is None:
        return 0
    for line in section_lines(raw.decode("utf-8"), "## Capabilities"):
        if line.startswith("|") and TOOL_PATH in line and not line.startswith("|---"):
            return 1
    return 0


def source_row(root, rev, base):
    raw, raw_base, lesson = show(root, rev, SOURCES), show(root, base, SOURCES), show(root, rev, LESSON)
    if raw is None or lesson is None:
        return 0, None
    rows = sources_rows(raw.decode("utf-8"))
    base_rows = sources_rows(raw_base.decode("utf-8")) if raw_base else {}
    gate = set()
    for line in section_lines(lesson.decode("utf-8"), "## Gate"):
        match = re.match(r"^\| (S\d{3}) \|", line)
        if match:
            gate.add(match.group(1))
    for sid, row in sorted(rows.items()):
        if sid in base_rows or len(row) < 11:
            continue
        if PKG67_MARK in row[1] and row[7] == "mined" and row[8] == OPENED and sid in gate:
            return 1, sid
    return 0, None


def frozen_files_ok():
    bad = []
    for path, want in FROZEN_FILES.items():
        try:
            got = hashlib.sha256(open(path, "rb").read()).hexdigest()
        except OSError:
            got = None
        if got != want:
            bad.append(path)
    return bad


def measure(root, rev, base, tool_cmd=None, out=sys.stdout):
    bad = frozen_files_ok()
    if bad:
        raise InputError("installed package files changed or missing: %s" % ", ".join(bad))
    raw_rc = show(root, rev, RECOMPUTE_PATH)
    if raw_rc is None:
        raise InputError("%s absent at %s" % (RECOMPUTE_PATH, rev))
    recompute = load_module(raw_rc, "recompute_ids_r27c2")
    names = [n for n in git(root, "ls-tree", "--name-only", rev, R26_ENVELOPES + "/").split("\n") if n.endswith(".json")]
    if len(names) != R26_TOTAL:
        raise InputError("expected %d round-26 envelopes at %s, found %d" % (R26_TOTAL, rev, len(names)))
    envelopes = [(os.path.basename(n), json.loads(show(root, rev, n).decode("utf-8"))) for n in sorted(names)]
    work = tempfile.mkdtemp(prefix="r27c2-run-", dir="/fast/scratch/hyaku" if os.path.isdir("/fast/scratch/hyaku") else None)
    try:
        if tool_cmd is None:
            tool = show(root, rev, TOOL_PATH)
            if tool is None:
                r26_ok, reasons26, red_ok, reasons_red, expected = 0, ["%s absent at REV" % TOOL_PATH], 0, ["tool absent"], {}
            else:
                tool_file = os.path.join(work, "xpin-attribute.mjs")
                with open(tool_file, "wb") as handle:
                    handle.write(tool)
                tool_cmd = ["node", tool_file]
        if tool_cmd is not None:
            os.makedirs(os.path.join(work, "r26"))
            os.makedirs(os.path.join(work, "red"))
            r26_ok, reasons26, expected = check_rows(recompute, tool_cmd, [(n, e, None) for n, e in envelopes], os.path.join(work, "r26"))
            red_ok, reasons_red, _ = check_rows(recompute, tool_cmd, red_cases(recompute, [e for _, e in envelopes]), os.path.join(work, "red"))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    dist = {a: 0 for a in ATTRIBUTIONS}
    for row in expected.values():
        dist[row[3]] += 1
    cap = capability_row(root, rev)
    src, sid = source_row(root, rev, base)
    for reason in reasons26 + reasons_red:
        print("FAIL " + reason, file=out)
    print("checker attribution of the round-26 envelopes: " + " ".join("%s=%d" % kv for kv in dist.items()), file=out)
    print("r26_rows_ok=%d/%d red_ok=%d/3 capability_row=%d source_row=%d%s rev=%s"
          % (r26_ok, R26_TOTAL, red_ok, cap, src, "" if sid is None else " (" + sid + ")", rev), file=out)
    return 0 if (r26_ok == R26_TOTAL and red_ok == 3 and cap == 1 and src == 1) else 1


# ------------------------------------------------------------------ selftest

STUB = r'''
import json, sys, importlib.util
spec = importlib.util.spec_from_file_location("rc", sys.argv[1]); rc = importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)
mode = sys.argv[2]
sys.path.insert(0, sys.argv[3]); import importlib
chk = importlib.util.spec_from_file_location("chk", sys.argv[3]); ck = importlib.util.module_from_spec(chk); chk.loader.exec_module(ck)
args = sys.argv[4:]
files = [a for i, a in enumerate(args) if not a.startswith("--") and (i == 0 or args[i-1] not in ("--pkg65", "--pkg67"))]
for f in files:
    d = json.load(open(f))["data"]
    s = d.get("evidence_id"); a, b = ck.ids_for(rc, d)
    if mode == "lazy": a = b = s
    if mode == "only65": b = a
    if mode == "skip" and f.endswith("analyze-base.json"): continue
    print("\t".join([f, s, a, b, ck.attribution(s, a, b)]))
'''


def selftest():
    here = os.path.dirname(os.path.abspath(__file__))
    lane = os.path.abspath(os.path.join(here, "..", ".."))
    scratch = tempfile.mkdtemp(prefix="r27c2-selftest-", dir="/fast/scratch/hyaku" if os.path.isdir("/fast/scratch/hyaku") else None)
    stub = os.path.join(scratch, "stub.py")
    open(stub, "w").write(STUB)
    me = os.path.abspath(__file__)
    failures = 0
    # The stub cases are anchored at fixed revisions, never at the live lane
    # HEAD: at HEAD the round-27 capability row and the S081 source row exist,
    # so the counter's exit code there followed later lane commits and the
    # correct-stub case could hold no verdict. C2_REV added the capability row,
    # BASE precedes it. correct-stub is measured at both, each with base == rev,
    # so no SOURCES row is new since the base and the refusal of the stub is
    # demanded whether or not the capability row exists at that revision.
    C2_REV = "97358f759a531f7ebc0354fb937d546da8d3b8bd"
    cases = [
        ("correct-stub", "correct", "r26_rows_ok=24/24 red_ok=3/3", [(C2_REV, C2_REV), (BASE, BASE)]),
        ("lazy-stub (echoes stored id for both pins; only the 3 both-rows pass)", "lazy", "r26_rows_ok=3/24 red_ok=1/3", [(C2_REV, BASE)]),
        ("only65-stub (no 6.7.0 rule; only the 3 both-rows pass)", "only65", "r26_rows_ok=3/24 red_ok=1/3", [(C2_REV, BASE)]),
        ("skip-stub (drops one envelope)", "skip", "r26_rows_ok=23/24", [(C2_REV, BASE)]),
    ]
    for name, mode, want, anchors in cases:
        ok = True
        for rev, base in anchors:
            rc = os.path.join(scratch, "recompute-%s.py" % rev[:8])
            open(rc, "wb").write(show(lane, rev, RECOMPUTE_PATH))
            buf = _Buffer()
            try:
                got = measure(lane, rev, base, tool_cmd=[sys.executable, stub, rc, mode, me], out=buf)
            except InputError as error:
                got, _ = 2, buf.write("input error: %s\n" % error)
            text = buf.getvalue()
            ok = ok and want in text and got == 1
            print("%s %s at %s: exit %d, expects %r | %s" % ("PASS" if ok else "FAIL", name, rev[:8], got, want, text.strip().split("\n")[-1]))
        failures += 0 if ok else 1
    # the default path with no tool at REV (the round base)
    buf = _Buffer()
    got = measure(lane, BASE, BASE, out=buf)
    ok = got == 1 and "r26_rows_ok=0/24 red_ok=0/3 capability_row=0 source_row=0" in buf.getvalue()
    failures += 0 if ok else 1
    print("%s tool-absent-at-base: exit %d | %s" % ("PASS" if ok else "FAIL", got, buf.getvalue().strip().split("\n")[-1]))
    # capability and source row parsing on fixtures
    ok = _rows_fixture(scratch)
    failures += 0 if ok else 1
    shutil.rmtree(scratch, ignore_errors=True)
    print("selftest cases=%d failures=%d" % (len(cases) + 2, failures))
    return 0 if failures == 0 else 1


def _rows_fixture(scratch):
    repo = os.path.join(scratch, "rows")
    subprocess.run(["git", "init", "-q", repo], check=True)
    env = dict(os.environ, GIT_AUTHOR_NAME="s", GIT_AUTHOR_EMAIL="s@invalid", GIT_COMMITTER_NAME="s", GIT_COMMITTER_EMAIL="s@invalid")

    def commit(files):
        for rel, text in files.items():
            os.makedirs(os.path.dirname(os.path.join(repo, rel)) or repo, exist_ok=True)
            open(os.path.join(repo, rel), "w").write(text)
        subprocess.run(["git", "-C", repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", repo, "commit", "-qm", "x"], check=True, env=env)
        return git(repo, "rev-parse", "HEAD").strip()

    row67 = "| S900 | 6.7.0 code `%s/dist` | code | A | s | a | t | mined | %s | r | u |\n" % (PKG67, OPENED)
    base = commit({SOURCES: "| S001 | %s old | code | A | s | a | t | mined | %s | r | u |\n" % (PKG67, OPENED),
                   SCORECARD: "## Capabilities\n\n| a | b |\n|---|---|\n", LESSON: "## Gate\n"})
    results = []
    good = commit({SOURCES: "| S001 | old |\n" + row67, LESSON: "## Gate\n\n| S900 | q |\n",
                   SCORECARD: "## Capabilities\n\n| a | b |\n|---|---|\n| x | `%s` |\n\n## Saturation\n" % TOOL_PATH})
    results.append(("good rows", capability_row(repo, good), source_row(repo, good, base)[0], (1, 1)))
    moved = commit({SCORECARD: "## Capabilities\n\n| a | b |\n\n## Saturation\n\n| x | `%s` |\n" % TOOL_PATH})
    results.append(("tool named outside ## Capabilities", capability_row(repo, moved), 1, (0, 1)))
    old = commit({SOURCES: "| S001 | %s old | code | A | s | a | t | mined | %s | r | u |\n" % (PKG67, OPENED), LESSON: "## Gate\n\n| S001 | q |\n"})
    results.append(("only a base-era row", 0, source_row(repo, old, base)[0], (0, 0)))
    nogate = commit({SOURCES: "| S001 | old |\n" + row67, LESSON: "## Gate\n\nnone\n\n## Mistakes\n\n| S900 | q |\n"})
    results.append(("row not in ## Gate", 0, source_row(repo, nogate, base)[0], (0, 0)))
    status = commit({SOURCES: "| S001 | old |\n" + row67.replace("| mined |", "| candidate |"), LESSON: "## Gate\n\n| S900 | q |\n"})
    results.append(("row status candidate", 0, source_row(repo, status, base)[0], (0, 0)))
    ok = True
    for name, cap, src, want in results:
        good_case = (cap, src) == want
        ok = ok and good_case
        print("%s rows-fixture %s: capability_row=%d source_row=%d want %s" % ("PASS" if good_case else "FAIL", name, cap, src, want))
    return ok


class _Buffer:
    def __init__(self):
        self.parts = []

    def write(self, text):
        self.parts.append(text)
        return len(text)

    def getvalue(self):
        return "".join(self.parts)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--root")
    parser.add_argument("--rev")
    parser.add_argument("--base", default=BASE)
    parser.add_argument("--tool-cmd", help="selftest only: command that replaces `node <tool at REV>`")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.root or not args.rev:
        parser.error("--root and --rev are required")
    try:
        rev = git(args.root, "rev-parse", "--verify", args.rev + "^{commit}").strip()
        return measure(args.root, rev, args.base, tool_cmd=shlex.split(args.tool_cmd) if args.tool_cmd else None)
    except InputError as error:
        print("input error: %s" % error, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
