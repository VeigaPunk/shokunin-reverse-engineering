# ScribeBlock — round 48, wave 1: block-25 draft, landing evidence, frozen-counter falsification

Seat: `ScribeBlock` (leaf; no dispatch). Scope: draft the `SKILL.md` craft
rule block 25 candidate for R48-C1, verify the round's C1 landing surface
end-to-end, and attack the frozen counters for vacuous clauses. Contract:
read-only on the lane tree; writes only inside
`.ufo/waves/round-48/w1/ScribeBlock*` and scratch.

## Axes (godspeed)

- **claim-coverage** — does the draft satisfy every frozen C1 clause at the
  declared freeze?
- **landing-mechanics** — can the artefact + registry repairs reach
  `met_target: true` end-to-end?
- **counter-honesty** — does any clause score a forgery green / a correct
  artefact red?

Frontier walked: drafted → simulated → falsified → measured end-to-end in a
fixture repo. All four axes moved; the last one exposed a kill-class defect.

## Deliverables (paths, all relative to the lane root)

- `.ufo/waves/round-48/w1/ScribeBlock/block.md` — the block-25 candidate, land
  verbatim.
- `.ufo/waves/round-48/w1/ScribeBlock/receipts/` — evidence:
  `c1-fixture-landed.json` (frozen counter, v3, on the landed fixture),
  `c1-fixture-landed-v2.json` (same, `--profile v2 --no-battery`),
  `ctl-c1-do-nothing-A4.json` (counter on the real lane at rev `663f30ee`,
  block absent), `skill-landed.md` (the simulated artefact, 1750→~1764
  lines), `simulate_landing.py`, `falsify.py`, `simulate-output.txt`,
  `falsify-output.txt` (sha256 `a4f06c32…`, `91b46984…`).

## Declared freeze — the prompt's hash is stale; the claims file rules

Prompt names `dc73587a8b9c1a23ba5a91dc7707ac7381a8b873` "(after disclosed
amendment A1)". The claims file itself declares the freeze as the commit
carrying its last amendment paragraph, and two further amendments landed:
- A3 `f3a7afc4` — `census_rederived_equal` compared an object with a list
  (never true; would have been unreachable at control time).
- A4 `0f06251b` — exit-0 classifier accepted a negated meaning
  (`0=not met` matched `\bmet\b`) and the row parser skipped indented rows.

**Declared freeze used here: `0f06251bf6a3a6964c715f67243d4df12e854258`**
(re-derived with `git log --format=%H -1 -- plans/round-48-claims.md` ≈ HEAD
`663f30ee`, plus the two evidence commits after A4). All pins below are at A4
bytes.

## Block-25 candidate (`block.md`) — clause-by-clause verification

| clause | status | evidence |
|---|---|---|
| 1 marker once, last craft block, `25. ` title | pass | fixture receipt: `marker_occurrences 1`, `block_is_last true`, `block_title "25. A verdict map binds "`, `rule_blocks 25` |
| 2 header `trigger \| v1 hole \| v2 arm \| exit`, 2 rows × 4 cells, exits ∈ {0,1,2} | pass | `header_ok true`, `rows 2`, exit cells `1`/`1` |
| 3 routed ids once each, arm keyed by id (`meaning`/`floor`) | pass | `routed_counts {R46-CL7:1, R47-CL10:1}`, `arm_by_id {R46-CL7:meaning, R47-CL10:floor}` |
| 4 arm cells ∈ {`meaning`,`floor`} | pass | `arm_tokens [meaning, floor]` |
| 5 `mutations_sha256` + four names named | pass | pin `25ce025f8b2be63a5122583191cbf7588db7dc2894c869fac2ab075a84f5c1ea` = `MUT_DIGEST`; names `gold-meaning, swapped-meaning, duplicate-meaning, permuted-arm` in prose |
| 6 `interpreter_sha256` | pass at A4 | pin `00f768c52a78f18a359c193cff08728a8dd8989e45121e7d496012d93d2649d0` = sha256 of `tools/round-48/meanings.py` (`sha256sum` run 2026-10-28T19:0xZ) |
| 7 ≥5 resolving citations incl. lessons-47 + ≥1 knowledge | pass | `refs 8`, `unresolved_citations []`, cited set covers `corpus/lessons/round-47.md` and `corpus/knowledge/2026-10-25-…-replay-gate-stop.md` |
| 8 registry meaning binding | reachable — needs L1 repair pass | see "Registry repairs required" |
| 9 battery 4/4/0/1/0 | **structurally impossible — see F0** | `battery genuine_green 0 != 1` |

The block carries its two HIGH routed defects in prose (R46-CL7 digit-binding,
R47-CL10 do-nothing artefact), names both arms (`meaning`, `floor`), both
pins, and a `Refs:` line with six cited paths over 8 HARD_REF occurrences.

## Registry repairs required for clause 8 (the landing's second half)

Live `SKILL.md` registry state at rev `663f30ee` (A4 counter semantics):
`registry_rows 40`, `census_paths 42`, `census_rederived_equal true`,
`meaning_rows_failed 16`, `registry_missing 2`.

**Missing rows** (must be added — they are the round's own tools):
- `tools/round-48/meanings.py`
- `tools/round-48/record2.py`
Proposed cells are in `simulate_landing.py` `NEW` (already exercised green).

**16 verdict maps failing `meaning_classes`** — minimal repairs proven green
in the simulation (each is a class-token insert that preserves the row's own
claims; full replacement cells in `simulate_landing.py` `REPAIRS`):

| path | failure | minimal repair |
|---|---|---|
| tools/round-41/c1-extra.py | seg0 no success token | `0=met, all three bindings…` |
| tools/round-41/c2-controls.py | seg0 no success token | `0=clean, no control reaches n/n…`; seg1 `1=not met, a control…` |
| tools/round-41/fetch-vendor.py | seg0 | `0=met, every external carrier…` |
| tools/round-41/local-source-gate.py | seg0 | `0=met, every out-of-lane row…` |
| tools/round-41/mk-l-carriers.py | seg1 | `1=no verdict: no explicit path…` |
| tools/round-42/c1-run.sh | seg1 | `1=no verdict: an unguarded command…` |
| tools/round-42/c2-controls.py | seg0 | `0=clean, no control reaches full score…` |
| tools/round-42/heldout-gen-v4.py | seg2 | `2=unevaluable, argparse rejected…` |
| tools/round-42/indep-eval-v4.py | seg0 | `0=wrote one record…` |
| tools/round-42/sqfs3-oracle.py | seg0 | `0=ok, producers agree…` |
| tools/round-42/unblob-logtee.sh | seg0 | `0=ok, the wrapped unblob…` |
| tools/round-43/c1-counter.py | seg0 | `0=met, met_target true,…` |
| tools/round-43/c2-score-r43.py | seg0 | `0=met, all 13 checks…`; seg1 `1=not met, at least one check false` |
| tools/round-44/c1-run.sh | seg0 | `0=clean, every carrier ran…` |
| tools/round-46/census.py | seg0 | `0=ok, census computed…`; seg1 `1=no verdict: an unhandled exception…` |
| tools/round-46/gate.py | seg1 | `1=no verdict: running gate.py as a program refuses…` |

`heldout-gen-v4.py` seg2 originally read `2=argparse rejected the argv` — the
only cell whose *digit* lacks its unevaluable token (it had neither
`could-not-evaluate`/`unevaluable`/`usage`/`error`/… in the segment head).

## Landing simulation (in-memory, before fixture)

`simulate_landing.py` inserts `block.md` before `## Config custody…`, applies
the 16 repairs row-scoped, appends the two rows, then scores genuine +
4 mutations:
`GENUINE exit 0`, `registry_rows 42 census 42 rederived True meaning_failed 0`,
battery `{forgeries_total 4, v2_green 4, v3_green 0, genuine_green 1, crash 0}`
— `BATTERY_MATCH True`. (`simulate-output.txt`, sha256 `a4f06c32…`)

## End-to-end fixture run (the strongest evidence)

Fixture `tmp.UsF7rRmP9Y` (git repo under scratch):
- commit `26de8b39…` = real `plans/round-4[1-8]-claims.md` + `tools/round-4[1-8]/` + cited corpus files + stub SKILL.md — passed as `--freeze`;
- commit `4c157954…` = same + landed `SKILL.md` (`skill-landed.md`).

`python3 -I -B tools/round-48/meanings.py --root $D --freeze 26de8b39 --rev
4c157954` → **exit 1**, receipt `c1-fixture-landed.json`: every content clause
green (`block_is_last`, `header_ok`, `routed_counts`, both pins match,
`refs 8`, `unresolved_citations []`, `registry_rows 42 == census_paths 42`,
`census_rederived_equal true`, `meaning_rows_failed 0`, all four forgeries
`v2_exit 0` / `v3_exit 1`) — and `failing: ["battery genuine_green 0 != 1"]`.

`--profile v2 --no-battery` on the same fixture → **exit 0**
(`c1-fixture-landed-v2.json`).

## F0 — KILL FINDING: `genuine_green` is structurally 0; R48-C1 is un-meetable at the A4 freeze

`run_battery` (`meanings.py:491-528`) scores the *genuine* artefact not against
the full rev tree but against `_fixture_files` (`:468-488`) — a fixed 6-path
map (`CLAIMS`, `SELF`, `CENSUS`, `CENSUS_TOOL`, `MUST_CITE`, one knowledge
file) plus only paths the block itself cites. Inside `score`, clause 8 calls
`census_rederive(files)` which `exec`s `census2.census_text(read)` over that
map: every claims file other than `round-48` reads `None`, every census path
other than the six reads `None`, so `derived["paths"]` can only ever be a
2-path subset while `doc["paths"]` is 42. `census_rederived_equal` is false
inside the battery **for any possible artefact** → `genuine_green` is
constantly 0 → clause 9's `genuine_green 1` fails → the counter always exits 1.

Same bug class the L1 already amended three times (A3 fixed `derived == list`;
this is `derived` computed over a file map that cannot see the census).
Reproduction: `receipts/c1-fixture-landed.json` `battery.fixtures[*].v3_failing`
all carry `committed census2.json does not equal a fresh derivation` and
`battery.genuine_exit 1` — while the genuine run against the real `files()`
(clause 8 proper, `receipt.genuine` pass) reads `census_rederived_equal true`.

Minimal repair (one line, reported — not applied, frozen):
`run_battery`'s `files` lambda should fall back to `gate.show(root, rev, p)`
for paths not in `base`, i.e. `files = lambda p: base.get(p) if base.get(p)
is not None else gate.show(root, rev, p)` — or `_fixture_files` must populate
every census-relevant path. Until an A5 lands, **the interpreter pin in
`block.md` must be re-derived at landing time** (it will change again).

## Falsification probes — five residual vacuities (each exit 0 demonstrated)

Run as `falsify.py` over the simulated landing (`falsify-output.txt`,
sha256 `91b46984…`):

- **F1 — the meaning binding reduces to a vocabulary test.** Replacing a
  registry verdict with `0=met; 1=not met; 2=unevaluable` (contentless bare
  tokens) scores exit 0. R46-CL7's "meanings" are keyword-in-segment, not
  meaning-vs-implementation. The `BANANA` guard only rejects its three literal
  placeholder words — a "synonym banana" passes.
- **F2 — segment polarity is guarded on seg0 only.** `1=not met or
  could-not-evaluate…; 2=unevaluable or a violation…` (each segment naming a
  foreign class) scores exit 0. A4 added `NEGATED` for seg0 only; segs 1/2
  may name multiple classes freely.
- **F3 — `refs` counts occurrences, `cited` distinct paths.** Clause 7 needs
  `refs >= 5` and the two must-cites; three extra duplicates of the same
  citation pad the count green (R47-CL7's identical hole, carried over).
- **F4 — `mutations_sha256` covers function bodies, not helper closures.**
  `_mut_digest` hashes each mutation's `inspect.getsource`, but the mutations
  mutate through module-level helpers (`_rewrite_registry`,
  `blocks_of`/`rewrite_rows`). Gutting `_rewrite_registry` to a no-op leaves
  the pinned digest identical AND the battery on-target: three of the four
  "forgeries" become silent no-ops, `forgeries_total` still counts 4, v2
  still scores them green, v3 red for unrelated reasons —
  `{4,4,0,1,0}` produced by a battery in which only `permuted-arm` actually
  mutates. R47-CL4's body-pin still misses the closure.
- **F5 — the routed-id scan reads cell 0 only.** `ID.findall(r[0])`: a second
  routed id smuggled into a `v1 hole`/`v2 arm`/`exit` cell is invisible to
  `routed_counts` and `arm_by_id`.

None of these currently make the landed artefact dishonest (my block uses
none of them), but they are the next round's routed-defect class, verbatim.

## Additional observations

- `SKILL.md` already contains `<!-- instrument-registry v2 -->` at L1705 /
  `<!-- /instrument-registry -->` L1750 — the section the clause-8 binding
  targets. Registry row header at `:597-599` of `meanings.py` selftest gives
  the 7-cell column order used: `path | purpose | verdict | selftest |
  pinned | write | owner`.
- `craft_section` requires literal `## Queue-drain craft ` with trailing
  space; `blocks_of` splits on `^- **`. The block must keep `- **25. …**`
  form exactly (lands before `## Config custody` at SKILL.md:643).
- `check_refs` exempts `SELF` (`tools/round-48/meanings.py`) from the
  line-selector requirement but still counts it as a ref — the block
  exploits this (bare interpreter citation) deliberately.
- Prompt-vs-file drift: prompt says freeze `dc73587a` (A1); the file and the
  commit chain say A4 `0f06251b`. I followed the file.
- `corpus/lessons/round-48.md` and `corpus/SOURCES.md` appeared modified /
  untracked mid-session (L1's own work — not mine; left untouched).
- `controls/ctl-c1-0-do-nothing.json` at A4 bytes predates my run; my
  `ctl-c1-do-nothing-A4.json` reproduces it at rev `663f30ee`
  (exit 1, marker absent, battery skipped).

## Commands (exact, citable)

| command | exit | note |
|---|---|---|
| `git log --format=%H -1 -- plans/round-48-claims.md` | 0 | `663f30ee` (A4 inside) |
| `sha256sum tools/round-48/meanings.py` | 0 | `00f768c5…` (interpreter pin) |
| `python3 -c 'import meanings; print(meanings.MUT_DIGEST)'` | 0 | `25ce025f…` |
| `python3 -I -B tools/round-48/meanings.py --selftest` | 0 | `cases=18 failures=0` |
| `python3 -I -B tools/round-48/meanings.py --root . --freeze 0f06251b… --rev HEAD --json-out …ctl-c1-do-nothing-A4.json` | 1 | do-nothing, marker absent |
| `python3 simulate_landing.py` | 0 | all-clause green + battery on-target |
| `python3 falsify.py` | 0 | 6 probes, all exit 0 on weakened artefact |
| `python3 -I -B … --root $D --freeze 26de8b39… --rev 4c157954…` | 1 | F0: `battery genuine_green 0 != 1` |
| same + `--profile v2 --no-battery` | 0 | ported profile green |

All ran with `TMPDIR=HYAKU_SCRATCH=/fast/scratch/hyaku/kaidoku-r48/ScribeBlock`
(non-/tmp, per R45-CL20). No installs (no tool needed). No git mutations
outside the fixture repo `$D` (its `rev-parse --show-toplevel` asserted
before every commit).

## Out of scope (by contract)

- `SCORECARD.md` / R48-C2 `record2.py` verification — other seats; not read
  beyond the docstring needed for the registry-row text.
- No edits to `SKILL.md`, `plans/`, `tools/`, `corpus/`, LOG — the repairs
  table above is *evidence for the L1*, not a landed change.
- Scratch `$S` retained until report copy is confirmed; fixture repo
  `tmp.UsF7rRmP9Y` carries the two landed commits `26de8b39`/`4c157954`.

## Known limits of this report

- The `interpreter_sha256` pin is at A4 bytes; if the L1 lands an A5 (F0
  makes one necessary), re-run `sha256sum tools/round-48/meanings.py` and
  update `block.md` before landing — M47-7's coupling defect, stated again.
- The registry repairs are minimal-token; an L1 may prefer fuller rewrites.
  All 16 + 2 rows are proven sufficient (simulation + fixture), not
  individually necessary.
- F1–F5 are demonstrated on `score()` in-memory; none is a frozen-file
  modification — they are residual *clause* holes for the next round's
  routing ledger.
