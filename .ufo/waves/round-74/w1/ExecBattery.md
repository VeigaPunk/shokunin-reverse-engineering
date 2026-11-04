# ExecBattery — frozen mutation battery

Axes: frozen provenance; declared-case mutation closure; receipt integrity; mismatched-pair refusal.

Freeze: `021914c0e638454e507087accfe41af1ab69f185`. Executed runner extracted directly from the committed blob (SHA-256 `156a92945f2acc257b025378e4de49064734a9652de19d6ed04b602161f0319b`). Targets are fetched by the frozen runner using `git show` at that same revision. No implementation files edited; no tools installed.

R74 target pin: `81d6a43223c5504eb4ad7312563d7a9b1bd3f6288e39c196ee1d542a4c617039`.

## Survivor lists
- r73probe: `["a-drop-genuine-canary", "b-unreadable-empty", "b-first-sample-only", "b-drop-canary-field", "c-swap-verdict-inputs", "c-skip-forged-subrun"]`; survivor_count=6; pristine cases=14; mutants=10; wrong-case kills=0.
- r74probe: `[]`; survivor_count=0; pristine cases=20; mutants=10; wrong-case kills=0.

## Commands and raw outputs
All commands run in `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

### r73probe — exit 0 (expected 0)
```sh
TMPDIR=/fast/scratch/hyaku/kaidoku-r74/ExecBattery python3 -I -B /fast/scratch/hyaku/kaidoku-r74/ExecBattery/probe-mutation.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 021914c0e638454e507087accfe41af1ab69f185 --patch-set r73probe --tool tools/round-73/seam-probe.py --work /fast/scratch/hyaku/kaidoku-r74/ExecBattery/work-r73 --expect-survivors 6 --json-out /fast/scratch/hyaku/kaidoku-r74/ExecBattery/r73probe.json
```
stdout:
```json
{
 "expected": {
  "survivor_names": null,
  "survivors": 6
 },
 "killed": [
  "a-drop-forged-detected",
  "a-drop-lie-clean",
  "a-drop-genuine-rc",
  "a-any-forged-sample"
 ],
 "killed_wrong_case": [],
 "min_pristine_cases": 14,
 "mutants": [
  {
   "cases": 14,
   "expect_case": null,
   "failed": [
    "a12-kernel-cases"
   ],
   "name": "a-drop-forged-detected",
   "rc": 1,
   "verdict": "killed"
  },
  {
   "cases": 14,
   "expect_case": null,
   "failed": [
    "a12-kernel-cases"
   ],
   "name": "a-drop-lie-clean",
   "rc": 1,
   "verdict": "killed"
  },
  {
   "cases": 14,
   "expect_case": null,
   "failed": [],
   "name": "a-drop-genuine-canary",
   "rc": 0,
   "verdict": "survived"
  },
  {
   "cases": 14,
   "expect_case": null,
   "failed": [
    "a12-kernel-cases"
   ],
   "name": "a-drop-genuine-rc",
   "rc": 1,
   "verdict": "killed"
  },
  {
   "cases": 14,
   "expect_case": null,
   "failed": [
    "a12-kernel-cases"
   ],
   "name": "a-any-forged-sample",
   "rc": 1,
   "verdict": "killed"
  },
  {
   "cases": 14,
   "expect_case": null,
   "failed": [],
   "name": "b-unreadable-empty",
   "rc": 0,
   "verdict": "survived"
  },
  {
   "cases": 14,
   "expect_case": null,
   "failed": [],
   "name": "b-first-sample-only",
   "rc": 0,
   "verdict": "survived"
  },
  {
   "cases": 14,
   "expect_case": null,
   "failed": [],
   "name": "b-drop-canary-field",
   "rc": 0,
   "verdict": "survived"
  },
  {
   "cases": 14,
   "expect_case": null,
   "failed": [],
   "name": "c-swap-verdict-inputs",
   "rc": 0,
   "verdict": "survived"
  },
  {
   "cases": 14,
   "expect_case": null,
   "failed": [],
   "name": "c-skip-forged-subrun",
   "rc": 0,
   "verdict": "survived"
  }
 ],
 "ok": true,
 "patch_set": "r73probe",
 "pristine": {
  "cases": 14,
  "failed": [],
  "rc": 0,
  "stderr_tail": ""
 },
 "pristine_ok": true,
 "rev": "021914c0e638454e507087accfe41af1ab69f185",
 "root": "/home/vgpnk/Projects/shokunin/kaidoku-shokunin",
 "runner": {
  "path": "tools/round-74/probe-mutation.py",
  "sha256": "156a92945f2acc257b025378e4de49064734a9652de19d6ed04b602161f0319b"
 },
 "schema": "kaidoku-r74-probe-mutation-v1",
 "survivor_count": 6,
 "survivors": [
  "a-drop-genuine-canary",
  "b-unreadable-empty",
  "b-first-sample-only",
  "b-drop-canary-field",
  "c-swap-verdict-inputs",
  "c-skip-forged-subrun"
 ],
 "target_pin": {
  "expect": null,
  "matched": null,
  "pinned": false
 },
 "target_sha256": "9c286fd7187e25a8c6de5d743e21d0402ec6c9862a14aecfaed75b2006710939",
 "tool": "tools/round-73/seam-probe.py",
 "work": "/fast/scratch/hyaku/kaidoku-r74/ExecBattery/work-r73/mut-text-cj8a52qx"
}
```
stderr:
```text

```

### r74probe — exit 0 (expected 0)
```sh
TMPDIR=/fast/scratch/hyaku/kaidoku-r74/ExecBattery python3 -I -B /fast/scratch/hyaku/kaidoku-r74/ExecBattery/probe-mutation.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 021914c0e638454e507087accfe41af1ab69f185 --patch-set r74probe --tool tools/round-74/seam-probe.py --work /fast/scratch/hyaku/kaidoku-r74/ExecBattery/work-r74 --expect-survivors 0 --expect-target-sha256 81d6a43223c5504eb4ad7312563d7a9b1bd3f6288e39c196ee1d542a4c617039 --json-out /fast/scratch/hyaku/kaidoku-r74/ExecBattery/r74probe.json
```
stdout:
```json
{
 "expected": {
  "survivor_names": null,
  "survivors": 0
 },
 "killed": [
  "a-drop-forged-detected",
  "a-drop-lie-clean",
  "a-drop-genuine-canary",
  "a-drop-genuine-rc",
  "a-any-forged-sample",
  "b-unreadable-empty",
  "b-first-sample-only",
  "b-drop-canary-field",
  "c-swap-verdict-inputs",
  "c-skip-forged-subrun"
 ],
 "killed_wrong_case": [],
 "min_pristine_cases": 20,
 "mutants": [
  {
   "cases": 20,
   "expect_case": "a12-kernel-cases",
   "failed": [
    "a12-kernel-cases"
   ],
   "name": "a-drop-forged-detected",
   "rc": 1,
   "verdict": "killed"
  },
  {
   "cases": 20,
   "expect_case": "a12-kernel-cases",
   "failed": [
    "a12-kernel-cases"
   ],
   "name": "a-drop-lie-clean",
   "rc": 1,
   "verdict": "killed"
  },
  {
   "cases": 20,
   "expect_case": "a12-genuine-canary-only",
   "failed": [
    "a12-genuine-canary-only"
   ],
   "name": "a-drop-genuine-canary",
   "rc": 1,
   "verdict": "killed"
  },
  {
   "cases": 20,
   "expect_case": "a12-kernel-cases",
   "failed": [
    "a12-kernel-cases"
   ],
   "name": "a-drop-genuine-rc",
   "rc": 1,
   "verdict": "killed"
  },
  {
   "cases": 20,
   "expect_case": "a12-kernel-cases",
   "failed": [
    "a12-kernel-cases"
   ],
   "name": "a-any-forged-sample",
   "rc": 1,
   "verdict": "killed"
  },
  {
   "cases": 20,
   "expect_case": "a12-proc-environ-unreadable",
   "failed": [
    "a12-proc-environ-unreadable"
   ],
   "name": "b-unreadable-empty",
   "rc": 1,
   "verdict": "killed"
  },
  {
   "cases": 20,
   "expect_case": "a12-kernel-multiple-samples",
   "failed": [
    "a12-kernel-multiple-samples"
   ],
   "name": "b-first-sample-only",
   "rc": 1,
   "verdict": "killed"
  },
  {
   "cases": 20,
   "expect_case": "a12-kernel-canary-field",
   "failed": [
    "a12-kernel-multiple-samples",
    "a12-kernel-canary-field"
   ],
   "name": "b-drop-canary-field",
   "rc": 1,
   "verdict": "killed"
  },
  {
   "cases": 20,
   "expect_case": "a12-arm-wiring",
   "failed": [
    "a12-arm-wiring"
   ],
   "name": "c-swap-verdict-inputs",
   "rc": 1,
   "verdict": "killed"
  },
  {
   "cases": 20,
   "expect_case": "a12-arm-forged-executed",
   "failed": [
    "a12-arm-forged-executed"
   ],
   "name": "c-skip-forged-subrun",
   "rc": 1,
   "verdict": "killed"
  }
 ],
 "ok": true,
 "patch_set": "r74probe",
 "pristine": {
  "cases": 20,
  "failed": [],
  "rc": 0,
  "stderr_tail": ""
 },
 "pristine_ok": true,
 "rev": "021914c0e638454e507087accfe41af1ab69f185",
 "root": "/home/vgpnk/Projects/shokunin/kaidoku-shokunin",
 "runner": {
  "path": "tools/round-74/probe-mutation.py",
  "sha256": "156a92945f2acc257b025378e4de49064734a9652de19d6ed04b602161f0319b"
 },
 "schema": "kaidoku-r74-probe-mutation-v1",
 "survivor_count": 0,
 "survivors": [],
 "target_pin": {
  "expect": "81d6a43223c5504eb4ad7312563d7a9b1bd3f6288e39c196ee1d542a4c617039",
  "matched": true,
  "pinned": true
 },
 "target_sha256": "81d6a43223c5504eb4ad7312563d7a9b1bd3f6288e39c196ee1d542a4c617039",
 "tool": "tools/round-74/seam-probe.py",
 "work": "/fast/scratch/hyaku/kaidoku-r74/ExecBattery/work-r74/mut-text-lvws57ft"
}
```
stderr:
```text

```

### mismatched-pair — exit 2 (expected 2)
```sh
TMPDIR=/fast/scratch/hyaku/kaidoku-r74/ExecBattery python3 -I -B /fast/scratch/hyaku/kaidoku-r74/ExecBattery/probe-mutation.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 021914c0e638454e507087accfe41af1ab69f185 --patch-set r74probe --tool tools/round-73/seam-probe.py --work /fast/scratch/hyaku/kaidoku-r74/ExecBattery/work-r74
```
stdout:
```json

```
stderr:
```text
{"schema": "kaidoku-r74-probe-mutation-v1", "unevaluable": "patch set r74probe targets tools/round-74/seam-probe.py, not tools/round-73/seam-probe.py"}
```

### validate-tampered — exit 1 (expected 1)
```sh
TMPDIR=/fast/scratch/hyaku/kaidoku-r74/ExecBattery python3 -I -B /fast/scratch/hyaku/kaidoku-r74/ExecBattery/probe-mutation.py --validate /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-74/w1/ExecBattery/r74probe-tampered.json
```
stdout:
```json
{
 "validate": "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-74/w1/ExecBattery/r74probe-tampered.json",
 "defects": [
  "survivor_count disagrees with the mutant rows"
 ]
}
```
stderr:
```text

```

### validate-r73probe — exit 0 (expected 0)
```sh
TMPDIR=/fast/scratch/hyaku/kaidoku-r74/ExecBattery python3 -I -B /fast/scratch/hyaku/kaidoku-r74/ExecBattery/probe-mutation.py --validate /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-74/w1/ExecBattery/r73probe.json
```
stdout:
```json
{
 "validate": "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-74/w1/ExecBattery/r73probe.json",
 "defects": []
}
```
stderr:
```text

```

### validate-r74probe — exit 0 (expected 0)
```sh
TMPDIR=/fast/scratch/hyaku/kaidoku-r74/ExecBattery python3 -I -B /fast/scratch/hyaku/kaidoku-r74/ExecBattery/probe-mutation.py --validate /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-74/w1/ExecBattery/r74probe.json
```
stdout:
```json
{
 "validate": "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-74/w1/ExecBattery/r74probe.json",
 "defects": []
}
```
stderr:
```text

```

## Findings
Exit-code deviations: []. Named tamper defect and mismatch refusal retained verbatim above and in command JSON files.

## Risks and bounds
The battery exercises declared selftests, not every real-host seam. The r73 arm is intentionally unpinned (no SHA expectation requested); its actual target SHA is retained in its receipt. Scratch paths embedded in receipts are ephemeral and removed before return. LSP not exposed in this seat; no symbol edits or refactors performed. No build/lint/formatter or unrelated gate executed.

## Self-evaluation
Accuracy 4/5: frozen blobs, exit codes and raw outputs retained; this does not establish real-host behavior. Completeness 5/5: two scoring arms, two clean validations, tampered validation and mismatch refusal all executed. Clarity 4/5: full raw JSON makes the report long but auditable. Actionability 5/5: persistent receipts and exact commands supplied. Conciseness 4/5: raw evidence duplicated intentionally to satisfy command/output retention. Overall 4.4/5; prefer results.json for machine consumption.
