# R39W2TriageMutants — mutation test of the frozen `tools/round-39/sqfs-triage.py`

**VERDICT: DEFECTS FOUND** — R39-C2's 20/20 is real and reproduces (author counter exit 0 / `met_target: true` at the freeze rev 6fdaf4f1 *and* at HEAD e40a25df; my independent harness agrees 20/20 with selftest 35/35), but **18 of 39 single-logic mutants survive both detectors** (held-out labels *and* `--selftest`). The held-out set + selftest pin a much narrower slice of the interpreter than the table grammar implies. Per the seat rules these survivors are coverage findings, not license to change the contract; the frozen interpreter itself was never modified.

## What was attacked

R39-C2 (depth): SKILL.md craft rule block 18 (triage table after `<!-- sqfs-triage-table v1 -->`), interpreter `tools/round-39/sqfs-triage.py`, held-out set `corpus/evidence/round-39/c2/heldout/` (manifest seed = freeze hash 8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b, 10 classes × 2 = H01..H20). Author verdict "met, `c2-counter.py` 20/20 at 6fdaf4f1".

Method: single-logic mutants applied to **scratch copies** of the interpreter (lane file never written). Detector per mutant:

1. label the 20 committed envelopes `heldout/H*/envelope.json` with the working-tree `SKILL.md` (sha256 f31ebd6339e9fff3396e04886acd65f5a283ffb14b3136e17499493b5dbe23b78; craft table block byte-identical to the freeze — `diff` of the marker region at 6fdaf4f1 vs HEAD: empty) and count agreements with `manifest.json` labels;
2. run the mutant's own `--selftest` (35 cases; expects exit 0).

Baseline (pristine copy, sha256 ef4a8a8b7428cf7221dd3aa16bc587507d308b1eacf01074def276e744beacf2 — byte-identical to the freeze, `git diff --quiet 6fdaf4f1 -- tools/round-39/sqfs-triage.py` clean): **labels 20/20, selftest `cases=35 pass=35 fail=0`, exit 0.** A mutant is KILLED-LABELS (<20), KILLED-RUNFAIL (labeling run crashed), KILLED-SELFTEST-ONLY (20/20 labels, selftest fails), or SURVIVED (both clean).

## Corpus facts that decide survivability (pristine `--json` + envelope inspection, `results/base.json`)

- Every held-out envelope has **exactly 1 chunk** (H17/H18: **0 chunks**); every handler is `squashfs_v4_be` or `squashfs_v4_le`. **No non-squashfs handler exists anywhere in the corpus.**
- Every envelope has **≤1 extraction gap, ≤1 dependency, ≤1 unpublished entry** — a flat corpus; no multi-gap/multi-dep case exists.
- Recorded sasquatch commands: **only bare `sasquatch-v4be …` strings** (no path prefix), **at most one per envelope**, and only in the six failing arms H13–H16, H19, H20 (`sasquatch-v4be -no-exit-code -f -d …` for AVM, `sasquatch-v4be -be -no-exit-code -f -d …` for body/version-minor). Successful and dep-missing arms record **no command at all** → `BE='n/a'` there. **A plain `sasquatch` (LE) command is never recorded anywhere** — held-out or selftest fixtures.
- `MaliciousSymlinkRemoved` appears in **both** `normalized_result.diagnostics[0].report` **and** somewhere under `raw_result` for H05/H06.

## Full mutant table (39 mutants; per-envelope flips in `results.json`)

| # | mutant | single-logic change | labels | selftest | verdict | flips |
|---|--------|---------------------|--------|----------|---------|-------|
| 1 | H-exact-v4be | H filter `startswith('squashfs')` → `== 'squashfs_v4_be'` | 16/20 | fail | KILLED-LABELS | H03,H04,H11,H12 → no-squashfs-chunk |
| 2 | H-prefix-squash | prefix `'squashfs'` → `'squash'` | 20/20 | pass | **SURVIVED** | — |
| 3 | H-no-filter | drop the squashfs-prefix filter (count all handlers) | 20/20 | pass | **SURVIVED** | — |
| 4 | H-lower | case-insensitive H filter | 20/20 | pass | **SURVIVED** | — |
| 5 | G-first-kind-only | G union → first kind only | 20/20 | fail | KILLED-SELFTEST-ONLY | exact-gap-superset |
| 6 | GD-first-gap-only | `break` after first gap (G and D) | 16/20 | fail | KILLED-LABELS | H09–H12 → unclassified (D emptied) |
| 7 | G-nonstr-included | drop `isinstance(kind, str)` guard | 20/20 | pass | **SURVIVED** | — |
| 8 | D-last-wins | D union → last dep wins | 20/20 | fail | KILLED-SELFTEST-ONLY | exact-dep-superset |
| 9 | D-nonstr-included | drop `isinstance(dep, str)` guard | 20/20 | pass | **SURVIVED** | — |
| 10 | BE-substring | `-be` token test → substring in raw cmd | 20/20 | fail | KILLED-SELFTEST-ONLY | be-token-not-substring |
| 11 | BE-token-prefix | `-be` token test → `startswith('-be')` | 20/20 | fail | KILLED-SELFTEST-ONLY | be-token-not-substring |
| 12 | BE-first-cmd-only | BE scans `commands[:1]` only | 20/20 | pass | **SURVIVED** | — |
| 13 | BE-any-to-all | BE any-command → all-commands | 20/20 | pass | **SURVIVED** | — |
| 14 | BE-invert-yes-no | BE default `'no'` → `'yes'` | 18/20 | fail | KILLED-LABELS | H13,H14 avm→body-extractor-failure |
| 15 | BE-na-to-no | `n/a` → `no` when no command | 6/20 | fail | KILLED-LABELS | H01–H12,H17,H18 → unclassified |
| 16 | SQ-exact-name | basename `startswith('sasquatch')` → `== 'sasquatch'` (drops `-v4be`) | 14/20 | fail | KILLED-LABELS | H13–H16,H19,H20 → unclassified |
| 17 | SQ-v4be-only | only `sasquatch-v4be` counts (drops plain sasquatch) | 20/20 | pass | **SURVIVED** | — |
| 18 | SQ-substring | basename test → `'sasquatch' in token` | 20/20 | pass | **SURVIVED** | — |
| 19 | SQ-no-basename | drop `rsplit('/', 1)` basename strip | 20/20 | pass | **SURVIVED** | — |
| 20 | SR-diagnostics-only | remove raw_result SR fallback | 20/20 | fail | KILLED-SELFTEST-ONLY | sr-from-raw-result |
| 21 | SR-raw-only | remove diagnostics SR scan | 20/20 | pass | **SURVIVED** | — |
| 22 | SR-substring | typename equality → substring | 20/20 | pass | **SURVIVED** | — |
| 23 | SR-invert | SR default `'no'` → `'yes'` | 4/20 | fail | KILLED-LABELS | H01–H08 → escaping-symlink-removed; H09–H20 → unclassified |
| 24 | P-unpublished-swap | P reads `unpublished_entries` instead of `files` | 14/20 | fail | KILLED-LABELS | H01–H06 → unclassified |
| 25 | P-bool | P = `bool(files)` | 20/20 | pass | **SURVIVED** | — (P type int→bool only) |
| 26 | P-plus-unpublished | P += unpublished entries | 20/20 | pass | **SURVIVED** | — (P +1 on H07/H08 only) |
| 27 | CMD-dedup-drop | drop command dedup | 20/20 | pass | **SURVIVED** | — |
| 28 | RM-last-match | first match wins → last match wins | 20/20 | fail | KILLED-SELFTEST-ONLY | first-match-order |
| 29 | RM-star-false | `*` cells never match | 16/20 | fail | KILLED-LABELS | H05,H06,H17,H18 → unclassified |
| 30 | RM-none-inverted | set-cell `none` → matches nonempty | 8/20 | fail | KILLED-LABELS | H01–H04,H07,H08,H13–H20 → unclassified |
| 31 | RM-hnone-inverted | handler `none`: reject H-empty → reject H-nonempty | 6/20 | fail | KILLED-LABELS | H01–H12 → no-squashfs-chunk; H17,H18 → unclassified |
| 32 | RM-exact-superset | exact set → table ⊆ envelope | 20/20 | fail | KILLED-SELFTEST-ONLY | exact-gap-superset, exact-dep-superset |
| 33 | RM-exact-subset | exact set → envelope ⊆ table | 16/20 | fail | KILLED-LABELS | H01–H04 clean → dep-missing-be/le |
| 34 | RM-fnmatch-equals | `fnmatchcase` → string equality | 12/20 | fail | KILLED-LABELS | H01–H08 → unclassified |
| 35 | RM-fnmatch-nocase | `fnmatchcase` → `fnmatch` | 20/20 | pass | **SURVIVED** | — |
| 36 | RM-files-gt0-dead | `>0` cells never match | 12/20 | fail | KILLED-LABELS | H01–H08 → unclassified |
| 37 | RM-files-zero-dead | `0` cells match any P | 14/20 | fail | KILLED-LABELS | H13–H16,H19,H20 → unclassified |
| 38 | RM-gt0-loose | `>0` rejects only P<0 (accepts P=0) | 20/20 | pass | **SURVIVED** | — |
| 39 | RM-zero-loose | `0` rejects only P<0 (accepts P>0) | 20/20 | pass | **SURVIVED** | — |

**Totals: 39 mutants — 18 SURVIVED, 14 KILLED-LABELS, 7 KILLED-SELFTEST-ONLY, 0 run-failures.** Exact old→new pairs for every mutant: `artifacts/R39W2TriageMutants/mutants-diff.txt`.

## Which features does the 20/20 actually depend on?

All six features are load-bearing somewhere, but each only through a narrow slice:

- **H** — only the **be/le discrimination** is pinned (mutant 1: LE envelopes collapse into `no-squashfs-chunk`). The `'squashfs'` prefix filter itself is unpinned: no held-out envelope contains a non-squashfs handler (H17/H18 have zero chunks), so mutants 2–4 are equivalent on the corpus. The single most load-bearing line is the **handler-`none` early reject** in `rule_matches` (mutant 31: 14 flips) — without it, rule 1's remaining cells (`be=n/a` + wildcards) swallow H01–H12.
- **G** — singleton presence/absence and exact values are pinned (mutants 29–31, 33). The **union across gaps is unpinned by the held-out set** (mutant 5 survives labels; killed only by the selftest's constructed two-gap envelope). The `isinstance(kind, str)` guard is unpinned (mutant 7).
- **D** — singleton exact values are pinned (rules 2/3; mutant 6 kills via emptied D; mutant 33 shows empty-D envelopes are one subset-semantics step away from `dep-missing-*`). **Union across gaps/dependencies is held-out-unpinned** (mutant 8 survives labels, selftest-only kill); the str guard is unpinned (mutant 9).
- **BE** — all three values are pinned: `n/a` (mutant 15: 14 flips — every command-less envelope), `'no'` default (mutant 14: H13/H14 pin it), `'yes'` via a `-be` token on a `sasquatch-v4be`-named command (mutant 16: 6 flips). But token **exactness** (10–11), **aggregation over commands** (12–13, 27), the **LE basename half** (17 — plain `sasquatch` is dead code on this corpus), and the **basename strip** (19) are all unpinned by both detectors.
- **SR** — the yes/no distinction is pinned (mutant 23: 16 flips). The **two detection sites are redundant on this corpus**: H05/H06 carry the typename in both diagnostics and raw_result, so removing the diagnostics scan (21) is a full survivor; the raw_result fallback is pinned only by the selftest's constructed envelope (20 = selftest-only kill). Typename exactness unpinned (22).
- **P** — must read `nr.files` (mutant 24: 6 flips) and only **zero vs nonzero** is consumed: mutants 25/26 change P's value/type on H01–H08 with zero label changes, and both boundary **exclusion** directions are unpinned (38/39: no detector case forces a `>0` rule to reject a P=0 envelope or a `0` rule to reject a P>0 envelope — rule order always masks it). The inclusion directions are pinned (36/37: 8 and 6 flips).

## Pinned only by the selftest (labels stay 20/20)

BE token exactness (10, 11), G union across gaps (5), D union across deps (8), exact-set superset direction (32), first-match order (28), SR raw_result fallback (20). Seven logic points owe their only pin to constructed selftest envelopes, not to the held-out set.

## Survivors = coverage findings (18)

1. **H filter precision** (H-no-filter, H-prefix-squash, H-lower): the corpus cannot see the filter — it has no non-squashfs handler to exclude. A future envelope with e.g. a `cpio` chunk plus a squashfs arm would distinguish them; today nothing does.
2. **sasquatch basename forms** (SQ-no-basename, SQ-substring, SQ-v4be-only): the corpus records only bare `sasquatch-v4be …` strings. Path-prefixed binaries, plain-`sasquatch` LE commands, and mid-token occurrences are untested; the docstring's "any extractor command naming sasquatch" has a dead LE half on this corpus.
3. **BE aggregation** (BE-first-cmd-only, BE-any-to-all, CMD-dedup-drop): ≤1 sasquatch command per envelope everywhere → any-vs-all, first-vs-all, and dedup are unpinned.
4. **G/D guard looseness** (G-nonstr-included, D-nonstr-included): all kinds/deps are strings on this corpus.
5. **P granularity** (P-bool, P-plus-unpublished): only zero/nonzero is consumed; exact count and the files-vs-unpublished distinction are unpinned.
6. **files boundary exclusions** (RM-gt0-loose, RM-zero-loose): the `0`/`>0` split is pinned only one-sided (inclusion); the exclusion directions are masked by rule order.
7. **fnmatch case sensitivity** (RM-fnmatch-nocase): `fnmatch` vs `fnmatchcase` are equivalent under POSIX `normcase`; untested.
8. **SR site redundancy** (SR-raw-only): the diagnostics scan is fully masked by the raw_result walk on this corpus.

## Answers to the seat's questions

- **Which features does the 20/20 actually depend on?** All six, but minimally: H (be/le + the handler-`none` reject), G/D (singleton presence + exact values + `none`/`*`/exact-set semantics), BE (three-valued via single v4be-named commands), SR (yes/no), P (zero/nonzero from `nr.files`). The prefix filter, set unions, command aggregation, LE basename path, P's count, and the files-boundary exclusions are **not** depended on.
- **Which mutants survive both?** The 18 in the table: H-prefix-squash, H-no-filter, H-lower, G-nonstr-included, D-nonstr-included, BE-first-cmd-only, BE-any-to-all, CMD-dedup-drop, SQ-v4be-only, SQ-substring, SQ-no-basename, SR-raw-only, SR-substring, P-bool, P-plus-unpublished, RM-fnmatch-nocase, RM-gt0-loose, RM-zero-loose. Sixteen are feature-equivalent on all 20 envelopes; P-bool/P-plus-unpublished change feature values (type / +1 on H07/H08) with no label change.

## Reproduction

```
S=/fast/scratch/hyaku/kaidoku-r39/R39W2TriageMutants        # removed afterwards
python3 mutate.py base        # pristine: 20/20, selftest 35/35, exit 0
python3 mutate.py chunk i j   # 39 mutants in slices; labels + selftest per mutant
python3 mutate.py merge       # results.json (39 records)
python3 mutate.py verify      # survivor --json feature-diff vs pristine
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && TMPDIR=$S/tmp python3 -I -B \
  tools/round-39/c2-counter.py --root "$PWD" --rev <rev> \
  --freeze 8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b --json-out <artifacts>/c2-counter-at-<rev>.json
# → exit 0, matched 20/20, met_target true at 6fdaf4f1 and at HEAD e40a25df
```

Artifacts (all under `.ufo/waves/round-39/w2/artifacts/R39W2TriageMutants/`): `mutate.py` (harness), `mutants-diff.txt` (exact edits), `results.json` (all 39 records with per-envelope flips), `results/base.json` (pristine features), `results/verify.json` (survivor equivalence), `results/chunk-*.json`, `c2-counter-at-freeze.json`, `c2-counter-at-head.json`.

## Bounds, tooling, restoration evidence

- Lane `tools/round-39/sqfs-triage.py` **never written**: sha256 `ef4a8a8b7428cf7221dd3aa16bc587507d308b1eacf01074def276e744beacf2` before and after the whole run; all mutants were separate copies under `$S/mutants/`. SKILL.md and the held-out set only read. No git/jj mutation; no sibling files touched; nothing written outside the report path and the artifacts dir.
- Tooling: **nothing installed** (python3 stdlib only; no pacman/uv/npm usage; no tool versions to record).
- Limits: the mutant set covers the tasking's named points plus three value inversions and two files-dead probes — it is not an exhaustive statement-level mutant space. Survivors are equivalence-on-this-corpus findings, not proofs of insensitivity outside it. Selftest fixtures (round-38 evidence, R38W2AvmProbe envelopes) were read, never written. Scratch removed on finish.
