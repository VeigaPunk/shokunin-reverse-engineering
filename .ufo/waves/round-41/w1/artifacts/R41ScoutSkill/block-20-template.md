- **SquashFS `extract-firmware` outcome triage v3 (round 41).** Table v3 reads the
  eight fields of rule block 19 and labels combined gap sets
  (`corpus/knowledge/2026-10-26-r41-sqfs-triage-v3.md:<A1>-<B1>`). <one sentence per
  repaired defect, each with its own citation:> R40-CL5's `escaping-symlink-removed`
  absorption of combined sets, the new `depth-limited-nested` label
  (`corpus/knowledge/2026-10-26-r41-sqfs-triage-v3.md:<A2>-<B2>`), the first-match
  precedence text the held-out labels are written from
  (`corpus/knowledge/2026-10-26-r41-sqfs-triage-v3.md:<A3>-<B3>`). Superseded for routing by
  nothing yet; table v2 (rule block 19) stays as the round-40 record. Scored on a
  held-out set seeded by the round-41 freeze, expected labels from a frozen independent
  evaluator, with the limits in
  `corpus/knowledge/2026-10-26-r41-sqfs-triage-v3.md:<A4>-<B4>` (interpreter
  `tools/round-41/sqfs-triage-v3.py`).

  <!-- sqfs-triage-table v3 -->
  <!-- sqfs-triage-actions: none inspect-input ... depth-limit-note -->
  | label | operation | provider | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | action | cause | source |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | <row 1> | ... |
