# RevC2Axes — the axes class: are the two head fractions the current claim, and can a forger keep them green?

Seat `RevC2Axes`, round 47 wave 1. Scope: the `axes` atom class of R47-C2 —
`tools/round-47/record.py`'s derivation of the leading `<resolved>/<total>` of the
`coverage` and `depth` rows of the current `## Owned axes` table.

Read-only on the lane tree; every fixture is its own `git clone --shared` of the lane
with plumbing commits, under `/fast/scratch/hyaku/kaidoku-r47/RevC2Axes/fx-*`.
Scratch is removed at yield; the fixture diffs, receipts and drivers are copied to
`.ufo/waves/round-47/w1/RevC2Axes/receipts/`.

## 0. The measurement, pinned

The lane moved under this review: `HEAD` was `3186f69b` at first read, the L1 landed
`e856beb5 → 07d2894e → a631bba0 → 04469ee8 → f54b3b6d → a0753786 → 31b092d1 → f7d6e58d
→ 09a9f912` (15 commits since the freeze) while I was measuring. Every number below names
its revision. At the last revision I observed, `09a9f912f4a639b91bce7dcd3711d8f391969d4f`:
HEAD's `record.py` → exit 0; the frozen `record.py` → exit 1 (`sections [round-46, round-47]`,
44 atoms, `corrections_bad ["exempts an atom that does not exist", "window pair names no atom
in scope"]`); command A → `24/24`; `exact.py --freeze 5017e1f` → exit 2; and all four
F2/F3/F4 fixtures still green on those bytes.

| # | bytes | rev | command | exit | result |
|---|---|---|---|---|---|
| M1 | frozen `record.py` sha256 `af666ce2…` (`5017e1f:tools/round-47/record.py`) | `5017e1f7299c3a812e87e7950148f54313dd279e` | `python3 -I -B tools/round-47/record.py --root $PWD --rev 5017e1f… --json-out …` | 1 | 50 atoms; 4 mismatches — seats r45 `40+32` vs dispatched `40+36`; window r46 unverifiable; **coverage `133/133` vs derived `138/138`**; **depth `20/20` vs derived `23/23`**. Battery `forgeries_green 0` (all three "no corrections section"). This reproduces the claims file's before-cell exactly. Receipt: `receipts/r47-freeze-record.json`. |
| M2 | frozen `record.py` | `1e2c3102952dc636650095643c1963c833859019` (the freeze A1/A2 declares) | same | 1 | `corrections_bad: ["window pair names no atom in scope"]`. **The frozen bytes cannot score the landing's own corrections section.** `receipts/c2-frozen-bytes-1e2c3102.json` |
| M3 | frozen `record.py` | `a631bba01633d2b5353306a569be4ce2e683d364` (A5) | same | 1 | sections `[round-46, round-47]`, 42 atoms, `corrections_bad` **2**: `window pair names no atom in scope`, and `- corrects seats round-45 …` → `exempts an atom that does not exist`. `receipts/c2-frozen-bytes-a631bba0.json` |
| M4 | frozen `record.py` | `f7d6e58d6e7f4e664bf443137c55ee08821de244` (final HEAD I saw) | same | 1 | same two `corrections_bad`, 44 atoms. `receipts/c2-frozenbytes-final.json` |
| M5 | **HEAD's own** `record.py` (sha256 `abf35257…` at a631bba0; re-read at f7d6e58d) | `f7d6e58d…` | same | **0** | `met_target true`, 44 atoms, `axes 2`, `mismatches []`. `receipts/c2-headbytes-final.json` |
| M6 | command A, lifted verbatim from `SCORECARD.md` `## Measurement recipes` recipe A (`receipts/recipeA.py`) | `a631bba0` | `python3 receipts/recipeA.py a631bba0` | 0 | `rule_blocks 24, citation_resolved_rules 23, depth_score 9.58` — **23/24** |
| M7 | command A | `f7d6e58d…` | same | 0 | `rule_blocks 24, citation_resolved_rules 24, depth_score 10.0` — 24/24 *after* `04469ee8` added a knowledge citation to block 24 |
| M8 | `tools/round-47/exact.py` (C1's counter, context only) | `f7d6e58d…` | `… --freeze F --rev f7d6e58d…` | **2** for F ∈ {`5017e1f`, `e856beb5`, `62e33f7d`, `2e4ae434`, `1e2c3102`}; 0 only for F = the rev itself | `reason: frozen_path_changed`. `receipts/c1-final-*.json` |

Structural facts measured on the way:
`git diff --stat 5017e1f..f7d6e58d -- plans/round-47-claims.md` → `21 insertions(+)`, no
deletion: **the frozen predicate text never changed**, only two disclosure paragraphs were
added. Six commits touched a frozen path after the freeze
(`git log 5017e1f..f7d6e58d --name-only -- tools/round-47/ plans/round-47-claims.md`):
`record.py` at `9018c53b` (A1), `62e33f7d` (A2), `2e4ae434` (A3), `1e2c3102` (A4),
`07d2894e` (A5); the claims file at `9018c53b` and `62e33f7d`; `exact.py` at `f54b3b6d` (A6).
`tools/round-46/gate.py` is byte-identical across the round (diff empty). The block-24
content repair `04469ee8` touched no frozen path.
The axes code itself (`collect_axes`, `coverage_pair`, `depth_pair`, `axis_pairs`, `FRAC`,
`AXIS_ROW`) is **unchanged between `5017e1f` and `f7d6e58d`** — the diff has no hunk in
those symbols — so every finding below applies to the bytes that certify the landing.

---

## F1 — HIGH — the depth fraction is not command A's count, and the counter cannot see the difference

The claims file's class table says the `depth` fraction derives from *"command A's
citation-resolution count over `## Queue-drain craft `"*. `record.py`'s `depth_pair`
docstring says *"exactly as command A reads them"*. Both are false.

`depth_pair` uses `HARD_REF = ((?:corpus|plans|tools)/[A-Za-z0-9._/-]+)(?::(\d+)(?:-(\d+))?)?`
— **any** `corpus|plans|tools` path, with the line selector optional. Command A's pattern
is `corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?` — **only a `corpus/knowledge/`
entry counts**.

Fixture: `fx-depth-divergence-azh8szki` (recreate with `R47_COUNTER=…/record.py python3
case2.py`, case `depth-derivation-diverges-from-command-A`; diff `receipts/fx-depth-derivation-diverges-from-command-A.diff`).
A 24th craft block citing `corpus/lessons/round-46.md:27-31` and `tools/round-47/exact.py`
and nothing under `corpus/knowledge/`:

```sh
python3 -I -B tools/round-47/record.py --root $FX --rev $REV --json-out $FX/r.json   # exit 0, depth atom green (24/24)
python3 receipts/recipeA.py $REV                                                     # exit 0, citation_resolved_rules 23, rule_blocks 24, depth_score 9.58
```

The same card with the row telling command A's number (`23/24`) → **exit 1**,
`mismatches [['axes','depth']]`. The counter rewards a row that contradicts its own cited
command and punishes one that quotes it.

**This was live in the landed card, not hypothetical.** At `a631bba0` block 24 carried no
`corpus/knowledge/` reference — `receipts/depth-by-block-A4.json` shows **block 24 is the
only block with no knowledge reference** (`record_py_depth_pair: [24,24]`) — while the
landed row read `24/24 queue-drain rule blocks … (command A, new block 24 …, citation_resolved_rules 24; …)`.
Command A at the same revision: M6 above, **23/24**. A wave-1 peer agrees:
`.ufo/waves/round-47/w1/ScribeShonen/receipts/commandA-at-A4.json` records the identical
`citation_resolved_rules 23, rule_blocks 24, depth_score 9.58`.
`04469ee8` repaired the *content* (M7 now reads 24/24 honestly); the *mechanism* is
unrepaired — `depth_pair` still measures a strict superset of command A, so the next block
that cites only a lesson or a tool re-opens the same false green.

**What the claim would have to say.** Either (a) the `axes` derivation is command A's
`citation_resolved_rules / rule_blocks` computed with command A's own pattern — and then
`depth_pair` must implement it; or (b) the axis is explicitly *record.py's* citation-count,
and the row must stop attributing it to command A. Today the row names command A, the code
measures something else, and the counter certifies the row.

## F2 — HIGH — the axes class has no cardinality: delete, rename or reflow one row and its atom vanishes silently

`collect_axes` only emits an atom when `AXIS_ROW = ^\|\s*(coverage|depth)\s*\|` matches **and**
`FRAC` finds a fraction on that physical line. Nothing requires both rows to exist; clause 2
(`classes` covers all five) is satisfied by whichever row survives.

| fixture | mutation | exit | `atoms_by_class.axes` |
|---|---|---|---|
| `fx-drop-depth-*` | `depth` row deleted from `## Owned axes` | **0** | **1** |
| `fx-rename-depth-*` | axis cell renamed `depth (craft)` | **0** | **1** |
| `fx-reflow-depth-*` | row split so the fraction sits on a continuation line | **0** | **1** |
| `fx-drop-coverage-*` | `coverage` row deleted | **0** | **1** |

```sh
R47_COUNTER=/fast/scratch/…/tools/round-47/record.py python3 case1.py   # depth-row-deleted: exit 0
R47_COUNTER=…/record.head.py python3 case5.py                            # h-depth-row-deleted: exit 0 (HEAD bytes)
```

Diffs: `receipts/fx-depth-row-deleted.diff`, `-renamed`, `-reflowed`, `fx-coverage-row-deleted.diff`.
Reproduced on the freeze bytes and on HEAD's bytes. This is R46-CL3's shape ("a row can claim
an id it does not address") still alive inside the class C2 uses to certify itself: one of the
two observables can be entirely absent and the counter prints `failing: []`.

**What the claim would have to say.** `axes_rows == 2`, one `coverage` and one `depth`, each
matching exactly once — a cardinality clause, exactly as C1 has `rows == 4`.

## F3 — HIGH — the fraction is the first `\d+/\d+` anywhere in the row, not the row's headline

`FRAC.search` runs over everything after the axis cell — including the score cell. The atom's
own label says "at the head of its Owned-axes row", which the code does not implement.

* **False green.** `| depth | 10 → 10 (23/23) | 20/20 queue-drain … |` → **exit 0**
  (`fx-preceded-truth`, `receipts/fx-false-headline-after-truthful-fraction.diff`): the row's
  headline metric says the stale `20/20`, the parenthetical earlier in the row says `23/23`,
  and the atom binds the parenthetical. A forger needs only to put the true number somewhere
  to the left of the false one.
* **False red.** An honest row that states its history in the score cell —
  `| coverage | 9.72 → 10.0 (133/133 → 138/138) | 138/138 … |` — → **exit 1**,
  `mismatches [['axes','coverage']]` (`fx-honest-history`, `receipts/fx-honest-history-in-score-cell.diff`).
  A landing that writes the before/after pair in the score cell is failed for being honest.

The landed rows currently lead with the current figure (`138/138 … at the round-47 landing`,
`24/24 … at the round-47 landing`) — the convention holds by authorial discipline, not by
clause. Nothing distinguishes a *current* claim from a *labelled historical* one; order is the
only signal, and order is what the counter mis-reads.

**What the claim would have to say.** "the fraction the observable cell *begins* with" — i.e.
parse the cell by `^\s*(\d+)/(\d+)` after the score cell is split off — and state that a
fraction before it is not a claim.

## F4 — HIGH — coverage maps are a token scan, so a stale map with a matching file count is green

`coverage_pair` = `len(stems ∩ tokens_in_##_Coverage_map) / len(stems)`, where `tokens` is any
`2026-10-\d{2}-[a-z0-9-]+` appearing anywhere in that section. A dangling entry is simply not
in `stems`, so it cannot lower the numerator — and nothing counts `dangling` at all.

Fixture `fx-stale-map-*`: one knowledge entry renamed (old file deleted, a new one added with a
new stem), the map keeps the old stem and gains the new one — **file count unchanged, map stale**:

```sh
python3 -I -B tools/round-47/record.py --root $FX --rev $REV --json-out $FX/r.json   # exit 0, coverage 138/138
python3 receipts/recipeA.py $REV   # mapped 138, knowledge_files 138, missing [], dangling ["2026-10-26-binwalk-v3-unit-of-work"]
```

Exit 0 with `axes` at 2 while command A reports a dangling map entry — and the landed row
literally reads `… command A `mapped 138`, `missing []`, `dangling []` …`. The counter certifies
a sentence it cannot check. `receipts/fx-coverage-stale-map-same-file-count.diff`;
control `fx-unmapped` (a file with no map token) correctly reds, so only the *dangling* half is
blind. Same on HEAD's bytes (`case5.py`, `h-coverage-stale-map`: exit 0).

**What the claim would have to say.** the atom is `(mapped, files, dangling)` with
`dangling == []` required, or the row drops `dangling []` from its own text.

## F5 — MEDIUM — the denominators are unpinned: R46-CL4's defect reproduced inside the class that claims to fix it

R46-CL4 is "the mutation list has no digest, so deleting a mutation changes the denominator
that the claim is judged on without failing a clause". The axes fractions are pure ratios; no
clause pins either total.

* `fx-shrink-depth`: delete the last craft block, set the row to `22/22` → **exit 0**
  (command A agrees: `rule_blocks 22, citation_resolved_rules 22`). Control: same card with the
  row still `23/23` → exit 1.
* `fx-shrink-coverage`: delete one knowledge file **and** its map token, set the row to
  `137/137` → **exit 0** (`mapped 137, knowledge_files 137, missing [], dangling []`).

`receipts/fx-depth-denominator-shrunk.diff`, `fx-coverage-denominator-shrunk.diff`. `24/24` and
`138/138` are not anchored to "24 rule blocks" or "the corpus": shrink the denominator and the
fraction survives. A perfect `N/N` is therefore not evidence that nothing was dropped.

**What the claim would have to say.** the depth atom names the block count it expects
(`rule_blocks == 24`, the round's own new-block number) and the coverage atom names the
file count (`knowledge_files == 138`), i.e. the numerator *and* the denominator are claims,
not a ratio.

## F6 — MEDIUM — an `axes` correction cannot be written; the class is dead code

`CORR = ^- corrects (seats|window|path|rev) (\S+):` **excludes `axes`**, while `corrects()`
carries an `axes` branch and `CORR_AXES` exists. So the claim's clause 3 sentence — *"an
`axes` correction must state `<resolved>/<total>`"* — is unreachable, and a repair line
`- corrects axes coverage: 138/138` is silently ignored (not counted, not rejected).

Fixture `fx-axes-corr-*` (case `axes-correction-unparseable`): card with `depth` repaired in
place, the stale `coverage` `133/133` left, both real corrections plus
`- corrects axes coverage: 138/138` → **exit 1**, `corrections 2`, `mismatches [['axes','coverage']]`.
`receipts/fx-axes-correction-unparseable.diff`. Consequence for the L1: an axes atom can only
be repaired by rewriting the row, never by the correction mechanism the claims file documents;
and a bogus `axes` correction line in the card is invisible.

**What the claim would have to say.** `(seats|window|path|rev|axes)` in the correction
grammar, or clause 3 must not describe an axes correction at all.

## F7 — HIGH (window class; it decides whether the landing's own verdict is legal) — clause 3 is falsified by the act of landing, and only the code was amended

Two frozen-bytes facts (M2, M3/M4):

1. At the declared freeze the landing's window correction is rejected:
   `window pair names no atom in scope`, because the only window atom in scope is the `<tip>`
   placeholder with `pair is None`, so `known_pairs` holds no window pair — while the *claim*
   says a window correction may name "a window the counter itself reproduces as empty" and
   clause 4 allows a pairless atom to be exempted. The frozen bytes contradict the frozen
   prose. (The L1's A1 deletes the code clause; the prose is unchanged, +21/–0.)
2. Landing a `## Round 47` section slides `sections()` to `[round-46, round-47]`, so
   `- corrects seats round-45: 2 waves, 76 seats total` becomes `exempts an atom that does not
   exist` — clause 3 verbatim: *"A correction that exempts an atom the card does not contain is
   itself a defect."* The card the L1 landed contains exactly that line, and the round-45 seat
   atom it corrects is the very defect the claims file's before-cell names. **The act of adding
   the round's own record section makes the frozen clause unsatisfiable.** A3 patched the code
   (`historical = class in (seats, window) and int(key) < oldest`); the predicate text was never
   touched, so the green verdict is produced by bytes the claim's own predicate forbids.

Side effect the L1 should exploit: the before-state (`mismatches 4`, 50 atoms, sections
45/46) and the landing state (44 atoms, sections 46/47) are not comparable by count. The
before/after table must be read per atom, not by mismatch total.

**What the claim would have to say.** clause 3 = "a correction that exempts an atom no
section in scope contains is a defect **unless the card's own records section is the round
that removes it from scope**", and the before/after comparison pinned to a fixed section pair
(e.g. `--sections round-46,round-47` at both ends).

## F8 — MEDIUM — a window repair is satisfiable by a tautology, and the battery turns one into a false red

`window_empty` runs `git log --name-status --format= A..B -- paths`; empty output counts as
evidence. Therefore `empty in <X>..<X> -- anything` (zero-length window) and
`empty in A..B -- <a path that never existed>` both re-derive as "empty".

* `fx-zero-window` (`empty in 5017e1f..5017e1f -- SKILL.md`) → **exit 0**: the `<tip>` atom is
  exempted by a correction that proves nothing. `receipts/fx-zero-length-window-correction.diff`.
* `fx-ghost-path-window` (`-- .ufo/waves/round-999/`) → **exit 1**, but for an unrelated reason:
  the battery's `non_empty` forgery rewrites the window and the result is *still* empty, so it
  counts as `forgeries_green 1` → `battery forgeries_green 1 != 0`. A card can be red solely
  because its correction named a path that never changed. `receipts/fx-window-correction-ghost-path.diff`.

**What the claim would have to say.** a window correction must name `A != B` **and** a path
that exists at `--rev`; and a forgery whose mutation is a no-op must be an error
(`correction_forgeries` decremented), not a green forgery.

## F9 — freeze integrity (C1's seat; reported because it gates every measurement above)

M8: `exact.py` prints `frozen_path_changed` and exits 2 for **every** candidate freeze except a
self-freeze at the measured rev. `touched/restored` name `plans/round-47-claims.md` (at the
freeze) and `tools/round-47/record.py` (from `9018c53b` on). The claims file's own
`## Frozen paths (exact)` lists both, so the document that declares the freeze is inside the
freeze: **any amendment to it breaks the freeze it declares**, and the round made seven
disclosed amendments (A1–A7), six of whose commits touch a frozen path. C2's counter never
checks its own bytes at all (`record.py` has no `frozen_set`/`SELF` check), which is why M5 can
be green with bytes no freeze covers. The block-24 content repair (`04469ee8`) touched no frozen
path, so repairing the F1 proxy harm and keeping the freeze were *not* in conflict; the conflict
is the counter's own amendments A1–A6.

**What the claim would have to say.** the declared freeze is a commit that already contains
every byte the claim measures, and amendments are forbidden after the first after-data run —
or the freeze is formally a series with each member named and the *last* member the only one
scored.

---

## Residual risk and verification gaps

* **The `2026-10-` regex floor.** `mapped` can only ever contain `2026-10-DD-…` stems. All 138
  files match today (checked: only `corpus/knowledge/.gitkeep` fails the pattern), but the first
  knowledge entry dated `2026-11-…` makes `N/N` unreachable by construction; the counter would
  then red a card that is telling the truth. Not a round-47 defect; a landmine for round 48.
* **The row text is unbounded.** Nothing caps the aim/limitation prose next to the fraction, so
  the head fraction can be true while the sentence that follows (`dangling []`, `citation_resolved_rules 24`,
  `command A`) is false — F1 and F4 are both instances.
* **Not run:** `record.py --selftest` at the landing (the claim does not require it; the SKILL
  registry row claims `9 cases`); [INFERENCE] that the A3 `historical` branch is the only reason
  M5 is green — I verified the branch exists in the bytes and that M4 (without it) is red on
  that line, but I did not re-run M5 with the branch disabled.
* **Not traced:** why `exact.py` reports `exact.py` itself as touched for
  `07d2894e..HEAD` while its blob OID is unchanged (`fb21a166` at both ends); the tool's own
  `touched` output is what I cite. The mechanism (directory pathspec / `history_touched`) belongs
  to C1's seat.
* Mechanism check left to the L1: `depth_pair`'s optional line selector means a rule block can
  be "resolved" by a bare path with no range, so depth can be green with a citation that points
  nowhere in particular. Command A is stricter only because it requires a *knowledge* file.

## Reproducing the fixtures

`receipts/` holds `driver.py`, `case1.py`…`case5.py`, `probe_depth.py`, `recipeA.py`, the two
counter byte-sets (`record-frozen-5017e1f.py`, `record-HEAD-a631bba0.py`), `fixture-index.json`
(every fixture's rev, exit, expected exit, command A values) and `fx-<name>.diff` for each
fixture's mutation against `5017e1f`. Each fixture is a fresh
`git clone -q --shared --no-checkout <lane> $D` with the toplevel asserted before the first
commit, then plumbing commits (`read-tree`/`hash-object`/`update-index`/`write-tree`/`commit-tree`).

```sh
export TMPDIR=/fast/scratch/hyaku/kaidoku-r47/RevC2Axes HYAKU_SCRATCH=$TMPDIR
python3 case1.py     # F2 (delete/rename/reflow), F3 (false green + false red)
python3 case2.py     # F4, F6, F8, F1 (freeze bytes)
R47_COUNTER=$TMPDIR/tools/round-47/record.head.py python3 case5.py   # F2/F3/F4 on HEAD's bytes
python3 case3.py     # F5 (both denominator shrinks) + controls
python3 case4.py     # F2 symmetric (coverage row deleted)
python3 probe_depth.py a631bba01633d2b5353306a569be4ce2e683d364      # per-block resolution, both definitions
```

Nothing was installed for this seat. No file outside
`.ufo/waves/round-47/w1/RevC2Axes/` was written in the lane; no mutating git command was run
in the lane or the fleet repo.
