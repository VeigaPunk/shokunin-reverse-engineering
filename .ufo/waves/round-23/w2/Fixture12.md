# Fixture12 — R23-C1 `duplicate_member` source review

Candidate `2838351450ff1ee4baa620c962a1153450d53311` (parent `6615aea`); baseline `aa1450b82f9ede35aada63efe8a34e01c6e02f72`.
Source review only. The suite and counter were **not executed** by me. Candidate bytes were read with `git show`; copies sit in the ignored `runtime/KaidokuR23.Fixture12/`.

Labels: **[O]** observed by me (bytes, hashes, git facts). **[R]** recorded in a committed artifact, not re-run by me. **[I]** inferred by tracing source, not executed.

## Verdict

- **Expected value matches the candidate source path.** `duplicate_member = {exit 1, count 1, c1_incomplete}` [I]. The committed run at `source_rev` 6615aea reports `selftest_clean` 21/21, with `duplicate_member` observed as `{exit 1, count 1, c1_incomplete}` [R]. The `count-c1.py` blob at 6615aea is byte-identical to the candidate's (sha256 `f4b8d16a…`) [O].
- **Positive-preserving [O].** The case differs from `positive` by one injected member in one file (`counter-fixtures.py:67-68`). `positive` pins count 2 (`expected-v2.json:8-12`).
- **Catches the realistic fault [I].** A last-wins resolution of `ok` would count the refused envelope: count 2, FAIL. This is the stated falsifier "refusal counted" (`claims.json:31`).
- **Weak mutation [I].** The case exercises one ordering of one key. A first-wins resolution, a rejection narrowed to `ok`, or tolerance of equal-value duplicates all pass the full 21-case selftest. The first two re-admit the stated falsifier.
- **Expectation defect [I, medium-high].** `exit 1` for a representation-level defect contradicts the counter's own decode-failure convention (exit 2) and the sibling pin `invalid_utf8` (exit 2). It needs an explicit rule from L1. Under the exit-2 reading the candidate FAILS this case.
- **Oracle independence.** Mechanism is independent [O]. The per-case values have no independent prior pin [O], so their provenance is not established.

## Findings

### F1 — How the duplicate reaches the verdict [I, traced]
1. Builder. `counter-fixtures.py:38` sets `selected = ['inspect-signal-decoders']` by default. `:66` is `raw = json.dumps(envelope)`. `:67-68` apply `raw.replace('"ok": true', '"ok": false, "ok": true')` only when `name == 'duplicate_member'`. `:69` writes `.ufo/waves/round-23/evidence/c1/inspect-signal-decoders.json`.
   - The envelope has exactly one `"ok"` (`fixture.json:57`; six `"ok"` keys in the file, one per envelope), so the replacement is unique.
   - The result is still syntactically valid JSON. The rejection is therefore semantic (duplicate-member policy), not a parse error.
2. Counter. `count-c1.py:118` reads the blob. `:123` runs `if eid in blob and bind_new(...) == 0`.
3. `count-c1.py:45` runs `pending = [r21.decode(text)]`. `r21:33-36` is `json.loads(..., object_pairs_hook=pairs)`. `r21:24-28` raises `ValueError('duplicate_member: ok')` on the second `ok`.
4. `count-c1.py:55-56` catches the error and returns 2. The append at `:124` never runs. The historical identify witness keeps the count at 1. `:129` yields `c1_incomplete`, and `main` returns 1.
5. Second strict layer: the legacy `bind_cli` (`.ufo/waves/round-22/tools/count-c1.py` at candidate) decodes strictly at `:72` and returns 2 at `:97-98`.

Result: the candidate source yields the pinned `{exit 1, count 1, c1_incomplete}` [I], corroborated by the recorded run [R].

### F2 — Mutation survival table [I; no mutant was run]

| # | Mutant | Pins touched | `duplicate_member` outcome | Verdict |
|---|---|---|---|---|
| M1 | last-wins in `r21.pairs` (drop raise at `r21:27-28`) | yes: legacy `HELPER_SHA256` (legacy `:38`) and `LEGACY_SHA256` (`count-c1.py:23`) | `ok=true` → walk passes (`count-c1.py:51`) → legacy `:72` → count 2 | FAIL, caught |
| M2 | first-wins in `r21.pairs` (keep first, skip later duplicates) | same as M1 | `ok=false` → refused at `count-c1.py:51-52` → count 1 | PASS, **survives**; re-admits "refusal counted" for `{"ok": true, "ok": false}`, which no fixture generates |
| M3 | rejection narrowed to key `ok` (other duplicates last-wins) | same as M1 | only duplicate in the fixture is `ok` → rejected → count 1 | PASS, **survives**; duplicate `errors`/`status`/`evidence_id` accepted, so nested refusal can be hidden |
| M4 | tolerate equal-value duplicates, reject only conflicting ones | same as M1 | fixture values conflict → rejected → count 1 | PASS, **survives** (low; policy-level) |
| M5 | fail-open: `count-c1.py:56` `return 2` → `return 0` | none | count 2 | FAIL, caught |
| M6 | `count-c1.py:55-56` re-raise instead of return 2 | none | `main` `:167-168` → exit 2 | FAIL, caught |
| M7 | `count-c1.py:45` `json.loads` (last-wins in walk only) | none | legacy `:72` still strict → 2 → count 1 | PASS; outcome-equivalent, not a defect |
| M8 | `count-c1.py:56` `return 2` → `return 1` | none | caller tests only `== 0` (`:123`) | outcome-equivalent |

Note on M2–M4: r21 is hash-pinned, so a change there must update the legacy `HELPER_SHA256` and `LEGACY_SHA256`. The selftest pins only `expected-v2.json` and the two inputs, not `count-c1.py` itself, so the coordinated update is feasible and the selftest stays clean.

### F3 — Expectation classification [O for pins; I for convention]
- `expected-v2.json:63-67` pins `duplicate_member` as `exit 1, count 1, c1_incomplete`. `expected-v2.json:73-77` pins `invalid_utf8` as `exit 2, count null, unevaluable`.
- The counter's convention for decode failures is 2 (`count-c1.py:55-56`; legacy `:97-98`; `r21:101` `evidence_unevaluable`). Its refusal convention is 1 (`count-c1.py:51-52`; legacy `:76-77`).
- For the duplicate, `r21:28` raises before any `ok` value is read. The binder's own classification is therefore 2 ("unevaluable"), not 1.
- `count-c1.py:123-124` discards the binder's code and tests only `== 0`. The `exit 1` pin records that silent drop, not the classification.
- `invalid_utf8` fails at `count-c1.py:118` (`.decode('utf-8')` outside any binder try), which reaches `main` `:167-168` and exits 2. The same artifact class therefore exits 2 when the defect is byte-level and 1 when it is representation-level. No documented rule explains the split.
- Assessment: the `exit 1` pin is at least unjustified, and the counter's own convention plus the stated contract (`count-c1.py:9`, "2=could-not-evaluate") better support 2. There is no false-pass hazard (a silent drop only lowers the count). This is a classification defect, not a coverage inflation.

### F4 — Independence and provenance
- **Mechanism independent [O].** The builder imports only stdlib (`counter-fixtures.py:7-13`). It does not import r21, r22, or any decision code. The duplicate is injected as text (`:67-68`), independent of the decoder.
- **Oracle hash-bound [O].** `SELFTEST_MANIFEST_SHA256 = 458b30d5…` (`count-c1.py:25`, enforced at `:139`) matches `expected-v2.json`. The `inputs` pins match (`counter-fixtures.py` `f2990b35…`, `fixture.json` `a1f5aff8…`).
- **History [O].** `git log` on `frozen/` and `tools/` up to candidate shows one commit, `2b40aec`. `git diff --stat 2b40aec 2838351 -- …/tools/ …/frozen/` is empty. The candidate commit touches 18 files, none under `tools/` or `frozen/`.
- **No prior per-case pin [O].** The R22 `expected-v2.json` (schema `kaidoku-r22-independent-controls-v2`) carries only `expected_finding: counter_controls_clean`, with no per-case values. The round-23 `counter-fixtures-v1.py:61-62` has the identical duplicate injection, but no v1 manifest exists in the candidate tree.
- **Conclusion [I].** The `duplicate_member` values were introduced in the same commit as the counter they test. Their independence from observed output cannot be shown from history. The recorded run agrees with them, which is consistent with either an independently specified oracle or copied output.

### F5 — Adjacent gaps (low)
- Truncated JSON or NaN envelopes take the same silent path (`count-c1.py:55-56` → `:123-124`) with no control. The F3 decision applies to them too.
- No control for equal-value duplicates (M4) or nested duplicates (M3).
- Self-checking: if the injection silently failed, the case would become `positive` and report count 2 against the pinned 1, so FAIL. I found no silent-pass path in the builder branch.

## Recommended controls (route to L1; not applied, read-only wave)
- **C1** `duplicate_member_reversed`: `"ok": true, "ok": false` → `{exit 1, count 1, c1_incomplete}`. Kills M2. Candidate passes.
- **C2** nested refusal-first duplicate, e.g. `normalized_result` with `"errors": ["execution_failure"], "errors": []` → `{exit 1, count 1, c1_incomplete}`. Kills M3 (nested variant) and nested last-wins.
- **C3** duplicate `evidence_id` with a differing value → `{exit 1, count 1, c1_incomplete}`. Kills M3 (identity variant).
- **C4** (policy-dependent) equal-value duplicate; its exit code follows the F3 decision.
- **D1** Settle the F3 exit-code rule and add a per-case rationale field. Any new case changes `expected-v2.json`, so `SELFTEST_MANIFEST_SHA256` (`count-c1.py:25`) must be re-pinned. That is a counter edit, outside this read-only wave.

## Produced files and hashes
- This report: `.ufo/waves/round-23/w2/Fixture12.md` (sha256 recorded in the final message).
- Ignored runtime copies in `.ufo/waves/round-23/runtime/KaidokuR23.Fixture12/` (sha256 from `sha256sum`):
  - `…round-22_tools_count-c1.py` `c925918f…` (equals `LEGACY_SHA256`)
  - `…round-22_frozen_expected-v2.json` `1abdd9df…` (equals R22 `SELFTEST_MANIFEST_SHA256`)
  - `…round-22_tools_counter-fixtures.py` `f90be315…`
  - `…round-23_frozen_counter-fixtures-v1.py` `96e65034…`
  - `…round-23_frozen_expected-v2.json` `458b30d5…` (equals `SELFTEST_MANIFEST_SHA256`)
  - `…round-23_frozen_fixture.json` `a1f5aff8…` (equals pinned input)
  - `…round-23_tools_count-c1.py` `f4b8d16a…`
  - `…round-23_tools_counter-fixtures.py` `f2990b35…` (equals pinned input)
  - `…round-20_tools_verb-coverage.py` `cfbf1880…` (equals `HELPER_SHA256`)
  - `…round-21_tools_verb-coverage.py` `61536938…` (equals `HELPER_SHA256`)
  - `…round-23_verify_initial_selftest.json` `d88207f1…` (recorded run, `source_rev` 6615aea)
- `claims.json` candidate blob sha256 `249811d9…`, identical to the worktree copy I read first.

## Installs or none
None. No package or tool was installed or updated. Only `git`, `sha256sum`, `diff`, and read-only `python3` JSON parsing of committed text were used. The counter and fixture builder were not executed.

## Commands run (read-only)
- `git show 2838351…:<path>` for each blob listed above: exit 0.
- `sha256sum`: first glob missed dot-prefixed names (exit 1); re-run with explicit names (exit 0).
- `diff` builder v1 vs v2: exit 1. Differences are extra cases only; the duplicate branch is identical.
- `diff` R22 vs R23 `expected-v2.json`: exit 1. Schemas differ; R22 has no per-case duplicate pin.
- `git merge-base --is-ancestor 2b40aec 2838351`: yes. `git log -- frozen/ tools/`: one commit. `git diff --stat 2b40aec 2838351 -- …`: empty, exit 0.
- `python3 -c` JSON parse of committed `claims.json` and `selftest.json`: exit 0.

## Open risks
- **Coordinated pin edits.** M2–M4 survive only with coordinated pin updates. `count-c1.py` is unpinned, so such an edit passes the selftest. Any change to r21 should trigger a re-check of both pins.
- **Recorded, not reproduced.** The `selftest.json` run is the author's, and I did not reproduce it. Its snapshot path is not in the repo. The equivalence I rely on rests on the `count-c1.py` blob match at 6615aea and the empty `frozen/`+`tools/` diff since `2b40aec`.
- **F3 unresolved.** The candidate's result on this case depends on L1's exit-code decision (F3). Under exit 2 the case fails at candidate.
- **Out of item, not checked.** The candidate subject line says "retain measured four-of-six coverage", while `claims.json` pins baseline 1/6 with target at least 2. Flagged for L1; I did not investigate it.

Report: .ufo/waves/round-23/w2/Fixture12.md
