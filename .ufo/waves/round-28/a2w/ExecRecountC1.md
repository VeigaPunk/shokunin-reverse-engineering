# R28-C1 counter re-run (seat ExecRecountC1)

UTC window: 2026-10-22T18:23Z to 2026-10-22T18:25Z. Lane: /home/vgpnk/Projects/shokunin/kaidoku-shokunin.
Lane tip under test: a267311678309fd17772407e8afa122ec3219289 (main). Lane was not modified; every check ran in a sandbox clone.

## Files changed

Only this report: /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-28/a2w/ExecRecountC1.md. No other lane file touched; no git write, commit, or index change in the lane.

## Commands and exit codes

1. `git clone -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin /fast/scratch/hyaku/kaidoku-r28/seats/a2w/ExecRecountC1/clone` -> exit 0; clone HEAD a267311678309fd17772407e8afa122ec3219289, clean tree.
2. `python3 -I -B tools/round-28/c1-heldout-naming.py --root <clone> --rev a267311678309fd17772407e8afa122ec3219289` -> exit 1 (reproducible: a second run gave the same bytes and exit 1).
3. `python3 -I -B tools/round-28/c1-heldout-naming.py --selftest` -> exit 0.
4. `python3 -I -B tools/round-28/c1-heldout-naming.py --root <clone> --emit-tally` -> exit 0 (stdout is the recomputed tally JSON; stderr carries one FAIL line for h09, expected because the working tree copy of runs.tsv still records the h09 refusal).

## Full counter stdout (run 2, verbatim)

```
FAIL h09: exit 1; operation differs; provider version differs; subject digest is not the carrier; subject path is not the carrier; envelope does not parse as an REA EVM envelope
FAIL row 395c1d44: carrier h09 run not valid
FAIL entry absent
primary rule openchain_sole_unfiltered_args_consistent: named 137, right 137, wrong 0, no_name 50
runs_ok=60/61 rows_complete=186/187 tally_equal=1 entry_ok=0
```

Exit code 1. stderr was empty (sha256 e3b0c442...b855, the empty-file hash).

The same run with `--root` pointed at the lane itself instead of the clone produced byte-identical output and exit 1 (observation: the counter reads only committed bytes through `git show`, so clone and lane agree).

## Selftest summary

Exit 0. `selftest cases=21 failures=0`. All 21 cases printed `ok` (green exit=0 want=0; the 18 red mutation cases exit=1 want=1; the red-pin-refusal case exit=2 want=2):

```
ok green-identical-4byte-bodies-across-selectors exit=0 want=0
ok red-early-run exit=1 want=1
ok red-pkg-sha exit=1 want=1
ok red-pkg-version exit=1 want=1
ok red-argv exit=1 want=1
ok red-exit exit=1 want=1
ok red-envelope-of-other-carrier exit=1 want=1
ok red-provider exit=1 want=1
ok red-envelope-sha exit=1 want=1
ok red-missing-openchain exit=1 want=1
ok red-lookup-status exit=1 want=1
ok red-lookup-early exit=1 want=1
ok red-lookup-sha exit=1 want=1
ok red-lookup-url exit=1 want=1
ok red-tally-edited exit=1 want=1
ok red-entry-wrong-triple exit=1 want=1
ok red-entry-old-row exit=1 want=1
ok red-row-not-in-gate exit=1 want=1
ok red-row-status exit=1 want=1
ok red-pin-refusal exit=2 want=2
selftest cases=21 failures=0
```

## Tally diff result

Committed tally: `git show a2673116:corpus/evidence/round-28/c1/tally.json`. Recomputed tally: `--emit-tally` from the clean clone tree.

- Byte diff: `diff -u committed-tally.json emit-tally.json` -> exit 0, zero lines of difference.
- sha256 of both files: 655d8d648ecd46fa8ae71aca4fba7f57ba0fabc7dbd122e55bd4b6d0f1d148a5 (identical).
- Python structural compare of the two JSON documents: `json_equal= True`; top-level keys `rows`, `tally`, `wrong_names` on both sides.
- The counter's own tally_equal=1 agrees.

## Findings, labelled

- Observation: at a2673116 the counter scores runs_ok=60/61, rows_complete=186/187, tally_equal=1, entry_ok=0, so exit 1. The frozen target 61/61 and 187/187 is missed; the miss is the known h09 refusal.
- Observation: the h09 envelope at that revision is a REA error document, not an EVM envelope. Its `details.issues[0].message` reads "Hex carrier requires complete hexadecimal byte pairs, an optional 0x prefix and outer ASCII whitespace; interior separators are invalid." This is the recorded cause of the exit 1 REA refusal on that carrier.
- Observation: the only held-out selector on carrier h09 is 395c1d44; it is the single row counted as incomplete, which is why rows_complete is 186 of 187.
- Observation: the primary rule `openchain_sole_unfiltered_args_consistent` names 137 selectors, all 137 right, 0 wrong, 50 with no name.
- Observation: the knowledge entry `corpus/knowledge/2026-10-22-r28-evm-heldout-selector-naming.md` does not exist at revision a2673116; it exists only as an uncommitted lane working-tree file. Hence `FAIL entry absent` and entry_ok=0.
- Observation (sandbox preview, not a lane claim): copying the four pending lane working-tree files (entry, lesson round-28.md, SOURCES.md, QUALITY.md) into the sandbox clone and committing them there yields entry_ok=1 with runs_ok=60/61, rows_complete=186/187, tally_equal=1, still exit 1 because of h09. Sandbox commit 8a66a02efc2360e588d46629c815be3b4d973b29; it exists only in the sandbox clone.
- Inference: after the entry and the accompanying SOURCES and lesson rows are committed, entry_ok will be 1 and the only remaining FAIL line will be the h09 carrier and its one selector. No other counter input is missing at the lane tip.

## Risks

- The frozen target for R28-C1 cannot be met on this data: 61/61 runs and 187/187 rows are unreachable while REA refuses the h09 runtime file. The round should report that miss rather than relax the target.
- The counter's exit code stays 1 for any lane tip until the h09 run itself becomes valid. The L1 should expect exit 1 and must not treat it as a counter bug.
- The tally is stable and reproducible; the tally_equal=1 result is not at risk from re-running.

## Blockers

None for this assignment.

## Artifacts (all under /fast/scratch/hyaku/kaidoku-r28/seats/a2w/ExecRecountC1/)

- clone/ (sandbox clone at a2673116, plus sandbox preview commit 8a66a02e)
- count.stdout  abe04add0f066d94f4e401637c36edcec73fa1e45f6fb1bdff8e5c538c1d0b69
- count.stderr  e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- selftest.stdout  e346a027f149f94c0cc441818ee0fc8884e1f2a03a43855f1f6c98b0da6d332d
- selftest.stderr  e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- emit-tally.json  655d8d648ecd46fa8ae71aca4fba7f57ba0fabc7dbd122e55bd4b6d0f1d148a5
- emit-tally.stderr  359a4d62227a2ab51842737d9f20e66aaa6535423a9c14401c59f2b46e7884a4
- committed-tally.json  655d8d648ecd46fa8ae71aca4fba7f57ba0fabc7dbd122e55bd4b6d0f1d148a5
- tally-bytediff.txt  e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 (empty)

Tooling: no install, no upgrade, no network fetch was needed. Only python3 and git from the host were used.

Report: .ufo/waves/round-28/a2w/ExecRecountC1.md
