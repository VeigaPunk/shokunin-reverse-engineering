# MutXpinTool — routed defect 8, mutation test of tools/round-27/xpin-attribute.mjs

Attacked item: routed defect 8 of `corpus/lessons/round-27-verifier-spotcheck.md` ("give …
`xpin-attribute.mjs` the mutation tests the dead seats did not run"); this seat covers the
`xpin-attribute.mjs` half only. **Verdict: holds under mutation.** 17 mutants, 17 killed, 0
survived, 0 inconclusive; the tool is not sensitive to any of the four defect classes named.

**Setup.** Sandbox clone at `/fast/scratch/hyaku/kaidoku-r28/seats/a2w/MutXpinTool/clone`
(`git clone -q` of the lane, clone HEAD `9db24c9e10287d44d9f780d782ab608f3c84ff5a`, final
`git status --porcelain` empty). Tool `tools/round-27/xpin-attribute.mjs`, pristine sha256
`8ea638379a4397dfc901334767d8015c88b16cf36c7f86e6a5beaf03a5d7f708` (the clone's copy and the lane's
copy had the same sha256 before the run). Pins as the round-27 receipt names them: `--pkg65
/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` (package.json 6.5.0), `--pkg67
/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents` (6.7.0). Corpus: the 24 round-26
envelopes of `corpus/evidence/round-27/c2/r26-attribution.tsv` column 1; Node v24.21.0. The
lane was never written; no `jj` command ran.

**Detectors** (each first run on the pristine bytes; the baseline passes all four, so every kill
below is real, not a baseline failure). **A** receipt diff: stdout vs the committed receipt
`corpus/evidence/round-27/c2/r26-attribution.tsv` (sha256
`b3c152811440cb8dc951e0e53c651bb809287345a062e65a8cc61bd48b6a4bbc`) plus exit code vs the
receipt's `exit=0`; baseline stdout byte-identical, exit 0. **B** committed checker
`tools/round-27/c2-xpin-check.py --root <clone> --rev HEAD --tool-cmd 'node <mutant>'`, a
non-zero checker exit kills; baseline `r26_rows_ok=24/24 red_ok=3/3 capability_row=1
source_row=1 (S081)`, exit 0. **C** the other three committed receipts, byte-compared:
`r27-c1-attribution.tsv`, `keyless-default.tsv`, `keyless-parse.tsv` (the last with `--parse`);
baseline all three byte-identical, exit 0. **D** the error path: an unreadable envelope must
exit 2 (baseline exit 2).

**Result per mutation.** `-`/`+` = removed/added rows in the receipt diff against
`r26-attribution.tsv`; A/B/C/D mark the detector that killed the mutant, `-` means that detector
passed it. Exact unified diffs: `work/M*.diff`; source diffs: `work/source-diffs.txt`.

| id | mutation | r26 `-`/`+` | killed by | exit | verdict |
|---|---|---|---|---|---|
| M01 | swap the projections: `id65` from the 6.7.0 pin, `id67` from the 6.5.0 pin | 21/21 | A,B,C | 0 | KILLED |
| M02 | drop `relationship_coverage` from the extracted text of the 6.7.0 pin | 24/24 | A,B,C | 0 | KILLED |
| M02b | drop `relationship_coverage` from the extracted text of both pins | 24/24 | A,B,C | 0 | KILLED |
| M02c | drop the conditional `relationship_coverage` spread of the 6.5.0 pin only | 3/3 | A,B,C | 0 | KILLED |
| M03 | mislabel the 6.5.0 verdict as `both` | 21/21 | A,B,C | 0 | KILLED |
| M04 | skip the id comparison: every envelope labelled `none` | 24/24 | A,B,C | 0 | KILLED |
| M05 | off-by-one: the two computed ids printed in swapped columns | 21/21 | A,B,C | 0 | KILLED |
| M06 | print the stored id in the `id67` column instead of the computed 6.7.0 id | 21/21 | A,B,C | 0 | KILLED |
| M07 | exit 2 on success instead of exit 0 | 0/0 | A,C | 2 | KILLED |
| M08 | skip envelopes whose `relationship_coverage` is null | 21/0 | A,B,C | 0 | KILLED |
| M09 | use the 6.5.0 projection for both pins | 21/21 | A,B,C | 0 | KILLED |
| M10 | input-error exit code changed from 2 to 3 | 0/0 | D | 0 | KILLED |
| M11 | `--parse` outcome word `accept` changed to `accepted` | 0/0 | C | 0 | KILLED |
| M12 | print the stored id in the `id65` column instead of the computed 6.5.0 id | 0/0 | B | 0 | KILLED |
| M13 | invert the attribution rule (both/none and 6.5.0/6.7.0 swapped) | 24/24 | A,B,C | 0 | KILLED |
| M14 | drop the `both` case: a both-matching envelope is labelled 6.5.0 | 3/3 | A,B,C | 0 | KILLED |
| M15 | read the evidence record from the envelope root instead of `.data` | 24/0 | A,B,C | 2 | KILLED |

**Diff excerpts.** The exact unified diffs are `work/M*.diff` and the source diffs
`work/source-diffs.txt`. M01 (`analyze-base.json`), base `stored | id65 | id67 | verdict` =
`ev_14f9…d328 | ev_14f9…d328 | ev_a4c5…c8a5 | 6.5.0`, mutant =
`ev_14f9…d328 | ev_a4c5…c8a5 | ev_14f9…d328 | 6.7.0`: the pins are transposed, attribution flips
6.5.0 → 6.7.0 on 21 of 24 rows. M02: the mutant's `id67` equals `id65`, so the verdict becomes
`both` on all 24 rows instead of 21×6.5.0 + 3×both — the 6.7.0 rule without
`relationship_coverage` is the 6.5.0 rule. M02c (`function-base.json`): base `id65 =
ev_b2b7…8b5`, mutant `id65 = ev_8439…a8`; only the 3 envelopes with a non-null
`relationship_coverage` move (tightest kill, 3 of 24 rows). M03: verdict `6.5.0` → `both` on 21
rows, checker `r26_rows_ok=3/24 red_ok=3/3`; M05 columns 3 and 4 transposed and M08 21 rows
vanish from stdout, each checker `r26_rows_ok=3/24`. M11: `keyless-parse.tsv` line 1 goes from
`parseEvidence-6.5.0 accept` to `parseEvidence-6.5.0 accepted` on all 37 rows. M12: stdout is
byte-identical to the receipt, so only detector B sees it — the checker prints `FAIL
red-tampered.json: tool ['6.5.0'], checker ['none']` and `red_ok=1/3`. M15: the tool dies on the
first envelope, exit 2, `envelope has no ".data" evidence record`.

**Coverage observations (findings, not defects).** (1) The committed checker does **not** fail on
a non-zero tool exit code: with M07 it prints `FAIL tool exit 2:` twice yet still reports
`r26_rows_ok=24/24 red_ok=3/3` and exits 0 (re-verified in isolation, 2026-10-22T18:30Z); detector
A catches M07 because the receipt records `exit=0`. (2) The r26 receipt alone cannot see M12: the
stored id equals the computed 6.5.0 id on all 24 round-26 envelopes, so printing the stored id in
the `id65` column leaves stdout identical; the checker's three red envelopes see it — a coverage
limit of the round-26 corpus. (3) The 6.7.0 label appears on no committed receipt row
(`6.5.0=21, 6.7.0=0, both=3, none=0` over 24 rows); the only 6.7.0 output in the corpus is the
checker's own red envelope — a limit of the receipts, not a tool defect.

**Restoration evidence.** After every mutant the tool bytes were rewritten from the pristine
buffer and re-hashed: `restored_ok=True` for all 17. The clone's final sha256 is
`8ea638379a4397dfc901334767d8015c88b16cf36c7f86e6a5beaf03a5d7f708`, equal to the pristine value
and to the lane's current value; `git status --porcelain` in the clone is empty (2026-10-22T18:49Z).
**Tooling.** No tool was installed or upgraded (Node v24.21.0, `python3` and `git` were already
present and sufficient); no network request and no REA call was made (the item does not ask for one).

**Artifacts** (seat dir `/fast/scratch/hyaku/kaidoku-r28/seats/a2w/MutXpinTool/`); per-mutant
`work/M*.out`, `work/M*.diff`, `work/M*.checker.txt` (77 files) sit there; hashes in the JSON.

| file | sha256 | role |
|---|---|---|
| `mutate.py` | `a9e12e5b9d70d78e3733437f76d7be6518fa146c048ecddd1fc2f49d8458ae01` | first 11-mutant pass |
| `mutate2.py` | `63d21f312b0bc268e6c4f104f6dc27df48d6b889114f202cce027d2ac2e33995` | 17-mutant set, two detectors |
| `mutate3.py` | `9b26a6329ce6e4dbf86df83e75f6ccba93d883220e3ffbdc27230a63587f9aae` | survivors vs the other receipts and the error path |
| `mutate_final.py` | `340856e79130b8b6c5910c09254dd20b63988e529638f499d8e6169bb720b19d` | consolidated 17 mutants, four detectors |
| `work/final-results.json` | `05435ccd2b0758b358a2227a010c0225469f3fc47126854a0a518080f21000c9` | verdicts, detector results, hashes, times |
| `work/results2.json` | `c7e4135b923eaa7b94f701c20957432ebd2b5adf037649249cc3a668c31ef260` | two-detector pass |
| `work/results3.json` | `48dc0c65f1a49cf3f0f48e873e0800d46902c686df2dac3034a49742c8b55074` | survivor pass against the other receipts |
| `work/baseline.tsv` | `b3c152811440cb8dc951e0e53c651bb809287345a062e65a8cc61bd48b6a4bbc` | pristine stdout, equal to the receipt |
| `work/source-diffs.txt` | `a4db14faae5e05fb3a41b2c5b0a0ec606674e38cedea9e2db979bc4d17da7243` | all 17 source diffs |