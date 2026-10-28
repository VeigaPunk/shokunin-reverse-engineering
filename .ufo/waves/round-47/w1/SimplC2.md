# SimplC2 — R47-C2 findings (frozen counter `tools/round-47/record.py`)

Seat `SimplC2`, lane `kaidoku-shokunin`, round 47. Counter measured at the declared freeze
`07d2894eabe88c326e9036262f20ad02662c860d` (`record.py` sha256
`abf352573d156ed1388683c882e40cab9897f426b9448356993bf41bf37779e7`, 603 lines, identical at
`HEAD` and in the worktree). Lane tree untouched: `git status --porcelain -- tools plans
SKILL.md SCORECARD.md corpus LOG.md` empty before and after. The assigned questions
(`axes` necessity, `CORR_MIN`) and the keep/cut table are in `report.md`.

## F1 — every `- corrects axes` line is invisible to the counter; frozen clause 3's axes provision cannot fire

`CORR` (line 50) is

```
CORR = re.compile(r"^- corrects (seats|window|path|rev) (\S+):\s*(.+)$")
```

`corrections()` builds entries only from `CORR.match`, so `entry["class"]` is never `axes` and
**both** `if cls == "axes"` branches inside `corrects()` (lines 280–289 and 292–299) are
unreachable — the second one also reads an undefined name `atom`.

Measured at the freeze, on the landing card itself:

| observation | value |
|---|---|
| `- corrects` lines in `SCORECARD.md` at `07d2894e` | 4 (`:3669` seats, `:3672` window, `:3675` axes coverage, `:3677` axes depth) |
| `corrections()` output | `[('seats','45'), ('window','46')]` |
| `CORR.match` on those 4 lines | `[True, True, False, False]` |
| receipt | `corrections 2`, `exempted 1`, `corrections_bad []`, exit 0 (`at-07d2894e.json`, sha `d366b080…`) |
| card + invented `- corrects axes coverage: 999/999` | exit 0, `corrections 2`, `corrections_bad []` — a **false** axes correction is not red (`card-matrix.json` case `axes-correction-false-999`) |
| false axes atom + axes correction exempting it | exit 1, `mismatches 1 != 0` — an axes atom can never be exempted (`card-matrix.json` case `axes-atom-false-plus-axes-correction`) |

Consequences for the claim text:

- Clause 3's "an `axes` correction must state `<resolved>/<total>`" and clause 4's axes path are
  **unreachable**. Clause 3's `corrections >= 2` counts seats/window/path/rev lines only.
- The landing's two `corrects axes` lines are decoration: they neither exempt an atom nor get
  re-derived. The record therefore says "4 corrections" where the receipt says 2, and the two
  uncounted ones are the two that describe the axes rows.
- The dead code is not the intent, the parser is: with `CORR` widened to
  `(seats|window|path|rev|axes)` (scratch variant `mut/wide`) the freeze card parses 4
  corrections, all re-derived true (`corrections_bad []`, exit 0), and a forged
  `- corrects axes coverage: 199/199` goes red (`corrections_bad 1`, exit 1) while the atom stays
  exempted. One alternation word is the whole gap.
- Frozen bytes → **do not edit**. L1 either discloses an amendment (A6-shaped) that adds `axes`
  to the alternation, or states in the landing evidence that axes corrections are inert and that
  `corrections 2` counts 2 of the 4 written lines.

## F2 — the kill rule's "two corrected mismatches" is one at the measured revision

The claim says: "Deleting the corrections section restores the two corrected mismatches."
Deleting *only* the corrections block at `07d2894e` (keeping the round-47 section, so the
last-two window is unchanged) gives:

```
exit 1
mismatches ['window:46']
failing ['mismatches 1 != 0', 'corrections 0 < 2']
```

The round-45 seats atom is outside the last-two window at the landing, so its correction is
historical (A3) and exempts nothing — `exempted` at the freeze is `['window:46']` only. One
mismatch is restored, not two, and the second failing clause is the count, not a restored
atom. Deleting the *whole* tail from `## Record corrections` onward does show two mismatches,
but only because it also deletes the round-47 section and moves the window back to rounds
45/46 — not the experiment the claim describes.

## F3 — clause 2 is self-referential (see `report.md` Q1)

`CLASSES` is the counter's own tuple; the `mut/cut` variant (tuple without `axes`, no
`collect_axes`) exits 0 at the freeze, differing from the base receipt only in `atoms 41→39`
and the vanished `atoms_by_class.axes` (`cli-cut.json`, sha `e4b92ec1…`). No receipt field can
evidence "classes covers all five".

## Observation (low severity, permitted by the frozen wording)

One `window` correction exempts **every** placeholder-window atom in scope, not just its own
round: adding a `git log 0425224..<tip> -- tools/x/` sentence to the round-47 section is
exempted by the round-46 correction (`exempted ['window:46','window:47']`, exit 0). Clause 4
("an atom that names no concrete window") permits it and `EXEMPT_MAX = 3` bounds it, so this is
a bounded vacuity, not a forgery path.

## Evidence

All commands run with `TMPDIR=/fast/scratch/hyaku/kaidoku-r47/SimplC2`, `python3 -I -B`.
`manifest.json` carries command, exit code, sha256 and UTC mtime per receipt.

| receipt | command | exit | sha256 |
|---|---|---|---|
| `at-07d2894e.json` | `tools/round-47/record.py --root <LANE> --rev 07d2894e…` | 0 | `d366b080e0112a57…` |
| `at-13a9e9e1.json` | same, `--rev 13a9e9e1…` (base) | 1 | `53d81a3d27a4c0c8…` |
| `at-HEAD.json` | same, `--rev HEAD` | 0 | `f80d580576d2d851…` |
| `exact-at-freeze.json` | `tools/round-47/exact.py --freeze 07d2894e --rev 07d2894e --profile v3` | 0 | `fb40aaf4a67d73ef…` (`rule_blocks 24`) |
| `cli-base.json` | scratch copy of the counter, freeze | 0 | `d366b080e0112a57…` |
| `cli-dead.json` | same bytes minus `corrects()` 292–299 | 0 | `d366b080e0112a57…` (byte-identical) |
| `cli-cut.json` | `CLASSES`/`collect_axes` without `axes` | 0 | `e4b92ec1af2b8815…` |
| `cli-min1.json` | `CORR_MIN = 1` | 0 | `d366b080e0112a57…` |
| `cli-bypass.json` | axes derivation returns true | 0 | `d366b080e0112a57…` |
| `card-matrix.json` | `fixtures/harness.py`, 14 card cases | 0 | `c063c5b767501d4d…` |
| `probe2.json` | `fixtures/probe2.py` (parser domain, dead locals, kill rule) | 0 | `325ca0fed1668964…` |
| `selftest-base.txt` / `selftest-dead.txt` | `--root <LANE> --rev HEAD --selftest` | 0 / 0 | `8d722cc1fd0bad1c…` (identical, 10 cases 0 failures) |

Base-revision check (the before-control reproduces): `at-13a9e9e1.json` → 4 mismatches
(`seats:45` 40/32 vs 40/36, `window:46` `<tip>` unverifiable, `coverage` 133/133 vs 138/138,
`depth` 20/20 vs 23/23), `corrections 0`, exit 1 — matches `ctl-c2-0-do-nothing.json`.

Fixtures are reproducible: `sh fixtures/setup.sh <LANE>` rebuilds the five variants from the
lane's frozen counter plus `fixtures/patches/*.diff`, then `python3 -I -B fixtures/harness.py`
and `fixtures/probe2.py` regenerate the matrices. Run from a clean `fixtures/` this reproduced
both matrices byte-identically (`card-matrix.json` sha `c063c5b767501d4d…`, `probe2.json` sha
`325ca0fed1668964…`); the rebuilt variants and rerun receipts were then deleted so the lane
tree carries only the scripts and the patches. Nothing in `fixtures/` writes outside this
directory.

No tool was installed. Scratch `/fast/scratch/hyaku/kaidoku-r47/SimplC2` removed after copying
the receipts.
