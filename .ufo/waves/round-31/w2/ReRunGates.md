# ReRunGates — round-31 freeze/axis gates re-run at tip

Seat: `KaidokuR31.ReRunGates` (wave 2). Date: 2026-10-23. Lane rev re-checked: `1288285eed81395e6af7c279a173b117b2c2eaa3` (= `git rev-parse HEAD` of the lane, 2026-10-23T04:31Z).

All commands ran read-only against the lane; no lane files modified, no installs performed (no tool installs were needed: `python3` + read-only `git`). No scripts/drafts beyond the three raw-output files listed below.

## Checked items

### 1. freeze-integrity gate — verdict: holds
Command:
`python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-31/freeze-integrity.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --round 31 --rev 1288285eed81395e6af7c279a173b117b2c2eaa3`
(run at 2026-10-23T04:31:07Z, `timeout 300`, exit `0`)

Excerpt (full stdout, 7 lines):
```
ok	corpus/evidence/round-31/c1/carriers.tsv	sha=46f180b837b7	commits_after_freeze=0
ok	corpus/evidence/round-31/c2/predictions.tsv	sha=acac45e3a6f0	commits_after_freeze=0
ok	tools/round-31/c1-sqlite-positive.py	sha=048020881b0a	commits_after_freeze=0
ok	tools/round-31/c2-sqlite-refusals.py	sha=d23948959835	commits_after_freeze=0
ok	tools/round-31/sqlite_oracle.py	sha=aefd8639383b	commits_after_freeze=0
freeze-integrity: CLEAN pins=5 freeze=35ba7c522dba rev=1288285eed81395e6af7c279a173b117b2c2eaa3
EXIT=0
```
Observation: all 5 frozen pins present with expected hashes and 0 commits after freeze; CLEAN; exit 0.

### 2. prefreeze-gate — verdict: holds
Command:
`python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/prefreeze-gate.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --round 31 --rev 1288285eed81395e6af7c279a173b117b2c2eaa3`
(run at 2026-10-23T04:31:07Z, `timeout 300`, exit `0`)

Excerpt (full stdout):
```
prefreeze round=round-31 freeze=35ba7c522dba55f9be27eb161d4254eacaa24330 rev=1288285eed81395e6af7c279a173b117b2c2eaa3 claims=.ufo/waves/round-31/claims.json
pins=5 present=5 unhashed=0 mismatch=0 data_before_freeze=0 tools_named=2 tools_unpinned=0 findings=0
verdict=CLEAN
EXIT=0
```
Observation: no unhashed/mismatched pins, no data before freeze, both named tools pinned; CLEAN; exit 0.

### 3. axis-fit-gate — verdict: holds
Command:
`python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/axis-fit-gate.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --round 31 --rev 1288285eed81395e6af7c279a173b117b2c2eaa3`
(run at 2026-10-23T04:31:07Z, `timeout 300`, exit `0`)

Excerpt (JSON single line, key fields):
```
"axis_claims": [{"axis": "coverage", "claim": "R31-C1", "controls_present": {"all-false (committed refusal envelopes for C1; all-accept for C2)": "head", "do-nothing": "exact", "junk-row (entry + PROVINCE/SKILL rows without envelopes)": "head", "no-reader (envelopes fabricated from the oracle or the predictions, never produced by REA)": "head", "shortcut keyed on ids/labels (another carrier's or request's envelope under the id)": "head"}, "surface": "ok", "unmoved_command": "ok"}, {"axis": "depth", "claim": "R31-C2", ...same controls..."}],
"findings": [], "notes": [],
"receipts": {"ancestor_of_first_envelope": true, "first_add": {"commit": "7474d26951ea03bb73f59050fa1fb77ee0d3e36b", "committer_ct": 1792729127}, "first_envelope_add": {"commit": "f368a101277ab9c4ddff428db739a734efb5c280", "committer_ct": 1792729175, "path": "corpus/evidence/round-31/c1/envelopes/chinook-autoinc.json"}, "ordering": "earlier", "path": ".ufo/waves/round-31/controls/receipts.tsv", "present": true, "rows": 10},
"verdict": "PASS"
EXIT=0
```
Observation: both axis claims report required controls present, surfaces ok, unmoved command ok; receipts block shows receipts.tsv (`7474d269`) added before the first envelope (`f368a101`, `ancestor_of_first_envelope: true`, `ordering: earlier`); verdict PASS; exit 0.

### 4. Ordering claim (envelopes later than receipts.tsv) — verdict: holds
Commands (read-only `git log --diff-filter=A`):
```
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin log --diff-filter=A --name-only --format='%H %cI' -- corpus/evidence/round-31/
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin log --diff-filter=A --format='%H %cI' -- .ufo/waves/round-31/controls/receipts.tsv
```
(run at 2026-10-23T04:31Z, exit 0)

Findings:
- Exactly one commit adds paths under `corpus/evidence/round-31/*/envelopes`: `f368a101277ab9c4ddff428db739a734efb5c280` at **2026-10-23T01:19:35-03:00** (adds all c1 and c2 envelope files + `runs.tsv`; first listed path `.../c1/envelopes/chinook-autoinc.json`).
- `corpus/evidence/round-31` files `carriers.tsv`/`predictions.tsv` (plus pypi sources) were added at the freeze commit `35ba7c522dba55f9be27eb161d4254eacaa24330` (2026-10-23T01:05:07-03:00), i.e. before both.
- `.ufo/waves/round-31/controls/receipts.tsv` added at `7474d26951ea03bb73f59050fa1fb77ee0d3e36b` at **2026-10-23T01:18:47-03:00**.
- 01:19:35 > 01:18:47 → the first commit adding any envelope path is later than the commit adding receipts.tsv. **Claim holds.** Consistent with the axis-fit gate receipt (`committer_ct` 1792729175 > 1792729127).

Note (method transparency): the narrower pathspec `'corpus/evidence/round-31/*/envelopes'` returns **empty** with `--diff-filter=A` because git pathspecs match the directory prefix, not the files beneath it (only the envelope dir's file paths are added). This first empty result was a pathspec artifact, not evidence of absence; the full listing above is the authoritative check.

## Residual risk / verification gaps
- The gates run read-only at the tip and certify the frozen claims/control state; they do not re-run the live C1/C2 counters (that is the L1's `after/` measurement, unchanged at 0007731e per context). This seat did not re-measure `carriers=12 pass=12` / `requests=23 matches=23`.
- Ordering was checked on the lane's default branch history only (the only history the lane exposes). No other gaps.

## Artifacts (seat dir `/fast/scratch/hyaku/kaidoku-r31/seats/w2/ReRunGates/`)
| file | sha256 |
|---|---|
| freeze-integrity.out | 4ca3efc9cf42712850d7a86a9c50badede01c96c176181b6fc340fc2ea058c87 |
| prefreeze.out | 65238bd99fcf5bcb964ee6c634f62651b11c888bdb508c89b76ddd90c05fa90e |
| axis-fit.out | 94bf5c2e803f6827530eb9c361ef72017fe06edadc6d54cdfa34acb8a870a126 |

(`tmp/` subdir also created under the seat dir; empty of artifacts.)
