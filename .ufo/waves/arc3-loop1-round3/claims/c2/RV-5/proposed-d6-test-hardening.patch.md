# RV-5 late-join — proposed test-hardening patch (patch TEXT only; seat writes no tool byte)

Seat RV-5 · chain c2 · reviewer · wave `arc3-loop1-round3` · 2026-10-19.
Base revision (the landed tool): `.ufo/gates/custody-pair/custody-pair.py`
sha256 `7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09`
(1155 lines, 54,279 B, mtime `2026-10-19 10:13:20 −03:00`). Every identity in
this file was re-derived by this seat at write time.

`.ufo/gates/custody-pair/` is EX-21's real target (round-3 implementer); this
seat is read-only there and proposes text only, per the wave's seat discipline.

## Defect this closes (a test-coverage hole, not a behaviour hole)

The landed D6 closure is **two-layered**: an explicit guard
(`custody-pair.py:726-728`) and the pre-existing `except OSError` around
`tempfile.mkdtemp` (`:730-733`). The landed selftest case
`selftest-missing-scratch-usage-exit` (`:1055-1074`) asserts only
`returncode == EXIT_USAGE` and `"Traceback" not in stderr`. Therefore the case
**cannot distinguish which layer closed the hole**, and reverting the explicit
guard alone leaves the case PASSing.

Measured by this seat (independent mutation matrix, 8 mutants;
`claims/c2/RV-5/late-join/mutation-matrix.log`, tool sha256 above):

| mutant | selftest |
|---|---|
| `M3-scratch-isdir-line-only` — revert `if not base.is_dir():` → `if False:` | **CLEAN 22/22 exit 0** (case stays PASS; declared class still 2 via the mkdtemp `except OSError`) |
| `M3b-scratch-both-layers` — revert the guard **and** the `except OSError` | DIRTY exit 3, fails exactly `selftest-missing-scratch-usage-exit` |

So the *behaviour* (D6 → USAGE 2, no traceback) is closed by two independent
layers and survives either single revert; but the *case* is load-bearing only
against the both-layers revert. This is a coverage hole in the test, and the
same one RV-5's earlier sabotage run recorded (`sabotage-7cd19c3c/sabotage.log`,
`S3-scratch-guard-reverted CLEAN`).

Contrast — every other closure is load-bearing against its single-line revert
(same matrix): `M1` (verify-side UNEVALUABLE guard) → 3 cases fail; `M1b`
(parser error keys) → 1 case fails; `M2` (guard scope, both arms) → 2 cases;
`M2b` (inode arm only) → 1 case; `M4` (`--require-paths` gate) → 1 case.

## The patch (drop-in; replaces the body of `case_missing_scratch`, `:1055-1074`)

```diff
--- a/.ufo/gates/custody-pair/custody-pair.py
+++ b/.ufo/gates/custody-pair/custody-pair.py
@@ -1054,9 +1054,9 @@
     #     child cannot recurse into this case; the in-process arm asserts the class too.
     def case_missing_scratch():
         tool = str(Path(__file__).resolve())
-        for label, scratch in (("missing", root / "does-not-exist"),
-                               ("file", root / "scratch-is-a-file"),
-                               ("tmp", "/tmp/ex21-selftest-must-not-run")):
+        for label, scratch, expect in (("missing", root / "does-not-exist", "scratch base is not a directory"),
+                                       ("file", root / "scratch-is-a-file", "scratch base is not a directory"),
+                                       ("tmp", "/tmp/ex21-selftest-must-not-run", "/tmp is excluded scratch")):
             if label == "file":
                 Path(scratch).write_text("x", encoding="utf-8")
             p = subprocess.run([sys.executable, tool, "selftest", "--scratch", str(scratch)],
@@ -1064,8 +1064,14 @@
             assert p.returncode == EXIT_USAGE, "expected USAGE exit %d for %s scratch, got %d" % (
                 EXIT_USAGE, label, p.returncode)
             assert "Traceback" not in p.stderr, "raw traceback for %s scratch: %s" % (label, p.stderr)
-        rc = cmd_selftest(argparse.Namespace(scratch=str(root / "does-not-exist")))
+            assert expect in p.stderr, "declared USAGE message missing for %s scratch (which layer closed it?): %s" % (label, p.stderr)
+        import io, contextlib
+        err = io.StringIO()
+        with contextlib.redirect_stderr(err):
+            rc = cmd_selftest(argparse.Namespace(scratch=str(root / "does-not-exist")))
         assert rc == EXIT_USAGE, "expected USAGE exit %d in-process for a missing base, got %d" % (EXIT_USAGE, rc)
+        assert "scratch base is not a directory" in err.getvalue(), (
+            "in-process missing base did not hit the is_dir guard: %s" % err.getvalue())
     run_case(cases, "selftest-missing-scratch-usage-exit", case_missing_scratch)
```

Two assertions are added, both class-line assertions on messages the tool
already emits: (1) each subprocess arm must print its **declared** message
(`scratch base is not a directory` for missing/file, `/tmp is excluded scratch`
for the `/tmp` arm) — under the single-line revert the missing/file arms still
exit 2 but via the mkdtemp layer, whose message differs; (2) the in-process arm
must hit the explicit guard, captured by redirecting `stderr` (the existing
in-process arm discards stderr, which is why it could not see the layer).

No case count change: still 22 cases. No production-code change.

## Proof (measured before writing this text; scratch copies under `/var/tmp/rv5-late/harden/`)

| copy | sha256 | selftest |
|---|---|---|
| landed tool (base) | `7cd19c3c…` | CLEAN 22/22 exit 0 |
| `patched-clean.py` — base + this diff | `d47e4fd5964dc2d16938f45425503411f9c5a4fcccba926f608d2e4f7e4a0f95` | **CLEAN 22/22 exit 0** |
| `patched+M3.py` — patched **and** `if not base.is_dir():` → `if False:` | `c47be2cf858e0986f16a78974640412cb25e51d1589ce70f3cf8f9f20f6a5005` | **DIRTY exit 3, fails exactly `selftest-missing-scratch-usage-exit`** |

The third row is the point: with this test, the explicit D6 guard becomes
load-bearing under a single-line revert — the same standard every other landed
closure already meets.

## Related, not fixed here (out of this patch's scope)

- The explicit guard is a **literal-prefix** check on `str(base)` (`:722-725`)
  and `base.is_dir()` is called before symlink resolution, so `selftest
  --scratch <symlink-to-/tmp>` runs its fixtures **under `/tmp`**. Measured
  first-hand: `mkdir /var/tmp/.../scratch5 && ln -s /tmp .../tmp-link`, then
  `selftest --scratch .../tmp-link` → exit 0, `scratch: .../tmp-link/custody-pair-selftest-5rwrnovd`,
  and `/tmp/custody-pair-selftest-5rwrnovd` created on disk (removed by this
  seat after measuring). This contradicts README.md's "`selftest --scratch`
  requires an existing, non-`/tmp` directory". `/tmp` on this host is
  quota-exhausted (EDQUOT) — the standing hazard the guard exists for. Closing
  it needs a resolved-path check in the tool (production code), which is the
  implementer's call, not a test change; recorded for the parent.
- Sidecar write path unguarded (`--paths X.sha256 --out X` clobbers `X.sha256`):
  measured first-hand by this seat, and proposed by CR-4 §1. Cross-referenced,
  not re-proposed.
- D3 gate counts **stanzas**, not distinct covered paths: a 5-stanza
  single-path reference passes `--require-paths 5` at exit 0 while printing all
  five canonical paths as unaccounted. Measured first-hand, and proposed by
  RV-7 §2. Cross-referenced, not re-proposed.

Rule-#14 note: the base identity, both patched-copy identities, the landed
tool's identity and the mutation results were all re-derived in the same run
that produced this text (`claims/c2/RV-5/late-join/mutation-matrix.log`,
`claims/c2/RV-5/late-join/precision.log`).
