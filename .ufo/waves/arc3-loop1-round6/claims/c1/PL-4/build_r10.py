"""Build the r10 (G21 frontier register) extension of c1-census-v10.py.

Applies exact text replacements to the scratch copy; each replacement must
fire exactly once or the build aborts. The gate itself is never touched.
"""
import sys

SRC = "/var/tmp/pl4-arc3r6/c1-census-v10.py"
DST = "/var/tmp/pl4-arc3r6/c1-census-v10-r10.py"

txt = open(SRC, encoding="utf-8").read()


def rep(old, new):
    global txt
    n = txt.count(old)
    if n != 1:
        sys.exit("ABORT: replacement anchor found %d times (want 1):\n%r" % (n, old[:120]))
    txt = txt.replace(old, new)


# R1 — provenance block in the leading docstring (before its terminator)
rep("""  (the queue-drain rule-#14 discipline).\"\"\"""",
    """  (the queue-drain rule-#14 discipline).

ARC3-LOOP1-ROUND6 r10 — G21 FRONTIER REGISTER (2026-10-19, seat PL-4; instrument
sha256 before this edit d0772ce8…). The round-1 R1 residual closes: the Frontier
region (PROVINCE.md :73-93 `## Frontier`, :133-162 `### Round-4 frontier
(post-unlock)`) is UNDECLARED in SCOPE, and its bullets carry no pin/version/
path loci, so L3 never fires on them and the instrument read PASS identically
whether or not a frontier bullet was stale (measured before this edit: v10
returns PASS exit 0 on a scratch tree carrying the retracted literal "real
solc/vyper-compiled bytecode untested" back inside :91-93). Closed as a
declared SECONDARY classification for locus-free bullets (the register option,
not a SCOPE declaration — a SCOPE row would still never fire: classify() needs
a locus). FRONTIER[] rows pin each bullet's span and assert REQUIRED earning
anchors (positive floor: a stripped, rewritten-empty or truncated bullet fails
REQUIRED-absent) and FORBIDDEN retracted literals (a reintroduced stale literal
fails FRONTIER-STALE). SCOPE bounds are UNCHANGED and every existing counter
keeps its semantics; the run gains one counter (frontier_errors) and two
declared fail classes (FRONTIER-STALE for a FORBIDDEN match, FRONTIER-UNEVALUABLE
for a REQUIRED-absent or uncheckable row), reported in text and --json. G21
rows are keyed to the r5-audit tree; any frontier edit re-keys the register in
the same commit — the same standing rule as the records-commit bound. Residual,
named: a brand-new bullet appended past :162 (the register's last declared
line) sits outside the register until re-keyed — the same past-the-bound
residual the records-commit rule already governs for SCORECARD.md:856+.\"\"\"""")

# R2 — verdict doc line gains the G21 conjunct
rep("""(>= 1 current-ok DETECTION per readable scoped file, r9 floor) AND no
unevaluable scoped file.""",
    """(>= 1 current-ok DETECTION per readable scoped file, r9 floor) AND no
unevaluable scoped file AND frontier_errors == 0 (G21 frontier register, r10:
every declared frontier bullet carries its REQUIRED anchors and none carries a
FORBIDDEN retracted literal).""")

# R3 — G21 entry in the DEFECT CLASSES list (after G20)
rep("""                                           invariance check.)""",
    """                                           invariance check.)
  G21 frontier-claim register            (r10, R1 residual): Frontier bullets
                                           (PROVINCE.md :73-93, :133-162)
                                           carry no pin/version/path loci, so
                                           L3 never fires on them and v10 read
                                           PASS identically whether or not a
                                           frontier bullet was stale; the
                                           FRONTIER[] register asserts each
                                           declared bullet's REQUIRED earning
                                           anchors (positive floor) and
                                           FORBIDDEN retracted literals
                                           directly on its text; a FORBIDDEN
                                           match is FRONTIER-STALE, a
                                           REQUIRED-absent/uncheckable row is
                                           FRONTIER-UNEVALUABLE""")

# R4 — the register table, after SCOPE
rep("""    ("SCORECARD.md", 769, 855, "DATED", 769, r"arc2-loop1-round3"),
]""",
    """    ("SCORECARD.md", 769, 855, "DATED", 769, r"arc2-loop1-round3"),
]

# ---- L1b: frontier-claim register (r10, G21). Frontier bullets carry no
# pin/version/path loci, so the L1/L2/L3 machinery is silent on them by
# construction; these rows are keyed by DIRECT TEXT ASSERTION, not by locus,
# and deliberately live OUTSIDE SCOPE (a CURRENT SCOPE row would still never
# fire -- classify() needs a locus to grade). Register files must also appear
# in SCOPE (the read loop is keyed on SCOPE's file set). Each row:
#   (file, start, end, [REQUIRED regex...], [FORBIDDEN regex...])
# REQUIRED  at least one match per pattern inside the declared span (positive
#           floor: a stripped/rewritten/truncated bullet fails REQUIRED-absent)
# FORBIDDEN no match may occur (a reintroduced retracted literal fails
#           FRONTIER-STALE). Patterns are case-insensitive.
# Keyed to the r5-audit tree (HEAD c625d5d); any frontier edit re-keys the
# register in the same commit.
FRONTIER = [
    ("PROVINCE.md", 75, 80, [r"Claimed in MINT\\.md, not yet held"], []),
    ("PROVINCE.md", 82, 83, [r"PE subtypes", r"x86-64 AND ARM64"], []),
    ("PROVINCE.md", 84, 86, [r"32 MiB", r"oldest-first"], []),
    ("PROVINCE.md", 87, 88, [r"Alternate providers", r"\\bIDA\\b"], []),
    ("PROVINCE.md", 89, 90, [r"unsupported_host"], []),
    ("PROVINCE.md", 91, 93, [r"EVM bytecode", r"solc-0\\.8\\.37", r"vyper-0\\.4\\.3"],
     [r"untested"]),
    ("PROVINCE.md", 135, 138, [r"RISC-V", r"r5-01"], []),
    ("PROVINCE.md", 139, 144, [r"90 MB PE", r"arc2-r7"], []),
    ("PROVINCE.md", 145, 146, [r"\\.jsc", r"Ignition"], []),
    ("PROVINCE.md", 147, 148, [r"sasquatch", r"unblob"], []),
    ("PROVINCE.md", 149, 150, [r"adb device surface", r"22/24"], []),
    ("PROVINCE.md", 151, 156, [r"1Password", r"asar"], []),
    ("PROVINCE.md", 157, 160, [r"Cross-version", r"r12-02|r14-01"], []),
    ("PROVINCE.md", 161, 162, [r"Operator-gated", r"\\bIDA\\b"], []),
]""")

# R5 — frontier_check, between assert_markers and cache_versions
rep("""        if not (1 <= ml <= len(lines)) or not re.search(mr, lines[ml - 1]):
            errs.append("%s:%d marker %r absent from %r" %
                        (f, ml, mr, (lines[ml - 1][:70] if 1 <= ml <= len(lines) else "<beyond EOF>")))
    return errs


def cache_versions():""",
    """        if not (1 <= ml <= len(lines)) or not re.search(mr, lines[ml - 1]):
            errs.append("%s:%d marker %r absent from %r" %
                        (f, ml, mr, (lines[ml - 1][:70] if 1 <= ml <= len(lines) else "<beyond EOF>")))
    return errs


def frontier_check(filelines):
    \"\"\"G21 (r10): assert the frontier-claim register directly on bullet text.
    Locus-free bullets never reach classify(), so this is the only grading
    they get: REQUIRED anchors are the positive floor (a stripped, rewritten
    or truncated bullet fails REQUIRED-absent), FORBIDDEN literals name the
    retracted claims whose reintroduction must fail the run (FRONTIER-STALE).\"\"\"
    errs = []
    for (f, s, e, req, forb) in FRONTIER:
        lines = filelines.get(f)
        if not lines:
            errs.append("%s:%d-%d frontier uncheckable (file unreadable)" % (f, s, e))
            continue
        seg = "\\n".join(lines[s - 1:e])
        for pat in req:
            if not re.search(pat, seg, re.I):
                errs.append("%s:%d-%d REQUIRED %r absent (G21 frontier register)"
                            % (f, s, e, pat))
        for pat in forb:
            m = re.search(pat, seg, re.I)
            if m:
                errs.append("%s:%d-%d FORBIDDEN %r matched %r (FRONTIER-STALE)"
                            % (f, s, e, pat, m.group(0)))
    return errs


def cache_versions():""")

# R6 — G19 truncation threshold includes register rows (rows past EOF must
# never be absorbed silently; the H1 class must not reopen for the frontier)
rep("""        max_end = max((s[2] for s in SCOPE if s[0] == f), default=0)""",
    """        max_end = max([s[2] for s in SCOPE if s[0] == f]
                      + [r[2] for r in FRONTIER if r[0] == f], default=0)""")

# R7 — run the register
rep("""    scope_errors = assert_markers(filelines)""",
    """    scope_errors = assert_markers(filelines)
    frontier_errors = frontier_check(filelines)""")

# R8 — declared fail class, split by cause: a FORBIDDEN match is a
# reintroduced retracted literal (FRONTIER-STALE); REQUIRED-absent or an
# uncheckable row means the declared bullet text could not be graded
# (FRONTIER-UNEVALUABLE). Both fail the run.
rep("""    declared = (["UNREADABLE"] if unreadable else []) + ([] if g2_ok else ["BLIND-INSTRUMENT"])""",
    """    frontier_class = (["FRONTIER-STALE"] if any("FORBIDDEN" in e for e in frontier_errors)
                      else ["FRONTIER-UNEVALUABLE"] if frontier_errors else [])
    declared = (["UNREADABLE"] if unreadable else []) + ([] if g2_ok else ["BLIND-INSTRUMENT"]) \\
               + frontier_class""")

# R9 — verdict conjunct
rep("""    ok = (not stale) and (not unatt) and (not undecl) and (not unres) and (not scope_errors) \\
         and (not g11) and g2_ok and (not unreadable)""",
    """    ok = (not stale) and (not unatt) and (not undecl) and (not unres) and (not scope_errors) \\
         and (not g11) and g2_ok and (not unreadable) and (not frontier_errors)""")

# R10 — --json carries the register outcome
rep("""                          "unreadable": unreadable, "declared_fail_classes": declared,""",
    """                          "unreadable": unreadable, "declared_fail_classes": declared,
                          "frontier_rows": len(FRONTIER), "frontier_errors": frontier_errors,""")

# R11 — text report line (VERDICT line itself stays byte-identical)
rep("""    print("\\nSCOPE-ERRORS (marker assertions): %r" % scope_errors)""",
    """    print("\\nSCOPE-ERRORS (marker assertions): %r" % scope_errors)
    print("FRONTIER register (G21): %d rows asserted, errors: %r"
          % (len(FRONTIER), frontier_errors))""")

open(DST, "w", encoding="utf-8").write(txt)
print("built", DST, len(txt.splitlines()), "lines (from", len(open(SRC, encoding='utf-8').read().splitlines()), ")")
