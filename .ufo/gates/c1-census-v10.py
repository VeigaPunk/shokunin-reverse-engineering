"""C1 census v10 — v9 (sha256 213fe679…) re-keyed per arc2-loop1-round4 Z1 section 4d.

E22 DISPOSITION — arc3-loop1-round1, EX-28 (measured 2026-10-19 at HEAD
e845c2b; instrument sha256 before this edit 36e96cd5…). The arc2-loop1-round3
carried debt "census scope-table drift (FAIL undeclared=2 at 766-line HEAD vs
PASS at 701-line b21c0da — re-key or retire next calibration round)"
(SCORECARD.md:850-852) is DISCHARGED AT HEAD BY RE-KEY. Nothing retired.

  Finding does not reproduce. v10 reads PASS 0/0/0/0 (scope-errors [], g11 [])
  at 1336-line HEAD; four independent captures (EX-26 / EX-30 / SC-6 / RV-11)
  share one digest 3b677b8e…; the two blocks UNDECLARED under v9 (:731-737,
  :747-766) now sit inside the round-2 row and read current-ok. v9 stays red
  at HEAD by construction (RV-11: v9@HEAD FAIL undeclared=2, marker absent
  at :635).

  One stale row at HEAD, re-keyed here. ("PROVINCE.md", 45, 62, DATED) named
  marker line 40 — the table intro, which lies OUTSIDE its own range. G15
  checked only that the named line carried the marker, so a DATED row could
  date itself by another row's line and the drift stayed invisible. Re-keyed
  to line 45, which carries the row's own dated receipt text ("2026-10-13
  receipt"); G18 now asserts marker_line in [start, end] for every DATED row,
  so the class cannot recur silently. The re-key is range-neutral: CR-5's
  creep differ (scope-diff.py) flags no signature — no row added, no DATED
  bound widened, no CURRENT->DATED flip, no open-ended bound.

  Refused, each with cause measured rather than asserted:
   - Tail expansion. Declaring SCORECARD.md:856-1336 (rounds 4-10 records) as
     DATED is fail-OPEN: a planted `rea-agents@6.3.0` inside a DATED range
     reads "historical (dated scope)" and the run returns PASS exit 0 (CR-5
     t5-dated-shelter / widen-swallow; replicated by EX-28). The fixed bound
     is kept instead: a locus past :855 reads UNDECLARED -> FAIL exit 1
     (CR-5 t2/t6; EX-28 fixture). Round 4 refused the same laundering path
     (Z1 §4d; SCORECARD.md:908).
   - Retiring the capability-table rows :619/:620. Measured: retired -> the
     :620 locus reads UNDECLARED (FAIL); re-keyed CURRENT -> AMBIGUOUS (FAIL).
     Each row records a capability demonstrated in a named past round, so
     DATED is its correct class; G16 keeps a live value inside them current-ok.
   - Re-classing any CURRENT row to DATED: refused as creep, no measurement
     needed (a CURRENT surface must stay reconciled).

  Standing rule for records commits (round-3/round-4 precedent): text appended
  past the declared bound must be locus-free in this instrument's unit — no
  `rea-agents@x.y.z`, no bare `6.x.y`, no `~`- or `/`-absolute `path:line` —
  or the bound must be re-keyed in the same commit as a DATED row whose marker
  line carries that section's own date/round token.

ARC3-LOOP1-ROUND2 r9 — H1+H3 FAIL-CLOSURES (2026-10-19, EX-16, C2's real-path
write; instrument sha256 before this edit 6f1d19ff…). Two round-1 latent holes
close as declared FAIL classes, merged from the round-1 patch texts RV-11/H1
(proposed-missing-file-guard) and CR-5/H3 (proposed-g2-positive-floor). Scope
bounds are UNCHANGED (creep audit: scope-diff.py 0 flags).

   - UNREADABLE (H1 class). A scoped file that cannot be read was absorbed as
     `lines=0 loci=0`; with all its declared rows CURRENT no marker assertion
     fired and the run read PASS exit 0. Re-measured before (claims/c2/EX-16/
     receipts/before/): SKILL.md absent -> PASS exit 0; and the same silent
     class for zero-byte, truncated (rows beyond EOF), is-a-directory and
     EACCES roots. Now: any scoped file that is unreadable (OSError) OR holds
     fewer lines than its declared max end is a declared could-not-evaluate
     class -- reported (`UNREADABLE (could-not-evaluate): [...]`, counts read
     `lines=None`), carried in --json, and fails the verdict (exit 1) whatever
     the row classes are. DATED-bearing files keep their existing
     "marker uncheckable" SCOPE-ERRORs as well.
   - BLIND-INSTRUMENT (H3 class). `g2_ok`'s old second disjunct was true
     exactly when the run found nothing, so needles neutered -> loci=0 read
     PASS exit 0 (re-measured: h3-blind-all / h3-blind-gate). G2 is now a
     PER-READABLE-FILE positive floor: >= 1 current-ok locus per scoped file
     the run could read (EX-14's variant B, measured to dominate the global
     variant A on head/blind/nullskill -- the global floor still swallows a
     per-file collapse such as a needle-stripped or blanked SKILL.md while
     the other two files stay loud). Per-ROW floors are refuted by EX-14's
     occupancy map: 4 DATED rows are zero-locus by design at HEAD. A
     violating run is declared (`DECLARED FAIL CLASSES:
     ['BLIND-INSTRUMENT']`) in text and --json, exit 1; the G2 report line
     carries the per-file substrate so the number is auditable. Unreadable
     files are exempt from the floor (they are the H1 class and already force
     FAIL). Residual, named: per-needle PARTIAL blindness (e.g. PIN alone
     neutered) keeps each file's current-ok count above zero and still reads
     PASS -- a token floor is not a coverage floor (EX-14 §5); only the
     external locus/assertion-count + scope-diff audit sees it, and that
     audit remains the certificate for any instrument touch.
   - Still named, NOT closed here (no silent widening): H2 same-line inline-
     marker excusal; t5 DATED-shelter for historical-looking non-live values;
     H4 self-certification (covered externally, see above).
   - Still named, NOT closed here (no silent widening): H2 same-line inline-
     marker excusal; t5 DATED-shelter for historical-looking non-live values;
     H4 self-certification (covered externally, see above).

  Post-edit identity is recorded in the landing receipt (claims/c2/EX-16/
  receipts/after/after-sha256.txt + landing-diff.md), NOT inline: an artifact
  that records its own byte-identity must re-derive it after every revision,
  so a hash written into the file it hashes would be stale by construction
  (the queue-drain rule-#14 discipline).

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
residual the records-commit rule already governs for SCORECARD.md:856+."""
#!/usr/bin/env python3
"""C1 census instrument v10-r9 (arc3-loop1-round2: H1+H3 fail-closures; the
v9-era structure and claim text below are retained as the instrument's history,
not as a current self-description — see the r9 provenance block at the top).

Claim under test (C1): after the round's commit, every current-surface
version/pin statement in PROVINCE.md / SKILL.md / SCORECARD.md states a
per-surface resolved value backed by a 2026-10-18 receipt (config grep,
package.json census) or is explicitly marked historical; stale Kimi-pin
statements N -> 0; no availability->holding inference (configured != held).

STRUCTURE (three layers, each independently falsifiable)
  L1 SCOPE     an explicit declared table of file:line ranges, each classed
               CURRENT (live state, must be reconciled) or DATED (record of a
               past verification, historical by construction). Every DATED
               range declares the marker that makes it historical, and the
               instrument ASSERTS that marker is present (marker assertion)
               AND that its line lies inside the range it dates (G18) -- a row
               that names a line in another row's range dates nothing.
               A locus inside no declared range is UNDECLARED and fails the
               run -- so file growth can never silently shrink the census
               (CR5's "silent skip" lesson).
  L2 ANCHORS   live anchors re-derived on every run: configured pins by grep
               of the three client configs; cache identities by package.json;
               config pointers by resolving path:line in the live file. No
               constant is baked in, so a drift re-anchors the instrument.
  L3 ASSERT    four assertion families (pin / bare version / cache identity /
               pointer) with per-occurrence clause attribution.

DEFECT CLASSES REPAIRED
  G1  case-insensitive needles            (CR5 variant A false PASS)
  G2  positive-assertion guard            (CR5 variants B/H silent clean)
  G3  no partition, no post-marker exon   (CR5 variant H escape hatch)
  G4  wide statement vocabulary           (CR5 variant I vocabulary hole)
  G5  live anchors re-derived             (nothing constant baked in)
  G6  every locus declared or UNDECLARED  (no silent skip)
  G7  configured != held guard
  G8  prose folding                       (value and client name on different
                                           physical lines of one paragraph)
  G9  nearest-PRECEDING attribution       (a trailing client name is a lead-in
                                           for the next statement, never the
                                           owner of the preceding value)
  G10 per-assertion physical line         (no block-level collapse)
  G11 receipt-backing requirement         (a current-ok locus must sit in a
                                           block carrying receipt language)
  G12 line-scoped inline markers          (a marker elsewhere in a folded
                                           block must not excuse the line)
  G13 bare-version needle made safe       (`(?<![\\d.])`; bare versions are
                                           collected even when the block also
                                           holds an @-pin)
  G14 clause-local attribution, else AMBIGUOUS (a CURRENT locus whose clause
                                           names no client is not guessed at)
  G15 marker assertions                   (every DATED range must actually
                                           carry its declared marker; a
                                           stripped marker is SCOPE-ERROR)
  G16 live-match outranks scope           (a value equal to the live anchor is
                                           current-ok even inside a DATED
                                           section, so a dated section can
                                           neither shelter a false live claim
                                           nor hide a true one; v8 reported a
                                           current-ok locus as 'historical')
  G17 version-intrinsic clause class      (a bare version whose clause names no
                                           client but describes version-
                                           intrinsic behaviour -- doctor /
                                           skill / expects -- is verified
                                           against the package.json census of
                                           a cache for that version instead of
                                           being dumped in AMBIGUOUS)
  G18 marker line inside its own range    (the marker assertion checked only
                                           that the NAMED line carried the
                                           marker, so a DATED row could date
                                           itself by a line in another row's
                                           range -- the stale-row class EX-28
                                           found at HEAD, PROVINCE.md 45-62
                                           naming :40; now a SCOPE-ERROR)
  G19 unreadable/undeclarable scoped file (r9, H1): an absent/zero-byte/
                                           truncated/EACCES/directory scoped
                                           file was absorbed as lines=0 loci=0
                                           and, when its rows were all
                                           CURRENT, read PASS exit 0; now a
                                           declared UNREADABLE fail class
                                           (rows beyond the declared max end
                                           count as truncated too)
  G20 positive floor, not vacuous         (r9, H3): G2's second disjunct was
                                           true exactly when the run found
                                           nothing, so a blind instrument read
                                           PASS.  The floor is PER READABLE
                                           FILE OVER CURRENT-OK DETECTIONS.
                                           The unit is load-bearing knowledge:
                                           refuted at HEAD are (a) per-SCOPE-
                                           row floors (4 DATED rows are
                                           zero-locus by design, EX-14's map)
                                           and (b) per-file BLOCK floors
                                           (SKILL.md has 0 current-ok blocks
                                           but 3 current-ok dets; CR-2's
                                           false-FAIL episode, CR-3's unit
                                           table).  Do not re-key the unit
                                           without re-running the HEAD
                                           invariance check.)
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
                                           FRONTIER-UNEVALUABLE

Verdict: PASS iff stale == 0 AND ambiguous == 0 AND undeclared == 0
AND unresolved == 0 AND scope_errors == 0 AND g11 == [] AND G2 holds
(>= 1 current-ok DETECTION per readable scoped file, r9 floor) AND no
unevaluable scoped file AND frontier_errors == 0 (G21 frontier register, r10:
every declared frontier bullet carries its REQUIRED anchors and none carries a
FORBIDDEN retracted literal).
Exit 0 PASS, 1 FAIL, 2 anchor failure.
Usage: python3 c1-census-v10.py [--root DIR] [--json] [--quiet]
"""
import argparse, json, os, re, sys

HOME = os.path.expanduser("~")
CLIENTS = {"devin": HOME + "/.config/devin/mcp_config.json",
           "omp": HOME + "/.omp/agent/mcp.json",
           "kimi": HOME + "/.kimi-code/config.toml"}
PATH_TOKENS = [(re.compile(r"mcp_config\.json", re.I), "devin"),
               (re.compile(r"mcp\.json", re.I), "omp"),
               (re.compile(r"config\.toml", re.I), "kimi")]
NAME_TOKENS = [(re.compile(r"devin", re.I), "devin"),
               (re.compile(r"\bomp\b", re.I), "omp"),
               (re.compile(r"kimi", re.I), "kimi")]

# ---- L1: declared scope. line numbers are 1-based, inclusive -------------
SCOPE = [
    ("PROVINCE.md", 8, 13, "CURRENT", None, None),
    ("PROVINCE.md", 15, 26, "CURRENT", None, None),
    ("PROVINCE.md", 40, 43, "DATED", 40, r"verified on this host 2026-10-13"),
    ("PROVINCE.md", 44, 44, "CURRENT", None, None),
    ("PROVINCE.md", 45, 62, "DATED", 45, r"2026-10-13"),
    ("PROVINCE.md", 64, 71, "CURRENT", None, None),
    ("PROVINCE.md", 119, 131, "DATED", 119, r"verified 2026-10-13"),
    ("SKILL.md", 10, 16, "CURRENT", None, None),
    ("SKILL.md", 18, 20, "CURRENT", None, None),
    ("SCORECARD.md", 56, 60, "CURRENT", None, None),
    ("SCORECARD.md", 273, 326, "DATED", 273, r"2026-10-16"),
    ("SCORECARD.md", 417, 466, "DATED", 417, r"2026-10-16"),
    ("SCORECARD.md", 467, 502, "DATED", 467, r"2026-10-16"),
    ("SCORECARD.md", 503, 533, "DATED", 503, r"2026-10-16"),
    ("SCORECARD.md", 534, 560, "DATED", 534, r"2026-10-16"),
    ("SCORECARD.md", 619, 619, "DATED", 619, r"luna-round-\d"),
    ("SCORECARD.md", 620, 620, "DATED", 620, r"luna-round-\d"),
    ("SCORECARD.md", 636, 702, "DATED", 636, r"2026-10-18"),

    ("SCORECARD.md", 703, 768, "DATED", 704, r"arc2-loop1-round2"),
    ("SCORECARD.md", 769, 855, "DATED", 769, r"arc2-loop1-round3"),
    ("SCORECARD.md", 1759, 2122, "DATED", 1759, r"arc3-loop1-round7"),
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
    ("PROVINCE.md", 75, 80, [r"Claimed in MINT\.md, not yet held"], []),
    ("PROVINCE.md", 82, 83, [r"PE subtypes", r"x86-64 AND ARM64"], []),
    ("PROVINCE.md", 84, 86, [r"32 MiB", r"oldest-first"], []),
    ("PROVINCE.md", 87, 88, [r"Alternate providers", r"\bIDA\b"], []),
    ("PROVINCE.md", 89, 90, [r"unsupported_host"], []),
    ("PROVINCE.md", 91, 93, [r"EVM bytecode", r"solc-0\.8\.37", r"vyper-0\.4\.3"],
     [r"untested"]),
    ("PROVINCE.md", 135, 138, [r"RISC-V", r"r5-01"], []),
    ("PROVINCE.md", 139, 144, [r"90 MB PE", r"arc2-r7"], []),
    ("PROVINCE.md", 145, 146, [r"\.jsc", r"Ignition"], []),
    ("PROVINCE.md", 147, 148, [r"sasquatch", r"unblob"], []),
    ("PROVINCE.md", 149, 150, [r"adb device surface", r"22/24"], []),
    ("PROVINCE.md", 151, 156, [r"1Password", r"asar"], []),
    ("PROVINCE.md", 157, 160, [r"Cross-version", r"r12-02|r14-01"], []),
    ("PROVINCE.md", 161, 162, [r"Operator-gated", r"\bIDA\b"], []),
]

FRONTIER_SECTIONS = (
    ("PROVINCE.md", "## Frontier", 2),
    ("PROVINCE.md", "### Round-4 frontier (post-unlock)", 3),
)

PIN = re.compile(r"rea-agents@(\d+\.\d+\.\d+)", re.I)
VER = re.compile(r"(?<![\d.])6\.\d+\.\d+")
PTR = re.compile(r"((?:~|/)[\w./+-]+\.(?:json|toml|ya?ml)):(\d+)")
CACHE = re.compile(r"_npx/([0-9a-f]{6,})")
REA_GATE = re.compile(r"rea-agents|\brea\b|config\.toml|mcp_config\.json|mcp\.json|mcp_servers|devin|\bomp\b|kimi|npx", re.I)
INLINE_MARKER = re.compile(r"historical|verified 2026-10-13|not re-probed|superseded|baseline|retain their original", re.I)
RECEIPT = re.compile(r"2026-10-18|receipt|SHA-256|sha256|re-grepped", re.I)
SECTION = re.compile(r"^#{1,4} ")
BULLET = re.compile(r"^\s*[-*+] ")
CLAUSE_SPLIT = re.compile(r"[;()\u2014\u2013]|\.\s")
HOLDING = re.compile(r"\bheld\b|live[- ]verified", re.I)
HOLDING_OK = re.compile(r"configured|available|not held|availability|never stands", re.I)


def live_pins():
    out = {}
    for client, path in CLIENTS.items():
        try:
            txt = open(path, encoding="utf-8", errors="replace").read()
        except OSError:
            out[client] = None
            continue
        m = re.search(r"rea-agents@(\d+\.\d+\.\d+)", txt)
        out[client] = m.group(1) if m else None
    return out


def units(lines):
    i, n = 0, len(lines)
    while i < n:
        if not lines[i].strip():
            i += 1
            continue
        if SECTION.match(lines[i]) or lines[i].lstrip().startswith("|"):
            yield (i, i, lines[i].strip())
            i += 1
            continue
        j = i + 1
        while j < n and lines[j].strip() and not SECTION.match(lines[j]) \
                and not lines[j].lstrip().startswith("|") and not BULLET.match(lines[j]):
            j += 1
        yield (i, j - 1, " ".join(lines[k].strip() for k in range(i, j)))
        i = j


def line_of(lines, a, b, offset):
    acc = 0
    for k in range(a, b + 1):
        seg = lines[k].strip()
        if acc <= offset <= acc + len(seg):
            return k + 1
        acc += len(seg) + 1
    return a + 1


def clause_bounds(text, off):
    lo, hi = 0, len(text)
    for m in CLAUSE_SPLIT.finditer(text):
        if m.end() <= off:
            lo = m.end()
        elif m.start() > off:
            hi = m.start()
            break
    return lo, hi


def nearest_client(text, off, limit_lo=0):
    best = None
    for pat, client in PATH_TOKENS + NAME_TOKENS:
        for m in pat.finditer(text, limit_lo, off):
            dist = off - m.end()
            is_path = (pat, client) in PATH_TOKENS
            if best is None or dist < best[0] or (dist == best[0] and is_path and not best[2]):
                best = (dist, client, is_path)
    if best is None:
        return None
    win = best[0]
    clients = []
    for pat, client in PATH_TOKENS + NAME_TOKENS:
        for m in pat.finditer(text, limit_lo, off):
            if win <= off - m.end() <= win + 4 and client not in clients:
                clients.append(client)
    return clients


def scope_of(fname, line):
    for (f, s, e, cls, ml, mr) in SCOPE:
        if f == fname and s <= line <= e:
            return (cls, ml, mr)
    return (None, None, None)


def assert_markers(filelines):
    """G15: every declared DATED range must carry its marker text.
    G18: the marker line must lie inside the range it dates."""
    errs = []
    for (f, s, e, cls, ml, mr) in SCOPE:
        if cls != "DATED" or ml is None:
            continue
        lines = filelines.get(f)
        if not lines:
            errs.append("%s:%d marker uncheckable (file unreadable)" % (f, ml))
            continue
        if not (s <= ml <= e):
            errs.append("%s:%d marker line outside its own declared range %d-%d (G18)"
                        % (f, ml, s, e))
        if not (1 <= ml <= len(lines)) or not re.search(mr, lines[ml - 1]):
            errs.append("%s:%d marker %r absent from %r" %
                        (f, ml, mr, (lines[ml - 1][:70] if 1 <= ml <= len(lines) else "<beyond EOF>")))
    return errs


def frontier_check(filelines):
    """G21 (r10): assert the frontier-claim register directly on bullet text.
    Locus-free bullets never reach classify(), so this is the only grading
    they get: REQUIRED anchors are the positive floor (a stripped, rewritten
    or truncated bullet fails REQUIRED-absent), FORBIDDEN literals name the
    retracted claims whose reintroduction must fail the run (FRONTIER-STALE)."""
    errs = []
    for (f, s, e, req, forb) in FRONTIER:
        lines = filelines.get(f)
        if not lines:
            errs.append("%s:%d-%d frontier uncheckable (file unreadable)" % (f, s, e))
            continue
        seg = "\n".join(lines[s - 1:e])
        for pat in req:
            if not re.search(pat, seg, re.I):
                errs.append("%s:%d-%d REQUIRED %r absent (G21 frontier register)"
                            % (f, s, e, pat))
        for pat in forb:
            m = re.search(pat, seg, re.I)
            if m:
                errs.append("%s:%d-%d FORBIDDEN %r matched %r (FRONTIER-STALE)"
                            % (f, s, e, pat, m.group(0)))
    registered_starts = {(f, s) for f, s, e, req, forb in FRONTIER}
    for f, heading, level in FRONTIER_SECTIONS:
        lines = filelines.get(f)
        if not lines:
            continue
        starts = [i for i, line in enumerate(lines) if line.strip() == heading]
        if len(starts) != 1:
            errs.append("%s: heading %r occurs %d times (FRONTIER-UNEVALUABLE)"
                        % (f, heading, len(starts)))
            continue
        start = starts[0]
        end = len(lines)
        for i in range(start + 1, len(lines)):
            match = SECTION.match(lines[i])
            if match and len(match.group(0).split()[0]) <= level:
                end = i
                break
        for i in range(start + 1, end):
            if BULLET.match(lines[i]) and (f, i + 1) not in registered_starts:
                errs.append("%s:%d unregistered bullet in %r (FRONTIER-UNEVALUABLE)"
                            % (f, i + 1, heading))
    return errs


def cache_versions():
    """G17: every version present in an npx rea-agents cache."""
    vers = set()
    base = os.path.join(HOME, ".npm", "_npx")
    try:
        for h in os.listdir(base):
            pkg = os.path.join(base, h, "node_modules", "rea-agents", "package.json")
            try:
                m = re.search(r'"version"\s*:\s*"(\d+\.\d+\.\d+)"',
                              open(pkg, encoding="utf-8", errors="replace").read())
            except OSError:
                continue
            if m:
                vers.add(m.group(1))
    except OSError:
        pass
    return vers


def ptr_check(ptr_path, lineno, live):
    path = os.path.expanduser(ptr_path)
    try:
        lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
    except OSError as ex:
        return "unresolved", "unreadable (%s)" % type(ex).__name__
    if not (1 <= lineno <= len(lines)):
        return "unresolved", "line %d beyond EOF (%d lines)" % (lineno, len(lines))
    content = lines[lineno - 1]
    m = re.search(r"rea-agents@(\d+\.\d+\.\d+)", content)
    if not m:
        return "stale", "line holds no rea-agents pin: %r" % content.strip()[:60]
    for pat, c in PATH_TOKENS:
        if pat.search(ptr_path):
            if live.get(c) and m.group(1) != live[c]:
                return "stale", "pins %s but live %s=%s" % (m.group(1), c, live[c])
    return "ok", "pins %s" % m.group(1)


def cache_check(h, stated):
    pkg = "%s/.npm/_npx/%s/node_modules/rea-agents/package.json" % (HOME, h)
    try:
        txt = open(pkg, encoding="utf-8", errors="replace").read()
    except OSError:
        return "unresolved", "no cache at _npx/%s" % h
    m = re.search(r'"version"\s*:\s*"(\d+\.\d+\.\d+)"', txt)
    if not m:
        return "unresolved", "no version field in _npx/%s" % h
    if stated and m.group(1) != stated:
        return "stale", "cache holds %s, statement says %s" % (m.group(1), stated)
    return "ok", "cache holds %s" % m.group(1)


def classify(fname, lines, live, out):
    loci = []
    for (a, b, text) in units(lines):
        if not REA_GATE.search(text):
            continue
        occ, spans = [], []
        for m in PIN.finditer(text):
            occ.append(("pin", m.start(), m.group(1)))
            spans.append((m.start(), m.end()))
        for m in VER.finditer(text):
            if any(s <= m.start() < e for s, e in spans):
                continue
            occ.append(("bare", m.start(), m.group(0)))
        for m in PTR.finditer(text):
            occ.append(("ptr", m.start(), m.group(0)))
        if not occ:
            continue
        det = []
        for kind, off, val in occ:
            phys = line_of(lines, a, b, off)
            cls, ml, mr = scope_of(fname, phys)
            inline = bool(INLINE_MARKER.search(lines[phys - 1]))
            marker = "inline:%d" % phys if inline else ("scope-marker:%d" % ml if ml else None)
            lo, hi = clause_bounds(text, off)
            clause = text[lo:hi]
            clients = nearest_client(text, off, limit_lo=lo)
            cache_h = CACHE.search(text[lo:hi])
            if kind == "pin":
                target = clients or [None]
            elif cache_h:
                target = ["__cache__"]
            elif kind == "bare":
                target = clients or [None]
            else:
                target = ["__ptr__"]
            for c in target:
                if c == "__cache__":
                    state, why = cache_check(cache_h.group(1), val)
                    disp = {"ok": "current-ok", "stale": "STALE", "unresolved": "UNRESOLVED"}[state]
                elif c == "__ptr__":
                    pm = PTR.search(text, off)
                    state, why = ptr_check(pm.group(1), int(pm.group(2)), live)
                    if state == "stale" and cls == "DATED":
                        disp, why = "historical", "dated scope"
                    else:
                        disp = {"ok": "current-ok", "stale": "STALE", "unresolved": "UNRESOLVED"}[state]
                elif c is None:
                    if cls == "DATED":
                        disp, why = "historical", "dated scope"
                    elif inline:
                        disp, why = "historical", "inline marker"
                    elif re.search(r"doctor|expects|skill|reports|aligned|stale", clause, re.I):
                        # G17: version-intrinsic claim, not a client-surface claim
                        if val in cache_versions():
                            disp, why = "current-ok", "version-intrinsic; %s cache exists" % val
                        else:
                            disp, why = "UNRESOLVED", "version-intrinsic; no cache for %s" % val
                    else:
                        disp, why = "AMBIGUOUS", "no client token in clause"
                else:
                    if val == live.get(c):
                        disp, why = "current-ok", "matches live %s" % c
                    elif cls == "DATED" or inline:
                        disp, why = "historical", "dated scope" if cls == "DATED" else "inline marker"
                    else:
                        disp, why = "STALE", "live %s=%s" % (c, live.get(c))
                # G16: a value equal to ANY live anchor is a true statement, so a
                # DATED section may not re-label it historical.
                if disp == "historical" and val and val in live.values() \
                   and not re.search(r"6\.4\.0", str(val)):
                    disp, why = "current-ok", "value equals a live anchor"
                det.append({"kind": kind, "client": c, "value": val, "line": phys,
                            "scope": cls, "disp": disp, "marker": marker, "why": why})
        if not det:
            continue
        disps = {d["disp"] for d in det}
        if any(d["scope"] is None and d["disp"] != "historical" for d in det):
            disp = "UNDECLARED"
        elif "STALE" in disps:
            disp = "STALE"
        elif "UNRESOLVED" in disps:
            disp = "UNRESOLVED"
        elif "AMBIGUOUS" in disps:
            disp = "AMBIGUOUS"
        elif disps == {"historical"}:
            disp = "historical"
        elif disps == {"current-ok"}:
            disp = "current-ok"
        else:
            disp = "info"
        g11 = (disp == "current-ok") and not RECEIPT.search(text)
        rec = {"file": fname, "block": "%d-%d" % (a + 1, b + 1), "disp": disp,
               "asserts": det, "g11_no_receipt": g11, "text": text[:170]}
        loci.append(rec)
        out.setdefault(disp, []).append(rec)
        if g11:
            out.setdefault("g11", []).append("%s:%d" % (fname, det[0]["line"]))
        if disp in ("current-ok", "STALE") and HOLDING.search(text) and not HOLDING_OK.search(text):
            out.setdefault("g7", []).append("%s:%d" % (fname, det[0]["line"]))
    return loci


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="/home/vgpnk/Projects/shokunin/kaidoku-shokunin")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()
    files = sorted({s[0] for s in SCOPE})
    live = live_pins()
    if not all(live.values()):
        print("ANCHOR-FAIL: %r" % live)
        return 2
    out, counts, filelines, unreadable = {}, {}, {}, []
    for f in files:
        max_end = max([s[2] for s in SCOPE if s[0] == f]
                      + [r[2] for r in FRONTIER if r[0] == f], default=0)
        try:
            lines = open(os.path.join(args.root, f), encoding="utf-8", errors="replace").read().splitlines()
        except OSError as ex:
            unreadable.append("%s: %s" % (f, type(ex).__name__))
            counts[f] = {"lines": None, "loci": None}
            filelines[f] = None
            continue
        if len(lines) < max_end:
            # G19: declared rows past EOF are unevaluable, never a silent zero.
            unreadable.append("%s: %d lines < declared max %d (rows beyond EOF)"
                              % (f, len(lines), max_end))
            counts[f] = {"lines": None, "loci": None}
            filelines[f] = None
            continue
        filelines[f] = lines
        counts[f] = {"lines": len(lines), "loci": len(classify(f, lines, live, out))}
    scope_errors = assert_markers(filelines)
    frontier_errors = frontier_check(filelines)
    stale, unatt = out.get("STALE", []), out.get("AMBIGUOUS", [])
    undecl = out.get("UNDECLARED", [])
    unres = out.get("UNRESOLVED", [])
    g11, g7 = out.get("g11", []), out.get("g7", [])
    # G20 (r9, H3): the old second disjunct was true exactly when the run found
    # nothing, so a blind instrument read PASS.  The floor is PER READABLE FILE
    # over current-ok DETECTIONS (EX-14's variant B, measured to dominate the
    # global variant A on head/blind/nullskill): every scoped file the run
    # could read must contribute >= 1 current-ok assertion, so a per-file
    # collapse (needles stripped, content blanked) is declared even when other
    # files stay loud.  Dets are counted, not blocks: SKILL.md's only
    # locus-bearing block is mixed (current-ok + historical) and carries block
    # disposition "info", so a block-count floor false-FAILs the ordinary run
    # (measured; EX-14's §6 snippet as written reproduces that false FAIL).
    # Unreadable files are exempt here -- they are the H1 class and already
    # force FAIL via `unreadable`.  Per-ROW floors are refuted by EX-14's map
    # (4 DATED rows are zero-locus by design at HEAD).
    n_loci = sum((c["loci"] or 0) for c in counts.values())
    n_current_ok = sum(1 for recs in out.values() if isinstance(recs, list)
                       for rec in recs if isinstance(rec, dict)
                       for d in rec["asserts"] if d["disp"] == "current-ok")
    floor = {f: 0 for f in files}
    for recs in out.values():
        if not isinstance(recs, list):
            continue
        for rec in recs:
            if not isinstance(rec, dict):
                continue
            for d in rec["asserts"]:
                if d["disp"] == "current-ok":
                    floor[rec["file"]] += 1
    h3_ok = all(floor[f] > 0 for f in files if filelines[f] is not None)
    g2_ok = h3_ok
    frontier_class = (["FRONTIER-STALE"] if any("FORBIDDEN" in e for e in frontier_errors)
                      else ["FRONTIER-UNEVALUABLE"] if frontier_errors else [])
    declared = (["UNREADABLE"] if unreadable else []) + ([] if g2_ok else ["BLIND-INSTRUMENT"]) \
               + frontier_class
    ok = (not stale) and (not unatt) and (not undecl) and (not unres) and (not scope_errors) \
         and (not g11) and g2_ok and (not unreadable) and (not frontier_errors)
    verdict = "PASS" if ok else "FAIL"
    if args.json:
        print(json.dumps({"live": live, "counts": counts, "verdict": verdict,
                          "stale": stale, "ambiguous": unatt, "undeclared": undecl,
                          "unresolved": unres, "scope_errors": scope_errors,
                          "unreadable": unreadable, "declared_fail_classes": declared,
                          "frontier_rows": len(FRONTIER), "frontier_errors": frontier_errors,
                          "g2_ok": g2_ok, "g2_floor": "1/readable-file", "current_ok_per_file": floor,
                          "g11": g11, "g7": g7,
                          "historical": out.get("historical", []),
                          "current_ok": out.get("current-ok", [])}, indent=1))
        return 0 if verdict == "PASS" else 1
    print("live anchors (re-derived): %r" % live)
    for f, c in counts.items():
        print("%-14s lines=%-4s loci=%s" % (f, c["lines"], c["loci"]))
    if not args.quiet:
        for k in ("STALE", "AMBIGUOUS", "UNDECLARED", "UNRESOLVED",
                  "historical", "current-ok", "info"):
            v = out.get(k, [])
            print("\n-- %s (%d) --" % (k.upper(), len(v)))
            for r in v:
                print("  %s block %s [scope %s]%s" % (r["file"], r["block"],
                      r["asserts"][0]["scope"] if r["asserts"] else "?",
                      "  [no receipt language]" if r["g11_no_receipt"] else ""))
                for d in r["asserts"]:
                    print("      :%d [%s] %s=%s -> %s (%s)" %
                          (d["line"], d["kind"], d["client"], d["value"], d["disp"], d["why"]))
    print("\nSCOPE-ERRORS (marker assertions): %r" % scope_errors)
    print("FRONTIER register (G21): %d rows asserted, errors: %r"
          % (len(FRONTIER), frontier_errors))
    print("UNREADABLE (could-not-evaluate): %r" % unreadable)
    print("G2 positive-assertion guard: %s (current-ok loci per file: %s; total loci=%d; floor=1/file)"
          % ("ok" if g2_ok else "SUSPECT",
             ", ".join("%s=%d" % (f, floor[f]) for f in files), n_loci))
    print("G7 configured!=held warnings: %r" % g7)
    print("G11 current-ok without receipt language: %r" % g11)
    print("DECLARED FAIL CLASSES: %r" % declared)
    print("VERDICT: %s  (stale=%d ambiguous=%d undeclared=%d unresolved=%d)"
          % (verdict, len(stale), len(unatt), len(undecl), len(unres)))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
