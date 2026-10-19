# PATCH PROPOSAL (not applied) — EX-07 `reconcile.py`: spurious MISMATCH without `--abi`

- Target: `.ufo/waves/arc3-loop1-round1/claims/c1/EX-07/reconcile.py`
- Target revision at finding: sha256 `647395a0f8a2d00e73f02c242186a3b17f0396713b3a00d2caf0fca82e87b9a6`
- Found by: SEAT RV-2 (reviewer), 2026-10-19, while re-running EX-07's
  reconciliation driver as the seat-line comparison step.
- Status: PROPOSED only — no repo file was modified by RV-2.

## Defect D1

`reconcile.py` builds the `M2_keccak_scan` source row from the ABI signatures.
When `--abi` is omitted, `m2 = {}` (line 81) and the row is still emitted as an
empty set (line 96), then compared against the `M1_chain` reference. A clean
carrier therefore reports a false mismatch and exit 1.

Repro (current revision, clean carrier — no tampering anywhere):

```
$ python3 claims/c1/EX-07/reconcile.py --code claims/c1/RV-2/Rv2Token.runtime.hex hex \
    --planted claims/c1/RV-2/expected-selectors.txt \
    --probe claims/c1/RV-2/probe-runtime-hex-6.4.0.json
...
M2_keccak_scan               n= 0  MISMATCH  missing=['095ea7b3', '18160ddd', '23b872dd', '70a08231', 'a9059cbb'] extra=[]
VERDICT: MISMATCH PRESENT
EXIT=1

$ python3 ... (same, plus --abi claims/c1/RV-2/Rv2Token.abi.json)
VERDICT: ALL SOURCES AGREE
EXIT=0
```

Impact: low for the recorded round (EX-07's canonical runs passed `--abi`, so
`reconciliation-run.txt` / `reconciliation.md` verdicts are unaffected), but a
parent or later seat re-running the driver without `--abi` — a natural reading
of the usage string, since `--abi` is optional — gets a false failure on a
clean tree, which is the exact class of misleading signal reviewers exist to
remove.

## Proposed diff

```diff
--- a/.ufo/waves/arc3-loop1-round1/claims/c1/EX-07/reconcile.py
+++ b/.ufo/waves/arc3-loop1-round1/claims/c1/EX-07/reconcile.py
@@
-    # M2 keccak scan over ABI signatures: verify each selector's bytes are present
-    m2_found = {}
-    for sig, sel in m2.items():
-        m2_found[sel] = code.hex().find(sel)
-    sources["M2_keccak_scan"] = norm([s for s, off in m2_found.items() if off >= 0])
+    # M2 keccak scan over ABI signatures: verify each selector's bytes are present.
+    # Emit the row only when an ABI was supplied; an empty M2 row would be
+    # compared against the M1 reference and force a spurious MISMATCH/exit 1.
+    if args.abi:
+        m2_found = {}
+        for sig, sel in m2.items():
+            m2_found[sel] = code.hex().find(sel)
+        sources["M2_keccak_scan"] = norm([s for s, off in m2_found.items() if off >= 0])
+    else:
+        print("M2_keccak_scan: skipped (no --abi supplied)")
```

Alternative (equivalent): keep the row but exclude it from the verdict when
`args.abi` is None.

## Verification the patch author should run

1. No-ABI run above → must exit 0 with `VERDICT: ALL SOURCES AGREE` (or an
   explicit skip line, depending on variant).
2. With `--abi` → unchanged `ALL SOURCES AGREE` (no regression).
3. Tamper controls must still fail: dropped-selector probe → `MISMATCH`,
   exit 1; bogus planted entry → `MISMATCH`, exit 1. (Both reproduced by
   RV-2 against the unpatched revision: `claims/c1/RV-2/attack/tampered-drop-one.json`,
   `claims/c1/RV-2/attack/planted-plus-bogus.txt`.)
