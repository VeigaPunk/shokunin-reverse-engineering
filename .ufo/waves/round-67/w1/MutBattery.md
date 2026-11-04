# MutBattery — R67-C2 battery mutation probe (round 67, w1)

Seat: mutation-tester, leaf. Scope: five mutants of the frozen R67-C2 battery
`tools/round-67/mutation-battery.py` (`cabc0a0b…851ab`), scratch copies only, at
`a7a4ce6902204d5c6cc6c4e3e78b4bffe8312b92`. Full detail, diffs and receipts:
`.ufo/waves/round-67/w1/MutBattery/mutants.md` and
`.ufo/waves/round-67/w1/MutBattery/receipts/`.

Protocol: frozen bytes copied to scratch, one hunk applied per mutant, each
driven through the battery's own `--selftest`, `--score` and `--control` against
the real lane, work/out/TMPDIR inside scratch. Baseline pristine copy in the
same harness: `--selftest` 9 cases 0 failures rc 0; `--score` killed_before 0,
survived_before 2, killed_after 2, verified true rc 0; `--control` 0/2, green —
identical to the committed before-arms, so a red would mean something and these
greens are survivals.

| mutant | defect | sha256 | expected detector | actual output | verdict |
|---|---|---|---|---|---|
| N1 | `EXPECTED_CASE` accepts any failing case name | `ddb8fcca…513a8` | `--score` verdict | rc 0, verified true, killed_after 2 (byte-identical to pristine but for `counter.sha256`) | **survived** |
| N2 | `killed_after` drops the case-name condition | `84b6db28…d8824` | `--score` verdict | rc 0, verified true, killed_after 2, identical receipt | **survived** |
| N3 | `control()` swaps killed_before/survived_before | `049e7c8d…0420` | `--control` receipt | rc 0, control_ok true, prints killed_before 2 / survived_before 0 (pinned before-arm: 0/2) | **survived** |
| N4 | `selftest()` drops `equiv-doctored-diffs` | `c51b3bbf…c2e28` | `--selftest` case inventory | rc 0, `SELFTEST CLEAN cases=8 failures=0`; score still verified true | **survived** |
| N5 | missing `after_out` counted as a kill | `cdd3f989…0bbdab` | `--score` verdict | rc 0, verified true, identical receipt | **survived** |

All five survive the battery's own three modes. None of the modes exits non-zero;
for N1/N2/N3/N5 the `--score` receipt is byte-identical to the frozen one except
the battery's self-hash, so only a hash pin on `cabc0a0b…` distinguishes them.

## Discriminating probes (in-process; injector substitution, not CLI receipts)

- **Probe A, wrong-defect pair** (arm→False, recipe_a_equivalence→False; both
  still survive their own r66 selftests). Pristine battery: killed_after 0,
  verified false, exit 1. **N1 and N2: killed_after 2, verified true, exit 0** —
  a green R67-C2 certificate for a pair that leaves both declared defects alive.
  N3/N4/N5 match pristine here.
- **Probe D, unimportable mutants** (no receipt written). Pristine killed_after
  0; N2/N5 report 2 with killed_before 2, so the verdict stays false — N5's
  weakened branch is reachable but masked by the pinned before-arm; only the
  `killed_after` field lies.
- **Probe C, counter raises inside the battery's checks**: the exception escapes
  `score()`, process rc 1, **no receipt at all**, not the documented exit 2 —
  identical for the frozen bytes (instrument gap, F5).

## Disclosed gaps

1. Verdict layer unbound (N1/N2): nothing asserts that a mutant failing a
   non-target case is not a kill; probe A issues a false green.
2. `--control` aggregates unbound (N3): the inverse before-arm prints with exit 0.
3. Case inventory unbound (N4): 8 cases pass as clean.
4. Missing-receipt handling unbound (N5): masked today, but `killed_after` is not
   trustworthy on a red run.
5. No could-not-evaluate guard around the after-detector (F5): a raising counter
   yields a traceback, no receipt, exit 1.
6. A green `--score` receipt identifies its instrument only by `counter.sha256`;
   consumers must pin `cabc0a0b…851ab`.

None of this contradicts R67-C2 on the frozen bytes: the pristine instrument
still reports killed_before 0, killed_after 2, verified true at `a7a4ce69…`, and
both declared survivors are killed by the named cases. These are limits on what
that green receipt evidences — the after-detector's non-zero exit must be read
together with `after_failed_cases`, and the before-arm fixtures must not be
regenerated from the instrument under test.

## Restoration evidence

- Frozen battery sha256 before and after: `cabc0a0b6a47ca00d3e5c20e9795ba4c129b44a3c14a882d69f9c6b2534851ab` (unchanged, never opened for writing).
- r66 pins unchanged before/after: `3c5cfb03…1045b`, `1be9d046…55aa`
  (`receipts/hashes.txt`).
- Mutant bytes re-hashed after all runs; hashes match those built and reported.
- Post-run on the actual frozen path: `--score` rc 0 verified true (killed_before
  0, killed_after 2, self-hash `cabc0a0b…851ab`), `--selftest` rc 0, 9 cases 0
  failures (`receipts/post/`).
- No writes to `tools/`, `corpus/`, `corpus/evidence/`, `PROVINCE.md`,
  `SCORECARD.md`, `LOG.md`, `SKILL.md`, the fleet repo or sibling lanes;
- `git -C kaidoku-shokunin status --porcelain` unchanged by this seat. No
  `after.json` written.
- Bytecode: CLI runs used `-I -B`; the in-process probes imported the frozen r66
  counters without `-B` and likely created the gitignored
  `tools/round-66/__pycache__/closure-boundary.cpython-314.pyc` inside the probe
  window. Source bytes and pinned hashes unchanged; cache is derived and not
  load-bearing.
- Scratch `/fast/scratch/hyaku/kaidoku-r67/MutBattery` deleted before yield; no
  `/tmp` use. No tool installs.

## Limits

Five mutants only, as assigned. Probes A/C/D monkeypatch the injector functions
to reach states the CLI cannot construct; they run the frozen `score()`/
`selftest()` bodies against the real pinned counters and are not counted as CLI
receipts. Probe C's stimulus is outside the two declared survivors and is used
only to reach N5's branch and F5. No repair attempted; a surviving mutant is a
coverage finding.
