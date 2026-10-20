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

### luna-round-3 — family-scoped evidence-id identity

- Motivating evidence: SCORECARD open gap 'Authority contradiction' —
  SKILL.md:211-214 and corpus/README.md:169 universally claimed evidence ids
  are `f(content, path, params)` (path-sensitive, cite `subject.digest.sha256`),
  disproven by corpus/knowledge/2026-10-14-r9-02-queue-a-ops-2.md:146-169
  (`analyze_function` ids hash analysis content + parameters, not path;
  module attribution travels in unauthenticated `subject`).
- Work: one axis-move on depth, dispatched as a 64-seat wave on
  openai-codex/gpt-6-luna-max (reports `.ufo/waves/luna-round-3/`, no live
  probes — corpus-textual round). Adjudication from primary sources: the r4
  lineage (corpus/knowledge/2026-10-13-r2-evidence-bundle-schema.md:244-250)
  verifies BOTH directions — the revenger-verifier family is path-sensitive
  (same bytes, different paths → different ids; jadx per-run, apktool
  deterministic), and r5-01:83-85 plus r9-02 verify `analyze`/`inspect`/
  `analyze_function` ids content+params-keyed. Critic C1's guard honored:
  anti-substitution and pinned-byte guidance retained; only the path-hash
  formula scoped.
- Landed at `638fb211` (lane identity): SKILL.md Known limits bullet and
  corpus/README.md Known gaps line rewritten family-scoped with three corpus
  citations each; corpus/QUALITY.md gained criterion 15 superseding 14 per
  that file's never-rewrite governance (#14 retained as the superseded row).
  PROVINCE untouched (C7's conditional request-byte pin for module-identity
  probes recorded as named debt, not this round's move).
- Measured at `638fb211`: command A unchanged (mapped 72, missing [],
  dangling [], coverage 10.0, depth 10.0, 9/9 rules); census — universal
  pattern active hits 0 (the one remaining literal hit is QUALITY row 14,
  retained by design as the superseded row). r9-02 cited mentions: 3.
- Dissent recorded: seat C8 argued re-scope to calibration; the parent kept
  depth (false domain claim removed) and adopted C8's contradiction-count
  observable as the round's primary measurement. Seat R2 wrote its report
  under a misnamed file (R2-reviewer-readme.md) — format debt only.

### luna-round-4 — freshness debt-drain (19-finding census)

- Motivating evidence: named drift debt from luna-rounds 1-3 — 12 V-seat
  map-row findings (round 1), README staleness post-round-2 (v37 line), the
  README:130 SKILL-range pointer (round 3), recorded in SCORECARD open gaps.
- Work: one axis-move on freshness (fleet axis; not a lane-owned proxy — the
  parent's recording ruling is in SCORECARD.md and the round report). Wave:
  64 seats on openai-codex/gpt-6-luna-max (58 + 6 backfill; the parent's
  short-count error recorded and repaired, same pattern as luna-round-2).
  Reports `.ufo/waves/luna-round-4/`.
- Landed at `6a71cd5` (lane identity, amended once pre-records: eight wording
  tweaks to satisfy the wave's own census matchers — each tweak reviewed as
  MORE faithful to the knowledge files): 14 repair groups in corpus/README.md
  — REA-service row (3/7 kept as the verified count + 8-client registry
  clarification + 10/10 unchanged r2 values + r4 fourth-consecutive verdict),
  archives row (120 deduplicated nodes / 130 occurrence hashes; AppImage
  ELF-only graph + unindexed overlay), Firmware row split (Firmware + new
  Frontier prerequisites row, token set held at 72), r5-01 timeout qualifier,
  r5-02 3/3-probed-of-286 scope, r9-02 status scope (inferred not evidenced),
  r12-01 per-leg fidelity (L200 byte-exact only), typora/libsignal/r4-15
  Knowledge rows, lessons round-13 pointer (SKILL.md:81-195), Known-gaps skill
  line as dated R4 record. Asar row + crash row adjudicated NO-CHANGE (V01a:
  row supported; D01: row supported).
- Measured at `6a71cd5`: command A unchanged (mapped 72, missing [],
  dangling [], coverage 10.0, depth 10.0, 9/9 rules); wave census 14/19 PASS
  + 5 ADJUDICATED-with-cause (F01 census encodes removing the verified 3/7;
  F02 encodes the refuted round-1 asar claim; F05 targets content no seat
  flagged — the flagged universal is the knowledge file's historical erratum,
  file debt for a future round; F16's replacement matcher encodes one wording,
  stale-pass verified; F18's z=1 is structurally unsatisfiable while the
  rea-skill-contract token exists, stale-pattern absence verified).
  Token set 72/72 PASS. Named debt carried forward: r1 asar knowledge-file
  framing (round 5+), r4u-01 firmware size decimals (C05), README stale
  frontier summaries (:157/:160 content), PROVINCE request-byte pin (C7,
  round 3), r9-02 file's own later-summary tension (V12b).

### luna-round-5 — freshness: seven debt dispositions, first two-lane wave

- Motivating evidence: the carried debt queue from rounds 3-4 (r1-asar file
  framing, r4u-01 size decimals, PROVINCE request-byte pin, README stale
  frontier + nits rows, r9-02 status tension, r5-02 ~283 wording, r12-01
  L197 inconsistency, revenger's open drift-governance question).
- Work: one axis-move on freshness, dispatched as the first 128-seat
  two-lane wave under the operator's updated contract — 64 luna seats +
  64 deepseek-v4.1-flash seats (58 + 6 backfill after the parent's third
  short-count; repaired, root cause named again). Reports
  `.ufo/waves/luna-round-5/`. Cross-lane convergence adjudicated by Z/R
  seats: item 2 (r4u-01) unanimous across 30 readings (both decimals wrong;
  29,367,752 / 84,258,816; one lane reconstructed the transcription slip);
  item 7 adjudicated — the L197 correction already existed as a landed
  erratum; item 6 confirmed '~283' mislabels a call count (281 calls + 2 jmp
  exact); revenger's open question answered with a PROVINCE scope note (map
  is live state; never re-bases a sibling's frozen receipts).
- Landed at `7125dd4` (lane identity, amended once pre-records: the
  Runtime-obs bullet opener renamed to 'Runtime-obs depth' to clear the
  wave census's stale-opener detector): five APPEND-ONLY knowledge errata
  (asar-surface, r4u-01-firmware-deep, r9-02-queue-a-ops-2, r5-02-call-targets-jq,
  r12-01-queue-b-ready), PROVINCE.md request-byte pin (same-physical-line at
  the probe conventions) + revenger scope note at the registry paragraph,
  corpus/README.md :131 (four-nit dispositions) + :163 (held-vs-frontier
  reconciliation, genuine residuals named).
- Measured at `7125dd4`: wave census 6/7 PASS + SIZES ADJUDICATED (the check
  compares a raw comma-formatted token against normalized text —
  structurally unsatisfiable; the erratum's arithmetic is established by 30
  lane readings + the inline recheck `29367752`/`84258816`); TOKENSET 72/72;
  MAP-ROWS byte-identical; command A unchanged (72/72, 9/9, 10.0/10.0).
  Append-only tails verified: every knowledge edit extends the file, no
  historical bytes rewritten.

### luna-round-6 — operability: pre-registered 10-leg e2e battery on REA 6.5.0

- Motivating evidence: luna-round-2 proved per-client package inventory
  (configured pins, catalog counts) but never running processes; the
  6.5-only verb set recorded by A6 was inventory, not exercise.
- Work: one axis-move on operability (fleet axis, unowned proxy). First
  TWO-LANE battery: 64 luna + 64 deepseek-v4.1-flash seats = 127 distinct
  seats (parent short-counted lane A 53/64 — fourth occurrence; the wave's
  128th slot was lost to a double-counted EX7 across an interrupted
  re-dispatch; recorded, counting self-check continues to fail upward).
  Predictions frozen by the parent before dispatch (prereg audited by PS4).
- Landed at `bc91424` (lane identity): the full receipt bundle is committed
  TRACKED (receipts/leg-1..10.md lane A, receipts-B/leg-1..10.md lane B,
  census-final.txt, census-laneB-final.txt) — a deliberate durability move:
  the round-5 r12-01 erratum had to attribute a numeral because /tmp receipts
  were gone; battery receipts now survive. Map/PROVINCE/SKILL untouched
  (measurement-only round); zero config drift (BC3); zero
  availability-to-holding upgrades (AC4).
- Measured: lane A 10/10, lane B 10/10 vs frozen outcome classes (AC1/BC1
  independent recounts); cross-lane class agreement 10/10, byte-identical
  L1/L2/L7/L10; frozen census PASS reproduced twice byte-identical (AC3/BC4);
  command A + token set unchanged (AC8). Defects recorded: lane-A manifest
  lists L1 only (RV5); BB7/BB8 original receipts overwritten by compare seats
  (custody; current bytes hash-match); L10 detoured to inspect_wasm_artifact
  (class preserved, predicted harmony fallback never executed); ~1.2GB /tmp
  battery litter (hygiene debt, other sessions may share /tmp — left).

### luna-round-7 — coverage: six 6.5.0-verb knowledge entries (72 → 78)

- Motivating evidence: luna-round-6's battery exercised six 6.5-only verbs
  with cross-lane receipts; the corpus held no entries for them (inventory
  vs knowledge gap).
- Work: one axis-move on coverage. Two-lane wave (64 luna + 59+5 deepseek);
  cross-lane drafting with convergence seats; wave catches folded into the
  FINAL-MANIFEST: hyphenated filenames (underscore stems break command A's
  map-token regex — three independent simulations), metadata fields on all
  six (source:/verified-at:/recheck:), entry 4 admits only lane-B's
  real-carrier SQLite result (lane A's synthetic fixture fails QUALITY-12),
  entry 2 keeps the two carriers distinct, entry 3 uses provider-exact fuse
  names + keeps E3D's resource bounds and reproducer, entry 5's call shows
  only the pattern argument (limit 100 is the tool default).
- Landed at `3395b6d` (lane identity): six entry files, six 3-cell map rows
  after r14-02, six 4-cell Knowledge rows at the table end. Prior 72
  entries byte-identical.
- Measured at `3395b6d`: command A — knowledge_files 78, mapped 78,
  missing [], dangling [], citation_resolved_rules 9/9, coverage 10.0,
  depth 10.0. Seat defects recorded: E4V/S1's 'receipts untracked' claim
  false (26 receipt files tracked at bc91424; parent re-verified); Q1-Q6
  graded absence not content (drafts landed after their reads); BB1 composed
  entries 3/5 without a prior gate pass (disclosed in the manifest THREATS).

### luna-round-8 — operability: REA 6.4.0 symmetry battery (78 → 79)

- Motivating evidence: luna-round-6 exercised the 6.5.0 surface; the Kimi
  6.4.0 pin had package inventory (round 2) but no live battery, and the
  six round-7 entries' 6.5-only scope deserved live corroboration.
- Work: one axis-move on operability. Two-lane wave (64 luna + 64
  deepseek). Frozen pre-dispatch predictions; 10-leg battery: version exact
  6.4.0; tools/list 170; the six 6.5-only verbs each TYPED-REFUSAL
  (-32602) on real carriers; six names absent from the 170-list; jq
  control RESULT (inspect_binary_layout; the literal `analyze` verb is
  absent from 6.4.0 too — fallback recorded). Scored 10/10 (CA6 census,
  PB0 independent re-verification).
- Landed at `18dc397d` (lane identity): the consolidated
  2026-10-16-l8-01-6p4-symmetry-battery.md entry + map/Knowledge rows
  (denominator 78→79; command A re-measured 79/79, 9/9, 10.0/10.0) and
  the round-8 receipt bundle committed TRACKED (round-6 durability
  precedent). QB3's two wording flags applied (leg-8-RV3 stdout-only
  identity; count computed from tools[].name).
- Defects/adjudications (ZB2 list): leg-3's display-layer hash defect
  self-repaired during the wave (current bytes = claim = /tmp raw); leg-10
  append-only supersession (head-hash preserved, MANIFEST annotated);
  eleven stale early-snapshot verdicts superseded by late evidence; zero
  config drift closed against the round-6 baseline (no round-8 pre-pair —
  carried debt); six-of-37 scope stated in the entry's limitations.

### luna-round-9 — freshness: carried-spill queue

- Motivating evidence: four carried items from rounds 3-8 debt lists
  (r4-16 stale two-site erratum; census instrument debt; /tmp-dependence
  question; jq-shadow safety-language bleed).
- Work: one axis-move on freshness, two-lane wave. All four items
  converged with gates (RB1-RB4 final texts certified clause-by-clause).
- Landed at `40162fc` (lane identity, append-only): r4-16 EOF erratum
  cross-referencing r12-01's corrected four-site account (two-site summary
  marked historical; "7 values" attributed, not re-derived); jq-shadow
  safety-verdict scope qualification naming all four 'benign' loci,
  scoped to byte-identity + recorded provenance, explicit non-endorsement
  per PROVINCE.md:114-116.
- Measured at `40162fc`: command A 79/79, 9/9, 10.0/10.0; both appended
  files prefix-identical to their base blobs (append-only proven);
  PROVINCE untouched; zero deletions.
- Item 2 (census known-limits) and item 3 (/tmp audit) land in this
  SCORECARD section and the round report: instrument limits documented as
  ADJUDICATED-not-PASS with a retest trigger; /tmp audit found NO current
  lane instruction or gate dependent on /tmp persistence (historical
  verify-recipes citing /tmp outputs are archival debt, labeled; L7-01
  npm-cache cold-start untested); ~1.2GB litter remains operator hygiene —
  no deletion authorized or performed.
- Carried debt (named, not landed): r3-jq-provenance companion bleed
  (:60,:136); stale :107-109 refusal pointers at SCORECARD.md:79 (frozen
  reconciliation table — untouchable) and lessons/2026-10-15-round-1.md
  (historical).

## 2026-10-16 — protocol conformance: SCORECARD contract fields

- Evidence and motive: 2026-10-16 operator amendment (fleet `84bade0`,
  `AXES.md:57-83` — §Capabilities, §The stagnation nudge, §SCORECARD.md
  contract table) adds `capabilities` and `saturation` to the contract.
  Already present here as real recordable fields: the axes score tables
  (§Owned axes; every round section), `planned` and `retired` (§Verdicts,
  planned, retired :152-156; each round section's closing lines, e.g. :610-613).
- Added by this rollout, additive only: `## Capabilities` (empty repertoire
  table plus its entry rule) and `## Saturation` (line and window N to be
  declared by the lane on its next round, not asserted here). No other
  section or file was touched in this change.
- No axis claim was made and no score moved: no capability row, saturation
  line, or stagnation window is asserted by this rollout; all pre-existing
  content is byte-identical.

### luna-round-10 — calibration: the arc closeout

- Work: one axis-move on calibration — the arc's self-assessment reconciled
  against its own evidence. Two-lane closeout wave: per-round auditors
  (W1-W10), debt-ledger collectors/reconcilers (both lanes' D/DB chains),
  SHONEN final assessment (S/SB seats), the arc census (C/X seats),
  adversaries (A/CB seats), and the final report assembly.
- Audit findings (all dispositioned in the round-10 report): four SCORECARD
  living-row rewrites inside records commits (rounds 2/3/4/7 — deviations
  from the append-only letter of the completion criterion; numstat-confirmed;
  disclosed, not retro-fixed); ten prose-decorated MANIFEST verdict values
  across nine rows (fleet rule: ledger slips are integrator-owned — the lane
  records, does not alter); five parent dispatch short-counts (round 7 now
  explicitly named) with round 6 at 127/128 distinct seats, structural;
  SHONEN 4x[~] arc-wide under the fleet's named-non-author-verifier bar.
- Declarations (per the 2026-10-16 operator amendment, fleet 84bade0):
  Capabilities rows for the two demonstrated battery forms (rounds 6/8);
  saturation line 10.0 on the finite proxies + stagnation window N = 10
  lane-rounds (capabilities entered inside the window — nudge not triggered).
- Measured at closeout: command A 79/79, 9/9, 10.0/10.0 (replayed at
  c343939 and 40162fc); 43 tracked receipt artifacts inventoried; arc
  statistics: 9 admitted rounds, 9 improved / 27 unchanged / 0 harmed,
  knowledge 72 -> 79, 19 lane-identity commits (N2/Y4 verified 46/46
  reachable commits), zero sibling writes, zero pushes (A5: ahead 24).
- Outbound debt routed (not absorbed): Tameshi's stale universal evidence-ID
  formula (verification-patterns-fleet.md:35,73,102) — correction routed to
  Tameshi's owner; tsukuroi ADJ-06 — remains integrator debt. Both verified
  sibling-side read-only.

- 2026-10-17 — README: Devin wiki link. Operator directive (2026-10-17):
  insert the Devin wiki link into the README header of every repository
  with a generated wiki. a `**Wiki:**` link added to the `README.md` header to
  https://app.devin.ai/org/veigapunk/wiki/VeigaPunk/shokunin-reverse-engineering?branch=main.
  Evidence: the org's Devin wiki index lists this repo's generated wiki;
  sibling lane READMEs carry the same `**Wiki:**` header.
  Documentation-only change; no round run, no axis moved.
### arc2-loop1-round1 — freshness + operability + depth: three claims

- Motivating evidence: carried debt named at the luna-round-9 close
  (`LOG.md:883-886`): the r3-jq-provenance companion bleed (`:60`,`:136`) and
  the stale `:107-109` refusal pointers; plus the luna-round-8 custody defect
  — zero config drift closed against the round-6 baseline with no round-8
  pre-pair (`SCORECARD.md:544-545`, `LOG.md:856-858`). First round of the
  reset stagnation window (`SCORECARD.md:624-632`, declared at luna-round-10).
- Work: one round, three claims, parent-integrated (no seat commits; seat
  reports `.ufo/waves/arc2-loop1-round1/`). C1 freshness: qualify the r3
  safety-label loci append-only; append the lessons correction note;
  adjudicate `SCORECARD.md:79` NO-CHANGE-with-cause (baseline-revision
  citation convention `SCORECARD.md:16-17`; in `## Open gaps`, not the frozen
  :39-49 table). C2 operability (capability acquisition): config custody
  pre/post-pair around the live battery. C3 depth: SKILL.md queue-drain rule
  #10 + custody SOP section.
- Dispatch (operator-directed): recovery dispatch — the first attempt
  delivered 18 seats (P1, P4, E1, E6, E7, E8, E11, E14, E17, E18, E20,
  E24, E25, SC1, R7, V3, V4, V5); the remaining 46 seats were dispatched
  as replacements on the devin provider per the operator directive of
  2026-10-18 (provider substitution directed by the operator, not a lane
  choice). 64 seat reports delivered.
- Landed at `58116aa` (lane identity, append-only): r3-jq-provenance
  EOF "Safety-verdict scope" note naming `:60` and `:136` (byte-identity +
  recorded-provenance scope, explicit non-endorsement per
  `PROVINCE.md:114-116`; form of
  `corpus/knowledge/2026-10-13-r2-jq-shadow-verdict.md:244`); lessons
  correction note (the `:152` `PROVINCE.md:107-109` token is
  baseline-correct, read at HEAD as `:114-116`; drift commit `7125dd4`);
  SKILL.md rule #10 (config custody pre/post-pair required for any
  zero-drift claim — a claim without a pre-pair is void; bounded by the
  already-landed luna-round-8 record only: `SCORECARD.md:544-545`,
  `LOG.md:856-858`,
  `corpus/knowledge/2026-10-16-l8-01-6p4-symmetry-battery.md:15`) + custody
  SOP; SHONEN.md pointer refresh; wave artifacts at `df31bfb`; SCORECARD.md
  round section + capability row entered (row draft E14/P3 reconciled;
  conditions per `AXES.md:62-64` met); receipts
  `.ufo/waves/arc2-loop1-round1/receipts/` committed.
- Battery (BATTERY seats; REA 6.5.0 served from the local npx cache, no
  network): leg 1 `doctor` live probe — exit 1, `healthy:false`, 22
  scope_checks (11 ok / 11 not-ok: 9 registration `config_drift` +
  hopper/ida `missing_analysis_engine`), identity `cli_package_version
  6.5.0`, 207 MCP / 153 CLI (E24); leg 2 `binary_session {}` census PASS —
  207 tools, 153 CLI commands, `tools_sha256 805433f1…`, `close_binary {}`
  → `null`, server exit 0, no process remains (E25); leg 3 PASS — pinned
  `/usr/lib/libjq.so.1.0.4` (sha256 `7e8bccc6…` exact match) open → decode
  `0x117070` → `f30f1efa` / ENDBR64 → bundle 18991 B exported → close
  `{"result": null}`, server exit 0, closure confirmed (E26); all opened
  sessions closed, zero residue (E28).
- Measured at `df31bfb`: command A 79/79, rules 9 → 10,
  citation_resolved_rules 10/10, coverage/depth 10.0; r3 unqualified
  safety-label loci 2 → 0 (`:60`,`:136` named by the appended note,
  historical bytes retained); lesson `PROVINCE.md:114-116` count 0 → 1;
  config post-pair re-verify — 3/3 sha256 byte-identical, drift 0/3
  (pre-pair `.ufo/waves/arc2-loop1-round1/receipts/config-pre-pair.txt:1-4`,
  `2026-10-18T14:49:13Z`, 3-way corroborated E11/V4/V5; post-battery captures
  E26 16:41–16:42Z after leg-3 close, E23 16:42:22Z, CR3 16:44:29Z, P3
  16:45:06Z; post-pair receipt
  `.ufo/waves/arc2-loop1-round1/receipts/config-post-pair.txt`,
  `2026-10-18T16:52:56Z`).
- Census scope (recorded here per the CR5 sweep): "unscoped benign loci
  N→0" is scoped to safety-sense artifact-verdict loci in editable corpus
  files (`corpus/knowledge/2026-10-13-r3-jq-provenance.md:60,:136`). The
  fleet token census also matches `corpus/README.md:90,:160` (unqualified
  safety-sense labels on the same jq verdict — deferred with cause) and
  `LOG.md:21` (frozen historical entry — not editable; non-endorsement
  recorded here).
- Defects / adjudications: doctor `config_drift` scope checks are
  environment checks, distinct from C2's three-file sha256 custody (E14
  threat note); E24 anomalies recorded (ghidra provider checks `ok:true`
  with `config_drift` classifications; `skill` stale at equal versions;
  `host` `arch unknown`). SC2 refutation carried, not landed:
  `PROVINCE.md:10,:18` claim Kimi `rea-agents@6.4.0` at `config.toml:1478`,
  but the file's only `rea-agents` occurrence is `6.7.0` at `:2940`
  (re-grepped this session).
- Carried debt (named, not landed): README `:90,:160` qualification
  (deferred with cause above); PROVINCE Kimi-pin correction; `SCORECARD.md:68`
  drifted `:160` pointer; `.bashrc`/`~/.profile` custody-pair extension from
  the next round's pre-pair; luna-round-9 /tmp-hygiene item unchanged.
- Scope: no config edits, no pushes, no writes outside this repo; client
  configs read as sha256 only; `PROVINCE.md` untouched.

### arc2-loop1-round2 — calibration + freshness + operability: three claims

- Motivating evidence: round-1's carried debt — SC2's live refutation of the
  Kimi pin (only `rea-agents@6.7.0` at `config.toml:2940`; `:1478` =
  `model = "kimi-k3"`), the README :90/:160 labels deferred with cause, the
  SCORECARD.md:68 drifted pointer (CR5), and E15's queued 5-path custody
  extension. Owned axis: calibration (most-falsifiable tie-break of the
  saturated 10.0 three-way).
- Work (parent-integrated; 64 seats on devin/deepseek-v4-1-flash-max, 60
  reports delivered — 4 non-completions recorded). C1 calibration: reconcile
  every current-surface pin statement to the 2026-10-18 live receipts,
  line-neutral (CR7's +18 shift attack would have staled 7 landed citations in
  append-only files — refused). C2 freshness: README :90,:160 in-cell
  qualification + SCORECARD:68-72 discharged-pointer reword (R2's 5-for-5;
  both debts discharged at 7125dd4). C3 operability: 5-path custody pair around
  a 2-leg 6.7.0 battery + SOP amendment.
- Landed at `b3cd790` (lane identity): PROVINCE.md (surface summary,
  drift-prone values, Core cells — "spawn"→"registers" per CR1's grade ladder),
  SKILL.md (inventory paragraph + SOP 5-path amendment, craft byte-identical),
  SCORECARD.md (Version-drift supersession :56-61, :68-72 reword, capability
  row), corpus/README.md (:90,:160 — whole file byte-matches the reviewer's
  certified prediction `ba7265eb…`); wave artifacts `b21c0da`.
- Measured at `b21c0da`: command A 79/79, 10/10 rules, 10.0/10.0; C1 census
  instrument (E22 v9) **PASS 0/0/0/0** on the work tree (6 hard-stale + 1
  contradicted + 1 ambiguous loci → 0); C2 n_unqualified 2→0, :68-bullet
  drifted pointers 2→0; custody in-window zero drift 0/5 (five captures).
- Battery (6.7.0, local cache): leg 1 doctor exit 1 / 27 checks / identity
  6.7.0 / `tools_sha256 af39310c…` (build-recorded constant; counts 153/207/6
  live-measured); leg 2 census PASS — 207 tool names byte-identical to 6.5.0,
  clean close. One registry packument revalidation observed (payload
  cache-served) — recorded, not hidden.
- **Drift event (the detector's first live catch):** `~/.kimi-code/config.toml`
  rewritten 2026-10-18T17:32:20Z — AFTER the post-pair closed the bracket at
  17:08:57Z. Pure additions (~295 lines of provider/model tables); the rea pin
  is byte-identical (`rea-agents@6.7.0`), relocated :2938→:3225; live hash
  `f10b01e9…` vs receipt `3546e033…`. Recorded verbatim at
  `receipts/drift-config-toml-20261018T173220Z.txt`; not repaired (operator-
  owned); in-window zero-drift claim stands; next live round's pre-pair
  re-baselines all five paths.
- Cross-domain findings (routed, not absorbed): CR1's wire-log probe — 0 of
  2195 Kimi client tool-logs declare `mcp__rea__*`, so the 6.7.0 server is
  configured-but-not-held on Kimi (plausibly never loaded); doctor lists 5 rea
  registrations (grok/codex included) outside the 5-path custody set.
- Carried debt: SCORECARD.md:270 stale `:157` parenthetical; MINT.md:10,
  corpus/QUALITY.md:18, lessons/2026-10-15-round-1.md:82,
  corpus/knowledge/2026-10-13-mcp-registrations.md:9,:80,:88 (dead
  `:1284/:1287` pointers), r4-16-frontier-rescan.md:43; SCORECARD.md:291
  (dated, historical); systemd user env + ~/.bash_profile carrier limits;
  Kimi-side rea load probe.
- Scope: no config edits (the drifted config was NOT restored), no pushes, no
  writes outside this repo; five custody paths read as sha256 digests only.

### arc2-loop1-round3 — freshness verified; coverage inconclusive; operability form-refuted

- Motivating evidence: the pointer-drift class (round-2 named debt
  SCORECARD:270 + mcp-registrations/r4-16 dead `:1284/:1287` pointers), the
  >90MB PE scale wall (PROVINCE's recorded next step), and three rounds of
  drifted-pointer bites motivating a citation-drift gate. Owned axis: coverage
  (most-falsifiable tie-break).
- Dispatch: 64 seats, `devin/deepseek-v4-1-flash-max`; 60 reports delivered
  (4 non-completions — second consecutive; named dispatch defect). One batched
  call.
- C1 freshness — LANDED at `fd30b9c`: PROVINCE.md:18 + SCORECARD.md:59
  re-anchored in place (line-neutral); append-only errata
  `corpus/knowledge/2026-10-13-mcp-registrations.md` (88→111, prefix-identical)
  and `2026-10-13-r4-16-frontier-rescan.md` (936→975, prefix-identical) — all
  content-anchored to `[mcp_servers.rea]` + the 17:55:49Z receipt sha256.
  Measured at `dbba2dd` (E23 instrument, unit = unwarned): **6 → 0**, minted 0.
  Dated records adjudicated NO-CHANGE-with-cause (SCORECARD.md:270, :698).
  Correction to round-2's own drift record (CR8 §3b): the 17:32Z rewrite's
  added tables were opencode-go-7, not alibaba-token-plan.
- C2 coverage — INCONCLUSIVE (honest stop): bisect leg held (2.5MB
  decompile.exe, exit 0, 44.117s, 6,337 procs, `ev_92dea347…`, deterministic
  rerun, RSS 1.63GiB). The 91.6MB leg ran 30m01s under
  `REA_GHIDRA_STARTUP_TIMEOUT_MS=3600000` + `GHIDRA_HEADLESS_MAXMEM=8G`, died
  at its own outer 1800s cap — typed `cancelled`, `cleanup:complete`, no
  evidence sealed, deadline never reached (RSS peak 8.89GB > `-Xmx8G`; the heap
  knob is load-bearing; r4-12's 900s wall is removed — the constraint moved to
  wall-clock depth). Claim cannot verify; no knowledge entry (CR3's
  re-run-dressed-as-a-move refusal); command A 79/79 both sides. Decisive-run
  recipe recorded (scoped systemd containment, TMPDIR off tmpfs, deadline-only
  >5400s).
- C3 operability — NOT VERIFIED (form refuted): gate implementations proven
  (E14 15/15 selftest; E15 10/10 + live red→green) but the form fails the Gate
  standard on measured grounds (unpinnable churning targets; false-positive
  surface on honest receipt-anchored citations; frozen clause 8-vs-9-line
  defect). Adjudicated to a future PROBE registration over in-repo citations
  (E16 row classes) with R6's fixes; the durable repair (content-anchor
  citations) landed under C1.
- Custody: pre-pair 17:55:49Z 5/5 (config re-baselined `bd5a78d1…` per round-2
  disposition). **Witnessed in-window mutate-and-revert** 18:01:40Z
  (`9ac8023b…`, +14 lines) → reverted 18:02:33Z via `cp -p` (mtime+inode
  restored; ctime survives); writer = interactive Kimi session afa2dd53 (CR8,
  from its own wire.jsonl). config.toml zero-drift claim VOID as bare; four
  other paths held; endpoints 5/5; excursion verbatim at
  `receipts/drift-config-toml-mutate-revert-20261018T180140Z.txt`.
- Carried debt: LOG.md:1005/:1018 receipt-anchored :2940 references (named
  correction = this entry); lessons/2026-10-15-round-1.md:82; errata-internal
  dead-token rise (unit stated); E22 census scope drift; C3 probe debt; E11's
  unreproduced 0-byte probes; the 17.7MB agent-browser PE rung (unrun).
- Scope: no config edits or restores (the reverted transient was left exactly
  as found), no pushes, repo-local only; five custody paths as digests only.

### arc2-loop1-round4 — depth + operability + freshness: three claims admitted

- Dispatch: 64 seats, devin/deepseek-v4-1-flash-max; 60 reports (4
  non-completions, third consecutive — standing dispatch defect). One batched
  call.
- C1 depth — LANDED at `265e1aa`: queue-drain rule #11 (operator-mutable file
  citations anchor by stanza key + receipt, never bare line numbers; token-
  free text per E21; SHONEN:6 refreshed same commit). Measured: command A
  rules 10→11, 11/11 resolvable, 79/79, 10.0/10.0.
- C2 operability — LANDED at `265e1aa`: citation-drift probe at
  `.ufo/gates/citation-drift/` (7989ed4e…; probe semantics: drift reported at
  rc 0, 2 = could-not-evaluate, --strict = gate map) + SKILL.md registry row;
  capability row entered. Selftest 10/10; findings=0 at HEAD; built from Z1's
  convergence (R3 F1-F3 + Z1's false-clean fix); zero graded config.toml line
  numbers.
- C3 freshness — LANDED at `265e1aa`: census v10 (v9 213fe679… re-keyed per
  Z1 §4d; fixed bounds — the open-ended form's laundering was measured and
  refused by CR3/P3/R3) → PASS 0/0/0/0 at the work tree; lessons:82
  append-only erratum (prefix-identity proven).
- Custody: pre-pair 19:03:02Z 5/5; in-window drift 19:17:21Z (config state 7,
  e0634d8c…, stanza :3155; writer interactive session session_2a39273f) —
  config.toml zero-drift VOID as bare; four other paths held; post-pair
  19:44:52Z 5/5 on the new baseline; drift record committed.
- Round infrastructure — the decisive 91.6MB PE run (CR2 containment: 7G
  scope, 1G swap, disk TMPDIR, 7200s deadline) OOM-killed itself at its own
  cap in 4m42s: kernel CONSTRAINT_MEMCG, one in-scope victim, zero bystanders
  (containment validated in the wild; REA mislabels the kill `cancelled`).
  Wall = memory (10 decompile workers + JVM ~7GiB), not time; next attempt:
  REA_GHIDRA_DISABLED_ANALYZERS + worker reduction. reset-failed executed.
- **Defect recorded:** `1692acb` ("rule 11", author `v <v@x>`) — seat V5's
  scratch chain aborted on a /tmp quota error before its `cd`, so its
  `git add -A && git commit` ran at the repo root: 4 pure additions (E23.md,
  E4.md, the pre-pair receipt, a stray root e16-table.json), zero
  modifications, no custody path. Kept in history per no-rewrite; stray file
  removed in `265e1aa`; seat pipelines never git-mutate (reinforced in
  dispatch templates).
- Carried debt: lessons:37 / LOG.md:685 / rubric.json:61 SKILL citations on
  shifted lines (pre-existing class); 60/64 dispatch defect; probe frozen-
  guard (probe-exempt); E22-v9 fence superseded by v10; /tmp tmpfs quota
  pressure across the wave (seats relocated to /var/tmp, evidence intact).
- Scope: no config edits or restores, no pushes, repo-local only.

### arc2-loop1-round5 — C1 archive audit

- Re-derived the r3 E23 C1 submetric from archived commits `679af5d` and
  `dbba2dd`: base unwarned loci 6→0. This is not a raw dead-pointer decrease
  (raw dead loci 6→12) or an overall instrument PASS; current host config
  `e0634d8c…` makes the historical `:3296`/`:3298` references minted, so the
  old `minted=0` is not replayable without the uncommitted `bd5a78d1…` config.
- Re-ran Command A: r3 `679af5d`/`dbba2dd` both 79/79 and 10/10; r4 work
  `1692acb`→`265e1aa` 10/10→11/11, 79/79 at both. `0e8c96b` is the later
  records descendant of `265e1aa`, not its before-state.
- R4 freshness comparison: archived v9 at `1692acb` FAILs with undeclared=2;
  v10 at `265e1aa` and `0e8c96b` PASSes 0/0/0/0. No separate r4 six-to-zero
  claim; the E23 unwarned-locus result remains 0 in both r4 trees.
- Audit of honest stops: r3's 30-minute outer cap did not test its 60-minute
  REA deadline; r4's later 7-GiB cgroup OOM likewise supplies no deadline
  result. The r3 gate-form `NOT VERIFIED` remains accurate; r4's replacement
  probe is a different deliverable and retains frozen-run guard debt.
- Evidence and detailed commands: `.ufo/waves/arc2-loop1-round5/P2.md`.
  Scratch confined to `/var/tmp/arc2-l5r5-P2/`; no corpus or sibling report
  edits, no config changes, no git mutations, and no live REA call.

### arc2-loop1-round5 — verification round: the audit catches a parent defect

- Dispatch note (corrected by this entry's own audit): the declaration said
  64 seats; the items array carried 60; all 60 completed (the round's wave
  reports). `openai-codex/gpt-6-luna-max`, one batched call, 100% delivery.
- C1 calibration — audit of rounds 1-4 at cited commits (git archive trees,
  fidelity verified): 20 measurements audited, 13 confirmed, 7
  dispositioned. Command A reproduced at df31bfb/b21c0da/dbba2dd (10/10) and
  265e1aa (11/11), 79/79 throughout; r4 probe selftest 10/10 + findings=0;
  census v10 PASS at 265e1aa/0e8c96b; r3 E23 unwarned 6→0 scoped-confirmed;
  r1 receipts MANIFEST 8/8 + prefix identities; README certification
  ba7265eb… at b3cd790; r4 SHONEN refresh confirmed.
- Dispositions: **(1) rounds 2-4's "64 dispatched / 60 delivered / 4
  non-completions" records are FALSE** — each wave dispatched 60 items and
  completed 60/60; the defect was a parent counting slip (count the items
  array, not the intent); corrections land here per append-only convention;
  **(2)** r2's "6 hard-stale" restated as 5 stale + 1 ambiguous (P1/S2/R1);
  **(3)** r2 census PASS receipt-scoped (v10 cannot replay the r2 tree —
  adjudicated; v9 replays PASS at b21c0da); **(4)** r3 raw 6→12 + minted=0
  receipt-scoped (config snapshot gone; the 19:17Z churn moved the stanza to
  :3155); **(5)** r4 probe --rev dead-revision reports at rc 0 instead of
  exit 2 (named debt); **(6)** CR4's axis point: reruns test reproducibility,
  calibration lives in the dispositions; **(7)** r3's honest stops affirmed
  in retrospect (E15).
- C2 operability — defect class identified + mitigation landed:
  `corpus/lessons/2026-10-18-wave-dispatch-counting.md` (roster-freeze
  protocol; re-dispatch rule for true shortfalls). README index row deferred
  (insertion would shift :177, staling a landed pointer — caught pre-commit).
- C3 freshness — missed-item register dispositioned per item (trio
  adjudicated: lessons:37 baseline-valid, LOG:685 dated, rubric.json frozen;
  probe frozen-guard named; v9 fence closed; zero unsafe edits).
- Custody: pre-pair + V3's matching capture + post-pair 5/5; no live probes
  (verification shape); no custody-path churn since the r4 post-pair (SC2).
- Process deviations: seat P2 wrote a LOG entry mid-wave (accurate content,
  retained; deviation recorded — seats do not write LOG).
- Carried debt: probe --rev; README index row + :177 re-point; GhidraClient
  citations; memory-scoped PE retry; E11's 0-byte probes.
- Scope: no config edits, no pushes, repo-local; verification reads only.

### arc2-loop1-round6 — coverage (mid-rung HELD) + operability + freshness

- Dispatch: 128 seats, `xai-oauth/grok-4.7-fast`, 128/128 delivered (r5
  lesson applied: roster frozen, items counted, method reviewed).
- C1 coverage — mid-rung HELD: 17.7MB agent-browser PE, 2479s at 6G heap,
  exit 0, `ev_8b688ce7…`, 11 segments / 19,012 procedures; NATURAL hold
  (envelope preset `ghidra-default` — no mitigation in force). Landed as
  knowledge entry + line-neutral map token: 79 → 80 (command A at b910a33:
  80/80, missing [], dangling []). Big leg honest-negative: 91.6MB service
  sealed `execution_failure` in 7.554s — the guessed analyzer name
  `Decompiler Parallel Convention Analysis` is not a Ghidra registry name
  (registered: `Call Convention ID`), REA aborts before disabling anything;
  refusal envelope committed as a receipt; the costume-retry attack was
  verified from the envelope before any claim.
- C2 operability — probe `--rev` preflight: dead/absent revision → exit 2
  `revision_unresolvable` (matches the registry row's declared map);
  selftest 11/11; all other behaviors byte-stable.
- C3 freshness — README lessons-index row + SCORECARD :177→:178 re-point as
  a coupled landing (the insert alone stales the probe — Z2 measured);
  probe findings=0 + census v10 PASS post-landing.
- Custody: pre/post pairs 5/5 on their own baselines; the two user-service
  runs touched no custody path; zero host OOM (containment corroborated).
- Process notes: the round-4 `--scope` lifetime trap was the fix pattern for
  both runs (`systemd-run --user` services, caller-independent). One parent
  no-op caught pre-commit by the grep gate (token append's sed pattern
  didn't match the row; re-applied by exact anchor).
- Carried debt: renamed-analyzer retry; r6-lesson index row (deferred pair);
  capability-row candidate.
- Scope: no config edits, no pushes, repo-local; service runs observed
  read-only.

### arc2-loop1-round7 — coverage (the wall falls) + depth + freshness

- Dispatch: 24 seats (items array counted at 24), zai/glm-5.3-flash, 24/24.
- C1 coverage — the 91.6MB wall FALLS: service `arc2-r7-pe` sealed HELD
  (mitigated) — 1424.663s wall, 7.9G/9G peak, zero OOM, `ev_a4aa9b0d…`,
  75,218 procedures; three validated analyzers disabled and proven honored
  (ghidra.log:276); zero decompile workers (the round-4 memory driver).
  Entry + token: 80 → 81 (command A at bd3b962: 81/81, 12/12 rules).
  Unknowns recorded: natural control, rerun id-stability.
- C2 depth — rule #12 (caller-independent services; adjudicated bounded
  form; corrected r4 story) + SHONEN 12/12.
- C3 freshness — caller-independent-services lesson + README row +
  :178→:179 coupled re-point; probe findings=0 + census PASS post-landing.
- Custody: pre-pair == service start (21:40:26Z); post-pair 5/5; no
  custody/repo fds on the service; r6 residue reset-failed.
- Process notes: the r5 counting lesson held (24 == 24); CR1's stop rule
  recorded — a fifth wall engagement without a new mechanism retires the
  thread.
- Carried debt: natural control; rerun stability; E41 probe-table gap;
  r7-lesson index row.
- Scope: no config edits, no pushes, repo-local; service observed read-only.

### operator directive — provider substitution (between rounds 7 and 8)

- Operator request 2026-10-18: run one deepseek round on the hyper provider
  instead of devin. Applied to the schedule: **arc2-loop1-round10 (this loop)
  rides `hyper/deepseek-v4.1-flash`** (64-128 seats); all other deepseek seats
  (loops 2-3's R1-R4, R10s) stay on `devin/deepseek-v4-1-flash-max` unless the
  operator directs otherwise. Recorded per the goal's substitution rule; the
  round-10 dispatch and records will cite this entry.

### operator directive — skip the 128-seat xai-grok rounds (between rounds 7 and 8)

- Operator request 2026-10-18: skip the 128-seat xai-grok rounds. Applied:
  **arc2-loop2-round6 and arc2-loop3-round6 are operator-skipped** — no wave,
  no claims, no axis moves; each closes with a records-only lane-identity
  commit (LOG entry + SCORECARD section + report stating the skip).
  Loop 1's R6 already ran (128/128, admitted 3/3) and is unaffected. Skipped
  rounds do not count toward the stagnation window. Recorded per the
  substitution/skip logging rule; the skipped rounds' records will cite this
  entry.

### arc2-loop1-round8 — the natural control seals the attribution

- Dispatch: 20 seats (items counted at 20), zai/glm-5.3-flash, 20/20.
- C3 calibration — natural control SEALED: `arc2-r8-ctl` (91.6MB, NO
  disabled analyzers, same caps/deadline as r7) kernel-OOM-killed at 9G in
  4m42.945s, 10-12 decompile workers, round-4's profile reproduced → the
  analyzer disable is PROVEN NECESSARY; r7 entry errata'd append-only
  (attribution scoped, not corrected); named unknown "natural hold" resolves
  (none at this cap). R1's fairness matrix: only the disable differed.
- C1 operability — capability row entered (contained user-service analyze,
  analyzer-disable recipe; first-working r7; r8 kill cited as necessity
  proof); insertion coupled with census SCOPE re-key + probe sc698 re-pin
  (wave-measured; both instruments green post-commit at 6bc4c29).
- C2 freshness — re-scoped by the wave (declared reading already landed in
  r7 — double-count avoided): mechanism-matched-walls lesson + README row +
  :179→:180 coupled re-point.
- Custody: pre-pair == service-start second; in-window config.toml drift
  (operator-side class) recorded; post-pair re-baselines; reset-failed on
  the spent unit.
- Process notes: the probe grades git objects at HEAD — gate runs belong
  post-commit (a pre-commit flag sent us looking for a phantom); roster
  freeze file still unwired (4th wave).
- Retired: the 91.6MB wall thread (CR1's stop rule).
- Carried debt: roster-freeze; README:22/:174 stale wall text; rerun
  id-stability; natural control at 7G.
- Scope: no config edits, no pushes, repo-local; the control service was
  observed read-only, never signalled.

### operator directive — round 9 model substitution (between rounds 8 and 9)

- Operator request 2026-10-18: run round 9 on codex luna max instead of sol
  max. Applied: **arc2-loop1-round9 rides `openai-codex/gpt-6-luna-max`**
  (16-32 seats); the loops 2-3 R9s keep the scheduled model unless the
  operator directs otherwise. Recorded per the substitution rule; round 9's
  dispatch and records will cite this entry.

### arc2-loop1-round9 — freshness (wall text) + depth (rule #13) + operability (roster)

- Dispatch: 24 seats (items counted), openai-codex/gpt-6-luna-max (operator
  substitution recorded), 24/24; roster frozen retrospectively (C3's
  amendment wires pre-dispatch freeze for rounds 10+).
- C1 freshness — stale pre-fall wall rows reworded same-line (:22 map, :175
  frontier; CR1's correction: :117 is the dated r4 synopsis, left historical;
  R1's limit: the r8 `cancelled` wrapper is not the OOM diagnosis — the
  rewords carry attribution via the erratum/journal). Stale-wall-state 2 → 0.
- C2 depth — queue-drain rule #13 (a mitigation claim carries its natural
  control; bounded, two corpus citations, token-free) + SHONEN 13/13;
  command A at 3fb6803: 81/81, 13/13, 10.0/10.0.
- C3 operability — roster frozen (`receipts/roster-frozen.txt`) + the
  counting lesson's wire-it amendment (pre-dispatch roster + items==roster
  assertion).
- Custody: pre/post pairs 5/5; no live probes (textual round).
- Carried debt: roster pre-dispatch wiring (operational at round 10); rerun
  id-stability; r4-row capability backfill (low value).
- Scope: no config edits, no pushes, repo-local.

### arc2-loop1-round10 — rerun id-stability (split) + probe extension + hyper census

- Dispatch: 64 seats frozen PRE-DISPATCH (the r9 gate's first run); ~59/64
  delivered — operator interrupted the wave; deficit recorded, not
  backfilled. hyper/deepseek-v4.1-flash (operator substitution).
- C1 calibration — BIG leg CLOSES: `arc2-r10-big` re-derived `ev_a4aa9b0d…`
  with a 5204-byte envelope byte-identical to the r7 receipt (cmp rc 0,
  parent-verified); id STABLE at 91.6MB; id domain measured (RFC 8785
  canonical JSON; excludes subject.name/local_path). MID leg = named debt:
  `arc2-r10-mid` oom-kill at 9G in 53.602s — a recipe-provenance error (the
  r6 run was uncapped at an 18.26 GiB measured peak); the r6 erratum names
  the containment requirement. Z1's discipline: one scale point answered,
  not two.
- C2 freshness — probe table 13 → 31 entries (E8's draft, CR2-constrained;
  "frozen-run" restated as a manual rerun); first live catch in-round
  (readme175-sc1217 needle) fixed; README:175 :1217→:1216 coupled re-point;
  findings=0 + selftest 11/11 post-fix.
- C3 adjacency — hyper-lane census recorded operator-facing: ~59/64 under
  interruption (operator-side, no lane conclusion); quality samples
  comparable; full table wave-limited.
- Custody: pre/post 5/5; services clean; containment corroborated (both
  kills in-scope).
- **Operator directive: PUSH authorized ("finish this round and push to
  remote") — executed post-records; the no-push scope rule yields to the
  explicit instruction.**
- Carried debt: mid-leg faithful retest (>18.3G or uncapped); the r10
  5-seat deficit; the full C3 census.
- Scope: no config edits; repo-local + the authorized push only.

### operator halt — regimen stopped at arc2-loop1-round10 (2026-10-18)

- Operator directive: "stop, this push is enough." The 3-loop x 12-round
  regimen halts with loop 1 at 10/12 rounds complete (all ten admitted per
  their per-axis verdicts; rounds 11-12 and loops 2-3 unrun). Published state:
  main == origin/main at 110cc08 (the round-10 records + the post-merge
  corrections). This entry is local-only — no further pushes per the operator.
  Resumption, if the operator wants it, starts at arc2-loop1-round11 with the
  recorded carried debt (mid-leg faithful retest, the r10 5-seat deficit,
  roster pre-dispatch wiring now operational).

### arc3-loop1-round1 — EVM real-solc leg + probe frozen-run guard + census E22 disposition (2026-10-19)

- New arc per the operator's 2026-10-19 directive (goal-scheduled, 14 rounds per
  loop). Claims frozen pre-dispatch at
  `.ufo/waves/arc3-loop1-round1/claims-frozen.md`; roster + items-array
  assertion held (64 = 64; a parent-side roster enumeration caught and recorded
  a draft miscount before dispatch — the r5 lesson applied to our own freeze).
- C1 coverage: solc installed under an isolated wave prefix (receipt: tarball
  sha256 `0e1a1ab6…575a51`; ambient global copy pre-existed, receipted prefix
  carries provenance); four on-host compiles; probe recovered planted selectors
  K/K on every runtime leg (`ev_45849c8b…` 5/5, `ev_56d89cb4…`/`ev_9259f412…`
  6/6, `ev_92b7e2fc…` 9/9 by the convergence seat, `ev_d0d0b054…` 11/11 attack
  carrier); creation legs parsed-and-empty (`ev_c80379e1…`, `ev_f875e21e…`);
  raw ≡ hex; rerun ids re-derive; independent keccak + disassembler recon
  agreed on every set/offset. Landed
  `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md` (10,225 B, sha256
  `dd986f56…`) + the line-neutral map row.
- C2 operability: citation-drift probe gained the frozen-run guard (probe
  `e2665074…`, expected `ff47bfd6…`, table byte-stable `738b3a56…`); selftest
  13/13; tampered/absent/unpinned baselines → declared exit-2 classes; findings
  = 0 at HEAD; the registry row states the semantics (one merged row).
- C3 freshness: census E22 disposition — v9 recovered byte-exact
  (`213fe679…`), FAIL at the 766-line tree reproduced, PASS at HEAD confirmed;
  one latent marker-line defect re-keyed (marker moved into its own row range)
  + G18 assertion added; disposition recorded in the instrument header
  (`6f1d19ff…`); creep audit 0 flags.
- Parent integration: applied the entry (with the critic's recheck fix — the
  host's `/tmp` quota fails this probe; disk-backed TMPDIR is required), the
  map row, the merged registry row; measured command A 82/82, 13/13 at the work
  commit; custody 5/5 zero drift across the wave (post-pair captured at
  integration). Wave interrupted by the harness: 54/64 seat reports, deficit
  recorded, not backfilled.
- Scope: kaidoku repo only; no pushes (the standing no-push rule holds; the
  round-14 git-audit round verifies commit correctness per the arc schedule);
  installs limited to npm solc under the wave prefix.

### arc3-loop1-round2 — rule #14 + census fail-closures + custody v2 (2026-10-19)

- Wave: 64 seats, opencode-go key 2; 64/64 delivered (first full wave of the
  arc). Claims frozen pre-dispatch; the freeze itself needed one discarded
  draft (roster arithmetic caught parent-side before dispatch — recorded in the
  round-2 freeze header).
- C1 depth: rule #14 (self-identity re-derivation) landed **form-fixed** —
  the raw seat payload cited a bare SCORECARD range (rule-#11 violation caught
  by RV-2/VZ-1); the verifier-applied fix (section-key anchor) is what landed.
  Command A at work commit `28aa7a9`: 14 rules, 14/14; prior 13 pure-insertion
  rstrip-identical. SHONEN:6 → `81-255`, 14/14 same commit. Fresh identities:
  SKILL.md 390 L `c134afcb…`; SHONEN.md `3edb044c…`.
- C2 freshness: census H1+H3 landed at `d0772ce8…` (610 L). Absent scoped file
  → FAIL `UNREADABLE`; neutered needles → FAIL `BLIND-INSTRUMENT`; ordinary
  PASS; scope byte-stable (creep audits 0 flags); the injection matrix and
  mutation tests are in the round-2 wave tree. Mid-wave block-unit floor
  revision false-FAILed HEAD; caught in-wave, re-keyed to detections.
- C3 operability: custody-pair v2 committed (`112d01dc…`, 889 L; selftest
  15/15). Same-content rewrite 0/13 → 13/13 detected; v1 label defect gone and
  reproduced-as-declared on old receipts (exit 12, sha256 contract 5/5); one
  merged registry row. First live catch: the Kimi client config drifted between
  integration captures (CONTENT-DRIFT, exit 10) — operator-side churn class,
  recorded not repaired; other 4/5 held.
- Scope: kaidoku repo only; no pushes; no installs; custody read-only.

### arc3-loop1-round3 — EVM optimizer leg + custody hardening + probe-table extension (2026-10-19)

- Wave: 64 seats frozen pre-dispatch on token-plan key 1. The lane exhausted its
  monthly quota mid-run (43 reports landed, freeze measured by the integrator's
  poller). Operator-directed devin backfill: 18 of 21 remaining seats re-dispatched
  and landed; final census 62/64 (EX-14, SC-3 reports pending, artifact trees
  complete). Substitution recorded with cause and per-lane counts.
- C1 coverage: optimizer-enabled + non-ERC-20 carriers recovered K/K across two
  pins with same-source optimizer-off controls (identical sets; binary-search
  layouts at K=8/11/13; zero decoy false positives). Landed the r3 entry with
  seven reviewer fix sets applied (fresh identity `bf39c584…`, 18,596 B) + the
  additive map token (README `a451ad16…`). The r1 entry gained an append-only
  erratum (creation blobs embed their runtime dispatch tables; `16ee4b79` is a
  CBOR-trailer artifact) — fresh identity `5761003f…`. Command A at `c418be0`:
  83/83, 14/14.
- C2 operability: custody-pair hardening landed at `7cd19c3c…` (1155 L; README
  `f30df42e…`): EACCES → UNEVALUABLE exit 14 (no fail-open MATCH), verify
  coverage gate, write-guard extended to set(paths) ∪ CUSTODY_PATHS (alias
  refusal measured), selftest scratch guard; selftest 15 → 22 with sabotage
  arms; round-2 regression 41/41. Registry row revised in the same commit.
  Live pair MATCH 5/5.
- C3 freshness: probe table 31 → 57 (+26) + quoted 4 → 5 (the r2 SHONEN-repoint
  record closed). C2↔C3 collision (precedence-clause anchor vs the revised row,
  four-seat-measured) resolved by the re-anchored optional-group needle + digest
  re-pin + same-commit landing. Census acceptance 12/12; findings=0 both modes.
- Custody: 4/5 held; the Kimi client config's pre-wave drift (12:57:45Z,
  operator-side class) recorded; v1 re-read contract reads 4/5 by cause.
- Hygiene: one committed `.pyc` caught by the pre-commit name check and removed
  in `5be4a26` + a root `__pycache__/` ignore. A mid-wave third-party clobber of
  the r1 historical receipt was observed, exonerated, and restored byte-identical
  within the same minute (two seats' reports).

## 2026-10-19 — arc3-loop1-round4 (work commit `40de383`; records this entry)

Round 4 of arc3 loop 1: 48-seat wave on the declared R4 fallback lane
`devin/deepseek-v4-1-flash-max` (hyper provider exhausted — 402 on all seats;
token-plan quota died mid-R3). All 48 reports delivered; three chains VERIFIED.

- C1 coverage: Vyper leg landed — `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md`
  (vyper 0.4.3, runtime 1,562 B, `inspect-evm-interface` 15/15 K/K at both pins,
  `ev_405e2a2a…`, third dispatch shape). Four review fix sets applied to the
  draft before landing (PUSH32-substring, same-path, argument-count mechanism,
  QUALITY cite); EX-07's 6.5.0-boundary correction applied to the r3 sibling.
  Map token added to `corpus/README.md` (83→84 mapped).
- C2 freshness: PROVINCE staleness census (6→9 rows under peer re-measurement:
  F2's sub-cap crashpad core inspects exit 0; C2 "35 features" a corpus
  miscount of its own 34-name list; C3 asar row names 9 where host holds 12)
  repaired same-line — EX-15's 8-hunk set + EX-12's asar-row patch + PL-2's
  coupled ghidra erratum, 162→162 lines, nothing above :116 shifted, B2 cites
  r12-02+r14-01. `JEB (unprobed)` adjudicated NO-CHANGE.
- C3 operability: custody-pair residuals closed at `520341d` (sidecar scope,
  mkdir guard, distinct-path gate, both-absent ruling; selftest 22→28; pair
  MATCH 5/5).
- Instruments at `40de383`: command A 84/84, 14/14, 10.0/10.0; census PASS;
  probe findings=0 both modes.
- Named debt: the census cannot grade Frontier-region repairs (UNDECLARED
  scope, R1 residual); `ptr_check` unreachable on pinned clauses (R2); the
  pre-existing dirty `.ufo/waves/arc2-loop1-round10/C3.md`; `/tmp` quota.

## 2026-10-19 — arc3-loop1-round5 (work commit `58c3db7`; records this entry)

Round 5 of arc3 loop 1: 64-seat correctness sweep on `openai-codex/gpt-6-luna-max`
(the scheduled R5 provider), all 64 reports delivered. The sweep re-derived
arc3 rounds 1–4 first-hand and dispositioned the arc2 carried debt.

- C1 calibration (sweep): all scoped numbers reproduce — command A at 7
  revisions (82→84), census PASS, citation-drift 0/0 both modes, custody 28/28,
  PROVINCE 162, Vyper 15/15 + sha `57d6fd0a…`. Five discrepancies caught and
  corrected: "all nine literals cleared" → 8/9 + adjudicated NO-CHANGE; custody
  invocation `--selftest` → positional `selftest`; revision grouping
  (`5be4a26` r3-hygiene, `520341d` r4-C3 parent of `40de383`); Vyper CODECOPY
  (2-byte entry, not 26-byte table); roster-table TB omission.
- C2 coverage (corpus audit): three dated entries audited per-claim; selectors
  / identities / dispatch shapes VERIFIED. Append-only errata landed — r4
  initcode (parsed-and-empty ≠ byte absence; runtime embedded at +20), r4
  "no Core promotion" (superseded by `40de383`'s own PROVINCE `Core, arc3-r4`),
  r4 CODECOPY wording, r1 Smoke digest domain, r3 initcode + matrix-only rows
  recorded UNVERIFIABLE.
- C3 freshness (debt): mid-leg retest STOPPED (operator host-cost gate not
  evidenced — honest stop); r10 deficit DISCHARGED-BY-PRECEDENT (corrected set
  E1,E17,E28,R7,CR1); hyper-vs-devin census CARRIED-forward (denominators not
  reconstructible in-repo).
- Instruments at `58c3db7`: command A 84/84, census PASS, probe 0/0, custody
  28/28, PROVINCE 162.

## 2026-10-19 — arc3-loop1-round6 (work commit `2fba56f`; records this entry)

Round 6 of arc3 loop 1: 48 seats, delivered as 3 zai + 45 opencode-go-7 after
two provider substitutions and two dispatch interruptions. The scheduled
`xai-oauth/grok-4.7-fast` returned 403 on all seats; the zai wave was
interrupted after 3 seats delivered verified artifacts (kept); `antigravity/
gemini-3.8-flash` and `cursor/grok-4.7-xhigh-fast` were each interrupted at
dispatch; the 45 remaining seats completed on `opencode-go-7/deepseek-v4.1-flash`.

- C1 operability: census Frontier blind spot (R1 residual since r4) CLOSED —
  PL-4's G21 frontier-register patch applied to `c1-census-v10.py` (sha
  `d0772ce8…` → `80027570…`, 713 lines). The register pins each Frontier
  bullet's span and asserts REQUIRED anchors + FORBIDDEN retracted literals;
  the reintroduced stale literal now FAILs `FRONTIER-STALE` where v10 read
  PASS. Clean tree PASS, 14 rows asserted, errors []; 17 shared counters
  unchanged.
- C2 coverage: the r3/r4 `viaIR` Unknown CLOSED —
  `corpus/knowledge/2026-10-19-arc3-r6-viair-dispatch-shape.md` (EX-7's entry
  with VZ-3's three corrections: CBOR `73`→`64`, the 15-functions census, the
  SUB-leg scoping). viaIR compiles a fourth dispatcher class (inverted guard
  + linear EQ chain + `SUB`-terminated leg); probe K/K 15/15 both pins. Map
  token landed; command A 84→85.
- C3 depth: rule #15 landed (corrected `a1bceb40…` text — the `:34`→`:29` and
  `r1:24`→`:31` citation fixes applied): parsed-and-empty ≠ byte-absence —
  settle byte questions with a census, not the probe's function count.
  `rule_blocks` 14→15, all 15 resolved.
- Instruments at `2fba56f`: command A 85/85 + 15/15, census PASS + G21
  register, probe 0/0 both modes, custody 28/28, PROVINCE 162.

## 2026-10-19 — arc3-loop1-round7 (work commit `7deeb36`; records this entry)

Round 7 of arc3 loop 1: 24 seats on `openai-codex/gpt-6-luna-max` (zai slot —
the lane is usage-exhausted; operator directive substitutes luna-max for all
remaining zai slots this session). All 24 reports delivered.

- C1 operability: `ptr_check` blind spot — mechanism proven (candidate patches
  catch seeded dead pointers, G21 + 19-key JSON intact) but landing withheld:
  the live `PROVINCE.md:18` pointer is `:3546` (not the `:3298` receipt the
  claim named) and reads `stale`, so no patch satisfies "clean PASS" without a
  fake anchor or a live FAIL. Adjudicated PARTIAL — recorded in
  `claims/c1/C1-ADJUDICATION.md`; the pointer needs a re-anchored receipt
  before the instrument can grade it.
- C2 coverage: `ev_` Evidence-ID formula Unknown CLOSED —
  `corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md` (EX-3's
  entry; `ev_` + sha256 of canonical JSON over the semantic projection;
  path-bearing fields affect the id, display fields don't; 8/8 envelopes
  recomputed). Map token landed; command A 85→86.
- C3 calibration: pacman inventory re-derived — 1350 live vs dated 1556
  (−206, cache eviction, retention-varying). No-edit adjudication on the dated
  value; append-only erratum landed on the pacman entry.
- Instruments at `7deeb36`: command A 86/86, census PASS + G21, probe 0/0 both
  modes, custody 28/28, PROVINCE 162.

## 2026-10-19 — arc3-loop1-round8 (work commit `53fcf0c` + probe fix `227443e`; records this entry)

Round 8 of arc3 loop 1: 24 seats on `openai-codex/gpt-6-luna-max` (the second
zai slot — lane usage-exhausted, operator substitution). All 24 reports
delivered; the wave caught a pre-existing gate FAIL (the r7 SCORECARD section
outside declared scope) and folded its fix into the coupled landing.

- C1 operability: `ptr_check` blind spot CLOSED — EX-1's candidate applied
  (gate sha `80027570…`→`e4fb740c…`). The `if not occ` suppression removed so
  `path:line` pointers are collected in pin-carrying clauses; a new
  SCORECARD DATED row (1759-1813) fixes the undeclared FAIL; DATED stale
  pointers class `historical`. Live `:4126` evaluates `current-ok`; a dead
  re-key FAILs `stale=1`. G21 + 19-key JSON + prior counters intact.
- C2 freshness: PROVINCE pin pointer re-anchored `:3546`→`:4126` in the same
  commit (the live `rea-agents@6.7.0` line; `:3546` had drifted to a Copilot
  block). Receipt at `.ufo/receipts/arc3-loop1-round8-kimi-rea-line.txt`
  (content sha `eb237377…`/`eb1c7da7…`). The `17:55:49Z receipt` needle
  restored contiguous in `227443e`.
- C3 coverage: Vyper non-default-optimizer Unknown CLOSED —
  `corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md`
  (EX-8's entry): `--no-optimize` an EQ/ISZERO chain, `-O codesize` a packed
  selector/target table, `-O none` ≡ `--no-optimize` resolved. Map token
  landed; command A 86→87.
- Instruments at `227443e`: command A 87/87, census PASS + G21 + live
  pointer `current-ok`, probe 0/0 both modes, custody 28/28, PROVINCE 162.

## 2026-10-19 — arc3-loop1-round9 (work commit `eb5a2c4`; records this entry)

Round 9 of arc3 loop 1: 48 seats on `openai-codex/gpt-6-luna-max` (scheduled
provider). All 48 reports delivered; the wave caught a second pre-existing
gate FAIL (the r8 SCORECARD section's pin outside the declared scope row) and
its fix folded into the landing.

- C1 freshness: `PROVINCE.md:50` perishable-value residual repaired same-line —
  the 1556 count now carries the dated qualifier + the live 1350/−206 delta +
  the `available:true` clause dated. SCORECARD scope re-keyed 1759-1813 →
  1759-1870 to fix the r8-section undeclared FAIL; instrument reads PASS.
- C2 coverage: viaIR final-selector-miss residual CLOSED —
  `corpus/knowledge/2026-10-19-arc3-r9-viair-fallback-miss.md` (EX-8's entry):
  the `SUB`-leg mismatch branch distinguishes the no-fallback revert path from
  the payable-fallback storage-write path; 15/15 both variants. Map token
  landed; command A 87→88.
- C3 calibration: pin-line drift class characterized — sole `rea-agents@`
  match at `:4126`, `current-ok`; position-sensitive not content-sensitive;
  recorded on the r8 receipt.
- Instruments at `eb5a2c4`: command A 88/88, census PASS + G21 + ptr
  `current-ok`, probe 0/0 both modes, custody 28/28, PROVINCE 162.

## 2026-10-19 — arc3-loop1-round10 (work commit `9c1d1fe`; records this entry)

Round 10 of arc3 loop 1: 48 seats on `openai-codex/gpt-6-luna-max` (scheduled
devin-deepseek slot — the devin lane is exhausted, operator substitution).
All 48 reports delivered.

- C1 coverage: second verb family's `ev_` formula CLOSED —
  `corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md` (EX-4's
  entry): `inspect_rust_binary` is path-sensitive (its semantic projection
  carries path fields); all four envelope IDs recomputed. Map token landed;
  command A 88→89.
- C2 depth: rule #16 landed (SC-2's "Co-land every truth dependency"): name
  the dependency, land the complete set in one commit, a scratch projection
  is not a landed result. `rule_blocks` 15→16, all 16 resolved.
- C3 operability: G21 register's append-past-:162 residual CLOSED — PL-3's
  unregistered-bullet guard applied (sha `e4fb740c…`→`d6b4deaa…`); a seeded
  bullet at :163 now FAILs `FRONTIER-UNEVALUABLE`.
- Instruments at `9c1d1fe`: command A 89/89 + 16/16, census PASS + G21 +
  unregistered-bullet guard + ptr `current-ok`, probe 0/0 both modes, custody
  28/28, PROVINCE 162.

## 2026-10-19 — arc3-loop1-round11 (work commit `5ee13b3`; records this entry)

Round 11 of arc3 loop 1: 32 seats on `openai-codex/gpt-6-luna-max` (scheduled
zai-max slot — lane usage-exhausted, operator substitution). All 32 reports
delivered.

- C1 coverage: third verb family's `ev_` formula CLOSED —
  `corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md`
  (CR-2's entry): `inspect_artifact`'s outer id is path-sensitive (nested
  inventory Evidence inside `normalized_result`); the nested id is
  path-stable. Map token landed; command A 89→90.
- C2 freshness: three receipts re-derived — Ghidra 34/39 (delta 0/0), pacman
  1350 + 1350 sig (delta 0 vs r9 live), ASAR 12 (bounded by unreadable
  `/opt/containerd`). No errata needed.
- C3 calibration: `available:true` scope re-derived — provider group
  `rea-artifact-graph` `available:true`, targetless per-tool entries
  `available:false`/`target_required`; attached Kimi session
  `unknown`/`config_drift`. Recorded on the pacman entry.
- Instruments at `5ee13b3`: command A 90/90 + 16/16, census PASS + G21 +
  guard + ptr `current-ok`, probe 0/0 both modes, custody 28/28, PROVINCE 162.

## 2026-10-19 — arc3-loop1-round12 (work `4072ebb`, fix `6a35398`; records this entry)

Steered round 12, finished as frozen. 48 seats frozen on
`openai-codex/gpt-6-luna-max` (antigravity down, operator substitution);
47/48 delivered, `CN-1` named non-completion; halted at `de77d75`. Integrated
in session kaika W2a with a 10-member batched L2 swarm. Motivating evidence:
`.ufo/waves/arc3-loop1-round12/claims/verdicts/VZ-1.md` (one candidate per
claim), R12Critic (no claim falsified; C3 scope narrowed), R12Reviewer and
R12Mutation (C3 needles: PL-4 17/24 kill → order-free token lookaheads).

- C1 coverage: fourth `ev_` family CLOSED —
  `corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md`
  (`inspect_go_binary` path-sensitive via three semantic path fields; live
  rerun reproduced `ev_87621921…`; 27/27 stored ids reconciled by a retained
  script). Command A 90 → 91.
- C2 depth: rule #17 (projection-local field sensitivity) at
  `SKILL.md:293-314`; command A 16 → 17; SHONEN count correction at EOF.
- C3 operability: three `recheck:`-grading rows (0 → 3; entries 57 → 60;
  `expected.json` pin `7994eec7…`); seeds 3/3 caught, selftest 13/13.
- Harm caught and fixed: `4072ebb` shifted pinned README/SHONEN lines
  (strict probe findings=5); `6a35398` restored them (findings=0).
- Lesson `corpus/lessons/round-12.md` (ten mistake classes, `## Gate`);
  QUALITY criteria added: none (claim cap held by the frozen claims).
  Class #10: the census's default `--root` is the lane main checkout; the
  round's census figures come from `git archive <rev>` trees with `--root`.
- Custody: unpaired live legs disclosed; post-only receipts under
  `.ufo/waves/arc3-loop1-round12/receipts/` bracket an operator-side
  `~/.bashrc` change at 21:46:35Z after the last live leg.
- Instruments at `6a35398`: command A 91/91 + 17/17, census PASS, probe strict
  clean, selftests 13/13 and 28/28, PROVINCE 162.

## 2026-10-19 — arc3-loop1-round13 — source-curation capability (records this entry)

Godspeed directive: name coverage/depth/calibration; iterate in parallel; keep
only source curation that improves future learning without upgrading source
documentation into held REA capability. The r12 claims remain frozen and
closed. This steer is one source-registry capability only; no ARM64X carrier,
analysis run, new knowledge entry, or numeric score change.

- Created `corpus/SOURCES.md` under the integrated Contract v1: 11 columns,
  scope-specific tiers, opened anchors and quotes in the lesson Gate, ordered
  study paths, one bounded search log, unopened leads, and S022 retained as a
  scoped rejection with a concrete flip condition.
- Census — `0 → 22` rows, measured by
  `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/kaidoku-shokunin /home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/kaidoku-shokunin`
  on 2026-10-19. Before: registry missing, FLEET.rows=0, exit 1. After:
  FLEET.rows=22, tier.A/B/C=20/1/1, status.mined/rejected=21/1,
  invalid=0/0, missing=0, exit 0. No existing row was corrected in place.
- Lesson `corpus/lessons/round-13.md` records 22 round-local source openings,
  the selection search, the author mistake, and the orchestrator-owned
  non-author fresh re-open/admission limit. `QUALITY.md` receives only its
  required tier/source pointer; `SKILL.md` receives one durable registry
  pointer. No README index or PROVINCE frontier anchors moved.
- L2: one batched call, eight leaf seats — planner, connector, scout, scribe,
  reviewer, critic, and two disjoint executors. Their reads identified
  frontier paths, reopened installed Go/BSim sources and primary papers/docs,
  checked contract traps and source-scope risks, and found the SoK full text
  unavailable. No L2 made file edits; their dispatched outputs are not the
  outside admission check.
- No target binary or artifact was executed; no live REA provider/session was
  probed; no ARM64X capability was attempted. The orchestrator owns registry
  admission and a fresh non-author source sample. Round report:
  `.ufo/reports/round-13/kaidoku.md`.

## 2026-10-19 — arc3-loop1-round13 post-review correction (append-only)

The parent completed a fresh non-author source review after the lane commit.
It agreed with representative source admissions (S003/S008) and the S022
rejection, while finding citation-fidelity defects in the S017/S018 Gate
quotes. The lesson now appends the exact View8 CLI sentence and the Check
Point `Introduction` location; `SOURCES.md` anchors themselves remain valid.

Trend correction: expansion is **unchanged**, not improved — no uncovered-
ground `knowledge/` entry was admitted; source rows and the source-curation
capability are tracked separately. Quality is unchanged; discernment is
**improved** because the outside sample agrees with the source dispositions.
No numeric axis score changed. Follow-on: round 14 may admit a source-backed
knowledge entry only if the same coverage-map question remains uncovered.

## 2026-10-20 — round-14 — source diagnosis and quote-regression instrument

Claims: C1 **depth**, source-backed Go RTTI bootstrap differential diagnosis;
C2 **calibration/capability**, a local captured-quote regression gate. The
initial coverage label was rejected before integration because the
cross-version Go surface was already held; `claims-review.json` preserves
the attribution refinement without reducing the technical deliverable.

- Motivation: the prior non-author spotcheck caught a spliced S017 quote and
  S018's wrong section (`corpus/lessons/round-13-verifier-spotcheck.md`).
  `corpus/lessons/round-14.md` mines both and grounds QUALITY #16.
- C1 lands `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md`, citing
  reopened S001/S003/S004/S007. It distinguishes a range warning that
  continues from the conditional invalid-snapshot bootstrap failure; the
  historical op run's exact cause stays unknown. An append-only correction
  marks the older causal inference superseded; same-line README/PROVINCE
  edits remove current causal overstatement without shifting frozen anchors.
- SKILL receives a source-only diagnostic table and a quote-fidelity
  registry row at the end, leaving existing craft anchors intact.
- C2 lands `.ufo/waves/round-14/tools/quote-fidelity.py`, isolated selftest
  cases, frozen source/manifest pins, paired wrong/corrected quotations,
  and documented raw-excerpt limits. At this work-entry stage no unrun
  check is called passed; measured outcomes follow in the records entry.
- Frontier: no new source rows; permitted used-by appends on
  S001/S003/S004/S007/S017/S018 are logged old→new in the lesson.
  Source snapshots are short disclosed excerpts, not redistributed full pages.
- One validated batched wave: `.ufo/waves/round-14/spec.json`,
  `dispatch.json`, and `w1/swarm-registry.json`; L1 holds the canonical
  planner seat, with bounded planning walks in CoverageGap/ClaimSeparation
  and adversarial axis attribution in AttackNovelty/AttackTrends.
  Advisory seats do not supply a non-author promotion or admission check.
- Initial lane status was clean; no inherited round work was swept.
  The prior verifier lesson is untouched. No target/provider execution,
  client configuration change, tool installation/update, or new L0 question.

Round-14 correction to historical LOG line 99: “Go toolchain bump …
collapses symbol recovery” describes a difference recorded across two builds,
not a controlled causal result. The same qualification supersedes the old
layout-cause sentence in r4-10. Original log bytes remain append-only.
The bounded sweep is retained in `.ufo/waves/round-14/correction-sweep.json`;
current README and PROVINCE summaries now state historical inventories,
with the old run's precise cause unknown.
