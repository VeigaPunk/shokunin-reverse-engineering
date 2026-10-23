# MutC2Judge — C2 judging selftest mutation probe

## Result and scope

**Observation:** 14 independent mutants tested: **7 killed, 7 survived, 0 inconclusive** (50% killed for this selected set). Every mutant had a passing pristine detector and a passing byte-exact restored detector. Only `--selftest` was run; no measure/build mode, REA, carrier execution, oracle execution, Git/JJ write, tool install/update, or agent dispatch occurred. This is a selftest-coverage finding, not a judgment of either frozen claim.

Axes: guard sensitivity, independence of negative cases, scratch isolation, and exact restoration. Each mutation touched only its own scratch copy of `judge()` or `committed_agrees()`. All twelve requested defect categories were included; offset and compressed-size guards were additionally isolated from their combined deletion.

**Expected detector:** the unmodified tool's bounded `--selftest` should return nonzero for an exercised contract violation. A nonzero pristine result would have made that mutant inconclusive; none occurred. Kills below are assertion-result changes, not parse errors or timeouts.

## Commands and receipts

Producing driver commands (both exited **0**):

```text
timeout 120 /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/probe.py baseline
timeout 240 /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/probe.py mutated
```

The second command ran mutant detectors, archived their bytes, then restored every working copy in a `finally` block and ran the same detectors again. Maximum concurrency was four; each detector had a 20-second command timeout and a 25-second driver backstop. All subprocesses completed and were reaped; none remain running.

Full stdout, stderr, exact argv, exit code, UTC start/end, and before/after detector hashes for **all 42 detector invocations** are preserved in:

- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/output/pristine.json` — 14 pristine runs, UTC `2026-10-23T02:43:37.097991+00:00` through `2026-10-23T02:43:37.276081+00:00`.
- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/output/mutated.json` — 14 mutant runs, UTC `2026-10-23T02:44:10.079207+00:00` through `2026-10-23T02:44:10.243404+00:00`.
- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/output/restored.json` — 14 restored runs, UTC `2026-10-23T02:44:10.244997+00:00` through `2026-10-23T02:44:10.425037+00:00`.

In each receipt, select `results[]` by its `id`; `command`, `stdout`, `stderr`, `exit`, `utc_start`, `utc_end`, `sha256_before`, and `sha256_after` are the actual recorded values. Every invocation had empty stderr. Every pristine/restored invocation exited 0 and printed `selftest cases=16 failures=0`.

### Exact detector commands and mutant UTC intervals

The same command in each row was run on pristine, mutant, and restored bytes. Times below identify the mutant phase; other phase times are in the corresponding receipts.

| ID | Exact detector command | Mutant UTC start → end (2026-10-23) |
|---|---|---|
| M01 | `/usr/bin/timeout 20 /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/cases/M01-refusal-ok-guard.py --selftest` | `02:44:10.079207+00:00` → `02:44:10.118931+00:00` |
| M02 | `/usr/bin/timeout 20 /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/cases/M02-refusal-message-guard.py --selftest` | `02:44:10.079328+00:00` → `02:44:10.118256+00:00` |
| M03 | `/usr/bin/timeout 20 /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/cases/M03-refusal-message-casefold.py --selftest` | `02:44:10.079598+00:00` → `02:44:10.118819+00:00` |
| M04 | `/usr/bin/timeout 20 /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/cases/M04-refusal-stderr-ignored.py --selftest` | `02:44:10.079737+00:00` → `02:44:10.119021+00:00` |
| M05 | `/usr/bin/timeout 20 /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/cases/M05-acceptance-exit-guard.py --selftest` | `02:44:10.118401+00:00` → `02:44:10.157927+00:00` |
| M06 | `/usr/bin/timeout 20 /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/cases/M06-operation-guard.py --selftest` | `02:44:10.118959+00:00` → `02:44:10.157704+00:00` |
| M07 | `/usr/bin/timeout 20 /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/cases/M07-subject-guard.py --selftest` | `02:44:10.119286+00:00` → `02:44:10.159796+00:00` |
| M08 | `/usr/bin/timeout 20 /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/cases/M08-package-comparison.py --selftest` | `02:44:10.119321+00:00` → `02:44:10.159984+00:00` |
| M09 | `/usr/bin/timeout 20 /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/cases/M09-offset-comparison.py --selftest` | `02:44:10.157847+00:00` → `02:44:10.203675+00:00` |
| M10 | `/usr/bin/timeout 20 /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/cases/M10-size-comparison.py --selftest` | `02:44:10.158214+00:00` → `02:44:10.203718+00:00` |
| M11 | `/usr/bin/timeout 20 /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/cases/M11-offset-size-comparison.py --selftest` | `02:44:10.160002+00:00` → `02:44:10.218270+00:00` |
| M12 | `/usr/bin/timeout 20 /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/cases/M12-committed-ok-comparison.py --selftest` | `02:44:10.160215+00:00` → `02:44:10.214779+00:00` |
| M13 | `/usr/bin/timeout 20 /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/cases/M13-committed-evidence-comparison.py --selftest` | `02:44:10.203928+00:00` → `02:44:10.243404+00:00` |
| M14 | `/usr/bin/timeout 20 /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/cases/M14-freeze-time-boundary.py --selftest` | `02:44:10.203955+00:00` → `02:44:10.241823+00:00` |

## Mutant table

Line numbers refer to the pristine source. All results below are **observations**. Proposed missing cases are separately labeled inferences below.

| ID | Single defect | Mutant exit | Exact stdout summary | Verdict | Detecting case / coverage finding |
|---|---|---:|---|---|---|
| M01 | Delete refusal `ok is True` guard, lines 203–204 | 0 | `selftest cases=16 failures=0` | survived | Existing accepted-refusal fixture is still rejected for absent message |
| M02 | Delete refusal message guard, lines 205–206 | 1 | `selftest cases=16 failures=3` | killed | `red-do-nothing`, `red-other-message`, `red-empty-predicted-message` |
| M03 | At line 205, lowercase predicted message and both streams before comparison | 0 | `selftest cases=16 failures=0` | survived | No case-only message mismatch |
| M04 | At line 205, inspect stdout only; ignore stderr | 0 | `selftest cases=16 failures=0` | survived | No green refusal with message only in stderr |
| M05 | Delete `code != 0 or` at line 208 | 0 | `selftest cases=16 failures=0` | survived | No otherwise-valid accepted envelope with nonzero exit |
| M06 | Delete operation guard, lines 211–212 | 0 | `selftest cases=16 failures=0` | survived | No otherwise-valid envelope with wrong operation |
| M07 | Delete subject SHA guard, lines 213–214 | 1 | `selftest cases=16 failures=1` | killed | `red-accept-wrong-subject` |
| M08 | Replace comparison/return at lines 222–223 with `rea_tuples(metas[0])`; preserve shape validation | 1 | `selftest cases=16 failures=1` | killed | `red-accept-wrong-packages` |
| M09 | At line 226, drop offset comparison, retaining compressed-size comparison | 1 | `selftest cases=16 failures=1` | killed | `red-accept-wrong-offset` |
| M10 | At line 226, drop compressed-size comparison, retaining offset comparison | 0 | `selftest cases=16 failures=0` | survived | No size-only discrepancy |
| M11 | Delete both offset/size comparisons, lines 226–227 | 1 | `selftest cases=16 failures=1` | killed | `red-accept-wrong-offset`; this does not establish size coverage |
| M12 | Delete committed/live ok comparison, lines 251–252 | 0 | `selftest cases=16 failures=0` | survived | Existing ok-mismatch fixture is still rejected for evidence-ID mismatch |
| M13 | Delete committed/live evidence-ID comparison, lines 253–254 | 1 | `selftest cases=16 failures=1` | killed | `red-committed-id-differs` |
| M14 | At line 247, change `added <= freeze_ct` to `added < freeze_ct` | 1 | `selftest cases=16 failures=1` | killed | `red-committed-before-freeze` actually supplies equal timestamps |

### Exact failing stdout excerpts

These excerpts are from the commands/times above; their full stdout and empty stderr remain in the mutant receipt.

```text
M02 (exit 1):
FAIL red-do-nothing got=P2-match (refused with predicted message)
FAIL red-other-message got=P2-match (refused with predicted message)
FAIL red-empty-predicted-message got=P2-match (refused with predicted message)
selftest cases=16 failures=3

M07 (exit 1):
FAIL red-accept-wrong-subject got=P2-match (accepted, packages=1)
selftest cases=16 failures=1

M08 (exit 1):
FAIL red-accept-wrong-packages got=P2-match (accepted, packages=1)
selftest cases=16 failures=1

M09 (exit 1):
FAIL red-accept-wrong-offset got=P2-match (accepted, packages=1)
selftest cases=16 failures=1

M11 (exit 1):
FAIL red-accept-wrong-offset got=P2-match (accepted, packages=1)
selftest cases=16 failures=1

M13 (exit 1):
FAIL red-committed-id-differs got=True (ok)
selftest cases=16 failures=1

M14 (exit 1):
FAIL red-committed-before-freeze got=True (ok)
selftest cases=16 failures=1
```

## Survivors named as missing selftest cases

**Inference from the observed survivors and source:** the following independent fixtures are missing. These are proposed detector cases, **not additional executed checks**; the contract was not changed and no repair was made.

| Survivor | Missing selftest case name | Isolated fixture and expected pristine result |
|---|---|---|
| M01 | `red-accepted-refusal-with-predicted-message` | Predict refusal; supply `env={"ok":true}` and the exact predicted message in stdout. Expect `P2-miss` despite the matching message. |
| M03 | `red-refusal-message-case-only` | Predict `Dependency section is empty`; supply a refused envelope with only `dependency section is empty` in the streams. Expect `P2-miss`, because the message must appear verbatim. |
| M04 | `green-refusal-message-stderr-only` | Refused envelope; empty stdout; exact predicted message only in stderr. Expect `P2-match`. |
| M05 | `red-acceptance-valid-envelope-nonzero-exit` | Reuse the fully valid acceptance fixture and oracle reading, changing only exit code from 0 to 1. Expect `P2-miss`. |
| M06 | `red-acceptance-wrong-operation` | Reuse the fully valid acceptance fixture, changing only `data.operation` from `inspect_rust_binary` to another operation. Expect `P2-miss`. |
| M10 | `red-acceptance-wrong-compressed-size` | Keep matching packages, subject and offset 10; change only oracle size from 5 to 6 against metadata `compressed_bytes=5`. Expect `P2-miss`. |
| M12 | `red-committed-ok-differs-independent-of-id` | `committed={"ok":true}`, `live={"ok":false}`, `added=200`, `freeze_ct=100`. Expect `False`; the evidence-ID guard is inapplicable because live is refused. |

**Observation (M01 command, exit 0, UTC `2026-10-23T02:44:10.079207+00:00`):** the existing accepted-refusal red case passes for a different guard:

```text
ok red-accepted-when-refusal-predicted got=P2-miss (predicted message absent)
selftest cases=16 failures=0
```

**Observation (M12 command, exit 0, UTC `2026-10-23T02:44:10.160215+00:00`):** the existing committed-ok red case passes for a different guard:

```text
ok red-committed-ok-differs got=False (committed evidence_id differs)
selftest cases=16 failures=0
```

The pristine outputs instead say `(accepted, refusal predicted)` and `(committed ok False != live ok True)`, respectively. **Inference:** case names alone overstate independent guard coverage; the assertions compare only the result label/boolean, so another guard masks these deletions. A surviving mutant is a coverage gap, not permission to weaken the predicate.

## Pristine/restored output and exact restoration

**Observation:** all 28 pristine/restored stdout values were identical, with this complete output; all exited 0 with empty stderr:

```text
ok green-refusal-matches got=P2-match (refused with predicted message)
ok green-acceptance-matches got=P2-match (accepted, packages=1)
ok red-do-nothing got=P2-miss (predicted message absent)
ok red-accepted-when-refusal-predicted got=P2-miss (accepted, refusal predicted)
ok red-other-message got=P2-miss (predicted message absent)
ok red-empty-predicted-message got=P2-miss (predicted message absent)
ok red-refused-when-acceptance-predicted got=P2-miss (not accepted (exit 1))
ok red-accept-wrong-packages got=P2-miss (package multiset differs)
ok red-accept-wrong-offset got=P2-miss (offset/size differ)
ok red-accept-wrong-subject got=P2-miss (subject sha256)
ok green-committed-agrees got=True (ok)
ok green-committed-refusal-agrees got=True (ok)
ok red-committed-absent got=False (committed envelope absent or not added after the freeze)
ok red-committed-before-freeze got=False (committed envelope absent or not added after the freeze)
ok red-committed-ok-differs got=False (committed ok False != live ok True)
ok red-committed-id-differs got=False (committed evidence_id differs)
selftest cases=16 failures=0
```

Define pristine hash **H0** = `1c357fca7b00a8aa1a524d17b7cda50526a3aa49af87f07bb94a51f678857a6b`.

For **every** mutant the byte sequence was **H0 → its archived mutant hash below → H0**. Each phase's before/after detector hashes were equal, so detector execution itself did not change the script. Restoration copied the exact pristine bytes, not a reverse patch. The lane source retained H0 in all three receipts and the final SHA-256 inventory. Archival mutant snapshots are deliberately retained only as evidence; every working case file is restored. No lane file other than this report was written.

**Unknown / not evaluated:** live REA behavior, measure-mode target attainment, and whether any proposed additional case would kill unrelated mutations. No conclusion about those was drawn.

## Artifact inventory (all SHA-256)

The producing inventory command was:

```text
timeout 20 sha256sum /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/probe.py /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/c2-rust-refusals.py /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/cases/*.py /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/snapshots/*.py /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/output/*.json /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c2-rust-refusals.py /home/vgpnk/.omp/agent/RULES.md /home/vgpnk/.agents/skills/godspeed/SKILL.md /home/vgpnk/.agents/skills/shokunin/SKILL.md
```

It exited 0. This lists all 33 scratch artifacts; no extra drafts or raw-output files were created.

| Absolute artifact path | SHA-256 |
|---|---|
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/probe.py` | `a1221d944ef60fc02f52b892cea64a9c97a74bafaab08978da56e386e2e98e5b` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/c2-rust-refusals.py` | `1c357fca7b00a8aa1a524d17b7cda50526a3aa49af87f07bb94a51f678857a6b` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/output/pristine.json` | `775518328a9bf3cf34f0a1d0b63039e3e191c4484d329b4aeeb02d7ffa90d187` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/output/mutated.json` | `10eb3c06d065f9e543b5798d1638fcb0fa6ca8876e7cadff97c57d69dc2ed442` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/output/restored.json` | `e551f298e88a4ed23954f40ffbc4658ada2388598ad8956e708250f170ad672b` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/cases/M01-refusal-ok-guard.py` | `1c357fca7b00a8aa1a524d17b7cda50526a3aa49af87f07bb94a51f678857a6b` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/cases/M02-refusal-message-guard.py` | `1c357fca7b00a8aa1a524d17b7cda50526a3aa49af87f07bb94a51f678857a6b` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/cases/M03-refusal-message-casefold.py` | `1c357fca7b00a8aa1a524d17b7cda50526a3aa49af87f07bb94a51f678857a6b` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/cases/M04-refusal-stderr-ignored.py` | `1c357fca7b00a8aa1a524d17b7cda50526a3aa49af87f07bb94a51f678857a6b` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/cases/M05-acceptance-exit-guard.py` | `1c357fca7b00a8aa1a524d17b7cda50526a3aa49af87f07bb94a51f678857a6b` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/cases/M06-operation-guard.py` | `1c357fca7b00a8aa1a524d17b7cda50526a3aa49af87f07bb94a51f678857a6b` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/cases/M07-subject-guard.py` | `1c357fca7b00a8aa1a524d17b7cda50526a3aa49af87f07bb94a51f678857a6b` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/cases/M08-package-comparison.py` | `1c357fca7b00a8aa1a524d17b7cda50526a3aa49af87f07bb94a51f678857a6b` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/cases/M09-offset-comparison.py` | `1c357fca7b00a8aa1a524d17b7cda50526a3aa49af87f07bb94a51f678857a6b` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/cases/M10-size-comparison.py` | `1c357fca7b00a8aa1a524d17b7cda50526a3aa49af87f07bb94a51f678857a6b` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/cases/M11-offset-size-comparison.py` | `1c357fca7b00a8aa1a524d17b7cda50526a3aa49af87f07bb94a51f678857a6b` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/cases/M12-committed-ok-comparison.py` | `1c357fca7b00a8aa1a524d17b7cda50526a3aa49af87f07bb94a51f678857a6b` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/cases/M13-committed-evidence-comparison.py` | `1c357fca7b00a8aa1a524d17b7cda50526a3aa49af87f07bb94a51f678857a6b` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/cases/M14-freeze-time-boundary.py` | `1c357fca7b00a8aa1a524d17b7cda50526a3aa49af87f07bb94a51f678857a6b` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/snapshots/M01-refusal-ok-guard.py` | `8233ecc929f24a066ed428af7c450c097f3d2a42a598945153ab649247b2f756` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/snapshots/M02-refusal-message-guard.py` | `4ccbd21481170b601910b35645def5f5740afae41dccd72ecd8654e909c5a5ce` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/snapshots/M03-refusal-message-casefold.py` | `b8763034c26e17ffa07f53e29b7b4f8c61370fb589a773f0780daa797596c5c1` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/snapshots/M04-refusal-stderr-ignored.py` | `30bb395ec293f5ad3815a206c7318540dfaf14c40f02dfc37471f6215f72747e` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/snapshots/M05-acceptance-exit-guard.py` | `974d04852f3cc281a51e1a6133866392ee8f21888844c1e4d9e40d8b3384d8d6` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/snapshots/M06-operation-guard.py` | `f5b66115c396d9d34e5f7e924bc16a41fe042afbb5d5c107c1a6c1e52877ff30` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/snapshots/M07-subject-guard.py` | `fc6e3d633811f77fb998f3af1a8db8985e62fb0dd157281dffa41230e0f84168` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/snapshots/M08-package-comparison.py` | `1ba5a4be07b3c40482ffbbad9bc8a027edb828b47340ebe8970215876a6e810b` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/snapshots/M09-offset-comparison.py` | `43eccefdd2a63a3197f697dd40872af68e32d64682c0a1b852c9dfb1759cdf84` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/snapshots/M10-size-comparison.py` | `d6808cf62d4f287038f2d738bc7ed41203d3fcde1105ce1ba97b928906fffcfc` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/snapshots/M11-offset-size-comparison.py` | `c5223994cb7f121189675d8aa34a39cc09a47065e0e46a5d9d612e8d0e52d156` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/snapshots/M12-committed-ok-comparison.py` | `870b9297b32902487e9ce97d1d5b42ac72a647459a43a61281cd02047cd7140c` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/snapshots/M13-committed-evidence-comparison.py` | `bd5250cd4cf2841a6be4bb9737155b1bdaa1f673c436e2cbea2a13e2f95677c5` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Judge/snapshots/M14-freeze-time-boundary.py` | `5c54dd70e7243b7e458f924c7a08d3c9109a53c568e27ce50b9d08c1b6c10fe7` |

## Opened local primary source and instruction references

Access date for all rows: **2026-10-23**. Ordinary local file reads only; no remote sources were opened. Hashes are of the served local file bytes. Each located quote is at most 25 contiguous words.

| URL | SHA-256 | Located quote |
|---|---|---|
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c2-rust-refusals.py` | `1c357fca7b00a8aa1a524d17b7cda50526a3aa49af87f07bb94a51f678857a6b` | Line 205: `if not message or (message not in out_text and message not in err_text):` |
| `file:///home/vgpnk/.omp/agent/RULES.md` | `beb647d0d4bba504e918ae988335a43403c6cff7033e42e75a2577e9ca0999ed` | Line 9: `Official sources only; never pipe an unverified remote script into a shell.` |
| `file:///home/vgpnk/.agents/skills/godspeed/SKILL.md` | `1d6167238784245e003d0c8d38197cc25824018545e31bc81de25edb38d5f83a` | Line 13: `2. **Iterate cheap, in parallel.**` |
| `file:///home/vgpnk/.agents/skills/shokunin/SKILL.md` | `59ca05018dbf0ba92a96a8d5bf672931111d01a134d640245aff60c865d0cb6e` | Line 18: `A shokunin is a domain specialist that earns its domain through demonstrated` |

No tool installation or update was needed; the probe used the existing Python standard library and coreutils.
