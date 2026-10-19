# C1 adjudication — the `ptr_check` blind spot (arc3-loop1-round7)

The claim asked to extend the census instrument so a `path:line` pointer in a
clause that also carries a pin/version is evaluated — closing the R2 residual
(`classify()` collects pointer loci only `if not occ`, `c1-census-v10.py:511-514`).

## What the wave established (measured, not asserted)

- **The blind spot is real and confirmed** by every c1 seat (PL-1, PL-2,
  EX-1, EX-2, RV-1, RV-2) and every verdict seat: the baseline gate reads PASS
  while never evaluating the `:18` pointer — `ptr_check` is unreachable on a
  pin-carrying clause. `python3 .ufo/gates/c1-census-v10.py --json` → PASS,
  G21 14 rows, zero pointer assertions in PROVINCE block 15-26.
- **Candidate patches exist and catch the seeded fault.** EX-1's
  digest-checked receipt candidate and RV-2's anchor variant each read PASS
  on a clean scratch tree and FAIL `UNRESOLVED`/`STALE` on a re-keyed dead
  pointer (`:999999`), with G21 and the 19-key JSON contract intact. The
  *mechanism* the claim asks for is demonstrably buildable.

## The landing blocker (the discrepancy the verdicts caught)

- **The frozen claim named the wrong pointer.** It assumed `PROVINCE.md:18`
  carries `~/.kimi-code/config.toml:3298` — but the live text carries
  `:3546` (the 2026-10-19 re-read); `:3298` is only a *historical receipt
  suffix*, not a full `PTR`-regex matchable locus.
- **The live pointer is genuinely stale.** Direct `ptr_check` calls return
  `('stale', …)` for *both* `:3298` (holds `max_context_size`) and `:3546`
  (the config is now ~4,150 lines; the pin is no longer there). There is no
  "clean PASS" tree: any patch that honestly evaluates the pointer FAILS on
  the live `PROVINCE.md:18`, and any patch that passes must anchor a receipt
  that does not bind the live line's content (the custody receipt stores a
  whole-config sha, not the target line).
- **The receipt anchor is weaker than the claim assumed.** The cited custody
  receipt (`arc3-loop1-round1/claims/cross/receipts/config-pre-pair.txt`)
  records `sha256-capture-only; no file contents read` — a whole-file digest,
  not the target line's content. It cannot adjudicate `:3546` as
  current-by-design.

## Ruling: adjudicated PARTIAL — mechanism proven, landing withheld

The claim's *falsifiable* half is met (blind spot confirmed + a working
candidate that catches seeded faults on scratch). The claim's *acceptance*
half — "still reads PASS on the current tree" — is **unsatisfiable as
written**, because the current tree's pointer is stale and the claim predates
that discovery. Landing either (a) a patch that fakes a receipt anchor the
receipt doesn't carry, or (b) a patch that fails the live tree, would both be
dishonest. The honest move is to withhold the gate edit and record the
discrepancy: **the pointer itself needs a re-anchored receipt first** (a
calibration action — re-receipt the live pin line, then the instrument can
grade it), and the instrument extension can land once the anchor is real.

This is recorded as a **partial**, not a failure and not an improvement — the
mechanism is proven but the landing is genuinely blocked by a receipt that
predates the pointer's own drift. Carried as named debt for the next round.

## Residual for the operator

The `~/.kimi-code/config.toml` pin line has drifted twice this arc
(:2940 → :3227 → :3298 → :3546). The perishable `path:line` citation class is
the root cause; a receipt-stamped pointer survives each drift only as a
receipt, not as a live line. The clean fix is a re-receipt of the *current*
pin line in the same commit that extends the instrument.
