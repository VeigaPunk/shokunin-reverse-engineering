# ScribeLesson — round 47 wave 1: verification of the two frozen counters, the lesson draft, and eleven findings

Seat `ScribeLesson` (leaf). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Read-only on
the lane tree: everything written here is under `.ufo/waves/round-47/w1/ScribeLesson/`, plus this
file. No commit, push, stage or mutating git ran in the lane; the only git mutations were in
fixture repos and one `git clone` into scratch. No tool was installed.

Revisions used, all named explicitly: first freeze `5017e1f7`; base `13a9e9e1`; before-state
`3186f69b` (the tip before the landing); landing `e856beb5`; `1e2c3102` (after A4); verification
tip `a631bba0` (A5 in the record). The lane advanced twice while I was measuring; every receipt
records the `--rev` it was produced at, and the tip rows were re-measured at `a631bba0`.

## Behaviour: what the two counters actually return

| counter | command | exit | differing value |
|---|---|---|---|
| R47-C1 at the `3186f69b` before-state | `python3 -I -B tools/round-47/exact.py --root . --freeze 5017e1f7… --rev 3186f69b… --json-out …` | 1 | `block_present 0`, `rule_blocks 23`, `marker_occurrences 0` — the claims' Before bullet reproduces exactly |
| R47-C1 at the landing `e856beb5` | same, `--rev e856beb5` | **2** | `frozen_path_changed` |
| R47-C1 at `1e2c3102` | same | **2** | `frozen_path_changed ["plans/round-47-claims.md","tools/round-47/","tools/round-47/record.py"]` |
| R47-C1 at the tip `a631bba0`, `--freeze` = the frozen file's own formula `git log -1 -- plans/round-47-claims.md` = `62e33f7d` | same, freeze substituted | **2** | `frozen_path_changed ["tools/round-47/","tools/round-47/record.py"]` |
| R47-C1 at the tip, `--freeze` = the A5 paragraph's "declared freeze" `07d2894e` | same, freeze substituted | **0** | met; `block_present 1`, `rule_blocks 24`, `rows 4`, `refs 8`, battery `4/4/0/1` |
| R47-C2 at `3186f69b` | `python3 -I -B tools/round-47/record.py --root . --rev 3186f69b… --json-out …` | 1 | 4 mismatches: seats r45 (`wave 2: 32` vs dispatched `36`), window r46 (`<tip>` placeholder → `unverifiable`), axes coverage `133/133` vs `138/138`, axes depth `20/20` vs `23/23`; `corrections 0 < 2` |
| R47-C2 at the landing `e856beb5` | same, `--rev e856beb5` | 0 | met; `atoms 50`, sections `45+46`, `corrections 2`, `exempted 2` |
| R47-C2 at the tip `a631bba0` | same, `--rev a631bba0` | 0 | met; `atoms 42`, sections `46+47`, `exempted 1` (the round-46 `<tip>` atom, still in the card) |

C2 is met at every revision I measured, including the two that rewrote its own frozen
instrument — it has no freeze arm to fail. C1 is met only under one of the three freeze values
the frozen claims file itself supplies.

## Gates

Both documented selftest invocations, run as the registry rows spell them:

| gate | command | result |
|---|---|---|
| C1 selftest | `exact.py --selftest --root . --freeze 5017e1f7… --rev 3186f69b…` | exit 0, `EXACT_SELFTEST: cases=16 failures=0` — matches `SKILL.md:1748` |
| C2 selftest | `record.py --selftest --root . --rev 3186f69b…` | exit 0, `RECORD_SELFTEST: cases=10 failures=0` — `SKILL.md:1749` says **9** (F9) |
| C1 discrimination battery | inside `exact.py` at the A5 freeze | `forgeries_total 4 / v2_green 4 / v3_green 0 / genuine_green 1 / crash 0` — the four holes are measured, not asserted |
| C2 discrimination battery | inside `record.py` at the tip | `correction_forgeries 3 / forgeries_green 0` |
| positive controls (must stay red) | `receipts/c1-inproc.json` | `blobberish` → 1; duplicate routed id → 1; three-of-four digest → 1; swapped flag pair → 1 |

## Findings

Each line is: what is wrong, the exact command, the differing value, and a path that shows it.
None of these is a request to edit frozen bytes. (The `F*` ids here and the `M47-*` ids in
`lesson.md` are separate sequences: `F*` orders by severity, `M47-*` orders as the lesson's
mistake table reads.)

**F1 (HIGH, C1) — the claim has three freeze values and two of them return 2.**
`exact.py` takes `--freeze`; the frozen claims file defines `<FREEZE>` three ways: the commit
that first contains it (`5017e1f7`, and every control in `.ufo/waves/round-47/controls/` uses
it), its own formula `git log --format=%H -1 -- plans/round-47-claims.md` (`62e33f7d`, the A2
commit), and the A1/A5 paragraph's "declared freeze" (`07d2894e`). At the tip `a631bba0` those
give **2, 2, 0** respectively. Receipts: `receipts/tip-a631-exact.json`,
`receipts/formulafreeze-head-exact.json`, `receipts/a5freeze-head-exact.json`. The artefact is
not in question — `--freeze 07d2894e` and `--freeze 1e2c3102` both return 0 with
`rule_blocks 24`, `rows 4`, `refs 8` and the full battery. Repair, in the claims file only:
pin the literal `<FREEZE>` in the Counting command line to the A5 commit and re-label the
`ctl-c1-0` before-control as measured at *the first freeze* rather than *the freeze*. Note that
the frozen text's sentence "a change makes **both** counters exit 2" is false for C2 (F2).

**F2 (HIGH, C2) — the calibration counter has no freeze arm at all.**
`python3 -I -B tools/round-47/record.py --help` offers `--root/--rev/--no-battery/--selftest/--json-out`;
there is no `--freeze`, `grep -n "freeze\|frozen" tools/round-47/record.py` returns nothing, and
the module never calls `gate.freeze_state`. At `1e2c3102` C1 returns 2 and C2 returns 0 met
(`receipts/tip1e2c-exact.json` vs `receipts/tip1e2c-record.json`), so the counter that grades the
record cannot notice the record's instrument being rewritten. Repair: take `--freeze`, call
`gate.freeze_state(root, freeze, rev, "plans/round-47-claims.md")`, and add the selftest case
"a commit that edits `tools/round-47/record.py` after the freeze is exit 2" — the case fails
today and passes after the arm is bound.

**F3 (HIGH, C1) — the executed `gate.py` is outside the frozen set, so five worktree lines forge a met verdict.**
`exact.py` pins `tools/round-47/exact.py` with `interpreter_sha256` and freezes `tools/round-47/`
+ the claims file, then imports and executes `tools/round-46/gate.py` for every read.
`receipts/atk-c1-gate-overlay.py` clones the lane at `3186f69b`, inserts five lines in the
worktree copy of `tools/round-46/gate.py` so `show(..., "SKILL.md")` answers a fabricated block
24 for the clone root only, and runs the frozen command: before, exit 1 `block_present 0`;
after, **exit 0 `met_target true`** with the battery `4/4/0/1`, against a committed `SKILL.md`
with `marker_occurrences 0` and the counter's own `rule_blocks 23`. Receipt
`receipts/gate-overlay.json`; `git status --porcelain` inside the clone shows exactly
`M tools/round-46/gate.py`. This is R46-CL10's door, re-opened at the shared core. Repair:
add `tools/round-46/gate.py` to `## Frozen paths` or pin its sha256 in the block beside
`interpreter_sha256`.

**F4 (HIGH, C2) — the `seats` class derives from the dispatch spec, so an undispatched wave counts as 40 seats.**
`record.dispatch_counts` reads `.ufo/waves/round-N/w*-dispatch.json → counts.spawn`. Round 46
committed `w2-dispatch.json` with `spawn 40`, has **one** file under `w2/`
(`swarm-registry.json`) and **zero** `results.json`, and the commit that adds that dispatch file
says "the wave-2 spec left undispatched". The counter therefore verifies `Waves: 40 + 40 = 80
seats`, the claim R46-V1 falsified. Receipt `receipts/c2-clauses.json` `F4`:
`derive → [true, {claimed [40,40,80], derived [40,40,80], dispatch [40,40]}]`,
`round46_results_json_at_rev 0`, `dispatch_commit 22fd0d6b … the wave-2 spec left undispatched`.
Repair: derive seats from a settlement artefact (a `*-results.json`, or the count of seat
reports at `--rev`) and keep `dispatch.spawn` as a separate, differently-named atom.

**F5 (HIGH, C2) — the `window` class uses the log form that C1 exists to forbid.**
`record.window_empty` runs `git log --name-status --format= A..B -- paths`. Fixture
`/fast/scratch/hyaku/kaidoku-r47/ScribeLesson/fx-merge` (built with `git commit-tree`, so its
history is one commit deep): plain form stdout `""`; `-m --diff-merges=first-parent` stdout
`"M\ttools/round-46/gate.py"`; the reversed pair prints it twice; `git diff --name-status base
merge` prints it once; `record.window_empty(...)` returns `{"empty": true}`. Receipt
`receipts/merge.json`. So a window claim is satisfiable by a range in which a merge resolution
edited a frozen path — R46-CL6's blindness, closed for `gate.py` by block 24's row 4 and open
here. Repair: the armed, ordered form plus a selftest case built from this `commit-tree` fixture.

**F6 (MEDIUM, C1) — clause 5 binds the token, not the pairing, and reads neither prose column.**
`score()` only tests `r[2].strip("` ") ∈ {"symbol","once","digest","order"}`. Rotating the four
tokens across the four routed ids exits **0**; emptying every `v2 hole` cell to `—` exits **0**.
Receipt `receipts/c1-inproc.json` (`A2-arm-token-rotated-against-holes`, `A2b-hole-column-emptied`);
same-file controls show the clause does catch `blobberish` (exit 1) and the genuine block (0).
This is R46-CL7 in the column the block labels `v3 arm`. Repair: a fixed `{id → token}` map plus
one selftest case per single swap.

**F7 (MEDIUM, C1) — clause 1's "last craft block" sees only `- **` bullets.**
`blocks_of` splits on `(?m)^- \*\*`, so a 25th rule written as `### 25. …` or `* **25. …**` leaves
`block_is_last` true: both exit **0** (`receipts/c1-inproc.json`, `A1-later-rule-as-heading`,
`A1b-later-rule-star-bullet`).

**F8 (MEDIUM, C2) — `axes` corrections are never parsed.**
`CORR = ^- corrects (seats|window|path|rev) (\S+): (.+)$` excludes `axes`, so the `axes` branch of
`corrects()` is dead and clause 3's "an `axes` correction must state `<resolved>/<total>`" is
unreachable. The landing writes four correction lines, two of them `axes`
(`SCORECARD.md:3669-3678`), and the counter reports `corrections 2`.
`receipts/c2-clauses.json` `F1_corrections_parsed` is `[]` for a card carrying only axes lines,
and `F1` reports `corrections 0`. Repair: add `axes` to the alternation and re-derive the stated
fraction (`138/141` must go red).

**F9 (LOW) — the registry case count is stale by one.** `receipts/self-record.txt` prints
`RECORD_SELFTEST: cases=10 failures=0`; `SKILL.md:1749` says "9 cases". R46-CL8 verbatim on the
new instrument. The `exact.py` row (`16 cases`) matches (`receipts/self-exact.txt`).

**F10 (LOW) — the claims file names a control that does not exist.**
`plans/round-47-claims.md` names `controls/ctl-c1-1-v2-profile.json` ("produced after the landing");
`git ls-tree -r --name-only HEAD .ufo/waves/round-47/controls` lists four files and not this one,
although the landing has happened. R46-V7 verbatim.

**F11 (MEDIUM) — the record's atom count contradicts the counter at the same revision.**
`## Round 47` says "over 50 atoms" and "4 → 0 mismatches over 50 atoms"; appending that section
moved the last-two window from `45+46` to `46+47`, so the counter derives `atoms 42` at the tip.
`receipts/landing-e856-record.json` (`atoms 50`, sections `45+46`) vs
`receipts/tip-a631-record.json` (`atoms 42`, sections `46+47`). The before and after counts are
also taken over different populations. No clause reads either number.

## What holds, and must not be "repaired"

Verified this round, with the witness in parentheses: clause 4's multiset equality (duplicate id
→ 1); clause 6's digest pin (three-of-four → 1); clause 7's literal and order (swapped pair → 1,
and on a real repo the reversed pair prints the merge twice — `receipts/merge.json`); clause 8's
eight refs all carry selectors and resolve, `corpus/lessons/round-46.md` among them;
`interpreter_sha256` equals the bytes at `--rev` (`dcef54f1…`); the block is marker-unique and
last; the C2 `path` (12 at the before-state, 8 at the tip) and `rev` atoms all verified; the
C2 before-state reproduces the claims' four mismatches exactly, including the round-45 seat
atom's `40/36` dispatch values.

## Touched surfaces

- Written (only): `.ufo/waves/round-47/w1/ScribeLesson/` — `lesson.md`, `MANIFEST.txt`,
  `self-exact.txt`, `self-record.txt`, `receipts/` (12 counter receipts, 4 attack scripts).
- Written: this file, `.ufo/waves/round-47/w1/ScribeLesson.md`.
- Read-only: `SKILL.md`, `SCORECARD.md`, `plans/round-47-claims.md`, `tools/round-47/*`,
  `tools/round-46/gate.py`, `corpus/lessons/*`, `corpus/SOURCES.md`, `.ufo/waves/round-4{5,6,7}/*`.
- Fixtures: `/fast/scratch/hyaku/kaidoku-r47/ScribeLesson/{fx-merge,clone}` and the counters'
  own `gate.scratch` roots. Scratch removed after the receipts were copied here.
- No install; no change to `~/.local/bin` or any PATH directory.

## Out of scope

No product code, no judge, no commit/push/publish/deploy, no edit to `SKILL.md`, `plans/`,
`tools/`, `corpus/`, `LOG.md`, `SCORECARD.md`, no fleet-repo write, no sibling lane. I did not
"fix" frozen bytes: F1 and F2 are reported as defects of the claim, not as edits.

## Artifacts

- `receipts/MANIFEST.txt` — every artefact's sha256, byte count, UTC mtime, and the command and
  exit code that produced it.
- `receipts/*.json` — counter runs at `3186f69b`, `e856beb5`, `1e2c3102`, `a631bba0` under the
  three freeze values, plus the four attack receipts.
- `receipts/atk-c1-inproc.py`, `atk-c1-gate-overlay.py`, `atk-c2-clauses.py`,
  `atk-c2-merge-window.py` — re-runnable attacks; each prints its own JSON.
- `lesson.md` — the `corpus/lessons/round-47.md` draft: the `## Mistakes` table (M47-1..M47-11),
  the routing table for R46-CL1..CL11 and V1..V10 with the witness for each, the `## Gate`
  (S142/S143 admitted on re-measured bytes, S144 rejected with its flip condition) and the
  census line 142 → 144.

The two fixture paths quoted above (`…/fx-merge`, `…/clone`) live under the scratch root, which
the contract requires removing at yield; both are rebuilt byte-for-byte by
`receipts/atk-c2-merge-window.py` and `receipts/atk-c1-gate-overlay.py`, and the receipts record
the values they produced before removal.
