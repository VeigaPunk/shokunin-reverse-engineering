# ExecProv — R80-C2: the receipt-provenance sweep and its base arm

Seat: ExecProv (leaf). Scope: implement and measure `tools/round-80/receipt-provenance.py`
and deliver its **base** arm; the round-80 landing repair is the L1's, and no lane production
file was edited here. Every write is under
`.ufo/waves/round-80/w1/ExecProv/` plus this report. Git was read-only in the lane
(`rev-parse`, `show`, `rev-list`, `cat-file`); the only fixture repo is a scratch clone whose
commits never leave the scratch dir.

- Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
- Base rev: `16dfa009bf143080dfcdfc5f9ec34bd359536d90`
- Candidate: `.ufo/waves/round-80/w1/ExecProv/receipt-provenance.py`
  (landing path `tools/round-80/receipt-provenance.py`), 28 387 bytes, 635 lines,
  sha256 `b07ee0c028d1f1623eb3173ba81551e4c69c27cf6d1299b0ddb3a732242c4001`
- Host: Python 3.14.8 (`-I -B`), git 2.56.0

## What the instrument does

Population: `l1/scores/*.json` under `.ufo/waves/round-<N>/` for N = `--from-round` (60)
through `--to-round` (79), any path containing `/attacks/` excluded, each file read from git
at `--rev` (`git show <commit>:<path>` — the working tree is never the population source), a
receipt absent at `--rev` skipped. Only JSON objects carrying an `instrument.path` string and
a 64-hex `instrument.sha256` enter the population (either hex case; the digest is compared
case-insensitively, so a case flip cannot drop a receipt silently); malformed JSON at `--rev`
is exit 2.

Provenance: the digest is committed iff it equals the sha256 of `git show <tip>:<path>` or of
`git show <r>:<path>` for some committed revision `r` of that path (`git rev-list --all --
<path>`). Blobs are read with one `git cat-file --batch` per instrument path; the working tree
is never read; a symbolic `--rev` is refused (a `--symbolic-full-name` hit, or a non-hex
argument, is exit 2) and a receipt's declared `rev`/`record.rev` is recorded
(`declared_rev_literal`), never used as an anchor. An `instrument.path` that is absolute,
carries a `..` segment or a control character is a named defect and is never passed to git.

Classification: `expected_controls = ["prov-forged-instrument.json"]`; a flagged receipt whose
basename is in it counts as `expected_control_flags`, every other flag as `unexpected`. The
receipt carries `receipts`, `flagged`, `expected_control_flags`, `unexpected`, `rows`
(`path`, `instrument`, `digest`, `verdict`, `matched_rev`, `defect`, `declared_rev`,
`declared_rev_literal`), `instrument.path`/`instrument.sha256` (this file's digest),
`checked_at`, `rev` (resolved 40-hex), and the git cost counters. Exit 0 iff
`unexpected == 0`; 1 otherwise; 2 when the population or the revision cannot be read.

`--validate` re-derives `receipts`, `flagged`, `expected_control_flags` and
`unexpected = flagged - expected_control_flags` from `rows`, rejects a `matched_rev` on a
flagged row or a missing 40-hex `matched_rev` on a committed row, rejects a defect verdict
without a named defect and a clean path carrying one, rejects duplicate row paths, checks the
self digest and the round, and rejects an `unexpected` that is not the difference.

## Selftest — 20 cases, 0 failures, exit 0

`selftest.txt` (raw output). Cases, one line each: `green-fixture-toplevel`,
`green-tip-digest`, `green-history-digest`, `green-uppercase-digest`,
`red-uncommitted-digest`, `red-working-tree-only`, `red-attacks-excluded`,
`red-no-instrument-skipped`, `green-expected-control`, `red-path-escape`,
`red-absolute-path`, `red-no-git-with-escaping-path`, `green-path-defect-clean`,
`red-symbolic-rev`, `green-abbreviated-rev`, `green-validate-consistent`,
`red-validate-unexpected-mismatch`, `red-validate-receipts`,
`red-validate-self-digest`, `red-validate-committed-without-rev`.
The fixture is a throwaway three-commit repo under `TMPDIR` (the seat scratch): v1 committed,
v2 committed as tip, v3 only in the working tree; receipts for the tip digest, the history
digest, the tip digest upper-cased, an unknown digest, the working-tree digest, the declared
control basename, a JSON without an instrument block, a non-64-hex digest, an `/attacks/`
fixture, `../outside.txt` and `/etc/passwd` (8 population rows). `red-no-git-with-escaping-path`
installs a spy on the module `git` and asserts no git argv ever contains `..`, i.e. the escape
path never reached git.

## Base arm at `16dfa009` — measured, exit 1

```
python3 -I -B receipt-provenance.py --root <lane> --rev 16dfa009 \
    --from-round 60 --to-round 79 --json-out prov-base-at-16dfa009.json
{"exit": 1, "receipts": 34, "flagged": 2, "expected_control_flags": 1,
 "unexpected": 1, "ok": false,
 "unexpected_paths": [".ufo/waves/round-79/l1/scores/c2-at-landing.json"],
 "git_calls": {"show": 153, "rev_list": 12, "cat_file": 12, "rev_parse": 2},
 "elapsed_seconds": 0.393}
```

`--validate` on `prov-base-at-16dfa009.json`:
`{"defects": [], "receipts": 34, "flagged": 2, "expected_control_flags": 1, "unexpected": 1}`,
exit 0. This matches the frozen base reading exactly.

The two flags, verbatim from the receipt rows:

| receipt | instrument | digest | verdict |
|---|---|---|---|
| `.ufo/waves/round-69/l1/scores/prov-forged-instrument.json` | `tools/round-69/packed-elf.py` | `000…000` | uncommitted (expected control) |
| `.ufo/waves/round-79/l1/scores/c2-at-landing.json` | `tools/round-79/pointer-bind.py` | `a0044c4c5006ac0f7e7fe57513c28bc9f98002aaab188575b87b0377466f9811` | uncommitted (unexpected) |

The other 32 rows are committed; each carries the 40-hex revision whose blob matched
(32/32 committed rows have `matched_rev`).

Population derivation at `16dfa009`: 141 candidate `scores/*.json` in rounds 60–79; 107 carry
no `instrument` block (skipped, not flagged); 0 live `/attacks/` paths; **34** receipts with
an `instrument.path` and a 64-hex digest. The 34 receipts name **12** distinct instrument
paths and 79 committed revisions of them (2 200 050 blob bytes hashed).

## Target-arm simulation (fixture clone; no lane edit)

To show the predicate is reachable and the pin is real, the lane was cloned read-only into
scratch (`git clone --shared`; toplevel verified equal to the clone dir before the first
commit; all four commits inside the clone), then probed in four directions:

| probe | rev | exit | receipts | flagged | expected | unexpected | reading |
|---|---|---|---|---|---|---|---|
| digest edited, **not committed** | `253fc817` | 1 | 34 | 2 | 1 | 1 | working tree is not an anchor |
| digest edited and **committed** | `da061c24` | **0** | 34 | 1 | 1 | **0** | target shape; `--validate` defects `[]` |
| `--rev main` (symbolic) | — | **2** | — | — | — | — | `rev 'main' is not a hexadecimal commit id; a symbolic revision is never treated as a committed revision` |
| committed receipt with `instrument.path ../outside.txt` | `698d4b82` | 1 | 35 | 2 | 1 | 1 | `verdict defect`, `defect: instrument.path '../outside.txt' contains a '..' segment`; flagged |
| repaired receipt **deleted**, not repaired | `2a55a45b` | 0 | **33** | 1 | 1 | 0 | population dropped by one; the count is the guard |

The repair used the committed blob digest `40905d396245313bedb7d0ae25b63f322b39e8e877371630e84d7616f12cb877`
of `tools/round-79/pointer-bind.py`. The target run is `repair-sim/prov-target-sim.json`
(34/1/1/0, `ok true`, exit 0) and its `--validate` is defect-free. The deletion row is
`repair-sim/deletion-control.json`; exit 0 at 33 receipts is exactly the kill-rule signal
("a `receipts` count other than 34 without a disclosed population change"), not a pass.

Raw outputs: `repair-sim/worktree-only.json` / `.txt`, `repair-sim/target.txt`,
`repair-sim/validate-target.txt`, `repair-sim/symbolic-rev.txt`, `repair-sim/escape-probe.json`
/ `.txt`, `repair-sim/deletion-control.json` / `deletion.txt`, and
`repair-sim/simulation-summary.json`.

## Git commands and cost

Base run (all read-only in the lane): 179 git processes in 0.393 s —
`show` ×153 (141 population candidates + 12 tip instrument blobs), `rev-list` ×12,
`cat-file --batch` ×12 (79 revision:path blobs, 2.2 MB), `rev-parse` ×2. The clone
simulation (clone + 4 fixture commits + 5 tool runs) took 4.02 s wall; the five tool runs
after the clone measured 0.196–0.216 s each. Every receipt carries its own `git_calls` and
`elapsed_seconds`.

## Verification actually run

- `--selftest`: exit 0, `SELFTEST cases=20 failures=0` (`selftest.txt`).
- `--rev 16dfa009`: exit 1, 34/2/1/1, unexpected `c2-at-landing` (`base-sweep.txt`,
  `prov-base-at-16dfa009.json`).
- `--validate prov-base-at-16dfa009.json`: `defects []`, exit 0 (`validate-base.txt`).
- The five simulation probes above, each with its raw receipt under `repair-sim/`.

No build, lint, test or formatter of the lane was run; no tracked lane file was modified
(`git diff` and `git diff --cached` are empty), and the untracked `tools/round-80/` set
observed at report time is not this seat's (see below).

## Existing landing-path file (observed, not written by this seat)

While verifying the evidence dir, `tools/round-80/receipt-provenance.py` was found to already
exist in the lane working tree as an **untracked** file: 17 725 bytes, mtime 10:45:26,
sha256 `b59068d68857a6ebfdde2ebb0864d41c888f9eb896a254ba6a19fb5525e42b10`. This seat did not
write, copy or modify it; the candidate delivered here is the 28 387-byte file in
`ExecProv/receipt-provenance.py` (sha256 `b07ee0c0…`). Measured read-only, the pre-existing
file differs in a way the L1 must decide on:

- its `--selftest` exits 0 with `SELFTEST cases=14 failures=0` (`existing-tool-selftest.txt`);
- it **refuses the frozen base command**: `--rev 16dfa009` exits 2 with
  `"--rev '16dfa009' is not a 40-hex commit"` (`existing-tool-base.txt`), so it cannot produce
  the frozen base arm as written; with the full commit
  `16dfa009bf143080dfcdfc5f9ec34bd359536d90` it does reproduce 34 / 2 / 1 / 1 and validates
  (`existing-tool-base-fullrev.json`, `.txt`, `existing-tool-validate-fullrev.txt`);
- its row schema is `receipt`/`sha256`/`reason`/`verdict` (`bound`, `uncommitted-digest`), not
  the `path`/`instrument`/`digest`/`verdict`/`matched_rev` shape the seat named.

The delivered candidate accepts the abbreviated base rev (and refuses symbolic names), so the
frozen command runs as written. The L1 lands one instrument at that path; this seat's
candidate is the one under its evidence dir.

## Risks / limits

- Population discovery is a filesystem walk of the candidate glob, then a `git show` per
  candidate at `--rev`; a receipt deleted from the working tree but still present at `--rev`
  would be missed by the walk (it cannot be found), which lowers `receipts` — the count check,
  not silence, is what makes that visible. A receipt present at `--rev` but absent from the
  working tree is skipped by the same rule; the spec's population is the walked glob.
- An empty population (a wrong `--root`, or a round range with no receipts) scores
  0/0/0/0 with exit 0; the frozen predicate's `receipts 34` is what distinguishes that from a
  pass, and the deletion control above shows the same count-only guard in practice.
- `git rev-list --all` is all refs, as the seat text specifies; a blob reachable only from a
  dangling object is not matched, while a blob on any other ref is.
- The tip anchor is the resolved `--rev` commit; later commits are covered by the `--all`
  history clause, so the result does not depend on HEAD.
- `--validate` checks `instrument.sha256` against **the file that runs it**: the delivered
  receipt must be validated by the identical instrument bytes (the landed copy keeps the
  digest).
- The selftest fixture is synthetic (three commits, one instrument path); it exercises the
  rule shapes, not the 34-receipt lane population. The lane population is measured separately
  by the base arm.
- An `instrument.path` containing `:` is not separately rejected; git's `<rev>:<path>`
  parsing treats only the first colon as the separator, and no such path exists in the
  population.

## Tooling

No tool was installed or upgraded; no pacman transaction was attempted (host-wide pause
respected). Python 3.14.8 and git 2.56.0 used as found. Scratch
`/fast/scratch/hyaku/kaidoku-r80/ExecProv/` was created, passed explicitly as `TMPDIR`, and
removed before this report; no tool hardcodes `/tmp`.
