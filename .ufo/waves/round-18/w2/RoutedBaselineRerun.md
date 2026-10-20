HOLDS — the C1 counting command reproduces 6 open defects at baseline and 0 at the lane revision; every baseline-open check names a real, independently confirmed gap.

Seat: KaidokuR18.RoutedBaselineRerun (author-side advisory, read-only; the tool itself runs only read-only `git` subprocesses: rev-parse/cat-file/show/merge-base, `.ufo/waves/round-18/tools/routed-defects.py:72-119`).

# Commands run (verbatim)

```
python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 9011581d84527ba34c675f9cf912e54d2e72d470
python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev b2aad08ceeee8dd125ce0d316056d8bd766c7f94
python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 9011581d84527ba34c675f9cf912e54d2e72d470 --strict
python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev b2aad08ceeee8dd125ce0d316056d8bd766c7f94 --strict
```

(The `--root` path was given absolutely as assigned; outputs were redirected to /tmp, outside the lane.)

# Observed results (observation, from captured JSON)

| rev | exit | exit --strict | open_count | named_open | substance_open |
|---|---|---|---|---|---|
| 9011581d84527ba34c675f9cf912e54d2e72d470 (baseline) | 0 | 1 | 6 | 6 | 6 |
| b2aad08ceeee8dd125ce0d316056d8bd766c7f94 (REV) | 0 | 0 | 0 | 0 | 0 |

- Baseline: all six defects {R17-PINMAP, R17-VALIDATE16, R17-PRODUCER-REV, R17-SUMS-RUNLOG, R17-REGISTRY, R17-S032-DIGEST} open with named_open=True and substance_open=True.
- REV: all six closed on both sets. `--strict` semantics confirmed at routed-defects.py:1275-1289 (exit 1 iff open_count > 0); observed 1 at baseline, 0 at REV.
- This matches claims.json:13 ("open routed R17 defects 6 at 9011581 -> 0") and the amendment ("named 6, substance 6 -> after 0").

# Each baseline-open check names a real gap (observation)

Independent `git show 9011581:path` checks confirm no check fails spuriously:

- R17-PINMAP (10/10 baseline checks red): `carrier-run.py` has zero `map_sha256` literals (grep -c = 0) and `receipt-validate.py` has zero `mid_map` literals; SCORECARD.md/LOG.md/knowledge doc have zero `R17-` defect-name lines; `corpus/lessons/round-18.md` and `.ufo/waves/round-18/runs/` do not exist at 9011581 (cat-file -e → 128). All real absences — round-18 artifacts legitimately post-date the baseline.
- R17-VALIDATE16 (7/7 red): `.ufo/waves/round-18/evidence/validate16/summary.json` absent at 9011581 (real — evidence created this round); no `R17-VALIDATE16` line in SCORECARD.md/LOG.md (grep -c = 0).
- R17-PRODUCER-REV (5/5 red): no `R17-PRODUCER-REV` line in SCORECARD.md/LOG.md/knowledge (grep -c = 0); correction lines were appended only this round.
- R17-SUMS-RUNLOG (4/4 red): baseline `.ufo/waves/round-17/predictions/SHA256SUMS` has 17 lines and **no `predictions/carriers.tsv` line** (listed in full; the missing historical line is `8ac38afe…4d3eb5  predictions/carriers.tsv`); LOG.md has no `R17-SUMS-RUNLOG`/`7/8` line. Real manifest gap.
- R17-REGISTRY (9/9 red): `git show 9011581:SKILL.md` — row `go-route-compare` (line 540) 5th cell lacks `Write scope:`; `receipt-validate` (541) lacks it; `pins` (542) lacks it and says `tool / kaidoku`; `go-buildinfo-probe` (545) lacks it; `citation-drift` (448) 2nd cell is `probe / kaidoku`, not `gate …`. All real cell contents.
- R17-S032-DIGEST (3/3 red): `corpus/SOURCES.md` at 9011581 has 0 `supersedes S032` rows (S033 opened this round); `.ufo/waves/round-18/evidence/s032-digests.json` absent (cat-file -e → 128). Real.

# REV anchors (observation, `git show b2aad08:path` line numbers)

- R17-PINMAP: `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:204-205`, `SCORECARD.md:2438`, `corpus/QUALITY.md:31` (row 21, why-cell names spotcheck + R17-PINMAP), `corpus/lessons/round-18.md:62` (Mistakes row 1), `carrier-run.py:511,650,711` (`map_sha256` in code), `receipt-validate.py:514,566` (`mid_map_sha256_mismatch`, `mid_map_compare_mismatch`), `.ufo/waves/round-18/runs/calib-aether/receipt.json:1937-1956` (3 pin_checks each with `map_path`+`map_sha256`).
- R17-VALIDATE16: `.ufo/waves/round-18/evidence/validate16/summary.json` (rev=da64646…, 8 receipts, int exits, validator_sha256=61844882…), `SCORECARD.md:2439`, `LOG.md:2159`; summary labels equal the 8 receipt-bearing run dirs at da64646.
- R17-PRODUCER-REV: `SCORECARD.md:2440`, `LOG.md:2161`, knowledge `:206`; both producer revs verified ancestors of REV via `git merge-base --is-ancestor`.
- R17-SUMS-RUNLOG: REV `SHA256SUMS:5` = `8ac38afe…4d3eb5  predictions/carriers.tsv`; `LOG.md:2160` states true fraction 7/8 (7 `== <label> start` lines at da64646 run-log / 8 carriers.tsv labels).
- R17-REGISTRY: `SKILL.md:540,541,542,545` 5th cells now carry `Write scope:` with existing scoped paths; `SKILL.md:448` citation-drift 2nd cell now starts `gate`.
- R17-S032-DIGEST: `corpus/SOURCES.md:39` S033 row, 11 cells, teaches starts `supersedes S032 —`, anchor cell contains `fetch-time` and 40-hex `a214355498e84aa86280be0c31c955aaf94f2d12`; `.ufo/waves/round-18/evidence/s032-digests.json` holds 5 distinct 64-hex page digests (s032_recorded + 3 fetches shown; ≥2 required).

# Assessment

- HOLDS on the amended C1 count: 6 → 0, named 6 → 0, substance 6 → 0, strict exit 1 → 0.
- Baseline-open checks are not vacuous: every failure was re-verified against the baseline Git objects directly (absent paths, absent lines, absent literals, real wrong-cell contents).
- No REV-side check passes on a technicality spotted in this pass: the satisfying anchors are code (tokenized, non-comment) or real evidence files, not just prose tokens — consistent with the wave-1 circularity fix (substance checks at routed-defects.py:240-291, 435-483, 514-526, 564-609, 676-687, 746-778).

# Caveats (observation → inference boundary)

- I verified checks individually against objects, not that the check *set* exhaustively covers each routed defect (that is the sibling reviewers' scope).
- The `r18-receipt-pinmaps` substance check found receipts under `.ufo/waves/round-18/runs/`; I spot-checked calib-aether only (3 mid maps, verified digests reported by the tool at receipt.json:1937-1956). Other receipts were not individually re-opened — inference of the tool's reported pass, not independent re-verification.
- No tools installed; python3 + system git only. No lane files written; only this report.
