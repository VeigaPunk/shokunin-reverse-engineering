"""Seed the fault arms. Every edit asserts the original line content first."""
import shutil

CLEAN = "/var/tmp/pl4-arc3r6/clean/PROVINCE.md"
orig = open(CLEAN, encoding="utf-8").read().splitlines()
assert orig[90].startswith("- **EVM bytecode (extended)**"), orig[90]
assert "solc-0.8.37" in orig[91] and "vyper-0.4.3" in orig[91], orig[91]
assert orig[92].startswith("  carrier (arc3-r4)"), orig[92]


def plant(tree, lines91_92_93=None, line137=None, truncate=None):
    for f in ("PROVINCE.md", "SKILL.md", "SCORECARD.md"):
        shutil.copy("/var/tmp/pl4-arc3r6/clean/" + f, "/var/tmp/pl4-arc3r6/%s/%s" % (tree, f))
    dst = "/var/tmp/pl4-arc3r6/%s/PROVINCE.md" % tree
    lines = open(dst, encoding="utf-8").read().splitlines()
    if lines91_92_93:
        assert lines[90].startswith("- **EVM bytecode")
        lines[90], lines[91], lines[92] = lines91_92_93
    if line137:
        assert "r5-01" in lines[136], lines[136]
        lines[136] = line137
    if truncate:
        lines = lines[:truncate]
    open(dst, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(tree, "->", len(lines), "lines")


plant("seeded-forbidden",
      ["- **EVM bytecode (extended)** — selectors held on synthetic dispatcher",
       "  (Core, r3-07); real solc/vyper-compiled bytecode untested, synthetic",
       "  dispatcher only."])
plant("seeded-forbidden-only",
      ["- **EVM bytecode (extended)** — selectors held on synthetic dispatcher",
       "  (Core, r3-07), real solc-0.8.37/vyper-0.4.3-compiled bytecode untested",
       "  (synthetic dispatcher only); selectors stay bare hashes."])
plant("seeded-required-evm",
      ["- **EVM bytecode (extended)** — see corpus.",
       "  (earning citations removed)",
       "  (earning citations removed)"])
plant("seeded-required-riscv",
      line137="  (riscv-bypass corpus entry); full 29 MB EXEC")
plant("clean-truncated", truncate=161)
