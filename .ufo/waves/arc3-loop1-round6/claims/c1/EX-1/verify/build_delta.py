#!/usr/bin/env python3
"""EX-1 scratch-only delta: add a REGION coverage assertion to PL-4's r10.

NOT applied to the gate. Builds /var/tmp/ex1-arc3r6/r10-coverage.py from the
patched r10 copy, then this file is diffed against r10 for the artifact.
"""
SRC = "/var/tmp/ex1-arc3r6/r10-from-patch/c1-census-v10-r10.py"
DST = "/var/tmp/ex1-arc3r6/r10-coverage.py"

s = open(SRC, encoding="utf-8").read()

anchor = '''PIN = re.compile(r"rea-agents@(\\d+\\.\\d+\\.\\d+)", re.I)'''
assert anchor in s, "PIN anchor not found"

regions = '''REGIONS = [
    ("PROVINCE.md", 73, 94, {73: r"^## Frontier$"}),
    ("PROVINCE.md", 133, 162, {133: r"^### Round-4 frontier \\(post-unlock\\)$"}),
]
# rows whose span is a single bullet: the first line must open a bullet and no
# later line in the span may open another one (a compensated insertion puts a
# second bullet inside a shifted window).
FRONTIER_SHAPE = {("PROVINCE.md", s): "bullet" for s in
                  (82, 84, 87, 89, 91, 135, 139, 145, 147, 149, 151, 157, 161)}

'''

s = s.replace(anchor, regions + anchor, 1)

fn_anchor = '''def frontier_check(filelines):'''
assert fn_anchor in s

region_fn = '''def region_check(filelines):
    """EX-1 delta (G22): every non-blank line inside a declared frontier region
    must sit in a FRONTIER row span (or be a declared header anchor), and no
    non-blank content may sit past the declared tail.  Without this, a new
    bullet inserted at :132-:135 is absorbed by the shifted REQUIRED windows
    (measured: the frozen stale literal at :134 read PASS exit 0)."""
    errs = []
    for (f, s, e, anchors) in REGIONS:
        lines = filelines.get(f)
        if not lines:
            continue  # frontier_check already reports the unreadable row
        covered = set()
        for (rf, rs, re_, req, forb) in FRONTIER:
            if rf == f:
                covered.update(range(rs, re_ + 1))
                if FRONTIER_SHAPE.get((rf, rs)) == "bullet":
                    span = lines[rs - 1:min(re_, len(lines))]
                    if span and not span[0].strip().startswith("- **"):
                        errs.append("%s:%d registered bullet no longer opens its span (FRONTIER-UNREGISTERED)"
                                    % (f, rs))
                    for off, seg in enumerate(span[1:], start=1):
                        if seg.strip().startswith("- **"):
                            errs.append("%s:%d second bullet inside registered span %d-%d (FRONTIER-UNREGISTERED)"
                                        % (f, rs + off, rs, re_))
        for ln in range(s, min(e, len(lines)) + 1):
            seg = lines[ln - 1]
            if ln in anchors:
                if not re.search(anchors[ln], seg):
                    errs.append("%s:%d REGION anchor mismatch %r (FRONTIER-UNREGISTERED)"
                                % (f, ln, seg.strip()[:60]))
                continue
            if not seg.strip():
                continue
            if ln not in covered:
                errs.append("%s:%d non-registered content %r (FRONTIER-UNREGISTERED)"
                            % (f, ln, seg.strip()[:80]))
        if e == max(r[2] for r in FRONTIER if r[0] == f):
            for ln in range(e + 1, len(lines) + 1):
                if lines[ln - 1].strip():
                    errs.append("%s:%d content past declared tail %d: %r (FRONTIER-UNREGISTERED)"
                                % (f, ln, e, lines[ln - 1].strip()[:80]))
    return errs


'''

s = s.replace(fn_anchor, region_fn + fn_anchor, 1)

old = "    frontier_errors = frontier_check(filelines)"
new = "    frontier_errors = frontier_check(filelines) + region_check(filelines)"
assert old in s
s = s.replace(old, new, 1)

open(DST, "w", encoding="utf-8").write(s)
print("wrote", DST, len(s.splitlines()), "lines")
