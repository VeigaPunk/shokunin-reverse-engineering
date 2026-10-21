# Fixture14 — R23 counter control `invalid_utf8` (source review)

Candidate `2838351450ff1ee4baa620c962a1153450d53311` (base `aa1450b82f9ede35aada63efe8a34e01c6e02f72`).
Scope: `frozen/expected-v2.json` case `invalid_utf8`; `frozen/fixture.json`; the `invalid_utf8` branch of `tools/counter-fixtures.py`.
Axes: (1) distinguishing power against the stated fault; (2) expectation correctness; (3) positive preservation; (4) oracle independence; (5) mutation breadth.

Method: candidate bytes only (`git show`, `git grep`, `nl`, `sed` print ranges, `sha256` over piped blobs). The suite was not executed and the counter was not run. The recorded artifact `verify/initial/selftest.json` was read only. The four pinned inputs are blob-identical at its `source_rev` `6615aeae642aec36959180e7ea940b2794c7f1cb` and at the candidate (`count-c1.py` 0f966a50018b, `counter-fixtures.py` 55356faade5c, `fixture.json` 92c2f04ae7e0, `expected-v2.json` 7e4199d73d8d), so the recorded run covers these bytes. [Observed]

Stated fault: `LOG.md:2520-2523` (R22 lifecycle, inherited by R23): "invalid UTF-8 … cannot create a witness". [Observed]

## Findings

### 1. Answers to the assignment questions

- **Does the case distinguish the stated fault? Partly.** It exercises one strict-decode site, `tools/count-c1.py:118` (the cited evidence blob). Realistic lenient, skip, or refusal-swallowing mutants of that site change the outcome and are killed. Invalid bytes in knowledge-entry text (`:99`) and in `corpus/SOURCES.md` (`:69`, `:70`, `:86`) can also feed a witness, and no case exercises them (G1, G2). [Observed by code reading; kill claims Inferred from the outcome table]
- **Wrong expectation for `invalid_utf8`? None found.** `{exit 2, count null, finding unevaluable}` matches the exit contract (`count-c1.py:166` sets 0/1; `:167-168` maps `ValueError`/`UnicodeError` to `unevaluable`, exit 2) and the recorded observation. [Observed]
- **Positive preserving? Yes.** It is a one-factor mutation of the positive template. `counter-fixtures.py:38` selects the same single verb; the S058 row (`:82-84`), entry (`:79`), envelope and citation (`:64-70`) are shared code; the only invalid-UTF-8-specific statement is `:91-92`. `git grep` finds `invalid_utf8` only at `counter-fixtures.py:91` and `expected-v2.json:73`. Recorded positive: exit 1, count 2, `c1_incomplete`. [Observed]
- **Independent oracle? Yes for this case.** `fixture.json:56-63` is a hand-typed synthetic envelope (`control: "synthetic, never a producer observation"`). The harness imports only stdlib modules. The `invalid_utf8` expectation block carries the same exit, count and finding values at `frozen/expected.json:73-76` and `frozen/expected-v1.json:73-76` (compared by key/value output, not a byte diff). `round-22/frozen/expected-v2.json` has no `invalid_utf8` entry, so the case is new in R23. The v1 and v2 branches are identical (`counter-fixtures-v1.py:83-84` vs `counter-fixtures.py:91-92`). [Observed]

### 2. Traced path for the case (Observed from code and the recorded run)

1. `counter-fixtures.py:91-92` overwrites `.ufo/waves/round-23/evidence/c1/inspect-signal-decoders.json` with `b'\xff'` after the eligible entry (`:79`) cites it (`:70`).
2. `count-c1.py:99` decodes the entry (ASCII, passes). `:101-110` finds the S058 row with `int(sid[1:]) >= 58` (`:107`) and used-by naming the entry, so the entry is eligible.
3. `:112-114` takes the `.json` path. `:116-117` finds no `..`.
4. `:118` raises `UnicodeDecodeError` (a `ValueError`), caught at `:167-168`, giving stdout `{"finding":"unevaluable", "error": …}` and exit 2.
5. Recorded `verify/initial/selftest.json`, case `invalid_utf8`: observed `{exit 2, count null, finding unevaluable}`, stdout error `"'utf-8' codec can't decode byte 0xff in position 0: invalid start byte"`, stderr empty. The selftest recorded `passed 21, total 21`.

The case reaches the intended decode, so the expectation is not satisfied by a different branch.

### 3. Weak mutations and gaps (surviving mutants), ranked

- **G1 (stated-fault survivor; single site).** `count-c1.py:99` is the only strict decode of knowledge-entry content. That content drives eligibility (`:101-110`), verb mentions (`:100`, `:119-121`), evidence ids (`:111`) and cited paths (`:112`). A lenient `decode('utf-8','replace')` at `:99` lets an eligible entry with invalid bytes create a witness. No fixture places non-UTF-8 bytes in any knowledge entry, so this mutant survives the suite. Suggested control (not implemented): eligible entry carrying raw `\xff` in a non-verb line, expected `{exit 2, null, unevaluable}`.
- **G2 (stated-fault survivor; three sites).** `corpus/SOURCES.md` is decoded strictly at `:69`, `:70`, `:86`. `rows` (`:86`) drives eligibility. Relaxing only `:86` is masked by the whole-file strict decode at `:70`; relaxing `:69`, `:70` and `:86` together lets an invalid byte in a non-gating column of an S058 row keep the row eligible. No case covers this. Suggested control: S058 row with raw `\xff` in column 3, expected exit 2.
- **G3 (decode-scope divergence from the reused R22 read path; unpinned).** R23 decodes only cited `.json` paths of eligible entries (`:109-114`, decode at `:118`). The reused R22 path decodes every cited evidence path of verb-matched entries, carriers included: `round-22/tools/count-c1.py:115-120` (`read_blob`, strict decode at `:120`), `:147-151` (verb gate, then `cited_prefixes`), `:153-156` (path loop, read at `:156`). `round-20/tools/verb-coverage.py:127-129` (`cited_prefixes`) has no `.json` filter. Consequences: a non-JSON carrier with invalid bytes gives exit 2 under R22 read semantics and is silently ignored in R23 (`:113-114`, comment "Carrier bytes are cited provenance"). An ineligible entry's invalid cited JSON is never read in R23 but is read by R22 when verb-matched. No case pins either behaviour. This affects only exit classification, not witnesses. [Observed code divergence; intent Inferred from the `:114` comment]
- **G4 (positive-preservation control absent).** No case cites a non-JSON carrier with invalid bytes beside a valid envelope. A correct candidate should give `{exit 1, count 2, c1_incomplete}` (carrier skipped at `:113-114`, JSON still binds). Without this control, a mutant that drops the `.json` gate and turns the positive into `unevaluable` survives. Suggested control: add a `.stdout` carrier with `\xff` cited by the same entry.
- **G5 (oracle reason unpinned; witness shape incidental).** `counter-fixtures.py:111-112` compares only `exit`, `count` and `finding`. `expected-v2.json` has no `error` key, so an `unevaluable` from another cause on this fixture passes. The shared template limits this: a fixture-wide defect also breaks `positive`. The current witness is also incidental: `b'\xff'` replaces the whole envelope, so the evidence id disappears. A lenient decoder is killed only because the id is missing, not because of the UTF-8 fault. Suggested controls: pin `error` contains `codec can't decode` for this case, and add a valid envelope with a raw `\xff` inside a string value (id present), expected exit 2.
- **G6 (undocumented policy split; no wrong expectation).** Undecodable bytes are fatal (`:118` → `:167-168` → exit 2). Malformed or duplicate JSON is not fatal: `bind_new` returns 2 at `:55-56`, the `== 0` test at `:123` fails, the verb is not counted, and the run exits 1 (`duplicate_member`, `expected-v2.json:63-67`). R22 has the same split (`round-22/tools/count-c1.py:163-164`, `unsupported_candidates`). The LOG sentence does not say which class is "could-not-evaluate". The expectations match the code; the rationale is undocumented.

Equivalent mutant, not a gap: removing `UnicodeError` alone from `count-c1.py:167` changes nothing, because it is a `ValueError` subclass. Its presence is dead weight.

Limit: `invalid_utf8` cannot observe the historical identify witness, since exit 2 emits no count. Preservation of that witness is checked only by `positive`.

### 4. Adjacent (outside Fixture14; flagged, not solved)

- **A1 — `old_source` oracle moved, and the S058 floor is now untested.** `expected-v2.json:33-36` expects exit 2. `expected-v1.json:33-36` expected exit 1, count 1. The recorded v2 stdout is `{"error": "historical_sources_changed"}`, produced at `count-c1.py:72-73` before the entry loop. No case reaches the S058 floor at `:107`. The v1→v2 expectation change coincides with the new check, which is a decision-derived expectation move (Inferred from the sequence). Route to the `old_source` seat.

### 5. Stale W1 proposal findings touching this item (re-evaluated at candidate)

- `w1/CounterGitIsolation.md` ("`UnicodeError`, `RecursionError` → unevaluable"): holds at `count-c1.py:167-168`.
- `w1/CounterRefusals.md` C7 ("duplicate-member and non-finite JSON rejected"): holds only as "not counted, exit 1" (`:55-56`, `:123`). "Rejected" does not mean exit 2 (see G6).
- `w1/ReviewFrozenTargets.md` ("R23 counting command absent from `tools/`"): stale. `.ufo/waves/round-23/tools/count-c1.py` exists at the candidate (blob 0f966a50018b). Noted only; outside this item.

## Produced files and hashes

- `.ufo/waves/round-23/w2/Fixture14.md` (this report). Its sha256 is in the final message.
- Pinned inputs, verified at the candidate:
  - `frozen/expected-v2.json` sha256 `458b30d5a6420c1b37874c3364d3ae3b22529d6c3560b5241848a21eec97096f` (equals `count-c1.py:25` `SELFTEST_MANIFEST_SHA256`).
  - `tools/counter-fixtures.py` sha256 `f2990b35d113b5e44317e7f00e6ca5157baae1efb5ee1a1b8e4995d0ace1a97f` (matches the manifest `inputs`).
  - `frozen/fixture.json` sha256 `a1f5aff8ebb5e5d327522031b74ed91283708907af0fc4a6df24812479bfef4b` (matches the manifest `inputs`).
  - `round-22/tools/count-c1.py` sha256 `c925918fb871151f86065aa5b3e9d10334ab845ed67c265ae0977f05e09b1879` (equals `count-c1.py:23` `LEGACY_SHA256`).
- Contract deviation, disclosed: during review I wrote three scratch copies of candidate blobs (`r22-counter.py`, `r21-helper.py`, `r20-helper.py`) to `/tmp`, outside the allowed paths. I removed them with `rm -f`; none remain. No runtime clone was created and no git write was made.

## Installs

None.

## Open risks

- The recorded selftest (21/21) is author-side evidence at `6615aea`. I read it and did not re-run it. [Observed record; not independently verified]
- The only stated-fault wording is `LOG.md:2520-2523` (R22). I found no R23-specific statement of the decode scope. Whether G3's scope narrowing is intended is Unknown; the `:114` comment suggests yes, but nothing pins it.
- The exit-2 expectation is stricter than the LOG sentence ("cannot create a witness"). It follows the counter's exit contract (`:166-168`), not the LOG. This is acceptable, but the oracle should cite the contract. [Inferred]
- No independent (non-author) admission of these findings.

Report: .ufo/waves/round-23/w2/Fixture14.md
