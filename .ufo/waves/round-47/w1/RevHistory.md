# RevHistory — round 47, wave 1: why the round-46 record claimed 40 + 40 seats and an empty window

Seat: `RevHistory` (revenger). Lane `kaidoku-shokunin`, round 47, wave 1.
Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Frozen surface cited: `plans/round-47-claims.md` + `tools/round-47/` at
`5017e1f7299c3a812e87e7950148f54313dd279e` (A1 `9018c53b`, A2 `62e33f7d`, A3 `2e4ae43`,
A4 `1e2c310295` are the disclosed series; nothing frozen was edited by this seat).
Lane tip moved under the wave while I measured (`a631bba0` → `f54b3b6d` → `f7d6e58d`); every
number below is pinned to the revision printed next to it.

---

## 1. Verdict

The two round-46 record atoms failed for **different reasons at different times**, and only one of
them is a freeze case:

| atom as written at `deee6595` | true when written? | when it changed |
|---|---|---|
| `Waves: 40 + 40 = 80 seats` | **no — false at the moment it was written** | became *documentarily* true at `22fd0d6b`, when the never-dispatched wave-2 **plan file** entered the tree; no seat ever spawned |
| `git log --name-status 0425224..<tip> -- tools/round-46 plans/round-46-claims.md` "is empty at every measurement above" | **yes** — at every concrete tip then available the range prints 0 lines; at the only measurement cited it was *degenerate* (`0425224..0425224`) | became **false** at `332f4884` (F5), which edits `tools/round-46/attest.py` and `tools/round-46/gate.py`; the same section's own append `c8de6c47` then added measurements at `332f4884` and `58eb04b6`, so the sentence contradicts its own section |

So the seat claim needs a *falsification*, not a correction-by-substitution; the window claim needs
a correction that keeps the falsifying commit visible. The frozen round-47 correction section does
the opposite for both: it repairs the round-**45** seat atom (the one that is merely miscounted) and
replaces the round-46 window with a span that *starts at the commit that broke it*, while the
round-46 seat atom — `R46-V1`, the HIGH routed defect this round exists to repair — is left in the
card and scored **green** by the counter.

---

## 2. Timeline reconstructed from committed state

| UTC−03 | event | evidence |
|---|---|---|
| 13:48 | `w1-dispatch.json` written, `counts.spawn 40` | file; `python3 -c json → {'spawn': 40, 'resume': 0, 'total': 40}` |
| 13:49:16 | `w1.ready` written | `stat` (manifest row) |
| 14:02 | `w2-dispatch.json` (40) + `w2/swarm-registry.json` (40 × `kind=spawn`, **all `agentId: null`**) written — untracked | `stat`; registry dump |
| 14:02:13 | `w1.ready.dispatched` written (the wave-1 hand-off; 14 of the 40 names carry a retry suffix `-2/-3/-4`) | `stat` |
| — | **no `w2.ready` is ever created** | `git log --all --diff-filter=A -- '.ufo/waves/round-46/*ready*'` → only `w1.ready`, `w1.ready.dispatched` |
| 14:04:38 | `deee6595` — LOG round-46 entry + SCORECARD `## Round 46` written: "wave 1 = 40 seats … wave 2 = 40 seats … Round total 80, inside the 64–128 band; per-seat output in `.ufo/waves/round-46/{w1,w2}-results.json`" and "Waves: 40 + 40 = 80 seats." | `git log -S` for both phrases → first appearance `deee6595` |
| 14:09:34 | `332f4884` (F5) modifies `tools/round-46/attest.py`, `tools/round-46/gate.py` | `git show --name-status 332f4884` |
| 14:10:30 | `c8de6c47` appends the F5/A4/B1 amendment, adding measurements at `332f4884` and `58eb04b6`; the empty-window sentence is not revisited | `git log -- SCORECARD.md` |
| 14:11:20 | `22fd0d6b` — "… **the wave-2 spec left undispatched** …" — adds `w2-dispatch.json`, `w2-spec.json`, `w2/swarm-registry.json`; the only file ever committed under `w2/` is the registry | `git log --diff-filter=A`; `git ls-tree -r <rev> .ufo/waves/round-46/w2` |
| 14:41 | `r46-w1-results.json` written — `seats 40`, 40 results — and **never committed** (`git ls-files --error-unmatch` → 1) | manifest row `git-ls-files exit 1` |

`w2/swarm-registry.json`: `members 40`, `kinds {'spawn': 40}`, non-null `agentId` **0**.
Wave 1 really ran: 40 dispatched seats, 40 results, 38 of 40 base seat names carry a committed
artefact at `f7d6e58d` (2 have none: `R46W1MutGate`, `R46W1SentTools` — settlement, not counts;
the spot-check's V4 settlement numbers are not re-litigated here).

---

## 3. The seats atom: false when written, made green by committing the plan

The counter's seat derivation reads **the plan**, not the dispatch:

```python
# tools/round-47/record.py:65-82
path = f".ufo/waves/round-{rnd}/w{i}-dispatch.json"
spawns.append(int(payload["counts"]["spawn"]))
```

`.ready`, `.ready.dispatched`, the registry's `agentId`, and any `*-results.json` are never read.

**The counter's own instrument says the claim was false at the writing revision.**
Run at `deee6595` (the commit that authored the sentence):

```
$ python3 -I -B tools/round-47/record.py --root <lane> --rev deee6595 --json-out ... \
    --no-battery
exit 1   atoms 47   mismatches 5
  MISMATCH seats 46 | "Waves: 40 + 40 = 80 seats"
    derived {"claimed": [40,40,80], "derived": [40,0,40], "dispatch": [40]}
```

(`receipts/c2-at-deee6595.json`, stdout sha256 `25247e200e017e93…`.)
The next commits, `22fd0d6b` (14:11:20, "… the wave-2 spec left undispatched …") and
`c0112995` (14:12:10, "the seats' late evidence files"), derive `[40,40,80]` for the same atom and
it is scored `verified` (`receipts/c2-at-c0112995.json`, exit 1 but **without** `seats:46`; the four
remaining mismatches are `seats:45`, `window:46`, `axes:coverage`, `axes:depth`). The truth value
changed because a JSON file was `git add`ed — not because a wave ran. At the base `13a9e9e1` the
atom is already green (50 atoms, 4 mismatches, `seats:46` absent), which is why R47-C2's before-cell
never names it.

**Consequence for the frozen claim.** `battery.correction_forgeries == 3`,
`forgeries_green == 0`, `mismatches == []` are all met at `a631bba0` and `f7d6e58d`
(`receipts/c2-at-{a631bba0,f7d6e58d}.json`, exit 0, `exempted` 1 = the round-46 window atom) while
the card still asserts `40 + 40 = 80` at a truth of 1 dispatched wave of 40. The instrument cannot
catch `R46-V1`, and it forbids the truth — see §5.

---

## 4. The window atom: true when written (degenerately), false from F5

`0425224..<tip> -- tools/round-46 plans/round-46-claims.md`, measured over every tip the sentence
then had:

```
0425224..0425224   0 lines      (the only measurement cited, and it is base==tip)
0425224..227d6982  0 lines
0425224..87578656  0 lines
0425224..6e018068  0 lines
0425224..7bf33e31  0 lines
0425224..781e19ae  0 lines
0425224..1e32827b  0 lines
0425224..332f4884  2 lines  ← F5: M tools/round-46/attest.py, M tools/round-46/gate.py
0425224..58eb04b6  2 lines
332f4884..58eb04b6 0 lines  ← the frozen correction's span
```

(`receipts/manifest.json`, `kind: git-log-window`, one row per span; empty spans hash to the empty
stdout sha256 `e3b0c44298fc1c14…`.)

So: **true when written** (the only cited measurement was degenerate, so the claim was vacuous from
birth), and **false from `332f4884`** — the very commit the same section appends as its measured
freeze. The declared correction `empty in 332f4884..58eb04b6` is literally true and semantically
misleading: it substitutes the sentence's concrete base (`0425224`) with the commit that falsified
it, and its rationale — "named a `<tip>` placeholder no command can resolve" — names the wrong
defect. The base *was* resolvable; the claim was falsified by a commit, not by a placeholder.

Why the counter allows the substitution: `WINDOW = ([0-9a-f]{7,40})\.\.([0-9a-f]{7,40})` needs both
sides hex, so `0425224..<tip>` has `pair None`; `derive()` returns `unverifiable`, and `exempt()`
then returns `True` for *any* window correction whatever it states
(`tools/round-47/record.py:206-217, 330-338`). The base half of the claim is discarded exactly where
it carries the evidence.

---

## 5. Falsifications of the frozen R47-C2 clauses

Fixture: `D=/fast/scratch/hyaku/kaidoku-r47/RevHistory/fix-clone`, a local `--no-hardlinks` clone of
the lane asserted with `git -C "$D" rev-parse --show-toplevel` == `$D`; checked out to `a631bba0`
(A5); one commit per attack with `git -C "$D" -c user.name=revhist@fixture -c user.email=revhist@fixture commit`;
the counter invoked with `--root "$D"`. Driver kept as `attack-fixture.py`; per-step receipts in
`receipts/fixture/`; run log `receipts/fixture/attack-run.json`.

| # | mutation of the landed corrections/card | clause it should trip | expected under a counter that binds the dispatch | measured | rev | stdout sha256 |
|---|---|---|---|---|---|---|
| 0 | none (control at A5) | — | 0 | **0** | `a631bba016` | `538dbb87d88b…` |
| A | window correction → `empty in 58eb04b6..58eb04b6` (degenerate) | Cl.3 "reproduces as empty" / Cl.4 exemption | 1 | **0** — accepted, atom exempted | `5dbabef88a` | `65d28da5f88b…` |
| B | window correction → `empty in 0425224..58eb04b6` (**the sentence's real span**) | Cl.3 | 1 (non-empty) | **1**, `{"empty": false}` | `c5d99114d5` | `7249ec0792a2…` |
| F | window → `empty in 58eb04b6..58eb04b6 -- does/not/exist` | Cl.3 pathspec | 1 | **0** — a path that never existed | `8ec68a0437` | `89debe091ef2…` |
| C | `- corrects seats round-46: 1 wave, 40 seats total` (**the truth**, R46-V1) | Cl.3 | 0 | **1**, `claimed [1,40] derived [2,80]` | `5f0db01e5a` | `648125de30e2…` |
| D | `- corrects seats round-46: 2 waves, 80 seats total` (**the false plan**) | Cl.3 | 1 | **0** | `1980eab275` | `f785b238c66b…` |
| I | seat sentence re-written truthfully as `Wave 1: 40 seats; wave 2: 0 seats (…)` | Cl.1 | 0 | **1**, 1 mismatch (`seats:46`) | `b5619175b0` | `1525dac670f9…` |
| J | seat sentence replaced by truthful prose that matches neither seat regex | Cl.1 | 0 | **1**, `no atoms of class(es) ['seats']` | `3ba5eeddec` | `00e4c58934d8…` |
| G | `- corrects axes coverage: 137/138` | Cl.3 "every correction line re-derives" | 1 | **0** | `2a44f3b0f3` | `a30db3e12834…` |
| H | `- corrects axes depth: 23/24` | Cl.3 | 1 | **0** | `488c77bc2b` | `4a57bc29e7da…` |

Read together (C, D, I, J): **no green truthful repair of the round-46 seat atom exists.** The
truthful correction is red; the truthful sentence is a mismatch; deleting the sentence removes the
`seats` class and trips clause 2; the only green statement is the false one. The only green *and*
honest construction is to leave the false sentence in place and state the falsification in prose
that matches neither `Waves?: a + b = c seats` nor `Wave 1: a seats; wave 2: b seats`.

G/H are a second, independent defect: `CORR = ^- corrects (seats|window|path|rev) (\S+):` has no
`axes` alternative, so the `axes` branch of `corrects()` is unreachable. The landed section has four
`- corrects` lines and the counter parses **two** (`corrections 2` at `a631bba0` and `f7d6e58d`);
the two `axes` corrections are neither re-derived nor counted, so clause 3's "every correction line
itself re-derives" holds vacuously for half the section.

A/F: `window_empty` never checks the pathspec exists and never rejects `base == tip`, so the
exemption can be discharged by a window that cannot bear on the atom at all.

### 5b. The single seats atom the counter scores at the landing is the false one

`sections()` takes the **last two** `## Round N` headings. While the round-47 section did not yet
exist, the window was `[round-45, round-46]`; the moment the round-47 section was appended it became
`[round-46, round-47]` and the round-45 seat atom scrolled out. Measured:

| rev | what it is | sections | atoms | exempted | exit |
|---|---|---|---|---|---|
| `1e2c310295` | A4 freeze | `[45,46]` | 50 | `seats:45`, `window:46` | 0 |
| `e856beb5` | the landing (block 24 + corrections) | `[45,46]` | 50 | `seats:45`, `window:46` | 0 |
| `caafeffa` | the round-47 section lands | `[46,47]` | 41 | `window:46` | 0 |
| `f7d6e58d` | tip while measuring | `[46,47]` | 44 | `window:46` | 0 |

(`receipts/c2-at-{1e2c310295,e856beb5,caafeffa}.json`.) Two consequences:

1. The card's after-cell (`atoms 50`, `exempted 2 <= 3`) reproduces **only at revisions that do not
   contain the round-47 section the cell itself lives in**. Every re-measure at a revision carrying
   the record reads 41–44 atoms and one exemption.
2. From `caafeffa` on, the counter's **only** `seats` atom is the round-46 `40 + 40 = 80` sentence,
   and it is scored `verified`. The round-45 seat correction — the one correction the card calls
   repaired — is now historical: its atom is out of scope at every landing-bearing revision, so it
   is never exercised there, and the worse of the two seat atoms is the only one measured.

---

## 6. What the correction should say — and the constraint on how

**Seats.** Do **not** append `- corrects seats round-46: …`: any truthful value is red (C) and the
frozen bytes forbid changing the instrument. The record must carry the falsification as prose that
the two seat regexes cannot parse, in both places:

- `LOG.md` round-46 entry (the routed `R46-V1` asked for this and it is still owed; C2 never reads
  `LOG.md`, so this is free of counter risk):
  > Wave 2 was planned at 40 seats and **never dispatched**: `w2/swarm-registry.json` carries 40
  > `spawn` members with `agentId: null`, no `w2.ready` ever existed, and the only file ever
  > committed under `w2/` is the registry (`22fd0d6b`, "the wave-2 spec left undispatched"). The
  > round ran one dispatched wave of 40. `r46-w1-results.json` (40 results) is untracked;
  > `r46-w2-results.json` does not exist.
- `SCORECARD.md`: same statement, phrased *outside* the two seat shapes, next to (not replacing)
  the existing sentence — replacing it trips clause 2 (J).

**Window.** The correction's span (`332f4884..58eb04b6`) is the right empty span, but a correction
that stops there lets the card read as though the frozen set was never touched. The honest form
states the breach and then the residual span, e.g.

> corrects window round-46: the sentence `0425224..<tip> -- tools/round-46
> plans/round-46-claims.md` "is empty at every measurement above" was true only of the degenerate
> measurement it cites (`0425224..0425224`); it is false from `332f4884`, which modifies
> `tools/round-46/attest.py` and `tools/round-46/gate.py` (`0425224..58eb04b6` = 2 lines). The
> empty span is `332f4884..58eb04b6`; `empty in 332f4884..58eb04b6 -- tools/round-46
> plans/round-46-claims.md`.

Caveat the L1 must weigh: the frozen clause only checks that the stated span is empty, so this
prose passes, but so does the degenerate form (A) and the bogus-pathspec form (F). The clause cannot
distinguish an honest correction from a vacuous one; that gap is round-48 material, not a reason to
weaken the correction.

**Round-48 rows this reconstruction implies (all against `tools/round-47/record.py`).**
1. `dispatch_counts` must prefer the dispatch *receipt* (`.ready.dispatched` / registry `agentId` /
   `*-results.json`) over `counts.spawn`; a plan file is not a dispatch.
2. `CORR` needs `axes` in its alternation, or clause 3 is unenforced for axes lines.
3. `window_empty` must reject `base == tip` and refuse a pathspec that does not exist at `--rev`.
4. `exempt()` for a window atom must bind a concrete base when the atom supplies one
   (`0425224..<tip>` names `0425224`), otherwise the load-bearing half of the claim is discarded.
5. The card's own after-cell figures are re-derived by no clause: `atoms 50` / `exempted 2`
   reproduce only at `e856beb5` (§5b); every revision that carries the round-47 section reads
   41–44 atoms and one exemption, so the row's numbers stop reproducing at the tip it is filed at.

---

## 7. Scope and limits

- Not run by this seat: `tools/round-47/exact.py` and the C1 surface (other seats own it); the
  three selftest suites; `--profile v2` ports.
- The counter was run with `--no-battery` for every measurement above (the battery's own fixtures
  need a second repo and are covered by siblings). The one-commit-per-attack fixtures I ran are
  in `receipts/fixture/` and are reproducible from `attack-fixture.py`.
- No install, upgrade or tool change was made. All git actions were read-only in the lane; the only
  commits in this session were made inside the scratch clone, with `-C "$D"` and an explicit
  `-c user.name/-c user.email`, after asserting the clone's toplevel.
- Nothing under the lane was edited except this report directory.

## 8. Receipts

`receipts/manifest.json` — every command, `cwd`, exit, stdout sha256, UTC, and the sha256 of each
JSON receipt (24 rows). Lane counter receipts: `c2-at-13a9e9e1.json` (exit 1, 50 atoms, 4
mismatches), `c2-at-deee6595.json` (exit 1, 47 atoms, 5 mismatches, `seats:46`),
`c2-at-c0112995.json` (exit 1, 50 atoms, `seats:46` gone), `c2-at-a631bba0.json` (exit 0, 42 atoms,
exempted 1), `c2-at-f7d6e58d.json` (exit 0, 44 atoms, exempted 1), `c2-at-1e2c310295.json`,
`c2-at-e856beb5.json` (exit 0, 50 atoms, exempted 2, sections `[45,46]`),
`c2-at-caafeffa.json` (exit 0, 41 atoms, exempted 1, sections `[46,47]`). Fixture:
`receipts/fixture/*.json`, `receipts/fixture/attack-run.json`, driver `attack-fixture.py`.
