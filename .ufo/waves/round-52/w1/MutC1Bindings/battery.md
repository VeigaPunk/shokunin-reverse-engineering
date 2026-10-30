# R52-C1 binding-mutation battery — the v2 counter's documentation bindings

**Seat:** MutC1Bindings (mutation-tester) · **wave:** r52-w1 · **lane:** `kaidoku-shokunin`
**Round base:** `c525de54a53eb3c4fee28ede2721da4527cf8ece` · **claims draft:** `ab0eafedc41402b43b41a4362084119578dfe7ce`
**Target instrument:** `tools/round-52/c1-counter.py` (v2). The round-52 v2 draft under
review was `.ufo/waves/round-52/w1/ExecCounterV2/c1-counter.py` (seat status `failed`).

---

## 0. What this battery is for

The R52-C1 landing-bindings bullet (`plans/round-52-claims.md:162-172`) lists documentation
obligations the counter must be able to re-derive. The frozen round-50 counter proves nine
of them (`BINDINGS`, `tools/round-50/c1-counter.py:432-434`). This battery answers, for
every binding:

1. **Which fixture mutation flips it** (and therefore which selftest case the v2 counter
   must carry), and
2. **What the expected finding id is** in the counter's receipt, and
3. **Whether the binding is live at all** — a binding whose fixture mutation changes
   nothing is a **dead check**: it can never fail, so it proves nothing.

Two families are covered:

- **Doc bindings** — the nine `BINDINGS`, of which six are documentation bindings
  (`province_core_section`, `province_core_row`, `frontier_note`, `entry_present`,
  `sourced`, `coverage_map_row`) and three are table bindings
  (`carriers_spec_ok`, `gap_rule_ok`, `frozen_tables_valid`).
- **Receipt-side mutations** — the receipt clauses that carry the subject/handler/freshness
  identity: `subject_pin_ok`, `handler_ok`, `receipt_fresh`, `carrier_fresh_ok`.

**Finding id convention.** The counter's receipt reports a false binding as
`res['bindings'][<name>] is False`, and `failing_lists()` (`c1-counter.py:2500-2508`)
emits the bare binding name. A false carrier clause is emitted as
`<carrier_id>:<clause>`. The frozen selftest harness matches on `b:<binding>` for
bindings. Both spellings are given below.

---

## 1. The detector (how these results were produced)

`binding-probe.py` (this directory) is a self-contained, offline, no-REA probe.

- It **does not re-implement** the bindings. It extracts the binding block
  (`# ---- bindings` … `res['met_target']`) **verbatim** from the counter source under
  test and `exec`s it in a namespace built from that counter module's own globals, so
  `ENTRY`, `STEM`, `CORE_HEADING`, `FRONTIER_MARK`, `OPENED_DATES`, `HANDLER_RE`,
  `AVM_MARKER_RE`, `LE_AVM_RE`, `SID_RE`, `section()`, `cells()` and `sid_tokens()` are
  the **shipped bytes**, not a re-typed copy.
- The receipt clauses are extracted with `ast.get_source_segment` on the exact
  `d['<key>'] = …` assignment, then `eval`'d against the counter's own `all_adds`,
  `is_ancestor` and `squashfs_chunk_handlers`.
- Each case runs in a **fresh scratch git repo** (`git init` in the seat scratch, a
  throwaway identity set **in that clone only**), so the history-sensitive clauses
  (`receipt_fresh`) are exercised against real commits.
- **No REA, no network, no lane writes.** The probe writes only into
  `/fast/scratch/hyaku/kaidoku-r52/w1-MutC1Bindings`.

Run:

```
python3 binding-probe.py <counter.py> <out.json> <scratchdir>
```

The probe is **counter-agnostic**: the fixtures are built from the counter under test's
own constants, so the same battery runs against the frozen v1 counter and the round-52 v2
counter without edits. **If the counter under test does not import, the probe reports it
and injects the missing module-level names into an in-memory copy only** — see Finding F1.

**Baseline:** the pristine fixture tree must make all six doc bindings true
(`verdict: GREEN`). A red baseline makes every case inconclusive; the probe exits
non-zero and says so rather than reporting a vacuous battery.

### 1.1 Results (both counters, identical)

| | v1 `tools/round-50/c1-counter.py` | v2 draft `ExecCounterV2/c1-counter.py` |
|---|---|---|
| baseline | GREEN | GREEN |
| KILLED (mutation flips the named binding) | 33 | 33 |
| NO-OP (mutation changes nothing — dead check) | 2 | 2 |
| DEAD (named landing obligation not covered) | 8 | 8 |
| total cases | 44 | 44 |

The two runs are identical because **the binding block is byte-identical** between the
v1 counter and the v2 draft (verified: both extract to 2614 identical bytes). Every
finding below therefore applies to the v2 as it stands.

---

## 2. Doc-binding battery — the fixture mutation that must flip each binding

Each row: **case id · binding · fixture mutation · expected finding id · verdict.**
All mutations are on the pristine fixture tree, one at a time.

### 2.1 `province_core_section` — `PROVINCE.md` has the `## Round-52 additions to Core` heading

| case | fixture mutation | expected finding | verdict |
|---|---|---|---|
| D01 | heading typo'd → `## Round-52 addition to Core` | `b:province_core_section` | KILLED |
| D02 | heading carries a suffix → `## Round-52 additions to Core (verified 2026-10-30)` | `b:province_core_section` | KILLED |
| D03 | heading demoted to `### Round-52 additions to Core` | `b:province_core_section` | KILLED |

**Mechanism:** `section()` (`c1-counter.py:571-583`) does an exact whole-line
`lines.index(heading)` and then stops at the next `## ` line. D02 is therefore the
load-bearing case: a *semantically identical* heading with a parenthetical is **red**.
The v2 counter must keep this exact-match discipline, or the section boundary moves.

### 2.2 `province_core_row` — a row in that section naming `squashfs_v4_le`, the AVM marker and the entry path

| case | fixture mutation | expected finding | verdict |
|---|---|---|---|
| D04 | first cell names the BE handler (`squashfs_v4_be`) | `b:province_core_row` | KILLED |
| D05 | handler prefix only (`squashfs_v4`) | `b:province_core_row` | KILLED |
| D06 | the LE row is absent from the section | `b:province_core_row` | KILLED |
| D07 | row cites another entry path (`…r41-avm-be-squashfs-core.md`) | `b:province_core_row` | KILLED |
| D08 | row sits under a different heading (`## Round-51 additions to Core`) | `b:province_core_row` | KILLED |
| D09 | row names no AVM marker **anywhere** | `b:province_core_row` | KILLED |
| D10 | layout column drops the marker, first cell keeps `AVM-marker` | `b:province_core_row` | **NO-OP** |

D05 matters because `HANDLER_RE` is `(?<![A-Za-z0-9_-])squashfs_v4_le(?![A-Za-z0-9_-])`
  (`c1-counter.py:426`)
— a **not-a-prefix** test. The v2 must not weaken it to `startswith`.

**D10 is a dead check (see Finding F2).** `AVM_MARKER_RE` scans the *whole row* with the
entry path removed, so the marker can be satisfied by any cell. Verified against the
**real lane row** (`PROVINCE.md:446`): emptying the layout column keeps
`province_core_row` true.

### 2.3 `frontier_note` — one line carries `Round-52 frontier note`, the stem and an LE-AVM token

| case | fixture mutation | expected finding | verdict |
|---|---|---|---|
| D11 | frontier note absent | `b:frontier_note` | KILLED |
| D12 | wrong frontier mark (`Round-51 frontier note`) | `b:frontier_note` | KILLED |
| D13 | note keeps the stem but drops the LE-AVM token | `b:frontier_note` | KILLED |
| D14 | note carries the BE token (`AVM BE`) | `b:frontier_note` | KILLED |
| D15 | note names the wrong stem (the round-50 stem) | `b:frontier_note` | KILLED |

**D13 is the specificity case and must not be lost in the port.** The stem
`2026-10-30-r52-avm-le-squashfs-core` itself contains `avm-le`, which satisfies
`LE_AVM_RE`. The shipped code defends this with `l.replace(STEM, '')`
(`c1-counter.py:2454-2456`) before searching the token. Any v2 rewrite that drops that
`.replace()` makes D13 silently green. **D13 is the single most likely regression in the
port** — keep it verbatim.

### 2.4 `entry_present` — the knowledge entry exists at REV

| case | fixture mutation | expected finding | verdict |
|---|---|---|---|
| D16 | entry file renamed (stem moved to `…-v2.md`) | `b:entry_present` | KILLED |

### 2.5 `sourced` — the entry's `source:` lines name an S-id whose `corpus/SOURCES.md` row is opened in the window and lists the entry in used-by

| case | fixture mutation | expected finding | verdict |
|---|---|---|---|
| D17 | used-by dropped (points at another entry) | `b:sourced` | KILLED |
| D18 | source row opened **before** the window (2026-10-29) | `b:sourced` | KILLED |
| D19 | source row opened **after** the window (2026-10-31) | `b:sourced` | KILLED |
| D20 | entry cites an S-id with no SOURCES row | `b:sourced` | KILLED |
| D21 | S-id substring trap (entry says `S11210`, row says `S1121`) | `b:sourced` | KILLED |
| D22 | the SOURCES row has the wrong cell count (10, not 11) | `b:sourced` | KILLED |

D21 is the `SID_RE` guard (`c1-counter.py:430`): `(?<![0-9A-Za-z])(S\d{3,})(?![0-9A-Za-z])` must not match a
longer digit run. D22 is the `len(c) != 11` gate — a malformed SOURCES row must be
**skipped**, not mis-parsed.

### 2.6 `coverage_map_row` — `corpus/README.md` `## Coverage map` maps the entry stem

| case | fixture mutation | expected finding | verdict |
|---|---|---|---|
| D23 | map row removed | `b:coverage_map_row` | KILLED |
| D24 | map row names another stem | `b:coverage_map_row` | KILLED |
| D25 | stem appears only under `## Knowledge`, not in the map | `b:coverage_map_row` | KILLED |

D25 is the section-scoping case: the check is `section(readme, '## Coverage map')`, so a
stem mentioned only in the Knowledge index does **not** satisfy it.

### 2.7 Table bindings (not documentation bindings, listed for completeness)

`carriers_spec_ok`, `gap_rule_ok` and `frozen_tables_valid` are the frozen-table
bindings. Their mutation families (frozen table edited at the freeze, carrier dropped,
`projection` set to `core`/`plus-mime`, gap rule naming another claim, gap rule omitting
the device kind, oracle table added after the freeze) already exist in the frozen v1
selftest at `c1-counter.py:4157-4355` and are **out of this battery's scope** — they are
owned by the counter port seat. The R52-specific extension (`law_shape_ok`: the frozen
rule lists no char-device/fifo/socket/block detail under `removed.silent`, and `allowed`
for those kinds is the empty list) is likewise out of scope here and **must** get its own
mutation battery from the law owner; it is listed as an open obligation in §5.

---

## 3. No-op risk — the landing obligations the nine bindings do **not** derive

These are the cases where the fixture mutation is exactly what the claims require to be
**false**, and the shipped bindings **do not notice**. Each is a **DEAD** check: the
counter would score a non-conforming landing as met.

| case | landing obligation (claims:162-172) | fixture mutation | expected finding | verdict |
|---|---|---|---|---|
| N01 | the entry cites **S243/S244/S245/S249 and S250/S251** | the entry's `source:` lines drop S250/S251 and keep one in-window row | *(none — `sourced` stays true)* | **DEAD** |
| N02 | `SCORECARD.md` coverage head names **141/141 → 142/142** | the SCORECARD head still says 141/141 | *(no binding reads SCORECARD.md)* | **DEAD** |
| N03 | PROVINCE: **LE `hsqs` leaves the Frontier list** | the `LE AVM members (\`hsqs\`)` clause is left in the Frontier list | *(none — `frontier_note` stays true)* | **DEAD** |
| N04 | a **LOG entry** | no LOG.md entry for round 52 | *(no binding reads LOG.md)* | **DEAD** |
| N05 | the entry **names the fresh receipts** | the entry names no receipt path | *(no binding checks the receipt citation)* | **DEAD** |
| N06 | **exactly one instrument-registry v2 row** per new instrument | no registry row for the round-52 counter | *(no binding counts registry rows)* | **DEAD** |
| N07 | the frontier note records the **promotion** | the note says the members **stay Frontier** (a "measured, not promoted" note) | *(none — `frontier_note` stays true)* | **DEAD** |
| N08 | the row names the **LE AVM-marker layout** | the only `AVM marker` mention in the row is the **negative BE clause** | *(none — `province_core_row` stays true)* | **DEAD** |

**N01 and N07 are the two that matter most for the claim itself.**

- **N01** — the claims demand the entry cite *S243/S244/S245/S249 **and** S250/S251*.
  The shipped `sourced` binding is satisfied by **one** matching row
  (`b['sourced'] = bool(ok_ids)`, `c1-counter.py:2478`). A green `sourced` therefore
  proves *one* opened, used-by-listing source row — **not** the claim's citation set.
  This is the same gap `RevCounterPort/checklist.md:62` and `:332` raised.
- **N07** — the claims' *subject* is the promotion **Frontier → Core**. The shipped
  `frontier_note` binding proves only that the mark, the stem and an LE-AVM token
  co-occur on one line. A round-52 note that says "**stay Frontier**; measured only"
  scores green. The binding is blind to the very thing the round is about.
- **N03** is the same defect seen from the other side: the binding never checks that the
  `LE AVM members (\`hsqs\`)` clause was *removed* from the Frontier list — the round-40,
  -41, -42, -44, -49 and -50 notes each still carry a "Still Frontier: LE AVM members
  (`hsqs`)" clause (`PROVINCE.md:394,405,408,416,430,438,448`).
- **N08** is a false-green on the row's *meaning*: `AVM_MARKER_RE` matches the string
  `AVM marker` wherever it occurs, including in the lane's own sentence "the AVM marker
  test exists only in the BE branch" — i.e. a row that explicitly says the marker is a
  **BE-branch** thing satisfies a binding that is supposed to prove the row claims the
  **LE** AVM-marker layout. Verified against the real lane row (`PROVINCE.md:446`).

**Consequence for the L1.** These eight are **not** counter bugs to be patched silently —
they are a *coverage finding* on the frozen nine-binding set. The claim's landing
obligations exceed what the nine bindings prove. The v2 counter must **add** the missing
bindings (see §5) or the claim must state the narrower contract it actually enforces.

---

## 4. Receipt-side mutations

These are **clause** failures, so the finding id is `<carrier_id>:<clause>`.

### 4.1 A receipt whose subject digest ≠ the carrier pin

| case | mutation | expected finding | verdict |
|---|---|---|---|
| R1 | `subject.digest.sha256` = a different 64-hex than the carrier's pin | `g7581:subject_pin_ok` | KILLED |

The clause is `d['subject_pin_ok'] = (subj['digest']['sha256']) == pin`
(`c1-counter.py:2324-2325`). A receipt that names a **different subject** than the
pinned carrier is red. Note the v2 must keep the *exact* comparison — the subject digest
is inside the hashed `semanticProjection`, so `evidence_id_ok` breaks too, but
`subject_pin_ok` is the clause that names the mismatch.

### 4.2 A receipt naming the wrong handler

| case | mutation | expected finding | verdict |
|---|---|---|---|
| R2 | chunk handler = `squashfs_v4_be` | `g7581:handler_ok` | KILLED |
| R3 | chunk handler = `squashfs_v4` (bare prefix) | `g7581:handler_ok` | KILLED |
| R4 | chunk handler = `squashfs_v3` | `g7581:handler_ok` | KILLED |

The clause is `bool(d['squashfs_handlers']) and all(h == HANDLER for h in d['squashfs_handlers'])`
(`c1-counter.py:2333-2334`) — **exact equality**, no prefix test, no default, and a
receipt with no squashfs-family chunk at all is red (`bool([])` is false). The v2 must not
relax this to `startswith(HANDLER)`.

### 4.3 A stale receipt-fresh base

`receipt_fresh` is `bool(adds) and all(a != freeze and is_ancestor(root, freeze, a) for a in adds)`
(`c1-counter.py:2316-2317`), where `adds` is every commit in the **full** history of REV
that adds the receipt path (`all_adds`, `git log -m --full-history --diff-filter=A`).

| case | mutation | expected finding | verdict |
|---|---|---|---|
| R5 | receipt added **before** the freeze commit | `g7581:receipt_fresh` | KILLED |
| R6 | receipt added **at** the freeze commit | `g7581:receipt_fresh` | KILLED |
| R7 | receipt added **after** the freeze commit | *(none — stays true; the control)* | KILLED |
| R8 | **stale base**: the base commit is **newer** than the receipt's add | `g7581:receipt_fresh` | KILLED |
| R9 | control: the base commit is **older** than the receipt's add | *(none — stays true)* | KILLED |

**R8/R9 are the pair that pins the `--receipt-fresh-base` flag** the claims demand
(`claims:131`: "the v2 counter therefore exposes the round-sensitive constants as explicit
flags (`--gap-rule`, `--receipts`, `--provenance-base`, `--receipt-fresh-base`)"). R8
proves the base is load-bearing (a stale base turns a fresh receipt red); R9 proves the
clause is not trivially always-red. **Neither flag exists in the v2 draft** — see F1.

R5/R6 also matter operationally: the committed round-50 receipts were added **before**
the round-52 freeze, so under the round-52 base they are red on `receipt_fresh`. The
control driver must therefore pin the base to the round-50 freeze to score CTL-OLD and
CTL-NEW as the claims specify (`claims:120-132`, especially `claims:126-132`: the
round-50 receipts fail `receipt_fresh` and every byte-dependent clause, and the v2
counter must expose the round-sensitive constants as flags so the control driver can
pin the round-50 values).

### 4.4 A re-scored pin carried on the frozen allow-list

| case | mutation | expected finding | verdict |
|---|---|---|---|
| R10 | a re-scored pin (the four round-50 carrier pins) carried on the frozen `re_scored_pins` allow-list | `g7581:carrier_fresh_ok` | **NO-OP** |

The counter under test has **no `re_scored_pins` constant** (`grep -c` = 0 in the v2
draft). Under v1 semantics a re-scored pin is simply "not fresh", so the v2 must **add**
the allow-list the claims specify (`claims:81`: "`carrier_fresh_ok` = pin fresh OR
pin on the frozen allow-list; the receipt names `prior_pin_sources` and the allow-list so
the waiver is visible, never silent") **and** carry a case proving the four pins pass
**only** through the allow-list — otherwise the waiver is a silent hole.

---

## 5. Open obligations for the L1 (not discharged by this battery)

These are recorded, not fixed — the v2 counter is the integration owner's instrument and
the freeze is the L1's commit.

1. **Add the missing landing bindings** (or narrow the claim to what the nine bindings
   prove). Minimum set implied by N01–N08:
   - `sources_cited` — the entry's `source:` lines name **every** S-id the claims list
     (S243/S244/S245/S249/S250/S251 + the round-52 rows), not just one.
   - `frontier_promoted` — the round-52 frontier note records the **promotion**, and the
     `LE AVM members (\`hsqs\`)` clause is absent from the Frontier list (N03, N07).
   - `scorecard_head` — `SCORECARD.md`'s coverage head reads 142/142 (N02).
   - `log_entry` — a round-52 LOG entry exists (N04).
   - `entry_receipts` — the entry names the fresh round-52 receipt paths (N05).
   - `registry_rows` — exactly one `instrument-registry v2` row per new instrument under
     `tools/round-52/` and no extra code files (N06).
   - `province_row_layout` — the row's **layout cell** names the LE AVM marker, so the
     negative BE clause cannot stand in for it (N08, D10).
2. **Add `--provenance-base` and `--receipt-fresh-base`** (the claims name them; the v2
   draft has neither — F1) and pin them in the control driver.
3. **Add `re_scored_pins`** and the case proving the four pins pass only through it (R10).
4. **Port the D13 `.replace(STEM, '')` discipline** into the v2 frontier-note check, and
   keep the D13 selftest case.
5. `law_shape_ok` / `census_rederived_ok` / `depth_gap_recorded` and the law-rule mutation
   family (M1–M4) are the **law owner's** scope; this battery does not cover them and
   they must get their own battery before the freeze.

---

## 6. Findings

**F1 — the round-52 v2 counter draft does not import.**
`.ufo/waves/round-52/w1/ExecCounterV2/c1-counter.py` drops the module-level `TARGET = 4`
and `IDS = ('g7581','g7582','c6490','c6430')` constants (the v1 lines 394-395). Because
`measure()`'s default arguments (`target=TARGET`, `expected_ids=IDS`,
`c1-counter.py:2147-2148`) are evaluated at `def` time, the module raises
`NameError: name 'TARGET' is not defined` **at import**. The probe had to inject the
missing names into an in-memory copy to reach the binding code at all. The same draft
also lacks `law_shape_ok`, `census_rederived_ok`, `depth_gap_recorded`, `re_scored_pins`,
`--provenance-base` and `--receipt-fresh-base` — i.e. the predicate the claims state is
not implemented (the seat's own status.json says `failed` on exactly this point).

**F2 — `province_core_row`'s AVM-marker clause is not layout-scoped (D10, N08).**
`AVM_MARKER_RE` scans the whole row minus the entry path, so (a) emptying the layout
column keeps the binding true, and (b) a row whose only marker mention is the lane's own
"*the AVM marker test exists only in the BE branch*" sentence satisfies a binding meant to
prove the row claims the **LE** AVM-marker layout. Both verified against the real lane row
`PROVINCE.md:446`.

**F3 — `frontier_note` cannot distinguish a promotion from a non-promotion (N07).**
The binding proves mark + stem + LE-AVM token co-occur on one line; a round-52 note that
says the members **stay Frontier** scores green. This is the claim's central subject
(Frontier → Core) and it is unchecked.

**F4 — `sourced` proves one source row, not the claim's citation set (N01).**
`b['sourced'] = bool(ok_ids)`. A green `sourced` does not show the entry cites
S243/S244/S245/S249 **and** S250/S251.

**F5 — the four round-50 carrier pins have no freshness waiver (R10).** The v2 draft has
no `re_scored_pins` allow-list; under the shipped semantics the four re-scored pins are
simply "not fresh", so either the claim's four-carrier re-measure is unsatisfiable or the
waiver is added without a case that shows it is narrow.

---

## 7. Reproduction

```
S=/fast/scratch/hyaku/kaidoku-r52/w1-MutC1Bindings
mkdir -p "$S"; export TMPDIR="$S"
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
python3 "$S/binding-probe.py" tools/round-50/c1-counter.py "$S/out-v1.json" "$S"
python3 "$S/binding-probe.py" .ufo/waves/round-52/w1/ExecCounterV2/c1-counter.py "$S/out-v2.json" "$S"
```

The probe writes only into `$S`. The lane tree is untouched (read-only contract honoured).

**Artifacts in this seat directory**

| file | what |
|---|---|
| `battery.md` | this specification |
| `binding-probe.py` | the offline detector (no REA, no network) |
| `out-v1.json` | full per-case results against the frozen v1 counter |
| `out-v2.json` | full per-case results against the round-52 v2 draft |
| `probe-receipts.md` | commands, exit codes, stdout sha256, UTC times |
| `status.json` | the wave-accounting status file |
