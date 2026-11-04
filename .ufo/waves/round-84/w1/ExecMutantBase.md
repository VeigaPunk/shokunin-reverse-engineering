# ExecMutantBase — R84-C2 independent base-arm reproduction

Base: `043b89a25241710a68b45526c3287fb3c8d907c3`. Frozen table `.ufo/waves/round-84/mutants.json`
(sha256 `dbb6d4c93df656d4c8341dee8a42e9256ba77e1d2e56ecda5b07d1db77b8982b`, matches the
`claims.json` fixture pin). I did not read or trust `pre/c2-base.json` until after my run.

## Method

- Targets read with `git -C <lane> show 043b89a2…:<path>` (read-only). Blob sha256:
  `tools/round-82/conjunction-gate.py` f009009993…bf163a (20464 B);
  `tools/round-82/printed-command.py` 88b1dff238…c5c061487 (28440 B);
  `tools/round-83/source-bind.py` 800a759e20…5963db3c (7031 B).
- Per mutant: anchor counted in the BASE blob (floor: both edits counted), edits applied
  to a private copy of the target at its repo-relative path; pristine copy and mutant copy
  are separate private roots. Each runs `python3 -I -B <target> --selftest` with cwd = that root.
- Verdict: killed iff anchors are all exactly 1, pristine rc 0 with no failing case, mutant
  rc non-zero, and the declared case name is in the mutant's failing list.
- Runner: one inline Python run (system Python 3.14.8, stdlib only). No tool installed or
  upgraded. No repo, fleet, or sibling writes; no git mutation.
- Parser shapes:
  - `conjunction-gate.py`, `printed-command.py`: stdout is one indent=1 JSON summary
    `{selftest, cases, case_names, failures}` followed by `SELFTEST cases=N failures=M`.
    I `raw_decode` from the first `{` and cross-check the trailing line (consistent in all 13).
  - `source-bind.py`: stdout lines `selftest <case>: ok|FAIL rc=[..]` plus `selftest: passed|FAILED`;
    the `--json-out` receipt is read for the same checks (names agree with stdout).

## Per-mutant results

| id | target | anchors (BASE) | pristine (rc, cases, failures) | mutant (rc, cases, failures) | declared case | declared exists at BASE | verdict |
|---|---|---|---|---|---|---|---|
| floor | conjunction-gate | 1, 1 | 0, 21, none | 1, 21, `floor-refused` | floor-refused | yes | killed |
| failure | conjunction-gate | 1 | 0, 21, none | 1, 21, `failures-refused` | failures-refused | yes | killed |
| binder | conjunction-gate | 1 | 0, 21, none | 1, 21, `binder-refused`, `first-declared-defect-binder` | binder-refused | yes | killed |
| membership | printed-command | 1 | 0, 15, none | 1, 15, `bare-name-refused`, `unpinned-path-refused` | bare-name-refused | yes | killed |
| pin-call | printed-command | 1 | 0, 15, none | 0, 15, none | runtime-pin-mismatch-refused | no | survived |
| static-refusal | printed-command | 1 | 0, 15, none | 0, 15, none | static-defect-no-execution | no | survived |
| source-mined | printed-command | 1 | 0, 15, none | 0, 15, none | sourced-row-rejected-status | no | survived |
| source-date | printed-command | 1 | 0, 15, none | 0, 15, none | sourced-row-wrong-date | no | survived |
| source-base | printed-command | 1 | 0, 15, none | 0, 15, none | sourced-row-at-base | no | survived |
| source-plan | printed-command | 1 | 0, 15, none | 0, 15, none | sourced-plan-missing | no | survived |
| source-entry | printed-command | 1 | 0, 15, none | 0, 15, none | sourced-entry-uncited | no | survived |
| sb-header-position | source-bind | 1 | 0, 6 cases, none | 0, 6 cases, none | late-single-header | no | survived |
| sb-duplicate-last | source-bind | 1 | 0, 6 cases, none | 0, 6 cases, none | duplicate-target-second | no | survived |

Pristine summaries are green for all 13 runs. Source-bind has 6 cases each run:
`positive, withdrawn, malformed, duplicate, duplicate-after-window, unavailable`.
Conjunction-gate has 21 cases and printed-command has 15 cases at BASE.

## Count

Independent count: **4 killed, 9 survived**. This matches the claimed 4/9 (`pre/c2-base.json`
reports the same verdict and the same failing names for all 13 rows; I checked after my run).

## Declared cases missing at BASE

Nine declared case names do not exist at BASE in any form:
`runtime-pin-mismatch-refused`, `static-defect-no-execution`, `sourced-row-rejected-status`,
`sourced-row-wrong-date`, `sourced-row-at-base`, `sourced-plan-missing`, `sourced-entry-uncited`,
`late-single-header`, `duplicate-target-second`. These are the nine survivor rows. The four
killed rows all have their declared case present at BASE.

## Divergence and cause

No divergence in count, verdict, or failing names from the recorded `pre/c2-base.json`.
The cause of each survivor is structural, not a runner artifact:

- **pin-call, static-refusal**: the BASE selftest calls `pin_matches()` and `static_defects()`
  directly. It never reaches the `run_block()` call sites the mutants edit, so the disabled
  refusal is unobserved.
- **source-mined, source-date, source-base, source-plan, source-entry**: the anchors live in
  `sourced_arm()`, which the selftest never calls. Its checks use `sources_row()` and
  `entry_cites()` on synthetic text, and those helper results do not depend on the edited lines.
- **sb-header-position**: no fixture has a single `source:` header at index >= 12, so the
  mutant is unobservable on the six existing cases. Diagnostic (scratch, not a fixture change):
  `entry_cites` on `'\n'*12 + 'source: S299 — …'` is `false` at pristine and `true` under the
  mutant, so a late-single-header case would kill it.
- **sb-duplicate-last**: the two-header fixture `duplicate` refuses both ways because the
  first-cited case is not the last header. Diagnostic: with the second header citing S299,
  pristine returns `false` and the mutant returns `true`, so a duplicate-target-second case
  would kill it.

Nothing else diverges. The four kills also trigger extra declared-free failing cases
(`first-declared-defect-binder`, `unpinned-path-refused`); these are not counted as the kill
binding, which stays on the declared case.

## Evidence files (wave dir)

- `.ufo/waves/round-84/w1/ExecMutantBase/base-arm-receipt.json`: per-mutant anchors, blob digest,
  pristine and mutant summaries, failing names, parser shape, verdict, the source-bind diagnostic.
- `.ufo/waves/round-84/w1/ExecMutantBase/candidates/base-arm-mutants.patch`: unified diffs of
  each applied mutant against its BASE blob (13 hunks).

Scratch `/fast/scratch/hyaku/kaidoku-r84/ExecMutantBase/` removed after the copy.

## Tooling

No tool installed or upgraded. pacman, `uv tool`, and `npm -g` were not used. Python 3.14.8 was the
existing system interpreter.

## Caveats

- Frozen bytes were only read. No edits to `tools/*`, `.ufo/waves/round-84/mutants.json`,
  `claims.json`, or `plans/round-84-claims.md`.
- Each private copy holds only the target file at its repo-relative path. All three targets
  are self-contained; `printed-command.py --selftest` and `source-bind.py --selftest` use only
  stdlib and temp dirs. Selftests did not touch the lane tree.
- No `task` spawn, no labrat probe, no commit, no push.
