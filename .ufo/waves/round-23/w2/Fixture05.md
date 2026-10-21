# Fixture05 — R23-C1 `missing_source` case, source review

Scope: frozen case `missing_source` (`frozen/expected-v2.json:28-32`), `frozen/fixture.json`, and the `missing_source` branch of `tools/counter-fixtures.py` (lines 75-76). Candidate `2838351450ff1ee4baa620c962a1153450d53311`; baseline `aa1450b82f9ede35aada63efe8a34e01c6e02f72`.

Method: `git show` / `git rev-parse` on candidate blobs; copies in `runtime/Fixture05/`; static trace of the counter and binder; retained producer outputs read only. The suite and counter were not executed. Production files, peer reports, and configs were not touched.

Labels: [observed] = blob, hash, line, or retained output read directly. [inferred] = static trace. [unknown] = not checked.

## Verdict

- **Expectation correct.** `exit 1, count 1, c1_incomplete` matches the candidate rule. No wrong expectation found for this case.
- **Distinguishes the fault, through `count` only.** The fault is the forward source link: the entry's first `source:` line must cite an S058+ row. Removing that gate changes count 1 → 2. Exit and finding are identical for the faulty and correct counter.
- **Minimal differential.** `missing_source` differs from `positive` only in line 1. Its discriminating power depends on `positive` binding in the same run.
- **Weak mutations survive the whole suite:** a body-only S-ID scan and removal of the `startswith('source:')` gate. Separately, `missing_source` alone passes any regression that stops new binding.

## Findings

### F1 — Pinned inputs [observed]
- `counter-fixtures.py` blob `55356faade5c11165783fc551a8a7f5275e65a6f`, sha256 `f2990b35d113b5e44317e7f00e6ca5157baae1efb5ee1a1b8e4995d0ace1a97f` (equals `expected-v2.json` `inputs`).
- `frozen/fixture.json` blob `92c2f04ae7e01456cffd8b97aefcd63bcaaa55f5`, sha256 `a1f5aff8ebb5e5d327522031b74ed91283708907af0fc4a6df24812479bfef4b` (equals `inputs`).
- `frozen/expected-v2.json` blob `7e4199d73d8dd0f8ef27e56cb04935d015eea93d`, sha256 `458b30d5a6420c1b37874c3364d3ae3b22529d6c3560b5241848a21eec97096f` (equals counter constant `SELFTEST_MANIFEST_SHA256`).
- `count-c1.py` blob `0f966a50018bba2fa5af3d6f9af1541f660c43c2`, sha256 `f4b8d16ac195ca106a99cbb9236d36d1283dee349c6fef3a49567de0bbea0cc2`.
- The four pinned blobs are byte-identical at `6615aeae…` and at the candidate (`git rev-parse --short`), so retained outputs at `6615aeae` apply to candidate bytes.

### F2 — Fault injection and positive preservation [observed]
- `counter-fixtures.py:38` default selection `['inspect-signal-decoders']`; no override for `missing_source`.
- `:47` base first line `source: S058 synthetic isolated control`.
- `:70` verb line `inspect-signal-decoders ev_<64×'5'> .ufo/waves/round-23/evidence/c1/inspect-signal-decoders.json`.
- `:75-76` replaces the first line with `source: none`. The target string matches exactly, so the replacement is not a silent no-op.
- `:83-84` S058 row keeps used-by = ENTRY. The reverse link (row→entry) is intact; only the forward link (entry→S-ID) is removed.
- Evidence file, cited path, and envelope IDs are identical to `positive`. The diff is line 1 only.
- Python `-I` check on the candidate text: `missing_source` text has `S-ids in text: []`; first line `'source: none'`. Positive first line has `S058`.

### F3 — Counter gate and binding path [observed lines; outcome inferred]
- `count-c1.py:101-110`: first-line gate (`:102`), S-ID scan on `first` (`:105`), row and used-by check (`:107`), `continue` (`:110`).
- `count-c1.py:111-124`: cited path, `ids`, and `bind_new` on each T1 verb mentioned in the entry; witness appended at `:123-124`.
- `count-c1.py:81-83`: historical baseline must equal `['identify-flutter-build']`, so the expected count 1 includes that witness.
- `count-c1.py:129`: `finding = c1_complete if 6 else c1_incomplete`. `main()` exits 0 only at 6 (`count-c1.py` main).
- Candidate, `missing_source`: no S-ID → `continue` at `:110` → no new binding → count 1, exit 1, `c1_incomplete`. [inferred]
- Gate removed (mutant): same envelope → `bind_new` → `r22.bind_cli` (`r22-count-c1.py:69-96`) → `r21.bind` (`r21-verb-coverage.py:77-101`, operation rule `:85` `verb.replace('-','_')`, `ID` `:21`, `refused` `:39-55`, `records` `:58-75`) returns `evidence_bound` → count 2. [inferred]
- Positive binds: `fixture.json:56-64` operation `inspect_signal_decoders`, 64-hex id at `:62`. [inferred]

### F4 — Expectation values [observed]
- `expected-v2.json:28-32`: `{"exit": 1, "count": 1, "finding": "c1_incomplete"}`.
- Count 1 = historical `identify-flutter-build` (baseline; `claims.json` cites R22 C1=1/6), new witness excluded. Consistent with the rule.
- Literal JSON, SHA-pinned in the counter. Not computed from counter output.
- v1 (`frozen/expected-v1.json`) has the same `missing_source` values. A diff of `counter-fixtures-v1.py` vs v2 has hunks only at `57a58,63`, `64a71,72`, `85c93,102`; the `missing_source` branch is unchanged.

### F5 — Template independence [observed]
- `counter-fixtures.py:7-13` imports stdlib only (`copy, json, os, Path, subprocess, sys, tempfile`). No decision import. The counter runs as a subprocess with `-I -B`.
- Operation strings match retained producer envelopes, not only the binder convention:
  - `uart-help.envelope.json`, `inventory.envelope.json`: `inspect_signal_decoders`.
  - `decode-uart-hi.envelope.json`, `decode-official-uart.envelope.json`: `decode_signal_recording`.
  - `inspect-dart-aot-saber-1330203.envelope.json`: `inspect_dart_aot`.
  - `identify-flutter-build-saber-1330203.envelope.json`: `identify_flutter_build`.
- Synthetic evidence IDs and `normalized_result.control` are hand-authored.

### F6 — Retained producer outputs [observed; not reproduced by me]
- `verify/initial/selftest.json` (`source_rev 6615aeae…`): `passed: true`, 21/21, `selftest_clean`. `missing_source` observed `{count 1, exit 1, c1_incomplete}`.
- `verify/initial/metadata-red-green.json`: `counter_sha256` equals F1 candidate hash. It has three comparisons only (`positive`, `meta_false`, `meta_array`). None varies the source gate.

### Weak mutations [inferred from trace; none executed]

| # | Mutant | `missing_source` | Whole suite | Note |
|---|---|---|---|---|
| W1 | S-ID scan over whole text (`count-c1.py:105`) instead of `first` | survives: text has zero S-IDs | survives all 21: no case places an S-ID outside line 1 | first-line restriction never exercised |
| W2 | Remove `startswith('source:')` gate (`:102`) | survives: `source: none` still starts with `source:` | survives all 21: no case has an unlabeled header | gate untested |
| W3 | Any regression that stops new binding | passes (count 1) | caught only by `positive` | per-case attribution vacuous |
| W4 | Row-only eligibility (drop S-ID requirement, `:105-107`) | killed (count 2) | — | realistic regression, caught |
| W5 | Delete gate `:101-110` | killed (count 2) | — | caught |
| W6 | Drop historical witness | killed (count 0) | — | case also pins the historical floor |
| W7 | Treat `source: none` as unevaluable | killed (exit 2) | — | caught |

Survivors W1 and W2 are the fault family the falsifier "source linkage absent" names. Naming: `missing_source` tests a present-but-non-linking label (`source: none`), not an absent header.

Suggested discriminators for L1, not added (frozen files are read-only):
- Body-only variant: first line `source: none`, body contains `S058`; expect `1/1/c1_incomplete`. Kills W1.
- Unlabeled-header variant: first line `S058 synthetic isolated control`, row used-by = ENTRY; expect `1/1/c1_incomplete`. Kills W2.
- Report `missing_source` as `positive − 1`, or assert `positive.count == 2` as a per-case precondition. Addresses W3.
- Retain a red/green run that mutates `count-c1.py:101-110`. Closes the W4-class evidence gap.

### Informational [observed]
- `counter-fixtures.py:84` splice leaves a blank line between the S057 and S058 rows, because baseline `SOURCES.md` has a blank line before `## Paths`. The line-based parser (`count-c1.py:86-91`) ignores blank lines; no effect.
- Not audited: the other 20 cases; `historical_baseline_changed` (`count-c1.py:82`) is assumed to hold at baseline, per `claims.json`.

## Produced files and hashes
- `.ufo/waves/round-23/w2/Fixture05.md` (this report).
- Retained copies in `.ufo/waves/round-23/runtime/Fixture05/` (ignored runtime; blob-identical to candidate):
  - `r20-verb-coverage.py` sha256 `cfbf1880c4fb2bba80e3c2e40e236165a67c03bf51cced4983b469cfe315b26f`
  - `r21-verb-coverage.py` sha256 `615369384bf821a44e4d3c458006ed169939025d8fd3415f318ae37bb52f887b`
  - `r22-count-c1.py` sha256 `c925918fb871151f86065aa5b3e9d10334ab845ed67c265ae0977f05e09b1879`
  - `r23-count-c1.py` sha256 `f4b8d16ac195ca106a99cbb9236d36d1283dee349c6fef3a49567de0bbea0cc2`
  - `r23-counter-fixtures.py` sha256 `f2990b35d113b5e44317e7f00e6ca5157baae1efb5ee1a1b8e4995d0ace1a97f`
  - `fixture.json` sha256 `a1f5aff8ebb5e5d327522031b74ed91283708907af0fc4a6df24812479bfef4b`
  - `expected-v2.json` sha256 `458b30d5a6420c1b37874c3364d3ae3b22529d6c3560b5241848a21eec97096f`
  - `retained-selftest.json` sha256 `d88207f14f27699cd4365734dab5acf0ab040abe9d002bac5def088f346f7d7d`
  - `retained-red-green.json` sha256 `1286b8c41deff5892b2889073487b75c222a61fa1fa7eef8f3d1ad21ade97e79`
  - `retained-r22-c1.json` sha256 `d38056cc3da5cc41706b0f8431c8709981112ac6ec9d2957b5bc3bf65b6f87d1`

## Installs
None.

## Open risks
- Candidate-level results rest on static trace plus a retained producer run on identical bytes. I did not reproduce the suite, as assigned.
- No retained mutant run exercises the source gate (W4 evidence gap).
- The real producer envelope schema beyond `operation` and `meta.command` was not compared.
- Baseline historical count (1) is taken from `claims.json`, not re-derived.
