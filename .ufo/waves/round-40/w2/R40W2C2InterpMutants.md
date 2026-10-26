# R40W2C2InterpMutants — mutation test of `tools/round-40/sqfs-triage-v2.py`

**VERDICT: DEFECTS FOUND** — I attacked the enforcement layer behind R40-C2 (depth): the claim that the
frozen v2 interpreter's logic is pinned by its two detectors, the 45-case `--selftest` and the 26 held-out
envelopes scored under SKILL.md rule block 19. Of **32 valid single-logic mutants**, 19 are killed by both
detectors, 6 are killed by the selftest only, and **7 survive both** — each probe-confirmed to be a real
behavioral difference, not an equivalent mutant (evidence below). The frozen interpreter itself was never
modified: it still scores 45/45 selftest and 26/26 held-out, so R40-C2's numbers are not falsified — but the
test coverage around them has named gaps, and one of them (`M03`) is the mutation-side confirmation of a
limit the claims file already discloses.

## What I attacked

The interpreter (`tools/round-40/sqfs-triage-v2.py`, sha256
`336c621c46e78ca528d08597e7ed652c89fe95e31dbfe339fbfd86381c6b8617`, byte-identical at the measured revision
`42c10a58`, at tip `4d62ee5a`, at HEAD and in the worktree) plus its two detectors:

1. `--selftest` — 45 cases (baseline: exit 0, `SELFTEST cases=45 pass=45 fail=0`).
2. Held-out — `python3 -I -B <mutant> --skill SKILL.md corpus/evidence/round-40/c2/heldout/H{01..26}/envelope.json`,
   each `path<TAB>label<TAB>action` line compared to `manifest.json` `label_actions`
   (baseline: exit 0, 26/26 pairs match). This is the same evaluation the C2 counter performs per carrier
   (`c2-counter.py:262 run_interp`, `:665` tab invocation, `:732` `pair_match = label==expected_label and
   action==expected_action`), so a held-out kill is a counter kill.

## Method

```
S=/fast/scratch/hyaku/kaidoku-r40/R40W2C2InterpMutants
mkdir -p "$S"; export TMPDIR="$S" HYAKU_SCRATCH=/fast/scratch/hyaku
cp <lane>/tools/round-40/sqfs-triage-v2.py "$S/pristine.py"     # mutants are scratch copies only
python3 -I -B "$S/mutants/Mxx.py" --selftest                    # detector 1: exit 0 survive / 1 killed
python3 -I -B "$S/mutants/Mxx.py" --skill <lane>/SKILL.md \
    <lane>/corpus/evidence/round-40/c2/heldout/H01/envelope.json … H26/envelope.json
                                                                # detector 2: pair diff or exit != 0 = killed
```

32 mutants, one logic change each (exact old→new strings in `results.json`; regenerable with
`artifacts/R40W2C2InterpMutants/harness.py`). One earlier M27 attempt was a syntax-error mutant
(replacement dropped `return '*'` → IndentationError); it is discarded and not counted — the valid M27
replaces it. Baseline pristine copy: selftest 45/45 exit 0; held-out 26/26 exit 0.

Fidelity note: the worktree `SKILL.md` carried a concurrent sibling append (round-40 instrument registry,
+19 lines at EOF, `git diff` shows insertions only after line 1384). The craft section and v2 table bytes
are untouched by that append; I re-ran the held-out detector for pristine and all 32 mutants against the
pinned `42c10a58` SKILL.md blob (`ab8c7463a2430956…`, 212826 bytes): **0 verdict flips**.

## Results — mutant | selftest kills? | held-out kills? | missing test

| mutant | site (one logic change) | selftest kills? | held-out kills? | missing test |
|---|---|---|---|---|
| M01 | operation guard compare inverted (`!=`→`==`) | KILL (20 cases) | KILL (H01–H24) | — |
| M02 | provider guard compare inverted (`!=`→`==`) | KILL (19) | KILL (H01–H24) | — |
| M03 | operation guard dropped | KILL (2) | **survive** | held-out cannot test the operation cell alone: the out-of-domain class (H25/H26) varies operation AND provider together, so the provider guard alone masks an operation-only defect — the mutation-side confirmation of the claims' disclosed limit ("operation and provider change together in the out-of-domain class, so the provider cell is not tested alone"; symmetrically here, the operation cell is not tested alone) |
| M04 | `classify` iterates `reversed(rules)` (last match wins) | KILL (6) | KILL (H11,H12,H17,H18) | — |
| M05 | marker search keeps scanning (last v2 marker wins) | **survive** | **survive** | no fixture has two v2 markers in one craft section: selftest `c_first_table_wins` uses one marker plus an unmarked second table; the real SKILL.md has one v2 marker in craft. Probe P-M05: two markers/tables → pristine `first`, mutant `second` |
| M06 | exact set compare weakened to subset (`==`→`<=`) | KILL (8) | KILL (H01–H08) | — |
| M07 | set cell `none` accepts any values (`not values`→`True`) | **survive** | **survive** | no fixture pairs a `gap kinds`/`dependencies` `none` row against an envelope carrying a nonempty set where that row precedes the correct row. On the closed 13-class set every such earlier row is blocked by another cell (files/be/sr/handler/gap-exact) — the class set is closed under this mutation, matching the disclosed limit "a table with one load-bearing cell per label can also score a closed class set". Probe P-M07: pristine `rightRow`, mutant `noneRow` |
| M08 | exact set compare widened to superset (`==`→`>=`) | KILL (2) | **survive** | held-out cannot reach the superset direction: the only earlier rows that could newly match are blocked on the current class set (avm row `be=no` vs H19–H22 BE=`yes`; body row `files=0` vs H21/H22 P>0; mixed row `sr=yes` vs H09/H10 SR=`no`) |
| M15 | set-cell repeated-member check disabled | **survive** | **survive** | no selftest case with a repeated set member: `c_malformed_set_cell` only tests the empty member (`unpublished-entry+`). Probe P-M15: `gaps='a+a'` → pristine exit 2, mutant exit 0 |
| M09 | handler fnmatch reduced to exact equality | KILL (12) | KILL (16: H01–H12,H19–H22) | — |
| M10 | `fnmatchcase`→`fnmatch` (normcase) | **survive** | **survive** | equivalent mutant on POSIX: `os.path.normcase` is identity on Linux, so `fnmatch`≡`fnmatchcase` here (probe: both False for case-mismatched handler). The docstring's `fnmatchcase` claim is only observable on case-normalizing platforms — platform-dependent, not actionable in this lane |
| M11 | `>0` row admits P=0 (`<=0`→`<0`) | KILL (1) | KILL (H05,H06) | — |
| M12 | `0` row inverted (`!=0`→`==0`) | KILL (6) | KILL (H05,H06,H19–H22) | — |
| M13 | `handler none` inverted (requires a handler) | KILL (13) | KILL (H01–H24) | — |
| M14 | action-vocabulary membership check disabled | KILL (1) | **survive** | expected: a valid frozen table declares every action it uses, so parse-vocabulary mutants are structurally invisible to held-out scoring; the selftest (`unknown-action`) is the load-bearing detector |
| M16 | duplicate-label check disabled | KILL (1) | **survive** | same reasoning as M14 (`duplicate-label` is selftest-only by nature) |
| M17 | `DEFAULT_LABEL` renamed (`unclassified`→`unknown`) | KILL (5) | KILL (H25,H26) | — |
| M18 | `DEFAULT_ACTION` renamed (`none`→`inspect-input`) | KILL (5) | KILL (H25,H26) | — |
| M19 | `rule_matches` final `return True`→`False` (no row ever matches) | KILL (20) | KILL (H01–H24) | — |
| M20 | `-be` token test inverted (`in`→`not in`) | KILL (6) | KILL (H17–H22) | — |
| M21 | BE default when commands exist flipped `no`→`yes` | KILL (3) | KILL (H17,H18) | — |
| M22 | `names_sasquatch` `startswith`→exact `'sasquatch'` (v4be binary unseen) | KILL (3) | KILL (H17,H18) | — |
| M30 | BE command sources drop `normalized_result.diagnostics` | **survive** | **survive** | no fixture records a sasquatch command only in `normalized_result.diagnostics` (selftest and held-out commands are all visible via `data.diagnostics`/`raw_result`). Probe P-M30: command only under `normalized_result.diagnostics` → pristine `avmR`, mutant `bodyR` |
| M23 | SR diagnostics typename compare inverted (`==`→`!=`) | KILL (1) | KILL (H13–H16) | — |
| M24 | SR `raw_result` fallback disabled | KILL (1) | **survive** | held-out escaping envelopes carry `MaliciousSymlinkRemoved` in `normalized_result.diagnostics`, so the `raw_result` fallback is exercised only by selftest `sr-from-raw-result` |
| M25 | SR raw_result typename compare inverted (`==`→`!=`) | KILL (9) | KILL (12: H01–H06,H09–H10,H13–H16) | — |
| M26 | bare-string provider ignored (`provider_id` forced `''`) | **survive** | **survive** | no fixture records `provider` as a bare string, although the docstring promises "a provider recorded as a bare string is used as is". Probe P-M26: string-provider envelope → pristine `strprov`, mutant `unclassified` |
| M28 | blank-line walk between vocabulary and table disabled | **survive** | **survive** | no fixture has blank lines between the vocabulary line and the table header, although the docstring explicitly allows them ("blank lines between it and the table header are allowed"); selftest `_block` and the real SKILL.md (line 362→363) are both adjacent. Probe P-M28: two blanks → pristine exit 0, mutant exit 2 |
| M29 | blank-line walk unbounded (skips prose too) | KILL (31) | KILL (exit 2, all 26) | — |
| M31 | trailing pipe no longer stripped (extra empty cell per row) | KILL (31) | KILL (exit 2, all 26) | — |
| M27 | domain `*` cell no longer accepted (`**` required) | KILL (1) | **survive** | expected: the frozen table uses no `*` domain cell; the `*` escape hatch is covered only by selftest `c_star_domain_cells` |
| M32 | H collects only handlers exactly `'squashfs'` (`startswith` dropped) | KILL (18) | KILL (H01–H22) | — |

Totals: 32 mutants — 19 killed by both, 6 selftest-only, 7 double survivors. (Requirement was ≥15.)

## The seven double survivors (coverage findings, not contract changes)

Each was probed to prove it is a real behavioral difference (probes in `artifacts/…/probes/`, pristine vs
mutant on a minimal SKILL/envelope):

- **M05 last-marker-wins** — P-M05: pristine `(first, none)` vs mutant `(second, inspect-input)`.
  Missing: one selftest case with two `<!-- sqfs-triage-table v2 -->` markers (each followed by a table) in
  one craft section, expecting the first.
- **M07 `none` set-cell accepts any** — P-M07: pristine `(rightRow, inspect-input)` vs mutant
  `(noneRow, none)`. Missing: one selftest case placing a `deps=none`/`gaps=none` row before the correct row
  on a deps/gaps-bearing envelope. Note this cannot be fixed by adding held-out classes alone: the current
  13-class set is closed under the mutation.
- **M15 repeated set member accepted** — P-M15: pristine exit 2 vs mutant exit 0. Missing: one selftest
  case with `gaps='a+a'` expecting exit 2.
- **M26 bare-string provider ignored** — P-M26: pristine `(strprov, none)` vs mutant
  `(unclassified, none)`. Missing: one selftest case with `"provider": "unblob"` (string) expecting a match.
- **M28 blank-line tolerance removed** — P-M28: pristine exit 0 vs mutant exit 2. Missing: one selftest
  case with blank lines between the vocabulary line and the header expecting exit 0 (the docstring promises
  this tolerance; no fixture exercises it).
- **M30 `normalized_result.diagnostics` BE source dropped** — P-M30: pristine `(avmR, inspect-input)` vs
  mutant `(bodyR, none)`. Missing: one selftest case with the sasquatch command recorded only under
  `normalized_result.diagnostics` (all current fixtures expose commands via `data.diagnostics`/`raw_result`,
  making that source dead code on today's data).
- **M10 `fnmatchcase`→`fnmatch`** — equivalent on POSIX (normcase is identity on Linux; probe shows both
  variants case-sensitive here). Not a test gap on this host; it becomes observable only on
  case-normalizing platforms. Recorded for completeness, not actionable in this lane.

## Held-out-only survivors — why held-out cannot see them

- **M03 (operation guard dropped)**: the only domain-mismatched held-out class (H25/H26) mismatches
  operation *and* provider; the provider guard alone returns them to `unclassified`. This is the
  mutation-side confirmation of the disclosed limit that operation and provider change together in the
  out-of-domain class. A held-out class that mismatches operation only (same provider `unblob`, e.g.
  `inspect_firmware_regions` with `provider.id=unblob`) would kill it — that is a generator change, hence a
  finding for L1, not a defect I may make.
- **M08 (superset)**: unreachable on the current class set — every earlier row that a superset reading
  would newly match is blocked by the `be`/`files`/`sr` cells (details in the table row).
- **M14/M16 (vocabulary/duplicate-label parse checks)**: a valid frozen table cannot exercise malformed-table
  mutants; held-out survival is structural. The selftest is the load-bearing detector here, and it kills both.
- **M24 (raw_result SR fallback off)**: held-out escaping envelopes carry the
  `MaliciousSymlinkRemoved` report in `normalized_result.diagnostics`; the `raw_result` fallback path is
  exercised only by selftest `sr-from-raw-result`.
- **M27 (`*` domain cells rejected)**: the frozen table uses no `*` domain cell; selftest
  `c_star_domain_cells` is the only exercise.

## Held-out feature ground truth (pristine `--json`, all 26)

`OP=extract_firmware` and `PV=unblob` for H01–H24; H25/H26 are `inspect_firmware_regions`/`binwalk`.
BE: `n/a` ×18 (H01–H16, H23–H24), `no` ×2 (H17,H18), `yes` ×4 (H19–H22). SR `yes`: H07,H08,H11,H12 only.
`D` nonempty: H13–H16 only (`sasquatch-v4be` / `sasquatch`). `G` nonempty: H09–H22. P=0: H05,H06,H13–H20,
H23–H26; P>0: the rest. Full per-envelope dump: `artifacts/…/heldout-features.json`. This is what makes the
survivor analyses above exact (e.g. H21/H22 are gzip-wrapped **BE** bodies with `-be` passed, BE=`yes`,
which is why the avm row cannot swallow them under M08).

## Calibration notes for L1

- The seven double survivors are cheap selftest kills (one case each, listed above); none requires touching
  the frozen table, the held-out set, or the interpreter's contract. M10 is POSIX-equivalent — record it as a
  platform note, not a gap.
- M03 is the strongest calibration finding: the held-out set cannot distinguish "operation guard present"
  from "provider guard alone", because its single out-of-domain class varies both cells together. If L1 ever
  widens the out-of-domain class (same provider, different verb), M03 becomes held-out-killable.
- The interpreter's own behavior is intact: pristine selftest 45/45, held-out 26/26, both on the worktree
  SKILL.md and on the pinned `42c10a58` blob.

## Tooling

No tools installed, upgraded, or removed (no pacman/uv/npx/cargo activity); sasquatch, sasquatch-v4be and
unblob untouched. No vendor bytes downloaded or copied (none needed — the mutation test uses committed
fixtures only).

## Bounds compliance and restoration evidence

- Writes: this report and `artifacts/R40W2C2InterpMutants/` only (`results.json`, `heldout-features.json`,
  `harness.py`, `mutants/M01..M32.py`, `probes/P-M05…P-M30`). No writes to `corpus/`, `tools/`, `plans/`,
  `SKILL.md`, or anywhere else in the lane or fleet; no sibling files touched.
- VCS: no git/jj mutation of any kind (not even read-only git was needed beyond the `git show`/`git diff`/
  `git status` used above, all read-only).
- Restoration: the lane tool was never modified — mutants are scratch copies. sha256 of
  `tools/round-40/sqfs-triage-v2.py` before == after ==
  `336c621c46e78ca528d08597e7ed652c89fe95e31dbfe339fbfd86381c6b8617`, identical to the blobs at `42c10a58`,
  tip `4d62ee5a`, and HEAD; `git status --porcelain -- tools/round-40/sqfs-triage-v2.py` is empty.
- Scratch `/fast/scratch/hyaku/kaidoku-r40/R40W2C2InterpMutants` removed at the end of the run.
