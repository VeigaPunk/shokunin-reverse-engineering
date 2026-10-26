# R41W2C2InterpMut — mutation sweep of the C2 interpreter and evaluator

**Verdict: DEFECTS FOUND** — 9 of 41 mutants survive the full tasked kill check (own `--selftest` AND the 52 held-out pairs unchanged), every one of the 32 kills came from `--selftest` alone (the held-out pair oracle killed nothing by itself), and the two pristine tools disagree on 5 envelope shapes the held-out set never exercises. What I attacked: the frozen R41-C2 oracle pair `tools/round-41/sqfs-triage-v3.py` (interpreter) and `tools/round-41/indep-eval-v3.py` (evaluator) — whether single-point behavior changes along the six tasked axes (contains-form parsing, exact vs contains, BE token, SR detection, P counting, step order) are detectable. The landed C2 pair result itself reproduces: baseline cross-agreement interpreter vs evaluator is 52/52 on the held-out envelopes, so these are coverage defects in the kill check, not a falsification of the 52/52 claim.

## 1. Baseline (pristine bytes, before any mutation)

Scratch `S=/fast/scratch/hyaku/kaidoku-r41/R41W2C2InterpMut` (removed at the end); pristine copies:

```
6ad2b4e1638a2b5f883d7bed14f8863ad5396dbc1af64b7cd521720ea42b6aa4  pristine/sqfs-triage-v3.py
26178d71c0f7634c3f1371ad5c4c7de3b59c49636cdf1b61bf8b2e461c75dce1  pristine/indep-eval-v3.py
94d13b445701609f110ca6512e99f87afbdc00ccee3123b817853107f3cd725c  pristine/SKILL.md
```

- `python3 -I -B pristine/sqfs-triage-v3.py --selftest` → exit 0, `SELFTEST cases=69 pass=69 fail=0`.
- `python3 -I -B pristine/indep-eval-v3.py --selftest` → exit 0, 46 cases, steps 1–12 all covered.
- 52 held-out envelopes fed exactly as `c2-counter.py` feeds them (interpreter: the 52 `envelope.json` paths with `--skill SKILL.md`; evaluator: the same bytes as a flat `<ID>.json` directory):
  interpreter exit 0 with 52 pairs, evaluator exit 0 with 52 pairs, **cross-agreement 52/52, disagree []** — the C2 landing's matched count reproduces at the tool level at the working tree (tip 7a24ff74…).

## 2. Method

41 hand-written mutants (20 interpreter `I*`, 21 evaluator `E*`), each 1–4 minimal exact-string edits; every anchor asserted to occur exactly once in the pristine source before application (`RuntimeError` otherwise; none fired). Per-mutant unified diffs kept in `diffs/`. Kill check per mutant, in order: (1) `--selftest` must exit 0; (2) the 52 held-out `(label, action)` pairs must equal the pristine baseline. A follow-up pass (`pairskill.py`) re-ran the pairs check alone for every selftest-killed mutant to split "killed by both oracles" from "selftest-only kill". Survivors got purpose-built killing-case envelopes (`killcases.py`), each verified by actually running pristine vs mutant on it.

Drivers: `tools/mutdrive.py`, `tools/pairskill.py`, `tools/killcases.py` (in the artifacts dir). No tool installs were needed or made (python3 stdlib only); nothing to record under the 2026-10-19 tooling authorization.

## 3. Interpreter `sqfs-triage-v3.py` — 20 mutants

| id | axis | mutation | verdict | killer |
|----|------|----------|---------|--------|
| I01 | contains-form | `match_set` contains `<=` → `==` | KILLED both | selftest `contains-single-matches-superset`; pairs 17 (C01,C02,C03,C05,C06,C09,C10,H27,H28,H29,H30,H33,…) |
| I02 | exact-vs-contains | exact `==` → contains `<=` | KILLED selftest-only | `exact-single-rejects-superset`; pairs 0; pair-level killer K7 |
| I03 | contains-form | contains direction inverted (`values <= payload`) | KILLED both | selftest `contains-single-matches-superset`; pairs 25 |
| I04 | contains-form | `endswith('+')` guard dropped | KILLED both | selftest `exact-single-matches-singleton`; pairs 3 (C07,H09,H10) |
| I05 | contains-form | member split on `'+'` instead of `','` | KILLED selftest-only | `contains-pair-requires-all`; pairs 0 — every contains cell in the real table is single-member, so the comma syntax is held-out blind |
| I06 | be-token | `-be` token test → substring test | KILLED selftest-only | `be-token-not-substring` (the `-be=1` trap); pairs 0 — no `-be`-substring token in any held-out argv (measured) |
| I07 | be-token | `be = 'yes'` assignment dead | KILLED both | selftest `be-values`; pairs 2 (H19,H20: body-extractor-failure→avm-marker-be-dropped) |
| I08 | sr-detection | diagnostics key `__typename__` → `type` | **SURVIVED** | masked by the raw_result fallback; killer K12 |
| I09 | sr-detection | raw_result dict scan removed | KILLED selftest-only | `sr-from-raw-result`; pairs 0 |
| I10 | p-counting | P collapsed to 0/1 | **SURVIVED** | unkillable by pairs (see §5); features P 5→1 shown |
| I11 | p-counting | files absent reads P=1 | **SURVIVED** | killer K2 |
| I12 | step-order | first-match → last-match (`reversed(rules)`) | KILLED both | selftest `contains-single-matches-singleton`; pairs 12 (C01,C02,C06,C10,H17,H18,H29,H30,H35,H36,H39,H40) |
| I14 | handler-set | `startswith('squashfs')` H-filter dropped | **SURVIVED** | killer K3 |
| I15 | p-counting | `>0` cell accepts P=0 (`<=0`→`<0`) | KILLED both | selftest `published-files-split`; pairs 8 (H05,H06,H17,H18,H19,H20,H37,H38) |
| I16 | contains-form | reserved-word check dropped (contains branch) | KILLED selftest-only | `reserved-word-as-contains-member` |
| I17 | contains-form | duplicate contains member accepted | KILLED selftest-only | `malformed-contains-duplicate` |
| I18 | contains-form | malformed contains member accepted | KILLED selftest-only | `malformed-contains-space` |
| I18b | exact-vs-contains | malformed exact member accepted | KILLED selftest-only | `malformed-contains-trailing-comma` (first failing case) |
| I19 | be-token | BE `n/a` → `no` when no command recorded | KILLED selftest-only | `be-values`; pairs 0; pair-level killer K4 |
| I20 | domain-guard | provider guard dropped | KILLED selftest-only | `domain-guard-provider`; pairs 0 (out-of-domain envelopes deviate on operation too) |

## 4. Evaluator `indep-eval-v3.py` — 21 mutants

| id | axis | mutation | verdict | killer |
|----|------|----------|---------|--------|
| E01 | be-token | `-be` token test → substring test | **SURVIVED** | killer K1; the evaluator selftest lacks the `-be=1` trap its interpreter sibling has |
| E02 | be-token | BE `n/a` → `no` | KILLED selftest-only | `s5-boundary-no-argv`; pairs 0; pair-level killer K4 |
| E03 | sr-detection | `TYPENAME_KEYS` → `("type",)` | KILLED selftest-only | `s8-mixed`; pairs 0 — masked on held-out by the stdout defence (all 13 SR=yes envelopes carry the token in `raw_result.execution.stdout.text` too) |
| E04 | sr-detection | stdout fallback removed | **SURVIVED** | killer K8 |
| E05 | sr-detection | diag-level holder dropped (report-only) | **SURVIVED** | killer K9 |
| E06 | p-counting | files absent reads P=1 | KILLED selftest-only | `b-files-absent-reads-as-p-zero`; pairs 0 (held-out files-absent envelopes are out-of-domain, step 1 masks); pair-level killer K2 |
| E07 | p-counting | P collapsed to 0/1 | **SURVIVED** | unkillable by pairs (see §5) |
| E08 | step-order | step 3 moved after step 4 | **SURVIVED** | killer K5 |
| E09 | step-order | depth-limited checked before step 4 | KILLED both | `s7-partial-precedes-depth`; pairs 5 (C02,C06,C10,H39,H40) |
| E11 | contains-form | step 10 exact `g == {ue}` → membership | KILLED selftest-only | `s10-boundary-singleton-not-met`; pairs 0 — no envelope reaches step 10 with extra gap kinds |
| E12 | step-order | step 8 `sr and ue∈g` → `sr or ue∈g` | KILLED both | `s9-escaping`; pairs 5 (C07,H07,H08,H09,H10) |
| E13 | step-order | LE checked before BE (exact membership) | KILLED selftest-only | `s3-dep-both-be-first`; pairs 0 (no both-dependencies envelope); pair-level killer K6 |
| E13b | exact-vs-contains | substring dependency match, LE first | KILLED both | `s3-dep-be`; pairs 2 (H13,H14) |
| E14 | handler-set | squashfs prefix narrowed to `_be` | KILLED both | `s2-le-handler-is-a-squashfs-handler`; pairs 19 (all le envelopes) |
| E15 | step-order | step-5 HF→H fallback dropped | KILLED selftest-only | `s5-avm-marker-be-dropped`; pairs 0 (held-out avm envelopes record the failing gap's handler) |
| E16 | domain-guard | provider guard dropped | KILLED selftest-only | `s1-pr-binwalk`; pairs 0 |
| E18 | sr-detection | `SR is True` clause dropped in classify | KILLED both | `s8-mixed`; pairs 5 (C11,H07,H08,H11,H12) |
| E19 | p-counting | step 4 `p > 0` → `p >= 0` | KILLED both | `s5-avm-marker-be-dropped`; pairs 6 (H17,H18,H19,H20,H37,H38) |
| E20 | step-order | clean ↔ clean-empty flipped | KILLED both | `s2-le-handler-is-a-squashfs-handler` (first failing); pairs 6 (H01–H06) |
| E21 | step-order | step 2 moved last | KILLED both | `s2-no-handler`; pairs 2 (H23,H24) |
| E22 | be-token | argv keys drop `command` | KILLED both | `s5-avm-marker-be-dropped`; pairs 2 (H17,H18) |

Totals: **41 mutants — 32 killed (15 by both oracles, 17 selftest-only), 9 survived.**

## 5. The 9 survivors, each with a verified killing case

Every killing case below was run against pristine AND mutant; the flip is observed, not predicted. Envelopes in `kill/K*.json`, full runs in `out/killcases-out.json`.

1. **I08** (SR diagnostics key): all 52 held-out envelopes carry `raw_result` containing the `MaliciousSymlinkRemoved` token (measured: 52/52 with raw_result; 13/13 SR=yes envelopes have the token in raw_result too), so the interpreter's second SR path masks the first. Killer **K12** — SR recorded only in `normalized_result.diagnostics[].report.__typename__`, no `raw_result` at all: pristine `escaping-symlink-removed` → mutant `clean`.
2. **I10 / 8. E07** (P collapse to 0/1): demonstrated on K11 (clean envelope, 5 files): pristine features `P=5`, mutant `P=1`, pair `('clean','none')` in both. **No killing case exists in the frozen apparatus**: the table grammar only expresses `0`/`>0`, and the counter's `observed_features_match_declared` binding reads the manifest's `published` (`nonzero`/`zero`) — also magnitude-blind. Only an oracle comparing exact published counts would kill these.
3. **I11** (files absent → P=1): the only held-out envelopes without a `files` key are H25/H26 (out-of-domain), where step 1 decides regardless; the interpreter selftest has no files-absent case (the evaluator's does — `b-files-absent-reads-as-p-zero`). Killer **K2** — in-domain envelope without `files`: pristine `clean-empty` → mutant `clean`.
4. **I14** (H-filter dropped): every held-out chunk handler is `squashfs_v4_be`/`squashfs_v4_le` or absent (measured), and no interpreter selftest case uses a non-squashfs handler. Killer **K3** — `chunks[].handler = "gzip"` only: pristine `no-squashfs-chunk` → mutant `unclassified`.
5. **E01** (BE substring): no argv token in the 52 held-out envelopes contains `-be` as a substring without being `-be` (measured: 0), and the evaluator selftest's trap case (`b-be-token-substring-trap`) uses an argv with no `-be` substring either. Killer **K1** — argv token `-be=1` (the exact shape the interpreter's own `c_be_token_not_substring` uses): pristine `avm-marker-be-dropped` → mutant `body-extractor-failure`.
6. **E04** (stdout SR fallback removed): no stdout-only SR case exists in the evaluator selftest or held-out. Killer **K8** — token only in `raw_result.execution.stdout.text`: pristine `escaping-symlink-removed` → mutant `clean`.
7. **E05** (diag-level holder dropped): real and synthetic envelopes always nest the report object. Killer **K9** — `__typename__` directly on `diagnostics[]`: pristine `escaping-symlink-removed` → mutant `clean`.
9. **E08** (step 3 ↔ 4 swap): held-out dependency envelopes carry only the dependency gap (no `extractor-failure`), and the evaluator selftest has no dep+failure case. Killer **K5** — `missing-extractor-dependency` + `extractor-failure`, P=3: pristine `dep-missing-be` → mutant `partial-body-failure`.

## 6. Pristine divergences the held-out set never exercises

Five synthetic shapes on which the two **unmutated** frozen tools disagree (any future envelope with one of these shapes breaks `matched == 52` with no mutation at all):

| case | interpreter | evaluator | root cause |
|------|-------------|-----------|------------|
| K6 both-dependencies `D={sasquatch,sasquatch-v4be}` | `unclassified` | `dep-missing-be` | interpreter dependency cells are exact sets; evaluator step 3 is membership ("D holds") |
| K7 superset-D `D={sasquatch-v4be,unsquashfs}` at an exact dep row | `unclassified` | `dep-missing-be` | same root; the v3 grammar **rejects** the contains form for the dependencies column (selftest `c_deps_cell_has_no_contains_form`), so the table cannot express step 3's membership semantics on supersets |
| K8 SR token only in `raw_result.execution.stdout.text` | `clean` | `escaping-symlink-removed` | interpreter has no stdout-text defence; evaluator does |
| K9 `__typename__` directly on `diagnostics[]` (no nested report) | `clean` | `escaping-symlink-removed` | interpreter reads only report-nested holders; evaluator reads diag and report |
| K10 token in `raw_result.report[].reports[].__typename__` | `escaping-symlink-removed` | `clean` | interpreter scans raw_result dicts; evaluator does not — this is exactly the envelope shape of the interpreter's own selftest case `c_sr_from_raw_result` |

[INFERENCE] these shapes are reachable from real REA output (trimmed receipts, non-nested reports); the held-out corpus contains none of them, which is why the landing's 52/52 is unaffected.

## 7. Calibration findings

- **The held-out pair oracle killed nothing on its own.** All 32 kills fired at `--selftest`; 15 of those would also have died on pairs, 17 are held-out blind (I02, I05, I06, I09, I16, I17, I18, I18b, I19, I20, E02, E03, E06, E11, E13, E15, E16). The selftest carries the entire kill load.
- **SR detection is double-pathed in both tools** (interpreter: diagnostics report + raw_result dicts; evaluator: diagnostics diag/report holders × 4 keys + stdout text). On held-out data both paths always fire together, so every single-path SR mutation is pair-masked (I08, I09, E03, E04, E05). The interpreter's selftest never exercises its diagnostics path at all (its synthetic envs put SR in raw_result only) — that path is covered only by real held-out data, and there only jointly with the fallback.
- **The real v3 table never uses a multi-member contains cell** (all are single-member: `missing-extractor-dependency+`, `extractor-failure+`, `depth-limited+`, `unpublished-entry+`), so contains-comma parsing (I05) is invisible to the held-out data.
- **P magnitude is invisible to the entire frozen apparatus** (pair oracle and the counter's declared-`published` binding alike): I10/E07 are unkillable by oracle design, not by luck.
- **Asymmetric files-absent coverage**: the evaluator selftest pins absent-`files` → P=0; the interpreter's does not (I11 survives until a trimmed in-domain envelope is tested).

## 8. Bounds, evidence, limits

- Wrote only this report, the artifacts dir `.ufo/waves/round-41/w2/artifacts/R41W2C2InterpMut/`, and scratch `/fast/scratch/hyaku/kaidoku-r41/R41W2C2InterpMut` (removed after staging). No VCS mutation anywhere (mutants ran on scratch copies; no sandbox clone was needed); no lane file outside the two allowed paths touched; no vendor firmware bytes copied or redistributed; no tool installed.
- Key commands and exits: baseline selftests exit 0 / 0; baseline pairs exit 0 / 0 (52 pairs each, cross-agreement 52/52); `python3 -I -B mutdrive.py` exit 0 (`TOTAL 41 mutants: 32 killed, 9 survived`); `python3 -I -B pairskill.py` exit 0 (17 selftest-only kills); `python3 -I -B killcases.py` exit 0 (12 cases, all flips observed).
- Limits: mutants are hand-written single-point edits along the six tasked axes, not exhaustive operator coverage; killing cases are synthetic envelopes built from the precedence text and the tools' own feature readers — they demonstrate oracle sensitivity, not REA behavior; the five divergences are shown on synthetic envelopes only.
- Artifact index: `tools/{mutdrive,killcases,pairskill}.py`; `out/{mutants-results.json,pairs-also-kills.json,killcases-out.json,baseline-interp.tsv,baseline-eval.json,baseline-interp-selftest.txt,baseline-eval-selftest.txt,sweep.log,killcases.log,prep-features.json}`; `kill/` 12 killing-case envelopes; `diffs/` 41 per-mutant unified diffs; `hashes.txt` sha256 of every artifact.
