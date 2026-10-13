# kaidoku-shokunin — Iteration Log

- 2026-10-13 — round 0: minted as shonen (sibling mint; rationale in MINT.md).
- 2026-10-13 — round 1: 16-lane curation wave (fleet `.ufo/waves/kaidoku-r1/`).
  14 knowledge entries admitted to `corpus/knowledge/` (4 reject candidates
  retained in-file as calibration); `corpus/lessons/2026-10-13-round-1.md`;
  QUALITY.md grown to 9 admission criteria + 5 weak signals; PROVINCE.md and
  SKILL.md placeholders filled from verified probes; corpus/README.md index
  built. End-to-end domain task: `rea analyze/search/decompile` on
  `/usr/bin/jq` via Ghidra (167 procedures, `evidence_id`-bearing output;
  knowledge/2026-10-13-rea-live-jq-e2e.md). Frontier probed-not-held: PE
  import, recorded crashes, firmware regions, managed AnyCPU (typed
  `unsupported PE architecture`), offline ELF layout (`provider_unavailable`).

- 2026-10-13 — round 2: audit + expansion wave (16 lanes, fleet
  `.ufo/waves/kaidoku-r2/`). Round-1 audit: ~100 verify commands re-run, all
  admit/reject verdicts upheld; 1 factual erratum (34 Ghidra features), 2
  verify-command defects, criterion-5 labeling gap recorded. Promoted to Core:
  PE-via-Ghidra (proven e2e), cross-version compare machinery, crash-inspect
  mechanism (32 MiB cap found). Headline: `~/.local/bin/jq` verified
  byte-identical to upstream jq-1.8.2 release — benign. Firmware blocked on
  `REA_BINWALK_COMMAND`; AnyCPU managed still rejected; ev_-id session scoping
  and +0x100000 .so rebase rules learned.

- 2026-10-13 — round-2 LOG errata (prescribed by the r2 audit, landed now):
  the r1 entry's "`evidence_id`-bearing output" overclaimed — the jq CLI
  report carried no literal `ev_*` id; "Frontier probed-not-held" wrongly
  grouped firmware (only catalog-listed, never probed in r1); and commit
  `a43d442` touched `SHONEN.md` checkboxes without recording it. Corpus-count
  conflict reconciled: crash corpus was 175 in one entry vs 176 in another —
  intra-round drift (a core rotated during the wave), not a contradiction.

- 2026-10-13 — round 3: audit + expansion wave (16 lanes, fleet
  `.ufo/waves/kaidoku-r3/`). Round-2 audit: all admits/rejects upheld; 4
  errata appended (jq-shadow search mechanism, capability_unavailable exit
  code, firmware verify defect, compare_functions surface attribution) plus
  index/province fixes. 12 new knowledge entries. Promoted to Core: runtime
  observation (self-launched CDP on chromium+electron), EVM selectors, PE
  ARM64, synth-carrier macOS ops (keyed-archive/IB/dylib-trace), .node addon
  taxonomy, APK inventory, MCP retained-evidence session incl. record_pairs
  `status:changed`. Headline: jq-shadow provenance RESOLVED (kimi-code swarm
  agent-2, 2026-10-03); obsidian.asar = real app w/ 45 ipcMain ops; evidence
  ids are content-addressed and reproduce across sessions. SKILL.md grown to
  full decision tables + error patterns — all SHONEN.md gates now closed;
  eligible for roster promotion pending operator decision.
## 2026-10-13 — Round 4 + unlock wave (audit r3 + expansion + operator-authorized provisioning)

Round-4 wave: 16 lanes under `.ufo/waves/kaidoku-r4/`. Four audit lanes
re-verified all r3 knowledge entries and corpus consistency; twelve expansion
lanes pushed frontier. All r3 claims survived re-verification — ten errata
appended (EVM bytecodeOffset semantics, typora 99.38%, list-* census 11 +
MCP-only verbs, renderer-asar grep-recipe + constraint census 29, managed
AnyCPU precision, jq-shadow timestamp ~1ms, crash oversize-class +
coredumpctl-decompression, keyed-archive weak-dylib `undetermined` + recipe
363B, appimage error-envelope precision, evidence-id `f(content,path,params)` —
three-lane corroborated). Also corrected from r4 consistency audit: the r3
LOG had omitted the verb-family promotion and QUALITY criteria 10–11 (they
landed in files, not the log — recorded here).

Expansion held: 1Password asar + 188MB Rust N-API core; typora `.jsc`
Ignition disassembly via version-matched electron run-as-node; four
runtime-observation verbs; `compare-javascript-export-shapes` e2e; managed
surface mapped (`0x14c` works, `0xfd1d` refused — dnfile/dncil covers all);
91.6MB ARM64 PE measured scale wall (`provider_timeout` ~900s internal);
`inspect-binary-layout` first-held (jq full RELRO, persistent pwnenv);
AppImage inner asar reachable via unblob/7z carve ("Grok Bot" = Cursor `sand`);
libsignal anatomy; frontier rescan → r5 roadmap.

Unlock wave (operator-authorized installs): 6 lanes under
`.ufo/waves/kaidoku-r4u/`. Firmware regions + extract exercised on nvidia
blobs (RISC-V `target_unavailable` is REA's own gate); full Android surface
opened (jadx-headless-mcp 0.7.1-all sha256-pinned + apktool 3.0.3 — real Java
decompile); unblob extract live (pacman pkg carved 100% where binwalk saw 0);
dnfile+dncil full-IL coverage; wakaru spawn-OOM ROOT-CAUSED and FIXED
(`prlimit --as=1GiB` vs node shim — bind `@wakaru/cli-linux-x64` ELF; fix
applied `.bashrc:63`, `recover-javascript-sources` held `ev_4898906e…`); adb
surface mapped device-free (2/24 serial-free verbs, telemetry bug noted).

New QUALITY criteria 12–14 (synth-carrier bytes, grep -o|wc -l, evidence-id
domain) + weak-signal 6 (blame-the-tool before checking the spawn wrapper).
SKILL decision table expanded to the whole held surface; known-limits section
moved to r4. Two expansion lanes (signal-asar, real version-pair) still in
flight at integration — their entries land on return.

## 2026-10-13 — Round 4 follow-up: final two lanes landed

Signal-asar and real-version-pair lanes returned after the main integration
and are now admitted as `2026-10-13-r4-05-signal-asar.md` and
`2026-10-13-r4-10-real-version-pair.md`. Signal's 38.5MB asar hit three honest
walls (integrity-mismatch on distro-postprocessed `.node` natives —
`record-and-continue` marks them observed-untrusted; per-source timeout
aborting the whole run; 68-92KB webpack chunks exhausting the 8GiB worker
heap during semantic) routed around via `--artifact-format directory` on a
9.2MB pruned core → 173 IPC ops / 95 literal channels / zero sender
validations / strict-CSP V8-cachedData preload (Typora-like loader shape but
with source shipped). The `op` version pair exercised the full compare
pipeline at 41-43MB (every verb re-imports fresh — per-call
`REA_GHIDRA_STARTUP_TIMEOUT_MS` required) and surfaced a NEW hazard class:
Go toolchain bump (1.25.7→1.26.8) collapses symbol recovery 33,060→11,595
procs (11,588 `FUN_*`) — symbol-keyed pairing is unsafe across Go versions;
pair by ELF role/address. CLI `rea compare` still caps at `status:unknown`;
domain `compareBundles`+`record_pairs` reaches `status:changed` only with ALL
members paired. Round-5 audit-A (landed early) confirmed all three audited
r4 files HOLD; five minor errata appended (1Password file-count wording,
.jsc disassembly nondeterminism + recipe ordering, xvfb GPU flag nuance).

## 2026-10-13 — HOURS.md ledger opened

- Operator seed per PROTOCOL.md §Craft-hours: shonen→shokunin now requires
  ≥10,000 verified craft-hours AND the SHONEN gate. Ledger starts at 0;
  instrumented rounds accrue collective in-domain lane-minutes.
- Evidence: fleet commit; PROTOCOL.md §Craft-hours.
