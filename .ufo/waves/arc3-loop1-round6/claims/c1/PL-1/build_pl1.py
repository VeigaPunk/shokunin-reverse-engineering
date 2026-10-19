import re
src=open('/var/tmp/pl1-arc3r6/pl4-r10.py').read()

old_table = src[src.index('FRONTIER = ['):src.index('\nPIN = re.compile')]
new_table = '''FRONTIER = [
    # (file, start, end, anchor_line, anchor_regex, [REQUIRED...], [FORBIDDEN...])
    # ANCHOR: the declared line must match anchor_regex -- a reflow or insertion
    # that shifts the region fails loudly (FRONTIER-ANCHOR) instead of silently
    # grading shifted lines. REQUIRED (positive floor) and FORBIDDEN (retracted
    # literals) run against the span with whitespace collapsed, so a literal
    # PROVINCE's ~80-col wrap splits across lines still matches.
    # FORBIDDEN provenance, derived first-hand from `git show 40de383~1:PROVINCE.md`
    # (all three are that commit's before-state, repaired in 40de383):
    #   :92-93  "real solc/vyper-compiled bytecode untested"
    #   :139-141 "hits REA's ~900s internal session deadline"
    #   :157-159 "probe-refused since r2"
    ("PROVINCE.md", 73, 73, 73, r"^## Frontier$", [], []),
    ("PROVINCE.md", 75, 80, 75, r"Claimed in MINT\\.md, not yet held",
     [r"Claimed in MINT\\.md, not yet held"], []),
    ("PROVINCE.md", 82, 83, 82, r"\\*\\*PE subtypes\\*\\*",
     [r"PE subtypes", r"x86-64 AND ARM64"], []),
    ("PROVINCE.md", 84, 86, 84, r"Recorded crashes >32 MiB",
     [r"32 MiB", r"oldest-first"], []),
    ("PROVINCE.md", 87, 88, 87, r"\\*\\*Alternate providers\\*\\*",
     [r"Alternate providers", r"\\bIDA\\b"], []),
    ("PROVINCE.md", 89, 90, 89, r"\\*\\*macOS-only surfaces\\*\\*", [r"unsupported_host"], []),
    ("PROVINCE.md", 91, 93, 91, r"\\*\\*EVM bytecode \\(extended\\)\\*\\*",
     [r"EVM bytecode", r"solc-0\\.8\\.37", r"vyper-0\\.4\\.3"],
     [r"untested"]),
    ("PROVINCE.md", 133, 133, 133, r"^### Round-4 frontier \\(post-unlock\\)$", [], []),
    ("PROVINCE.md", 135, 138, 135, r"\\*\\*RISC-V analysis\\*\\*", [r"RISC-V", r"r5-01"], []),
    ("PROVINCE.md", 139, 144, 139, r"\\*\\*>90 MB PE scale wall\\*\\*",
     [r"90 MB PE", r"arc2-r7", r"CLOSED"],
     [r"hits REA's ~900s internal session deadline"]),
    ("PROVINCE.md", 145, 146, 145, r"source mapping\\*\\*", [r"\\.jsc", r"Ignition"], []),
    ("PROVINCE.md", 147, 148, 147, r"\\*\\*sasquatch\\*\\*", [r"sasquatch", r"unblob"], []),
    ("PROVINCE.md", 149, 150, 149, r"\\*\\*adb device surface\\*\\*",
     [r"adb device surface", r"22/24"], []),
    ("PROVINCE.md", 151, 156, 151, r"\\*\\*Signal/1Password-scale asar analysis\\*\\*",
     [r"1Password", r"asar"], []),
    ("PROVINCE.md", 157, 160, 157, r"\\*\\*Cross-version residuals\\*\\*",
     [r"Cross-version", r"r12-02|r14-01", r"EXERCISED"],
     [r"probe-refused since r2"]),
    ("PROVINCE.md", 161, 162, 161, r"\\*\\*Operator-gated, still absent\\*\\*",
     [r"Operator-gated", r"\\bIDA\\b"], []),
]
'''
src = src.replace(old_table, new_table)

old_fn = src[src.index('def frontier_check(filelines):'):src.index('\ndef cache_versions():')]
new_fn = '''def frontier_check(filelines):
    """G21 (r10, PL-1 verification build): assert the frontier-claim register
    directly on bullet text. Locus-free bullets never reach classify(), so this
    is the only grading they get: an ANCHOR at each declared line (a reflow or
    insertion that shifts the region fails loudly instead of silently grading
    shifted lines), REQUIRED anchors as the positive floor, and FORBIDDEN
    literals naming retracted claims whose reintroduction must fail the run.
    REQUIRED/FORBIDDEN run against the span with whitespace collapsed, so a
    literal split by PROVINCE's line wrap is still seen."""
    errs = []
    for (f, s, e, al, ar, req, forb) in FRONTIER:
        lines = filelines.get(f)
        if not lines:
            errs.append(("FRONTIER-UNEVALUABLE",
                         "%s:%d-%d frontier uncheckable (file unreadable)" % (f, s, e)))
            continue
        if not (1 <= al <= len(lines)) or not re.search(ar, lines[al - 1], re.I):
            errs.append(("FRONTIER-ANCHOR",
                         "%s:%d anchor %s absent (row %d-%d needs re-key)"
                         % (f, al, ar, s, e)))
            continue
        seg = re.sub(r"\\s+", " ", "\\n".join(lines[s - 1:e]))
        for pat in req:
            if not re.search(pat, seg, re.I):
                errs.append(("FRONTIER-UNEVALUABLE",
                             "%s:%d-%d REQUIRED %s absent (G21 frontier register)"
                             % (f, s, e, pat)))
        for pat in forb:
            m = re.search(pat, seg, re.I)
            if m:
                errs.append(("FRONTIER-STALE",
                             "%s:%d-%d FORBIDDEN %s matched %s (FRONTIER-STALE)"
                             % (f, s, e, pat, m.group(0))))
    return errs
'''
src = src.replace(old_fn, new_fn)

old_cls = """    frontier_class = (["FRONTIER-STALE"] if any("FORBIDDEN" in e for e in frontier_errors)
                      else ["FRONTIER-UNEVALUABLE"] if frontier_errors else [])"""
new_cls = """    frontier_class = sorted({cls for cls, _ in frontier_errors})"""
assert old_cls in src
src = src.replace(old_cls, new_cls)

old_json = '"frontier_rows": len(FRONTIER), "frontier_errors": frontier_errors,'
new_json = ('"frontier_rows": len(FRONTIER),\n'
            '                          "frontier_errors": ["%s %s" % (c, m) for c, m in frontier_errors],')
assert old_json in src
src = src.replace(old_json, new_json)

old_print = """    print("FRONTIER register (G21): %d rows asserted, errors: %r"
          % (len(FRONTIER), frontier_errors))"""
new_print = """    print("FRONTIER register (G21): %d rows asserted, errors: %r"
          % (len(FRONTIER), ["%s %s" % (c, m) for c, m in frontier_errors]))"""
assert old_print in src
src = src.replace(old_print, new_print)

open('/var/tmp/pl1-arc3r6/pl1-r10.py','w').write(src)
print("built pl1-r10.py", len(src.splitlines()), "lines")
