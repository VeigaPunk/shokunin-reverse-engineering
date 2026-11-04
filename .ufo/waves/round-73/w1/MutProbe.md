# MutProbe: round-73 probe selftest attacks

Axes: detection sensitivity, false-green resistance, exact restoration, environment-value confidentiality.

## Method and controls

Ten independent scratch copies of the current lane `tools/round-73/seam-probe.py`; no lane-source mutation. Each ran the same bounded detector, `python3 -I -B <copy>/seam-probe.py --selftest`, on pristine, mutated, and byte-restored contents (30 invocations total). All pristine/restored runs: rc 0, cases 14, failures []. Each invocation had TMPDIR explicitly set to the assigned scratch parent and cwd set to the lane. No tools installed; no environment values recorded.

Source and every pristine/restored copy SHA-256: `7264d0c861d5d0f5344a4009dba738579a10952d27a207dd0d8530cf434b48ed`. Every restoration matched exact original bytes. Scratch `/fast/scratch/hyaku/kaidoku-r73/MutProbe-4/` was removed in finally after copying receipts. Source bytes remained unchanged at receipt creation. These are working-tree observations, not an assertion that the working tree equals the frozen declaration.

## Actual outcomes

| Mutant | rc | Failed cases | Verdict / binding |
|---|---:|---|---|
| a-drop-forged-detected | 1 | a12-kernel-cases | killed; existing clean/empty forged-kernel rejection binds |
| a-drop-lie-clean | 1 | a12-kernel-cases | killed; existing empty forged-shims rejection binds |
| a-drop-genuine-canary | 0 | [] | survived; no independent genuine canary test binds |
| a-drop-genuine-rc | 1 | a12-kernel-cases | killed; existing rc=1 rejection binds |
| a-any-forged-sample | 1 | a12-kernel-cases | killed; existing clean forged-kernel rejection binds |
| b-unreadable-empty | 0 | [] | survived; no unreadable environ acquisition test binds |
| b-first-sample-only | 0 | [] | survived; no multi-process acquisition test binds |
| b-drop-canary-field | 0 | [] | survived; no acquisition field-schema test binds |
| c-swap-verdict-inputs | 0 | [] | survived; no arm-wiring execution test binds |
| c-skip-forged-subrun | 0 | [] | survived; no forged-subrun execution test binds |

Totals: **4 killed, 6 survived, 0 inconclusive**. All four kills are behavioral assertion failures, not syntax errors or baseline failures. Full stdout/stderr, per-mutant hashes, expected detector names, and controls are in `MutProbe/results.json`; ten unified mutation patches are alongside it.

## Exact missing cases

- `a12-genuine-canary-only`: genuine rc 0, both required classes, exact allowlist keys, but one sample has canary_present=True; require ok=False. Existing dirty genuine fixture changes both keys and canary, so key comparison masks deletion of the canary conjunct. This is an independent-field guard gap; the combined fixture remains rejected.
- `a12-proc-environ-unreadable`: mock open raising PermissionError, require `_proc_environ` returns None; mocked polling must omit that PID rather than fabricate an empty environment sample.
- `a12-kernel-multiple-samples`: deterministic mocked /proc scan with two matching shim PIDs, later one dirty; require both samples retained.
- `a12-kernel-canary-field`: deterministic mocked kernel scan with canary present/absent; require explicit boolean `canary_present` in both output samples.
- `a12-arm-wiring`: stub arm subprocess/thread/witness boundaries, execute `kernel_witness_arm`, capture verdict arguments, and require genuine first, forged second.
- `a12-arm-forged-executed`: execute the stubbed arm; require forged git and readelf producer launches and kernel polling before verdict. Pure verdict fixtures cannot bind deletion of the actual forged sub-run.

Survivors are selftest coverage findings, not permission to alter the contract or a claim that a full runtime probe would pass those mutants. This assignment ran only the requested --selftest detector.

Self-evaluation: accuracy 4 (actual per-run outputs/hashes retained; working tree not declaration-attested); completeness 5 (all ten attacks and controls); clarity 4 (grouped existing case obscures the precise short-circuit clause, described above); actionability 5 (six exact missing cases); conciseness 4 (full raw output intentionally relegated to JSON). Overall 4.4. Highest-impact improvement: bind arm execution and kernel acquisition, then independently vary genuine canary. User-agreement check: findings stay scoped to the requested detector.

Report: .ufo/waves/round-73/w1/MutProbe/results.json
