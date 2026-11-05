# ScribeEntry — round 90, R90-C1 (coverage) and R90-C2 (depth), draft entry

Seat: ScribeEntry (scribe). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Base of the plan: `fc52cc9dc`; measured revision: `18b21f092` (current HEAD at measurement; `git rev-parse --short HEAD`). Tree writes: this seat dir only. No tracked file, no git mutation, no install (every tool used was already present: `/usr/bin/upx` 5.2.0, `/usr/bin/bwrap`, `python3`, REA 6.5.0 from the npx cache). No install to record.

## Outcome

- **R90-C1 is not met at this measurement.** The frozen counter's first run returns `P1 6 of 6; P2 3 of 4; P3 4 of 4`, exit 1, `met_target` false. The frozen expectation is `P1 6 of 6; P2 4 of 4; P3 4 of 4`. The entry records the label as measured and does not enter the class into Core. Per L1 direction the verdict is the L1's to take at the landing revision.
- **R90-C2 is not met at HEAD**, as expected: block 30 is not in `SKILL.md` at `18b21f092` (depth counter, exit 1). Writing block 30 is not in this seat's task.
- **Entry drafted:** `.ufo/waves/round-90/w1/ScribeEntry/2026-11-04-r90-break-point-szcpr.md` (14,891 bytes, 112 lines; the byte count is `wc -c`, measured after the last edit), the candidate for the L1 to integrate byte-exactly.

## Measured (command → result, exit, receipt)

All commands run from the lane root with absolute receipt paths; `RC` = `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ScribeEntry/receipts`.

| # | command (abridged) | result | exit | receipt |
|---|---|---|---|---|
| 1 | `python3 -I -B tools/round-90/upx-later-block-battery.py --root . --rev 18b21f092 --pkg <rea 6.5.0> --work /fast/scratch/hyaku/kaidoku-r90/ScribeEntry/battery --expect "P1 6 of 6; P2 4 of 4; P3 4 of 4" --json-out $RC/c1-battery.json` | label `P1 6 of 6; P2 3 of 4; P3 4 of 4`, `met_target` false; all controls true | 1 | `$RC/c1-battery.json`, `$RC/c1-battery.rc`, `$RC/c1-battery.stdout`, `$RC/c1-battery.time` (3m47s wall) |
| 2 | `python3 -I -B tools/round-89/depth-blocks-v2.py --root . --rev 18b21f092 --expect-blocks 30 --json-out $RC/c2-depth-head.json` | `blocks 29 resolved 29 expect 30 unresolved 0 met=False` | 1 | `$RC/c2-depth-head.json`, `.stdout`, `.rc` |
| 3 | `python3 -I -B tools/round-90/upx-break-repair.py --selftest` | `SELFTEST cases=17 failures=0` | 0 | `$RC/repair-selftest.stdout`, `.rc` |
| 4 | `python3 -I -B tools/round-89/depth-blocks-v2.py --selftest` | `SELFTEST cases=10 failures=0` | 0 | `$RC/depth-selftest.stdout`, `.rc` |
| 5 | instrument pins: `sha256sum` of the nine instruments in `.ufo/waves/round-90/claims.json` `instruments` | all nine equal the pins (`upx-later-block-battery.py` 84664f52…, `upx-break-repair.py` aaf3536e…, and the seven others) | 0 | `$RC/pins-check.txt` |
| 6 | `/usr/bin/upx -V`; `sha256sum /usr/bin/upx`; `sha256sum` of rea-agents `package.json` | `upx 5.2.0`, sha256 cf2f6e7c… = pin; rea `package.json` a500302… = pin | 0 | `$RC/pins-check.txt` |
| 7 | `sha256sum rea-agents/package.json` | a500302319c1… equals the pin | 0 | — |
| 8 | independent layout: packs jq, xxd, libz, docker-init with `upx --best` and reads the first segment, intact totals | jq 30,800/30,800 (5 blocks); xxd 38,928/38,928 (5); libz 98,592/108,560 (3); docker-init 851,288/851,288 (5); packed sizes 14,036 / 19,560 / 65,580 / 357,784 | 0 | `$RC/indep-layout.json`, `$RC/scripts/indep.py` |
| 9 | independent tamper matrix: 4 carriers × every first-segment block × stored ±7 (36 cells), repair run in an isolated `in/` directory; `upx -t`, `upx -d` sha check | 26 recovered, 8 unchanged, 2 out-of-window writes; interior non-last 18 of 20 | 0 (repair rc 0 in all 36 cells) | `$RC/indep-cells.json`, `$RC/indep-cells-summary.txt`, `$RC/indep-matrix-summary.txt`, `$RC/scripts/cells.py` |
| 10 | `upx -t` on every tampered cell (36) | 36 of 36 `Exception: compressed data violation`, rc 1 | 1 (per cell) | `$RC/upx-t-tamper-messages.txt` |
| 11 | per-cell repair info (derived, accounting) | interior block 1: jq 1644/1658 → 1651; xxd 943/957 → 950; docker-init 195/209 → 202; accounted = `u_len` | 0 | `$RC/indep-info/*.info.json`, `$RC/indep-info-summary.json` |
| 12 | in-process `repair()` timing, 5 runs per carrier, interior tamper | median/min: jq 10.3/9.1 ms (13,135 offsets); xxd 11.0/8.2 ms (18,662); libz 43.1/40.3 ms (56,002); docker-init 139.5/132.5 ms (356,909) | 0 | `$RC/scan-timing.txt` |
| 13 | REA on the 1267 bytes, two reruns on a copy at a different path | both 1268, rc 0; evidence ids `ev_8af5b445…` (both) | 0 | `$RC/rea-dinit-p2-rerun1.json`, `…rerun2.json` (+ `.rc`, `.stderr`) |
| 14 | REA counts gathered from the battery's candidate directory (`r90-boxes-1awyz7f3`, 14 candidate runs and 4 originals) | docker-init bytes (sha `0bd49c8d…`): 1268 in six runs, 1267 in one (`cand-wfjxkumn`) | 0 | `$RC/rea/*.rea.json`, `$RC/rea/rea-orig-*.json` |
| 15 | `git status` for tracked-file changes | no change by this seat; the modified and untracked entries are other seats' and the L1's | — | — |

## What I found

1. **C1 P2 cell (docker-init, round-89 class) fails on one REA run.** Repair rc 0, `upx -d` pin, `upx -t` rc 0, `rea_recover` false because REA reported 1267, the original reports 1268. Six other REA runs on the same bytes report 1268. The counter's REA arm is therefore not stable at the single-count level on this carrier (measured, cause not identified). This is recorded as Limit 6 in the entry, with receipts.
2. **Last-block defect (new, measured).** The break-point repair's stored-chain-intact branch with no survivor falls through to the round-89 law instead of refusing as its own docstring says. On jq and libz with a −7 tamper on the last block, that law writes the four-byte `UPX!` word at the chain-stop sentinel (jq 10,094; libz 60,124), outside the window, rc 0, `upx -t` still rc 1 (`indep-cells.json` cells `jq-b4--7`, `libz-b2--7`). The frozen counter scores interior cells only, so it cannot see this. Routed to the L1 as an executor defect: the fall-through should refuse for later-block prefixes, or the docstring should state the branch.
3. **Labels.** Eight cells return rc 0 with no changed bytes, fail `upx -t` rc 1, and are labelled `intact` (`indep-info-summary.json`). Label and packer disagree; recorded as Limit 2.
4. **Interior derivation holds on jq, xxd, docker-init.** 18 of 18 interior cells in both directions, derived value equal to the midpoint of the ±7 pair, accounting equal to `u_len`, stored chain under-accounting in every such cell.
5. **libz is out of class as declared** (stored chain 98,592 of 108,560), and its interior tamper is returned unchanged with the `intact` label (2 of 2 cells). Recorded as the declared exclusion, measured.
6. **Scan cost** is reported as four measured points, not a curve (`scan-timing.txt`); the per-offset minimum is 0.37–0.72 µs across carriers.

## Source-row status

- S311, S312 (registry rows opened 2026-11-04), S306, S309, S310 are cited by their registry ids and anchors, as in the round-88/89 entries.
- **Pack-side row: absent.** The scout's report `.ufo/waves/round-90/w1/ScoutUpxPack/ScoutUpxPack.md` does not exist at this checkout (`ls` → `No such file or directory`), and `corpus/SOURCES.md` ends at S315 with no new row. The entry says so and cites none. The L1 must add the row, or the entry's source list stays as it is.

## Provenance-trio deviation (flag for the L1)

- The file name uses the date 2026-11-04 as the task specified. The measurement ran at 2026-11-05 03:00 UTC (`date -u`). The entry's `verified-at:` line states 2026-11-05 with the receipt path, since the measurement date is the true one. If the L1 wants the file date and the verified-at date to match, one of the two must change.
- No SCORECARD round-90 section existed at draft time (`grep -n 'round-90' SCORECARD.md` found none). `verified-at:` therefore names the receipt path, not a section (L1 direction 4, D-89-6).

## Round-89 and round-90 write boundary

Read-only on `LOG.md`, `SCORECARD.md`, `tools/round-89/`, `corpus/lessons/round-89.md`, `corpus/QUALITY.md`, `.ufo/waves/round-89/`. Read `tools/round-89/depth-blocks-v2.py` for the counter only (its `--selftest` and the depth command). No write to any of those.

## Limits of this report

- The independent matrix and the timing are one run each; the REA reruns are two more. The battery itself was run once.
- The entry's `[unknown]` labels (32-bit ELF, LZMA-filtered shared objects, multi-member overlays, carriers outside the four pins) are unmeasured.
- I did not run `tools/round-90/control-cheat-repack.py` directly; its arms are the battery's `cheat_repack` record only.

## Cleanup

Scratch `/fast/scratch/hyaku/kaidoku-r90/ScribeEntry/` is removed after the receipts were copied into `RC` (see final line of the seat transcript).
