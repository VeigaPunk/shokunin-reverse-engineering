# R43W2C1Lookup — C1 union and lookup falsification

## Outcome

**No falsifier found for this assigned surface.** At measured score revision `77d196c66f4fea00d7d543728b190ebdfaf6d0f0` (C1 score receipt), recomputation from the frozen round-42 dev-arm named-class declared tuples and the round-43 held-out combo envelope observed tuples gives 39 distinct union tuples, 21 unseen of 24, and threshold 12. This matches the C1 receipt exactly. The frozen lookup control independently scores 19/24, `below_half: false`; it is reported and not bound. Its bytes match the freeze.

Lane tip read: `5856614ac4bf7f2363bbcd1956644474a82108e5`. The C1 receipt's `revision` is `77d196c66f4fea00d7d543728b190ebdfaf6d0f0`; the receipt's counter exit is 0. I verified the dev manifest, round-43 held-out manifest and lookup control blobs at that measured revision have the same SHA-256 as the checked-out lane tip. This report's attack is specifically against the C1 union/lookup clauses, not a new scoring run of all C1 predicates at the later tip.

## Recomputed union and threshold

Following P43-C1's defined source and six-field tuple, the standalone script in `artifacts/R43W2C1Lookup/recompute_union.py` reads the committed `corpus/evidence/round-42/c2/dev/manifest.json`, skips `class == combo`, canonicalizes each `declared_features`, then reads each held-out combo's `envelope.json` and derives its observed tuple from envelope contents. It does not use round-43's own named-class tuples as the union. A separate reference cross-check against the frozen counter's `declared_features`, `observed_features`, and `REQUIRED_FEATURES` returned the same union and lists.

- Dev manifest: 78 carriers; 54 named-class carriers yielded 39 distinct tuples. No non-combo carrier canonicalized to `None` (including out-of-domain carriers); 24 combo carriers skipped for the union.
- Held-out: 24 combo IDs C01–C24; observed tuples available for all 24 (none skipped).
- Unseen: 21 IDs: C01, C02, C04, C05, C06, C07, C08, C09, C10, C12, C13, C14, C15, C16, C17, C18, C19, C21, C22, C23, C24.
- Seen: C03, C11, C20.
- `ceil(24/2) = 12`; counter expression `(24 + 1) // 2` is also 12. `21 >= 12`, so the binding is true with a margin of 9. There is no denominator omission or threshold/count discrepancy.
- Receipt says source `corpus/evidence/round-42/c2/dev/manifest.json (carriers[].declared_features)`, `dev_named_tuples: 39`, `n_combos: 24`, `need: 12`, and the identical unseen/seen lists. The held-out manifest's declarative `combo_unseen.declared_outside_ids` also has the same IDs; the binding itself is independently recomputed from observed envelope tuples, not accepted from that manifest field.

## Lookup score and binding status

I ran the frozen evaluator and interpreter directly over copies of the 24 committed combo envelope files in scratch, then compared each `(label, action)` by carrier ID:

- Evaluator: 24 results, no skipped IDs. Interpreter: 24 results. Match: 19/24; mismatches exactly C05, C09, C17, C21, C23. The matched ID set equals the receipt's `lookup.scored_ids`.
- The committed C1 receipt reports `n_combos: 24`, `score: 19`, `below_half: false`, `binding: false`, no missing expected outputs, and `identical_to_freeze: true`.
- The receipt's binding keys containing “lookup”/“half” are only `lookup_control_identical`; there is no score/below-half binding. In `c1-counter.py`, `lookup_below_half` is written only into `res['lookup']`; final success is computed from the separate binding dictionary (`all(v is True for v in b.values())`). Thus the lookup score is reported, not bound. This correctly avoids imposing an unreachable `< half` target on the frozen lookup control.
- Raw lookup-control SHA-256 at freeze and at lane tip is `7f193c8fdea23e2410909b7b6d6da6965f66e58052e6d576db2dc83429f4304f`; `git log` found no touch to that path in FREEZE..tip, and the blob at the measured C1 revision has the same digest.

## Evidence, revisions, commands

The frozen plan was read first. Principal source hashes and hashes for every C01–C24 envelope are recorded in `artifacts/R43W2C1Lookup/read-input-sha256.txt` (that file SHA-256: `4d289efc2d05373b89bfcb1cbc2c02907db695bf7d0a12ab4157b17a3c38a304`). Principal hashes: plan `0326dff974d48df575486256dbd5a0b36593dbc84155d0d40560b64d3c20d83e`; counter `3a23e93ee95f4b0d69a2f4d03ed2592c9f0b81dbb6188cb6818a18a8f4f33c79`; round-42 dev manifest `ba3d73876cbe953619a66ed603d2622a741b90ffc6d7d1f9756986c3db388d17`; round-43 held-out manifest `980eafa59ca3890bf45945a02a6e608da511435d972d1ec978a38fd068ef2555`; C1 score `13a495dbb6862d6cfbdd1f41e4a09460740f86bf93e8bb08e313b06d92b8a55c`; C1 controls summary `143d4c38412c8d4af785243ffdabc5e8735d0237818643ce1bb151e4db624e5d`; round-42 C2 stop receipt `0b4e6026e1d92f3d4a5e4c73da6a0ee4574998fc40d58edbd5ca8ab9997f21eb`.

Commands (run from lane root unless stated):

1. `git rev-parse HEAD` → `5856614ac4bf7f2363bbcd1956644474a82108e5`; `git merge-base --is-ancestor f3f8db389416d094b1ddeb1215ddcf914bfc0d1c HEAD` → exit 0. Freeze is an ancestor.
2. `python3 -I -B <scratch>/recompute_union.py` → exit 0. Output retained as `artifacts/R43W2C1Lookup/recompute_union.out`; key output is `distinct named union tuples: 39`, `unseen n=21`, `seen n=3`, `skipped (obs None): []`, `need (ceil(n/2)): 12 binding ... True`, with all three reference comparisons true.
3. `python3 -I -B tools/round-42/indep-eval-v4.py --envelopes <scratch>/combo-env` → exit 0; JSON output retained as `artifacts/R43W2C1Lookup/eval.json`.
4. `python3 -I -B tools/round-42/sqfs-triage-v4.py --skill .ufo/waves/round-42/controls/c2/CTL-C2-7-lookup.md --json <scratch>/combo-env/*.json` → exit 0; JSON output retained as `artifacts/R43W2C1Lookup/lookup.json`.
5. Score comparison from those JSON outputs → 24 expected, 24 interpreted, 19 matched, 5 mismatches, `below_half false`; retained summary `artifacts/R43W2C1Lookup/lookup-score.json`.
6. Initial evaluator attempt `... indep-eval-v4.py --envelopes <scratch>/combo-env --json` → exit 2, CLI usage error (`--json` unsupported); rerun with supported `--envelopes DIR` form above succeeded. Error retained as empty/failed-attempt capture `artifacts/R43W2C1Lookup/eval.err` (the stderr from the successful invocation is empty).
7. `git diff --quiet FREEZE..HEAD --` on dev manifest, fixtures, both frozen round-42 tools, C1 counter and lookup control → exit 0. The lookup control's `git log FREEZE..HEAD -- <path>` produced no rows; freeze and tip `git show ... | sha256sum` both gave the digest above.

C1 control receipt context: `.ufo/waves/round-43/controls/c1/summary.json` says `ok: true`, `errors: []`, `kill_rule_fires: false`. I also read both C2 score receipts, without extending this assigned attack to C2: at `77d196c66f4fea00d7d543728b190ebdfaf6d0f0` and `09ab56b8fdc2efcc3b58b203644537d84dd5ac9e`, each C2 receipt has exit 1 and `checks.sources_numstat_three_additions: false`, while its gate and copy-audit exits are 0 and `rows_failed` is empty. This is an observed C2 stop, not a conclusion about the union/lookup attack. Round-42 lookup receipt records its own 19/24, `below_half: false`, `binding: false` result.

## Scope, axes, limits

- Impacted axes: **coverage** (anti-enumeration witness/count) and **calibration** (reported lookup behavior versus binding); no direct depth-axis claim is tested here.
- No correction is indicated by this attack. The union source, tuple measurement, threshold, score, and reported-not-bound status agree with the frozen predicate and committed C1 receipt.
- `[INFERENCE]` The held-out manifest contains `named_tuple_union_sha256: da11f0ef…`; two straightforward candidate serializations of the independently reconstructed union did not reproduce that digest. The frozen predicate and counter bind the actual tuple union/count rather than this manifest hash, so I found no evidence that this hash mismatch is a predicate failure; its serialization contract was not established in this attack.
- No REA, unblob, sasquatch, or extractor was run; only committed envelope JSON was read and frozen labeling/evaluation tools were invoked. No repo-wide tests, formatters, or linters were run. No tool installation, VCS mutation, or production edit was performed. Scratch was `/fast/scratch/hyaku/kaidoku-r43/w2/R43W2C1Lookup/` and was removed before yield. Disk check before probes: `df -h /fast/scratch` reported 314G available.

Report: .ufo/waves/round-43/w2/R43W2C1Lookup.md
Artifacts: .ufo/waves/round-43/w2/artifacts/R43W2C1Lookup/
