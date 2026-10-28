# ScribeQuality — round 47, wave 1

Seat `ScribeQuality` (quality scribe, leaf — no subagent dispatch). Lane
`kaidoku-shokunin`; base `13a9e9e1`, first freeze `5017e1f7`
(`plans/round-47-claims.md` + `tools/round-47/`). Read-only on the lane tree; everything
below was measured, not re-run for decoration, and each value names the receipt that
carries its argv, exit code, stdout sha256 and UTC instant
(`.ufo/waves/round-47/w1/ScribeQuality/runs/manifest.txt`).

**The lane moved under the session.** HEAD was `3186f69b` when I started and `31b092d1` when
I stopped; the freeze became a series (`A1 9018c53b`, `A2 62e33f7d`, `A3 2e4ae434`,
`A4 1e2c3102`, `A5 07d2894e`, `A6 f54b3b6d`) and `corpus/lessons/round-47.md` grew while I
worked. Every measurement below is pinned to the revision in its own receipt; the final
batch is all at `a07537869cf37963dff559fc75271dfa8fbb2542` (2026-10-28T17:59Z), which is the
A6-pin commit and differs from `31b092d1` only in evidence files and prose.

## Deliverable

`.ufo/waves/round-47/w1/ScribeQuality/quality.md` — two candidate `corpus/QUALITY.md`
admission rows in the file's own shape (`| # | criterion | why (lesson) | supersedes |`),
next free numbers **88** and **89**, each with a red-before demonstration naming the round
and the receipt, plus the row numbers I checked for duplication (rows 1–87 read in full, the
Signals table 1–6, and the three appended correction blocks).

- **Row 88 — a forgery battery scores constructed artefacts, never attempted ones.** Forged
  bytes are hashed before scoring and must differ from the genuine artefact's; a no-op or
  unbuildable fixture is a battery defect (exit 1, named), never a `hole-measured`/`killed`
  increment; the pin that freezes the mutation set must cover behaviour (forged digests),
  not names.
- **Row 89 — a machine-read repair/exemption section is a closed grammar.** The classes the
  line pattern accepts, the classes the dispatcher implements and the classes the claim
  declares are one set asserted at run time; an unparsed line that opens with the section
  marker is a defect; every declared class carries a selftest case in which a false value
  keeps the counter red.

Nearest existing rows compared line by line and **not** duplicated: 40 (legitimate
look-alike), 67/69/70/71 (replay class sets, mutant triple — all assume a constructed
artefact), 77 (occurrence enumeration and duplicate rows), 87 (claim prose not implemented —
89 is the narrower mechanical instance plus the per-class selftest), 21/73 (a verdict is not
the compared object). If the L1 judges 89 redundant with 87, the surviving half is the
per-class selftest clause, which 87 does not state.

## Gates run (all read-only; receipts under `ScribeQuality/`)

| check | command | exit | value |
|---|---|---|---|
| C1 at the landing, declared freeze | `exact.py --freeze a0753786 --rev a0753786` | 0 | `met_target true`, `rule_blocks 24`, `rows 4`, `refs 9`, header exact, pins `interpreter 01a4bca7…`, `mutations 19a2166e…`, battery `4/4/0/1/0` (`c1-at-head.json`) |
| C1 at the landing, **first** freeze | `exact.py --freeze 5017e1f7 --rev a0753786` | **2** | `reason frozen_path_changed`; changed `plans/round-47-claims.md`, `tools/round-47/`, `tools/round-47/exact.py`, `tools/round-47/record.py` (`c1-at-head-first-freeze.json`) |
| C2 at the landing | `record.py --rev a0753786` | 0 | 50 atoms, `verified 48`, `exempted 2`, `corrections 2`, `corrections_bad []` (`c2-at-head.json`) |
| probe: no-op mutation | `probe-noop-mutation.py --rev a0753786` | 0 | battery tuple unchanged, `score()` exit 0 (`receipt-noop-mutation.json`) |
| probe: axes correction | `probe-axes-correction.py --rev a0753786` | 0 | 4 lines in the card, 2 parsed, `999/999` accepted (`receipt-axes-correction-unparsed.json`) |
| probe: window pathspec | `probe-window-pathspec.py --rev a0753786 --window 13a9e9e1..a0753786 --paths tools/round-47` | 0 | bogus path `atom_ok true`; backticked path `atom_ok false` (`receipt-window-pathspec.json`) |
| freeze re-derivation | `runs/freeze-rederivation.out` | — | `git log -1 -- plans/round-47-claims.md` → `62e33f7d`; `--diff-filter=A --reverse` → `5017e1f7`; six commits over frozen paths since `5017e1f7`; `grep -c freeze tools/round-47/record.py` → **0** |

Both counters were also re-run mid-session at `07d2894e` and gave the same verdicts; the
`a0753786` batch supersedes those files and is the one cited.

## Findings

### F1 — the C1 battery counts a mutation that mutates nothing, and `v2_green` absorbs it (NEW; corrects the lane's own R47-CL4)

`corpus/lessons/round-47.md` R47-CL4 routes: "*`mutations_sha256` is over the mutation names
… a behaviour change that keeps the names … is invisible to the pin, **though the battery's
`v2_green` count would move**.*" Measured, the count does **not** move:
`tools/round-47/exact.py:367-371` appends `{"error": "mutation was a no-op"}`, increments
**both** `forgeries_total` and `v2_green`, and `continue`s — the no-op lands on the flattering
side of the very tuple clause 9 compares (`exact.py:290` never reads
`fixtures[*].error`). With `substring-arm` replaced in memory by an identity mutation and the
frozen file otherwise untouched (sha256 `01a4bca7…`):

```
noop_battery  {forgeries_total 4, v2_green 4, v3_green 0, genuine_green 1, crash 0}
noop_score    exit 0, met_target true, failing []
```

So a re-pinned interpreter whose `substring-arm` body stopped mutating still reaches
`failing == []`: the round's own claim would certify three measured holes as four. Provenance:
`receipt-noop-mutation.json`; historical sibling instance `l1/scores/c2-at-L1.json`
(`forgeries_green 1`, the round's M47-2(a)) is the same class on the C2 side.

### F2 — the landing's two `- corrects axes …` lines are never parsed, and a false one is accepted (NEW)

`tools/round-47/record.py:50` — `CORR = re.compile(r"^- corrects (seats|window|path|rev) (\S+):…")`
— has no `axes` alternative, so `corrections()` never yields an axes entry; `corrects()`'s
axes branch at `:280` is unreachable, and its twin at `:292` is dead code referencing an
undefined `atom` (`NameError` if ever reached). At the landing:

| value | measured |
|---|---|
| `- corrects` lines in `## Record corrections — round 47` | **4** |
| lines the counter parses | **2** (`seats 45`, `window 46`) |
| `axes coverage: 138/138` → `axes coverage: 999/999` | counter still exit 0, `corrections_bad []`, `mismatches 0` |

The claims file's R47-C2 clause 3 sentence "an `axes` correction must state
`<resolved>/<total>`" is therefore a requirement no frozen line evaluates, and the two axes
correction lines the landing ships certify nothing. Receipts: `c2-at-head.json`,
`receipt-axes-correction-unparsed.json`.

### F3 — R47-C2 has no freeze guard at all, while the claims file says it has one (NEW)

`plans/round-47-claims.md:10-11`: "*Nothing in this file or in `tools/round-47/` changes after
the freeze: a change makes **both counters** exit 2 `frozen_path_changed`.*" `record.py`
contains **zero** occurrences of `freeze` (`grep -c freeze tools/round-47/record.py` → 0): its
CLI takes `--root/--rev/--json-out` only, it never calls `gate.freeze_state`, never refuses a
dirty frozen path, and its receipts carry no `freeze`/`frozen_path_changed` field
(`c2-at-head.json`; the L1's `l1/scores/c2-at-A4.json` likewise has `freeze: null`). Measured
at the first freeze, C1 refuses the landing as `frozen_path_changed` while C2 scores it green.

### F4 — the first freeze is six commits behind the landing (partly routed as R47-CL5; the discrepancy below is new)

`git log --format=%h 5017e1f7..HEAD -- plans/round-47-claims.md tools/round-47/` →
`9018c53b 62e33f7d 2e4ae434 1e2c3102 07d2894e f54b3b6d`. The claims file — the frozen rule per
the contract — carries **A1 and A2 paragraphs only**, still says "*the freeze is a series of
two*", and still states that nothing in the file or `tools/round-47/` changes after the
freeze; `corpus/lessons/round-47.md` declares the full seven-commit series and names A6
`f54b3b6d` as the declared freeze. Rules file and record disagree about the freeze the claims
were judged on. Receipt: `c1-at-head-first-freeze.json` (exit 2, four changed paths, the
counter itself among them), `runs/freeze-rederivation.out`.

### F5 — the claims file's freeze-re-derivation command returns the last touch, not the freeze (NEW)

`plans/round-47-claims.md:8-10` prescribes `git log --format=%H -1 -- plans/round-47-claims.md`
to re-derive the freeze. At `31b092d1` that prints `62e33f7d` (A2), while the first freeze is
`5017e1f7` and the declared freeze is `f54b3b6d`; the first-add form
(`--diff-filter=A --reverse`) prints `5017e1f7`. A `-1` walk is a last-touch walk, so any
amendment repoints the citation and `plans/round-47-claims.md@<freeze>` is false as soon as a
second commit touches the file. Receipt: `runs/freeze-rederivation.out`.

### F6 — a window atom's pathspec is free text: a path that does not exist reads as "empty", a backticked path reads as "not empty" (NEW)

`record.py` derives the pathspec with `re.findall(r"--\s+([A-Za-z0-9._/ -]+)", tail)` and then
runs `git log --name-status --format= A..B -- <paths>`; `git log` over a pathspec that matches
nothing prints nothing and exits 0. Atom-level verdicts (`collect`+`derive`, the exact
functions `evaluate_text` uses) for the same non-empty window `13a9e9e1..a0753786`, which holds
commits under `tools/round-47`:

| spelling | pathspec the counter used | verdict |
|---|---|---|
| `-- \`tools/round-47\`` | `[]` (backtick stops the regex) | `atom_ok false`, `empty false` — the **true** claim is red |
| `-- tools/round-47` + prose | `['tools/round-47','is','empty',…]` | `atom_ok false` (saved by the first real path) |
| `-- tools/round-95 does not exist` | all words, none tracked | **`atom_ok true`, `empty true`** — the **false** claim is verified |

Receipt: `receipt-window-pathspec.json`. The class is not instantiated on the landing's own
line (its paths are followed by a closing backtick), so this is a satisfiability finding, not
a defect in the landed value.

### F7 — the green C1 receipts pass `--freeze == --rev` (NEW, minor)

`l1/scores/c1-at-A2.json` and `c1-at-A4.json` carry `freeze == rev`, so `frozen_path_changed`
is empty by construction and the guard the round added cannot bite; my own
`c1-at-head.json` in that form is equally vacuous. The only measurement that exercises the
guard is the first-freeze run (F4, exit 2).

### F8 — the C1 "before" control describes a battery reason its receipt does not contain (NEW, minor)

R47-C1 "Before" says `.ufo/waves/round-47/controls/ctl-c1-2-freeze-battery-absent.json` shows
the battery "cannot even be built (`marker blocks 0`)". The receipt records
`battery: {"skipped": "artefact fails a structural clause first"}` — `evaluate()` never calls
`run_battery` because the structural clause fails first — and the string `marker blocks 0`
appears in no committed receipt. The claim is honest about the outcome and wrong about the
value (QUALITY 21/73 class).

### Confirmed positive (calibration)

At `a0753786` the C1 structural clauses are genuinely met — 24 craft blocks, the marked block
last and titled `24. `, exact header, 4 rows, 4 exact arm tokens, routed-id multiset exact,
`refs 9` all resolving with line selectors, `corpus/lessons/round-46.md` cited, both pins
matching (`c1-at-head.json`) — and C2 re-derives 48 of 50 atoms with two exemptions. Nothing
in this report disputes those structural results; F1–F3 are about what the batteries and the
repair grammar do not measure.

## Out of scope / not run

- Did not edit `corpus/QUALITY.md`, `SKILL.md`, `SCORECARD.md`, `plans/`, `tools/`, `LOG.md`,
  the fleet repo, `.ufo/state/`, `.ufo/watchdog.log`, or any sibling lane. The two rows are a
  draft for the L1 to land or reject.
- Did not run the counters at the amendments' intermediate revisions except where a receipt
  names them; did not re-run any L1 receipt.
- No pacman (host-wide pause); nothing installed, so nothing to record in the install log.
- `Exempted`/`corrections` slack was not attacked further (`exempted <= 3` had exactly 2 and
  `corrections >= 2` exactly 2); `exempt_keys` in `evaluate_text` is computed and never used —
  dead code, noted, not scored.

## Touched surfaces

Wrote only under `.ufo/waves/round-47/w1/ScribeQuality/` (three probe scripts, four receipt
JSONs, `runs/` with the command manifest, `quality.md`) and this report at
`.ufo/waves/round-47/w1/ScribeQuality.md`. Scratch `S=/fast/scratch/hyaku/kaidoku-r47/ScribeQuality`
was used for `TMPDIR` (battery fixtures; `run_battery` deletes its own) and removed before
yield; nothing was written under `/tmp`. Disclosure: one `importlib` load at 17:49Z, before I
adopted `python3 -I -B` for every run, may have refreshed the gitignored
`tools/round-47/__pycache__/*.pyc`; `git status --porcelain tools/round-47 plans SKILL.md
SCORECARD.md` is empty and all later runs used `-I -B`.

## Artifact paths

- `.ufo/waves/round-47/w1/ScribeQuality/quality.md` — the two candidate rows (88, 89)
- `.ufo/waves/round-47/w1/ScribeQuality/runs/manifest.txt` — argv/exit/stdout-sha256/UTC/rev per run
- `.ufo/waves/round-47/w1/ScribeQuality/c1-at-head.json` — C1 green (freeze == rev)
- `.ufo/waves/round-47/w1/ScribeQuality/c1-at-head-first-freeze.json` — C1 exit 2 at the first freeze
- `.ufo/waves/round-47/w1/ScribeQuality/c2-at-head.json` — C2 green, `corrections 2`
- `.ufo/waves/round-47/w1/ScribeQuality/receipt-noop-mutation.json` — F1
- `.ufo/waves/round-47/w1/ScribeQuality/receipt-axes-correction-unparsed.json` — F2
- `.ufo/waves/round-47/w1/ScribeQuality/receipt-window-pathspec.json` — F6
- `.ufo/waves/round-47/w1/ScribeQuality/runs/freeze-rederivation.out` — F3/F4/F5
- probe sources: `probe-noop-mutation.py`, `probe-axes-correction.py`, `probe-window-pathspec.py`
