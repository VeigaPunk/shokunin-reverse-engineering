# MutCorrections — round 47 C2: mutations of the corrections section

Seat: `MutCorrections` (mutation-tester). Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Claim attacked: **R47-C2** (`tools/round-47/record.py`, `plans/round-47-claims.md` § R47-C2).
Read-only on the lane tree; every mutation ran in a fixture clone under
`/fast/scratch/hyaku/kaidoku-r47/MutCorrections` (removed before yield; receipts copied to
`.ufo/waves/round-47/w1/MutCorrections/receipts/`).

## 0. Instrument and measured bytes

| item | value |
|---|---|
| detector | `tools/round-47/record.py` at the measured rev (sha256 `abf352573d156ed1388683c882e40cab9897f426b9448356993bf41bf37779e7`; identical at `07d2894e` and at the tip `f7d6e58d`) |
| fixture | `git clone --no-hardlinks <lane> <scratch>/clone`, then `git fetch origin main && git reset --hard origin/main`; `git rev-parse --show-toplevel` asserted equal to the clone before every commit |
| measured rev | `f7d6e58d6e7f4e664bf443137c55ee08821de244` (lane tip at first measurement; `SCORECARD.md` sha256 `de955ec7d9378f0ab3c0b3577c4a0a7330b44ef79f35a1403b5497fdcbfdff0b`, byte-equal to the lane worktree) |
| landing tip re-run | `b1a058f32c6908a6b92248052f151d0b0e2c76b1` ("final receipts at the tip"; `SCORECARD.md` sha256 `1e3afadb80f27c54e108e3bb8f9ad27bef721ae249253782996407ba24662861`, `atoms 44`, `exempted 1`, `corrections 2`, exit 0) — the survivors and controls were re-run here (§1b) |
| also measured | `07d2894eabe8…` (A5), `1e2c310295…` (A4), `a0753786…` (A7), `6f9fd7f8…` — same matrix, same exits (`matrix-at-07d2894.tsv`, `receipts/at-*.json`, `receipts/own-6f9fd7f8.json`) |

Counting command, every row below (both modes run from the clone so the detector and the bytes are the
same revision):

```sh
cd <clone>
python3 -I -B tools/round-47/record.py --root "$PWD" --rev <MUTANT_REV> [--no-battery] \
  --json-out receipts/<name>.<mode>.json
```

### Baseline (pristine tip)

| run | exit | failing | atoms | exempted | corrections | corrections_bad |
|---|---|---|---|---|---|---|
| `tip-base` @ `f7d6e58d` (2026-10-28T18:01Z) | 0 | `[]` | 44 | 1 | 2 | 0 |
| `restored-1`, `restored-2` @ `07d2894e`, after restore, twice | 0, 0 | `[]` | 41 | 1 | 2 | 0 |

Both restored runs printed byte-identical stdout (sha256 `d366b080e0112a5750edc6d169f760643867d03e9258c260d8e6fc956df4e4c2`), so the detector is deterministic on
these bytes and a later red is attributable to the mutation, not to run-to-run noise.

## 1. Mutation matrix

Each row is one commit on top of the pristine tip, card restored from the tip before each mutation.
`clause` = `--no-battery` (does the *predicate* see it), `full` = battery on (the claim's counting
mode). Exit 0 = mutant survived (green), 1 = killed, 2 = could not evaluate (none occurred).

| # | mutation | what it changes | clause | full | detected by | verdict |
|---|---|---|---|---|---|---|
| 1 | `wrong-round-in-window` | `- corrects seats round-45:` → `round-46:` (key now names the in-window round) | **1** | 1 | `corrections_bad 1` — claimed `[2,76]`, derived `[2,80]` from dispatch `[40,40]` | killed |
| 2 | `cross-round-total` | `round-45: 2 waves, 76` → `80 seats total` (80 is round-46's total) | **1** | 1 | `corrections_bad 1` — claimed `[2,80]`, derived `[2,76]` from dispatch `[40,36]` | killed |
| 3 | `ghost-path-exemption` | adds `- corrects path corpus/does/not/exist.md: landed` | **1** | 1 | two distinct reasons on one line: `{"exists": false}` and `"exempts an atom that does not exist"` | killed |
| 4 | `ghost-path-non-atom` | `- corrects path corpus/README.md:` (path exists, is not an atom) | **1** | 1 | `"exempts an atom that does not exist"` | killed |
| 5 | `ghost-path-window-pathspec` | window correction whose pathspec is `does/not/exist/` | **0** | 1 | clause sees nothing; red comes from `battery forgeries_green 1` (the `non_empty` forgery is a no-op over a nonexistent path) | **survived at clause level** |
| 6 | `window-pair-out-of-scope` | window pair `332f4884..332f4884` (self-empty, not the atom's window) | **0** | **0** | nothing | **survived** |
| 7 | `window-pair-real-other-commits` | window pair `1e2c310295..07d2894eab` over `tools/round-47/exact.py` (real commits, real path, empty, unrelated to the atom) | **0** | **0** | nothing | **survived** |
| 8 | `window-pair-atom-range` | window pair `0425224..58eb04b6` — **the atom's own range**, over the atom's own pathspec | **1** | 1 | `corrections_bad 1` (`empty: false`) | **the honest repair is rejected** |
| 9 | `duplicate-correction` | the seats line twice | **0** | **0** | nothing (`corrections 3`) | **survived** |
| 10 | `wrong-round-historical-true` | seats line replaced by `- corrects seats round-43: 2 waves, 64 seats total` (true, round 43 is outside the window) | **0** | **0** | nothing | **survived** |
| 11 | `false-axes-correction` | `- corrects axes coverage: 138/138` → `1/2` | **0** | **0** | nothing | **survived** |
| 12 | `false-axes-bogus-axis` | `- corrects axes bogus: 1/2` | **0** | **0** | nothing | **survived** |
| 13 | `axes-corrections-deleted` | both `- corrects axes …` lines removed | **0** | **0** | nothing (`corrections` stays 2) | **control: the landed axes corrections are inert** |
| 14 | `duplicate-replaces-repair` | the window line replaced by a second seats line | **1** | 1 | `mismatches 1` (the `<tip>` atom loses its exemption) | killed — control: the window repair is load-bearing |

Mutant commits (this tip run, `matrix.tsv`): `4ae4bea9` #1, `d1c7550d` #10, `73266e93` #2,
`95ee43c4` #3, `bfd4413b` #4, `789b8f8f` #5, `2cab9897` #6, `1593d4db` #7, `463ef66f` #8,
`a56eee4d` #9, `ba40cce8` #14, `ef17f6f1` #11, `324ebc0a` #12, `45856fd9` #13.
Per-row stdout sha256 and UTC are in `matrix.tsv`; JSON receipts and captured stdout in
`.ufo/waves/round-47/w1/MutCorrections/receipts/`.

Score: **6 killed, 6 survived, 1 honest repair rejected, 1 inert control.** Every kill in rows 1–4 and
14 is a genuine clause kill (the receipt names the failing clause). Rows 5 and 14 are also killed in
full mode, but by the battery, not by the clause — see W1.

## 1b. Re-run at the landing tip `b1a058f3` (card sha `1e3afadb`)

The card at the landing tip carries **two** `- corrects` lines — the two `axes` lines were replaced by
prose that repairs the two `## Owned axes` heads in place — and the counter reports `atoms 44`,
`exempted 1`, `corrections 2`, `failing []`, exit 0. Seven mutations were re-applied to that card
(one commit each on top of `b1a058f3`; receipts `receipts/<name>.*.json`):

| mutation | commit | clause | full | verdict |
|---|---|---|---|---|
| `cross-round-total` (`round-45: 2 waves, 80 seats total`) | `2ee8064f` | 1 | 1 | killed (`corrections_bad 1`) |
| `wrong-round-historical-true` (`round-43: 2 waves, 64 seats total`) | `9054e527` | **0** | **0** | **survived** |
| `window-pair-out-of-scope` (`332f4884..332f4884`) | `a6994162` | **0** | **0** | **survived** |
| `window-pair-real-other-commits` (`1e2c310295..07d2894eab -- tools/round-47/exact.py`) | `6f2b21ac` | **0** | **0** | **survived** |
| `duplicate-correction` (seats line twice) | `e17adb7c` | **0** | **0** | **survived** (`corrections 3`) |
| `false-axes-correction` (inserts `- corrects axes coverage: 1/2`) | `9c02880b` | **0** | **0** | **survived** |
| `window-pair-atom-range` (`0425224..58eb04b6`, the atom's own range) | `99bf4f33` | 1 | 1 | honest repair rejected |

Every exit matches the matrix at `f7d6e58d`. The landing edit that removed the inert `axes` lines
changed nothing the counter reads: `corrections` stays 2, and a *false* axes correction inserted into
the landed section is still green (row 6).

Receipt naming: the seven names in this table were re-run here, so
`.ufo/waves/round-47/w1/MutCorrections/receipts/<name>.*.json` holds the **landing-tip** run (revs
`2ee8064f`, `9054e527`, `a6994162`, `6f2b21ac`, `e17adb7c`, `9c02880b`, `99bf4f33`); the `f7d6e58d`
run of those same names is recorded by exit and stdout sha256 in `matrix.tsv`. The other receipts
(`wrong-round-in-window`, `ghost-path-*`, `duplicate-replaces-repair`, `false-axes-bogus-axis`,
`axes-corrections-deleted`) are the `f7d6e58d` run.

## 2. Findings

### F1 — `axes` corrections are never parsed, so clause 3's axes requirement is unenforceable (HIGH, vacuity)

`record.py:50` — `CORR = re.compile(r"^- corrects (seats|window|path|rev) (\S+):\s*(.+)$")` — omits
`axes` from the alternation, while `corrects()` carries an `axes` branch at `record.py:280` and a
second, unreachable one at `record.py:292` that references an undefined `atom` (`NameError` if it were
ever reached). Consequences, all measured:

- the landed card carries **4** `- corrects` lines (`grep -c '^- corrects' SCORECARD.md` → `4`) and the
  counter reports **`corrections 2`** (`receipts/tip-base.json`);
- a false axes correction is green: `- corrects axes coverage: 1/2` → exit **0**, both modes
  (`receipts/false-axes-correction.*.json`), and so is `- corrects axes bogus: 1/2`;
- deleting both axes lines changes nothing: `axes-corrections-deleted` → exit **0**,
  `corrections 2` (`receipts/axes-corrections-deleted.*.json`).

The claims file's clause 3 — "an `axes` correction must state `<resolved>/<total>`" — binds nothing.
`known_pairs` (`record.py:328`) is likewise computed and never read, which is the residue of A1's
deleted window-pair clause.

At the landing tip `b1a058f3` the card has already conceded this seam in prose — "the counter's
correction grammar parses `seats`, `window`, `path` and `rev` only, and an `axes` correction would be
silently inert (wave-1 `ConnSeparability`)" — and repaired both heads in place, so the section now has
2 `- corrects` lines and `corrections 2`. The frozen clause still requires the axes correction it
describes; a false one inserted into the landed section is green (§1b row 6). The claim's landed
surface therefore does not implement its own clause 3.

### F2 — the window exemption for a placeholder atom is unconditional (HIGH, satisfiable by any empty window)

`record.py:330-338`:

```python
def exempt(atom, entry):
    if atom["class"] != entry["class"]:
        return False
    if atom["class"] == "window":
        if atom.get("pair") is None:
            return True  # a placeholder claim is replaced by a concrete window
```

A window atom that names `<tip>` has no pair, so **any** window correction whose *own* stated window
is empty exempts it — regardless of which revisions it names or which pathspec it covers. Measured:
`332f4884..332f4884` (self-empty) → exit 0; `1e2c310295..07d2894eab -- tools/round-47/exact.py`
(real, empty, unrelated) → exit 0. Clause 4's "a `window` exemption covers only an atom whose window
pair the correction states, **or** an atom that names no concrete window" has its second disjunct
swallow the first for the only atom class it was written for.

### F3 — the landed window repair repudiates the atom instead of correcting it (HIGH; the card ships it)

The round-46 atom (`SCORECARD.md:3635`) claims:

```
git log --name-status 0425224..<tip> -- tools/round-46 plans/round-46-claims.md  is empty at every measurement above
```

The landed correction (`SCORECARD.md:3672`) states `empty in 332f4884..58eb04b6`. Measured:

| command | exit | stdout sha256 | lines |
|---|---|---|---|
| `git log --name-status --format= 0425224..58eb04b6 -- tools/round-46 plans/round-46-claims.md` | 0 | `7cd667fc1a11d75ba61b12bac5c458742f8b3fcaaf66e4f8df3e9dd67f77363e` | **4 — not empty** |
| `git log --name-status --format= 332f4884..58eb04b6 -- tools/round-46 plans/round-46-claims.md` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty input) | 0 |

The only change inside the atom's claimed range is `332f4884` (`M tools/round-46/attest.py`,
`M tools/round-46/gate.py`) — and the correction's window *starts at that commit*, spanning
`2026-10-28 14:09:34 -0300 .. 14:09:45 -0300` (11 seconds). So the atom was false at the tip it cites,
and the repair substitutes a window that begins after the falsifying commit. The counter cannot see it
(F2). Worse, the *honest* repair — stating the atom's own range — is rejected: mutation #8
(`empty in 0425224..58eb04b6 -- tools/round-46 plans/round-46-claims.md`) exits **1** with
`corrections_bad 1` because that range is not empty. **For a false window atom, the only passing
correction is a window that is not the atom's.**

### F4 — a nonexistent pathspec is accepted as window evidence (MEDIUM)

`window_empty()` (`record.py:90`) runs `git log … A..B -- <pathspec>` and reads only `stdout == ""`.
`git log` over a path that does not exist at either rev prints nothing and exits 0, so
`- corrects window round-46: empty in 332f4884..58eb04b6 -- does/not/exist/` re-derives as *true*
(`receipts/ghost-path-window-pathspec.no-battery.json`: `mismatches []`, `corrections_bad []`,
exit **0**). The `path` class checks existence; the `window` class never does. The full-mode red on
this mutant is accidental (W1), not detection.

### F5 — the repair floor counts lines, not distinct in-scope repairs (MEDIUM)

`record.py:382` — `if len(corr) < CORR_MIN` with `CORR_MIN = 2` — counts correction *lines*, and
`record.py:363` waives the "exempts an atom that does not exist" complaint for any `seats`/`window`
correction whose key is a round number older than the window. Measured:

- `duplicate-correction` (the same seats line twice) → exit **0**, `corrections 3`;
- `wrong-round-historical-true` (`- corrects seats round-43: 2 waves, 64 seats total` — true,
  but round 43 is not in the card) → exit **0**, `corrections 2`, `exempted 1`.

The landed card is already in this shape: its `round-45` seats correction exempts nothing
(`tip-base.json`: `exempted` holds only the window atom), so "at least two re-derived corrections"
is met by **one** in-scope repair plus one historical no-op. A duplicate alone would also satisfy it.
At the landing tip the same line could name round 43 instead of round 45 with no change in verdict
(§1b `wrong-round-historical-true` → exit 0, `corrections 2`), which is what makes the exemption's
scope unenforceable: the counter cannot tell a repair from a true statement about a round the card
never mentions.

### F6 — the card's own atom counts contradict the receipts they cite, and no clause can see it (MEDIUM, calibration)

Two rows of the landed card state numbers about the counter, and both are wrong against the receipt
they cite:

| row | claim | cited receipt | receipt says | my re-run |
|---|---|---|---|---|
| `## Owned axes` calibration | "re-derives **42 atoms** … `exempted 1 <= 3`" | `c2-at-A7.json` (`a0753786`) | `atoms 42`, exemptions 1 | `atoms 42`, exemptions 1 ✔ |
| `## Round 47` R47-C2 | "`atoms 42` … `exempted 2 <= 3`" | `c2-at-A7.json` (`a0753786`) | `atoms 42`, exemptions **1** | ✘ on `exempted` |
| (the landing's own receipt) | — | `c2-at-FINAL.json` (`6f9fd7f8`) | `atoms 44`, exemptions 1 | `atoms 44`, exemptions 1 |

So the landing row's `exempted 2` contradicts its own cited receipt, and its `atoms 42` is stale at the
landing revision (`44`). Earlier in the round the same rows said `50 atoms` / `exempted 2`, true only at
`1e2c310295`. The counter is silent because these are prose integers: `axes` atoms collect
only `<n>/<n>` fractions (`record.py:44`) and `rev` atoms only backticked hex (`record.py:47`), so a
sentence *about the instrument* is outside every atom class. `mismatches []` therefore coexists with a
row that misstates its own receipt — the same failure shape the round exists to remove, one level up.

Reproduction (clone at the landing tip):

```sh
python3 -I -B tools/round-47/record.py --root <clone> --rev 1e2c310295… --json-out r-a4.json  # atoms 50, exempted 2
python3 -I -B tools/round-47/record.py --root <clone> --rev a0753786…   --json-out r-a7.json  # atoms 42, exempted 1
python3 -I -B tools/round-47/record.py --root <clone> --rev 6f9fd7f8…   --json-out r-final.json # atoms 44, exempted 1
```

### W1 — the battery's red is not evidence the clause works (battery coupling)

`run_battery()` treats a no-op forgery as a green forgery (`record.py`, `forged()`: `"mutation was a
no-op"` → `forgeries_green += 1`), and two of the three forgeries are applied by regex over the raw
card (`correction-window-not-empty` needs an `empty in A..B` substring; `correction-wrong-seat-total`
needs `- corrects seats round-N: … N seats total`). Measured consequences:

- `ghost-path-window-pathspec` is red in full mode only because the `non_empty` forgery built from
  root..tip over `does/not/exist/` is *also* empty — the forgery was a no-op
  (`"mutation was a no-op"`, `forgeries_green 1`);
- `duplicate-replaces-repair` is red in full mode partly because the card no longer contains any
  `empty in A..B`, so `correction-window-not-empty` is again a no-op (`forgeries_green 1`).

A2 and A5 were both "a forgery that was a no-op" (`QUALITY.md` 78b). The class is not closed: the
battery still derives its fixtures from card text instead of from the parsed correction entry, so a
card-wording change can flip the battery red or green without touching the defect it names. Direction
for the L1 (not applied — frozen bytes): build each forged correction from the parsed `corr` entry and
score `mutation == no-op` as its own named failure, so a no-op can never be reported as
`forgeries_green`.

## 3. Cross-seat data (measured here, not my lane; for the C1 owner)

- The frozen claims file fixes the freeze at the commit carrying its A1 paragraph (`9018c53b`) and
  states "Nothing in this file or in `tools/round-47/` changes after the freeze: a change makes both
  counters exit 2 `frozen_path_changed`". Commits after `9018c53b` touching `tools/round-47/`:
  `62e33f7d` (A2), `2e4ae434` (A3), `1e2c3102` (A4), `07d2894e` (A5), `f54b3b6d` (A6).
  `git diff --numstat 5017e1f7..f7d6e58d -- tools/round-47/ plans/round-47-claims.md` →
  `record.py +28/−11`, `exact.py +15/−1`, `plans/round-47-claims.md +21/−0`. The card re-declares the
  freeze as A6 `f54b3b6d`; from A6 through the tip, `tools/round-47/exact.py` (content sha256
  `01a4bca7a60bb598…`) and `record.py` (`abf352573d156ed1…`) are byte-identical at every rev, so the
  A6 reading of the freeze is self-consistent — the churn is between the claims file's own text
  (freeze = the commit carrying its A1 paragraph, `9018c53b`) and A6.
- The lane tip moved four times during this seat's run (`07d2894e` → `f7d6e58d` → `09a9f912` →
  `b1a058f3`); the matrix was re-run at `f7d6e58d` and the surviving/control subset at `b1a058f3`,
  with identical exits. `record.py` and `exact.py` are byte-identical at every rev from A6 to
  `b1a058f3`; only `SCORECARD.md` changed (`de955ec7…` → `1e3afadb…`, another seat's landing edit).

## 4. What I did not test

- `rev`, `path`-exists and `seats`-pair atoms outside the corrections section (no mutation of the
  round-section prose itself; out of this seat's assignment).
- `--freeze` handling in `exact.py` beyond the read-only blob comparison in §3 (C1 owner's lane).
- Any mutation of `tools/round-47/record.py` itself: the assignment is corrections, and the detector
  was held byte-identical to the measured rev on purpose.

## 5. Restoration evidence

| item | before | after |
|---|---|---|
| clone HEAD | `f7d6e58d6e7f4e664bf443137c55ee08821de244` | `f7d6e58d6e7f4e664bf443137c55ee08821de244` (`git reset --hard`) |
| `SCORECARD.md` sha256 (clone) | `de955ec7d9378f0ab3c0b3577c4a0a7330b44ef79f35a1403b5497fdcbfdff0b` | `de955ec7d9378f0ab3c0b3577c4a0a7330b44ef79f35a1403b5497fdcbfdff0b` |
| `tools/round-47/record.py` sha256 (clone) | `abf352573d156ed1388683c882e40cab9897f426b9448356993bf41bf37779e7` | same (never edited) |
| `git status --porcelain` (clone) | – | `?? receipts/` only (this seat's own receipt dir) |
| pristine counter after restore, twice | – | exit 0 both, stdout sha256 `d366b080e011…4e4c2` identical |
| lane worktree `SCORECARD.md` sha256 | `de955ec7d937…` at my first measurement | `1e3afadb80f2…` at yield — changed by **another seat** (`6f9fd7f8`, "axes repaired in place"), not by this one; this seat wrote only `.ufo/waves/round-47/w1/MutCorrections*` |
| second snapshot (landing tip) | – | clone `reset --hard b1a058f3`, card sha256 back to `1e3afadb80f2…`, `git status --porcelain` = `?? receipts/` only, `record.py` still `abf35257…` |

Scratch `/fast/scratch/hyaku/kaidoku-r47/MutCorrections` removed after the receipts and scripts were
copied here (`.ufo/waves/round-47/w1/MutCorrections/`: `receipts/`,
`scripts/mutate.py`, `scripts/drive.sh`, `matrix.tsv`, `matrix-at-07d2894.tsv`). No install was needed for this seat.

## 6. Reading for the L1

C2's predicate kills a false correction that names an in-window round, a cross-round total, or a
ghost path — those four arms are real. It does **not** bind a correction to the atom it claims to
repair: the class/key check is satisfied by any empty window (F2), by any historical round (F5), or by
no line at all for `axes` (F1); and the landed card's own window correction is an evasion of a false
atom rather than a repair (F3). The claim's target (`failing == []`, exit 0) is met at the tip — this
seat reproduces exit 0 at `f7d6e58d` and at the landing `b1a058f3` — but it is met by an instrument
whose "two re-derived corrections" reduces to one repair plus one no-op (F5), whose window repair is an
evasion of the atom it names (F3), and whose axes clause has no implementation at all (F1). The card's
own counts about the counter are wrong at the landing and no clause can see them (F6).
