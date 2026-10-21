# Fixture09 — round-23 `nested_refusal` source review

Seat: `KaidokuR23.Fixture09` (leaf, source-review only). Candidate: `2838351450ff1ee4baa620c962a1153450d53311`. Baseline B: `aa1450b82f9ede35aada63efe8a34e01c6e02f72`.
Scope: `frozen/expected-v2.json` case `nested_refusal`, `frozen/fixture.json`, and the nested branch of `tools/counter-fixtures.py`. The suite, the counter and the fixture were not executed.

Labels: **Observed** = read from candidate blobs (`git show 2838351…:PATH`) or from a recorded producer artifact. **Inferred** = static trace of candidate code, not executed. **Unknown** = not determinable from the sources.

The stated fault was not given in the seat prompt. I used the falsifier `refusal counted` (`.ufo/waves/round-23/claims.json`) and the R23 stated fault in `corpus/lessons/round-23.md:48` ("metadata ancestry was discarded before binding").

## Verdict

1. **Expectation: correct.** `expected-v2.json:48–52` = `{exit 1, count 1, c1_incomplete}`. It is an independent constant, unchanged from v1. Derivation: the baseline `identify-flutter-build` witness contributes 1, and the refusal removes the one `inspect-signal-decoders` witness. Positive-preserving: relative to `positive`, the only input change is `counter-fixtures.py:52–53`.
2. **Distinguishes the stated fault: no.** The stated R23 fault is about metadata ancestry. This case puts the refusal under `data`, which the pinned R22 binder already rejects. The expected result holds with or without the R23 pre-walk, so the case is a redundant composite-chain guard, not a discriminator of the R23 change.
3. **Weak mutation: yes.** Placement under `data` is absorbed by pinned code. No candidate case exercises the R23-decisive refused shape under `meta`.

## Findings

### F1 — `nested_refusal` cannot discriminate the R23 wrapper (Observed source; Inferred outcome)

- Mutation: `counter-fixtures.py:52–53` sets `data.normalized_result = {'errors': ['execution_failure']}` on the single default verb (`:38`; no override for this name at `:39–44`). The rest of the path (`:47–50`, `:64–70`, `:72–82`) is identical to `positive`.
- Candidate: the R23 pre-walk returns 1 at `count-c1.py:51` (`r21.refused(data)` via `normalized_result`), before the binder call at `:54`.
- Counterfactual, pre-walk removed or its refused branch deleted: the pinned R22 binder still returns 1. `round-22/tools/count-c1.py:76` and `:79` pass; the record DFS at `:84–94` returns 1 at `:92` on `refused(record)`; R21 `refused()` recurses into `normalized_result` (`round-21/tools/verb-coverage.py:52–54`). Result: exit 1, count 1, unchanged.
- Consequence: no targeted `count-c1.py` regression of refusal ancestry under `data` changes this case's result. Dropping the pre-walk, dropping its refused branch, or re-routing the record through `r21.bind` (which blocks at `verb-coverage.py:68, 97–98`) all leave it green. Its only failure modes are changes to the pinned chain, which the digest pins already catch (`count-c1.py:23, 62–63`; R22 `HELPER_SHA256`).
- Corroboration (Observed, documents): W1 `CounterRefusals.md:200` marks the data DFS as "none nested" (no gap). W1 `CriticGate.md:184–185` lists the bind_cli nested traversal as a covered non-finding. The producer's recorded red/green (`verify/initial/metadata-red-green.json`) compares legacy/current only for `positive` (0/0), `meta_false` (0/1) and `meta_array` (0/1); it has no `nested_refusal` row.

### F2 — the R23-decisive refused shape under `meta` is untested (Observed case list; Inferred gap)

- Candidate meta cases exercise only the `ok` branch: `meta_false` (`counter-fixtures.py:58–59`) and `meta_array` (`:60–61`, `raw_result=[{'ok': False}]`). No case puts an `error`/`errors`/`code`/`status`/`exit_code`-shaped dict under `meta`.
- Legacy `refused(meta)` is one level deep (`verb-coverage.py:39–55`, called at `round-22/tools/count-c1.py:79`). It misses `meta.diagnostics.error` and `meta.raw_result[0].errors`. Legacy therefore counts such an envelope. Only the R23 pre-walk refused branch (`count-c1.py:51` applied to meta descendants) blocks it. This is the discriminator the nested case should have been.
- W1 proposed exactly this as `meta_nested_refusal` (`CounterRefusals.md:218`; `meta.diagnostics.error` at `:109`). The candidate did not adopt it. Recommended, not implemented: add the case with expected `{exit 1, count 1, c1_incomplete}`, using the F4 derivation.
- Of the R23-decisive controls (legacy counts, R23 blocks), `meta_false` and `meta_array` (recorded) exercise the ok branch. Only `sibling_refusal` (`counter-fixtures.py:62–63`, `result={'errors': …}`, Inferred decisive) exercises the refused branch.

### F3 — narrow refusal shape (Observed)

- Only the truthy `errors` list is used (`counter-fixtures.py:53`). The REFUSALS vocabulary (`verb-coverage.py:16–20, 46–49`), `exit_code` (`:50–51`) and `error` (`:43–45`) are not exercised. Inside `data` the pinned DFS also covers them, so the impact is small. The case still does not cover the shapes its name implies.

### F4 — expectation, independence, positive-preservation (Observed)

- `expected-v2.json:48–52` = `{exit 1, count 1, finding c1_incomplete}`. Identical in `expected-v1.json:48` and `expected.json:48`. The v1→v2 diff hunks (`@@ -1,7`, `@@ -31,9`, `@@ -74,6`) do not touch these lines. The value was not moved to fit the candidate.
- Derivation: `count-c1.py:81–83` requires historical `t1_exercised == ['identify-flutter-build']`, so the baseline contributes 1. The new witness at `:123` is blocked by the refusal. Positive = 2, nested = 1, delta 1 = the one removed witness. The exit is 1 because the count is not 6 (`:166`).
- Recorded run (`verify/initial/selftest.json`, `source_rev` 6615aea): `selftest_clean`, 21/21 passed. `nested_refusal` observed `{count 1, exit 1, c1_incomplete}`, passed. `positive` observed count 2, passed. Recorded, not re-executed by me.
- The recorded run applies to the candidate. `git diff --stat 6615aea 2838351` over `tools/`, `frozen/`, `corpus/SOURCES.md`, `.ufo/waves/round-20` and `round-22` is empty. The sha256 values match `verify/initial/source-pins.json` (see Checks).

### F5 — adjacent, out of item: `old_source` expectation moved v1→v2 (Observed diff; Inferred ordering)

- `expected-v1.json:33–37` = exit 1 / count 1 / c1_incomplete. `expected-v2.json:33–37` = exit 2 / null / unevaluable. The fixture branch text is unchanged (v1 `counter-fixtures-v1.py:69–70, 77–78`; candidate `counter-fixtures.py:77–78, 85–86`).
- The counter changed. The new `historical_sources_changed` guard (`count-c1.py:69–73`) runs before the entry scan (`:98` onward), so the S051 eligibility rule (`:105–107`) is never reached by this case.
- W1 `ReviewSourceReuse.md:11` had stated the intent as "S051 cannot qualify" and flagged the missing invariant. The move follows that finding. However, the frozen case now asserts the guard, not non-qualification, and the change landed in the same manifest revision (schema and counter-fixtures digest also bumped). The recorded run passes against the moved value, so it is not independent evidence. L1 should confirm that the rationale is recorded.
- Adjacent: no case mutates the S058 row's tier, status or date (`count-c1.py:107`), so those predicates have no negative control.

### F6 — oracle integrity (Observed)

- The manifest pins `counter-fixtures.py` and `fixture.json` (`expected-v2.json` `inputs`), but not the counter under test. The manifest's own digest is a constant inside that counter (`count-c1.py:25`). A commit that edits `count-c1.py:25` and `expected-v2.json` together passes selftest. Only review protects it. `verify/initial/source-pins.json` is producer-written, not an independent pin.
- Templates are hand-authored to the binder's schema (`fixture.json:56–68`, labelled synthetic). They test binder behaviour, not producer conformance.

### F7 — adjacent, out of item: `refused_parent` also absorbed (Observed; Inferred)

- `counter-fixtures.py:50–51` (top-level `ok:false`) is rejected by legacy `round-22/tools/count-c1.py:76`. It does not discriminate the R23 wrapper either. Noted only.

## W1 stale findings re-evaluated against the candidate

| W1 item | Claim | Status at `2838351` |
|---|---|---|
| `CriticGate.md:184–185` | bind_cli nested traversal covers nested/list refusals in the envelope | Confirmed for `data` (round-22 `:84–94`). Not for `meta` refused shapes (F2). |
| `CounterRefusals.md:199–200` | `meta` has no DFS; `data` DFS has no gap | `data` confirmed. `meta` refused branch exists in code (`count-c1.py:51`) but has no case (F2). |
| `CounterRefusals.md:218` N1 | `meta_ok_false`, `meta_nested_refusal` | `meta_false` present (`:58–59`). `meta_nested_refusal` absent (F2). |
| `CounterRefusals.md:219` N2 | `sibling_refusal`, `sibling_error` | `sibling_refusal` present (`:62–63`). `sibling_error` absent. |
| `ReviewEvidenceBinding.md:9, 13` | add metadata `ok:false` and metadata-array refusal controls | `meta_false`, `meta_array` present; red/green recorded (`metadata-red-green.json`). |
| `ReviewSourceReuse.md:11` | missing invariant for a changed inherited row; `old_source` expects S051 cannot qualify | Guard added (`count-c1.py:69–73`). `old_source` moved to exit 2 (F5). |

## Checks run

- Read-only only: `git show`, `git grep`, `git diff --stat`, `sha256sum` against candidate blobs. A `python3` JSON parse of recorded `selftest.json`, `metadata-red-green.json` and `source-pins.json`, for display only.
- No counter, fixture or suite executed. No mutation run. No pacman or other installs. No writes outside `.ufo/waves/round-23/w2/`.
- Candidate blob sha256 (computed here): `tools/count-c1.py` = `f4b8d16ac195ca106a99cbb9236d36d1283dee349c6fef3a49567de0bbea0cc2`; `tools/counter-fixtures.py` = `f2990b35d113b5e44317e7f00e6ca5157baae1efb5ee1a1b8e4995d0ace1a97f`; `frozen/fixture.json` = `a1f5aff8ebb5e5d327522031b74ed91283708907af0fc4a6df24812479bfef4b`; `frozen/expected-v2.json` = `458b30d5a6420c1b37874c3364d3ae3b22529d6c3560b5241848a21eec97096f`; round-22 `tools/count-c1.py` = `c925918fb871151f86065aa5b3e9d10334ab845ed67c265ae0977f05e09b1879` (equals `LEGACY_SHA256`, `count-c1.py:23`).

## Produced files and hashes

- `.ufo/waves/round-23/w2/Fixture09.md` (this file). Its own digest is recorded in the seat hand-off, since a file cannot contain its own digest.
- Candidate blob digests listed above (read-only).

## Installs

None.

## Open risks and unknowns

- F1 and F2 outcomes are static traces, not executions. A designated Run seat or L1 can confirm them with one mutation pass in a private clone. Predictions: (a) deleting `count-c1.py:44–56` leaves `nested_refusal` passing; (b) adding a `meta_nested_refusal` case passes on the candidate and fails when the pre-walk refused branch is removed. Not run here.
- Unknown: the producer's complete red/green (not present in the candidate beyond `metadata-red-green.json`) may cover sibling or nested cases. I could not determine this from the sources.
- Self-pinned expectations and hand-authored templates (F6) limit what selftest can prove.
