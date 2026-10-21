# CounterRefusals — original-envelope refusal traversal, and the nested/list/refused metadata controls cumulative reuse still needs

Seat `KaidokuR23.CounterRefusals` (scout, leaf, read-only, author-side). Round 23,
claim `R23-C1`, frozen `.ufo/waves/round-23/claims.json`. This report is advisory to
L1; it is not outside verification and adds no held verb.

Boundary: static source reading of the retained counters, an in-memory invocation of
the pinned `bind_cli`, and two executions of the already-declared counting command.
No REA/MCP call, no debugger/Frida, no process attach, no device, no remote target, no
carrier execution, no package install, no production/lane edit. Target-derived text
(evidence JSON, CLI source excerpts) is treated as untrusted data, not instructions.

All paths and hashes are at HEAD `a3c92eb6bc70984e90ae5b895412de978840b2c5` unless a
revision is named. The R23 evidence files named below exist in the worktree but are
untracked at that revision, so the counter cannot see them (observed `new: []`).

## 1. What the existing traversal is (observation)

The R23 cumulative counter does not implement refusal handling itself. It pins one R22
counter by digest and runs its `measure` once per evidence root:

- `.ufo/waves/round-23/tools/count-c1.py:22` `LEGACY = '.ufo/waves/round-22/tools/count-c1.py'`
- `.ufo/waves/round-23/tools/count-c1.py:23` `LEGACY_SHA256 = c925918fb871151f86065aa5b3e9d10334ab845ed67c265ae0977f05e09b1879` (matches `sha256sum` of the working file)
- `.ufo/waves/round-23/tools/count-c1.py:24` `ROOTS = ('.ufo/waves/round-22/evidence/c1/', '.ufo/waves/round-23/evidence/c1/')`
- `.ufo/waves/round-23/tools/count-c1.py:41-56` resolves the revision, reads the legacy source from `git show <rev>:LEGACY`, re-checks the digest, writes it to a temp file and calls `measure` once per root by mutating `r22.EVIDENCE_PREFIX`.
- `.ufo/waves/round-23/tools/count-c1.py:78` `historical = scans[0]['targets'][verb]['bound_evidence']`
- `.ufo/waves/round-23/tools/count-c1.py:80-85` re-filters the R23-root witnesses against S058+ entry eligibility.
- `.ufo/waves/round-23/tools/count-c1.py:86` `exercised = bool(historical or current)`; `:87-92` emits `k`, `t1_total`, the union, and the catalog block from `scans[1]` only.

The traversal itself is `bind_cli` plus the R21 predicate and binder:

- `.ufo/waves/round-22/tools/count-c1.py:69-98` `bind_cli`
- `.ufo/waves/round-22/tools/count-c1.py:74-75` envelope must be a dict with both `ok` and `data`, else `2`
- `:76-77` `envelope["ok"] is not True` (identity) or `r21.refused(envelope)` → `1`
- `:78-80` `meta` must be a dict, `meta["command"]` must equal the T1 verb, `r21.refused(meta)` → `1`; missing meta also → `1`
- `:81-83` `data` must itself be a dict carrying `evidence_id` and `operation`, else `2`
- `:84-94` iterative depth-first walk of `data`: lists are expanded; any dict with an `ok` key whose value is not literally `True` → `1`; any dict for which `r21.refused` is true → `1`; otherwise all values are pushed
- `:95-96` the record is passed to `r21.bind`, with `CLI_BIND_VERB` mapping only `debug-with-gdb → gdb-console` and `debug-with-rizin → rizin-debug-command`; other verbs use hyphen→underscore
- `:97-98` `ValueError`/`RecursionError` → `2`

The predicate and carrier walk (R21):

- `.ufo/waves/round-21/tools/verb-coverage.py:16-20` `REFUSALS` set
- `:33-36` `decode` rejects duplicate members and non-finite numbers
- `:39-55` `refused`: truthy `error`/`errors`; `code`/`status`/`completion_status` exactly in `REFUSALS`; `exit_code` present and not an `int` 0; recursion only through `raw_result` and `normalized_result`
- `:58-74` `records`: supported carriers are a bare record, list, `evidence`, `evidences`, `records`, `result`; an ancestor refusal is inherited
- `:77-101` `bind`: id shape, decode, carrier walk, exact `evidence_id`+`operation` match, `any(blocked)` → refused, else bound (with `pathless` flag)

Return types are a tri-state, not a boolean: **0 bound/countable, 1 refused, 2 unevaluable**.
The R22 candidate loop counts only 0 and records 2 in `unsupported_candidates`
(`.ufo/waves/round-22/tools/count-c1.py:160-164`). A `1` leaves no output trace.

The accepted R22 counter is a different file: `.ufo/waves/round-22/frozen/count-c1.py`
has no envelope, meta, or refusal traversal at all; it binds a bare record. R23 pins
the later tools version, so the historical R22 witnesses are re-derived under the
envelope traversal at the counting revision, not read from the R22 accepted result.
The R22 final record `.ufo/waves/round-22/verify/final/after-c1.json` was produced by
the pinned tools counter and bound both identify envelopes; `original-after-c1.json`
(frozen counter) bound only the extracted `identify-godot.evidence.json`. That
difference is why the traversal, not the frozen counter, is the right thing to harden
for cumulative reuse.

### Baseline executions (observation)

```
python3 -I -B .ufo/waves/round-22/tools/count-c1.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --rev e9db7e2d5798ff3d5f1ba5ccd76bb86f2cc5c1bb
# exit 1; t1_exercised_count 1; t1_exercised ["identify-flutter-build"];
# bound: ev_6a84742a… identify-flutter-build-saber.envelope.json,
#        ev_3458b996… identify-godot.envelope.json
```

```
python3 -I -B .ufo/waves/round-23/tools/count-c1.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --rev a3c92eb6bc70984e90ae5b895412de978840b2c5
# exit 1; finding c1_incomplete; k 1; t1_total 6;
# historical: two identify-flutter-build envelopes above; new: [] for all six verbs
```

The second run is the current cumulative baseline: `1/6`, exact incomplete count `5/6`.
The R23 signal envelopes bind in isolation (below) but are invisible until committed
and cited by an S058+ entry.

## 2. Observed control matrix (observation)

Harness: `python3 -I -B -` imports the pinned
`.ufo/waves/round-21/tools/verb-coverage.py` and
`.ufo/waves/round-22/tools/count-c1.py` and calls
`bind_cli(r21, json.dumps(envelope), verb, evidence_id)` on synthetic envelopes. No
file was written; no lane state changed. The table is the transcribed return code.

| code | shape |
|---:|---|
| 0 | valid envelope: `ok:true`, matching `meta.command`, direct record with matching id/operation |
| 1 | envelope `ok:false` with `data` present |
| 2 | envelope `ok:false` **without** `data` (real typed-refusal shape) |
| 2 | envelope missing `data` |
| 1 | envelope `ok:"true"` (string) |
| 1 | `meta` absent |
| 1 | `meta` is a list |
| 1 | `meta.command` mismatch |
| 1 | `meta.error` non-empty |
| 1 | `meta.exit_code: 1` |
| 1 | `meta.exit_code: null` (false refusal; see N10) |
| 0 | `meta.ok:false` (ignored) |
| 0 | `meta.ok:0` (ignored) |
| 0 | `meta.diagnostics.error` (nested error ignored) |
| 0 | `meta.records:[{ok:false}]` (nested ok ignored) |
| 0 | `meta.status:"unavailable"` (not in `REFUSALS`) |
| 1 | `data.ok:false` |
| 1 | `data.ok:"true"` (string) |
| 1 | `data.result.ok:false` |
| 1 | `data.records:[{ok:false}]` |
| 0 | `data.records:[{evidence_id,operation}]` (no refusal; gate passes on the outer record) |
| 2 | `data` is a list of records |
| 2 | `data = {records:[record]}` |
| 2 | `data = {ok:false, records:[record]}` (refusal not classified) |
| 0 | top-level sibling `result:{ok:false}` |
| 0 | top-level sibling `warning:{error:{code:…}}` |
| 0 | top-level sibling `results:[{ok:false}]` |
| 0 | top-level `provider:{status:"unavailable",code:null}` |
| 1 | `data.status:"error"` |
| 0 | `data.status:"unknown"` |
| 1 | `data.status:"VALIDATION_ERROR"` |
| 0 | `data.status:"validation_error"` (case) |
| 0 | `data.status:"unavailable"` |
| 1 | `data.completion_status:"failed"` |
| 0 | `data.completion_status:"complete"` |
| 0 | `data.completion_status:"unknown"` (timeout still counts) |
| 0 | `data.output_truncated:true` (partial output still counts) |
| 1 | `data.exit_code:1` |
| 0 | `data.exit_code:0` |
| 1 | `data.exit_code:null` (false refusal) |
| 0 | `data.error:{}` |
| 0 | `data.error:""` |
| 1 | `data.error:{code:""}` (any non-empty error object) |
| 1 | `data.errors:[{code:"execution_failure"}]` |
| 0 | `data.errors:[]` |
| 1 | `data.normalized_result:{status:"error"}` |
| 1 | `data.normalized_result:{items:[{status:"error"}]}` |
| 1 | `data.normalized_result:{tool:{exit_code:null}}` |
| 0 | envelope `raw_result:[{ok:false,error:…}]` (`refused()` is list-blind) |
| 0 | `meta.raw_result:[{error:…}]` (`refused()` is list-blind in metadata) |
| 1 | `data.raw_result:[{ok:false,error:…}]` (the data DFS reaches the list) |
| 1 | `data.code:"failed"` |
| 0 | `data.code:"FAILED"` (case) |
| 1 | `data.provider_operation_health:{state:"failed",exit_code:null}` (blocked by null exit_code, not by `state`) |
| 0 | `data.provider:{status:"unavailable",code:"executable_missing"}` (provider rejection code not in `REFUSALS`) |
| 1 | `data.records:[{ok:false, evidence:{same id}}]` (refusal ancestor wins over a nested copy) |
| 1 | `data.operation` mismatch |
| 1 | `evidence_id` mismatch |

Two consequences worth separating:

1. **The old R22 C1Refusal finding is closed as a count but open as a classification.**
   The attack shape `data = {ok:false, records:[record]}` now returns **2**, not **0**:
   the direct-record gate at `count-c1.py:81-83` rejects it before the DFS. It cannot
   count. It is nevertheless reported as `unsupported_candidates`, not as a refusal;
   the refusal ancestry is not preserved in the output.
2. **The current R23 evidence does not contain control-shaped payload keys.** A
   recursive scan of `.ufo/waves/round-23/evidence/c1/*.envelope.json` for
   `ok`/`error`/`errors`/`code`/`status`/`completion_status`/`exit_code` found no hits
   inside `data`. The four successful envelopes bind under the pinned traversal:

```
0  inventory.envelope.json          ev_940cf7bb…  inspect_signal_decoders
0  uart-help.envelope.json          ev_4be13793…  inspect_signal_decoders
0  decode-official-uart.envelope.json ev_1d361f25… decode_signal_recording
0  decode-uart-hi.envelope.json     ev_bcadf773…  decode_signal_recording
-  decode-invalid-decoder.envelope.json  ok:false, error.execution_failure, no data, no evidence_id
```

The last file is a deliberate typed refusal. It has no `evidence_id`, so the R22
candidate loop never even calls `bind_cli` for it (`count-c1.py:158` skips blobs that
do not contain the cited id). It must not count, and does not; but it is invisible in
the R23 output rather than counted as a refusal.

## 3. Controls that hold today (observation)

- **C1 Envelope shape.** `ok` and `data` are required; non-object input is unevaluable.
- **C2 Envelope success.** `ok is True` by identity, not truthiness.
- **C3 Envelope refusal.** Truthy `error`/`errors`; refusal-token `code`/`status`/`completion_status`; non-zero/non-int `exit_code`; recursion into `raw_result`/`normalized_result`.
- **C4 Metadata binding.** `meta` object, exact `command`, `refused(meta)`; missing meta is refused.
- **C5 Record gate.** `data` must be the evidence record itself with `evidence_id` and `operation`.
- **C6 Nested refusal walk.** Any reachable dict under `data` with `ok` present and not `True`, or a refused control field, blocks the envelope. Lists are expanded.
- **C7 Binder.** Duplicate-member and non-finite JSON rejected; supported carrier set; ancestor refusal inherited; exact id+operation; `any(blocked)` blocks; operation aliases for the two debugger verbs.
- **C8 Citation and source linkage (R22 half).** Exact file membership (directories do not expand, `count-c1.py:154`); the id must occur in the blob; only code 0 counts; the entry must cite an S051+ mined A/B row opened `2026-10-21` whose used-by names the entry (`:129-142`).
- **C9 Cumulative wiring (R23 half).** Two fixed roots; historical from the R22 root, new from the R23 root; S058+ floor for new entries (`count-c1.py:71-74`); per-verb union so a verb is never double counted (`:86-87`); catalog block emitted once (`:90-91`); legacy source digest pinned (`:23,43-45`); historical witness loss is indirectly caught by fixture `positive` expecting count 2 (`frozen/expected.json`).

## 4. Controls needed for cumulative reuse

### 4.0 The three container classes, and where the current walk is blind

| container class | reached today by | blind spot |
|---|---|---|
| envelope top level | `ok` identity, `refused(envelope)` (which checks `error(s)`, `code`, `status`, `completion_status`, `exit_code`, and recurses only through `raw_result`/`normalized_result`) | every sibling container not named `data`/`meta`: `result`, `results`, `warning`, `provider`, `diagnostics`; and any list-wrapped refusal in envelope `raw_result` (list-blind) |
| `meta` | `refused(meta)` only; no DFS | `meta.ok` (any value), `meta.records[...].ok`, nested `meta.diagnostics.error`; list-wrapped refusals in `meta.raw_result` |
| `data` | full DFS over dicts and lists before binding | none nested — but the direct-record gate rejects a list or wrapper `data` (code 2) **before** the DFS, so a refused wrapper is classified unevaluable |
| `data.normalized_result` | DFS reaches it; `refused` also recurses | provider availability `status`/`code`/`state` values are not all in `REFUSALS`; `completion_status:"unknown"` and `output_truncated` count |
| `data.raw_result` | DFS reaches it (including lists) | none for refusals, but large raw payloads are walked dict-by-dict |

The practical rule for cumulative reuse: the traversal is **not** a uniform
"any refusal anywhere blocks" walk. It is a union of (a) a shallow envelope/meta
predicate that ignores `ok` and lists, and (b) a deep `data` walk that is skipped
when `data` is not already the record. Both halves need a control before the two
roots can be compared year over year.

Each row below gives the shape observed in §2, why it matters when R22 and R23
evidence are counted together, the narrow control, and the fixture that would pin it.
`[INFERENCE]` marks source-derived expectations not executed end-to-end in this report.

### 4.1 Count-affecting refusal controls (a refused envelope could count)

| id | observed shape | cumulative risk | narrow control | fixture |
|---|---|---|---|---|
| N1 | `meta.ok:false` / `meta.records:[{ok:false}]` → 0 | Metadata refusal is invisible; a new R23 entry could cite an envelope whose metadata declares failure and k rises. | Apply the same recursive `ok`/`refused` walk to `meta` before accepting the command, or reject any `meta` containing `ok` not literally `True`. | `meta_ok_false`, `meta_nested_refusal`; expect count 0, exit 1 |
| N2 | top-level `result`/`warning`/`results`/`provider` carrying `ok:false` or `error` → 0 | A refusal in a sibling container of `data` is never traversed; a copied/derived envelope can hide the parent refusal outside `data`. | Walk every top-level value except `data` (which is already walked) for control signals, or define a closed carrier allowlist and reject unknown non-scalar siblings. | `sibling_refusal`, `sibling_error`; expect 0 |
| N3 | `status:"unavailable"`, `provider.code:"executable_missing"`, `state:"failed"` → 0 | The `REFUSALS` set omits provider rejection codes and the `state` key; a successful envelope carrying unavailable-provider diagnostics would count. | Add `contracts/providerSelection.js:16-30` codes and `state` to the checked control fields; normalize case (see N11); scope to control objects so prose is never matched. | `provider_rejection_code`, `provider_state_failed` |
| N4 | `completion_status:"unknown"` → 0 | A timed-out/truncated gdb or rizin command can count as exercised. R23's boundary excludes new debug execution, but the rule must be explicit for cumulative reuse. | Decide and encode: either block on `completion_status != "complete"` (conservative) or emit `partial:true` and keep it out of any mastery wording. | `completion_unknown`, `output_truncated` |
| N5 | same `evidence_id` in a refused file and a valid file → the valid file still counts (per-file loop, `count-c1.py:153-164`) | A copy can erase a parent refusal across roots; this is the claim's explicit falsifier. REA binds `evidence_id` to the record's semantic projection (`dist/domain/evidence.js:133-140`), but the counter never compares projections. | Group code-0 witnesses by `evidence_id` across both roots; if a cited carrier for the same id returns 1 and its semantic projection matches, block; if projections differ, mark ambiguous/unevaluable. | `duplicate_id_refused_cross_root` |
| N6 | envelope bytes are never compared with the producing `run.stdout` (explicit R22 limit) | A fabricated `ok:true` envelope around a refused record's data is indistinguishable from a producer call. | Keep the R22 provenance pairing (`verify/final/provenance.json`) as a separate required gate for every counted new witness: paired `.run.json`, exit 0, stdout equal to envelope; do not call the counter authenticated. | `envelope_without_run`, `stdout_mismatch` |
| N7 | `error:{}` / `errors:[]` → 0; `error:{code:""}` → 1 | Empty control objects are treated as success; malformed refusal containers pass. | Treat a present but empty `error`/`errors` as unevaluable (2) or document that only non-empty objects refuse; cover both in fixtures. | `error_empty_object`, `errors_empty_list` |

### 4.2 Classification and audit controls (no count change, but refusals are hidden)

| id | observed shape | cumulative risk | narrow control | fixture |
|---|---|---|---|---|
| N8 | `data = {ok:false, records:[record]}` → 2; `data` list → 2 | The direct-record gate keeps the R22 attack from counting, but reports it as an unsupported representation, so an auditor cannot tell "refused" from "unparseable". | Run a refusal pre-scan over `data` (and the envelope) before the record gate; return 1 when a refusal is present and 2 only when the carrier is merely unsupported without refusal evidence. | `data_wrapper_refused` expects refused, not unevaluable |
| N9 | top-level `ok:false` envelope with no `data`/id never reaches `bind_cli` (`:158` skips it) | The real `decode-invalid-decoder` refusal is invisible in the R23 output. It cannot count, but the final report cannot say "we saw and rejected a refusal". | Add a cited-file classification pass: if a cited file is `ok:false` and `meta.command` matches the verb, record `refused_candidates` with path and error code even without an evidence id. | `refusal_no_data` cites the refusal; expect `refused_candidates` non-empty, count unchanged |
| N10 | every refusal reason collapses to `1` | The claim's falsifiers ("refusal counted", "copy erases parent refusal") cannot be audited from the counter output. | Return `(code, reason)` internally (`envelope_not_ok`, `envelope_refused`, `meta_missing`, `meta_command`, `meta_refused`, `data_gate`, `nested_ok`, `nested_refused`, `binder_refused`, `unevaluable`) and aggregate counts per verb/root. | `reason_tags` |
| N11 | `status:"VALIDATION_ERROR"` → 1 but `"validation_error"`/`"FAILED"` → 0 | Case variants silently count. | Compare `value.lower()` against a lower-cased refusal set; keep exact key names. | `uppercase_status` |
| N12 | `exit_code:null` → 1 (false refusal), including `provider_operation_health` which declares `exit_code: z.number().int().nullable()` (`contracts/toolOutputSchemaPrimitives.js:185`) | A future successful envelope carrying nullable provider health would be rejected and a valid new verb lost. This is an undercount, opposite to N1-N3. | Refuse only when the value is an `int` and non-zero; absent/null is not a refusal. | `null_exit_code_sibling` expects 0 |
| N13 | duplicate `bound_evidence` pairs and the hard `[:5]` cap (`count-c1.py:168`) | The wrapper only sees at most five witnesses per verb/root; duplicates crowd out valid ones, and a sixth valid witness can be dropped. The R23 docstring discloses undercount but not which candidates were lost. | Dedupe by `(evidence_id,path)` before the cap; emit `candidate_count` and `candidates_truncated`. Consider scanning all files in the wrapper instead of relying on the capped list. | `six_witnesses` where the sixth is the only valid one |
| N14 | historical witnesses are recomputed, not asserted (`count-c1.py:78`) | If an R22 source row or entry is edited, `historical` silently becomes empty and k drops. The claim's falsifier "inherited identify lost" needs a loud failure. | Assert the expected historical verb/witness set (at minimum `identify-flutter-build` with an R22-root envelope) and emit `historical_witness_lost` rather than a lower k. | `historical_lost` expects an explicit failure finding |
| N15 | new controls would apply only to the R23 root if implemented in the wrapper | Historical and new evidence would be admitted under different refusal rules, making cumulative k non-comparable. | Either apply the additional refusal re-check to both roots (read the R22 file at rev) or emit `historical_policy: r22_pinned` as an explicit, disclosed asymmetry. | `historical_parity` |

### 4.3 Cumulative source-linkage and wiring controls

| id | observed shape | cumulative risk | narrow control | fixture |
|---|---|---|---|---|
| N16 | wrapper picks **any** S058+ eligible entry that contains path/eid/verb (`count-c1.py:80-85`); the entry that actually bound the witness is not recorded | An unrelated eligible entry can supply the new-source linkage for a witness documented by a different entry — "mere mention" at the linkage step, even though the envelope itself is bound. [INFERENCE from the exact expressions, simulated with synthetic text.] | Record the binding entry for each witness (rescanning entries for the exact path/id/verb) and require the S058+ row's used-by to name that same entry; or emit both entries and require L1 to admit the pairing explicitly. | `other_entry_links` expects the new witness rejected |
| N17 | wrapper re-check uses a case-sensitive hyphen-only token: `(?<![A-Za-z0-9_-])<verb>(?![A-Za-z0-9_-])` (`:83`); legacy `command_pattern` accepts hyphen or underscore and is case-insensitive (`.ufo/waves/round-20/tools/verb-coverage.py`, R21 `_measure` usage) | An entry that names `decode_signal_recording` binds under the legacy scan but is dropped from `new` by the wrapper. Observed predicate comparison: legacy `True`, wrapper `False` for underscore and mixed-case forms. | Reuse `r20.command_pattern(verb)` in the wrapper, or state a strict literal-entry contract and keep both predicates in sync. | `underscore_token_entry` expects the new witness counted |
| N18 | inherited R22 `eligible` is a **set of texts**, not entry paths (`count-c1.py:133-142`, used at `:161`) | A duplicate knowledge text at another path inherits historical eligibility without its own source row used-by. This is inherited R22 behavior, but cumulative reuse makes copied entries more likely. | Recompute historical eligibility by entry path in the wrapper, or pin the expected historical witnesses (N14) and disclose the inherited text-keyed limit. | `duplicate_text_entry` expects no historical witness from the copy |
| N19 | `t1_exercised_count` and `t1_total` only (`count-c1.py:88-92`) | The claim asks for the exact incomplete count; it is derivable but not emitted, and per-verb state is only `historical`/`new`. | Emit `t1_incomplete_count = t1_total - k` and a per-verb `reason` (`historical`, `new`, `refused_only`, `unbound`, `unmentioned`). | `incomplete_count` |
| N20 | catalog block from `scans[1]` only (`:90-91`) | Correct today; summing the two scans would produce `270/153`. | Assert `catalog_total == 153`, emit the block once, and never sum. | `catalog_single_block` |
| N21 | reserved payload keys are not documented, but the DFS treats `ok`/`error(s)`/`code`/`status`/`completion_status`/`exit_code` at any depth in `data` as control signals | A future schema field with one of these names could false-refuse a successful envelope. Current R23 signal payloads have none (observed scan), but the contract is implicit. | Document the reserved control-key set for T1 evidence; add a schema/payload scan to the fixture suite; keep the DFS behavior explicit rather than accidental. | `payload_control_key` expects a documented decision (block or permit) |
| N22 | evidence is read with `git show <rev>:path` (`count-c1.py:131,151-156`) | Worktree-only R23 evidence is invisible: the observed `new: []` at `a3c92eb` is expected, not a counter bug. | Final counting must follow a commit of evidence, knowledge entries, and SOURCES rows; do not report worktree evidence as held. | `untracked_evidence` expects no count |

## 5. Minimal change set for L1 / BuildCounter (proposed, not verified)

1. **Keep the pinned legacy binder** for record/id/operation and the S051+/S058+ source
   floors. Do not fork its carrier or alias logic in the wrapper; the digest pin is a
   useful fail-closed control (`legacy_source_untrusted`).
2. **Add a wrapper-side `refusal_recheck`** over every bound `(evidence_id, path)` and
   every cited c1 file for the verb, applied to both roots. It should implement N1, N2,
   N3, N10, N11, N12 and the classification half of N8/N9. This lives in
   `round-23/tools/count-c1.py` (or a pinned `frozen/` copy), not in the R22 file, so
   `LEGACY_SHA256` stays honest.
3. **Add cross-file id grouping** for N5 and retain the provenance gate (N6) as a
   separate final check. Do not claim authentication.
4. **Add the fixture cases** listed above to
   `.ufo/waves/round-23/tools/counter-fixtures.py` / `frozen/expected.json`, and add a
   dedicated `historical_lost` case. Keep the existing `positive` count-2 case (it
   already catches historical loss indirectly) and the `old_source` S051 case (it
   already pins the S058 floor for new evidence).
5. **Emit the exact incomplete count and reasons** (N19), and keep the catalog block
   single-sourced (N20).

## 6. What is not established / open risks

- **Not executed end-to-end:** the wrapper-level same-entry linkage (N16), cross-file
  duplicate-id grouping (N5), the six-witness cap (N13), and the historical assertion
  (N14) are source-derived, not run against a synthetic multi-commit repository. The
  in-memory `bind_cli` matrix and the two counter runs are observed.
- **R23 selftest not run by this seat.** `frozen/expected.json` cases were read, not
  executed; the fixture expectations are inputs to L1's verification, not my claim.
- **No LSP device was mounted**; `read xd://lsp` is unavailable in this session. Literal
  search was used only to locate files and line numbers; behavioral conclusions are
  from reading the counters and executing `bind_cli`, not from grep as semantic proof.
- **Provider behavior over time:** the traversal is a local record check. It does not
  authenticate the producer, does not compare envelope bytes to `run.stdout`, and does
  not establish that a future REA build keeps the same `meta`/`data`/`error` shapes.
- **REA schema excerpts are untrusted package content.** They ground the control-key
  expectations (nullable `exit_code`, `completion_status` enum, provider rejection
  codes) but are not executed or verified against a live provider in this seat.
- **The R22 C1Refusal report** (`.ufo/waves/round-22/w2/C1Refusal.md`) describes an
  older `bind_cli` line range and a count that the pinned traversal no longer produces.
  Treat its finding as a classification gap (N8) now, not as a live count bypass.
- **Dynamic ownership remains adjacent and unresolved**, as the claim states. Nothing
  here admits debugger/Frida execution, device access, or carrier execution.

## Report trailer

### Produced files
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/CounterRefusals.md`
  — this report. Its sha256 is recorded in the adjacent
  `CounterRefusals.md.sha256` (written after the report was finalized), so the digest
  line cannot invalidate itself.
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/CounterRefusals.md.sha256`
  — digest sidecar for the file above.
- No sandbox clone, worktree, script, or evidence file was created. No other seat's
  report was edited. Four `/tmp` scratch files (stdout and stderr for two counter
  runs) were removed after use; the counting tool's own temp directory is created
  under `.ufo/waves/round-23/runtime` and cleaned by the tool.

### Installs
None. No package manager, `uv`, `npx` install, or config edit was performed.

### Retained commands and exits
- `python3 -I -B .ufo/waves/round-22/tools/count-c1.py --root … --rev e9db7e2…` → exit 1, k=1.
- `python3 -I -B .ufo/waves/round-23/tools/count-c1.py --root … --rev a3c92eb…` → exit 1, k=1, historical two identify witnesses, new empty.
- In-memory `bind_cli` matrix (§2 table) → codes as tabled; no files written.
- Pin/input hashes observed:
  - `.ufo/waves/round-22/tools/count-c1.py` `c925918fb871151f86065aa5b3e9d10334ab845ed67c265ae0977f05e09b1879`
  - `.ufo/waves/round-23/tools/count-c1.py` `7c356b97da675a7bdb1dd0f8d113f97c1f47228419c608f6817e095e2b2508f6`
  - `.ufo/waves/round-23/tools/counter-fixtures.py` `96e65034bcf2206c0e9c6335da264695f4741ed91e9a357c56484e6cd35e2849`
  - `.ufo/waves/round-23/frozen/expected.json` `ad1b446268e8ada9c5cc9ca084827dad4dba1fafc374ee55925b56c9e5d0fc24`
  - `.ufo/waves/round-23/frozen/fixture.json` `a1f5aff8ebb5e5d327522031b74ed91283708907af0fc4a6df24812479bfef4b`
  - R23 evidence envelopes: `inventory` `5f802187…`, `uart-help` `462bc694…`, `decode-official-uart` `7d5e07cc…`, `decode-uart-hi` `a40c947c…`, `decode-invalid-decoder` `04697e72…`.
