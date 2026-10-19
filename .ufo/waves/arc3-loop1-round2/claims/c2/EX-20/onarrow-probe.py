#!/usr/bin/env python3
"""EX-20 follow-up probe — the narrow in-EOF tail-shelter row.

Question: is the external certificate's CREEP FLAG list sufficient to refuse a
scope-table edit? The r9 landing closes bounds that exceed EOF; an attacker can
instead add a NARROW DATED row that covers only the appended block and stays
inside EOF. This probe measures both layers for that shape, on the before and
after instruments.

Usage: python3 onarrow-probe.py <tool.py> [<tool2.py> ...]
"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("ls", os.path.join(HERE, "launder-suite.py"))
ls = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ls)

for tool in sys.argv[1:]:
    planted = ls.tree("P6")
    ml = ls.marker_line(planted, "Records appended 2026-10-19")
    start = ml - 2
    src = open(tool, encoding="utf-8").read()
    assert ls.BOUND_OLD in src
    row = '    ("SCORECARD.md", %d, %d, "DATED", %d, r"2026-10-19"),' % (start, ml, ml)
    var = src.replace(ls.BOUND_OLD, ls.BOUND_OLD + "\n" + row, 1)
    out_path = "/dev/shm/ex20r2/variants/O-narrow-%s.py" % os.path.basename(tool)
    open(out_path, "w", encoding="utf-8").write(var)
    rc, out, k = ls.run(out_path, planted)
    digest = __import__("hashlib").sha256(out.encode()).hexdigest()[:16]
    flags, drc = ls.audit(tool, out_path)
    print("tool=%s" % tool)
    print("  added row: SCORECARD.md %d-%d DATED marker_line=%d (file has %d lines)"
          % (start, ml, ml, ml + 0))
    print("  instrument: exit=%s %s | %s | %s | %s" %
          (rc, k["verdict"], k["g2"], k["undecl"], k["scopeerr"]))
    print("  out-sha256=%s  unreadable=%s" % (digest, k["unread"]))
    print("  certificate: scope-diff exit=%s flags=%s" % (drc, flags))
    keep = os.path.join(HERE, "receipts", "O-narrow-%s.out" % os.path.basename(tool))
    open(keep, "w", encoding="utf-8").write(out)
    print("  receipt: %s" % keep)
