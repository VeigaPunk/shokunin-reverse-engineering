# proposed-scratch-mkdir.patch.md — RV-12 (reviewer, chain c3)

Target (EX-31's file, chain c3, designated implementer — this is patch TEXT only;
RV-12 wrote no byte of the real target):

    .ufo/gates/custody-pair/custody-pair.py

Measured at revision
`112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa`
(2026-10-19T12:13Z, sha256 re-derived).

## Defect

`selftest --scratch <dir>` whose `<dir>` does not exist crashes with an
uncaught traceback and exit **1** — not the declared `USAGE` class (exit 2):

```
$ python3 .ufo/gates/custody-pair/custody-pair.py selftest --scratch /var/tmp/rv12/does-not-exist
  File ".../custody-pair.py", line 630, in cmd_selftest
    root = Path(tempfile.mkdtemp(prefix="custody-pair-selftest-", dir=str(base)))
  File "/usr/lib/python3.14/tempfile.py", line 381, in mkdtemp
    _os.mkdir(file, 0o700)
FileNotFoundError: [Errno 2] No such file or directory: '/var/tmp/rv12/does-not-exist/custody-pair-selftest-8sxn90ku'
exit=1
```

Reproduced twice (12:05Z at rev `b10ad1c8…`, 12:13Z at rev `112d01dc…`) — this is
not revision churn. Exit 1 is outside the tool's declared exit map
(`README.md` "Exit codes": 0/10/11/12/13/2/3), so a CI harness keying on the
declared classes reads a crash as an undeclared failure class. The README usage
line (`README.md:32`) documents `selftest [--scratch /dev/shm]` without stating
that the directory must pre-exist; the default path (`/dev/shm`, `/var/tmp`) is
validated by `default_scratch()`, but an explicit `--scratch` is not.

## Patch text

In `cmd_selftest` (currently `custody-pair.py:623-630`), insert a validation
step between the `/tmp` guard and `mkdtemp`:

```python
     base = Path(args.scratch).expanduser() if args.scratch else default_scratch()
     if str(base).startswith("/tmp") and not args.scratch:
         print("USAGE: /tmp is excluded scratch (EDQUOT hazard)", file=sys.stderr)
         return EXIT_USAGE
+    if not base.is_dir():
+        try:
+            base.mkdir(parents=True, exist_ok=True)
+        except OSError as exc:
+            print("USAGE: scratch root not usable: %s (%s)" % (base, exc), file=sys.stderr)
+            return EXIT_USAGE
     root = Path(tempfile.mkdtemp(prefix="custody-pair-selftest-", dir=str(base)))
```

Either half is sufficient; creating the dir is friendlier, and the
`EXIT_USAGE` fallback keeps the declared exit map total for an unwritable root.

## Verification each half needs (unrun by RV-12)

- `selftest --scratch /var/tmp/rv12/does-not-exist` → creates the dir, runs 15/15
  CLEAN, exit 0.
- `selftest --scratch /proc/nope` → `USAGE:` line, exit 2, no traceback.
- `selftest --scratch /var/tmp/rv12/self2` (existing) → unchanged CLEAN 15/15 exit 0.
- `selftest` with no `--scratch` → unchanged (default `/dev/shm`).
