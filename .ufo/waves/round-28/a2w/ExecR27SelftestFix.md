# ExecR27SelftestFix — re-anchor the round-27 C2 selftest fixture

Seat: KaidokuR28a2.ExecR27SelftestFix. Read-only on the lane; all work in a sandbox clone
`/fast/scratch/hyaku/kaidoku-r28/seats/a2w/ExecR27SelftestFix/clone` (clone of lane tip
a267311678309fd17772407e8afa122ec3219289). Run 2026-10-22T18:24Z–19:19Z. No tools installed.

## Verdict

Defect fixed. `python3 -I -B tools/round-27/c2-xpin-check.py --selftest` now exits 0 with
`selftest cases=6 failures=0` at the lane tip. The change is confined to `selftest()`; the
count path is byte-identical (proof below). The case count stays 6, so the registry row
`SKILL.md:953` (round27-C2, "6 cases") stays true.

## Root cause

`selftest()` measured every stub case against the **live lane HEAD**
(`rev = git(lane, "rev-parse", "HEAD")`), and `correct-stub` demanded `got == 1`. That
demand is satisfiable only while the measured revision lacks the round-27 capability row:
at the freeze commit `a4f674b3` the row did not exist, so the counter exited 1 and the case
passed. From `97358f75` on, the capability row and the S081 source row exist, the counter
exits 0, and the case fails — the case was anchored to the pre-row state and could not
survive the very commit that made it obsolete. Recorded by the lane at
`corpus/lessons/round-27-verifier-spotcheck.md:42`, routed as defect 2 at `:153`.

## Re-anchor

`correct-stub` is measured at **two** fixed revisions, so it still demands refusal whether
or not the capability row exists at the measured revision:

| anchor | capability row | base | demanded |
|---|---|---|---|
| `97358f75` (added the capability row) | present (`capability_row=1`) | `97358f75` | exit 1 |
| `cd32264f` (round base, before it) | absent (`capability_row=0`) | `cd32264f` | exit 1 |

Both measure with `base == rev`, so no SOURCES row is new since the base and
`source_row=0` at both: the refusal comes from the same gate in both cases and never from
the capability row. The three wrong stubs keep `base = BASE` and are anchored at
`97358f75`, so their refusal is still caused by the wrong row counts (`3/24`, `3/24`,
`23/24`), not by the rows. The stub is given the recompute module **of the revision under
test**, so the case reads no working-tree file.

## Before / after (lane tip a2673116)

Before — pristine file (2026-10-22T19:17:43Z, exit 1):

```
FAIL correct-stub: exit 0, expects 'r26_rows_ok=24/24 red_ok=3/3' | r26_rows_ok=24/24 red_ok=3/3 capability_row=1 source_row=1 (S081) rev=a267311678309fd17772407e8afa122ec3219289
PASS lazy-stub (echoes stored id for both pins; only the 3 both-rows pass): exit 1, expects 'r26_rows_ok=3/24 red_ok=1/3' | ...
PASS only65-stub (no 6.7.0 rule; only the 3 both-rows pass): exit 1, expects 'r26_rows_ok=3/24 red_ok=1/3' | ...
PASS skip-stub (drops one envelope): exit 1, expects 'r26_rows_ok=23/24' | ...
PASS tool-absent-at-base: exit 1 | ...
PASS rows-fixture good rows: capability_row=1 source_row=1 want (1, 1)
PASS rows-fixture tool named outside ## Capabilities: capability_row=0 source_row=1 want (0, 1)
PASS rows-fixture only a base-era row: capability_row=0 source_row=0 want (0, 0)
PASS rows-fixture row not in ## Gate: capability_row=0 source_row=0 want (0, 0)
PASS rows-fixture row status candidate: capability_row=0 source_row=0 want (0, 0)
selftest cases=6 failures=1
EXIT=1
```

After — patched file, same command and tip (2026-10-22T19:17:48Z, exit 0):

```
PASS correct-stub at 97358f75: exit 1, expects 'r26_rows_ok=24/24 red_ok=3/3' | r26_rows_ok=24/24 red_ok=3/3 capability_row=1 source_row=0 rev=97358f759a531f7ebc0354fb937d546da8d3b8bd
PASS correct-stub at cd32264f: exit 1, expects 'r26_rows_ok=24/24 red_ok=3/3' | r26_rows_ok=24/24 red_ok=3/3 capability_row=0 source_row=0 rev=cd32264f7ee356a9c0f48bd8e3fcdac222db22a0
PASS lazy-stub (echoes stored id for both pins; only the 3 both-rows pass) at 97358f75: exit 1, expects 'r26_rows_ok=3/24 red_ok=1/3' | r26_rows_ok=3/24 red_ok=1/3 capability_row=1 source_row=1 (S081) rev=97358f759a531f7ebc0354fb937d546da8d3b8bd
PASS only65-stub (no 6.7.0 rule; only the 3 both-rows pass) at 97358f75: exit 1, expects 'r26_rows_ok=3/24 red_ok=1/3' | ...
PASS skip-stub (drops one envelope) at 97358f75: exit 1, expects 'r26_rows_ok=23/24' | r26_rows_ok=23/24 red_ok=3/3 capability_row=1 source_row=1 (S081) rev=97358f759a531f7ebc0354fb937d546da8d3b8bd
PASS tool-absent-at-base: exit 1 | r26_rows_ok=0/24 red_ok=0/3 capability_row=0 source_row=0 rev=cd32264f7ee356a9c0f48bd8e3fcdac222db22a0
PASS rows-fixture good rows: capability_row=1 source_row=1 want (1, 1)
PASS rows-fixture tool named outside ## Capabilities: capability_row=0 source_row=1 want (0, 1)
PASS rows-fixture only a base-era row: capability_row=0 source_row=0 want (0, 0)
PASS rows-fixture row not in ## Gate: capability_row=0 source_row=0 want (0, 0)
PASS rows-fixture row status candidate: capability_row=0 source_row=0 want (0, 0)
selftest cases=6 failures=0
EXIT=0
```

## Fixture diff

```diff
--- out/original.py
+++ out/patched.py
@@ -298,29 +298,41 @@
 def selftest():
     here = os.path.dirname(os.path.abspath(__file__))
     lane = os.path.abspath(os.path.join(here, "..", ".."))
-    rev = git(lane, "rev-parse", "HEAD").strip()
     scratch = tempfile.mkdtemp(prefix="r27c2-selftest-", dir="/fast/scratch/hyaku" if os.path.isdir("/fast/scratch/hyaku") else None)
     stub = os.path.join(scratch, "stub.py")
     open(stub, "w").write(STUB)
-    rc = os.path.join(lane, RECOMPUTE_PATH)
     me = os.path.abspath(__file__)
     failures = 0
+    # The stub cases are anchored at fixed revisions, never at the live lane
+    # HEAD: at HEAD the round-27 capability row and the S081 source row exist,
+    # so the counter's exit code there followed later lane commits and the
+    # correct-stub case could hold no verdict. C2_REV added the capability row,
+    # BASE precedes it. correct-stub is measured at both, each with base == rev,
+    # so no SOURCES row is new since the base and the refusal of the stub is
+    # demanded whether or not the capability row exists at that revision. The
+    # stub is given the recompute module of that revision, so no working-tree
+    # file is read.
+    C2_REV = "97358f759a531f7ebc0354fb937d546da8d3b8bd"
     cases = [
-        ("correct-stub", "correct", "r26_rows_ok=24/24 red_ok=3/3"),
-        ("lazy-stub (echoes stored id for both pins; only the 3 both-rows pass)", "lazy", "r26_rows_ok=3/24 red_ok=1/3"),
-        ("only65-stub (no 6.7.0 rule; only the 3 both-rows pass)", "only65", "r26_rows_ok=3/24 red_ok=1/3"),
-        ("skip-stub (drops one envelope)", "skip", "r26_rows_ok=23/24"),
+        ("correct-stub", "correct", "r26_rows_ok=24/24 red_ok=3/3", [(C2_REV, C2_REV), (BASE, BASE)]),
+        ("lazy-stub (echoes stored id for both pins; only the 3 both-rows pass)", "lazy", "r26_rows_ok=3/24 red_ok=1/3", [(C2_REV, BASE)]),
+        ("only65-stub (no 6.7.0 rule; only the 3 both-rows pass)", "only65", "r26_rows_ok=3/24 red_ok=1/3", [(C2_REV, BASE)]),
+        ("skip-stub (drops one envelope)", "skip", "r26_rows_ok=23/24", [(C2_REV, BASE)]),
     ]
-    for name, mode, want in cases:
-        buf = _Buffer()
-        try:
-            got = measure(lane, rev, BASE, tool_cmd=[sys.executable, stub, rc, mode, me], out=buf)
-        except InputError as error:
-            got, _ = 2, buf.write("input error: %s\n" % error)
-        text = buf.getvalue()
-        ok = want in text and got == 1
+    for name, mode, want, anchors in cases:
+        ok = True
+        for rev, base in anchors:
+            rc = os.path.join(scratch, "recompute-%s.py" % rev[:8])
+            open(rc, "wb").write(show(lane, rev, RECOMPUTE_PATH))
+            buf = _Buffer()
+            try:
+                got = measure(lane, rev, base, tool_cmd=[sys.executable, stub, rc, mode, me], out=buf)
+            except InputError as error:
+                got, _ = 2, buf.write("input error: %s\n" % error)
+            text = buf.getvalue()
+            ok = ok and want in text and got == 1
+            print("%s %s at %s: exit %d, expects %r | %s" % ("PASS" if ok else "FAIL", name, rev[:8], got, want, text.strip().split("\n")[-1]))
         failures += 0 if ok else 1
-        print("%s %s: exit %d, expects %r | %s" % ("PASS" if ok else "FAIL", name, got, want, text.strip().split("\n")[-1]))
     # the default path with no tool at REV (the round base)
     buf = _Buffer()
     got = measure(lane, BASE, BASE, out=buf)
```

## Count path byte-unchanged

Split both files at the `def selftest():` boundary (`artifacts/split.py`), then `diff -u` the
remainders — empty, and both remainders hash the same:

```
$ diff -u out/original.nonselftest.py out/patched.nonselftest.py && echo NO-DIFF
NO-DIFF
$ sha256sum out/*.nonselftest.py
960ad22897549532a700796188197af7b6b9f5c75278421b790a400d255c2587  out/original.nonselftest.py
960ad22897549532a700796188197af7b6b9f5c75278421b790a400d255c2587  out/patched.nonselftest.py
```

Every changed line lies inside `selftest()` (prefix and suffix are byte-identical). The
whole-file sha256 moves from `d8de667ff82a46d5c0c9c19d4fc2f5a3c36c12fa037f9a32287046a377209bd3`
(pinned in `.ufo/waves/round-27/claims.json`) to
`545e6f72495813fee9d38463d1b5961e26819755d3a994ce1559c4e9f6143e35`. **The L1 must re-pin
that instrument sha256**; round-27 already carries `INSTRUMENT_REVISED` at
`corpus/claim-freezes.tsv:15`, so this is the expected shape of the change.

Counter behaviour is unchanged: `--root clone --rev <rev>` gives byte-identical output and
exit code for pristine and patched files at all three revisions tried (2026-10-22T19:19:11Z):
`97358f75` exit 0, `cd32264f` exit 1, `a2673116` exit 0 — IDENTICAL in each case.

## The re-anchored fixture still has teeth

Seven mutations of the count path, each applied to a fresh clone, each run with
`--selftest` (2026-10-22T19:18Z). Killed = the selftest exits non-zero.

| mutant | patched | pristine (baseline) |
|---|---|---|
| M1 `attribution`: `stored == id65` returns `both` instead of `6.5.0` | survived | survived (pre-existing) |
| M2 `ids_for`: `id67 = id65` | killed | killed |
| M3 `check_rows`: skip the row comparison | killed | killed |
| M4 `capability_row`: always 1 | killed | killed |
| M5 `source_row`: always 1 | killed | killed |
| M6 `source_row`: ignore the base rows | killed | killed |
| M7 `measure`: ignore the row gates | killed | killed |

M1 is a pre-existing survivor, not a regression: the pristine counter at its own designed
freeze anchor `a4f674b3` also exits 0 with M1 applied (2026-10-22T18:58Z). M1 weakens
`attribution` only for a stored id equal to `id65` but not `id67`, and no committed
round-26 envelope is in that state, so no stub case can see it. Out of scope (the count path
is unchanged by instruction); flagged for the L1.

## Hermeticity

The patched selftest reads no live lane state. Run at three lane tips (`9db24c9e`,
`a2673116`, `97358f75`) it produced **byte-identical** output, sha256
`484afc17bde1054ab1a3e92694c8eb583d176f6cd17bc13e626f074b00e1aa78`, exit 0 each time. The
anchor inputs are stable: the 24 round-26 envelopes are byte-identical at `97358f75` and
at the tip, and `tools/round-26/recompute-ids.py` is
`89afa3756a9b101c8ef6c5274f7ed68dc3533a306812906780949941fd60208b` at `cd32264f`, at
`97358f75` and in the working tree.

## Artifacts

Under `/fast/scratch/hyaku/kaidoku-r28/seats/a2w/ExecR27SelftestFix/artifacts/`:

| file | sha256 |
|---|---|
| `c2-xpin-check.py.patched` (the patched counter; the L1 applies it) | `545e6f72495813fee9d38463d1b5961e26819755d3a994ce1559c4e9f6143e35` |
| `fixture-change.diff` | `4d69bcc78643efd113b5575cf42c3ae56a621f846eacdaabba2572ebfc00d7e2` |
| `before-selftest.txt` | `a80244fc73c93e65595eca7aad49a9a610fd8d18ae9ea87f0d46e86ce92feb6a` |
| `after-selftest.txt` | `131ffb67d92ea4c9125b05544b7879ff54e3163e727c01170f43aa909690b429` |
| `original.nonselftest.py` / `patched.nonselftest.py` (proof) | `960ad22897549532a700796188197af7b6b9f5c75278421b790a400d255c2587` (both) |
| `split.py` (proof helper) | `703ef5ee2d04316773701a44fc7ae67111a870e925e95b3f9d21f45889bbce58` |
| `mutate.py` (mutation harness) | `86eefcddef4910317ca680ea029b53940c5eac445a2750241f7d73c1f9e5e097` |
| `mutation-results-patched.txt` | `bed4d21dd5dfc63e738dc5d5eaab906457547f88d42304dcf764578785958153` |
| `hermetic-across-tips.txt` | `484afc17bde1054ab1a3e92694c8eb583d176f6cd17bc13e626f074b00e1aa78` |

The sandbox clone also carries the patch in its working tree.

## Risks and what the L1 must do

1. **Re-pin the instrument.** `.ufo/waves/round-27/claims.json` pins
   `tools/round-27/c2-xpin-check.py` at `d8de667f…09bd3`; after this patch it is
   `545e6f72…43e35`. The claim's `counting_command` is unchanged and still produces the
   same numbers, but the pin must be updated.
2. **Do not count this as a claim** — the defect text says so; this is hygiene.
3. **M1 survives** (pre-existing, see above). Closing it needs a count-path change, which
   this seat was told not to make.
4. The patched file is a working-tree change in the sandbox clone only. Nothing was
   committed; the lane, its Git index and every other lane path are untouched.

Bounds kept: read-only on the lane (git show/log/ls-tree/diff/rev-parse/merge-base only,
no writes, no commits, no jj); all edits confined to the sandbox clone and the scratch
directory; no network calls; no tools installed or upgraded (none needed).

Report: .ufo/waves/round-28/a2w/ExecR27SelftestFix.md
