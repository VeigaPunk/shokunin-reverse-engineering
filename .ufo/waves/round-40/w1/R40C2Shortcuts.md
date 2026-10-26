# R40-C2 shortcut controls — seat R40C2Shortcuts (round 40, wave 1)

**DEFECTS FOUND.** Seven pre-freeze controls (CTL-C2-0…6) plus a candidate table are built and
format-validated under two independent interpreters (this seat's minimal one and the R40C2Interp
seat's), and each control is scored against 43 envelopes (26 synthetic class fixtures + 17
committed round-39 envelopes). The controls do what they were meant to do. On the way they
exposed eight defects (§4), three of them material and to be settled **before the freeze**:
**D1** is fatal as it stands — the R40C2TableDraft block, the text destined for `SKILL.md`
block 19, makes the R40C2Interp interpreter exit 2 (`cause` has no `->`); **D3** — its rows 5–6
are big-endian-only, so two of the draft's own permitted held-out replicates score
`unclassified`; **D4** — the `provider` column has no discriminating held-out evidence (637/637
real `extract_firmware` envelopes carry `provider.id = unblob`).

Base `fa6a8a3f85ec65946b3a54d37c0ddd1d6748664f`; nothing here is committed (L1 integrates).

## 1. What exists, with hashes

All under `.ufo/waves/round-40/w1/artifacts/R40C2Shortcuts/`:

| file | sha256 | what |
|---|---|---|
| `CTL-C2-0.md` | `f08b91d0…3059f` | byte copy of `SKILL.md` at the base (`git show fa6a8a3f:SKILL.md`, blob `be4b4acd`); no v2 marker |
| `CTL-C2-1.md` | `11d6fd0b…db614` | catch-all: one row, every condition cell `*` |
| `CTL-C2-2.md` | `14dfcf51…d5438e` | live v1 table (SKILL.md:333-343) transcribed into v2, `*` operation/provider, best action per label |
| `CTL-C2-3.md` | `6375870d…581b3f` | candidate table, actions rotated one row (label right, action wrong) |
| `CTL-C2-4.md` | `1a56ac97…dd38fb` | candidate table, domain guard removed (`*` operation/provider on every row) |
| `CTL-C2-5.md` | `593badbb…7927d0` | candidate table without the `mixed-symlinks` row |
| `CTL-C2-6.md` | `5f8a0353…a734c3` | candidate table plus a final `*` default row (`escalate`/`inspect-manually`) |
| `best-table.md` | `5e63959b…95f4f` | the candidate table the controls derive from (not a control) |
| `probe-shadow.md` | `ef54071a…f7341` | grammar probe: an unreachable row the draft grammar still accepts |
| `sqfs-triage-v2-min.py` | `0ce94a91…c239ae3` | minimal v2 validator/classifier (this seat's), 9-case selftest |
| `mk-controls.py` | `69847055…181f9d` | emits the controls; `--from FROZEN.md --out DIR` regenerates CTL-3…6 from the adopted table |
| `mk-envelopes.py` | `13a544aa…3bce7` | emits the 26 class fixtures (JSON only, no carriers) |
| `run-controls.py` | `06152de9…b1932e` | format-validates and scores every control under both interpreters |
| `control-matrix.tsv` | `3ecf89a9…06bba5` | 344 scored cells (8 parsable controls × 43 envelopes) |
| `control-summary.tsv` | `d13775df…07f40a` | per control: exits, correct count, wrong classes |
| `interp-agreement.tsv` | `4da198a7…b84dd7` | minimal vs seat interpreter, cell by cell |
| `scribe-block-probe.txt` | `506a72da…2ce5` | the R40C2TableDraft block measured at 18:20Z and 18:29Z (defects D1/D3) |
| `envelopes/` (+`expected.tsv`) | 27 files | 13 draft classes × 2 replicates, expected `(label, action)` |

Rebuild everything: `python3 -I -B mk-envelopes.py && python3 -I -B mk-controls.py &&
python3 -I -B run-controls.py` (exit 0; 1 if any control or the candidate table misbehaves).

## 2. Grammar as implemented, and where I had to choose

No `sqfs-triage-v2.py` existed when this seat started, so `sqfs-triage-v2-min.py` implements the
wave-dispatch grammar (marker → first table in `## Queue-drain craft`; 12-column header; first
full match; unique labels; closed action vocabulary on the line directly above the table;
`*`/exact operation and provider; `none`/fnmatch handler; `none`/`a+b` sets; `yes|no|n/a|*`;
`0|>0|*`; malformed cell → exit 2; envelope = bare `data` or `{ok,data,meta}`; `--table-only`).
Five points the dispatch leaves open and how I resolved them, all of which the freeze should state:

1. **`none` and `unclassified` are reserved.** A vocabulary token `none`, or a row labelled
   `unclassified`, makes a matched row indistinguishable from the no-match result on one half of
   the scored pair. My validator rejects both; the seat interpreter accepts `none` (defect D2).
2. **Vocabulary placement.** Accepted when it is the last non-blank line before the table header,
   tolerating the marker line between it and the vocabulary. Both this seat's files and the
   seat's own samples use that layout.
3. **`cause` is prose, no `->` required.** The dispatch's header separates the action column, so
   the v1 `cause -> action` shape has no v2 meaning. The seat interpreter still demands `->`
   (defect D1). Every control's cause carries a ` -> ` tail anyway, so the controls are valid
   under either reading — do not read that tail as agreement with D1.
4. **Absent `provider` → `PV = ''`**, matched only by a `*` provider cell.
5. **Duplicate labels → exit 2; duplicate *cell vectors* are not checked** (probe-shadow, D5).

Cross-check: on the 344 scored cells the minimal validator and the seat interpreter agree
**344/344** (`interp-agreement.tsv`, no `NO` row), so the predictions below do not depend on which
of the two is frozen. The seat interpreter's own grammar text still calls the column
`cause -> action` (line 42) while its header constant is the v2 header — a documentation fossil
of the same origin as D1.

## 3. The controls, measured

Scoring set: 26 synthetic fixtures for the draft's 13 classes — `clean-be`, `clean-le`,
`clean-empty`, `escaping-symlink-removed`, `in-tree-symlink-metadata`, `mixed-symlinks`,
`dep-missing-be`, `dep-missing-le`, `avm-marker-be-dropped`, `body-extractor-failure`,
`partial-body-failure`, `no-squashfs-chunk`, `out-of-domain` — each twice, the second replicate
differing in a non-decision feature (endianness where the class permits it, published-file count
inside the same bucket, envelope wrapper shape, `raw_result` noise); plus the 17 committed
round-39 envelopes (K1–K6, `R39C2AxisFit/env-*` minus `env-deple`, whose name says LE but whose
recorded handler is `squashfs_v4_be`). Fixtures are JSON built from the grammar's feature
definition and anchored on real vectors (cited per class in `mk-envelopes.py`); no carrier was
built and no extractor ran.

| control | `--table-only` (min / seat) | correct | wrong classes (measured) |
|---|---|---|---|
| CTL-C2-0 base SKILL | **2 / 2** | — (`marker … absent from the craft section`) | all 43 unscored; unevaluable by design |
| CTL-C2-1 catch-all | 0 / 0 | **0/43** | every class and every real envelope |
| CTL-C2-2 v1 ported | 0 / 0 | **31/43** | `clean-empty`, `mixed-symlinks`, `body-extractor-failure` (LE replicate), `partial-body-failure`, `out-of-domain`, K5/K6/env-sym |
| CTL-C2-3 actions rotated | 0 / 0 | **2/43** | every in-domain class; only the two `out-of-domain` envelopes "pass" trivially (`unclassified`/`none`) |
| CTL-C2-4 no domain guard | 0 / 0 | **41/43** | `out-of-domain` only — r1 → `no-squashfs-chunk`/`probe-superblock`, r2 → `clean`/`match-oracle` |
| CTL-C2-5 no mixed row | 0 / 0 | **38/43** | `mixed-symlinks` only (2 fixtures + K5, K6, env-sym) — all refusals (`unclassified`/`none`), no borrowed label |
| CTL-C2-6 + `*` default row | 0 / 0 | **41/43** | `out-of-domain` only → `escalate`/`inspect-manually` |
| best-table (candidate) | 0 / 0 | **43/43** | — (all 13 classes, all 17 real envelopes) |
| probe-shadow | 0 / 0 | 2/43 | accepts an unreachable row (D5) |

### Predicted vs measured, per control

Predictions were structural (written from the grammar and the v1 cells before the run); the
measured column above confirms them exactly, with one dependency worth stating.

- **CTL-C2-0** — predicts exit 2 for every envelope score: a counter that reads the base SKILL
  must report *unevaluable*, never `met_target`. Measured 2 under both interpreters. This is the
  only control whose verdict is an exit code, so the predicate must name it
  ("no v2 marker → exit 2") and the score receipt must record it (R39-CL6).
- **CTL-C2-1** — predicts every class wrong: one row cannot carry a decision. Measured 0/43. If
  a counter scores "a label was produced" or "labels are from the frozen vocabulary" it passes
  this control; only exact `(label, action)` pairs kill it.
- **CTL-C2-2** — predicts exactly the three routed defects plus the two v2-only classes:
  R39-CL1 (`*` domain cells let `binary_overview` borrow `no-squashfs-chunk` or `clean`),
  R39-CL2 (row 6's `gap kinds = *` sends every mixed-link envelope to
  `escaping-symlink-removed`), R39-CL3 (no `P>0` failure row and no `P=0` clean row → refusal),
  and — measured, not foreseen as certain — the v1 body row's `be yes` cannot see an LE body
  failure. Measured 31/43 with exactly those 12 cells wrong.
- **CTL-C2-3** — predicts every in-domain class wrong *and* every label right, so a label-only
  counter passes 43/43 while an action-scoring counter fails 41/43. That is the load-bearing
  argument for the action column; keep it as the calibrated control for "action scored".
- **CTL-C2-4** — predicts the out-of-domain class only, with two different false labels, so even
  a counter that only checks "out-of-domain must not be `unclassified`" cannot see it. Measured
  41/43.
- **CTL-C2-5** — predicts the mixed class only, and predicts *refusal*, not a borrowed label,
  because the escaping row is cut to `gap kinds = none` and the in-tree row to
  `symlink removed = no`. Measured 38/43. Consequence for the predicate: P40-C2's "assigns
  **every** held-out envelope the pair" is the clause that makes this control red; a
  "fraction decided" metric would score it 41/43.
- **CTL-C2-6** — predicts the out-of-domain class only: a `*` default row is invisible to every
  in-domain class and destroys exactly the guard. Measured 41/43.

## 4. Defects, with the smallest safe correction

### D1 (fatal at freeze) — the draft block cannot be parsed by the seat interpreter

Evidence (`scribe-block-probe.txt` §§A.0/A): the R40C2TableDraft block wrapped in a minimal
SKILL at `## Queue-drain craft` under
`python3 -I -B …/R40C2Interp/sqfs-triage-v2.py --skill draft-block-skill.md --table-only` gives

```
sqfs-triage-v2: line 34: cause -> action cell has no "->" separator      (block.md 68000e0c…, 18:20Z)
sqfs-triage-v2: line 37: cause -> action cell has no "->" separator      (block.md 14ea1d73…, 18:29Z)
exit=2 both times; the block carries zero ` -> ` (grep -c ' -> ' -> 0)
```

The block moved once inside this wave (indentation and wording) and still fails, which is itself a
freeze hazard: every measurement below has to be re-run against the final bytes.

The dispatch grammar has no such requirement, the v2 header separates `action` from `cause`, and
every one of the block's cause cells is plain prose. If block 19 lands as written, the frozen
table is unevaluable at scoring time and P40-C2 cannot reach `met_target` for a *format* reason.
The check is one stale pair of lines (`sqfs-triage-v2.py:356-357`) and its docstring echo
(`:42`). **Smallest safe correction:** freeze the interpreter without the `->` check (and fix
`:42` to read `cause`), or — if the L1 prefers to keep it — add a ` -> ` tail to every cause cell
in block 19 *and* to every control, and say so in the grammar. Do not freeze a block and an
interpreter that disagree. Whatever is chosen, the freeze commit must run the frozen interpreter
against the frozen block bytes (this is R39-CL4 restated with teeth).

### D2 — `none` is accepted as an action token
The seat interpreter's embedded `TABLE_BLOCK` declares a vocabulary that includes `none` and
gives the `clean` row the action `none` (`sqfs-triage-v2.py:173,185`; `table-only.txt` prints
`actions: none …`). Then `(clean, none)` — a decisive row — is byte-identical in the action half
to the no-match result `(unclassified, none)`, and a counter that scores actions only, or a
reader who checks the action first, cannot separate them. **Correction:** reserve `none` for the
no-match action (and `unclassified` for the no-match label) in the frozen grammar; my validator
enforces both and every control respects it.

### D3 — the draft block's rows 5–6 are big-endian-only, and the draft permits LE replicates
Evidence (`scribe-block-probe.txt` §C, block.md `14ea1d73…` at 18:29Z, with only D1 disabled so
the block's decisions are visible): `body-extractor-failure` and `partial-body-failure` both require
`handler = squashfs_v4_be` **and** `-be = yes`, so of the two replicates for each class the LE one
(handler `squashfs_v4_le`, `-be = no`) is `unclassified`/`none`:

```
WRONG body-extractor-failure-r2    unclassified   none
WRONG partial-body-failure-r2      unclassified   none
```

P40-C2 requires replicates that "differ in a non-decision feature, and … endianness where the
class allows", so the generator is invited to produce exactly these. **Correction (one cell set
each):** cut both rows endianness-agnostic — handler `squashfs_v4_*`, `-be` `*` — keeping
`published files` `0` vs `>0` to separate them, and keep the `avm-marker-be-dropped` row *ahead*
of `body-extractor-failure` so the BE marker case is still the narrower decision. That is what
`best-table.md` does (rows 4–6) and it scores 43/43, including both LE replicates. If the L1
would rather keep the rows BE-only, then the two classes must be written as BE-only in the claim
and the generator must not vary endianness for them — the draft as written does not say that.

### D4 — the `provider` column has no discriminating held-out evidence
Measured over every real REA envelope in `corpus/evidence` + `.ufo/waves` (has
`normalized_result`; 2008 envelopes, 29 operations, 47 unparsable JSON skipped; at
2026-10-26T18:4xZ, sibling artifacts growing): **637/637** with `operation = extract_firmware`
carry `provider.id = unblob`; **109/109** with `operation = binary_overview` carry
`provider.id = rea-workflow`. The only `extract_firmware` with
another provider anywhere is this wave's own synthetic mutation
(`R40C2ReconMixed/synth/prov-changed.json`, `binwalk`). So the drafted out-of-domain class (a
non-`extract_firmware` *operation*) is caught by the operation column alone, and the provider
column is an unexercised clause — the "universal clauses the counter does not enumerate" pattern.
**Correction, pick one and write it:** (a) keep both columns but state in the knowledge entry that
`PV` was invariant within each operation across all 620+110 committed envelopes, and add a
second out-of-domain replicate that varies provider only, declared as a format control (it cannot
come from a real REA run today); or (b) drop the provider column and guard on `operation` alone.
Do not claim the provider guard discriminates when nothing in the set exercises it.

### D5 — an unreachable row passes format validation
`probe-shadow.md` (row 1 strictly broader than row 2, labels unique, every cell legal) exits 0
under both interpreters. A table can therefore report 11 "row decisions" while one row can never
be the first match, inflating the decision count P40-C2 asks the counter to report.
**Correction:** the counter must count **distinct matched rows over the held-out set**
(observable), never declared rows; and the grammar gets the cheap half of a dead-row check —
two rows with identical condition cells → exit 2. Full shadow detection (pattern containment) is
out of scope; say so rather than implying it is checked.

### D6 — `-be = n/a` on the symlink and clean rows asserts a recorder property, not an outcome
`block.md` (and v1 before it) writes `n/a` for `-be` on `mixed-symlinks`,
`escaping-symlink-removed`, `in-tree-symlink-metadata`, `clean`, `clean-empty`, which is true only
because REA records no child argv on a successful extraction (K1–K6: `BE = n/a`). The moment a
successful run records its argv — the very question R40C1Revenger is opening for C1 — a standard
BE clean envelope has `BE = yes` and `clean`/`clean-empty`/two symlink rows stop matching.
**Correction (cheap robustness, no class changes):** `*` in the `-be` cell for those rows; the
column then decides only where the outcome names it (marker vs body). `best-table.md` does this
and stays 43/43. If the freeze keeps `n/a`, the claim must not vary endianness/argv recording
across those classes.

### D7 — several live candidate tables plus an embedded one
In one wave there are now at least four table texts: `R40C2TableDraft/block.md`,
`R40C2ReconDomain/v2-table-proto.md`, `R40C2AxisFit/min7-table.md`, this seat's `best-table.md`,
and the interpreter's own embedded `TABLE_BLOCK` (which differs from all of them and carries D2).
Only one may be authoritative. **Correction:** the freeze names exactly one table source (block 19
bytes in `SKILL.md`) and the interpreter's embedded block is either deleted or asserted equal to
the `SKILL.md` slice by the counter; `--print-table` must print the frozen slice, not a copy.

### D8 — control format validation still has to be pinned by the freeze commit
All seven controls parse today, under two interpreters, but "today" is not "at the freeze": D1
alone shows how a format rule can move under the controls. **Correction:** the freeze commit
runs `sqfs-triage-v2-min.py --table-only` *and* the frozen interpreter `--table-only` on each
committed control file and records the exit codes in the freeze receipt (CTL-C2-0 = 2, every
other = 0), and the counter re-runs the same check at `REV` on the committed control bytes.

## 5. Freeze sequence this seat recommends (cheap, ordered)

1. Settle D1 (interpreter vs. `->`), then D2 (`none` reserved).
2. Adopt one table; apply D3 (rows 5–6 endianness-agnostic) and D6 (`*` in `-be` on the
   non-marker rows) or state the alternatives in the claim.
3. `python3 -I -B mk-controls.py --from <the adopted block's table> --out <artifacts>/controls/`
   and commit those seven files (CTL-C2-0 from `git show BASE:SKILL.md`). The generator keeps
   CTL-C2-1/2 independent of the adopted table and rebuilds 3–6 from it, so the "forgot one row"
   control is always one row away from the frozen table. Exercised twice in scratch:
   `--from best-table.md` produced 8 files that all exit 0 under both interpreters; `--from` the
   scribe's block inherited its cause format and its `best-table.md` copy exited 2 at line 14 —
   the derivation inherits the source's format state, which is the point of validating at freeze.
4. Freeze receipt: for each control, the `--table-only` exit code under the frozen interpreter,
   plus the counter's re-run of the same check at `REV` (D8).
5. Declare in the claim that the score is all-or-nothing over `(label, action)` pairs (CTL-C2-5
   depends on the word "every"), and that a table must never pick `none` or `unclassified`
   as an answer (D2, CTL-C2-6).

## 6. Limits (not claimed)

- No REA, unblob or sasquatch run was made; no carrier was built. The 26 fixtures are JSON
  envelopes I authored from the grammar's feature definition and anchored on round-39 vectors —
  they are *not* REA output, and the class expectations are this seat's candidate assignment,
  not a frozen manifest. `heldout-gen-v2.py` remains the authority for what the classes really
  produce; if its replicates differ from mine (e.g. `no-squashfs-chunk` with a non-squashfs gap,
  or a `mixed-symlinks` carrier that also publishes zero files), change `mk-envelopes.py`,
  re-run `mk-envelopes.py` then `run-controls.py`, and read the new matrix — the matrix is
  generated, not hand-scored.
- I did not measure the round-39 held-out carriers (`corpus/evidence/round-39/c2/heldout` holds
  only `manifest.json`; no envelope JSONs are committed), and I ran no C2 carrier.
- The minimal validator is a pre-freeze stand-in: it implements the dispatch grammar, not the
  frozen interpreter's choices. Where they differ (D1) the agreement table says so by exit code,
  not by a silent pass.
- `env-deple.json` is excluded from the real-envelope set: its file name says little-endian while
  its recorded chunk handler is `squashfs_v4_be` (v1 labels it `clean`); using it as an LE
  expectation would bake a round-39 naming error into a round-40 control.
- D4's envelope counts cover `corpus/evidence` and `.ufo/waves` JSON that parse and carry
  `normalized_result` (2008 envelopes over 29 operations); 47 unparsable JSON files were skipped.

## 7. Tooling, environment, scratch

No tool installed or upgraded. Commands used (all read-only w.r.t. the lane except this seat's
artifacts directory): `python3 -I -B` on the four scripts above, `git show BASE:SKILL.md`,
`sha256sum`, and the interpreter invocations recorded in `scribe-block-probe.txt`. `TMPDIR` was
`/fast/scratch/hyaku/kaidoku-r40/R40C2Shortcuts` (scratch removed before this report was
finished); the only other scratch use was the two-line patch of a *copy* of the seat interpreter
used for D1/D3 measurement — the copy lived in scratch and is not evidence, the patch is quoted
verbatim in `scribe-block-probe.txt` §B.
