# R46W1ScribeBlock23 — rule block 23 draft (R46-C1 landing evidence)

Seat: scribe, round 46 wave 1, lane `kaidoku`. Deliverable drafted, not landed: the L1 pastes.
All git reads were read-only; every write is inside `.ufo/waves/round-46/w1/R46W1ScribeBlock23/`.

## Deliverable

`block.md` — 33 lines, 6,290 bytes, sha256 `067e39dac8338d998b842ce55d91631cd8de87b58c78df8d8ca2899aad7defa8`.
Machine receipts: `receipts.json` (12 records, command + exit + stdout sha256 + UTC each).

The draft is not a paraphrase of the landed block; it was written from the two frozen
predicates and the thirteen routed lesson rows, then measured against the counter's own
`score()` (R8). It differs from the block now in `SKILL.md`: 16 refs instead of 9, and every
ref resolves at both the first freeze and the current freeze.

### (a) Title line — 16 words, begins `- **23. `

```
- **23. A measure is only evidence when its own forgeries fail.** <!-- freeze-integrity-table v2 -->
```

### (b) Table — exact header, thirteen data rows

Header is exactly `| trigger | v1 hole | v2 arm | exit |`. Every row is four cells; no cell
carries a literal `|`; every exit cell is `1` or `2`. Rows and ids, in file order:

| id | arm token(s) named | exit |
|---|---|---|
| R45-CL2 | presence | 1 |
| R45-CL6 | merge (+ blob) | 2 |
| R45-CL7 | marker | 1 |
| R45-CL9 | refs + rows | 1 |
| R45-CL13 | pin + rows + battery | 1 |
| R45-CL14 | header + marker + presence | 1 |
| R45-CL15 | dirty + restored | 1 |
| R45-CL18 | pathspec + restored | 1 |
| R45-CL19 | blob | 2 |
| R45-CL20 | output + header | 2 |
| R45-CL22 | output | 2 |
| R45-CL23 | commit | 1 |
| R45-CL24 | pin | 1 |

All fourteen vocabulary tokens are used at least once (`tokens_unused: []`), each routed id
appears exactly once in cell 0 (`ids_unique: 13`).

Exit semantics applied, not copied: 1 where the clause runs and fails, 2 where the instrument
can only decline to evaluate — a merge-introduced touch and a squash-folded restore are both
`frozen_path_changed`/unknowable rather than "not met", the refused scratch root and refused
`--json-out` target produce no verdict at all.

### (c) Refs — fifteen citations with selectors, verified at two revisions

`corpus/lessons/round-45.md` (eleven ranges: `77-79`, `90-97`, `98-101`, `107-120`, `142-159`,
`160-172`, `173-183`, `197-211`, `212-217`, `224-234`, `235-247`), `plans/round-46-claims.md`
(three ranges: `37-109`, `110-167`, `168-177`), and
`corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md:36-48`.
Every range was checked with `1 <= start <= end <= line_count` against **both**
`31820472784284727546808acc31b3ea1e73919b` and the current freeze `04252247` (R7: all resolve,
both revs). Each round-45 range starts on its `- **R45-CLn` row and ends on the line before the
next row (R45-CL24 ends at EOF, 247).

### (d) Pin sentence

The block carries, in one sentence: `S142`, the path `tools/round-46/attest.py`, and
`sha256:e6c44d2d57dbbc65ed8d14b642a6101eea264b05faf68c25606525b8fe532346`.

**That is not the value this seat's spec told me to compute.** See F1 — the spec's command
(`git show 3182…:tools/round-46/attest.py | sha256sum` → `dd1e7df1…`) is red under the frozen
predicate at every revision that can be scored. The draft records both hashes, the measured-freeze
one first so `PIN.search()` reads it, with the freeze chain named in prose.

## F1 (HIGH) — the freeze in the seat spec is not the scorable freeze

The claims file defines the freeze as the commit that first contains `plans/round-46-claims.md`
and `tools/round-46/`, re-derived by `git log --format=%H -1 -- plans/round-46-claims.md`. That
command returns `31820472784284727546808acc31b3ea1e73919b` (R5) — and cannot see the round's later
instrument-only commits, because they touch no file under `plans/`. Measured:

```
git -C <lane> log --oneline --name-status 31820472..HEAD -- tools/round-46/ plans/round-46-claims.md
50862e4a  M tools/round-46/{attest.py,gate.py,registry.py}   "complete the freeze … declared as
                                                              the authoritative freeze"
65678df0  M tools/round-46/attest.py                          "the freeze is the instrument that
                                                              can actually be scored"
04252247  M tools/round-46/registry.py                        F4 (v1 registry profile)
```

`attest.py` bytes per revision (`git show <rev>:tools/round-46/attest.py | sha256sum`, R1–R4):

| revision | sha256 |
|---|---|
| `31820472` (claims-file derivation, seat spec) | `dd1e7df1682c5b63ed9f5f75a3aff26c7914e6d41885e5e2da717aa91165d0fb` |
| `65678df0` | `e6c44d2d57dbbc65ed8d14b642a6101eea264b05faf68c25606525b8fe532346` |
| `04252247` | `e6c44d2d…532346` |
| `HEAD` (`1e32827b`) | `e6c44d2d…532346` |

Consequences, measured with the frozen library `gate.freeze_state(root, <freeze>, HEAD)`:

- freeze `31820472` → **exit 2** `frozen_path_changed` on `tools/round-46/`, `attest.py`,
  `gate.py`, `registry.py` (R9c).
- freeze `65678df0` → **exit 2** on `tools/round-46/`, `registry.py` (R9b).
- freeze `04252247` → **exit 0**, no change (R9a). HEAD's last commit touching `tools/round-46/`
  is `04252247`, so that is the only freeze candidate clean at HEAD.

So a block pinned to `dd1e7df1…` cannot be scored: at any rev the freeze arm permits, the pin
clause fails. Verified directly — the same `block.md` with the measured-rev pin swapped to the
first-freeze value scores `exit 1, ["interpreter sha256 pin does not match the bytes at rev"]`
at `31820472`, and `exit 0, failing []` at `65678df0`, `04252247`, `17a72375`, `1e32827b` (R8).
The landed block in `SKILL.md` already carries `e6c44d2d…` (A2 commit `6e018068`, "re-pin block
23 to the measured freeze's interpreter bytes"), so the draft agrees with the landed state and
not with the seat prompt.

Reconciliation for the L1 (I did not edit the frozen file): cite the round as
`plans/round-46-claims.md@04252247`, record the three-commit re-freeze chain in the round report
(commit messages are currently the only place it exists), and carry the definition defect
— "first commit containing the file" vs. "instrument bytes that can be scored" — as a routed
item for round 47. Until then the freeze's identity is unverifiable from the frozen bytes.

## F2 (MEDIUM) — the freeze argument is caller-supplied and unconstrained

`gate.freeze_state` takes `freeze` as given (`gate.py:144`), derives the frozen *set* from the
claims file at **rev**, not at freeze (`gate.py:63-89`), and never checks that `--freeze` equals
the claims file's own derivation. Any ancestor at or after the last instrument commit therefore
yields exit 0. That is how `04252247..04252247` scores clean while the frozen definition names
`31820472`. No clause of R46-C1 or R46-C2 binds it; I report it, and the draft's rows say
nothing stronger than the claim does.

## F3 (LOW) — the landed block's refs are revision-dependent

`corpus/lessons/round-46.md` does not exist at `31820472` (it is created after the freeze). The
landed block cites it twice, so scored at the first freeze it fails with
`unresolved or unvalidated citations: 2` plus the pin mismatch (measured, read-only, same
harness, 9 refs). At `04252247`/HEAD it is green (9 refs, `failing []`). The draft deliberately
cites no post-freeze file, so it is green at both — 16 refs, no unresolved citation at either
revision. This is a portability improvement, not a claim that the landed block is wrong at the
measured revision.

## Coverage / depth / calibration

- Coverage: all thirteen routed ids, one row each, exact header, four cells, exits in `{1,2}`,
  all fourteen vocabulary tokens, fifteen resolving line-selected citations, `S142`, the
  interpreter path and a single 64-hex pin.
- Depth: each "v1 hole" cell names the actual defect mechanism, not the symptom — e.g. CL18
  "the log scope and the freeze scope were different sets" (the pathspec boundary, lesson
  `:197-206`), CL15 "the flag replaced the scope" (`:173-183`), CL23 "the comparison was between
  quoted strings and real paths" (`:230-234`). CL20 names both halves and states that the
  eight-column registry gap stays routed rather than claiming it closed — the round-46 house
  header is seven cells (`registry.py:41-42`).
- Calibration: the draft is measured by the frozen instrument's own `score()`, not described.
  What that does **not** establish: the nine-forgery battery, `--selftest`, and the registry
  counter were **not run** by this seat — they are the L1's scoring step, and no battery number
  is claimed here.

## Receipts (`receipts.json`)

| id | command (abbreviated) | exit | stdout sha256 | UTC |
|---|---|---|---|---|
| R1 | `git show 31820472:tools/round-46/attest.py \| sha256sum` | 0 | `0b1f9f76…258d6` | 17:02:09Z |
| R2 | `git show 65678df0:…/attest.py \| sha256sum` | 0 | `5689fce3…84d9e` | 17:02:09Z |
| R3 | `git show 04252247:…/attest.py \| sha256sum` | 0 | `5689fce3…84d9e` | 17:02:09Z |
| R4 | `git show HEAD:…/attest.py \| sha256sum` | 0 | `5689fce3…84d9e` | 17:02:09Z |
| R5 | `git log --format=%H -1 -- plans/round-46-claims.md` | 0 | `9757eb4b…25d7` | 17:02:09Z |
| R6 | `git log --name-status 31820472..HEAD -- tools/round-46/ plans/…` | 0 | `2fee5a30…2aed` | 17:02:09Z |
| R7 | citation range check, 15 refs × 2 revisions | 0 (all resolve) | — | 17:02:09Z |
| R8 | `attest.score(block.md substituted for block 23 in HEAD SKILL.md)` at 5 revs | 0 | `b2f59656…a65c` | 17:02:10Z |
| R9a | `gate.freeze_state(04252247, HEAD)` | 0 | `f843b722…4975` | 17:02:10Z |
| R9b | `gate.freeze_state(65678df0, HEAD)` | 0 (verdict `{"exit": 2}`) | `dc545f85…1d63` | 17:02:10Z |
| R9c | `gate.freeze_state(31820472, HEAD)` | 0 (verdict `{"exit": 2}`) | `53ab2af5…4dd2` | 17:02:10Z |
| R10 | `sha256sum block.md` | 0 | `067e39da…defa8` | 17:02:10Z |

R8 verdicts: `04252247` → 0, `1e32827b` → 0, `65678df0` → 0, `17a72375` → 0, `31820472` → 1
(pin only). Rows 13, refs 16, `rule_blocks` 23, header exact, `marker_occurrences` 1,
`block_is_last` true in every post-F3 run.

## Surfaces touched

- Wrote: `.ufo/waves/round-46/w1/R46W1ScribeBlock23/block.md`,
  `.ufo/waves/round-46/w1/R46W1ScribeBlock23/receipts.json`, this report.
- `git status --porcelain` for the seat path shows only `?? .ufo/waves/round-46/w1/R46W1ScribeBlock23/`.
  No tracked file, frozen path, sibling lane or fleet-root file was modified.
- No installs; nothing written under `/tmp`; scratch `/fast/scratch/hyaku/kaidoku-r46/R46W1ScribeBlock23`
  removed after `receipts.json` was copied out.

## Out of scope (not done, deliberately)

`SKILL.md` (L1 lands it), the registry rows (other seats), the nine-forgery battery and both
counters' scoring runs, any commit. F1/F2/F3 are reported, not fixed — the files are frozen.
