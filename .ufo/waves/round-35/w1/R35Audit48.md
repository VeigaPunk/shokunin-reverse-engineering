# R35Audit48 — mutation probe report (wave 1, seat)

Seat: R35Audit48 | Role: UFO-FSD mutation tester | Scope: audit trend evidence limits
Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
Probe assignment: challenge one claimed invariant of the frozen round-35 counters with one
plausible defect. Lane read-only; all probed artifacts in private `/tmp` scratch.

## Claimed invariant probed
Frozen claim C2, D-1 ("round-35 census-start receipt … carries the base count (rows=106,
EXIT=0, 9 W04 warnings)"), as enforced by `tools/round-35/c2-calibration-counter.py`
(instrument sha `576c14dd95c0a54b2de05b765d171b25429a893289b85516258e83daa9179b94`).
Counter check: D1_census_content_missing (unanchored substring tests `"rows=106"`,
`"EXIT=0"`, `"W04"` over the census bytes).

## Plausible defect (mutation)
Census row count corrupted `106 -> 1060` (e.g., keystroke/merger slip). All other
D-1 conditions held (census commit precedes first corpus/SOURCES.md change; same commit
topology and dates as the pristine fixture). Only the census file bytes differ.

## Detector (same bounded behavioral detector on pristine / mutated / restored bytes)
`python3 -I -B tools/round-35/c2-calibration-counter.py --root <scratch> --base <BASE>
--rev <REV> --freeze <FREEZE> --json-out <receipt>` on three scratch repos with identical
topology (commit1 = full green corpus + census; commit2 = corpus/SOURCES.md change):
- pristine: census `… rows=106\nEXIT=0\n9 W04 warnings …` (mirrors real
  `.ufo/waves/round-35/assimilation/census-start.txt` line layout)
- mutant: census with `rows=1060`
- restored: exact byte copy of pristine

## Outputs (detector results)
| stage | exit | stdout | receipt.failing | receipt.pass | census sha256 |
|---|---|---|---|---|---|
| pristine | 0 | `C2_CLEAN revision=2e99cf50…` | [] | true | `1e238089…78405` |
| mutant (rows=1060) | 0 | `C2_CLEAN revision=60aec366…` | [] | true | `bbd6fa87…d3d` |
| restored | 0 | `C2_CLEAN revision=2e99cf50…` | [] | true | `1e238089…78405` |

Behavioral equivalence of mutant vs pristine (rc, failing, pass): identical →
**mutant SURVIVED**; the detector does not distinguish the inflated census from the
claimed one. `'rows=106' in 'rows=1060'` is True — the defect is invisible to the check.

## Verdict
SURVIVED (coverage finding, not a contract change). Evidence limit established: the D-1
content check enforces substring presence, not the claim values:
- any row count whose decimal representation starts with `106` (1060, 10600, …) passes;
- any exit token starting `EXIT=0` passes (`EXIT=0x`, `EXIT=00`…);
- any string containing `W04` passes (so "10 W04 warnings" also passes);
exact base-count equality (rows=106, EXIT=0, 9 W04) cannot be falsified by this counter.
Same family, static inspection only (not probed, single-probe stop): C1
`registry_opened_not_this_round` uses `startswith("2026-10-25")` → `2026-10-250` would
pass; C1/C2 citation regexes accept the row id anywhere after `source:` on that line.
Counter read-only and untouched (sha256 at start == canonical instrument hashes in
`.ufo/waves/round-35/claims-canonical.json`: C1 `e28792c7…`, C2 `576c14dd…`).

## Restoration evidence
Restored census bytes sha256 == pristine sha256 (`1e238089…78405`); restored detector run
exit 0, failing=[] — byte-exact restoration. No lane file was ever modified (lane
`git status --porcelain` pre/post probe showed only pre-existing untracked w1 artifacts:
claims-canonical-note.md, w1-dispatch.json, w1-settle.json, w1-spec.json, w1.ready).

## Limits / commands
- No `find`/`du` under `/fast/scratch`; no subagents/background; no pacman; no VCS mutation.
- Detector command line (recorded above) run with `-I -B`; scratch under `/tmp/r35audit48b/`.
- Instrument/control not re-run on lane state; C2 do-nothing-at-base control untouched.
