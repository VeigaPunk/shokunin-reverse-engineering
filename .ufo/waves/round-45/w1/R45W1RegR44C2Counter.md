# R45W1RegR44C2Counter — `tools/round-44/c2-counter.py` at the round-45 freeze

Seat: `R45W1RegR44C2Counter` (leaf). Lane `kaidoku`, round 45 wave 1. Read-only on the lane
tree; writes only under `.ufo/waves/round-45/w1/R45W1RegR44C2Counter/`. Nothing committed,
staged or pushed; scratch removed before yield. No install or upgrade performed (pacman
transactions are paused host-wide and nothing was needed).

**Verdict.** The frozen instrument is real, its three exits are each reproducible on real bytes
at the freeze, and its self-test is bit-identical to the round-44 L1's recorded run. The row
already landed at `SKILL.md:1638` **passes** the R45-C2 predicate but is **inaccurate on the
pinned-value path**, and it is **silent on two measured defects** (a lying stdout claim gate,
and an `expected_edit` restore hole). Draft row + corrections: `row.md`; every measurement:
`receipt.md` and `receipts/`.

## Frozen bytes

| path | sha256 at `f762b72` = worktree |
|---|---|
| `tools/round-44/c2-counter.py` | `085192ea6c3f3f4d67c58ce459ef06e1febd0b668dc367ccfbdd12661736c277` |
| `tools/round-44/c2-rubric.json` | `e8cc0dedd6b4bbfb323983018806de4b6ad59b80b1aeee111aa2d8ebf55e755e` |

`git diff --stat f762b72 -- tools/round-44 plans/round-44-claims.md` printed nothing. Lane HEAD
`faa875bc` had no modified tracked file (`git status --porcelain` = untracked `.ufo/` only).

## Three exits, all observed

| run | argv `--rev` / `--freeze` | exit | what it printed |
|---|---|---|---|
| selftest | `--selftest` | **0** | 24 arms, all `ok`, `{"ok": true}`; stdout sha `a5e942a1…` **identical** to `.ufo/waves/round-44/l1/selftest-c2-counter.txt` |
| met | `55bcce69` / `c48f8a4` | **0** | `met_target true`, 80/80 evaluated, `mismatches []`, `usable_as_claim_score true`; all six fields equal the round-44 L1's recorded receipt (`1c55af14…`) |
| not met | `c48f8a4` / `c48f8a4` | **1** | 80 evaluated, 3 mismatches named: `C2-a1-owned-coverage-count`, `C2-a2-owned-depth-count`, `C2-a4-owned-depth-craft-range` — exactly the three target entries |
| could-not-evaluate | `f762b72` / `c48f8a4` | **2** | `frozen_path_changed` = 8 `tools/round-44/control-fixtures/**` paths, `entries_evaluated 0`, `met_target false`; set identical to `.ufo/waves/round-44/l1/c2-score-at-final-tip.json` (`de0a7e65…`) |

## `frozen_path_changed` path (source-read)

`freeze_integrity()` unions two walks (`git log --name-only --no-renames` and
`--diff-merges=first-parent --name-only --no-renames`) over `FREEZE..REV`, then per frozen path
`path_status_changes()` (`M/D/T/R/U`, plus `A` when the path existed at FREEZE). Consequences
measured, not assumed:

- a **plain** frozen path touched and later restored to its freeze bytes → **exit 2**
  (`state: touched_after_freeze`; fixture `receipts/restore-probe.json`), so tip equality does
  not un-block;
- an **`expected_edit`-bound** path appended and then restored to its freeze bytes → **exit 0,
  `met_target true`, `state: unchanged`** (fixture `receipts/bound-probe.json`) — the claim's
  "a later restore does not un-block" is **false on this arm**, which is the open item R44-CL10
  confirmed first-hand. `SCORECARD.md` is the rubric's only bound-edit path;
- `frozen_dirs` (`tools/round-44`) reds on changed, added **and** untouched-but-touched paths.

## Rubric binding (source-read + parser output)

`parse_rubric()` returns `(doc, entries, frozen_spec, declared, frozen_dirs, malformed)`; the
rubric body is read from the **freeze blob** unless `--rubric`/`--pre-freeze`, and
`rubric_source != 'freeze'` forces `claim_score false`. Malformed rubric, entry without
`check`/`command`/`asserted`, duplicate id, and an `expected_edit` that binds no content are all
`Unevaluable` → exit 2. Measured on the shipped rubric:

```
frozen_spec  ['SCORECARD.md','SHONEN.md','SKILL.md',
              'tools/round-44/c2-counter.py','tools/round-44/c2-rubric.json']
edit_bound   ['SCORECARD.md']      frozen_dirs ['tools/round-44']
entries      80  (SCORECARD 55, SHONEN 22, corpus/README 3)  checks {'json'}  repair_commands 0
claims_file_in_frozen_spec False
```

`plans/round-44-claims.md` appears in this counter only as docstring/comment
(`c2-counter.py:4`, `:129`); the claims file is pinned by `tools/round-44/c1-counter.py:273`.
The `claim_gate.usable_as_claim_score` conjunction (`finalize()`) is
`claim_score ∧ rubric_source=='freeze' ∧ counter_sha256_at_freeze ∧ rubric_sha256_at_freeze ∧
exit_code==0 ∧ met_target ∧ ¬frozen_path_changed ∧ ¬unevaluable`.

## Findings for the landing

1. **Row correction — pinned-value path.** Landed cell names
   "`tools/round-44/c2-rubric.json` (frozen) and `plans/round-44-claims.md`". Replace the claims
   file with what this counter freezes: rubric + counter (by constant), the rubric's three
   `frozen_paths`, `frozen_dirs tools/round-44`; note that the claims file is the C1 counter's
   pin. This is the "self-assessment vs repo state" mismatch the calibration axis measures.
2. **Row correction — selftest cell.** Landed carries no arm count where all sibling rows carry
   one; measured 24 arms, exit 0.
3. **Instrument defect — the stdout summary lies about the claim gate.** `main()` builds the
   printed `claim_gate` without `exit_code`/`met_target`/`frozen_path_changed`/`unevaluable`, so
   exit 1 and exit 2 runs print `usable_as_claim_score: true` while their `--json-out` receipts
   correctly say `false` (`c2-counter.py:1695-1705`; evidence: the two score runs' stdout). Only
   the receipt is authoritative — worth a sentence in the row's verdict cell or a CL row.
4. **Freeze design carry-over.** The round-44 directory freeze over `tools/round-44` was
   invalidated by the next wave rewriting control fixtures under it, so R44-C2 is exit 2 from
   that commit onward. R45 freezes `tools/round-45/` (also a directory): keep wave-2
   falsification inputs and control fixtures under `.ufo/waves/round-45/`, never under
   `tools/round-45/`, or R45-C1/C2 will inherit the same permanent exit 2.
5. **Disclosed limit.** A `C2_DEFAULT_FROZEN` path absent at the freeze and created later is
   recorded `absent_at_freeze` and is not a change (inert here — all three exist at
   `c48f8a4`). `frozen_dirs` has no such hole.
6. **Scope honesty.** The shipped rubric has zero `repair_command` entries, so the
   "note-is-never-evidence" machinery is exercised only by selftest arms 10/11; the three
   repairs land solely through `SCORECARD.md`'s bound append.

## Evidence map

- `row.md` — the exact 7-column row (first cell the backticked path, exit cell naming `0`/`1`/`2`),
  cell map, parser validation, and the delta against `SKILL.md:1638`.
- `receipt.md` — exact argv, exit, stdout sha256 and UTC for all nine commands; the 24 selftest
  arms with the red clause each pins; the three real-byte scores; both restore fixtures; the
  findings; what was not run.
- `receipts/` — `selftest.json` (24 arms), `receipt.tsv` (machine table), `parse-rubric.txt`,
  `row-final.md`/`row-final.txt` (row validated by `tools/round-45/c2-counter.py`'s own
  `parse_rows`/`exits_ok`), `restore-probe.json`, `bound-probe.json`,
  `score-f762b72.exit2.json` (whole), and key-projected copies of the two ~750 KB exit-0/exit-1
  receipts (`_projection_of` + the digests in `receipt.md` bind them to the originals).

## Checks the integrator should run

- `python3 -I -B tools/round-45/c2-counter.py --root <lane> --freeze f762b727 --rev <landed>`
  after the registry row is amended — the draft row was validated against that file's
  `parse_rows`/`exits_ok`, not against a full score.
- If the R44-C2 row's pinned-value cell is amended, re-run `tools/round-44/c2-counter.py` at
  `--rev 55bcce69` (exit 0 expected) to show the instrument still scores before citing the new
  wording.

## Risks / blockers

- **No blocker.** Nothing in the lane tree was modified; the two fixture repos live only in
  scratch and were removed with it.
- The exit-0/exit-1 receipts are committed only as projections; if the landing needs the full
  80-entry records, they must be re-generated (6 s each) rather than recovered.
