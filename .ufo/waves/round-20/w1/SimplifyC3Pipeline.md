# C3 pipeline — YAGNI review (round 20, w1)

Seat: `KaidokuR20.SimplifyC3Pipeline-2` (read-only). Base: `14f0260ad319ecc26994381b2415d5a999003375`
(`refs/heads/main`, per contract). First written 2026-10-20T17:54:14-03:00, last updated
2026-10-20T18:04:23-03:00 (clock at each write).
Scope: the six C3 artifacts assigned by W20 items 20–25 — `swiss-misread-v2.py`, `first-failure-extract.py`,
`compare-first-failure.py`, `retro-v2.py`, `run-carriers.sh`, `measure.py` — plus the freeze producer they
depend on (`gen-predictions.py`). Observation vs inference is labelled per claim.

State note: the C3 artifacts were absent at 17:46 (`W20/tools/`), landed 17:57–18:00 while this review ran, and
were then checked against their bytes (sha256 in §5). The lane working tree also changed as D1–D6 patches landed
(e.g. `.ufo/waves/round-17/tools/receipt-validate.py`, `.ufo/gates/*`); those are not this seat's writes. Line
anchors were taken at the bytes read; `receipt-validate.py:1142` in particular may shift with D6d. No C3 finding
depends on the working-tree state of any of those D-item files.

## Axes

1. **Calibration** — the forecast must be expressible in the log's vocabulary, on a non-vacuous set, with
   a denominator that cannot be narrowed after the fact.
2. **Coverage** — labels that actually freeze, bind and compare (N ≥ 8, receipt-validated, freeze-blob-identical).
3. **Depth** — the variadic mechanism and the first-failure site are carried, without adding fields nothing compares.
4. **Deletion** — every artifact must be the only place its law lives; no second parser, no second comparator,
   no sums file that duplicates a commit.

## 1. Minimum set: 5 tools (4 C3 + D3's guard) + driver + generator; 3 verbs

| Verb | Artifact | Why it cannot be deleted or reused as-is |
|---|---|---|
| freeze | `gen-predictions.py` (R19 copy) | must write the v2 blob, the forecast, and the freeze set; R19's 133 lines are ~75 % reusable |
| freeze (engine) | `swiss-misread-v2.py` | mask + first-failure predicate; **delivered 1,899 lines, 62 insertions / 9 deletions over R18** (§2.1, §5) |
| bind | `runs/<label>/receipt.json` via unchanged `carrier-run.py` + `receipt-validate.py --require-mid-maps` | already binds carrier/prediction/tool bytes by sha256 (`pins_pre`/`pins_post`) |
| bind (carrier) | `carrier-guard.py check` per label (D3, not mine) | exec-bit/ctime/content refusal before each run |
| compare (evidence) | `first-failure-extract.py` | new: the association "failure record → its `Caused by` read" does not exist in `log-extract.py` output (§2.4) |
| compare (decision) | `compare-first-failure.py` | contract fixes it as a separate tool (`contract.md:79-80`); it must *import* the extractor, never re-parse (§4) |
| run | `run-carriers.sh` | W19 copy + 4 hunks (§2.3); R19/R18 drivers are the only proven run law |
| measure | `measure.py` | C1/C2 blocks + binding block reusable; only `c3` is new (§2.5) |
| retro | `retro-v2.py` as a **thin batch driver only** — shells `compare-first-failure` per label; retained table is the artifact | delivered 258 l. with no matcher; a second matching law here would be the one thing to delete (§3, D-1) |

Minimum: the six assigned files are all justified, but their content is 4 rebuilt tools (v2, extract, compare,
measure), 1 batch driver with no logic of its own (retro), 1 copied run driver (4 hunks), and 1 generator;
D3's `carrier-guard.py` supplies the only extra executable. Genuine remaining deletions are D-2 (4 tokens),
D-4 (one unread file), D-9 (3 lines), the predicate breadth in D-6, and the selftest stubs (two envelope cases).

## 2. Reuse ledger (measured)

### 2.1 W18 emulator, unchanged body

`.ufo/waves/round-18/tools/swiss-misread.py` is 1,846 lines. The **mask alone** is 6 changed lines in 2 hunks
(`:937-939` `_markup_func`, `:1044-1046` `_type_refs`), and the inherited selftest still prints
`SELFTEST: CLEAN cases=15` (exit 0, §6 cmd 5). [OBS] The delivered v2 is 1,899 lines: 62 insertions / 9 deletions
across 10 hunks, all additive to R18 (helper, predicate, projection, CLI defaults, 2 cases). [OBS, §5]

The inherited 15 cases never build a `func` type — `_fixture()` (`:1673-1745`) creates one map type and a name
chain only — so the mask is **untested by inheritance**. The new `variadic_masked` case is therefore not YAGNI
padding; the other required case (`first_failure_shape`) is interface conformance. [OBS from `_fixture` body]

The mask is behaviourally decisive, not cosmetic. Vet's v1 walk fails at `index 1801722468838924630` via
`func.param[7]`; the masked walk fails at `13902080` via `type@0x73f4a0 → elem` (§6 cmd 7). [OBS]

**Copy, not wrapper.** A wrapper subclassing `Machine`/rebinding `_type_refs` would be ~25 lines, but
`analyse()` constructs `Machine` directly (`:1303`) and the prediction's `emulator_sha256` would name the wrapper,
not the 1,846-line body it depends on. The copy keeps the base literally diffable and attributable. [INF]

### 2.2 W17 run mechanics, unchanged

`carrier-run.py` (756 l.), `pins.py` (298 l.) unchanged. Receipts record absolute-path → `{sha256,size,mtime_ns}`
for 152 pins (`runs/pass2/t1250-vet/receipt.json` `pins_pre.entries`), so binding is already content-addressed. [OBS]
`receipt-validate.py` (1,167 l.) is used unchanged *by C3* for the binding gate (`--require-mid-maps` exists,
`:1142`); D6d's argv-token correction is a separate lane item and does not alter that gate's semantics. [OBS]

### 2.3 W19 run driver — 4 hunks, ~300/356 lines untouched

`.ufo/waves/round-19/run-carriers.sh` (356 l.) already derives `W` from its own location (`:45`), so a copy at
`W20/run-carriers.sh` writes `W20/runs` and reads `W20/predictions` with no path edit. `SELFTEST: CLEAN cases=29`
(exit 0, §6 cmd 10). Required deltas (tasking item 24):

1. `:52` default `SWISS_MISREAD` → `$W/tools/swiss-misread-v2.py` (otherwise the run pins v1; the prediction blob
   still names v2, but `producer.json` would misattribute the engine);
2. `:57` `W17_TOOLS` drops `log-extract.py` and `compare.py` (5 → 3, see D-2);
3. `:346-347` replace the `log-extract` + `compare.py` pair with `first-failure-extract` + `compare-first-failure`
   (two invocations → two invocations; no new per-label work);
4. insert the per-label `carrier-guard.py check` (tasking item 24) and the `--dry-run` branch before the run loop.
   `:291` still says "W19/runs" — cosmetic, one word.

Everything else (TSV law, label regex, frozen-sha gate, producer.json, `rm -rf`/out-dir guard, pin set) is unchanged.
The selftest stubs `:91-108` must be renamed/rewritten with the two new tools; its 29 assertions otherwise carry over.
**Delivered:** 451 lines, hunks 1–4 in place (`:21-24` tools, guard call, `--dry-run`, compare at `:438-441`);
only D-2's pin-set trim is missing. [OBS, §5]

### 2.4 `first-failure-extract` is genuinely new — but only ~150 lines [INF]

`log-extract.py` (679 l.) cannot answer "the first failure": `parse_log` appends EOF/invalid-index reads as
positionless values (`:187`, `:190`) and dedupes `symbol_analysis_failures` (`:199`, `:303`), so the `Caused by:`
read can no longer be attributed to the failure record that precedes it. Observed in the target log: the failure
record is `ghidra.log:186` and its cause is `:229` — 43 lines later. [OBS]
Feed-forward law to reuse **by copying the three constants** (`LINE_RE`, `EOF_READ_RE`, `INVALID_INDEX_RE`,
`:90`, `:113-114`): importing W17 `log-extract.py` at runtime would make a REV-materialised extractor read live
bytes and break revision purity (`measure` materialises only the round's tools dir, `measure.py:148-190`). [INF from measure]

### 2.5 W19 measure — keep c1/c2 + binding, replace only c3

1,393 lines; reusable verbatim: `_git`/`_resolve`/`_tree`/`_materialize`/`_import_scope`/`_load_module`/`_invoke`/
`_run_tool` (`:117-298`), the fixture harness (`:935-1360`), and the binding block (`:655-670`) which already
materialises `receipt-validate.py` + `pins.py` from REV and runs `--require-mid-maps` per label. Replace
`_claim_c3` (`:581-700`) and `RUNS_RE`/`SUMS` constants; add `--freeze <hash>`. Also reuse `_prediction_entries`
(`:500-533`) — note it reads **only** `carrier.sha256`, which is the anchor for D-2/D-3. [OBS]
**Delivered:** 671 lines with a generic `_claim_tool` for c1/c2 (`:30-31`, `:455-456`); c3 uses the all-label
denominator and blob-OID freeze equality (`:380-390`, `:414`), so the D-only-denominator hazard is closed. [OBS, §5]

### 2.6 Freeze generator

`gen-predictions.py` (133 l.) reusable for the freeze loop, `decision-rule.json` skeleton and blob writes (`:45-110`).
Drop the `predict.py`/`buildinfo-probe.py` calls (`:64-75`), because W20 sets `extra_expectations: none` and
nothing in the W20 path reads `expected.*` (D-3).
**Delivered:** 185 lines; no `predict.py`; the probe stays for eligibility and the sha self-check (`:104-118`);
`extra_expectations: []`; `SHA256SUMS` still written (D-4); no empty-D refusal (D-9). [OBS, §5]

## 3. Deletions (each with a named refutation)

- **D-1 `retro-v2.py` → batch only.** It must not re-implement matching. Either (a) a 20-line driver that shells
  `compare-first-failure` per label and writes one JSON, or (b) drop the file entirely and retain the table from a
  documented 8-iteration loop. Pick (a) only because the falsifier names the *retained* retro
  (`claims.json:39`).
  **Delivered status: satisfied.** `retro-v2.py` (258 l.) shells `compare-first-failure.py` per label, holds no
  matcher, and emits a CSV. Two cheap additions: an envelope-shaped stub (its current stub prints the bare
  object, so it cannot catch the contract break in §5), and a report line naming `decision-rule.json`'s
  `emulator.sha256` so the table is tied to the frozen bytes. [OBS, §5]
- **D-2 `log-extract.py` + `compare.py` leave the W20 run path.** W20 compares `first_failure` only; the two
  artifacts per label (`observation.json`, `compare.json`) become unread. `compare.py` also cannot consume the new
  prediction shape: `load_inputs` requires `prediction.expected` to be an object (`compare.py:73-93`). Keep both
  files untouched as W17 evidence.
  **Delivered status: half taken.** The run loop calls only `compare-first-failure` (`run-carriers.sh:438-441`),
  but `W17_TOOLS` (`:28`) still lists both and preflight still requires them (`:218-219`), so every run pins and
  hashes two tools it never executes. Delete the two names at `:28` and the two paths at `:218-219`. [OBS, §5]
- **D-3 `predict.py` is gone; keep the buildinfo probe.** The delivered generator calls no `predict.py`; the probe
  remains for eligibility and the sha self-check (`gen-predictions.py:104-118`), which is a real use, not route
  ballast. The route/`expected.*` fields are absent from the delivered prediction blob and `extra_expectations`
  is `[]` (`:158`). No further change. [OBS, §5]
- **D-4 drop `predictions/SHA256SUMS` and measure's `_sums_labels` (`:534-557`).** The C3 falsifier is
  "any prediction blob differs from the freeze commit" (`claims.json:39`) — Git *is* the identity; `run-carriers`
  reads only the TSV sha column (`:9`, `:284-290`). R19 already carried this as an unread artifact
  (`w2/SkillRegistryNew.md:17`). Dropping it removes one generated file and one selftest family.
  **Delivered status: open.** `gen-predictions.py:70-72` still writes `predictions/SHA256SUMS`; neither
  `measure.py` nor `run-carriers.sh` mentions it (grep exit 1). One generated file with zero readers. [OBS, §5]
- **D-5 `decision-rule.json` holds the rule and the D set only.** R19 embedded a per-label `table` with full read
  lists (`gen-predictions.py:120-123`), duplicating 340 KB of prediction payload (9 files; vet alone 57,551 B).
  The delivered `table` (`gen-predictions.py:176`) is a compact per-label forecast summary
  (`label/go_version/h1/h0/d`), not the read lists — acceptable. No change. [OBS, §5]
- **D-6 the v2 predicate is part of the minimum, not a refinement.** See §5 — without it the forecast is red by
  construction on 3/8 retro labels. **Delivered status: narrow.** The loop continues only on `invalid_data`
  (`swiss-misread-v2.py:1335-1336`), and `first_failure_record` projects any remaining kind (`:1463-1471`), so an
  `unmapped`/`invalid_length` stop becomes a failure no log can express. Extend the continue-set to every kind
  except `past_eof`/`invalid_index`; 8/8 today, held-out risk otherwise. [OBS, §5]
- **D-7 CLI is contract-shaped in the delivered tool.** `swiss-misread-v2.py:1867-1872` registers `--carrier`,
  `--label`, `--snapshot-dir`, `--go-version`, `--selftest`, `--debug`; the generator calls it with
  `--snapshot-dir` and `--label` (`gen-predictions.py:124-126`). No alias or further option is needed. [OBS, §5]
- **D-8 make `markup_type`'s trail pop exception-safe.** `self.trail.pop()` is skipped when the raise at `:852`
  unwinds, and the raise at `:848` happens after `trail.append` (`:845`). With a single fatal stop this is benign.
  **Delivered status: open and now reachable** — the `continue` at `:1335-1336` leaves the failed path on
  `machine.trail`, so a later fatal failure's `path` (kept in `walk`, not in `first_failure`) is polluted. Clear
  the trail on each non-fatal continue, or wrap the pop. [OBS from control flow]
- **D-9 refuse to freeze an empty D set.** `gen-predictions.py:167-175` computes `diagnostic` and writes every
  blob regardless. An all-silent 10/10 freeze would pass every gate while forecasting nothing. Exit 2 on
  `not diagnostic` before the first write; it is the claim's only vacuity guard. [OBS, §5]

## 4. What must NOT be cut

- **Extract/compare split.** The extractor's output is the retained evidence (truth table over 15 R18 + 16 R19
  logs: 8 pass1, 8 pass2); the comparator decides. Collapsing them into one file would be smaller but would let
  the judge re-extract with different bytes. The split is contract-imposed (`contract.md:79-80`), so it is not
  YAGNI debt.
- **`receipt-validate --require-mid-maps`** as the binding oracle — do not re-implement mid-map checks in measure.
- **Freeze-blob equality in measure** (`--freeze <hash>`), not just a 64-hex `carrier.sha256`; R19's frozen test was
  the weaker one (`measure.py:519-531`).

## 5. Calibration: the trap this pipeline can fall into (measured)

The mask alone is not enough. R18's walk aborts on **any** `ReadError` (`:1310-1334`), including `invalid_data`,
which is the emulator's own "unsupported Go type" raise (`:852`) — Ghidra does not abort there; it logs a
`GoTypeManager` WARN and continues (observed at `t1250-compile/.../ghidra.log:338-340`, followed by a completed
analysis). The tool's own docstring (`swiss-misread.py:63-70`) says only `past_eof` reproduces Ghidra's EOF text;
R19's bound log confirms `invalid_index` does too (`Invalid index: 13902080`). [OBS]

Measured comparison of the two predicates against the 8 bound R19 logs (`--require-mid-maps` on all 8 pass2
receipts: exit 0, `counts {valid: 8, invalid: 0, unreadable: 0}`; only vet fails):

| label | naive (break on any `ReadError`) h1 | corrected (break only on `past_eof`/`invalid_index`) h1 | bound log |
|---|---|---|---|
| go | `invalid_data@12209568` | null | silent |
| gofmt | `invalid_data@5730496` | null | silent |
| asm | null | null | silent |
| cgo | null | null | silent |
| compile | `invalid_data@15524544` | null | silent (`:347` NPE is `AnalysisTaskWrapper`, not `Golang*`) |
| cover | null | null | silent |
| preprofile | null | null | silent |
| vet | `invalid_index@13902080` | `invalid_index@13902080` | `:186` + `Caused by … Invalid index: 13902080` at `:229` |

[OBS, probe] Naive all-label result 5/8; corrected 8/8. The naive run also makes D = {vet} (the `invalid_data`
labels fail both h1 and h0), so a **D-only denominator reads 1/1** while three false forecasts sit outside it.
The cheaper variant — keep the break, emit null for non-loggable kinds — also scores 8/8 on the retro but is
unsound: a carrier whose first stop is `invalid_data` and whose walk would later hit a real `Invalid index` would
be forecast silent. Only the held-out set distinguishes the variants; take the sound one (continue). [INF]
Two rules follow, both cheap:

1. **Denominator = every frozen label with a bound log**, never the D set. D is reported for discrimination only.
2. **Refuse to freeze when D is empty** (exit 2 in the generator). "All silent" otherwise scores 10/10 while
   forecasting nothing — the exact vacuity the W20 falsifier prompt targets.

Retro status: the 8/8 above is **post-hoc** (R19 outcomes were known and the probe was tuned on them); it is not
prediction evidence and must be labelled as such in the artifact. The held-out test is the 10 go1.24.6 carriers.
I deliberately did **not** run `analyse()` on any go1.24.6 carrier; I only censused parser eligibility (§6 cmd 9).

`phase`: the two sides use different vocabularies (prediction = failing site, e.g. `func.param`/`map.Elem` from
`machine.trail`; log = analyzer stage from the stack). Never compare it for equality. Use it once: a null
prediction plus a non-null log failure whose stage is not the markup walk (`GolangSymbolAnalyzer.added`) is
**exit 2 unevaluable**, not a mismatch. That is the only place the field earns its slot. [INF]

### Delivered state (checked against bytes)

Sizes: `swiss-misread-v2.py` 1,899 / `first-failure-extract.py` 316 / `compare-first-failure.py` 178 /
`retro-v2.py` 258; `measure.py` 671, `run-carriers.sh` 451, `gen-predictions.py` 185.
Selftests: 17 / 4 / 6 / 5 cases, all `CLEAN`, exit 0 (§6 cmd 17). [OBS]

End-to-end on the 8 bound R19 logs with the current bytes: **8/8 match** — 7 both-null, vet
`invalid_index@13902080` (prediction `va 7599264`, `phase markup_walk`; observation `va null`, `phase markup`)
(§6 cmd 18). The 7 nulls are vacuous agreement, which is why the D-non-empty rule (D-9) matters. [OBS]

A transient contract break, now fixed: the 17:57 comparator treated the extractor's envelope as the failure
object and exited 2 on every log (`extractor result: kind must be a non-empty string`); the 18:00:23 bytes unwrap
`observed["first_failure"]` (`compare-first-failure.py:72-77`). Both `compare` and `retro` selftests still stub
the **bare** shape, so neither can catch this class — one envelope-shaped case in each is the substance check.
[OBS]

Compile log through the extractor: `first_failure: null`, `other_errors: 1` = the `AnalysisTaskWrapper` NPE at
line 347. The item-21 separation works (§6 cmd 19). [OBS]

Tool bytes at review close (sha256): v2 `a4810430…cf1e`, extract `aa4372b2…e485`, compare `44150d13…5121f`,
retro `57d95bf0…659f`. Any re-run must bind the retro table to `decision-rule.json`'s `emulator.sha256`; the
table alone does not name the bytes that produced it.

## 6. Commands run (exact, with exits)

```
 1 ls .ufo/waves/round-20/ .ufo/waves/round-20/tools/            -> exit 2 (tools/ absent at review time)
 2 git diff --stat 8a8da7e refs/heads/main -- W18/run-carriers.sh W19/run-carriers.sh -> exit 0 (+356, new file)
 3 diff -u W18/run-carriers.sh W19/run-carriers.sh              -> exit 0
 4 python3 log scan over runs/pass2/*/logs/*/ghidra.log         -> exit 0 (8 logs: 7 with 0 failures, vet 1)
 5 python3 -I -B <masked copy> --selftest                       -> SELFTEST: CLEAN cases=15, exit 0
 6 diff mask-only copy | grep -c '^[+-][^+-]'                   -> 6 changed lines, exit 0
 7 masked copy on go/vet/compile (--carrier, byte reading)      -> exit 0 each
 8 python3 log lines: vet :186/:229, compile :338-340/:347      -> exit 0
 9 parse_buildinfo census on 10 go1.24.6 carriers               -> eligible=10/10, exit 0
10 bash .ufo/waves/round-19/run-carriers.sh --selftest          -> SELFTEST: CLEAN cases=29, exit 0
11 python3 prediction summary (walk index/kind per label)       -> exit 0
12 naive mask-only probe on 8 go1.25.0 labels                   -> exit 0 (table §5)
13 corrected-predicate probe on 8 go1.25.0 labels               -> exit 0 (8/8 vs logs)
14 python3 -I -B W17/tools/receipt-validate.py --require-mid-maps \
     $(find runs/pass2 -maxdepth 2 -name receipt.json)           -> exit 0, counts {valid:8, invalid:0, unreadable:0}
15 git status --porcelain --untracked-files=no (at 17:54)    -> empty, exit 0 (D-item patches landed later)
16 wc -l W20 tools (v2 1899, extract 316, compare 178, retro 258) -> exit 0
17 python3 -I -B <each W20 C3 tool> --selftest                  -> CLEAN 17/4/6/5, exit 0 each
18 v2 + compare-first-failure on 8 labels x bound logs          -> 8/8 match, exit 0 per label
19 first-failure-extract on compile log                         -> first_failure null, other_errors 1 (line 347), exit 0
20 first-failure-extract on vet log                             -> invalid_index 13902080, lines 186/229, exit 0
21 sha256sum W20 C3 tools                                       -> (hashes in §5), exit 0
```

Correction of my own first pass: a raw `b"\xff Go buildinf:"` scan reported `link` as having build info; the real
parser returns `(None,None,None)` because the magic at `3461224` is a **string constant inside the linker**
(`flags=117, ptrsz=114`). Both `go-1.25.0/.../link` and `go-1.24.6/.../link` fail this way. The R19 exclusion
(`decision-rule.json` `excluded`) is therefore a parser limit, correctly recorded; the W20 list omits `link`, and
all 10 listed go1.24.6 carriers parse. [OBS]

Coverage facts for the builder: all 10 W20 candidates carry `map.group[` strings and no `GOEXPERIMENT=noswissmap`
(so `true_kind=swiss`); R19 left 15 round-18 logs for extractor coverage; go1.25.0 has no `pprof`/`trace`, which is
why R19 had 8 labels and W20 must reach its N from the 1.24.6 set. [OBS]

## 7. Tradeoffs

- The v2 copy duplicates 1,846 lines. Accepted: the delivered diff is 62 insertions / 9 deletions (mask helper at
  both sites, predicate, projection, CLI, 2 cases), and the freeze blob can name both the copy and its base
  (`emulator` + `emulator_sha256`).
- Keeping every r18 field costs ~340 KB of predictions. Accepted as tasking-bound (`item 20`), but measure must not
  copy it into `decision-rule.json` (D-5).
- `run-carriers.sh` stays a copy rather than a symlink because item 24's guard/dry-run/compare changes make a real
  file unavoidable; the copy is 300 lines of proven driver for 4 hunks.
- The retro cannot be evidence of calibration, only of implementation consistency. Treat 8/8 as a build check.

No tool was installed or upgraded for this review. This seat wrote no lane file other than this report; it created
no patch and made no tracked modification.
