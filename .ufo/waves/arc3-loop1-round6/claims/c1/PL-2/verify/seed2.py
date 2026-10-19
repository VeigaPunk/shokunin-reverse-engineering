import sys
S = "/var/tmp/pl2-arc3r6-verify"
def lines(tree):
    p = f"{S}/{tree}/PROVINCE.md"
    L = open(p, encoding="utf-8").read().splitlines()
    assert len(L) == 162, (tree, len(L))
    assert L[90].startswith("- **EVM bytecode (extended)**"), L[90]
    assert "solc-0.8.37" in L[91] and "vyper-0.4.3" in L[91]
    return p, L
def write(p, L):
    open(p, "w", encoding="utf-8").write("\n".join(L) + "\n")

p, L = lines("seed-forbidden")
L[90] = "- **EVM bytecode (extended)** — selectors held on synthetic dispatcher"
L[91] = "  (Core, r3-07); real solc/vyper-compiled bytecode untested, synthetic"
L[92] = "  dispatcher only."
write(p, L)

p, L = lines("seed-forbidden-only")
L[91] = "  (Core, r3-07), real solc-0.8.37/vyper-0.4.3-compiled bytecode untested"
L[92] = "  (synthetic dispatcher only); selectors stay bare hashes."
write(p, L)

p, L = lines("seed-required-evm")
L[90:93] = ["- **EVM bytecode (extended)** — see corpus.",
            "  (earning citations removed)", "  (earning citations removed)"]
write(p, L)

p, L = lines("seed-required-riscv")
assert "r5-01" in L[136], L[136]
L[136] = "  (riscv-bypass corpus entry); full 29 MB EXEC"
write(p, L)

p, L = lines("trunc-161")
write(p, L[:161])
print("seeded 5 trees OK")
