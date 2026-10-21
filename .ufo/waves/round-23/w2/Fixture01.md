# R23 W2 — Fixture01: `frozen/expected-v2.json` case `positive` source review

Candidate source commit `2838351450ff1ee4baa620c962a1153450d53311`; baseline `aa1450b82f9ede35aada63efe8a34e01c6e02f72`. All reads via `git show <rev>:<path>`; no suite execution, no writes outside `w2/`. Scope: `positive` case only, plus the exact `counter-fixtures.py` branch it takes (default/no-mutation branch) and `frozen/fixture.json`.

## Findings

### F1 — PASS: the `positive` expectation is correctly derived and distinguishes the stated fault class at candidate source

**Verified (hash, observed):** candidate bytes match every pin in the chain:

| File (at candidate) | sha256 | Pinned by |
|---|---|---|
| `.ufo/waves/round-23/frozen/expected-v2.json` | `458b30d5a6420c1b37874c3364d3ae3b22529d6c3560b5241848a21eec97096f` | `count-c1.py:25` `SELFTEST_MANIFEST_SHA256` — match |
| `.ufo/waves/round-23/tools/counter-fixtures.py` | `f2990b35d113b5e44317e7f00e6ca5157baae1efb5ee1a1b8e4995d0ace1a97f` | `expected-v2.json` `inputs` — match |
| `.ufo/waves/round-23/frozen/fixture.json` | `a1f5aff8ebb5e5d327522031b74ed91283708907af0fc4a6df24812479bfef4b` | `expected-v2.json` `inputs` — match |
| `.ufo/waves/round-23/tools/count-c1.py` | `f4b8d16ac195ca106a99cbb9236d36d1283dee349c6fef3a49567de0bbea0cc2` | (self; identical to snapshot rev `6615aeae` below) |
| baseline `.ufo/waves/round-22/tools/count-c1.py` | `c925918fb871151f86065aa5b3e9d10334ab845ed67c265ae0977f05e09b1879` | `count-c1.py:23` `LEGACY_SHA256` — match |
| baseline round-20/round-21 helpers | `cfbf1880…`, `61536938…` | R22 `HELPER_SHA256` pins — match |

`fixture.json` `base` == counter `BASELINE` (`count-c1.py:26`); `fixture.json` documents carry `ok:true`, `meta.command == <verb>`, distinct `ev_`+64-hex ids, and `data.operation` exactly matching the binder's normalization (`gdb_console`, `rizin_debug_command` per R22 `CLI_BIND_VERB`; hyphen→underscore for the rest) — all six consistent with `bind` (`round-21/tools/verb-coverage.py:77-102` at baseline).

**Verified (byte-level trace of the `positive` branch — inferred outcome, stated as such):** `positive` takes no `if name ==` mutation branch (`counter-fixtures.py:38,50-97`): one valid envelope at `.ufo/waves/round-23/evidence/c1/inspect-signal-decoders.json`, entry `corpus/knowledge/control-r23-synthetic.md` headed `source: S058 synthetic isolated control`, S058 SOURCES row inserted before `## Paths` with used-by = the entry (`counter-fixtures.py:82`). At the candidate counter:

- Historical prefix survives: baseline `corpus/SOURCES.md` has `## Paths` at line 65, after all `| S0xx |` rows (S001–S057), so the row-append keeps `source_rows(new)[:len(old)] == old` (`count-c1.py:72`) — no spurious exit 2.
- Eligibility gate passes exactly: `S058`, `58>=58`, tier col[4]=`A`, col[8]=`mined`, col[9]=`2026-10-21`, entry in col[11] (`count-c1.py:107`).
- Citation/mention/binding all fire on the same single verb: `cited_pattern` (`count-c1.py:97`) matches the cited `.json` path (space-preceded, `.json`-suffixed, no `..`); `command_pattern` (R20 helper, lookaround-guarded, IGNORECASE) matches only `inspect-signal-decoders` in the entry text; `HEX64` (`(?<![A-Za-z0-9_])ev_[0-9a-fA-F]{64}(?![A-Za-z0-9_])`) matches `ev_5555…5` in text and blob; `bind_new` walk finds no `ok != true` and R21 `refused()` (structural `error/errors/code/status/completion_status/exit_code/raw_result/normalized_result`, `verb-coverage.py:39-55`) is False everywhere; `bind_cli` passes (`ok is True`, `meta.command == verb`, `data` has `evidence_id`+`operation`); R21 `bind` returns 0 (record unblocked, `operation == 'inspect_signal_decoders'`) (`count-c1.py:42-57,120-123`).
- Historical leg contributes exactly one verb: `r22.measure(root, BASELINE)` returns `t1_exercised == ['identify-flutter-build']`, count 1 — OBSERVED record `.ufo/waves/round-23/before-r22-c1.json` (argv rev `aa1450b8…`), and runtime-asserted at `count-c1.py:82-83` (`historical_baseline_changed` → exit 2).
- ⇒ held = 2, `finding: c1_incomplete` (`count-c1.py:129`), counter exit `1` (`count-c1.py:166`); harness compares `{exit, count, finding}` (`counter-fixtures.py:111-112`) → matches expected `{exit:1, count:2, finding:"c1_incomplete"}`.

**Verified (observed):** the recorded selftest run applies byte-identically to the candidate: `verify/initial/selftest.json` ran at snapshot rev `6615aeae…`, which is an ancestor of the candidate (merge-base check), and `git diff --stat 6615aeae→28383514 -- .ufo/waves/round-23` shows ONLY additions under `verify/initial/` (15 files, +357 lines) — `count-c1.py`, `counter-fixtures.py`, `expected-v2.json`, `fixture.json` unchanged (digests above equal at both revs). Its `positive` record: observed `{count: 2, exit: 1, finding: c1_incomplete}`, `passed: true`.

**Fault distinction (the assignment's core question):** yes. The case is baseline + exactly one fully valid new-root witness, so any counter defect of the claimed class flips the observable: ignoring the new root, mis-parsing the S058 gate, over-strict citation/HEX64 regex, broken bind chain → count 1; loose binder / mention-counting → count ≥3; crash → exit 2 / count null / `unevaluable`; false-complete → `c1_complete`/exit 0. All are caught by the `{exit,count,finding}` triple against the frozen template.

### F2 — PASS: independent template, not a decision-derived oracle

`expected-v2.json` is frozen data; at runtime the counter only digests it (`count-c1.py:139`) and the harness compares observed to it (`counter-fixtures.py:111-112`). No expectation is computed from counter decisions on any execution path. Cross-pinning is mutually consistent (counter pins manifest; manifest pins counter-fixtures + fixture.json; fixture.json pins the counter's BASELINE). Author-side caveat: counter and expectations share an author (L1), so this is mechanical independence only, not author independence — consistent with claims `not_claimed: "independent non-author admission"`. Not a defect.

### F3 — POSITIVE-PRESERVING behavior verified

The control envelope stays fully valid through every gate the positive path exercises: refusal walk (top-level `ok:true`; no structural refusal fields in envelope/meta/data/`normalized_result.control`), `meta.command` == verb, operation normalization, `ev_<64hex>` id form. Note the synthetic envelope is deliberately minimal (no `subject`, no raw stdout) — `bind` returns 0 with the `pathless` flag; both module docstrings declare these are control inputs, never producer Evidence claims, so the case validates the counting/binding path, not producer-envelope fidelity. Deliberate and documented; no wrong expectation here.

### F4 — Weak mutations / residual gaps in the `positive` case (no wrong expectation found)

- (a) `count: 2` is aggregate: a mutated counter that mis-attributed the new witness onto the historical verb `identify-flutter-build` would still observe count 2 and pass. Not reachable in candidate code (per-verb `command_pattern` guard at `count-c1.py:120` + per-verb target dict), and per-verb `targets[]` attribution is not compared by the harness — residual gap under mutation only.
- (b) For `positive`, `exit:1` and `finding:"c1_incomplete"` are both functions of `count<6`; the only quantitative discriminator is `count`. The triple still catches crash-to-unevaluable and false-complete, so it is not vacuous.
- (c) The harness records `stdout`/`stderr` (`counter-fixtures.py:106-110`) but judges only the three keys; a counter reaching the right triple by the wrong mechanism (e.g., promoting catalog `mentioned` into `targets`) would pass. That is the manifest's declared scope (code/count/finding), acceptable, but it bounds what `positive` proves.

### F5 — Stale W1 proposal re-evaluated against candidate bytes

`frozen/expected.json` (v1) vs `expected-v2.json`: the `positive` expectation is IDENTICAL (`{exit 1, count 2, c1_incomplete}`) in both; v2 only added refusal/negative cases and hardened `old_source`/`inherited_lost`/`catalog_changed` to exit 2. No stale v1-era positive finding survives — the v2 positive expectation is correct against `28383514`. (Other cases' deltas are out of this seat's scope.)

## Produced files and hashes

- `.ufo/waves/round-23/w2/Fixture01.md` (this report) — sha256 `44af12ee67e964799c1f8868595bc6384651844c56dba2a90fbe9816d4288f5f`

No other files produced; no lane file modified.

## Installs

None.

## Open risks

- The positive case's discriminating power against exotic label-swap mutations is aggregate-only (F4a); per-verb attribution is guarded only by the same code a mutation would alter.
- The recorded passing selftest is anchored at ancestor `6615aeae` with byte-identical reviewed inputs; I did not re-execute (seat forbids it). Any future change to `counter-fixtures.py`/`expected-v2.json`/`fixture.json`/`count-c1.py` invalidates that anchoring until a fresh selftest record exists at the new rev.
- Positive-case fidelity is to the counting/binding contract, not to producer envelope shapes (F3); it cannot detect a binder that under-validates real producer envelopes while accepting the minimal control shape.

## Report trailer

- `.ufo/waves/round-23/w2/Fixture01.md`
