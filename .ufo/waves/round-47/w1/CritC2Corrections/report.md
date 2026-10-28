# CritC2Corrections — seat report

**Verdict: predicate too weak.** R47-C2's exemption route does not have to be about the atom it
exempts. Cheapest false-but-passing card: fixture `$S/fx` base `03ff8de444947739eee57d66137a7c2675c5847f`,
card commit `deda0d5ca7a6fbbb9fba8211de7debd309e3fc6e` —

```
## Round 9
Base `03ff8de4`. Waves: 1 + 1 = 2 seats. Wave 1: 7 seats; wave 2: 9 seats.
`git log 0425224..<tip> -- tools/x/keep.md` is empty at every measurement above.

## Record corrections — round 47
- corrects seats round-9: 2 waves, 2 seats total
- corrects window round-9: empty in 03ff8de4..03ff8de4 -- tools/x/keep.md
```

The seat pair is false (dispatched 1 and 1) and the window names a rev no repo has. The seats line
restates the already-true sum atom and exempts the false pair by round key; the window line is a
degenerate self-window.

```sh
python3 -I -B tools/round-47/record.py --root $S/fx --rev deda0d5ca7a6fbbb9fba8211de7debd309e3fc6e
# exit 0 · failing [] · corrections 2 · exempted 2 · battery 3/0
```

Floors: **`corrections >= 2` does not stop it** (duplicates count — `861c3e7`, exit 0; a historical
`seats round-7` line that repairs nothing counts — `811601b`, exit 0). **`exempted <= 3` does not
stop it** — it is a cap on retained falsehoods, satisfied at exactly 3, and it bites only at 4
(`791c0a9`, `exempted 4 > 3`, exit 1). Neither requires the false sentence to be edited.

Live instance at the declared freeze `1e2c310295…`: the round-46 "window is empty" sentence is false
(`0425224..1e2c310295` modifies `tools/round-46/attest.py` and `gate.py`) and is exempted by
`empty in 332f4884..58eb04b6` — a window that starts at the very commit that made the change.
Reducing it to `332f4884..332f4884` still scores **exit 0** (T1); stating the honest window
`0425224..58eb04b6` scores **exit 1** (T2). The instrument pays for changing the subject.

Also found: the `axes` arm of clause 3 is unreachable (`CORR` grammar has no `axes`; the landed card
carries 4 `- corrects` lines and the counter reports `corrections 2`); `record.py:292-299` is dead
code referencing an undefined `atom`; the window battery forgery is pathspec-dependent; `--selftest`
is unreachable without dummy `--root/--rev`.

Smallest safe correction: bind a window correction to the atom's own named rev and reject degenerate
windows + empty pathspecs (S1), and bind a seats correction to the atom's shape (S2), then dedupe
before counting (S3). Measured: `record-s1s2-patch.py` (A5 instrument + S1 + S2 + the symmetric
`wave 1: a seats; wave 2: b seats` grammar) turns the live A4 card red (exit 1, the record must edit
its two sentences), turns the cheapest-false card red (exit 1), and passes the one card that names
the false atom's real figures (`ebc4b8b3…`: frozen exit 1, patched exit 0). Full text, code sketch
and receipts: [`../CritC2Corrections.md`](../CritC2Corrections.md).

## Artifacts in this directory

| file | content |
|---|---|
| `fixture-run3.json` | cards A (cheapest-false, exit 0), B (padded, exit 0), C (uncorrected, exit 1), D (axes arm, exit 1) |
| `fixture-run4.json` | E duplicate-padding (exit 0), G control (exit 0) |
| `fixture-run5.json` | F four-false (`exempted 4 > 3`, exit 1) |
| `fixture-run6.json`, `fixture-run7.json` | H grammar-evasion, without and with a window correction (exit 0) |
| `realvariants.json` | T0 lane tip / T1 tautology (both exit 0), T2 honest window (exit 1), T3 removed (exit 1) |
| `rec-1e2c310295….json`, `rec-2e4ae434….json`, `head-nobattery.json` | the frozen counter on the lane at the declared freeze, at A3, and at HEAD — all exit 0 |
| `selftest.out` | `RECORD_SELFTEST: cases=10 failures=0` |
| `patch-liveA4.json`, `patch-fixtureA.json` | the S1+S2 instrument on the live A4 card (exit 1) and the cheapest-false card (exit 1) |
| `fixture-run10.json`, `fixture-run11.json` | honest-repair card, placeholder and concrete window; frozen vs patched instrument |
| `record-s1s2-patch.py` | the S1+S2 instrument (scratch build; frozen bytes untouched) |
| `drive.py`, `drive2.py`, `drive3.py`, `drive4.py`, `realvariants.py` | drivers that rebuild every fixture |

No installs. Scratch `$S` removed after this copy. Lane tree untouched; no git/jj mutation outside
the scratch fixture and the scratch clone.
