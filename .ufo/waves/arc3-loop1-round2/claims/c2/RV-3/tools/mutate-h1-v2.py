#!/usr/bin/env python3
"""RV-3 mutation harness v2 — landed v11 shape (sha256 82fb807e…).

Reverts the H1 guard (absent/unreadable/short scoped file -> declared
UNREADABLE class) along four independent cuts, leaving H3 (G2 positive floor),
G11, G15/G18 and the scope table untouched:

  m-term   drop ONLY the verdict term `and (not unreadable)`
           -> guard still collects, reports and serializes, but never fails
             (a report-only, inert guard).
  m-eof    drop ONLY the G19 rows-beyond-EOF check (OSError catch kept)
           -> truncation-to-zero stays fail-open; absence still fails.
  m-full   revert the whole H1 class (collection, both sites, verdict term,
           report line, JSON field, declared-class entry) == v10 H1 semantics.
  m-h3     revert ONLY the H3 floor (g2_ok back to the v10 disjunction),
           H1 intact -> isolation control: absent-SKILL must still FAIL.

Usage: mutate-h1-v2.py <landed.py> <outdir>
"""
import os
import re
import sys

DECL_OLD = ('    out, counts, filelines, unreadable = {}, {}, {}, []\n'
            '    for f in files:\n'
            '        max_end = max((s[2] for s in SCOPE if s[0] == f), default=0)\n'
            '        try:\n'
            '            lines = open(os.path.join(args.root, f), encoding="utf-8", errors="replace").read().splitlines()\n'
            '        except OSError as ex:\n'
            '            unreadable.append("%s: %s" % (f, type(ex).__name__))\n'
            '            counts[f] = {"lines": None, "loci": None}\n'
            '            filelines[f] = None\n'
            '            continue\n'
            '        if len(lines) < max_end:\n'
            '            # G19: declared rows past EOF are unevaluable, never a silent zero.\n'
            '            unreadable.append("%s: %d lines < declared max %d (rows beyond EOF)"\n'
            '                              % (f, len(lines), max_end))\n'
            '            counts[f] = {"lines": None, "loci": None}\n'
            '            filelines[f] = None\n'
            '            continue\n')

DECL_NEW = ('    out, counts, filelines = {}, {}, {}\n'
            '    for f in files:\n'
            '        try:\n'
            '            lines = open(os.path.join(args.root, f), encoding="utf-8", errors="replace").read().splitlines()\n'
            '        except OSError:\n'
            '            counts[f] = {"lines": 0, "loci": 0}\n'
            '            filelines[f] = None\n'
            '            continue\n')

EOF_ONLY_OLD = ('        if len(lines) < max_end:\n'
                '            # G19: declared rows past EOF are unevaluable, never a silent zero.\n'
                '            unreadable.append("%s: %d lines < declared max %d (rows beyond EOF)"\n'
                '                              % (f, len(lines), max_end))\n'
                '            counts[f] = {"lines": None, "loci": None}\n'
                '            filelines[f] = None\n'
                '            continue\n')

TERM_OLD = ' and (not unreadable)\n'
DECLARED_OLD = '    declared = (["UNREADABLE"] if unreadable else []) + ([] if g2_ok else ["BLIND-INSTRUMENT"])\n'
DECLARED_NEW = '    declared = ([] if g2_ok else ["BLIND-INSTRUMENT"])\n'
JSON_OLD = '                          "unreadable": unreadable, "declared_fail_classes": declared,\n'
JSON_NEW = '                          "declared_fail_classes": declared,\n'
PRINT_OLD = '    print("UNREADABLE (could-not-evaluate): %r" % unreadable)\n'
G2_OLD = '    g2_ok = h3_ok\n'
G2_NEW = ('    g2_ok = n_current_ok > 0 or (not stale and not unatt and not undecl and not unres)\n')


def sub_once(src, old, new, tag):
    n = src.count(old)
    if n != 1:
        print("MUTATE-ERROR: %s anchor found %d times (expected 1)" % (tag, n))
        sys.exit(2)
    return src.replace(old, new, 1)


def main():
    src_path, outdir = sys.argv[1], sys.argv[2]
    src = open(src_path, encoding="utf-8").read()
    os.makedirs(outdir, exist_ok=True)

    m_term = sub_once(src, TERM_OLD, "\n", "term")

    m_eof = sub_once(src, EOF_ONLY_OLD, "", "eof")

    m_full = src
    m_full = sub_once(m_full, DECL_OLD, DECL_NEW, "decl-block")
    m_full = sub_once(m_full, TERM_OLD, "\n", "term")
    m_full = sub_once(m_full, DECLARED_OLD, DECLARED_NEW, "declared")
    m_full = sub_once(m_full, JSON_OLD, JSON_NEW, "json")
    m_full = sub_once(m_full, PRINT_OLD, "", "print")

    m_h3 = sub_once(src, G2_OLD, G2_NEW, "g2")

    for name, text in (("m-term", m_term), ("m-eof", m_eof),
                      ("m-full", m_full), ("m-h3", m_h3)):
        p = os.path.join(outdir, "mutant-%s.py" % name)
        open(p, "w", encoding="utf-8").write(text)
        print("wrote %s (%d bytes)" % (p, len(text)))


if __name__ == "__main__":
    main()
