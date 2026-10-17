## CLAIM
Convergence diff, item 2 (r4u-01 `.fwimage` decimal misconversion). Substance: CONVERGENT across both lanes — both `:41` decimals are wrong; correct values 29,367,752 B / 84,258,816 B; disposition is an append-only EOF erratum. Residuals for the parent: (a) the Lane A erratum drafts' headings collide with C4's gate literal; (b) the original readelf receipt is absent from the entry (history UNPROVABLE; closed practically by hash-matched re-verification).

## METHOD
Primaries first, before any lane read: HEAD text (worktree == HEAD), `python3 -c 'print(0x1c01dc8,0x505b000)'`, read-only `readelf -SW` + `sha256sum` on `/usr/lib/firmware/nvidia/610.57.04/{gsp_tu10x,gsp_ga10x}.bin`, `:49` arithmetic, round-4 queue `.ufo/reports/luna-round-4/kaidoku.md:50-52`. Then diffed every item-2 output: Lane A C2/C4/C5/C7/D2/F1/F2/G2/H1/H2/H4/K1/P0/P1/P2/R1/R2/R6/R7/S2/T2/T3/V2/X1/X2/X4; Lane B CB5/CB10/FB/HB1/PB0/VB2; `receipts/census-pre.out`.

## FINDINGS
- CONVERGENT, unanimous (30 readings): `:41` pairs `0x1c01dc8`=29,358,536 B and `0x505b000`=84,242,432 B; both decimals wrong; correct **29,367,752** / **84,258,816** (understated 9,216 / 16,384). `:103` is hex-only; `:49` extent 29,365,384+37×64 = 29,367,752 = `0x1c01dc8`, exactly. All agree: byte-prefix append, no rewrite; `:41` is the only error copy. Lane B HB1 additionally hypothesizes the ga10x slip ('b' misread as '7': 0x5057000 = 84,242,432).
- Ground truth (my run): `readelf -SW` shows `.fwimage` sizes `1c01dc8` / `505b000`; sha256s match `:10-13`; `.fwversion` @`1c01e2c` is consistent with section end `0x1c01e08`. Worktree r4u-01 sha256 `d565f690…` (agrees with FB/SB2).
- DIVERGENT (interface; unreconciled in either lane): C4's gate requires the final heading to contain `## Errata (round 5 freshness`; C2 recommends `## Errata (luna-round-5, …)`; drafts use `## Errata (round 5 audit…)` (D2), `### Erratum (luna round 5…)` (R7 — h3 would nest under `## Errata (round 6)`, `:114-119`), or no heading (G2/V2). X1/`census-pre.sh` pass on any tail containing the four tokens. Land a top-level heading containing "Errata (round 5 freshness" to satisfy both gates.
- UNILATERAL/minor, no disposition change: D2 alone anchors the durable queue (round-4 report in HEAD; C05 disk-only — verified); H2 alone flags `:63` "13.7 MB" as truncating 13.756760 MB; HB1 alone notes `:25` "24 nonzero bytes" wording. Timing artifacts: R1 "D2 unavailable", R6 "H1 absent", CB5/CB10 "siblings not visible".

## THREATS
No REA probes per wave rules; if the on-disk blobs were substituted, arithmetic alone still yields both corrected values. The heading fix is textual, pre-landing; re-verify after landing via X1/T3 append-prefix checks plus C4's gate.

## VERDICT
FINDING: item 2 CONVERGENT across both lanes (29,367,752 / 84,258,816, append-only); reconcile the errata heading contract before landing.
