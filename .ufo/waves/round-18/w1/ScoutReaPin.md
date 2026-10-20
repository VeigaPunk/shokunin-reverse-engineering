# ScoutReaPin — REA CLI pin reproducibility (round 18, W1)

Verdict: **PASS**. `npx -y rea-agents@6.5.0` still prints `6.5.0`, its `analyze --help` surface
renders with no target, and the run is **cache-only reproducible** (offline, 0.64 s). `rea-agents@6.7.0`
**is also cached** on this host in a separate npx tree. No install or upgrade was performed; nothing
outside this file was written.

Scope guard: only `--version` and `analyze --help` were run — never `analyze` against a target —
consistent with `LANE/.ufo/waves/round-18/contract.md:14`.

## Axes (named before measuring)

- **A1 calibration** — does the pin recorded in the seat prompt / generator still resolve to the same
  artifact bytes it did on 2026-10-16?
- **A2 operability** — does the pinned CLI run on today's host toolchain, and does it need the network?
- **A3 depth** — is a second version cached that could silently substitute if the pin text is dropped?

## Commands, exit codes, outputs (observed)

### 1. Pinned version

```
$ npx -y rea-agents@6.5.0 --version
6.5.0
EXIT=0
```

### 2. `analyze --help`, no target

```
$ npx -y rea-agents@6.5.0 analyze --help > /tmp/rea_analyze_help.txt 2>&1; echo "EXIT=$?"
EXIT=0
```
26 lines; first line `rea analyze — Get an overview of an app`; usage `rea analyze <path> [options]`.
Full numbered surface (kept inline so a later round can diff it without re-running):

```
 1  rea analyze — Get an overview of an app
 2
 3  Usage: rea analyze <path> [options]
 4
 5  Arguments:
 6    path  App, program, or analysis database path
 7
 8  Options:
 9    --snapshot <string>                            Load and update a local analysis snapshot
10    --target-format <dos-com|raw-binary>           Explicit headerless interpretation (dos-com or raw-binary); omission preserves header-based detection
11    --architecture <6502|x86|x86_64|arm|arm64>     Caller-supplied CPU family; required with --target-format raw-binary
12    --entry-point <string>                         Caller-supplied load and entry address (0xhex); required with --target-format raw-binary
13    --provider <value>                             Bind deep analysis to a provider ID or use deterministic auto selection
14    --integrity-policy <fail|record-and-continue>  Behavior when declared application integrity does not match
15    --source-path <array>                          Exact inventoried file path relative to the application root; repeat to select several. No implicit dependencies.
16
17  Global Options:
18    --filter-output <keys>              Filter output by key paths (e.g. foo,bar.baz,a[0,3])
19    --format <toon|json|yaml|md|jsonl>  Output format
20    --full-output                       Show full output envelope
21    --help                              Show help
22    --llms, --llms-full                 Print LLM-readable manifest
23    --schema                            Show JSON Schema for command
24    --token-count                       Print token count of output (instead of output)
25    --token-limit <n>                   Limit output to n tokens
26    --token-offset <n>                  Skip first n tokens of output
```

### 3. Cache inventory (the literal `ls` in the ticket)

```
$ ls ~/.npm/_npx/*/node_modules/rea-agents/package.json
ls: cannot access '/home/vgpnk/.npm/_npx/52027bd8fc0022aa/node_modules/rea-agents/package.json': No such file or directory
/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/package.json
/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json
EXIT=2
```

Exit 2 is only the `52027…` member missing, not a failed listing. Cross-checked with
`find ~/.npm/_npx -maxdepth 3 -name rea-agents -type d` → exactly the same two directories (exit 0).
`52027bd8fc0022aa` is a **`node@22` npx cache** (`package.json` `_npx.packages: ["node@22"]`, lock
`node 22.23.3`), **not** a rea-agents install.

Versions read from each cached `package.json`:

| npx dir | version | installed (mtime) |
|---|---|---|
| `ad9a3fdbcad992c6` | **6.5.0** | 2026-10-16 12:49 |
| `a1722018f28f9df2` | **6.7.0** | 2026-10-20 11:09 |

### 4. Each cache's own binary (rules out a mislabeled tree)

```
$ node .../ad9a3fdbcad992c6/node_modules/rea-agents/scripts/rea.mjs --version
6.5.0
EXIT_650=0
$ node .../a1722018f28f9df2/node_modules/rea-agents/scripts/rea.mjs --version
6.7.0
EXIT_670=0
```

### 5. Offline run (cache-only proof)

```
$ time npm_config_offline=true npx -y rea-agents@6.5.0 --version
6.5.0

real    0m0.638s
EXIT=0
```

### 6. Artifact identity vs registry

```
$ npm view rea-agents@6.5.0 version dist.tarball dist.integrity
version = '6.5.0'
dist.tarball = 'https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz'
dist.integrity = 'sha512-C6BG7LyrAdR74mSjertM6PrxJkcNZ2bfQNOJornPo9erDEp2tyPRVYPnV5Yodr+1RqewCQla68WulXlVnveD+A=='
EXIT1=0
```

Cached lock entry (`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/package-lock.json`,
`packages["node_modules/rea-agents"]`):

```
6.5.0 sha512-C6BG7LyrAdR74mSjertM6PrxJkcNZ2bfQNOJornPo9erDEp2tyPRVYPnV5Yodr+1RqewCQla68WulXlVnveD+A==
https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz
```

Integrity strings are identical → the cached tree is byte-identical to the published 6.5.0 tarball.

### 7. Registry drift

```
$ npm view rea-agents version time.modified
version = '6.7.0'
time.modified = '2026-10-18T08:12:05.977Z'
EXIT2=0
```

### 8. Host toolchain

`node=v24.21.0 npm=11.19.0 npx=11.19.0`; `command -v rea` → empty (exit 1, no PATH binary);
`npm ls -g --depth=0` has no rea-agents (only `agent-browser@0.38.2`). Both cached 6.5.0 and 6.7.0
declare `engines.node = "^22.19.0 || ^24.11.0 || >=26.0.0"`; `bin` is `scripts/rea.mjs` under both
`rea` and `rea-agents`. 6.5.0 has 39 runtime deps, 6.7.0 has 40.

### 9. Other pins in the npm content cache

```
$ grep -rl "rea-agents/-/rea-agents-$v.tgz" ~/.npm/_cacache/index-v5
6.4.0 -> 0 entries
6.5.0 -> 1 entry
6.7.0 -> 1 entry
```

## Observations vs inference

**Observed (O):**
- O1 `npx -y rea-agents@6.5.0 --version` → `6.5.0`, exit 0.
- O2 `npx -y rea-agents@6.5.0 analyze --help` → exit 0, 26 lines, no path argument supplied.
- O3 Two rea-agents npx trees only: 6.5.0 (`ad9a…`, 2026-10-16) and 6.7.0 (`a172…`, 2026-10-20).
- O4 The `52027…` tree is `node@22`; `rea-agents` is absent there.
- O5 Offline invocation succeeds in 0.64 s.
- O6 Cached 6.5.0 tarball integrity equals the registry `dist.integrity`.
- O7 Registry still serves 6.5.0; latest is 6.7.0 (modified 2026-10-18).
- O8 Host node 24.21.0 satisfies both packages' engines; no `rea` on PATH.

**Inference (I):**
- I1 The 6.5.0 run resolved from `ad9a3fdbcad992c6`; npx hashes the request spec, and that is the only
  6.5.0 tree, whose own binary self-reports 6.5.0 (O4).
- I2 The pin is load-bearing: `npx -y rea-agents` unpinned now resolves 6.7.0 (O7), and 6.7.0 is
  already resident (O3), so dropping the `@6.5.0` suffix changes the run silently.
- I3 Replay of the corpus's many `rea-agents@6.4.0` claims (313 mentions under `LANE/corpus/`) is
  **not** offline-reproducible — no 6.4.0 tarball index entry (O9). 6.5.0/6.7.0 are.
- I4 The 6.7.0 tree's 2026-10-20 11:09 install is same-day as this round; corpus already records
  6.7.0 as the kimi MCP pin (`LANE/corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:952`). The
  lane's CLI pin remains 6.5.0 per the seat prompt and generator
  (`LANE/.ufo/waves/round-18/gen-wave1.py:299-300`); the two versions coexist without collision
  because each has its own npx tree.

## Remaining unknowns

- U1 Whether round-17/18 carrier run logs actually recorded `6.5.0` (vs an unpinned invocation) — not
  inspected here; that lives in the run envelopes, outside this seat's ticket.
- U2 Phrase of a first-pass shell expansion that echoed a `52027…/rea-agents/package.json` path;
  immediately re-tested (`ls` exit 2, `find` shows two dirs) and it does not exist. Recorded only so
  the L1 does not count a phantom third version.

## Non-actions

- No `analyze`/`search`/`decompile` against any target; no Ghidra; no carrier execution.
- No installs, upgrades, or cache mutations; no git/jj writes; only this report was created.
