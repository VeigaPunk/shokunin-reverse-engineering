#!/usr/bin/env python3
"""RV-2 independent seeder. Builds scratch trees from the repo's byte copies,
asserts every edit landed, and keeps line counts explicit. No reuse of PL-4 code."""
import hashlib, os, shutil, sys

REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
BASE = "/var/tmp/rv2-arc3r6/trees"
FILES = ["PROVINCE.md", "SKILL.md", "SCORECARD.md"]

ORIG91_93 = [
    "- **EVM bytecode (extended)** \u2014 selectors held on synthetic dispatcher\n",
    "  (Core, r3-07), real solc-0.8.37 carriers (Core, arc3-r1/r3) and a vyper-0.4.3\n",
    "  carrier (arc3-r4); selectors stay bare hashes (no signature DB \u2192 no name resolution).\n",
]

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def mk(name):
    d = os.path.join(BASE, name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    for f in FILES:
        shutil.copyfile(os.path.join(REPO, f), os.path.join(d, f))
    return d

def lines_of(d):
    with open(os.path.join(d, "PROVINCE.md"), encoding="utf-8") as fh:
        return fh.read().splitlines(True)

def write_lines(d, ls):
    with open(os.path.join(d, "PROVINCE.md"), "w", encoding="utf-8") as fh:
        fh.writelines(ls)

def replace_span(d, start, end, new_lines):
    ls = lines_of(d)
    assert ls[start - 1:end] == ORIG91_93 if (start, end) == (91, 93) else True
    old = ls[start - 1:end]
    assert len(old) == end - start + 1
    ls[start - 1:end] = new_lines
    write_lines(d, ls)
    out = lines_of(d)
    assert out[start - 1:start - 1 + len(new_lines)] == new_lines
    return len(out)

trees = {}

# 0. clean
d = mk("clean")
assert len(lines_of(d)) == 162
for f in FILES:
    assert sha(os.path.join(d, f)) == sha(os.path.join(REPO, f)), f
trees["clean"] = (d, 162)

# 1. seeded-forbidden: the frozen claim's example literal, line-count neutral,
#    earning anchors removed (so REQUIRED and FORBIDDEN both fire)
d = mk("seeded-forbidden")
n = replace_span(d, 91, 93, [
    "- **EVM bytecode (extended)** \u2014 real solc/vyper-compiled bytecode untested,\n",
    "  synthetic dispatcher only; selectors stay bare hashes (no signature DB \u2192\n",
    "  no name resolution).\n",
])
assert n == 162
trees["seeded-forbidden"] = (d, n)

# 2. seeded-forbidden-only: anchors kept, only the retracted literal added
d = mk("seeded-forbidden-only")
n = replace_span(d, 91, 93, [
    "- **EVM bytecode (extended)** \u2014 selectors held on synthetic dispatcher\n",
    "  (Core, r3-07), real solc-0.8.37 carriers (Core, arc3-r1/r3) and a vyper-0.4.3\n",
    "  carrier (arc3-r4); real compiled bytecode untested; selectors stay bare hashes.\n",
])
assert n == 162
trees["seeded-forbidden-only"] = (d, n)

# 3. seeded-forbidden-case: case-insensitivity probe
d = mk("seeded-forbidden-case")
n = replace_span(d, 91, 93, [
    "- **EVM bytecode (extended)** \u2014 selectors held on synthetic dispatcher\n",
    "  (Core, r3-07), real solc-0.8.37 carriers (Core, arc3-r1/r3) and a vyper-0.4.3\n",
    "  carrier (arc3-r4); real compiled bytecode UnTeStEd; selectors stay bare hashes.\n",
])
assert n == 162
trees["seeded-forbidden-case"] = (d, n)

# 4. seeded-required-evm: earning anchors stripped
d = mk("seeded-required-evm")
n = replace_span(d, 91, 93, [
    "- **EVM bytecode (extended)** \u2014 see corpus.\n",
    "  No earning citations retained in this seeded arm.\n",
    "  (padding keeps the line count neutral)\n",
])
assert n == 162
trees["seeded-required-evm"] = (d, n)

# 5. seeded-required-riscv: r5-01 citation removed from :137
d = mk("seeded-required-riscv")
ls = lines_of(d)
assert "r5-01" in ls[136]
ls[136] = "  (receipt: corpus/knowledge/2026-10-13-riscv-bypass.md); full 29 MB EXEC\n"
assert "r5-01" not in ls[136]
write_lines(d, ls)
assert len(lines_of(d)) == 162
trees["seeded-required-riscv"] = (d, 162)

# 6. clean-truncated: 161 lines, content loss past :131 invisible to v10
d = mk("clean-truncated")
ls = lines_of(d)[:161]
write_lines(d, ls)
assert len(lines_of(d)) == 161
trees["clean-truncated"] = (d, 161)

# 7. seeded-insert-one: brand-new frontier bullet inserted at :135 (1-line shift).
#    Falsification probe for PL-4's "insertions inside :132-162 are caught" claim.
d = mk("seeded-insert-one")
ls = lines_of(d)
ls.insert(134, "- **Brand-new frontier item** \u2014 inserted after :134, no earning citation.\n")
write_lines(d, ls)
assert len(lines_of(d)) == 163
trees["seeded-insert-one"] = (d, 163)

for name, (d, n) in sorted(trees.items()):
    print("%-24s lines=%d  PROVINCE sha=%s" % (name, n, sha(os.path.join(d, "PROVINCE.md"))[:16]))
print("TREES-BUILT", len(trees))
