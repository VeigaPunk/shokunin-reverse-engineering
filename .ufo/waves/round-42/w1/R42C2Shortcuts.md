# R42C2Shortcuts — round 42 wave 1

**Verdict: DEFECTS FOUND** — the A1 C2 target can be reached by 15-row first-match tables that do **not** encode the draft's precedence steps: the counter (`matched == n` + bindings) cannot distinguish the intended v4 table from structurally different minimal tables, and the rows the draft treats as load-bearing (the `failing handler` column, the `dependencies` column, the OP guard) are entirely avoidable. Six concrete new combo draws / replicates are described that no disc of the minimal tables found here satisfies; they should be added to `heldout-gen-v4.py` before the freeze.

Seat scope: shortcut-construction attack on the R42-C2 predicate as amended (A1). Leaf seat: no subagents, no background jobs, no `agent://all` writes. Lane writes only this report and `artifacts/R42C2Shortcuts/`. No VCS mutation; no REA/unblob/sasquatch runs on reserved C1 carriers (none touched). No tool installs were needed (stdlib only; the tooling directive's install channels were not exercised).

---

## 1. What was constructed

The seat's item: *find shortcut tables that would reach the C2 target without encoding the draft label precedence (numbered steps 1–13)*, from planned classes' feature tuples, and tables scoring all but one class, reporting which held-out class or combo draw exposes each.

**Universe U (2022 tuples)** — the union of:
1. the 52 committed round-41 held-out envelopes (features from the frozen `indep-eval-v3.py`, re-labelled with the A1 transcription);
2. the 78 committed round-42 **dev-arm envelopes** of `R42C2Gen` (`dev42-runs/*/envelope.json.gz`, features extracted with the round-41 evaluator's own reader `E.features` — covers the real legacy (H41–H50), container (H51/H52), residue (H53/H54) named classes and the 24 real combos with their actual `H/G/D/BE/SR/P/HF` tuples);
3. predicted legacy-family tuples (unblob 26.6.4 handler names `squashfs_v1`, `v2`, `v2_nonstandard`, `v3`, `v3_ddwrt`, `v3_broadcom`, `v3_nonstandard` from the installed `handlers/filesystem/squashfs.py:101-410`; clean per handler, dependency missing, zero-file, partial and full-body failure × both byte orders);
4. predicted `container-depth-limited` and `unknown-residue` named classes;
5. the widened combo factor space (handler family × endian × in-tree × escaping × damage {none,partial,zeroid} × dependency {none,le,be,both} × residue × container × depth × second chunk, ≥2 decision factors per draw).

Expected pairs for every tuple come from `v4eval.py`, a transcription written only from the amended precedence text (`plans/round-42-claims.md:84-107`). The transcription reproduces the v3 evaluator's pairs on all 52 round-41 envelopes (0 mismatches) and agrees with `R42C2ReconLegacy`'s independent A1 labels on the measured legacy envelopes (compare_a1.tsv: dep→`dep-missing-le`, clean→`clean`, depth→`depth-limited`, residue→`unknown-residue`, container→`container-depth-limited`).

**Grammar** used for rows: the L1/R42C2Grammar v4 decision — 13 columns, `failing handler` right after `handler`; `handler` globs over F (`none` = F empty); `failing handler` globs over HF (`*` matches anything including empty HF); `dependencies` has the contains form `name+`.

**Solver** (`mintable.py`): for each (label, action) group, generates every row matching all members (domain cells: op/pr tokens or `*`; handler `*`/`none`/fnmatch over F; failing-handler patterns over HF; gap cells exact/contains; dependency cells exact/contains; be/sr/files enums), prunes dominated rows (touched-set), then searches ordered covering (feasibility memoized on the placed-group set). Minimum row count is exactly the number of non-unclassified pairs (a row carries exactly one pair), so "smallest" = 15 rows for U.

## 2. Main findings

### F1. Minimal tables exist and do not encode the precedence

A 15-row canonical table scores **2022/2022** on U (0 mismatches), including all 78 real dev envelopes. Table A in `artifacts/R42C2Shortcuts/tables.md`. Structural properties of the found minimum:

- **OP cell is `*` on every row** (no row pins `operation`; the domain guard survives only because the OOD envelope's provider is `binwalk` and the rows that would otherwise swallow it pin `provider=unblob`).
- **`failing handler` is used nowhere** (all rows `fh=*`); the avm/legacy/body split is achieved by handler(F)-level patterns plus row order.
- **`dependencies` is unused** in the canonical variant (Table B uses `deps=*` everywhere and still scores 2022/2022; 27 vs 28 constrained cells).
- The `handler`/`gaps`/`be`/`sr`/`files` columns **are** load-bearing (restricting any of them to `*` makes the minimum infeasible — see F3).

So the counter cannot tell the intended table from a table that, e.g., never looks at the failing-handler column and never pins OP.

### F2. Forced-order pairs (order the minimum must encode)

Only two unordered group pairs force an order in every 15-row table (computed over all candidate rows):

| pair | direction | why |
|---|---|---|
| `unknown-residue` vs `depth-limited` | residue **before** depth | residue row (contains `unknown-chunk-handler`) and depth row (contains `depth-limited`) both match combined `G ⊇ {unknown-chunk-handler, depth-limited}`; step 9 precedes step 10 |
| `avm-marker-be-dropped` vs `body-extractor-failure` | avm **before** body | both match P=0 `extractor-failure` v4 envelopes; only the `-be`/handler split separates them, and a single body row cannot exclude the avm single without a cell the body group cannot pin |

Every other overlap (partial/depth, dep/failure, clean/escaping, mixed/in-tree, no-chunk/container, clean-empty/escaping, …) is resolvable by cells, so the minimum can be built with very little of the precedence's order — the draft's step order is mostly **not forced** by the held-out shapes.

### F3. Column essentiality (restrict the column to `*` on every row)

| column | min rows after restriction |
|---|---|
| `op`, `pr`, `fh`, `deps` | 15 (still feasible) |
| `handler`, `gaps`, `be`, `sr`, `files` | infeasible (no 15-row table) |

The `failing handler` column added in A1 (and the `dependencies` column) are **not needed by any minimum**, on the whole predicted universe including the real dev envelopes.

### F4. All-but-one-class tables and drop fates

- Removing **any single named class or family** keeps min = 15 except when the removal empties a group: `planned:avm-marker-be-dropped` and `planned:no-squashfs-chunk` are the **only** sources of their groups in U today (the combo factor space cannot draw BE=no on a v4 BE chunk, and combos always carry F ≠ ∅), so dropping either yields a 14-row table (exemplar: Table C drops the legacy row and scores 141/2022 only because the 141 legacy envelopes then fall to `unclassified`).
- Drop fates (first-found table) — what happens to a group when **its own row is omitted**:
  - partial → mislabelled `body-extractor-failure`/`depth-limited`/`unknown-residue` (90/76/66);
  - depth → all 62 fall to `unclassified`;
  - in-tree → all 15 go `mixed-symlinks`;
  - mixed → all 17 go `depth-limited`;
  - clean → all 19 go `escaping-symlink-removed`;
  - clean-empty → all 9 fall to `unclassified`;
  - escaping → all 14 go `clean-empty`;
  - dep-be → 128 go `body-extractor-failure` (the dep+zeroid combos), 66 fall to `unclassified`;
  - dep-le → 256 go `legacy-body-failure` (dep+zeroid legacy combos), 173 fall to `unclassified`;
  - avm → all 4 go `body-extractor-failure`;
  - body → all 70 go `legacy-body-failure`;
  - no-chunk → all 4 fall to `unclassified`;
  - legacy → all 141 fall to `unclassified`;
  - container → split (100 `depth-limited`, 320 `legacy-body-failure`, 115 `unclassified`, 99 `unknown-residue`);
  - residue → all 103 go `depth-limited`.

These fates are exactly what controls CTL-C2-8 (no legacy row), CTL-C2-10 (no container/residue rows) and a no-depth row must detect on dev envelopes; note several are not `unclassified` but a **different label**, so a kill rule counting only `unclassified` fall-through would miss them.

### F5. Exposure frontier (outside-U tuples each minimal table mislabels)

Deviation scan over a 5-kind × 4-dep × BE/SR/P × multi-H grid (≈ 3600 tuples): the canonical and least-constrained tables deviate on 3628 grid tuples, the no-deps variant on 3280. Most are far outside the planned classes; the ones closest to the planned surface, with their nearest planned class, are:

| probe | expected (A1) | canonical table gives | nearest planned class / combo draw |
|---|---|---|---|
| OP=`inspect_firmware_regions`, PR=`unblob` (op moves, provider stays) | `unclassified` | `clean` | out-of-domain (today OOD moves op **and** provider together) |
| H=`{tar}`, F=∅, G=∅, P>0 (container at depth 3 without a SquashFS chunk) | `no-squashfs-chunk` | `clean` | container-depth-limited (today container draws always carry `depth-limited`) |
| H=`{tar}`, F=∅, G=`{unknown-chunk-handler}` | `no-squashfs-chunk` (step 3 precedes step 9) | `unknown-residue` | unknown-residue (today residue draws always have F ≠ ∅) |
| G=∅, SR=yes, P=0 | `escaping-symlink-removed` (step 12 ignores P) | `clean-empty` | escaping-symlink-removed (today escaping envelopes publish >0 files) |
| extractor-failure gap **without a handler** (HF=∅), v4 BE, BE=no, P=0 | `avm-marker-be-dropped` (HF falls back to F) | `legacy-body-failure` | avm-marker-be-dropped (today REA records the failing gap handler) |

The first four are all *realistic* REA envelope shapes that the current generator never produces; a held-out seed drawn from them would break every table of the found family. The fifth requires the REA envelope to omit the failing-gap handler (the draft's HF fallback exists precisely for that case).

## 3. A1 delta (changes vs the pre-A1 draft and this seat's first pass)

- Pre-A1, the same method on the unamended 13-step text produced a 13-row table (12 labels + default) scoring the pre-A1 universe; it was validated through the real v3 interpreter grammar on the 52 real envelopes plus 7 handler-mutated legacy envelopes (59/59). That analysis is superseded; it is kept only as evidence of the method.
- Amendment A1 adds `container-depth-limited`, `unknown-residue` and the HF/L semantics; the minimum rose to 15 rows, with residue-before-depth and avm-before-body as the only forced orders.
- **Calibration finding**: the first-pass table (built with the assumption HF=H on clean envelopes) scored 0/2022 on the predicted universe but **18/78 mismatches on the real dev envelopes** — every clean/dep envelope carries `HF=[]` (no extractor-failure gap ⇒ no failing handler). After correcting the universe to the real HF semantics and re-running, the canonical table scores 78/78 on the dev envelopes. Lesson for the freeze: predicted universes must use HF=∅ on non-failure envelopes or tables are built that break on real REA shapes; the `R42C2ReconLegacy` measured legacy envelopes corroborate the corrected shapes (D=`sasquatch` → `dep-missing-le`, depth/residue/container labels as predicted).

## 4. Recommended combo factors / replicates no found shortcut satisfies

Each recommendation is a factor vector whose tuple makes every 15-row table of the minimal family found here mislabel it (probe results above; verified against the canonical table):

1. **OOD-with-unblob**: `operation` ≠ `extract_firmware` while `provider.id` stays `unblob`. Forces the OP column (or a guard) back into every row; today's OOD class moves op and provider together, letting all rows keep `op=*`.
2. **Container without depth-limited**: F=∅, G=∅, P>0 (e.g. a tar/TRX at `--max-depth 3` with no SquashFS chunk). Forces `no-squashfs-chunk`-before-`clean` ordering or a handler pin on clean.
3. **F=∅ + residue**: G = {`unknown-chunk-handler`} with F=∅. Forces step-3-before-step-9 ordering between the no-chunk and residue rows.
4. **Escaping zero-file**: SR=yes, G=∅, P=0. Removes the `files=>0` crutch from the escaping row (today every escaping envelope publishes files).
5. **Failure envelope with an extractor-failure gap carrying no handler** (HF=∅, falling back to F): forces the table to use the failing-handler fallback semantics instead of relying on HF being populated.
6. **Mixed-family multi-chunk damage** (both directions): H={v4_be, v3} with the failure on v3 (HF={v3}, BE=no, P=0) and the converse — these discriminate HF-based from H-based rows; partially present in dev (C17: failure on v4_be) but the legacy-failing direction is not drawn.

Additional generator notes:
- Keep the `dep` both-names draw (D={sasquatch, sasquatch-v4be} on v4_be, dev C04) — it is the only member forcing the deps contains-form; and keep ≥2-decision-factor draws (dev: 22/24 combos outside the named union — the `combo_unseen_majority` binding is comfortably met, and the CTL-C2-7 exact-lookup ceiling is 2/24).
- A replicate of the `avm` class with P=0 and **HF=∅** would specifically break tables relying on `fh` globs (as the canonical one does).

## 5. What this means for the freeze

- The counter's `matched == n` and binding set cannot detect a table that reaches the target without encoding the precedence (F1–F3). If the goal is that the table *is* the precedence, add structural bindings: e.g. forbid `op=*` rows, require the `failing handler` cell to be non-`*` on the avm/body/legacy rows and the `dependencies` cell to be non-`*` on the dep rows, or add the F5 probes to the held-out set so they stop being free.
- The two forced orders (residue before depth; avm before body) are the only order facts the current shapes demand; a table that gets them right in any cell-equivalent way passes the current target.
- The all-but-one-class fates (F4) give the L1 a ready-made expectation table for the CTL-C2-8 / CTL-C2-10 kill-rule scoring.

## 6. Evidence

All commands ran from `$S=/fast/scratch/hyaku/kaidoku-r42/R42C2Shortcuts` with `TMPDIR=$S`; scratch was removed before yield.

- `python3 -I -B tools/round-41/indep-eval-v3.py --envelopes corpus/evidence/round-41/c2/heldout --out heldout-v3-pairs.json` → exit 0, 52 envelopes, `v4eval.py` transcription matches v3 pairs on all 52.
- `UNIVERSE_OUT=… universe.py` → exit 0, wrote `universe-a1.json` (2022 tuples).
- `UNIVERSE_PATH=… MINTABLE_OUT=… mintable.py` → exit 0, min = 15 rows, canonical table in `mintable-a1.json`.
- Canonical-table scoring: 2022/2022 on U; **78/78 on the real dev envelopes** (features from `envelope.json.gz` via `E.features`).
- `ANALYZE_OUT=… analyze.py` → exit 0, wrote `analyze-a1.json` (forced orders, column essentiality, drop fates, all-but-one-class sizes, deviation counts).
- Pre-A1 grammar check: table rendered as a v3-marker block and run through the real `tools/round-41/sqfs-triage-v3.py --skill … --json` on the 52 real envelopes + 7 handler-mutated ones → exit 0, 59/59 (12-column grammar only; the v4 13-column parser does not exist yet — the A1 tables are validated with the same matching semantics, and the L1/Interp seat owns the real v4 interpreter run).
- Artifacts: `tables.md` (Tables A/B/C), `universe-a1.json`, `mintable-a1.json`, `analyze-a1.json`, `v4eval.py`, `universe.py`, `mintable.py`, `analyze.py`, `heldout-v3-pairs.json`.
- Limits: the combo factor space and legacy predictions are reconstructions from the draft + unblob handler names + dev envelopes; the dev envelopes are the only real round-42 REA data in the lane so far. The deviation-grid numbers are synthetic envelope shapes and are marked by construction.
