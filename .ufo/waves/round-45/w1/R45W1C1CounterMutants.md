# R45 wave 1 — mutation probe of the frozen `tools/round-45/c1-counter.py`

Seat `R45W1C1CounterMutants`, leaf, lane `kaidoku-shokunin`, round 45 wave 1.
Target: `tools/round-45/c1-counter.py` at freeze
`f762b7273e3f6ca3c710bb37d5de92a4a4417aec` (blob sha256
`2cfc5a4853585879b0924f4c002ed4581dced02f061068d325c2cd3da130a509`, 366 lines).
Detector: the instrument's own `python3 -I -B <copy> --selftest` (9 cases), plus the
receipt returned by `evaluate()` for the two shapes the selftest never builds.
Verdict: **4 killed, 2 survived.** Both survivors are coverage holes in the selftest,
not defects in the landed predicate; the exact missing case for each is named below.

## Axes

- **coverage** — does the selftest have a case for every predicate clause the counter
  implements? Answer: no — clause 1 is only exercised from below (`21`) and clause 2 is
  exercised by no case at all.
- **depth** — does a surviving mutant change a real verdict? Yes for m1: a 23rd craft
  rule would be scored `met_target: true` while predicate clause 1 (`== 22`) is false.
- **calibration** — is a kill attributable to the case that is supposed to catch it?
  4/4 kills are, but m5 is killed only by `green`, and `red-interpreter-fails` passes
  *vacuously* under m5 (receipt says `skipped: True`, exit is still 1).

## Method (exact)

```
S=/fast/scratch/hyaku/kaidoku-r45/R45W1C1CounterMutants
git -C <lane> show f762b7273e3f6ca3c710bb37d5de92a4a4417aec:tools/round-45/c1-counter.py > "$S/pristine.py"
sha256sum "$S/pristine.py" <lane>/tools/round-45/c1-counter.py   # identical: 2cfc5a48…
python3 -I -B "$S/mutate.py"                                      # one asserted-once replacement per mutant
TMPDIR="$S" HYAKU_SCRATCH="$S" python3 -I -B "$S/<mutant>.py" --selftest
```

`mutate.py` aborts unless each anchor string occurs exactly once, so every mutant is a
single behavior-bearing hunk (diffs: `diffs.txt`, 6 hunks for 6 mutants). `--selftest`
builds its own throwaway git repos; `TMPDIR`/`HYAKU_SCRATCH` were pinned to `$S`, so
nothing was written under `/tmp`.

## Unmutated baseline (the line to record)

```
$ TMPDIR=$S HYAKU_SCRATCH=$S python3 -I -B $S/pristine.py --selftest
C1_SELFTEST: cases=9 failures=0
exit 0   stdout sha256 296734f224877a86e8d216bcde5382bbe0f18ff1dadddb1d18099f3754fdac6d
2026-10-28T15:40:53Z
```

Run twice, byte-identical stdout (`base1.out` / `base2.out` sha equality), so the
detector is deterministic and a red mutant cannot be noise.

## Results

| mutant | one-hunk change | exit | selftest line | named case that went red | verdict |
|---|---|---|---|---|---|
| m1-rule-blocks-ge | `if rule_blocks != 22:` → `if rule_blocks < 22:` | 0 | `cases=9 failures=0` | **none** (stdout byte-identical to baseline) | **SURVIVED** |
| m2-skip-marker-check | delete the `block22_present != 1` reason | 0 | `cases=9 failures=0` | **none** (stdout byte-identical to baseline) | **SURVIVED** |
| m3-any-exit-cell | exit-cell test → `if False:` | 1 | `cases=9 failures=1` | `red-bad-exit-cell` (expect 1, got 0) | killed |
| m4-ignore-unresolved | delete the `unresolved` reason | 1 | `cases=9 failures=1` | `red-bad-citation` (expect 1, got 0) | killed |
| m5-skip-selftest | `if run_selftest and block22_present == 1:` → `if False:` | 1 | `cases=9 failures=1` | `green` (expect 0, got 1) | killed (weakly) |
| m6-drop-frozen-arm | delete the `frozen_path_changed` exit-2 arm | 1 | `cases=9 failures=1` | `red-frozen-touched-is-exit-2` (expect 2, got 0) | killed |

Per-run exit codes, stdout sha256 and UTC stamps: `receipts.tsv`. Raw selftest output:
`{baseline,m1…m6}*.out`.

Kill detail for the four killed mutants (each is a single failing case, no collateral):

- m3: the exit-cell predicate is the only witness for `red-bad-exit-cell`; the row
  `| … | ok | … |` must produce exit 1 and does so only through `bad_exit`.
- m4: with the unresolved reason deleted, `red-bad-citation` drops from exit 1 to exit 0
  — the receipt still lists `corpus/lessons/round-44.md:9999` in
  `block22_unresolved_citations` but reports `met_target: true`.
- m5: `green` catches it because a skipped run leaves `selftest={"ok":False,"skipped":True}`
  and the "preflight selftest" reason fires on the good repo.
- m6: `red-frozen-touched-is-exit-2` turns 2 → 0; the counter then scores a repo whose
  frozen path was committed-after-freeze as met.

## Survivor 1 (m1) — hole: the rule-block count is only tested from below

Under m1 the whole selftest output is byte-identical to baseline
(sha `296734f2…`), so the 9 cases cannot see it. Cause: the only block-count case is
`red-relabelled-21-block`, which builds **21** blocks; `21 < 22` still fires under `>=`,
so the case keeps passing for the wrong reason. No case builds **23** blocks.

Real divergence, reproduced (`probe-holes.out`), repo = 22 plain rules + the perfect
marked block (23 blocks, 8 rows, 4 resolving refs, S140, interpreter, stub selftest ok):

```
probe H1 pristine : rule_blocks 23, failing ["rule_blocks 23 != 22"],              exit 1
probe H1 m1       : rule_blocks 23, failing [],                     met_target true, exit 0
```

**Exact case that should have caught it** (name `red-extra-rule-block`):

```python
def extra_block(d):
    f = make_repo(d, skill_with(22, good_block()), STUB_OK)   # 22 plain + block = 23
    return evaluate(d, f, f)
case("red-extra-rule-block", 1, extra_block)
```

Impact if left: SKILL.md gains one more craft rule and the counter silently keeps
`met_target: true` although predicate clause 1 (`rule_blocks == 22`) is false. This is a
coverage hole in the selftest only — `evaluate()` still implements `== 22`; nothing to
"fix" in the frozen instrument.

## Survivor 2 (m2) — hole: the marker clause is exit-code-redundant and never asserted

Under m2 the selftest output is again byte-identical to baseline. Removing the
`block22_present != 1` reason cannot change any exit code, and that is structural, not
luck: `rows`, `refs`, `header` and `cites` are only computed inside
`if block22_present == 1:` (line 144), so whenever `block22_present != 1` the receipt
carries `rows == 0`, `refs == 0`, `header_ok == False` and at least three other reasons
fire independently. Observed on both reachable shapes (`probe-holes.out`):

```
22 blocks, marker stripped : pristine exit 1 failing [… "block22_present 0 != 1", "block22_rows 0 < 8",
                             "block22 table header lacks trigger/arm/exit/receipt", "block22_refs 0 < 4"]
                             m2        exit 1 failing [ same list minus the block22_present entry ]
22 blocks, marker twice    : pristine exit 1 failing ["block22_present 2 != 1", …]
                             m2        exit 1 failing [ … same list minus that entry ]
```

So m2 is equivalent w.r.t. exit code; only the receipt text differs. The selftest asserts
`code == expect` and nothing else, which is why it survives.

**Exact case that should have caught it** (name `red-marker-absent`, receipt-asserting):

```python
def marker_absent(d):
    block = good_block().replace(MARKER, "<!-- unrelated -->")
    f = make_repo(d, skill_with(21, block), STUB_OK)          # 22 blocks, none marked
    return evaluate(d, f, f)
# needs a receipt-aware assertion, e.g.
#   code == 1 and any("block22_present" in r for r in receipt["failing"])
#   (and symmetrically for the duplicate-marker shape: block22_present == 2 must be reported)
```

Impact if left: none on today's verdicts. It matters only as a calibration defect — the
predicate clause 2 is enforced transitively, so a future refactor that stops zeroing
`rows`/`refs` outside the marker branch would silently drop the marker requirement with
no red case to notice. That is the reason to add the receipt assertion rather than the
case alone.

## Calibration finding on the m5 kill

m5 is killed by `green`, but `red-interpreter-fails` — the case whose stated purpose is
"an interpreter whose selftest fails scores 1" — still exits 1 under m5 for the wrong
reason (`probe-m5.out`):

```
red-interpreter-fails / pristine : exit 1 preflight_selftest {"cases":11,"exit":1,"failures":1,"ok":false}
red-interpreter-fails / m5       : exit 1 preflight_selftest {"ok":false,"skipped":true}
```

A case asserting `receipt["preflight_selftest"].get("exit") == 1` would make
`red-interpreter-fails` discriminating instead of vacuous. As written it cannot tell
"the interpreter ran and failed" from "the interpreter never ran".

## Instrument sanity against the real tree (context, not part of the probe)

Frozen bytes score the real repo as expected; both runs use the frozen counter directly
(`ctl-freeze.*`, `ctl-head.*`):

- `--freeze f762b727 --rev f762b727` → exit 1,
  `rule_blocks 21`, `block22_present 0`, `block22_rows 0`, `block22_refs 0` — exactly the
  "before" values `plans/round-45-claims.md` records for the do-nothing control, so the
  frozen counter reproduces the claim's stated before.
- `--freeze f762b727 --rev faa875bc` (HEAD) → exit **0**, `met_target: true`,
  `rule_blocks 22`, `block22_rows 10`, `block22_refs 7`, unresolved `[]`,
  cites S140 + interpreter, `preflight_selftest {cases:11, failures:0}`.
- `git log f762b727..HEAD -- plans/round-45-claims.md tools/round-45/` prints nothing:
  no frozen path was touched after the freeze, so the score is admissible.
- Observation for the L1: `SKILL.md` block 22 is already committed at HEAD
  (`e715263c`, amended by `1f4b27f8`), and `SKILL.md` is clean in the worktree
  (committed blob sha256 `19c20927…` == worktree sha256). Wave 1 is therefore verifying
  a landed tree, not a pre-landing one; the green receipt above is the current verdict.

## Restoration and integrity evidence

- The frozen original was never written: `sha256sum` of the lane file before and after
  all runs is `2cfc5a4853585879b0924f4c002ed4581dced02f061068d325c2cd3da130a509`; the
  blob extracted from the freeze commit has the same hash.
- `git -C <lane> status --porcelain tools/round-45 plans/round-45-claims.md` — empty;
  `git -C <lane> diff --stat` on those paths — empty. No staging, commit or checkout was
  run; all git calls were read-only.
- Each mutant lives in its own copy; `pristine.py` was re-hashed after the mutant and
  probe runs (unchanged), and the probes re-import the pristine copy, so no mutant state
  leaked between runs.
- Scratch `$S` was removed after every artifact was copied here; `manifest.sha256` lists
  the 26 files that survive under this directory.

## Reproduction

```
cd .ufo/waves/round-45/w1/R45W1C1CounterMutants
S=$(mktemp -d -p /fast/scratch/hyaku)          # any non-/tmp scratch
cp *.py "$S"/ && cd "$S"
sha256sum pristine.py                          # 2cfc5a48…
TMPDIR=$S HYAKU_SCRATCH=$S python3 -I -B pristine.py --selftest
python3 -I -B mutate.py                        # regenerate m1…m6 from pristine.py
for m in m*.py; do TMPDIR=$S HYAKU_SCRATCH=$S python3 -I -B "$m" --selftest; echo "$m rc=$?"; done
TMPDIR=$S HYAKU_SCRATCH=$S python3 -I -B probe_holes.py
```

`receipts.sh` is the exact runner used (per-run exit, stdout sha256, UTC stamp).

## Limits

- The detector is the instrument's own selftest. These verdicts say what that selftest
  can and cannot see; they are not an independent semantic audit of `evaluate()`.
- Two survivors were classified by construction of the missing shape and by structural
  argument; no claim is made that m1/m2 are the only survivors — I probed only the six
  assigned points.
- No tool was installed for this probe (python 3.14.8, git 2.x already present).
- Not run: `frozen-path-preflight.py --selftest` directly (exercised through the counter
  at HEAD, `cases=11 failures=0`); `c2-counter.py`.

## Artifacts

`manifest.sha256` (27 files): `report.md`, `receipts.tsv`, `diffs.txt`, `mutate.py`,
`probe_holes.py`, `probe_m5.py`, `receipts.sh`, `pristine.py`, the six mutant scripts and
their seven selftest outputs, `probe-holes.out`, `probe-m5.out`, `ctl-freeze.{json,out}`,
`ctl-head.{json,out}`.
