# proposed patch text — scratch-guard residuals (seat EX-26, chain c2)

Target: `.ufo/gates/custody-pair/custody-pair.py` (+ its selftest), revision under
test **`7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09`**
(1155 lines, 54279 B, 2026-10-19 10:13:20 -03). EX-21 owns the write; this seat
proposes text only and has applied nothing to the real target.

Evidence for every claim below is in `EX-26/evidence/` and the measured
before→after table is `EX-26/scratchguard-after.md`.

## P1 — fence the `mkdtemp` `OSError` arm (behavior verified; only the case is missing)

The landed `cmd_selftest` closes three exit-1 paths: the `/tmp` prefix check
(`:723`), a non-directory base (`:726`), and an `OSError` out of `mkdtemp`
(`:729-733`). The tool's own selftest case `selftest-missing-scratch-usage-exit`
fences only the second: with the `try/except` deleted from a scratch copy
(`mutAB`) the selftest still reports `CLEAN cases=22 passed=22 failed=0 exit=0`,
so the third arm can regress silently (`evidence/mutation-fence-7cd19c3c.out`).
The case below is proven in both directions on scratch: it FAILs without the
`try/except` (`fixAC`, `DIRTY 16/17`) and PASSes with it (`fixAB`, `CLEAN 17/17`),
and it FAILs on the unguarded base (`baseC`, `DIRTY 15/17`).

```diff
     run_case(cases, "selftest-missing-scratch-usage-exit", case_missing_scratch)
+
+    # a base that exists but cannot host a fixture root is USAGE too (the
+    # mkdtemp OSError arm; mode-0500 and /proc are the measured shapes)
+    def case_unusable_scratch():
+        import stat
+        bad = root / "unusable-scratch"
+        bad.mkdir()
+        bad.chmod(stat.S_IRUSR | stat.S_IXUSR)      # 0o500: exists, not writable
+        try:
+            proc = subprocess.run(
+                [sys.executable, str(Path(__file__).resolve()), "selftest",
+                 "--scratch", str(bad)], capture_output=True, text=True)
+            assert "Traceback" not in proc.stderr, "--scratch <mode 0500 dir> tracebacked"
+            assert proc.returncode == EXIT_USAGE, (
+                "--scratch <mode 0500 dir> exit %d (want USAGE %d)"
+                % (proc.returncode, EXIT_USAGE))
+            assert proc.stderr.lstrip().startswith("USAGE:"), (
+                "stderr not a USAGE line: %r" % proc.stderr[:80])
+        finally:
+            bad.chmod(0o700)
+    run_case(cases, "selftest-unusable-scratch-usage-exit", case_unusable_scratch)
```

Notes: the chmod-back in `finally` keeps the fixture root removable; the case uses
the module's own process (`__file__`) so it exercises the CLI surface, not an
in-process call; nothing here touches a custody path.

## P2 — `default_scratch()` failure arm must exit in the declared map (R1)

Measured at `7cd19c3c` (`evidence/residual-probes-real-7cd19c3c.out`): with
`os.access` stubbed false (the arm is unreachable on this host — `/dev/shm` is
writable), the process exits **1** while printing
`USAGE: no writable scratch dir (/dev/shm, /var/tmp); /tmp is excluded (EDQUOT hazard)`.
`SystemExit(<str>)` sets status 1; the declared map says `USAGE` = 2.

```diff
 def default_scratch() -> Path:
     for cand in (os.environ.get("CUSTODY_PAIR_SCRATCH"), "/dev/shm", "/var/tmp"):
         if not cand:
             continue
         p = Path(cand)
         if p.is_dir() and os.access(p, os.W_OK):
             return p
-    raise SystemExit("USAGE: no writable scratch dir (/dev/shm, /var/tmp); /tmp is excluded (EDQUOT hazard)")
+    print("USAGE: no writable scratch dir (/dev/shm, /var/tmp); /tmp is excluded "
+          "(EDQUOT hazard)", file=sys.stderr)
+    raise SystemExit(EXIT_USAGE)
```

`EXIT_USAGE` is defined above this function, so the reference resolves. A
`SystemExit(2)` propagates cleanly through `main()`'s caller
(`sys.exit(main())`), unchanged in shape. If the parent prefers no `raise` at all,
the equivalent is for `cmd_selftest` to catch the failure and `return EXIT_USAGE`
— larger diff, same declared class.

## P3 — normalize the `/tmp` exclusion (R2, optional, low severity)

At `:723` the predicate is a string test, so `--scratch //tmp/x` (which
`os.path.realpath` resolves to `/tmp/x`) is accepted, while `/tmp/x` is refused.
Predicate evaluated, no `/tmp` write performed (host rule):
`evidence/residual-probes-real-7cd19c3c.out`.

```diff
     base = Path(args.scratch).expanduser() if args.scratch else default_scratch()
-    base_s = str(base)
+    base_s = os.path.realpath(str(base))
     if base_s == "/tmp" or base_s.startswith("/tmp/"):
```

This also catches a symlink placed in a writable directory that points into
`/tmp`. It does not change the happy path (`realpath` of an existing base is that
base). If the parent prefers to hold the guard as a *string* policy statement
rather than a normalized one, P3 can be dropped with no effect on P1/P2.

## What this seat did NOT propose

- No change to the landed guard's semantics (`:723`, `:726`, `:729-733` are
  correct as measured — 11/11 bad inputs → USAGE 2, 4/4 good inputs → CLEAN 22/22).
- No README change: the README at re-derived `f30df42e…` (10:15:12) is consistent
  with the tool (14-row present, 22 cases named, scratch line at `:49-50`). The
  earlier `cases=15` / missing-14-row states were mid-edit churn, timestamped in
  `scratchguard-after.md` §1 and §6.