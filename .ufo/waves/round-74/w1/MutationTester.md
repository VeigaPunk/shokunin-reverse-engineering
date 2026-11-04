# MutationTester — round-74 record-audit atom attack (r74-w1)

Seat: mutation-tester. Target: `tools/round-74/record-audit.py` ATOMS, attacked in scratch
copies only. The lane file was never edited: sha256 `5bcd1462ee25c3ab3ef92f5ff22eda43bfc15dbbca15750f4c678eb9b1a32c5c`
before and after all runs; `git status --porcelain -- tools/round-74/` empty throughout.
Scratch root `/fast/scratch/hyaku/kaidoku-r74/MutationTester/` (deleted before this report's yield).

## Method

Five scratch copies of the instrument (byte-identical clones, sha `5bcd1462…`), one semantic
mutation each. Every copy ran `python3 -I -B <copy> --root <lane> --rev <rev> --json-out <receipt>`
at base `04fdc2c4dbedbe5ee50a069af14310068393233e`, freeze `021914c0e638454e507087accfe41af1ab69f185`,
and current tip `5ba6a2181a23c2a52628b14d6884ab0159f6747b`, plus `--selftest`. All data is read via
`git show`, so sibling seats' uncommitted work could not contaminate runs.

Baseline (required for conclusive verdicts): pristine at base returned rc 1,
`mismatch_count 11`, mismatches `D3, D6, D7b, D8, D9, D10, D11, D12, D13, D14, D15` — exactly the
frozen receipt `.ufo/waves/round-74/pre/c2-at-base.json` (count 11, same names, `rev 04fdc2c4…`).
Baseline reproduces the committed evidence → verdicts below are conclusive, not inconclusive.

Detector = the two committed distinguishers named in the assignment: (a) the frozen base receipt —
a mutant whose base rc / mismatch set differs from the frozen receipt cannot have produced it;
(b) the audit's own `--selftest` (12 parser cases). Freeze/tip runs are supplementary context.

## Result table

| mutant | semantic mutation (scratch copy sha256[:12]) | rc / failures at base | selftest verdict | verdict |
|---|---|---|---|---|
| D8 | drop the resolve conjunct: `ok = (r73>=3 and r74>=2)` — accepts a capability row with a dangling evidence pointer (`9e8cc25b39dc`) | rc 1, count 11, set identical to frozen receipt | rc 0, 12 cases, 0 failures — identical to pristine | **SURVIVOR** — neither distinguisher sees it |
| D9 | accept the round-72 entry: `ok = used and (R73_ENTRY in used or basename(KNOWLEDGE_R72) in used)` (`17584053f1dc`) | rc 1, **count 10** — `D9_s275_used_by` flips ok (base cell names `…r72-checker-env-capsule.md`) | rc 0, 12 cases, 0 failures — identical to pristine | **KILLED** by the committed base receipt `pre/c2-at-base.json`, which names `D9_s275_used_by` |
| D11 | drop one required page: `R73_REJECTED_PAGES[:3]` (drops `index.html#_section_5`) (`ed2206356d0d`) | rc 1, count 11, set identical to frozen receipt | rc 0, 12 cases, 0 failures — identical to pristine | **SURVIVOR** — neither distinguisher sees it |
| D13 | accept a file without the trailing newline: `ok = text is not None` (`42d663d90c60`) | rc 1, **count 10** — `D13_readme_newline` flips ok (base README ends `'ity.'`) | rc 0, 12 cases, 0 failures — identical to pristine | **KILLED** by the committed base receipt `pre/c2-at-base.json`, which names `D13_readme_newline` |
| D14 | accept a receipt with no runner binding: `ok = bool(receipt) and blob is not None` (`b470f4befd49`) | rc 1, count 11, set identical to frozen receipt | rc 0, 12 cases, 0 failures — identical to pristine | **SURVIVOR** — neither distinguisher sees it |

## Why the survivors survive (named debt, exact case each needs next round)

The base receipt kills a mutant only when the mutated conjunct is the atom's *sole* failure reason
at base. For D8/D11/D14 the base failure reason is a different conjunct, and `--selftest` never
executes any atom (its 12 cases exercise parser helpers: `section`, `first_lines`, `split_row`,
`table_rows`, `row_for`, D7b selection logic, used-by cell extraction, `str.endswith`) — so the
selftest distinguishes none of the five mutants. Structural finding: **the atoms have no red-arm
coverage; only D9 and D13 are pinned, and only by the frozen before-world receipt.**

- **D8 survivor.** At base the atom fails on row counts (`r73: 0, r74: 0` over 31 table rows,
  `unresolved: []`), so removing the resolve conjunct changes nothing; at freeze and tip the atom is
  still red for the same reason (the round-73/74 capability rows are not in any committed SCORECARD
  yet). When the landing makes it green, a dangling pointer would also be green.
  *Named case needed:* `capability-pointer-unresolved-red` — a fixture capabilities body with
  r73=3 and r74=2 rows where exactly one row's evidence pointer is a non-existent path; the atom
  must fail. Requires an atom-level selftest hook (feed a synthetic scorecard body to
  `atom_capability_rows`).
- **D11 survivor.** At base all four required pages have 0 rejected rows (`per_page` all 0 over 11
  pre-existing rejected rows for other pages), so requiring three instead of four unsatisfied pages
  is indistinguishable; same at freeze/tip (still all 0). At the landing all four are present, and a
  dropped requirement is invisible there too.
  *Named case needed:* `rejected-pages-one-missing-red` — fixture registry with `rejected` rows for
  `proc.5.html`, `proc_cmdline.5.html`, `proc_pid.5.html` but none for `index.html#_section_5`;
  the atom must fail.
- **D14 survivor.** `R74_PRE` (`pre/c1-base-arm.json`) does not exist at base, so the atom is red
  under both versions (`receipt: null`); at freeze and tip the receipt exists with a correct binding,
  so both are green. The `path == PROMUT` and `sha256 == blob` conjuncts are bound by no committed
  evidence and no selftest case.
  *Named case needed:* `runner-binding-wrong-sha-red` (and optionally `runner-binding-wrong-path-red`)
  — fixture receipt whose `runner.sha256` is a stale hash of the probe blob (resp. wrong path); the
  atom must fail.

D9 and D13 need no new case: the frozen receipt already kills them. (An atom-level selftest red arm
`used-by-r72-entry-red` would be nice-to-have but is not debt.)

## Supplementary observations (context, no claim scored)

- At every revision measured the pristine audit is red: count 11 at base `04fdc2c4`, **9 at the
  freeze `021914c0` and 9 at the current tip `5ba6a218`** (mismatches `D3, D6, D7b, D8, D9, D10,
  D11, D12, D13`). The record repairs have not landed in any commit as of this probe; the C2
  "mismatch_count 0 at the landing revision" state does not yet exist in the lane's history.
  D14 and D15 are already green at the freeze.
- D9 and D13 mutants flip their atom at freeze and tip as well (count 8 vs pristine 9) — the
  distinguishability of these two mutants does not depend on the landing.
- No claim is made here about runtime behaviour of the lane; this probe measures only what the
  committed evidence distinguishes.

## Receipts

All 20 run receipts in `.ufo/waves/round-74/w1/MutationTester/`:
`summary.json` (matrix + verdict booleans + watch-atom evidence), `selftest-pristine.json`, and
`{pristine,D8,D9,D11,D13,D14}.{base,freeze,tip}.json` (18 audit receipts exactly as the copies
wrote them). Restoration evidence: lane `tools/round-74/record-audit.py` sha256
`5bcd1462ee25c3ab3ef92f5ff22eda43bfc15dbbca15750f4c678eb9b1a32c5c` before and after; no lane file
other than this report and the receipt directory was written; scratch deleted.
