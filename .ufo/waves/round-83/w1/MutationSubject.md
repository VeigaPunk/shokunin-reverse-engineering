# MutationSubject — round83 source-attribution mutation probe

Author-side evidence only; no outside admission, integration, or production changes.

## Axes and method

Axes: defect sensitivity; committed-real-entry relevance; exact restoration/isolation. Coordinated with ExecCandidate, which explicitly announced stable candidate bytes before the probe. Candidate snapshot: `.ufo/waves/round-83/w1/MutationSubject/subject-snapshot.py`.

Executed one bounded adapter invocation. It reads frozen audit/case blobs at declaration `de4e58b2c22bf4376dc81bd32dfe0b9ac605e17e` using absolute-root read-only `git show`, extracts the audit's unchanged `load_function` and `score`, and uses the committed real entry at BASE `650344bc37ca303fb9487c1174192057af499b9b`. For each of six required fault variants it runs the identical detector on pristine, mutated, and exactly restored scratch bytes. Frozen score remains exactly eight cases, two real, with strict boolean matching. No predicate/counter/fixture changes.

The adapter also evaluates two separately labeled grammar witnesses, never added to the frozen population: a valid source header on line 13, and two valid source headers. These demonstrate real behavioral defects in the surviving mutations, not new admission criteria.

## Observed results

All six pristine and restored runs: rc0, zero frozen mismatches, zero supplemental mismatches. Results below are frozen-score verdicts, not claims about a committed CLI invocation.

| Mutation | Expected detector | Observed frozen mismatches | Verdict | Supplemental witness |
|---|---|---|---|---|
| lexical presence across text | real-withdrawn, commentary-only, withdrawn-head (minimum expected set) | real-withdrawn, commentary-only, withdrawn-head, absent-source | killed (rc1) | late-header and duplicate-header fail |
| allfalse | real-primary, plain-positive, multi-positive | same three | killed (rc1) | neither fails |
| alltrue | real-withdrawn, commentary-only, withdrawn-head, absent-source, embedded-id | same five | killed (rc1) | both fail |
| drop multi-id after first id | multi-positive | multi-positive | killed (rc1) | neither fails |
| ignore header position by moving all source lines to beginning | no frozen case covers late headers | none | survived (rc0) | late-header fails |
| ignore duplicates by retaining first source line | no frozen case covers duplicates | none | survived (rc0) | duplicate-header fails |

The lexical mutant deliberately regresses to whole-text lexical presence, rather than copying the old first-source-line implementation; its additional `absent-source` mismatch is therefore expected from this broader defect. It still kills on the actual committed `real-withdrawn` case. Allfalse kills actual `real-primary`; alltrue kills actual `real-withdrawn`. Drop-multi-id has direct synthetic coverage but neither real-entry row distinguishes it because that entry has only one leading positive source. Header-position and duplicate weaknesses have synthetic grammar relevance only: the retained real entry does not exercise either condition. Those two survivors are frozen-detector coverage findings; they do not authorize changing the frozen eight cases or contract. The supplemental observations establish that these were behavior-changing mutants, not equivalent rewrites.

## Restoration and receipt identity

Original snapshot, every pristine scratch input, and every restored scratch input SHA-256:
`fa08b06340eb49929ffc34d69ac789c4fde91e83b4714afaff20b020e940ed18`.

| Mutant | Mutated SHA-256 |
|---|---|
| lexical-presence | `1b82cef466726907c6f69be36b2fb815c7d68bd92e992d4951da33e682cc15e9` |
| allfalse | `5c12cd49707a69ee5865131caa7fd3f0efbdc6506135bd8fdb12366c57c85e42` |
| alltrue | `c29f21523b44880206015cf4266102c5b0348701518c1ef1812b8628b9f17108` |
| drop-multi-id | `77d4dc6b36eb7c8ba926f4fa00b16d60400b7e197f92954c348c9b9c1d0a684b` |
| ignore-header-position | `472002c1e523b2947e16811faf39924a1218234f716d16633a9505fecd0ed289` |
| ignore-header-duplicates | `33e785e83b86698575c76fc4b0dfce19d1522af5d502a44cdc636c4171d3bcf4` |

Frozen cases SHA-256: `2066da67577812070fb93bc004bc8818b7f92b761d79fff29f2713189add441f`.
Frozen audit SHA-256: `386e7891b4ffedae6f3df12c8c741e81aaa2338dfea3447dc26537f274646521`.
Committed real-entry SHA-256: `c14b43393b85cc64275f06c00a9195fd03d0e54c4e78c01f897649096b5089ee`.

Full per-case observed/expected booleans, before/mutant/after hashes, and restoration flags are retained in `.ufo/waves/round-83/w1/MutationSubject/mutation-results.json`. Every `exact_restoration` is true. Receipt records `scratch_removed: true`; the assigned scratch directory was removed by the adapter's finally block after restoration. No clone, git/jj mutation, package installation, production write, or sibling write occurred. No builds, linters, or formatters ran.

## Executable handoff

Script: `.ufo/waves/round-83/w1/MutationSubject/mutation-probe.py` (executable). It refuses an existing scratch directory and enforces explicit TMPDIR. Reproduce from the saved, actually probed snapshot:

```sh
env TMPDIR=/fast/scratch/hyaku/kaidoku-r83/MutationSubject python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-83/w1/MutationSubject/mutation-probe.py --subject /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-83/w1/MutationSubject/subject-snapshot.py
```

The observed invocation used ExecCandidate's announced stable `candidates/source-bind.py` instead of the saved snapshot. L1 can supply integrated bytes via `--subject`; those later bytes are not claimed tested here. The adapter exercises the frozen scoring functions on private file bytes, not the full committed-target CLI admission path. Tools installed: none.

## Self-assessment

Accuracy 4/5: full receipt grounds all six verdicts; no committed CLI admission exercised. Completeness 4/5: all required faults probed, but two have no frozen-case coverage, explicitly retained as findings. Clarity 4/5: separate frozen versus supplemental verdicts; lexical variant differs from legacy and is labeled. Actionability 4/5: executable snapshot-replay command supplied; integration remains L1-owned. Conciseness 4/5: hash detail is retained for restoration audit. Overall 4.0/5. Highest-impact next action is L1's interpretation of the two coverage survivors without modifying the frozen calibration instrument; broader gate exercise is outside this seat. The user should agree insofar as author-side bounded evidence, not outside admission, was requested.
