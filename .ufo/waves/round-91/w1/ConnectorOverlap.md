# ConnectorOverlap — round 91 sibling-overlap sweep (read-only)

Seat: ConnectorOverlap (connector). Lane: kaidoku-shokunin. Declaration commit `deb2765a55fef0e4e81500a027dfe59951b69e87`. No lane file was edited; the only write is this report plus the copied hit list in `.ufo/waves/round-91/w1/ConnectorOverlap/hits-files.txt`. Scratch was used for grep output only and removed before yield. Tools installed: none. pacman was not run.

## Commands and exit codes

1. `grep -rIl --exclude-dir=.git -F -- <term> /home/vgpnk/Projects/shokunin/*-shokunin/` for the nine terms `stop-boundary`, `stop_boundary`, `chain-stop`, `last block`, `T7-chain`, `upx-stop-boundary`, `stop-boundary-battery`, `depth-blocks-v3`, `record-cells`. Exit 0 for each term. 457 hit files in total (kaidoku-shokunin included, since the glob covers every lane; the kaidoku hits are the lane's own files).
2. `grep -rIn ... -F -- 'chain-stop'` and `grep -rIn -iE 'last-block|stop boundary|stop-boundary|sz_cpr|szcpr|b_info'` over sibling lanes. Exit 0. The `b_info` pattern is noise (`r95b_info` in audio-shokunin's jack-client receipts); it was not used for classification.
3. A wide `grep -rIl -E '\bsz_cpr\b|\bupx\b|b_info'` over all siblings was killed at the 300 s deadline (`bg_4201`, "[Command timed out after 300 seconds]"). Not used.
4. `timeout 240 grep -rIl --exclude-dir=.git -F -e sz_cpr -e szcpr -e 'upx -t' -e 'UPX!' -e upx-break -e upx-chain -e upx-magic -e upx-field` over siblings. Exit 0, 4 files (listed below).
5. `grep -rIl -F -e 'UPX ' -e 'upx ' -e 'last block'` over siblings, `timeout 100`. Exit 0, 280 files. Only the first matching line per file was printed, and the output was truncated at 120 lines, so this sample is not complete.
6. `grep -rIl -F -e 'UPX ' -e 'upx '` over siblings, `timeout 200`. Exit 0, counts per lane only (tsukuroi 12, mado 4, kotodama 2, kumitate 2, tabi 2, kengaku 1, game-dev-3d 1, revenger 2). Not opened individually.
7. For every sibling file that contains `last block` (`grep -rIl -F -- 'last block'`, then `xargs grep -lE 'UPX|upx|sz_cpr|szcpr|b_info|packed'`), 9 files match. Six were opened and match only the generic word `packed`: kagi `round-26/build/ClockS027-artifacts/chlog.body`, kama `round-42/c3/vllm-v0.32.0-kv_cache_utils.py`, kama `round-81/w1/SC02Lesson/vllm-releases.atom`, kengaku `round-50/w1/R50C1MutHostile.md`, kumitate `round-80/w1/K80LabratC2.md`, revenger `round-63/source-snapshots/appnote.txt`. The other three (kagi `round-27/sandboxes/.../chlog.body`, kama `round-42/w1/out/R42C01/vllm-v0.32.0-kv_cache_utils.py`, revenger `corpus/snapshots/APPNOTE.TXT`) appear to be same-named copies of the opened files; they were not opened, so that is unverified. Exit 0.

Scope note: item 5 printed the first match per file for only the first 120 output lines, so I did not read every "last block" hit line. The classification of the "last block" term rests on check 7, which is exhaustive over all "last block" files and has no UPX co-occurrence. The sampled lines were prose, JSON, code fences and table text.

## Hit list by class

### (a) Same class: UPX 5.2.0 packed ELF, last-block `sz_cpr` ±7 (T7-chain-stop-boundary)

**Sibling lanes: none.** No sibling lane contains `stop-boundary`, `stop_boundary`, `T7-chain`, `upx-stop-boundary`, `stop-boundary-battery` or `depth-blocks-v3`. The UPX class vocabulary (`sz_cpr`, `szcpr`, `upx -t`, `UPX!`, `upx-break`, `upx-chain`, `upx-magic`, `upx-field`) appears in exactly four sibling files, none of them class (a) (see section (c)).

**Lane itself** (kaidoku-shokunin, not a sibling; listed so the main agent has the complete class inventory):
- `tools/round-91/upx-stop-boundary-repair.py` — the candidate repair; class `T7-chain-stop-boundary`.
- `tools/round-91/stop-boundary-battery.py` — the frozen counter.
- `corpus/knowledge/2026-11-05-r91-stop-boundary-refusal.md` — the knowledge entry.
- `plans/round-91-claims.md`, `.ufo/waves/round-91/claims.json`, `.ufo/waves/round-91/l1/scores/c1-at-declaration.json`, `.ufo/waves/round-91/l1/scores/c1-regression-at-declaration.json`, `.ufo/waves/round-91/pre/c1-base-round90-repair.json`, `.ufo/waves/round-91/pre/probes/c1-candidate-premeasure-mislabeled-rev.json`, `.ufo/waves/round-91/w1/ExecCandidate/c1-at-declaration-repro.json`, `.ufo/waves/round-91/w1/ExecCandidate/c1-base-repro.json`, `.ufo/waves/round-91/r91-w1-spec.json`, `.ufo/waves/round-91/r91-w1-dispatch.json`, `.ufo/waves/round-91/w1/swarm-registry.json`.
- Lane docs that name the class: `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`, `LOG.md`, `corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/lessons/round-91.md`, `.ufo/waves/round-91/w1/ScribeQuality.md`, `.ufo/waves/round-91/w1/ScribeQuality/rows-draft.md`.
- Adjacent class in the same lane (round-90 interior blocks, not T7): `tools/round-90/upx-break-repair.py`, `corpus/knowledge/2026-11-04-r90-interior-block-szcpr.md`, `.ufo/waves/round-90/w1/ExecMutation/receipts/mut/M01..M08-upx-break-repair.py`, `.ufo/waves/round-90/w1/ScribeEntry/2026-11-04-r90-break-point-szcpr.md`, `.ufo/waves/round-90/w1/ExecDeriveIndep/szcpr_law.py`, `.ufo/waves/round-90/w1/ExecMatrix/matrix.py`, `.ufo/waves/round-90/w1/ReviewerC1/ReviewerC1.md`, `.ufo/waves/round-90/r90-w1-results.json`. These use `chain-stop` and `last block` in the round-90 sense (interior blocks), so they are the nearest neighbour, not an overlap with a sibling.

**Top three class (a) hits read to confirm the class** (all three are in the lane, since no sibling has class (a) material):
1. `tools/round-91/upx-stop-boundary-repair.py:1-123` (`[#723D]`). Defines `CLASS = "T7-chain-stop-boundary"`: packed UPX 5.2.0 `--best` little-endian ELF x86-64, last block before the chain stop carries an in-range `sz_cpr` moved by ±7; `upx -t` answers `compressed data violation`. Rule: when no successor decides the walk, run `upx -t`; green returns the input byte-identical (rc 0), red is a typed refusal (rc 2, no output file). Matches the claim.
2. `tools/round-91/stop-boundary-battery.py:1-83` (`[#337F]`). Four carriers (jq, xxd, libz, docker-init) × directions (−7, +7) = 8 cells, plus 4 intact arms. Label `refused R of C; unsafe U; intact I of 4`. The class definition matches item 1.
3. `corpus/knowledge/2026-11-05-r91-stop-boundary-refusal.md` (`[#B480]`). Same class definition and rule. Measured base (round-90 repair): refused 0/8, unsafe 2, intact 4/4. Declaration (round-91 repair): refused 8/8, unsafe 0, intact 4/4. Limits: packer dependence (`upx 5.2.0`, sha256 `cf2f6e7c…c969`), four carriers, two directions. These are consistent with the claim text and with `pre/c1-base-round90-repair.json`.

I did not re-run the counter; the task was read-only and these reads only confirm class membership.

### (b) Different class

- `lore-shokunin/.ufo/waves/round-88/S1.md:50` — "first chain-stop state" in a holder-ledger / record-disclosure context (non-dict records, holder metadata). Not a binary or UPX class.
- `lore-shokunin/.ufo/waves/round-88/X4.md:52` — "chain-stop cause" in the same holder-ledger context. Not UPX.

### (c) Unrelated use of a term (or a cross-reference that is not the class)

- **`stop-boundary`, `stop_boundary`, `T7-chain`, `upx-stop-boundary`, `stop-boundary-battery`, `depth-blocks-v3`:** no sibling hit. All hits are inside kaidoku-shokunin.
- **`chain-stop`:** sibling hits only in lore-shokunin (class b above). Kaidoku hits (14 files) are the lane's round-90 class.
- **`last block`:** 335 hit files in the first grep (254 in sibling lanes, 81 in kaidoku-shokunin). Per sibling-file count: kengaku-shokunin 93, kumitate-shokunin 26, kama-shokunin 21, souji-shokunin 20, tameshi-shokunin 15, kotodama-shokunin 14, mado-shokunin 14, tsukuroi-shokunin 14, chousa-shokunin 7, kasegi-shokunin 7, game-dev-2d-shokunin 4, revenger-shokunin 4, kake-shokunin 3, lore-shokunin 3, kagi-shokunin 2, kotoba-shokunin 2, mori-shokunin 2, tabi-shokunin 2, game-dev-3d-shokunin 1. The lines I sampled are prose, JSON, code fences and table text. No sibling file containing `last block` co-occurs with a UPX term (check 7); that is the basis for class (c), not a line-by-line read of all 254 files. Example lines: `kengaku-shokunin/.ufo/waves/round-50/w1/R50C1MutHostile.md:315` ("The last block is the point of the seat"); `kumitate-shokunin/.ufo/waves/round-80/w1/K80LabratC2.md:122` (`runs3.txt` last block).
- **`record-cells`:** `tameshi-shokunin/.ufo/waves/round-87/w1/T87CN1.md:25` and `:29`, and `tameshi-shokunin/.ufo/waves/round-87/r87-w1-results.json:34`. These cite kaidoku `tools/round-91/record-cells.py:77-78` (a `git cat-file -t` == `blob` check) as a shared primitive for the round-87 census. Unrelated to the UPX class. **Anomaly to flag:** a round-87 tameshi document cites a round-91 kaidoku path. Either the tameshi file was edited after round 87 or the citation is inaccurate. I did not open the kaidoku file to decide which. The main agent should weigh this when reading the `record-cells` name.
- **`UPX` / `upx` outside the class (checked because they are the tool name):**
  - `revenger-shokunin/reports/round-73/tool-probes.md:83` — a probe row (`upx -t /usr/bin/true`, NotPackedException). Tool probe, not the class.
  - `kotodama-shokunin/.ufo/waves/round-90/w2/stage/ConnectorSiblings/owners-000.txt:130` and `.../linguistic-owners.txt:112` — an owner-table row that cites the kaidoku counter discipline (QUALITY 167: "the counter tests the output — `upx -t`"). Cross-reference to a rule, not to the class.
  - `tameshi-shokunin/.ufo/waves/round-32/w1/CtlRegionDiff.md:276` and `:744` — the string `UPX!` appears inside embedded base85-like data. Incidental.
  - `game-dev-3d-shokunin/reports/round-102/adversary/F6.md:54` — a historical pacman log line that installs `upx`. Not a claim, not relevant to the class.
- **Other `UPX ` / `upx ` prose hits** (tsukuroi 12, mado 4, kumitate 2, kotodama 2, tabi 2, kengaku 1, game-dev-3d 1, revenger 2): counted in check 6 and not opened. None of them matched `sz_cpr`, `szcpr`, `upx -t`, `UPX!` or the `upx-break/chain/magic/field` names (check 4), so none is class (a).

## Verdict

**No sibling lane claims the T7 class.** The class (UPX 5.2.0 packed ELF, last block `sz_cpr` ±7, refused with rc 2) exists only in kaidoku-shokunin, in the round-91 files listed above. The new instrument names (`stop-boundary-battery`, `depth-blocks-v3`, `upx-stop-boundary-repair`, `T7-chain`, `stop_boundary`) appear in no sibling lane. The one shared-name collision is `record-cells`: it appears in tameshi round-87 as a citation to a kaidoku round-91 file, and that citation is the anomaly to check.

Affected axes for the round-91 claims: coverage (no sibling duplicate of R91-C1 found, so no dedupe needed); depth (R91-C2 block 31 is not present in any sibling lane); calibration and freshness are not affected by this sweep.

## Files written

- `.ufo/waves/round-91/w1/ConnectorOverlap.md` (this report)
- `.ufo/waves/round-91/w1/ConnectorOverlap/hits-files.txt` (the 457-path hit list from check 1, copied from scratch)
