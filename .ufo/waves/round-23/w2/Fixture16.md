# Fixture16 — `meta_array` case review (R23-C1, source-review only)

Scope: `.ufo/waves/round-23/frozen/expected-v2.json` case `meta_array`,
`.ufo/waves/round-23/frozen/fixture.json`, and the `meta_array` branch of
`.ufo/waves/round-23/tools/counter-fixtures.py`, all read at candidate
`2838351450ff1ee4baa620c962a1153450d53311` via `git show`. No suite execution.

## Verdict

**Valid discriminator; expectations correct.** `meta_array` is the sole case in
the manifest that forces the list-descent branch of the counter's refusal walk.
No wrong expectation; one narrow residual gap noted below.

## Trace (observed)

- Fixture template (fixture.json:56-68): `inspect-signal-decoders` envelope is
  `{"ok": true, "meta": {"command": "inspect-signal-decoders"}, "data": {...,
  "operation": "inspect_signal_decoders", "normalized_result": {"control": ...}}}`.
- Mutation (counter-fixtures.py:60-61):
  `envelope['meta']['raw_result'] = [{'ok': False}]`, applied before
  `raw = json.dumps(envelope)` (line 66), so the serialized blob carries the
  mutation. `ok`, `meta.command`, `data.operation`, `data.evidence_id` all stay
  binding-valid — refusal is only inside a JSON array.
- Counter path (tools/count-c1.py:42-53, `bind_new`): whole-envelope iterative
  walk; `isinstance(node, list)` → `pending.extend(node)` (lines 48-49) descends
  the array, reaches `{'ok': False}`, `'ok' in node and node['ok'] is not True`
  → returns 1 (reject).
- Why this is the only coverage of that branch: the reused legacy binder
  `bind_cli` (round-22/tools/count-c1.py:69-100, sha256
  `c925918f…b1879`, digest pinned by count-c1.py `LEGACY_SHA256`) deep-walks
  **only `data`** (pending seeded `[record]`, line ~86). For `meta` it calls only
  `r21.refused(meta)` (line 79); `refused` recurses into `raw_result` values only
  when they are dicts (round-21 verb-coverage.py:52-54, `refused(node.get(key))`
  returns False for a list). So `bind_cli` alone **accepts** this envelope →
  a counter lacking list descent or meta descent yields `count 2 / exit 0 /
  c1_complete` and the case fails loudly. Sibling cases partition the space:
  `meta_false` (dict-level `ok:false` in `meta`), `nested_refusal` (dict inside
  `data`, already caught by legacy `bind_cli`), `sibling_refusal` (top-level
  sibling `result.errors`). `meta_array` uniquely isolates list descent.

## Expected values — correct (observed)

- `expected-v2.json:83-87`: `{exit:1, count:1, finding:"c1_incomplete"}`.
- count: rejected new envelope adds nothing; only historical
  `identify-flutter-build` remains → `t1_exercised_count = 1`.
- exit: count-c1.py `code = 0 if count==6 else 1` → 1.
- finding: `c1_incomplete` (count<6, no exception).
- Robustness: any `ValueError/RecursionError` inside `bind_new` → return 2 →
  still rejected → same triple. Uncaught `TypeError`/`AttributeError` → no JSON
  on stdout → harness records `{exit:N, count:null, finding:null}` ≠ expected →
  fails. Expectation is fail-closed in both directions.
- Pin integrity at candidate (observed sha256):
  `counter-fixtures.py` `f2990b35…e1a97f`, `fixture.json` `a1f5aff8…bfef4b` —
  both match `expected-v2.json.inputs`; `expected-v2.json` itself `458b30d5…`
  matches `SELFTEST_MANIFEST_SHA256` in count-c1.py:23.

## Positive-preserving (observed)

- Mutation is a structural refusal marker, not a shape corruption: envelope stays
  a dict with valid `ok`/`data`; positive and `all_six` templates are unmutated
  and must still bind (count 2 / count 6). The case checks refusal propagation,
  not tolerance for malformed JSON — correct for the claim's "copy erases parent
  refusal"/"refusal counted" falsifiers.
- Oracle independence: `counter-fixtures.py` imports stdlib only
  (copy/json/os/pathlib/subprocess/sys/tempfile); expectations are static
  literals in the digest-pinned manifest; the counter is invoked as a black-box
  subprocess (`sys.executable -I -B count-c1.py --root repo --rev rev`,
  line 106). No decision-code import — independence holds.

## Residual weakness (low)

1. **Single refusal marker per slot.** The array contains only `{'ok': False}`.
   An array-wrapped `{'errors': [...]}` or `{'exit_code': 1}` under `meta` is
   unprobed; a hypothetical binder that descends lists but forgets `refused()`
   on list elements would pass all 21 cases. Same shape applies to every case —
   each probes one marker. Not a wrong expectation.
2. **No benign-list-in-meta positive.** An over-strict binder that rejects any
   list under `meta` passes `meta_array` and every other case, because no
   template has a legitimate array inside `meta` (real envelopes do — e.g. list
   values inside `meta` subfields). `positive`/`all_six` don't cover this axis.
   Minor; the same blind spot exists for benign dicts carrying an `ok` key.
3. Note: `meta_array` shares its oracle triple with 13 other cases — it can
   distinguish the fault class but not the exact rejection clause (return 1 vs
   2 collapse to the same observable). Acceptable for a count-based oracle.

## Produced files

- `.ufo/waves/round-23/w2/Fixture16.md` (this report).

## Installs

None. Read-only wave; no pacman/uv/cargo/npm transactions.

## Open risks

- `count-c1.py` itself is not digest-pinned by the selftest (only manifest +
  helper + fixture are); a weakened `bind_new` is caught by these cases, but a
  same-commit weakening plus expectation edit would be a collusion, not a
  detectable tamper — inherent to the self-pinning design, out of case scope.
- Suite not executed per assignment; all traces are source-derived. Observed:
  file bytes, digests, control flow. Inferred: runtime subprocess outputs.
