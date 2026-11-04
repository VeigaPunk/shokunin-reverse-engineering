# LabratProbe — round 76 (r76-w1)

**Hypothesis (falsifiable).** The round-75 printed R75-C1 counter command fails for exactly the
two reasons the gate's routed defect 4 names — the omitted required `--work` and the abbreviated
`--expect-target-sha256` digest — and no third.

**Subject.** After-arm line printed in the round-75 report's *Before → after measurements*
(`.ufo/reports/round-75/kaidoku.md`, R75-C1 after), line breaks joined, exactly as committed in
the C2 fixture `.ufo/waves/round-76/pre/fixtures/r75-printed.md`:

```
python3 -I -B tools/round-75/probe-mutation.py --root . --rev 538b8b81 --tool tools/round-75/seam-probe.py --patch-set r75probe --expect-survivors 0 --expect-target-sha256 1fc1c8fc… --expect-sole b-drop-canary-field
```

Probe environment: lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, lane HEAD
`201df797` (the worktree carried only pre-existing sibling edits; `git show <rev>:<tool>` is
rev-addressed and unaffected), Python 3.14.8, `python3 -I -B`, all scratch under
`/fast/scratch/hyaku/kaidoku-r76/RevengerProbe/`. Read-only: no lane file written except this
evidence; the battery wrote only under its `--work` scratch dir.

## Runs

### Run 1 — printed argv with the ellipsis (no `--work`)

```
python3 -I -B tools/round-75/probe-mutation.py --root . --rev 538b8b81 --tool tools/round-75/seam-probe.py --patch-set r75probe --expect-survivors 0 --expect-target-sha256 1fc1c8fc… --expect-sole b-drop-canary-field
```

- rc **2**, 30 ms, stderr empty.
- stdout: `{"unevaluable": "missing required arguments: work"}`
- Nothing executed: `main()` checks the four required options (`rev`, `tool`, `patch_set`,
  `work`) before any git read, pin check or generated copy.

### Run 2 — digest bound, `--work` still absent

Same argv with `--expect-target-sha256 1fc1c8fc6d08b8626ead431961f286753805a08893b73bdb2350261ad1ac410d`.

- rc **2**, 29 ms, stderr empty.
- stdout: `{"unevaluable": "missing required arguments: work"}` — identical to run 1; the
  missing-argument preflight precedes the pin check, so the ABBREVIATED digest is not the first
  branch reached.

### Run 3 — digest bound **and** `--work <fresh empty dir>` added

Same argv as run 2 plus `--work /fast/scratch/hyaku/kaidoku-r76/RevengerProbe/work3.tmpQcX`.
Run under `timeout --signal=TERM --kill-after=5 20`.

- rc **0**, **619 ms** — completed well inside the 20 s cap; no SIGTERM was delivered and no
  child survived (no `mut-text-*` process left).
- stdout 5067 bytes: `ok true`, `survivor_count 0`, `survivors []`, 15 `killed`, 0
  `killed_wrong_case`; `pristine {cases 25, failed [], rc 0}`; sole detector
  `b-drop-canary-field: true` with `failed ["a12-kernel-canary-field"]`;
  `target_pin {expect <full digest>, matched true, pinned true, pinned_before_exec true}`;
  `target_sha256` equals the bound digest; `runner.sha256 d7757ae2…`.
- Full stdout preserved at `LabratProbe/step3-stdout.json`
  (sha256 `83f20d17964f3d4faa80948952d0fda3c95cb7f37958e8d99e1dbb45218b7822`).
- `--json-out` was not supplied and is not needed; `--rev 538b8b81` resolves at this lane.

### Run 4 — `--work` added, abbreviated digest kept

Run 3's argv with `--expect-target-sha256 1fc1c8fc…`.

- rc **2**, 30 ms, stderr empty.
- stdout: `{"unevaluable": "target pin mismatch before execution: expected 1fc1c8fc\u2026, blob at 538b8b81:tools/round-75/seam-probe.py is 1fc1c8fc6d08b8626ead431961f286753805a08893b73bdb2350261ad1ac410d"}`
- The supplied work dir stayed empty: the pin is compared in `score()` before `score_text()`
  creates any generated copy, so nothing executed.

## Digest ground truth

`git show 538b8b81:tools/round-75/seam-probe.py | sha256sum` =
`1fc1c8fc6d08b8626ead431961f286753805a08893b73bdb2350261ad1ac410d` — the full digest the
report's line abbreviates, and the digest run 3 consumed.

## Conclusion

**Complete.** The two reasons the gate names are the complete set. The smallest additions that
make the printed command runnable are exactly (1) `--work <an existing empty directory>` and
(2) the full 64-hex `--expect-target-sha256` digest; with only those two changes the printed
command runs verbatim, exits 0 in 0.62 s, and reproduces the reported counter (`survivor_count
0`, 15/15 killed by their declared cases, pristine 25 green, pin matched before execution). No
`--json-out`, `--min-pristine-cases` or other flag is required, and `--rev 538b8b81` is valid.

The two defects are ordered, not independent at the surface: with both present the observed
message is the `--work` refusal (run 1 = run 2); the abbreviated digest only becomes visible
after `--work` is supplied (run 4). A static block-refuser such as `tools/round-76/plan-command.py`
sees the ellipsis first and refuses with `PLACEHOLDER_UNBOUND` (its r75-printed arm), which is
why the gate's two named reasons read as a pair.
