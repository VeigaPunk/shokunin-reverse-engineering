# CriticC1Miss — R28-C1 honest-stop handling (round 28, attempt 2, wave a2w)

Seat KaidokuR28a2.CriticC1Miss, critic, 2026-10-22 18:22Z-18:29Z. Attacked: how the round handles the R28-C1 miss (h09 refused by REA), the committed handling at lane tip `2832c5b3e20d84729bbd7f1b30afc081de9557b5`, and the M28-1 Mistakes row. Read-only on the lane; mutations only in sandbox clone `/fast/scratch/hyaku/kaidoku-r28/seats/a2w/CriticC1Miss/clone`. No REA, no network, no installs.

## Verdict
- Freeze integrity: **holds** (observation). `git diff --stat 87d3dfb6 2832c5b3 -- .ufo/waves/round-28/claims.json tools/round-28/c1-heldout-naming.py corpus/evidence/round-28/c1/carriers.tsv corpus/evidence/round-28/c1/heldout.tsv` printed nothing, exit 0 (18:27Z). `runs.tsv` and `envelopes/h09.json` were touched only by `ca4069a4`. Counter at `2832c5b3`: `runs_ok=60/61 rows_complete=186/187 tally_equal=1 entry_ok=1`, exit 1 (18:27:23Z).
- SCORECARD row (`SCORECARD.md:3139` at `2832c5b3`): **holds**. It says "target missed: honest stop", and the owned axes stay unchanged.
- Knowledge entry wording: **fails** (counterexample in move 8).
- M28-1 captured-by = "none": **fails**. An existing rule applied (see the Mistakes row section).
- QUALITY row 43 "same input check the tool applies": **fails** on one case (see the screen section).

## Forbidden moves, the rule each breaks, and what the counter does
Sandbox runs used `python3 -I -B tools/round-28/c1-heldout-naming.py --root <clone> --rev HEAD`, with each mutation committed at 18:26:26Z.
1. **Re-run h09 with the frozen argv.** M2 added a second h09 row with exit 0: `FAIL h09: 2 call records (need exactly 1)`, `runs_ok=60/61`, exit 1. It breaks the one-call-per-carrier rule in `.ufo/waves/round-28/claims.json:38`. Inference: REA's hex check would refuse the same bytes again.
2. **Link h09 (`solc --link`), run it with `raw` encoding, or swap in another carrier.** The new bytes or argv no longer match the frozen `runtime_sha256` and ARGV, so the counter refuses them (`tools/round-28/c1-heldout-naming.py:172-173,196-199`). This also breaks `corpus/QUALITY.md:44` (#34: a replacement result is reported beside the frozen one and never replaces it; the original target decides) and `corpus/QUALITY.md:14` (#4: a new artifact has a new identity). Such a run MAY appear only as a separately labelled, uncounted probe after the freeze.
3. **Delete h09's refused record.** M1: `FAIL h09: 0 call records (need exactly 1)`, still `60/61`, exit 1. It breaks `corpus/QUALITY.md:28` (#18: execution evidence keeps argv, stdout and exit).
4. **Drop h09 from `carriers.tsv` or `heldout.tsv`.** M3: `PIN pinned input differs from its pin: corpus/evidence/round-28/c1/carriers.tsv`, exit 2. It breaks `corpus/QUALITY.md:43,48` (#33 and #38) and `claims.json:15` (`pin_note`).
5. **Narrow the counter (TARGET 60/186 plus re-pinned lists) and re-emit the tally.** M4 printed `runs_ok=60/60 rows_complete=186/186 tally_equal=1`. The only failure left was `entry absent`, so this edit exits 0 once an entry lands. **This is the strongest counterexample: the counter cannot see a self-edit.** Only `.ufo/waves/round-24/tools/freeze-gate.py` catches it (`INSTRUMENT_REVISED`, commit `defb9b9e`, `disclosed: 0`). But round-28 is already `FLAGGED` at `a2673116` for `INSTRUMENT_UNPINNED` (collect-c1.py) and `INSTRUMENT_UNRESOLVED` (select-heldout.py), so the verdict stays `FLAGGED` and only the code set changes. Catching it therefore needs the `corpus/claim-freezes.tsv` round-28 row checked with `--disclosures`. The move breaks `scripts/hyaku/lane-addendum.md:210` ("Never narrow a target after landing: a miss is an honest stop."), `corpus/QUALITY.md:43` and `corpus/QUALITY.md:44`.
6. **Narrow in prose** ("60/60 runnable carriers", "all valid carriers"). It breaks `lane-addendum.md:210` and `:205-206` (no universal clause unless the counter enumerates it).
7. **Call 60/61 met or near-met, admit the round, or move the coverage score.** It breaks `lane-addendum.md:199-200` ("harmed or unprovable claims are reported, not prettified"), `templates/round-prompt.md:37-40` (every claim verifies) and `corpus/QUALITY.md:44`. The verdict label `rejected-honest-stop` belongs to the outside closure (`scripts/hyaku/closure-prompt.md:79`), not to the lane.
8. **Say REA "did not recover" h09's selector.** This breaks `corpus/QUALITY.md:21` (#11: parsed-and-empty versus excluded) and `:15` (#5). **Observed at `2832c5b3`:** the entry `corpus/knowledge/2026-10-22-r28-evm-heldout-selector-naming.md:35` says "REA recovered 186 of 187 selectors (the missing one is h09's `useIt(uint256)`)", and `:64` says "at a cost of 50 unnamed rows". REA never analyzed h09: its envelope is an `invalid_request` refusal. The tally row for 395c1d44 has `recovered_by_rea: False` with every rule output `None`, and it is the only row with `recovered_by_rea` false (tally.json read at 18:24Z). M4 shows primary `no_name 49` once h09 is removed.
9. **Count the h09 envelope as an exercised run.** It breaks `corpus/QUALITY.md:36` (#26: a typed refusal does not count).
10. **Make `tools/round-28/hex-screen.py` (added at `9db24c9e`, after the freeze) a C1 instrument or add it to `claims.json`.** It breaks `corpus/QUALITY.md:43` (#33). It is hygiene for later freezes, not a re-score.

## Statements the honest report must contain
1. R28-C1 missed its frozen target. At `<tip>` the counter exits 1 with `runs_ok=60/61 rows_complete=186/187 tally_equal=1 entry_ok=1`. Give the command and the revision. The claim is not met and the coverage axis does not move.
2. Cause: REA 6.5.0 refused h09 (`Cr1LibUser.noopt.runtime.hex`, sha256 `f9dc4ccf…6c68`) at input with `invalid_format`, because of `__$a2bad93077572174e8e5044433a5a7d5f3$__` (S086). REA never analyzed this carrier. Cite `envelopes/h09.json` and runs.tsv row h09, exit 1.
3. Both misses have this one cause. The only failing row is `FAIL row 395c1d44: carrier h09 run not valid`, and its lookups are complete (counter output 18:25:09Z).
4. The tally split, in words: REA recovered 186 of 186 selectors on the 60 carriers it ran. The one unrun row is inside primary `no_name 50`, so 49 rows were run but not named and 1 was not run. The frozen tally keeps its field name `recovered_by_rea`, but prose must not call that row unrecovered. Fix entry `:35` and `:64` with a named correction line.
5. Nothing changed after the freeze: claims.json, the counter and both lists are byte-identical from `87d3dfb6` to the tip; there was no re-run, no deletion and no narrowing.
6. Hypotheses are reported as observed, and neither depends on h09 (inference). h09 adds at most one row, so the primary rule's wrong count is at most 1 of 138, about 0.7%, which is under 5%: H1 holds either way. Named is at least 137 of 187, more than half: H2 fails either way.
7. The observed triple (named 137, right 137, wrong 0) is a measurement and not an admitted claim. The M28-1 fix (the screen and row 43) applies to future freezes and does not re-score C1.

## Mistakes row: captured-by is not "none"
The template asks for "the criterion or rule that should have caught it, or `none`" (`templates/round-prompt.md:70-71`). A rule existed, and so did the lane's own knowledge:
- The rule: `scripts/hyaku/lane-addendum.md:203-204` says "Size it to what one round can land and verify". A 61/61 target was sized without checking that each carrier was admissible to the tool. The freeze probed 1 of 61 carriers (`claims.json:20`, VaultA only).
- The knowledge: `corpus/knowledge/2026-10-13-r3-evm-interface.md:88-90` recorded this exact refusal text in round 3. The carrier's origin record `.ufo/waves/arc3-loop1-round3/claims/c1/CR-1/recon/SUMMARY.md:12-18` lists five probed carriers, Cr1LibUser is not among them, and `CR-1/probe/` (13 files) holds no Cr1LibUser envelope. So the lane never had a successful REA run on h09 (observation).
- `tools/round-28/select-heldout.py:5-19` admits any ABI with a paired runtime and has no admissibility filter.

Proposed row:

| id | class | evidence pointer | captured-by | fix and how it was shown able to fail |
|---|---|---|---|---|
| M28-1 | a frozen carrier list held a carrier REA refuses on input format, so the frozen target 61/61 was unreachable before any run | `runs.tsv` row h09, exit 1; `envelopes/h09.json` `invalid_format`; `Cr1LibUser.noopt.runtime.hex` holds `__$a2bad930…$__`; `arc3-loop1-round3/.../CR-1/recon/SUMMARY.md:12-18` (never probed) | `scripts/hyaku/lane-addendum.md:203-204` claim sizing ("Size it to what one round can land and verify"), unenforced; the input rule was already in `corpus/knowledge/2026-10-13-r3-evm-interface.md:88-90`; no QUALITY row covered inputs (rows 38-40 cover instruments only) | QUALITY row 43 and `tools/round-28/hex-screen.py`. Red: `FAIL h09 … placeholders=1`, `carriers=61 fail=1`, exit 1. Green on the same list without h09: `carriers=60 fail=0`, exit 0 (18:25:55Z). The next EVM freeze commits the screen's exit-0 output |

## Screen and QUALITY row 43: smallest corrections
- **`0X` prefix.** REA strips the prefix with `/^0x/i` (`rea-agents` 6.5.0 `dist/evm/EvmBytecodeCarrier.js:17`, sha256 `4984eb8e…f83f`). The screen's `(?:0x)?` is case-sensitive. On a scratch file `0X6001600101` the screen printed `FAIL u1 upper.hex placeholders=0` (exit 1), while REA's regex run in node accepted it (`rea_regex upper= true`). That is a false refusal (observation from code; REA itself was not run). Fix: `(?:0[xX])?`.
- **Unbound bytes.** The screen reads working-tree bytes and never compares them with `carriers.tsv` column 4 (`runtime_sha256`), so its committed output is not tied to the frozen bytes. Fix: refuse a carrier when sha256(bytes) differs from column 4.
- **Empty file.** Both regexes accept an empty file (`empty= true`; the screen passed `e1`). Whether REA refuses empty bytes later in the pipeline is unknown.

## Artifacts (`/fast/scratch/hyaku/kaidoku-r28/seats/a2w/CriticC1Miss/`)
- `counter-a2673116.txt` abe04add0f066d94f4e401637c36edcec73fa1e45f6fb1bdff8e5c538c1d0b69
- `counter-2832c5b3.txt` 598c5b0c00bb6ebb422ecce481fd2b8280e11747fb95144dcbdcd631226fb5f4
- `green.txt` 7abfcf161b84ff0f1dd9f06cfcb5ef4c31c5c001c4e7822cef82bf3081db4a8b; `carriers-minus-h09.tsv` 4a8407bd317af89699afb8776f88e50c10d58c9a1d1aa327f363d5130c6c0105
- `fake.txt` 0827d6a7671812e30fb84d7963bb88ddfb30c12eac9ad4b8e4861bc7f4e0b228; `fake.tsv` d1d131b60fbb86e57729e94f14d7195da731e688475b2c259aa70250c8999ff0; `rea-regex.txt` dbf4e72d1216925e82b63b1b1f4d7109fd3c5a501c15b32f153d104e5351f2bf
- `fg-HEAD.json` (M4 sandbox) e7ae94841eb7ac75fbeab5f04e3b0c61290847e34ea0bb8ab0042da5cfa08d6e; `fg-a267311678309fd17772407e8afa122ec3219289.json` ec69e6e40935d3294ed4fe987ebfd79b403eb919eacc2b690cc9c99ebd185f99
- `clone/` sandbox, branch `sandbox`, M4 tip `6c374aa7` (M1 and M2 were reset; their output is quoted above).
- Lane `tools/round-28/hex-screen.py` read at sha256 99c312b5ac3a6d5fd97016d5a55dcf6c6f49fb414529e21c56ea9ecda4eccbec.

Tooling: no installs or updates. Checks for the L1 to run: the counter at the final tip; `freeze-gate.py --disclosures corpus/claim-freezes.tsv` for round-28; a grep of the entry and README for "recovered 186" and "50 unnamed" after the correction.
