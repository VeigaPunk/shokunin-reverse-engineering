<!-- corpus entry — kaidoku-shokunin round 1 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r1/10-rea-live.md. Each candidate's `suggested:` field is its curation verdict; `reject` rows are retained calibration entries. -->

# 10 — REA live end-to-end run on /usr/bin/jq (round-1 evidence)

Lane: kaidoku-shokunin. Date: 2026-10-13. Host: Linux x86_64, node v24.21.0, npx 11.19.0.
Target: `/usr/bin/jq` — ELF 64-bit LSB PIE, x86-64, dynamically linked, stripped, 30,800 bytes,
sha256 `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`.
Every `rea` invocation below was `timeout 600 npx -y rea-agents@6.4.0 <verb> ...`.

## Run log (exact commands + wall-clock)

| # | Command | Wall | Result |
| - | ------- | ---- | ------ |
| 1 | `npx -y rea-agents@6.4.0 --help` | <1s | ~150 verbs listed; global opts `--format`, `--filter-output`, `--snapshot`, `--token-limit`, `--mcp` |
| 2 | `npx -y rea-agents@6.4.0 doctor` | ~8s | `healthy:false` — Ghidra 12.1.4 healthy at `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC`; Hopper + IDA missing; 18 scope_checks |
| 3 | `rea inspect-binary-layout /usr/bin/jq --format json` | 0.66s | FAILED `provider_unavailable` — needs `REA_PWNTOOLS_PYTHON` (pwntools 4.15.0 + pyelftools 0.33 + Unicorn 2.1.2); absent on host |
| 4 | `rea analyze /usr/bin/jq --format json` | 5.5s | OK — 30 segments, 167 procedures, 190 strings; provider `ghidra` 12.1.4, `import_mode: ephemeral-source-immutable` |
| 5 | `rea search /usr/bin/jq "" --kind procedures` | 0.66s | FAILED `VALIDATION_ERROR` — pattern requires ≥1 char |
| 6 | `rea search /usr/bin/jq ".*" --kind procedures --mode regex --format json` | 5.1s | OK — 167 results: 90 local (`FUN_00102020`…`FUN_001044b0`, `entry`, `_INIT_0`) + 77 `<EXTERNAL>::` imports (jq_*, jv_*, libc) |
| 7 | `rea decompile /usr/bin/jq 0x103ed0 --format json` | 5.2s | OK — C-like output: stderr dump callback using `jv_get_kind`, `jv_string_value`, `jv_dump_string`, `jv_free` |
| 8 | `rea decompile /usr/bin/jq 0x103fa0 --snapshot /tmp/rea-jq.snap.json --format json` | 5.3s | OK — jq `process()` loop (`jq_start`/`jq_next`/`jq_halted`/`jv_dump`, `--raw-output0` NUL check); snapshot written |
| 9 | `rea search /usr/bin/jq "usage" --kind strings --snapshot /tmp/rea-jq.snap.json` | 5.2s | OK — 1 hit `0x1052c8` = full `jq - commandline JSON processor` usage text; snapshot accepted |
| 10 | `rea analyze /usr/bin/jq --format json` (backgrounded) | ~6s | OK — live session dir observed mid-run, removed after close |

## Where REA stores sessions/projects

- Per-invocation session root: `mkdtemp($TMPDIR, "rea-ghidra-")` → e.g. `/tmp/rea-ghidra-bGA7MK/`, mode 0700.
  Contents observed live: `project/rea-project.gpr` + `rea-project.rep` (Ghidra project),
  `session.json` (run_id, unix-socket endpoint `bridge.sock`, pid, `ownership_kind: posix-process-group`),
  `ownership.json`, `ghidra.log`, `script.log`, `target-<sha256-prefix>.bin` (REA copies the source binary
  into the session — `/usr/bin/jq` is root-owned; import is on the copy), plus `home/ tmp/ cache/ config/ data/`.
- Spawned engine: `java ... ghidra.app.util.headless.AnalyzeHeadless <runtimeRoot>/project rea-project
  -import target-*.bin -readOnly -deleteProject -scriptPath <pkg>/bridge/ghidra
  -postScript ReaGhidraNoReturnFix.java -postScript ReaGhidraBridge.java session.json`.
  `-deleteProject` + `PrivateRuntimeRoot.close()` ⇒ the whole `rea-ghidra-*` tree is `rm -rf`'d on close
  (verified: dir gone ~seconds after exit). Sessions are ephemeral by design; closing = process exit.
- Persistence across invocations is opt-in: `--snapshot <path>` writes a mode-0600 JSON bundle
  (`{binding, entries, evidence_bundle, target, workflow_entries}`; 14,354 B for jq). Reuse does NOT
  skip Ghidra re-analysis — snapshot load run still took ~5.2s (full re-import each call).
- Host state outside sessions: `~/.cache/ghidra/{fscache2,packed-db-cache}`, `~/.config/ghidra/ghidra_12.1.4_PUBLIC/`
  (logs, prefs — these existed from prior runs), npx package at `~/.npm/_npx/<hash>/node_modules/rea-agents`.
- Concurrency note: a second `rea mcp` server (pid 35735, npx cache `dea9475797100b20`, NOT this lane's shell)
  held live session `/tmp/rea-ghidra-RqxIxo` analyzing a different 43,320-byte target (`target-8bc9a73afd7d.bin`).
  Independent evidence that `rea mcp` keeps long-lived sessions and that multiple sessions coexist under /tmp.

## Candidate: REA one-shot CLI analyze→search→decompile pipeline works on a small stripped ELF
- claim: On this host, `rea analyze`, `rea search`, and `rea decompile` each succeed on `/usr/bin/jq`
  in ~5–6s wall clock each, routing to the local Ghidra 12.1.4 provider, with no manual project setup.
- source: run log rows 4,6,7,8 above; outputs `/tmp/rea-analyze-jq.json`, `/tmp/rea-search-procs.json`,
  `/tmp/rea-decompile-{small,main}.json`
- verify: `timeout 600 npx -y rea-agents@6.4.0 analyze /usr/bin/jq --format json | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['normalized_result']['procedure_count'])"` → expect `167`
- verified-at: 2026-10-13
- suggested: admit — verified end-to-end three times with consistent 167-procedure inventory and
  coherent decompilation (FUN_00103fa0 is jq's `process()` loop; names are FUN_* because the binary is stripped).

## Candidate: REA Ghidra sessions are ephemeral /tmp/rea-ghidra-* trees, self-cleaning on close
- claim: Each `rea` CLI invocation creates `mkdtemp($TMPDIR,"rea-ghidra-")` (0700) containing a Ghidra
  project (`project/rea-project.gpr`+`.rep`), runs AnalyzeHeadless with `-readOnly -deleteProject`, and
  removes the entire tree on close; no persistent project remains after CLI exit.
- source: observed `/tmp/rea-ghidra-bGA7MK` mid-run then absent post-exit;
  `dist/process/PrivateRuntimeRoot.js` (`mkdtemp` + `rm recursive` in `close()`);
  `dist/ghidra/GhidraLauncher.js:299-309` (runtime paths); live java cmdline (pid 36958 args).
- verify: `(npx -y rea-agents@6.4.0 analyze /usr/bin/jq & sleep 2 && ls /tmp/rea-ghidra-*/project/rea-project.gpr && wait && ! ls -d /tmp/rea-ghidra-* 2>/dev/null)`
- verified-at: 2026-10-13
- suggested: admit — directly observed create+delete; matches shipped source and `-deleteProject` flag.
  Caveat to record: a crash may orphan the dir (no evidence of janitor sweep).

## Candidate: `--snapshot` is REA's cross-invocation persistence, not a Ghidra-project cache
- claim: `--snapshot <path>` writes/loads a versioned JSON evidence bundle (jq run: 14,354 B, keys
  `binding,entries,evidence_bundle,target,workflow_entries`), but every invocation still pays the full
  ~5s Ghidra re-import — the snapshot accumulates REA-side evidence, it does not cache the analysis DB.
- source: `/tmp/rea-jq.snap.json` (written by run 8, consumed by run 9; timing identical 5.2s);
  `dist/application/binary/AnalysisSnapshotFiles.js` (serialize/parse via `domain/analysisSnapshot.js`).
- verify: `npx -y rea-agents@6.4.0 search /usr/bin/jq "usage" --kind strings --snapshot /tmp/rea-jq.snap.json`
  then `python3 -c "import json;print(json.load(open('/tmp/rea-jq.snap.json')).keys())"`
- verified-at: 2026-10-13
- suggested: admit — measured; timing parity argues the snapshot is not a DB cache (binding-validated
  per `BinarySessionOpen.js:55-60`, which also fails `profile_mismatch` on wrong-target reuse).

## Candidate: `inspect-binary-layout` fails closed without a pwntools Python — honest negative
- claim: `rea inspect-binary-layout` has exactly one provider (`pwntools-elf`) which refuses unless
  `REA_PWNTOOLS_PYTHON` points to a Python carrying pwntools 4.15.0 + pyelftools 0.33 + Unicorn 2.1.2;
  REA never installs Python packages itself. Host lacks all three ⇒ typed `provider_unavailable` in 0.66s.
- source: run log row 3 JSON rejection (`candidate_ids:["pwntools-elf"]`, remediation text);
  `python3 -c "import elftools"` / `import unicorn` both ImportError on this host.
- verify: `npx -y rea-agents@6.4.0 inspect-binary-layout /usr/bin/jq --format json` → expect
  `code:"provider_unavailable"` until a qualifying interpreter is installed and env var set.
- verified-at: 2026-10-13
- suggested: admit — failure is typed, fast, and gives exact remediation; a valid negative data point
  for the "ELF inspection without Ghidra" path.

## Candidate: stripped-ELF decompilation quality is usable for triage, not naming
- claim: On stripped jq, REA/Ghidra recovers faithful control flow and libc/libjq call sites
  (`jq_start`, `jq_next`, `jv_dump`, `__fprintf_chk`) but every local procedure is `FUN_<addr>` and
  every parameter `param_N`/`undefined8`; semantics must be inferred from callees and strings.
- source: `/tmp/rea-decompile-main.json` — FUN_00103fa0 clearly = jq `process()` (raw-output0 NUL guard,
  `jq_halted` exit-code path); `/tmp/rea-decompile-small.json` — FUN_00103ed0 = jv-to-stderr dumper.
- verify: `npx -y rea-agents@6.4.0 decompile /usr/bin/jq 0x103fa0 --format json | grep -c FUN_` → >0;
  cross-check symbol-free names vs `nm -D /usr/bin/jq | grep jq_`.
- verified-at: 2026-10-13
- suggested: admit — decompiled bodies are readable and API-rich; naming is the expected stripped cost,
  not a tool defect. `/usr/bin/jq` is a thin CLI over libjq, so 77 of 167 "procedures" are EXTERNAL thunks.

## Candidate: validation and flag interaction failures are typed and cheap
- claim: REA rejects bad input fast with structured errors: empty `--pattern` → `VALIDATION_ERROR`
  (zod `too_small`, 0.66s); `--token-limit` + structured `--format json` → `UNSUPPORTED_OUTPUT_COMBINATION`
  ("Token windows cannot preserve structured output. Remove --token-limit/--token-offset and use
  --filter-output or command pagination", 0.65s).
- source: run log row 5 + stderr output of the rejected `--token-limit 3000 --format json` attempt.
- verify: `npx -y rea-agents@6.4.0 search /usr/bin/jq "" --kind procedures` (expect VALIDATION_ERROR);
  `... --token-limit 10 --format json` (expect UNSUPPORTED_OUTPUT_COMBINATION).
- verified-at: 2026-10-13
- suggested: admit — both reproduced; good discipline signals for scripted use (token windows require
  non-structured formats like `--format toon`/`md`).

## Candidate: environment readiness = Ghidra-only (Hopper/IDA/pwntools absent)
- claim: `rea doctor` reports `healthy:false` overall yet the native-binary pipeline is fully
  serviceable because the Ghidra chain (installation, platform, x64 arch, headless, native decompiler,
  Java 21.0.12.1) is green; only Hopper, IDA-MCP, pwntools-python and skill files are missing.
- source: `rea doctor` scope_checks (18 rows), saved `/tmp/rea-doctor.json`; env `GHIDRA_INSTALL_DIR=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC`.
- verify: `npx -y rea-agents@6.4.0 doctor --format json | python3 -c "import sys,json;d=json.load(sys.stdin);print([c['name'] for c in d['scope_checks'] if not c['ok']])"`
- verified-at: 2026-10-13
- suggested: admit — doctor's top-level false overstates unfitness for ELF work; the per-check rows are
  the real signal. jq analysis never touched a missing provider.

## Summary
REA 6.4.0 ran a real end-to-end ELF pass on /usr/bin/jq — `analyze` (167 procs/190 strings/30 segments), procedure+string `search`, and two `decompile`s including jq's `process()` loop — each in ~5–6s through ephemeral, self-cleaning `/tmp/rea-ghidra-*` Ghidra sessions; `--snapshot` gives opt-in JSON persistence; `inspect-binary-layout` fails typed-and-fast without pwntools.
