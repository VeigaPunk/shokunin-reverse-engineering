# MutRegistry — mutation probe of `tools/round-68/registry-conformance.py`

Round 68, wave w1, seat `MutRegistry`. Date 2026-11-03.

- Instrument (frozen, never edited): `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-68/registry-conformance.py`
  sha256 `a300d831c7ef1de47448c2feb8dcbd9ceaf597f7e5f4b996a8e4cc510c6e8315` (confirms the frozen pin).
- Base revision: `fcbe200f6739c38939e0dabf3f251de2cc6bd727`.
- Every mutant is a separate copy under scratch `mut/<ID>.py`; each is scored twice:
  (A) `--selftest` (exit code + printed `cases` + `failed` list) and
  (B) a scoring call `--root <fixture> --rev main` against four scratch git fixtures, plus the
  lane itself at the read-only base revision (which also replays the frozen before-arm).
- The pristine instrument was scored through the same detectors first (baseline column below).

Detector runs are `python3 -I -B`. Pristine baseline: selftest exit 0, 11 cases, `failed: []`;
fixtures behave as designed (`foreign` 0 mismatch, `thin`/`duplicate`/`unregistered` 1 mismatch each);
lane@base: exit 1, `mismatches 2`, `scope_size 69`, `registry_rows 73`, `unregistered` =
`tools/round-67/avm-le-counter.py`, `tools/round-67/mutation-battery.py`. That matches
`l1/pre/c1-at-base.json` exactly (observation), so the baseline is green and a mutant result is
scoreable.

## Scores (full matrix in `scores.tsv`, machine data in `results.json`)

| Mutant | Mutation | `--selftest` | Failing case(s) | Fixture/verdict detector | Verdict |
|---|---|---|---|---|---|
| M1 | drop own-round check | exit 1, prints 11 | `clean`, `empty-registry` | `foreign`: clean→mismatch (scope 1→2, unregistered `tools/round-50/foreign.py`); lane@base: `mismatches 2→7`, `scope 69→77` | **killed** |
| M2 | drop `thin` from `mismatches` | exit 1, prints 11 | `thin-cell` | `thin`: exit 1→0, `mismatches 1→0` while `thin` still names the row | **killed** |
| M3 | drop the duplicate test | exit 1, prints 11 | `duplicate-rows` | `duplicate`: exit 1→0, `duplicate_rows` `[reg.py]`→`[]` | **killed** |
| M4 | `mismatches` = 0 unconditionally | exit 1, prints 11 | `unregistered`, `duplicate-rows`, `row-absent`, `thin-cell`, `empty-registry` | `unregistered`: exit 1→0; lane@base: exit 1→0, `mismatches 2→0` while `unregistered` still names both tools | **killed** |
| M5 | verdict grammar relaxed to `re.search(r"0\|1\|2", cell)` | exit 1, prints 11 | `thin-cell` | `thin`: exit 1→0, `thin` `[reg.py]`→`[]` on a cell naming only codes 0 and 1 | **killed** |
| M6 | drop the `row-absent` case, print the registered 11 | exit 1, prints **11** | `case-inventory` (executed list 10 entries vs `REGISTERED_CASES` 11) | scoring path byte-identical: no fixture or base change (expected, mutation is confined to `selftest()`) | **killed** |
| S1 (supplementary, outside the assigned six) | `registry_rows` = `len(by_path)` (distinct paths, not rows) | exit 0, prints 11 | none | no verdict change anywhere; only signature is the receipt field on `duplicate`: `registry_rows 2→1` | **SURVIVED** |

Baseline-vs-mutant rows for the four fixtures (exit / mismatches): pristine `foreign` 0/0,
`thin` 1/1, `duplicate` 1/1, `unregistered` 1/1. M6 reproduces that row exactly on all four fixtures
and at base (1/2), i.e. its scoring behavior is unmodified (observation from `results.json`).

## Per-mutant detail

### M1 — own-round check dropped
Anchor replaced: `if not tool.startswith(own): continue` → `pass`. A plan's citation of another
round's existing tool now enters its own round's regime.
- `--selftest`: exit 1; `failed = ["clean", "empty-registry"]`. `clean` fails on
  `scope_size == 1` (mutant 2, because `plans/round-67-claims.md` cites `tools/round-50/a.py`);
  `empty-registry` fails because the same foreign path becomes unregistered in an empty registry.
- Fixture `foreign` (round-67 plan cites existing `tools/round-50/foreign.py`, only `reg.py`
  registered): pristine exit 0 / `scope_size 1`; mutant exit 1 / `scope_size 2` /
  `unregistered ["tools/round-50/foreign.py"]`. This is the direct false input: a foreign-cited,
  unregistered tool.
- Live base (read-only): pristine `mismatches 2`, `scope 69`; mutant `mismatches 7`, `scope 77`
  (extra names include `tools/round-27/xpin-attribute.mjs`, `tools/round-39/gen-squashfs.py`,
  `tools/round-40/gen-squashfs.py`, `tools/round-40/score-receipt.sh`). The before-arm predicate
  would also reject the mutant, since it names more than the two round-67 instruments.

### M2 — `thin` not counted
`mismatches` sum loses `+ len(thin)`.
- `--selftest`: exit 1; `failed = ["thin-cell"]`.
- Fixture `thin` (row verdict `0=met; 1=not met`): pristine exit 1 / `mismatches 1` /
  `thin ["tools/round-67/reg.py"]`; mutant exit 0 / `mismatches 0` / `ok true`, with `thin` still
  naming the row (receipt self-contradiction). Killed by the fixture; the base probe cannot catch it
  because the frozen registry has `thin: []`.

### M3 — duplicate test dropped
`duplicate_rows` forced to `[]`.
- `--selftest`: exit 1; `failed = ["duplicate-rows"]`.
- Fixture `duplicate` (two full rows for one path): pristine exit 1 / `mismatches 1`;
  mutant exit 0 / `mismatches 0` / `duplicate_rows []`. Base probe cannot catch it (base has no
  duplicates).

### M4 — constant zero
`mismatches = 0`.
- `--selftest`: exit 1; `failed = ["unregistered", "duplicate-rows", "row-absent", "thin-cell",
  "empty-registry"]` (the `clean` and `legacy-excluded` cases still pass, correctly).
- Fixture `unregistered`: pristine exit 1; mutant exit 0 / `mismatches 0` / `ok true`.
- Live base: pristine exit 1 / `mismatches 2`; mutant exit 0 / `mismatches 0` / `ok true` while the
  same receipt still lists both round-67 tools in `unregistered`. This is a predicate-defeating
  mutant caught twice: by the before-arm exit code and by the receipt's internal inconsistency.

### M5 — relaxed verdict grammar
`VERDICT_RE` collapsed to a single `re.compile(r"0|1|2")`.
- `--selftest`: exit 1; `failed = ["thin-cell"]`.
- Fixture `thin`: pristine `thin ["tools/round-67/reg.py"]`, exit 1; mutant `thin []`, exit 0.
  The cell names only codes 0 and 1, which is exactly the thin case the strict grammar exists to
  catch; the relaxed grammar accepts any digit anywhere. The `verdict-grammar` case still passes
  (its cells name all three codes), so `thin-cell` is the binding case.

### M6 — one case dropped, eleven printed
The `row-absent` census call and its `cases.append` are removed, and the printed count is changed
from `len(cases)` to `len(REGISTERED_CASES)`.
- `--selftest`: exit 1; prints `"cases": 11`; `failed = ["case-inventory"]`.
- Executed tuples: 9 assertion cases + `case-inventory` = 10 (inference from the diff: exactly one
  `cases.append` block is gone). The inventory case derives its list from the executed tuples, so
  the dropped name is detected; the printed 11 is now a constant and no longer evidence of coverage.
- Fixture/base scoring: identical to pristine on all four fixtures and at base — by construction,
  since `census`/`run_score` are untouched. Detector B does not apply to M6.

## Survivors

**Assigned six: none.** Each is killed by `--selftest`, and M1–M5 are independently killed by a
fixture scoring call (M4 additionally by the frozen before-arm). The failing sets are distinct per
mutant, so no two mutants are being caught by the same accidental assertion.

**S1 (supplementary, survived — coverage finding, not a contract change):** replacing
`"registry_rows": len(rows)` with `len(by_path)` passes all 11 cases (no case asserts
`registry_rows`) and changes no exit code or `mismatches` on any fixture or at base. Its only
observable signature is the field value on the `duplicate` fixture: pristine `registry_rows 2`
(two rows) vs mutant `1` (one distinct path), while `mismatches` stays 1 in both. The field is part
of the R68-C1 predicate (`registry_rows 77`), but on a mismatch-clean measured revision duplicates
are empty, so rows == distinct paths and the conflation is observationally equivalent there. The
case that would bind it, per QUALITY #108, is a registry fixture with one duplicated path that
asserts `registry_rows == 2` (two rows, one path) alongside `duplicate_rows == [path]` — i.e. a
case that feeds the mutated expression a false input, not a restatement of the existing
`duplicate-rows` case (which asserts the list and the count only). Not repaired here.

A second latent, non-scoring observation (unknown/design note, not a survivor of these mutants):
`REGISTERED_CASES` is hand-maintained and `case-inventory` compares it to the executed tuple names.
A mutant that drops a case *and* inserts the missing name back into the executed list in the right
position would pass the inventory check. That requires editing the same function that computes the
list, so it is not a plausible accidental defect; reported as an observation only.

## Restoration evidence

- Pristine sha256 before any work: `a300d831c7ef1de47448c2feb8dcbd9ceaf597f7e5f4b996a8e4cc510c6e8315`.
- Pristine sha256 after all probes: `a300d831c7ef1de47448c2feb8dcbd9ceaf597f7e5f4b996a8e4cc510c6e8315`
  (`results.json`: `pristine_unchanged: true`; `stat` size 12558, mtime 1793756177 unchanged).
- `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin status --porcelain -- tools/round-68/registry-conformance.py`
  printed nothing before and after; the lane was never written.
- Mutant sources removed from scratch with the scratch dir; copies and diffs retained under
  `.ufo/waves/round-68/w1/MutRegistry/mut/` and `*.diff`.

## Method notes

- Fixtures were built only under `/fast/scratch/hyaku/kaidoku-r68/MutRegistry/fixtures/*` with
  `git init`/`add`/`commit`; each was preceded by an assertion that
  `git rev-parse --show-toplevel` equals that fixture directory. The lane repo was read-only
  (`ls-tree`, `show`, `log`) throughout; no lane or fleet-repo git mutation, no `jj` command.
- Fixture contents are reconstructed by `mutate.py` (`build_fixtures`), so the deleted scratch is
  reproducible.
- No tools installed or upgraded; no pacman transaction.

Labels: exit codes, case lists, counts and hashes above are observations from executed commands
(`scores.tsv`, `results.json`). M6's executed-case count is an inference from its diff. The S1
binding-case recommendation is an inference. Nothing here is unknown except whether a later
measured revision introduces duplicate rows (not this seat's to measure).
