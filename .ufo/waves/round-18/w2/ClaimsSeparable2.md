# ClaimsSeparable2 — re-judge claim separability at REV b2aad08

PARTIAL — C1 is coupled to C3 as built (one undeclared witness check); C2 is separable (proven by counterexample); C3 is separable. The coupling is real but disclosable in one sentence; it is not a reason to reject C1.

All anchors are `git show b2aad08ceeee8dd125ce0d316056d8bd766c7f94:<path>` unless marked working-tree. No tool was installed or updated (none needed). Only this report was written; the two experiments ran in a `mktemp -d` clone whose `origin` remote was removed first; the lane saw read-only git and read-only tool runs only.

## Commands (all run from the lane root; exit codes observed)

```
python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root . --rev b2aad08…   # exit 0, open_count 0 (named 0, substance 0)
python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root . --rev 9011581…   # exit 0, open_count 6
python3 -I -B .ufo/waves/round-18/tools/head-rev-lint.py  --root . --rev b2aad08…   # exit 0, live 0, fixture 15, annotated 6, files 39
python3 -I -B .ufo/waves/round-18/tools/head-rev-lint.py  --root . --rev 9011581…   # exit 0, live 3 (citation-drift-probe.py:477 default-HEAD, custody-pair.py:327 rev-parse-HEAD, round-17/verify.py:59 rev-parse-HEAD), fixture 8
```

Both before/after numbers reproduce claims.json's C1/C2 amendments exactly. [OBSERVATION]

## F1 — C1→C3 coupling is real, one-directional, and undeclared [OBSERVATION + INFERENCE]

- The as-built PINMAP substance set ends with `checks.append(_pinmaps_retained_check(root, rev))` — routed-defects.py:290 — implemented at routed-defects.py:323-373 as check `r18-receipt-pinmaps`: it fails if `.ufo/waves/round-18/runs/` is absent (:326-329), and passes only on a `runs/*/receipt.json` whose `steps.*.pin_checks` each carry `map_path` + `map_sha256` that matches the sha256 of the committed map blob (:365-368; failure :370-373). A defect is open when named OR substance fails (routed-defects.py:187-196, `open: named_open or substance_open` at :192).
- At REV every dir under `.ufo/waves/round-18/runs/` is a C3 label (15 trees: 12 synthetic + calib-aether + calib-notesmd-cli + real-kimi-webbridge, plus run-log.txt) — `git ls-tree b2aad08:.ufo/waves/round-18/runs/`. The receipts are C3 carrier-run receipts; e.g. s1250-swiss-nethttp/receipt.json pin_checks carry `map_path`+`map_sha256` (`8f05d6f9…`, `20a6e5a2…`). [OBSERVATION]
- Counterexample (throwaway clone, b2aad08 tree minus `.ufo/waves/round-18/runs`, committed): `routed-defects.py --root . --rev <expA>` → exit 0, `open_count 1`, R17-PINMAP open, sole broken check `r18-receipt-pinmaps`, detail `.ufo/waves/round-18/runs/ absent at rev`. [OBSERVATION] So C1's 6→0 is not reachable without committed round-18 carrier-run receipts; in this lane their only honest producer is C3's runs. [INFERENCE]
- Second, softer edge: C1's named check (d) requires the literal `map_sha256` in `W17/tools/carrier-run.py` (contract.md:32; routed-defects.py:228-236), but that tool fix is contracted as a C3 in-place additive fix (contract.md:128-130). Both C1 edges therefore sit on C3-side outputs (the fix and its exercised runs).
- Undeclared: claims.json C1 falsifiable (:13) and the C1 amendment (:37) say only "revision-scoped Git-object test … 6 -> 0"; contract.md's amendment C1 (:149) restates the gating but not the receipts dependency. Evaluation remains a pure function of REV; what C1's green state presupposes is artifact provenance from C3's execution. [OBSERVATION on texts; INFERENCE on the gap]
- Not a truth-coupling the other way: C3's falsifiable inputs (frozen predictions, retained logs, compare.json `fields` entries incl. literal `extra.eof_reads` — s1250-swiss-nethttp/compare.json) read nothing from C1's corpus corrections; the baseline lint shows none of the three live HEAD sites is in C3's run path, so C3 does not need C2 either. [OBSERVATION + INFERENCE]

## F2 — C2 is separable (proven) [OBSERVATION]

Counterexample (throwaway clone): baseline 9011581 + only the three routed site files checked out from b2aad08 (citation-drift-probe.py, custody-pair.py, round-17/verify.py), committed:
- `head-rev-lint.py --root . --rev <expB>` → exit 0, live 0 (fixture 10, annotated 4) — C2 green;
- `routed-defects.py --root . --rev <expB>` → exit 0, open_count 6 — C1 fully red, C3 artifacts absent.

C2's green state is reachable with zero C1/C3 artifacts; head-rev-lint reads Git objects at REV only (head-rev-lint.py:608-…, live count :664), jj-red-before builds its own throwaway clone. No reverse edge: no C1/C3 check reads the three C2-fixed files. [OBSERVATION; the "no reverse edge" is INFERENCE from the routed-defects.py source constants at :49-67 and the baseline lint site list]

## F3 — shared instrument, not shared truth [OBSERVATION]

`W18/measure.py REV` aggregates all three counters (contract.md:139-143): verification flows through one tool, so a measure.py defect would hit all three claims at once. That is a verification coupling, not a state dependency between claims; the per-claim counters are independently runnable (commands above).

## Recommended honest wording of independence

- **C1**: "Independent of C2. Dependent on C3 for exactly one substance check: `r18-receipt-pinmaps` (routed-defects.py:290,323-373) requires a committed `.ufo/waves/round-18/runs/*/receipt.json` with hash-verified mid maps, which only C3's carrier runs produce in this lane; the 6→0 transition is evaluable only at a revision that also carries round-18 carrier-run receipts. C1 does not depend on C3's verdict (confirmed/refuted/unresolved)."
- **C2**: "Fully separable: before/after from head-rev-lint over Git objects at REV plus a throwaway-clone red-before receipt; no C1 or C3 artifact is an input (counterexample: three-file fix on baseline → live 0 while routed-defects reports 6)."
- **C3**: "Independent of C1 and C2: falsifiable inputs are the frozen predictions, bound retained logs and compare `extra.*` fields under W18. One-way note: C3's receipts are the sole in-lane witness for C1's `r18-receipt-pinmaps`."

## Smallest safe correction

One sentence in claims.json C1's falsifiable_before_after (or a one-line amendment) declaring the `r18-receipt-pinmaps` dependency on round-18 receipts — no tool change, no re-run. Alternative (heavier, not recommended now): demote `r18-receipt-pinmaps` to a reported non-gating check, restoring the routed defect's original either/or (corpus/lessons/round-17-verifier-spotcheck.md:137, "Either retain mid maps (or their digest) or append a named correction"). The as-built requires both paths; that is stricter than routed and defensible, but then the dependency must be worded.
