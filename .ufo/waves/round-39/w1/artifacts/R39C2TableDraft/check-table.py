#!/usr/bin/env python3
"""Draft-only self-check for the round-39 SquashFS triage table.

This is NOT the frozen interpreter (tools/round-39/sqfs-triage.py is the L1's
to write). It implements the grammar exactly as the round-39 seat brief states
it and is used here only to prove two things about the drafted block:

  1. every data row has nine well-formed condition cells, and
  2. every envelope whose class is already known from committed evidence
     classifies to that class, with no row matched twice in the wrong order.

Usage: python3 check-table.py BLOCK.md [ENVELOPE.json ...]
Exit:  0 all expectations hold, 2 a malformed cell/table (grammar refusal).
"""
import fnmatch
import json
import sys

MARKER = "<!-- sqfs-triage-table v1 -->"
HEADER = ["label", "handler", "gap kinds", "dependencies",
          "-be in child argv", "symlink removed", "published files",
          "cause -> action", "source"]


def refuse(message):
    print(message, file=sys.stderr)
    sys.exit(2)


def section_text(path):
    """The first markdown table after the marker, to the end of the file."""
    text = open(path, encoding="utf-8").read()
    idx = text.find(MARKER)
    if idx < 0:
        refuse("exit 2: no sqfs-triage-table marker")
    lines = text[idx + len(MARKER):].splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.lstrip().startswith("|"):
            start = i
            break
    if start is None:
        refuse("exit 2: no table after the marker")
    table = []
    for line in lines[start:]:
        if not line.lstrip().startswith("|"):
            break
        table.append(line)
    return table


def cells(line):
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    return [c.strip() for c in body.split("|")]


def unquote(value):
    """Condition cells: surrounding backticks and spaces are not part of the value."""
    v = value.strip()
    if len(v) >= 2 and v.startswith("`") and v.endswith("`"):
        v = v[1:-1].strip()
    return v


def parse_table(path):
    lines = section_text(path)
    header = cells(lines[0])
    if header != HEADER:
        refuse("exit 2: header %r != %r" % (header, HEADER))
    if not set(cells(lines[1])) <= {"-", "---", ":--", "--:", ":-:"} and \
            not all(set(c) <= set("-: ") for c in cells(lines[1])):
        refuse("exit 2: second table line is not a separator")
    rules = []
    for n, line in enumerate(lines[2:], start=3):
        c = cells(line)
        if len(c) != 9:
            refuse("exit 2: row %d has %d cells" % (n, len(c)))
        label = c[0]
        handler, gaps, deps, be, sr, pub = [unquote(x) for x in c[1:7]]
        action, src = c[7], c[8]
        if not label:
            refuse("exit 2: row %d has an empty label" % n)
        if not (handler == "*" or handler == "none" or
                any(ch in handler for ch in "*?[")):
            # a bare literal is legal: fnmatch matches it exactly
            pass
        if handler not in ("*", "none") and not handler:
            refuse("exit 2: row %d handler empty" % n)
        for name, value in (("gap kinds", gaps), ("dependencies", deps)):
            if value in ("*", "none", ""):
                if value == "":
                    refuse("exit 2: row %d %s empty" % (n, name))
                continue
            for part in value.split("+"):
                if not part or part != part.strip() or " " in part:
                    refuse("exit 2: row %d %s malformed: %r" % (n, name, value))
        for name, value in (("-be in child argv", be), ("symlink removed", sr)):
            if value not in ("yes", "no", "n/a", "*"):
                refuse("exit 2: row %d %s malformed: %r" % (n, name, value))
        if pub not in ("0", ">0", "*"):
            refuse("exit 2: row %d published files malformed: %r" % (n, pub))
        rules.append(dict(label=label, handler=handler, gaps=gaps, deps=deps,
                          be=be, sr=sr, pub=pub, action=action, src=src))
    if not rules:
        refuse("exit 2: no data rows")
    return rules


def features(envelope):
    doc = envelope.get("data", envelope)
    n = doc.get("normalized_result") or {}
    H = {c.get("handler") for c in n.get("chunks") or []
         if isinstance(c.get("handler"), str) and c["handler"].startswith("squashfs")}
    G = {g.get("kind") for g in n.get("extraction_gaps") or []}
    D = set()
    for g in n.get("extraction_gaps") or []:
        D |= set(g.get("dependencies") or [])
    argv_seen, any_be = [], False
    for d in n.get("diagnostics") or []:
        rep = d.get("report") or {}
        cmd = rep.get("command")
        if isinstance(cmd, str):
            argv = cmd.split()
        elif isinstance(cmd, list):
            argv = [str(a) for a in cmd]
        else:
            continue
        if any("sasquatch" in a for a in argv):
            argv_seen.append(argv)
            any_be = any_be or ("-be" in argv)
    BE = "n/a" if not argv_seen else ("yes" if any_be else "no")
    SR = "yes" if any(
        (d.get("report") or {}).get("__typename__") == "MaliciousSymlinkRemoved"
        for d in n.get("diagnostics") or []) else "no"
    P = len(n.get("files") or [])
    return dict(H=H, G=G, D=D, BE=BE, SR=SR, P=P)


def match(r, f):
    h = r["handler"]
    if h == "none":
        if f["H"]:
            return False
    elif h != "*":
        if not any(fnmatch.fnmatchcase(x, h) for x in f["H"]):
            return False
    for cond, got in ((r["gaps"], f["G"]), (r["deps"], f["D"])):
        if cond == "*":
            continue
        want = set() if cond == "none" else set(cond.split("+"))
        if got != want:
            return False
    if r["be"] != "*" and r["be"] != f["BE"]:
        return False
    if r["sr"] != "*" and r["sr"] != f["SR"]:
        return False
    if r["pub"] == "0" and f["P"] != 0:
        return False
    if r["pub"] == ">0" and f["P"] <= 0:
        return False
    return True


def classify(rules, f):
    for r in rules:
        if match(r, f):
            return r["label"]
    return "unclassified"


def main():
    block = sys.argv[1]
    rules = parse_table(block)
    print("rows: %s" % ", ".join(r["label"] for r in rules))
    if len(sys.argv) == 2:
        return 0
    failures = 0
    for pair in sys.argv[2:]:
        path, _, expected = pair.partition("=")
        env = json.load(open(path, encoding="utf-8"))
        f = features(env)
        got = classify(rules, f)
        ok = got == expected
        failures += 0 if ok else 1
        print("%-4s %-52s expected=%-26s got=%-26s H=%s G=%s D=%s BE=%s SR=%s P=%d"
              % ("ok" if ok else "FAIL", path.split("/")[-1], expected, got,
                 sorted(f["H"]), sorted(f["G"]), sorted(f["D"]),
                 f["BE"], f["SR"], f["P"]))
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
