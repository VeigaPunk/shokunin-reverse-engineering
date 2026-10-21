# Fixture13 — `helper_tamper` source review (R23 candidate)

**Candidate:** `2838351450ff1ee4baa620c962a1153450d53311` · **Baseline:** `aa1450b82f9ede35aada63efe8a34e01c6e02f72`
**Scope:** `frozen/expected-v2.json` row `helper_tamper`; `frozen/fixture.json`; the `helper_tamper` branch of `tools/counter-fixtures.py`. Candidate bytes only (`git show`, `git rev-parse`, `git ls-tree`, `git log`, `git diff --stat`, `sha256sum`). The counter, selftest, fixture harness, and mutants were **not executed**.
**Labels:** **observed** = read from candidate bytes or a recorded artifact; **[INFERENCE]** = outcome derived by reading code, not run; **unknown** = not determinable from these bytes.
**Stated fault (my reading):** a committed change to the frozen round-22 legacy helper (`.ufo/waves/round-22/tools/count-c1.py`) that the R23 counter reuses via `r22.measure` must be refused, not counted. Grounds: row name, R22 committed-helper analog, and count-c1.py:2-3 ("original R22 binding policy is reused unchanged").

## Verdict

| Question | Answer |
|---|---|
| Expected code/count/finding correct? | **Yes.** `{exit 2, count null, finding unevaluable}` (expected-v2.json:68). Fail-closed on an untrusted legacy helper. The literal is identical in `expected.json`, `expected-v1.json`, and `expected-v2.json` (observed), so it was not retuned. Introduced at `2b40aec`, untouched by candidate `2838351` (blob-identical to parent `6615aea`, observed). Matches R22's committed-helper expectation (round-22 counter-fixtures.py:152-153, computed as exit 2 / count None). |
| Positive-preserving? | **Yes.** The row differs from `positive` only at counter-fixtures.py:88-90, a committed 19-byte comment append to `.ufo/waves/round-22/tools/count-c1.py`. The default selection (:38), envelopes, and text (:45-70) are shared. |
| Independent template? | **Yes.** Literal row, digest-pinned: `SELFTEST_MANIFEST_SHA256` at count-c1.py:25, checked at :138-140; inputs pinned at expected-v2.json:3-6. The harness imports only stdlib (counter-fixtures.py:7-13) and runs the counter as a subprocess (:105-106). It never imports the counter or legacy code. |
| Distinguishes the stated fault? | **Yes, for committed legacy tamper.** The only discriminator is the committed-blob SHA-256 pin at count-c1.py:61-63, which runs before the legacy module is loaded (:80). Removing it would make the row produce exit 1 / count 2 / c1_incomplete **[INFERENCE]**. |
| Distinguishes the wider helper-tamper family? | **No.** Uncommitted/worktree reads, execution-before-refusal, weaker-than-byte pins, and refusal reason all survive. See F1–F4. |

## Findings

### F1 — MEDIUM: no row detects a worktree (uncommitted) read of the legacy helper
- **observed:** every row starts with `reset --hard` and `clean -fd` (counter-fixtures.py:35-36). Every write is committed: writes at :69, :79, :87, :90, :92, :94, :96, :98-99; `git add` at :100-102; commit at :103. So at count time, worktree == HEAD in all 21 rows.
- **observed:** the counter reads the legacy from the blob: count-c1.py:61 `git show rev:LEGACY`.
- **observed:** R22 had an uncommitted row. round-22 counter-fixtures.py:247-248 overwrites the helper's working copy with `raise RuntimeError("uncommitted_helper_executed")`, expects exit 0 / count 6 (:152-153), and restores it at :263-264. R23 has no uncommitted row (21 rows, all committed).
- **[INFERENCE]:** a mutant that reads the legacy from the worktree (for hashing or loading) passes all 21 rows.
- **observed:** round-20/21 helper blob reads come from R22 `revision_helpers` (round-22 count-c1.py:50-51, "never mutable worktree code"), which R23 calls at count-c1.py:84. Nothing in R23 fails if that regresses; R22's `helper_drift` was the only test.
- **Fix:** restore an uncommitted-drift row. After commit, overwrite the clone's legacy worktree copy with a raising sentinel. Expect the positive result `{exit 1, count 2, c1_incomplete}`. Needs new frozen digests (L1).

### F2 — MEDIUM: the tamper is a no-op, so execute-before-refuse survives
- **observed:** the appended text is `'\n# changed control\n'` (counter-fixtures.py:90), which runs nothing at import.
- **[INFERENCE]:** a counter that `load()`s the legacy (count-c1.py:80) before the pin (:62-63) still returns exit 2 for this row. The row cannot detect executing an untrusted helper before refusal. R22 used a raising sentinel for exactly this (round-22 counter-fixtures.py:248).
- **Fix:** a committed row whose appended text raises at import, e.g. `raise RuntimeError("tampered_legacy_executed")`. A correct counter refuses before `load`, so exit 2 and the expectation are unchanged. An exec-first mutant raises and fails the row.

### F3 — LOW-MEDIUM: pin strength is exercised only by a size change
- **observed:** the append changes the file length (19 bytes).
- **[INFERENCE]:** a length-only check (`len(legacy) != N`) refuses this row and so passes it. No other row touches the legacy file, so it survives the whole suite.
- **Fix:** a committed, same-length, behavior-preserving byte substitution inside an existing legacy comment or docstring, expecting exit 2. Only a byte-exact pin refuses it.

### F4 — LOW: refusal reason is not asserted
- **observed:** `observed` = {exit, count, finding} (counter-fixtures.py:111); `passed` compares only the expected keys (:112). Any exit 2 / `unevaluable` passes.
- **observed (recorded artifact):** the prior run's helper_tamper stdout is `{"error": "legacy_source_untrusted", "finding": "unevaluable"}`, so the pin was the refusal in that run. The row does not enforce it.
- **[INFERENCE]:** a different `unevaluable` refusal passes this row.
- **Note:** the lane worktree's counter-fixtures.py already adds `error` to `observed` (worktree :122-123). That is drift, not candidate. Enforcing it needs coordinated edits to counter-fixtures.py and expected-v2.json plus new digests (L1).

## Mutation coverage ([INFERENCE] unless marked)

| Mutant | helper_tamper | Other rows | Basis |
|---|---|---|---|
| Pin removed | killed | — | exit 1 / count 2 vs expected exit 2 |
| Pin constant set to tampered hash | killed | — | accepts → exit 1 |
| Pin only in `--selftest` wrapper | killed | — | row runs measure via `--rev` (counter-fixtures.py:105-106; count-c1.py:162-165) |
| Hash baseline blob instead of rev | killed | — | count-c1.py:61 would read baseline and accept |
| Comment-stripped or AST hash | killed | — | comment-only change is invisible to it |
| Length-only pin | **survives** | survives | F3 |
| Worktree read (hash or load) | **survives** | survives | F1 |
| Execute before pin | **survives** | survives | F2 |
| Different refusal, same exit/finding | **survives** | survives | F4 |

## Strengths (observed)
- A behavior-preserving (comment-only) tamper means only a byte-exact committed-blob pin can refuse it. That is why the row kills the normalization, baseline-blob, and selftest-only mutants above.
- The pin runs before any legacy load (count-c1.py:61-63 before :80). Fail-closed order holds.
- The finding must equal `unevaluable`, so argparse exit 2 (`parse_args` at count-c1.py:158, outside `try`) cannot spoof the row (counter-fixtures.py:111-112).

## W1 re-evaluation (against candidate)
- **W1 CriticSeparation.md:15** says `tools/counter-fixtures.py:45,59` "only ever writes under the round-23 prefix." **Stale at candidate.** Writes now go outside that prefix: :89-90 (round-22 legacy, this row), :94 (round-22 evidence), :96 (unlink), :98-99 (round-20 catalog). All writes stay in the disposable clone (:29-31).
- **W1 CriticSeparation.md:86** (legacy sha identical at B, HEAD, worktree): **holds.** Candidate rev blob = `c925918f…1879` (observed); baseline = same (observed); pin at count-c1.py:23 (observed); worktree = same (observed).
- No W1 item covers uncommitted drift, pin strength, execution-before-refusal, or reason assertion. F1–F4 are new relative to W1.
- Out of item, observed: W1 F2's `inherited_lost_replaced` variant (W1 line 24) is absent. Candidate has only `inherited_lost` (:95-96, unlink with no replacement).

## Moving-worktree drift (not candidate; for L1)
- Worktree `tools/counter-fixtures.py` sha256 `687c4074…` ≠ candidate `f2990b35…`, the digest pinned at expected-v2.json:4. **[INFERENCE]** a selftest run from the worktree would raise `snapshot_tampered` at count-c1.py:142-144.
- Worktree counter-fixtures.py differs from candidate by 22 diff lines. It adds rows `symlink_evidence`, `symlink_knowledge`, `inherited_entry_lost`, `inherited_entry_changed`. The `helper_tamper` text is unchanged (worktree :94-96).
- Worktree `tools/count-c1.py` sha256 `3949fa95…` ≠ candidate `f4b8d16a…` (37 diff lines). The `LEGACY_SHA256` line is unchanged (worktree :23).

## Recorded evidence (prior run, not produced here)
- `.ufo/waves/round-23/verify/initial/selftest.json` at candidate (blob `28a5f96d…`, sha256 `d88207f1…`): exit 0, passed true, `source_rev` `6615aeae…`, finding `selftest_clean` 21/21. Row helper_tamper observed `{exit 2, count null, finding unevaluable}`.
- Its inputs are blob-identical to the candidate (`git rev-parse` parent vs candidate): count-c1.py `0f966a50…`, counter-fixtures.py `55356faa…`, expected-v2.json `7e4199d7…`, fixture.json `92c2f04a…`. So the recorded pass applies to these inputs. It is not a result from this seat and does not exercise F1–F4.

## Produced files and hashes
- Candidate sha256 (from `git show` bytes): count-c1.py `f4b8d16a…`; counter-fixtures.py `f2990b35…` (pinned); expected-v2.json `458b30d5…` (pinned); fixture.json `a1f5aff8…` (pinned); round-22 legacy count-c1.py `c925918f…` (pinned, also at baseline).
- This report: `.ufo/waves/round-23/w2/Fixture13.md`.
- Scratch: `.ufo/waves/round-23/runtime/Fixture13/` created and emptied. My transient `/tmp/r22-*` and `/tmp/r23-*` read copies were removed. Other `/tmp` entries belong to sibling seats and were not touched.

## Installs or none
None. No pacman, uv, cargo, or npm installs. No config edits.

## Open risks
- All mutant outcomes are [INFERENCE]. The contract forbids executing the suite; none were run.
- The recorded selftest pass is a prior run at `6615aea`. It is not evidence for F1–F4.
- Any new row changes frozen digests (expected-v2 inputs; `SELFTEST_MANIFEST_SHA256` at count-c1.py:25). L1 must re-pin. I did not propose digest values.
- The live worktree no longer matches the candidate. A selftest run from it is not the reviewed artifact.
