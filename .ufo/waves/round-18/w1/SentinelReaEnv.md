# SentinelReaEnv — REA run hygiene for the 10 planned r18 carrier runs

Seat `KaidokuR18.SentinelReaEnv` (author-side advisory). Axes: calibration, operability, depth.
I wrote only this file. I installed nothing. I ran no REA analyze/search/decompile, no Ghidra, and no carrier.
Scratch went under `/tmp/kr18-sentinel-*` and was removed afterwards (`ls -d /tmp/kr18-sentinel-*` → none).
Tags: **OBS** = I saw it with the command shown. **INF** = my inference.

Files reviewed:
- `LANE/.ufo/waves/round-17/tools/carrier-run.py`, sha256 `953373e5…3fb0`. `git diff --stat refs/heads/main -- <file>` printed nothing (exit 0), so the file is unchanged from B `9011581d`. The `map_sha256` C3 edit had not landed when I read it. All `:N` anchors below refer to this version.
- `LANE/.ufo/waves/round-18/carriers/build.sh`, sha256 `29384ed8…553e`. It is untracked (`??`).
- REA 6.5.0 installed at `~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` (`REA/` below).
- npm 11.19.0 / node v24.21.0 under fnm (`NPM/` = `~/.local/share/fnm/node-versions/v24.21.0/installation/lib/node_modules/npm`).

## Verdict
None of the five named surfaces leaks a secret on the success path. I found one MEDIUM gap in process cleanup. It applies only on the timeout path, which r17 never exercised. I also found three LOW gaps and two INFO notes. Toolchain provenance holds end to end: go.dev JSON → tarball → extracted tree → byte-identical rebuild of all 8 carriers.

## Findings

### F1 — MEDIUM (operability) — the timeout SIGKILL does not reach the Ghidra JVM, so the JVM, `session.json` (bridge token) and `bridge.sock` can outlive the run
- **OBS:** carrier-run starts npx in its own session (`carrier-run.py:104-105` `start_new_session=True`). On timeout, `_stop_group` signals only that group: `os.killpg(proc.pid, SIGTERM)`, waits 15 s, then `killpg(..., SIGKILL)` (`:114-120`).
- **OBS:** REA starts the JVM in a different group. It calls `spawn(..., {detached: platform !== "win32"})` (`REA/dist/process/ProviderProcess.js:56`), and `processGroupId: pid` (`:68`) records the JVM as its own group leader. A killpg on the npx group therefore never signals the JVM.
- **OBS:** REA traps SIGTERM and turns it into an abort (`REA/dist/cli-runtime/cli.js:923-928`). The 15 s grace normally lets REA close its own provider (INF: graceful path cleans; not exercised). The SIGKILL branch skips that cleanup.
- **OBS:** After a SIGKILL, the run only records the leftovers. If `session_parent_leftovers` is non-empty, `:403-410` keeps the root and `:431-433` returns 2. It never looks for or kills surviving PIDs. `run-carriers.sh:17-38` (W17, to be adapted) then moves on to the next carrier.
- **Exploit/failure path (INF):** a stuck analysis on carrier *k* hits the 1500 s timeout and REA misses the 15 s close. An orphaned Ghidra JVM keeps analysing next to carrier *k+1*. That skews timing and memory for later runs. Meanwhile `/tmp/kr17-rea-*/rea-ghidra-*/session.json` (mode 0600, holding `token`, `REA/dist/ghidra/GhidraLauncher.js:95-106`) stays usable together with the live `bridge.sock`. Any same-uid process can use them, and this host runs about 200 peer agents. Per-run private roots keep the logs from cross-binding.
- **r17 exposure (OBS):** in 8/8 receipts, every step has `timeout:false`, `stop:null` and `exit:0` (jq over `runs/*/receipt.json`). The path has never run.
- **Smallest remediation:** when `_stop_group` returns `"sigkill"` (and again just before the leftovers check), scan `/proc/*/cmdline` for `private_root`. The JVM's argv contains `-Djava.io.tmpdir=<runtimeRoot>/tmp` and the descriptor path, both under it. `killpg(os.getpgid(pid), SIGKILL)` each match, and record `{pid, pgid}` in the step as `orphans_killed`.

### F2 — LOW (trust boundary) — the log copy can follow a symlink swapped in after the check
- **OBS:** `LogPoller.scan` checks `os.path.isfile(src) and not os.path.islink(src)` (`:224`) and then calls `open(src, "rb")` (`:226`), which follows symlinks.
- **Exploit path (INF):** this needs a same-uid writer inside the 0700 runtime root, which in practice means a compromised Ghidra JVM (a parser bug triggered by a hostile carrier). Swapping `ghidra.log` to a symlink to `session.json` between the two calls would copy the 64-hex token into `out_dir/logs/` and from there into Git.
- **Smallest remediation:** `fd = os.open(src, os.O_RDONLY | os.O_NOFOLLOW)`, require `stat.S_ISREG(os.fstat(fd).st_mode)`, and read from that fd.

### F3 — LOW (calibration/provenance) — receipts do not bind the REA bytes that ran
- **OBS:** the only REA identity in a receipt is the argv spec `npx -y rea-agents@6.5.0` (`:350`). Running `grep -o '6\.5\.0' runs/pro-aether/analyze.json | wc -l` gives `0`. REA's own output carries only `"version":"12.1.4"` (Ghidra).
- **OBS:** which npx runs depends on the inherited `PATH` (`:269`). Here it resolves through an fnm multishell symlink, `/run/user/1000/fnm_multishells/<id>/bin/npx` → `NPM/bin/npx-cli.js`. libnpmexec calls `pacote.manifest(spec, {preferOnline: true})` (`NPM/node_modules/libnpmexec/lib/index.js:28-30`), so every step contacts the registry. Over 10 runs with at least 2 steps each, that is at least 20 contacts.
- **OBS (bytes are right today):** the lockfile integrity is `sha512-C6BG7Lyr…veD+A==` (`~/.npm/_npx/ad9a3fdbcad992c6/package-lock.json`), and `npm view rea-agents@6.5.0 dist.integrity` returns the same value (exit 0). I ran `npm pack rea-agents@6.5.0` into a mkdtemp; `openssl dgst -sha512 | base64` gave the same digest, and `diff -rq x/package <installed>` exited 0.
- **Smallest remediation:** record in the receipt `node --version`, `npm --version`, the `realpath` of the npx used, and the npx-cache `package-lock.json` integrity for `node_modules/rea-agents`. Optionally add `--prefer-offline` to `npx_base`.

### F4 — LOW (env allowlist) — the `REA_GHIDRA_*` prefix lets analysis-altering knobs through, including a JAR loaded into Ghidra
- **OBS:** `child_environment` keeps every key where `k.startswith("REA_GHIDRA_")` (`:280`). REA 6.5.0 reads `REA_GHIDRA_{COMPILER_SPEC_ID,DISABLED_ANALYZERS,LANGUAGE_ID,NATIVEAOT_JAR,SEED_FILE,STARTUP_TIMEOUT_MS}` (grep over `REA/dist/cli-runtime/*.js`). NativeAOT recovery is limited to Linux x86-64 ELF or native PE targets on Linux (`binary-BVOr2mgE.js:3343-3346`), which covers all 10 carriers.
- **Mitigation present (OBS):** the values are written to `rea_ghidra_env` (`:324-325`). In r17 this was `{}` in 7/8 runs and `{"REA_GHIDRA_STARTUP_TIMEOUT_MS":"900000"}` in pro-op. No gate checks it.
- **Exploit path (INF):** an ambient `REA_GHIDRA_DISABLED_ANALYZERS` or `…_NATIVEAOT_JAR` in the L1 shell would quietly change the Go outcome being measured, or load third-party code into the JVM.
- **Smallest remediation:** allow exactly `REA_GHIDRA_STARTUP_TIMEOUT_MS`, and return 2 with `unexpected_rea_ghidra_env` when any other `REA_GHIDRA_*` is set.

### F5 — INFO — `child_env_keys` understates the environment REA and Ghidra actually receive
- **OBS:** I re-ran the carrier-run allowlist (`env -i PATH HOME LANG USER LOGNAME TMPDIR NODE_DISABLE_COMPILE_CACHE`) with `npx -y --package=rea-agents@6.5.0 -c env`. It exited 0, and npm had added 30 keys (37 in the child env vs 7 passed in):
  - `COLOR`, `EDITOR`, `INIT_CWD`, `NODE`, `PWD`, `SHLVL` and `_`;
  - 15 `npm_config_*` keys;
  - `npm_command` and `npm_execpath`;
  - `npm_lifecycle_{event,script}`;
  - `npm_node_execpath` and `npm_package_{json,name,version}`.

  Observed values: `npm_config_local_prefix=/home/vgpnk` and `npm_package_name=@1password/oph`, the name in `/home/vgpnk/package.json`, because no lane-level or fleet-level `package.json` exists (`ls` confirmed). `npm_package_json=/home/vgpnk/Projects/shokunin/package.json` points at a file that does not exist; that path came from my cwd. The L1's cwd, the W17/W18 directory, would yield a different path. INF: REA and the JVM receive this metadata. It is harmless but unrecorded.
- REA hands its environment on to the JVM: `ghidraJavaEnvironment` spreads it (`REA/dist/ghidra/GhidraInstallation.js:290-297`), and `ProviderProcess.js:26-31` adds `REA_PROCESS_RUN_ID`. The CLI supplies it as `environment: input.environment` (`binary-BVOr2mgE.js:8558`). INF: `input.environment` is `process.env`; I did not trace it to the definition.
- No value matched `token|auth|secret|passw` except the package name. `~/.npmrc` is absent (`test -e` only; not opened). So nothing leaks today. The gap is that the receipt cannot show this.
- Smallest fix: document it in the receipt limits. No code change is needed.

### F6 — INFO (operability) — `build.sh` states the toolchain digests but does not recreate them
- **OBS:** the toolchain digests appear only in comments (`build.sh:3-4`). The download, verify and extract steps are not in the recipe, and the tarballs exist only in `/tmp/kr18-dl/` (mode 755, owner vgpnk). That directory does not survive a reboot.
- Smallest fix: add a `fetch-toolchains` stanza (curl, `sha256sum -c`, `tar -C`), or a sibling `TOOLCHAINS.sha256`.

## Surfaces with no finding (all OBS)
| Surface | Evidence |
|---|---|
| `session.json` bridge-token exclusion | Only `LOG_NAMES = ("ghidra.log","script.log")` are copied (`:40`, `:221`). REA writes the token only to `session.json` (`GhidraLauncher.js:95-106`, `:447`; token = `randomBytes(32).toString("hex")`, `binary-BVOr2mgE.js:5956`). The bridge Java sources never print or log the token (`grep token REA/bridge/ghidra/*.java \| grep -i 'print\|log\|write'` exit 1). r17 log dirs hold `8 ghidra.log` + `8 script.log` and nothing else. `find runs -name session.json -o -name ownership.json -o -name '*.tmp' -o -name bridge.sock` finds nothing. Every 64-hex string in the r17 receipt, analyze and inspect JSON sits under a digest key (`sha256`, `sha256_pre/post`, `stdout/stderr_sha256`, `digest`, `evidence_id`). |
| Private TMPDIR | `tempfile.mkdtemp(prefix="kr17-rea-", dir="/tmp")` creates a 0700 root (`:299`), exported as `TMPDIR` (`:281`). The glob is scoped to it (`:303`). REA uses an inherited TMPDIR when it has no dot element (`GhidraSessionRoot.js:28-31`). The socket falls back to `/tmp` only above 107 bytes (`binary-BVOr2mgE.js:5333-5345`); this path is about 50 bytes, so it stays in the root. All 8 r17 receipts show `session_parent=/tmp/kr17-rea-*`, `leftovers []`, `unbound []` and `bound 1`. Right now there are no `/tmp/kr1[78]-rea-*` and no `/tmp/rea-ghidra-*` (`ls`, count 0). **Unrelated live process:** `pgrep -af` shows pid 3221 `npm exec rea-agents@6.5.0 mcp`. It shares global `/tmp`, which is why the private root matters. |
| No carrier execution | The argv is only `npx … inspect-go-binary\|analyze\|search <carrier>` (`:354-383`). REA's Go inspector imports no `child_process`/`execFile`/`spawn` (`grep -l` over `REA/dist/go/*.js` exit 1). `build.sh` only runs `go build` and `sha256sum` (`:19-26`), under `env -i`, with `GOTOOLCHAIN=local`, `GOENV=off` and `CGO_ENABLED=0`, and `go.mod` has no `require`. That rules out a toolchain or module download. |
| Toolchain provenance | See the command log. The tarball sha256s match my own fetch of the go.dev JSON. `tar -d` reports only Uid/Gid differences (14175 and 14496 entries), plus one "Cannot stat" on the empty root name. There is no `Contents/Size/Mode differs`. The member lists are identical to `find` output (diff exit 0). `VERSION` reads `go1.24.6` / `go1.25.0`. An independent `OUT=$(mktemp -d) bash build.sh` rebuild matches `SHA256SUMS` 8/8 (diff exit 0). |
| Calibration carriers | `sha256sum -c` against the r17 `carrier.sha256_pre` values: `/usr/bin/aether: OK`, `/home/vgpnk/.local/bin/notesmd-cli: OK` (exit 0). |

## Command log (exit codes as observed)
```
sha256sum /tmp/kr18-dl/go1.24.6.linux-amd64.tar.gz /tmp/kr18-dl/go1.25.0.linux-amd64.tar.gz   # exit 0
  bbca37cc395c974ffa4893ee35819ad23ebb27426df87af92e93a9ec66ef8712  go1.24.6
  2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613  go1.25.0
curl -sS --compressed 'https://go.dev/dl/?mode=json&include=all' -o <tmp>                      # exit 0 (2256879 B, sha256 6b83804b…5950)
jq '…go1.24.6|go1.25.0 linux-amd64.tar.gz…'                                                     # exit 0; same two sha256, kind=archive, sizes 78583176 / 59659213
jq same filter on L1's /tmp/kr18-dl/dl.json                                                     # exit 0; identical digests
tar -d -z -f go$v.tar.gz -C ~/.local/opt/go-$v --strip-components=1                            # exit 1 (uid/gid only, see above)
diff <(tar -tzf … | normalise) <(find ~/.local/opt/go-$v …)                                     # exit 0 for both
OUT=$(mktemp -d) bash round-18/carriers/build.sh; diff vs ~/.local/share/kaidoku-r18/carriers/SHA256SUMS  # build exit 0, diff exit 0
cd ~/.local/share/kaidoku-r18/carriers && sha256sum -c SHA256SUMS                               # 8× OK, exit 0
jq -r '.packages["node_modules/rea-agents"]…' ~/.npm/_npx/ad9a3fdbcad992c6/package-lock.json   # exit 0: 6.5.0 sha512-C6BG7Lyr…veD+A==
npm view rea-agents@6.5.0 dist.integrity dist.tarball --json                                    # exit 0: same integrity
npm pack rea-agents@6.5.0 (mkdtemp); openssl dgst -sha512 -binary | base64; diff -rq x/package <installed>  # same digest; diff exit 0
env -i PATH HOME LANG USER LOGNAME TMPDIR NODE_DISABLE_COMPILE_CACHE npx -y --package=rea-agents@6.5.0 -c env  # exit 0 (F5)
jq -c '[.steps[]|{t:.timeout,s:.stop,e:.exit}]' round-17/runs/*/receipt.json                    # 8× all false/null/0
sha256sum -c <r17 aether+notesmd sha256_pre>                                                    # OK OK, exit 0
git -C LANE diff --stat refs/heads/main -- .ufo/waves/round-17/tools/carrier-run.py             # empty, exit 0
```

## Install record
None.
