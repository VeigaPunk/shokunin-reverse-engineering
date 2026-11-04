# R71-C1 independent base-world re-derivation

Axes: coverage; base-world reproducibility; failure attribution.

## Result
Frozen round-71 probe: rc 1, arms_passed 7, target 10, failed ["A8_child_env_observed", "A9_concurrent_collision", "A10_run_binding"].
Round-70 probe, independently executed at landing: rc 0, arms_passed 7, target 7, failed [].

## Frozen identity and pinned packer
Freeze: `b827a8b5d54f2885ec9be7786389f356c59226ce`; base-world landing: `7c155617bb42dadf1725b88a06fe3f235c364f0a`.
The frozen probe blob SHA256 matches claims.json: `7c7734af66f571618bb948f90a5d2d7048f245de122f294574939970db1bf157`.
The landing route blob SHA256 is `417b116803fbf78b44220d4a2caeb30d1261030353bc1b1c81d22c3b0146048a`.
The receipt-recorded packer path already existed: `/fast/scratch/hyaku/kaidoku-r70/l1/landing/upx-pinned-copy`. Its measured SHA256 and the recreated copy under my scratch both match UPX 5.2.0 pin `cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969`.
No external write was needed or permitted: the existing round-70 path was reused read-only for --expect-upx so A2 compares the historical argv path exactly. The recreated own-scratch copy was removed with scratch. This is the only deviation from the requested recreate-at-historical-path wording.
Pin observations retained in `setup.json`. No tools installed or upgraded. No LSP interface was exposed; source inspected directly.

## Probe command and exact missing-arm observations
```
python3 -I -B /fast/scratch/hyaku/kaidoku-r71/ExecC1Base/seam-probe71.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 7c155617bb42dadf1725b88a06fe3f235c364f0a --tool tools/round-70/packed-elf.py --battery tools/round-70/mutation-check.py --pkg /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --work /fast/scratch/hyaku/kaidoku-r71/ExecC1Base --receipt /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-70/l1/scores/c3-at-landing.json --expect-upx /fast/scratch/hyaku/kaidoku-r70/l1/landing/upx-pinned-copy --json-out /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-71/w1/ExecC1Base/base-probe.json
```
The command intentionally omits --nonce-commitment, exactly as assigned. A10 therefore reports the missing-input branch, not a nonce-validation runtime failure. The independent legacy CLI rejections and absent receipt fields below separately establish the missing binding capability.

### A8_child_env_observed
```json
{
  "id": "A8_child_env_observed",
  "observed": {
    "children": [],
    "raw_allowlisted": false,
    "raw_canary_present": false,
    "raw_home_under_run": false,
    "raw_tmpdir_under_run": false,
    "rc": 2,
    "receipt_observed": {},
    "records": 0,
    "run_root": null
  },
  "ok": false
}
```

### A9_concurrent_collision
```json
{
  "id": "A9_concurrent_collision",
  "observed": {
    "battery": [
      {
        "rc": 0,
        "work_dir": "/fast/scratch/hyaku/kaidoku-r71/ExecC1Base/a9-7mfu4scc/mutation-check-y66bs67s"
      },
      {
        "rc": 0,
        "work_dir": "/fast/scratch/hyaku/kaidoku-r71/ExecC1Base/a9-7mfu4scc/mutation-check-xj2ohdhw"
      },
      {
        "rc": 0,
        "work_dir": "/fast/scratch/hyaku/kaidoku-r71/ExecC1Base/a9-7mfu4scc/mutation-check-_idcwf3r"
      }
    ],
    "distinct_battery_dirs": 3,
    "distinct_run_roots": 1,
    "route": [
      {
        "own_home": false,
        "own_tmp": false,
        "rc": 2,
        "records": 0,
        "run_root": null,
        "verdict_claimed": null
      },
      {
        "own_home": false,
        "own_tmp": false,
        "rc": 2,
        "records": 0,
        "run_root": null,
        "verdict_claimed": null
      },
      {
        "own_home": false,
        "own_tmp": false,
        "rc": 2,
        "records": 0,
        "run_root": null,
        "verdict_claimed": null
      }
    ]
  },
  "ok": false
}
```

### A10_run_binding
```json
{
  "id": "A10_run_binding",
  "observed": {
    "missing": "no --receipt or no --nonce-commitment"
  },
  "ok": false
}
```

A9 is not evidence of an actual collision: all three concurrent battery runs succeed with three distinct work_dirs. The route preflights all exit 2 and expose no run_root or observed child logs; distinct_run_roots=1 is the set of three nulls, not a demonstrated shared directory.

## Independent legacy flag transcripts
All commands execute the exact landing blob extracted read-only with git show; only the basename changes. Full argv/stdout/stderr/rc are retained in the corresponding *-transcript.json files.

### child-env-log
```
python3 -I -B /fast/scratch/hyaku/kaidoku-r71/ExecC1Base/packed-elf70.py --child-env-log /fast/scratch/hyaku/kaidoku-r71/ExecC1Base/child.jsonl
rc=2
stdout=''
stderr:
usage: packed-elf70.py [-h] [--root ROOT] [--rev REV] [--pkg PKG]
                       [--work WORK] [--upx UPX] [--json-out JSON_OUT]
                       [--check-receipt CHECK_RECEIPT] [--skip-run]
                       [--selftest]
packed-elf70.py: error: unrecognized arguments: --child-env-log /fast/scratch/hyaku/kaidoku-r71/ExecC1Base/child.jsonl
```

### challenge
```
python3 -I -B /fast/scratch/hyaku/kaidoku-r71/ExecC1Base/packed-elf70.py --challenge public-test-challenge
rc=2
stdout=''
stderr:
usage: packed-elf70.py [-h] [--root ROOT] [--rev REV] [--pkg PKG]
                       [--work WORK] [--upx UPX] [--json-out JSON_OUT]
                       [--check-receipt CHECK_RECEIPT] [--skip-run]
                       [--selftest]
packed-elf70.py: error: unrecognized arguments: --challenge public-test-challenge
```

### carriers
```
python3 -I -B /fast/scratch/hyaku/kaidoku-r71/ExecC1Base/packed-elf70.py --carriers jq
rc=2
stdout=''
stderr:
usage: packed-elf70.py [-h] [--root ROOT] [--rev REV] [--pkg PKG]
                       [--work WORK] [--upx UPX] [--json-out JSON_OUT]
                       [--check-receipt CHECK_RECEIPT] [--skip-run]
                       [--selftest]
packed-elf70.py: error: unrecognized arguments: --carriers jq
```

### nonce-commitment
```
python3 -I -B /fast/scratch/hyaku/kaidoku-r71/ExecC1Base/packed-elf70.py --check-receipt /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-70/l1/scores/c3-at-landing.json --nonce-commitment 0000000000000000000000000000000000000000000000000000000000000000
rc=2
stdout=''
stderr:
usage: packed-elf70.py [-h] [--root ROOT] [--rev REV] [--pkg PKG]
                       [--work WORK] [--upx UPX] [--json-out JSON_OUT]
                       [--check-receipt CHECK_RECEIPT] [--skip-run]
                       [--selftest]
packed-elf70.py: error: unrecognized arguments: --nonce-commitment 0000000000000000000000000000000000000000000000000000000000000000
```

## Receipt shape and cause attribution
The committed landing receipt is retained as `round70-landing-receipt.json`; `receipt-fields.json` records exact top-level membership:
```json
{
  "run_root": {
    "present": false,
    "value": null
  },
  "child_env_observed": {
    "present": false,
    "value": null
  },
  "run_nonce": {
    "present": false,
    "value": null
  },
  "run_binding": {
    "present": false,
    "value": null
  }
}
```
A8: legacy argparse rejects --child-env-log and --carriers; the receipt has only builder-described child_env, not raw child_env_observed. Source excerpts show run(..., env=None), readelf calls without env, and direct git subprocesses without env; these inherit caller environment. The packer allowlist/selftest still passes A3; that is not runtime observation of every child.
A9: the old route makes an internal packed-* directory but does not publish run_root or support the child-env log needed to attribute each concurrent preflight. Its existing seven-arm probe tests two sequential battery runs; the new route evidence requirement is not available. Do not conflate missing evidence with measured collision.
A10: the old receipt has no run_nonce/run_binding, --challenge is rejected, and --check-receipt plus --nonce-commitment exits 2 with an unrecognized-arguments error. Thus the old checker cannot satisfy the new binding interface.

## Legacy seven-arm probe transcript
```
python3 -I -B /fast/scratch/hyaku/kaidoku-r71/ExecC1Base/seam-probe70.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 7c155617bb42dadf1725b88a06fe3f235c364f0a --tool tools/round-70/packed-elf.py --battery tools/round-70/mutation-check.py --pkg /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --work /fast/scratch/hyaku/kaidoku-r71/ExecC1Base --receipt /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-70/l1/scores/c3-at-landing.json --expect-upx /fast/scratch/hyaku/kaidoku-r70/l1/landing/upx-pinned-copy --json-out /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-71/w1/ExecC1Base/round70-probe.json
rc=0
{
  "arms_passed": 7,
  "target": 7,
  "failed": []
}
```
Landing source line excerpts and seven arm append sites are retained in `source-excerpts.txt`. Full legacy execution output is retained in `round70-probe-transcript.json` and `round70-probe.json`.

## Scope, retained evidence and limits
Read round-70 spot-check, R71-C1 plan and claims container. No frozen instrument, repository configuration, sibling evidence, state file or PATH directory changed. All created artifacts are in this seat findings directory; temporary extracted blobs, packer copy and fixtures were confined to own scratch, then removed. Nested scratch paths in receipts are run pointers only, not retained evidence. Source tools invoke their own selftests as part of the explicitly assigned probes; no unrelated gate/build/lint/formatter was run.
Evidence: base-probe.json; base-probe-transcript.json; round70-probe.json; round70-probe-transcript.json; child-env-log-transcript.json; challenge-transcript.json; carriers-transcript.json; nonce-commitment-transcript.json; round70-landing-receipt.json; receipt-fields.json; source-excerpts.txt; setup.json.
No blocker. Risk/limit: the assigned no-commitment command cannot independently exercise A10’s commitment comparison, and failed legacy argument parsing prevents observing the newer route preflight outputs. Both limitations are stated rather than interpreted as stronger runtime evidence.

## Self-evaluation
Accuracy 4/5: exact raw observations retained; A10 is explicitly a missing-input branch. Completeness 4/5: all requested runs and field checks retained; historical packer already existed and was not rewritten outside scope. Clarity 4/5: transcripts separated from interpretation; raw observations are lengthy. Actionability 5/5: named artifacts and pins support direct integration. Conciseness 4/5: full stderr/JSON costs length but preserves attribution. Overall 4.2/5. Improvements: integrate the A10 limitation explicitly; keep nested scratch pointers distinct from retained evidence. Would the user agree: likely, with the historical-path scope deviation disclosed.

VERDICT: met — independently observed R71-C1 BASE at 7/10, exactly A8/A9/A10 false; legacy probe is 7/7 and legacy CLI/receipt lacks the three new evidence interfaces.
