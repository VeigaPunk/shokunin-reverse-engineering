# MutC2Checker — mutation test of the R27-C2 checker

Seat: MutC2Checker (mutation tester). Round 27, attempt 1, wave 1. Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
UTC window 2026-10-22T15:02Z to 2026-10-22T15:06Z. No REA call was made; the checker never calls REA.

## What was attacked

`tools/round-27/c2-xpin-check.py` (sha256 `d8de667ff82a46d5c0c9a19d4fc2f5a3c36c12fa037f9a32287046a377209bd3`, unchanged in the lane, verified at lane HEAD and at `main` after the R27-C1 data commit).
Attack surface: the tool side of the counter, that is what `--tool-cmd` feeds the checker, plus the checker's own red fixtures and its selftest.

## Detector and baseline

Detector (one command, used for every row):

```
python3 -I -B tools/round-27/c2-xpin-check.py --root <root> --rev <rev> --tool-cmd "<tool>"
```

A mutant is killed when the row counters drop below 24 of 24 and 3 of 3, and survives when they stay at 24 of 24 and 3 of 3.
Baseline: `tools/ref-correct.mjs`, a node tool that loads each installed package's own exported `digestCanonicalValue` and that package's own `semanticProjection` source text. Baseline at `main` (`a4f674b3`, 2026-10-22T15:02:19Z, exit 1): `r26_rows_ok=24/24 red_ok=3/3 capability_row=0 source_row=0`. The baseline is not circular: its ids come from the packages, the checker's from the round-26 Python recompute, and they agree on 27 of 27 fixtures.

At `main` the process exit is 1 for every tool because `capability_row=0` and `source_row=0` (the capability row, the SOURCES row and `corpus/lessons/round-27.md` do not exist yet, and the tool `tools/round-27/xpin-attribute.mjs` is not committed). To get a discriminative process exit I used a sandbox clone `clone/` at commit `37cc97393e3f7992279f1eb1b53ad1169171fd23` (a clone of the lane plus one sandbox commit that adds a capability row, an S081 source row and a round-27 lesson gate row; the lane itself was not touched). Baseline there, 2026-10-22T15:04:14Z, exit 0: `r26_rows_ok=24/24 red_ok=3/3 capability_row=1 source_row=1 (S081)`. The same suite was also run against lane `main` after it advanced to `9dca26df135a2c558aaa575534ad42662b372d5d` (2026-10-22T15:05:02Z to 15:05:09Z): every row count is identical to the `a4f674b3` run.

## Wrong tools, results

Eight wrong tools sit in `tools/`. "Checker output line" is the counters line the checker printed; "exit" is the checker process exit (clone run, so it is decided by the tool result alone).

| wrong tool | checker output line | exit | killed or survived |
|---|---|---|---|
| `w1-lowercase-trim.mjs` (ids trimmed and lower-cased) | `r26_rows_ok=24/24 red_ok=3/3 capability_row=1 source_row=1 (S081)` | 0 | survived (equivalent: stdout sha256 `58794fec…` equals the reference byte for byte) |
| `w2-swap-65-67.mjs` (id65 and id67 columns swapped) | `r26_rows_ok=3/24 red_ok=1/3 capability_row=1 source_row=1 (S081)` | 1 | killed (23 FAIL lines) |
| `w3-coverage-both.mjs` (no hashing, "both" when coverage is non-null) | `r26_rows_ok=3/24 red_ok=1/3 capability_row=1 source_row=1 (S081)` | 1 | killed (23 FAIL lines) |
| `w4-extra-lines.mjs` (a second row for the same envelope) | `r26_rows_ok=0/24 red_ok=0/3 capability_row=1 source_row=1 (S081)` | 1 | killed (27 FAIL lines) |
| `w4b-extra-noise.mjs` (extra lines that are not envelope rows) | `r26_rows_ok=24/24 red_ok=3/3 capability_row=1 source_row=1 (S081)` | 0 | survived |
| `w5-relative-paths.mjs` (paths relative to the working directory) | `r26_rows_ok=0/24 red_ok=0/3 capability_row=1 source_row=1 (S081)` | 1 | killed (27 FAIL lines) |
| `w6-exit-1.mjs` (correct rows, then exit 1) | `r26_rows_ok=24/24 red_ok=3/3 capability_row=1 source_row=1 (S081)` | 0 | survived (2 FAIL lines, `FAIL tool exit 1:`) |
| `w7-retyped-python.py` (correct rows, retyped Python projection) | `r26_rows_ok=24/24 red_ok=3/3 capability_row=1 source_row=1 (S081)` | 0 | survived (stdout sha256 `58794fec…`, identical to the reference) |

Exact FAIL excerpts (clone run): `FAIL analyze-base.json: tool ['6.5.0'], checker ['6.5.0']` (w2), `FAIL analyze-base.json: tool ['none'], checker ['6.5.0']` (w3), `FAIL analyze-base.json: tool printed 2 lines` (w4), `FAIL analyze-base.json: tool printed 0 lines` (w5), `FAIL tool exit 1: ` (w6).

## Which survivors matter to the R27-C2 statement

- `w7-retyped-python.py` matters most. The R27-C2 statement says the ids must come from each package's own `digestCanonicalValue` and that package's own `semanticProjection` source text, "not a retyped projection". The counter cannot see the method: a tool that retypes the projection in Python and prints the same rows passes 24 of 24 and 3 of 3. Observation: the counter's evidence for "using each installed package's own canonical digest code" is not evidence at all. The frozen limits in `claims.json` already say this is a reviewer item; this probe confirms the gap is real and that a reviewer must read the tool source. A second reason it matters: the 24 envelopes hold no float, no integer beyond 2^53 and no non-ASCII string or key (`out/probe-value-shapes.txt`), so even a retyped writer that mishandles those shapes would print identical rows on every fixture. The counter can never separate the two methods by output.
- `w6-exit-1.mjs` matters. The tool contract in the frozen claim says "exit 0". The checker records a non-zero tool exit as a reason line but does not let it change a counter, so the counter printed 24 of 24, 3 of 3 and exited 0 for a tool that exits 1. The counter's own "exit 0" receipt therefore does not show that the tool completed cleanly.
- `w4b-extra-noise.mjs` matters mildly. The contract says one stdout line per envelope. The checker parses any line with five tab cells whose first cell is an envelope path and ignores everything else, so a tool that prints a header line and a summary line still passes. Output hygiene is not counted.
- `w1-lowercase-trim.mjs` does not matter. The ids are `ev_` plus a lower-case hex digest with no whitespace, so the mutation is a no-op on every possible id of that shape; the stdout was byte for byte the reference.

## Checker fixture mutations and the selftest

All three were made in the sandbox clone only; the lane file was never edited.

| fixture mutation | selftest verdict | evidence |
|---|---|---|
| F1: delete the `red-coverage-set.json` case from `red_cases` | killed, selftest notices | `FAIL correct-stub: exit 1, expects 'r26_rows_ok=24/24 red_ok=3/3' | r26_rows_ok=24/24 red_ok=2/3 …`, `selftest cases=6 failures=3`, exit 1 (2026-10-22T15:03Z) |
| F2: expect `6.5.0` instead of `both` for `red-coverage-set.json` | killed, selftest notices | `input error: fixture red-coverage-set.json derives both, expected 6.5.0`, `selftest cases=6 failures=4`, exit 1 (2026-10-22T15:03Z) |
| F3: weaken the 6.5.0 rule in `ids_for` so it always carries `relationship_coverage` (id65 becomes id67) | killed, selftest notices | `input error: fixture red-minted-67.json derives both, expected 6.7.0`, `selftest cases=6 failures=4`, exit 1; the tool run with the correct reference tool also stops with exit 2 and the same input error (2026-10-22T15:04Z) |

F3 was an extra probe beyond the assignment: it asks whether the selftest can notice a weakened recompute. It can, because the red fixture `red-minted-67` is cross-checked against the checker's own derivation and the two disagree. The selftest is not a rubber stamp for the red fixtures.

Pristine selftest in the clone: `selftest cases=6 failures=0`, exit 0 (`out/selftest/baseline.txt`).

## Restoration evidence

After each fixture mutation the clone file was restored with `git -C clone checkout -- tools/round-27/c2-xpin-check.py` and the hash was re-read: `d8de667ff82a46d5c0c9a19d4fc2f5a3c36c12fa037f9a32287046a377209bd3` after F1, after F2 and after F3, matching the frozen value in `claims.json`. The selftest after the restore printed `selftest cases=6 failures=0`, exit 0 (`out/selftest/restored-after-F1.txt`). The baseline tool was run before the mutants and again after them (`ref-correct.mjs` then `restored-ref-correct.mjs`): 24 of 24 and 3 of 3 in both, at both revisions, and stdout sha256 `58794fec…` unchanged. Lane `git status --porcelain` before and after shows the dispatcher's and other seats' files only; the one file I wrote in the lane is this report. The lane's `corpus/SOURCES.md` shows as modified and a new `corpus/knowledge/2026-10-22-r27-renamed-copy-evidence-id-identity.md` appeared at 2026-10-22T15:05Z, both from the sibling R27-C1 knowledge seat, not from this probe (my S081 row was added in the clone only). The lane checker file hash is `d8de667f…` at the end.

## One more observation on the checker's own diagnostics

Observation: the reason line compares only the fourth cell. `got[0][3:]` is the attribution, so for the killed swap mutant the checker prints `FAIL analyze-base.json: tool ['6.5.0'], checker ['6.5.0']` — two identical strings, while the real difference is in the id columns. A reviewer reading the failure log sees a difference that is not there. Inference: the message should show the id columns too, otherwise a real failure looks like a no-op.

## Limits of this probe

- The correct reference tool is my own code (no committed `tools/round-27/xpin-attribute.mjs` existed at the time of the run), so the baseline proves the checker's expected values are reproducible from the installed packages, not that the future tool is correct.
- The clone commit `37cc9739` exists only to make the checker's process exit depend on the tool; it adds a capability row, an S081 source row and a lesson gate row that the lane does not have.
- The mutation set covers the seven named wrong-tool classes and one extra. It does not cover a tool that hangs, writes files or mutates the corpus.
- Nothing in the lane was changed, committed, or pushed. No REA call was made. No tool was installed or upgraded.

## Artifacts (all under `/fast/scratch/hyaku/kaidoku-r27/seats/MutC2Checker/`)

| file | sha256 |
|---|---|
| `tools/lib.mjs` | `d162566775cf13050950c67f3aa57d9bd9b429df3aa041358b1ac03f8fc43f73` |
| `tools/ref-correct.mjs` (baseline) | `bf89e12217252bf2c38841faf41d97a39b8111a3e98f2123e5becf489f7bf4a0` |
| `tools/w1-lowercase-trim.mjs` | `0cc6422f3fe0f02bd275dbe99d16773b2d348dd822db6419875c7ea6facabafe` |
| `tools/w2-swap-65-67.mjs` | `6c4a75f260d16c5ae527a3e408f082f2722f92be2f0997aa2a27cbc4b31f29eb` |
| `tools/w3-coverage-both.mjs` | `6577a734ee9fb6e02520f69090a8d41ce7410e3f9812ab8ccd09889fe57ce724` |
| `tools/w4-extra-lines.mjs` | `6ee519014513099b9d9fd836cf6c12a17ae0a9bd634003e1f6aa713b986a520e` |
| `tools/w4b-extra-noise.mjs` | `a28d2e4487cc624e7059647c8e8c2347e7d3c6ea33aa3002b1e055f0f0b5b974` |
| `tools/w5-relative-paths.mjs` | `f75ac43bf7cbdec58bfcdbf61c03c46a650e555605d657823148538b06cc6f76` |
| `tools/w6-exit-1.mjs` | `51ae5c66ad12c2082c14d5b3a4b4fb6ad90b243dedf7544eba9fbf42d28e39c0` |
| `tools/w7-retyped-python.py` | `ed3b533b9dbdffc2ca3032977b553d0a9dbf2c938ee1f2d0ffdfc85394071741` |
| `tools/run-mutants.sh` | `11876f2ec197ee20fc76f708fa50b4c0a7e6d1346b0f190b4509810b494309ea` |
| `tools/compare-outputs.py` | `5e9e1b8ee3e30c950042deaf3d2fa950d894c8cb9c122ff0ac5203028281a3c7` |
| `tools/analyze.py` | `ba76d0b948a79adb3402c9ba11a269f711805d60e67b39cdbbbb7364c4862b53` |
| `tools/probe-value-shapes.py` | `872ee3c948abb91b6b0dee84a910880fcd541878f072602d2e1f7a8fb22214aa` |
| `out/main/*.txt` (lane `main` runs, 10 files) | per file, recorded in the run files |
| `out/main9dca/*.txt` (lane `main` at `9dca26df`, 10 files) | per file, recorded in the run files |
| `out/clone/*.txt` (sandbox clone runs, 10 files) | per file, recorded in the run files |
| `out/selftest/baseline.txt` | `c21408fcaa7d62aff503cf0ea6371f09f381c845f3bfc0e132f4e158f762b369` |
| `out/selftest/F1-red-coverage-set-removed.txt` | `b0e88b78dcc8109ffcedc435c87300ece1500ca01f64edefe17b419ea9a07808` |
| `out/selftest/F2-expected-attribution-changed.txt` | `1b22ec8e9477c1143b6b09bc58a455ff5cffc96b1810f477fc2701729c2d5035` |
| `out/selftest/F3-weakened-65-rule.txt` | `4821f84cb08f31412dbf372c397780c9bf57b46b2186c5362615e8a3972423c1` |
| `out/selftest/F3-real-tool-check.txt` | `cfb4dbdace835c552a93197c82e43dd747e99d5592c147e11b4ad155728be55d` |
| `out/selftest/restored-after-F1.txt` | `c21408fcaa7d62aff503cf0ea6371f09f381c845f3bfc0e132f4e158f762b369` |
| `out/compare/summary.txt` | `322bc011337a868582c90977bd7798d4dc48b9e4f32319d8791121d168b3d62f` |
| `out/probe-value-shapes.txt` | `83b2508aa9f1bf63cfcfb717d15d814ab30f9a4d0cb59b88785fa433a4587a02` |
| `clone/` | sandbox clone at `37cc9739`, not a lane artifact |

Report: .ufo/waves/round-27/w1/MutC2Checker.md
