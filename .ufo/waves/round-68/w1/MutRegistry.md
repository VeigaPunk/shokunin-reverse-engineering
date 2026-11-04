# MutRegistry — mutation-test report (R68-C1 instrument)

Round 68 / w1 / seat `MutRegistry`. Instrument `tools/round-68/registry-conformance.py`
(sha256 `a300d831c7ef1de47448c2feb8dcbd9ceaf597f7e5f4b996a8e4cc510c6e8315`, frozen pin confirmed).
Base revision `fcbe200f6739c38939e0dabf3f251de2cc6bd727`.

## Scope actually executed

Six assigned mutants, each in its own scratch copy, scored by `--selftest` and by a real scoring call
(`--root/--rev`) against four purpose-built git fixtures plus the lane at the frozen base (read-only).
Every mutant was also diffed against the pristine bytes to confirm a single intended anchor changed
(`M1.diff`–`M6.diff`). Full matrix: `scores.tsv`; machine data: `results.json`; per-mutant line,
failing case set and survivor analysis: `mutants.md`.

## Baseline (pristine instrument)

| Detector | Result |
|---|---|
| `--selftest` | exit 0, 11 cases, `failed: []` |
| fixture `foreign` (foreign-round citation, registered own tool) | exit 0, `mismatches 0`, `scope_size 1` |
| fixture `thin` (`0=met; 1=not met`) | exit 1, `mismatches 1`, `thin [tools/round-67/reg.py]` |
| fixture `duplicate` (two rows, one path) | exit 1, `mismatches 1`, `duplicate_rows [tools/round-67/reg.py]` |
| fixture `unregistered` (own tool, no row) | exit 1, `mismatches 1`, `unregistered [tools/round-67/b.py]` |
| lane @ `fcbe200f…` | exit 1, `mismatches 2`, `scope_size 69`, `registry_rows 73`, unregistered = the two round-67 tools |

The lane@base row reproduces `l1/pre/c1-at-base.json` exactly (observation), so the baseline is green
and the before-arm is scoreable.

## Verdicts

| Mutant | Model defect | `--selftest` | Failing case(s) | Independent fixture kill | Verdict |
|---|---|---|---|---|---|
| M1 | own-round check dropped → foreign tool in scope | exit 1 | `clean`, `empty-registry` | `foreign`: 0→1 mismatch, scope 1→2; lane@base 2→7 mismatches, scope 69→77 | **killed** |
| M2 | `thin` removed from `mismatches` | exit 1 | `thin-cell` | `thin`: exit 1→0, mismatches 1→0 (thin still listed) | **killed** |
| M3 | duplicate test dropped | exit 1 | `duplicate-rows` | `duplicate`: exit 1→0, list `[reg.py]`→`[]` | **killed** |
| M4 | `mismatches` 0 unconditionally | exit 1 | `unregistered`, `duplicate-rows`, `row-absent`, `thin-cell`, `empty-registry` | `unregistered`: exit 1→0; lane@base: exit 1→0, mismatches 2→0 while the receipt still lists both unregistered tools | **killed** |
| M5 | grammar relaxed to `re.search(r"0\|1\|2", cell)` | exit 1 | `thin-cell` | `thin`: exit 0, `thin []` on a 0/1-only cell | **killed** |
| M6 | one case dropped, 11 printed | exit 1 | `case-inventory` (10 executed names vs 11 registered) | n/a — scoring path untouched and every fixture/base result identical to pristine | **killed** |

Each of the six exits non-zero under `--selftest`; the failing sets are distinct, so no mutant is
caught only by a shared accidental assertion. M4's constant-zero is additionally refuted by the frozen
before-arm (exit 1 expected, mutant exits 0) and by the mutant receipt's own inconsistency
(`mismatches 0` with two names under `unregistered`). M2's thin mutant likewise reports
`thin [row]` with `mismatches 0`; the fixture catches the exit-code flip regardless of that
inconsistency.

M6 detail: the printed `"cases": 11` is now `len(REGISTERED_CASES)` (a constant), while the executed
list contains 9 assertion cases + `case-inventory` = 10 (inference from the diff). The
`case-inventory` case derives its executed list from the tuples, so the drop is detected even though
the printed count lies. A mutant that dropped a case *and* re-inserted its name into the executed list
would pass the inventory check; it requires editing the same expression that builds the list, so it is
reported as a design observation, not a plausible accidental defect.

## Survivors

- Assigned six: **none**.
- Supplementary probe S1 (`registry_rows = len(by_path)`, distinct paths instead of rows):
  **survived** both detectors. All 11 cases pass; no fixture or base verdict changes. Its only
  signature is `registry_rows 2→1` on the `duplicate` fixture (one path, two rows), where both runs
  still report `mismatches 1`. The field is pinned in R68-C1 (`registry_rows 77`), but on a
  mismatch-clean measured run `duplicate_rows` is empty, hence rows == distinct paths and the
  conflation cannot change the pinned value. QUALITY #108 binding case: a fixture with a duplicated
  path asserting `registry_rows == 2` and `registry_paths == 1` (feeds the mutated expression a false
  input); the existing `duplicate-rows` case asserts only the list and `mismatches`, so it does not
  bind the count. Not repaired here — a survivor is a finding, and the instrument is frozen.

## Restoration / non-mutation evidence

- Pristine sha256 before and after: `a300d831c7ef…c6e8315` both times; `pristine_unchanged: true`
  in `results.json`; size 12558 and mtime 1793756177 unchanged; `git status --porcelain --
  tools/round-68/registry-conformance.py` empty before and after.
- All mutant work lived under `/fast/scratch/hyaku/kaidoku-r68/MutRegistry/`; fixture git repos were
  created only there, each after asserting `git rev-parse --show-toplevel` equalled the fixture dir.
  The scratch dir was deleted before this report; mutant copies and diffs are retained in this wave
  dir. The lane and fleet repos were read-only; no `jj` command; no commits.
- No tools installed; no pacman transaction.

## Files (all absolute)

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-68/w1/MutRegistry.md` (this report)
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-68/w1/MutRegistry/mutants.md`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-68/w1/MutRegistry/scores.tsv`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-68/w1/MutRegistry/results.json`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-68/w1/MutRegistry/mutants.json`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-68/w1/MutRegistry/mutate.py`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-68/w1/MutRegistry/mut/M1.py` … `M6.py`, `S1.py`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-68/w1/MutRegistry/M1.diff` … `M6.diff`, `S1.diff`

Labels: exit codes, counts, case lists and hashes are observations from the runs recorded in
`scores.tsv`/`results.json`. M6's executed-case count and the S1 binding-case recommendation are
inferences. No unknowns affect the verdicts.
