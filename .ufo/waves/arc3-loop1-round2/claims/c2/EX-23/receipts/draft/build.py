#!/usr/bin/env python3
"""EX-23 draft builder: v10 -> header patch + H1/H3 companion hunks (scratch only).

Emits three files:
  draft_hdr_only.py  v10 + header/records hunks only   (scope-neutrality check)
  draft_impl_only.py v10 + H1/H3 implementation hunks only
  draft_v11.py       v10 + both                        (the full v11 draft)
Every replacement is asserted; a missing anchor is a hard error.
"""
import pathlib, sys

SRC = pathlib.Path('/var/tmp/ex23/v10.py')
src = SRC.read_text()

# ---------------------------------------------------------------- header hunks
HDR_TITLE_OLD = '"""C1 census v10 \u2014 v9 (sha256 213fe679\u2026) re-keyed per arc2-loop1-round4 Z1 section 4d.'
HDR_TITLE_NEW = '''"""C1 census v11 \u2014 v10 (sha256 6f1d19ff\u2026) + H1 absent-file guard + H3 positive
floor per arc3-loop1-round2.

V11 REVISION (arc3-loop1-round2; 2026-10-19). BEFORE-state: v10, 490 lines,
sha256 6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b, HEAD
14b1682. The file path stays .ufo/gates/c1-census-v10.py (the frozen round-2
write target); v11 is this header's revision id, not a new file. Two round-1
named holes are CLOSED, each injected against the BEFORE bytes (v10) and the
AFTER bytes (this revision) at HEAD 14b1682, scratch copies only:
  H1 absent scoped file. v10 at a root deleting SKILL.md reads lines=0 loci=0
     and PASS exit 0 (both SKILL rows are CURRENT, so no marker assertion
     fires); v11 reads UNREADABLE ['SKILL.md: FileNotFoundError'] -> FAIL
     exit 1.  [EX-23/EX-16 receipt]
  H3 blind instrument. v10 with PIN/VER/PTR neutered reads loci=0 on all three
     files and still PASS exit 0 -- G2's second disjunct ("nothing found") is
     vacuously true; v11 reads G2 SUSPECT (current-ok=0) and BLIND (zero loci
     on a non-empty scope) -> FAIL exit 1.  [EX-23/EX-16 receipt]
Declared classes added by v11 (binding tokens; the report and the verdict
line must carry exactly these names):
  UNREADABLE (could-not-evaluate)  a scoped file the run could not read
                                   (absent / OSError) -> FAIL, never silent.
  BLIND                            zero loci classified on a non-empty scope,
                                   or zero current-ok loci (G2 SUSPECT) ->
                                   FAIL; a blind instrument and a clean one
                                   no longer print the same verdict.
Ordinary run at HEAD 14b1682 stays PASS 0/0/0/0 exit 0 with locus counts
unchanged (PROVINCE.md 6 / SCORECARD.md 9 / SKILL.md 2); the SCOPE table is
byte-identical to v10 (no row added, removed, re-keyed or retired).
RESIDUAL LEDGER (named, not closed by v11):
  H2  inline-marker token excuses an arbitrary value (latent at HEAD; the
      inline-marker branch does no cache-existence check).
  H4  SELF-CERTIFICATION -- OPEN AND NAMED: this instrument cannot detect its
      own SCOPE widening or its own detection narrowing. No edit to this file
      may cite its own PASS as evidence for the edit. The certificate for any
      future re-key is the external diff audit (CR-5 scope-diff.py form) plus
      locus-count invariance; the v11 diff is certified that way (rows
      before=20 after=20, 0 added / 0 removed / 0 changed, CREEP FLAGS []),
      not by this instrument's verdict.  [EX-23 receipt]
  H5  unit boundary: a version statement carrying no rea/kimi/devin/omp token
      is not a locus in this unit (stated, not fixed).
  H6  fixed-bound rationale comment at the SCOPE rows (optional mechanical
      guard) stays unlanded.
  H7  found this round: a scoped file truncated to 0 lines still reads silent
      PASS under v11's minimal H1 form (measured, EX-23 receipt); the one-line
      extension (0-line -> UNREADABLE) is measured in the same receipt and is
      NOT landed unless EX-16 lands it -- the class above covers absent and
      unreadable only.
Landing record: the fresh v11 digest and the locus-count invariance are
re-derived by the integrator at the records commit (self-identity discipline,
queue-drain rule #14). This stanza names the BEFORE state only -- it is not
its own verification.'''

SEC_TITLE_OLD = '"""C1 stale-statement census instrument v9 (E22, arc2-loop1-round2) \u2014 FINAL.'
SEC_TITLE_NEW = '''"""C1 stale-statement census instrument v11 (arc3-loop1-round2) \u2014 v10 + H1/H3
fail-closures (G19/G20; declared classes UNREADABLE, BLIND); residual ledger
H2/H4/H5/H6/H7 named in the stanza above.'''

G18_TAIL_OLD = '''  G18 marker line inside its own range    (the marker assertion checked only
                                           that the NAMED line carried the
                                           marker, so a DATED row could date
                                           itself by a line in another row's
                                           range -- the stale-row class EX-28
                                           found at HEAD, PROVINCE.md 45-62
                                           naming :40; now a SCOPE-ERROR)'''
G18_TAIL_NEW = G18_TAIL_OLD + '''
  G19 absent-scoped-file fail-closure (H1)(a scoped file that cannot be read
                                           is the declared UNREADABLE
                                           (could-not-evaluate) class -> FAIL;
                                           v10 absorbed it as lines=0 loci=0
                                           silent PASS)
  G20 positive floor               (H3)   (G2's second disjunct -- "nothing
                                           found" -- is vacuous, so a blind
                                           instrument printed PASS; v11
                                           requires current-ok >= 1 AND total
                                           loci > 0 on a non-empty scope,
                                           else the declared BLIND class ->
                                           FAIL)'''

VERDICT_OLD = '''Verdict: PASS iff stale == 0 AND ambiguous == 0 AND undeclared == 0
AND unresolved == 0 AND scope_errors == 0 AND g11 == [] AND G2 holds.
Exit 0 PASS, 1 FAIL, 2 anchor failure.
Usage: python3 c1-census-v9.py [--root DIR] [--json] [--quiet]'''
VERDICT_NEW = '''Verdict: PASS iff stale == 0 AND ambiguous == 0 AND undeclared == 0
AND unresolved == 0 AND scope_errors == 0 AND g11 == [] AND unreadable == []
AND blind == 0 AND G2 holds (current-ok >= 1).
Exit 0 PASS, 1 FAIL, 2 anchor failure (a live anchor config unreadable).
Usage: python3 .ufo/gates/c1-census-v10.py [--root DIR] [--json] [--quiet]
       (path frozen for arc3-loop1-round2; revision id v11 as above)'''

header_hunks = [
    (HDR_TITLE_OLD, HDR_TITLE_NEW),
    (SEC_TITLE_OLD, SEC_TITLE_NEW),
    (G18_TAIL_OLD, G18_TAIL_NEW),
    (VERDICT_OLD, VERDICT_NEW),
]

# ------------------------------------------------------- H1/H3 impl companion
H1_OLD = '''    out, counts, filelines = {}, {}, {}
    for f in files:
        try:
            lines = open(os.path.join(args.root, f), encoding="utf-8", errors="replace").read().splitlines()
        except OSError:
            counts[f] = {"lines": 0, "loci": 0}
            filelines[f] = None
            continue
        filelines[f] = lines
        counts[f] = {"lines": len(lines), "loci": len(classify(f, lines, live, out))}
    scope_errors = assert_markers(filelines)'''
H1_NEW = '''    out, counts, filelines, unreadable = {}, {}, {}, []
    for f in files:
        try:
            lines = open(os.path.join(args.root, f), encoding="utf-8", errors="replace").read().splitlines()
        except OSError as ex:
            unreadable.append("%s: %s" % (f, type(ex).__name__))
            counts[f] = {"lines": 0, "loci": 0}
            filelines[f] = None
            continue
        filelines[f] = lines
        counts[f] = {"lines": len(lines), "loci": len(classify(f, lines, live, out))}
    scope_errors = assert_markers(filelines)'''

H3_OLD = '''    g2_ok = len(out.get("current-ok", [])) > 0 or (not stale and not unatt and not undecl and not unres)
    ok = (not stale) and (not unatt) and (not undecl) and (not unres) and (not scope_errors) \\
         and (not g11) and g2_ok'''
H3_NEW = '''    total_loci = sum(c["loci"] for c in counts.values())
    scoped_lines = sum(c["lines"] for c in counts.values())
    blind = (total_loci == 0) and (scoped_lines > 0)
    g2_ok = len(out.get("current-ok", [])) > 0
    ok = (not stale) and (not unatt) and (not undecl) and (not unres) and (not scope_errors) \\
         and (not g11) and (not unreadable) and (not blind) and g2_ok'''

JSON_OLD = '''                          "g11": g11, "g7": g7, "g2_ok": g2_ok,'''
JSON_NEW = '''                          "g11": g11, "g7": g7, "g2_ok": g2_ok,
                          "unreadable": unreadable, "blind": blind,
                          "total_loci": total_loci,'''

REPORT_OLD = '''    print("\\nSCOPE-ERRORS (marker assertions): %r" % scope_errors)
    print("G2 positive-assertion guard: %s" % ("ok" if g2_ok else "SUSPECT"))'''
REPORT_NEW = '''    print("\\nSCOPE-ERRORS (marker assertions): %r" % scope_errors)
    print("UNREADABLE (could-not-evaluate): %r" % unreadable)
    print("G2 positive-assertion guard: %s (current-ok=%d, total loci=%d)"
          % ("ok" if g2_ok else "SUSPECT", len(out.get("current-ok", [])), total_loci))
    print("BLIND (zero loci on non-empty scope): %s" % ("FAIL" if blind else "no"))'''

VLINE_OLD = '''    print("VERDICT: %s  (stale=%d ambiguous=%d undeclared=%d unresolved=%d)"
          % (verdict, len(stale), len(unatt), len(undecl), len(unres)))'''
VLINE_NEW = '''    print("VERDICT: %s  (stale=%d ambiguous=%d undeclared=%d unresolved=%d unreadable=%d blind=%d)"
          % (verdict, len(stale), len(unatt), len(undecl), len(unres), len(unreadable), int(blind)))'''

impl_hunks = [
    (H1_OLD, H1_NEW), (H3_OLD, H3_NEW), (JSON_OLD, JSON_NEW),
    (REPORT_OLD, REPORT_NEW), (VLINE_OLD, VLINE_NEW),
]


def apply(text, hunks, label):
    for i, (old, new) in enumerate(hunks):
        n = text.count(old)
        if n != 1:
            print("ANCHOR FAIL %s hunk %d: count=%d" % (label, i, n))
            for j, (o, _) in enumerate(hunks):
                print("   hunk %d present=%d" % (j, text.count(o)))
            sys.exit(2)
        text = text.replace(old, new)
    return text


hdr_only = apply(src, header_hunks, "header")
impl_only = apply(src, impl_hunks, "impl")
full = apply(apply(src, impl_hunks, "impl"), header_hunks, "header")

pathlib.Path('/var/tmp/ex23/draft/draft_hdr_only.py').write_text(hdr_only)
pathlib.Path('/var/tmp/ex23/draft/draft_impl_only.py').write_text(impl_only)
pathlib.Path('/var/tmp/ex23/draft/draft_v11.py').write_text(full)
print("OK: 3 drafts written")
print("header-only delta lines: %d" % (len(hdr_only.splitlines()) - len(src.splitlines())))
print("full v11 lines: %d (v10: %d)" % (len(full.splitlines()), len(src.splitlines())))
