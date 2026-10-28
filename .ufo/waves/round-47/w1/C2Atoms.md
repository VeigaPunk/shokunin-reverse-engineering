# C2Atoms — R47-C2 atom verification and attack (round 47, wave 1)

Seat: `C2Atoms` (executor/verifier, leaf). Lane `kaidoku-shokunin`.
Task: enumerate and independently re-derive every atom `tools/round-47/record.py` extracts at
`13a9e9e1`, confirm the counter's four mismatches, and attack the frozen instrument before landing.
No lane file was edited; every fixture ran in a throwaway clone under
`/fast/scratch/hyaku/kaidoku-r47/C2Atoms/`.

## Verdict

1. **The atom layer is sound.** 50 atom instances / 41 distinct `(class,key,atom)` triples at the
   base `13a9e9e1`; my independent derivation (raw `git show` / `cat-file` / `ls-tree` / `rev-parse`
   / `merge-base`, no import of `record.py`) agrees with `record.derive()` on **every atom, zero
   disagreements**, at the base and at the landing. The counter's four base mismatches reproduce
   exactly, with the values below.
2. **The repair layer is not.** Four live forgeries score the counter green (`S1`, `S3`, `S6`, `S11`
   below), and one landed record cell contradicts the receipt it cites (`F7`). Details in Findings.

## Instrument pins (all receipts name their revision)

| role | rev | `tools/round-47/record.py` sha256 |
|---|---|---|
| freeze | `5017e1f7299c3a812e87e7950148f54313dd279e` | `af666ce26c72e209e165779958489ed53182a1e68270aa9353da32ca2c8abe9d` |
| A1 (drop window-pair clause) | `9018c53b16503c8d06d398b75503406508119946` | `787f909a76d43f9b…` |
| A2 (real window forgery) | `62e33f7dd75c8e3285967b26419842c106f6c965` | `fb6d5735cb93340b…` |
| A3 (historical corrections) | `2e4ae434…` | `8c0abb8b36a51d60…` |
| A4 (selftest fixture) | `1e2c3102952dc636650095643c1963c833859019` | `c704c3d407325264f8e2d990a8873524b0c5bbbf52d5dcc10ee8df411c9d6fa7` |
| A5 (ghost forgery inside the section) | `07d2894eabe88c326e9036262f20ad02662c860d` | `abf352573d156ed1388683c882e40cab9897f426b9448356993bf41bf37779e7` |
| attack pin / current | `04469ee8f30b9c086000c518bc482693282dd931` | `abf35257…` (unchanged through `f7d6e58d`) |

`grep -c frozen_path_changed tools/round-47/record.py` → **0**: `record.py` carries no frozen-path
check and no self-digest (see F8).

## Counter runs (exact commands, UTC 2026-10-28)

| # | card rev | command | exit | `failing` | atoms / verified / exempted / corrections | artifact sha256 |
|---|---|---|---|---|---|---|
| R1 | `13a9e9e1` (base) | `python3 -I -B tools/round-47/record.py --root . --rev 13a9e9e1… --json-out .ufo/waves/round-47/w1/C2Atoms/receipt.json` | **1** | `mismatches 4 != 0`, `corrections 0 < 2` | 50 / 46 / 0 / 0 | receipt.json `53d81a3d27a4c0c832b334f0cc69aa97e414339574dc6b458f730630fd4d7e36` |
| R2 | `13a9e9e1` | same `--no-battery` | **1** | (R1) | 50 / 46 / 0 / 0 | stdout `83ff46b799e27363975425da661a695ba9e5b75024af18f494ab9d8457cf9477` |
| R3 | `e856beb5` (landing) | `… --rev e856beb5… --json-out …/receipt-at-landing.json` | **0** | `[]` | 50 / 48 / **2** / 2 | `facc68dc4c21a89db21619112e11ef377c67432d7317c4d0e16402e58b7846e0` |
| R4 | `07d2894e` (A5) | `… --rev 07d2894e` | **0** | `[]` | **41 / 40 / 1** / 2 | reproduces committed `c2-at-A5.json` (`d366b080…`) |
| R5 | `a631bba0` (post-A5 card) | `… --rev a631bba0 --json-out …/receipt-at-head.json` | **0** | `[]` | **42 / 41 / 1** / 2 | `cedd96ed1c36be4821b5d7ecb774136df9be7fe1554b420276916a15a8369b28` |

R1's battery: `correction_forgeries 3`, `forgeries_green 0`, and all three fixtures carry
`{"error": "no corrections section"}` (see F5).

## Atom inventory at the base `13a9e9e1`

Sections in scope: `round-45`, `round-46`. 50 atom instances, 41 distinct triples (duplicates are
the same backticked rev repeated, e.g. `1f4b27f8` ×5, `0425224` ×4).

| class | instances | distinct | source |
|---|---|---|---|
| seats | 2 | 2 | `Wave 1: 40 seats; wave 2: 32 seats` (r45), `Waves: 40 + 40 = 80 seats` (r46) |
| window | 1 | 1 | the r46 `<tip>` sentence |
| path | 12 | 12 | 8 × `.ufo/waves/round-45/…`, 4 × `.ufo/waves/round-46/…` |
| rev | 33 | 24 | every backticked 7–40 hex token |
| axes | 2 | 2 | `coverage 133/133`, `depth 20/20` heads |

## Two atoms per class, re-derived with my own commands

| class | atom | command I wrote | value | counter | agree |
|---|---|---|---|---|---|
| seats | r45 pair, claimed `40 / 32` | `git show 13a9e9e1:.ufo/waves/round-45/w{1,2}-dispatch.json \| python3 -c 'json…["counts"]["spawn"]'` | `40`, `36` | mismatch | ✔ |
| seats | r46 sum, claimed `40 + 40 = 80` | same over `round-46/w{1,2}-dispatch.json` | `40`, `40` → 80 | verified | ✔ |
| window | r46 sentence | `git show 13a9e9e1:SCORECARD.md \| grep -c 'is empty'` → 1 atom in scope; the pair is `<tip>` | `unverifiable` | mismatch | ✔ |
| window | the same sentence's real window | `git log --name-status --format= 0425224..13a9e9e1 -- tools/round-46 plans/round-46-claims.md` | `M tools/round-46/attest.py`, `M tools/round-46/gate.py` → **not empty** (sha `23b39bb9…`) | — | the claim is false in substance, not only unparsable |
| path | `.ufo/waves/round-45/` | `git cat-file -t 13a9e9e1:.ufo/waves/round-45/` | `tree` | verified | ✔ |
| path | `.ufo/waves/round-46/controls/ctl-c2-1-v1-scope.json` | `git cat-file -e 13a9e9e1:<path>` | exit 0 | verified | ✔ |
| rev | `5382acc85f9d8617fe242fc116819b8055dfc4c7` | `git rev-parse --verify <tok>^{commit}` + `git merge-base --is-ancestor <oid> 13a9e9e1` | same oid, ancestor | verified | ✔ |
| rev | `50862e4a` | same | `50862e4a041499dd2ce0da68d10301b765bb9997`, ancestor | verified | ✔ |
| rev (negative control) | `e856beb5` (descendant) | `git merge-base --is-ancestor e856beb5 13a9e9e1` | exit **1** (rejected) | n/a | the ancestor clause discriminates |
| axes | `coverage 133/133` | `git ls-tree -r --name-only 13a9e9e1 -- corpus/knowledge \| grep -c '\.md$'` + README coverage-map token intersection | `138 / 138`, `missing []`, `dangling []` | mismatch | ✔ |
| axes | `depth 20/20` | count `^- \*\*` blocks in `## Queue-drain craft ` and check every `(corpus\|plans\|tools)/…(:line)` resolves inside its file at the rev | `23 / 23` | mismatch | ✔ |

The other 10 path atoms, 31 rev instances, both seats atoms and both axes atoms were re-derived by
the same script (`rederive.py`, receipts `rederive.json` / `rederive-landing.json`).

### Disagreements

`compare.py` joins both verdict sets by `(class,key,atom)`:

- base `13a9e9e1`: counter 41 distinct / mine 41; `only_in_counter []`, `only_in_mine []`,
  **`disagreements []`**; both name the same false set `{axes coverage, axes depth, seats 45, window 46}`.
- landing `e856beb5`: **`disagreements []`**; false set `{seats 45, window 46}` — i.e. at the landing
  the two axes heads are genuinely `138/138` and `24/24`, and the two remaining false atoms are
  suppressed by exemption, not repaired.

### The counter's four mismatches, confirmed

| atom | claimed | derived | evidence |
|---|---|---|---|
| `seats 45` | `wave 2: 32` | `36` (total 76, not 72) | `.ufo/waves/round-45/w2-dispatch.json` `counts.spawn 36` |
| `window 46` | `0425224..<tip>` | `unverifiable`; the concrete window is non-empty | `git log 0425224..13a9e9e1 -- tools/round-46 plans/round-46-claims.md` |
| `axes coverage` | `133/133` | `138/138` | 138 `corpus/knowledge/*.md`, all 138 mapped |
| `axes depth` | `20/20` | `23/23` | 23 craft rule blocks, all citations resolve |

The claims file's "Before" narrative is therefore exact, including the round-45 wave-2 value `36`
and the `133/133 → 138/138`, `20/20 → 23/23` pairs.

## Attacks (fixture clone, commits only inside the fixture; toplevel asserted every write)

Card under test = `SCORECARD.md` at the named revision, one text mutation per scenario, committed in
a fresh `git clone --no-hardlinks` of the lane; the counter is a **materialised copy** at the pinned
revision (never the moving worktree file). Receipts: `attacks-freeze.json` (pin `5017e1f`),
`attacks-HEAD.json` (pin `1e2c3102`, card `e856beb5`), `attacks-now.json` (pin `04469ee8`, card
`04469ee8`). Each scenario records `commit`, `card_sha256`, `stdout_sha256`, `exit`.

| # | forgery | pin `1e2c3102`, card `e856beb5` | pin `04469ee8`, card `04469ee8` | what it shows |
|---|---|---|---|---|
| S0 | none (control) | exit 0 | exit 0 | the landing reproduces green in a clean clone |
| **S1** | `- corrects axes coverage: 138/138` → `999/999` | **exit 0** | **exit 0** | axes corrections are never parsed or re-derived (F1) |
| S2 | drop the corrections section (also truncates the later round section) | exit 1, `mismatches 2` | exit 1, `mismatches 2` | the kill rule "deleting the corrections section restores the two mismatches" holds |
| **S3** | window correction re-pointed at `empty in 13a9e9e1..e856beb5 -- corpus/knowledge` | **exit 0**, exempted 2 | **exit 0**, exempted 1 | the r46 window atom is exempted by a window about a *different path in a different round* (F2) |
| S3b | window correction states `0425224..332f4884` (not empty) | exit 1, `corrections that do not re-derive: 1` | exit 1 | the window class *does* discriminate when the pathspec exists — negative control |
| S4 | window correction ends at the measured rev | exit 0 | exit 0 | A2's fix: the non-empty forgery is now a real forgery (was a no-op at the freeze pin) |
| S5 | roll the window forward (`## Round 47`, `## Round 48`) and delete all corrections | exit 1, `mismatches []`, failing `corrections 0 < 2` | exit 1, same | clause 1 is satisfied by scoping, not by repair: the false r45/r46 atoms simply leave the window (F2) |
| **S6** | only two *historical* corrections (round-45 seats, round-46 window) and no atom of either round in scope | exit 1 (battery ghost invisible → `forgeries_green 1`) | **exit 0**, `exempted []`, `corrections 2` | `corrections >= 2` is satisfiable by lines that name rounds outside the card and repair nothing (F3) |
| S6b | same, with the seats total `77` | exit 1 | exit 1 | the historical branch still re-derives its own total — negative control |
| S7 | append `- corrects path .ufo/waves/round-46/controls/ctl-c1-0-do-nothing.json: nothing is re-derived here` | **exit 0**, `corrections 3` | exit 0, `corrections 2` (line dropped, see F6) | a path/rev "correction" re-derives existence only; its text is never read |
| S8 | append a `## Round 47` section *after* the corrections section | exit 1, `battery forgeries_green 1 != 0` | exit 0 | pre-A5 the ghost forgery landed outside the section and turned a *true* card red; A5 fixes the battery, the parser truncation remains (F6) |
| **S11** | rewrite the r46 sentence to `0425224..13a9e9e1 -- corpuss/round-46` | **exit 0** | **exit 0** | a false "is empty" claim is green when the pathspec names nothing (F4) |

Freeze pin `5017e1f`: S0 (the landing card, unchanged) is **exit 1**
`corrections that do not re-derive: 1` — A1's red-before reproduces.

## Findings

**F1 — `axes` corrections are dead text (claims clause 3, `classes`, dead code).**
`CORR = re.compile(r"^- corrects (seats|window|path|rev) (\S+):…")` (record.py:50) cannot match
`axes`; the `axes` branch in `corrects()` (record.py:280-289) is therefore unreachable, and a second
copy of the same branch exists after the `path` branch (record.py:292-301). Consequences:
`corrections` is **2** at every landing rev while the section holds **4** `- corrects` lines; a
false axes correction is accepted (S1); an axes line naming a nonexistent atom is invisible, so
clause 3's ghost-atom rule does not cover the class the landing actually ships two of.
Command: `grep -c '^- corrects' SCORECARD.md` → 4 vs `"corrections": 2` in `receipt-at-landing.json`.
Fixture: `attacks-*.json` S1 (`card_sha256` recorded).

**F2 — the window exemption is key-blind and pair-blind (claims clause 1 + "exempted ≤ 3").**
`exempt()` returns `True` for a `window` atom with no concrete pair, for *any* correction of class
`window` (record.py:330-337), and A1 removed the pair check entirely. The landed correction states
`empty in 332f4884..58eb04b6 -- tools/round-46 plans/round-46-claims.md` — empty by the freeze
definition — while the sentence it supersedes names `0425224`, and `0425224..13a9e9e1` over the same
pathspec **is not empty** (two files modified by `332f4884`). The counter is green with
`exempted [window 46]`, so `mismatches == []` reports "no atom disagrees" about a record that still
disagrees. Any unrelated-but-empty window launders the atom (S3). Add S5: once a round adds a
section, the round-45 seat atom is not even examined, and `mismatches == []` still holds with zero
corrections.

**F3 — `corrections >= 2` is satisfiable with two out-of-scope lines (A3's `historical` branch).**
record.py:361-368 accepts a `seats`/`window` correction for a round older than the oldest section
without requiring the atom to exist. S6: a card whose last two sections are synthetic and whose only
corrections are the round-45/46 lines scores **exit 0** with `exempted []` — no atom is repaired, no
atom is even in scope, and the minimum is met. The claims file's "each correction line itself
re-derives" is true but empty: the line re-derives its own dispatch files, not the record.

**F4 — the `window` class cannot catch a false "empty" claim.**
`window_empty()` runs `git log --name-status --format= A..B -- <pathspec>`; a pathspec that names
nothing makes every window empty. S11 rewrites the round-46 sentence to
`0425224..13a9e9e1 -- corpuss/round-46` and the atom scores **verified**. The class catches only a
claim with no `A..B` (the `<tip>` placeholder), i.e. the malformed case, not the false case that
R46-V2 actually was.

**F5 — clause 6 is vacuous where it matters.**
`run_battery()` counts a fixture with `error: "no corrections section"` as a forgery that stayed red
(record.py:403-410). R1/R2 receipts: `correction_forgeries 3`, `forgeries_green 0`, all three
fixtures `{"error": "no corrections section"}`. So "three forged corrections each score the counter
red" is satisfied by forging nothing; the minimum `corrections >= 2` is the only clause that fails in
that state.

**F6 — `- corrects` lines after a later `## ` heading are silently dropped.**
`corrections()` (record.py:242-257) reads between `CORR_HEAD` and the next `\n## `. Pre-A5 the ghost
forgery was appended at EOF and landed outside the section, turning a true card red (S8 at pin
`1e2c3102`); A5 fixed the battery by inserting after the heading, but the parser is unchanged: at the
current card S7's appended line is dropped and `corrections` stays 2. A drafter who writes a
correction after the round section gets no error and no effect.

**F7 — the landed R47-C2 row contradicts the receipt it cites (the R46-V3 defect class, inside the
repair round).**
Row `R47-C2`, after cell: "`exit 0, atoms 50, mismatches [], corrections 2 both re-derived,
exempted 2 <= 3, battery 3/0` (`.ufo/waves/round-47/l1/scores/c2-at-A7.json`)", `measured at
1e2c310295`. `c2-at-A7.json` (`a0753786`) records `atoms 42`, `verified 41`, `exempted 1`; the A5
receipt records `atoms 41`, `exempted 1`. The numbers are true only at A4 `1e2c310295`, a revision
that **predates the round-47 section**, so the after-cell describes a card in which the round's own
section was not in scope. No atom class covers "the round's numeric claims about the counter's
output", so clause 1 cannot catch this. Fix: state `atoms 41 / exempted 1` at A5 (or cite
`c2-at-A4.json` with `atoms 50 / exempted 2` and name A4 as the measured revision).

**F8 — C2's instrument is not freeze-integrity-protected.**
The claims file says any change under `tools/round-47/` after the freeze "makes both counters exit 2
`frozen_path_changed`". `record.py` contains no such check and no self-digest (unlike C1's
`interpreter_sha256`): `grep -c frozen_path_changed tools/round-47/record.py` → 0, and the file
changed at A1, A2, A3, A4 and A5 (`af666ce2… → c704c3d4… → abf35257…`) while scoring green. The
series is disclosed in the round-47 section, but the claimed enforcement is unimplemented; a later
edit to `record.py` would be undetectable by any predicate in the claims file.

**F9 — the amendments' red-before/red-after claims reproduce.**
At pin `5017e1f` the landing card is red (`corrections that do not re-derive: 1`) — A1's premise
holds. S4 (window correction ending at the measured rev) is red at the freeze pin and green at the
current instrument — A2's fix is real. S8 is red at `1e2c3102` and green at `≥07d2894e` — A5's fix
is real. A3 is real but widens the vacuity in F3.

## Risks / not run

- The lane moved during verification (`13a9e9e1 → e856beb5 → 9018c53b → 62e33f7d → 2e4ae434 →
  1e2c3102 → caafeffa → 07d2894e → a631bba0 → 04469ee8 → 31b092d1 → f7d6e58d`). Every receipt names
  the revision and the `record.py` sha256 it scored; nothing here is asserted of an unnamed revision.
- Not run (outside this seat): `tools/round-47/exact.py`, `--profile v2|v3`, block 24 — R47-C1.
- No lane file, frozen byte, `.ufo/state/`, sibling directory or fleet-root file was written. The
  only writes are this report, its receipts under `.ufo/waves/round-47/w1/C2Atoms/`, and scratch.
- No installs.

## Sources

`plans/round-47-claims.md` (clauses 1-6, R47-C2), `tools/round-47/record.py` (lines 45-52, 145-306,
306-395, 395-443), `tools/round-46/gate.py` (`show`/`resolve`/`out_path`), `SCORECARD.md`
(`## Owned axes` rows 23-24, `## Round 45` seats line, `## Round 46` window sentence, `## Record
corrections — round 47`, `## Round 47`), `.ufo/waves/round-45/w{1,2}-dispatch.json`,
`.ufo/waves/round-46/w{1,2}-dispatch.json`, `.ufo/waves/round-47/w1-dispatch.json`,
`.ufo/waves/round-47/l1/scores/c2-at-A5.json`, `c2-at-A7.json`, `controls/ctl-c2-0-do-nothing.json`.

Receipts: `receipt.json`, `receipt-at-landing.json`, `receipt-at-head.json`, `rederive.json`,
`rederive-landing.json`, `compare-base.json`, `compare-landing.json`, `attacks-freeze.json`,
`attacks-HEAD.json`, `attacks-now.json`, `receipts.tsv`, `attack.py`, `rederive.py`, `compare.py`.
