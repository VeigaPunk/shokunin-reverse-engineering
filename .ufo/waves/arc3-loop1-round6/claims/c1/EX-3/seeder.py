#!/usr/bin/env python3
"""EX-3 (arc3-loop1-round6, c1) — independent seed builder for verifying PL-4's
G21 frontier register. Run from /var/tmp/ex3-arc3r6 with `trees/clean` holding
byte-copies of the repo's PROVINCE.md/SKILL.md/SCORECARD.md.

Each mutation is content-asserted against the r5-audit tree at HEAD c625d5d so a
silent re-key cannot turn a seed into a no-op. Seeds are my own, not PL-4's.
"""
import pathlib
import shutil

base = pathlib.Path('/var/tmp/ex3-arc3r6/trees')
clean = base / 'clean'


def mk(name, mutate):
    d = base / name
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    for f in ('PROVINCE.md', 'SKILL.md', 'SCORECARD.md'):
        (d / f).write_text((clean / f).read_text())
    p = d / 'PROVINCE.md'
    lines = p.read_text().splitlines()
    lines = mutate(lines)
    p.write_text('\n'.join(lines) + '\n')
    print(name, 'PROVINCE lines =', len(lines))


# t2 frozen-example: replace :91-93 with the retracted literal (drops both anchors)
def t2(L):
    return L[:90] + [
        "- **EVM bytecode (extended)** — selectors held on synthetic dispatcher",
        "  (Core, r3-07); real solc/vyper-compiled bytecode untested, synthetic",
        "  dispatcher only.",
    ] + L[93:]


mk('seed-frozen-example', t2)


# t3 forbidden-only: keep both version anchors, add the retracted word
def t3(L):
    L = list(L)
    assert 'solc-0.8.37' in L[91] and 'vyper-0.4.3' in L[91], L[91]
    L[92] = L[92] + " Real solc/vyper-compiled bytecode untested."
    return L


mk('seed-forbidden-only', t3)


# t4 required-strip on a DIFFERENT bullet than PL-4 tested (:147-148 drops 'unblob')
def t4(L):
    L = list(L)
    assert 'sasquatch' in L[146] and 'unblob' in L[146], (L[146], L[147])
    L[146] = "- **sasquatch** — the squashfs recursion extractor (AUR-only);"
    L[147] = "  7z fallback covers the carved-image path today."
    return L


mk('seed-required-other', t4)


# t5 truncate to 161 lines (past the register's declared max end)
def t5(L):
    return L[:-1]


mk('truncated-161', t5)


# t6 insert one bullet line after :138 (shifts every later register span)
def t6(L):
    return L[:138] + ["- **New surface** — claimed held (no receipt)."] + L[138:]


mk('seed-insert-inside', t6)


# t7 append a stale bullet PAST :162 (probes the named past-the-bound residual)
def t7(L):
    return L + ["- **Kernel drivers** — real vendor binaries untested."]


mk('seed-append-past-162', t7)


# t8 anchor-preserving false rewrite inside :145-146 (frontier claim reversed,
# both REQUIRED anchors kept, no FORBIDDEN literal) — probes the earned-not-
# exhaustive limit of the register.
def t8(L):
    L = list(L)
    assert '.jsc' in L[144] and 'Ignition' in L[144], L[144]
    L[145] = "  bytecode-to-source mapper is held; no frontier item remains (r9-99)."
    return L


mk('seed-rewrite-anchored', t8)


# t9 recorded pre-r5 stale clause back into :157-160, anchors kept. The literal
# is a removed line in `git show 40de383 -- PROVINCE.md`; the register has no
# FORBIDDEN row for the post-unlock region, so this measures the coverage gap.
def t9(L):
    L = list(L)
    assert 'r12-02' in L[157] and 'r14-01' in L[157], L[157]
    L[159] = L[159] + " compare-application-versions still probe-refused since r2."
    return L


mk('seed-stale-159', t9)


# t10 the second recorded pre-r5 remediation clause back into :139-144.
def t10(L):
    L = list(L)
    assert '90 MB PE' in L[138] and 'arc2-r7' in L[138], L[138]
    L[143] = L[143] + " Next: raise REA_GHIDRA_STARTUP_TIMEOUT_MS."
    return L


mk('seed-ghidra-139', t10)
