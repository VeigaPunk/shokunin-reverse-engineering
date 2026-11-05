# Round 94 — claims declaration (frozen before candidate scoring)

Lane `kaidoku`, round 94, attempt 1. Base `8a40ceb6516bb38c19c37bcbff2bb3332f31c832`
(lane tip at round start, `jj-lane.sh state` `ahead=0 behind=0`). Machine-readable twin:
`.ufo/waves/round-94/claims.json`. Before-state receipts are committed in this declaration
under `.ufo/waves/round-94/pre/`, measured at the base with the frozen round-93 counter.

## Owned axes and lowest-axis obligation

All four owned axes (coverage, depth, calibration, freshness) sit at 10.0 on their finite
proxies (SCORECARD `## Owned axes`); saturation 10.0, stagnation window 10. The last
capability entered in round 92, so the stagnation window has not closed and no waiver is
invoked. Calibration and depth are tied-lowest; both claims sit on them. Two claims, distinct
axes, causally separable: C1's measurement reads `tools/` bytes only, C2's measurement reads
`SKILL.md`, `corpus/QUALITY.md` and `corpus/knowledge/` bytes only.

## Routed defects this round carries (round-93 spot-check, lesson `round-93.md` `## Mistakes`)

- M93-e (the frozen v3 receipt writer crashes on the honest case): carried as R94-C1.
- Named limit 2 / successor counter (`corpus/lessons/round-93-verifier-spotcheck.md`, "carried"):
  R94-C1's successor counter is declared here as a new declaration; v3 stays pinned, unedited.
- D-93-A (wrong revision in the round-93 report text), D-93-B (no committed WAVE-DONE pointer),
  D-93-C (stale SCORECARD parenthetical), D-93-D (truncated receipts with no atomic write): fixed
  in this round's bookkeeping where the fix is in lane bytes; D-93-D is also answered by the v4
  atomic writer. The original truncated r93 files are kept as evidence and not rewritten.

## R94-C1 — calibration (measured): a JSON-safe receipt for the frozen repair battery

- **Surface.** The frozen round-93 counter `tools/round-93/stop-boundary-repair-battery-v3.py`
  scores a repair command and writes a receipt with `--json-out`. On the honest repair its
  receipt write raises `TypeError` (bytes in `fresh_cells[*].output`), so the positive control
  exits 1 with no valid receipt, and the two forgery receipts that do write are the only
  evidence. Calibration here = the receipt, the stdout verdict and the predicted verdict agree
  on every frozen run.
- **Candidate instrument.** `tools/round-94/stop-boundary-repair-battery-v4.py` imports the v3
  verdict code by path (sha pinned below) and changes only the receipt writer: bytes become
  `{"bytes": n, "sha256": hex}` via the `json` module's `default` hook; any other unknown type
  raises `TypeError` (no `str()` fallback); the receipt is written to `<json-out>.tmp` and renamed
  only after `json.dump` returns.
- **Frozen counting command (after).** For each frozen run, the public CLI with `--json-out`:
  `python3 -I -B tools/round-94/stop-boundary-repair-battery-v4.py --root . --repair-cmd <cmd> --work <scratch> --rev <measured> --expect '<FROZEN_LABEL>' --json-out <wave>/c1-v4-<name>.json > <wave>/c1-v4-<name>.stdout 2> <wave>/c1-v4-<name>.stderr; echo $? > <wave>/c1-v4-<name>.rc`
  where `<cmd>` is `tools/round-92/upx-stop-boundary-search-repair.py` (name `pos`),
  `.ufo/waves/round-93/controls/table5-window.py` (`F1`), `.ufo/waves/round-93/controls/carrierread5.py`
  (`F2`), `.ufo/waves/round-93/controls/identity_noop.py` (`F3`). Then
  `python3 tools/round-94/c1-receipt-agreement.py --dir <wave>  --prefix c1-v4`.
- **Frozen label (positive, the same string as round 93):**
  `repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2`.
- **Before (do-nothing control, scored at base with the frozen round-93 counter, committed here):**
  `.ufo/waves/round-94/pre/c1-base-v3-agreement.json`: valid 2 of 4, agree 2 of 4, predicted 2 of 4
  (`met False`). The positive run exits 1 with `TypeError` (`c1-base-v3-pos.stderr`) and the F3
  receipt is truncated (`c1-base-v3-F3.json`). The v3 counter is the do-nothing control: it cannot
  reach the target because it crashes on the honest case.
- **Frozen target (after, at the measured revision):** `c1-receipt-agreement.py` prints
  `counts_of_4` `{valid: 4, agree: 4, predicted: 4}`, `met` true, exit 0. Predicted verdicts:
  `pos` met True exit 0; `F1`, `F2`, `F3` met False exit 1.
- **Kill rule:** the positive run not met; any forgery met True; any receipt not valid JSON;
  any stdout line disagreeing with its receipt; the v4, v3, round-92 battery, round-92 v2 or
  agreement-counter sha256 differing from the pins below; the wrong `upx` sha (`cf2f6e7c6846a7c9…`).
- **Pins (sha256).** v4 `c41d54d72257ad41db7da5c42bea9e8ebc66fea88257660edc6e20c147266272`;
  agreement `dc384a4464c2cb045dea491d56855685e8058dc5567a6c3b6d6dc899875836c9`; v3
  `60026511e54cdc1df71233c491392fafcc89705808fa5c187d96a85862cbd4e3`; round-92 battery
  `63e9df431f5d7aeeca2bd5384efff36b4f2ebedfdc3ee71aaa250287fc9388bc`; round-92 v2
  `f6ddb48b4d9cbd460002db68d834f909955e2c7d4e60d7ad85325ef4e66f1874`.
- **Measured revision.** The declaration commit (this file's commit). The repair tool
  `tools/round-92/upx-stop-boundary-search-repair.py` is unchanged from round 92.
- **Limits named before data.** The fresh-pack arm has one source (`/usr/bin/env`). The
  forgeries are the round-93 controls. The `--selftest` exercises writer helpers only; the claim's
  evidence is the public-CLI runs above. A helper-only green is not counted.

## R94-C2 — depth: a craft decision table for the receipt-path failure class

- **Surface.** Round 93 found a counter whose receipt path crashed on the honest case (M93-e)
  and a selftest that did not exercise the public path. No craft row names that class, so a
  reader of `SKILL.md`'s craft section cannot find the guard. Candidate: craft block 33 (append-
  only; blocks 1-32 unchanged) with a decision table, corpus criteria QUALITY 189 and 190 that
  state the rules the rows assert, and a knowledge entry citing Python's `json` documentation
  (S319, opened this round).
- **Before (do-nothing control, committed here):** `.ufo/waves/round-94/pre/c2-base-block33-after-manifest.json`
  exit 1, `block 33 missing (craft has 32 blocks)`; `pre/c2-base-depth-v2.txt` exit 1
  `blocks 32 resolved 32 expect 33`; `pre/c2-base-depth-v3.txt` exit 1 (`blocks 32 ... expect 33`).
- **Frozen counting commands (after, at the measured revision):**
  1. `python3 -I -B tools/round-93/craft-citation-semantic.py --root . --manifest .ufo/waves/round-94/manifests/block33-after.json --block 33 --rev <measured> --json-out <wave>/c2-after-block33.json` → exit 0, `ok`.
  2. `python3 -I -B tools/round-89/depth-blocks-v2.py --root . --rev <measured> --expect-blocks 33` → exit 0, `blocks 33 resolved 33`.
  3. `python3 -I -B tools/round-91/depth-blocks-v3.py --root . --rev <measured> --expect-blocks 33 --shape-from 33` → exit 0, `required-shaped 1/1`.
- **Frozen predicate (the three keywords sets are in the manifest, frozen here):** block 33 carries
  the marker `receipt-path-json-safe v1`, a decision table with at least three body rows of at
  least four cells; each row's criterion cites exactly one QUALITY row whose text contains the
  row's frozen keywords: row `honest-case receipt crashes` → QUALITY 189 contains
  `bytes become a length and a sha256` and `temporary file`; row `truncated receipt read as a pass`
  → QUALITY 189 contains `complete JSON or absent`; row `helper-only selftest misses the public path`
  → QUALITY 190 contains `through its public command` and `re-read by a JSON parser`.
- **Frozen target (after):** the three commands exit 0 at the measured revision; block 33 at base
  exit 1 (done above); no depth regression: the v2 count of blocks resolved equals 33 of 33.
- **Kill rule:** any of the three commands unmet at the measured revision; block 33 present at base;
  the checker `craft-citation-semantic.py` sha256 (`34cf6579d7d0614336add1710912877492c68517331736fa5e4021ffedf05340`),
  the depth counters' sha256s (`depth-blocks-v2.py` `359f15e1…dcf18f`, `depth-blocks-v3.py`
  `bcf6c4ea…aeb052f`) or the manifest sha256 (`9d72f995…40ae`) differing from the pins.
- **Named limit (stated before data).** The keyword atom is a vocabulary check: a criterion that
  carries the keywords passes whether or not it states the rule. That residual is the round-93 limit
  already in QUALITY 188; C2 does not claim more than the vocabulary check.

## Sourced claim (frontier step)

R94-C1's and R94-C2's knowledge entry cite `S319` (Python `json` documentation, `default` hook:
"It should return a JSON encodable version of the object or raise a TypeError."), opened 2026-11-05
at `https://docs.python.org/3/library/json.html`, sha256 `8021264aedd0ae972ac10cc3ba950be85d95b62d4869289b4686bad62b9794c0`.

## Exploratory claims

None. Two counting claims.

## Honest stop

Both claims are single-commit byte-level predicates a closure can re-derive with one command.
Neither target is narrowed after landing: a miss is reported as a miss.
