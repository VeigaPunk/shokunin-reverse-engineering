# CriticClaims: round-93 attack on the two claim headlines (R93-C1, R93-C2)

Seat: CriticClaims (critic, leaf). Lane `kaidoku-shokunin`, round 93, attempt 1.
Frozen declaration: `92a240521bd1bf2213b75d18d9b176a8dafdc67c` (base `0a2a23da5eb50410a8a0df90c031d9f4fdadb024`).
The lane was not modified. Every run used a scratch clone of the freeze commit (`clone`), a drafted-C2 fixture (`clone-c2`), or a scratch-only serialization patch (`clone-diag`). Receipts and logs are in `w1/CriticClaims/receipts/` and `w1/CriticClaims/logs/`.

## Verdicts

| claim | attack | verdict |
|---|---|---|
| R93-C1 calibration | headline "the fresh-pack arm rejects the five-carrier table (F1) and carrier-read (F2) forgeries while admitting the honest repair" | **FAILS AS FROZEN.** The mechanism claim holds (F1 and F2 are refused on fresh near cells under v3), but the frozen positive command cannot write its own receipt. It crashes on the honest path with rc 1, and the receipt it leaves is truncated. Under the claim's kill rule ("positive not met; any receipt missing") this is a kill at the frozen command. The headline is also wider than the measurement (section C1-3). |
| R93-C2 depth | headline "block 32's criterion column states each rule it asserts" | **FAILS AS DRAFTED.** The frozen after-atom is green on the draft, but the draft breaks the depth clause (no `corpus/knowledge/` citation, a dangling lesson line range). Its intact-input row cites QUALITY 184, which does not state the intact-input rule. The rule appears only in block 32's own column, and no atom checks that column. |

## C1: R93-C1 (calibration)

### C1-1. The before receipts are admissions: holds
Re-derived from the committed receipts with `jq`, not from the prose:
- `pre/r93-do-nothing-r92label-F1.json`: `tool` = `tools/round-92/stop-boundary-repair-battery.py`, `counter_sha256` 63e9df43…, `repair` = `controls/table5-window.py` (sha 3271c1ca…), `label` = `repaired 10 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10`, `met_target` true, `exit` 0, `revision` base-0a2a23da.
- `pre/r93-do-nothing-r92label-F2.json`: the same label and met/exit, `repair` = `controls/carrierread5.py` (sha cc6a07c7…).
- `pre/r93-negative-control-identity-r92label.json` (F3): met false, exit 1. `pre/r93-positive-r92repair-r92label.json`: met true, exit 0.

The admission is real. The label is measured on the public five carriers only.

### C1-2. Frame: "admitted" is the correct measured frame; "forgery" is a mechanism label, and the label does not separate mechanisms
- F1 (`table5-window.py`) derives nothing. It looks up the public carriers' packed images and matches a ±16 window by position. The control's docstring says "pinned" images, but the code packs the five carriers at run time into a TMPDIR cache keyed only by file index, so nothing is pinned.
- F2 (`carrierread5.py`) is the round-92 repair with `upx_green` replaced by membership in the five public packed images.
- Both are counterfeit mechanisms that pass an output-only label. That is what "admitted" means here, and the prose should say so.
- The scratch probe `derive_walk_dverdict.py` (in `w1/CriticClaims/probes/`) is the round-92 repair with its verdict replaced by `upx -d` success on the candidate. It is an open derive-by-walk. Under the frozen v3 counter with the serialization patch (C1-3a below) it gets `repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2`, met True, exit 0 (`receipts/diag-derivewalk-v3-patched-serialization.json`).
- So the fresh arm kills closed lookups and membership verdicts. It does not exclude a repair that derives correct bytes by another oracle. The headline must not say "rejects forgeries" in general. It must say "rejects closed-table and carrier-membership counterfeits".

### C1-3. Blocking defect: the frozen positive command cannot produce its receipt
Frozen command (`claims.json` `frozen_command_positive`), run at the freeze commit in `clone` with `--root .`, `--rev 92a240521…`, the frozen `--expect`, and `--json-out`:
- Result: rc 1. The traceback ends `TypeError: Object of type bytes is not JSON serializable`, "when serializing dict item 'output' … list item 0 … dict item 'fresh_cells'" (`logs/pos-v3-at-freeze.err`). The receipt file is truncated at 706 bytes and is not valid JSON (`receipts/pos-v3-at-freeze.json`).
- Cause: `tools/round-93/stop-boundary-repair-battery-v3.py` line 333 writes `fresh_cells` including each cell's raw `output` bytes, then calls `json.dump` (line 353). `score_fresh_cell` keeps `out` as bytes. A cell that is not refused has bytes output, so the dump always fails on any non-refusing fresh cell: repaired, silent, wrong, or unsafe.
- Same command without `--json-out`: rc 0, `repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2 met True exit 0` (`logs/pos-v3-at-freeze-nojson.out`). The label is right; only the receipt path is broken.
- The F3 frozen run crashes the same way (rc 1, truncated 703-byte receipt). Its met-false is an accident of the crash, not a measurement.
- F1 and F2 wrote valid receipts only because their fresh near cells are refused (no bytes). That is also why the unscored probe `pre/probe-v3-F1-unscored.json` was valid: the failure never ran on a non-refusing cell. The honest path has never produced a receipt under v3.
- Fix options (not applied by me; the counter is frozen): (a) a counter amendment that serializes outputs as sha256 or hex, which changes the counter's pin, so it is a declared freeze amendment or a new claim; or (b) drop `--json-out` and accept no receipt, which fails "any receipt missing". I could not find a non-freeze-breaking path to a valid positive receipt.
- Diagnostic only (scratch `clone-diag`, `json.dump(..., default=hex)`; not a deliverable): positive met True exit 0; F1 met False exit 1 (`repaired 10 of 12; … intact 5 of 6; … fresh-roundtrip 0 of 2`); F2 met False exit 1 (`repaired 10 of 12; … intact 6 of 6; … fresh-roundtrip 0 of 2`); F3 met False exit 1 (`repaired 0 of 12; … far-refused 0 of 12`). So the arms classify correctly once the serialization is fixed. The defect is in the receipt path, not the logic.

### C1-3b. Scope the headline must carry (named limits, with what I measured)
1. **Window.** The battery's near cells are ±7 and its far cells are ±40. Any window from 7 to 39 is indistinguishable under the counter. I measured it: the honest repair with `WINDOW = 39` (`probes/window39.py`) gets met True, exit 0 under the patched serialization (`receipts/diag-window39-v3-patched-serialization.json`). The ±16 cap is the tool's own bound and is not measured by this counter.
2. **Two-green branch.** The tool's own selftest prints "two-green fixture NOT constructible in the swept window (0 greens, spread 0)" (`tools/round-92/upx-stop-boundary-search-repair.py --selftest`, rc 0, `SELFTEST cases=6 failures=0`). Every fresh and public cell has exactly one green value, so "exactly one green" is not exercised by the battery. The entry must not claim that branch.
3. **Derive-by-walk.** Shown above: an open walker with a different oracle passes v3. Output-only.
4. **Mechanism beyond output.** The row's claimed mechanism (`upx -t` decides each candidate) is not measured. Only output is.
5. **Format.** ELF64 little-endian UPX 5.2.0 `--best`, last-block `sz_cpr` tamper only. `mutate_source` raises on non-ELF input, so PE and Mach-O are unmeasured (exit 2 would result; they are not tried).
6. **One fresh source.** `FRESH_SOURCES` has one entry, `/usr/bin/env` (sha a9ba02dc… verified). I grepped `tools/round-80..92` for `/usr/bin/env` as a quoted carrier path: no hits (shebang lines only). It is held out of those tools' carrier lists, but it is one held-out source, not a held-out class.
7. **`fresh-roundtrip` is not an independent oracle.** It is counted only on near cells whose output is `repaired`, meaning output == the fresh pristine pack. Whether `upx -d` of the pristine pack equals the mutated source is a packer property the counter never checks separately. Given `repaired`, `fresh-roundtrip 2 of 2` follows.
8. **The label's `wrong 0; unsafe 0` is public-only.** Fresh `wrong` and `unsafe` classes are never counted (v3 lines 292–300). A fresh cell that is unsafe appears only as `repaired 11 of 12`. Pass/fail is unaffected (met requires `repaired == 12`), but the label understates.
9. **Forgery controls are not pinned.** `claims.json` pins the counter, the imports, and the honest repair (ce1b1769…). It does not pin F1, F2, or F3. Their shas at freeze: table5-window 3271c1ca…, carrierread5 cc6a07c7…, identity_noop 518422b5…. The entry should record these.

### C1-4. Positive-control pin: holds
`tools/round-92/upx-stop-boundary-search-repair.py` is `ce1b1769d56c1d90fcf2ee0800ca508476b45eddc2e8a6d7e2f01aa8d12a70c1` at base `0a2a23da`, at freeze `92a24052`, and at the round-92 landing `a3d3c649` (`git show <rev>:tools/round-92/upx-stop-boundary-search-repair.py | sha256sum`). The round-92 battery `63e9df43…` and the v2 `f6ddb48b…` match the `imports_sha256` pins. The v3 counter at freeze is `60026511…`, and the C2 counter is `34cf6579…`; both match `claims.json`.

### C1-5. Arithmetic: holds
From `pre/probe-v3-F1-unscored.json` (`jq`):
- `scored` 12 = public 10 near + fresh 2 near. ✓
- `far` 12 = public 10 + fresh 2 (fresh near ±7 and far ±40 both at `delta` −7/+7/−40/+40). ✓
- `intact` 5 = public 5 + fresh 0. The fresh identity is false (`fresh_intact` rc 2, `box_after` `['in']`, `identity` false), so the label reads `intact 5 of 6`. ✓
- `repaired` 10 = public 10 + fresh 0; `refused` 2 = fresh near; `fresh_far_refused` 2; `fresh_roundtrip` 0. ✓
- Label `repaired 10 of 12; wrong 0; unsafe 0; intact 5 of 6; far-refused 12 of 12; fresh-roundtrip 0 of 2`, met false, exit 1. ✓
The frozen target arithmetic (12, 12, 6, 12, 2) matches the sum of public and fresh counts.

### C1-6. Kill rule: fails as frozen
The kill rule has three triggers: "positive not met", "any receipt missing", and "pin differs". The first two trigger at the frozen command (C1-3). The pins do not differ (C1-4).

## C2: R93-C2 (depth)

### C2-1. Keyword atoms frozen before data: holds, with a qualifier
- `git show 92a240521 --stat` lists `manifests/block31-before.json`, `manifests/block32-after.json`, `tools/round-93/craft-citation-semantic.py`, `claims.json`, and the before receipt, all in the freeze commit (committed 10:45:21).
- Manifest sha256s match the pins: block31-before `4792fca4…`, block32-after `a28d841f…`. The counter `34cf6579…` matches.
- Working-tree mtimes: the manifests are 10:43:01, the freeze is 10:45:21, and the drafts are 10:47:49. The keywords existed before the drafts. That supports "pre-data" for the keyword lists.
- Qualifier: the after-manifest's keywords were written against the existing QUALITY text. The intact-row keywords are satisfied by row 184 (see C2-3), so the keyword set was frozen before the draft, not before the citation choice.

### C2-2. Could block 32 pass the atoms while row 3 of block 31 stays miscited, and is that honest? History: holds; the fix claim: fails
- The before-manifest on block 31 is exit 1 at base (`receipts/c2-before-at-base.json`), exit 1 at freeze (`receipts/c2-before-at-freeze.json`), and exit 1 on the drafted worktree (`receipts/c2-before-drafted-worktree.json`). Block 31 stays red, which is honest history.
- But block 31 row 3 still cites QUALITY 169, and block 31 carries no supersession pointer. A reader following that row is still misled. The minimal honest step is a one-line pointer outside the table ("row 3 superseded by block 32"). It does not change the before atom (the marker, shape, and row keywords stay the same). The entry should name this or add it, not leave block 31 silent.

### C2-3. Is the before red the same atom D-91-3 named? Yes, and the after atom drops the discriminating phrase
- The before red is `row 'intact input refused by mistake': QUALITY 169 lacks ['never refuse an intact input', "packer's verdict"]`. This is the same atom D-91-3 named in the spot-check (`corpus/lessons/round-92-verifier-spotcheck.md` §6 item 5, line 74). Not dressed up.
- The after-manifest's intact row uses `["exactly one candidate", "packer's own verdict"]`. The phrase "never refuse an intact input" is gone. Both remaining phrases are in QUALITY 184.
- I probed QUALITY row texts with Python (`w1/CriticClaims/logs`, probe output recorded in this report):
  - row 184 contains "exactly one candidate" and "packer's own verdict". It does not contain "intact", "never refuse", or "return the input byte-identical".
  - row 178 contains "return the input byte-identical" and "rc 2", and its text says "unless `upx -t` on the input is green, in which case return the input byte-identical". It is the row that states the intact-input branch, but the frozen intact keywords do not point at it.
  - no QUALITY row before 188 contains "never refuse an intact input".
- So the frozen after-manifest, read as a constraint, forces the intact row's citation onto 184, which is the one-green search rule. The rule "never refuse an intact input" is stated only in block 32's own criterion column, and no atom checks that column.

### C2-4. Gameability: a criterion containing the keywords without stating the rule
- The atoms are substring tests on the cited QUALITY row (`craft-citation-semantic.py` line 160: `k not in qrow`). They do not parse the cited text, do not check the block's criterion cell, and do not check that the cited row states the row's rule.
- Demonstrated on the drafted block 32 (`clone-c2`, worktree): the after-manifest returns exit 0 (`receipts/c2-after-drafted-worktree.json`, `checked` row 3 cites 184 with `missing_keywords: []`) while 184 does not state the intact-input rule.
- Stuffed-row fixture (`root-stuff`, Row 188 text repeated with "states the rule the row asserts" and "semantic atom" prefixed): the after-manifest exits 0 (`receipts/c2-after-drafted-patched.json` is the patched run; the stuffed run exit 0 is in the logs). Containment alone is green.
- Residual the entry must name: "the after atoms check that the cited row contains the frozen keywords. They do not check that the cited row states the block's rule, and they do not read the criterion cell."

### C2-5. Freeze-integrity: the after-manifest does not bind Row 188's bytes
- The after-manifest's row 4 keywords are "states the rule the row asserts" and "semantic atom". The row 188 draft contains both (`row188-draft-text.txt`, the extracted row). Its sha256 is `3070b5b97cfa9b2f478e75070f294481128fd4eeb63bb49c7ab65d9a535ee9b2`.
- The manifest pins keywords, not bytes. A reworded Row 188 that keeps those two substrings passes. The stuffed fixture shows it. The after receipt records only `missing_keywords`, not the row's sha.
- Minimal wording lock: the landing commit records `sha256` of the extracted Row 188 text (`_quality_row(…,188)`) in the knowledge entry and cites it from the after receipt. Land the draft byte-exact (sha `3070b5b9…`) or re-record the sha in the same commit as the receipt. A reword after the receipt is a new receipt.

### C2-6. The drafted block 32 fails the depth clause
- `tools/round-89/depth-blocks-v2.py --root . --worktree --expect-blocks 32` (`clone-c2`, drafted, as-is): exit 1, `blocks 32 resolved 31 expect 32 unresolved 1`. Unresolved: `{"block":32,"problems":["no-citation"]}`. The v2 resolver accepts only `corpus/knowledge/` citations, and the draft has none.
- `tools/round-91/depth-blocks-v3.py --expect-blocks 32`: exit 1, same unresolved block 32, `required_shape` true, `table_rows` 4.
- Also, the draft's lesson pointer `corpus/lessons/round-92-verifier-spotcheck.md:96-100` is dangling. The file has 75 lines, so the range is empty (`wc -l`, `sed -n 96,100p | wc -c` → 0). No counter checks non-knowledge paths or line ranges, so no counter catches it. The draft also calls D-91-3 "§5". The lesson section is §6 item 5 (line 74); §5 is trend verdicts.
- Patched (scratch, `clone-c2`): Refs changed to `corpus/lessons/round-92-verifier-spotcheck.md:74` and `corpus/knowledge/2026-11-05-r92-stop-boundary-repair.md:16` (line 16 states "exactly one green value … write that output, rc 0"), and "§5" changed to "§6 item 5". Result: after-manifest exit 0; depth v2 `blocks 32 resolved 32 expect 32 unresolved 0 met=True exit=0`; depth v3 `… required-shaped 2/2 … met=True exit=0`. The patched draft is in `drafts-validated/SKILL-drafted-patched.md`.

### C2-7. Selftest and depth at freeze
- `craft-citation-semantic.py --selftest --work <scratch>`: `SELFTEST cases=10 failures=0`, exit 0 (`logs/c2-selftest.log`). The keyword-miss case is the prose control.
- Depth at freeze with `--expect-blocks 31`: v2 exit 0 (`blocks 31 resolved 31 … met=True`), v3 exit 0 (`required-shaped 1/1`).

## What the L1 must change before landing (routing, not applied by me)
1. **C1:** the positive receipt cannot be written under the frozen counter. Decide between a declared counter amendment (new pin, new claim) and an honest stop for C1 this round. Do not land the C1 headline on the current counter.
2. **C1 headline scope:** "rejects closed-table and carrier-membership counterfeits (F1, F2) for ELF64-LE UPX 5.2.0 `--best` last-block ±7 tamper, one held-out fresh source (`/usr/bin/env`), near ±7 and far ±40; does not exclude a derive-by-walk with a different oracle, any window in 7–39, the two-green branch (unexercised), or non-ELF formats; `fresh-roundtrip` is not independent; `wrong`/`unsafe` on the label are public-only."
3. **C2:** the drafted block 32 fails the depth clause as drafted. Add the corpus/knowledge citation and fix the lesson line selector and section, as in C2-6.
4. **C2 row 3:** either (a) cite a row that states the intact-input branch (Row 188 with "never refuse an intact input" and the two frozen phrases, cited from row 3), or (b) disclose in the entry that row 3 cites 184, which states the one-green search rule and not the intact-input branch, and that the intact rule is stated only in block 32's column.
5. **C2 Row 188:** record its sha256 in the entry and receipt (C2-5).

## Side checks
- s318 draft (`corpus/lessons` not touched; `l1/drafts/s318-draft.md`): `curl -fsSL https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_unix.cpp` → sha256 `bf83c4133c27d39433db63bf604daf577d429d734c542d29c0b9cc8ed229642e` (matches the draft); lines 476 (`unpackExtent`), 496 (bound), 609 (`unpack`), 681 (bound) match the draft's citations. Not an item of this seat; recorded for the integrator.

## Commands, exit codes and receipts
Scratch: `/fast/scratch/hyaku/kaidoku-r93/CriticClaims` (removed before yield). Every counter ran with `-I -B`. No counter ran against the lane root.
- `git show 92a240521:tools/round-93/stop-boundary-repair-battery-v3.py | sha256sum` → `60026511…` (pin). Same for `craft-citation-semantic.py` (`34cf6579…`), both manifests (`4792fca4…`, `a28d841f…`), and the honest tool at `0a2a23da`, `92a24052`, `a3d3c649` (`ce1b1769…`).
- Frozen positive, json-out, at freeze: `python3 -I -B tools/round-93/stop-boundary-repair-battery-v3.py --root . --repair-cmd tools/round-92/upx-stop-boundary-search-repair.py --work <s>/work/pos --rev 92a240521… --expect '<frozen>' --json-out <r>` → rc 1 (`TypeError: bytes not JSON serializable`); receipt 706 bytes, invalid JSON. (`receipts/pos-v3-at-freeze.json`, `logs/pos-v3-at-freeze.err`)
- Same without `--json-out` → rc 0, met True. (`logs/pos-v3-at-freeze-nojson.out`)
- F1, F2 frozen → rc 1, met False, valid receipts. (`receipts/F1-v3-at-freeze.json`, `receipts/F2-v3-at-freeze.json`)
- F3 frozen → rc 1 crash, receipt 703 bytes invalid. (`receipts/F3-v3-at-freeze.json`)
- Diagnostic serialization-patched (`clone-diag`): pos rc 0 met True; F1 rc 1 met False; F2 rc 1 met False; F3 rc 1 met False; derive-walk rc 0 met True; window39 rc 0 met True. (`receipts/diag-*-v3-patched-serialization.json`)
- Honest tool selftest `--selftest` → rc 0, `SELFTEST cases=6 failures=0`; two-green fixture not constructible. (`logs/r92-tool-selftest.log`)
- C2 before base / freeze / drafted: rc 1 each (`receipts/c2-before-*.json`). After at freeze: rc 1 (block 32 missing, `receipts/c2-after-at-freeze.json`). After drafted as-is: rc 0 (`receipts/c2-after-drafted-worktree.json`).
- Depth drafted as-is: v2 rc 1 (`resolved 31 … unresolved 1`, `receipts/depth-v2-drafted.json`), v3 rc 1 (`receipts/depth-v3-drafted.json`). Patched draft: after rc 0 (`receipts/c2-after-drafted-patched.json`), v2 rc 0, v3 rc 0 (`receipts/depth-*-drafted-patched.json`).
- Freeze depth `--expect-blocks 31`: v2 rc 0, v3 rc 0 (`receipts/depth-*-freeze-31.json`).
- Selftest C2 → rc 0, `SELFTEST cases=10 failures=0` (`logs/c2-selftest.log`).

## Files written (all in the seat directory)
- `.ufo/waves/round-93/w1/CriticClaims.md` (this report)
- `.ufo/waves/round-93/w1/CriticClaims/CriticClaims.md` (copy)
- `.ufo/waves/round-93/w1/CriticClaims/receipts/` (C1 and C2 receipts above)
- `.ufo/waves/round-93/w1/CriticClaims/logs/` (run logs, rc.txt)
- `.ufo/waves/round-93/w1/CriticClaims/probes/` (`derive_walk_dverdict.py`, `window39.py`, `v3-patched-serialization-DIAGNOSTIC-ONLY.py`, `p_unix.cpp.v5.2.0` with sha and quoted lines)
- `.ufo/waves/round-93/w1/CriticClaims/drafts-validated/` (`SKILL-drafted-patched.md`, `QUALITY-with-row188.md`, `row188-draft-text.txt`)

## Tools installed or updated
None.

## Lane state
Read-only. The lane has untracked `corpus/lessons/round-93.md` and round-93 wave directories created by other seats or the L1; I did not create them. An untracked `tools/round-93/__pycache__/craft-citation-semantic.cpython-314.pyc` appeared after 10:40. All my counter runs used `-B` and scratch roots, so I did not write it.
