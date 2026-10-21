# KaidokuR23.CriticOriginal — R23-C1 refusal-walk falsification

Scope: whether the new all-envelope structural refusal walk in `bind_new` can still drop
metadata/list/sibling refusal ancestry before the legacy binder runs, and whether the result
is local association or authentication. Source review only. All bytes were read with
`git show 2838351450ff1ee4baa620c962a1153450d53311:PATH` (B=`aa1450b82f9ede35aada63efe8a34e01c6e02f72`).
No counter, selftest, build, producer replay, or target execution was run by this seat.

Verdict: **no ancestry drop inside the structural vocabulary at the candidate bytes.** The four
held verbs survive every counterexample I could build from local evidence. The remaining gaps are
vocabulary/representation tradeoffs and one stale prose line. None of them changes k=4 at the
candidate.

## Findings

### F1 — The walk reaches every container (observed)
`count-c1.py` (blob sha256 `f4b8d16ac195ca106a99cbb9236d36d1283dee349c6fef3a49567de0bbea0cc2`,
equal to `counter_sha256` in `verify/initial/metadata-red-green.json`), lines 43–56:
- The root is decoded with `r21.decode`, which rejects duplicate members and the NaN/Infinity
  literals. That closes `"ok":false,"ok":true` shadowing; the `duplicate_member` fixture covers it.
- The walk is an iterative stack over every list item and every dict value, so there is no depth
  limit from the walk itself. A deep decode raises `RecursionError`, which returns 2.
- Every dict is checked for `'ok' in node and node['ok'] is not True` or `r21.refused(node)` before
  `r22.bind_cli` is called. So `meta`, `meta.raw_result[…]`, siblings of `data` such as `result`,
  and anything under `data` are all checked. Values like `ok: 1`, `ok: "true"` and `ok: null` fail
  closed.
- The walk is a strict superset of what `bind_cli` checks (`r22.py:70-97`: top level, `meta`, and
  the `data` subtree only). On a hit it returns 1 before the legacy binder is reached, so the legacy
  path cannot remove an ancestor.
- Frozen fixtures `meta_false`, `meta_array`, `sibling_refusal`, `nested_refusal` and
  `refused_parent` exercise each placement (`counter-fixtures.py:50-62`). Legacy binder 0 versus
  current 1 is recorded for `meta_false` and `meta_array` in `metadata-red-green.json`; that file
  was produced at source revision `6615aea`, not by this seat.

### F2 — The ancestry is only as complete as `REFUSALS` and `refused()` (inferred tradeoff, not exploitable at candidate)
`r21.py:16-55` (sha256 `615369384bf8…`, pinned by `r22.py:38`) recognises only these signals: a
truthy `error`/`errors`; a string `code`/`status`/`completion_status` in the 16-word `REFUSALS`
set; a non-int or non-zero `exit_code`; and `raw_result`/`normalized_result` one level down.
Working from the source alone, each of the following synthetic placements, in `meta` or as a
sibling, would pass both the walk and the binder and return 0:
- `{"isError": true}`, `{"success": false}`, `{"OK": false}`
- `{"exitCode": 1}`, `{"returncode": 1}`, and `{"exit": 1}`. `exit` is the key this round's own
  `*.run.json` schema uses; for example `decode-invalid-decoder.run.json` has `exit: 1`.
- `{"status": "timeout" | "cancelled" | "partial" | "unavailable" | "ERROR"}`, and `{"code": 1}`
  (numeric code)
- falsy refusal payloads such as `{"error": {}}`, `{"error": ""}`, `{"errors": {}}`
- refusals in **serialized JSON strings**, for example `"raw_result": "{\"ok\":false}"`. Strings are
  opaque to the walk.
- refusals carried in dict **keys**, for example `{"execution_failure": {...}}`, or in **prose**
  under `diagnostics` or `limitations`.

What I checked at the candidate (my own read-only inventory of all 9 `*.envelope.json` under
`round-23/evidence/c1/`):
- Every credited envelope has `raw_result: null`.
- No string holds embedded JSON.
- No `status`, `exit` or `isError` keys occur, and `evidence_links: []`.
- The only refusal-shaped keys sit in the deliberately refused `decode-invalid-decoder.envelope.json`:
  `ok:false`, `error.code: execution_failure`, `error.details.diagnostics.exit_code: 1`. The walk
  catches that file through `ok`.

So the gap is a tradeoff of the vocabulary that R21 chose and R22/R23 reuse unchanged. It is not a
defect that changes the current count. The fixtures only inject in-vocabulary signals, so none of
these shapes has a negative fixture.

### F3 — One credited witness is a disclosed partial observation that the walk cannot see (observed; tradeoff, disclosed)
`inventory.envelope.json` (`ev_940cf7bb…`) is the **only** witness held for
`inspect-signal-decoders`; `uart-help` is cited but its id is not, so it does not bind. That
envelope is `ok:true`, but `data.normalized_result.diagnostics` is prose reporting
`srd: SyntaxError: Failed to load decoder signature … (pd.py, line 138)` and Python-prefix warnings.
The catalog has 110 decoders with no `signature` entry, and `output_window` reports
110/110/110 with `has_more:false`.

The walk cannot see this because it is prose; `r21.refused` docstring line 40 says "never arbitrary
quoted prose". The entry discloses it fully at
`corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md` lines 17–26 and does not claim
completeness. This is acceptable as "verb exercised". It would not be acceptable as "catalog
complete", and the prose does not claim that.

### F4 — Cross-file ancestry ("copy erases parent refusal") is not enforced by the counter (observed: counter design; observed: holds at candidate)
`count-c1.py` reads only the cited `*.json`. It never opens the sibling `*.run.json`, and its
`limit` string says "run stdout checked separately". My read-only parity check of all four
credited witnesses found:

| Witness | `run.exit` | `stderr` | Run stdout vs envelope |
| --- | --- | --- | --- |
| inventory | 0 | `""` | byte-equal |
| decode-official-uart | 0 | `""` | byte-equal |
| decode-uart-hi | 0 | `""` | byte-equal |
| inspect-dart-legacy-saber | 0 | `""` | byte-equal |

For the three uncredited `connect-dart-symbols` runs, the envelope sha256 equals the
self-asserted `stdout_sha256`. Run-level parity therefore rests on `describe-signals.py` and
`describe-dart.py` (the `signal-records` and `dart-record` controls, exit 0 at `6615aea`, not
re-run by this seat), not on the counter.

### F5 — Historical witnesses bypass `bind_new` (observed; not exploitable)
`count-c1.py:81` measures the R22 root with the legacy `r22.measure(root, BASELINE)`, so the
`identify-flutter-build` witnesses never pass through the all-envelope walk. Two guards make this
safe:
- `count-c1.py:67-68` pins the old root's tree to B.
- At B, both `identify-flutter-build-saber.envelope.json` and `identify-godot.envelope.json` have
  zero walk hits anywhere, including outside `data`.

The Godot witness has `flutter_detected:false, coverage:"complete"`. That is a negative
identification, and it is still one held verb, as the entry states.

### F6 — Local association, not authentication (observed)
Nothing in the counter, the binder or the helpers checks a producer signature, a recomputed
`evidence_id` derivation, or custody. The envelope, the `run.json` and `stdout_sha256` are all
written by the same author. A hand-written `ok:true` envelope with matching `meta.command`,
`operation` and id, plus an eligible S058+ row, would count. This matches what the claim declares:
`claims.json` `not_claimed` includes "authentication" and "independent non-author admission", and
the counter's `limit` says "no authentication".

Candidate prose does not overclaim. The 2838351 changes to LOG.md, SCORECARD.md and the
round-23 lesson say "not Evidence authentication or outside admission" and "author-side verdicts
do not certify outside admission".

### F7 — Stale knowledge line (observed; calibration, outside walk scope)
`corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md:117` (last changed in `2b40aec`) says
"Dart parsing and both debugger verbs remain unheld". At 2838351 the counter holds
`inspect-dart-aot` through `inspect-dart-legacy-saber.envelope.json` (`after-c1.json`
`t1_exercised`). This does not affect the count, but it contradicts the claimed 4/6.

## Counterexample, impacted axes, smallest safe correction
- **Strongest counterexample:** an `ok:true` envelope whose refusal sits in `meta` as
  `{"exit": 1}`, `{"isError": true}`, or a serialized JSON string. It binds with exit 0 per
  `r21.py:39-55` plus `count-c1.py:43-54`. No candidate envelope has this shape (F2), so k=4 is
  unaffected.
- **Impacted axes:** calibration (counter fidelity, and F7), coverage (only if future envelopes take
  those shapes). Depth: none.
- **Smallest safe correction (author-side, L1's call):**
  - Keep R21's pinned vocabulary, since changing it would change the reviewed digest. In
    `bind_new` only, also reject `isError is True`, `success is False`, and a non-zero or non-int
    `exit`/`exitCode`/`returncode`.
  - Fail as unevaluable (2) on any string value that decodes as a JSON object or array.
  - Add one negative fixture per shape to the frozen manifest. That requires a new manifest digest.
  - Fix the wording at line 117 by appending a dated correction rather than rewriting the line.
  - Otherwise, record F2 as an accepted tradeoff in the round's limits.

## Produced files and hashes
- `.ufo/waves/round-23/w2/CriticOriginal.md` (this report; sha256 is reported in the final handoff,
  since the file cannot contain its own hash).
- Scratch in `.ufo/waves/round-23/runtime/CriticOriginal/` was removed after use. It held
  read-only extracted copies of `count-c1.py`, `r22.py`, `r21.py` and `r20.py` (sha256 matched the
  pins `f4b8d16a…`, `c925918f…`, `61536938…`, `cfbf1880…`) and three inventory/parity scripts that
  only parsed git blobs.

## Commands run
All exited 0:
- `git show`, `git log`, `git diff --stat`, `git ls-tree` against 2838351 and B
- `python3 -I -B` on three read-only blob-inventory scripts (`inventory.py`, `parity.py`,
  `historical.py`); none imported or executed the counter

## Installs
None.

## Open risks
- F2 vocabulary gaps have no negative fixtures, so they are unproven either way for future
  envelope shapes.
- The run-parity controls (F4) were not re-run by this seat. The counter alone does not enforce
  them.
- Authentication and outside admission remain unclaimed and unverified (F6).
- The count is verified only at the named commit; this seat did not run the counter.
