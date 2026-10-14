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

## 2026-10-13 — Round 5: r4/r4u corpus re-audit (13/13 HOLD), consistency repairs in flight, RISC-V `target_unavailable` bypassed

Round-5 wave: 5 lanes under fleet `.ufo/waves/kaidoku-r5/`. Three adversarial
audit lanes re-verified the round-4 corpus, a consistency lane cross-checked
the repo's indexes, and the expansion lane broke the RISC-V wall. Correction
to the follow-up above, first: it says "five minor errata appended" but lists
four, and exactly four bullets exist (r4-06×1, r4-07×2, r4-08×1) — four it is
(flagged by this round's consistency audit, LOG.md:104).

Audit A (`01-audit-A.md`): r4-06 (1Password asar), r4-07 (jsc bytecode), r4-08
(observe verbs) re-run from re-synthesized inputs — every sha256 pin held, all
three HOLDS, nothing refuted. Errata filed as `## Errata (round 5 audit)`
blocks on r4-06:325, r4-07:212, r4-08:285: the asar lists 480 files (REA's 423
is the relevant-file subset; "limitations ≈560" → 288 top-level entries);
`--print-bytecode` disasm is a nondeterminism band (531,851 B / 115 blocks vs
530,020 / 116) and the recipe is order-sensitive (flag before the flag-hash
dummy); xvfb electron FATALs on `--disable-gpu` alone on this host. Audit B
(`02-audit-B.md`): r4-09/-11/-12/-13 — 8/8 `compare-javascript-export-shapes`
outputs byte-identical (`cmp -s`, incl. a 63 MB request), 2914/2914 dncil
decode, 196/181 machine census exact; zero refuted. Fleet drift recorded:
`REA_PWNTOOLS_PYTHON` is now persisted (`~/.bashrc:58`, `~/.profile:7`) —
reproduce the r1–r3 refusal semantics only under `env -u`. Audit C
(`03-audit-C.md`): 6/6 r4u entries HOLD (firmware deep, jadx, unblob, dnfile
IL, wakaru OOM chain, adb taxonomy); determinism asymmetry verified across
providers — managed/android/adb verbs mint content-deterministic evidence ids
(three reproduced byte-exact), jadx/unblob per-run. The errata B/C filed sit
UNCOMMITTED as `## Errata (round 5 audit)` blocks on
`corpus/knowledge/2026-10-13-r4-11-managed-unlock.md:166` (boundary
arithmetic: Pinta.Effects at exactly 220,160 B PASSES → fail count 13 of 14,
sweep 23 complete / 13 resource-limit),
`r4u-02-jadx-decode.md:234` (locales 88, not 92 — byte-identical evidence id
proves a miscount), `r4u-04-dnfile-il.md:177` (Pinta.Core census 15,992 rows
/ 31 tables, not 14,417 / 17).

Consistency audit (`04-audit-consistency.md`, repo @ f507327): README
knowledge table 56/56 complete both directions, host asar census 9/9 exact,
all errata blocks cite real original text — but DRIFT: six stale PROVINCE.md
Frontier bullets contradicting the Round-4 Core table (`:70-97` vs
`:128-140`), the signal lane still marked "in flight" (`:160`),
`REA_APKTOOL_JAR` documented where the real key is `REA_APKTOOL_COMMAND`
(`:20`, `:134` — SKILL.md:69 spells it right), SKILL.md:48 stale `zstd -d`
step, coverage map missing 12 r4-era entries (44/56). The repair list is
in flight this wave by sibling lanes (PROVINCE/SKILL/README); the log-side
count slip is repaired here by append, not by editing the entry above.

Headline — `05-riscv-deep.md`: the RISC-V `target_unavailable` wall is
bypassable. The gate is REA's parse-time e_machine allowlist
(`dist/domain/binaryTarget.js:105`, switch `:208-222` = {3,62,8,40,183};
EM_RISCV=243 has no case). Route A (through REA): patch e_machine 243→183
(2 bytes at offset 18) + `REA_GHIDRA_LANGUAGE_ID=RISCV:LE:64:default` → RC=0,
94 procedures plus the `csreg` block on the 766 KB carved EXEC in ~50 s; the
control (patch, no override) gives 0 procedures as arm64 — clean A/B. Honesty
tax: the envelope records the patched `architecture:"arm64"` and patched
sha256, so declare the patch wherever that evidence is cited. Route B (around
REA): direct `analyzeHeadless` imports the UNPATCHED 29 MB EXEC natively
(auto-detects `RISCV:LE:64:default:gcc`) and a 900 s-capped auto-analysis
reaches 10,766 functions / 3,141,043 instructions / 42,057 symbols with a
coherent RV64 entry sequence. Scaling: the full patched EXEC still dies
`provider_timeout` through REA at 330 s default and at 1800 s raised — keep
REA-route slices ≲1 MB, send full firmware to direct Ghidra. Dead ends
pinned: `.hop` rename skips the parse but no provider accepts `database`
kind; `--target-format` is dos-com only (0xff00 B cap); `extract-firmware
--offset/--length` verifies a slice's sha256 but publishes 0 files. Working
rule: RISC-V via REA = patch + override for bounded slices; full GSP EXEC =
direct `analyzeHeadless`, budget >30 min for complete auto-analysis.
- 2026-10-13 — round 5 close-out (goal-mode wave, 6 zai lanes + parent): the
  in-flight round is now closed and the record repaired. Landed: SCORECARD.md
  created (the missing axis record README/AXES require — three-trend primary
  verdicts + six-axis secondary readings, all evidence-anchored, never
  scalar); PROVINCE repaired per the r5 consistency audit (six stale Frontier
  bullets pruned, REA_APKTOOL_JAR → REA_APKTOOL_COMMAND at both sites, signal
  asar 'in flight' → landed, r4-10/12/14/16 citations reconciled — each edit
  carries an [r5-audit C#] marker); SKILL.md zstd -d stale claim fixed;
  SHONEN.md boxes annotated with their documented verifier evidence (none
  UNDOCUMENTED) and the stale PROTOCOL.md line-cite corrected (419-428);
  coverage map backfilled 44/56 → 56/56 (12 rows); the asar under-count minor
  (6 → 9) fixed in both sites; this LOG entry. Verification: the consistency
  audit's checks 1/2/5/8 re-run post-repair → PASS (the re-audit also
  corrected a premise: six r5 errata blocks exist, three committed + three
  now landing here). Godspeed verdicts: operability improved (record now
  complete: SCORECARD + LOG + committed errata), calibration improved (stale
  claims pruned with audit authority), freshness improved (coverage map
  complete), quality improved (audit PASS), expansion unchanged. Carried
  forward: the RISC-V bypass (05-riscv-deep) awaits its corpus entry — queued
  as a round-6 candidate.
- 2026-10-13 — round 6 (goal-mode, 3 zai lanes + parent): the RISC-V
  headline lands as corpus and the Queue-A head is exercised. r5-01-riscv-bypass
  (96 L): the target_unavailable gate pinned (dist/domain/binaryTarget.js:105,
  elfArchitecture allowlist :208-222), bypass #1 re-run live by both the lane
  AND the audit at independent paths with the IDENTICAL evidence id
  (ev_e9a735a2…, 94 procedures), bypass #2 (direct analyzeHeadless, 10,766
  functions / 3.14M instructions), the arm64 honesty tax, the three dead ends.
  Four stale wall claims repaired (PROVINCE:128-131, SKILL:53, README:44/119 —
  each 'bypassed via e_machine patch + language override (r5-01)'). r5-02-call-targets-jq:
  the assigned one-arg form refuses (VALIDATION_ERROR, address required — the
  op takes [path, address]); the two-arg form resolves 3/3 GOT-indirect sites
  in jq's main to EXTERNAL thunks with bit-exact evidence ids; the honest
  not-call verdict verified; Queue-A 'self-provisionable NOW' confirmed;
  frontier-rescan gained an append-only erratum (Queue-A row 1 exercised).
  Audit verdicts: both entries VERIFIED. Append-only errata landed: the
  candidate-6 timeout mechanism no longer reproduces on the warm host
  (conclusion survives; mechanism wave-scoped), and the superseded
  'RISC-V wall' framing in r2-firmware-probe, r4u-01-firmware-deep, and
  lessons/round-4 now each carry a pointer to r5-01. Coverage map 56 → 58.
  Godspeed verdicts: expansion improved (two held surfaces documented with
  re-runnable verify lines), quality improved (audit bit-exact, errata
  append-only), discernment improved (validation-refusal vs gate-refusal
  distinguished; mechanism-vs-conclusion separated), operability unchanged.
