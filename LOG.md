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
- 2026-10-13 — round 7 (goal-mode, 3 zai lanes + parent): four more Queue-A
  ops discharged on libjq. r7-01: inspect-native-api resolves jq_next by name
  AND by the queue's 0x117070 address to identical composed dossiers
  (decompiler-inferred signature at low confidence, 85-entry jump table
  typed into 47 cases); inspect-native-data-type reveals a SECOND distinct
  refusal family (invalid_request 'Supply exactly one of type or address',
  vs r5-02's VALIDATION_ERROR) plus honest unavailable non-verdicts. r7-02:
  the 0x117070 queue hint proven to be jq_next's Ghidra-space entry
  (ENDBR64 decode + nm/objdump triangulation); raw file-vaddr probes return
  honest outside-memory — the PIE +0x100000 rule extends to shared objects;
  inspect-native-load-image is provider-format-gated (DOS MZ/COM only) yet
  still emits its full payload (base 0x100000, 29 mappings, 729
  relocations, 185 entries). Audit: both entries VERIFIED, all evidence ids
  bit-reproduced — and the audit confirmed evidence ids are content-
  addressed across lanes and rounds (three independent lanes, identical
  ids). One erratum row-label corrected (rows 4–5, the 3rd/4th
  still-unexercised). Cross-lane corroboration: r7-02's decode independently
  confirms r7-01's name-resolution inference. Noted for future lanes:
  `which jq` → static ~/.local/bin/jq shadows the pinned dynamic /usr/bin/jq.
  Coverage 58 → 60. Godspeed verdicts: expansion improved (4 ops held with
  re-runnable verify), quality improved (audit 0 defects), discernment
  improved (two refusal families distinguished; format-gate vs env-gate
  separated), calibration improved (the content-addressed evidence-id
  property now documented).
- 2026-10-14 — round 8 (goal-mode, 2 zai expand lanes + resumed audit + parent):
  Queue-A rows 6, 8, 9 discharged (and row 7 closed as a census defect — it
  was already exercised by r4-09, re-derived byte-exact). r8-01:
  annotate-native-function — annotations do NOT persist (a fresh
  inspect-native-api re-derived r7-01's envelope byte-identically with the
  original name); interior addresses snap to the containing function's
  entry; unknown names refuse post-analysis (14.2 s import before the
  error — a new cost class vs r7-01's 0.7 s pre-analysis gates). r8-02:
  trace-javascript-semantics — the status machine refuses absence claims on
  partial graphs (zero-match seeds return `partial`, not the schema's
  `no-match`; consumers must test total_seed_matches); compare-source-to-
  bundle succeeds from held artifacts alone (19/19 exact via
  exact-source-digest) and the typora `.jsc` wall resolves as the data
  model's, not a missing tool. Audit (resumed after its poll cap honestly
  expired pre-landing): r8-01 VERIFIED 9/9; r8-02 VERIFIED with one
  wrong-by-one-artifact parent-Evidence pointer — corrected by append-only
  erratum (:ev_4c3202c9, not ev_039c8069) plus a recorded terminology
  hazard (two "truncated" layers). Line 172 dual-discharge adjudicated
  complementary (7 distinct ids, disjoint seeds, zero contradiction). The
  audit lane's honest no-verdict-at-cap is itself recorded as the right
  behavior. Coverage 60 → 62. Godspeed verdicts: expansion/quality/
  discernment/calibration improved (non-persistence proven by re-derivation;
  the partial-graph status semantics documented; the census defect closed
  with byte-exact evidence).
- 2026-10-14 — round-7/8 README repair (uncounted, parent-side defect): the
  round-7 coverage-map insert silently no-op'd — a python tuple typo
  (implicit string concatenation: rows[0] was the character "|", not the
  first row) inserted two characters into the signal-asar row instead of
  two rows, and the round-7 "coverage 60" claim was wrong (the map stayed at
  58 through round 8). The round-8 insert then failed its anchor assert
  (the r7 rows it searched for never existed) and committed without README
  changes — its "coverage 62" claim was likewise premature. Both defects are
  the parent's integration tooling, not the lanes': the lesson is to verify
  map-row counts with grep AFTER writing, in the same command as the write.
  Repaired now: the mangled row cell restored, the four missing rows
  (r7-01, r7-02, r8-01, r8-02) inserted, map verified at 62 unique knowledge
  files cited (12 rows in the recent-entries table + the knowledge/ table
  rows reconciled).
- 2026-10-14 — round 9 (goal-mode, 2 zai expand lanes + audit + parent):
  Queue-A rows 10+11 (r9-01) and 13+14 (r9-02) discharged; line 176 skipped
  per the provisioning-only convention. r9-01: the Evidence-BUNDLE input
  shape (verbs consume canonical bundles, not ev ids — hand-wrapped bundles
  refuse verbatim); build-reconstruction-obligation-ledger mints 171
  obligations from the real graph, all static-only, 0/171 verified;
  evaluate-reconstruction-coverage gates on package-proof (partial → ready);
  cross-verb asymmetry: referential TypeErrors project as non-retryable
  unreadable_output (ledger) vs retryable invalid_request (coverage). r9-02:
  verify-managed-native-boundaries observes all four statuses live (libgtk
  39/39 unresolved — honest structural negative; glibc setenv dossier
  contradicted/module-mismatch; same bytes renamed → verified — the
  authentication boundary: module attribution is CALLER-ATTESTED);
  project-managed-application-graph lands members-only and three-evidence
  union projections. Audit: both VERIFIED, every id bit-reproduced across
  THREE independent runs (content-addressing now audit-proven); meta-
  finding: expand lanes take 19–25 min, the r8 12-min cap would have failed
  again, a 40-min cap suffices with ~15 min headroom, and an audit must
  re-stat after first-sighting (r9-02 stayed writable ~4 min after first
  appearing). Incident recorded: the shared /tmp/r9-* scratch namespace
  collided between concurrent lanes (both re-pinned lane-uniquely, live
  re-hash clean) — future lanes namespace scratch from the first write.
  Coverage 62 → 64. Godspeed verdicts: expansion/quality/discernment/
  calibration improved (bundle input shape, coverage-gate semantics, and the
  caller-attested authentication boundary documented; audit-cap calibration
  measured).
- 2026-10-14 — round 10 (goal-mode, 2 zai expand lanes + audit + parent):
  Queue-A effectively drained. r10-01 (rows 15+16): compare-managed-members
  round-2 — real verdicts {unchanged 2, changed 14, added 1241, removed
  1047, unknown 588} where round-1 read all-unknown 1382; internally-minted
  member ids differ from CLI ids at identical bytes/mvids (never substitute
  across invocation shapes); inspect-web-network-capture — the census's
  chromium --log-net-log hint REFUTED (1,310-event netlog refuses on the
  har-schema gate), playwright recordHar route yields lossless 5/5 records
  with a THIRD authority grade (historical-reference/observed). r10-02:
  FOUR more census defects of the row-7 class closed (reconcile-javascript-
  runtime and observe-web-session were held by r4-08 the same day the census
  queued them; lines 181/187 flagged too) + rows 20–21 discharged (six web
  verbs: artifact-block contract, scr_ identity join across two verbs,
  honest zero WebMCP tools, screenshot determinism proven by sha identity).
  Audit: both VERIFIED, no defects (one cosmetic nit: CDP node ids print as
  strings); append-only proven (130/0); the post-first-sighting-append
  protocol held again (r10-02's +193 B census note caught by re-stat); the
  r9 scratch-namespacing lesson applied cleanly — zero collisions. Queue-A
  remaining: line 176 (provisioning-only), 186, 188, 189. Coverage 64 → 66.
  Godspeed verdicts: expansion/quality/discernment/calibration improved (the
  census's exercised-set blindness is now a NAMED defect class — four
  closures; the netlog refutation and the third authority grade documented).
- 2026-10-14 — round 11 (goal-mode, 2 zai expand lanes + audit + parent):
  **Queue A fully drained** (lines 165–189 all accounted; only line 176
  remains, provisioning-only by convention). r11-01 (lines 186+188): the
  export-web-scripts chain — the census-missed response_body retention
  gate; trace-web-module-imports needs REA_BROWSER_EXECUTABLE (absent from
  the 18-op capabilities matrix); tool acceptance ≠ map correctness (a
  semantically-wrong map passed the tool, caught by an independent
  decoder); the capture-process pair records the FOURTH authority grade
  (controlled-replay/observed) and pins the A/A2 wall-clock-id semantics
  (traceSpec restores timing-insensitive verdicts). r11-02 (line 189,
  row 25): the first Apple-graph projection on this host — the homogeneous
  inspect_artifact feed law (the census hypothesis of keyed-archive/IB
  feeds is REFUTED at the workflow layer) and the 64-bit Mach-O 32-byte
  header law; Queue-B recon seeds round 12 (5 rows ready-now: binwalk,
  unblob, jadx, apktool, compare-application-versions; 1 one-fix: pwntools
  venv pkg_resources; 1 one-knob: wakaru prlimit; 1 one-device: adb).
  Audit: both VERIFIED; five defect-nits (sha tail slip, row-alias
  collision between the two errata, a false 'stderr empty' claim, two
  header nits, one unreproduced datum) — all landed as append-only errata.
  Coverage 66 → 68. Godspeed verdicts: expansion/coverage improved (Queue A
  complete), quality improved (audit-bit-exact; nits surfaced and fixed),
  discernment improved (four refusal/feed laws documented), calibration
  improved (the recon classifies Queue B honestly: 5 ready-now, not the
  census's vaguer env-gated).
- 2026-10-14 — round 12 (goal-mode, 2 zai expand lanes + audit + parent):
  Queue-B ready-now ledger. r12-01: L195 closed as the SIXTH row-7-class
  census defect (r4-13 held pwntools before the census wrote; the
  setuptools<81 pin law proven in a /tmp venv copy — bare setuptools 84
  drops pkg_resources, <81 restores unicorn 2.1.2); L196/L197/L199×4/L200×1
  confirmed right-at-write holdings (byte-exact re-derivations, four-site
  normalization law for per-run ids); three never-exercised tails discharged
  live — trace-android-references ×3 with a positive control, the FIRST
  Android application-graph projection on this host (13 dex / 8 native libs
  / 104 jni-bridge candidates, digest-keyed join, same homogeneous
  inspect_artifact feed law as the Apple projector), and the first-ever
  inspect-apktool-client success (592 B, environment-sourced 3.0.3).
  r12-02: L203 compare-application-versions discharged (first real JS
  application-version diff: 218 items, 10 changes all semantic-key-paired,
  unknowns honest under partial coverage; managed-graph class reads
  all-unknown as a disciplined non-verdict) + the full Queue-B exercised-set
  ledger: remaining open set = adb 22 serial verbs (one device), JEB ×4,
  ida ×12, hopper ×13, L204's decompiler route, L203's runtime-reconciliation
  input class. Audit: both VERIFIED; adversarial close-check found ZERO
  false closes; three defect-nits errata'd. Cross-file defect repaired
  (parent): PROVINCE.md:117 + LOG.md:76 cited phantom evidence id
  ev_4898906e… (appears nowhere in the corpus) — corrected to r4u-05's
  recorded success id ev_5cb1856a… with an inline correction note.
  Coverage 68 → 70. Godspeed verdicts: expansion/coverage/quality/
  discernment/calibration all improved (the Queue-B ledger is the
  deliverable — the lane now knows exactly what remains and why).
- 2026-10-14 — round 13 (goal-mode, distillation lane + verify lane, zai):
  the queue-drain craft synthesis lands in SKILL.md as `## Queue-drain
  craft (rounds 5-12, distilled in round 13)` (+116 L, 9 rules, every rule
  citing its corpus entry): content-addressed evidence ids with the three
  per-run exception classes; the +0x100000 PIE pre-shift rule (executables
  AND shared objects, honest outside-memory on raw probes); the refusal
  family taxonomy with cost classes (0.7 s pre-analysis validation vs 14.2 s
  post-analysis semantic refusals); the four authority grades and what each
  licenses; input contracts (canonical bundles only, homogeneous
  inspect_artifact feeds shared by the Apple+Android projectors, positional
  schemas); the caller-attested authentication boundary; tool acceptance ≠
  correctness; the census-defect class (six instances, with the
  bookkeeping-lag nuance); refuted provisioning hints. Distill lane
  self-corrected four drifted anchors before landing; verify lane VERIFIED
  all 9 rules against their evidence (no overclaims) with 4 nits — 3 fixed
  at integration (2 anchor precisions, 1 heading scope), 1 accepted
  (authority enum observation). Godspeed verdicts: depth improved (craft now
  distilled to decision level), quality improved (verify-passed, zero
  overclaims), calibration improved (each rule carries exactly its evidence
  strength), expansion unchanged (no new surface — deliberate).
- 2026-10-14 — round-13 tail correction (parent-side, uncounted): the round
  commit message claimed "4 nits: 3 fixed" — in fact nit 1 (the r10-02
  anchor) had already been self-corrected by the distill lane before landing
  (the verify lane read a pre-correction cut), so only 2 fixes applied at
  integration (the r9-02 anchor range extended to :146-169 for the quoted
  moral; the heading scoped to "rounds 5-12, distilled in round 13"). Recorded
  so the round record matches the tree.
- 2026-10-14 — round 14 (goal-mode FINAL, 2 zai lanes + audit + parent): the
  Queue-B residual disposition + final sweep. r14-01: three of six 'blocked'
  items were exercisable after all — L203 fully discharged on its third
  input class (directional coverage law: right-complete x left-partial
  asserts removed), L204 discharged END-TO-END (the 'no SDK' premise
  corrected: dotnet RUNTIMES + nuget reachability make ilspycmd
  framework-dependent — first corpus success for managed reconstruction,
  import-managed-reconstruction under the exact-build lock), line 176
  discharged via the line-186 export chain with the main.js→lib.js edge
  parsed — Queue A+B now fully drained, no asterisks. Residue recorded with
  live-re-verified blockers and exact unblock actions: adb 22 (zero devices,
  ev_d4d8cc77 4th production), JEB x4 (key unset), ida x12 (config unset),
  hopper x13 (launcher absent). r14-02: final sweep — coverage map 56→70/70
  (14 rows backfilled, bookkeeping lag), r5 consistency checks 1/2/5/8 PASS,
  cross-citation health (one new phantom ev_2628de89 — fleet-attested,
  anchored at asar-surface by parent), promotion-eligibility recorded
  (eligibility only: 4 SHONEN gates with verifier evidence, carried debt
  resolved, 10 verified rounds — the operator decides promotion). Audit:
  both VERIFIED, one anchor nit fixed. Godspeed verdicts: expansion
  improved (the 'blocked' class shrank by half under live re-verification),
  quality/calibration improved, depth unchanged. THE LANE'S TENTH GOAL-ERA
  ROUND — kaidoku at 10/10.

## 2026-10-15 — operator-steered round 1: reconcile current assessment with landed REA evidence

- **Trigger / baseline:** `6645585873c4e66372b15687c47000abf8d91978:SCORECARD.md`
  still called r5 pending and planned its completed integration, while
  `LOG.md:172-194,402-423` recorded local completion through historical r14.
  The legacy card deliberately had no numeric axis fields. This is today's
  operator-steered r1, not a renumbering or rewrite of historical r1–14.
- **One axis move — calibration:** replace the expired current-state view
  with an evidence-backed assessment; restore bounded numeric fields and
  retain genuine residuals. `evidence/round-1-2026-10-15/rubric.json` freezes
  nine failure-selected reconciliation obligations and their baseline sources.
  The executed baseline jq count returned aligned=0, total=9, score=0;
  this is a newly reconstructed completeness proxy, not an old numeric score
  or unbiased accuracy. The closing entry records the committed after reading.
- **Controls, not extra moves:** source-object counting found 72 knowledge
  files / 70 mapped (9.72/10), missing exactly the two r14 notes; 9/9 existing
  queue-drain rules have resolvable file/range citations (10/10 structural
  proxy only). Baseline output: `evidence/round-1-2026-10-15/baseline.json`;
  reproducible recipes A/B: `SCORECARD.md`. Neither control implies full
  domain coverage, semantic correctness, or freshly executed holdings.
- **Attestation correction:** `SHONEN.md` now has four `[~]`, not four `[x]`.
  GateReviewer traced the cited r1–r4 reports and r2/r3/r5 audit waves to this
  lane and its dispatched workers; they are not outside promotion verifiers.
  Historical gate assertions and “kaidoku at 10/10” in `LOG.md:418-423` do not
  establish promotion eligibility or an expertise score. The latter counts
  ten goal-era rounds. No promotion or outside discernment review is claimed.
- **Single batched host dispatch:** planner CalibrationPlanner; connector
  OverlapConnector; executors CoverageExecutor, DepthExecutor, DebtExecutor;
  scribe EvidenceScribe; scout ProviderScout; reviewer GateReviewer; critic
  ClaimCritic. One `task` call spawned all nine role-routed workers. No model
  aliases, routing/config changes, padding, or separate UFO missions were used.
  Worker reviews remain same-lane evidence, not outside SHONEN verification.
- **Live re-verification:** ProviderScout's `binary_session {}` returned REA
  6.5.0, 207 MCP tools, 153 CLI commands, skill 42, catalog digest
  `805433f17bb4f709558ff20c04f96fe561fca2938fd0f459b1f8cc0f6b438ded`.
  It is status, not an Evidence-ID-bearing holding. The dated lesson
  `corpus/lessons/2026-10-15-round-1.md` preserves the excerpt, counting
  method, mixed client pins and known limits. Availability did not become
  coverage; old 6.4.0/170/v37 summaries are explicitly marked unresolved drift.
- **Executed smoke:** opened pinned `/usr/lib/libjq.so.1.0.4` under Ghidra
  12.1.4, decoded `0x117070` as `f30f1efa` / ENDBR64 (observed,
  shipped-artifact), exported the complete record, then closed the provider.
  Subject sha256 `7e8bccc6df37a55fb90703c9069b3770f5cdc502e96959c866d2f30fbf5e8b6b`;
  evidence `ev_f5e5da50ea8ff88ca9b26a97cebe1ac440c41414e0effd9bfe1943f464780481`;
  durable bundle `evidence/round-1-2026-10-15/rea-bundle.json`.
  `sha256sum` + `objdump -d --start-address=0x17070 --stop-address=0x17074`
  independently matched the carrier digest and instruction bytes. Static
  decode is not runtime observation or a safety verdict.
- **Residuals deliberately retained:** two unmapped r14 notes; family-specific
  evidence-ID law versus universal old summaries; obsolete README frontier
  and r13 fix counts; provider/client drift; device/provider/scale limits;
  historical “benign payload” scope bleed; missing historical fleet r5 report
  and ledger rows beyond r4. `SCORECARD.md`, Open gaps, names the exact sources.
  R5's local zstd/count/asar repairs are landed; fleet-only count/history
  debt remains separate. No domain source tree or sibling repo was changed.
- **Artifacts:** current SCORECARD; bounded SHONEN assessment; this append;
  new lesson and its index row; frozen rubric, baseline and native bundle.
  The post-change review/commit evidence is recorded in the closing entry
  and `evidence/round-1-2026-10-15/result.json`. The filed 2026-10-13 r1 fleet
  report will retain its original bytes and receive only a dated reassessment.

## 2026-10-15 — Interactive round-1 recovery: durable local evidence, admission blocked

- **Motivation and identity:** initial `git status --short --branch` showed
  `main` ahead by one commit, only untracked `.ufo/` native-session material.
  Work commit `c265db9bd3c0883fbaf4487f839559c85a736826` contained the new
  assessment, frozen rubric/baseline and old bundle, but its referenced
  `evidence/round-1-2026-10-15/result.json` was absent and no local report
  existed. Preserve all inherited bytes and sessions; recover the existing
  operator-steered r1, not round 2 or a reset of historical r1–14.
- **Correction to the promises at :480-484 and the old lesson :140-143,154-160:**
  the result now lands locally, with fresh **L1-author** source reviews.
  The interrupted worker's named specialist reviews are not reconstructed
  from transcripts or claimed completed. No fleet report reassessment or
  shared ledger update was written; those paths are outside this dispatch.
  The inherited 9/9 assessment is not an admitted or verified round.
- **Plan and wave:** `.ufo/rounds/interactive-r1/wwkd-plan.md` was saved before
  recovery mutations. The canonical `ufo-swarm-wave.mjs plan --spec <saved
  wave-spec.json> --route-families` returned exit 0, spawn=32, resume=0,
  total=32. Complete stdout/stderr/argv are retained in `wave-validation.json`.
  The 32 scopes were **not dispatched**: required content `@m_composer`,
  audit `@m_grok`, connector `@m_antigravity`→`@m_zfl` bindings are not
  realized by the existing overrides/cards. Observed executor/reviewer/
  connector `@m_mid`, scribe `@m_fast`, critic `@m_strong`; named
  antigravity fallback list empty. Exact shape evidence and operator unblock:
  `routing-observation.json`. No pins, overlays, global edits or provider
  health probes were used. Zero new L1s or L2s were spawned.
- **Fresh measurements:** immutable Git-object counting for baseline
  `6645585873c4e66372b15687c47000abf8d91978` and work commit `c265db9...`
  reproduced 70/72 mapped knowledge files and 9/9 resolvable citation blocks
  at both revisions. Recipe A: SCORECARD; full output:
  `.ufo/rounds/interactive-r1/source-measurements.json`. Recipe B executed
  with `/usr/bin/jq --slurpfile r evidence/round-1-2026-10-15/result.json`
  returned baseline aligned=0,total=9,score=0 and after
  aligned=9,total=9,score=10. Each after flag has its own reviewed source
  argument in the result. No semantic truth, mastery or outside review is
  inferred from counting flags or resolving citations.
- **Actual smoke:** REA `binary_session {}` reported closed, 6.5.0, 207 tools,
  153 CLI commands, skill 42, unchanged catalog digest. Opened only the pinned
  `/usr/lib/libjq.so.1.0.4` at SHA-256
  `7e8bccc6df37a55fb90703c9069b3770f5cdc502e96959c866d2f30fbf5e8b6b`;
  Ghidra 12.1.4 decoded `0x117070` as `f30f1efa` / ENDBR64, 4 bytes,
  observed/shipped-artifact. Evidence
  `ev_f5e5da50ea8ff88ca9b26a97cebe1ac440c41414e0effd9bfe1943f464780481`;
  exported `.ufo/rounds/interactive-r1/rea-bundle.json`, then owned close
  returned `result:null`. Independently ran `sha256sum` and bounded `objdump`
  as recorded in the recovery lesson, exit 0. No target execution, external
  live research or safety verdict.
- **Local acceptance evidence:** recovery gate initially returned
  `RECOVERY_EVIDENCE: COULD_NOT_EVALUATE finding=missing_result exit=2`;
  after result recovery, `RECOVERY_EVIDENCE: CLEAN
  finding=pinned_package_consistent author_review=9/9 coverage=70/72
  citation_rules=9/9 admitted=false verified_round_increment=0`, exit 0.
  `--selftest` exercised nine isolated subprocess exit/finding pairs and
  returned `RECOVERY_SELFTEST: CLEAN cases=9 exit=0`. `--admission` returned
  `ROUND_ADMISSION: COULD_NOT_EVALUATE
  finding=required_alias_bindings_missing+applicable_receipt_binding_missing
  exit=2`. Full unabridged verdicts, stderr and process codes:
  `.ufo/rounds/interactive-r1/gate-before.json`, `gate-results.json`.
  Expected snapshot digests and selftest outcomes are persisted in
  `expected.json`; registry is in SKILL. Evidence integrity is not native
  judgment or semantic review.
- **Per-axis verdicts:** inherited calibration move improved on its selected
  nine-obligation rubric; coverage/depth unchanged. Recovery adds durability,
  not another scored round. Expansion unchanged; quality improved only for
  the assessment evidence chain; discernment unchanged. Four SHONEN `[~]`
  remain author assertions. All named map/version/authority/scope/fleet
  history debt stays open; no domain frontier or promotion claim was added.
- **Receipt/continuation debt:** selected launch/pane/Sighting metadata names
  run/session `shk-kaidoku-interactive-20261015T050057Z`, mission
  `m_645cfa32b5284aaab568431141665df8`, pane `%14`, argv dispatch only.
  No taskKey or dispatcher-supplied prompt/config/receipt binding exists in
  those inspected metadata surfaces or the prompt. `receipt-binding-observation.json`
  records the shape-only check. Do not fabricate it from arbitrary hashes;
  mint/validate/complete were not attempted. Operator/integrator must provide
  both applicable binding and required role routing before a fresh authorized
  session recovers round 1. **Verified-round increment: 0.** No in-session
  continuation loop, saturation stop or at-least-100 success is claimed.
- **Landed-work handoff:** result, gate/fixtures expectations, full observations,
  recovery lesson/index, SCORECARD correction and this append are owned lane
  changes. The report/continuation land after the work commit and cite it;
  their exact hashes are recorded there. No push, shared report/ledger edit,
  host remediation or runtime/session transcript staging is authorized.

### Interactive recovery handoff durability

- Work landed at `23c0fd5f2e5838da737341ac468edabca1784da7`, lane identity;
  17 explicitly selected owned files, no push. The local report
  `.ufo/reports/round-1/kaidoku.md` and fresh-session continuation
  `.ufo/continuation/kaidoku-interactive-r1.{md,json}` were written after
  that commit and cite it. The receipt-binding/routing blockers, full gate
  verdicts and zero verified-round increment are included for the integrator.
- Read-only pane check `tmux display-message -p -t %14
  '#{pane_id} #{pane_current_command} dead=#{pane_dead}'` returned
  `%14 node dead=0`, exit 0. The interactive pane and native session
  material remain intact; no transcript bodies were read or staged.
- The following handoff-only commit lands this append and those three
  report/continuation files under the same lane identity. It does not imply
  receipt validation, Sighting completion, a new round or a fleet ledger write.

### Admission-diagnostic correction — no new round

- Review identified a real gate defect in `23c0fd5...`: the `--admission`
  branch raised the missing-binding finding unconditionally. The historical
  exit 2 in `gate-results.json` was a recorded blocker, not verification of
  its observation contents. This corrects that interpretation in the earlier
  recovery log/scorecard/lesson/report; original filed bytes remain intact.
- `verify-recovery.py` now parses the routing and receipt observations:
  required aliases agree with persisted expectations, observed aliases
  agree with canonical wave preflight, spawned/settled counts agree with
  the undispatched result, and receipt absence agrees with argv-launch
  metadata shape. Inconsistent contents fail before a blocker is emitted.
  `expected.json` persists the independent route/receipt contract.
- Three added fixtures exercise semantic contradictions behind re-pinned
  isolated snapshots: ready-versus-blocked routing, settlement without
  dispatch, and contradictory receipt absence. All twelve self-invocation
  subprocess cases matched their expected code/finding. The actual package
  returned evidence exit 0 and admission exit 2 with the same two derived
  blockers. Full commands/stdout/stderr/codes:
  `.ufo/rounds/interactive-r1/gate-correction-results.json`.
- Added `corpus/lessons/2026-10-15-round-1-admission-correction.md` and its
  index row; appended the SCORECARD correction. This is author correction,
  not outside discernment review or another axis-move. The SKILL registry
  remains required by canonical PROTOCOL Gate standard and accurately
  describes the local evidence gate; it is not a provider holding.
- Routing and applicable receipt authority remain blocked on the same
  operator/integrator actions. No wave dispatch, second L1, config change,
  receipt, push, Sighting completion or verified-round increment. Corrected
  work lands before the report erratum and updated continuation; a final
  actual-tree gate run will be observed before delivery.

- Admission correction work landed at
  `a3f2e1be58ceaaba1c57ba996698bd86b36123e6`, lane identity. After that commit,
  appended an erratum to `.ufo/reports/round-1/kaidoku.md` and the Markdown
  continuation; added `.ufo/continuation/kaidoku-interactive-r1-admission-correction.json`
  as the superseding machine handoff. The original report/JSON and full old
  outputs remain preserved. The handoff commit includes this LOG append;
  final actual-tree gate output is delivered by the command surface, without
  inventing an admission or a new verified round.

### luna-round-1 — coverage map 70/72 → 72/72

- Motivating evidence: baseline command A at `a79945c4` returned mapped=70,
  missing `2026-10-14-r14-01-queue-b-residual` and
  `2026-10-14-r14-02-final-sweep`, coverage_score=9.72, dangling=[], depth
  10.0 (9/9 rules). Both files were listed in the Knowledge table
  (`corpus/README.md:126-127`) but absent from the coverage map.
- Work: one axis-move on coverage, dispatched as one 64-seat wave on
  openai-codex/gpt-6-luna-max; seat reports at `.ufo/waves/luna-round-1/`
  (64/64 delivered). Adversarial seat C5 forced partial qualifiers on both
  new rows: r14-01 keeps device/operator-gated residue recorded not forced;
  r14-02 keeps checks 3/4/6/7 not re-run and a fleet-attested but
  corpus-unanchored evidence id reported not fixed. Seat D3's four-cell
  row-format claim was refuted by direct pipe count (every map row is 3 cells).
- Landed at `2abd30f5` (lane identity): two map rows after r12-02. Measured
  at `2abd30f5`: mapped=72, missing=[], dangling=[], coverage_score=10.0,
  depth_score=10.0, 9/9 rules; full output in the round report
  `.ufo/reports/luna-round-1/kaidoku.md`.
- Named debt for future rounds (V-seat drift hunts, deliberately not fixed
  under one-axis discipline): 12 coverage-map row drift findings plus README
  summary drift, all listed in the round report; the stale-summaries bullet's
  `:157` pointer is at `:160` in HEAD (seat C7). Four pre-existing untracked
  `.ufo/interactive-sessions/` files predate this wave; left untouched.
- Reviewer seat R4 self-reported a no-peeking breach (worktree grep returned
  M2's path metadata only); its convergence draft corroborated M2's substance
  and no row wording relies on R4-exclusive claims. Per seat R8 no SHONEN
  box advanced: all four remain `[~]`.

### luna-round-2 — per-client REA surface calibration

- Motivating evidence: SCORECARD open gap 'Version drift' — the 2026-10-15
  drift observation (live 6.5.0 / 207 tools / 153 CLI / skill v42 / catalog
  805433f1…) vs province/skill summaries still describing 6.4.0/170/127/v37
  as the surface.
- Work: one axis-move on calibration, dispatched as a 64-seat wave on
  openai-codex/gpt-6-luna-max (58 + 6 backfill after the parent's short-count
  error; the defect is recorded in the round report and fleet ledger, repaired
  in-round). Live receipts 2026-10-16 at
  `.ufo/waves/luna-round-2/receipts/`: doctor on both versions (exit 1,
  live_server unknown — package inventory, not process identity), MCP
  tools/list 207 (6.5.0, two independent runs) and 170 (6.4.0, two), CLI
  help censuses, catalog sha256s, skill versions, Ghidra 12.1.4 / JDK
  21.0.12.1 reverify, operator configs hash-identical before/after (seats
  S2/S5).
- Landed at `75af886a` (lane identity): PROVINCE surface summary now per
  client (Devin/OMP 6.5.0, Kimi 6.4.0), drift-prone values reverified with
  both cache/catalog identities, the Core table's present-tense per-client
  spawn clause reconciled; SKILL Domain 6.4.0 counts marked historical plus a
  dated per-client inventory paragraph. Historical cells (Core probe records,
  coverage-map evidence cells, LOG, lessons) untouched; no availability→holding
  inference (guard passes F1/F7 CLEAN).
- Named debt: the 6.5-only tool/CLI name set (seat A6: 37 tools + 27 CLI
  verbs) is recorded inventory, not holdings; provider env keys not re-probed
  (marked explicitly historical in the new text); seat B2's stale L7 receipt
  hash noted for its owning round; PROVINCE '3/7 clients registered' kept
  (seat A5 found it still accurate).
