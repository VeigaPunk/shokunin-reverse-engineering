# R40ConnCounterHistory — cross-round counter-history connector (wave 1, pre-freeze)

**Verdict: DEFECTS FOUND** — the DRAFT round-40 designs fix the r39 fabrication *mechanism* but not
its *kill-control expectation*: I demonstrate live that an oracle-fabricated receipt (no REA run)
has a semantic projection byte-equal to a genuine fresh run, so the draft's C1 kill control
"fabricated from the oracle … must now fail the rerun binding" is false as written. Three further
pre-freeze blockers are grounded in bytes: the draft L1/L2 AVM-layout writer emits big-endian
metadata block-length headers (marker-only standard-BE body), so its carriers cannot pass P40-C1;
the round-39 independent oracle derives endianness from magic only and has no AVM (LE-header) mode;
and the C2 v2 class list adds four classes the v1 generator cannot produce (partial-body-failure
P>0, clean-empty, mixed-symlinks, out-of-domain), with no class-set-equality assertion in the draft
(r34b pattern). Ranked exposure list below; everything is pre-freeze and feeds the freeze.

Axes named (round-40 declared): **coverage** (R40-C1) and **depth** (R40-C2); **calibration** is
touched where the counter's own honesty (rerun not skipped, environment pinned) is the measured
object.

Method: read the DRAFT claims (`plans/round-40-claims.md`), SCORECARD rounds 32–39, QUALITY rows
55–82, the r39 closure (`corpus/lessons/round-39-verifier-spotcheck.md` §5), the r39 wave-1/2
falsification records (`R39W2C1Fabricate.md`, `R39W2C2AxisFit.md`, `R39W2C2TableReview.md`,
`R39C1Controls.md`, `R39AssimAvmCritic.md`), and the round-39 instruments (`tools/round-39/`).
Live probes (all development inputs; no REA/unblob on any round-40 carrier, none built): two genuine
REA 6.5.0 runs on a K1 copy (determinism), an oracle-fabricated K1 receipt compared against a real
run's projection, the draft AVM writer's `--endian avm` output through unblob 26.6.4, and a read of
`sqfs-list.py` for AVM handling. No tool installed/upgraded/removed; no VCS mutation; scratch
`/fast/scratch/hyaku/kaidoku-r40/R40ConnCounterHistory` removed at exit.

---

## 1. Live findings

### 1.1 The semantic projection is deterministic across genuine runs (grounds the rerun compare)

Two REA runs of the K1 carrier copy (sha256 `1cfb6c33…`, pinned round-39 carrier bytes):

```
cd $S && REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 \
  extract-firmware --format json --full-output k1.sqsh out1   # rc 0, 2.8 s
cd $S && REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 \
  extract-firmware --format json --full-output k1.sqsh out2   # rc 0, 2.6 s
```

- Raw envelopes differ only in: `data.evidence_id`, `data.normalized_result.output_directory`,
  `data.parameters.output_directory`, `meta.duration` (field diff, `diffenv.py`). Everything else —
  including `raw_result.execution.stdout.text` (unblob banner), `raw_result.report`,
  `normalized_result.files` (full list with `relative_path`/`sha256`/`size`),
  `extraction_gaps`, `diagnostics[].report.__typename__`, `chunks[].handler/extraction_failed`,
  `coverage`, `published_bytes` — is byte-equal.
- The projection `{operation, provider, chunks[(handler,failed)], gaps[(kind,relpath)],
  files[(relpath,sha256,size)], diag[__typename__], coverage, published_bytes}` is EQUAL across
  the two runs and EQUAL to the committed round-39 K1 `after.json` (`proj2.py`). So freezing those
  fields is grounded; path/id/timing fields must never enter the projection (the r39 wave-2
  "two-run" note, `R39C1Controls.md` §2.4, is confirmed again).

### 1.2 An oracle-fabricated receipt passes the rerun binding — the draft's kill control is false as written

`fab-K1-after.json`: built from frozen lane bytes only (K1 pin, `oracle.tsv` 5 rows, known
handler, known `MaliciousSymlinkRemoved` shape from the committed r39 receipt) — no REA, unblob or
sasquatch process. Its semantic projection (1.1 fields) is **byte-equal** to the genuine fresh run's
projection (`python3 proj2.py fab-K1-after.json env1.json` → `EQUAL`).

Consequence: the draft kill control "a receipt fabricated from the oracle with a re-minted evidence id
**(must now fail the rerun binding)**" would NOT fail. The draft's C1 predicate says the fresh
counter-owned run "yields the same semantic projection as the committed receipt"; an oracle-derived
receipt is content-true, so it matches. The rerun clause rotates the guarantee from "this receipt was
produced by a run" (which no content check can prove — r36 F1/r38 §3) to "the carrier genuinely
extracts to this content" (which is provable and is arguably the right claim). The freeze must
therefore either (a) re-scope the kill control to a **counterfeit** receipt (content ≠ any real run:
invented/extra/missing files, wrong sha256, wrong gap kinds) and state plainly that the rerun
certifies content-equality, not receipt authorship/recency; or (b) adopt the cleaner design the r39
wave-2 already recommended (`R39W2C1Fabricate.md` §5): grade the counter-owned run, keep the
committed receipt only as an optional cross-check of normalized fields (never ids, never
`raw_result`). Under (b) the kill control becomes structural — a counter that cannot run REA, or
skips the run, must exit red.

Residual accepted shortcut: copying a *real previous-round receipt* (r38 K1–K4 are byte-identical to
r39 modulo run identity) re-mints to a passing receipt too — the rerun cannot tell recency. State
this limit in the freeze; it is the content-equality design's boundary.

### 1.3 The draft L1/L2 writer cannot emit genuine AVM-layout carriers

Draft `R40C1AvmWriter/gen-squashfs.py` (dev prototype), `--endian avm` mode: marker is set
(`mkfs == bytes_used == 4469`), but the metadata block-length headers are packed **big-endian**
(the round-39 `pack(e,'H',…)` with `e='avm'` → `'>'`). On my fresh 4469-byte image:
inode_table_start 4192, first metadata header `80a8` → LE decode 10368 (> remaining file bytes,
implausible), BE decode 168. So it is a marker-only standard-BE body — the exact shape
`R39AssimAvmCritic.md` barred from C1 carriers (its `--endian avm` identity finding). Unblob
26.6.4 on it selects `squashfs_v4_be`, drops `-be` (marker holds), and `sasquatch-v4be` fails:
`ExtractCommandFailedReport exit_code=1`, 0 files. The same body with `--endian be` extracts fine
with `-be`.

Consequence: if L1/L2 are built with this writer, P40-C1's rerun cannot pass (0 published files vs
oracle) — the carriers are unreachable before any run, the QUALITY-43 pre-screen class, and the
M38-3/M38-4 "stale premise / harness cannot produce the receipt" family. The freeze needs either a
writer that truly emits little-endian block-length headers under the BE superblock (none exists in
the lane yet), or L1/L2 must be dropped / re-derived from vendor bytes; and every frozen carrier must
be screened with the exact rerun input check before the freeze.

### 1.4 The round-39 oracle reader has no AVM mode

`tools/round-39/sqfs-list.py` decides endianness from the magic alone (`hsqs`→LE, `sqsh`→BE) and
reads metadata block-length headers in that endianness; there is no marker/LE-header special case.
On a genuine AVM-layout carrier (BE superblock, LE block-length headers — the format the claim
defines) it would mis-walk the metadata chain. The "independent pure-Python oracle" must gain an
AVM mode before the freeze, or the oracle for V1/V2/L1/L2 is wrong and the claim is either
unreachable or vacuous.

### 1.5 C2 v2 generator gap

`tools/round-39/heldout-gen.py` RECIPES/DEFAULT_CLASSES contain no `clean-empty`, `mixed-symlinks`,
`partial-body-failure`, or `out-of-domain` recipes (v1 body-failure is `zero-id-table` → P=0 only;
class `version-minor-mismatch` shares the body label). The v2 class list adds all four, 2 envelopes
each, with byte-identical regeneration required. Partial-body-failure with P>0 was measured in
wave 1 on a natural xz mid-stream corruption (`full-be1-xz`, `R39W2C2TableReview.md` D1); that
recipe must be made deterministic and pinned (position from seed) or the class cannot be generated
with the required determinism — a freeze blocker for C2 as much as for C1.

---

## 2. Ranked exposure list (historical class → draft design → cheapest test)

Ranking = recurrence × decisiveness against a coverage/depth verdict × test cost.
"Exposed" = the draft as written can be met by the historical shortcut; "addressed" = structurally
fixed; "partial" = text gestures, mechanism absent from the predicate/counter.

| rank | historical class (lesson/QUALITY) | draft design | exposure | cheapest test (all pre-freeze) |
|---|---|---|---|---|
| 1 | r39 CL5 re-minted fabrication / r36 F1 (QUALITY 78) | C1 rerun clause + kill control "fabricated from the oracle … must fail the rerun" | **EXPOSED — CONFIRMED LIVE (§1.2):** oracle-derived receipt passes the rerun; the kill control cannot fire | already run (seconds). Freeze must re-scope to a counterfeit-receipt control and/or grade the counter-owned run (control b in §1.2) |
| 2 | r34b M34-10 "gate runs no reader" (QUALITY 72) | C1 rerun | **EXPOSED unless implementation is careful:** the rerun is a subprocess; any try/except around it, or a `met_target` computed without the rerun compare, makes the clause decorative | mutant counter: set `REA_UNBLOB_COMMAND=/nonexistent` (rerun subprocess must fail) while a valid committed receipt exists → must exit red; also assert `met_target` is conjunctive with the rerun compare |
| 3 | r38 M38-3/M38-4 stale premise / harness-cannot-produce (QUALITY 43) | L1/L2 carriers "from a writer that emits little-endian block lengths" | **EXPOSED — CONFIRMED LIVE (§1.3):** the only draft writer emits BE headers; its `avm` output fails through unblob with 0 files | build a carrier with the draft writer, run the exact rerun pipeline (unblob only) on it → 0 files, `ExtractCommandFailedReport` (§1.3 already did this) |
| 4 | r34b unregistered classes / floor-dropping (QUALITY 69/70) | C2 held-out: "all N envelopes (2 per class)" | **EXPOSED:** N is derived from the manifest, not from a frozen class registry; a manifest with 11 classes (22→20 envelopes) passes "for all N" | red fixture: 11-class manifest (one class pair dropped) → counter must exit red; same for an enlarged 13-class manifest |
| 5 | r34 size/fixed-slice replay (QUALITY 67; r32 "structure vs shape") | C2 scoring by (label, action) | **EXPOSED in labels-only form:** an interpreter that maps `subject.digest.sha256` → manifest labels (fixture identity: key) reproduces 20/20 without parsing the table | red fixture: subject-digest-lookup interpreter (a few lines) scored by the frozen counter → must exit red; the counter should also assert per-envelope matched rule index and that every table row fires |
| 6 | r36 shadow rows/decoys (QUALITY 77) + r38 stub-at-path (QUALITY 81) | C1 doc bindings (PROVINCE row/cite, SOURCES opened row/used-by, README row, entry) | **EXPOSED:** the draft repeats the r38/r39 binding language; `entry_present` is existence-only, `section()` takes the first match, README stem matching is prefix/substring | port the r38 matrix recipes onto r40 text: decoy duplicate `## Round-40 additions to Core` heading earlier in file; reuse an existing opened SOURCES row; README stem-prefix; one-line stub entry with a bare `source:` line — each must go red |
| 7 | r32 lexical calibration (QUALITY 58) + r39 CL3 cause/action | C2 scored closed-vocabulary action + unique labels | **PARTIAL:** pair-scoring rejects a label-right/action-wrong table (kill list has it), but a table whose actions are correct *by vocabulary co-occurrence* while causes are nonsense still passes (cause unscored — state this limit); duplicate-label refusal must be a parse-time schema error | swap the action cells of two rows (red); duplicate a label across rows (parse refusal); state that cause cells remain unscored (or add them to the pair) |
| 8 | r39 CL1 domain guard | C2 operation/provider guard → `unclassified` | **PARTIAL:** the guard must be a hard precondition in the interpreter, not a table row — a wildcard row labelled `unclassified` cannot express the negation and would swallow in-domain envelopes if ordered last | construct a non-firmware envelope (`operation=analyze_function`, `provider=ghidra`) carrying firmware-shaped `normalized_result` features → must be `unclassified`; and a genuine `extract_firmware`/`unblob` envelope must never hit the guard |
| 9 | r39 CL2 mixed symlinks + CL3 D1/D2 | C2 mixed-symlinks row; partial-body P>0; clean-empty P=0 | **PARTIAL:** rows are drafted but the generator cannot produce the two new P-classes (§1.5); the mixed row order (before escaping) is a cheap check; the loop-symlink vector (S118 recursive branch) will still land in the escaping row with a false cause (D3 residual — decide caveat vs feature) | run the generator for every v2 class twice and `cmp` carriers (byte-identity); feed the K5/K6 feature vector (SR=yes + `unpublished-entry` gaps) → must label mixed, not escaping; loop vector → explicit decision |
| 10 | r39 CL4 post-freeze control inputs (QUALITY 80) | C1/C2 kill controls | **ADDRESSED in text** (control tables/inputs format-validated in the freeze commit) — keep; extend to the new C2 generator classes, the C1 fabrication harness (xpin, oracle/symlink TSVs) and the rerun's own argv | run `freeze-drift.py`-style path/commit check over claims + counters + control generators at the measured revision; replay one control receipt at the freeze revision |
| 11 | r35 coupled counter (M35-1) | C1/C2 separability | **ADDRESSED on paper** (explicit Separability section) — the runtime form is the exposure: C1's rerun at scoring time must not read C2 data, and both must not collide in scratch | cross-fixtures: C1-complete state with zero C2 data (and vice versa) → each counter clean or honestly unevaluable, never failed by the other's absence |
| 12 | — (new, environment) | C1 rerun at scoring time | **EXPOSED:** scoring depends on the live toolchain; `npx -y` may fetch on a cold cache (network), and a PATH shim named `sasquatch-v4be` (or a swapped `~/.local/bin/unblob`) changes what the rerun measures | hash the resolved rea package `package.json`, unblob and sasquatch-v4be bytes at scoring time and refuse on mismatch (QUALITY 39); invoke REA from the pinned package root or warm the cache at the freeze; rerun with a fake `sasquatch-v4be` on PATH → red |

---

## 3. What the draft already fixes (keep)

- The rerun clause itself is the right response to R39-CL5; with the §1.2 re-scope it replaces
  receipt-integrity with content-equality against an independent oracle — strictly stronger than
  r39.
- Freeze-integrity rule (no frozen path touched after freeze; later restore does not un-block;
  exit 2 `frozen_path_changed`) carries from r39 and covers the r38 M38-1/M38-9 classes.
- "Control tables and control receipts' inputs are committed and format-validated in the freeze
  commit" covers QUALITY 80 (r39-CL4); "every score receipt records the counter's exit code" covers
  R39-CL6.
- C2 seed = freeze commit hash + byte-identical regeneration + manifest-first-added order is the
  QUALITY-69 mechanism done right (keep; add the class-set-equality assertion of rank 4).
- Explicit separability section (rank 11).
- Labels unique per row and the closed vocabulary for actions are the right grammar moves (rank 7).

## 4. The one bounded move (connector proposal)

**Before the freeze, decide what the C1 rerun proves and make the kill control match it.** The
cheapest correct package: (i) re-scope the C1 fabrication kill control to a counterfeit receipt
(content ≠ reality) and add the skip-the-rerun mutant control (rank 2), the environment-pin control
(rank 12) and the doc-binding matrix controls (rank 6); (ii) require the L1/L2 writer to emit true
little-endian block-length headers and re-screen every carrier with the exact rerun pipeline before
the freeze (rank 3); (iii) add the C2 class-set-equality and distinct-decisions assertions (rank 4)
and the domain-guard discriminator (rank 8). Everything else in the draft can stand. This is four
decisions, protects both owned axes, and each test costs minutes — the live ones above cost seconds.

## 5. Risks / limits

- The rerun design is judged from the draft text and the round-39 instruments (no round-40 counter
  exists yet); implementation slips are therefore projected, not measured. The §1.2 finding is
  demonstrated, not inferred.
- Determinism was measured on K1 (gzip BE, 5 files) only; [INFERENCE] that the same stable field
  set holds for larger/xz carriers (K6, and vendor members) — freeze the fields from §1.1, which is
  the set the probe proved stable.
- The writer probe used a partially built tree (one `mkdir -p` failure left `bin/run` absent); this
  does not affect the finding (marker, header endianness and extractor failure are independent of
  the missing file).
- Held-out discipline kept: no REA/unblob on any round-40 carrier (none exists), no C2 held-out
  carrier built, no vendor image touched; K1 bytes are the round-39 development copy explicitly
  allowed. `sasquatch-v4be`/unblob untouched; no installs; read-only git.
Artifacts: `proj2.py`, `diffenv.py`, `fab-K1-after.json` (the oracle-fabricated receipt, sha256
`12811793642608df346fa543b60c78bdb9fecc14af015feb1bdac50bac55742c`), `determinism.txt`,
`avm-writer-probe.txt`, `oracle-avm-check.txt`.
## A. Evidence (commands, outputs, exits) — artifacts under
`.ufo/waves/round-40/w1/artifacts/R40ConnCounterHistory/`

```
# 1.1 determinism (dev K1 copy; sha256 1cfb6c33… == round-39 pin)
cd $S && REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 \
  extract-firmware --format json --full-output k1.sqsh out1   # rc 0
cd $S && REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 \
  extract-firmware --format json --full-output k1.sqsh out2   # rc 0
python3 diffenv.py env1.json env2.json   # only evidence_id / output_directory ×2 / duration
python3 proj2.py env1.json env2.json     # EQUAL
python3 proj2.py <committed r39 K1 after.json> env1.json      # EQUAL
# 1.2 fabricated receipt vs real run
python3 (build fab-K1-after.json from oracle.tsv + symlinks + known handler; no REA)
python3 proj2.py fab-K1-after.json env1.json                 # EQUAL
# 1.3 writer probe
python3 …/R40C1AvmWriter/gen-squashfs.py tree dev-avm.sqsh --endian avm --comp gzip
python3 - <<'PY' (superblock: mkfs==bytes_used==4469; hdr 80a8; lenBE 168, lenLE 10368) PY
unblob -v -e ub-avm-dev dev-avm.sqsh   # rc 0; handler squashfs_v4_be; argv NO -be;
                                        # ExtractCommandFailedReport exit_code=1; 0 files
unblob -v -e ub-be-dev dev-be.sqsh      # rc 0; argv WITH -be; files extracted
# 1.4 oracle reader
grep -n "mkfs|bytes_used|avm|marker|endian" tools/round-39/sqfs-list.py   # magic-only endianness
```


Report: `.ufo/waves/round-40/w1/R40ConnCounterHistory.md`
