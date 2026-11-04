# ExecRepairs — round 74

Axes: record accuracy, append-only preservation, resolving evidence, bounded scope.

## Changes

Only SCORECARD.md, PROVINCE.md, corpus/README.md and this exclusive advisory report were written. No instruments or filed claim rows were rewritten. No installs, git mutations, environment dumps, builds, tests, linters or formatters were run. Markdown changes do not require symbol refactoring; no LSP tool is mounted in this seat.

SCORECARD gains three round-73 and two round-74 capability rows, each with four cells/five literal pipes matching its header. The appended round-73 selection block distinguishes the 11-arm before comparator from the 8/12 route differential. PROVINCE gains bounded round-74 Core closure and the four named Frontier exclusions. README receives only its missing terminal newline.

## Exact edit hunks

Coordinates below refer to the pre-edit snapshots SCORECARD.md#42FD, PROVINCE.md#A583 and corpus/README.md#4B51. Unshown bytes were not targeted.

```diff
--- a/SCORECARD.md
+++ b/SCORECARD.md
@@ -648,0 +649,5 @@
+| kernel-side environment witness bound by ancestry | reads the kernel environment of a sampled descendant and detects clean child dumps contradicted by dirty kernel samples, with a forged control in A12 | `.ufo/waves/round-73/l1/scores/c1-at-landing.json` (12/12 arms, forged_detected true) | round 73 |
+| record-vs-receipt audit | re-derives seven self-assessment atoms against cited receipts over the previous round's outside routed-defect population | `.ufo/waves/round-73/l1/scores/c2-at-landing.json` (0 mismatches, seven atoms) | round 73 |
+| reader-seam selftest closure | binds each of the three round-72 reader-seam mutation survivors to a declared killing case on the pinned target | `.ufo/waves/round-73/l1/scores/c3-at-landing.json` (r73: 0 survivors, pristine 38 cases) | round 73 |
+| kernel-witness probe-mutation closure | scores ten defect classes against declared cases with `tools/round-74/probe-mutation.py`, closing the six round-73 A12 selftest survivors | `.ufo/waves/round-74/pre/c1-post-at-declaration.json` (r74probe: 0 survivors, pristine 20 cases, target pinned) | round 74 |
+| record-audit v2 | re-derives sixteen atoms over the round-73 routed set and planned items with `tools/round-74/record-audit.py`, retaining D1-D7 and adding D7b plus D8-D15 | `tools/round-74/record-audit.py`; `.ufo/waves/round-74/pre/c2-at-base.json` (11 mismatches at base; not a landing result) | round 74 |
@@ -5766,0 +5772,9 @@
+
+**Before-arm selection (round 74 correction)**
+R73-C1's before-arm is `.ufo/waves/round-73/pre/c1-at-base-r72probe.json`
+(`pre/c1-at-base-r72probe.json` in the filed row): the round-72 probe reports
+11 arms, 11 passed, and no A12. The other before run,
+`.ufo/waves/round-73/pre/c1-at-base.json` (`pre/c1-at-base.json`, 8 of 12),
+is the route differential using the round-73 probe against the round-72 route,
+not R73-C1's before-arm. This selection supplements, rather than rewrites,
+the filed claim row.
--- a/PROVINCE.md
+++ b/PROVINCE.md
@@ -555,0 +556,10 @@
+## Round-74 additions to Core
+
+- **Core — kernel-witness selftest case closure:** `tools/round-74/seam-probe.py`
+  binds the A12 verdict, kernel-sample parsing and arm wiring to declared cases;
+  `tools/round-74/probe-mutation.py` scores ten defect classes, including the six
+  round-73 survivors. Retained evidence:
+  `.ufo/waves/round-74/pre/c1-post-at-declaration.json` (r74probe: 0 survivors,
+  pristine 20 cases, target pinned).
+- **Still Frontier:** a wrapper that never runs a sampled process,
+  `PR_SET_MM_ENV_START` relocation, non-Linux substrates, and signed receipts.
--- a/corpus/README.md
+++ b/corpus/README.md
@@ -339 +339 @@
-Round-73 frontier note, 2026-11-04: **the kernel-side environment witness** is Core for `tools/round-73/seam-probe.py` A12 (`2026-11-04-r73-kernel-witness-record`; S277, S275): the observer reads `/proc/<pid>/environ` for a shim it started, bound by ancestry, and the arm carries its own lying-shim control. This supersedes the round-72 note's 'producer-independent (hostile-wrapper) child census' line for the sampled-descendant case only. Still Frontier: a wrapper that never runs a sampled process, `PR_SET_MM_ENV_START` relocation (privileged), non-Linux substrates, signed receipts, other packers/carriers, anti-UPX stubs, packed PE/Mach-O, semantic inventory equality.
\ No newline at end of file
+Round-73 frontier note, 2026-11-04: **the kernel-side environment witness** is Core for `tools/round-73/seam-probe.py` A12 (`2026-11-04-r73-kernel-witness-record`; S277, S275): the observer reads `/proc/<pid>/environ` for a shim it started, bound by ancestry, and the arm carries its own lying-shim control. This supersedes the round-72 note's 'producer-independent (hostile-wrapper) child census' line for the sampled-descendant case only. Still Frontier: a wrapper that never runs a sampled process, `PR_SET_MM_ENV_START` relocation (privileged), non-Linux substrates, signed receipts, other packers/carriers, anti-UPX stubs, packed PE/Mach-O, semantic inventory equality.
```

## Retained evidence

Read-only `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 021914c0e638454e507087accfe41af1ab69f185:<path>` succeeded for all evidence pointers used in the five rows:

| Path | Observed result |
|---|---|
| .ufo/waves/round-73/l1/scores/c1-at-landing.json | rc 0, 33825 bytes |
| .ufo/waves/round-73/l1/scores/c2-at-landing.json | rc 0, 3464 bytes |
| .ufo/waves/round-73/l1/scores/c3-at-landing.json | rc 0, 1578 bytes |
| .ufo/waves/round-74/pre/c1-post-at-declaration.json | rc 0; r74probe, survivor_count 0, pristine 20 cases, target_pin.matched true; ten named declared-case kills |
| tools/round-74/record-audit.py | rc 0, 28682 bytes |
| .ufo/waves/round-74/pre/c2-at-base.json | rc 0; population.atoms 16, mismatch_count 11 at 04fdc2c4dbedbe5ee50a069af14310068393233e |

Also resolved tools/round-74/probe-mutation.py (18167 bytes) and tools/round-74/seam-probe.py (71029 bytes) at the freeze, both rc 0. These were evidence-object reads, not instrument reruns.

The first multi-file edit was rejected atomically because replacing the final README line with identical text did not change the trailing-newline state. Fresh reads showed all three files unchanged; the subsequent edit applied all additions and inserted the terminal newline via an empty final-line insertion. Tool behavior was reported through the mandated QA device. Successful edit snapshots: SCORECARD.md#972A, PROVINCE.md#E36D, corpus/README.md#83BE.

Scratch /fast/scratch/hyaku/kaidoku-r74/ExecRepairs-2 was created and removed under an EXIT trap; the command exited successfully. No scratch receipts were generated.

## Risks / parent checks

No blocker. The v2 capability cites the frozen implementation and baseline receipt, explicitly not an unobserved zero-mismatch landing result. Parent owns post-integration verification: audit the final committed revision, confirm five-pipe new rows, README final byte 0a, and additions-only preservation of filed lines. No post-edit verification was run by this seat.

Self-assessment: accuracy 4 (landing verification intentionally parent-owned), completeness 4 (acceptance-byte checks intentionally parent-owned), clarity 4 (exact hunks are long but required), actionability 4 (parent checks explicitly named), conciseness 4 (report retains full requested hunks); mean 4.0. Highest-impact remaining action is the parent integration gate, not another leaf run.
