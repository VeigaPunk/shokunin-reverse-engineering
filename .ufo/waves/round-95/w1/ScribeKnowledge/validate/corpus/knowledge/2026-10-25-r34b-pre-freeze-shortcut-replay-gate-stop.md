# The pre-freeze shortcut-replay gate, and the stop that proved it insufficient (round 34, run-6 re-dispatch)

author: kaidoku-shokunin (round 34, run-6 re-dispatch, attempt 1)
status: instrument retained; **capability denied** — the claim stopped (`.ufo/waves/round-34/r34b/claim-stop.json`, landed `cd75b92e`)
sources: S106 (binutils `readelf.c`, version-needs decode order); corpus/QUALITY.md rows 67-74
revisions: base `ec3125ad3d130d92f888a4128dfaa2982f36fff7`; freeze `c79bbe7b0959132b9873ff3431cf5eb313b58b33`; stop `cd75b92e583735729546b0ea3b250f2df6d0652a`

## What was built

`tools/round-34/replay-gate.py` was built to make QUALITY 67 executable. It does not discharge that criterion on its own: the round's own stop shows that a registered-class set can hold while the surface is still shape-recoverable. Given a config it

1. runs a **registered structural reader** (the positive control) through the counter under test;
2. runs each **registered shortcut class** through the same counter, with the same predicate;
3. prints one of three verdicts:

| verdict | exit | condition | printed line |
|---|---|---|---|
| `REPLAY_GATE_CLEAN` | 0 | the positive control meets the target and **no registered** shortcut does | `finding=no_shortcut_meets_target` |
| `REPLAY_GATE_REFUSED` | 2 | at least one registered shortcut meets the target, naming its class | `finding=shortcut_meets_target` |
| `REPLAY_GATE_UNEVALUABLE` | 3 | the positive control is absent or below target, the counter receipt is unreadable, the counter's own target differs, or the config fails schema (fewer than three classes, duplicate class names, no `{reader}` slot) | `finding=<typed reason>` |

`tools/round-34/c2-shortcut-gate-counter.py` runs the gate's isolated self-test, the red case and the green case in one command and reports six clauses: `gate_present`, `selftest_clean`, `mutants_killed`, `red_refused`, `green_clean`, `green_positive_meets_target`.

The demonstration surface is deliberately synthetic: eight 512-byte `MREC` record-chain fixtures (magic, `u16 version`, `u16 count`, `u32 records_off`, `u32 names_off`, 8-byte records, NUL-terminated ASCII name pool), `expected.json` from the writer's spec, and nine reader files (seven registered classes, the structural positive control, one inert pin). The **red** config uses a shape-only counter that scores readers on the fixture's own path; the **green** config permutes each fixture's name pool per run and passes only opaque temporary paths.

## Measured

| surface | command | observed |
|---|---|---|
| before (base `ec3125ad`) | `python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root <base> --rev ec3125ad…` | `GATE_COUNTER_UNEVALUABLE finding=gate_absent`, exit 2 |
| production (freeze `c79bbe7b`) | same command, `--root <lane> --rev c79bbe7b…` | `GATE_COUNTER_OK … selftest_failures=0 mutants_killed=3 red=REPLAY_GATE_REFUSED green=REPLAY_GATE_CLEAN green_positive_matched=8`, exit 0 |
| five controls | `--gate controls/gates/*.py` | all MISS; max 5 of 6 clauses; failing clause named per control |

Receipts: `.ufo/waves/round-34/r34b/{before,after,controls}/`, landed `b917ea64`.

## Why the capability is denied

The green surface's only perturbation was name-pool reordering, so every invariant of the record array survived it. Five independent seats produced structure-blind readers that reach the green target of 8/8:

| class | key | evidence |
|---|---|---|
| content multiset | sorted set of SONAME tokens | `w1/CtlMultiset-files/nameset.py` (sha256 `2e8feaea92ee…`), 8/8 at three seeds; L1 rerun 2026-10-25T07:28Z |
| payload | count + ordered `(flags, value)` pairs, every name byte zeroed | `w1/ACounterexample2.md` lineage; `w1/CritCounterLimits.md` probe (8/8), `w1/ExecRedReproduce.md` |
| value/offset | record tails read at fixed offsets | `w1/MutShortcutClasses.md` (`s2d_fixed_slice_offsets_memo` 8/8) |
| record signature | `(count, ordered (flags,value))` | `w1/MutShortcutClasses.md` (`s2b_record_sig` 8/8) |
| identity leak | offline replay of the deterministic transform, or the copy name `opaque-<sha256(copy)[:20]>` | `w1/MutShortcutClasses.md` (digest replay and label replay both 8/8) |

Registering any of them flips the same gate to `REFUSED`, so the refusal mechanism works and the **registered set was unfaithful to the class it names**. A target a control that skips the claimed work can reach is not an improvement (§9 of the round contract; r29-C1 precedent). No SCORECARD capability row entered, no axis score moved (10→10, delta 0).

## What "structural decoding" means here — S106

S106 pins binutils `readelf.c` at tag `binutils-2_47` (commit `6ce87bbc`), captured as sha256 `7e81eedf19b2b93663bb3f598f74b54c107bd699f551667eb1b3d0e33eddeeff`. The `SHT_GNU_verneed` branch (`:14020`) counts records from `sh_info` (`:14058`), bounds each against `endbuf` (`:14056`, `:14067-14068`), decodes `vn_version, vn_cnt, vn_file, vn_aux, vn_next` in that order (`:14072-14076`) and each aux record likewise (`:14102-14106`), and resolves both name fields through the dynamic string table (`DT_STRTAB`/`DT_STRSZ`, `:467-470`); `sh_link` appears only in the `Link:` label. Ten malformed-record paths degrade to `break`/`warn`, including the located quote at `:14149` `warn (_("Missing Version Needs information\n"))`, and the function still returns true (`:14418`).

That is the standard a structure-sensitive decoder has to meet: bounded record traversal with the association carried by a `name_off`-style field, not by a name vocabulary. The frozen green surface did not force it.

## Limits

- The gate attests receipt shape, not the counter's measurement: `met_target` is trusted from the counter's own JSON and never cross-checked with `matched` (`w1/CritCounterLimits.md` probe D); a 1,979-byte gate that runs no reader satisfies all six clauses (probe E).
- Refusal is filtered by free-text class label, so a shortcut relabelled `structural` is excluded from `over` and prints CLEAN even on the red config (`w1/RevengerGateFailModes.md` D1).
- The registered set is not asserted against the pinned set: dropping classes down to `MIN_SHORTCUTS = 3` still prints CLEAN (`w1/RevPredicateIdentity.md` M3).
- The predicate asserted in the frozen claims file is not the sentence the counter and receipts carry (`predicate-reconciliation.json`; `PREDICATE_IDENTITY_FALSE`).
- Pins were declarative at the freeze: no instrument re-hashed them, and the frozen container was not the shape `tools/round-34/freeze-integrity.py` accepts (`instruments_missing`, exit 3). The enforced container is `.ufo/waves/round-34/r34b/instruments.json`.
- `permute()` treats trailing NUL padding as empty strings, so single-record fixtures occasionally draw the identity permutation (10/5000 on `beta`, 13/5000 on `epsilon`); the target-8 conjunction never survived.
- Synthetic fixtures are author-built and one-format; `expected.json` derives from the writer's spec, so fixture↔expected agreement is tautological and the byte-level decode is the evidence.
- A python reader is arbitrary code; a clean replay is not a statement that no reader executed.

## The repair route (not a claim)

`.ufo/waves/round-34/r34b/w1/CtlMultiset-files/mini-counter-fresh.py` generates fresh content per run and derives the expectation from the generation, so no key-invariant memory can survive: demonstrated 8/8 for the structural reader and 0/8 for all nine structure-blind classes (`w1/ExecRedReproduce.md`, `w1/ARepairFresh.md`). It is a next-round instrument, not evidence for this round's claim.

## Rejected

Treating CLEAN as held capability. CLEAN is relative to the caller's class list; the round's own counterexample shows the list, not the fixture design, was doing the work.

## Provenance trio (appended round 36 — the header above is not rewritten)

source: S106 — GNU binutils `readelf` version-needs reader, https://sourceware.org/git/?p=binutils-gdb.git;a=blob_plain;f=binutils/readelf.c;hb=6ce87bbc521cf46eaee9a1f7ef61cee2cdfb3e32 (tracked capture `.ufo/waves/round-34/prep/R34ElfReader-files/readelf.c-binutils-2_47`, sha256 `7e81eedf19b2b93663bb3f598f74b54c107bd699f551667eb1b3d0e33eddeeff`); corpus/QUALITY.md rows 67-74 as cited above.
verified-at: 2026-10-26 — re-read at lane `d2e46ef5e2b2e8ba681b2fa55d50f298c4c4b8be`: `corpus/SOURCES.md:112` (S106, mined, opened 2026-10-25, recheck `on-release`, used-by this entry); stop record `.ufo/waves/round-34/r34b/claim-stop.json`; addendum `.ufo/waves/round-34/r34b/claim-stop-addendum.json`; seat report `.ufo/waves/round-34/r34b/w2/AWaveAccounting.md`; lesson `corpus/lessons/round-34.md` (M34-15, M34-16); `corpus/QUALITY.md:126` row 76.
recheck: on-release — reopen S106 at the next binutils tag and re-read the claim-stop record; the standing check `grep -n '^| S106 ' corpus/SOURCES.md` must keep this entry in `used-by`.
