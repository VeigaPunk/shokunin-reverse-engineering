# ExecFreezeGate — freeze-order gate for round 28

Seat: KaidokuR28a2.ExecFreezeGate. Read-only lane; all work in a sandbox clone
`/fast/scratch/hyaku/kaidoku-r28/seats/a2w/ExecFreezeGate/clone` (rev 9db24c9e10287d44d9f780d782ab608f3c84ff5a, clone of lane tip). Run 2026-10-22T18:30Z.

## Verdict

Freeze ORDER holds for both round-28 freezes (observation, from commit times below).
The round-24 gate itself FLAGS round-28 under its own rules — two schema-evolution
findings, neither is an ordering violation. `claims-c2.json` is outside the gate's
audit surface entirely (its filename fails the gate's `claims\.json$` regex), so the
ordering table below is the only check applied to C2.

## Commands and output

1. `git clone -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin .../clone` → exit 0.
2. `python3 -I -B .ufo/waves/round-24/tools/freeze-gate.py --root . --rev HEAD --require-clean round-28`
   → exit 1. Audited 15 freezes; `required_failed: ["round-28"]`. Full JSON saved
   (artifact below). Round-28 freeze entry:

   ```
   "claims_file": ".ufo/waves/round-28/claims.json",
   "freeze": "87d3dfb65fec4b636664bd5727822feba5d35317",
   "findings": [
     {"finding": "INSTRUMENT_UNRESOLVED", "name": "select-heldout.py"},
     {"finding": "INSTRUMENT_UNPINNED",  "path": "tools/round-28/collect-c1.py"}],
   "verdict": "FLAGGED"
   ```

3. `git log --diff-filter=A --format='%cI %H' --reverse -- <path>` per row below → exit 0.
4. `git show <freeze>:<counter> | sha256sum` → both recorded pins equal freeze blobs
   (c1 `29c2b571…27c` match yes; c2 `4fdf7db8…0ef` match yes).

## First-commit table (UTC; -03:00 local stamps converted)

| Claim | Instrument / input | First commit (UTC) | Commit | First data commit (UTC) | Order |
|---|---|---|---|---|---|
| R28-C1 | claims.json (freeze) | 17:17:16 | 87d3dfb65fec | — | — |
| R28-C1 | tools/round-28/c1-heldout-naming.py | 17:17:16 | 87d3dfb65fec | runs.tsv/envelopes 17:22:32 (ca4069a4); db/ and tally.json 17:25:49 (cb8d495e) | PASS |
| R28-C1 | tools/round-28/select-heldout.py (producer) | 17:17:16 | 87d3dfb65fec | same as above | PASS |
| R28-C1 | tools/round-28/collect-c1.py (producer) | 17:17:16 | 87d3dfb65fec | same as above | PASS |
| R28-C1 | tools/round-25/a2/resolve-selectors.py (loaded) | 09:31:23 | 08c7a7299ed6 | same as above | PASS |
| R28-C1 | carriers.tsv, heldout.tsv (frozen inputs) | 17:17:16 | 87d3dfb65fec | same as above | PASS |
| R28-C2 | claims-c2.json (freeze) | 17:21:55 | 86fa8526aeaf | — | — |
| R28-C2 | tools/round-28/c2-filtered-flag.py | 17:21:55 | 86fa8526aeaf | db/ 17:45:05 (a2673116) | PASS |
| R28-C2 | tools/round-28/collect-c2.py (producer) | 17:21:55 | 86fa8526aeaf | db/ 17:45:05 (a2673116) | PASS |
| R28-C2 | selectors.tsv, canonical-signatures.json (inputs) | 17:21:55 | 86fa8526aeaf | db/ 17:45:05 (a2673116) | PASS |

Every counted data path was first committed after its freeze commit: C1 data at
ca4069a4 and cb8d495e postdate 87d3dfb6; C2 data at a2673116 postdates 86fa8526.

## Findings (labels)

- Observation: the gate's FLAGGED verdict on round-28 is a pin-schema mismatch, not
  an order defect — the round-28 file pins producers under `producers_not_counters`
  and frozen inputs under `loaded_by_counter`, keys the round-24 gate never reads;
  `select-heldout.py` is cited by bare filename inside a claim string
  (`...paired by the frozen pairing rule in select-heldout.py...`), which the gate
  scores INSTRUMENT_UNRESOLVED.
- Observation: `claims-c2.json` is invisible to the gate (regex requires basename
  `claims.json`); C2's instrument pin, freeze commit and ordering were verified by
  the direct checks above instead.
- Observation: both recorded instrument pins match the blobs at their freeze commits.
- Observation: no committed instrument was revised after its freeze (no INSTRUMENT_REVISED
  finding for round-28; `git rev-list freeze..HEAD -- <counter>` returned 0 for both).
- Unknown: whether the L1 wants the round-24 gate ported to the multi-key pin schema or
  accepts this direct commit-time audit for round 28.

## Artifacts (sha256)

- gate-out.json `5ed56a93533d862f6eb283244ad18b67d26a051210248371029b41b2616d4fe0` —
  full gate JSON at `/fast/scratch/hyaku/kaidoku-r28/seats/a2w/ExecFreezeGate/gate-out.json`
- clone/ — sandbox clone at rev 9db24c9e (directory, not hashed)

## Tooling

No installs; system python3 and git sufficed.

Report: .ufo/waves/round-28/a2w/ExecFreezeGate.md
