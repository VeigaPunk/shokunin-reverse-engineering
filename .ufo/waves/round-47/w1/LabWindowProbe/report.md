# LabWindowProbe — R47-C2 `window` class: is the landed empty window the one the record meant?

Seat: `LabWindowProbe` (round 47, wave 1). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Probe state pinned at **HEAD `09a9f912` (2026-10-28T18:01:45Z)**; the lane moved four times while
this probe ran (`07d2894e` -> `f54b3b6d` -> `31b092d1` -> `09a9f912`, measured revision `a0753786`).
Nothing in the lane tree was edited. `tools/round-47/record.py` at the pinned state is
sha256 `abf352573d156ed1388683c882e40cab9897f426b9448356993bf41bf37779e7` (A5 bytes); the frozen
window correction and the C2 claim row were unchanged across all four HEAD moves.

## 1. The four requested windows, measured

Exact command form (the same call `record.py:window_empty` makes, plus a `--` separator and the
`-m` / `--diff-merges` arms):

```
git -C <lane> log --name-status --format= [arm] <A>..<B> -- tools/round-46 plans/round-46-claims.md
```

Byte counts are raw stdout bytes (the 52-byte row below is 51 content bytes + final newline; my
first shell substitution stripped that newline and read 51). `sha256` is over raw stdout.

| window | arm | rc | bytes | sha256 (first 16) |
|---|---|---|---|---|
| `332f4884..58eb04b6` | (none) | 0 | **0** | `e3b0c44298fc1c14` |
| `332f4884..58eb04b6` | `-m` | 0 | **0** | `e3b0c44298fc1c14` |
| `332f4884..58eb04b6` | `--diff-merges=first-parent` | 0 | **0** | `e3b0c44298fc1c14` |
| `332f4884..58eb04b6` | `-m --diff-merges=first-parent` | 0 | **0** | `e3b0c44298fc1c14` |
| `0425224..58eb04b6` | (none) | 0 | **52** | `f7ace3d35eb91c95` |
| `0425224..58eb04b6` | `-m` | 0 | **52** | `f7ace3d35eb91c95` |
| `0425224..58eb04b6` | `--diff-merges=first-parent` | 0 | **52** | `f7ace3d35eb91c95` |
| `0425224..58eb04b6` | `-m --diff-merges=first-parent` | 0 | **52** | `f7ace3d35eb91c95` |
| `58eb04b6..58eb04b6` | (none) | 0 | **0** | `e3b0c44298fc1c14` |
| `58eb04b6..58eb04b6` | `--diff-merges=first-parent` | 0 | **0** | `e3b0c44298fc1c14` |
| `332f4884..332f4884` | (none) | 0 | **0** | `e3b0c44298fc1c14` |
| `332f4884..332f4884` | `--diff-merges=first-parent` | 0 | **0** | `e3b0c44298fc1c14` |
| `0425224..332f4884` | (none / `-m` / `--diff-merges=first-parent`) | 0 | **52** | `f7ace3d35eb91c95` |
| `0425224..0425224` | (none / `-m` / `--diff-merges=first-parent`) | 0 | **0** | `e3b0c44298fc1c14` |

The 52 bytes are exactly:

```
M	tools/round-46/attest.py
M	tools/round-46/gate.py
```

`git rev-list --merges` is 0 for `332f4884..58eb04b6` and for `0425224..58eb04b6`, so the
`--diff-merges` arms cannot differ on these ranges; that is measured above, not assumed.

## 2. Verdict: one non-degenerate empty window exists, and it is a re-anchoring

- **Yes**, exactly one non-degenerate candidate window is empty: `332f4884..58eb04b6` (0 bytes,
  rc 0, every arm). It is the window the landed correction names, and `record.py` reproduces it:
  `record.window_empty(lane, '07d2894e', '332f4884', '58eb04b6', ['tools/round-46',
  'plans/round-46-claims.md']) -> (True, None)`.
- It is empty **because the start endpoint is the last commit in all history that touches those
  paths**: `git log -1 --format='%h %s' -- tools/round-46 plans/round-46-claims.md` -> `332f4884`
  ("round-46 F5 ..."). For any tip at or after that commit the window is empty by construction.
- **The window the round-46 sentence literally wrote is not empty.** Its start is the declared
  round-46 freeze `0425224`, and `0425224..58eb04b6` is **52 bytes**: F5 (`332f4884`) modified
  `tools/round-46/attest.py` and `tools/round-46/gate.py`. So the record defect the correction
  names (`R46-V2`, an "empty" window that is not empty at the measured tip) is *true*, and the
  correction suppresses it by moving the start past the offending commit rather than stating it.
- The correction's clause "this is the concrete window it meant" is therefore unsupported as
  written. It is only defensible as "the measured freeze per the F5 amendment is `332f4884`
  (round-46 section, Amendment F5/A4/B1), so the frozen-set window it meant is post-F5". The
  landed sentence does not say that, and it omits the 52-byte fact.
- Degenerate self-windows (`58eb04b6..58eb04b6`, `332f4884..332f4884`) are also empty. That is
  the hole in section 3, not a property of the record.

Recommended edit (still green under the frozen counter, so it costs nothing):
keep `332f4884..58eb04b6` but state the falsified literal window explicitly — `0425224..58eb04b6`
is not empty (52 bytes, `M tools/round-46/attest.py`, `M tools/round-46/gate.py`); `332f4884` is
the last commit touching the frozen set, and it is the measured freeze the F5 amendment names.

## 3. Forgery: a vacuous window satisfies the frozen `window` correction

`record.py` (frozen, A5 bytes) accepts any empty pair as a `window` correction and never relates
it to the atom. Two clauses conspire:

- `record.py:206-219` — a window atom whose pair is a placeholder (`<tip>`) is
  `unverifiable`, i.e. always a mismatch until exempted;
- `record.py:333-336` — `exempt()` returns `True` for any placeholder window atom as soon as a
  `window` correction exists (the key is not compared for that branch);
- `record.py:271-279` — a `window` correction is checked only for "the pair reproduces as empty";
  the pathspec is split but never validated against the atom or against the tree.

Measured against the real card at `--rev 07d2894e` (current records.py, full battery on):

| mutated correction | counter | battery | meaning |
|---|---|---|---|
| as landed (`332f4884..58eb04b6`) | exit 0 | 3/0 | control |
| `empty in 58eb04b6..58eb04b6 -- tools/round-46 plans/round-46-claims.md` | **exit 0** | 3/0 | self-window; vacuous, accepted |
| `empty in 332f4884..332f4884 -- tools/round-46 plans/round-46-claims.md` | **exit 0** | 3/0 | self-window; vacuous, accepted |
| `empty in 0425224..58eb04b6 -- tools/round-46 plans/round-46-claims.md` | exit 1 | 3/0 | `corrections_bad: [{window: 0425224..58eb04b6, empty: false}]` |
| `empty in 58eb04b6..58eb04b6 -- no/such/path` | exit 1 | **1** | clause 3 accepts it (`corrections_bad []`); the counter only goes red because its own `non_empty` battery forgery then mutates a pair whose pathspec matches nothing and stays empty |
| window correction deleted | exit 1 | 1 | placeholder mismatch restored (kill rule holds) |

So: the counter *can* measure the difference between the landed window and the literal one (row 4),
but the exemption path never asks it to. A forger who wants the round-46 window atom exempted can
write `58eb04b6..58eb04b6` and score the whole predicate green without any true statement about
the round-46 freeze. Route to round 48: reject `A == B`, require the correction's pathspec to equal
the atom's pathspec (or resolve in the tree), and require the pair to sit inside the atom's round
range or explicitly declare that the start moved and why.

## 4. The `window` class cannot see a merge-carried change

`record.py:90-94` runs `git log --name-status --format= A..B -- paths` with **no** `-m` /
`--diff-merges` arm. That is the arm R46-CL6 is about, now inherited by C2. Fixture (evil merge:
the merge commit edits a path neither parent touched after the base):

```
fixture /fast/scratch/.../ev3-RrVp  base=4dc7335b tip=1728ae84  2026-10-28T18:01:37Z
parents: 26a54505 076845e1
git diff --name-status base..tip -- tools/x  ->  M	tools/x/a.txt
git log --name-status --format=            base..tip -- tools/x  ->  0 bytes
git log --name-status --format= -m         base..tip -- tools/x  ->  31 bytes
git log --name-status --format= --diff-merges=first-parent base..tip -- tools/x  ->  15 bytes
```

`record.window_empty(fixture, tip, base, tip, ['tools/x'])` returns `(True, None)` while
`git diff base..tip -- tools/x` shows the blob changed. So a correction can name a window that is
"empty" by the counter's own test while a frozen path in it was rewritten by a merge resolution.
The round-46 ranges here contain no merges, so the landed `332f4884..58eb04b6` is genuinely empty
under every arm; the defect is in the class, not in this instance.

## 5. Secondary falsifications found while probing the same counter

### 5a. `- corrects axes …` lines are parsed by nothing

`CORR` (`record.py:50`) is `^- corrects (seats|window|path|rev) (\S+):` — no `axes`. The landed
section prints **four** `- corrects` lines; `record.corrections()` parses **two** (seats, window).
Measured at `07d2894e`:

- card as landed: exit 0, `corrections 2`, `corrections_bad []`;
- `- corrects axes coverage: 1/1` (false): exit 0, `corrections_bad []`;
- `- corrects axes does-not-exist: 1/1` (no such atom): exit 0, `corrections_bad []`.

So the section's own sentence "each `corrects` line below ... is itself re-derived by the counter"
is false for the two `axes` lines, and the claims file's clause 3 ("an `axes` correction must state
`<resolved>/<total>`") is unimplemented in the frozen interpreter. The card's `corrections 2`
quoted in the C2 row is literally correct and materially misleading: four lines are shown to a
reader as re-derived evidence, two are inert text.

### 5b. The C2 claim row contradicts the receipt it cites

At HEAD `09a9f912` the row reads `over 50 atoms ... exit 0, atoms 50, mismatches [], corrections 2
both re-derived, exempted 2 <= 3, battery correction_forgeries 3 / forgeries_green 0
(c2-at-A7.json)`, `measured at 1e2c310295`.

- `c2-at-A7.json` is at rev `a0753786` and reports `atoms 42`, `verified 41`, `exempted 1`,
  `corrections 2`, `corrections_bad []`, battery `3/0`, exit 0.
- First-hand re-run at `a0753786` (current records.py, `--json-out` inside
  `.ufo/waves/round-47/w1/LabWindowProbe/`): identical — `atoms 42`, `exempted 1`, exit 0.
- `atoms 50 / exempted 2` is the number for the earlier section pair (round-45 + round-46, rev
  `1e2c310295`), not for the A7 measurement. Two numbers in the row are stale copies.

This is the same defect class C2 exists to close (a self-assessment false about its own
measurement), and no atom class checks quoted measurement numbers: `record.py` collects
`seats/window/path/rev/axes` only, so `atoms 50` is unchecked prose.

### 5c. Freeze series: C2's interpreter cannot detect its own drift

Observed during this probe: the declared freeze moved `5017e1f` -> A4 `1e2c310295` -> A5
`07d2894e` -> A6 `f54b3b6d` while the probe ran, and `A1..A6` each rewrote bytes in
`tools/round-47/` after the freeze declared before it. `record.py` has no `--freeze` argument and
never calls `gate.freeze_state`; only `exact.py` does, so the claims-file sentence "a change makes
both counters exit 2 `frozen_path_changed`" holds for C1 only. Measured:

```
python3 -I -B tools/round-47/exact.py --root . --freeze 07d2894e --rev f54b3b6d ...
  -> exit 2, frozen_path_changed ["tools/round-47/", "tools/round-47/exact.py"]
python3 -I -B tools/round-47/exact.py --root . --freeze 5017e1f --rev f54b3b6d ...
  -> exit 2, frozen_path_changed ["plans/round-47-claims.md", "tools/round-47/",
                                  "tools/round-47/exact.py", "tools/round-47/record.py"]
```

Consequence for C2: its before/after receipts were produced by different interpreter bytes
(`record.py` sha256 `c704c3d4…` at A4, `abf35257…` at A5/A6) and no clause of C2 notices. The A5
fix exists precisely because the A4 battery was layout-dependent: A4 bytes at rev `1e2c310295`
score exit 0 (`battery 3/0`) but at rev `07d2894e` score exit 1 (`battery forgeries_green 1`),
because the forgery appended a `- corrects` line at end-of-file, inside the corrections section
only when that section is the last block. That property, not the forgery, produced the A4 green.

## 6. Not run / limits

- The `--diff-merges` arms were exercised only on these linear ranges and on the fixture; no other
  merge topology was tested.
- I did not re-run `record.py` at the base `13a9e9e1` (the 4-mismatch before-state) — the
  `ctl-c2-0-do-nothing.json` control was taken as given, not re-verified.
- I did not evaluate R47-C1's clauses; `exact.py` was invoked once, only to demonstrate freeze
  drift.
- No claim verdict is offered here. No installs were made; no tool was added or upgraded.

## 7. Evidence

All under `.ufo/waves/round-47/w1/LabWindowProbe/`:

- `window-receipt.json` — 24 runs (6 windows x 4 arms) with exact command, rc, raw bytes, full
  sha256, UTC.
- `c2-at-1e2c310295.json`, `c2-at-07d2894e.json`, `c2-at-a0753786.json` — first-hand record.py
  receipts at the three revisions named above.
- `A4code-at-1e2c310295.json`, `A4code-at-07d2894e.json` — the A4 interpreter (sha `c704c3d4…`)
  run at both revisions: exit 0 / exit 1, the layout-dependent battery.
- `exact-freeze-07d2894e-at-A6.json`, `exact-freeze-5017e1f-at-A6.json` — freeze drift.
- `receipts/forgery_probe.out` (+ `.py`) — the five window-correction mutations with battery.
- `receipts/axes_probe.out` (+ `.py`) — parsed vs printed corrections; false and ghost axes lines.
- `receipts/evil-merge-transcript.txt` — evil-merge fixture, all four log arms.
- `receipts/*.out` — raw console transcripts for every run above.

Scratch `/fast/scratch/hyaku/kaidoku-r47/LabWindowProbe` (including the two git fixtures) was
removed after these receipts were copied; the transcripts above are the citable evidence.
