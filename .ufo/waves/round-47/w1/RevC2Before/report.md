# RevC2Before — R47-C2 before-state: replication, independent re-derivation, and attack

Seat `RevC2Before`, lane `kaidoku-shokunin`, round 47 wave 1. Read-only on the lane tree;
every mutation below happened in a clone under `$S=/fast/scratch/hyaku/kaidoku-r47/RevC2Before`
(removed after the receipts were copied here).

| | |
|---|---|
| base | `13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5` |
| first freeze | `5017e1f7299c3a812e87e7950148f54313dd279e` |
| declared freeze now | A6 `f54b3b6de9085d3db449ed5d0916296cb29c1f6d` (six post-freeze commits) |
| lane HEAD when the seat opened | `3186f69b49798f2cc05727bbfd1604505fcee03b` |
| lane HEAD when the seat closed | `09a9f912f4a639b91bce7dcd3711d8f391969d4f` |
| `record.py` @ 5017e1f | sha256 `af666ce26c72e209e165779958489ed53182a1e68270aa9353da32ca2c8abe9d` (kept as `receipts/record.py@5017e1f.py`) |
| `record.py` @ HEAD | sha256 `abf352573d156ed1388683c882e40cab9897f426b9448356993bf41bf37779e7` |

The L1 landed A1–A7 **while this seat was running** (`9018c53b`, `62e33f7d`, `2e4ae434`,
`1e2c3102`, `07d2894e`, `f54b3b6d`, then `04469ee8`, `a0753786`, `31b092d1`, `f7d6e58`,
`09a9f912`). Findings are labelled with the bytes they were measured with: `frozen` =
`record.py@5017e1f`, `landed` = the worktree/HEAD bytes. Both are kept, because the round's
own claim is that they agree.

---

## 1. The before-state replicates, and each of its four atoms is independently confirmed

`python3 -I -B tools/round-47/record.py --root <LANE> --rev 13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5 --json-out <OUT>`
→ **exit 1**, `atoms 50`, `verified 46`, `mismatches 4`, `corrections 0`,
`atoms_by_class {axes 2, path 12, rev 33, seats 2, window 1}`,
stdout sha256 `53d81a3d27a4c0c832b334f0cc69aa97e414339574dc6b458f730630fd4d7e36`
(2026-10-28T18:03:32Z). Identical to `.ufo/waves/round-47/controls/ctl-c2-0-do-nothing.json`,
and identical under the frozen and the landed bytes — the before-state is stable.

Independent re-derivation, not the counter's own code:

1. **`seats/45`** — card says `Wave 1: 40 seats; wave 2: 32 seats (counts from
   .ufo/waves/round-45/{r45-w1,r45-w2}-results.json)`.
   `git show 13a9e9e1:.ufo/waves/round-45/w2-dispatch.json` → `{"resume":0,"spawn":36,"total":36}`;
   `w1-dispatch.json` → `{"spawn":40}`. And the file the sentence *cites* disagrees with it too:
   `git show 13a9e9e1:.ufo/waves/round-45/r45-w2-results.json` → `{"wave":"r45-w2","seats":36,
   "results":[36 items]}`. So `32` contradicts both the dispatch and its own cited receipt — the
   claim file's before text ("claimed `wave 2: 32`, dispatched `36`") understates the defect. Confirmed.
2. **`window/46`** — `0425224..<tip> -- tools/round-46 plans/round-46-claims.md` is empty at every
   measurement above`. No concrete pair → `unverifiable`, which the claim counts as a mismatch.
   It is also **false**:
   `git log --name-status --format= 0425224..13a9e9e -- tools/round-46 plans/round-46-claims.md`
   → `M tools/round-46/attest.py`, `M tools/round-46/gate.py` (both at `332f4884`). Confirmed, and
   worse than recorded (see F4).
3. **`axes/coverage`** — 133/133 vs 138/138. My own count at the base:
   `git ls-tree -r --name-only 13a9e9e1 -- corpus/knowledge` → 138 `.md` files; 138 unique stems;
   `corpus/README.md` `## Coverage map` → 138 `2026-10-..-*` tokens; intersection 138, unmapped `[]`,
   dangling `[]`. Also `1f4b27f8` → 138 files (the round-45 prose's `knowledge_files 138` is true),
   `e1c83313` → 133 (the row's number is true only at the revision it names). Confirmed 138/138.
4. **`axes/depth`** — 20/20 vs 23/23. My own resolver over `## Queue-drain craft ` at the base:
   23 `- **` blocks, 23 with every `corpus/|plans/|tools/` citation resolving in range, `bad []`.
   Confirmed 23/23.

`corrections 0 < 2` is the only other failing clause, as the claim says.

---

## 2. Findings

### F1 — HIGH — the landed after-cell is false about its own receipt (atoms 50 / exempted 2)

`SCORECARD.md` `## Round 47` (`09a9f912`) states R47-C2's after as
"`tools/round-47/record.py` over 50 atoms" and "exit 0, `atoms 50`, … `exempted 2 <= 3`", and the
calibration line repeats "4 → 0 mismatches over 50 atoms".

```
$ python3 -c "import json;d=json.load(open('.ufo/waves/round-47/l1/scores/c2-at-A7.json'));print(d['atoms'],len(d['exempted']))"
42 1                                    # exit 0
$ python3 -I -B tools/round-47/record.py --root . --rev 09a9f912f4a639… --json-out <OUT>
atoms 44 exempted 1 corrections 2 mismatches 0        # exit 0, stdout sha256 bda3988f7c7d67f2b4…
```

Three different numbers for one graded run: the card says **50/2**, the round's own A7 receipt says
**42/1**, the same counter at the lane head says **44/1**. 50 is the *base* receipt's atom count —
the window moved when the round-47 section was appended (round-45's 24 atoms left the last-two
window). No atom class reads the counter's `atoms`/`exempted`, so nothing fails.

*What the claim must say:* the record's after-cell must reproduce the cited receipt field for field,
and one clause must bind the record's counter-output atoms (e.g. `record.py` re-reads
`l1/scores/c2-at-*.json` and requires the card's `atoms`/`exempted`/`corrections` to equal the
receipt's at the cited rev). Without that, "the record re-derived against the repo" excludes the
record's most specific factual claim.

### F2 — HIGH — one fenced line turns a detected false atom into exit 0 (landed card)

Landed card, append `Waves: 9 + 9 = 99 seats.` to the round-47 section:

```
P2  exit 1, atoms 45, mismatches [seats/47], failing ["mismatches 1 != 0"]
    python3 -I -B tools/round-47/record.py --root $S/fx-p2_false_seats_visible --rev <tip> --json-out <OUT>
    stdout sha256 e86cfedb6d8dc071…   2026-10-28T18:03:34Z
```

Same sentence, with one fenced line inserted after the `## Round 47 —` heading:

```
P3  exit 0, atoms 26, mismatches [], failing []
    python3 -I -B tools/round-47/record.py --root $S/fx-p3_false_seats_fence_hidden --rev <tip> --json-out <OUT>
    stdout sha256 46cb87ff4ec2db5e…   2026-10-28T18:03:38Z
```

`sections()` ends a section at the first `\n## ` at column 0, fence-blind
(`record.py` `sections()`: `card.find("\n## ", pos + 1)`), so a `## …` line inside a code block
truncates the section body and every claim after it is never collected. A fenced `## Round 99`
heading instead **replaces** a real section in the last-two window: base card + one fenced
`## Round 99` → `sections ['round-46','round-99']`, atoms 50 → 26, the false round-45
`wave 2: 32 seats` drops out of scope, exit 0 (`fx-c4_fenced_round_heading`,
`fx-c13_decoy_section_core_only`, exit 0 with `false_sentence_present: true`).

*What the claim must say:* atoms are claims in the **prose** of the last two sections; headings and
sentences inside fenced code blocks are not sections and not claims (SCORECARD.md carries fenced
blocks routinely, so this is not hypothetical).

### F3 — HIGH — A1's stated premise is false, and the clause A1 deleted was the only one that caught an unrelated-window repair

The claims file A1 paragraph says the frozen clause made the target "unreachable by construction".
It did not. With `record.py@5017e1f` (sha256 `af666ce2…`), base card + rounded window restated as a
concrete pair + seats/path/window corrections:

```
P4 frozen   exit 0  atoms 50 mismatches [] corrections 3 corrections_bad [] battery 3/0
   stdout sha256 ac78476b0c23d547…  2026-10-28T18:03:41Z
P4 landed   exit 0  atoms 50 mismatches [] corrections 3 corrections_bad [] battery 3/0
   stdout sha256 dc22c6c4438865db…  2026-10-28T18:03:42Z
```

The repair is to state the window **in place** (a concrete pair), not to exempt it — the frozen
clause only required a window *correction*'s pair to exist in the card, and a card whose sentence
carries that pair satisfies it. So the clause was satisfiable; A1 removed it for a false reason.

What the deletion cost:

```
P5 frozen   exit 1  corrections_bad ["window pair names no atom in scope"]   sha 11a939c73fdd2044…
P5 landed   exit 0  corrections_bad []                                       sha 48bfeffc74f5c577…
```

P5 keeps the placeholder atom and exempts it with a true but **unrelated** window
(`empty in 22fd0d6..22fd0d6 -- corpus/lessons/round-46-verifier-spotcheck.md` for a claim about
`0425224..<tip> -- tools/round-46 plans/round-46-claims.md`). The frozen bytes called that what it
is; the landed bytes call it a repair. This is exactly the "exempts bubbles without re-deriving
anything" shape the claim's kill rule names, and it is now green.

*What the claim must say:* A1 is withdrawn (or restated: "the frozen clause admitted only in-place
restatement, which we judged too rigid" — not "unreachable"), and a window exemption must name the
atom's own path set, or state the atom's window and its non-emptiness.

### F4 — HIGH — the landed window correction is true and vacuous: it starts at the commit that falsifies the atom

Landed `## Record corrections — round 47`:

```
- corrects window round-46: empty in 332f4884..58eb04b6 -- tools/round-46 plans/round-46-claims.md
  — the round-46 sentence named a `<tip>` placeholder … and `git log --name-status --format=`
  over it prints nothing.
```

```
$ git log --name-status --format= 332f4884..58eb04b6 -- tools/round-46 plans/round-46-claims.md | wc -l
0                                       # exit 0 — the correction re-derives
$ git log --name-status --format= 0425224..13a9e9e -- tools/round-46 plans/round-46-claims.md
M   tools/round-46/attest.py
M   tools/round-46/gate.py              # exit 0 — the atom's own window is NOT empty
```

`332f4884` **is** the commit that touched the frozen paths (`round-46 F5: … the frozen set is now
derived at BOTH ends and unioned …`). A window that begins at the falsifying commit excludes it by
construction, so its emptiness carries no information about the atom's window (`0425224..tip`),
which is false. The record now exempts a false sentence with a true sentence about a different
range, and never states the falsity anywhere.

*What the claim must say:* a `window` exemption for a pair-less atom must state the atom's intended
window **and** whether it is empty; if it is not empty the correction must say so (the counter
re-derives non-emptiness too), otherwise the repair is substitution, not correction.

### F5 — HIGH — the C2 counter has no freeze arm and no self-pin; the claims file's freeze sentence is false for it

Claims file lines 10–11: "Nothing in this file or in `tools/round-47/` changes after the freeze: a
change makes **both** counters exit 2 `frozen_path_changed`."

```
$ grep -n "freeze_state\|add_argument" tools/round-47/record.py
474-478: --root --rev --no-battery --selftest --json-out          # no --freeze
32: SELF = "tools/round-47/record.py"                             # defined, never read
$ python3 -I -B tools/round-47/exact.py --freeze 5017e1f7 --rev 09a9f912f4 --json-out <OUT>
exit 2  reason frozen_path_changed  ['plans/round-47-claims.md','tools/round-47/',
                                     'tools/round-47/exact.py','tools/round-47/record.py']
$ python3 -I -B tools/round-47/record.py --root . --rev 09a9f912f4 --json-out <OUT>
exit 0                                                            # same frozen paths, no arm
```

`record.py` calls only `gate.resolve/show/out_path/scratch/emit/main_guard`; `gate.freeze_state`
— the round-46 `frozen_worktree_dirty` / `frozen_path_changed` core — is never invoked, and there is
no `interpreter_sha256` analogue for C2 (C1 has one; C2 does not). Consequence: `record.py`
executed from the worktree is the instrument, and it was edited four times post-freeze (A1, A3, A4,
A5 — A1 and A3 relax clauses, see F3, F6, F12) plus once in `exact.py` (A6). While this seat ran the
worktree copy was dirty against the freeze: at 14:47
`git status --porcelain -- tools/round-47/` → ` M tools/round-47/record.py` with exactly A1's hunk
removed (that diff is quoted in F3's evidence), and at 14:58 the worktree sha256 was
`abf35257…` against the freeze's `af666ce2…` — and the counter graded normally throughout.

*What the claim must say:* C2 gets the same `--freeze` arm and a `interpreter_sha256` pin as C1, or
the freeze sentence is narrowed to C1 and the record states that C2's instrument is the worktree
tree (and lists the six post-freeze commits as its freeze series, which the round section now does —
but the frozen claims file still says "both counters").

### F6 — MEDIUM-HIGH — `- corrects axes …` lines are unparsed: two landed corrections are unverified prose

`CORR = re.compile(r"^- corrects (seats|window|path|rev) (\S+):")` excludes `axes`, while
`corrects()` carries an `axes` branch that nothing can reach.

```
landed card, `- corrects axes depth: 24/24` → `99/99`:
P6 exit 0, corrections 2, corrections_bad [], mismatches []   sha e65d199960589a5b…  18:03:51Z
```

The claim's clause 3 says "an `axes` correction must state `<resolved>/<total>`", and the landed
record carries two such lines (`axes coverage: 138/138`, `axes depth: 24/24`). Neither is parsed, so
neither is re-derived; a false one passes. The axes *row* is edited in place and that edit is graded,
so the harm is confined to false provenance in the corrections section — but it is exactly the
"corrections that re-derive" property the claim sells.

*What the claim must say:* either `axes` joins the `CORR` alternation (with the pair-against-row-head
check), or the landed record stops writing `- corrects axes` lines and says the axes repair is the
row edit.

### F7 — MEDIUM — a section with zero atoms is green

```
P7  card = base + axes fixed + 2 true corrections + "## Round 47 — nothing measured this round
      \n\nNo counter was run."
    exit 0, atoms 26, mismatches [], failing []     sha 17de07462ad52396…  18:03:57Z
```

The class-coverage clause is global (`atoms_by_class`), not per section, so the **newest** section —
the one that is supposed to be "the current self-assessment" — can contribute nothing and the target
is still met. `sections` is satisfied because the headings exist (claims clause 5).

*What the claim must say:* each of the two sections carries at least one atom of at least one class
(preferably: the newest section carries at least the `axes`-bearing claim and one measured atom), or
clause 2 becomes per section.

### F8 — MEDIUM — the window class is a literal trigger word

Rephrase `… is empty at every measurement above` → `… was empty at every measurement above` and add
one true `… is empty` sentence elsewhere:

```
fx-c14_rephrase_trigger_word: atoms 50, window atoms 1 (the true sentence),
mismatches [seats/45, axes/coverage, axes/depth]   exit 1
```

The false window claim is no longer an atom; the class check stays satisfied by the decoy sentence.
Any phrasing other than the exact `is empty` ("was empty", "has no diff", "prints nothing") is
ungraded.

*What the claim must say:* the window class is "a sentence citing `git log` over a window and a
pathspec", not a sentence containing `is empty` — or the claim states the trigger verbatim and the
record keeps the verb.

### F9 — MEDIUM — the `axes` atom is the first fraction *anywhere* in the row remainder, including the score cell

```
fx-c7_first_fraction: row head edited to `| coverage | 9.72 → 10.0 138/138 | 133/133 knowledge
files mapped …` → coverage atom verifies (mismatches drop to [seats/45, window/46]), while the
observable sentence still says 133/133.
```

`collect_axes` runs `FRAC.search` over everything after the axis cell, so a true `138/138` inserted
in the score column satisfies the atom and the false observable stays. (The round-47 section already
rows this as "the `axes` class reads only the leading fraction, not the 0–10 score cell next to it" —
the other half of the same defect: it reads the *first* fraction, not the *observable* one.)

*What the claim must say:* the graded number is the observable column's leading fraction; the row
must carry exactly one `<resolved>/<total>` and it must be the one in the observable column.

### F10 — MEDIUM — path atoms are graded on their longest matching prefix

```
fx-c18_brace_path_token: section sentence `Evidence: .ufo/waves/round-46/{nope,nada}-results.json.`
→ path atoms 12 → 13, the new atom verifies, mismatches unchanged (4).
```

`WAVE_DIR` stops at `{`, so the atom is `.ufo/waves/round-46/`, a directory, and
`git show <rev>:.ufo/waves/round-46/` exits 0. The base card already carries one such atom
(`.ufo/waves/round-45/` from the brace-expanded citation). Any citation of the form
`dir/{a,b}.json` is existence-checked on `dir/`.

*What the claim must say:* a path atom is a file path; a token ending in `/` or containing `{` is
either expanded or reported as unresolvable, not scored.

### F11 — MEDIUM — the causal-separability paragraph is false: C2 reads the craft section

Claims file: "R47-C2's counter reads `SCORECARD.md` and the `.ufo/waves/round-*/` dispatch and
receipt files; it never reads the craft section." `record.py` `depth_pair()` does exactly that:

```python
craft = skill.split("## Queue-drain craft ", 1)[1].split("\n## ", 1)[0]
rules = re.split(r"(?m)^- \*\*", craft)[1:]      # -> the axes/depth atom
```

Fixture: base + one resolvable block 24 in SKILL.md →

```
depth atom claimed [20, 20], derived [24, 24]     # record.py --rev <fixture tip> --no-battery
```

So C2's `axes/depth` target depends on C1's landing (23/23 before block 24, 24/24 after), and the
landed correction `- corrects axes depth: 24/24` is only meaningful post-landing. "Either lands and
scores without the other" is not true for the depth half of the axes class.

*What the claim must say:* the axes/depth derivation reads `SKILL.md`; the two claims share that
surface, which is why the depth correction lands with block 24.

### F12 — MEDIUM — the battery is vacuous in the before-state and can misclassify an honest repair

* Before-state: `battery {"correction_forgeries": 3, "forgeries_green": 0}` with all three fixtures
  `{"error": "no corrections section"}`. Clause 6 therefore passes **for free** at the base — no
  forgery is built, none is scored. (`forged()` counts the error branch as a forgery.)
* `wrong_total` is a no-op whenever the corrections section has no
  `- corrects seats round-N: … N seats total` line → `forgeries_green 1` → red on an otherwise green
  card (`fx-c6_axes_correction_unreachable`, `fx-c2b_green_with_false_seats`).
* `non_empty` (frozen) replaces the pair's tip with `rev`; if `A..rev` is empty the "forgery" stays
  empty → `forgeries_green 1`. A **true** correction therefore fails clause 6:
  `- corrects window round-46: empty in f762b72..13a9e9e -- tools/round-47/` (true: the directory did
  not exist at `13a9e9e`) → `mismatches []`, `failing ["battery forgeries_green 1 != 0"]`, exit 1
  (`fx-c12_battery_window_path_after_rev`). A2 changed the mutated window to `root..rev`, which is
  non-empty for any path a round-4x tool touched and therefore closes the common case; the class
  survives for a correction over a path that changes nowhere between the root commit and `rev`
  (exactly a path introduced after `rev` — the shape `tools/round-47/` had at `13a9e9e1`).

Both defects are the ones A2/A5 name; they are confirmed independently here, and the before-state
vacuity (first bullet) is not disclosed anywhere.

### F13 — LOW — predicate field names that the receipt does not have

Clause 2 says "`classes` covers all five"; the receipt emits `atoms_by_class` and no `classes` key
(`sorted(receipt)` → `atoms, atoms_by_class, battery, corrections, corrections_bad, counter,
exempted, failing, met_target, mismatches, rev, sections, verified`). Clause 4's "`exempted <= 3`"
counts exempted **atoms**, not corrections; one seats correction can exempt two atoms.

### F14 — LOW/MEDIUM — "every machine-checkable atom" is wider than the five classes, and one ungraded atom in the window is false

Ungraded but machine-checkable, inside the two graded sections:

* `the **declared freeze is `0425224`**` (round 46). `git show --stat 0425224` → only
  `tools/round-46/registry.py`; `git log --format=%H -1 13a9e9e -- plans/round-46-claims.md` →
  `31820472…`. Under the round-46 claims file's own freeze definition ("the commit that first
  contains this file and `tools/round-46/`") the freeze is not `0425224`.
* `Is empty at every measurement above` — false (F4), recorded as `unverifiable` only.
* `knowledge_files 138`, `rule_blocks 23`, `citation_resolved_rules 23/23`, `coverage_score 10.0`,
  `mapped 138` — prose numbers, none graded (`138` happens to be true at `1f4b27f8`); the round-45
  paragraph's `rule blocks 21 → 22` and `citation_resolved_rules 22/22` are equally ungraded.
* `See `corpus/knowledge/2026-99-99-does-not-exist.md`.` adds no atom at all
  (`fx-c9_path_scope`: atoms 50 unchanged) — as scoped, but it is a file-existence claim that no
  command checks.

*What the claim must say:* the surface is "atoms of five syntactic classes", not "every
machine-checkable atom"; and either the round-46 freeze attribution is corrected or the claims'
scope is stated so a reader knows attribution prose is unaudited.

### F15 — LOW — the amendment ledger in the frozen claims file stops at A2

`git log --format='%h' 5017e1f7..09a9f912f4 -- tools/round-47 plans/round-47-claims.md` → six
commits (`9018c53b`, `62e33f7d`, `2e4ae434`, `1e2c3102`, `07d2894e`, `f54b3b6d`). The claims file
carries paragraphs for **A1 and A2 only**; A3 (a clause change: corrections for out-of-window rounds
stay valid), A4 (selftest fixture), A5 (battery ghost-atom placement), A6 (fixture citations +
`exact.py` edit) are described only in the round section and commit messages. A2's paragraph says
"Every clause, threshold and kill rule is byte-identical to A1" — true for A2, misleading as a
description of the series, since A3 and A5 changed clause and battery semantics.

---

## 3. What the record needs before it can be called green

1. Replace `atoms 50` / `exempted 2` with the cited receipt's values (`42` / `1` at `a0753786`;
   `44` / `1` at `09a9f912`) and add a clause that binds the record's counter-output atoms (F1).
2. Restate or withdraw A1's "unreachable by construction": the frozen bytes exit 0 (F3), and say
   what the deletion cost — an unrelated true window now exempts a false claim (F3/P5).
3. State the round-46 window truth: `0425224..13a9e9e -- tools/round-46 plans/round-46-claims.md`
   is **not** empty (`332f4884`), and the correction's `332f4884..58eb04b6` is a different,
   structurally-empty range (F4).
4. Fence-aware `sections()`/`collect()`, or a claim that says fences are part of the surface (F2).
5. `--freeze` + self-pin for `record.py`, or narrow the claims' freeze sentence to C1 (F5).
6. `axes` in the `CORR` alternation, or no `- corrects axes` lines in the record (F6).
7. A per-section atom floor (F7); the trigger stated as a window-with-pathspec, not the word
   `is empty` (F8); the observable-column fraction as the graded one (F9); `{`-tokens and directory
   tokens refused (F10); the separability paragraph corrected to name `SKILL.md` (F11); the
   before-state battery vacuity disclosed and `wrong_total`/`non_empty` no-ops treated as
   could-not-evaluate rather than as a red/green verdict (F12).

---

## 4. Residual risk and what was not run

* Nothing in §1 or §2 depends on the fleet repo, on `.ufo/state/`, or on any file outside the lane.
  All mutations were made in clones; the lane tree was read only.
* **Not run:** `record.py --selftest` against the landed bytes (the round's own test suite; I
  measured its behaviour through fixtures instead), and the C1 counter's clauses beyond the freeze
  arm shown in F5 (that is RevC1Before's scope).
* The base card's own `0425224..<tip>` sentence was left untouched in every fixture except where
  stated; no fixture "fixed" frozen bytes.
* Fixtures were rebuilt per probe from a local clone at `13a9e9e1` (or the lane at HEAD for the
  landed-card probes) and are gone with `$S`; the mutation functions are preserved verbatim in
  `receipts/attack.py`, `attack2.py`, `attack3.py`, `frozen_exp.py`, `probes.py` and re-create every
  case deterministically.
* The lane HEAD moved five times during the seat; `record.py` changed bytes once (A1) and semantics
  three more times (A3, A4, A5). Findings F1–F3 were re-measured at `09a9f912`; F6/F7 at `09a9f912`;
  F8–F12 at `13a9e9e1` with the landed counter (no clause involved changed between them apart from
  A3's out-of-window rule, which none of those fixtures exercise).

---

## 5. Receipts in this directory

Reproduce any case (the harnesses expect `$S/fx0` — a clone pinned at the base — and the frozen
counter bytes):

```sh
S=/fast/scratch/hyaku/kaidoku-r47/RevC2Before; mkdir -p "$S"
export TMPDIR="$S" HYAKU_SCRATCH="$S"
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
git clone -q "$L" "$S/fx0" && git -C "$S/fx0" config user.email st@r47 \
  && git -C "$S/fx0" config user.name "r47 fixture" \
  && git -C "$S/fx0" checkout -q 13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5
mkdir -p "$S/frozen/tools/round-47" "$S/frozen/tools/round-46"
git -C "$L" show 5017e1f7:tools/round-47/record.py > "$S/frozen/tools/round-47/record.py"
git -C "$L" show 5017e1f7:tools/round-46/gate.py   > "$S/frozen/tools/round-46/gate.py"
# then: python3 receipts/probes.py   (or attack.py / attack2.py / attack3.py / frozen_exp.py)
```

Every fixture asserts `git -C "$D" rev-parse --show-toplevel` equals `$D` before its first commit.

| file | what | exit / sha256 / UTC |
|---|---|---|
| `record-base.json` | P1 before-state at `13a9e9e1` (frozen bytes) | 1 / `53d81a3d…` / 17:50:39Z |
| `record-base-current.json` | P1 again with the landed bytes | 1 / `53d81a3d…` / 18:02:46Z |
| `receipts/revc2-probes.json` | every probe below with command, exit, stdout sha256, UTC | — |
| `record-at-head.json` | landed card at `f7d6e58` | 0 / atoms 44 |
| `record-at-final-head.json` | landed card at `09a9f912` | 0 / `bda3988f…` / atoms 44, exempted 1 |
| `exact-at-head.json` | C1 counter at `3186f69` (no block yet) | 1 |
| `exact-freeze-5017e1f.json` | C1 counter, freeze `5017e1f`, rev `09a9f912` | 2 `frozen_path_changed` (4 paths) |
| `exact-freeze-f54b3b6.json` | C1 counter, declared freeze A6 | 0 |
| `receipts/attack-results.json`, `attack2-results.json`, `attack3-results.json` | the fixture battery (F2, F7–F12) | per case |
| `receipts/frozen-experiment.json` | frozen vs landed bytes on the same cards (F3) | per case |
| `receipts/f4.json` | frozen-bytes reachability (F3/P4) | frozen 0, landed 0 |
| `receipts/landed-probe.json` | red→green on the landed card (F2/P2,P3) | 1 then 0 |
| `receipts/record.py@5017e1f.py` | the frozen counter bytes this seat measured | sha256 `af666ce2…` |
| `receipts/{attack,attack2,attack3,frozen_exp,probes}.py` | the exact harnesses | — |
| `receipts/{base.stdout,base-current.out,head.out,fh.out,exact.out,frozen_exp.out}` | raw stdout of the lane runs | — |
