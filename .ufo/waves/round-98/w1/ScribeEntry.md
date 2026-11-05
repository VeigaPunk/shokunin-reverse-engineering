# ScribeEntry — round 98 knowledge-entry drafts

Seat: ScribeEntry (scribe). Round 98, attempt 1. Lane `kaidoku-shokunin`. Nothing under `corpus/`,
`tools/round-98/`, `.ufo/waves/round-98/pre/`, `.ufo/waves/round-98/l1/`, `plans/`, `LOG.md`,
`SCORECARD.md` was written; no git mutation anywhere.

## Deliverables (all under `.ufo/waves/round-98/w1/ScribeEntry/`)

| path | content |
|---|---|
| `2026-11-05-r98-pe-upx-tamper-repair.md` | the R98-C1 knowledge-entry draft (frontmatter: S324 + existing S308/S309; the held class; the repair rule; the oracle; the controls and their labels; explicit Still-Frontier limits) |
| `README-draft.md` | the coverage-map row, the `## Knowledge` table row and the `Round-98 frontier note` line, in the style of `corpus/README.md:383-393` |
| `2026-11-05-r98-c2-allowlist-calibration.md` | supplementary draft for R98-C2 (not named in the seat item; round 98 carries two claims and the C1 entry cannot carry C2) |
| `receipts/*.json` | the receipts behind every label below, re-run by this seat in its own scratch |

## Commands run (all executed; exit codes as observed)

Clone: `git clone --shared /home/vgpnk/Projects/shokunin/kaidoku-shokunin $S/clone` then
`git -C $S/clone checkout --detach 72346895a35a74af18151b125934fa0c09fe1e3c`;
`git -C $S/clone rev-parse --show-toplevel` printed `/fast/scratch/hyaku/kaidoku-r98/ScribeEntry/clone`.

| # | command (run in `$S/clone`) | label / result | exit |
|---|---|---|---|
| 1 | `python3 -I -B tools/round-98/pe-upx-tamper-battery.py --repair-cmd tools/round-98/upx-pe-repair.py --work $S/work/c1 --json-out $S/work/c1-receipt.json --rev 72346895a35a74af18151b125934fa0c09fe1e3c` | `recovered 18 of 18; intact 6 of 6; refused 2 of 2; effective 18 of 18 met True` | 0 |
| 2 | same, `--repair-cmd tools/round-98/controls/identity-copy.py` | `recovered 0 of 18; intact 6 of 6; refused 0 of 2; effective 18 of 18 met False` | 1 |
| 3 | same, `--repair-cmd tools/round-87/upx-magic-repair.py` | `recovered 0 of 18; intact 0 of 6; refused 2 of 2; effective 18 of 18 met False` | 1 |
| 4 | `python3 -I -B tools/round-98/allowlist-check.py --counter tools/round-98/stop-boundary-repair-battery-v8.py --rev 72346895… --work $S/work/c2 --json-out $S/work/c2-receipt.json` | `legs passed 4 of 4; public 1; real14 1; stub9 1; extra 1 met True` | 0 |
| 5 | same, `--counter tools/round-97/stop-boundary-repair-battery-v7.py` | `legs passed 1 of 4; public 0; real14 0; stub9 0; extra 1 met False` | 1 |
| 6 | `python3 -I -B tools/round-98/stop-boundary-repair-battery-v8.py --selftest` | `SELFTEST cases=24 failures=0` | 0 |
| 7 | `python3 -I -B tools/round-97/stop-boundary-repair-battery-v7.py --selftest` | `SELFTEST cases=23 failures=0` | 0 |

The five frozen labels above equal the committed pre-side receipts
(`.ufo/waves/round-98/pre/c1-identity-control.json`, `c1-r87-control.json`, `c2-v7-control.json`,
all at base `d0aebc28`, exit 1) and the L1 receipts at the landing commit.
Tool digests at `72346895a`: battery `a34d1253…4feee8`, repair `2fa1102d…1dfa4`,
allowlist-check `c8106aff…5317`, v8 `7a983746…8a83`; `upx --version` = `upx 5.2.0`
(`/usr/bin/upx`, sha256 `cf2f6e7c…c969`); host `python3 3.14.8`. No tool was installed or upgraded.

## Behaviour of the class, as measured by this seat (probes, in the draft entry)

- All six packed carriers carry **exactly one** `UPX!` word, at offset 992 = the PackHeader
  (format byte 9 win32/pe or 36 win64/pe, version 13); the section table is `UPX0`, `UPX1`, `.rsrc`
  (3 sections); `isection[1].rawdataptr` is 1024 on all six, so the gate's first window
  `[960, 1984)` contains 992 on every carrier and the fallback window at `isection[2].rawdataptr`
  (36864…130048) never does.
- The refusal message splits by **architecture**, not by tamper: win32/pe carriers answer
  `CantUnpackException: file is modified/hacked/protected; take care!!!` and win64/pe carriers
  `…: file is possibly modified/hacked/protected; take care!` (all 18 files, rc 1). S324
  lines 3192-3203: the two strings are the `x` / `!x` branches of the x86-stub probe
  (`"\x8b\x1e\x83\xee\xfc\x11\xdb"`, commented x86-only).
- **The repaired PE is byte-identical to the untampered packed file** on all 18 recovered cells and
  all 6 intact cells (repair message lists only `magic@992`, `name0,name1` — never `name2`,
  because the third section is already `.rsrc`).
- **PE unpack is not byte-identical to the original carrier** (same length; 386/390/405/412/974/216
  differing bytes for t32/t64/w32/w64/winhello/fastlist64; `t32` `6b4195e6…` vs unpack `2a300a74…`),
  so the oracle is unpack equivalence, not original bytes — unlike the round-87 ELF class.
- Out-of-population probe (not scored, not a coverage claim): on `t32` alone the same repair
  recovered all three tampers of packs made with `-1`, `--lzma` and `--best --brute`
  (PackHeader also at 992 in each).
- S324 also bounds two frontier clauses: UPX 5.2.0 refuses to *pack* `win64/arm64`
  (line 142) and `.NET` files (line 2209), so ARM64 PE and .NET PE are unreachable for this
  packer rather than merely unmeasured.

## Findings

1. **A corpus entry for round 98 was committed during this wave, not by this seat.**
   `corpus/knowledge/2026-11-05-r98-pe-upx-tamper-repair.md` plus the round-98 `corpus/README.md`
   rows (coverage map, `## Knowledge` table, frontier note) were committed as `9cb930014`
   ("round-98: PE UPX tamper knowledge entry, S324, README map/index/frontier note, QUALITY 198-199,
   capability row; landing receipts"), first visible in the working tree at 18:02-18:03 — before this
   seat's wave directory existed (18:04). The seat item says "do not write into `corpus/`", so I did
   not touch it; my drafts live in the wave directory. Findings 2-6 below are against that committed
   text, which the integrator may want to reconcile with my drafts.
2. **The committed entry states the refusal message as one string**
   (`corpus/knowledge/2026-11-05-r98-pe-upx-tamper-repair.md:16-17`: "the renamed files answer
   `CantUnpackException: file is (possibly) modified/hacked/protected`"). Measured, it is **two**
   strings, split by architecture (see above): the three win32/pe carriers never produce the
   "possibly" wording — they answer `file is modified/hacked/protected; take care!!!`. The split is
   the packer's own x86-stub probe (S324 lines 3192-3203), not a tamper difference. My draft states it.
3. **The committed entry's repair-rule text omits the population's `name2` branch.** The repair renames
   section 2 only when it is neither `.rsrc` nor `UPX2*`; all six carriers are `.rsrc`, so the
   branch is never exercised by the frozen population (no repair message contains `name2`). My draft
   says so.
4. **The `UPX2`-named third section is a real but unmeasured UPX case**, not a hypothetical: S324
   line 2652 writes `"UPX2"` when the original has no resources. None of the six carriers is in that
   shape, so the section-2 rename branch is untested. Named in the draft's Still-Frontier list.
5. **The frozen battery cannot separate the structural PackHeader search from a fixed-offset
   patch**: all six carriers put the PackHeader at offset 992 and `isection[1].rawdataptr` at 1024.
   The repair does search the gate's windows (the recorded offset 992 lies inside `[960, 1984)`), but
   the population does not prove the search is necessary. Named as a limit.
6. **ARM64 PE / .NET PE frontier wording.** The in-tree note lists "ARM64 PE, PE DLLs and .NET"
   as Still Frontier; for UPX 5.2.0 the first and third are pack-time refusals (S324 lines 142,
   2209), i.e. unreachable, not unmeasured. My draft distinguishes the two.
7. **R98-C2's own limits are narrower than a coverage move.** v8 = v7 + the five missing
   allow-list keys + one selftest case (`verify-catches-nine-key-stub`). The widened list is bound
   to the verdict's *current* fourteen keys; a future verdict key would again refuse the public
   run. Round-97 routed defects 3-6 and defect 7 stay open (`plans/round-98-claims.md`).
8. **No host change was needed and none was made.** No sysctl, no pacman transaction, no
   namespace workaround; scratch was `/fast/scratch/hyaku/kaidoku-r98/ScribeEntry` (405 G free on
   `/fast` at 18:05 UTC), removed on exit.

## Known limits of this seat's work

- The drafts are drafts: nothing was filed into `corpus/`, `SCORECARD.md` or `LOG.md`.
- The out-of-population mode probe (`-1`, `--lzma`, `--best --brute` on `t32`) is one carrier and is
  labelled as a probe in the draft, never as coverage.
- The repaired PE is accepted by the packer; whether it runs on Windows is untested (no Windows
  host on this lane) and is stated as such.
