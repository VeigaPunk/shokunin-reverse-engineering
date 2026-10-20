# MutateTemporalSweep — author-side advisory

**Axes:** calibration (separate detector coverage from source correctness); depth (single-point, non-equivalent regressions with bounded witnesses).

**Observed:** 11 isolated one-line mutants; **4 killed, 7 survived, 0 inconclusive** under the assigned `--selftest` detector. Every pristine/restored run passed. All eleven mutants changed behavior on a separate small Git fixture. Survivors are **coverage findings**, not proof that the committed implementation is defective or that C1 fails.

## Target, detector, isolation

- Revision: `da64646adcb19c1ede7537b799b8c7d283fe43da`.
- Target: `.ufo/waves/round-17/tools/temporal-sweep.py`; committed blob and copied worktree blob both `bfbf6d64a73c3a6478e35664eee01557b5256db2`.
- Pristine SHA-256, **H0**: `3f640a77fe60e58d1ec0a6e943b040203098306c043ead5744f7384877f4c071`.
- Scratch: `/tmp/r17-MutateTemporalSweep.Zw01FB/`; `m01.py` through `m11.py`, one changed line per copy. Canonical source was never edited.
- Python: `Python 3.14.8`; no installs/updates, carrier execution, REA, Ghidra, delegation, commits, or pushes.
- Expected detector: reject each behavioral regression via nonzero `--selftest`. Verdicts below use only that detector, **not** the supplementary witnesses.

Executed driver commands:

```text
python3 -B -I /tmp/r17-MutateTemporalSweep.Zw01FB/probe.py baseline
python3 -B -I /tmp/r17-MutateTemporalSweep.Zw01FB/probe.py mutated-restored
```

For each `NN=01..11`, the exact detector argv in all three phases was:

```text
/usr/bin/python3 -B -I /tmp/r17-MutateTemporalSweep.Zw01FB/mNN.py --selftest
```

Each invocation had a 45-second limit; at most four copies ran concurrently. There were 33 detector invocations: pristine → mutated → restored for each copy. All 22 pristine/restored invocations returned exit `0`, stdout `SELFTEST: CLEAN cases=6\n`, stderr empty. All seven surviving mutants returned those same values. The four kills returned exit `1`, stdout empty, and the assertion failures recorded below. No timeouts occurred.

## Mutation matrix

All anchors refer to the target at the named revision; each replacement preserved line numbering.

| ID | Behavior-bearing point | Single-line mutation | Detector result |
|---|---|---|---|
| m01 | `.ufo/waves/round-17/tools/temporal-sweep.py:169` | Replace `and REQUIRED_PHRASE in line.lower()` with `and True` | **Killed**, assertion at line 290 |
| m02 | `.ufo/waves/round-17/tools/temporal-sweep.py:168` | Replace `re.search(re.escape(token) + r"(?!\d)", line)` with `re.search(re.escape(token), line)` | **Survived** |
| m03 | `.ufo/waves/round-17/tools/temporal-sweep.py:144` | Replace committed correction-line filter `if MARKER in l` with `if True` | **Survived** |
| m04 | `.ufo/waves/round-17/tools/temporal-sweep.py:56` | Remove `across` from the temporal-preposition alternatives | **Survived** |
| m05 | `.ufo/waves/round-17/tools/temporal-sweep.py:56` | Remove `execution` from the run/execution alternatives | **Killed**, assertion at line 263 |
| m06 | `.ufo/waves/round-17/tools/temporal-sweep.py:130` | Replace join with `joined = line.rstrip()` | **Survived** |
| m07 | `.ufo/waves/round-17/tools/temporal-sweep.py:132` | Replace start-line guard with `if m:` | **Killed**, assertion at line 263 |
| m08 | `.ufo/waves/round-17/tools/temporal-sweep.py:161` | Replace resolution of `sites_rev` with `canonical_sites_rev = canonical_rev` | **Killed**, assertion at line 306 |
| m09 | `.ufo/waves/round-17/tools/temporal-sweep.py:177` | Discover new sites at `canonical_sites_rev` instead of `canonical_rev` | **Survived** |
| m10 | `.ufo/waves/round-17/tools/temporal-sweep.py:127` | Replace `if MARKER in line:` with `if False:` | **Survived** |
| m11 | `.ufo/waves/round-17/tools/temporal-sweep.py:44` | Replace knowledge directory with `SITE_DIRS = ["corpus/lessons/"]` | **Survived** |

Exact final stderr lines from the killed mutants (preceded by Python tracebacks):

```text
m01: AssertionError: {'sites': 3, 'corrected': 2, 'unqualified': 1, 'new_unqualified_at_rev': 0}
m05: AssertionError: {'sites': 2, 'corrected': 0, 'unqualified': 2, 'new_unqualified_at_rev': 0}
m07: AssertionError: {'sites': 5, 'corrected': 0, 'unqualified': 5, 'new_unqualified_at_rev': 0}
m08: AssertionError: {'sites': 2, 'corrected': 1, 'unqualified': 1, 'new_unqualified_at_rev': 0}
```

## Surviving mutants: observed witnesses and missing cases

A supplementary fixture witness was run in **all three phases for every ID**, using the same argv for that ID:

```text
/usr/bin/python3 -B -I /tmp/r17-MutateTemporalSweep.Zw01FB/witness.py mNN /tmp/r17-MutateTemporalSweep.Zw01FB/mNN.py
```

The witness imports the selected copy, creates a fresh `/tmp` Git repository, commits only the listed text, and prints `json.dumps(sweep(root, rev, [], sites_rev=old)["counts"], sort_keys=True)`. For m09 it makes the specified second commit; other survivor fixtures have `rev=old`. Literal `\n` below denotes a newline. All witness invocations exited `0`, stderr empty. These are exact stdout values, each followed by a newline:

```text
A = {"corrected": 0, "new_unqualified_at_rev": 0, "sites": 1, "unqualified": 1}
B = {"corrected": 1, "new_unqualified_at_rev": 0, "sites": 1, "unqualified": 0}
C = {"corrected": 0, "new_unqualified_at_rev": 0, "sites": 0, "unqualified": 0}
D = {"corrected": 0, "new_unqualified_at_rev": 1, "sites": 1, "unqualified": 1}
```

| Survivor | Witness fixture / missing selftest case | Observed pristine → mutant → restored |
|---|---|---|
| m02 | `LOG.md="# log\npins unchanged during run\n"`; `SCORECARD.md="R16-PROVENANCE LOG.md:20 temporal stability not evidenced\n"`. Missing negative test: `LOG.md:20` must not correct `LOG.md:2`. | A → B → A |
| m03 | `LOG.md="pins unchanged during run\n"`; `SCORECARD.md="LOG.md:1 temporal stability not evidenced\n"`. Missing negative test: exact location + phrase **without the marker** is not a correction. | A → B → A |
| m04 | `LOG.md="pins unchanged across execution\n"`. Missing positive test for the integrated `across execution` wording. | A → C → A |
| m06 | `LOG.md="pins unchanged during\nthe run\n"`. Missing positive test for the integrated two-line join, including attribution to the first line. | A → C → A |
| m09 | First commit: `LOG.md="pins unchanged during run\n"`; second adds `SKILL.md="new pins unchanged during run\n"`; baseline sites stay fixed. Missing assertion that `new_unqualified_at_rev == 1` for an introduced claim. | D → A → D |
| m10 | `LOG.md="R16-PROVENANCE pins unchanged during run\n"`. Missing negative test for the implementation's existing marker-line exclusion policy. | C → A → C |
| m11 | `corpus/knowledge/witness.md="pins unchanged during run\n"`, no other files. Missing positive test that discovered knowledge Markdown participates in the census. | A → C → A |

**Observation:** the built-in fixture has no knowledge file or wrapped claim (`.ufo/waves/round-17/tools/temporal-sweep.py:236-250`), and its initial count assertion explicitly removes `new_unqualified_at_rev` (`.ufo/waves/round-17/tools/temporal-sweep.py:262`). The seven differences above establish non-equivalence rather than merely counting edits that happen to pass.

**Inference:** these seven missing regression cases would detect the corresponding mutants; they were exercised as witnesses, not added to or passed off as the assigned selftest. The implementation's stricter correction rule is documented at `.ufo/waves/round-17/tools/temporal-sweep.py:156-169`; this probe challenges that integrated behavior rather than silently substituting the older path-only rule in the shared contract. No production fix or claim-admission judgment is proposed here.

## Hashes and exact restoration

For **every row**, the pristine hash was H0; mutated detector/witness runs left their input hash unchanged; the restored hash was H0 before and after both restored runs. The driver restored each copy from `pristine.py` in a `finally` block even when the detector returned nonzero. Restored witnesses matched their pristine outputs for all eleven IDs.

| ID | Pristine | Mutated SHA-256 | Restored |
|---|---|---|---|
| m01 | H0 | `4e2e1d7386f0ca4e2c2cb57c5ba0a5540e04438023ce1c6b86629e5d0fc93a4e` | H0 |
| m02 | H0 | `9bc4cff9842c70dfb20ba442c65e50ca61eafbd7cc70e2b1a28553d6442b57d3` | H0 |
| m03 | H0 | `2fdba87feefeaf6ee83c02b5cca54f62d687243c30a00f9dc51a1b61f0adab10` | H0 |
| m04 | H0 | `df24b176efd81dedff4ee6784b53eba704f3782075e2656c92245f7bf53807aa` | H0 |
| m05 | H0 | `e91c2c00c1d0d72ebdc7f14df4b19a412ca7de65aebadf7f90e9935a5fc6d604` | H0 |
| m06 | H0 | `bd1cb7143e48924fc90173c3b4d48d22ffa7131ec5325b605a622675d0fdebe8` | H0 |
| m07 | H0 | `837e5e370c48f52bcf48426eb433ea7df7cfb20bf8a1419077f1e3c0bcc7cd9e` | H0 |
| m08 | H0 | `2dfd4e3c5f2810b0df5eb622c3843a199583ae55a722b081d2bffbe05566c200` | H0 |
| m09 | H0 | `f2863832a5b377e9ecaab94db6428d03cecfb4153b0f4341bb553d8f74b09863` | H0 |
| m10 | H0 | `51b0f345bbb717987d88f8325c2f79e0cf243c4d2f9eeeff504ab0528149692a` | H0 |
| m11 | H0 | `2e037a9dd41b62466a5117d854edf3fef26a9a8f4b81adeba63f2fedc0480c44` | H0 |

Raw captures and bounded driver/witness scripts remain in the named scratch directory (`baseline.json`, `results.json`, `probe.py`, `witness.py`); all target copies there are restored. This report embeds the findings and hashes so the result does not depend solely on temporary artifacts. Only this report was written inside the lane.
