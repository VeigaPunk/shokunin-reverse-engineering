# RevC2Window — R47-C2 attack: the window class

Seat `RevC2Window`, wave 1, round 47. Read-only on the lane; every measurement below was
made from my own scratch copies and from a read-only clone. No frozen byte was modified.

**Answer up front.** Of the four mandated vectors, one is detected (rename-only ranges, when
the pathspec names either side of the rename), one is detected only by accident (an empty
`--` pathspec is graded as an *unrestricted* range, so it is red for the wrong reason and
green when the range is empty), and two pass outright (a pathspec that names no path, and a
window whose tip is not pinned to `--rev`). Beyond those, the window atom accepts a reversed
pair, a degenerate `X..X` pair, a merge-only range, and a second pair on the same line; and
every red window atom that names a pair is laundered to green by a correction that states the
same pair with a dead pathspec. Worst of all, the **landed** round-46 correction narrows the
window past the one commit that makes the original sentence false (HIGH-0), and the counter
reports the record clean. Measured on all three instrument states (frozen, A1–A4,
A6–A7): **identical behaviour on all 36 attack runs.**

## 0. Instruments and revisions measured

| role | revision | sha256 of `tools/round-47/record.py` |
|---|---|---|
| frozen (the claimed surface) | `5017e1f7299c3a812e87e7950148f54313dd279e` | `af666ce26c72e209e165779958489ed53182a1e68270aa9353da32ca2c8abe9d` |
| amended A1–A4 | `1e2c3102952dc636650095643c1963c833859019` | `c704c3d407325264f8e2d990a8873524b0c5bbbf52d5dcc10ee8df411c9d6fa7` |
| current (A5–A7) | `31b092d17e77f5064c919383a9bc1e6cbfd2d1ff` | `abf352573d156ed1388683c882e40cab9897f426b9448356993bf41bf37779e7` |

`tools/round-47/exact.py` at the freeze: `dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c`
— equal to the `interpreter_sha256` pin in `SKILL.md` block 24, so that pin is honest at the
freeze. `tools/round-46/gate.py` is byte-identical at the freeze and at lane HEAD
(`git diff --stat 5017e1f -- tools/round-46/` → empty).

The lane advanced while I measured (base `13a9e9e1` → freeze `5017e1f` → A1–A7 → `31b092d1`).
Every claim below names the revision it was measured at, and each was re-measured at the tip.

### Fixture

`receipts/probe.py` builds one deterministic repo (fixed identity and dates, so the object
ids are stable across runs):

| ref | oid | content |
|---|---|---|
| `c1` | `f935b668` | base: `tools/y/keep.md`, `tools/other/a.md`, corpus, SKILL, dispatch files |
| `c2` | `1ec0c07b` | touches `tools/other/a.md` only |
| `c3` | `039f8872` | touches `tools/y/keep.md` |
| `c4` | `e4236ca0` | **rename only**: `tools/y/keep.md` → `tools/z/keep.md` |
| `c5` | `27f3183c` | `tools/other/a.md` again; `tools/y/` no longer exists |
| `side` | `491e7d93` | touches `tools/q/q.md` (not the merge window's path) |
| `merge` | `16915655` | merge whose **resolution** edits `tools/z/keep.md` |
| `orphan` | `a553459e` | root commit touching neither `tools/x` nor `tools/y`/`tools/z` |

Each case is a card committed on top, so `--rev` is the card commit; seats/path/rev/axes
atoms are held green (control `k00` exits **0**), so an exit 0 on any other case means the
counter accepted the forged window sentence. Runs use `--no-battery` to isolate clause 1 from
clause 6. `--json-out` cannot be used in a fixture: `gate.out_path` requires the target to be
inside `--root`; receipts are captured stdout with sha256.

```
python3 -I -B $S/inst/tools/round-47/record.py --root $FIX --rev <card-commit> --no-battery
# instrument under test: RECORD_OVERRIDE=$S/inst[-head|-cur]/tools/round-47/record.py python3 probe.py
```

## 1. The four mandated vectors — verdicts

| vector | case | exit | window atom | detected? |
|---|---|---|---|---|
| abbreviated hashes, 7 hex (git's default short form) | `k01` | **0** | verified | resolved and accepted — correct |
| abbreviated hashes, 6 hex | `k02` | 1 | `unverifiable` | red **without ever resolving** the id |
| hex naming a non-commit object (a blob) | `k03` | 1 | `empty: false` | red, but the window is graded as a phantom tree (below) |
| window tip outside `--rev`'s ancestry (orphan commit) | `k09` | **0** | verified | **not detected** |
| **path that does not exist** | `k04` | **0** | verified | **not detected** |
| **`--` with an empty pathspec**, range has a commit | `k05` | 1 | `pathspec: []` | rejected only because the *unrestricted* range is non-empty |
| **`--` with an empty pathspec**, range empty | `k06` | **0** | verified | **not detected** — nothing is verified |
| **rename-only range**, pathspec = old path | `k13` | 1 | `empty: false` | detected (`D tools/y/keep.md`) |
| **rename-only range**, pathspec = new path | `k14` | 1 | `empty: false` | detected (`A tools/z/keep.md`) |
| **rename removed the pathspec directory** before the window | `k15` | **0** | verified | **not detected** |

The three detections in `k05`/`k13`/`k14` are real but incidental: `k05` fails because the
arm drops the pathspec entirely and grades the whole range, and `k13`/`k14` fail because git
still prints the `D`/`A` side of the rename. None of them is a clause.

## 2. Findings by severity

### HIGH-0 — the landed round-46 repair narrows the window past the commit that falsifies the sentence, and no clause compares bases

The round-46 sentence (`SCORECARD.md:3635`, still in place) reads
"`git log --name-status 0425224..<tip> -- tools/round-46 plans/round-46-claims.md` is empty at
every measurement above". The correction supplies the tip (`58eb04b6`). Read with the
sentence's own base, the claim is **false**:

```
git -C $LANE log --name-status --format= 0425224..58eb04b6 -- tools/round-46 plans/round-46-claims.md
  -> exit 0, 52 bytes, "M\ttools/round-46/attest.py\nM\ttools/round-46/gate.py\n"   sha f7ace3d35eb9
git -C $LANE log --name-status --format= 332f4884..58eb04b6 -- <same paths>
  -> exit 0,  0 bytes                                                              sha e3b0c44298fc
git -C $LANE log --name-status --format= 0425224..332f4884 -- <same paths>
  -> exit 0, 52 bytes  (one commit: 332f4884, "round-46 F5: close the two HIGH instrument defects")
```

The correction states `332f4884..58eb04b6`: its base **is** the commit that changed
`attest.py` and `gate.py`, so the window is empty because it excludes the only falsifying
commit. `record.py` cannot see this — the atom's pair is `None`, so `exempt()` takes the
placeholder branch and the correction's numbers are never compared with the base the atom
names (`0425224`). Result at the tip: `mismatches []`, exit **0**, `exempted: [window]`
(`receipts/card-at-current-cur.json`), and `V3` shows the same atom accepted with an outright
degenerate pair `58eb04b6..58eb04b6` (`receipts/realcard-current.json`).

Corroborated independently by seat `LabWindowProbe`
(`.ufo/waves/round-47/w1/LabWindowProbe/window-receipt.json`): self-windows 0 B, the literal
`0425224..58eb04b6` 52 B, `record.py` exit 0 on the self-windows with the full battery.

**What the claim would have to say:** for an atom that names a concrete base and a placeholder
tip, the exemption must state **that same base** (`0425224..<tip>`), and the atom must then be
red; the honest repair is to record the atom as *false and corrected* — "`attest.py` and
`gate.py` changed in `0425224..332f4884`; the sentence's 'is empty' is false for its own base"
— not an emptiness exemption over a shortened window. Clause 4 must require the correction's
base to equal the base the exempted atom states.

### HIGH-1 — a merge-only range reads empty: `R45-CL6`'s defect class inside the window arm

`window_empty()` (`record.py:90-95` at the freeze) runs `git log --name-status --format=`.
For a merge commit that prints **no file list**. `gate.history_touched()` uses
`-m --diff-merges=first-parent` precisely because of this; the window arm does not.

```
# k16: the only commit in c5..merge touching the path is the merge resolution
git -C $FIX log  --name-status --format= 27f3183c..16915655 -- tools/z/keep.md   -> 0 bytes
git -C $FIX log  -m --diff-merges=first-parent --name-status -z --format= \
                 27f3183c..16915655 -- tools/z/keep.md                          -> "M\0tools/z/keep.md\0"
git -C $FIX diff --name-status 27f3183c 16915655 -- tools/z/keep.md             -> "M\ttools/z/keep.md"
python3 -I -B record.py --root $FIX --rev <k16-card> --no-battery               -> exit 0
# control k18: a non-merge commit (c4) also touches tools/z/keep.md in range
python3 -I -B record.py --root $FIX --rev <k18-card> --no-battery               -> exit 1
```

Any landing that resolves a conflict on the paths it claims untouched reads as empty.
Independently reproduced by seat `LabWindowProbe` on an *evil merge* (a change present in
neither parent): `window_empty -> (True, None)` while `git diff base..tip` shows the blob
changed (15 B first-parent, 31 B with `-m`) —
`.ufo/waves/round-47/w1/LabWindowProbe/receipts/evil-merge-transcript.txt`.
**What the claim would have to say:** clause 1's `window` derivation must be the
first-parent arm, not `--name-status` alone — "derived by `git log -m
--diff-merges=first-parent --name-status` over `A..B -- paths`".

### HIGH-2 — emptiness is free: a pathspec that names no path passes

`window_empty` never checks that the pathspec resolves at `rev` or is touched in the window,
and emptiness is monotone-decreasing in the pathspec, so naming a path that does not exist
(the `k04`/`k15` form) is a zero-cost forgery — including the honest-looking variant where a
rename removed the directory before the window (`k15`, exit **0**).

**What the claim would have to say:** "`pathspec` is non-empty and every entry resolves at
`--rev` (`git rev-parse --verify <rev>:<path>` or a non-empty `git ls-tree -r --name-only
<rev> -- <path>`); a pathspec with no tree entry at `--rev` is `unverifiable`, never empty."

### HIGH-3 — exemption laundering: a red window atom is repaired by a correction over the same pair with a different pathspec

`exempt()` (`record.py:330-339` at the freeze) compares only
`(cm.group(1), cm.group(2)) == atom["pair"]`. The pathspec is never compared, so a correction
may "supersede" an atom while stating a completely different, dead path.

```
# arm A: the atom is RED
-git log c2..c3 -- tools/y/keep.md` is empty.            -> exit 1, window mismatch
# arm B: same atom + `- corrects window round-9: empty in c2..c3 -- tools/none/`
                                                          -> exit 0, exempted: [window]
```

**All seven red window atoms that name a pair** (`k03`, `k05`, `k10`, `k13`, `k14`, `k18`,
`k20`) flip from exit 1 to exit 0 on arm B, on all three instruments. On the real card this
is `V3`: the round-46 `<tip>` placeholder is exempted by a correction stating
`empty in 58eb04b6..58eb04b6` — a degenerate window — and the counter exits **0**.

**What the claim would have to say:** clause 4 must bind the exemption on both dimensions —
"a `window` exemption covers only an atom whose pair *and* pathspec the correction states,
compared as sets, or an atom that names no concrete window *and whose round the correction
names*".

### HIGH-4 — free evidence: an undeclared amendment accepts a correction for a round that has no atom

`A3` (`2e4ae434`, in `tools/round-47/record.py`, **not** declared in
`plans/round-47-claims.md`, whose only amendment paragraphs are A1 and A2) switches off the
"exempts an atom that does not exist" check for any `seats`/`window` correction whose numeric
key is below the oldest round in scope. My `V5` adds one such line to the real card:

```
- corrects window round-3: empty in 58eb04b6..58eb04b6 -- tools/none/
```

| instrument | corrections | corrections_bad | exit |
|---|---|---|---|
| frozen `5017e1f` | 3 | 3 | 1 |
| A1–A4 `1e2c3102` | 3 | 0 | **0** |

The line exempts nothing, repairs nothing, names a round with no atom, and its window is a
degenerate pair over a nonexistent path — and it counts toward `corrections >= 2`. A2's own
paragraph in the claims file asserts "Every clause, threshold and kill rule is byte-identical
to A1"; A3 makes that sentence false at the revision the claim is measured at.

**What the claim would have to say:** either restore the existence check, or bind a
historical correction to the round's own dispatch file
(`files(".ufo/waves/round-<n>/w1-dispatch.json")` must exist) and declare A3 in the claims
file with its red-before control.

### MEDIUM-1 — a reversed pair, a degenerate pair, or a tip outside `--rev` all read empty

`k07` (`c3..c2`, whose forward `c2..c3` changes the path), `k08` (`c3..c3`) and `k09` (tip =
an orphan commit) all exit **0**. `window_empty`'s `rev` parameter is accepted and **never
used** (`record.py:90`), so the atom is not "run at `--rev`" as the claim states: nothing
requires `base` to be an ancestor of `tip`, `base != tip`, or `tip` to be reachable from
`--rev`.

**What the claim would have to say:** "`base` is a strict ancestor of `tip`, and `tip` is an
ancestor of (or equal to) `--rev`; otherwise `unverifiable`."

### MEDIUM-2 — C1's freeze arm is red at the landing revision, and the file holds two competing freeze definitions

```
python3 -I -B tools/round-47/exact.py --root $LANE --freeze <F> --rev 1e2c3102 --no-battery
  F = 5017e1f (original)                 -> exit 2  frozen_path_changed [plans/…, tools/round-47/, tools/round-47/record.py]
  F = 9018c53b (A1, "the declared freeze")-> exit 2  frozen_path_changed [plans/…, tools/round-47/, tools/round-47/record.py]
  F = 62e33f7d (A2)                      -> exit 2  frozen_path_changed [tools/round-47/, tools/round-47/record.py]
  F = 1e2c3102 (the revision itself)     -> exit 0  failing []
```

`plans/round-47-claims.md:9-10` defines the freeze as `git log --format=%H -1 --
plans/round-47-claims.md`; at the current head that re-derives **`62e33f7d`**, which is
itself exit 2. Line 27 declares the freeze to be the commit carrying the A1 paragraph
(`9018c53b`), also exit 2. Only a freeze placed at the last commit is green — and a freeze
declared after the last change cannot be violated, so the arm proves nothing about the
instrument it grades. Line 10-11 still says "Nothing in this file or in `tools/round-47/`
changes after the freeze" while the file changed twice (A1 +12 lines, A2 +9) and
`record.py` four times.

This also falsifies the claims file's **causal separability** sentence ("Either lands and
scores without the other"): `record.py` lives inside `tools/round-47/`, which is C1's frozen
set, so every C2 repair mechanically fails C1's freeze arm.

### MEDIUM-3 — the frozen instrument rejected the round's own prescribed repair (now repaired by A1; recorded for the freeze record)

`controls/ctl-c2-0-do-nothing.json` / the `Before` cell re-derives exactly as written at base
`13a9e9e1` (exit 1, 4 mismatches: round-45 seats `40+32` vs `40+36`, the round-46 `<tip>`
placeholder, `coverage 133/133` vs `138/138`, `depth 20/20` vs `23/23`; sha256
`53d81a3d27a4c0c832b334f0cc69aa97e414339574dc6b458f730630fd4d7e36`). But at the landing the
frozen instrument exited **1** on its own repair:

```
V1 (card as committed at 1e2c3102) with record.py@af666ce2:
  failing: ["corrections that do not re-derive: 1"]
  corrections_bad: [{"detail": "window pair names no atom in scope",
                     "line": "- corrects window round-46: empty in 332f4884..58eb04b6 -- tools/round-46 plans/round-46-claims.md"}]
```

`evaluate_text`'s `known_pairs` check required the correction's pair to already belong to
some atom, while the only window atom names no pair — so *no* window correction was legal and
C2's target was unreachable by construction. A1 removes exactly that check and V1 then exits
**0**. The correction's pair is genuinely empty at the tip
(`git log --name-status --format= 332f4884..58eb04b6 -- tools/round-46 plans/round-46-claims.md`
→ 0 bytes, exit 0), so the landed repair is *true* — but see HIGH-3: it is not *forced* to be.

### LOW — four smaller calibration defects

1. **Only the first pair on a line is graded** (`k12`): a sentence carrying
   `c1..c2` (empty) and `c2..c3` (non-empty) exits **0**; the second claim is never checked.
2. **A stated glob is silently truncated to its directory** (`k10`): `-- tools/x/*.txt`
   is extracted as `["tools/x/"]` because `[A-Za-z0-9._/ -]+` stops at `*`. The receipt
   prints the rewritten pathspec, so an honest claim can be falsified by a pathspec the card
   never wrote.
3. **Prose becomes an atom** (`k11`): any line containing "is empty" is a window atom; "The
   dangling list is empty." is `unverifiable` and red. Text written without a closing backtick
   (`k19`) also swallows the following words into the pathspec (`["tools/x/","is","empty"]`).
4. **A correction appended at the end of the file is silently ignored** once the corrections
   section is no longer last: at the tip `## Round 47` follows it, so `V5`'s appended
   `- corrects window round-3:` line yields `corrections 2` with no `corrections_bad` entry
   (`receipts/realcard-current.json`). A5 fixed this for the battery's own forgery, not for a
   lander writing a repair.
5. **`- corrects axes …` is unparseable** (`V4`): `CORR` is
   `^- corrects (seats|window|path|rev) …`, so the two axes correction lines in the landed
   section are silently dropped — `corrections` is 2 with or without them, and the two axes
   atoms are green only because the `## Owned axes` row itself was edited. Clause 3 specifies
   an `axes` correction form the code cannot read.

## 3. Current state of the two claims (as measured, not as claimed)

| measurement | revision | exit | detail |
|---|---|---|---|
| `record.py` current instrument, committed card | `31b092d1` | **0** | `failing []`, `mismatches []`, 2 corrections, 0 bad, battery 3/0, `atoms_by_class` window 2, exempted 1 |
| `record.py` frozen instrument, committed card | `31b092d1` | 1 | `corrections that do not re-derive: 2` |
| `exact.py`, documented freeze | `1e2c3102` | **2** | `frozen_path_changed` (see MEDIUM-2) |
| `exact.py`, freeze = rev | `1e2c3102` | 0 | `failing []` |

So C2 is green at the tip and C1 is green only under a freeze that cannot fail. The window
class contributes nothing to C2's greenness beyond the exemption of the round-46 placeholder.

## 4. Positive controls (what I could not falsify)

- `k00`: a genuinely empty window over a live path → exit 0 on every instrument (fixture is
  sound).
- The round-47 section's own load-bearing window — "the round's `git log --name-status
  --format= e856beb5..1e2c310295 -- corpus/knowledge PROVINCE.md` is empty, so no domain
  surface moved" — reproduces empty (0 bytes, exit 0, sha256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`), and stays empty when
  extended to the tip `31b092d1` (0 bytes). Both revisions resolve; `PROVINCE.md` exists at
  the tip. I could not falsify it, and the extended-window check means it is not a
  measured-at-an-older-revision claim.
- 7-hex abbreviations resolve and are accepted (k01) — the claim's `{7,40}` floor is honest;
  a 6-hex id is refused without resolution (k02), which is the conservative direction.

## 5. Residual risk and verification gaps (what I did not run)

- I did not test an **ambiguous** abbreviation (two objects sharing a 7-hex prefix): forcing
  one in a fixture is object-hash luck, not engineering. If it occurs, `git log` fails and the
  atom goes red — the safe direction — but I did not measure it.
- I did not test a window whose pathspec is a **glob that exists** (`tools/x/*.md` matching
  real files): extraction truncates to the directory, so it over-matches; the `k10` case shows
  the direction, not the whole space.
- I did not test **shallow clones** (`--depth`) where `base` is unreachable: `git log` fails
  there and the atom goes red; unmeasured.
- Submodules, case-insensitive filesystems and `.gitattributes` rename overrides were not
  exercised.
- I reviewed only the `window` class; `seats`/`path`/`rev`/`axes` correctness belongs to the
  seats that own them, and I did not audit the battery's other two forgeries beyond confirming
  `forgeries_green 0` at the tip.

## 6. Recommended clause text (minimum set that closes the measured forgeries)

Replace clause 1's `window` derivation and add two clauses:

1. derivation: `git log -m --diff-merges=first-parent --name-status` over `A..B -- paths`
   (closes HIGH-1);
2. reachability: `base` a strict ancestor of `tip` and `tip` an ancestor of `--rev`; a
   pathspec that resolves to no tree entry at `--rev` is `unverifiable`, and `pathspec == []`
   is a defect, not an unfiltered window (closes HIGH-2, MEDIUM-1, `k05`/`k06`);
3. exemption identity: a `window` exemption binds pair **and** pathspec (set equality); for a
   placeholder atom it must state **the same base the atom states** and must not lengthen or
   shorten the window, and it must name the round whose sentence it replaces (closes HIGH-0,
   HIGH-3);
4. declare A3 (or restore the existence check) and re-state A2's byte-identity sentence
   against the bytes actually measured (closes HIGH-4, MEDIUM-2).

## 7. Receipts (in `receipts/`)

| file | what it is |
|---|---|
| `matrix-frozen.json` | 36 attack runs, `record.py@5017e1f`, command + exit + stdout sha256 + UTC + receipt slice + ground truth |
| `matrix-amended.json` | same matrix, `record.py@1e2c3102` (A1–A4) |
| `matrix-current.json` | same matrix, `record.py@31b092d1` (A5–A7) — behaviour differences: none |
| `realcard-frozen.json` | `V1`–`V5` on the lane's committed card, frozen instrument |
| `realcard-amended.json` | `V1`–`V5`, A1–A4 instrument |
| `realcard-current.json` | `V1`–`V5` at the tip `31b092d1`, A6–A7 instrument (`V1` exit 0; `V3` exit 0 with a degenerate pair; `V5` is a no-op append at the tip, see LOW 5) |
| `narrow-0425224__58eb04b6.txt` | 52 bytes — the round-46 sentence read with its own base (`M attest.py`, `M gate.py`) |
| `narrow-332f4884__58eb04b6.txt` | 0 bytes — the window the landed correction actually states |
| `base.json` | the `Before` cell re-derived at `13a9e9e1` (4 mismatches, exit 1) |
| `card-at-current-cur.json`, `card-at-current-frozen.json` | tip `31b092d1` under both instruments |
| `exact-fz-*.json` | C1 freeze arm for each candidate freeze |
| `r47-window.txt`, `r47-window-ext.txt` | the round-47 no-domain-surface window, claimed and extended (both 0 bytes) |
| `probe.py`, `realcard.py` | the fixture builders; deterministic, rerun to reproduce every number above |

Reproduce from the freeze (the scratch tree was removed after these receipts were copied):

```
S=$(mktemp -d -p /fast/scratch/hyaku)            # never /tmp
mkdir -p $S/inst/tools/round-47 $S/inst/tools/round-46
git -C $LANE show 5017e1f:tools/round-47/record.py > $S/inst/tools/round-47/record.py
git -C $LANE show 5017e1f:tools/round-46/gate.py  > $S/inst/tools/round-46/gate.py
cp receipts/probe.py receipts/realcard.py $S/
git -C $LANE clone --shared --no-checkout $LANE $S/lane-copy   # read-only on the lane
HYAKU_SCRATCH=$S TMPDIR=$S python3 $S/probe.py                 # -> $S/matrix.json
```

Tooling: no installs — `git`, `python3` and the frozen modules only. Scratch root
`/fast/scratch/hyaku/kaidoku-r47/RevC2Window`, removed after these receipts were copied.
