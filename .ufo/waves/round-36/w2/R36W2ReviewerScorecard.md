# R36W2ReviewerScorecard — wave-2 falsification of the SCORECARD.md / SHONEN.md landing

Seat: R36W2ReviewerScorecard (leaf, no subagents). Reviewed diff: `git diff cab59f221fe19726b5692bfa4d9a9679e96b8a73 01a44dbf45913a1bdcabbbfb85b7bb9d232cb930 -- SCORECARD.md SHONEN.md` (SCORECARD.md +18/−2, SHONEN.md +1/−1; nothing else in these two files changed). Lane HEAD at review time was `6f2ba761` (wave-2 dispatch only: adds `.ufo/waves/round-36/w1-results.json`, `w1/R36ReviewerQualityBar.md`, `w2-*` files — no SCORECARD/SHONEN/receipt changes after the tip), so every tip check below holds at `01a44dbf` and at HEAD.

**Verdict: no falsification found.** Every before/after value, command, measured-at revision and pointer in the round-36 section, the restated coverage row, the new capability row and SHONEN box 4 matches the committed receipts and the observed repo state; both frozen counters additionally re-run green at the reviewed tip. One minor pointer imprecision in the planned line and three observations, none blocking.

## Method

- Read `plans/round-36-claims.md` (frozen predicates P36-C1/P36-C2, kill rules) and `corpus/lessons/round-36.md`; read `AXES.md` §Capabilities (fleet root `/home/vgpnk/Projects/shokunin/AXES.md:56-66` — the lane has no AXES.md; the SCORECARD reference resolves there).
- Read both counters (`tools/round-36/c1-counter.py`, `c2-counter.py`) to learn the observables before trusting any receipt field.
- Checked all 7 control receipts (`.json` + `.out`), both C2 after-receipts, the C1 after-receipt, and the raw per-carrier envelopes in `corpus/evidence/round-36/c1/K{1..4}/` at `01a44dbf` via `git show`.
- Re-ran both frozen counters at `01a44dbf` (read-only; `--json-out` into my scratch; `HYAKU_SCRATCH` pointed at my seat dir). Results embedded below.
- Verified PROVINCE/README/SOURCES/QUALITY surfaces cited by the rows at `01a44dbf` via `git show` + grep; fetched the S108 source URL once into scratch and confirmed sha256 `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287` equals the digest recorded in the S108 row before reading its lines.

## Verification matrix

| # | Checked item | Result | Evidence |
|---|---|---|---|
| 1 | Restated coverage row `SCORECARD.md:23` — "124/124 knowledge files mapped after the round-36 landing" | **match** | My C2 rerun at `01a44dbf`: `command_a {knowledge_files: 124, mapped: 124}`; both new entries have `## Coverage map` rows (`corpus/README.md:195-196`) and capability rows (`README.md:89-90`); `git diff --name-status cab59f22 01a44dbf -- corpus/knowledge/` shows exactly two `A` entries, the two named (`2026-10-26-r36-sasquatch-squashfs-recursion.md`, `2026-10-26-unblob-sasquatch-dependency.md`) plus one `M` (r34b corrections, not an add) |
| 2 | Coverage row — "122/122 at `cab59f22…`, round 36 recount" | **match** | `controls/ctl-c2-0-do-nothing.json` `observed.command_a {knowledge_files: 122, mapped: 122}`; raw `git ls-tree` count at base is 123 including `corpus/knowledge/.gitkeep` — command A counts `.md` files only (`c2-counter.py` command_a), so 122 is the correct observable |
| 3 | Coverage row — historical 116/116 @ `c369242f`, 109/109 @ `ebe2cb4a`, 78/78 @ `3395b6d`, 107/107 @ `7ef837a4` | **consistent** | Raw `.md` counts at those revs are 117/110/79/108 — exactly command-A count +1 (`.gitkeep`) at every rev checked, so the restated numbers are consistent with the same observable. Mapped-half at historical revs not recomputed (residual gap R1) |
| 4 | Capability row `SCORECARD.md:627` — pointers resolve at tip | **match** | `git cat-file -e 01a44dbf:<path>` OK for `corpus/evidence/round-36/c1/`, `tools/round-36/c1-run.sh`, `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md` |
| 5 | Capability row — "official sasquatch 4.5.1 binary on PATH" | **receipt-backed** | `K1/after-run.json`: `sasquatch /home/vgpnk/.local/bin/sasquatch`, `sasquatch_sha256 ad02d27a…4c774754` = the official onekey-sec deb member digest recorded in SOURCES S107 (`corpus/SOURCES.md:113`), `sasquatch_version "unsquashfs version 4.5.1 (2022/03/17)"`, `rea rea-agents@6.5.0`, `exit 0` |
| 6 | Capability row — "publishes every regular file … without it … publishes no member" | **match (member sense)** | `K1/after.json` publishes exactly the 3 oracle files, sha256-identical to `K1/oracle.tsv` (README.txt `88dc952a…`, etc/config.ini `bf53724a…`, payload.bin `5b61b326…`); `K1/before.json`: 0 files, gap `missing-extractor-dependency` deps `["sasquatch"]`. K3/K4: after hits 2130/2130 = oracle_files, before hits 0 + same gap. Nuance → observation O2 |
| 7 | Capability row — carrier provenance | **match** | `carriers.json` K3 sha256 `b644d034…c35f29fb`, K4 `8efcec73…9efe1c2` = the GitHub release digests recorded in SOURCES S109 (`corpus/SOURCES.md:115`); `K1/after-run.json carrier_sha256` = `carriers.json` K1 |
| 8 | AXES §Capabilities: "rows enter only through a round that demonstrates the capability running" | **satisfied with a timing note** | Demonstration is committed at the tip: per-carrier `after.json`/`after-run.json` + `before.json`, and wave-1 reports `R36ExecReproK{1..4}.md` etc. (43 files in `.ufo/waves/round-36/w1/`). The canonical round report `.ufo/reports/round-36/kaidoku.md` does **not** exist at `01a44dbf` nor at HEAD → observation O3 |
| 9 | Round-36 section `SCORECARD.md:3385` — base/freeze/controls hashes | **match** | All three resolve as commits; controls dir byte-unchanged `6a870b92 → 01a44dbf` (`git diff --stat` empty) |
| 10 | "all seven controls exit 1" | **match** | `grep -H 'exit=' controls/*.out` → `CTL-C1-0/1/2 exit=1`, `ctl-c2-0/1/2/3 exit=1` (7/7) |
| 11 | C1 row `SCORECARD.md:3391` — before cell | **match** | `ctl-c1-0-do-nothing.json`: revision = base, `carriers_matched 0`, `met_target false`, every binding false (`coverage_map_row/entry_present/province_core_row/province_core_section/sourced` all `false`) |
| 12 | C1 row — after cell | **match** | `.ufo/waves/round-36/after/c1-at-ffc81341.json`: revision `ffc81341…`, `carriers_matched 4`, `met_target true`, all five boolean bindings true, per-carrier `matched true` ×4, `after_oracle_hits` 3/4/2130/2130 = `oracle_files`, `before_oracle_hits 0` + `before_sasquatch_gap true` ×4, `after/before_evidence_id_ok true` ×4 |
| 13 | C1 row — counting command | **match** | Table command = claims-file command with `<lane>`/`<REV>` placeholders; receipt `argv` confirms the concrete form (`--freeze 790561d4…`, `--pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`) |
| 14 | C2 row `SCORECARD.md:3392` — before cell "3 mismatches, exit 1 at base" | **match** | `ctl-c2-0-do-nothing.json`: `mismatches 3` = O1 `[116,116]` vs `[122,122]` + unresolved `receipts-B/` + unresolved `ScoutSkillPlacement.md` — exactly the three enumerated in the frozen claims file |
| 15 | C2 row — after cell at `d2e46ef5` and `ffc81341` | **match** | `c2/after-at-d2e46ef5.json`: `mismatches 0`, `guards_ok true`, knowledge 122 (entry not yet present — "before C1's entry existed" ✓), adjacent `[97,118]`; `after/c2-at-ffc81341.json`: `mismatches 0`, `guards_ok true`, knowledge 124/124, adjacent `[97,125]`, pointers 38 ≥ base 34 |
| 16 | C2 row — guards semantics | **verified live** | Controls show each guard actually bites: `ctl-c2-2` (delete bad pointers) fails on `pointers_not_fewer false` (32<34); `ctl-c2-3` (substitute other documents) fails on `unrepaired` (base-unresolved pointers not repaired by same-document pointers); `ctl-c2-1` (junk count 999/999) fails on O1 |
| 17 | Owned-scores paragraph `SCORECARD.md:3394` | **match** | 122/122 → 124/124 ✓ (receipts), 17/17 unchanged ✓ (`resolved_rules 17 / rule_blocks 17` at base and tip), 3 → 0 mismatch ✓ |
| 18 | "scored against do-nothing and skip controls … before any claimed data" | **match** | Git history order: `790561d4` (freeze: counters, carriers.json, oracle.tsv ×4, before.json ×4, selftest) → `6a870b92` (7 controls, all exit 1) → `3310d8fa` (after receipts) → `d2e46ef5` → `ffc81341` |
| 19 | Planned line `SCORECARD.md:3396` — QUALITY 77/78 named fixes | **match** | `corpus/QUALITY.md:85-86`: 77 = every-occurrence matching + intended-document repair; 78 = package-root pin + reproduction as provenance — the four named fixes are exactly these |
| 20 | Planned line — "S108 lines 40-50" | **minor imprecision** → finding F1 | See below |
| 21 | Planned line — ".jsc frontier lead recorded in the round-36 lesson" | **match** | `corpus/lessons/round-36.md` "Routed defects" section, R35-D4 bullet |
| 22 | `retired: none. Saturation line and stagnation window unchanged` | **match** | Diff touches none of those lines; last capability row in the table is the round-36 row |
| 23 | SHONEN box 4 `SHONEN.md:12` — `PROVINCE.md:97-125` at `01a44dbf` | **match** | `## Adjacent` heading at `PROVINCE.md:97`; last non-blank line of the section is 125 (126-127 blank, `### Round-4 additions to Core` at 128); matches the C2 receipt's `adjacent_range [97,125]` |
| 24 | Box 4 — "safety refusal at :116-118" | **match** | `PROVINCE.md:116-118` = the "Quality/safety verdicts on findings … never 'is it safe, trustworthy, or licensed for reuse'" refusal |
| 25 | Box 4 — "round-36 dated tooling bullet at :119-125 reconciling the installer line :110-115" | **match** | `PROVINCE.md:110-115` = the "Installing engines … never runs the installer" bullet; `:119-125` = the 2026-10-26 dated tooling bullet citing the 2026-10-19 operator directive and `rea setup`/client-config carve-out |
| 26 | Box 4 — `PROVINCE.md:8-14` versions, `PROVINCE.md:24` v42 | **match** | 8-14 carry the 6.7.0 207/153 and 6.5.0 207/153 pins; line 24 carries "Installed shared REA skill is v42/207 tools" |
| 27 | Box 4 — repaired pointer `.ufo/waves/round-30/w1/ScoutSkillPlacement.md` | **match** | Resolves at tip; contains the `2832c5b3`/`2f18996d` drift content it is cited for (4 hits); rest of the box line byte-identical to the pre-round text |

## Independent re-runs at the reviewed tip (embedded evidence; scratch is deleted)

`python3 -I -B tools/round-36/c2-counter.py --root . --rev 01a44dbf45913a1bdcabbbfb85b7bb9d232cb930 --base cab59f221fe19726b5692bfa4d9a9679e96b8a73` → **exit 0**:
`{"assertion_mismatches": [], "guards_ok": true, "met_target": true, "mismatches": 0, "revision": "01a44dbf…", "unresolved": []}`; observed: `adjacent_range [97,125]`, `command_a {knowledge_files: 124, mapped: 124, resolved_rules: 17, rule_blocks: 17}`, pointers 41 (base 34).

`python3 -I -B tools/round-36/c1-counter.py --root . --rev 01a44dbf45913a1bdcabbbfb85b7bb9d232cb930 --freeze 790561d4e3aca732a434081aa9573ec2fa5fd7d0 --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` → **exit 0**:
`carriers_matched 4`, `met_target true`, `carriers_unchanged true`, bindings all true (`entry_source_ids/opened_source_rows [S107, S108, S109]`).

Note: the committed after-receipts measure `d2e46ef5`/`ffc81341`; the receipts themselves were committed at `01a44dbf` (normal for this lane's flow — receipt records the measurement, commit lands it). My reruns above extend both targets to the reviewed tip, which the committed receipts alone did not cover.

## Findings

**F1 (minor, planned line `SCORECARD.md:3396`)** — "big-endian SquashFS v4 through `sasquatch-v4be` (unblob's `squashfs_v4_be` handler, S108 lines 40-50)". In the S108 source (sha256-verified against the row's recorded digest) the `squashfs_v4_be` handler NAME is defined at `squashfs.py:513-514` (`class SquashFSv4BEHandler` / `NAME = "squashfs_v4_be"`), outside the cited range; lines 40-50 hold the `case Endian.BIG, 4:` selection of `V4BE_EXECUTABLE` (40-41) and the AVM test (48-50). The citation is within S108's declared scope ("names and invokes its SquashFS extractors") but the range does not contain the handler name it is offered as evidence for. Suggest citing `S108 lines 513-514` (handler) alongside `40-41` (selection) when the round-37 plan is written. Not a claim; no receipt affected.

**O2 (observation, capability row `SCORECARD.md:627`)** — "without it REA reports a `missing-extractor-dependency` gap naming sasquatch and publishes no member". True in the SquashFS-member sense (before-case oracle hits 0/2130 on K3/K4), but the K3/K4 before envelopes do publish 2 non-member files each (the carved ELF runtime chunk and the raw `.squashfs_v4_le` image chunk, e.g. `K3/before.json`: `firmware.bin_extract/0-944632.elf64_extract/carved.elf`, `firmware.bin_extract/944632-11454968.squashfs_v4_le`). This whole-file-chunk behavior is disclosed in the frozen claims file and in `corpus/README.md:89`; suggest "publishes no SquashFS member" if the row is ever touched again.

**O3 (observation, AXES §Capabilities timing)** — the capability row entered at `01a44dbf`, but `.ufo/reports/round-36/kaidoku.md` does not exist at `01a44dbf` or at HEAD (`.ufo/reports/` has no round-36 directory; `6f2ba761` adds no report). The passing demonstration is committed (per-carrier receipts + 43 wave-1 reports), and this round's own M36-5 process fix requires the round report to file only after the final lane hash and WAVE-DONE of every wave — i.e. after wave 2. Flagging so the closer lands the round report with the demonstration before the round is scored closed; until then the row rests on wave reports + receipts, not on a round report.

**O4 (observation, provenance scope)** — the C1 verdict cell's "provenance by four independent reproductions" cites `w1/R36ExecReproK{1,2,3,4}.md`. I verified they exist at the tip and spot-read `R36ExecReproK1.md` (committed-receipt byte-identity via `git show | cmp`, `normalized_result.files` set equality true, second-run determinism); a full read of all four is the repro seats' lane, not mine.

## Residual risk and verification gaps

- R1: the mapped-half of the historical counts (116/109/78/107) was not recomputed from the README coverage maps at those revisions; only the file-count half was (consistent +1 `.gitkeep` at every rev checked). These values are carried over from previously reviewed rows.
- R2: I did not re-execute REA `extract-firmware` myself (no re-run of the harness); the member-parity and evidence-id checks above are the counter's own recomputation plus my raw-envelope reads of committed bytes. Per QUALITY 78, provenance rests on the four wave-1 reproductions (O4).
- R3: K2's envelope was checked only through the counter's `matched true`/hits 4/4 fields, not by raw read like K1/K3.

## Bounds and tooling record

- Wrote only this report file in the lane; no VCS mutation (read-only git only); scratch `/fast/scratch/hyaku/kaidoku-r36/R36W2ReviewerScorecard` removed at the end.
- No tools installed or upgraded (operator 2026-10-19 authorization unused). One data fetch: `curl` of the S108 source URL into scratch, digest-verified against the S108 row before use. No pacman transactions.
