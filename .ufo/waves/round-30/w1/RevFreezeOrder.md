# RevFreezeOrder — instrument/freeze order and pre-freeze data audit (round 30, wave 1)

Scope: were the R30 instruments and frozen inputs committed before the claims file,
and was no REA data on any carrier or mutant committed or (as far as the repository
shows) produced before the freeze? Verdicts against corpus/QUALITY.md rows 33 and 38.
All commands run in /home/vgpnk/Projects/shokunin/kaidoku-shokunin (lane), read-only,
2026-10-23 ~02:30–02:47Z. Freeze committer time 4ee65c67 = 2026-10-23T02:35:13Z.

## Commit order table

`git log --format='%H %cI %s' d210fb8f..main` (observation, exit 0):

| order | commit | committer time (UTC) | role | content (`git show --stat`) |
|---|---|---|---|---|
| base | d210fb8fa62d | 2026-10-22T20:51:49Z | lane base | — |
| 1 | 0dbabf78b6ab | 2026-10-23T02:34:24Z | instruments + frozen inputs | 6 files, +977: tools/round-30/{rust_dep_oracle.py, c1-rust-positive.py, c2-rust-refusals.py}, corpus/evidence/round-30/c1/{carriers.tsv, pypi-uv-0.13.0.json}, c2/predictions.tsv |
| 2 | 4ee65c677105 | 2026-10-23T02:35:13Z | freeze | 1 file, +74: .ufo/waves/round-30/claims.json |

`main` == `4ee65c67` == `HEAD` at audit time; no commits after the freeze.
First-add checks: `git log --all --diff-filter` shows claims.json first added by
4ee65c67 on main; the instrument commit precedes it by 49 s. Order holds.

## Pin table (sha256 of `git show <rev>:<path>` vs claims.json)

Claims pins: instruments {oracle f0b144c6…, c1 e07563d6…, c2 1c357fca…};
frozen_inputs {carriers.tsv c968cd1e…, pypi-uv-0.13.0.json 2eaed6c8…,
predictions.tsv 6852df3a…}. `git show $rev:$p | sha256sum` for all six paths at
4ee65c67 and at main: **all six match at both revisions, identical across them**
(observation). Pins are full sha256s, not bare names; no `instrument_supersessions`
needed since no instrument byte changed after the freeze. instrument_commit field
(0dbabf78) names the actual first-add commit of all six files (observation).

Working-copy jj snapshots (refs/jj/keep) d15bd668 and 7d9a24d1 (parent d210fb8f,
committer time equal to 0dbabf78) and 8a268fbc (parent 0dbabf78, same time as
4ee65c67) contain the same six paths plus claims.json in 8a268fbc; all blob ids are
**identical** to the main-line versions (claims.json blob 5180ffaa in both
8a268fbc and 4ee65c67). They are not ancestors of main; they duplicate, never
anticipate or alter, the pinned content. No envelopes/runs.tsv in any snapshot.

## Data absence at/before freeze

`git ls-tree -r --name-only <rev> -- corpus/evidence/round-30 | grep -E 'envelopes|runs\.tsv'`
at d210fb8f, 0dbabf78, 4ee65c67, main: **(none)** at all four (observation, exit 0).
`git log --all -- corpus/evidence/round-30` shows only 0dbabf78 (+ the two byte-
identical jj snapshots). `git status --porcelain`: no untracked or modified path
under corpus/evidence/round-30 or tools/round-30; the only untracked round-30 paths
are .ufo/waves/round-30/{before/,w1/,w1-*.json,w1-dispatched-at.txt}, all post-freeze
(observation). Conclusion: no REA data on any carrier or mutant committed at or
before the freeze — observation.

## pre_freeze_probe check

claims.json asserts: "none of REA on any carrier or mutant" before the freeze; only
readobj screens, oracle runs, and a node zlib probe.

- Scratch audit: every file under /fast/scratch/hyaku/kaidoku-r30/ outside
  wheels/, carriers/, mutants/, seats/ with mtime < 02:35:13Z is exactly one file:
  `uv-0.13.0.json` (23:21:10Z local = 02:21:10Z UTC, the PyPI fetch). Wheel members
  carry archive mtimes (1980); carriers were extracted 02:26:45Z, mutants dir 02:32Z.
  No envelope-shaped output file predates the freeze (observation).
- npm evidence: ~/.npm/_logs contains rea-agents debug logs only from
  02:45:45–02:45:51Z (post-freeze wave-1 selftest runs). npx cache dir
  ad9a3fdbcad992c6 btime 2026-10-22T08:21:54Z (rea-agents 6.5.0, package.json
  sha256 a5003023… matches claims' rea_pin) — the binary existed ~18 h before the
  freeze, so "could not have run" is NOT provable from install time (observation;
  absence of run output is what the repo/logs show, not impossibility).
- Mutant/carrier byte integrity: sha256 of all 19 mutants == predictions.tsv
  sha256 column (19/19); all 16 carriers == carriers.tsv sha256 column (16/16)
  (observation, python3 hashlib). Mutant mtimes 02:35:15Z and 4 carrier mtimes
  02:42–02:43Z are post-freeze touches consistent with the counter's deterministic
  rebuild (`mutants=19 rebuilt pin_mismatch=0` in the before receipt) and a seat's
  re-extraction; bytes are byte-identical to the frozen pins (inference from
  matching sha256; mtime touch noted, contents provably unchanged).
- before/ receipts (untracked, written 02:35:15Z, post-freeze): c1 at d210fb8f →
  `PIN pinned input absent … exit=2`; c1 selftest `cases=25 failures=0`; c2 →
  `mutants=19 rebuilt pin_mismatch=0` + `PIN predictions file differs … exit=2`;
  c2 selftest `cases=16 failures=0` (observation of file contents).

## QUALITY row 33 — verdict: HOLDS

Instruments committed before claims.json (49 s), pinned by sha256 at the freeze,
freeze commit = first adder of claims.json on main, instrument files unchanged at
main (no undisclosed post-freeze change, no supersession needed, no absent-at-freeze
instrument). The R23/R19 failure pattern (instrument absent at freeze) does not
apply. Observation-backed.

## QUALITY row 38 — verdict: HOLDS (with residual notes)

- Instrument + red fixtures in one commit before the data: 0dbabf78 carries both
  counters, the oracle, embedded selftests (red fixtures incl.
  `red-committed-before-freeze`, `red-committed-same-commit-as-freeze`), and the
  frozen refusal-prediction table; zero data commits exist, so the instrument is
  trivially before all data it counts. Holds.
- Refusal rule for pre-instrument data: both counters gate the committed clause on
  `git log --diff-filter=A %ct` of each envelope vs the claims-file first-add time
  (`env_added <= freeze_ct` → fail, tools/round-30/c1-rust-positive.py:186,
  c2-rust-refusals.py:247). Freeze time > instrument time, so any envelope first
  committed before or at the instrument commit is refused — stronger than the row's
  literal bar. Selftest fixtures red-committed-before-freeze/same-commit-as-freeze/
  no-freeze-commit all return fail (before/c*-selftest.txt, exit 0). Holds.
- Before record: exists as untracked .ufo/waves/round-30/before/{c1,c2}-{at-d210fb8f,selftest}.txt
  (written 02:35:15Z). Committed-before-data ordering is preserved only when the L1
  commits these ahead of the first envelope commit — currently true (no envelopes
  anywhere). Holds now; flagged below.

## Findings / residual risk (none blocking)

1. [low] runs.tsv is write-only in both counters (no committed-runs time check);
   utc_start rows are scored by nothing. A forged committed runs.tsv would not be
   caught by the counters — but it also scores nothing; envelope clauses carry the
   gate. Not a row-38 breach (no run exists to refuse yet).
2. [info] rea-agents 6.5.0 was installed on this host ~18 h pre-freeze (npx cache
   btime); "no REA run produced output before the freeze" is supported by the
   absence of output files, npm logs, and commits — it is not proven impossible.
   Deleted files would leave no trace in the repo; labelled unknown at the margins.
3. [info] 4 carriers and all 19 mutants have post-freeze mtimes; sha256 matches the
   frozen columns exactly (16/16, 19/19), so contents are provably the pinned bytes.
4. [info] The before receipts are untracked; row-38 order requires them committed
   before the first data commit — L1 integration item, not a defect at this point.
5. [info] jj working-copy snapshots in refs/jj/keep contain claims.json and the
   instruments with byte-identical blobs; unreachable from main, harmless to the
   freeze semantics (counters search `git log <rev>` from main revs).

## Tooling

No installs performed or needed (git, python3, find, stat, sha256sum all present).
No pacman/npx transactions by this seat.

## Artifacts

Seat scratch dir: none created (all checks were read-only git/python one-liners;
no files written outside this report). This report:
`.ufo/waves/round-30/w1/RevFreezeOrder.md` (in-lane report per contract).

## Evidence index (command → excerpt → exit → UTC)

- `git log --format='%H %cI %s' d210fb8f..main` → two commits listed above; exit 0; ~02:30Z.
- `git show --stat 0dbabf78 | head` → 6 files +977; exit 0; ~02:30Z.
- `git show --stat 4ee65c67 | head` → 1 file +74 (claims.json); exit 0; ~02:30Z.
- `git show <rev>:<path> | sha256sum` × 6 paths × {4ee65c67, main} → all match pins; exit 0; ~02:31Z.
- `git ls-tree -r --name-only <4 revs> -- corpus/evidence/round-30 | grep -E 'envelopes|runs\.tsv'` → `(none)` ×4; exit 0; ~02:31Z.
- `find /fast/scratch/hyaku/kaidoku-r30 -type f -printf '%T+ %p'` → only pre-freeze non-input file: uv-0.13.0.json 02:21:10Z; exit 0; ~02:33Z.
- `stat -c '%w %y' ~/.npm/_npx/ad9a3fdbcad992c6` → btime 2026-10-22T08:21:54Z; exit 0; ~02:36Z.
- `grep -rl rea-agents ~/.npm/_logs` → 11 logs, all 02:45:45–51Z; exit 0; ~02:37Z.
- python3 sha256 check vs carriers.tsv/predictions.tsv `sha256` column → 16/16, 19/19 OK; exit 0; ~02:40Z.
- `git rev-parse <snap>:<path>` blob compare → all 6 `same`; exit 0; ~02:41Z.
- `cat .ufo/waves/round-30/before/*.txt` → exit=2 base PIN records, selftests 25/0 and 16/0; exit 0; ~02:36Z.
- `git status --porcelain` → no round-30 corpus/tools untracked paths; exit 0; ~02:31Z.
