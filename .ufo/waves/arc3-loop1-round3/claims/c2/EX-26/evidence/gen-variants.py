#!/usr/bin/env python3
"""EX-26 scratch harness: derive fix variants of custody-pair.py by exact anchor
substitution, asserting every anchor is present exactly once. Writes nothing
outside /dev/shm/ex26/. Scratch only -- the real target is EX-21's.
"""
import hashlib
import pathlib
import sys

BASE = pathlib.Path("/dev/shm/ex26/custody-pair-base.py")
SRC = BASE.read_text(encoding="utf-8")

ANCHOR_BASE = '    base = Path(args.scratch).expanduser() if args.scratch else default_scratch()\n'
GUARD_A = (
    '    if not base.is_dir():\n'
    '        print("USAGE: scratch base is not a directory: %s" % base, file=sys.stderr)\n'
    '        return EXIT_USAGE\n'
)
MKD_OLD = '    root = Path(tempfile.mkdtemp(prefix="custody-pair-selftest-", dir=str(base)))\n'
MKD_NEW = (
    '    try:\n'
    '        root = Path(tempfile.mkdtemp(prefix="custody-pair-selftest-", dir=str(base)))\n'
    '    except OSError as exc:\n'
    '        print("USAGE: scratch base not writable: %s (%s)" % (base, exc), file=sys.stderr)\n'
    '        return EXIT_USAGE\n'
)

# Case block inserted just before the tail summary ("    passed = sum(...)")
TAIL = '    passed = sum(1 for _, ok, _ in cases if ok)\n'
NEW_CASES = '''    # 13. scratch-guard: an explicit --scratch that is not a directory is USAGE (exit 2)
    def case_missing_scratch():
        for bad in (root / "does-not-exist", root / "does-not-exist" / "nested"):
            proc = subprocess.run(
                [sys.executable, str(Path(__file__).resolve()), "selftest", "--scratch", str(bad)],
                capture_output=True, text=True)
            assert "Traceback" not in proc.stderr, "--scratch %s tracebacked" % bad
            assert proc.returncode == EXIT_USAGE, (
                "--scratch %s exit %d (want USAGE %d)" % (bad, proc.returncode, EXIT_USAGE))
            assert proc.stderr.lstrip().startswith("USAGE:"), (
                "--scratch %s stderr not a USAGE line: %r" % (bad, proc.stderr[:80]))
    run_case(cases, "selftest-missing-scratch-usage-exit", case_missing_scratch)

    # 14. scratch-guard: a scratch base that exists but is not writable is USAGE too
    def case_unwritable_scratch():
        import stat
        bad = root / "read-only-scratch"
        bad.mkdir()
        bad.chmod(stat.S_IRUSR | stat.S_IXUSR)  # 0o500: a dir, not writable
        try:
            proc = subprocess.run(
                [sys.executable, str(Path(__file__).resolve()), "selftest", "--scratch", str(bad)],
                capture_output=True, text=True)
            assert "Traceback" not in proc.stderr, "--scratch <mode 0500 dir> tracebacked"
            assert proc.returncode == EXIT_USAGE, (
                "--scratch <mode 0500 dir> exit %d (want USAGE %d)" % (proc.returncode, EXIT_USAGE))
            assert proc.stderr.lstrip().startswith("USAGE:"), (
                "stderr not a USAGE line: %r" % proc.stderr[:80])
        finally:
            bad.chmod(0o700)
    run_case(cases, "selftest-unwritable-scratch-usage-exit", case_unwritable_scratch)

'''


def write_variant(name: str, guard: str, oserror: bool, cases: bool) -> pathlib.Path:
    assert SRC.count(ANCHOR_BASE) == 1, "anchor base: %d hits" % SRC.count(ANCHOR_BASE)
    assert SRC.count(MKD_OLD) == 1, "anchor mkdtemp: %d hits" % SRC.count(MKD_OLD)
    text = SRC.replace(ANCHOR_BASE, ANCHOR_BASE + guard)
    if oserror:
        text = text.replace(MKD_OLD, MKD_NEW)
    if cases:
        assert text.count(TAIL) == 1, "anchor tail: %d hits" % text.count(TAIL)
        text = text.replace(TAIL, NEW_CASES + TAIL)
    outdir = pathlib.Path("/dev/shm/ex26") / name
    outdir.mkdir(parents=True, exist_ok=True)
    # the module's own TZ case resolves a *sibling* named custody-pair.py
    # (custody-pair.py:733), so each variant keeps the canonical filename.
    dst = outdir / "custody-pair.py"
    dst.write_text(text, encoding="utf-8")
    print("%s  sha256=%s  lines=%d" % (dst, hashlib.sha256(text.encode()).hexdigest(),
                                       text.count("\n")))
    return dst


if __name__ == "__main__":
    print("base: %s sha256=%s" % (BASE, hashlib.sha256(SRC.encode()).hexdigest()))
    write_variant("fixA", GUARD_A, oserror=False, cases=False)     # EX-34 Option A literal
    write_variant("fixAB", GUARD_A, oserror=True, cases=True)      # extended + cases
    write_variant("fixB", "", oserror=False, cases=False)          # negative control = base
    # fence-integrity controls: the two new cases against unfixed / half-fixed code
    write_variant("baseC", "", oserror=False, cases=True)          # cases, no guard -> 2 FAILs
    write_variant("fixAC", GUARD_A, oserror=False, cases=True)     # is_dir only -> 1 FAIL
    sys.exit(0)