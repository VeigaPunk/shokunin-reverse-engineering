<!-- corpus entry — kaidoku-shokunin round 6 goal-mode expand lane (EXPAND R2), finished 2026-10-14T00:33Z. Spec/authority: corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md Queue A row 1 (line 165). All live runs inside timeout 600 npx -y rea-agents@6.4.0 …; verification completed 2026-10-14T00:33Z (UTC-midnight boundary). -->

# r5-02 — `resolve-native-call-targets` on /usr/bin/jq: Queue-A head exercised

Axes: **boundary-honesty** (assigned one-arg refusal kept distinct from the
two-arg success path) / **gate-truth** (does "self-provisionable NOW" hold
with zero operator env?) / **resolution-semantics** (what a "resolved target"
actually is on a BIND_NOW GLOB_DAT binary) / **substrate-immutability**
(target byte-identical before/after every probe).

Target: `/usr/bin/jq` — ELF 64-bit LSB PIE x86-64, stripped, 30,800 B, sha256
`e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`, 755
root:root (identity == the r1 record, `2026-10-13-rea-live-jq-e2e.md:5-8`;
re-pinned before and after every probe). The binary is BIND_NOW/PIE
(`readelf -d`: `FLAGS BIND_NOW`, `FLAGS_1 NOW PIE`) and has **no `.plt`
section** (`objdump -d` disassembles only .init/.text/.fini), so every
external call is `call *0x…(%rip)` through an `R_X86_64_GLOB_DAT` GOT slot
(`readelf -r`). Census: **286 GOT-indirect sites = 284 call + 2 jmp**
(`grep -cE` over `/tmp/r5-jq.disasm.txt`). Implementation anchors cited from
npx cache `dea9475797100b20` — the r2/r4-recorded warm cache
(`2026-10-13-r4-16-frontier-rescan.md:22`); all three on-disk 6.4.0 caches
(`9b9809298fe40d2c`, `af752b90495482d7`, `dea9475797100b20`) verified
`version 6.4.0` via their package.json.

## Candidate: the assigned one-arg form REFUSES — `VALIDATION_ERROR`, required `address`

- claim: `npx -y rea-agents@6.4.0 resolve-native-call-targets /usr/bin/jq
  --format json` (path only, exactly as the queue phrased it) exits **1 in
  0.7 s**: 542 B structured refusal on stdout, stderr empty. Verbatim:
  `{"code":"VALIDATION_ERROR","message":"Invalid input: expected string,
  received undefined\n\nDetails: [ { \"expected\": \"string\", \"code\":
  \"invalid_type\", \"path\": [\"address\"], … } ]","fieldErrors":[{"code":
  "invalid_type","missing":true,"path":"address","expected":"string",
  "received":"","message":"Invalid input: expected string, received
  undefined"}]}`. The CLI takes exactly two positionals — `path` and
  `address` "Exact native address" — plus `--provider`/`--target-format`
  (`~/.npm/_npx/dea9475797100b20/node_modules/rea-agents/dist/cli/
  coreNativeCommands.js:143,146`; verb name map
  `dist/cliCommandNames.js:39`; bridge input schema
  `dist/ghidra/GhidraFunctionValues.js:48-49`). `--schema` agrees: required
  `[path, address]`, options `provider` and `target-format` (`dos-com`
  const).
- source: `/tmp/r5-ct-main.json` (verbatim stdout), `/tmp/r5-ct-main.err`
  (0 B), `/tmp/r5-ct.schema.json`.
- verify: `timeout 600 npx -y rea-agents@6.4.0 resolve-native-call-targets
  /usr/bin/jq --format json; echo $?` → same JSON, exit 1.
- verified-at: 2026-10-14T00:33Z
- suggested: admit — this is a validation refusal, not a gate refusal (no
  provider was ever contacted, 0.7 s); any r6+ driver must supply one
  call-site address per invocation. Queue-A row's verb was right, its
  implicit one-liner shape was not.

## Candidate: two-arg success path — probed GOT-indirect sites resolve 3/3, one target each

- claim: with a call-site address the op is fully live, ghidra-only, zero
  operator env: exit 0, ~5.4 s, 4,002-byte envelope; provider ghidra 12.1.4,
  `confidence "observed"`, `authority "shipped-artifact"`, subject digest ==
  the pinned `/usr/bin/jq` sha256, analysis-profile digest
  `a04af771c3a78edf03c11c3b8652d4812dfce76da00d380345526a333361b5c9`. Three
  `call *0x…(%rip)` sites inside `main` (procedure `0x102020`) each return
  **exactly one target** with `status "resolved-indirect"`,
  `mechanism "computed"`, `basis "provider-reference"`, one `COMPUTED_CALL`
  reference (`operand_index -1`, `provenance "ghidra-reference-manager"`,
  `source "analysis"`):
  `0x1020a3` (GOT slot 0x7ea8 = `jq_init`) → **`0x109110`**, ev
  `ev_db50c389f7c128206f8dd413c8708b0b968066c31e566293f0ef083d56b67242`;
  `0x10207b` (GOT 0x7f78 = `jv_array`) → **`0x1091e0`**, ev
  `ev_4e3303af034579fe13c463365977b8852c3f42757c4563a6a8e335a25820d10f`;
  `0x10206a` (GOT 0x7fb8 = `setlocale@GLIBC_2.2.5`) → **`0x109220`**, ev
  `ev_c9fcea3d6375c9efe8d8ca927d169c728c91bcc1aa3d11ffae5189337ea276bb`.
- source: `/tmp/r5-ct-site.json`, `/tmp/r5-ct-site2.json`,
  `/tmp/r5-ct-site3.json`; site→GOT mapping from `objdump -d` comments +
  `readelf -r` GLOB_DAT rows; output binding
  `dist/ghidra/GhidraFunctionValues.js:284`.
- verify: `timeout 600 npx -y rea-agents@6.4.0 resolve-native-call-targets
  /usr/bin/jq 0x1020a3 --format json | python3 -c "import json,sys;
  r=json.load(sys.stdin)['normalized_result']; print(r['status'],
  r['targets'][0]['address'])"` → `resolved-indirect 0x109110`.
- verified-at: 2026-10-14T00:33Z
- suggested: admit — this discharges exactly the r3 gap the queue cites
  ("r3 xrefs left these unresolved",
  `2026-10-13-r4-16-frontier-rescan.md:165`): the sites resolve via the
  provider's recorded call references, not fresh operand decoding.

## Candidate: a "resolved target" is Ghidra's EXTERNAL thunk — one hop to the import, never into libjq's body

- claim: the returned targets sit past the file image (last ELF vaddr
  ≈ 0x8038 per `readelf -lW`; targets 0x109110/0x1091e0/0x109220) — they
  are Ghidra EXTERNAL-block thunk functions, one per imported symbol.
  Cross-check: `search /usr/bin/jq "jq_init" --kind procedures --mode regex`
  → ev `ev_9bd058a0280ea12629e20a8c94ffd97927c311afa4bc0b0c4443045fbc902a6b`
  returns `{"address":"0x109110","value":"<EXTERNAL>::jq_init"}` — the exact
  address the resolver produced for the jq_init call site (alongside
  Ghidra's space-qualified `EXTERNAL:0x20` row for the same symbol).
  Ceiling for the Queue-A claim, stated plainly: the op names **which
  import** each GOT-indirect site calls (closing the r3 naming gap); it does
  NOT recover libjq's function bodies — that needs `import-reference-source`
  (jq source tree) or a run against `libjq.so` itself (not exercised here).
- source: `/tmp/r5-ct-extsearch.json` vs `/tmp/r5-ct-site.json`;
  `readelf -lW /usr/bin/jq` program headers.
- verify: `timeout 600 npx -y rea-agents@6.4.0 search /usr/bin/jq "jq_init"
  --kind procedures --mode regex --format json | python3 -c "import json,sys;
  print(json.load(sys.stdin)['normalized_result'])"` → both rows
  `<EXTERNAL>::jq_init`, addresses `EXTERNAL:0x20` and `0x109110`.
- verified-at: 2026-10-14T00:33Z
- suggested: admit — fixes the reading of any future "resolved" count on
  this binary: N targets == N named imports, not N recovered bodies.

## Candidate: honest non-verdict off call sites — `status "not-call"`, zero targets, exit 0

- claim: aiming the op at a non-call address (`0x102020`, main's entry)
  neither errors nor fabricates: exit 0, 3,208-byte envelope, ev
  `ev_b0238bea9dce7b527f6271f1c28aafb5a009f528bf87d74cc6b0aa774c55be3e`,
  `status "not-call"`, `mechanism "unavailable"`, `targets []`. Every
  success/not-call envelope carries the same two per-op limitations,
  verbatim: "Targets are static Ghidra ReferenceManager call-reference
  observations. Computed calls without call references remain unresolved; a
  resolved reference is not proof of runtime execution." and
  "Objective-C, Swift, vtable and closure mechanisms are not identified by
  this reference-only boundary." Envelope-level gate, verbatim: "The session
  serves operations only after Ghidra reports default auto-analysis
  complete; incomplete analysis does not expose partial results."
- source: `/tmp/r5-ct-nocall.json`; limitations arrays in all four envelopes.
- verify: `… resolve-native-call-targets /usr/bin/jq 0x102020 --format json |
  python3 -c "import json,sys;r=json.load(sys.stdin)['normalized_result'];
  print(r['status'], r['mechanism'], len(r['targets']))"` → `not-call
  unavailable 0`.
- verified-at: 2026-10-14T00:33Z
- suggested: admit — failure modes are now typed three ways:
  arg-validation refusal (`VALIDATION_ERROR`, exit 1), typed non-verdict
  (`not-call`, exit 0), and the declared unresolved class (computed calls
  without reference-manager entries). A fourth, session-level gate exists
  but was never hit (all runs post-auto-analysis).

## Candidate: Queue-A premise holds — self-provisionable, read-only, warm-cache cheap

- claim: the queue's gate column ("ghidra",
  `2026-10-13-r4-16-frontier-rescan.md:165`) is the entire dependency — no
  operator key or env (contrast Queue B rows), runs on the warm npx cache,
  ~5.4 s wall per probe, 0.7 s for the typed refusal. Immutability proven:
  `/usr/bin/jq` sha256 identical before and after all live runs — matches
  the envelope's `import_mode "ephemeral-source-immutable"` and the r1
  observation that REA copies the target into the session
  (`2026-10-13-rea-live-jq-e2e.md:30-31`). Address-space pitfall for future
  drivers: objdump file vaddrs need Ghidra's base `+0x100000` (`0x20a3` →
  `0x1020a3`; consistent with r1's `0x103fa0` = jq `process()`).
- source: sha256 pins in this lane's run log (below); envelope
  `analysis_profile.parameters.import_mode` in `/tmp/r5-ct-site.json`.
- verify: `sha256sum /usr/bin/jq` before and after any run →
  `e8156675…84f7806` both times.
- verified-at: 2026-10-14T00:33Z
- suggested: admit — Queue A row 1 discharged with live evidence; sweeping
  the remaining ~283 call sites is bulk-repetition of the proven form, not a
  new gate. The `2 jmp *0x…(%rip)` sites were not probed (op is
  call-reference-scoped); treat jump-target resolution as untested.

## Run log

| # | command | result |
|---|---|---|
| 1 | `resolve-native-call-targets --schema --format json` | 995 B: args required `[path,address]`; options `provider`, `target-format` (`dos-com` const) |
| 2 | assigned form `… resolve-native-call-targets /usr/bin/jq --format json` | exit 1, 0.7 s — `VALIDATION_ERROR` missing `address` (542 B stdout, 0 B stderr) |
| 3 | `… resolve-native-call-targets /usr/bin/jq 0x1020a3 --format json` | exit 0, 5.4 s — ev_db50c389…, 1 target `0x109110` (jq_init) |
| 4 | `… resolve-native-call-targets /usr/bin/jq 0x10207b --format json` | exit 0 — ev_4e3303af…, 1 target `0x1091e0` (jv_array) |
| 5 | `… resolve-native-call-targets /usr/bin/jq 0x10206a --format json` | exit 0 — ev_c9fcea3d…, 1 target `0x109220` (setlocale@GLIBC_2.2.5) |
| 6 | `… search /usr/bin/jq "jq_init" --kind procedures --mode regex --format json` | exit 0 — ev_9bd058a0…: `0x109110` == `<EXTERNAL>::jq_init` |
| 7 | `… resolve-native-call-targets /usr/bin/jq 0x102020 --format json` (non-call site) | exit 0 — ev_b0238bea…: `not-call` / `unavailable` / 0 targets |
| 8 | `sha256sum /usr/bin/jq` before and after #2–#7 | `e8156675…84f7806` both — substrate untouched |

Scratch (reproducibility, `/tmp`): `r5-ct.schema.json`,
`r5-ct-main.{json,err}`, `r5-ct-site{,2,3}.{json,err}`,
`r5-ct-extsearch.{json,err}`, `r5-ct-nocall.{json,err}`,
`r5-jq.disasm.txt` (full objdump -d, 286 GOT-indirect sites).

## Summary

Queue A's head verb is now exercised with live evidence instead of a queued
assumption. The literal assigned invocation (`resolve-native-call-targets
/usr/bin/jq --format json`) refuses typed-and-fast — `VALIDATION_ERROR`,
required second positional `address`, exit 1, 0.7 s — so the op is not a
one-liner; the two-arg form works fully on this host: three probed
GOT-indirect call sites in stripped `/usr/bin/jq` (BIND_NOW, GLOB_DAT slots,
no PLT) each resolved to exactly one target via the ghidra
reference-manager (`resolved-indirect` / `computed` /
`provider-reference`), and those targets are Ghidra `EXTERNAL` thunks
(`0x109110` == `<EXTERNAL>::jq_init` by independent search evidence) — i.e.
the op names the import behind each GOT-indirect site, closing the r3
"left unresolved" gap one hop short of libjq's actual bodies. Off call
sites it returns an honest `not-call`/0-target verdict; declared limits
reserve unresolved status for computed calls without reference-manager
entries. The Queue-A premise "self-provisionable NOW" is confirmed:
ghidra-only, no operator env, ~5.4 s per probe on the warm npx cache, and
`/usr/bin/jq` sha256-identical before/after (read-only). Untested residue:
the 2 `jmp *…(%rip)` sites and any computed call lacking a reference entry.
