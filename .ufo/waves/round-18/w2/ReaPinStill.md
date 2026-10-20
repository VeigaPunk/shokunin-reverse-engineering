HOLDS

# ReaPinStill: r18 REA argv pin and npx-cache integrity (round 18, wave 2 falsify)

- **Seat:** `KaidokuR18.ReaPinStill`, author-side advisory.
- **Revision:** REV = `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`. The lane `HEAD` = `refs/heads/main` = REV (checked with read-only `git rev-parse`). `git status --porcelain -- .ufo/waves/round-18/runs` printed nothing.
- **Anchors:** `path:line` means `git show REV:path` unless marked *host*.
- **Tags:** **OBS** means I saw it with a command listed under Commands. **INF** means inference.
- **Axes:**
  - calibration: the record matches what ran.
  - operability: a later seat can recheck it.
  - depth: what the pin proves and what it does not.

## Verdict

Both target claims hold. I tried to break each one and could not.

**T1. Every r18 REA argv uses `rea-agents@6.5.0` (OBS).**
- All 15 receipts have exactly 2 REA steps: `analyze` and `inspect-go-binary`. All 30 argvs start `["npx","-y","rea-agents@6.5.0"]`, and none deviates. No `search` steps ran.
- A negative grep for `rea-agents` not followed by `@6.5.0` under `runs/` gets 75 hits. Every hit is a bridge *path* inside a `ghidra.log`, and every path points into the 6.5.0 npx tree.
- Four further checks agree with the receipts:
  1. The producing tool defaults to 6.5.0, and no run overrode it.
  2. `carrier-run.stdout` carries the same argvs.
  3. The argv recorded in the receipt is the same list object the tool spawned.
  4. All 15 hash-bound `ghidra.log` files show Ghidra running REA bridge scripts from `~/.npm/_npx/ad9a3fdbcad992c6/`. That directory name is the first 16 hex characters of sha512(`rea-agents@6.5.0`), which is how npx names its cache directory. No other npx directory appears anywhere in `runs/`.

**T2. The cached package integrity is unchanged (OBS).**
- `npx -y rea-agents@6.5.0 --version` printed `6.5.0` and exited 0. It does the same offline and under the carrier-run env allowlist.
- The lock integrity matches the w1-recorded value and today's registry `dist.integrity`.
- Every regular file in the npx tree is byte-identical to an integrity-verified tarball, except one install-script artifact that no lock integrity covers (I1).
- No file or symlink in the tree has a ctime after the install (2026-10-16 12:49:41 -0300). That window includes the runs (16:24:07–16:32:10Z). INF from ctime semantics: the bytes that ran are the bytes I verified today.

Two gaps make this result depend on host state and leave it ungated (G1, G2 below). Neither one falsifies T1 or T2.

## T1 evidence (argv)

| What | Anchor (OBS) |
|---|---|
| `analyze` argv[2] = `rea-agents@6.5.0` | `runs/<label>/receipt.json:1922`, all 15 labels |
| `inspect-go-binary` argv[2] | `:1973` (s1246-noswiss-methods, s1246-noswiss-nomethods, s1246-swiss-methods, s1246-swiss-nethttp, s1246-swiss-nomethods, s1250-noswiss-methods, s1250-noswiss-nomethods, s1250-swiss-methods, s1250-swiss-nomethods); `:1982` (calib-notesmd-cli, real-kimi-webbridge, s1246-noswiss-nethttp, s1250-noswiss-nethttp, s1250-swiss-nethttp); `:1991` (calib-aether) |
| Stdout copy | `runs/<label>/carrier-run.stdout`, same strings one line lower (1923, 1974/1983/1992). The only diff from `receipt.json` is an added `receipt_path` key and a trailing newline |
| npx base argv | `.ufo/waves/round-17/tools/carrier-run.py:352` `["npx", "-y", "rea-agents@%s" % rea_version]` |
| Default 6.5.0 | `carrier-run.py:288` (`rea_version="6.5.0"`), `:731` (`--rea-version` default) |
| Recorded argv = spawned argv | `carrier-run.py:164,170` (`run_step`: `"argv": argv`, then `runner(argv, …)`), `:449,461` (`_run_polled`), `:97-107` (`Popen(argv, …)`) |
| No override | `run-carriers.sh:269-274` passes no `--rea-version`; `orig_argv` has none in all 15 receipts |
| Producing tool identity | `carrier-run.py` blob `37961db5…` is the same at eb6c266 and REV. Its sha256 `6665dc7a…` equals each receipt's `pins_pre` entry and `producer.json` `tool_sha256` (15/15). The `run-carriers.sh` blob `54509dfe…` is the same at eb6c266 and REV. `producer.json` `branch_tip` = `eb6c2668` (15/15). `runs/run-log.txt:1` says "at producing revision eb6c2668…" and `:32` records `run-carriers exit=0` |
| Runtime path binding | `runs/<label>/logs/rea-ghidra-*/ghidra.log:36` (all 15) gives the script dir `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/bridge/ghidra`. For example, `runs/calib-aether/logs/rea-ghidra-HtDopV/ghidra.log:239-243` runs `ReaGhidraNoReturnFix.java` and `ReaGhidraBridge.java` from there. `receipt-validate.py --require-mid-maps` over all 15 receipts exits 0, so these are the hash-bound logs |
| No npm cache redirect | `child_env_keys` has no `npm_*` key in 15/15. The `carrier-run.py:271-273` allowlist would admit `npm_config_cache`, but none was set. `~/.npmrc` and `$PREFIX/etc/npmrc` are absent (`test -e` exit 1; I did not open them). `npm config get cache` under the carrier-run allowlist returns `/home/vgpnk/.npm` |
| Claim text | `corpus/knowledge/2026-10-20-r18-swiss-map-replay.md:2` says "15 REA 6.5.0 `analyze` sessions … 16:24–16:32 UTC". This matches the receipt step window 16:24:07.220Z–16:32:10.092Z |

## T2 evidence (cache)

### How npx resolves the pinned spec

Host toolchain: npm 11.19.0, libnpmexec 10.3.2, node v24.21.0. `npx` resolves to `…/fnm/node-versions/v24.21.0/installation/lib/node_modules/npm/bin/npx-cli.js`.

- The npx dir is sha512(spec)[:16] (*host* `libnpmexec/lib/index.js:250-262`). The hashes are:
  - `rea-agents@6.5.0` → `ad9a3fdbcad992c6`
  - `rea-agents@6.7.0` → `a1722018f28f9df2`
  - unpinned `rea-agents` → `9b9809298fe40d2c`, which does not exist
- No shadow install can win:
  - The local prefix `/home/vgpnk` has no `node_modules`.
  - The global root has no `rea-agents`.
  - An npx-tree hit needs an exact `node.pkgid === spec.raw` (*host* `index.js:59`).
- `.bin/rea-agents` links to `../rea-agents/scripts/rea.mjs`. The installed `package.json` reads `rea-agents 6.5.0`.

### Integrity

- The lock entry `packages["node_modules/rea-agents"]` is:
  - version `6.5.0`
  - resolved `https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz`
  - integrity `sha512-C6BG7Lyr…veD+A==`

  The integrity string equals the one at `.ufo/waves/round-18/w1/ScoutReaPin.md:115,123` and today's `npm view` output.
- I checked all 178 lock entries:

  | Entries | Result |
  |---|---|
  | 168 | Verified against their cacache tarballs: recomputed sha512 = lock integrity, and every regular member is byte-identical. This includes `rea-agents` itself, 1650/1650 files |
  | 2 (`fast-uri` 3.1.8, `jose` 6.2.12) | Not in cacache. Verified against a fresh registry download: integrity matches, files identical (44/44 and 80/80) |
  | 2 (`incur`, `pino`) | Identical, 242/242 and 203/203. The first pass flagged them because my walker skipped `node_modules/` dirs that ship inside these tarballs |
  | 1 (`frida` 17.23.2) | 346/346 identical, plus one installed-only file, `build/frida_binding.node` (I1) |
  | 5 (`@lydell/node-pty-{darwin-arm64,darwin-x64,linux-arm64,win32-arm64,win32-x64}`) | Optional for other platforms; not installed |

- File accounting adds up: 7712 byte-identical + 1 frida artifact + 3 npm metadata files (`package.json`, `package-lock.json`, `node_modules/.package-lock.json`) = 7716, which is the `find -type f` count.

### Time binding

- `find <tree> -newerct '2026-10-16 12:50:00'` returns only two directories: the tree root and `node_modules/rea-agents/`.
- Before my checks, the tree root's mtime was `2026-10-20T16:31:10.175Z`. That is 240 ms after the last REA step started (`real-kimi-webbridge` analyze at `16:31:09.935Z`).
  - INF: npx creates and removes `concurrency.lock` on every run (*host* `index.js:268-269`, `with-lock.js:72,116`). So no `rea-agents@6.5.0` npx run touched the tree between the last r18 step and my check.
  - After my three runs, the root mtime was 13:49:52 -0300. The tree hash was the same before and after (`93e02602…1829`, 7716 files), and no lock was left behind.
- The mtime of `node_modules/rea-agents/` is 2026-10-18 18:14:01 -0300, so some entry was created or removed then (U1).
  - No package byte changed: no current entry has a later ctime, and all 1650 tarball files are present and identical.
  - The change predates w1's `npm pack` + `diff -rq`, which exited 0 (`.ufo/waves/round-18/w1/SentinelReaEnv.md:36,85`).

## Gaps

### G1 (MEDIUM; calibration and operability): the pin is observed but never gated

`receipt-validate.py --require-mid-maps` returns exit 0 with 360 checks and no findings on the REV s1246-swiss-nethttp receipt. It returns the same on a copy with both steps' `argv[2]` rewritten to `rea-agents@6.7.0`.

- The validator only checks that argv is a list (`.ufo/waves/round-17/tools/receipt-validate.py:358-363`).
- In round 18, `verify.py`, `measure.py` and `controls.py` contain no `rea-agents`/`rea_version` check (`git grep` finds only unrelated `argv` lines).
- The knowledge entry offers this validator as its read-only recheck (`corpus/knowledge/2026-10-20-r18-swiss-map-replay.md:3`). That recheck would pass a run made with a different REA, yet `:2` attributes the results to REA 6.5.0.

Smallest fix: add one assertion, in `verify.py` or as a receipt-validate flag, with two checks:
- every `steps.*.argv[:3] == ["npx","-y","rea-agents@6.5.0"]`
- every bound `ghidra.log` contains `_npx/ad9a3fdbcad992c6/`

Reproduce (read-only; uses `/dev/fd`, writes no file):

```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps <(git show b2aad08ceeee8dd125ce0d316056d8bd766c7f94:.ufo/waves/round-18/runs/s1246-swiss-nethttp/receipt.json | python3 -I -B -c 'import json,sys; r=json.load(sys.stdin); [s["argv"].__setitem__(2,"rea-agents@6.7.0") for s in r["steps"].values()]; print(json.dumps(r))'); echo "exit=$?"
# observed: counts {"invalid":0,"receipts":1,"unreadable":0,"valid":1}, checks_performed 360, findings [], exit=0 (unmutated receipt: identical)
```

### G2 (LOW; calibration): receipts bind REA by spec string, not by bytes

- Receipt top-level keys (`bound_sessions` … `unbound_sessions`) and `producer.json` keys (`branch`, `branch_tip`, `label`, `recorded_at_utc`, `tool_sha256`) record no node or npm version, no npx realpath, and no lock integrity.
- `git grep -c -F 6.5.0` over `runs/*/{analyze.json,inspect-go.json,analyze.stderr,inspect-go.stderr}` matches 0 files. REA's output identifies only Ghidra (`"version":"12.1.4"`).
- w1 already raised this as F3 (`.ufo/waves/round-18/w1/SentinelReaEnv.md:33-37`). I found no disposition at REV: `git grep` for `SentinelReaEnv|REA bytes|lock(file)? integrity` outside w1 finds nothing in round 18.
- So T2's byte-level binding rests on live host state (ctime, cacache) that is not in Git. It is lost at the next reify or cache clean.
- The ghidra.log path binding from T1 check 4 is in Git, but it names a directory, not bytes.

Smallest fix: the F3 remedy. Record `node --version`, `npm --version`, `realpath $(command -v npx)`, and the npx-tree lock integrity (or this report's tree hash) in each receipt.

## Info

- **I1.** `node_modules/frida/build/frida_binding.node` is a frida install-script product (`hasInstallScript: true`) and no lock integrity covers it.
  - sha256 `5b2db5ae57c058ad0765e627d9d9c9c98e4e90c09746c6f727b7a80769eed7a5`, 112,775,824 B.
  - mtime 2026-10-09 10:26:09 -0300, ctime 2026-10-16 12:49:41 -0300, so by ctime it is unchanged since install.
  - I did not trace whether `analyze` or `inspect-go-binary` load it (U2).
- **Caret range.** The npx-tree root `package.json` records `"rea-agents": "^6.5.0"` with `_npx.packages ["rea-agents@6.5.0"]`. This does not affect pinned runs, because npx needs an exact pkgid match (*host* `index.js:59`). INF: a future reify of that tree could float within `^6`.
- **6.7.0 tree.** The root mtime of `a1722018f28f9df2` is 2026-10-20 13:45:44 -0300, after the r18 window, so some host process ran the 6.7.0 spec after the runs. The pinned spec cannot select that tree.
- **Live MCP process.** `npm exec rea-agents@6.5.0 mcp` (pid 3221, started 2026-10-20 09:57:31 -0300) shares the 6.5.0 tree.
- **Harness glob bug.** In the tool shell, `runs/*/receipt.json` expanded to 16 paths, including the nonexistent `runs/run-log.txt/receipt.json`. `bash -c` gives 15. I reported it to `xd://report_issue`. Rechecks of the 15 receipts should run the glob through `bash -c`.

## Commands (exit codes as observed)

LANE = `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, REV as above, D = `~/.npm/_npx/ad9a3fdbcad992c6`. All lane reads were read-only.

```
git -C LANE rev-parse --verify 'REV^{commit}'                                        # 0
git -C LANE rev-parse HEAD refs/heads/main                                           # 0 (both = REV)
git -C LANE status --porcelain -- .ufo/waves/round-18/runs | wc -l                   # 0: 0 lines
git -C LANE grep -n -o -E 'rea-agents@[^" ,\\]*' REV -- .ufo/waves/round-18/runs     # 0: all hits rea-agents@6.5.0
git -C LANE grep -o -F rea-agents@6.5.0 REV -- .ufo/waves/round-18/runs | wc -l     # 0: 60 (30 receipt.json + 30 carrier-run.stdout)
git -C LANE grep -n -P 'rea-agents(?!@6\.5\.0)' REV -- .ufo/waves/round-18/runs | wc -l   # 0: 75, all ghidra.log bridge paths (grep -v of the bridge path: count 0)
git -C LANE grep -n -P '_npx/(?!ad9a3fdbcad992c6/)' REV -- .ufo/waves/round-18/runs  # 1 (no other npx dir)
git -C LANE grep -l -F _npx/ad9a3fdbcad992c6/node_modules/rea-agents/bridge/ghidra REV -- '.ufo/waves/round-18/runs/*/logs/*/ghidra.log' | wc -l   # 0: 15
python3 -I -B - <<EOF (walk every "argv" key in the 15 REV receipts via git show)   # 0: total_argv 30, nonconforming 0; no --rea-version; no npm_* env keys; all step exits 0
diff <(git show REV:.ufo/waves/round-18/runs/s1246-swiss-nethttp/carrier-run.stdout) <(git show REV:.ufo/waves/round-18/runs/s1246-swiss-nethttp/receipt.json)   # 1: only receipt_path + EOF newline
git -C LANE show {9011581,eb6c266,REV}:.ufo/waves/round-17/tools/carrier-run.py | sha256sum   # 0: 953373e5… / 6665dc7a… / 6665dc7a…
git -C LANE rev-parse {eb6c266,REV}:.ufo/waves/round-18/run-carriers.sh {eb6c266,REV}:.ufo/waves/round-17/tools/carrier-run.py   # 0: 54509dfe…/37961db5… at both
cd LANE/.ufo/waves/round-18 && npx -y rea-agents@6.5.0 --version                     # 0: 6.5.0
env -i PATH HOME LANG USER LOGNAME TMPDIR=/tmp NODE_DISABLE_COMPILE_CACHE=1 npx -y rea-agents@6.5.0 --version   # 0: 6.5.0
npm_config_offline=true npx -y rea-agents@6.5.0 --version                            # 0: 6.5.0
npm view rea-agents@6.5.0 version dist.integrity dist.tarball --json                 # 0: sha512-C6BG7Lyr…veD+A==, rea-agents-6.5.0.tgz
python3 -I -B -c '…D/package-lock.json packages["node_modules/rea-agents"]…'        # 0: 6.5.0, resolved, same integrity; root dep ^6.5.0
git -C LANE grep -n -F "$lock_integrity" REV -- .ufo/waves/round-18/w1/ScoutReaPin.md   # 0: :115, :123
find D -type f | wc -l ; find D -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum   # 0: 7716 ; 93e02602005ebc5e…1829 (same before and after my npx runs)
find D -newerct '2026-10-16 12:50:00' -printf '%y %C+ %p\n'                          # 0: 2 directories only
python3 -I -B - (178 lock entries vs ~/.npm/_cacache/content-v2 tarballs, in memory)   # 0: ok 168, not-installed 5, no-cacache 2, content-diff 3 (resolved by the next two)
python3 -I -B - (incur/pino/frida member-by-member)                                  # 0: 242/242, 203/203, 346/346 (+ frida_binding.node)
curl -fsSL <resolved> | python3 -I -B -c … (fast-uri, jose)                          # 0/0: integrity True; 44/44, 80/80
printf '%s' rea-agents@6.5.0 | sha512sum | cut -c1-16                                # 0: ad9a3fdbcad992c6
npm prefix ; npm prefix -g ; npm config get cache ; ls "$(npm root -g)"              # 0: /home/vgpnk (no node_modules), fnm install prefix, /home/vgpnk/.npm, no rea-agents
test -e ~/.npmrc ; test -e <fnm prefix>/etc/npmrc                                    # 1 ; 1
bash -c 'python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps .ufo/waves/round-18/runs/*/receipt.json'   # 0: valid 15/15
receipt-validate on REV receipt, unmutated / 6.7.0-mutated (G1 command)               # 0 / 0
```

## Residual unknowns

- **U1.** What created or removed an entry in `D/node_modules/rea-agents/` at 2026-10-18 18:14:01 -0300. It had no byte effect (see T2).
- **U2.** Whether REA `analyze` or `inspect-go-binary` loads `frida_binding.node`, the one file no integrity covers.
- **U3.** The ctime argument assumes no clock manipulation or subvolume rollback on the host. It cannot be attested from Git.

## Install and write record

- No installs or updates.
- I wrote only this file, plus one harness note to `xd://report_issue`.
- Host side effects:
  - My three npx runs contacted the registry (preferOnline, *host* `index.js:30`). Each created and removed `D/concurrency.lock`, so the root mtime moved; the file tree hash did not change.
  - `npm view` and the two `curl` tarball reads stayed in memory.
- Not done: no REA analyze/search/decompile, no Ghidra, no carrier executed, no git/jj writes.
