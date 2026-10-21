# Fixture06 — `old_source` case review (R23-C1)

Seat: KaidokuR23.Fixture06 · Reviewer, source-review only. No suite execution, no mutation run.
Candidate: `2838351450ff1ee4baa620c962a1153450d53311` · Baseline B: `aa1450b82f9ede35aada63efe8a34e01c6e02f72`.

## Scope read (all via `git show` at pinned commit, never worktree)

- `.ufo/waves/round-23/frozen/expected-v2.json` sha256 `458b30d5a6420c1b37874c3364d3ae3b22529d6c3560b5241848a21eec97096f` — matches `SELFTEST_MANIFEST_SHA256` in count-c1.py. ✓
- `.ufo/waves/round-23/frozen/fixture.json` sha256 `a1f5aff8ebb5e5d327522031b74ed91283708907af0fc4a6df24812479bfef4b` — matches `inputs` pin. ✓
- `.ufo/waves/round-23/tools/counter-fixtures.py` sha256 `f2990b35d113b5e44317e7f00e6ca5157baae1efb5ee1a1b8e4995d0ace1a97f` — matches `inputs` pin. ✓
- `.ufo/waves/round-23/tools/count-c1.py` (the DUT), `.ufo/waves/round-22/tools/count-c1.py` sha256 `c925918fb871151f86065aa5b3e9d10334ab845ed67c265ae0977f05e09b1879` — matches `LEGACY_SHA256` pin. ✓
- `corpus/SOURCES.md` at baseline (57 source rows; S051 row is line 57, tier `A`, status `mined`, opened `2026-10-21`, used-by `corpus/knowledge/2026-10-21-r22-flutter-static-boundary.md, corpus/lessons/round-22.md`).

## What `old_source` actually does (observed, source trace)

`counter-fixtures.py` `run()`:

1. Rewrites the synthetic knowledge entry header `source: S058` → `source: S051` (`text.replace('source: S058', 'source: S051')`). The entry otherwise keeps the `positive` shape: `inspect-signal-decoders` verb mention, `ev_555…` hex id, cited `.ufo/waves/round-23/evidence/c1/inspect-signal-decoders.json` path — all committed to the clone.
2. Still inserts a fresh `| S058 |` row before `## Paths` (row text identical to every other case; `duplicate_source_id` not tripped — one S058 row only).
3. Mutates the baseline `| S051 |` row in place: `line.rstrip().rstrip('|') + ', ' + ENTRY + ' |'` appends `corpus/knowledge/control-r23-synthetic.md` to S051's used-by cell.

Expected: `{"exit": 2, "count": null, "finding": "unevaluable"}`.

## Does the expectation hold at candidate? — Yes (traced)

In `count-c1.py` `measure()`, evaluation order is:

1. `LEGACY` blob sha → `legacy_source_untrusted` (helper_tamper).
2. CATALOG blob vs baseline → `catalog_changed` (catalog_changed case).
3. `rev-parse rev:ROOTS[0]` vs baseline → `historical_evidence_changed` (historical_root_injection, inherited_lost).
4. **Sources-row prefix check**: `source_rows(new)[:len(source_rows(old))] != source_rows(old)` → `historical_sources_changed`.
5. Entry scan / eligibility (`sid >= 58`, tier A/B, `mined`, `2026-10-21`, used-by) → binding → count.

The mutated S051 line still matches `^\| S[0-9]+ \|` (row preserved, used-by extended), so it occupies position 51 of the new prefix and differs from the baseline line → step 4 raises `historical_sources_changed` → `{"finding": "unevaluable", "error": "historical_sources_changed"}`, exit 2. Expected `{exit:2, count:null, finding:"unevaluable"}` is met. `count: null` is structurally consistent — the unevaluable output carries no `t1_exercised_count` key, and `out.get()` yields `None`.

## Findings

### F1 (medium) — `old_source` does not exercise the named fault; it measures `historical_sources_changed`

The intended fault (R22-era S051+ source cited where R23 requires S058+) is never evaluated. Step 4 raises before any entry is scanned. Evidence: the mutation had to edit a baseline row to satisfy used-by — S051's baseline used-by names only r22 files — and baseline-row edits are exactly what the prefix guard exists to reject. The case distinguishes **registry-immutability tamper**, not **stale-source citation**. The name is misleading about which guard carries the outcome.

Mutant analysis (source-level): a counter with `int(sid[1:]) >= 58` deleted still exits 2 (guard fires first). A counter with the prefix guard deleted exits 1/count 1 (S051 ineligible on `sid`). So the case kills the guard-removal mutant and cannot kill the recency-predicate mutant.

### F2 (medium) — `sid >= 58` recency predicate is unreachable by any fixture of this design

Any sub-58 id is a baseline-owned id. Making it eligible requires used-by membership, which requires editing that baseline row → `historical_sources_changed`. The alternative (a new duplicate sub-58 row) trips `duplicate_source_id`. Therefore no entry-authored input can isolate the `>= 58` predicate: it is either redundant-with or shadowed-by earlier guards in every constructible case. The suite contains zero coverage of the R23-vs-R22 recency tightening; this is a real coverage gap in the falsifier set ("new source relevance or ownership unsupported" is only partially probed — `wrong_usedby` covers used-by, `missing_source` covers absent citation, nothing covers stale-but-otherwise-valid source rows).

### F3 (low) — Expectation `{exit:2, count:null, finding:unevaluable}` is a weak oracle

`observed` compares only exit/count/finding; `error` is unconstrained. Any `ValueError` raised before output — and even any non-JSON crash exiting 2 — satisfies the expectation. A counter hardwired `sys.exit(2)` passes all six unevaluable cases (`old_source`, `helper_tamper`, `invalid_utf8`, `historical_root_injection`, `inherited_lost`, `catalog_changed`). At minimum the case should assert `error == 'historical_sources_changed'` (and would then need renaming, since that error is not "old source").

## Positive-preserving check

Aside from the two source mutations, the case is identical to `positive`: same eligible S058 row, same committed envelope/entry/path/id. The evidence path is intact, so absent step-4 the entry would be fully evaluated — the mutations are layered, not contradictory. The case is positive-preserving in structure; the defect is that its second mutation (S051 row edit) routes the outcome to a different guard than the name advertises.

## Oracle independence

Confirmed independent: expected values are hand-declared literals in `expected-v2.json` (frozen, sha-pinned, verified above); the runner executes `counter-fixtures.py` as a template (deep-copied `fixture.json` documents, per-case `if name == …` mutations) and compares `observed` against the frozen manifest. No import of or derivation from `count-c1.py` decision logic; the DUT runs as a `sys.executable -I -B` subprocess. The oracle is template-derived, not decision-derived. ✓

## Produced files

- `.ufo/waves/round-23/w2/Fixture06.md` (this report)

## Installs

None.

## Open risks / verification gaps

- All conclusions are source-level traces; no execution (per lane bounds — Run seats own execution). If `run()` behaves other than as read (e.g., `git`/`python` subprocess behavior in the disposable clone), the observed `error` string would confirm or refute F1 immediately; recommend the selftest capture surface `error` in assertions.
- F1/F2 are author-side observations for L1's canonical planner; whether to fix by (a) renaming the case + asserting `error`, or (b) restructuring eligibility so stale-source is distinguishable (e.g., a new unused sub-58… impossible — see F2; the honest fix is accepting that `>= 58` is guarded redundancy, or dropping the used-by requirement for a dedicated stale-source row) is L1's call.
- `old_source` is currently the *only* exerciser of the `historical_sources_changed` guard among the 21 cases, so it is not redundant — the risk is mislabeled coverage, not dead weight.
