# Fixture15: source review of R23 frozen case `meta_false`

- Candidate: `2838351450ff1ee4baa620c962a1153450d53311`; baseline `aa1450b82f9ede35aada63efe8a34e01c6e02f72`.
- Scope: `frozen/expected-v2.json` `meta_false` (:78-82); `frozen/fixture.json` `inspect-signal-decoders` block (:56-68); `tools/counter-fixtures.py` selection (:38), loop (:48), `meta_false` branch (:58-59).
- Method: `git show <candidate>:PATH`, `git ls-tree`, `sha256sum`, `grep`/`sed`/`ls` only. Nothing was executed: no counter, no `--selftest`, no fixture run, no clone, no git write.
- Labels: **OBSERVED** = bytes or command output. **INFERRED** = source trace, not executed. **UNKNOWN** = not determinable from the frozen artifacts.

## Verdict

- `meta_false` distinguishes the stated fault (N1: `meta.ok:false` accepted) at candidate source. The count field separates the candidate (count 1) from a binder that ignores `meta.ok` (count 2). [INFERRED]
- Expectation `{exit 1, count 1, finding c1_incomplete}` is correct under the counter's cumulative semantics. No wrong expectation found for this case. [INFERRED]
- It is a negative control. Its discriminating power holds only when read with `positive` (count 2) in the same selftest run. [INFERRED]
- Weak points: (a) only literal `False` is tested, so narrowing `is not True` to `is False` survives the suite (F4); (b) binder refusal and unevaluable are indistinguishable at suite level (F5); (c) the synthetic `meta.ok` shape is not in the one retained real envelope (F7).

## Findings

### F1. Distinguishes N1 at candidate [INFERRED, mutant analysis]

Candidate path for `meta_false` (top-level `ok` stays true; only `meta.ok` is set false):
- Measure reaches the `inspect-signal-decoders` citation (`count-c1.py:121-123`).
- `bind_new` walks every dict. The envelope passes. The `meta` dict fails `'ok' in node and node['ok'] is not True` (`False is not True`), so it returns 1 (`count-c1.py:51-52`).
- `== 0` is false at `:123`, so there is no witness. Only the historical witness remains: count 1, exit 1, `c1_incomplete`. Matches `expected-v2.json:78-82`.

Mutant M-legacy (walk removed; `bind_new` returns `r22.bind_cli` directly):
- Legacy `bind_cli` checks `meta.get("command") != verb or r21.refused(meta)` (`.ufo/waves/round-22/tools/count-c1.py:78-79`).
- `r21.refused` (`.ufo/waves/round-21/tools/verb-coverage.py`, `def` at `:39`) reads only `error/errors`, `code/status/completion_status`, `exit_code`, and `raw_result/normalized_result`. It never reads `ok`.
- The legacy record walk covers only `data`. Result: 0, count 2, exit 1, `c1_incomplete`.
- Only `count` differs (1 vs 2), so the selftest reports `selftest_failed`. **Detected.**

Mutant M-skip-meta (walk visits all dicts except key `meta`): same result. **Detected.**

Implication: `count` is the only separating field. Exit and finding are identical for counts 1 and 2 (both are not 6). Relaxing `count` to null would make this case vacuous.

### F2. Expectation check [INFERRED + OBSERVED]

- Count 1 is the historical `identify-flutter-build` witness plus zero refused new witnesses. The counter enforces the historical set at `count-c1.py:82`. The value is derivable from the baseline and the refusal rule, not copied from candidate output.
- W1 `.ufo/waves/round-23/w1/CounterRefusals.md:218` (N1) says `expect count 0, exit 1`. That per-case value is stale, because the counter always includes the historical witness. Do not reinstate 0.
- Whether the frozen integer was copied from a run cannot be audited from the bytes alone. **UNKNOWN.** The independent derivation above matches it.

### F3. Positive preservation [INFERRED; gates OBSERVED]

- `positive` uses the same template with no mutation. The walk sees only top-level `"ok": true` and no refusal keys (`fixture.json:57, 59-60, 62-67`). Legacy `bind_cli` then calls `r21.bind`, which returns `evidence_bound` (0). Count 2, exit 1, `c1_incomplete`. Matches `expected-v2.json` `positive`.
- Gates `positive` depends on, all OBSERVED to hold at candidate:
  - legacy counter sha `c925918f…` (`count-c1.py:23`);
  - helper pins r20 `cfbf1880…` and r21 `61536938…`, identical at base and candidate;
  - manifest sha `458b30d5…` (`count-c1.py:25`);
  - fixture sha `a1f5aff8…`, counter-fixtures sha `f2990b35…`;
  - base `corpus/SOURCES.md` has `## Paths` at line 65, no S058 row, and no `| S` rows after line 65. The synthetic S058 row therefore registers with no duplicate and no prefix change.
- So the count-1 expectation is non-vacuous at candidate. [INFERRED]

### F4. Weak mutation: `is False` narrowing survives [OBSERVED + INFERRED]

- Mutant: `if ('ok' in node and node['ok'] is False) or r21.refused(node):` at `count-c1.py:51`.
- It still refuses literal `False`, so `meta_false` and `meta_array` both pass. It accepts `meta.ok` = `0`, `null`, or `""`.
- OBSERVED: every `ok` mutation in `counter-fixtures.py` is boolean or list: `:51` (top-level False), `:59` (meta False), `:61` (`raw_result=[{'ok': False}]`), `:68` (duplicate key). All `ok` values in `fixture.json` are top-level `true` (lines 5, 18, 31, 44, 57, 70). Nothing sets 0, null, or "".
- W1 `CounterRefusals.md:108` lists `meta.ok:0` as ignored by legacy. W1 `:199` says "meta.ok (any value)". W1 `:218` prescribes "reject any meta containing ok not literally True". The candidate implements that, and no case pins it. All 21 cases pass under the mutant.
- Recommendation for the owner: add a paired control with `meta.ok: 0` (and/or null) expecting `{exit 1, count 1, c1_incomplete}`. Not implemented here (source review only).

### F5. Weak mutation: refusal vs unevaluable indistinguishable [INFERRED]

- `bind_new` returns 1 for refusal (`count-c1.py:52`) and 2 for decode or recursion errors (`:55`). `measure` tests only `== 0` (`:123`) and has no else branch. Both codes are non-witness.
- Mutant `return 1` to `return 2` at `:52` leaves exit, count, and finding unchanged. It survives.
- Related, not a `meta_false` defect: legacy `measure` records binder-2 files as `unevaluable` (`.ufo/waves/round-22/tools/count-c1.py:161-163`). R23 drops them silently. `duplicate_member` (expected exit 1) encodes this silent path. The owner should decide whether binder-2 should be visible or exit 2.

### F6. Negative control is paired-only [INFERRED]

- Mutant "new binding never counts" (`bind_new` always nonzero) gives count 1 for `meta_false`, so `meta_false` passes. Only `positive` (expects 2) fails.
- The suite still fails, but `meta_false` alone does not prove the walk works. Read it together with `positive`.

### F7. Template realism [OBSERVED for one envelope; producer behavior UNKNOWN]

- Retained real envelope `.ufo/waves/round-22/evidence/c1/identify-godot.envelope.json` (2120 bytes, candidate): the only `"ok"` key is top-level `"ok":true`. Top-level `meta` is `{"command":"identify-flutter-build","duration":"122ms"}`. No `error`, `errors`, `code`, `status`, `completion_status`, or `exit_code` keys.
- So `meta.ok`, the shape `meta_false` injects, is not observed in that envelope. `meta_false` guards a hypothetical, fail-closed shape. W1's "observed shape" label for N1 is unsupported by the retained envelope. Other producer outputs were not checked. **UNKNOWN** beyond this file.
- The templates are independent of decision code. `counter-fixtures.py` imports only stdlib and calls the counter as a subprocess. Expected values are literals.
- Templates are simplified (no `subject`, `provider`, or `duration`). The binder does not read those fields.

### F8. Coverage gap vs W1 N1 spec [OBSERVED]

- W1 N1 names `meta_ok_false` and `meta_nested_refusal` (`meta.records:[{ok:false}]`). The frozen set has `meta_false` and `meta_array` (`meta.raw_result:[{ok:false}]`, `counter-fixtures.py:61`). `meta_nested_refusal` is absent.
- The generic walk handles list-in-meta; `meta_array` exercises the same path. This is an unpinned variant, not an uncovered path. Low.

### F9. Nits (no effect on verdict)

- The synthetic S058 row sits after a blank line (`body.replace('\n## Paths', ...)`), outside the Markdown table. `count-c1.py` parses lines, so this is harmless.
- v1 (`frozen/counter-fixtures-v1.py`) and both `expected` files had no `meta.ok` control. `meta_false` is new in v2.

## Re-evaluation of stale W1 findings against `2838351450…`

- W1 N1 (`CounterRefusals.md:218`, `meta.ok:false`): **closed** at candidate (`count-c1.py:42-55`, `is not True` walk over `meta`). Stale parts: `count 0` is superseded by 1; fixture names are replaced by `meta_false` and `meta_array`; `meta.ok:0` (W1 `:108`) is still uncovered (F4).
- W1 `:107` (legacy ignores `meta.ok`): confirmed by legacy source (`.ufo/waves/round-22/tools/count-c1.py:78-79`).

## Produced files and hashes

- `.ufo/waves/round-23/w2/Fixture15.md` (this report). Its sha256 is in the final message.
- Input pins verified by `git show <candidate>:PATH | sha256sum`:

| Path (candidate blob) | sha256 (prefix) | Pin check |
|---|---|---|
| `.ufo/waves/round-23/frozen/expected-v2.json` | `458b30d5a6…` | equals `count-c1.py:25` |
| `.ufo/waves/round-23/frozen/fixture.json` | `a1f5aff8ebb5…` | equals manifest `inputs` |
| `.ufo/waves/round-23/tools/counter-fixtures.py` | `f2990b35d113…` | equals manifest `inputs` |
| `.ufo/waves/round-22/tools/count-c1.py` | `c925918fb871…` | equals `count-c1.py:23`; same at base |
| `.ufo/waves/round-20/tools/verb-coverage.py` | `cfbf1880c4fb…` | equals helper pin; same at base |
| `.ufo/waves/round-21/tools/verb-coverage.py` | `615369384bf8…` | equals helper pin; same at base |

## Installs or none

None. No package or tool was installed. No pacman transaction. Shell use was limited to `git show`, `git ls-tree`, `sha256sum`, `grep`, `sed`, and `ls`.

## Open risks and limits

- Nothing was executed. All counter and selftest outcomes are source traces [INFERRED]. A run by the owning seat would turn F1 to F3 into OBSERVED.
- The stricter `bind_new` walk on real R23 envelopes (for example `decode-invalid-decoder`, `inspect-dart-legacy-saber`) was not examined. Positive preservation on real evidence is unverified here.
- Producer emission of `meta.ok` is UNKNOWN (F7).
- `expected-v2.json` `inputs` pins only the fixture and counter-fixtures. `count-c1.py` itself is not pinned. Tampering with it is caught behaviorally by `meta_false` and `positive`, not by the manifest.
