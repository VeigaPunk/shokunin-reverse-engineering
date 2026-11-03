# MutCounter — R64-C1 instrument mutation probe (w1 attack seat)

Claim under attack: **R64-C1** — "all 18 runs reproduce the frozen predicted label of their
cell (dump|view8|check), with every input and binary sha256 equal to its pin."
Target instrument: `tools/round-64/jsc-route-matrix.py`
sha256 `29efef4fb5492e7a4aa9cfb88ac2a7bf8b30c5462aafaf692c407ededba20deb` (read-only; never edited).

## What I ran

Six single-textual-change mutants of the frozen instrument on scratch copies, each guarded by
`assert text.count(old) == 1`, detector `python3 <copy> --selftest` (`TMPDIR` inside scratch;
in-memory fixtures only — no d8/view8/node, no network), plus the do-nothing arm
`--skip-run` expected at exit 1. Full table, verbatim FAIL lines and per-mutant hashes:
`w1/MutCounter/mutants.md`.

Baseline first: pristine copy of the frozen bytes → `SELFTEST CLEAN cases=22 failures=0`,
exit 0; `--skip-run` exit 1 (`runs_matching=0`, `verified=false`). Baseline green, so all six
verdicts are interpretable.

## Verdict: 5 killed, 1 survived

| mutant | behaviour destroyed | selftest | outcome |
|---|---|---|---|
| M1 | 134 (SIGABRT) mapped to `dump-ok` | 1 — `FAIL dump-sigabrt got='dump-ok' want='dump-exit-134'` | killed |
| M2 | `norm_rc` identity (negative signal deaths leak) | 1 — `FAIL dump-sigabrt got='dump-exit--6'`; `FAIL dump-sigsegv got='dump-exit--11'` | killed |
| M3 | verdict strictness (`matches >= total-1`) | 1 — `FAIL verdict-one-mismatch-exit got=0 want=1` | killed |
| M4 | prediction fidelity (`typora\|D1` re-predicted green) | 1 — `FAIL verdict-fake-green-count got=3 want=0` | killed |
| M5 | SFI marker brackets dropped from `SFI_RE` | **0 — `SELFTEST CLEAN cases=22 failures=0`** | **SURVIVED** |
| M6 | node check failure collapsed to `node-pass` | 1 — `FAIL check-fail got='node-pass' want='node-fail'` | killed |

Every mutant still exits 1 on `--skip-run`: the do-nothing control is not collapsible by any of
the six changes, so it cannot substitute for the selftest.

## Finding (coverage, not a contract change)

**M5 survives because the self-test has no negative fixture for the bracketed marker.**
Its only positive dump fixture is
`b"Start SharedFunctionInfo\n0x1: [SharedFunctionInfo] in OldSpace\n"` — the first line already
holds the *unbracketed* token, so `rb"SharedFunctionInfo"` still matches. M5's selftest stdout
is byte-identical to pristine (`diff` empty).

M5 is not an equivalent mutant. In-process classifier probe on in-memory fixtures:

| fixture | pristine | M5 |
|---|---|---|
| `b"0x1: [SharedFunctionInfo] in OldSpace\n"` | `dump-ok` | `dump-ok` |
| `b"0x1: SharedFunctionInfo in OldSpace\n"` | `dump-empty` | `dump-ok` |
| `b""` | `dump-empty` | `dump-empty` |

So the loosened classifier would report `dump-ok` on a dump carrying only banner text, i.e.
`dump-empty` detection is unguarded by the self-test. Impact on R64-C1 as frozen: none
observed. No predicted cell is `dump-empty` (the six predictions are `dump-ok`,
`dump-exit-134`, `dump-exit-139`), so M5 cannot flip a predicted label, and the prediction
table was left untouched and un-re-predicted.

## Kill-margin note

Each of the five kills rests on exactly one load-bearing case: `dump-sigabrt` (M1, M2),
`verdict-one-mismatch-exit` (M3), `verdict-fake-green-count` (M4), `check-fail` (M6). No margin
— deleting any single one of those five cases would silently admit its mutant. M4's kill is
notably narrow: the `verdict-one-mismatch-*` pair does not catch a mis-predicted cell (it flips
`typora|D2` only); only the fake-green-count case does.

Not probed (out of the six assigned changes, recorded as adjacent coverage only): the self-test
exercises pin checks for `probe`/`typora` but not for the `D1-snapshot`, `D1-icudtl` or
`view8.py` pins.

## Evidence pointers

- Table + verbatim outputs: `.ufo/waves/round-64/w1/MutCounter/mutants.md`
- Driver: `/fast/scratch/hyaku/kaidoku-r64/MutCounter/gen_mutants.py` (removed with scratch)
- Instrument sha256 before **and** after: `29efef4f…ba20deb` (unchanged)
- Mutants: M1 `7665b906…`, M2 `2d8c735c…`, M3 `8c189982…`, M4 `081ef02a…`, M5 `b4dfc41a…`,
  M6 `c225cde0…`; pristine copy `29efef4f…` (byte-copy of the frozen source)
- Scratch `/fast/scratch/hyaku/kaidoku-r64/MutCounter/` deleted before yield; no other writes.
