# LabWindowProbe — R47-C2 `window` class probe (round 47, wave 1)

Pinned at HEAD `09a9f912`, 2026-10-28T18:01:45Z. Full report + receipts:
`.ufo/waves/round-47/w1/LabWindowProbe/report.md` and `.../LabWindowProbe/`. No lane file edited.

## Probe result

`git -C <lane> log --name-status --format= [arm] <A>..<B> -- tools/round-46 plans/round-46-claims.md`
(raw bytes, rc 0 in every cell; `--diff-merges` arms identical because `git rev-list --merges` is 0
for both ranges):

| window | none | `-m` | `--diff-merges=first-parent` | `-m --diff-merges=first-parent` |
|---|---|---|---|---|
| `332f4884..58eb04b6` (landed correction) | 0 B | 0 B | 0 B | 0 B |
| `0425224..58eb04b6` (literal record window) | **52 B** | 52 B | 52 B | 52 B |
| `58eb04b6..58eb04b6` | 0 B | 0 B | 0 B | 0 B |
| `332f4884..332f4884` | 0 B | 0 B | 0 B | 0 B |
| `0425224..332f4884` (extra) | 52 B | 52 B | 52 B | 52 B |
| `0425224..0425224` (extra) | 0 B | 0 B | 0 B | 0 B |

52-byte content: `M\ttools/round-46/attest.py` + `M\ttools/round-46/gate.py`; sha256
`f7ace3d35eb91c95df996df7551a8b65b132400cd97b0c45fc25eaa81483a282`. Empty sha256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## Findings

1. **The correction is empty, but only by re-anchoring.** `332f4884` is the last commit in all
   history touching the round-46 paths (`git log -1 --format=%h -- tools/round-46
   plans/round-46-claims.md` -> `332f4884`), so the landed window is empty by construction. The
   record's literal start `0425224` is **not** empty: 52 bytes, F5 rewrote
   `tools/round-46/attest.py` and `gate.py`. The claim "this is the concrete window it meant"
   is unsupported; the honest sentence is "F5 (`332f4884`) is the measured freeze the F5 amendment
   names, and `0425224..58eb04b6` is not empty (52 bytes)". Cost of saying so: none, the frozen
   counter stays green.
2. **Vacuous corrections score green.** Against the real card at `07d2894e`, replacing the window
   with `58eb04b6..58eb04b6` or `332f4884..332f4884` leaves the full counter at exit 0, battery
   3/0. `record.py:333-336` exempts any placeholder window atom for any window correction, and
   `:271-279` only tests emptiness and never validates the pathspec (a `-- no/such/path`
   correction passes `corrections_bad`). The only mutation that goes red is the literal
   `0425224..58eb04b6` (`window not empty`) — the counter can measure the truth, the exemption
   path never asks for it.
3. **Merge-carried changes are invisible to the class.** `window_empty` (`record.py:90-94`) has no
   `-m`/`--diff-merges` arm. Evil-merge fixture: blob changes (`git diff base..tip -- tools/x` ->
   `M`), `git log --name-status --format=` prints **0 B**, `--diff-merges=first-parent` 15 B, `-m`
   31 B; `record.window_empty` returns `True`. R46-CL6 inherited, now inside C2.
4. **`- corrects axes …` is parsed by nothing.** `CORR` (`record.py:50`) lacks `axes`; the landed
   section prints four corrections, the counter parses two. `- corrects axes coverage: 1/1` and
   `- corrects axes does-not-exist: 1/1` both leave exit 0, `corrections_bad []`. The section's
   "each `corrects` line is itself re-derived" is false for the axes lines; claims-file clause 3's
   axes rule is unimplemented.
5. **The C2 row contradicts its own receipt.** At HEAD the row reads `atoms 50 … exempted 2 <= 3`
   citing `c2-at-A7.json`; that receipt (rev `a0753786`) reports `atoms 42, verified 41,
   exempted 1, corrections 2, battery 3/0`, reproduced first-hand. `atoms 50 / exempted 2` belongs
   to the earlier `1e2c310295` section pair. No atom class checks quoted measurement numbers.
6. **C2 cannot detect its own freeze drift.** The declared freeze moved
   `5017e1f` -> A4 -> A5 -> A6 during this probe; each amendment rewrote frozen interpreter bytes.
   `record.py` has no `--freeze` and never calls `gate.freeze_state`, so the claims-file promise
   "a change makes both counters exit 2 `frozen_path_changed`" holds for C1 only. Measured:
   `exact.py --freeze 07d2894e --rev f54b3b6d` -> exit 2 `["tools/round-47/",
   "tools/round-47/exact.py"]`; `--freeze 5017e1f` also lists `plans/round-47-claims.md` and
   `record.py`. The A4 green was layout-dependent: A4 record.py (sha `c704c3d4…`) is exit 0 at
   rev `1e2c310295` but exit 1 (`forgeries_green 1`) at rev `07d2894e`.

## Repair suggestions (no frozen byte touched)

- Reword the window correction to state the 52-byte literal window and cite the F5 re-declaration.
- Fix the C2 row: `atoms 42`, `exempted 1`, receipt rev `a0753786`.
- Route to round 48: reject `A == B`; bind the correction pathspec to the atom's pathspec (or tree
  resolution); add a merge-aware arm to `window_empty`; either implement `axes` corrections or stop
  printing them as re-derived; give `record.py` the same `--freeze`/`frozen_path_changed` arm.

Not run: base-revision before-state re-execution, any C1 clause, any other merge topology. No
installs. Scratch removed after receipts were copied.
