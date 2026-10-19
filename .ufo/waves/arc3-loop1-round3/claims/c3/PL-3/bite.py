#!/usr/bin/env python3
"""PL-3 bite suite: per-entry mutation falsification for the arc3 fragment.

For every proposed entry, serve the cited files from memory (no repo writes, no
mutations to real files) and verify:
  PASS  the entry is silent on the real content;
  BITE  a minimal drift mutation of its needle target/citing line reddens it,
        with the expected finding class and only that entry id reported.
Extracted entries get two mutations: a wrong stated number (citing line) and a
blanked needle (cited target line).
"""
import hashlib
import importlib.util
import json
import pathlib
import re
import subprocess
import sys

REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
OUT = pathlib.Path("/var/tmp/pl3")
PROBE = f"{REPO}/.ufo/gates/citation-drift/citation-drift-probe.py"

spec = importlib.util.spec_from_file_location("probe", PROBE)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)

frag = json.load(open(OUT / "entries-arc3.json"))
ENTRIES = frag["entries"]


def git_show(path):
    p = subprocess.run(["git", "-C", REPO, "show", f"HEAD:{path}"], capture_output=True)
    if p.returncode != 0:
        return None
    return p.stdout.decode("utf-8", "replace")


class MemTree:
    """Serves cited files from an in-memory dict; faithful to Tree's contract."""

    def __init__(self, files):
        self.files = files              # path -> text
        self.reported = set()

    def lines(self, target):
        if target not in self.files:
            self.reported.add(target)
            return None, "absent (memtree)"
        return self.files[target].splitlines(), None


def check(entry, files):
    f = probe.Findings()
    probe.check_entry(dict(entry), MemTree(files), f)
    return f


def mutate_line(text, needle, repl):
    """Replace ALL occurrences of `needle` on every matching line (a needle
    class that appears more than once must still fail closed when removed)."""
    lines = text.splitlines()
    hits = 0
    for i, l in enumerate(lines):
        if re.search(needle, l):
            lines[i] = re.sub(needle, repl, l)
            hits += 1
    if not hits:
        raise AssertionError("needle %r not found for mutation" % needle[:40])
    return "\n".join(lines) + "\n"


results = []
bites = passes = fails = 0
for e in ENTRIES:
    eid = e["id"]
    kind = e["kind"]
    src = e["file"]
    tgt = e.get("target", src)
    files = {}
    for p in ({src, tgt}):
        txt = git_show(p)
        if txt is None:
            files[p] = None
        else:
            files[p] = txt
    # control: silent on real content
    f0 = check(e, files)
    ctl_ok = not f0.rows
    # mutation
    if kind == "extracted":
        # m1: citing line states a number past the cited file's EOF (the
        # stated-number drift the extracted kind exists to catch)
        line_no = e["line"]
        lines = files[src].splitlines()
        m = re.search(e["pattern"], lines[line_no - 1])
        assert m, (eid, "pattern absent at citing line")
        g = e.get("target_group", 1)
        wrong = len(files[tgt].splitlines()) + 7
        mutated = lines[line_no - 1]
        idx = m.start(g)
        mutated = mutated[:idx] + str(wrong) + mutated[idx + len(m.group(g)):]
        lines[line_no - 1] = mutated
        f1 = check(e, {**files, src: "\n".join(lines) + "\n"})
        # m2: cited target's needle content blanked
        files2 = dict(files)
        files2[tgt] = mutate_line(files[tgt], e["must_match"], "ZZ_PL3_BLANKED")
        f2 = check(e, files2)
    else:
        files2 = dict(files)
        files2[tgt] = mutate_line(files[tgt], e["must_match"], "ZZ_PL3_BLANKED")
        f1 = f2 = check(e, files2)
    def bite(f):
        return bool(f.rows) and f.ids() & {
            "citation_dead", "citation_out_of_range", "citation_file_absent",
            "record_word_missing"} and {r[1] for r in f.rows} <= {eid}
    r = {"id": eid, "kind": kind, "control_silent": ctl_ok,
         "m1_classes": sorted(f1.ids()), "m1_bite": bite(f1),
         "m2_classes": sorted(f2.ids()), "m2_bite": bite(f2)}
    results.append(r)
    passes += ctl_ok
    bites += (r["m1_bite"] and r["m2_bite"])
    fails += (not (ctl_ok and r["m1_bite"] and r["m2_bite"]))

for r in results:
    flag = "OK " if (r["control_silent"] and r["m1_bite"] and r["m2_bite"]) else "FAIL"
    print(f"{flag} {r['id']:34} kind={r['kind']:9} ctl_silent={r['control_silent']} "
          f"m1={r['m1_classes']} m2={r['m2_classes']}")
print(f"\nBITE_SUITE: entries={len(results)} control_silent={passes} both_mutations_bite={bites} failed={fails}")
(OUT / "bite-suite.out").write_text(
    "\n".join(f"{r['id']}\t{r['kind']}\tcontrol={r['control_silent']}\tm1={r['m1_classes']}\tm2={r['m2_classes']}"
              for r in results) +
    f"\nBITE_SUITE: entries={len(results)} control_silent={passes} both_mutations_bite={bites} failed={fails}\n")
sys.exit(1 if fails else 0)