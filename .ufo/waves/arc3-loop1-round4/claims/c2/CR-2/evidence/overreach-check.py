#!/usr/bin/env python3
"""CR-2 overreach checker — wave arc3-loop1-round4, chain c2, seat CR-2.

Attack classes (seat line): (1) repair overreach — rewriting current text;
(2) scope creep into PROVINCE's authority/boundary statements;
(3) availability -> holding language.

Usage:  overreach-check.py <BASE-PROVINCE.md> <CAND-PROVINCE.md>

Exit 0 = no overreach flag; 1 = flags present; 2 = input error.
The real tree is never written; this reads two files only.
"""
import difflib
import re
import sys

# census v10 declared PROVINCE scope rows (file, start, end, class)
SCOPE = [
    (8, 13, "CURRENT"), (15, 26, "CURRENT"), (40, 43, "DATED"),
    (44, 44, "CURRENT"), (45, 62, "DATED"), (64, 71, "CURRENT"),
    (119, 131, "DATED"),
]

# content-anchored authority / boundary statements (baseline loci, by regex)
AUTHORITY = [
    (r"available\*?, not \*?held", "availability-vs-holding doctrine"),
    (r"ground moves to Core only after an end-to-end probe", "Core-promotion authority rule"),
    (r"The domain is a frontier, not a fence", "frontier boundary statement"),
    (r"Cross-lane registry this lane maintains", "cross-lane registry authority"),
    (r"never re-bases a sibling lane", "registry non-authority clause"),
    (r"Ground the lane refuses or defers", "Adjacent refusal boundary"),
    (r"never\s+absorbed", "non-absorption clause"),
    (r"operator-owned", "operator-ownership clause"),
    (r"never runs the installer", "installer refusal clause"),
    (r"Quality/safety verdicts on findings", "safety-refusal clause (SHONEN-pinned)"),
    (r"never \"is it safe", "safety-refusal wording"),
    (r"\(unowned\)", "unowned marker"),
    (r"REA's own\s+anti-trigger", "anti-trigger boundary"),
    (r"reported to the orchestrator", "orchestrator-escalation clause"),
]

# census G7 holding lexicon (instrument regex) + seat-line variants
HOLDING = re.compile(r"\bheld\b|\bholds\b|live[- ]verified|\blive-held\b|\bworks\b|\bworking\b", re.I)
HOLDING_OK = re.compile(r"configured|available|not held|availability|never stands|unowned", re.I)

# census gate + occurrence regexes (for the UNDECLARED-region hazard)
REA_GATE = re.compile(r"rea-agents|\brea\b|config\.toml|mcp_config\.json|mcp\.json|mcp_servers|devin|\bomp\b|kimi|npx", re.I)
PIN = re.compile(r"rea-agents@(\d+\.\d+\.\d+)", re.I)
VER = re.compile(r"(?<![\d.])6\.\d+\.\d+")
PTR = re.compile(r"((?:~|/)[\w./+-]+\.(?:json|toml|ya?ml)):(\d+)")

# the SHONEN.md:12 extracted range the citation-drift probe pins
SHONEN_RANGE = (88, 116)
SHONEN_NEEDLE = "Quality/safety verdicts on findings"
# PROVINCE.md:18 exact pins
LINE18_PINS = ["17:55:49Z receipt", "rea-agents@6.7.0"]

# the named stale item (frozen claim C2): the Frontier EVM bullet
FRONTIER = (73, 93)
ADJACENT = (95, 116)


def region(ln):
    if 8 <= ln <= 13: return "Surface-summary/Core header"
    if 15 <= ln <= 26: return "Drift-prone values"
    if 28 <= ln <= 36: return "Probe/reconciliation conventions (authority)"
    if 40 <= ln <= 71: return "Core tables / registry"
    if FRONTIER[0] <= ln <= FRONTIER[1]: return "Frontier"
    if ADJACENT[0] <= ln <= ADJACENT[1]: return "Adjacent (boundary)"
    if 119 <= ln <= 131: return "Round-4 additions to Core"
    if 133 <= ln <= 162: return "Round-4 frontier (post-unlock)"
    return "other"

# the frozen claim's declared census unit: Frontier bullets + surface-summary claims
IN_UNIT = lambda ln: (8 <= ln <= 13) or (15 <= ln <= 26) or (73 <= ln <= 93) or (133 <= ln <= 162)
CORE_TABLE = lambda ln: 40 <= ln <= 71


def scope_class(ln):
    for s, e, c in SCOPE:
        if s <= ln <= e:
            return c
    return "OUT-OF-SCOPE"


def occ_present(text):
    if PIN.search(text):
        return "pin"
    if VER.search(text):
        return "bare-version"
    if PTR.search(text):
        return "ptr"
    return None


def main(argv):
    if len(argv) != 3:
        print("usage: overreach-check.py BASE CAND", file=sys.stderr)
        return 2
    try:
        base = open(argv[1], encoding="utf-8").read().splitlines()
        cand = open(argv[2], encoding="utf-8").read().splitlines()
    except OSError as ex:
        print("cannot read input: %s" % ex, file=sys.stderr)
        return 2

    flags = []
    print("== identities ==")
    print("baseline lines=%d  candidate lines=%d" % (len(base), len(cand)))
    if len(base) != len(cand):
        flags.append("LINE-COUNT-MOVED %d -> %d (claim requires line count held)"
                     % (len(base), len(cand)))

    sm = difflib.SequenceMatcher(a=base, b=cand, autojunk=False)
    changed = []          # (ln, kind, oldtext, newtext)  kind: replace/insert/delete
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        if tag == "replace":
            n = max(i2 - i1, j2 - j1)
            for k in range(n):
                ln = i1 + k + 1
                o = base[i1 + k] if i1 + k < i2 else "<none>"
                nw = cand[j1 + k] if j1 + k < j2 else "<none>"
                changed.append((ln, "replace", o, nw))
        elif tag == "insert":
            for k in range(j1, j2):
                changed.append((j1 + 1, "insert", "<none>", cand[k]))
        elif tag == "delete":
            for k in range(i1, i2):
                changed.append((k + 1, "delete", base[k], "<none>"))

    print("\n== changed physical lines: %d ==" % len(changed))
    for ln, kind, o, nw in changed:
        print("  :%d [%s] region=%s scope=%s" % (ln, kind.upper(), region(ln), scope_class(ln)))
        if o != "<none>":
            print("      - %s" % o[:150])
        if nw != "<none>":
            print("      + %s" % nw[:150])

    # --- class 1: rewriting current/historical text outside the named item -----
    print("\n== class 1: repair overreach (non-named-line rewrites) ==")
    named_ok = []
    for ln, kind, o, nw in changed:
        r = region(ln)
        sc = scope_class(ln)
        if IN_UNIT(ln):
            named_ok.append(ln)
            continue
        if CORE_TABLE(ln):
            flags.append("CLASS1b out-of-unit Core-table edit :%d (%s, %s)" % (ln, r, sc))
            print("  FLAG :%d region=%s scope=%s — Core-table row, OUTSIDE the claim's declared "
                  "census unit (Frontier bullets + surface-summary claims)" % (ln, r, sc))
            continue
        flags.append("CLASS1 edit outside the declared unit: :%d (%s, %s)" % (ln, r, sc))
        print("  FLAG :%d region=%s scope=%s — outside the declared unit" % (ln, r, sc))
    if not flags or all("CLASS1" not in f for f in flags):
        print("  (no edit outside the declared unit; in-unit lines touched: %s)" % (named_ok or "none"))

    # --- class 2: scope creep into authority/boundary statements ---------------
    print("\n== class 2: scope creep into authority/boundary statements ==")
    creep = 0
    for ln, kind, o, nw in changed:
        # changed span only: the portion(s) that differ between old and new line
        if o == "<none>" or nw == "<none>":
            spans = [nw if o == "<none>" else o]
        else:
            sm2 = difflib.SequenceMatcher(a=o, b=nw, autojunk=False)
            spans = [o[i1:i2] for tag, i1, i2, j1, j2 in sm2.get_opcodes() if tag != "equal" and i2 > i1]
            spans += [nw[j1:j2] for tag, i1, i2, j1, j2 in sm2.get_opcodes() if tag != "equal" and j2 > j1]
        for rx, label in AUTHORITY:
            if any(re.search(rx, s) for s in spans):
                creep += 1
                flags.append("CLASS2 authority/boundary edit :%d (%s)" % (ln, label))
                print("  FLAG :%d %s — changed span touches this clause" % (ln, label))
    if creep == 0:
        print("  (no authority/boundary clause touched in any changed span)")

    # --- class 3: availability -> holding language -----------------------------
    print("\n== class 3: availability->holding language ==")
    hold = 0
    MITIG = re.compile(r"mitigated|RESULT-class|no availability|not held|unowned", re.I)

    def block_of(lines, ln0):
        """contiguous block containing line ln0 (1-based): stop at blank line,
        new list bullet, or heading."""
        i = ln0 - 1
        start = i
        while start > 0 and lines[start-1].strip() and not lines[start-1].lstrip().startswith("- ") and not lines[start-1].startswith("#"):
            start -= 1
        end = i
        while end + 1 < len(lines) and lines[end+1].strip() and not lines[end+1].lstrip().startswith("- ") and not lines[end+1].startswith("#"):
            end += 1
        return " ".join(lines[start:end+1])
    # target/wall usage: "held" describing an analyzed artifact (the wall/target
    # was held by the analyzer), not a capability holding
    # word-boundary PE; require a target/wall noun (the lane's "the wall/target HELD")
    TARGET = re.compile(r"\bwall\b|\btemplate\b|\bPE\b|\btarget\b|\bprocs\b|\bprocedures\b|75,218|91\.6|91MB")
    for ln, kind, o, nw in changed:
        if nw == "<none>":
            continue
        if not HOLDING.search(nw):
            continue
        # net-new only: the old line lacked a holding word
        if o != "<none>" and HOLDING.search(o):
            continue
        blk = block_of(cand, ln)
        if HOLDING_OK.search(blk) or MITIG.search(blk):
            print("  ok    :%d holding word qualified in its block (mitigated/RESULT-class/"
                  "configured/available/not-held): %s" % (ln, blk[:120]))
            continue
        if TARGET.search(blk):
            print("  ok    :%d holding word describes an analyzed target/wall (lane vocabulary, "
                  "not a capability claim): %s" % (ln, blk[:120]))
            continue
        hold += 1
        flags.append("CLASS3 net-new holding language without qualifier :%d" % ln)
        print("  FLAG :%d introduces holding language with no qualifier (block-scoped):" % ln)
        print("      + %s" % blk[:200])
    if hold == 0:
        print("  (no unqualified net-new holding language)")

    # --- hazard: gate+occurrence introduced into the undeclared 72-118 region --
    print("\n== hazard: census UNDECLARED loci (gate+pin/version/ptr in 72-118) ==")
    haz = 0
    for ln, kind, o, nw in changed:
        if nw == "<none>" or not (72 <= ln <= 118):
            continue
        if REA_GATE.search(nw) and occ_present(nw):
            haz += 1
            flags.append("UNDECLARED-hazard locus introduced :%d" % ln)
            print("  FLAG :%d gate+occ introduced outside declared scope: %s" % (ln, occ_present(nw)))
            print("      + %s" % nw[:150])
    if haz == 0:
        print("  (none)")

    # --- class 4: promotion-language overreach ---------------------------------
    print("\n== class 4: promotion language vs cited-entry scope ==")
    # corpus entries that disclaim Core promotion (measured at HEAD)
    NO_PROMO = [
        ("arc3-r1-evm-real-solc", r"arc3-r1"),
        ("arc3-r3-evm-optimizer-shapes", r"arc3-r3"),
    ]
    promo = 0
    for ln, kind, o, nw in changed:
        if nw == "<none>":
            continue
        for m in re.finditer(r"\(Core, ([^)]*)\)", nw):
            cited = m.group(1)
            for stem, rx in NO_PROMO:
                if re.search(rx, cited) and "r3-07" not in cited:
                    promo += 1
                    flags.append("CLASS4 promotion claim for a RESULT-class leg :%d" % ln)
                    print("  FLAG :%d names (%s) as Core, but corpus/knowledge/*%s* "
                          "reads 'RESULT-class, no Core promotion'" % (ln, cited, stem))
                    break
    if promo == 0:
        print("  (no Core-promotion claim on a RESULT-class leg)")

    # --- pinned invariants ------------------------------------------------------
    print("\n== pinned invariants (citation-drift probe) ==")
    def line_or_none(lines, ln):
        return lines[ln - 1] if 1 <= ln <= len(lines) else None
    l18 = line_or_none(cand, 18)
    for pin in LINE18_PINS:
        ok = l18 is not None and pin in l18
        print("  PROVINCE.md:18 contains %r: %s" % (pin, "yes" if ok else "NO"))
        if not ok:
            flags.append("PIN-BREAK PROVINCE.md:18 lacks %r" % pin)
    safety = [i + 1 for i, l in enumerate(cand) if SHONEN_NEEDLE in l]
    ok = len(safety) == 1 and SHONEN_RANGE[0] <= safety[0] <= SHONEN_RANGE[1]
    print("  safety-refusal clause at line(s) %s within SHONEN-pinned %d-%d: %s"
          % (safety, SHONEN_RANGE[0], SHONEN_RANGE[1], "yes" if ok else "NO"))
    if not ok:
        flags.append("PIN-BREAK safety clause moved out of %d-%d (now %s)"
                     % (SHONEN_RANGE[0], SHONEN_RANGE[1], safety))

    print("\n== SUMMARY ==")
    if flags:
        print("FLAGS: %d" % len(flags))
        for f in flags:
            print("  - %s" % f)
        print("RESULT: OVERREACH FLAGS PRESENT")
        return 1
    print("RESULT: CLEAN — no overreach flag in any of the three classes")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
