# Round 91 — lesson: a stop-boundary tamper is refused, the packer's verdict separates it from an intact carrier, and a calibration row must name a receipt that resolves

Declaration `deb2765a55fef0e4e81500a027dfe59951b69e87` (`plans/round-91-claims.md`, `.ufo/waves/round-91/claims.json`, `tools/round-91/`); base `2135f6e1d3f69a259b32cc5167c52ccb1a261c24`. Claims: R91-C1 coverage (capability: the last-block stop-boundary class enters Core as a measured refusal), R91-C2 depth (craft rule block 31, a decision table, shape-floored from block 31).

## Gate

**Sources opened this round (CORPUS.md rule 1: re-opened by this lane, this round).**

| row | URL | access date | HTTP / size / sha256 | located quote (≤25 words) | used for |
|---|---|---|---|---|---|
| S313 | https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_unix.cpp | 2026-11-05 | `curl -fsSL` exit 0 (HTTP 2xx); 24181 bytes; sha256 `bf83c4133c27d39433db63bf604daf577d429d734c542d29c0b9cc8ed229642e` (matches the row) | line 496: `if (sz_cpr > sz_unc || sz_unc > (int)blocksize)` (the per-block bound, the decoder's only per-block arithmetic check; the next header is not cross-checked) | C1 knowledge entry `corpus/knowledge/2026-11-05-r91-stop-boundary-refusal.md` (the sourced claim) |

Line numbers pinned by `grep -n` on the fetched file: 476 `unpackExtent`, 485 `fi->readx(&hdr, szb_info);`, 496 bound, 497 `throwCantUnpack("corrupt b_info");`, 504 `fi->readx(ibuf+j, sz_cpr);`. The scout seat (`ScoutSource`) re-derives the same lines from the same URL and records the upstream `master` drift for the row's recheck field.

**Admit / reject.** Admitted: S313 re-ground for the C1 knowledge entry. Rejected: none this round (no new row was opened). The assimilation set is empty (`merge/kaidoku/` absent; `considerthese/` absent), so the assimilation admit/reject pair does not apply.

**Spot-check.** Pending the non-author closure (`corpus/lessons/round-91-verifier-spotcheck.md`, not written by this lane).

**Registry changes (old → new, log per CORPUS.md rule 2).** S313 `used-by`: `corpus/knowledge/2026-11-04-r90-interior-block-szcpr.md` → `corpus/knowledge/2026-11-04-r90-interior-block-szcpr.md, corpus/knowledge/2026-11-05-r91-stop-boundary-refusal.md`. `status` `mined` → `mined`; `recheck` `on-release` → `on-release`; `opened` unchanged (2026-11-04; the 2026-11-05 re-open is recorded here, not in the row). Row count 221 → 221 (no row added). Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` exit 0 before (`/fast/scratch/hyaku/kaidoku-r91/census-before.txt`) and after (see `## Census`).

## Mistakes

Each row: class · evidence pointer · captured-by (the criterion or rule that should have caught it, or `none`) · fix.

- **M91-1 · survivor (boundary class: silent and unsafe `rc 0`).** The round-90 repair returns `rc 0` on all eight last-block cells: two write bytes outside the tampered window (the sentinel word), six return a file `upx -t` still rejects byte-identical. Evidence: `.ufo/waves/round-91/pre/c1-base-round90-repair.json` (`refused 0 of 8; unsafe 2; silent 6`; `unsafe` cells `jq` −7 at bytes 10094–10097 and `libz` −7 at 60124–60127). Captured-by: `none` — round 90's counter scored interior cells only, and QUALITY 176 named the defect without a counter arm. Fix: `tools/round-91/stop-boundary-battery.py` (arms `refused`, `unsafe`, `silent`, intact control) and the repair's refusal branch. Shown able to fail: the same counter exits 1 on the round-90 repair (`met False`, `refused 0 of 8`).
- **M91-2 · vacuous calibration row (receipt revision and placeholder).** Round-89 and round-90 `SCORECARD.md` claim rows name receipts whose revision does not resolve, does not agree with the row, or is a `--rev <measured>` placeholder. Evidence: `.ufo/waves/round-91/pre/c3-at-base.json` (`mismatches 5` over four rows: R89-C1 A2+A3, R89-C2 A3, R90-C1 A2+A3). Captured-by: `none` (the round-90 spot-check's D-5 found the placeholder by reading; no counter ran). Fix: `tools/round-91/record-cells.py`; selftest `foreign` and `absent` cases red before green. Corrections land as new rows (see `## Round-90 routed defects`), not as rewrites.
- **M91-3 · receipt attribution (own pre-declaration receipt).** The first candidate receipt was stamped with the base revision (`2135f6e1d`) although it scored candidate bytes. Evidence: moved to `.ufo/waves/round-91/pre/probes/c1-candidate-premeasure-mislabeled-rev.json`; the frozen candidate receipt is `.ufo/waves/round-91/l1/scores/c1-at-declaration.json` at `deb2765a`. Captured-by: QUALITY 173 (a claim's after-receipt is taken at the measured revision) — the rule existed and this lane missed it before declaration. Fix: re-measured at the declaration commit; the mislabeled file is kept as a premeasure, not a receipt.
- **M91-4 · false-refusal of intact carriers (own design error, caught by selftest).** The first version of the repair refused on every branch where no successor decided the walk, which refused intact carriers (`intact-fixture-identical` red). Evidence: the selftest run before the fix. Captured-by: the repair's own selftest (existing). Fix: the `upx -t` gate on the input, which separates intact from tampered; the intact arm of the frozen counter then holds `4 of 4`.
- **M91-5 · unsupported sentence in an admitted-draft (own knowledge draft, caught before landing).** The first knowledge draft said a `+7` value keeps the walked total equal to `u_len` on every carrier (it does not on `libz`) and cited a `--lzma` probe receipt that was never saved. Evidence: the draft's first version; corrected in `corpus/knowledge/2026-11-05-r91-stop-boundary-refusal.md` (Limits and the geometry paragraph). Captured-by: CORPUS.md "a count carries its command" (partial: the `libz` total was not checked against the probe output before writing). Fix: sentence corrected to the measured numbers; the unsaved probe is removed from the claims and its script was dropped from `pre/probes/`.
- **M91-6 · role error in the wave spec (process).** The first spec used `labrat` as a top-level swarm role; the validator refused it (`unknown_role`, `items[6]`). Evidence: `.ufo/waves/round-91/r91-w1-dispatch.err` (first attempt, overwritten by the accepted run). Captured-by: the validator (existing). Fix: the falsification item moved to a `reviewer` seat; `labrat` stays a depth-2 probe under an executor, per the card.

## Round-90 routed defects — dispositions

The round-90 non-author spot-check (`corpus/lessons/round-90-verifier-spotcheck.md`, §7) routed D-1..D-6 to round 91.

- **D-1 (record drift).** Disposition: correction entry appended to `LOG.md` (`## 2026-11-05 — round 91 correction of the round-90 record`) naming the superseded text (217 → 220 rows; QUALITY 172–173) and the measured tree (221 rows; S313/S314/S316 admitted, S315 rejected; QUALITY to 177). `SCORECARD.md` gets a correction row, not a rewrite.
- **D-2 (report minimum content).** Disposition: the round-90 report is not edited (append-only). The round-91 correction entry names the row `c264f7a4` and its missing `LOG.md` cell; the round-91 report's landed-changes table has a `LOG.md` cell on every row.
- **D-3 (receipt/revision attribution).** Disposition: `.ufo/waves/round-90/pre/c2-depth-at-base.json` records `54c277868511…` as its revision; the round-90 record's `at fc52cc9dc` is corrected in the round-91 correction entry. The measurement transfers (`sha256(SKILL.md)` equal at both revisions, per the spot-check).
- **D-4 (registry home).** Disposition: `SKILL.md` registry rows added for `tools/round-90/upx-break-repair.py`, `tools/round-90/upx-later-block-battery.py`, `tools/round-90/control-cheat-repack.py`, and the four round-91 instruments.
- **D-5 (SCORECARD counting command).** Disposition: the correction row names `499d2183a67058d5648b51a2abf50c10012b1292` and `.ufo/waves/round-90/l1/scores/c1-at-499d2183.json` for the round-90 C1 row (its `--rev <measured>` placeholder is the record-cells A2 failure, `pre/c3-at-base.json`).
- **D-6 (attack-share label).** Disposition: the round-91 report counts attack seats by the house list (reviewer, critic, mutation-tester, labrat-as-probe) and states the count.

## Wave `r91-w1` — seat results

Pending: the wave is dispatched through the inline handoff (`.ufo/waves/round-91/r91-w1.ready`, dispatch `r91-w1-dispatch.json`, 12 spawn seats). The seat-by-seat results and the disposition of every attack finding are recorded here when `WAVE-DONE r91-w1` arrives.

## Census

- Before: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` → exit 0, `ok` (`/fast/scratch/hyaku/kaidoku-r91/census-before.txt`; 221 rows).
- After: pending the final run at the round's last commit.

## Named limits (carried, not closed here)

- The frozen `refused` arm accepts any nonzero rc. Every one of the eight declaration cells exited 2 (`.ufo/waves/round-91/l1/scores/c1-at-declaration.json`, `cells[].rc`), but the frozen label does not assert rc 2. QUALITY 177 names this; the amendment belongs to a later round.
- The regression arm (`P1 6 of 6; P2 4 of 4; P3 4 of 4`) is run by a wave seat (`ExecRegress`), not by the L1 at the declaration commit; its receipt is copied into `l1/scores/` once the seat lands.
- `tools/round-91/record-cells.py` covers rounds 89–90 only (`--rounds`), and round 88's battery receipts predate the revision field; they are not re-derived.
