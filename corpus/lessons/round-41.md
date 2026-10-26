# Round 41 — genuine AVM-layout BE SquashFS v4 promoted to Core on four fresh carriers with an exact-path counter; triage table v3 matches the independent evaluator 52/52 but stops on a declared-tuple key mismatch

Base `49096c7e6f226af0c750c4b003be58883cb6049f`. Freeze `d764389e9cbe61b9d1b07538ff3bff02d50bb34f`
(`plans/round-41-claims.md`, `tools/round-41/*`, C1 carriers/oracles/gap rule, SKILL rule block 20 and its entry,
C2 control tables and the dev set, wave-1 evidence). Controls `9a8fb26001307bc2159934ed53c5fc43e5c8d615`. Data: C1
receipts `5ca6941b061591748c6755c1dcfc188941fcbd35` (V4 `after.json` added at `e9a24d07`), C2 held-out
`8a1f4c73057405a4b470af11d1d351a0f03f6c34`. C1 landing documents `042b87697e7d94e9fc2d3cbcf03541bfd5c03b98`;
measured revision `e9a24d07256d1606f01aa4d2d65f74e649c5f3d4`; scores `bf5286c9832142a2ceabe2076883dfa2a8e99356`.
L1 `KaidokuR41`. Wave 1: 41 seats (`.ufo/waves/round-41/w1/`); wave 2: 33 seats (`.ufo/waves/round-41/w2/`).

Author verdicts (closure pending):

- **R41-C1 met.** `tools/round-41/c1-counter.py` at `e9a24d07`: `carriers_matched 4` of 4, every binding true,
  `frozen_path_changed []`, exit 0, including a counter-time REA rerun of each carrier
  (`.ufo/waves/round-41/l1/scores/c1-at-e9a24d07.json`); `c1-extra.py` met, exit 0. Before: 0/4 at the freeze
  (do-nothing) and 0/4 with the round-40 receipts copied to the round-41 paths
  (`.ufo/waves/round-41/controls/c1/`). V3 (5490 wrapper) 8 files, 85 symlink gaps; V4 (5491 nested rootfs)
  6349 files, 611 symlink gaps + 4 `MaliciousSymlinkRemoved` removals; L3 13 files, L4 14 files, 3 symlink gaps
  each with both collision directions published exactly; each + 1 `depth-limited`. At `042b8769` the same
  counter scored 3/4 because V4's `after.json` was not in the tree (M41-3); that score is kept, not hidden.
- **R41-C2 not met — honest stop.** `tools/round-41/c2-counter.py` at `e9a24d07`: `matched 52` of `n 52`
  (every interpreter pair equals the independent evaluator's), `distinct_decisions 13`, real-receipt binding
  true, but `observed_features_match_declared` false, exit 1 (`.ufo/waves/round-41/l1/scores/c2-at-e9a24d07.json`):
  the 12 `combo` carriers carry their declared tuple under the manifest key `declared` while the frozen counter
  reads `class_expected.features`/`features`/`declared_features` (`declared_features.missing` = C01..C12). The
  stop is entailed at the freeze; the rule is not changed after scoring.

## Mistakes

| id | class | evidence pointer | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| M41-1 | a two-seat interface frozen without an end-to-end dry run: the generator wrote the combos' declared tuple under `declared`, the counter read three other keys, and the L1's pre-freeze dry run used its own control scorer (`tools/round-41/c2-controls.py`) instead of the frozen counter | `.ufo/waves/round-41/l1/scores/c2-at-e9a24d07.json` `declared_features`; `tools/round-41/c2-counter.py` declared-tuple lookup; manifest `corpus/evidence/round-41/c2/heldout/manifest.json` | QUALITY 83 (dry run before the freeze) — it was applied to C1 (`l1/dryrun-c1.json`) and not to C2 | QUALITY 84; `.ufo/waves/round-41/l1/mistakes/declared-keys.py`: held-out manifest → 12 unreadable, exit 1 (`m41-1-red.txt`); the same manifest with the tuple copied under `features` → exit 0 (`m41-1-green.txt`) |
| M41-2 | provenance written against the authoring host: S126's URL cell names a file in the sibling shokuknow project, unresolvable from a lane checkout (round-40 closure D1) | `corpus/SOURCES.md` S126; `w1/R41MistakeHunt.md` MH-1 | none | byte copies under `corpus/evidence/round-41/s126/`, map `corpus/evidence/local-sources.json`, gate `tools/round-41/local-source-gate.py` (23/23 selftest): S126 unresolved at the base, resolved at the tip; the gate still exits 1 on 18 other host-local rows (routed R41-CL3) |
| M41-3 | evidence silently left out of a commit: `jj-lane.sh` commits a named directory like `git add` and skips new files over 1 MiB, so V4's 2.8 MB `after.json` missed `5ca6941b` and the first score read 3/4 | `5ca6941b` stat (no V4 `after.json`); `l1/scores/c1-at-042b8769.json` (V4 `receipt_present` false); fixed at `e9a24d07` | none (the helper prints a warning; the L1 did not read it) | QUALITY 84; `.ufo/waves/round-41/l1/mistakes/evidence-tracked.py`: at `5ca6941b` → missing V4 `after.json`, exit 1; at `e9a24d07` → exit 0 |
| M41-4 | a seat kept editing its artifacts after the L1 copied them into the freeze | `.ufo/waves/round-41/w1/artifacts/R41C1Counter-postfreeze/README.txt` (mtimes 18:12 -03, freeze 18:06) | wave context rule "never touch them afterwards" (not enforced) | post-freeze versions moved aside, freeze bytes restored (`7a24ff74`); the frozen tool is the L1's copy in `tools/round-41/`, which wave 2 diffed (`w2/R41W2Freeze.md`) |
| M41-5 | `c1-run.sh` passes a JSON summary through `jq --argjson`, which exceeds ARG_MAX on a rootfs receipt; V4 has `after.json` but no `run.json` | `.ufo/waves/round-41/l1/c1-run-V4.log`; `corpus/evidence/round-41/c1/V4/run-harness-failure.log` | none | no counter clause reads `run.json`; fix routed R41-CL2 (`--slurpfile`), measured by `w2/R41W2C1Run.md` |

## Gate

### Sources opened this round (2026-10-26)

| row | URL | opened | located quote (≤25 words) |
|---|---|---|---|
| S127 | https://download.avm.de/fritzbox/fritzbox-5490/other/fritz.os/ | 2026-10-26T20:21:50Z (`w1/R41SrcAvm.md`) | "Product: FRITZ!Box 5490" / "Version: FRITZ!OS 7.31" (`info_en.txt` lines 8, 10; `w1/artifacts/R41SrcAvm/quote-excerpts.txt`) |
| S128 | https://download.avm.de/fritzbox/fritzbox-5491/other/fritz.os/ | 2026-10-26T20:21:52Z (`w1/R41SrcAvm.md`) | "Product: FRITZ!Box 5491" / "Version: FRITZ!OS 7.31" (`info_en.txt` lines 8, 10; same file) |
| S129 | https://raw.githubusercontent.com/ReFirmLabs/binwalk/26713972e3f9f52dc37d4a421c4554b0bd9e82ef/README.md | 2026-10-26T20:22:20Z (`w1/R41Assim.md`), re-opened by the L1 2026-10-26T21:17:49Z, HTTP 200, sha256 `87b8277e…11d4` | "This is an updated version of the Binwalk firmware analysis tool, re-written in Rust for speed and accuracy." (line 3) |

Registry 126 → 129 rows, all tier A, `mined`. S127/S128 land with the C1 documents (`042b8769`), S129 with
the assimilation (`e1c83313`). `used-by` changes: none on existing rows. S129's staged recheck prose
(`curl … | grep -c 'Binwalk v3'` -> 1) was stripped to `180d`; the recheck now lives in the entry header.

### Assimilation

Theme: SquashFS triage domain guard (`/home/vgpnk/Projects/shokuknow/merge/kaidoku`), review `w1/R41Assim.md`.
**Admit 1:** `firmware-region-vocabulary` → `corpus/knowledge/2026-10-26-binwalk-v3-unit-of-work.md` with four
repairs (commit pin, anchor lines 3 and 9, normalized recheck, name and used-by); every source re-opened.
**Reject 1:** `unblob-sasquatch-dependency` — duplicate ground: the lane already holds
`2026-10-26-unblob-sasquatch-dependency` (flip: a new upstream statement the held entry lacks). Id-collision
check (`w1/artifacts/R41Assim/assimilation/`): `reg-ids` 126, `staged-ids` 132, `collisions` 21 (S106–S126),
all positional drift; the 0–3-space guard is proven on an indented fixture. Renumber by document: staged
S109 (ReFirmLabs binwalk README) → lane S129. Quarantine slice: 5 rows, sha256 `7383a90e…28e6a`,
byte-identical to rounds 38–40; nothing appended from it.

### considerthese

No `considerthese/` directory exists in this lane.

## Round-40 spot-check disposition (`corpus/lessons/round-40-verifier-spotcheck.md` §5)

| id | state | where |
|---|---|---|
| R40-CL1 | fixed | exact-path rule in `tools/round-41/c1-counter.py`; both collision directions on L3/L4 scored exactly (C1 4/4) |
| R40-CL2 | open | the rerun proves consistency, not provenance (disclosed in the claims) |
| R40-CL3 | fixed in the C2 counter | whole `tools/round-41` and both writers are frozen paths; restore does not un-block (selftest) |
| R40-CL4 | fixed | partial recipe pinned by the damaged block's compressed length (`heldout-gen-v3.py` `partial_pin`) |
| R40-CL5 | fixed in prose | block 20 cause cells, no embedded table copy, layout pre-check, block-18/19 sentences; reviewed `w2/R41W2C2Table.md` |
| R40-CL6 | fixed | `fetch-vendor.py` checks `member_sha256` (and `nested.sha256`) fail-closed |
| R40-CL7 | open (operator) | vendor terms vs analysis; only paths, sizes and digests are published |
| D1 | fixed for S126 | M41-2 |
| D2 | open (operator) | round-40 vendor texts in history at `7fce3086` |
| D3 | addressed | expected pairs from an evaluator written from the precedence text, plus 12 seeded combos; C2 stopped on M41-1 |
| R36-CL5 | open | carried |

## Routed defects into round 42

| id | defect | evidence |
|---|---|---|
| R41-CL1 | C2 counter/generator declared-tuple key mismatch; refreeze with one key and an end-to-end dry run of the frozen counter on the dev set | M41-1 |
| R41-CL2 | `c1-run.sh` ARG_MAX on rootfs summaries | M41-5 |
| R41-CL3 | 18 other SOURCES rows name host-local paths without in-lane copies | `tools/round-41/local-source-gate.py` at the tip |
| R41-CL4 | the interpreter's handler `none` (no `squashfs*` chunk) and the precedence's step 2 (no `squashfs_v4_*` handler) diverge on a v1–v3-only chunk | `corpus/knowledge/2026-10-26-r41-sqfs-triage-v3.md:22-25` |

## Criteria added

- QUALITY 84 (M41-1, M41-3).

## Wave 2 (33 seats, all settled)

Neither author verdict was overturned. R41-C1 was re-scored met at `e9a24d07` and `e1c83313` (`w2/R41W2C1Rescore.md`). V3 and the oracles reproduce (`R41W2ReproV3.md`, `R41W2C1Oracle.md`). The reservation scan found zero REA/unblob runs on reserved carriers before the freeze (`R41W2Reservation.md`). All 8 removal mutations were refused (`R41W2C1Removal.md`). C1 is a coverage move (`R41W2C1AxisFit.md`).

Open C1 limits:

- Oracle-only fabrications pass the rerun projection on 3 of 4 carriers, though none reaches the target (`R41W2C1Fabricate.md`; R40-CL2).
- `fetch-vendor.py` follows symlinks on write (`R41W2C1Chain.md`).
- The path rule accepts a non-segment-bounded diagnostic root (`R41W2C1PathRule.md`).
- 12 of 29 counter mutants survive (`R41W2C1Mutants.md`).

R41-C2 stop confirmed (`R41W2C2Rescore.md`, `R41W2C2AxisFit.md`). A one-line mutant that reads `declared` flips the claim to met while the counter's 70-case selftest still passes (`R41W2C2CounterMut.md`). That is the rule changed after scoring, so it is not this claim's rule; it is routed as R41-CL1. Further C2 findings:

- 9 of 41 interpreter/evaluator mutants survive.
- The interpreter and the evaluator disagree on 5 envelope shapes that the held-out set never exercises (`R41W2C2InterpMut.md`).
- The lookup control scores 8 of the 12 combos (`R41W2C2Combos.md`).
- The `dep-missing-le` cause cell overclaims what the grammar can do (`R41W2C2Table.md`, MEDIUM).

All of these are routed into round 42 with R41-CL1..CL4.
