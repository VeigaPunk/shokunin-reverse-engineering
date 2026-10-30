# MutC1Bindings — R52-C1 binding-mutation battery (v2 counter documentation bindings)

**Seat:** MutC1Bindings (mutation-tester) · **wave:** r52-w1 · **lane:** `kaidoku-shokunin`
**Scope:** design + empirically validate the binding-mutation battery for the v2 counter's
documentation bindings and the receipt-side clauses. Leaf seat: no subagent dispatch, no
REA run, no network, no lane write.

**Verdict: SETTLED — the battery is delivered and measured. It also produces a
coverage finding the L1 must act on before the freeze: eight of the claim's landing
obligations are provably DEAD against the frozen nine-binding set, and the round-52 v2
counter draft does not import.**

---

## 1. What was built

`binding-probe.py` (seat dir) is an offline, no-REA detector. It does **not** re-implement
the bindings: it extracts the binding block verbatim from the counter source under test
and `exec`s it in a namespace built from that counter's own globals (`ENTRY`, `STEM`,
`CORE_HEADING`, `FRONTIER_MARK`, `OPENED_DATES`, `HANDLER_RE`, `AVM_MARKER_RE`,
`LE_AVM_RE`, `SID_RE`, `section()`, `cells()`, `sid_tokens()` — the shipped bytes). The
receipt clauses are extracted with `ast.get_source_segment` on the exact
`d['<key>'] = …` assignment and eval'd against the counter's own `all_adds`,
`is_ancestor`, `squashfs_chunk_handlers`. Each case runs in a fresh scratch git repo, so
the history-sensitive clause (`receipt_fresh`) is exercised against real commits. The
probe is counter-agnostic (fixtures are built from the counter under test's own
constants) and refuses to report on a red baseline.

**44 cases, run against both the frozen v1 counter and the round-52 v2 draft.**
Results are identical for both, because the two binding blocks are **byte-identical**
(verified: 2614 identical bytes).

| | v1 `tools/round-50/c1-counter.py` | v2 draft `ExecCounterV2/c1-counter.py` |
|---|---|---|
| baseline | GREEN | GREEN |
| KILLED (mutation flips the named binding) | 33 | 33 |
| NO-OP (mutation changes nothing — dead check) | 2 | 2 |
| DEAD (named landing obligation not covered at all) | 8 | 8 |

Receipts (exact command, exit code, stdout sha256, UTC time): `probe-receipts.md`.
Per-case results: `out-v1.json`, `out-v2.json`.

---

## 2. The three findings that matter

### F1 — the round-52 v2 counter draft **does not import** (blocking for the L1)

`.ufo/waves/round-52/w1/ExecCounterV2/c1-counter.py` drops the module-level `TARGET = 4`
and `IDS = ('g7581','g7582','c6490','c6430')` constants (v1 lines 394-395). Because
`measure()`'s default arguments (`target=TARGET`, `expected_ids=IDS`,
`c1-counter.py:2147-2148`) are evaluated at `def` time, the module raises
`NameError: name 'TARGET' is not defined` **at import**. The probe had to inject the two
names into an in-memory copy to reach the binding code at all. The same draft also has
**no** `law_shape_ok`, `census_rederived_ok`, `depth_gap_recorded`, `re_scored_pins`,
`--provenance-base` or `--receipt-fresh-base` — i.e. the predicate the claims state is
not implemented (the seat's own `status.json` says `failed` on exactly this point).
**The freeze cannot ship this draft as-is.**

### F2 — `frontier_note` cannot tell a **promotion** from a **non-promotion** (N07)

The binding proves only that `Round-52 frontier note`, the stem and an LE-AVM token
co-occur on one line. A round-52 frontier note that says the members **stay Frontier**
("measured, not promoted") scores **green**. This is the claim's central subject — the
Frontier → Core promotion of LE AVM members (`hsqs`) — and it is unchecked. The related
**N03**: the binding never checks that the `LE AVM members (\`hsqs\`)` clause was *removed*
from the Frontier list; the round-40/-41/-42/-44/-49/-50 notes all still carry it
(`PROVINCE.md:394,405,408,416,430,438,448`).

### F3 — `sourced` proves ONE source row, not the claim's citation set (N01)

`b['sourced'] = bool(ok_ids)` (`c1-counter.py:2478`). The claims demand the entry cite
**S243/S244/S245/S249 and S250/S251**; dropping S250/S251 while keeping one in-window
row leaves `sourced` true. A green `sourced` therefore does **not** show the claim's
citation set — the gap `RevCounterPort/checklist.md:62,332` also raised.

### Supporting: `province_core_row`'s marker clause is not layout-scoped (D10, N08)

`AVM_MARKER_RE` scans the whole row minus the entry path. Verified against the **real**
lane row `PROVINCE.md:446`: emptying the layout column keeps the binding true, and a row
whose only marker mention is the lane's own *"the AVM marker test exists only in the BE
branch"* sentence satisfies a binding meant to prove the row claims the **LE** AVM-marker
layout.

---

## 3. The battery, in brief

**Doc bindings** (25 cases). Each names the fixture mutation that must flip the binding
and the expected finding id (`b:<binding>` in the receipt's `failing_lists()` output):

- `province_core_section` (D01-D03): heading typo'd / suffixed / demoted to `###`.
  **D02 is load-bearing** — `section()` is an exact whole-line match, so a semantically
  identical heading with a parenthetical is red.
- `province_core_row` (D04-D09): BE handler / bare-prefix handler / row absent / cites
  another entry / row under another heading / no marker anywhere.
- `frontier_note` (D11-D15): note absent / wrong mark / stem-only without the LE token /
  BE token / wrong stem. **D13 is the most likely port regression**: the stem itself
  spells `avm-le`, so the shipped `.replace(STEM, '')` (`c1-counter.py:2454-2456`) must
  be preserved verbatim.
- `entry_present` (D16), `sourced` (D17-D22: used-by dropped / opened before / opened
  after / unknown S-id / `S11210`-vs-`S1121` substring trap / wrong cell count),
  `coverage_map_row` (D23-D25, including the section-scoping case).

**Receipt-side** (11 cases), finding id `<carrier_id>:<clause>`:

- **subject digest ≠ carrier pin** → `g7581:subject_pin_ok` (R1).
- **wrong handler** (`squashfs_v4_be` / bare `squashfs_v4` / `squashfs_v3`) →
  `g7581:handler_ok` (R2-R4). Exact equality, no prefix test, no default.
- **stale receipt-fresh base** → `g7581:receipt_fresh` (R5, R6, R8), plus the controls
  R7 and R9 that prove the clause is not trivially red. R8/R9 are the pair that pins the
  `--receipt-fresh-base` flag the claims name (`claims:131`).
- **re-scored pin on a `re_scored_pins` allow-list** → `g7581:carrier_fresh_ok` (R10):
  **NO-OP** — no such constant exists in either counter, so the waiver the claims specify
  (`claims:81`) is absent.

---

## 4. Open obligations handed to the L1 (recorded, not fixed — the counter and the
freeze are the integration owner's)

1. **Add the missing landing bindings** or narrow the claim to what the nine bindings
   prove. Implied set: `sources_cited` (the full citation set, N01), `frontier_promoted`
   (the note records the promotion AND the `hsqs` clause is gone, N03/N07),
   `scorecard_head` (142/142, N02), `log_entry` (N04), `entry_receipts` (N05),
   `registry_rows` (one row per new instrument, N06), `province_row_layout` (the layout
   cell names the LE marker, N08/D10).
2. **Add `--provenance-base` and `--receipt-fresh-base`** and pin them in the control
   driver, so CTL-OLD/CTL-NEW score the rule-scoped verdict rather than the round-50
   receipts' `receipt_fresh` failure.
3. **Add `re_scored_pins`** plus a case proving the four pins pass **only** through the
   allow-list, so the anti-replay waiver is narrow and visible.
4. **Preserve the D13 `.replace(STEM, '')` discipline** and keep the D13 selftest case.
5. `law_shape_ok` / `census_rederived_ok` / `depth_gap_recorded` and the law-rule
   mutation family (M1-M4) are the **law owner's** scope — this battery does not cover
   them (they do not exist yet) and they need their own battery before the freeze.

---

## 5. Contract compliance

- **Read-only on the lane tree.** The only files written are under
  `.ufo/waves/round-52/w1/MutC1Bindings/` and this report. No commit, push, stage, stash
  or mutating git/jj command in the lane or the fleet repo. (`git status` shows one
  pre-existing modification, `.ufo/waves/round-50/w3/ScribeEntryC1.md`, mtime 07:53 — not
  this seat's; this seat's files are 07:59.)
- **No REA run.** No `npx rea-agents`, no `rea`, no package invocation. The probe reads
  no REA source. No `--data-run`, no vendor download, no `corpus/evidence/` write.
- **Scratch** `S=/fast/scratch/hyaku/kaidoku-r52/w1-MutC1Bindings`, `TMPDIR=$S`, removed
  after the receipts were copied into the seat dir. Nothing written under `/tmp`.
- **Fixture repos:** each case creates its own `git init` clone under `$S` with
  `user.name`/`user.email` set **in that clone only**; no `git commit` with a throwaway
  identity anywhere else.
- **Tooling:** no tool was installed or upgraded — the probe uses only the stdlib and the
  `git` already present. Nothing to record under the operator's tooling authorisation.
- **Seats:** leaf member; no subagent dispatched; no `agent://all` broadcast.

---

## 6. Artifacts

| path | what |
|---|---|
| `.ufo/waves/round-52/w1/MutC1Bindings/battery.md` | **the deliverable** — the full battery specification (per-binding mutation → expected finding id, the no-op risk analysis, the receipts-side mutations, the open obligations) |
| `.ufo/waves/round-52/w1/MutC1Bindings/binding-probe.py` | the offline detector (no REA, no network, counter-agnostic) |
| `.ufo/waves/round-52/w1/MutC1Bindings/out-v1.json` | 44 per-case results against the frozen v1 counter |
| `.ufo/waves/round-52/w1/MutC1Bindings/out-v2.json` | 44 per-case results against the round-52 v2 draft |
| `.ufo/waves/round-52/w1/MutC1Bindings/probe-receipts.md` | commands, exit codes, stdout sha256, UTC times, and the explicit *not run* list |
| `.ufo/waves/round-52/w1/MutC1Bindings/status.json` | wave-accounting status file |
