# RevengerR34History — what the retained r34 winner memorized, and what the seven gate classes actually cover

Seat: `L1Kaidoku34-2.RevengerR34History` · wave r34b/w1 · read-only verification + bounded attack.
Lane tip before wave: `c79bbe7b` (freeze), base `ec3125ad` (claims.json). All runs on a scratch copy
`/fast/scratch/hyaku/kaidoku-r34b/w1/RevengerR34History/lane`; no lane file was written or executed.
Tooling: none installed or updated (nothing needed; python3 = `/usr/bin/python3`, stdlib only).

---

## 1. Reconstructed contract of the frozen instrument (R34-C2)

`tools/round-34/replay-gate.py` is a *witness runner*, not a family test. Its whole predicate is:

```
REPLAY_GATE_CLEAN  exit 0  iff  positive_control.met_target  AND  no registered shortcut.met_target
REPLAY_GATE_REFUSED exit 2 iff  any registered shortcut.met_target
REPLAY_GATE_UNEVALUABLE exit 3 on any config/run/field defect
```
(`evaluate()`, replay-gate.py — `over = sorted(row["class"] for row in findings if row["met_target"]
and row["class"] != positive_spec["class"])`).

Consequences that fix the semantics of "clean":
- CLEAN is quantified over **the config's shortcut list**, never over shortcut *families*.
- The positive control is accepted on the strength of a class *string* (`"structural"`); nothing
  inspects the reader's source, imports, or bytes.
- `MIN_SHORTCUTS = 3` is the gate's only floor on the registry; the c2 counter's `green_clean` clause
  needs only `gate exit 0` + `verdict CLEAN`, and it records `shortcuts_below_target` without scoring it.
  Refusal of a class is evidence only about the *witness file* that implements it.

Pinned identity verified by sha256 against `r34b/claims.json:pins` (all match, run 2026-10-25T07:19:03Z):
`replay-gate.py 8fa94b23…`, `c2-shortcut-gate-counter.py 41d59703…`, `gate-config-mini.json 4483f385…`,
`gate-config-naive.json 72b12941…`, `mini-counter.py 43ef669f…`, 8 fixture hashes, 9 reader hashes,
`mini-fix/build.py c6718051…`, `mini-fix/expected.json 5ebb5349…`, `mini-fix/spec.json 3cb59080…`.

---

## 2. What the retained r34 winning control memorized

Source: `.ufo/waves/round-34/w1/CtlLabels-files/size_lookup.pristine.py`
(sha256 `c68511f7bc2d10b005847139a5ef70331f50634a84d3d1ae63c762c570460b22`, identical to
`claim-stop.json:control_sha256`). Its imports are exactly `json, os, sys` — **no `struct`**, so it
cannot parse an ELF header, section table, PT_DYNAMIC, `.dynstr`, `.gnu.version_r` or a verneed chain.
Structure-blindness is a property of the import surface, not of a claim.

Three memorized dimensions, plus a fourth "nothing":

| dimension | mechanism (quoted from the pristine source) |
|---|---|
| **KEY** | `os.fstat(descriptor).st_size` → exact dict lookup into `TEMPLATES` (`descriptor = os.open(...)`, `size = os.fstat(descriptor).st_size`, `spec = TEMPLATES[size]`). 12 sizes, all distinct. |
| **SLICES** | 395 pre-baked `(offset, length)` pairs; `os.pread(descriptor, length, offset).decode("ascii")` per name. Absolute file offsets, exact byte lengths, ASCII only. |
| **ASSOCIATION** | a static per-size table: file order, per-file version order, and every `flags` / `other` / `hash` scalar as a literal; the *only* thing that moves through a slice is the string. `versions.sort(key=(name, other))`, `needed.sort(key=file)`. |
| **NOT memorized / not read** | all structural metadata, all bytes outside the 395 slices, any name↔record relation. |

Independent recomputation of the table (AST-eval of `TEMPLATES`, not a control run):

```
    size slices  bytes files records      size slices  bytes files records
   14416      5     58     1       4    747400      0      0     0       0
   43320      9     96     1       8   1097344    100   1978    61      77
   96992     19    181     2      17   1195144     17    176     1      16
  153776     61    829     3      58   2939928     27    276     4      25
  174032     48    901    25      34   ----------------------------------
  194992     51    675     4      47   TOTAL: 12 sizes, 395 slices,
  223536     13    142     2      11          5741 bytes, 107 files,
  448920     45    429     3      42          339 version records
```

This reproduces, digit for digit, the receipt's `size-summary.json:runtime_reads` ("395 fixed-position
exact-length ASCII string slices, 5741 bytes total across twelve carriers per schedule; e12 reads zero
content") and the per-carrier diagnostics in `size-pristine.receipt.json:schedule_inspection`
(e.g. 43320→9/96, 174032→48/901, 2939928→27/276, 747400→absent). Runtime identity is
`input size only; all twelve frozen sizes unique` (`size-summary.json:runtime_identity`).

Why it won the r34 surface: the counter's opacity perturbation renames the *path*
(`version-needs-counter.py:120`, `opaque-<secrets.token_hex(12)>.data`). Path renaming is orthogonal to
a size key, and the fixed slices address the copy's preserved bytes. Both schedules matched 12/12
(`size-summary.json:runs.pristine`, `schedules.0/1`, `translated_inputs: 11`).
`claim-stop.json:reason` states the same: *"Size uniquely identifies the fixture; fixed absolute name
slices adapt to randomized string-table naming while every scalar and record topology is memorized."*

Precise family, for the rest of this report:
**F = (key = input size) ∘ (extraction = fixed absolute byte slices) ∘ (association = memorized static
table)**. Its weakness is not any one of those; it is that *all three* are invariant under the
counter's perturbation.

---

## 3. The gate's green surface and its perturbation model

`mini-fix/build.py` + `mini-counter.py`. Eight 512-byte fixtures, `MREC` v1, `records_off = 16` for all,
`names_off` ∈ {24,32,40,48,56,64}, counts {1,2,3,4,5,6}, 25 records total, and — build.py's own words —
*"Names are unique across the set"*. Verified programmatically: `records_total=25 names_total=25
names_unique=25`.

The counter's only perturbation (`permute()`, `score()`):

| perturbed | preserved |
|---|---|
| order of the NUL-terminated name pool | input size (512 for all eight) |
| the u16 `name_off` field of every record (rewritten to the new pool offset) | magic, version, `count`, `records_off`, `names_off` |
| the path basename (`opaque-<sha256(transformed)[:20]>.data`) | every `flags` and `value` byte |
| | every name string, and the record order |
| | the whole transformed byte string itself (fixed seed, see D2) |

The seed is a hard-coded default (`mini-counter.py:139`, `--seed kaidoku-r34-mini-v1`), and the gate's
counter argv never overrides it (`gate-config-mini.json:counter.argv`). Two independent runs of the same
reader produce byte-identical `transformed_sha256` rows (2026-10-25T07:22:32Z).

So the perturbation is **one-dimensional**: it moves the *name→record index* and the *name*. Everything
that could identify a fixture or a record is held constant.

---

## 4. Baseline reproduction (independent, scratch copy)

| # | command (cwd = scratch `lane/`) | UTC | exit | observed |
|---|---|---|---|---|
| R1 | `python3 -I -B tools/round-34/replay-gate.py --selftest` | 07:19:14Z | 0 | 12 cases, `failures: 0`, `mutants_killed: 3` |
| R2 | `… replay-gate.py --root . --config tools/round-34/gate-config-mini.json` | 07:19:15Z | 0 | `REPLAY_GATE_CLEAN … shortcuts_below_target=7` |
| R3 | `… replay-gate.py --root . --config tools/round-34/gate-config-naive.json` | 07:19:16Z | 2 | `REPLAY_GATE_REFUSED … over=label-memorization` |

Per-class scores from R2 (receipt `out/gate-mini.json`):

| class | matched/8 | refused? |
|---|---|---|
| structural (positive) | 8 | meets |
| all-false | 0 | yes |
| size-keyed | **1** | yes |
| fixed-slice | 0 | yes |
| digest-keyed | 0 | yes |
| string-scan | 0 | yes |
| record-order-replay | 0 | yes |
| label-memorization | 0 | yes |

The claim's instrument-level target is therefore reproduced exactly (`selftest_failures=0`,
`mutants_killed=3`, red REFUSED on `label-memorization`, green CLEAN with positive 8). **C2 passes as
written.** Everything below is about what that pass does *not* mean.

The red/green contrast is narrower than it looks: both configs register the *same seven* reader files;
the only change is the counter (`naive-counter.py` hands the reader each fixture at its own path with its
own bytes, no permutation, no rename). Under the red counter exactly one row flips — `label-memorization`
0 → 8 — and the other six stay at 0,1,0,0,0,0. So the pair "red refused, green clean" demonstrates that
path identity is a reachable key; it demonstrates nothing about the six classes whose scores never moved.

---

## 5. Coverage matrix: does class C cover family F?

Coverage defined strictly, so the answer is falsifiable:
**C covers F** iff (i) `W_C` is refused, **and** (ii) a faithful re-expression of F through C's own
mechanism is also refused *for that mechanism's reason*. Otherwise C only *nominally registers* F.

Every "faithful variant" below is a reader I wrote in scratch and scored with the pinned counter
(`mini-counter.py --root . --control-reader <reader>`), same predicate, same eight fixtures.

| # | class (registered) | witness /8 | faithful F-variant through this class | /8 | verdict |
|---|---|---|---|---|---|
| 1 | `all-false` | 0 | none — emits `{"records":[]}` for every input | — | **NOT COVERING** (guaranteed-zero floor filler: no fixture can have an empty expected set, because `decode_fixture()` raises `Unevaluable("fixture_header")` on `count == 0`) |
| 2 | `size-keyed` | **1** | `readers/retained_size_fixed_slice.py` (exact port of F: `st_size` key + absolute `pread` slices + memorized topology) | **0** | **COVERS the key dimension, degenerately.** All eight fixtures are 512 bytes, so the size key space collapses to 1 and the class can match at most one fixture (it matches alpha). This certifies the *inverse* of F's precondition: F worked because the real set had 12 unique sizes. Coverage is not transportable to the condition that produced the failure. |
| 3 | `fixed-slice` | 0 | same port (`retained_size_fixed_slice.py`) — the slice dimension alone | 0 | **COVERS, genuinely.** Pool permutation moves the strings away from the memorized absolute offsets. This is the only class that defeats a real dimension of F. |
| 4 | `digest-keyed` | 0 | `readers/digest_keyed_full.py` (sha256 whole file, 8-hex table) | **8** | **NOT COVERING (vacuous witness).** `digest_keyed.py` bakes `"e1c4d1d5"`, a digest that never occurs. Because the transform is seeded deterministically (D2), the transformed bytes are constants; a real digest table wins outright. |
| 5 | `string-scan` | 0 | F memorizes `flags`/`value`; string-scan emits `flags=0, value=0` for every printable run | — | **NOT COVERING** (filler). It is refused because every fixture contains at least one non-zero scalar, not because the family is tested. |
| 6 | `record-order-replay` | 0 | `readers/invariant_signature.py` (key = `count` + ordered `(flags,value)` vector; memorized answer) | **8** | **NOT COVERING (mis-specified witness).** The witness is killed because `name_off` is *rewritten* to pool offsets ≥ `len(NAMES)=8`, not because replay by order is defeated. Record order and every scalar are preserved by the perturbation. |
| 7 | `label-memorization` | 0 | `readers/opaque_basename.py` (key = basename) | **8** | **NOT COVERING for identity keyed on the counter's own label.** The naive witness keys on fixture basenames; the counter's substitute name is `sha256(transformed)[:20]`, a stable function of the bytes. The class covers literal labels only. |

Net, against F: **2 of 7 classes touch a dimension of F (one only degenerately), 3 are vacuous
witnesses, 2 are guaranteed-irrelevant fillers.** No class touches the dimension F actually leans on —
the **memorized association** (record topology + 1 017 memorized scalars embedded in a static table).

Key-space arithmetic on the green surface makes the same point independently:

| key function | distinct values over 8 fixtures | measured matched |
|---|---|---|
| size | 1 (512 ×8) | 1 (`size_keyed`) |
| record count | 6 (counts 3,1,2,1,3,5,6,4) | 6 (`readers/count_keyed.py`) |
| ordered `(flags,value)` vector | 8 | 8 (`invariant_signature`) |
| name vocabulary (set) | 8 | 8 (`name_vocabulary`) |
| whole-file digest / basename | 8 | 8 (`digest_keyed_full`, `opaque_basename`) |

---

## 6. The family that still evades all seven

**Preserved-invariant replay (PIR):** a reader whose key is any function of the bytes the perturbation
provably leaves untouched — `count`, the ordered `(flags, value)` vector, record order, the name
vocabulary, and (because the seed is fixed) the whole transformed byte string or its generated
basename — carrying a memorized answer table, and never resolving `name_off`.

Instances, all 8/8 on the gate's own surface (all run 2026-10-25T07:20:15–07:20:16Z, exit 0):

| reader (scratch) | memorized object | /8 |
|---|---|---|
| `readers/name_vocabulary.py` | a 25-row `name → (flags, value)` dictionary | 8 |
| `readers/invariant_signature.py` | one answer per `(count, ordered flags/value)` | 8 |
| `readers/digest_keyed_full.py` | one answer per whole-file sha256 | 8 |
| `readers/opaque_basename.py` | one answer per generated basename | 8 |
| `lane/tools/round-34/mini-fix/readers/answer_key_adjacent.py` | reads the shipped `../expected.json` and selects by name vocabulary | 8 |

**Root cause, stated as a property of the counter, not of any witness:** the green surface's fixture set
has a **globally unique name vocabulary** (25 names, 25 records) and the perturbation only reorders the
pool. "Which record does this name belong to?" is therefore fully recoverable from the *preserved* pool
plus a 25-entry table — decoding `name_off` is never necessary to reach 8/8. The gate's association
dimension is exactly the one the counter never perturbs.

**Admission proof (the decisive attack).** The frozen gate, unmodified except for a config that names a
PIR reader as the positive control, returns CLEAN:

| run | config | UTC | exit | verdict |
|---|---|---|---|---|
| A1 | positive=`name_vocabulary`, 7 registered shortcuts | 07:20:25Z | 0 | `REPLAY_GATE_CLEAN … shortcuts_below_target=7` |
| A2 | positive=`invariant_signature` | 07:20:28Z | 0 | `REPLAY_GATE_CLEAN` |
| A3 | positive=`opaque_basename` | 07:20:30Z | 0 | `REPLAY_GATE_CLEAN` |
| A4 | positive=`answer_key_adjacent` | 07:20:33Z | 0 | `REPLAY_GATE_CLEAN` |
| A5 | same reader additionally registered *as a shortcut* | 07:20:27Z, 07:20:29Z, 07:20:32Z, 07:20:34Z | 2,2,2,2 | `REPLAY_GATE_REFUSED … over=<that class>` |

A1–A4 vs A5 is the whole result in one pair: the gate detects a PIR reader **iff someone registers it**.
CLEAN is therefore a statement about registry completeness, and the c2 counter's `green_clean` +
`green_positive_meets_target` clauses compute exactly that registry-relative statement.

---

## 7. Divergences (defects that make the registry-relative reading unavoidable)

**D1 — refusal branch blinded by a class-name collision.** `evaluate()` excludes rows by *class string*,
not by identity or path: `row["class"] != positive_spec["class"]`. `load_config()`'s duplicate check only
dedupes *within* `shortcuts`. Registering an evading reader as a shortcut under class `"structural"`
therefore hides it. Verified: config with `shortcuts += [{"class":"structural", path:invariant_signature}]`,
run 2026-10-25T07:22:03Z, **exit 0, `REPLAY_GATE_CLEAN`, `classes_over_target=[]`** while that row reports
`structural matched=8 met=True` (receipt `out/class-collision.json`). Two rows named `structural`, one of
them a shortcut at full target, and the stable verdict line still prints `shortcuts_below_target=7`.
The gate's own 12-case selftest has no collision case.

**D2 — the perturbation is deterministic and self-disclosed.** `mini-counter.py:139` defaults the seed to
the constant `kaidoku-r34-mini-v1`; the gate never passes `--seed`. Two runs give identical
`transformed_sha256` rows. The counter also prints those digests in its receipt. Any digest- or
name-keyed replay is therefore a *stable* replay, not a one-shot guess.

**D3 — opacity regression relative to the inherited instrument.** The stopped R34-C1 counter generates
paths with `secrets.token_hex(12)` (`version-needs-counter.py:120`); the new green surface generates
`opaque-<sha256(transformed)[:20]>.data` — a content digest. The gate registers `label-memorization` as a
class while shipping a label that is a deterministic function of the answer (`opaque_basename` 8/8).

**D4 — the answer key ships next to the readers.** `mini-fix/expected.json` is a pinned instrument and is
readable at reader runtime from `../expected.json` relative to any registered reader. Verified 8/8 with
no header parse at all (`answer_key_adjacent`). The gate has no rule against a reader reading repo state.

**D5 — latent fixture-layout assumption in `permute()`.** `decode_fixture()` accepts `records_off >= 16`
and reads with it, but `permute()` writes each rewritten `name_off` at `16 + 8*index`. All current
fixtures use `records_off = 16`, so this is latent; a fixture with `records_off != 16` would be permuted
into a corrupt state and the counter's verdict would be meaningless rather than red.

**Carry-through to the frozen claim.** The kill rule's six clauses
(`selftest_clean, mutants_killed, red_refused, green_clean, green_positive_meets_target, gate_present`)
are all satisfied by the instruments as pinned, and none of them samples D1–D5. The claim's target —
"a finite structural-decoding counter is frozen only after registered structure-blind shortcut readers are
scored … and none meets the target" — is literally true and structurally weak: it quantifies over
registered witnesses. `claim-stop.json:operator_ruling` asked to "route structure-blind replay before
future freezes"; the shipped route tests the *previous* failure's memorization dimensions (size, label,
fixed slice) rather than the property (perturbation-invariance of the key) that makes replay possible.

---

## 8. Minimal reproduction recipes (rebuildable without the scratch tree)

All four take `sys.argv[1]` = the transformed fixture and print
`{"schema":1,"records":[...]}` sorted by `(name,flags,value)`.

1. `invariant_signature` — `count` u16 at offset 6, `records_off` u32 at 8; key = JSON of the ordered
   `[flags, value]` pairs read at `records_off + 8*i`; `TABLE[key]` is the memorized answer. 8/8.
2. `name_vocabulary` — `re.finditer(rb"[ -~]{4,}", data)` for the pool strings; emit every memorized
   `name → (flags, value)` whose name is present (25 rows, names globally unique). 8/8.
3. `opaque_basename` — `os.path.basename(argv[1])`; `TABLE[basename]` (the 8 basenames are
   `opaque-` + `sha256(transformed)[:20]` + `.data`, listed in `out/transformed-meta.json`). 8/8.
4. `answer_key_adjacent` — `json.load(open(dirname(__file__)+"/../expected.json"))` and select the fixture
   whose name set is a subset of the strings found in the input. 8/8.

Collision config (D1): take `gate-config-mini.json` verbatim and append
`{"class": "structural", "path": "<any reader that meets target>"}` to `shortcuts` — the gate prints
`REPLAY_GATE_CLEAN` while that row reports `matched=8`.

---

## 9. Confidence and limits

- Contract, coverage table, key-space arithmetic, A1–A5, D1–D4: **high** — each is a run I executed here,
  with command, exit code and UTC recorded above; receipts in `out/`.
- D5: **high** as a code-reading claim; **not exercised** (no fixture with `records_off != 16` was built —
  building one would change the pinned instrument set, which is not mine to do).
- Intent attribution (whether the authors meant "seven classes" as coverage or as a floor): **inference**,
  marked as such; the observable fact is only that 2/7 touch the family and 5/7 cannot.
- Not done, by rule: no ELF carrier, fixture or reader binary executed as a program; no run of the R34-C1
  production reader or its twelve carriers; no lane VCS write; no tool install.
- Scratch evidence root: `/fast/scratch/hyaku/kaidoku-r34b/w1/RevengerR34History/` —
  `readers/*.py`, `out/gate-mini.json`, `out/gate-naive.json`, `out/score-*.json`, `out/admit-*.json`,
  `out/register-*.json`, `out/class-collision.json`, `out/det-run{1,2}.json`, `out/transformed-meta.json`.

**VERDICT: R34-C2's CLEAN is registry-relative, not structure-blind — of the seven registered classes
only `fixed-slice` genuinely covers a dimension of the retained r34 family (`size-keyed` covers it only by
size collapse; three witnesses are vacuous and two are structurally irrelevant), the memorized-association
dimension is covered by none, and the family that evades all seven — preserved-invariant key replay
(invariant signature / name vocabulary / content digest / generated basename), 8/8 measured — is certified
`REPLAY_GATE_CLEAN` by the frozen gate whenever it is named as the positive control, and is silently
excluded from `classes_over_target` when it is registered as a shortcut under the class string
`structural`.**
