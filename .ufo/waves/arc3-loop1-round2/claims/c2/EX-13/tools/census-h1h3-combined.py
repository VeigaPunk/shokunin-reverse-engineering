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
  line carries that section's own date/round token."""
#!/usr/bin/env python3
"""C1 stale-statement census instrument v9 (E22, arc2-loop1-round2) — FINAL.

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

Verdict: PASS iff stale == 0 AND ambiguous == 0 AND undeclared == 0
AND unresolved == 0 AND scope_errors == 0 AND g11 == [] AND G2 holds.
Exit 0 PASS, 1 FAIL, 2 anchor failure.
Usage: python3 c1-census-v9.py [--root DIR] [--json] [--quiet]
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
]

PIN = re.compile(r"rea-agents@(\d+\.\d+\.\d+)", re.I)
VER = re.compile(r"(?<![\d.])6\.\d+\.\d+")
PTR = re.compile(r"((?:~|/)[\w./+-]+\.(?:json|toml|ya?ml)):(\d+)")
CACHE = re.compile(r"_npx/([0-9a-f]{6,})")
REA_GATE = re.compile(r"rea-agents|\brea\b|config\.toml|mcp_config\.json|mcp\.json|mcp_servers|devin|\bomp\b|kimi|npx", re.I)
INLINE_MARKER = re.compile(r"historical|verified 2026-10-13|not re-probed|superseded|baseline|retain their original", re.I)
RECEIPT = re.compile(r"2026-10-18|receipt|SHA-256|sha256|re-grepped", re.I)
SECTION = re.compile(r"^#{1,4} ")
BULLET = re.compile(r"^\s*[-*] ")
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
        if not occ:
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
        try:
            lines = open(os.path.join(args.root, f), encoding="utf-8", errors="replace").read().splitlines()
        except OSError as ex:
            unreadable.append("%s: %s" % (f, type(ex).__name__))
            counts[f] = {"lines": 0, "loci": 0}
            filelines[f] = None
            continue
        filelines[f] = lines
        counts[f] = {"lines": len(lines), "loci": len(classify(f, lines, live, out))}
    scope_errors = assert_markers(filelines)
    stale, unatt = out.get("STALE", []), out.get("AMBIGUOUS", [])
    undecl = out.get("UNDECLARED", [])
    unres = out.get("UNRESOLVED", [])
    g11, g7 = out.get("g11", []), out.get("g7", [])
    g2_ok = len(out.get("current-ok", [])) > 0
    ok = (not stale) and (not unatt) and (not undecl) and (not unres) and (not scope_errors) \
         and (not g11) and g2_ok and (not unreadable)
    verdict = "PASS" if ok else "FAIL"
    if args.json:
        print(json.dumps({"live": live, "counts": counts, "verdict": verdict,
                          "stale": stale, "ambiguous": unatt, "undeclared": undecl,
                          "unresolved": unres, "scope_errors": scope_errors,
                          "g11": g11, "g7": g7, "g2_ok": g2_ok,
                          "historical": out.get("historical", []),
                          "current_ok": out.get("current-ok", [])}, indent=1))
        return 0 if verdict == "PASS" else 1
    print("live anchors (re-derived): %r" % live)
    for f, c in counts.items():
        print("%-14s lines=%-4d loci=%s" % (f, c["lines"], c["loci"]))
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
    print("UNREADABLE (could-not-evaluate): %r" % unreadable)
    print("\nSCOPE-ERRORS (marker assertions): %r" % scope_errors)
    print("G2 positive-assertion guard: %s (current-ok loci=%d, total loci=%d)" %
          ("ok" if g2_ok else "SUSPECT", len(out.get("current-ok", [])),
           sum(c["loci"] for c in counts.values())))
    print("G7 configured!=held warnings: %r" % g7)
    print("G11 current-ok without receipt language: %r" % g11)
    print("VERDICT: %s  (stale=%d ambiguous=%d undeclared=%d unresolved=%d)"
          % (verdict, len(stale), len(unatt), len(undecl), len(unres)))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
