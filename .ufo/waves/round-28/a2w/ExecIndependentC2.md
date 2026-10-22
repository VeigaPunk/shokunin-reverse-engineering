# ExecIndependentC2 - independent re-derivation of the R28-C2 numbers

## What this checks
Whether the four R28-C2 counts (responses_complete, entries, mismatches,
predicted_true) can be re-derived from the frozen inputs without the lane
counter `tools/round-28/c2-filtered-flag.py`. I wrote my own reader/predictor,
never importing or running the counter's logic.

Rule applied (from claims-c2.json / Sourcify 4byte `filterResponse`): a
candidate entry is predicted `filtered` exactly when its selector is a key of
the pinned `canonical-signatures.json` and the entry `name` differs from that
key's `signature` field. A canonical key with no `signature` field makes the
comparison `name != None`, always true; none of the five `system:magic`
placeholder keys occur among the 230 selectors, so this branch is never hit.

## Method (my own script)
- Script: `/fast/scratch/hyaku/kaidoku-r28/seats/a2w/ExecIndependentC2/independent_c2.py`
- sha256: `29461bdc6710a7af3dfa036f52860ee02b9e57a61a570c99211ac2a4e4b27fdb`
- Command: `python3 independent_c2.py`, run 2026-10-22T18:29Z, exit 0.
- Reads the lane working tree directly (not a pinned git rev):
  `corpus/evidence/round-28/c2/selectors.tsv` (230 selectors, all unique),
  `canonical-signatures.json` (36 keys), `db/openchain-<sel>.json` (230 files)
  plus `db/manifest.json` (230 rows, all status 200).
- Completeness gate: a response counts only if the manifest row has the exact
  expected URL (`...lookup?function=0x<sel>&filter=false`), status 200, and a
  sha256 equal to the file bytes; and the body parses with `ok: true` and holds
  the `0x<sel>` key in `result.function`. All 230 pass. (I do NOT check fetch
  time vs. counter commit or first-commit time - those need git, and my job is
  the arithmetic, not the freeze-order proof.)
- A response whose function value is `null` (48 selectors) or `[]` (0) is a
  valid answer with zero candidate entries.

## Counts (observation)
Command output, 2026-10-22T18:29Z, exit 0:
    responses=230/230 entries=246 mismatches=0 predicted_true=59
    canonical_selectors=10 entries_canonical=69 entries_not_canonical=177
    observed_filtered_true=59 observed_filtered_false=187
    target check: responses==230 entries==246 mismatches==0 predicted_true==59 -> True

Equal to 230/246/0/59: YES on all four. Independent derivation agrees with the
lane counter's committed result exactly.

## Entry-class detail (observation)
- 10 of the 230 selectors are canonical keys, all from the r25 set
  (`0x06fdde03`, `0x095ea7b3`, `0x18160ddd`, `0x23b872dd`, `0x313ce567`,
  `0x70a08231`, `0x8da5cb5b`, `0x95d89b41`, `0xa9059cbb`, `0xdd62ed3e`); zero
  held-out r28 selectors are canonical. Their responses carry 69 entries.
- The 220 non-canonical selectors carry 177 entries; every one is predicted and
  observed `filtered=false`. All 59 predicted/observed `filtered=true` entries
  sit under the 10 canonical selectors - the "name differs from canonical
  signature" branch.
- Structural checks: every one of the 246 entries has a boolean `filtered` and
  a `name`; every response holds exactly its own selector key and `ok: true`.
- The five `system:magic` canonical keys lacking a `signature` field never
  occur among the 230 selectors, so the always-true no-signature branch is
  untested here.

## Verdict
holds. My independent script reproduces 230/246/0/59 from the raw files with
zero code shared with the lane counter; the rule predicts every observed flag.
This confirms the C2 arithmetic only; `entry_ok` (knowledge-entry wording and
SOURCES/lesson gate) and the freeze-order checks are outside this item's scope
and were not re-derived.

## Artifacts
- `/fast/scratch/hyaku/kaidoku-r28/seats/a2w/ExecIndependentC2/independent_c2.py`
  sha256 `29461bdc6710a7af3dfa036f52860ee02b9e57a61a570c99211ac2a4e4b27fdb`
- No lane files written except this report; no installs; no network calls.
