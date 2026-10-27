# R43W2C1Mutation — generator tuple-check mutation probe

**Measured revision:** `5856614ac4bf7f2363bbcd1956644474a82108e5` (lane tip when captured); freeze `f3f8db389416d094b1ddeb1215ddcf914bfc0d1c`. The frozen plan was read first. This is a bounded falsification of the landed generator's offline tuple selftest, not a score of the entire C1 predicate.

## Inputs / provenance

- Plan: `plans/round-43-claims.md`; sha256 not captured before reading.
- Mutant specification: `.ufo/waves/round-43/w1/artifacts/R43MutGen/mutants.json`, sha256 `40bb66ee3ff5090545030513bbd4ea4f0251380047dfa1d485d459393eb1d242`.
- Landed generator: `tools/round-43/heldout-gen-v4r43.py`, sha256 `6ab0114d555a09a93ab61459c7adb76a45957a35dc69671b64e7733225aca97a`.
- Frozen C1 counter: `tools/round-43/c1-counter.py`, sha256 `3a23e93ee95f4b0d69a2f4d03ed2592c9f0b81dbb6188cb6818a18a8f4f33c79`.
- Landed selftest receipt: `.ufo/waves/round-43/w1/artifacts/R43C1Gen/receipt-selftest-tuple.txt`; reported `tuple-check selftest: 17/17 passed`, exit 0.
- C2 score receipt hash observed: `.ufo/waves/round-43/l1/scores/c2-at-09ab56b8.json`, sha256 `126b529eb5c3b0d61eaceb5f2e026eb3de9b0a9c2256239eabd86a23eaad9f4e`. Requested C1 score path at the captured revision was not found at the guessed `c1-at-5856614...` filename. No claim about its contents.

## Procedure and output

Scratch clone: `/fast/scratch/hyaku/kaidoku-r43/w2/R43W2C1Mutation/lane` (shared object clone of the lane; no commits or lane edits). Generator bytes were overwritten with each isolated fault and restored from the original byte string after each run. Detector command for each mutation and baseline/restoration:

`python3 -I -B <scratch clone>/tools/round-43/heldout-gen-v4r43.py --selftest-tuple --scratch /fast/scratch/hyaku/kaidoku-r43/w2/R43W2C1Mutation`

The pristine detector exited 0 and printed `tuple-check selftest: 17/17 passed`. Each mutant's exact changed-file hash, exit code, trailing output, and stderr are in `artifacts/R43W2C1Mutation/results.json` (sha256 `d0c6fe090e71cb03d87268419002e1d22cb5d871c2ffa15e211fb2c7967e3eda`). Restored bytes hash was exactly `6ab0114d555a09a93ab61459c7adb76a45957a35dc69671b64e7733225aca97a`; restored detector exit 0.

Faults were applied at the corresponding smallest tuple-comparison, finalization, or REA argv behavior point. The results show the shipped selftest **kills 12/20** implemented mutants: M01, M02, M07–M14, M16, M17. It **survives 8/20**: M03, M04, M05, M06, M15, M18, M19, M20. M18 changes run-time REA depth to the default and is not exercised by this offline test. Per actual outputs: M01/M02 fail the shipped `red: a wrong handler family` test; M07/M08/M10/M11 fail C02 (and other gap tests); M09, M13, M17 also fail green/other refusal checks; M12/M14 fail several red-key / C02 checks; M16 fails several refusal/no-write checks. See artifact for each exit and output.

**Important limitation:** the run above invoked the *landed 17-check offline selftest*, not the full R43MutGen 10-case external mutation suite. The R43MutGen artifact specifies additional discriminators (`ST-DEPS`, `ST-BEARGV`, `ST-SYMREMOVED`, `ST-PUBZERO`, `ST-KINDSWAP`, `ST-INCOMPLETE`, `ST-ORDER`) that are absent from the landed selftest receipt. Accordingly, the eight survivors identify landed-selftest coverage gaps, not survivors against those unrun discriminators. The six single-field mismatch cases and explicit order-semantics case were **not executed** in this probe; nor was a committed C02 directory passed through `--tuple-check`. The green self-certification and no-manifest behaviors were exercised indirectly by landed selftest checks and their outputs are captured in the receipt/result artifact. M18's run argv assertion was not executed. These remain unverified here; no REA/extractor or firmware input was run.

## Commands, boundaries, cleanup

Commands included lane `git rev-parse HEAD`, `git rev-parse <freeze>`, `sha256sum` of the listed inputs, `df -h /fast/scratch /home/vgpnk/Projects/shokunin` (562G and 590G available respectively), `git clone --shared <lane> <scratch>/lane`, and the detector command above. No installs, commits, tests/linters on the repo, reserved firmware inputs, or production changes. No disk-guard status file was present at `/run/disk-guard/status`.

The exact scratch clone and harness were removed before handoff; only this report and its result artifact remain under the assigned wave-2 paths.
