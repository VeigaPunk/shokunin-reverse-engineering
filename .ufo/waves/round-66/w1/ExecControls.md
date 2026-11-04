# ExecControls — R66-C1 controls + fail-ability arms (w1)

Scope: re-run the two committed do-nothing controls and three assigned fail-ability mutations of
`tools/round-66/closure-boundary.py`. No repository file was modified; only receipts and reports
were written under `.ufo/waves/round-66/w1/ExecControls/`.

## Frozen-input integrity (checked before running)

- `tools/round-66/closure-boundary.py` = `3c5cfb038d86cdde03fb659e1d42a44ffa5f42ccd019ab7ea9b52710d071045b` (matches seat pin)
- `tools/round-66/coverage-selfcheck.py` = `1be9d046cea38a96a4b62d038f7dbc76e8ea611000af4aee3b91a6def86555aa` (matches seat pin)

## Results

| step | command (TMPDIR=/fast/scratch/hyaku/kaidoku-r66/ExecControls, `python3 -I -B`) | exit | result |
|---|---|---|---|
| 1 | `l1/controls/c1-do-nothing.py --repo <lane> --out w1/ExecControls/c1-do-nothing.json` | 0 | **1/5 arms, ok false** — JSON-equal to committed `l1/controls/c1-do-nothing.json` |
| 2 | `l1/controls/c2-do-nothing.py --repo <lane> --rev 311079d… --out w1/ExecControls/c2-do-nothing.json` | 0 | **0/3 conditions, ok false** — JSON-equal to committed `l1/controls/c2-do-nothing.json` |
| baseline | `closure-boundary.py --verify --work $S/work-base --out base-verify.json` | 0 | **5/5, ok true** (positive control) |
| A | `$S/m1.py --verify` (`COUNT = 30` → `29`) | 1 | **3/5** — flipped **a3** (`entries 30 != 29`) and **a4** (truncated manifest greens: `count_ok true, ok true`) |
| B | `$S/m2.py --verify` (`post_cache` scan moved before `probe_fn()`, moved value used in `ok`) | 1 | **4/5** — flipped **a2** (`ok true`, empty `cache_present`, no finding; the unguarded probe's `.pyc` is invisible) |
| C | `$S/m3.py --skip-run` then `--verify` (`skip_run_receipt` returns `closure {ok:true, entries:30}`, `closure_claimed:true`) | 1 / 1 | `--skip-run` emits a closure object claiming ok; `--verify` **4/5**, flipped **a5** |

a1 stayed green in all mutants (no assigned mutation targets it). Every assigned mutation flipped
its arm; none stayed green, so no counter defect is reported on this axis. Per the seat rule, a
mutation that does **not** flip its arm would be a counter defect to report, never to fix — the
frozen `tools/round-66/*` and `tools/round-65/*` bytes were only copy sources.

## Evidence pointers (sha256)

- `w1/ExecControls/c1-do-nothing.json` `bbcc70c4…65284850` (rerun; equals committed)
- `w1/ExecControls/c2-do-nothing.json` `f4599e1b…c8ec24` (rerun; equals committed)
- `w1/ExecControls/base-verify.json` `f10fd02d…9b6553`
- `w1/ExecControls/m1-verify.json` `fcf105dc…d86540`; mutant `m1.py` `ad121361…65939d`
- `w1/ExecControls/m2-verify.json` `df97ec43…3a8d5`; mutant `m2.py` `d779dd42…8756114`
- `w1/ExecControls/m3-verify.json` `774ef6b8…afe70`; `w1/ExecControls/m3-skiprun.json` `c91ccced…7c9a2`; mutant `m3.py` `933052f6…d917bb8`
- Detail: `w1/ExecControls/findings.md` `ba024935…f04f8e`

## Risks / notes

- In mutant C the untouched `exit: 1` key keeps the `--skip-run` process exit nonzero while the
  emitted object claims ok; the a5 arm is evaluated on the object in `--verify` and still fails, so
  a5 remains load-bearing on the claim itself.
- No blockers. No tools installed. Scratch `/fast/scratch/hyaku/kaidoku-r66/ExecControls` removed.
