#!/usr/bin/env python3
"""RV-9 (chain c2) — ordinary-run verdict byte-identity audit, arc3-loop1-round2.

Runs nothing itself: takes two captured verdict files and asserts the second is
byte-identical to the first except for *exempt header/version lines*.

Exemption is a narrow whitelist applied PER LINE, and every exempt line is
printed with the rule that exempted it (no silent laundering):

  H1 banner     line names the instrument/version, e.g. 'C1 census vNN',
                'instrument vN', or a bare 'vN', or a version-comment banner.
  H2 digest     line carries an instrument sha256/digest identity.
  H3 title      a leading '# ...' / '===' style banner introduced by the edit.

Everything else is SUBSTANTIVE and must be byte-identical in the same order.
Exit 0 only if every difference is exempt; 1 otherwise.
Usage: verdict-identity.py <pre.out> <post.out>
"""
import re
import sys

BANNER = re.compile(r"\bcensus\b.*\bv\d+\b|\binstrument\b.*\bv\d+\b|^v\d+\b|\bv\d+\b\s*[-—(]")
DIGEST = re.compile(r"(sha256|digest)\b.*\b[0-9a-f]{8,}\b|\b[0-9a-f]{16,}\b")
TITLE = re.compile(r"^\s*(#{1,3}\s|={3,}|---)")


def classify(line):
    for name, rx in (("H1-banner", BANNER), ("H2-digest", DIGEST), ("H3-title", TITLE)):
        if rx.search(line):
            return name
    return None


def main():
    pre = open(sys.argv[1], "rb").read().decode("utf-8", "replace").splitlines()
    post = open(sys.argv[2], "rb").read().decode("utf-8", "replace").splitlines()
    if pre == post:
        print("IDENTICAL: the two verdicts are byte-identical (%d lines)."
              % len(pre))
        print("exempt lines used: none (no diff)")
        return 0
    import difflib
    sm = difflib.SequenceMatcher(None, pre, post, autojunk=False)
    exempt, substantive = [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        for ln in pre[i1:i2]:
            cls = classify(ln)
            (exempt if cls else substantive).append(
                ("-%s" % (cls or "SUBSTANTIVE"), ln))
        for ln in post[j1:j2]:
            cls = classify(ln)
            (exempt if cls else substantive).append(
                ("+%s" % (cls or "SUBSTANTIVE"), ln))
    print("pre lines=%d post lines=%d" % (len(pre), len(post)))
    print("EXEMPT (header/version) changed lines: %d" % len(exempt))
    for tag, ln in exempt:
        print("  %-14s %r" % (tag, ln))
    print("SUBSTANTIVE changed lines: %d" % len(substantive))
    for tag, ln in substantive:
        print("  %-14s %r" % (tag, ln))
    # order-preserving check on the substantive residue
    pre_sub = [l for l in pre if classify(l) is None]
    post_sub = [l for l in post if classify(l) is None]
    same_residue = pre_sub == post_sub
    print("substantive residue identical (order-preserving): %s" % same_residue)
    ok = not substantive and same_residue
    print("AUDIT: %s" % ("BYTE-IDENTICAL-EXCEPT-HEADER" if ok else "DIFFERS-SUBSTANTIVELY"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
