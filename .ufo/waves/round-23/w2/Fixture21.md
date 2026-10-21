# Fixture21 — source review of `catalog_changed` (R23-C1 counter controls), candidate 2838351450ff1ee4baa620c962a1153450d53311

Scope: `.ufo/waves/round-23/frozen/expected-v2.json` (case `catalog_changed`), `.ufo/waves/round-23/frozen/fixture.json`, and the exact `catalog_changed` branch in `.ufo/waves/round-23/tools/counter-fixtures.py` — all read via `git show 2838351450ff1ee4baa620c962a1153450d53311:PATH`. The counter under test is `.ufo/waves/round-23/tools/count-c1.py` at the same candidate. No suite execution, no producer replay, no installs.

## Verdict

**The `catalog_changed` case does distinguish its stated fault at candidate source.** The mutation lands on the exact path the counter guards, is committed (not just staged or written to a path the counter never reads), is the only delta versus the positive-preserving companions, and the expected triple matches the counter's documented contract. One non-blocking precision weakness on the expectation and one weak-mutation note; no wrong expectation found.

## Findings

### F1 (pass, observed) — mutation hits the guarded path; guard fires at candidate source
- Fixture branch, candidate `.ufo/waves/round-23/tools/counter-fixtures.py:97-99`:
  ```python
  if name == 'catalog_changed':
      p = repo/'.ufo/waves/round-20/verify/round20/verb-coverage.json'
      p.write_text(p.read_text()+'\n')
  ```
- Guard, candidate `.ufo/waves/round-23/tools/count-c1.py:64-65` with `CATALOG` defined at line 27 as the same path:
  ```python
  if git(root, 'show', rev+':'+CATALOG) != git(root, 'show', BASELINE+':'+CATALOG):
      raise ValueError('catalog_changed')
  ```
- Observed: the target file exists at baseline B=aa1450b8 (`git cat-file -e` rc=0) and ends with a single `\n` (`…pretty.json"]]}}}\n`, hexdump tail), so `+'\n'` is a real byte delta, not a no-op. The counter reads the blob at the committed rev (`rev+':'+CATALOG`), and the fixture commits the mutation (add block at counter-fixtures.py:100-102, commit at :103, rev captured at :104) — so the guard sees the mutated committed tree, not the worktree only.
- Observed: candidate and live bytes of both the branch and the guard are identical (live `counter-fixtures.py:103-105`, live `count-c1.py:65`); the live-vs-candidate diffs touch other regions only (`symlink_evidence`/`inherited_entry_*`, knowledge-preservation guard), so this finding transfers to the live tree.

### F2 (pass, observed) — positive-preserving behavior: mutation rides on an otherwise-valid positive commit, and per-case isolation holds
- The `catalog_changed` run performs the full positive pipeline first: baseline checkout (`:32-33`), per-case `git reset --hard base` + `git clean -fd` (`:35-36`), one synthetic envelope (`inspect-signal-decoders`), the ENTRY knowledge file with a compliant S058 row whose used-by is the real ENTRY, `git add` of all control paths (`:100-102`), and a successful commit (`:103`; any failure raises `RuntimeError` at `:26-27`). The only delta against the `positive` companion is the trailing newline.
- Counter path ordering (candidate `count-c1.py`): legacy sha (`:33-34`) → catalog compare (`:64-65`) → old-root (`:66-68`) → historical source rows (`:69-73`). The catalog guard is the second check, so `catalog_changed` fails closed before the historical basemeasure (`:77-86`) — the case cannot be masked by downstream behavior. For the positive companions the same preflight passes, so the catalog check is the sole discriminator.
- Non-vacuity, observed statically: a catalog-equal tree is demonstrably evaluable (the suite's own `positive` case expects `exit 1, count 2, finding c1_incomplete`, and `all_six` expects `exit 0, count 6, finding c1_complete` — expected-v2.json), so "guard removed / weakened to parsed-JSON compare" would leave the suite passing this case; the present guard bytes make it fail the expected triple instead.
- Per-case isolation: `reset --hard` + `clean -fd` at `:35-36` restore the clone before each case; the append cannot leak into other cases. Inferred: `git add` never silently no-ops (index refresh only); a lost mutation would produce a commit equal to base and observed `exit 1 / count 2 / c1_incomplete` ≠ expected `exit 2`, failing loudly.

### F3 (pass, observed) — expected code/count/finding match the counter contract; no wrong expectation
- expected-v2.json `catalog_changed`: `{"exit": 2, "count": null, "finding": "unevaluable"}`.
- Observed mechanics: `measure()` raises `ValueError('catalog_changed')` before any result object exists; `main()`'s catch (`count-c1.py:167-168`) prints `{'finding':'unevaluable','error':...}` and returns exit 2, per the documented contract in the module docstring (`:9`: `0=clean6/6;1=failed/incomplete;2=could-not-evaluate`). The harness reads only `exit`, `out.get('t1_exercised_count')`, `out.get('finding')` (`counter-fixtures.py:108-111`); the absent `t1_exercised_count` key yields `count: null` as expected. `passed = all(observed.get(k)==v)` at `:112` — no extra keys asserted, so the triple is exactly the contract.

### F4 (pass, observed) — expectation is hand-authored to the contract, not a decision-derived oracle; the case is a genuine new control
- Observed: `expected-v1.json` has 14 cases, `expected-v2.json` 21; `catalog_changed` is v2-only (v2-only set: `absolute_citation, catalog_changed, historical_root_injection, inherited_lost, meta_array, meta_false, sibling_refusal`; v1-only: none). No R22 predecessor contains a catalog-mutation case (R22 suite only pins `.ufo/waves/round-20/verify/round20/verb-coverage.json` as a DEPS sha — `round-22/frozen/counter-fixtures-v1.py:23-25`).
- The v2 suite is candidate-introduced: none of `tools/count-c1.py`, `tools/counter-fixtures.py`, `frozen/fixture.json`, `frozen/expected-v2.json` exists at baseline B (`git cat-file -e` rc=128 each); the wave commits B..2838351 are a3c92eb → 2b40aec → 6615aea → 2838351.
- Inputs are pinned, not free: `count-c1.py:139-144` verifies sha256 of expected-v2.json (`458b30d5…`) and of both manifest inputs before loading the fixture module; observed candidate and live blob hashes equal the pins exactly (`f2990b35…` fixtures, `a1f5aff8…` fixture.json). Envelopes are synthetic (`fixture.json` `data.normalized_result.control = "synthetic, never a producer observation"`), distinct evidence_ids per verb — independent of any producer decision output.
- Inferred (non-blocking): the expected triple is the uniform unevaluable template shared by `old_source`/`helper_tamper`/`invalid_utf8`/`historical_root_injection`/`inherited_lost`, i.e. authored from the counter's documented exit contract, not captured from a run of the code under test.

### F5 (weak-mutation note, non-blocking) — byte-level mutation and non-specific unevaluable expectation
- The guard is byte-equality, so the semantic-mutation depth is unreachable by construction (any semantic change is also a byte change); the trailing-newline mutation therefore distinguishes exactly {guard absent, guard semantic-only} and cannot probe a semantic-vs-byte guard distinction. This matches the fault's stated shape ("catalog frozen/unchanged") and is adequate; a semantic mutation would not add discrimination for this guard.
- The expectation does not pin `error == 'catalog_changed'`; any unevaluable exit (e.g. a `historical_*` guard firing spuriously) would also pass this case. In the constructed commit, the catalog guard is the only reachable unevaluable cause (it fires before the historical checks, and the positive companions prove the other preflight stages pass), so identity is pinned by construction. Observed at candidate `count-c1.py:167-168` + harness `:111-112`.

### F6 (scope-integrity note, observed) — the counter's CATALOG guard is report-integrity, not count-path integrity
- In candidate `count-c1.py`, the count numerator uses `r22.T1` (frozen six verbs), not the catalog; the catalog supplies only informational fields (`catalog_mentioned_count`, `catalog_total`, `catalog_zero_count`, `:95-97,130-133`). A silent catalog rewrite could not forge the 0-6 count; it could misreport the mention metrics that L1's claim narrative leans on. The `catalog_changed` case therefore guards an honest-reporting invariant, which is consistent with its `unevaluable` (fail-closed) expectation rather than a count change.

## Produced files and hashes
- `.ufo/waves/round-23/w2/Fixture21.md` — sha256 recorded by L1 at intake (single write; see report trailer below).

## Installs
None. No pacman/uv/cargo/npm activity; no new tools required for this source review.

## Open risks
- **Live-tree divergence (observed, out of assigned scope):** the worktree's `count-c1.py`, `counter-fixtures.py` differ from candidate (added `historical_knowledge_changed`, symlink-evidence handling, `inherited_entry_lost/changed` cases; untracked `frozen/counter-fixtures-v2.py` present). The `catalog_changed` branch/guard bytes are identical live vs candidate, so this case's verdict transfers, but the *suite* verdict belongs to the v2/live review, not this one.
- **No execution:** all dynamics above (add/commit/guard firing, `out.get` null behavior) are grounded in candidate bytes and baseline object checks; runtime confirmation belongs to the designated Run* seat. An unrun check is not passed — this report asserts only that the case is *capable* of distinguishing the fault at candidate source.
- **Harness safety dependency (inferred):** `run()` performs no `GIT_*` scrub itself; safety relies on being exec-loaded from `count-c1.py`'s `main()` (`count-c1.py:160-163` scrubs before selftest). Standalone invocation of `counter-fixtures.py` is not a supported path.
