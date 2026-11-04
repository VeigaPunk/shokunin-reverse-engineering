# ExecC1Base — R73-C1 BEFORE measurement

## Findings

- Exact requested `/proc/%d/environ` count: round-72 **0**, round-73 **1**. Requested round-72 `def .*kernel\|proc_` search: no matches.
- Round-72 does read `/proc/self/environ` through its git/readelf Perl shims (lines 286–355), and independently parses checker JSONL. It observes producer-side files and summaries, not a separate live-child `/proc/<pid>/environ` channel. Do not interpret the zero count as no procfs usage.
- Imported the declaration revision's round-72 probe using importlib. Executed a child inheriting the caller's environment plus a synthetic canary; retained only key names and canary presence. Then supplied fabricated clean four-key shim dumps plus matching clean checker witnesses. Exact call: `m.a11_verdict(0, obs, log, shims, str(S))`. Result: **ok=true, observed_ok=true**. Complete synthetic arguments and returned verdict are in `ExecC1Base/a11-forged-world.json`.
- This is a pure-verdict boundary experiment with a separately executed inherited-environment child, not an end-to-end forged checker attack. The actual child's environment is not an input to `a11_verdict`; clean fabricated evidence therefore passes.
- Ran the declaration revision's round-72 probe end to end against the named round-73 route, using declaration round-73 packed-elf and mutation-check blobs, explicit scratch work/TMPDIR and a pinned scratch UPX copy. Result: **target=11**, IDs A1–A11, **no A12**, **8/11 passed**, rc=1. This confirms the requested census, not an all-green probe.
- Round-73 `--selftest`: **14 cases**, no failures, rc=0.

## Retained evidence

All paths below are relative to `.ufo/waves/round-73/w1/`:

- `ExecC1Base/static-and-selftest.json`: exact search commands/results, observed selftest output, UPX copy digest.
- `ExecC1Base/a11-forged-world.json`: exact synthetic call inputs/result, actual child environment key names and canary presence, declaration module digest.
- `ExecC1Base/r72-end-to-end-summary.json`: full argv, return code, declaration blob digests, all eleven arm IDs/results and A2 binding defects. Raw stdout, environment values and nonce values were not retained.

## Risks and boundaries

The shared route receipt changed during this seat's execution: the initial read identified declaration rev `da6c17c1...` / producer digest `e184cf118427e4678dbbf2647eb615948cffc8ecf59783b13850046d0a9970b1`; the executed probe observed receipt rev `d36c6ee00122e9c991d7c8efc2e179dc0a10d9ed` / producer digest `ed3e26fab2ace12e94956704bab68940443fe093bd10aa2c70c75aa9c3284c1b`. A2, A10 and A11 failed. A2 also compares the supplied seat-local UPX path with the pre-existing receipt's L1-local path, so this receipt cannot establish successful seat-local path threading. No frozen receipt was rewritten and no green result is claimed.

No implementation files changed; no tools installed; no git writes. Scratch was deleted by the measurement driver's `finally` before reporting. No LSP interface was exposed in this seat; no symbol refactor was performed. Only assignment-authorized measurement/selftest commands were run.

## Self-evaluation

Accuracy 4/5: exact observations retained; receipt drift prevents attributing a green run to the declaration route. Completeness 4/5: all four requested measurements completed, but full-probe success was not observed. Clarity 4/5: explicit distinction between file witnesses and kernel witnesses; synthetic call details are in JSON. Actionability 4/5: argv and binding defects identify the integration issue; parent should use an immutable matching route receipt if it needs an all-green comparison. Conciseness 4/5: separate receipts keep this report bounded. Overall 4.0/5. Improvement: parent-owned immutable input binding would remove the route-drift ambiguity. User agreement expected because failures and experiment scope are explicit.
