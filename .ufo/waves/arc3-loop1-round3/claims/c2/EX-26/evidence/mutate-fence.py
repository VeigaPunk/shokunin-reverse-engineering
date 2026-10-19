#!/usr/bin/env python3
"""EX-26: mutation test of the landed revision's *own* scratch-guard fence case.

Takes the landed revision (kept under its canonical filename so the module's
self-referential TZ case still resolves) and produces two mutants by line
surgery with content asserts:

  mutA  -- guard block + try/except removed (pre-round-3 behaviour)
  mutAB -- is_dir guard kept, mkdtemp try/except removed (the half fix)

Then the mutant's own selftest is run: if the landed fence case
`selftest-unusable-scratch-usage-exit` FAILs on the mutant, the fence is
non-vacuous for that regression.
"""
import pathlib
import subprocess
import sys

SRC = pathlib.Path(sys.argv[1] if len(sys.argv) > 1
                   else "/dev/shm/ex26/snap/03bd6242/custody-pair.py")
lines = SRC.read_text(encoding="utf-8").splitlines(keepends=True)

start = next(i for i, l in enumerate(lines) if l.strip() == "if not base.is_dir():")
block = [l.rstrip("\n") for l in lines[start:start + 8]]
expected = [
    'if not base.is_dir():',
    'print("USAGE: scratch base is not a directory: %s" % base, file=sys.stderr)',
    'return EXIT_USAGE',
    'try:',
    'root = Path(tempfile.mkdtemp(prefix="custody-pair-selftest-", dir=str(base)))',
    'except OSError as exc:',
    'print("USAGE: cannot create a fixture root under %s (%s)" % (base, exc), file=sys.stderr)',
    'return EXIT_USAGE',
]
assert [b.strip() for b in block] == expected, [b.strip() for b in block]
assert lines[start + 8].strip() == "", repr(lines[start + 8])
print("guard block = source lines %d..%d of %s (asserted by content)" % (start + 1, start + 8, SRC))

plain = '    root = Path(tempfile.mkdtemp(prefix="custody-pair-selftest-", dir=str(base)))\n'


def emit(name: str, new_lines: list) -> pathlib.Path:
    d = pathlib.Path("/dev/shm/ex26") / name
    d.mkdir(parents=True, exist_ok=True)
    dst = d / "custody-pair.py"
    dst.write_text("".join(new_lines), encoding="utf-8")
    return dst


mutA = emit("mut-noGuard", lines[:start] + [plain] + lines[start + 8:])
mutAB = emit("mut-noExcept", lines[:start + 3] + [plain] + lines[start + 8:])

for name, tool in (("mutA (guard + try/except removed)", mutA),
                   ("mutAB (is_dir guard only, try/except removed)", mutAB)):
    proc = subprocess.run([sys.executable, str(tool), "selftest", "--scratch",
                           "/dev/shm/ex26/okdir"], capture_output=True, text=True)
    print("\n%s -> exit %d" % (name, proc.returncode))
    for l in proc.stdout.splitlines():
        if "CUSTODY_PAIR_SELFTEST" in l:
            print("  " + l)
    for l in proc.stdout.splitlines():
        if l.startswith("case ") and "FAIL" in l:
            print("  " + l[:120])