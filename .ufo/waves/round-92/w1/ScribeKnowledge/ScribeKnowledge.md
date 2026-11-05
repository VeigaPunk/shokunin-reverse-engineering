# ScribeKnowledge — round 92, wave w1 (scribe; knowledge draft for R92-C1)

Lane: kaidoku (`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`), declaration `11f8606178dfd9e72001b31daf412c5463106a63`, base `73a882712907606eba074377b536c6dd82517e25`.
Deliverables (seat dir): `knowledge-draft.md` (64 lines, not landed), this file.

## What I did

- Read the round-91 entry (house style), `plans/round-92-claims.md` R92-C1 and R92-C2, `claims.json`, `corpus/lessons/round-91.md` Gate/Mistakes/Limits, `corpus/QUALITY.md` rows 165–183 (last rows), and the frozen counters `tools/round-92/stop-boundary-repair-battery.py` and `stop-boundary-battery-v2.py` (read in full scoring logic) and the three `.ufo/waves/round-92/controls/cheat_*.py`.
- Did not fetch S313. `w1/ScoutSource/` is empty at the time of this seat; per the item, the located quote cell is `PENDING-scout` and the re-open fields are `RESULT:<pending L1>`.
- Did not run any candidate or measurement. No candidate tool exists at the declaration commit; the L1 runs the counter.

## Commands run (exit codes)

| command | exit | note |
|---|---|---|
| `git clone --shared -q <lane> <scratch>/clone && git -C <clone> checkout -q 11f8606…` | 0 | rev-parse printed `11f8606178dfd9e72001b31daf412c5463106a63` |
| `python3 -I -B tools/round-92/stop-boundary-repair-battery.py --help` (in clone) | 0 | argparse only; flags `--root --repair-cmd --work --rev --expect --json-out` confirmed |
| `python3 -I -B tools/round-92/stop-boundary-battery-v2.py --help` (in clone) | 0 | argparse only |
| `sha256sum` of the two counters and three cheat wrappers | 0 | see pins below |
| `grep` of `usr/bin/xz` in `tools/round-90/*.py`, `tools/round-91/*.py` | 1 | no match: xz is in no round-90/91 instrument |
| python: hash-table membership vs `pre/c1-control-do-nothing-round91-repair.json` packed sha256 | 0 | four table entries equal the four packed sha256 of the counter's fresh pack; xz not in table |
| `grep -n R87|R88` on `stop-boundary-battery-v2.py` and `claims.json` | 0 | see finding F2 |

Scratch `/fast/scratch/hyaku/kaidoku-r92/ScribeKnowledge/` is removed before yield (see end).

## Pins verified (match `claims.json`)

- `tools/round-92/stop-boundary-repair-battery.py` `63e9df431f5d7aeeca2bd5384efff36b4f2ebedfdc3ee71aaa250287fc9388bc` = `counter_sha256`.
- `tools/round-92/stop-boundary-battery-v2.py` `f6ddb48b4d9cbd460002db68d834f909955e2c7d4e60d7ad85325ef4e66f1874` = `imports_sha256` and C2 `counter_sha256`.
- Cheat wrappers `018ae7ca…`, `4abd318b…`, `7ef7f9e0…` = `instruments_sha256` entries.

## Facts taken from committed receipts (not new measurements)

- C1 do-nothing (round-91 repair, base): `repaired 0 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10`, exit 1, met false.
- C2 v1 counterfeits A, B, C at base: each `refused 8 of 8; unsafe 0; intact 4 of 4`, exit 0, met true (admitted 3 of 3).
- C2 v2 at base: A and B `refused 10 of 10; typed 10; unsafe 0; intact 4 of 5`, exit 1; C `refused 10 of 10; typed 0; unsafe 0; intact 5 of 5`, exit 1; positive control (round-91 tool) `refused 10 of 10; typed 10; unsafe 0; intact 5 of 5`, exit 0, met true.

## Attack: sentences in the draft and what the counter measures

| # | draft sentence (short) | measured by the frozen counter? | disposition |
|---|---|---|---|
| A1 | "five carriers ... `xz-unseen` ... not named in round-91" | the carrier list yes; the "not named" fact is by grep (exit 1, round-90/91 tools) | kept; grep recorded above |
| A2 | "Ten far cells at ±40 are the negative control" | yes (`far`, `far-refused`) | kept |
| A3 | "Input green → identity rc 0" | only the five intact carriers, identity arm | kept, scoped in Limits |
| A4 | "Exactly one green value ... writes output" | only indirectly: `repaired 10 of 10` on near cells | kept; Limits "Uniqueness" scopes it |
| A5 | "the packer's verdict chooses the value" | not measured as a provenance property | kept as declared design; Limits "Oracle" scopes it |
| A6 | "window ±16 is the tool's declared bound, not a property of the format" | no: no cell at 8..16 | kept as declared; Limits "Window" |
| A7 | "frozen counter measures locally confined output (`unsafe`, `wrong`) on its own cells" | yes, on 10 near cells only | scoped in text |
| A8 | "The two oracles differ ... does not grade the tool with its own oracle" | by code reading (counter compares to pristine bytes; tool uses `upx -t`) | kept, labelled as code fact |
| A9 | "Agreement with `upx -t` on intact input is measured by the intact arm" (first draft) | **no** — the intact arm measures identity only | **corrected** in draft |
| A10 | "A repair whose oracle is a five-image table passes the frozen label" (first draft, unmarked) | not run | **marked [INFERENCE, not run]** |
| A11 | "C2 excludes the four-entry table only" (first draft) | "only" not measured | **rewritten**: measured as counterfeit B `intact 4 of 5`; five-entry not excluded |
| A12 | "tool writes no bytes it did not take from that selection" (first draft) | no arm tests byte provenance beyond locality | **deleted**; replaced by "counter measures locality on its own cells" |
| A13 | "Cost: up to 33 upx -t runs; QUALITY 183 bounds work" (first draft) | no cost measured for the round-92 tool; QUALITY 183 concerns the round-91 tool | **corrected**: cost is `RESULT:<pending L1>`; round-91 curve named as round-91 |
| A14 | "Exit 0 means ... the kill rule passes" (first draft) | the counter does not compare its sha256 with the claims pin; the kill rule's pin clause is outside the exit | **corrected**: pin check is a separate L1 step |
| A15 | "packer dependence changes the outcome" | no | marked [INFERENCE] |
| A16 | "Refusal remains the shipped behaviour ..." | the refusal branch is not measured in a clean-merge sense | kept as the claim's kill-rule statement |
| A17 | "S313 supplies the per-block bound and the payload read" | not measured; registry row description + pending re-open | kept as registry description; quote `PENDING-scout` |

Remaining unmeasured sentences in the draft are either marked `[INFERENCE]`, `RESULT:<pending L1>`, or declared-design text. Nothing else in the draft reports a number.

## Findings for the L1 (no claim edited; routed)

- **F1 (window coverage).** The frozen counter's near cells are ±7 and far cells ±40. The declared window `±16` has no measured cell at 8..16. A claim that the window is "repaired" for ±16 would be unmeasured. The L1 should either state "±7 measured; 8..16 not measured" in the entry (as the draft does) or run a separate probe reported beside, not as, the frozen result (QUALITY 34).
- **F2 (freeze-integrity gap, real).** `tools/round-92/stop-boundary-battery-v2.py` loads `tools/round-87/upx-magic-repair.py` and `tools/round-88/upx-chain-repair.py` (`R87`, `R88`, used by `layout()` in both counters). Neither is pinned in `claims.json` `instruments_sha256` or in any receipt field. A change to round-87/88 would move the walk and the cell positions with no pin trip. Per QUALITY 55, 66, 68 this is a defect to report, not to fix inside the frozen claim. Suggested routing: the L1 adds the two sha256 values to the receipt at measurement time (receipt-level, not a claim edit) and records the gap in its report.
- **F3 (naming).** `claims.json` and the draft call the fourth carrier `docker-init`; the frozen counter's carrier id is `dinit` (`/usr/bin/docker-init`). The draft uses the counter's id with the path. No counter change.
- **F4 (`--rev` is a label).** Both counters write `--rev` into the receipt and do not check it against the repository. Only the receipt's own `revision` field carries it. QUALITY 173 requires the L1 to take the receipt at the measured revision; the L1 must not reuse a receipt taken at another commit.
- **F5 (`--rev <measured>` placeholder).** `claims.json` `frozen_command` contains `--rev <measured>`. The draft uses `<measured revision>` and says a receipt still carrying it is M91-2. The L1 substitutes the real revision when running.
- **F6 (kill rule vs exit code).** The claim's kill rule includes a counter-sha256 check that the counter does not perform. The L1 must compare the receipt's `counter_sha256` and `imports`/`instrument_v2_sha256` to `claims.json` before scoring a claim met.
- **F7 (registry line numbers).** The S313 registry row (`corpus/SOURCES.md:229`) cites `line 472 // Consumes b_info header block and …`; the round-91 entry cites `unpackExtent` at line 476 and the bound at 496. The re-open must pin the line numbers from the fetched bytes (grep -n), and the L1 should reconcile the registry row's line reference in its registry change, not in this draft.
- **F8 (quote).** The located quote must be a contiguous ≤25-word run from the served bytes (QUALITY 42). The scout's `ScoutSource.md` is absent; I left `PENDING-scout`. The L1 or scout must supply the quote from the re-open.
- **F9 (five-image table).** The C1 label does not exclude a repair that embeds the five pinned packed images. The C2 label does not exclude a five-entry table either. Both limits are in the draft; neither counter is changed.

## Not done / out of scope for this seat

- No counter run, no candidate build, no S313 fetch (the scout owns it; the L1 re-opens).
- No edit to `corpus/`, `plans/`, `SCORECARD.md`, `LOG.md`, `SOURCES.md` or any lane file. The draft is in the seat directory only; landing is the L1's job.
- No tool installed or upgraded. No sysctl or host-state change. pacman not invoked.
- No `RESULT` numbers written by this seat.

## Cleanup

Seat dir: `knowledge-draft.md`, `ScribeKnowledge.md`. Scratch `/fast/scratch/hyaku/kaidoku-r92/ScribeKnowledge/` (clone and tmp) removed after these files were written.
