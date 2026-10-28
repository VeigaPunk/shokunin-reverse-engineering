# Receipt — `tools/round-44/c1-run.sh` exit paths

All commands below were run from
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin` with
`S=/fast/scratch/hyaku/kaidoku-r45/R45W1RegR44C1Run`, `TMPDIR=$S`. `$S` was removed
after its outputs were copied to `outputs/` next to this file. Nothing was committed,
staged or written anywhere in the lane tree; the only writes are under
`.ufo/waves/round-45/w1/R45W1RegR44C1Run/`.

**No data run was executed.** No REA/`npx` extraction ran; the default evidence root
`corpus/evidence/round-44/c1/` was not written (`manifest.json` mtime
`2026-10-28 09:36:45 -0300`, before every probe at 15:40–15:41 UTC).

## Instrument identity (measured rev `faa875bc`)

| file | sha256 at HEAD | sha256 at freeze `f762b727` |
|---|---|---|
| `tools/round-44/c1-run.sh` | `c35d4b9bca6cd12e7ff1a89717da033841797dde5cf3f8bd3b262d3e9860b263` | identical |
| `tools/round-44/c1-run.py` | `55e2692a3085537c2a1dc40f987c3ad8b3d7478519ddbc8a4543926fa4b061a7` | identical |

## Probe results

`stdout`/`stderr` are sha256 of the captured streams; empty stream =
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

| probe | exact command | exit | stdout sha256 | stderr sha256 | UTC |
|---|---|---|---|---|---|
| help | `bash tools/round-44/c1-run.sh --help` | 0 | `d0c9f37edd5e8434dff8d64a2b8dca63d14a7700a33c2499305df4fc70d9d26f` | empty | 2026-10-28T15:40:24Z |
| badflag | `bash tools/round-44/c1-run.sh --definitely-not-an-option` | 2 | empty | `677856cc73912eb5572a062e501696c07d3dc215543d263f4b50f554bb433587` | 2026-10-28T15:40:24Z |
| missing_sibling | `env C1_RUN_PY=$S/no-such-c1-run.py bash tools/round-44/c1-run.sh --help` | 2 | empty | `6b8b4fadebb04db8ca1be236d82e637610e97bf0f3996a641c0c9adf74e1c68d` | 2026-10-28T15:40:24Z |
| unset_home | `env -u HOME bash tools/round-44/c1-run.sh --help` | **1** | empty | `43aff449dfcfeb75f6456ae8428209af1ae2977df1d646281d220ece947cfe0a` | 2026-10-28T15:40:24Z |
| unknown_carrier | `bash tools/round-44/c1-run.sh --carrier NOSUCHCARRIER --dry-run` | 2 | empty | `e95cc377070922ba0d875db859083d0698a524c68fe1a3d10c98ff39eac7f97c` | 2026-10-28T15:40:24Z |
| refusal_default | `bash tools/round-44/c1-run.sh` | 2 | empty | `bb1842d3b1f886264312f8db657ec7f38b0c6a777e8ef035a9bfad53a9c8f7c3` | 2026-10-28T15:41:02Z |
| dry_run | `bash tools/round-44/c1-run.sh --dry-run` | 0 | `f395c601703b874d59053f28be463160a4cb88e507ab4d0ddc90b91cdb3ae659` | empty | 2026-10-28T15:41:02Z |
| pin_mismatch | `bash tools/round-44/c1-run.sh --carrier v1le --carriers $S/carriers-bad-pin.json --evidence-root $S/ev --scratch $S/scratch --keep-scratch` | 1 | `c4fe8125d3e522f8d99db86946b58a5da07ccfbbfaa5e0a07ca3230d83bb0ed7` | `c4bcddcf0193d477d13c5d4e9803118fb82cf389e86ceb030470c3484e35cf84` | 2026-10-28T15:41:29Z |
| env_abort | `bash tools/round-44/c1-run.sh --carrier v1le --carriers $S/carriers-bad-pin.json --evidence-root $S/ev2 --scratch /proc/kaidoku-r45-nope` | **1** | empty | `916d96505c616676c7f1b0fc1d104ce9879f37cf67de131df57555bf2dc62dc6` | 2026-10-28T15:41:40Z |

Machine-readable: `probes.tsv` (name, exit, stdout sha, stderr sha, UTC); raw streams in
`outputs/`; the pin-mismatch manifest in `pin-mismatch-manifest.json`; the altered
carriers copy in `outputs/carriers-bad-pin.json` (only `carriers[id=v1le].sha256` was
set to 64 zeros; the real pin is `b45925fa…23e71`).

### The two undeclared-1 arms, verbatim

`unset_home` (stderr):

```
tools/round-44/c1-run.sh: line 50: HOME: unbound variable
```

`env_abort` (stderr tail):

```
  File ".../tools/round-44/c1-run.py", line 841, in main
    os.makedirs(scratch_root, exist_ok=True)
FileNotFoundError: [Errno 2] No such file or directory: '/proc/kaidoku-r45-nope'
```

Neither is "at least one carrier failed"; both exit 1. The header's contract
(`c1-run.sh:30-31`) says environment errors are 2.

### The declared arms, observed

- `pin_mismatch` — exit 1, no REA invocation (scratch contains only the empty
  `kaidoku-r44/`), stderr:
  `c1-run: carrier v1le: fixture … hashes to b45925fa… but the frozen pin is 000…0 (not running REA on unverified bytes)`.
  Manifest: `summary.failed=["v1le"]`, `status=failed`, `exit_code=null`,
  `freeze=null`.
- `refusal_default` — exit 2 before any write:
  `c1-run: refusing to write into the committed evidence root …/corpus/evidence/round-44/c1.`
- `dry_run` — exit 0, 22 stdout lines, `# DRY RUN: nothing was written.`, no manifest.
- `missing_sibling` — exit 2 via `err()` (`c1-run.sh:43`).
- `badflag` / `unknown_carrier` — exit 2; the latter is `c1-run: no carrier matches NOSUCHCARRIER`.

## Static readings (exact lines, measured rev)

| claim | location |
|---|---|
| exit contract comment: `0` receipt / `1` carrier failed / `2` usage-env | `tools/round-44/c1-run.sh:30-31` |
| `set -euo pipefail` | `tools/round-44/c1-run.sh:32` |
| `HOME` expanded unguarded under `set -u` | `tools/round-44/c1-run.sh:50` |
| `err()` = exit 2; `[[ -f $PY_TOOL ]]`, `python3`, `npx` checks | `tools/round-44/c1-run.sh:37,43,45,52` |
| `exec python3 -I -B "$PY_TOOL" "$@"` — child code passes through | `tools/round-44/c1-run.sh:54` |
| dry-run returns 0 after printing, writes nothing | `tools/round-44/c1-run.py:952` |
| no top-level exception guard: `sys.exit(main())` | `tools/round-44/c1-run.py:1049-1050` |
| `os.makedirs(scratch_root)` unguarded | `tools/round-44/c1-run.py:841` |
| committed-evidence-root refusal returns 2 | `tools/round-44/c1-run.py:835` |
| `return 1` only when `failures` non-empty | `tools/round-44/c1-run.py:1042-1046` |
| pin gate precedes the run (`pin_ok`) | `tools/round-44/c1-run.py:358,979-984` |
| `--freeze` recorded only, never verified | `tools/round-44/c1-run.py:784-785,897,965` |
| default carriers / evidence | `tools/round-44/c1-run.py:111-112` |
| oracle not referenced by the runner | `grep -c oracle tools/round-44/c1-run.py` → `0`, rc 1 |

## Not run

- No data run: no `--data-run`, no `KAIDOKU_C1_DATA_RUN=1` on the default evidence root,
  no `npx rea-agents` extraction.
- No self-test exists in either file (`grep -n selftest tools/round-44/c1-run.sh tools/round-44/c1-run.py` → no match).
- No frozen instrument (`tools/round-45/`, `plans/round-45-claims.md`) was executed or
  modified.
