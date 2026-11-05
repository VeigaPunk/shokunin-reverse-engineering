# MutationC1 — round 96 w1 report (mutate-run-revert, fresh mutants N1–N10)

Lane HEAD `3baac2ef4b9b2830d299125b8184ca06d9e6584d` (supersession of declaration
`e4d1f7de9deae83e6d5f78d2d7f0157196002af0`). Full table with hashes, receipts and per-mutant
detail: `.ufo/waves/round-96/w1/MutationC1/mutants.md` (SEAT). Diffs: SEAT `diffs/N1…N10`.
All runs used fresh `git clone --shared` copies under
`/fast/scratch/hyaku/kaidoku-r96/MutationC1` (one live clone at a time, discarded after each
mutant); the lane tree was never mutated; scratch removed at the end.

## Detector baseline (pristine, green — anchor for every verdict)

`python3 -I -B tools/round-96/kill-rule-v2.py --root . --work <s>/w-base --mutants
.ufo/waves/round-96/mutants.json --fixtures .ufo/waves/round-96/forgery --prefix forge
--expect 'repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12;
fresh-roundtrip 2 of 2' --json-out <s>/receipts/base-killrule.json` → **exit 0**, frozen
score label met, `identity_not_killed true`. Receipt: SEAT `receipts/base-killrule.json`.
(Note: `--expect` takes the battery FROZEN_LABEL, not the C1 score label; the score label is
the rule's own output. My first baseline used the wrong string and was red — pilot error,
superseded.)

## Verdicts

| mutant | file | verdict | decisive evidence |
|---|---|---|---|
| N1 resolve_rev hex-only again | stop-boundary-repair-battery-v6.py | **KILLED** | kill rule exit 1, honest K-dmain `pos` exit 1 (head=None → fail-closed `head-not-bound`); selftest green (blind). Clean receipts: `receipts/N1-killrule-clean.json` (rc 1), tree-level `receipts/N1-killrule.json` (rc 1, K-forgeries pin artifact adds red) |
| N2 count_problems bool rejection dropped | stop-boundary-repair-battery-v6.py | **SURVIVED** (coverage finding) | kill rule exit **0** with binding dropped (`receipts/N2-killrule-clean.json`); bool-count receipt refused on pristine (`counts-type:scored`) but **accepted** on mutant (`ok=True reasons=[]`) — `receipts/N2-boolprobe2.out`; no fixture/leg feeds bool counts |
| N3 verify_receipt met-False direction dropped | stop-boundary-repair-battery-v6.py | **KILLED** | selftest exit 1 (`verify-catches-met-lying: FAIL`); kill rule exit 1, `forge-met-lying` accepted (`receipts/N3-selftest.out`, `receipts/N3-killrule-clean.json`) |
| N4 main drops receipt["head"] | stop-boundary-repair-battery-v6.py | **KILLED** | kill rule exit 1, K-dmain `pos` exit 1; selftest green (blind) (`receipts/N4-killrule-clean.json`) |
| N5 c_fsync restore-before-count (count 0) | kill-rule-v2.py | **KILLED (meta, self-observed)** | mutated rule exit 1: own honest arm `K-fsync fsync_calls=0 ok=False` → `honest accepted 0 of 1` (`receipts/N5-killrule.json`) |
| N6 identity_not_killed forced True | kill-rule-v2.py | **SURVIVED in-suite; probe-only kill** | declared-mutant run exit 0 (`receipts/N6-killrule.json`). Killing-identity mutants file: pristine rule exit 1 (`identity_not_killed=false`) vs mutated rule exit **0** while its own receipt records M0 `killed=True` (`receipts/N6-probe-pristine.json`, `receipts/N6-probe-mutated.json`) |
| N7 probe write_receipt open(w) again | symlink-probe-v2.py | **SURVIVED in-suite (coverage finding)** | kill rule with `--probe` → mutant exit **0** (`receipts/N7-killrule.json`); planted-link demo: pristine leaves victim intact, mutant **clobbers the external victim** through a link at the probe's own `--json-out` (`receipts/N7-planted-link-demo.txt`; victim sha `297d0db4…` → `f5830127…`). First attempt was an invalid mutant (SyntaxError), discarded and redone |
| N8 c_probe consistency and→or | kill-rule-v2.py | **SURVIVED in-suite; unit-probe-only kill** | declared-mutant run exit 0 (`receipts/N8-killrule.json`); stub probe with lying receipt: pristine c_probe ok=False vs mutant ok=True (`receipts/N8-stubprobe-differential.txt`) |
| N9 schema=[] when counts is dict | stop-boundary-repair-battery-v6.py | **KILLED** | selftest exit 1 via `KeyError: 'fresh_scored'` (`receipts/N9-selftest.out`); kill rule crashes identically on `forge-unlabelled`, exit 1, no receipt (`receipts/N9-killrule-clean.stderr`) |
| N10 legacy rule counts M10 killed | legacy-kill-rule.py | **OBSERVED only by receipt-diff** | mutated rule: `r95-rule mutants killed 6 of 10`, M10 `killed=True` with `checks_all_ok=True` (forced), exit 1 (`receipts/N10-legacy.json`); committed `pre/c1-legacy-rule-at-base.json` (rule sha matches HEAD) records 5 of 10, survivors M10/M2/M3/M4/M6. No r96 instrument runs the legacy rule; exit code unchanged |

Score vs expectation: N1/N3/N4/N9 killed as expected; **N2 and N7 survived** (unobserved
bindings — bool-count schema, probe's own-receipt writer); N5 self-detected as predicted;
N6/N10 survive every in-suite leg and are caught only by the crafted probes recorded above.

## Incidental findings (fresh)

1. **cwd-dependent honest leg**: kill-rule-v2 passes a relative `--honest-dir` to the r95
   regression battery; the identical pristine command from a cwd outside the tree exits 1
   with only `r95-battery-regression` red (`receipts/cwd-artifact-demo.json`, reproduced from
   `/home/vgpnk`) vs green from the tree root (`receipts/base-killrule.json`).
2. **Tree-level counter mutants trip K-forgeries via the fixture-baked counter pin** (extra
   tree-tamper kill signal that masks the behavioral signal); per-mutant scoring should keep
   the harness's build_copy split (mutant copy, pins from pristine root) — used for all clean
   runs above.
3. **Selftest blind spots**: no symbolic-rev case (N1), no main-level head case (N4).

## Bounds compliance

- No lane file edited/created/deleted except SEAT paths: `w1/MutationC1/` (mutants.md,
  diffs/, receipts/) and this report `w1/MutationC1.md`; no git mutations anywhere (clones
  via `git clone --shared`, discarded by `rm -rf`).
- No subagents, no background jobs; no host changes; no tool installs (nothing needed).
- Scratch `/fast/scratch/hyaku/kaidoku-r96/MutationC1` removed after final verification;
  receipts were copied into SEAT first.

## Restoration evidence (teardown)

- Live clone discarded (`rm -rf` of the scratch clone after the last mutant); scratch
  `/fast/scratch/hyaku/kaidoku-r96/MutationC1` removed; receipts copied into SEAT first.
- Lane instrument bytes at teardown equal the pristine HEAD hashes exactly:
  v6 `7d7d559a…`, kill-rule-v2 `3b8c7583…`, symlink-probe-v2 `67b74a4b…`,
  legacy-kill-rule `2192da45…`.
- At teardown `git status` shows three **tracked** files modified (`SKILL.md`,
  `corpus/QUALITY.md`, `corpus/SOURCES.md`). These are NOT from this seat: at session start
  `git diff --stat` was empty (only `??` untracked entries) and this seat never wrote outside
  `.ufo/waves/round-96/w1/` — they are a sibling's concurrent C2 draft edits; left untouched.
- Seat writes: `w1/MutationC1/mutants.md`, `w1/MutationC1/diffs/N1…N10 *.diff` (10 files),
  `w1/MutationC1/receipts/` (23 files: base + per-mutant receipts/selftest outputs/probe
  outputs/cwd-artifact demo), and this report `w1/MutationC1.md`.

Report: .ufo/waves/round-96/w1/MutationC1.md
