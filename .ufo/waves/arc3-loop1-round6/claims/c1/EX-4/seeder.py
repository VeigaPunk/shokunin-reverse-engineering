import os, shutil
REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
BASE = "/var/tmp/ex4-arc3r6/trees"
FILES = ["PROVINCE.md", "SKILL.md", "SCORECARD.md"]
os.makedirs(BASE, exist_ok=True)

def mk(name, mutate=False):
    d = os.path.join(BASE, name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    for f in FILES:
        shutil.copyfile(os.path.join(REPO, f), os.path.join(d, f))
    if mutate:
        p = os.path.join(d, "PROVINCE.md")
        lines = open(p, encoding="utf-8").read().splitlines()
        mutate(lines)
        open(p, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    return d

def clean(l): pass

def forbid_91(l):
    assert "carrier (arc3-r4)" in l[92], l[92]
    l[92] = ("carrier (arc3-r4); real solc/vyper-compiled bytecode untested, "
             "synthetic dispatcher only.")
    assert "untested" in l[92] and "solc-0.8.37" in "\n".join(l[90:93]) \
        and "vyper-0.4.3" in "\n".join(l[90:93])

def req_evm(l):
    assert "EVM bytecode" in l[90]
    l[90] = "- **EVM bytecode (extended)** — see corpus."
    l[91] = "No carrier detail is recorded here yet."
    l[92] = "Earning citations intentionally absent for this arm."

def req_riscv(l):
    assert "r5-01" in l[136], l[136]
    l[136] = ("(see the RISC-V corpus note); full 29 MB EXEC")

def trunc_161(l):
    del l[161:]

def trunc_131(l):
    del l[131:]

def append_163(l):
    l.append("- **Brand-new stale claim** — real solc/vyper-compiled bytecode untested.")

def forbid_84(l):
    assert "oldest-first" in l[85], l[85]
    l[85] = l[85] + " Real solc/vyper-compiled bytecode untested."

def insert_140(l):
    l.insert(139, "Inserted neutral clarification line (register-shift arm).")

trees = {
  "clean": clean,
  "forbid-91": forbid_91,
  "req-evm": req_evm,
  "req-riscv": req_riscv,
  "trunc-161": trunc_161,
  "trunc-131": trunc_131,
  "append-163": append_163,
  "forbid-84": forbid_84,
  "insert-140": insert_140,
}
for name, fn in trees.items():
    d = mk(name, None if fn is clean else fn)
    print("%-12s %4d lines" % (name, len(open(os.path.join(d,"PROVINCE.md")).read().splitlines())))
