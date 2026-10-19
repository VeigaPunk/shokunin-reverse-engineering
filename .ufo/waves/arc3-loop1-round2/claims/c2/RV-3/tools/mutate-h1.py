#!/usr/bin/env python3
"""RV-3 mutation harness — revert ONLY the H1 absent-file guard.

Seat RV-3 (reviewer, c2), arc3-loop1-round2. Reads a census instrument,
locates the H1 guard (absent/unreadable scoped file -> declared could-not-
evaluate class) and emits mutants that remove it, without touching any other
guard (H3, G2, G11, G15/G18, scope table, needles).

Mutants:
  full     : H1 fully reverted == v10 behaviour (no record, no verdict term,
             no report line) -> absent scoped file folds into lines=0 loci=0
             and the run returns silent PASS.
  verdict  : record + report kept, only the verdict term dropped (report-only
             guard: proves the verdict term, not just the listing, is what
             closes the hole; a printed-but-inert guard would still PASS).

Usage: mutate-h1.py <census.py> <outdir>
"""
import os
import re
import sys


def die(msg):
    print("MUTATE-ERROR: %s" % msg)
    sys.exit(2)


def main():
    src_path, outdir = sys.argv[1], sys.argv[2]
    src = open(src_path, encoding="utf-8").read()
    os.makedirs(outdir, exist_ok=True)

    # --- locate the H1 guard -------------------------------------------------
    m_vars = re.search(r"^    out, counts, filelines(?:, (\w+))? = \{\}, \{\}, \{\}(?:, \[\])?$",
                       src, re.M)
    if not m_vars:
        die("could not locate 'out, counts, filelines' declaration")
    var = m_vars.group(1)
    if not var:
        die("no unreadable-list variable: H1 guard appears absent in %s" % src_path)

    m_collect = re.search(
        r"^        except OSError(?: as \w+)?:\n"
        r"^            %s\.append\([^\n]*\)\n"
        r"^            counts\[f\] = \{\"lines\": 0, \"loci\": 0\}\n" % re.escape(var),
        src, re.M)
    if not m_collect:
        die("could not locate the except-OSError collection block for %r" % var)

    m_term = re.search(r" and \(not %s\)\n" % re.escape(var), src)
    if not m_term:
        die("could not locate verdict term 'and (not %s)'" % var)

    m_report = re.search(r"^    print\(\"[^\n]*%s[^\n]*\n" % re.escape(var), src, re.M)
    if not m_report:
        die("could not locate report line for %r" % var)

    # --- mutant 1: full revert (== v10 semantics) ---------------------------
    full = src
    full = full.replace(m_vars.group(0), "    out, counts, filelines = {}, {}, {}", 1)
    full = full.replace(m_collect.group(0),
                        "        except OSError:\n"
                        "            counts[f] = {\"lines\": 0, \"loci\": 0}\n", 1)
    full = full.replace(m_term.group(0), "\n", 1)
    full = full.replace(m_report.group(0), "", 1)

    # --- mutant 2: verdict term only dropped (report-only guard) ------------
    verdict_only = src.replace(m_term.group(0), "\n", 1)

    for name, text in (("full", full), ("verdict", verdict_only)):
        p = os.path.join(outdir, "mutant-%s.py" % name)
        open(p, "w", encoding="utf-8").write(text)
        print("wrote %s (%d bytes)" % (p, len(text)))

    # --- mutation footprint --------------------------------------------------
    print("H1 var=%r  declaration=%r" % (var, m_vars.group(0).strip()))
    print("verdict term=%r" % m_term.group(0).strip())
    print("report line=%r" % m_report.group(0).strip())


if __name__ == "__main__":
    main()
