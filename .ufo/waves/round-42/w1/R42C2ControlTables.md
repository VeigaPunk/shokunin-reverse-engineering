DEFECTS FOUND — all ten A1 controls plus three extra control documents are built in the 13-column v4 grammar and the reference table reaches the arm's target (76/76), but **CTL-C2-7 (the lookup control) also reaches 76/76**, so the C2 dev kill rule ("any control at full score on the development envelopes stops C2") fires as worded — and it fires again, through a different control (CTL-C2-10, 76/76), when the same tables are scored with the peers' draft tools, whose evaluator still implements the pre-A1 text; everything else this seat owes — tables, generator, a 24-envelope real legacy/container/residue arm, the score table, calibration and draft attacks — is delivered.

# R42-C2 control tables — wave 1 (pre-freeze, after A1)

Seat `R42C2ControlTables` (executor). Lane base `c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c`; the draft and its amendment
A1 are `plans/round-42-claims.md:58-143`. Nothing here is frozen; the L1 integrates and commits. All artifacts are under
`.ufo/waves/round-42/w1/artifacts/R42C2ControlTables/` and every number below was produced by the files named in §10.

## 1. What is delivered

| file | kind | what it is |
| --- | --- | --- |
| `controls/CTL-C2-0-base-SKILL.md` | control | byte copy of the lane `SKILL.md` (v3 live, no v4 marker): the do-nothing document |
| `controls/CTL-C2-0b-v3-table-v4-marker.md` | control | the live v3 table block, marker swapped to `v4`, bytes otherwise unchanged — 12 columns, so the A1 interpreter refuses it (exit 2) |
| `controls/CTL-C2-0c-v3-rows-13col.md` | control (extra) | the same v3 rows widened to 13 columns (`failing handler` = `*`): the parseable do-nothing surface |
| `controls/CTL-C2-1-catch-all.md` | control | one domain-guarded `clean`/`none` row |
| `controls/CTL-C2-3-actions-rotated.md` | control | reference rows, action column rotated by one (no fixed point, asserted) |
| `controls/CTL-C2-4-exact-gap-sets.md` | control | reference rows with every `kind+` cell made exact |
| `controls/CTL-C2-7-lookup.md` | control | one row per (label, action) from the observed DEV tuples, specific-first |
| `controls/CTL-C2-7b-lookup-majority-fallback.md` | control (A1) | the same rows with the majority pair's row moved to an all-`*` fallback at the bottom |
| `controls/CTL-C2-7c-lookup-discovery-order.md` | control (extra) | the same rows as CTL-C2-7 in class-discovery order (order-sensitivity witness) |
| `controls/CTL-C2-7x-lookup-exact-tuples.md` | control (extra) | one row per distinct observed tuple, unique synthetic labels |
| `controls/CTL-C2-8-no-legacy-row.md` | control | reference rows without `legacy-body-failure` |
| `controls/CTL-C2-9-v4-handler-glob.md` | control | reference rows with every `handler` cell `squashfs_v4_*` |
| `controls/CTL-C2-10-no-container-residue.md` | control (A1) | reference rows without `container-depth-limited` and `unknown-residue` |
| `controls/CTL-C2-REF-v4-precedence.md` | witness (not a control) | the 15 A1 steps encoded first-match in the 13-column grammar |
| `c2-controls.py` | generator + scorer | builds every document above from `REF_ROWS` + the DEV arm, then scores each with `--interp`/`--eval` |
| `v4-check-interp.py` | DEV interpreter | the draft v4 contract (13 columns, `handler` over F, `failing handler` over HF, `kind+`/`name+`) with `--selftest` 70/70 |
| `preview-precedence.py` | DEV evaluator | A1 steps 1–15 executed literally, `--selftest` 78/78 (every step and every label covered) |
| `make-dev-slice.py`, `fixtures.json`, `rea-raw/`, `dev-legacy/` | DEV arm | 24 real REA 6.5.0 envelopes + manifest under the ONE key `declared_features` |
| `report-tables.py`, `step-matrix.md`, `class-tuples.md`, `scores-a1.json`, `scores-a1-v4only.json`, `scores-a1-peer-tools.json` | evidence | the numbers in §4–§7 (the last is the §6.5 cross-run with the peers' draft tools) |

## 2. The development arm

The arm is the only DEV data that exists for round 42 at this point; R42C2Gen's dev arm had not landed when this ran.

* **Slice A — 52 committed round-41 dev envelopes** (`.ufo/waves/round-41/controls/c2/dev`): 40 named v4 classes × 2 + 12
  `combo` carriers. Frozen data, no new run.
* **Slice B — 24 real envelopes produced here** (`dev-legacy/`): `REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y
  rea-agents@6.5.0 extract-firmware --format json --full-output --max-depth N <input> <fresh outdir>`, unblob 26.6.4,
  sasquatch 4.5.1. Inputs are unblob's MIT SquashFS fixtures (never a C1 carrier) plus round-41 C2 carriers used only as
  mixed-input halves in scratch. Each envelope's fixture URL, sha256, damage recipe and command are in `fixtures.json`
  and `dev-legacy/manifest.json`. Ids L01–L24: ten legacy-clean envelopes covering seven distinct runtime handler names (both byte
  orders for `squashfs_v1`/`squashfs_v3`, plus an LZMA variant), one legacy depth-limited,
  one legacy dep-missing, six legacy zero-file body failures (v1/v2/v3, both byte orders), two mixed clean, one mixed
  failure, one container (tar at `--max-depth 1`), one residue, two dep+failure unions.

Measured facts that the controls depend on (all from `dev-legacy/manifest.json`):

| fact | measurement |
| --- | --- |
| runtime handler names are **not** per-endian for v1–v3 | `squashfs_v1`, `squashfs_v2`, `squashfs_v2_nonstandard`, `squashfs_v3`, `squashfs_v3_ddwrt`, `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`; one name covers both magics (`unblob/handlers/filesystem/squashfs.py:101-453`) |
| every v1–v3 chunk resolves plain `sasquatch` | the extractor sets `EXECUTABLE = "sasquatch"` and switches to `sasquatch-v4be` only for `(BIG, 4)` (`squashfs.py:25-26,:40-41`); the dependency report is minted on `FileNotFoundError` from `Command.get_dependencies()` = `[self._executable]` (`extractors/command.py:69-71,:101-102`), **not** from the extractor's own `get_dependencies()` which lists both binaries (`squashfs.py:68-69`) → L12's gap names `sasquatch` only. A1 step 4's confirmation holds |
| `--max-depth 1` on any single-chunk image mints a `depth-limited` gap even with no nested image | L11: G = {`depth-limited`}, 2 files |
| a container is `container-depth-limited` | L21: tar holding the v3 fixture at `--max-depth 1` → H = {} (the `tar` handler is not SquashFS), G = {`depth-limited`}, P = 1 |
| residue needs non-padding bytes | L22: 200 deterministic pseudo-random bytes after the chunk → G = {`unknown-chunk-handler`}, REA publishes `4096-4296.unknown`; a `0xAA` tail is absorbed as a `padding` chunk and yields **no** gap |
| a multi-chunk input publishes its carved chunk files | L20/L23/L24: `firmware.bin_extract/0-4096.squashfs_v3` counts in `files`, so **P ≥ 1 in any multi-chunk envelope**; P = 0 is reachable only on single-chunk inputs |
| a dep gap plus a failure resolves at step 4 | L23/L24: G = {`extractor-failure`, `missing-extractor-dependency`}, D = {`sasquatch-v4be`}, P = 2 → `dep-missing-be` |
| a legacy zero-file failure is reachable both ways | L13 (LE, argv `sasquatch -le …`, BE = no) and L14 (BE, argv `sasquatch -be …`, BE = yes) → step 7 either way |

## 3. The grammar as implemented (L1 decision, from R42C2Grammar)

Thirteen columns, in this order: `label | operation | provider | handler | failing handler | gap kinds |
dependencies | -be in child argv | symlink removed | published files | action | cause | source`.

* `handler` globs over **F** (the `squashfs_*` names in H); `none` means F is empty; `squashfs_*` any.
* `failing handler` globs over **HF** = the handlers of the `extractor-failure` gaps, falling back to F when none carries
  one; `*` matches anything including an empty HF. A1 steps 6 and 7 put `squashfs_v4_be` / `squashfs_v[123]*` there and
  `squashfs_*` in `handler` — measured need: `a1-hf-v3-beside-clean-v4be-is-legacy` would be mislabelled
  `avm-marker-be-dropped` by a handler-over-H rule (this is exactly the pre-A1 draft's hole, and A1's HF closed it).
* `gap kinds` keeps the contains form `kind+` / `a,b+`; **`dependencies` now also takes `name+`** (`a,b+` = holds both),
  which the dep rows need because A1 step 4 tests membership: D = {`sasquatch`, `sasquatch-v4be`} must reach
  `dep-missing-be`, and an exact-set cell cannot express that. `deps-cell-has-contains-form` covers it.
* First match wins; no match prints `unclassified`/`none`; a v1/v2/v3 marker, a 12-cell table, a duplicate label, an
  undeclared action or a malformed cell makes the run unevaluable (exit 2).

Vocabulary is the round-41 twelve plus `cross-read-legacy` and `isolate-residue` (14 tokens; the A1 label set is 16
including `container-depth-limited`, `unknown-residue`, `legacy-body-failure`).

**Consequence for the claim text:** `CTL-C2-0b` — "the round-41 v3 table bytes under the v4 marker" — is a 12-column
document, so under this grammar it exits 2 and scores 0/76 instead of the claim's predicted "labels every legacy-chunk
envelope `no-squashfs-chunk` or `unclassified`". `CTL-C2-0c` (the same rows widened) is the measurable do-nothing
surface: 56/76, and every legacy/container/residue envelope is `unclassified`. The claim sentence should name 0c, not 0b.

## 4. Score table (A1 grammar, 76 envelopes: 12 combo + 64 named)

| control | rows | interp exit | matched | combo | named | missed steps (A1) |
| --- | --- | --- | --- | --- | --- | --- |
| SKILL.md live v3 table | 12 | 2 | 0/76 | 0/12 | 0/64 | all |
| CTL-C2-0 base SKILL | — | 2 | 0/76 | 0/12 | 0/64 | all |
| CTL-C2-0b v3 bytes under v4 marker | 12 | 2 | 0/76 | 0/12 | 0/64 | all (table unparseable) |
| CTL-C2-0c v3 rows widened | 12 | 0 | 56/76 | 12/12 | 44/64 | s2×1, s4×1, s7×6, s9×1, s10×1, s14×10 |
| CTL-C2-1 catch-all | 1 | 0 | 17/76 | 0/12 | 17/64 | s2–s14 (59 envelopes) |
| CTL-C2-3 actions rotated | 15 | 0 | 2/76 | 0/12 | 2/64 | all but s1 (labels 76/76) |
| CTL-C2-4 exact gap sets | 15 | 0 | 60/76 | 8/12 | 52/64 | s4×2, s5×10, s10×4 |
| CTL-C2-7 lookup | 16 | 0 | **76/76** | **12/12** | 64/64 | — |
| CTL-C2-7b lookup + majority fallback | 16 | 0 | 61/76 | 12/12 | 49/64 | s14×15 |
| CTL-C2-7c lookup, discovery order | 16 | 0 | 66/76 | 10/12 | 56/64 | s9×1, s10×9 |
| CTL-C2-7x lookup, exact tuples | 48 | 0 | 27/76 | 2/12 | 25/64 | s4×3, s5×14, s7×5, s8×2, s10×7, s11–s14 |
| CTL-C2-8 no legacy row | 14 | 0 | 70/76 | 12/12 | 58/64 | s7×6 |
| CTL-C2-9 all handler cells `squashfs_v4_*` | 15 | 0 | 2/76 | 0/12 | 2/64 | all but s1 (action hits 20) |
| CTL-C2-10 no container/residue rows | 13 | 0 | 74/76 | 12/12 | 62/64 | s2×1, s9×1 |
| **CTL-C2-REF** (witness) | 15 | 0 | **76/76** | 12/12 | 64/64 | — |

`kill_rule_fires = True` (from `scores-a1.json`). Per-envelope detail is in `step-matrix.md` and `class-tuples.md`.

## 5. Control by control: what it misses and why

* **CTL-C2-0 / live SKILL** — exits 2 (`line 434: refused marker '<!-- sqfs-triage-table v3 -->'; this interpreter
  reads only '<!-- sqfs-triage-table v4 -->' in the craft section`); 0/76. This is the claim's "unmoved" command,
  confirmed on base `SKILL.md`.
* **CTL-C2-0b** — the v3 header has 12 names against a 13-column grammar: exit 2, `table at line 9: header is […,
  'handler', 'gap kinds', …], expected […, 'handler', 'failing handler', 'gap kinds', …]`. It is still a valid
  do-nothing witness, but it can no longer demonstrate the claim's predicted *labels*; 0c does.
* **CTL-C2-0c** — the v3 rows parse and then miss exactly the new families: 10 legacy cleans (`clean` → `unclassified`),
  6 legacy failures (s7), the legacy dep (s4), the legacy depth envelope (s10), the container (s2) and the residue (s9).
  Every combo still scores, because combos use v4 handlers the v3 rows cover.
* **CTL-C2-1** — one row that is correct only for `clean`: it cannot separate `clean-empty` from `clean`, cannot label a
  dependency gap, a partial, a legacy failure, a residue or a container; 17/76 are exactly the 17 `clean` envelopes.
* **CTL-C2-3** — labels 76/76 and pairs 2/76 (only the two out-of-domain envelopes, which the interpreter answers
  itself). This is the witness that a label-only counter would score this table at full marks.
* **CTL-C2-4** — exact gap sets lose the 10 partial envelopes whose G also holds `unpublished-entry`/`depth-limited`
  (s5), the 4 depth envelopes whose G holds a second kind (s10) — the round-41 contains-form finding, reproduced on the
  widened arm — and the two dep+failure unions (s4), whose G holds both `missing-extractor-dependency` and
  `extractor-failure`, so neither the exact dep row nor the exact partial row matches.
* **CTL-C2-7** — full score (§7).
* **CTL-C2-7b** — the majority pair is `clean` (15 envelopes). Moving its specific row to an all-`*` bottom row loses the
  whole `clean` family (15 envelopes, s14): the merged `depth-limited` row (G = `*` after merging `depth-limited` and
  `depth-limited`+`unpublished-entry`) sits above and steals them as `raise-depth`. A fallback row buys unseen tuples,
  never its own class.
* **CTL-C2-7c** — the same 16 rows in discovery order: s10×9 (`depth-limited` and its combos) and one residue fall
  through, because the merged `clean`/`clean-empty` rows are then *above* the depth row and answer first. **Same table,
  different order: 76 vs 66.**
* **CTL-C2-7x** — literal exact-tuple enumeration: 48 rows, 27/76; the labels cannot be unique per class, so most rows
  carry a synthetic label and lose the label half (action hits 71/76).
* **CTL-C2-8** — misses exactly the six real legacy zero-file failures (s7) and nothing else: the legacy row is worth
  6 pairs on this arm. On the v4-only slice it is 52/52, i.e. it discriminates only because the arm contains the legacy
  family.
* **CTL-C2-9** — every handler cell widened to `squashfs_v4_*` makes the first (`no-squashfs-chunk`) row match every v4
  envelope, so the table collapses to 2/76 (the out-of-domain pair). The handler cell is load-bearing in the strongest
  possible way; the control is deliberately catastrophic, like round-41's CTL-C2-3.
* **CTL-C2-10** — misses the container (s2) and the residue (s9) and nothing else: those two rows are worth exactly one
  pair each on this arm, so the control is weak unless the dev arm carries more container/residue envelopes (see §9).
* **CTL-C2-REF** — 76/76: the 15 A1 steps are encodable as one first-match table with the 13-column grammar, with
  `HF` doing the step-6/7 work. This is the row set the frozen `SKILL.md` block 21 must reach; the table scribe can
  transcribe it (`controls/CTL-C2-REF-v4-precedence.md`), replacing its `cause`/`source` prose with cited rows.

## 6. Calibration

1. **A1 vs round 41 on the v4-only slice: 52/52.** `preview-precedence.py` and the committed round-41 evaluator
   (`ref-indep-eval-v3.py`) give identical (label, action) on all 52 round-41 dev envelopes, and the manifest's declared
   pairs agree on all 40 named ones. The A1 amendment changes nothing on a v4-only arm, as it should.
2. **Round-41 numbers reproduce exactly.** On the v4-only slice this seat's CTL-C2-7c (discovery order) scores **44/52**
   and CTL-C2-4 **38/52** — the two committed round-41 held-out values (`.ufo/waves/round-41/w2/R41W2C2Controls.md`).
   That anchors the scorer: same construction, same numbers.
3. **Interpreter contract**: `v4-check-interp.py --selftest` 70/70, including `deps-cell-has-contains-form`,
   `failing-handler-reads-HF` and `failing-handler-v4be`. **Evaluator**: 78 cases, every one of A1's 15 steps and all 16
   labels covered, 0 failures.
4. **Feature agreement**: the manifest's `declared_features` are the interpreter's own `--json` features, stored under one
   key (R41-CL1). The scorer never reads a second feature key; the round-42 counter should read exactly this one.
5. **Cross-run with the peers' draft tools.** Re-scored every control with `--interp
   ../R42C2Interp/sqfs-triage-v4.py --eval ../R42C2Eval/indep-eval-v4.py` (both read-only; `scores-a1-peer-tools.json`):

   | control | this seat's pair | peers' pair |
   | --- | --- | --- |
   | CTL-C2-0 / live SKILL | 0/76 (exit 2) | 0/76 (exit 2) |
   | CTL-C2-0b | 0/76 (exit 2) | 0/76 (exit 2) |
   | CTL-C2-0c | 56/76 | 58/76 |
   | CTL-C2-1 | 17/76 | 17/76 |
   | CTL-C2-3 | 2/76 (labels 76) | 2/76 (labels 74) |
   | CTL-C2-4 | 60/76 | 58/76 |
   | CTL-C2-7 | **76/76** | 70/76 |
   | CTL-C2-7b | 61/76 | 55/76 (labels 70) |
   | CTL-C2-7c | 66/76 | 66/76 |
   | CTL-C2-7x | 27/76 | 25/76 |
   | CTL-C2-8 | 70/76 | 68/76 |
   | CTL-C2-9 | 2/76 | 3/76 |
   | CTL-C2-10 | 74/76 | **76/76** |
   | CTL-C2-REF | **76/76** | 74/76 |

   Two findings: (a) the interpreters **agree on the grammar** — R42C2Interp's interpreter parses my 13-column reference
   table, prints the same `handler over F` / `failing handler over HF` semantics and the same 15 rows, so the L1's
   grammar decision is implemented identically in two places; (b) the two **evaluators disagree on exactly two
   envelopes**, L21 and L22: R42C2Eval's evaluator reads L21 as `no-squashfs-chunk`/`inspect-input` and L22 as
   `unclassified`/`none`, i.e. it still implements the 13-step pre-A1 list, while A1 says `container-depth-limited` and
   `unknown-residue`. Its file mtime is 18:56 local, i.e. it was written before the amendment reached this wave. It agrees with this seat on all
   52 v4 envelopes and on all 22 non-A1 legacy envelopes. Consequence: the reference table scores 74/76 against a
   pre-A1 evaluator, and CTL-C2-10 becomes the full-scoring control (dropping the container/residue rows costs nothing
   when the expectations are pre-A1). **Which control is the ceiling depends on the evaluator text**, which is a
   second reason to scope the kill rule per §7. Interop note: the interpreters expose `H` differently (R42C2Interp's
   feature map keeps non-SquashFS handler names such as `tar`, mine filters to `squashfs_*`); `c2-controls.py` now
   normalises `H` to the `squashfs_` prefix when it builds lookup cells, and R42C2Interp refuses a handler cell that
   globs over a non-squashfs name (`handler cell 'tar' does not begin 'squashfs'`), which is the stricter and correct
   behaviour. The frozen interpreter/evaluator pair must be reconciled before the counter reads them.

## 7. The kill rule fires — three measurements and what they mean

**7.1 Full score is a property of row order, not of coverage.** CTL-C2-7 (16 rows, most-specific first) and CTL-C2-7c
(same 16 rows, discovery order) differ only in row order: **76/76 vs 66/76**. Both are legal tables in this grammar. So a
number from this control measures the author's ordering choice at least as much as the table's depth.

**7.2 A lookup trained on a disjoint family collapses.** Build the lookup from the v4-only slice, score it on the 24
real legacy/container/residue envelopes: **2/24** (only the two mixed envelopes whose handler set contains a v4 name;
everything else `unclassified`). The discriminating property is therefore *disjointness of the build and scoring sets*,
not the dev score itself.

**7.3 On combos it is 12/12**, i.e. the arm's combo family is inside the named tuples' union — the opposite of what
`combo_unseen_majority` will require of the generator's combos. This arm's combos are round-41's (partial/depth/link
supersets); a specificity-sorted merge of per-label tuples absorbs them.

**Consequences for the claim, in order of preference:**

1. **Scope the binding, not the control.** Keep the dev kill rule for CTL-C2-0/0b/0c/1/3/4/7b/8/9/10 and score CTL-C2-7
   only on a family it was not built from — the claim's own `lookup_combo_below_half` already does this. On a disjoint
   family the measured collapse is 2/24, so the binding can be met; on this arm's combos it is 12/12, so the combo
   generator must draw tuples outside the dev named-tuple union (which `combo_unseen_majority` already requires — the two
   bindings are the same requirement seen twice).
2. **If the kill rule must include CTL-C2-7 as worded**, no dev arm that contains one exemplar of every precedence branch
   can pass: the label *is* the branch, so a per-label merge of that branch's tuple encodes the branch. Withholding a
   branch from the lookup's build set is the only way to keep the rule — and that is option 1 with extra steps.
3. **Freeze a build set for the lookup.** If the L1 wants a dev-scored CTL-C2-7, freeze a `lookup build` id list (e.g. the
   round-41 slice) inside the manifest, so "built from those dev tuples" is a fact of the freeze rather than of the
   scorer's `--dev` arguments.

**Also note:** on the v4-only slice, CTL-C2-7b, CTL-C2-8 and CTL-C2-10 are all 52/52 — three more full scores. They are
not shortcuts on a *v4-only* arm; they only discriminate once the legacy, container and residue families are in the arm.
The dev arm must therefore carry them (it does now), and the claim's "None may reach full score" should be read against
the widened arm, not against the round-41 slice alone.

## 8. Attacks on the A1 draft (measured)

* **D1 — `legacy-dep-missing-be` is unreachable from unblob's SquashFS handlers.** `SquashFSExtractor` switches to
  `sasquatch-v4be` only for `(Endian.BIG, version 4)` (`squashfs.py:40-41`), and the dependency report is minted from
  `Command.get_dependencies()` = the single resolved executable (`extractors/command.py:69-71,:101-102`), not from the
  extractor's two-name `get_dependencies()` (`squashfs.py:68-69`). A v1–v3 chunk therefore never produces a gap naming
  `sasquatch-v4be`. A1 step 4 is right to test `D` membership rather than the handler name,
  but the *class list* in the predicate should drop `legacy-dep-missing-be` or rename it `legacy-dep-missing` (LE only):
  a generator that tries to build it from fixtures will fail or will have to hand-mutate the envelope.
* **D2 — `P > 0` is structural in multi-chunk envelopes.** REA publishes each carved chunk under
  `<input>_extract/<start>-<end>.<handler>` (L20/L23/L24). So in any envelope with two or more chunks, step 5
  (`extractor-failure` and P > 0) fires before steps 6–8 whenever anything failed: the legacy/AVM/body rows are
  unreachable for mixed inputs. `combo` carriers built by concatenating chunks will therefore almost all land on
  `partial-body-failure`; a combo family that wants legacy/AVM labels must be single-chunk.
* **D3 — `unknown-chunk-handler` only appears for non-padding tails.** 200 bytes of `0xAA` were claimed by unblob's
  `padding` handler and produced no gap at all; pseudo-random bytes produced the gap and a `.unknown` file. The
  `unknown-residue` class recipe must specify non-padding filler or it will silently manufacture `clean` envelopes.
* **D4 — step 2's action is not discriminative.** `container-depth-limited` and `depth-limited` share `raise-depth`, so a
  table that swallows the container class into the depth row loses only the label. That is a deliberate-looking choice,
  but it makes CTL-C2-10's margin one pair instead of one label-and-action pair; if the container outcome wants its own
  move (e.g. `rerun-on-container-child`), A1 has to say so.
* **D5 — step 9 before step 10 is untested by measurement.** I measured a residue-without-depth envelope (L22) only. A
  nested carve whose child is depth-capped *and* leaves residue was not produced; the ordering "residue before depth" is
  therefore taken from the text, not from an envelope.
* **D6 — a container at `--max-depth 1` always carries `depth-limited`, but a container is not the only source of that
  gap.** L11 shows a plain single-chunk image at depth 1 also carries it — with a SquashFS handler, so step 10, correctly.
  The class recipe must keep F = ∅ as part of the test, otherwise "container" and "depth-capped image" are indistinguishable
  from the gap alone.
* **D7 — the residue file is not a filesystem file.** `4096-4296.unknown` counts in `P`, so `clean`'s `P > 0` is satisfied
  by residue alone. The claim's C1 exact-path rule already ignores nested carves; the C2 knowledge entry should say the
  residue file is a carve artifact, never an oracle match.

## 9. Risks and limits

1. **Not the frozen tools.** The headline numbers come from this directory's `v4-check-interp.py` and
   `preview-precedence.py`; the peers' draft pair exists now and was cross-run (§6.5), but R42C2Eval's evaluator still
   implements the pre-A1 precedence, so the two evaluators disagree on the two A1 classes until that seat updates. Re-run at the freeze with
   `python3 -I -B .ufo/waves/round-42/w1/artifacts/R42C2ControlTables/c2-controls.py --root <LANE> --dev <A> --dev <B>
   --out <ctl> --json-out <scores> --interp <frozen interp> --eval <frozen eval> --build`. Expected pattern with the
   same grammar: 0/0b 0, 0c ≈56, 1 ≈17, 3 =2, 4 ≈60, 7 =n (see §7), 7b ≈61, 7c ≈66, 8 ≈70, 9 =2, 10 ≈74, reference =n.
2. **The arm is not the hold-out.** 52 of the 76 envelopes are round-41's held-out set; using them as DEV is what the
   ticket prescribes while R42C2Gen's dev arm is missing, but the claim's dev/hold-out split must be re-cut from the
   generator's seed. Nothing here should be treated as held-out data.
3. **Arm size.** 24 legacy/container/residue envelopes give CTL-C2-8 and CTL-C2-10 a 6-pair and 1-pair margin. Both
   pass, but the margins are thin; R42C2Gen's dev arm should carry more container/residue carriers (2–4 each) so the
   kill rule is checked on more than one exemplar.
4. **Real-envelope breadth.** The v1–v3 fixtures hold no symlinks or devices, so steps 11–13 are unreachable on a legacy
   chunk (the claim already states this limit). No verified `encrypted-chunk` or `unknown-chunk-handler`-plus-depth
   envelope exists, so step 15 remains exercised only synthetically (evaluator selftest).
5. **Scope.** No reserved C1 carrier was opened; no REA/unblob run touched a published image; the round-41 C2 carriers
   used as mixed-input halves were read into scratch only and never copied into the lane; no tool installed or upgraded;
   no VCS mutation; scratch `/fast/scratch/hyaku/kaidoku-r42/R42C2ControlTables` removed before this seat yields (every cited
   artefact is copied into the artifacts directory).
   One scratch-only PATH addition was used for L23/L24: `$S/bin/sasquatch -> ~/.local/bin/sasquatch`, prepended to the
   child PATH with `~/.local/bin` removed, so that `sasquatch` resolved and `sasquatch-v4be` did not. Nothing was written
   into `~/.local/bin` or any other PATH directory.

## 10. Files and hashes

All under `.ufo/waves/round-42/w1/artifacts/R42C2ControlTables/` (whole directory 1,532,786 bytes; largest file is the
base-SKILL copy, 230,342 bytes, so nothing needs a rebuild-by-hash citation):

```
09b3c013b84d2488c6e1…  c2-controls.py
26178d71c0f7634c3f13…  ref-indep-eval-v3.py   (committed round-41 evaluator, kept as the
                                                calibration anchor of §6.1)
524eedadc7a36d124be6…  v4-check-interp.py
47a6bed5c3d49c2bf3c6…  preview-precedence.py
00d75d25b7e211c1f492…  make-dev-slice.py
c6fdc1d36c1526babe93…  report-tables.py
73b057970084708e0630…  fixtures.json
71bf5489a749a90f6a87…  scores-a1.json
6b3756385836f2b27b4c…  scores-a1-peer-tools.json
e85f85bf6db3c2a78483…  scores-a1-v4only.json
f2e07392e1358198e7e4…  step-matrix.md
0859dfc3845f1c869be7…  class-tuples.md
a5277e620467ee4f7613…  dev-legacy/manifest.json
94d13b445701609f110c…  controls/CTL-C2-0-base-SKILL.md
d0e7a229f418a3d11805…  controls/CTL-C2-0b-v3-table-v4-marker.md
991b35700d7e5f852b7a…  controls/CTL-C2-0c-v3-rows-13col.md
265216e8952f8c3d4d9e…  controls/CTL-C2-1-catch-all.md
f5db0f5dd387470a7c53…  controls/CTL-C2-3-actions-rotated.md
667ef6fd2b16bb1fb976…  controls/CTL-C2-4-exact-gap-sets.md
59147315489b0b2c1c96…  controls/CTL-C2-7-lookup.md
8c43d126fd0ffb71325e…  controls/CTL-C2-7b-lookup-majority-fallback.md
6b680f89b82c8cd60341…  controls/CTL-C2-7c-lookup-discovery-order.md
4342267e8a1234ef68ca…  controls/CTL-C2-7x-lookup-exact-tuples.md
d5d3d3566f98c872cb55…  controls/CTL-C2-8-no-legacy-row.md
6f09b440f39b6a193a05…  controls/CTL-C2-9-v4-handler-glob.md
39346bf2403f3b2e4d7f…  controls/CTL-C2-10-no-container-residue.md
70f908e04d9d625a5d50…  controls/CTL-C2-REF-v4-precedence.md
```

Re-score with:

```
python3 -I -B .ufo/waves/round-42/w1/artifacts/R42C2ControlTables/c2-controls.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --dev .ufo/waves/round-41/controls/c2/dev \
  --dev .ufo/waves/round-42/w1/artifacts/R42C2ControlTables/dev-legacy \
  --out "$S/ctl" --json-out "$S/scores.json" --build \
  [--interp <frozen sqfs-triage-v4.py>] [--eval <frozen indep-eval-v4.py>]
```

Exit 1 = a control at full score (the kill rule), 0 = none, 2 = usage/IO.

## A1 delta (what changed after the amendment arrived mid-build)

The pre-A1 run (12 columns, 15 steps→13, 76 envelopes) existed and is superseded; the delta, in order:

1. **Grammar: 12 → 13 columns.** `failing handler` added after `handler` in the interpreter, the generator's `HEADER`,
   `row_line`, every control table and the reference rows. `handler` now globs over F (it already did); the new column
   globs over HF with the F fallback. `dependencies` gained the contains form.
2. **Precedence: 13 → 15 steps (A1).** `container-depth-limited` split out of `no-squashfs-chunk` (step 2 vs 3);
   `unknown-residue` inserted at step 9, *before* depth-limited; steps 6/7 now read HF and L rather than the run-wide
   handler set; step 4 wording is membership, matching what the code already did. The evaluator was renumbered,
   re-selftested (78 cases) and re-calibrated at 52/52 against the round-41 evaluator.
3. **Controls added:** CTL-C2-7b is now *lookup + one majority-label fallback row* (the majority pair is `clean`,
   measured; 61/76) — my earlier exact-tuple lookup was renamed CTL-C2-7x (27/76) and kept as evidence. CTL-C2-10 (no
   container/residue rows) added: 74/76. CTL-C2-0c added because the verbatim v3 table (0b) no longer parses under 13
   columns; the claim's 0b sentence should be corrected.
4. **Arm extended:** 20 → 24 real envelopes, adding the two A1 classes — a tar container at `--max-depth 1`
   (`container-depth-limited`) and a non-padding residue tail (`unknown-residue`) — plus two dep+failure union envelopes
   that exercise step 4 against step 5 (`dep-missing-be`).
5. **Numbers that moved:** reference 76/76 (both runs); CTL-C2-0b 56/76 → exit 2 (0/76) with 0c taking its place at
   56/76; CTL-C2-8 70/76 (unchanged); CTL-C2-4 60/76 (unchanged); CTL-C2-7 76/76 (unchanged — the finding of §7 does not
   depend on A1); CTL-C2-10 new at 74/76; the container envelope moved from "correctly `no-squashfs-chunk`" under the
   pre-A1 text to a miss for the v3-derived controls under A1.
