<!-- corpus entry — kaidoku-shokunin round 4 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r4/07-jsc-bytecode.md. -->

# 07 — Typora `atom.compiled.dist.jsc` bytenode surface probe (round-4)

Axes: coverage (first byte-level characterization of the 388KB blob that is
99.4% of app.asar — a surface no REA verb reaches, per r3), verifiability
(every header field decoded twice: manual od + jscd `info`), reachability
(version-matched V8 host actually obtained ON THIS HOST — not a hypothetical),
frontier-mapping (ranked cheapest paths to decompiled JS).

## Candidate: `atom.compiled.dist.jsc` extracted — V8 code-cache blob, webpack bundle inside

- claim: `npx -y @electron/asar extract-file` from a `/tmp/jsc-probe` cwd
  produced 388,080 B (of 390,514 B app.asar = 99.38%; archive holds only
  this file + `launch.dist.js` + `package.json`, Typora 1.14.9).
  sha256 `6a0cb7b32270498ed190c589ca29c990a0e4b5f06f0cd6a5516e19a715c2dfe9`,
  `file`: bare `data`. First 32 B:
  `c3 06 de c0 11 2c 84 76 de 9f 03 00 99 0e 36 24 cb ff b0 33 d0 eb 05 00 …`
  — little-endian magic `0xC0DE06C3` = V8 serialized code-cache header.
  jscd `info` decodes: version_hash `0x76842c11`, source_hash `0x00039fde`
  (orig source length 237,534 B, non-module), flag_hash `0x24360e99`,
  ro_checksum absent, payload at offset 24. Entropy 6.2911 bits/byte, all
  256 byte values present, 0x00 dominant (82,829×) — structured serialized
  data, NOT packed/encrypted. String table is serialized inline:
  `strings -a -n 6` → 2,187 strings incl. `__webpack_modules__`,
  `__webpack_require__`, `ipcMain`, `BrowserWindow`, and Typora-domain
  surface: `addLicense`, `abnerworks.Typora`, `checkForUpdates`,
  `autoHideMenuBar`, `current-theme\.css$`,
  `REG IMPORT "`, `A required module cannot be loaded by Typora`.
  Conclusion: bytenode-compiled webpack main-process bundle; identifiers
  and literals fully recoverable — the bytecode is the only barrier.
- source: `sha256sum`/`file`/`od -A x -t x1z` dump; python3 byte-histogram;
  `strings` counts; `jscd info` field table; asar listing (3 entries).
- verify: `cd /tmp/jsc-probe && npx -y @electron/asar extract-file
  /usr/share/typora/resources/app.asar atom.compiled.dist.jsc &&
  sha256sum atom.compiled.dist.jsc` — sha256 must equal `6a0cb7b3…`.
- verified-at: 2026-10-13 round-4 lane (shells ec93c8, caca18, e78ddb,
  ee599f, 4a9560).
- suggested: admit — replaces r3's "opaque 388KB blob" with a fully
  decoded header + confirmed payload type.

## Candidate: REA has ZERO `.jsc`/V8-bytecode route — typed refusal recorded verbatim

- claim: `npx -y rea-agents@6.4.0 analyze-javascript-application
  /tmp/jsc-probe/atom.compiled.dist.jsc` → exit 1, typed refusal:
  `error: JavaScript application analysis failed` /
  `code: unsupported_target` / `category: unsupported_target` /
  `retryable: false` / message "accepts only a directory or an .asar
  file" / remediation "Select an extracted application directory, an app
  bundle, or an .asar file such as Contents/Resources/app.asar."
  `rea --llms` grep finds exactly ONE bytecode-adjacent verb —
  `rea inspect-evm-interface <path> <encoding>` (EVM, not V8) — and zero
  literal matches for `jsc|bytenode|asar`. The verb accepts an .asar
  *file* as input, so wrapping the blob back in an .asar would not help:
  the analysis targets JS source, not code-cache.
- source: verbatim stderr JSON/text above; `rea --llms` grep output
  (1 EVM line, 0 asar matches).
- verify: rerun the analyze command on the extracted file — refusal is
  deterministic (`retryable: false`).
- verified-at: 2026-10-13 round-4 lane (shells fe87f2, c12264).
- suggested: admit — r3's "NO REA verb handles it" is now proven at the
  contract level: refusal is typed, non-retryable, and `--llms` confirms
  no hidden verb.

## Candidate: host Node 24 CANNOT deserialize it — V8 version wall, proven empirically

- claim: host `node v24.21.0` = V8 `13.6.233.17`; a live
  `vm.Script("").createCachedData()` on host emits magic `0xC0DE0689` ≠
  the file's `0xC0DE06C3`. Replicating the loader recipe exactly (patch
  flag_hash bytes 12–16 from a live dummy, synthesize the 237,534-char
  ZWSP dummy source) still yields `cachedDataRejected = true`.
  `launch.dist.js` (the 1,383 B loader inside the same asar) is a
  bytenode-style runtime verbatim: `v8.setFlagsFromString("--no-lazy")`,
  `"--no-flush-bytecode"`, `setFlagHashHeader` copies bytes 12–16 of a
  locally-produced dummy cachedData, `getSourceHashHeader` reads
  bytes 8–12 → dummy source `'"' + '\u200b' × (n-2) + '"'`, then
  `Module._extensions[".jsc"]` → `vm.Script(…, {cachedData})` →
  `require("./atom.compiled.dist.jsc")`. It patches ONLY the flag hash —
  the version-stamped magic must match natively.
- source: host `process.versions`; node `-e` probe output
  (`host magic=0xc0de0689`, `cachedDataRejected = true`);
  `launch.dist.js` full text (1383 B, extracted).
- verify: the node `-e` snippet in the run log (row 7) — deterministic
  rejection on host node.
- verified-at: 2026-10-13 round-4 lane (shell f28093).
- suggested: admit — "wrong V8 ⇒ silent rejection" is now demonstrated,
  not assumed. Any decompile/exec path on this host MUST go through a
  version-matched V8.

## Candidate: exact V8 pinned — Electron 42.2.0 → V8 14.8.178.14 — and jscd v0.1.0 refuses it

- claim: `/usr/share/typora/version` = `42.2.0`; the `Typora` ELF
  contains literal string `14.8.178.14`; jscd `info` independently
  derives `v8: 14.8.178.14 (brute left-fold, V8 ≥ 12)` from the magic —
  three-way agreement. jscd (ejfkdev, pure-Rust static .jsc→JS, one 2.8MB
  musl binary, no patched V8) reports `supported: no (tables cover Node
  8.0.0–26.10.0 / V8 5.8–14.6)` — a *clear typed rejection*, not a guess,
  matching its stated design. This also explains the bytenode README's
  "Electron ≥ 42 (V8 ≥ 14.8)" warnings: 14.8 added a read-only-snapshot
  checksum field to the header. `npm view` probes: `bytenode@1.7.0`
  exists but is a *compiler only* (decompile explicitly out of scope
  upstream); `v8-disasm`, `bytenode-decompile`, `unjsc`, `v8-bytecode`,
  `jsc-decompile` → all E404. `wakaru@1.14.0` exists but is a source-
  level unbundler — useful only AFTER bytecode→JS, never on raw .jsc.
- source: version file + binary strings + jscd `info` output (all three
  quoted above); kitploit/release notes for jscd v0.1.0 scope; npm 404s.
- verify: `curl -fsSL -o jscd https://github.com/ejfkdev/jscd/releases/
  download/v0.1.0/jscd-v0.1.0-linux-amd64 && chmod +x jscd && ./jscd info
  atom.compiled.dist.jsc` → same table.
- verified-at: 2026-10-13 round-4 lane (shells bc761b, 850da8, 01dd78,
  d74004, f1ba3a).
- suggested: admit — the single most important frontier fact: the best
  current static decompiler stops one V8 minor short. Watch
  ejfkdev/jscd for a 14.8 table drop (actively maintained; v0.1.0 was
  2026-10-04).

## Candidate: version-matched V8 obtained ON THIS HOST — jsc deserializes AND disassembles TODAY

- claim: `/usr/share/typora/Typora` itself IGNORES `ELECTRON_RUN_AS_NODE`
  (launches GUI, emits wayland/Vulkan ozone error, hangs — both attempts
  killed). BUT `ELECTRON_RUN_AS_NODE=1 npx -y electron@42.2.0` downloads
  a matching prebuilt Electron and runs it as plain node:
  `process.versions` → v8 `14.8.178.14-electron.0` / node `24.15.0` /
  electron `42.2.0` — magic `0xC0DE06C3`, exact match. Re-running the
  loader recipe under it: **`cachedDataRejected = false`** — the blob
  deserializes cleanly. Adding `v8.setFlagsFromString("--print-bytecode")`
  before the `vm.Script` makes V8 print Ignition disassembly DURING
  deserialization → 530,020 B dump captured (`/tmp/jsc-probe/disasm.txt`),
  116 `[generated bytecode for function: …]` blocks spanning host
  builtins and app-path functions with source positions into the original
  237KB bundle (positions up to line ~4254; constant pools with real
  identifier names like `splitPath`, `isAsar` intact).
- source: `npx electron@42.2.0` version print; loader-recipe acceptance
  run; `wc -c disasm.txt`; head/tail of the disasm listing.
- verify: `ELECTRON_RUN_AS_NODE=1 timeout 90 npx -y electron@42.2.0 -e
  '<loader recipe + --print-bytecode>' > disasm.txt` → nonzero dump,
  `cachedDataRejected=false` on stderr.
- verified-at: 2026-10-13 round-4 lane (shells de4d01, d20d03, f28093,
  0dc7f0, 3443d4).
- suggested: admit — this is the frontier move of the round: full
  Ignition-level read access to Typora's compiled app is achievable with
  one npx line, zero patched binaries. Residual gap: `--print-bytecode`
  emitted 116 function listings (deserialized SFIs print once) — forcing
  EVERY inner SFI to materialize needs either executing the bundle under
  a stubbed `electron`/`ipcMain` harness or jsc2js's patched-d8
  `loadjsc()` walk (xqy2006/jsc2js: disasm text → View8 → approximate JS).

## Frontier verdict: `.jsc` decompilation IS reachable — cheapest paths ranked

1. **Working today, this host** — `npx electron@42.2.0` run-as-node +
   `--print-bytecode` = full Ignition disassembly. Bytecode→JS then needs
   a text mapper: jsc2js/View8 (github xqy2006/jsc2js; disasm→JS approx)
   or hand-analysis. Coverage of lazily-materialized SFIs needs an exec
   harness or a loadjsc-style SFI walk.
2. **Cheapest complete decompile once tables exist** — jscd: pure static,
   `--verify` via `node --check`, runnable output via `--runtime`.
   Currently hard-refuses V8 14.8 (tables ≤14.6). One upstream table
   drop away; file an issue with our `jscd info` output.
3. **Hosted** — jscdecompiler.com auto-detects V8 incl. newer Electron
   builds; works but uploads proprietary Typora code to a third party —
   policy call for the operator, not this lane.
4. **Heavy fallback** — jsc2js patched-d8 releases (need a V8-14.8 build)
   or compiling a matching V8/d8 — days of work, obviated by option 1's
   run-as-node disasm.
5. **Post-decompile** — wakaru on the emitted webpack JS to recover
   module boundaries (bundle internals already visible: `__webpack_*`).
6. **Not a path** — REA (typed refusal), host node 24 (rejected),
   bytenode itself (compile-only upstream).

## Run log

| # | command | result |
|---|---------|--------|
| 1 | `ls -la /usr/share/typora/resources/` | app.asar 390,514 B; lib.asar 8.3M; node_modules.asar 15M |
| 2 | `npx -y @electron/asar extract-file … atom.compiled.dist.jsc` (cwd /tmp/jsc-probe) | 388,080 B extracted — r1 cwd lesson applied |
| 3 | `sha256sum` + `file` + `stat` | `6a0cb7b3…2dfe9`; `data`; 388,080 B (99.38% of asar) |
| 4 | `od -A x -t x1z` head/tail | magic `c3 06 de c0` = 0xC0DE06C3; V8 code-cache header; `0a` pad tail |
| 5 | `strings -a -n 6` | 2,187 strings — webpack runtime + Typora domain names in clear |
| 6 | python3 byte histogram | entropy 6.2911 bits/B, 256/256 byte values — structured, not packed |
| 7 | node `-e` loader-recipe on host | host magic 0xC0DE0689 ≠ file 0xC0DE06C3; `cachedDataRejected=true` |
| 8 | `npx -y rea-agents@6.4.0 analyze-javascript-application <jsc>` | exit 1 `unsupported_target`, `retryable:false` — recorded verbatim |
| 9 | `rea --llms \| grep -iE 'bytecode\|jsc\|bytenode'` | 1 hit: `inspect-evm-interface` (EVM only); 0 `asar` matches in --llms |
| 10 | `asar list` + `package.json` + `launch.dist.js` extract | 3-file asar; Typora 1.14.9; 1,383 B bytenode-style `.jsc` loader (full recipe recovered) |
| 11 | `cat /usr/share/typora/version`; strings Typora | `42.2.0`; literal `14.8.178.14` in binary |
| 12 | `typora --version`; `ELECTRON_RUN_AS_NODE=1 Typora -e …` | GUI hangs, ozone/Vulkan error — Typora binary ignores run-as-node (2×, killed) |
| 13 | `npm view bytenode/v8-disasm/bytenode-decompile/unjsc/v8-bytecode/jsc-decompile/wakaru` | bytenode@1.7.0 (compiler only); wakaru@1.14.0 (source-level); rest E404 |
| 14 | web searches: jsc tooling | jscd (ejfkdev, Rust static); jsc2js (patched d8+View8); jscdecompiler.com (hosted); v8-version-analyzer (github-only, npm 404) |
| 15 | `curl -fsSL` jscd v0.1.0 linux-amd64 + `./jscd info <jsc>` | header fully decoded; `v8: 14.8.178.14`; `supported: no` (tables ≤14.6) |
| 16 | `ELECTRON_RUN_AS_NODE=1 npx -y electron@42.2.0 -p process.versions` | v8 `14.8.178.14-electron.0`, node 24.15.0 — version-matched host acquired |
| 17 | loader recipe under electron-node | `cachedDataRejected = false` — deserializes |
| 18 | `+ --print-bytecode` under electron-node | 530,020 B Ignition disasm, 116 function blocks, app source positions + names intact |

## Summary

The 388,080-byte blob is a **bytenode/V8-14.8.178.14 code-cache of a
webpack bundle** (Typora 1.14.9 main process, Electron 42.2.0) —
structured, unencrypted, with its entire string table and source-position
metadata serialized inline. REA is contractually blind to it
(`unsupported_target`, `retryable:false`; the only "bytecode" verb in
`--llms` is EVM). Host node 24 (V8 13.6) provably rejects it. The
version wall is the only wall: `npx electron@42.2.0` under
`ELECTRON_RUN_AS_NODE` supplies the exact V8 on this host, accepts the
blob (`cachedDataRejected=false`), and `--print-bytecode` already yields
a 530KB Ignition disassembly — bytecode-level read access is a solved
problem TODAY for one npx line. Full `.jsc`→readable-JS remains one step
out: jscd hard-refuses V8 14.8 (tables end at 14.6 — one upstream minor
short), so the standing cheapest-complete path is the run-as-node disasm
feeding a View8/jsc2js-style text mapper, or a jscd 14.8 table drop.
Scratch artifacts at `/tmp/jsc-probe/` (extracted jsc, jscd binary,
disasm.txt); repo tree untouched except this file.
