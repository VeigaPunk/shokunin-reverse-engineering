# R21-C2 `index_mismatch_equal_kind`

**Axis:** depth (C2). This is a single frozen-case result, not a C2-wide verdict.

## Frozen contract

The fixture labels `index_mismatch_equal_kind` with expected exit **1** and predicts `kind: invalid_index`, `index: 9`; its extractor observation has the same kind and `index: 10` (`.ufo/waves/round-21/fixtures/battery.json:177-190`). The independently frozen contract also expects exit **1** because a different index at equal kind is a mismatch (`.ufo/waves/round-21/fixture-contract.json:26`). Thus the case tests detection of an index mismatch while kind remains equal.

## Single-case execution

Executed the actual successor `tools/compare-first-failure.py` directly. In an external temporary directory, I wrote the fixture prediction, an empty placeholder log, and an inert extractor stub that ignores the log and prints the fixture's frozen observation envelope verbatim. The comparator invoked only that stub; no analyzed carrier was executed. The temporary directory was removed after the run.

**Producing argv:**

```text
/usr/bin/python -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/compare-first-failure.py --prediction /tmp/kaidoku-r21-R21Attack19-doi662_r/prediction.json --log /tmp/kaidoku-r21-R21Attack19-doi662_r/log.txt --extractor /tmp/kaidoku-r21-R21Attack19-doi662_r/extractor.py
```

**Expected exit:** `1` (fixture and independent contract)  
**Observed exit:** `1`  
**stdout:** `{"finding": "failure_mismatch", "last_line": 8, "match": false, "observed": {"index": 10, "kind": "invalid_index", "phase": "analysis", "va": null}, "predicted": {"index": 9, "kind": "invalid_index", "phase": "analysis", "va": null}}\n`  
**stderr:** empty

The observed result is the declared mismatch: equal `kind`, differing `index`. This one case passed its frozen expected exit.

## Nearby counterexample (UNRUN)

`kind_mismatch_equal_index` is a nearby complementary negative: the fixture keeps `index: 9` equal while changing kind from `invalid_index` to `other`, with expected exit **1** (`fixtures/battery.json:161-174`; `fixture-contract.json:25`). It was not executed.

## Limits and verification gaps

Only this C2 case was executed; no other frozen cases, the full battery, or the nineteen-result R20 retrospective regression were run. This result does not establish the overall C2 claim or malformed-observation behavior. No carrier, provider, REA producer, or other runtime was used. The mounted tool inventory has no LSP device (`read xd://lsp` returned “No such tool”), so LSP status/references/definition/diagnostics were unavailable; the literal search used only to locate the fixture ID is not semantic evidence. No tools were installed or updated.

Report: `.ufo/waves/round-21/w2/R21Attack19.md`