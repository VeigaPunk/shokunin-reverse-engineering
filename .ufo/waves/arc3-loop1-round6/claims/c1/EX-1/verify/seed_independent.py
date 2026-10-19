#!/usr/bin/env python3
"""EX-1 independent seeder for arc3-loop1-round6 c1 verification.

Builds byte-copies of the three scoped files from the repo head and applies
one content-asserted edit per tree. No PL-4 code is imported or reused.
"""
import hashlib, os, shutil, sys

REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
BASE = "/var/tmp/ex1-arc3r6/trees"
FILES = ["PROVINCE.md", "SKILL.md", "SCORECARD.md"]


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def fresh(name):
    d = os.path.join(BASE, name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    for f in FILES:
        shutil.copyfile(os.path.join(REPO, f), os.path.join(d, f))
    return d


def read(d):
    return open(os.path.join(d, "PROVINCE.md"), encoding="utf-8").read().splitlines()


def write(d, lines):
    with open(os.path.join(d, "PROVINCE.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def expect(cond, msg):
    if not cond:
        sys.exit("SEED ASSERTION FAILED: " + msg)


os.makedirs(BASE, exist_ok=True)
repo_prov = os.path.join(REPO, "PROVINCE.md")
base_lines = open(repo_prov, encoding="utf-8").read().splitlines()
expect(len(base_lines) == 162, "PROVINCE.md is 162 lines, got %d" % len(base_lines))
expect(base_lines[90].startswith("- **EVM bytecode (extended)**"), "line 91 is EVM bullet: %r" % base_lines[90])
expect("solc-0.8.37" in base_lines[91] and "vyper-0.4.3" in base_lines[91], "line 92 carries both carrier tokens")
expect(base_lines[132].startswith("### Round-4 frontier"), "line 133 is post-unlock header: %r" % base_lines[132])
expect("r5-01" in base_lines[136], "line 137 carries r5-01")
expect(base_lines[94].startswith("## Adjacent"), "line 95 is ## Adjacent: %r" % base_lines[94])

report = {}

# 0. clean: byte copies
d = fresh("clean")
expect(sha(os.path.join(d, "PROVINCE.md")) == sha(repo_prov), "clean PROVINCE byte-identical")
report["clean"] = {"edit": "byte copies", "lines": len(read(d)), "prov_sha": sha(os.path.join(d, "PROVINCE.md"))}

# 1. forbidden: reintroduce the frozen stale literal into :91-93, line-count neutral.
#    Keeps all REQUIRED anchors (EVM bytecode, solc-0.8.37, vyper-0.4.3) present.
d = fresh("forbidden")
lines = read(d)
expect(len(lines) == 162, "forbidden start 162")
lines[92] = "  carrier (arc3-r4); real solc/vyper-compiled bytecode untested, synthetic dispatcher only."
expect("untested" in "\n".join(lines[90:93]), "forbidden literal present in :91-93")
expect("solc-0.8.37" in "\n".join(lines[90:93]) and "vyper-0.4.3" in "\n".join(lines[90:93]), "required tokens kept")
write(d, lines)
expect(len(read(d)) == 162, "forbidden line-count neutral")
report["forbidden"] = {"edit": "PROVINCE.md:93 -> stale 'untested' literal, required tokens kept", "lines": 162}

# 2. required-evm: strip earning citations from :91-93 (positive floor), line-count neutral.
d = fresh("required-evm")
lines = read(d)
lines[90] = "- **EVM bytecode (extended)** — see corpus."
lines[91] = ""
lines[92] = ""
write(d, lines)
expect(len(read(d)) == 162, "required-evm line-count neutral")
report["required-evm"] = {"edit": "PROVINCE.md:91-93 earning tokens stripped", "lines": 162}

# 3. required-riscv: remove the r5-01 earning citation from :135-138.
d = fresh("required-riscv")
lines = read(d)
expect("r5-01" in lines[136], "riscv seed anchor")
lines[136] = lines[136].replace("(r5-01: `corpus/knowledge/2026-10-13-r5-01-riscv-bypass.md`)", "(see corpus)")
expect("r5-01" not in "\n".join(lines[134:138]), "r5-01 removed from :135-138")
write(d, lines)
report["required-riscv"] = {"edit": "PROVINCE.md:137 r5-01 citation removed", "lines": 162}

# 4. truncated: 161 lines (all other files intact) — silent content loss past SCOPE max 131.
d = fresh("truncated")
lines = read(d)[:161]
write(d, lines)
expect(len(read(d)) == 161, "truncated to 161")
report["truncated"] = {"edit": "PROVINCE.md truncated to 161 lines", "lines": 161}

# 5. append-163: brand-new stale bullet past the register bound (named residual).
d = fresh("append-163")
lines = read(d)
lines.append("- **New frontier claim** — real solc/vyper-compiled bytecode untested.")
write(d, lines)
expect(len(read(d)) == 163, "append 163")
report["append-163"] = {"edit": "stale bullet appended at :163 (past register bound)", "lines": 163}

# 6. insert-94: stale bullet inserted in the gap between the last registered
#    Frontier bullet (:93) and ## Adjacent (:95) — line-shifting.
d = fresh("insert-94")
lines = read(d)
lines.insert(93, "- **Inserted claim** — real solc/vyper-compiled bytecode untested.")
write(d, lines)
expect(len(read(d)) == 163 and read(d)[93] == "- **Inserted claim** — real solc/vyper-compiled bytecode untested.", "insert at 94")
report["insert-94"] = {"edit": "stale bullet inserted at :94, before ## Adjacent", "lines": 163}

# 7. insert-134: stale bullet inserted in the gap before the first post-unlock
#    registered bullet (:135) — line-shifting inside :133-162.
d = fresh("insert-134")
lines = read(d)
lines.insert(133, "- **Inserted post-unlock claim** — real solc/vyper-compiled bytecode untested.")
write(d, lines)
expect(len(read(d)) == 163 and read(d)[133].startswith("- **Inserted post-unlock claim**"), "insert at 134")
report["insert-134"] = {"edit": "stale bullet inserted at :134, first post-unlock slot", "lines": 163}

# 8. rewritten-claim: same bullet, REQUIRED anchors kept, a NEW stale claim not on
#    the FORBIDDEN list (measures forbidden coverage, named as earned-not-exhaustive).
d = fresh("rewritten-claim")
lines = read(d)
expect("selectors stay bare hashes" in lines[92], "rewrite anchor")
lines[92] = "  carrier (arc3-r4); selectors are name-resolved from a live signature DB."
write(d, lines)
expect(len(read(d)) == 162, "rewrite line-count neutral")
report["rewritten-claim"] = {"edit": "PROVINCE.md:93 stale claim rewritten, no FORBIDDEN literal used", "lines": 162}

for k in sorted(report):
    print("%-18s %s" % (k, report[k]))
