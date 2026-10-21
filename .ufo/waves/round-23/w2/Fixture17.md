# Fixture17: `sibling_refusal` review (R23-C1, candidate 2838351450ff1ee4baa620c962a1153450d53311)

Scope: `frozen/expected-v2.json` case `sibling_refusal`, `frozen/fixture.json`, and the `sibling_refusal` branch of `tools/counter-fixtures.py`, checked against candidate counter `tools/count-c1.py`.

Method: pinned bytes via `git show <rev>:PATH` (candidate and baseline aa1450b), `sha256sum`, `grep -n`/`sed -n`, and `json.load` on pinned blobs. Nothing was executed: no counter run, no fixture run, no suite, no clone writes.

Labels: **observed** = read from pinned bytes. **traced** = derived by static walk of pinned code, not run. **inferred** = not re-derived here.

## Verdict

- The expectation `{exit 1, count 1, finding c1_incomplete}` is correct for the traced candidate behavior. No wrong expectation found.
- The case distinguishes the sibling-refusal fault. Removing the envelope-wide refusal walk turns this envelope into a binding (count 2), and the case fails.
- The case is one-sided and single-shape. Five mutation classes (S1–S5) survive every v2 expectation. Four proposed rows would close them. Not applied: the fixtures are frozen and not mine to edit.

## Pinned inputs

| Path (candidate 2838351) | sha256 | Check |
|---|---|---|
| `.ufo/waves/round-23/frozen/expected-v2.json` | `458b30d5a6420c1b37874c3364d3ae3b22529d6c3560b5241848a21eec97096f` | equals `SELFTEST_MANIFEST_SHA256` in count-c1.py (observed) |
| `.ufo/waves/round-23/frozen/fixture.json` | `a1f5aff8ebb5e5d327522031b74ed91283708907af0fc4a6df24812479bfef4b` | equals manifest input pin (observed) |
| `.ufo/waves/round-23/tools/counter-fixtures.py` | `f2990b35d113b5e44317e7f00e6ca5157baae1efb5ee1a1b8e4995d0ace1a97f` | equals manifest input pin (observed) |
| `.ufo/waves/round-23/tools/count-c1.py` | `f4b8d16ac195ca106a99cbb9236d36d1283dee349c6fef3a49567de0bbea0cc2` | not pinned by the manifest (observed) |
| `.ufo/waves/round-22/tools/count-c1.py` | `c925918fb871151f86065aa5b3e9d10334ab845ed67c265ae0977f05e09b1879` | candidate = baseline = `LEGACY_SHA256` (observed) |
| `.ufo/waves/round-21/tools/verb-coverage.py` | `615369384bf821a44e4d3c458006ed169939025d8fd3415f318ae37bb52f887b` | candidate = baseline = `HELPER_SHA256` (observed) |
| `.ufo/waves/round-20/tools/verb-coverage.py` | `cfbf1880c4fb2bba80e3c2e40e236165a67c03bf51cced4983b469cfe315b26f` | candidate = `HELPER_SHA256` (observed) |
| `.ufo/waves/round-20/verify/round20/verb-coverage.json` | n/a | candidate identical to baseline (`git diff --quiet` exit 0, observed) |
| `corpus/SOURCES.md` at baseline | n/a | one `## Paths` at line 65; no S058 row; S051 at line 57 (observed) |
| `.ufo/waves/round-23/frozen/expected-v1.json`, `expected.json`, `counter-fixtures-v1.py` | n/a | no `sibling_refusal` entry or branch (observed) |

## Findings

### F1. Expected values: no defect

- `expected-v2.json:88` gives `sibling_refusal` = `{exit 1, count 1, c1_incomplete}`. `expected-v2.json:8` gives `positive` = `{exit 1, count 2, c1_incomplete}`.
- Traced: `bind_new` returns 1 for the sibling (`count-c1.py:51–53`, see F2). `count-c1.py:123` then never appends `inspect-signal-decoders`. `held` (`:127`) is the baseline historical set only. Count 1, `c1_incomplete`, exit 1 via `:166`.
- Inferred: the baseline historical set is `{identify-flutter-build}`. Corroborated by `claims.json` (`"before": 1`). `measure()` raises `historical_baseline_changed` on any other set, but I did not re-derive that set.
- `sibling_refusal` is a v2-only row (absent from v1 manifest and v1 fixtures). No expectation drift.

### F2. Discrimination: the case isolates the envelope-wide walk

- `count-c1.py:42–54` (`bind_new`): `pending = [decoded envelope]` (`:45`). For each dict node, `('ok' in node and node['ok'] is not True) or r21.refused(node)` returns 1 (`:51–52`). Otherwise the walk extends `node.values()` (`:53`). The fallback is `r22.bind_cli` (`:54`).
- Sibling envelope (traced): the root passes `:51` (`ok` is True, and `refused(root)` is False). The walk reaches `{'errors': ['execution_failure']}` under key `result`. `r21` `refused()` returns True because `node.get('errors')` is truthy (`r21:43–45`). `bind_new` returns 1.
- `bind_cli` alone would bind this envelope (traced). `count-c1.py`'s R22 copy, `bind_cli` at `round-22/tools/count-c1.py:69`:
  - `:76` checks only the root `ok` and `refused(root)`. `refused()` never reads a key named `result`.
  - `:84–92` walks only `record = envelope["data"]`.
  - `:96` binds and returns 0.
- Conclusion (traced): the case discriminates exactly the envelope-wide walk at `count-c1.py:53`.

### F3. Positive preservation: holds (traced)

- The sibling case and `positive` share byte-identical entry text, synthetic SOURCES row, eid, and path. Default selection is `counter-fixtures.py:38`. The only delta is root key `result`, appended at `counter-fixtures.py:62–63` to a per-case deepcopy (`:37`).
- Non-vacuity: `positive` (expected 2) shows the same entry, row, and eid reach `bind_cli`. So the sibling's count 1 cannot come from eligibility, mention, or path failure.
- Traced positive path: the walk finds nothing. `bind_cli` passes `meta.command`, record shape, and `r21.bind` (`r21:77`, `evidence_bound`, returns 0). Count 2.
- Per-case isolation: each case does `git reset --hard` and `git clean -fd` in the disposable clone (`counter-fixtures.py:35–36`, inside the loop at `:33`).

### F4. Oracle independence: mostly holds, one coupling

- Expected values are literals in `expected-v2.json`. The builder imports only `copy, json, os, pathlib, subprocess, sys, tempfile` (`counter-fixtures.py:7–13`). It imports no counter, r21, or r22 code.
- Coupling: the fixture template is shaped to exactly the fields `bind_cli` reads (`ok`, `meta.command`, `data.evidence_id`, `data.operation`). The refusal payload uses the counter's own predicate vocabulary (`errors`; `execution_failure` is in `REFUSALS`, `r21:16–17`). The case therefore validates the walk, not that producers emit this shape.
- The R21 selftest expresses the same structure differently. `r21 selftest:161` (`outer_refusal`) puts a singular `error: {code: ...}` beside `result`. `r21 selftest:160` is the canonical `error={'code': ...}` form. No v2 case uses singular `error`: `fixture.json` has 0 occurrences of `"error"`.

### F5. Narrow "sibling" coverage (gap)

- The comment at `count-c1.py:43` says refusal ancestry is kept "in metadata/sibling containers as well as data". The case's only sibling is key `result`, which is already an R21 carrier name (`r21:72`: `('evidence', 'evidences', 'records', 'result')`).
- No v2 case places a refusal under a non-carrier root key.

### F6. One-sided: no benign-sibling control

- Every v2 document in `fixture.json` has exactly keys `(data, meta, ok)` (observed). The only added root key in all of v2 is `sibling_refusal`'s `result`.
- No case checks that a benign sibling still binds.

## Mutation analysis (traced, not executed)

Killed by `sibling_refusal` (count 2 ≠ 1, case FAILS):
- **K1**: `bind_new` returns `bind_cli` directly, with no envelope walk.
- **K2**: the walk checks only `ok`, without `refused()` at `count-c1.py:51`.
- **K3**: the walk descends only into `data`/`meta`, so root `result` is never visited.
- **K4**: `refused()` drops the `errors` key (`r21:43`).

Survive every v2 expectation (traced):
- **S1 over-refusal**: any root key outside `{ok, meta, data}` refuses. Every other v2 envelope has only those keys.
- **S2 presence, not truthiness**: `refused()` uses `if key in node` (`r21:44`). No v2 case has an empty or falsy `error`/`errors`.
- **S3 carrier-restricted walk**: the walk descends only into R21 carrier keys plus `data`/`meta`. `result` is a carrier name. Every other v2 refusal sits under `data`, `meta`, or root `ok`.
- **S4 singular `error` dropped**: `refused()` loses `'error'` from its key tuple (`r21:43`). No v2 case uses singular `error`.
- **S5' list-only**: `refused()` accepts only list-valued `errors`. Both list-valued refusal rows (`sibling_refusal`, `nested_refusal`) still refuse. No string-valued `errors` case exists.

Equivalent, not a weakness: returning 1 vs 2 from `bind_new`. The only call site tests `== 0` (`count-c1.py:123`).

## Proposed additional v2 rows (not applied)

Expected values are static-trace predictions. The designated run seat must confirm them.

- **`sibling_benign`**: root `result: {'errors': []}` and `diagnostics: {'status': 'recorded'}`. Expect `{exit 1, count 2, c1_incomplete}`. Kills S1 and S2. Candidate: `[]` is falsy (`r21:44–45`), and `'recorded'` is not in `REFUSALS`.
- **`sibling_error_key`**: root `error: {'detail': 'opaque'}`. Expect `{exit 1, count 1, c1_incomplete}`. Kills S4. Pitfall: `error: {'code': 'execution_failure'}` does NOT kill S4, because the `code` leg (`r21:46–49`) still refuses.
- **`sibling_noncarrier`**: root `diagnostics: {'errors': ['execution_failure']}`. Expect `{1, 1, c1_incomplete}`. Kills S3.
- **`sibling_string_errors`**: root `result: {'errors': 'execution_failure'}`. Expect `{1, 1, c1_incomplete}`. Kills S5'.

## Produced files and hashes

- `.ufo/waves/round-23/w2/Fixture17.md` (this report). Its own sha256 is reported in the final message, since a file cannot embed its own hash.
- No other files written.

## Installs

None. Only read-only `git show`/`ls-tree`/`cat-file`/`diff --quiet`, `grep`, `sed`, `sha256sum`, and `python3 -c json.load` on pinned blobs.

## Open risks

- All verdicts are static traces. Nothing was executed. A runtime disagreement would have to come from a path not traced here.
- Baseline historical set `{identify-flutter-build}` is inferred from `claims.json`, not re-derived.
- The manifest pins fixtures and expected values, not the counter. Counter identity is recorded only by the run's argv and revision.
- Producer-shape question (F4) applies suite-wide, not only to this case.
- Peer reports untouched. No W1 proposal finding re-evaluated; out of item scope.
