# CritC2Calibration — R47-C2 challenged as *calibration*

Seat `CritC2Calibration`, round 47, wave 1. Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Read-only on the lane; every number below is
reproduced at the revision named beside it.

Measured revisions: base `13a9e9e1`, first freeze `5017e1f7`, A2 `62e33f7d`, A3 `2e4ae434`,
A4 `1e2c3102`, A5 `07d2894e`, A7 `a0753786`, R4 `31b092d1`, `09a9f912`, and the tip
`b1a058f3` (2026-10-28T18:11Z). The lane moved six times while I measured; every receipt names
its own revision, and `receipts/tip/` holds the tip re-measurement. Where a finding was repaired
mid-session I say so and give both revisions.

## Verdict — one line

**Predicate too weak.** At the tip `b1a058f3` (and at `09a9f912` before it) the counter's
`mismatches == []` rests on
39 of 44 atoms being token-resolvability (a backticked hex resolves, a `.ufo/waves/…` path exists);
of the 5 claim-carrying atoms, 1 is exempted, 1 is the round-46 seat total that the non-author
spot-check routed as the HIGH false claim (R46-V1) — *certified green* — and the calibration row
that would carry this claim's own score is not an atom at all. Here is what closes it: §7.

## 1. What "zero mismatches" is made of

Receipt `receipts/tip/c2-atom-census.json` (rev `b1a058f3`, 44 atoms — identical in shape at
`09a9f912`, `receipts/c2-atom-census.json`):

| class | atoms | kind | what a green atom proves |
|---|---|---|---|
| `rev` | 31 | token | a backticked 7–40 hex token resolves **and** is an ancestor of `--rev` |
| `path` | 8 | token | an `.ufo/waves/round-N/…` token exists at `--rev` |
| `seats` | 1 | content | round 46's `40 + 40 = 80 seats` (see §3 — verified, and false) |
| `window` | 2 | content | r46 placeholder (exempted), r47 `is empty` sentence (true) |
| `axes` | 2 | content | `coverage 138/138`, `depth 24/24` heads |

- **39/44 = 89 % are token atoms.** They cannot be false unless a merge rewrote history.
- **5 content atoms**, of which **1 is exempted** (annotation, not repair) and **2 are axis heads**.
- The `## Owned axes` table has three rows — `coverage`, `depth`, `calibration` — and
  `AXIS_ROW = (?m)^\|\s*(coverage|depth)\s*\|` (`record.py:41`) sees only two. **The calibration
  row is the one row the calibration counter never reads.**
- The counter takes no `--freeze`, pins no bytes (`grep -c 'freeze\|sha256' tools/round-47/record.py`
  → `0`, `0`), and its receipt carries no `freeze`/pin field
  (`receipts/c2-at-live.json`). `exact.py` gets `freeze_state` from `gate` (`exact.py:400-421`);
  `record.py` does not. So a C2 receipt cannot show *which* instrument produced it — material,
  because `record.py` changed five times after the first freeze (§6).

## 2. The claim's own ledger row is contradicted by the receipt it cites

`SCORECARD.md` `## Round 47`, row `R47-C2`:

> exit 0, `atoms 50`, `mismatches []`, `corrections 2` both re-derived, `exempted 2 <= 3`, …
> (`.ufo/waves/round-47/l1/scores/c2-at-A7.json`) … measured at `1e2c310295`   ← at `09a9f912`
> exit 0, `atoms 42`, … `exempted 2 <= 3` … (same receipt, same measured-at)      ← at `b1a058f3`

Receipts `receipts/ledger-vs-receipt.json` (`09a9f912`) and `receipts/tip/ledger-vs-receipt.json`
(`b1a058f3`):

| source | rev | atoms | exempted |
|---|---|---|---|
| ledger row at `09a9f912` | — | 50 | 2 |
| ledger row at `b1a058f3` (tip) | — | 42 | **2** |
| `## Owned axes` calibration row at `b1a058f3` | — | 42 | **1** |
| `c2-at-A7.json` — the file both rows cite | `a0753786` | 42 | **1** |
| `c2-at-A4.json` — the ledger row's *measured at* | `1e2c3102` | 50 | 2 |
| live counter at `b1a058f3` | `b1a058f3` | 44 | 1 |

- At `09a9f912` the row paired A4's figures (50 atoms, 2 exemptions) with the A7 file (42, 1), and
  the axis row in the same card already said 42 atoms / `exempted 1`. **The card contradicted
  itself about one receipt.**
- The atoms figure was repaired at `6f9fd7f8` ("record quotes its own receipts (atoms 42,
  exempted 1)"). **The `exempted 2 <= 3` figure was not**: at the tip the ledger row still states 2
  while the receipt it cites, and the axis row beside it, both state 1. Counter exit 0.
- Timeline (`receipts/tip/c2-timeline.json`): atoms 50 / exempted 2 for `62e33f7d`–`1e2c3102`
  (sections 45+46), 41 / 1 from `caafeffa` (sections 46+47), then 42, 44.

**No clause of R47-C2 can see any of this**: `atoms`, `exempted`, the cited receipt's content and
the measured-at cell are all outside the atom set. That is the direct answer to this seat's
question — the counter measures the prose of two round sections, not the self-assessment's own
numbers, and a claim row is exactly where those numbers live.

## 3. A routed HIGH record defect is certified **true** by the counter

`seats` atom, round 46: `Waves: 40 + 40 = 80 seats` → `derive(…) → ok True`, derived
`[40, 40, 80]` from `.ufo/waves/round-46/w{1,2}-dispatch.json` (`counts.spawn 40, 40`).

Evidence that the claim is the one the spot-check routed as false (`receipts/record-open-defects.json`,
all at the live rev):

```
git -C <lane> ls-tree -r --name-only <rev> .ufo/waves/round-46 | grep '\.ready'
  .ufo/waves/round-46/w1.ready
  .ufo/waves/round-46/w1.ready.dispatched          # wave 2 has no ready marker at all
… | grep -c 'results\.json$'   → 0                  # LOG.md cites {w1,w2}-results.json
git -C <lane> log --format='%H %ci %s' -- .ufo/waves/round-46/w2-dispatch.json
  22fd0d6b…  round-46: the wave-1 evidence (32 settled seat reports of 40 dispatched),
            the wave-2 spec left undispatched, and the round's receipts
round 45 (a wave pair that *was* dispatched): w1.ready, w2.ready
```

`dispatch_counts()` (`record.py:78-95`) reads `counts.spawn` from the **spec**; the marker
convention that distinguishes "spec written" from "dispatched" exists in this repo (round 45) and
is ignored. Consequence: the counter affirms the SCORECARD half of R46-V1, and it will affirm it
for as long as the round-46 section is in the two-round window.
Smallest safe correction (§7.1): a wave counts only when `<wave>.ready.dispatched` (or a
`*-results.json`) exists at `--rev`.

## 4. Exemption is annotation, and the annotation machinery has nine holes

Fixture driver: `fixtures/c2-attack.py` (14 cases; run command in §12). `receipts/c2-attack-cases.json`
= `reproduced 14 / 14`, `green_by_defect 9`, exit 0.

| # | case | expect | got | why a green here is blindness |
|---|---|---|---|---|
| 0 | control-honest-card | 0 | 0 | control |
| 1 | seats-split-false-totals-true | 0 | 0 | `corrects()` binds `(n_waves, sum)` only; claimed 20/20 vs dispatched 30/10 is exempted by `2 waves, 40 seats total` |
| 2 | seats-spec-not-dispatched | 0 | 0 | no `*.ready`, no `*.ready.dispatched`, no `*-results.json` anywhere; the plan file alone verifies the seats claim |
| 3 | window-placeholder-exempted-degenerately | 0 | 0 | a `<tip>` window atom is exempted by *any* window correction; `empty in <base>..<base>` is empty by construction |
| 4 | window-placeholder-honest-pair-rejected | 1 | 1 | the true window (`base..tip` over `tools/x`) is non-empty → the predicate prefers the vacuous correction to the honest one |
| 5 | rev-non-ancestor-exempted | 0 | 0 | `derive()` requires ancestry; `corrects()` for `rev` checks `rev-parse` only → the exemption is strictly weaker than the atom (`side_is_ancestor_of_tip: False`) |
| 6 | path-citation-outside-wave-dir-ignored | 0 | 0 | `WAVE_DIR` matches only `.ufo/waves/round-N/…`; three cited paths that do not exist are not atoms |
| 7 | log-and-report-claims-not-atoms | 0 | 0 | a sentence about `LOG.md`, a report's settlement and `*-results.json` adds no atom |
| 8 | corrections-can-be-exemption-free | 0 | 0 | A3's `historical` escape accepts `- corrects seats round-3: …` that exempts nothing; `CORR_MIN` then does not mean "two defects repaired" |
| 9 | doctored-dispatch-dropped-correction | 0 | 0 | commit an edited `w2-dispatch.json`, drop the correction → the false split is *verified* (the claims file's kill rule covers only the retained-correction case) |
| 10 | control-false-split-uncorrected | 1 | 1 | control: discrimination exists |
| 11 | control-honest-card-no-corrections | 1 | 1 | control: `corrections 0 < 2` |
| 12 | axes-correction-false-line-ignored | 0 | 0 | `- corrects axes coverage: 999/999` is silently ignored (§5) |
| 13 | axes-head-false-unrepairable | 1 | 1 | a false axis head cannot be repaired by the documented mechanism |

Case 0 also carries the depth-reader divergence: on the same `SKILL.md`,
`record.depth_pair → 1/1` and command A → 0/1 (`same_predicate: False`).

## 5. A frozen clause that cannot fire

`CORR = re.compile(r"^- corrects (seats|window|path|rev) (\S+):\s*(.+)$")` (`record.py:47`) omits
`axes`. Therefore:

- `corrects()`'s `axes` branch (`record.py:280-291`) is unreachable, and the duplicated block at
  `292-297` is dead code that references an undefined name `atom`.
- The frozen claim's clause 3 sentence "an `axes` correction must state `<resolved>/<total>`" and
  the landed-surface sentence "Each `- corrects <class> <key>: <statement>` line … is itself
  re-derived" are **false for the `axes` class**.
- At `09a9f912` the card carried **4** `- corrects` lines and the counter counted **2**
  (`receipts/c2-atom-census.json`: `counted 2 of 4`); the two ignored ones were the axes lines,
  which were then dropped at `6f9fd7f8` in favour of repairing the heads in place — so the card no
  longer depends on the dead clause (`receipts/tip/c2-atom-census.json`: `counted 2 of 2`). The
  hole itself remains: the next axes correction line anyone writes will be silently ignored.
- The consequence: since a false axis head cannot be exempted, the only repair is editing
  the head, and the counter then re-derives it with **its own** reader — see §6.

This is a frozen-document/frozen-code divergence. Do not edit frozen bytes to hide it; record it
(routed defect, or a disclosed amendment with red-before) and fix the regex in round 48.

## 6. The depth reader is not the observable the card names

The card's command A counts only `corpus/knowledge/(…)` refs (`SCORECARD.md:99-122`);
`record.depth_pair` uses `HARD_REF = ((?:corpus|plans|tools)/…)` (`record.py:44,221-243`). Same
label, different predicate (`fixtures/command-a.py` is command A verbatim):

| rev | command A | `record.depth_pair` | depth head in the card | counter |
|---|---|---|---|---|
| `13a9e9e1` (base) | 23/23 → 10.0 | 23 | 20/20 (mismatch) | red (correct) |
| `2e4ae434` (A3) | **23/24 → 9.58** (block 24 has 0 `corpus/knowledge` refs) | **24/24** | **24/24** | **green (false)** |
| `09a9f912` (live) | 24/24 → 10.0 | 24 | 24/24 | green (true) |

The A3 instance was repaired by the L1 at `04469ee8` ("block 24 cites a knowledge entry (proxy harm
repaired)") — verified: `receipts/command-a-2e4ae434.json` shows `unresolved_blocks [24]`,
`receipts/command-a-09a9f912.json` shows none, and
`receipts/command-a-repair-demo.json` shows one added `corpus/knowledge` citation with a line
selector moves the same predicate 23/24 → 24/24. **The class survives**: while the names differ,
the counter cannot fail a recurrence — it would certify whatever its wider reader prints.

## 7. What closes it (smallest safe corrections, ranked)

1. **`seats` truth = dispatch, not spec.** Count a wave only when `<wave>.ready.dispatched` exists
   at `--rev` (round 45 has both markers, round 46 has one); otherwise the atom is `could-not-
   evaluate`, not green. This retires §3 and part of R46-V1. Fixture case 2 is the counter-example.
2. **Add `axes` to `CORR`** (one-word regex fix) and delete the dead duplicate block
   (`record.py:292-297`). After that, a false axes head is repairable by exemption and the frozen
   clause 3 axes arm is real. Red-before is available: fixture case 12 is green today.
3. **Replace `depth_pair`'s `HARD_REF` with command A's pattern** so the axis atom is the observable
   it names. Without this, §6 recurs silently.
4. **Bind the counter's own ledger cell.** One new class `ledger`: every `atoms N` / `exempted N <= M`
   / `mismatches []` claim in a `| R47-C2 |`-shaped row must equal what the counter prints at the
   row's measured-at cell, and the cited `l1/scores/*.json` must contain those numbers. §2 then
   fails today (the tip row's `exempted 2` against the cited receipt's 1; 50/2 against 42/1 at
   `09a9f912`) and would have to be written honestly.
5. Make the battery test **exempting** forgeries, not just breaking ones: `A..A` window exemption of
   a `<tip>` atom (case 3/4 pair) and a non-ancestor `rev` exemption (case 5). Today all three
   forgeries break `corrects()` itself.
6. Pin `record.py`: either `--freeze` via `gate.freeze_state` like `exact.py`, or an
   `interpreter_sha256` field in the receipt. (§1: five amendments after the first freeze; A3–A5
   are not disclosed in the claims file, which was last amended at A2 `62e33f7d`.)

Frozen-byte edits are the wrong route for a claim whose freeze is already declared twice; route
1/2/3 as round-48 instrument defects, or make them a disclosed A-series amendment with red-before,
exactly as A1/A2 did.

## 8. Which routed record defects stay open

"Open" = the record still shows the defect and R47-C2 cannot fail it (probes in
`receipts/record-open-defects.json` at `09a9f912` and `receipts/tip/record-open-defects.json` at the
tip; every command and its exit is listed there).

| id | headline | C2 class that would see it | status at live rev | evidence |
|---|---|---|---|---|
| R46-V1 | seat count 40+40=80 vs 40 dispatched (HIGH) | `seats` — **present but inverted** | **OPEN** (SCORECARD half *certified true*; LOG half invisible) | §3; `LOG.md:3364-3366` still says "wave 2 = 40 seats … Round total 80 … per-seat output in `.ufo/waves/round-46/{w1,w2}-results.json`" and that file does not exist (`git cat-file -e` → 128) |
| R46-V2 | the `<tip>` empty-window sentence (HIGH) | `window` — present | **OPEN as a record claim**: the sentence stands verbatim; only annotated, and the annotation may be vacuous (fixture 3) | atom `window:46` = exempted |
| R46-V3 | before-cell measured at a different revision (MEDIUM) | none (`rev` checks resolvability, not "measured at") | **OPEN / out of class** | class census |
| R46-V4 | report settlement (32 of 40, 8 of 32 attack seats) (MEDIUM) | none — no class reads a report | **OPEN** | `record.py` reads only `SCORECARD.md`; `grep -c report record.py` = 0 |
| R46-V5 | lane dirty at closure, writing after the driver line (MEDIUM) | none — `git show` only, no worktree read | **OPEN and live** | `git status --porcelain` = 227 paths at the tip while the counter is green (`receipts/tip/record-open-defects.json`) |
| R46-V6 | stale self-test counts (LOW) | none | **OPEN and recurring** | `SKILL.md` registry row: "`record.py --selftest … : 9 cases`"; the code prints `cases=10 failures=0` (`receipts/record-selftest.txt`) |
| R46-V7 | four cited receipt paths absent (LOW) | `path` — present but **scope-limited** | **OPEN** | all four `git cat-file -e` → 128; `WAVE_DIR` covers only `.ufo/waves/…` (fixture 6) |

R46-CL5/CL7 (instrument classes) are out of this seat's scope; the round-47 card already routes
them.

## 9. Atom classes an honest self-assessment needs (and C2 lacks)

Each entry names the surface it would read and the defect it closes.

| proposed class | derives | from | closes |
|---|---|---|---|
| `ledger` | every `atoms/verified/exempted/mismatches/battery` figure in a round's claim row | the counter's own receipt at the row's measured-at cell | §2 (tip: `exempted 2` vs the receipt's 1) |
| `report` | a round report's settlement counts (seats reported, dead seats, attack seats) | `.ufo/waves/round-N/w*/` trees | V4 |
| `log` | each `## Round N` LOG entry's wave line, seat total and cited result paths | dispatch specs + `.ready.dispatched` + `*-results.json` | V1 (LOG half) |
| `province` | every `PROVINCE.md` row's cited `path:lines` | git show + line counts | drift between the province map and the repo |
| `registry` | every instrument row's `cases=N` and documented invocation | running the tool's `--selftest` / parsing its banner | V6 |
| `citation` | every `path:lines` token in the two round sections and the axis rows (not only `.ufo/waves/`) | git show + line counts | V7 |
| `cell` | each claim-ledger `measured at` revision and its before/after numbers | re-running the named counter at that revision | V3, §2 |
| `axes` (widened) | **all three** axis rows' heads, not just coverage/depth | command A / command B | the calibration row is currently unread |
| `worktree` | untracked/modified paths under the wave dirs at closure | `git status --porcelain` (a warn/2 class, not 0/1) | V5 |

Class *presence* is already enforced (`missing_classes`), so the cheapest hardening is a floor:
**at least one content atom per claim class that is not exempted** — today `window` would fail it
(1 atom, exempted) and `axes` would fail it (2 of 3 rows).

## 10. Per-clause verdict

| clause | holds? | note |
|---|---|---|
| 1 `mismatches == []` | holds at `09a9f912` and `2e4ae434` | but 89 % of the population is tokens; §3/§6 show greens on false claims |
| 2 `classes` cover all five | holds | hole: `window` is satisfied by one exempted atom; `axes` by 2 of 3 rows |
| 3 `corrections >= 2`, all re-derive | holds | satisfiable by exemption-free historical lines (case 8); the `axes` arm cannot fire (§5) |
| 4 `exempted <= 3` | holds (1 at live rev) | 3 exemptions = 60 % of the content atom budget |
| 5 `sections` = last two round headings | exact | but they are *historical*: at `2e4ae434` the counter measured rounds 45+46 and the round-47 landing had not landed; the window slid to 46+47 at `caafeffa` and the numbers changed with it (§2) |
| 6 battery `3 / 0` | holds | all three forgeries break `corrects()`; none tests an *exempting* forgery (§7.5) |

Kill rules in the claims file that I tested and that **hold**: the declared before-cell reproduces
(the counter at `13a9e9e1` exits 1 with exactly the four named mismatches —
`receipts/c2-at-base.json`); deleting the corrections section restores the mismatches (fixture 11);
a wrong seat total in a correction is caught (battery fixture 1); a non-empty window correction is
caught (battery fixture 2); a ghost `- corrects path` line inside the section is caught (battery
fixture 3).

## 11. Limits of this review

- Nothing was edited, staged, committed, or landed. `tools/round-47/` and
  `plans/round-47-claims.md` were read only; all mutations ran on copies in `$TMPDIR`.
- I did **not** run `tools/round-47/exact.py` (R47-C1 is another seat): the freeze/Pin statements
  about `record.py` are read from its source (`exact.py:399-421`) and from byte comparisons, not
  from a C1 receipt.
- Fixture cases call `record.evaluate_text` with a git-backed `files()`; the CLI battery was run
  once at the live rev, not in every fixture.
- The worktree is dirty and grew from 115 to 227 porcelain paths during the session; every figure
  is at a committed revision (the tip measured here is `b1a058f3`; the lane was still committing
  when I finished, so treat `b1a058f3` as the last revision I saw, not the last one that exists).
- Tooling: nothing installed; no pacman transaction; `python3` from the host.

## 12. Receipts

`receipts/index.md` lists every file with its exact command, exit code, file sha256 and UTC time.
`receipts/` holds the `09a9f912`-and-earlier measurements; `receipts/tip/` holds the `b1a058f3`
re-measurement. Three drivers are citable and re-runnable:

```sh
# 14-case fixture battery over the exemption machinery (exit 0 = every case reproduced)
python3 -I -B .ufo/waves/round-47/w1/CritC2Calibration/fixtures/c2-attack.py --lane <lane>

# command A, verbatim from SCORECARD's recipe, at a revision (and --repair-demo)
python3 -I -B .ufo/waves/round-47/w1/CritC2Calibration/fixtures/command-a.py <rev>

# census, timeline, ledger-vs-receipt, open-defect and pinning receipts
python3 -I -B .ufo/waves/round-47/w1/CritC2Calibration/fixtures/probes.py \
  --lane <lane> --rev <rev> --out-dir <dir>
```
