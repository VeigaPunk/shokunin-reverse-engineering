# ExecProbeCases — independent re-derivation of the six A12 selftest bindings (round-74 w1)

Seat: ExecProbeCases (executor) · 2026-11-04
Target: `tools/round-74/seam-probe.py` (read-only; sha256 `81d6a43223c5504eb4ad7312563d7a9b1bd3f6288e39c196ee1d542a4c617039`)

## Method

Six hand mutations, one per defect class, applied to byte-identical scratch copies of the
probe under `/fast/scratch/hyaku/kaidoku-r74/ExecProbeCases/` (scratch deleted after the
run). `tools/round-74/probe-mutation.py` was NOT used. Each variant ran as
`python3 -I -B <variant>.py --selftest` with cwd = the lane root and `TMPDIR` pinned to the
scratch tmp dir. Raw stdout/stderr per variant: `raw-outputs/*.selftest.{out,err}`;
per-variant sha256 manifest: `raw-outputs/variant-manifest.json`. Structured result:
`receipt.json`.

## Result matrix

| variant | mutation | rc | exact `failures` | declared case | verdict |
|---|---|---|---|---|---|
| pristine | none | 0 | `[]` (cases 20) | — | clean |
| m1 | delete `and not s.get("canary_present")` from `a12_verdict`'s `genuine_ok` | 1 | `["a12-genuine-canary-only"]` | a12-genuine-canary-only | binds, no cross-binding |
| m2 | `_proc_env` `except OSError` returns `{}` instead of `None` | 1 | `["a12-proc-environ-unreadable"]` | a12-proc-environ-unreadable | binds, no cross-binding |
| m3 | `kernel_witness` returns `list(seen.values())[:1]` | 1 | `["a12-kernel-multiple-samples"]` | a12-kernel-multiple-samples | binds, no cross-binding |
| m4 | delete the `"canary_present": ...` entry from the sample dict | 1 | `["a12-kernel-multiple-samples", "a12-kernel-canary-field"]` | a12-kernel-canary-field | binds, WITH cross-binding (D1) |
| m5 | swap the two witness arguments in `assemble_arm`'s verdict call | 1 | `["a12-arm-wiring"]` | a12-arm-wiring | binds, no cross-binding |
| m6 | `forged_subrun` returns `{"rc": [], "shims": {}, "kernel": {}}` before its first statement | 1 | `["a12-arm-forged-executed"]` | a12-arm-forged-executed | binds, no cross-binding |

All mutants and the pristine run printed empty stderr; every run reported `cases: 20`.

## Defect D1 — cross-binding (m4)

Mutation m4 (sample dict loses `"canary_present"`) fails two declared cases, not one.
Exact stdout of the m4 run:

```
{
 "cases": 20,
 "failures": [
  "a12-kernel-multiple-samples",
  "a12-kernel-canary-field"
 ],
 "selftest": "tools/round-74/seam-probe.py"
}
```

Cause: `a12-kernel-multiple-samples`'s third conjunct is
`any(s.get("canary_present") for s in samples)`, which depends on the very field schema
that `a12-kernel-canary-field` guards. A schema-destroying mutant is therefore detected
twice, and a failure of `a12-kernel-multiple-samples` does not uniquely attribute to the
multiple-samples conjunct. The coupling is asymmetric: m3 (first-sample-only truncation)
does NOT fail `a12-kernel-canary-field` (the surviving pid-10 sample still carries all
three booleans).

Scope note: R74-C1's survivor_count-0 result is unaffected — every mutant exits rc 1 with
its declared case in `failures`, and the pristine probe is green (rc 0, 20 cases,
no failures). D1 is a case-attribution precision finding about the case matrix, not an
operability failure.

## Acceptance check

- Per mutation rc 1 with its declared case present in `failures`: **holds** for all six.
- No other declared case fails for a mutation that is not its own: **does not hold for m4**
  (D1 above); holds for m1, m2, m3, m5, m6 (each fails exactly its own case).
- Pristine rc 0 with `cases 20` and empty `failures`: **holds**.

Report: .ufo/waves/round-74/w1/ExecProbeCases.md
