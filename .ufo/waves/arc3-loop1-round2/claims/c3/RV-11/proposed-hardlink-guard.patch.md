# proposed-hardlink-guard.patch.md — RV-11 review finding F2, NOT applied

Status: proposal only. RV-11 is a reviewer seat and did not write the target; the
guard below is a suggested hardening for `.ufo/gates/custody-pair/custody-pair.py`
(revision `112d01dc…`, 889 lines) if CR-4/the parent wants F2 closed this round.

## Finding (measured, scratch-only)

The write guard refuses `--out` only when the *resolved path* equals one of the 5
custody paths (`custody-pair.py:562-566`). A hardlink to a custody path resolves
to a different path name, so `capture --out <alias>` writes the receipt through
the shared inode — the exact "never touch custody-path bytes" invariant.
Reproducer + transcript: `claims/c3/RV-11/hardlink-guard/run.out`
(`guarded.conf` sha256 `8af5b1d5…` → `67e161eb…`; bytes replaced by the receipt,
exit 0, no refusal). Requires a pre-existing hardlink; the default flow never
creates one — low likelihood, direct invariant hit.

## Suggested change (sketch, for the implementer to adapt)

In `cmd_capture`, replace the guard at `:564-566` with a path-or-inode check:

```python
        out = Path(args.out).expanduser()
        warn_if_tmp(out)
        def _same_file(a: Path, b: Path) -> bool:
            try:
                sa, sb = os.stat(a), os.stat(b)     # os.stat: follow symlinks (write lands on the target inode)
            except OSError:
                return False
            return (sa.st_dev, sa.st_ino) == (sb.st_dev, sb.st_ino)
        if out.resolve() in {Path(p).expanduser().resolve() for p in CUSTODY_PATHS} \
           or any(_same_file(out, Path(p).expanduser()) for p in CUSTODY_PATHS):
            print("USAGE: refusing to write a receipt over a custody path (path or inode): %s" % out,
                  file=sys.stderr)
            return EXIT_USAGE
```

Notes for the implementer:
- `os.stat` (not lstat) on `out` is right here: if `out` is a symlink, the write
  lands on the target's inode, and `out.exists()` semantics matter — keep the
  path-based `resolve()` arm too, since a *dangling* symlink aimed at a custody
  path must also be refused (stat fails; resolve() still matches).
- Residual TOCTOU is inherent and out of scope; this closes the static case.

## Suggested selftest case (fixture only, scratch)

```python
    # 13b. write guard must also refuse a hardlink alias of a custody-path-like file
    def case_guard_hardlink():
        a = root / "guard-hardlink-a.conf"
        a.write_bytes(b"guard hardlink fixture\n")
        b = root / "guard-hardlink-alias.txt"
        os.link(a, b)
        before = capture_path(a)
        rc = cmd_capture(argparse.Namespace(out=str(b), paths=[str(a)], label="guard2"))
        after = capture_path(a)
        assert rc == EXIT_USAGE, "expected USAGE for hardlink alias, got %d" % rc
        assert before == after, "hardlinked alias was written through the guard"
    run_case(cases, "refuses-to-write-through-hardlink", case_guard_hardlink)
```

(The long-line target `b` is fine: the case must pass with the *actual* custody
paths untouched; `a` is a scratch fixture sharing only an inode with `b`.)
