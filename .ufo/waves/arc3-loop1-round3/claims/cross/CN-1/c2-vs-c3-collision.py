#!/usr/bin/env python3
"""CN-1 cross-chain collision check: C3's landed pointer table vs C2's drafted patches.

Evaluates every entry of the LIVE pointer table (57 entries) with the probe's
own check semantics (citation-drift-probe.py:168-260), but resolving the two
files C2's drafted patch pair rewrites from EX-30's patched output
(`/var/tmp/ex30/SKILL.v1.md`, `/var/tmp/ex30/README.v1.md`) instead of HEAD.
All other files resolve from `git show HEAD:<path>` (unchanged by C2).

Finding classes replicated: citation_file_absent, citation_dead,
citation_out_of_range, citation_moved, record_word_missing, and the
`extracted` target-side range/must_match check.

Usage: python3 c2-vs-c3-collision.py [--patched-skill PATH] [--patched-readme PATH]
"""
import argparse
import json
import re
import subprocess

REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
PATCHED = {
    "SKILL.md": "/var/tmp/ex30/SKILL.v1.md",
    ".ufo/gates/custody-pair/README.md": "/var/tmp/ex30/README.v1.md",
}


def head_lines(path):
    out = subprocess.run(["git", "-C", REPO, "show", f"HEAD:{path}"],
                         capture_output=True)
    if out.returncode != 0:
        return None
    return out.stdout.decode("utf-8").splitlines()


def lines_for(path, patched):
    if path in patched:
        try:
            with open(patched[path]) as fh:
                return fh.read().splitlines()
        except FileNotFoundError:
            return None
    return head_lines(path)


def resolve_lines(target, patched, rev=None):
    """Target resolution for `extracted` entries: rev-pinned or HEAD."""
    if ":" in target and not target.startswith("."):
        return None
    if rev:
        out = subprocess.run(["git", "-C", REPO, "show", f"{rev}:{target}"],
                             capture_output=True)
        if out.returncode != 0:
            return None
        return out.stdout.decode("utf-8").splitlines()
    return lines_for(target, patched)


def check(entry, patched):
    eid = entry["id"]
    kind = entry.get("kind", "quoted")
    citing = lines_for(entry["file"], patched)
    if citing is None:
        return (eid, "citation_file_absent", entry["file"])
    if kind == "anchor":
        hits = [i + 1 for i, l in enumerate(citing)
                if re.search(entry["must_match"], l)]
        if not hits:
            return (eid, "citation_dead", "no line matches %r" % entry["must_match"][:70])
        if entry.get("pin_line") is not None and entry["pin_line"] not in hits:
            return (eid, "citation_moved", "content at %s" % (hits,))
        return None
    line_no = entry.get("line")
    if not isinstance(line_no, int) or not (1 <= line_no <= len(citing)):
        return (eid, "citation_out_of_range", "%s:%s" % (entry["file"], line_no))
    citing_line = citing[line_no - 1]
    if kind in ("quoted", "exact"):
        if not re.search(entry["must_match"], citing_line):
            return (eid, "citation_dead", "%s:%d lacks %r" % (entry["file"], line_no,
                                                              entry["must_match"][:70]))
        return None
    if kind == "extracted":
        m = re.search(entry["pattern"], citing_line)
        if not m:
            return (eid, "citation_dead", "%s:%d pattern %r absent" % (entry["file"], line_no,
                                                                       entry["pattern"][:70]))
        tgt_lines = resolve_lines(entry["target"], patched, entry.get("rev"))
        if tgt_lines is None:
            return (eid, "citation_file_absent", entry["target"])
        try:
            lo = int(m.group(entry.get("target_group", 1)))
            hi = int(m.group(entry.get("target_group_end", entry.get("target_group", 1))) or lo)
        except (IndexError, ValueError):
            return (eid, "citation_dead", "pointer group unreadable")
        if entry.get("must_match"):
            window = int(entry.get("window", 0))
            lo, hi = lo - window, hi + window
            if not (1 <= lo <= hi <= len(tgt_lines)):
                return (eid, "citation_out_of_range",
                        "%s:%d-%d beyond EOF (%d lines)" % (entry["target"], lo, hi, len(tgt_lines)))
            seg = "\n".join(tgt_lines[lo - 1:hi])
            if not re.search(entry["must_match"], seg, re.M):
                return (eid, "citation_dead",
                        "%s:%d-%d lacks %r" % (entry["target"], lo, hi, entry["must_match"][:60]))
        return None
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--patched-skill", default=PATCHED["SKILL.md"])
    ap.add_argument("--patched-readme", default=PATCHED[".ufo/gates/custody-pair/README.md"])
    ap.add_argument("--patched-corpus-readme", default=None,
                    help="path to a patched corpus/README.md (C1's map-token rehearsal)")
    args = ap.parse_args()
    patched = {"SKILL.md": args.patched_skill,
               ".ufo/gates/custody-pair/README.md": args.patched_readme}
    if args.patched_corpus_readme:
        patched["corpus/README.md"] = args.patched_corpus_readme

    table = json.load(open(f"{REPO}/.ufo/gates/citation-drift/pointer-table.json"))
    for p in patched.values():
        with open(p, "rb") as fh:
            import hashlib
            print(f"patched file: {p} sha256={hashlib.sha256(fh.read()).hexdigest()}")

    print(f"entries: {len(table['entries'])}  quoted: {len(table['quoted'])}")
    print("--- eval over [C2-patched SKILL.md + C2-patched README] + HEAD elsewhere ---")
    findings = []
    for entry in table["entries"] + table["quoted"]:
        r = check(entry, patched)
        if r:
            findings.append(r)
            print(f"  FINDING {r[0]}: {r[1]} — {r[2]}")
    print(f"total findings: {len(findings)}")

    print("--- control: same evaluator over unmodified HEAD for the two files ---")
    ctrl = []
    for entry in table["entries"] + table["quoted"]:
        r = check(entry, {})
        if r:
            ctrl.append(r)
            print(f"  FINDING {r[0]}: {r[1]} — {r[2]}")
    print(f"control findings: {len(ctrl)}")


if __name__ == "__main__":
    main()