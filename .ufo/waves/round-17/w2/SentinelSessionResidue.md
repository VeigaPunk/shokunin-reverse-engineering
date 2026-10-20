# W2 SentinelSessionResidue — host residue after the eight round-17 carrier runs

Seat: author-side advisory sentinel (KaidokuR17.SentinelSessionResidue). Lane revision `da64646` (`git rev-parse HEAD` → `da64646adcb19c1ede7537b799b8c7d283fe43da`).
Axes: calibration (each severity matches observed impact) and depth (each claim reproduced on the host).
Scope: `/tmp/kr17-rea-*`, surviving `rea-ghidra-*`/`session.json`, and orphan java/Ghidra processes. Mode: read-only.
One scratch probe (F3) created `/tmp/kr17-rea-55swkalm`. I removed it myself with `rmdir`. I deleted nothing else. No installs.

## Verdict
- No secret residue and no orphan processes.
- The cleanup path at `tools/carrier-run.py:360-367` never ran: 8/8 runs left their private root in place. The same code also fails open: a leaked session dir would not change the exit code.

## F1 — Low (disk/hygiene): all 8 private roots survive, because npm's compile cache keeps `rmdir` from ever running
- **Evidence [OBS]:** `jq -c '{session_parent, leftovers:.session_parent_leftovers}' runs/*/receipt.json` returns `"leftovers":["node-compile-cache"]` for all 8 runs (`/tmp/kr17-rea-{y138m4zi,1cqz92us,odi4abuq,0o3ukbw2,5l3r8v9k,l9k4m3ex,g39lajwh,_qnkq6vy}`).
  - On the host, each root is `drwx------` and holds 535 files under `node-compile-cache/v24.21.0-x64-964aae3f-1000/`. The non-cache entry count is 0 for every root.
  - `du -sch /tmp/kr17-rea-*` → `21M total`.
- **Cause [OBS]:**
  - `carrier-run.py:366-367` calls `os.rmdir(private_root)` only when `leftovers == []`.
  - npm 11.19.0 runs `enableCompileCache()` unconditionally. See `~/.local/share/fnm/node-versions/v24.21.0/installation/lib/node_modules/npm/lib/cli.js:2-5`.
  - With `TMPDIR=private_root` (`carrier-run.py:264-265`), that cache lands inside the root.
  - The cache holds npm's own modules: `grep -rl -a npm` matches 535/535 files and `rea-agents` matches 0.
- **Content check [OBS]:**
  - `grep -rl -a -E '[0-9a-f]{64}'` finds 0 files in all 8 caches.
  - The 7 hits on `token|session.json|kr17|/usr/bin/op` are npm/postcss identifiers and help text (for example `postcss-selector-parser/dist/tokenize.js`). None is a value.
  - The file sets are identical across runs (`cmp` of the y138m4zi and _qnkq6vy listings → `same-file-set`).
- **Impact:** about 2.6 MB per run accumulates under `/tmp`. The private-root lifecycle that w1 asked for (`w1/SentinelPollRace.md:58`) is dead in practice. There is no confidentiality impact.
- **Smallest fix:** in `carrier-run.py`, after line 265, add `child_env["NODE_DISABLE_COMPILE_CACHE"] = "1"`. Also record it in the receipt, next to `rea_ghidra_env` at `:287-288`.
  - Verified on this node: `NODE_DISABLE_COMPILE_CACHE=1 node -p "require('node:module').enableCompileCache('/tmp/kr17-ssr-probe-nonexist')"` → `{ status: 3, message: 'Disabled by NODE_DISABLE_COMPILE_CACHE' }`. The directory was not created.
  - Alternative: `shutil.rmtree` only the `node-compile-cache` entry, and only when the leftovers are exactly `['node-compile-cache']`.

## F2 — Medium (correctness, fail-open) / Low (security): a leaked `rea-ghidra-*` session dir still gives exit 0
- **Evidence [OBS]:**
  - `carrier-run.py:365` only records `session_parent_leftovers`. The exit logic at `:376-383` never reads it.
  - Nothing else checks it either: `grep -rn 'leftover\|session_parent' tools/ contract.md claims.json` (excluding carrier-run.py) → no hits. So `receipt-validate.py` does not check it.
  - The w1 remediation said the cleanup "fails loudly if REA leaked a dir; record that, don't hide it" (`w1/SentinelPollRace.md:58`). The code records the leak but hides it from the exit code.
- **Exploit/failure path [INFERENCE from REA 6.5.0 source, `~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/ghidra/`]:**
  - REA keeps the runtime root when process cleanup fails closed (`GhidraClient.js:600-603`) or when root removal fails (`:664-670`, `ProviderCleanupError`).
  - That root holds `session.json`, which contains the 32-byte bearer `token` (`GhidraLauncher.js:95-98,447`; generated at `GhidraClient.js:430`). It may also hold the 0600 target snapshot copy.
  - The bound log is still copied, so `len(bound)==1` (`:381`) passes and the run reports exit 0, i.e. clean.
  - Reach is same-uid only: both the parent and REA's root come from owner-only `mkdtemp` (`process/PrivateRuntimeRoot.js:38-39`). The token is useless once the JVM is dead.
- **Not observed in these runs:** none of the 8 roots holds a `rea-ghidra-*` entry (F1 count).
- **Smallest fix:** after the F1 fix, add `if private_root is not None and leftovers: return receipt, 2` before `return receipt, 0` at `:383`. Keep the root on disk as evidence; do not delete it.

## F3 — Low (hygiene): early-error returns leak an empty private root that no receipt records
- **Evidence [OBS]:**
  - `mkdtemp` runs at `carrier-run.py:263`, before the early `return receipt, 2` exits at `:282` (pins), `:291` (carrier unreadable) and `:296` (out-dir).
  - None of those exits reaches the `rmdir` at `:367`, and there is no `try/finally`.
- **Reproduction (no REA invoked: the return at `:291` comes before any step):**
  ```
  python3 -I -B tools/carrier-run.py --carrier /nonexistent/kr17-ssr-carrier --label ssr-probe --out-dir /tmp/kr17-ssr-out
  → "error": "carrier unreadable: ...", "session_parent": "/tmp/kr17-rea-55swkalm"; exit=2
  ls -d /tmp/kr17-rea-* | comm -13 before -  → /tmp/kr17-rea-55swkalm
  ```
  No `receipt.json` is written, so the stray dir can only be traced from stdout. I removed it (`rmdir`); 8 roots remain.
- **Smallest fix:** move lines 259-267 to after the `:296` out-dir check, or wrap the body in `try/finally` and `rmdir` the root when it is empty.

## F4 — Info (provenance, outside this axis): `runs/run-log.txt` lists 7 of the 8 runs
- **[OBS]** `runs/run-log.txt:1` starts with `calib-esbuild-0.25.12 start 10:47:42`. The `calib-shfmt` start/end lines are missing.
- Yet `runs/calib-shfmt/receipt.json` shows `analyze` running 13:47:06–13:47:37Z (`carrier-run.exit`=0, `compare.exit`=0). Root `y138m4zi` has mtime 10:47, and `calib-shfmt` is row 1 of `predictions/carriers.tsv`.
- `run-carriers.sh` never writes the log itself (`:18,:30` echo to stdout), so the lines were lost when stdout was captured.
- **Fix:** re-derive the missing lines from the receipt timestamps, or label `run-log.txt` as partial.

## Bounded no-findings (checked, nothing found)
- **Surviving session dirs/tokens:**
  - `find /tmp -maxdepth 6 \( -name 'rea-ghidra-*' -o -name session.json -o -name '*.gpr' -o -name '*.rep' \)` → only `/tmp/kr17-pilot/logs/rea-ghidra-LuPZRm` and `/tmp/kr17-pilot/logs2/rea-ghidra-r9xmGu`. Those are copies holding only `ghidra.log` and `script.log`.
  - Their sha256 is byte-identical to `pilot/shfmt-log/ghidra.log` (`aaf677ed…`) and `pilot/esbuild-0.25.12-log/ghidra.log` (`f6b61152…`).
  - There is no `session.json` anywhere. The only unreadable dirs are the `systemd-private-*` ones.
  - No `rea-ghidra-socket-*` dirs exist. The socket path fits in 107 bytes, so REA never needed one (`GhidraTransport.js:12-14`).
- **Token leakage into lane artifacts:**
  - The retained `runs/*/logs/*/ghidra.log` files contain the `session.json` path only (for example `pro-op/.../ghidra.log:113`).
  - `grep -o -E '\b[0-9a-f]{64}\b'` over all retained ghidra/script logs → 0 hits.
  - `token` occurs 0 times in all `receipt.json` and `carrier-run.stdout` files.
  - The single `secret` hit is the dependency name `gsterjov/go-libsecret` in `pro-op/inspect-go.json`, which is carrier data.
  - The receipt env capture is limited to `REA_GHIDRA_*` (`carrier-run.py:287-288`).
- **Orphan processes:**
  - `pgrep -a -f 'java|ghidra|AnalyzeHeadless|GhidraBridge|rea-agents'` → only earlyoom (whose argv contains the word `java`) and pid 3221 `npm exec rea-agents@6.5.0 mcp`.
  - pid 3221 belongs to the `omp` session pid 3092. It started at 09:57:31, boot plus 23 s and before the runs. Its child is `3234 node …/.bin/rea mcp`, which has no children (`pgrep -P 3234` rc=1). It is host MCP, not run residue; do not kill it.
  - No process has an fd or cwd under `/tmp/kr17-rea-*` (`find /proc/*/fd /proc/*/cwd -lname '/tmp/kr17-rea-*'` → 0).
- **Selftest temp dirs:** no `/tmp/*selftest-*` or `/tmp/buildinfo-probe-*` remain. Every `mkdtemp` in `tools/*.py` has a cleanup step: rmtree, `rm -rf` (`temporal-sweep.py:365`) or walk plus rmdir (`buildinfo-probe.py:596-602`).

## Safe cleanup for L1 (your runs only)
Each target is derived from the receipts, and the command removes a root only if it holds nothing but the cache:
```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17
for d in $(jq -r '.session_parent' runs/*/receipt.json); do
  case "$d" in /tmp/kr17-rea-*) ;; *) continue;; esac
  [ "$(ls -A -- "$d")" = node-compile-cache ] && rm -rf -- "$d/node-compile-cache" && rmdir -- "$d"
done
```
Optional: `rm -rf /tmp/kr17-pilot`, which is the L1 pilot cwd. Its logs are duplicated byte-for-byte in `pilot/`; check `pilot/SHA256SUMS` first.

**Do NOT delete:**
- `/tmp/node-compile-cache`: shared and live. omp's MCP npm (pid 3221) created it at 09:57 and was still writing it at 11:08.
- Other seats' scratch:
  - `/tmp/kr17-{gocache,gover,ghidra,src}`: `w1/DraftSourcesRows.md:43`.
  - `/tmp/ghidra-hist` and `/tmp/gr17-*`: `w1/ScoutGhidraUpstreamGo.md:134`.
  - `/tmp/rea-go.json`: `w1/ConnAdjacencyReport.md:85`.
  - `/tmp/ghidra-{base-src,go-src,probe,master-files.txt}`, `/tmp/kr17-{dl.json,hdrs.txt,release.html,*.err}`.
  - `/tmp/tabi-selftest-stdout.txt`.
  
  Their owners should clean these up.
