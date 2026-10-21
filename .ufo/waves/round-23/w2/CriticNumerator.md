# CriticNumerator — R23-C1 denominator / numerator / debugger remainder

Candidate C=2838351450ff1ee4baa620c962a1153450d53311, B=aa1450b82f9ede35aada63efe8a34e01c6e02f72.
All bytes read via `git show C:PATH` / `git rev-parse C:PATH`. Source review only: the counting
command, selftest, producers and targets were NOT run (this seat is not a Run* seat).

Verdict: no numerator-inflation counterexample found at C. By source tracing, the expected
count is k=4/6 [INFERENCE: not executed]. The two unheld verbs are exactly `debug-with-gdb` and
`debug-with-rizin`. One fixable counter blind spot does not affect C.

## Findings

### F1 — Denominator frozen to the claimed six verbs (observed)
- `.ufo/waves/round-22/tools/count-c1.py` at C has sha256 `c925918f…1879`, which equals the
  `LEGACY_SHA256` pin in `.ufo/waves/round-23/tools/count-c1.py:23`.
- Legacy `T1` (`round-22/tools/count-c1.py:31-32`) is `identify-flutter-build, inspect-dart-aot,
  debug-with-gdb, debug-with-rizin, inspect-signal-decoders, decode-signal-recording`. It is
  identical, in the same order, to `claims.json` `claims[0].t1`.
- The R23 counter keys its targets and held set only on `r22.T1` (`count-c1.py:92-93,127`).
  `t1_total` is hard-coded to 6 and `finding` is complete only if `len(held)==6`
  (`count-c1.py:129-130`), so the denominator cannot grow or shrink.
- The catalog must be byte-equal to B (`:64-65`), and the historical evidence tree must match B
  (`:66-68`).
- Residual issue: the counter never cross-reads `claims.json`. The hash pin makes this harmless.

### F2 — Numerator is a per-verb union; duplicates cannot add a verb (observed)
- `held = [verb for verb in r22.T1 if targets[verb]['exercised']]`, with
  `exercised = bool(historical or new)` (`count-c1.py:125-127`). Any number of witnesses for one
  verb contributes at most 1.
- Cross-verb aliasing is closed in two places:
  - `bind_cli` requires `meta.command == verb` (`round-22 count-c1.py:79`).
  - `r21.bind` requires `record.operation == binding_verb.replace('-','_')`
    (`round-21/tools/verb-coverage.py`, `bind`).
  - So one envelope binds at most one verb.
- Duplicated identify envelopes cannot add a verb:
  - `connect-dart-symbols/identify-flutter-build-saber-1330203.envelope.json` is `ok:true`,
    `meta.command identify-flutter-build`, `ev_5e99…f2c6`. It could only feed the
    already-held historical `identify-flutter-build`.
  - It is also not cited by any `corpus/knowledge/` entry at C. `git grep round-23/evidence/c1`
    finds only the two new entries, and the Dart entry mentions only bare `connect-dart-symbols/`
    (`2026-10-21-r23-dart-legacy-layout-boundary.md:31`). That does not match `cited_pattern`
    (`count-c1.py:97`).
- Duplicated signal envelopes cannot add a verb:
  - `decode-uart-hi` (`ev_bcad…bd3e`) and `decode-official-uart` (`ev_1d36…7e5c`) both have
    `meta.command decode-signal-recording`, so together they add 1.
  - `uart-help` (`ev_4be1…94a`, `meta.command inspect-signal-decoders`) has an id that is not
    quoted in any entry, so it is unbound. If it were bound, it would still add 0 beyond
    `inventory`.
- `counter-fixtures.py` includes a `same_verb` control expecting count 1
  (`frozen/expected-v2.json`). That control was not run here.

### F3 — Per-verb witness trace at C (observed inputs, inferred outcome)

Source eligibility (`count-c1.py:104-108`):
- S058–S061 are all tier A, `mined`, opened `2026-10-21`.
- S058, S059 and S060 list `corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md` in
  used-by.
- S061 lists `corpus/knowledge/2026-10-21-r23-dart-legacy-layout-boundary.md` in used-by.
- Both entries' first lines start `source:` and cite those ids.

| Verb | Witness | Envelope facts | Expected |
|---|---|---|---|
| identify-flutter-build | historical, measured at B (asserted `:82-83`) | R22 entries blob-identical at C: `…r22-flutter-positive-dart-refusal.md` 41b69636…, `…r22-flutter-static-boundary.md` e1d05bf7… | held |
| inspect-dart-aot | `inspect-dart-legacy-saber.envelope.json` | ok:true, meta.command inspect-dart-aot, data.operation inspect_dart_aot, `ev_d2ff…7491`; no nested refusal keys | held |
| inspect-signal-decoders | `inventory.envelope.json` | ok:true, matching command/operation, `ev_940c…fdd0`; no structural refusal keys | held |
| decode-signal-recording | `decode-uart-hi`, `decode-official-uart` | ok:true, matching, two ids | held (once) |
| debug-with-gdb | none | — | unheld |
| debug-with-rizin | none | — | unheld |

- Refusal is not counted: `decode-invalid-decoder.envelope.json` has `ok:false`,
  `error.code execution_failure` and `error/details/diagnostics.exit_code 1`. `bind_new` returns 1
  at `count-c1.py:51`.
- The inventory's `signature` decoder load failure (entry `:21-24`) carries no `error`, `errors`,
  `code`, `status` or `exit_code` refusal field. It therefore neither blocks nor is hidden; the
  entry discloses it. Treat this as a tradeoff, not a defect.

### F4 — The two debugger verbs are precisely the remainder (observed)
- `git grep -i -E "debug.with.gdb|debug.with.rizin|gdb.console|rizin.debug.command"` over C's
  `corpus/knowledge` returns zero lines.
- With no mention, there are no candidate entries (`count-c1.py:120`). The two verbs cannot be
  held by mention, alias or historical witness, because B's held set is asserted to be identify
  only.
- The prose "Both debugger verbs remain unheld" (dart entry `:66`, signal entry `:117`) uses
  spaces, not verb tokens, so it creates no mention.
- `corpus/knowledge` changes B→C are 2 added entries only; the README, SOURCES and lessons files
  are modified/added outside the scanned prefix.

### F5 — Counterexample: the "inherited identify lost" check is blind to knowledge-entry loss (observed design, inferred effect)
- Historical witnesses are computed only at the baseline: `r22.measure(root, BASELINE)`
  (`count-c1.py:81,92`).
- The checks at the measured revision are:
  - historical evidence tree identity (`:66-68`);
  - SOURCES row-prefix preservation (`:69-73`).
- No check pins the pre-round `corpus/knowledge/` blobs at the measured revision. A revision that
  deletes or rewrites both R22 identify entries would still report `identify-flutter-build` as
  held.
- The fixture `inherited_lost` (`counter-fixtures.py:95-96`) only unlinks a historical evidence
  envelope, which the tree check already catches. It does not exercise entry loss.
- Impact: falsifier "inherited identify lost" and no_harm "All pre-round knowledge … unchanged".
  At C the effect is nil, because both entries are blob-identical (F3). This is a fixable defect,
  not a tradeoff.
- Smallest safe correction: in `measure`, require
  `git rev-parse rev:<path> == git rev-parse BASELINE:<path>` for every `corpus/knowledge/` path
  in B. Alternatively, also run `r22.measure(root, rev)` and require `identify-flutter-build` to be
  in its `t1_exercised`. Then add a fixture that deletes or edits the R22 identify entry.

### F6 — Minor, no inflation (observed)
- The R23 scan silently drops `bind_new` results equal to 2 (unevaluable). The legacy counter
  exposes these as `unsupported_candidates` (`round-22 count-c1.py:163-169`). This loses
  diagnostics only.
- `cited_pattern` keeps a trailing `.`: a sentence-final `…envelope.json.` would be skipped as
  non-`.json`. That is a false negative only, and no such citation exists at C.

## Produced files and hashes
- `.ufo/waves/round-23/w2/CriticNumerator.md` (this file; sha256 is in the final handoff).
- Contract deviation: one transient `/tmp/r21.py` copy of the pinned r21 helper (sha256
  `615369384bf8…`, equal to the pin) was written and immediately deleted. No other writes.

## Installs
None.

## Open risks
- k=4 is source-traced, not observed. The designated Run* seat's single
  `count-c1.py --root <LANE> --rev C` output is authoritative.
- Run-stdout ↔ envelope equality is outside this counter (`limit` field) and was not checked here.
- Source relevance and scope admission are still manual.
- The connector's `connect-dart-symbols/` envelopes are `ok:true` but uncredited. Any future entry
  citing them adds nothing to the verb count, but would need its own provenance review.
- F5 remains latent for later revisions until the check is fixed.
