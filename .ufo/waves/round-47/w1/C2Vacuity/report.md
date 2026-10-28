# C2Vacuity — R47-C2, can the exemption mechanism be abused?

Seat `C2Vacuity`, lane `kaidoku`, round 47 wave 1. Read-only on the lane tree: every mutation below
happened in a throwaway clone under `/fast/scratch/hyaku/kaidoku-r47/C2Vacuity/fix` (removed after
the receipts were copied here). No frozen byte was edited, no git state changed, no install was
performed.

**Instrument measured.** Every receipt in this directory was produced by the lane's own counter
executing from the lane worktree at git blob `636506bcb31d894343f9883621efdc4ffa22a38b`
(`sha256 abf352573d156ed1388683c882e40cab9897f426b9448356993bf41bf37779e7`,
`tools/round-47/record.py`), at `2026-10-28T18:01Z`, with `--root` = a clone of the lane and
`--rev` = a fixture commit on top of base `13a9e9e1…`. The lane was landing amendments *during*
this seat (`9018c53b`, `62e33f7d`, `2e4ae434`, `1e2c3102`, `07d2894e`, `f54b3b6d` all touch the
frozen paths); the first pass was measured at the pre-A5 bytes and every verdict below reproduced
after the re-measurement. `exits.txt` records the blob and lane HEAD per run, so a later reader can
tell whether the instrument moved again.

**Verdict.** The mechanism is *not* vacuous against the do-nothing record and three of the five
specified attack families stay red — but **four constructions reach `met_target: true` with a
materially false or unverifiable record** (A6, A7, A13, A14). The claim's Target sentence ("no atom
disagrees with committed state and none is `unverifiable`") is falsified by the claim's *own*
correction grammar: a `seats` correction binds `(waves, total)` and never the per-wave split, and a
`window` atom with no concrete pair is exempted by *any* reproducibly empty window. C2 also has
**no freeze arm at all**, although the claims file says a change to `tools/round-47/` makes "both
counters exit 2 `frozen_path_changed`".

## 1. What the frozen instrument actually is

| fact | evidence |
|---|---|
| `tools/round-47/record.py` at the declared freeze `5017e1f7` is blob `1f8e792898fd8d28ae4e63668eaebe07fa7a788d` | `git rev-parse 5017e1f7:tools/round-47/record.py` |
| at lane tip `3186f69b` it was `ace4f6df…`; at the measured tip it is `636506bc…` | `git rev-parse HEAD:tools/round-47/record.py` at each point; worktree clean (`git status --porcelain -- tools/round-47` = 0) |
| the frozen paths were amended **six times** after `5017e1f7` | `git log --format='%h %s' 5017e1f7..HEAD -- tools/round-47 plans/round-47-claims.md` → `9018c53b` A1, `62e33f7d` A2, `2e4ae434` A3 ("a seats/window correction for a round older than the window stays valid evidence" — a scoring change), `1e2c3102` A4, `07d2894e` A5, `f54b3b6d` A6 |
| the claims file at `5017e1f7` is `81aeb65e…`; at HEAD it is `15725e24…` | `git rev-parse 5017e1f7:plans/round-47-claims.md`, `git rev-parse HEAD:plans/round-47-claims.md` |
| `plans/round-47-claims.md:10-11` still states "Nothing in this file or in `tools/round-47/` changes after the freeze: a change makes both counters exit 2 `frozen_path_changed`" | `sed -n '10,11p' plans/round-47-claims.md` |
| `record.py` never reads the claims file, never pins its own bytes, and has no `--freeze` | `grep -c 'freeze_state\|frozen_path_changed' tools/round-47/record.py` = **0**; `--freeze …` → `record.py: error: unrecognized arguments`, exit 2 (argparse, *not* `frozen_path_changed`) |

The exemption machinery, as measured (blob `636506bc`, `record.py:326-370`):

```python
EXEMPT_MAX = 3                                                    # :36
CORR = re.compile(r"^- corrects (seats|window|path|rev) (\S+):\s*(.+)$")   # :50  — no `axes`
def exempt(atom, entry):                                          # :330
    if atom["class"] != entry["class"]: return False
    if atom["class"] == "window":
        if atom.get("pair") is None:
            return True   # :335 — a placeholder claim is replaced by a concrete window
        ...
    return str(atom["key"]) == str(entry["key"])                   # key only; shape is not in the key
```

`corrects()` re-derives a `seats` line as `(len(spawns), sum(spawns))` only (`:267-268`), a `rev`
line as `rev-parse` resolution **only** (`:300-302`, while the atom's own derivation also requires
ancestry, `:231-237`), and carries a reachable-looking `axes` branch (`:280-290`) plus a duplicated
unreachable one that names an undefined `atom` (`:292-296`) — unreachable because `CORR` cannot
produce an `axes` entry.

## 2. Attack matrix

Every row: card built from the byte-exact `SCORECARD.md` at base `13a9e9e1` (`cards/`, builder
`attack-builder.py`; `SIDESHA` is replaced with the empty side-branch commit created by the
fixture driver), committed in the throwaway clone, scored with:

```sh
python3 -I -B tools/round-47/record.py --root /fast/scratch/hyaku/kaidoku-r47/C2Vacuity/fix \
  --rev <fixture commit> --json-out <fixture>/r47-<attack>.json
```

| attack | met_target | exit | failing | exempted | corr / bad | mismatches | receipt sha256 (first 16) |
|---|---|---|---|---|---|---|---|
| `receipt.json` (base, lane) | False | 1 | mismatches 4 != 0; corrections 0 < 2 | — | 0 / 0 | seats:45, window:46, axes:coverage, axes:depth | `53d81a3d27a4c0c8` |
| `attack-A1b-exempt-all-true.json` | False | 1 | mismatches 2 != 0 | seats:45, window:46 | 48 / 0 | axes:coverage, axes:depth | `7874a823e3eed8be` |
| `attack-A1-exempt-every-atom.json` | False | 1 | mismatches 2 != 0; corrections that do not re-derive: 1 | seats:45, window:46 | 48 / 1 | axes:coverage, axes:depth | `8d51000aee99c03c` |
| `attack-A2-ghost-atom.json` | False | 1 | mismatches 3 != 0; corrections that do not re-derive: 2; battery forgeries_green 1 != 0 | seats:45 | 2 / 2 | window:46, axes:coverage, axes:depth | `63ea7337d9adeee4` |
| `attack-A3-seats-total-contradicted.json` | False | 1 | mismatches 2 != 0; corrections that do not re-derive: 1 | seats:45, window:46 | 2 / 1 | axes:coverage, axes:depth | `6fb5370fe9041d0f` |
| `attack-A4-window-not-empty.json` | False | 1 | mismatches 2 != 0; corrections that do not re-derive: 1 | seats:45, window:46 | 2 / 1 | axes:coverage, axes:depth | `76de070ca1eb1231` |
| `attack-A5-window-other-pair.json` | False | 1 | mismatches 2 != 0 | seats:45, window:46 | 2 / 0 | axes:coverage, axes:depth | `74ccf448c4069976` |
| `attack-A6-false-split-exempt.json` | **True** | **0** | — | seats:45 | 2 / 0 | — | `437e13e38fd8ca0a` |
| `attack-A7-nonancestor-rev-exempt.json` | **True** | **0** | — | seats:45, rev:ea6d6e27 | 3 / 0 | — | `1a1b9b3b5cd2b706` |
| `attack-A11-exempt-cap.json` | False | 1 | exempted 4 > 3 | seats:45, rev:ea6d6e27 ×3 | 3 / 0 | — | `c792c86735422cd3` |
| `attack-A12-axes-correction-dropped.json` | True | 0 | — | — | 2 / 0 | — | `0a8e4759a8bb697d` |
| `attack-A13-window-unrelated-pair.json` | **True** | **0** | — | seats:45, window:46 | 2 / 0 | — | `aacc28fc2f9646da` |
| `attack-A14-decorative-historical.json` | **True** | **0** | — | — | 3 / 0 | — | `74c6752abc5084ee` |
| `attack-A15-nonexistent-path-window.json` | False | 1 | battery forgeries_green 1 != 0 | — | 2 / 0 | — | `9b4a149695d7c0e7` |
| `attack-A8-duplicate-corrections.json` | False | 1 | battery forgeries_green 1 != 0 | — | 2 / 0 | — | `a68048d238d248ca` |
| `attack-A9-short-key.json` | False | 1 | battery forgeries_green 1 != 0 | — | 2 / 0 | — | `dca58a1d8b2fb634` |
| `attack-A10-honest-landing.json` | True | 0 | — | — | 2 / 0 | — | `7797253dec9fabad` |
| `attack-mut-orig.json` (pristine copy) | False | 1 | exempted 4 > 3 | seats:45, rev:ea6d6e27 ×3 | 3 / 0 | — | `a7cf8386db0cd303` |
| `attack-mut-weak.json` (`EXEMPT_MAX=99`) | **True** | **0** | — | seats:45, rev:ea6d6e27 ×3 | 3 / 0 | — | `e39d809ecdf3652e` |

`exits.txt` gives exit code, `met_target` and fixture commit per card; `manifest.json` gives the
full sha256 and UTC time of every receipt. Base `receipt.json` is byte-identical
(`53d81a3d…`) before and after the mid-seat amendments.

## 3. Findings

### F1 — HIGH: a false per-wave seat split scores `met_target: true` (A6)
Card `cards/A6-false-split-exempt.md` states `Wave 1: 36 seats; wave 2: 40 seats (counts from …)`;
the dispatch files say `40` and `36` (base receipt: `{"claimed": [40, 32], "derived": [40, 36]}`).
The correction `- corrects seats round-45: 2 waves, 76 seats total` re-derives `true` and
`exempt()` matches on class+key, so the swapped split is exempted, not corrected.
`corrects()` has no grammar for a per-wave split (`CORR_SEATS`, `:51`).
Result: exit 0, `exempted: [seats:45]`, `mismatches: []`, receipt `437e13e38fd8ca0a`, fixture
commit `5a179b27…`. Inside the claim's letter (clause 3 mandates this correction form), outside its
intent: clause 1 cannot bind the shape clause 3 is allowed to exempt.

### F2 — HIGH: an unverifiable `<tip>` window claim is exempted by an unrelated empty window (A13)
`cards/A13-window-unrelated-pair.md` keeps round 46's defective sentence
``0425224..<tip> -- tools/round-46 plans/round-46-claims.md` is empty at every measurement above.``
— the exact R46-V2 defect this round exists to close — and adds
`- corrects window round-46: empty in 13a9e9e1..13a9e9e1 -- corpus/knowledge/`, a window sharing no
revision, no pathspec and no atom with the claim. `exempt()` returns `True` for any atom whose
`pair` is `None` (`:335`), and no clause ties the correction's window to the atom.
Exit 0, `exempted: [seats:45, window:46]`, `corrections_bad: []`, `mismatches: []`, receipt
`aacc28fc2f9646da`, commit `2a4f5ece…`. A5 isolates the lever: the window atom is exempted by a
correction naming a different window with `corrections_bad []` (`74ccf448c4069976`).
Claim clause 4 ("or an atom that names no concrete window") authorises this; clause 1's gloss
("none is `unverifiable`") is then false — an exempted atom is never a mismatch.

### F3 — HIGH: C2 has no freeze arm; its own interpreter is unpinned and moved 6× after the freeze
`record.py` contains no `freeze_state` call (0 occurrences), takes no `--freeze`, and never hashes
itself or the claims file, so `plans/round-47-claims.md:10-11` ("a change makes **both** counters
exit 2 `frozen_path_changed`") is false for C2. Frozen paths changed at `9018c53b`, `62e33f7d`,
`2e4ae434` (A3 — scoring semantics: the historical exemption), `1e2c3102`, `07d2894e`, `f54b3b6d`;
A3 and A4 have no paragraph in the claims file.

Demonstration that the missing arm is load-bearing — one line of the counter changed
(`EXEMPT_MAX = 3` → `99`, line 36), same card:

```
record.orig.py  exit=1  met_target False  failing ['exempted 4 > 3']    receipt a7cf8386db0cd303
record.weak.py  exit=0  met_target True   failing []                    receipt e39d809ecdf3652e
$ diff record.orig.py record.weak.py   →   36c36   EXEMPT_MAX = 3 / EXEMPT_MAX = 99
```

Command: `python3 -I -B <copy> --root <fixture> --rev 82d4822d… --json-out <fixture>/r47-mut-<tag>.json`.
Both copies are here (`record.orig.py`, `record.weak.py`) with their stdout and receipts. Nothing in
C2 can detect this class of change.
**Routing note for C1 (not executed by this seat):** `gate.freeze_state` unions the set at both ends
(`gate.py:156-196`), so at any measured rev ≥ `62e33f7d` the amendments make `frozen_path_changed`
non-empty over `tools/round-47/` and `plans/round-47-claims.md`; C1 needs a re-declared freeze at
the amended commit before its exit 0 is reachable.

### F4 — MEDIUM: clause 3's `axes` correction form is unreachable; an axes line is silently dropped
`CORR` (`:50`) accepts only `seats|window|path|rev`, so `- corrects axes coverage: 138/138` is
neither counted nor flagged. A12's card carries four correction lines; the counter reports
`corrections: 2`, `corrections_bad: []`, exit 0 (receipt `0a8e4759a8bb697d`). `corrects()` keeps an
`axes` branch (`:280-290`) and a duplicated unreachable one that names an undefined `atom`
(`:292-296`) — dead code that clause 3 nonetheless specifies. Consequence: the two `## Owned axes`
rows (`133/133`→`138/138`, `20/20`→`23/23`) can only be repaired by editing the table, and
"exempt every atom" can never be green — A1b (all-true corrections, record untouched) exits 1 with
`mismatches 2`, the two axes atoms (`7874a823e3eed8be`).

### F5 — MEDIUM: a `rev` correction re-derives less than the atom it exempts (A7)
Atom: resolves **and** is an ancestor of `--rev` (`:231-237`). Correction: resolves only
(`:300-302`). A7 cites `ea6d6e27…`, an empty commit on the base that is not an ancestor of the
measured rev, and exempts it: exit 0, `exempted: [seats:45, rev:ea6d6e27]`
(`1a1b9b3b5cd2b706`, commit `8300ce43…`). This is the R46-V3 defect class ("the revision its
before-cell was measured at") re-entering through the correction grammar.
The cap holds: three such atoms → `exempted 4 > 3`, exit 1 (A11, `c792c86735422cd3`).

### F6 — MEDIUM: `corrections >= 2` is satisfiable by corrections unrelated to any atom in scope
A3 (`2e4ae434`) exempts `seats`/`window` keys older than the window from the "atom does not exist"
arm. A14 adds `- corrects seats round-40: 2 waves, 80 seats total` (round 40's dispatches are 42+38;
the card covers rounds 45–46) to an otherwise green card and exits 0 with `corrections_bad: []`
(`74c6752abc5084ee`). The claims' clause 3 says "A correction that exempts an atom the card does
not contain is itself a defect" — the counter contradicts that sentence for older `seats`/`window`
keys. Two identical true corrections also count as two (A8), red only because the battery then has
no `empty in` line to mutate.

### F7 — MEDIUM (landing trap): the battery silently requires a `round-<N>` seats key and an `empty in` line
`run_battery.wrong_total` matches `- corrects seats round-[0-9]+: … (\d+) seats total`; the key the
counter itself accepts, `- corrects seats 45: …`, makes the forgery a no-op → `forgeries_green 1`
→ permanent red: `failing ['battery forgeries_green 1 != 0']`, exit 1 (A9, `dca58a1d8b2fb634`).
Same with no window line at all (A8, `a68048d238d248ca`). Neither requirement is in the claims file.

### F8 — LOW: a mistyped `--json-out` directory reports "not met" instead of "could not evaluate"
`gate.emit` opens the path without creating parents and the `FileNotFoundError` escapes
`main_guard` (it is raised after evaluation): observed exit **1**, traceback, **no receipt**, when
`--json-out` named a non-existent directory inside the root; the same run with an existing
directory exits 1 *with* a receipt. A grading run can read a crash as "not met".

### Passes (red for the right reason)
- **Exempt everything, correct nothing** (A1, A1b): never green — the two `axes` atoms cannot be
  exempted (F4) and A1's per-round total is re-derived (`claimed [2,76]` vs `derived [2,80]`).
- **Exempt an atom that does not exist** (A2): the nonexistent path plus "exempts an atom that does
  not exist"; the battery also no-ops without a window line.
- **Seats total the dispatch files contradict** (A3): `claimed [2,75]` vs `derived [2,76]`.
- **A window that is not empty** (A4): `{"empty": False, "window": "31820472..13a9e9e1"}`.
- **Exemption cap** (A11): `exempted 4 > 3`.
- **A window over a pathspec that never existed** (A15): the atom verifies (`mismatches []`), but
  the battery's root..rev forgery is empty too → `forgeries_green 1`, exit 1
  (`9b4a149695d7c0e7`). Blocked incidentally by the battery, not by any clause.

## 4. Landing guidance, measured
- The intended landing **is reachable**: A10 (record made true by hand, axes rows edited, one
  `seats round-45` line, one empty-window `window round-46` line) exits 0 with `exempted: []`
  (`7797253dec9fabad`). Corrections are decorative once the record is true — which is exactly why
  F1/F2 matter.
- The known-green window is degenerate (`31820472..31820472`, empty because `A..A`); a window
  correction has to be *reproducibly* empty, and the battery only requires `root..rev` to be
  non-empty, so a degenerate window passes while an unrelated one does too (F2).
- Write the seats key as `round-45`, not `45` (F7), and include exactly one `empty in` line (F7).
- Do not expect an `axes` correction line to count (F4): edit the `## Owned axes` rows.

## 5. Calibration check of the claim's own `Before`
Base `receipt.json` (`53d81a3d27a4c0c8`, exit 1) reproduces the claims' `Before` exactly:
`mismatches 4` = seats:45 (`claimed [40,32]`, `derived [40,36]` — the claim says "wave 2: 32,
dispatched 36" ✓), window:46 (`unverifiable`, the `<tip>` placeholder ✓), axes:coverage
`133/133` vs `138/138` ✓, axes:depth `20/20` vs `23/23` ✓. The `Before` clause is honest.
The `Kill rule` sentence "A corrections section that exempts bubbles without re-deriving anything
fails clause 3/4" is **not** what the counter implements: a correction that re-derives *anything*
empty, however unrelated, exempts a placeholder atom (F2), and two unrelated historical corrections
satisfy `corrections >= 2` with zero exemptions (F6).

## 6. Evidence inventory (this directory)
`receipt.json` (base, lane), 19 `attack-*.json` receipts, `attack-*.stdout.json` (the counter's own
stdout, identical bytes), `exits.txt` (exit code + fixture commit + instrument blob per card),
`manifest.json` (sha256 + UTC + verdict per receipt), `cards/` (16 exact `SCORECARD.md` attack
cards, `SIDESHA` token), `attack-builder.py`, `remeasure.sh` (the driver that built every receipt and `exits.txt`),
`record.orig.py` / `record.weak.py` + their stdout and receipts (F3).

Reproduction: `git clone -q --shared <lane> $S/fix`; `git -C $S/fix rev-parse --show-toplevel` =
`$S/fix`; throwaway identity configured **inside the clone only**; empty side commit
`ea6d6e273c6f1d80004716aae8ff0da16731d440` on base (not an ancestor of any measured rev); per card
`git checkout --detach 13a9e9e1…`, write the card (with `SIDESHA` substituted), commit, score with
`--root $S/fix --rev <commit>`.

## 7. Not run
- `tools/round-47/exact.py` (R47-C1) and its battery — F3's routing note is read from `gate.py` and
  the commit log, not executed.
- `record.py --selftest` — post-integration gate owned by the L1.
- No network, no installs, no writes outside this directory and the scratch clone.
