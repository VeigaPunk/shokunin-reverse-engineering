## Round 65 — the `.jsc` route under a complete closure (verified); the coverage recipe's stale premise (honest stop)

Two claims, distinct axes, causally separable. Base `c99e907cb5576c13a7b22755d776b356fdfc1752`;
declaration `4a699a3fbd4073464521540c9e68974ed9939be5` (both instruments committed before the claims file,
QUALITY #33); operative freeze `922ed89f42bed28173035f3faaf705e0cb70abb7`. Neither instrument changed after
the freeze (the R29 pre-flight gate at the freeze: exit 0, audited 40, clean 19, round-65 not flagged).

| claim | axis | type | predicate (frozen) | before → after | verdict |
|---|---|---|---|---|---|
| R65-C1 | depth | capability acquisition | R65-C1 is verified iff (i) the frozen closure manifest matches every one of its entries (count and sha256) with no Python bytecode cache present before the first run, (ii) all 18 runs reproduce the frozen predicted label of their cell (dump, view8, check), and (iii) the after-run toolchain census equals the before-run census. | round 64: 9 pinned objects, a toolchain the run wrote into (F1/F2) → round 65 executed run: 30-entry closure matched, cache-free at the check, 18 of 18 labels, census equal (exit 0) | **verified** (two counter-boundary defects disclosed, M65-5) |
| R65-C2 | calibration | capability acquisition | R65-C2 is verified iff the repaired stem-keyed recipe reports, over the repository at the measured revision, `mismatches == 0` with `mapped > 0`, while the superseded date-limited recipe on the same revision reports a non-zero `population_dropped` naming the files it hides. | stem recipe 144 of 144 at the base, 145 of 145 at the landing, mismatches 0, exit 0; the superseded recipe A at the base reports 142 mapped of 144, **names** both files as missing and scores 9.86 — it has no `population_dropped` field, and the instrument's date mode that emitted one is not recipe A | **unprovable** (naming clause not emitted; before-arm misdescribes recipe A — honest stop, M65-2/M65-4) |

**R65-C1 receipts.** Counting command
`python3 -I -B tools/round-65/jsc-closure-matrix.py --probe .ufo/waves/round-64/inputs/probe-electron.jsc --work <scratch> --out <receipt>`:
wave run `.ufo/waves/round-65/w1/ExecMatrix/matrix-run.json` — exit 0, `runs_matching 18`, `runs_total 18`,
closure `ok true` with `entries 30`, `cache_present []`, `missing []`, census `{"equal": true, "added": [],
"removed": [], "changed": []}`, label histogram 6 × `dump-ok, view8-ok, node-fail`, 3 × `dump-exit-139`,
9 × `dump-exit-134`; instrument sha256 unchanged before/after (`79a4dca4…922c6`). Do-nothing arm
`.ufo/waves/round-65/l1/c1-before-donothing.json` exit 1, `runs_matching 0`, byte-identical to the wave's
control copy (`.ufo/waves/round-65/w1/ExecControls/donothing.json`, `cmp` exit 0). Controls: selftest 34
cases; one-byte pin mutation → exit 2 naming only `d8-14.8.178.1/snapshot_blob.bin`; planted
`__pycache__/x.pyc` → exit 2, removal → exit 0; census arms 0/1 (all `.ufo/waves/round-65/w1/ExecControls/`).
Independent re-derivations: the scout re-hashed all 30 entries with a second implementation
(`.ufo/waves/round-65/w1/ScoutFrontier/manifest-recheck.md`, 30/30 aligned) and the sentinel did the same
(`.ufo/waves/round-65/w1/SentinelProvenance/report.md`, 27/27 + 3/3, cache-free; verdict `provenance-open:
P1,P2,P3` — bytes stable, origins of the d8 binaries and probe not provable from bytes on this host). Review
(`.ufo/waves/round-65/w1/ReviewerClosure/review.md`): Q1–Q6 closed, nine advisory findings, none blocking;
round-64 F1 and F2 both repaired. Mutation: `.ufo/waves/round-65/w1/MutClosure/mutants.md` — 6 mutants,
6 killed, 0 survived (M1/M4/M6 are invisible to the selftest and killed by CLI arms). Counter-boundary
defects disclosed and left for a new freeze: the cache-free check runs before `python_probe` while the
before-census is taken after it (critic C1-F1), and the entry count is emitted but never asserted
(C1-F2, `evidence/trunc-manifest-29.json`). The executed run is clean (the probe runs with `-B` and the
env); the counter would not have caught a probe write.

**R65-C2 receipts.** The superseded recipe A, run verbatim at the base, prints `knowledge_files 144`,
`mapped 142`, `missing` = `jsc-mapper-cli-contract` and `jsc-mapper-release-inventory`, `coverage_score 9.86`
(critic `C2-F1`, `.ufo/waves/round-65/w1/CriticClaims/evidence/recipeA-at-base.json`; reproduced by the L1).
The stem recipe at the same base: 144/144, mismatches 0, exit 0
(`.ufo/waves/round-65/l1/c2-after-stem-at-base.json`), and 145/145 at the landing
(`.ufo/waves/round-65/l1/c2-stem-at-landing.json`). The instrument's `date` mode is **not** recipe A: it
filters the population and emits a `population_dropped` count recipe A never had
(`.ufo/waves/round-65/l1/c2-before-date.json`: population 142, dropped 2) — the critic's C2-F2 and M65-2.
The claim's naming clause is also unimplemented (C2-F3, M65-4). **Unprovable on both grounds; no post-freeze
edit, no narrowed target.** The instrument lands and is registered; **no capability row** is entered.

**Axes.** depth improves for the closure (round-64's blocking F1/F2 repaired and the route reproduced under
a complete closure); calibration is **not** claimed improved — the C2 move stops, and the honest stop plus
the corrected premise is the calibration evidence this round carries. coverage unchanged (no surface
widened; the map gained one entry, not a new kind of surface). No axis harmed: owned-axes rows byte-equal
base→record, PROVINCE unchanged, LOG additions only.

**Sources.** `SOURCES.md` 172 → 173 rows (S266 admitted; mined 163 → 164, rejected 9 → 9), 19 standing W04 at
both census ends. Lesson `corpus/lessons/round-65.md` (Gate: S266 admit, four rejects; M65-1 to M65-5).
QUALITY #102 (rule) and #103 (supersedes #102's why clause with the corrected evidence). Knowledge entry
`corpus/knowledge/2026-11-03-r65-jsc-closure-matrix.md` and its map row.

**Trends.** expansion **improved** (one admitted knowledge entry on mapper-closure ground, citing mined S266;
`SOURCES.md` +1). quality **improved** (round-64 F1/F2 repaired and demonstrated red/green; toolchain restored
cache-free; no admitted entry found false). discernment **improved** (three seats independently found the C2
defects before the L1 read them; the lane refused its own second claim rather than citing prose, and recorded
the reverse of its own premise; outside closure verification still pending).

**Wave.** One v1 wave `r65-w1`, 12 seats (policy band 8–16): 3 executor, 1 reviewer, 1 critic, 2
mutation-testers, 1 sentinel, 1 scout, 1 connector, 2 scribes; attack share 4/12 = 33%. L1 held the planner
seat (validator rejects a planner role). No residual call; no dead seats (`r65-w1-results.json`: 12/12
settled).

**planned (next steered round only):** (a) a NEW freeze for the coverage ground: the counter must run
recipe A verbatim as its before-arm, emit the hidden files as a list, carry its predicate constant, and the
claim may cite only emitted fields (M65-2/M65-4/QUALITY #103); (b) a NEW freeze for the closure counter's two
boundaries: a post-`python_probe` cache check folded into `closure.ok`, a frozen `COUNT` assertion, and the
reviewer's A1/A3/A5 residuals (M65-5); (c) the r63 planned record-section sweep stays open; (d) the standing
duties re-run every round that lands receipts; the r58/r60 bare-name findings and the r64 placeholder-token
disposition stay named debt; (e) the AVM LE-SquashFS re-freeze stays routed (host-absent surfaces unchanged).
