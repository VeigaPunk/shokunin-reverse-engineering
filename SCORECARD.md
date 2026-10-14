# kaidoku-shokunin — Scorecard

Axis record promised at `README.md:15-16`, per the fleet contract
(`AXES.md:33-38`). Primary verdicts are the three learning trends — what this
lane actually measures every round (`LEARNING.md:23-36`); the fleet's six axes
(`AXES.md:7-16`) are secondary readings of the same evidence. Verdict
vocabulary is `improved` / `harmed` / `unchanged` / `unprovable-but-better`,
never scalar (`LEARNING.md:25-26`) — no 0–10 scores are recorded here by
design. A trade is reported as a trade, never admitted (`LEARNING.md:34-35`).

State at writing (2026-10-13): rounds 1–4 are integrated (`LOG.md:3-105`,
commits `a43d442`→`f507327`); round 5 is mid-flight — its wave artifacts are
landed under fleet `.ufo/waves/kaidoku-r5/` but not yet integrated (see
`## Carried debt`). Mint context: round 0, sibling mint, rationale in
`MINT.md` (`LOG.md:3`).

## Primary verdicts — the three trends

| Trend | CURRENT verdict | Evidence |
|---|---|---|
| expansion | improved | 14 entries admitted r1 (`LOG.md:4-6`) → +12 r3 (`LOG.md:37`) → 18 r4-era files, `r4-05`…`r4-16` + `r4u-01`…`r4u-06` (`.ufo/waves/kaidoku-r5/04-audit-consistency.md:14-15`); new held surfaces enumerated r4 (`.ufo/reports/round-4/kaidoku.md:22-28`). Known lag: the coverage map holds 44 of 56 files — in-flight repair, `## Carried debt`. |
| quality | improved | Bar grown 9 criteria + 5 weak signals r1 (`LOG.md:6-7`) → 14 + 6 (`corpus/QUALITY.md:9-35`; 12–14 landed r4, `LOG.md:79-80`). Prior-round entries re-verified each round with all verdicts upheld: r1 ~100 verify re-runs (`LOG.md:16-17`), r2 (`LOG.md:34-35`), r3 (`LOG.md:48-50`); r5 adversarial audits: 13/13 files HOLD, "Nothing rises to REFUTED" (`.ufo/waves/kaidoku-r5/01-audit-A.md:19,140,212,306`, `02-audit-B.md:110`, `03-audit-C.md:12`). |
| discernment | improved | Deliberate rejects kept as calibration assets (`corpus/lessons/2026-10-13-round-1.md:5-9`); audits uphold admits AND rejects (`corpus/lessons/2026-10-13-round-2.md:11-13`). Disagreements became grounded criteria, not relaxations: criterion-5 labeling gap (`corpus/lessons/2026-10-13-round-2.md:21-23` → known gap `corpus/README.md:124`); `grep -c` verify defect → criterion 13 (`corpus/lessons/2026-10-13-round-4.md:5-7`, `corpus/QUALITY.md:23`); evidence-id shorthand → criterion 14 (`corpus/lessons/2026-10-13-round-4.md:12-16`, `corpus/QUALITY.md:24`); blame-the-tool → weak-signal 6 (`corpus/QUALITY.md:35`). |

Trade-rule check: no round recorded `expansion: improved` alongside
`quality: harmed`; the r4 verdicts are expansion improved, quality improved,
discernment verified-by-audit with 10 errata applied
(`.ufo/reports/round-4/kaidoku.md:13-21`, cross-checked against MANIFEST in
`.ufo/waves/kaidoku-r5/04-audit-consistency.md:146-151`).

## Secondary readings — the six axes

| Axis | CURRENT verdict | Last change | Evidence |
|---|---|---|---|
| depth | improved | r4 | SKILL.md grown to full decision tables and error patterns (`LOG.md:43-44`), expanded to the whole held surface including the unlock wave (`LOG.md:81-82`); every decision-table row verified as backed by a knowledge entry (`.ufo/waves/kaidoku-r5/04-audit-consistency.md:132-137`); numeric detail kept honest by errata (e.g. `.jsc` 531,851 B / 115 blocks vs claimed, `.ufo/waves/kaidoku-r5/01-audit-A.md:189-193`). |
| coverage | improved | r4 | Frontier→Core promotions every round: r2 (`LOG.md:18-20`), r3 (`LOG.md:37-41`), r4 additions table (`PROVINCE.md:128-140`); 18-section coverage map (`corpus/README.md:13-32`); host asar census exact 9/9 (`.ufo/waves/kaidoku-r5/04-audit-consistency.md:66-79`). Map lag (44/56) is found debt, in repair — `## Carried debt`. |
| operability | improved | r5 | Every knowledge entry carries a reproducible `verify:` command (example `corpus/knowledge/2026-10-13-r4u-05-wakaru-oom.md:55`); r5 audits re-executed recipes, not just read them — 8/8 compare outputs byte-identical incl. a 63 MB request (`.ufo/waves/kaidoku-r5/02-audit-B.md:110-113`), the full 20-minute REA run re-run with headline numbers reproduced (`.ufo/waves/kaidoku-r5/01-audit-A.md:131-134`). Defective recipes were caught and patched: 2 in r2 (`LOG.md:17-18`), `grep -c`→`grep -o|wc -l` (`corpus/QUALITY.md:23`), file-07 flag-ordering caveat (`.ufo/waves/kaidoku-r5/01-audit-A.md:197-206`). |
| freshness | improved | r5 | Each round re-verifies the previous one against live surfaces (`AXES.md:14` bar; r1 `LOG.md:16-17`, r2 `LOG.md:34-35`, r3 `LOG.md:48-50`, r5 three audit lanes); sha256 pins checked first, all matched (`.ufo/waves/kaidoku-r5/01-audit-A.md:12-14`). Drift that existed was found by the r5 consistency-audit lane — a mechanism this lane did not have in r1 — and is flagged for repair, not left silent (`.ufo/waves/kaidoku-r5/04-audit-consistency.md:208-212`; items in `## Carried debt`). |
| calibration | improved | r5 | Errata culture: 1+2 r2 (`LOG.md:17-18`), 4 r3 (`LOG.md:34-36`), 10 r4 (`LOG.md:49-56`), appended in place, never rewritten (`corpus/QUALITY.md:4-5`). Unprovable items named as UNVERIFIABLE with reasons, none load-bearing (`.ufo/waves/kaidoku-r5/02-audit-B.md:115-119`); intra-round count drift reconciled rather than ignored (`LOG.md:29-31`). |
| adjacency | improved | r4 | Contested/foreign scope reported, not absorbed: the jq-shadow anomaly was traced outside the lane to a kimi-code swarm agent and reported (`corpus/README.md:28`, `LOG.md:40-41`); the evidence-id claim was corroborated by an independent revenger-lane verifier (`LOG.md:56-57`, `.ufo/reports/round-4/kaidoku.md:19-21`); installer work stays in Adjacent as operator-owned (`PROVINCE.md:117-122`) — the r4 unlock wave ran only after operator authorization (`LOG.md:69-70`). Thinnest of the six readings; graded on the two cross-lane events above. |

## How measured

- **Admission bar:** `corpus/QUALITY.md:9-35` — 14 admission criteria plus 6
  weak-signal rows, each criterion citing the lesson that produced it, rows
  superseded by newer rows that name them (`corpus/QUALITY.md:4-5`).
- **Verify:-line discipline:** every knowledge entry opens with `source:`,
  `verified-at:` and carries a reproducible command per claim
  (`LEARNING.md:59-60`; worked example
  `corpus/knowledge/2026-10-13-r4u-05-wakaru-oom.md:55`); occurrence counts on
  minified files must use `grep -o … | wc -l` so the recorded verify itself
  reproduces (criterion 13, `corpus/QUALITY.md:23`).
- **Non-author check:** each round's audit re-runs prior-round verify commands
  and reviews gate decisions (`LEARNING.md:37-43`; r1: ~100 re-runs,
  `LOG.md:16-17`; r5: three adversarial audit lanes plus one consistency lane,
  fleet `.ufo/waves/kaidoku-r5/01`–`04`).
- **Verdict form:** per-trend verdicts from the protocol vocabulary, never
  scalar (`LEARNING.md:25-26`); expansion-with-quality-trade reported as a
  trade and never admitted (`LEARNING.md:34-35`).

## Move log

| Round | Move (one line) | Evidence |
|---|---|---|
| 1 | 16-lane curation: 14 knowledge entries admitted, 4 rejects retained in-file as calibration; QUALITY 9+5; PROVINCE/SKILL filled; first e2e (`rea analyze/search/decompile` on `/usr/bin/jq`, 167 procedures) | `LOG.md:4-13` |
| 2 | Audit r1 (~100 verify re-runs, all admits/rejects upheld; 1 factual erratum, 2 verify-command defects) + expansion: PE e2e proven, compare machinery, crash-inspect mechanism (32 MiB cap), jq-shadow verdict benign | `LOG.md:15-23` |
| 2e | r2-audit-prescribed LOG errata landed: `evidence_id` overclaim, frontier grouping, unrecorded SHONEN checkbox commit; 175/176 corpus-count conflict reconciled | `LOG.md:25-31` |
| 3 | Audit r2 (all upheld; 4 errata) + 12 new entries — runtime-obs CDP, EVM selectors, PE ARM64, synth-carrier macOS ops, `.node` taxonomy, APK inventory, MCP retained-evidence session, verb families; SKILL.md complete, all SHONEN gates closed | `LOG.md:33-45` |
| 4 | Audit r3 (all upheld; 10 errata) + 16-lane expansion + 6-lane operator-authorized unlock: wakaru OOM root-caused and fixed, firmware/Android/managed/binary-layout/AppImage/adb held; QUALITY criteria 12–14; r5 roadmap from frontier rescan | `LOG.md:46-83` |
| 4f | Final two r4 lanes landed (signal-asar directory-route, real-version-pair); Go symbol-recovery hazard recorded; r5 audit-A ran early — three r4 files HOLD, errata appended | `LOG.md:85-105` |
| 5 | In flight, not yet in LOG: three adversarial audits re-verified 13 r4-era files (all HOLD; two cosmetic numeric errata), consistency audit found 4 DRIFT areas, RISC-V lane proved `target_unavailable` bypassable (2-byte `e_machine` patch + `REA_GHIDRA_LANGUAGE_ID`, 94 procedures) — integration pending | `.ufo/waves/kaidoku-r5/01-audit-A.md:306`, `02-audit-B.md:110`, `03-audit-C.md:12-15`, `04-audit-consistency.md:195-206`, `05-riscv-deep.md:1-3` |

| 6 | expansion / quality / discernment (all improved) | r5 in-flight, record repaired (round 5) | r5-01-riscv-bypass + r5-02-call-targets-jq land with audit-bit-exact evidence (independent re-runs reproduced every evidence id); 4 stale wall claims repaired; 4 append-only errata; coverage 56→58 | `.ufo/waves/kaidoku-r6` lanes R1/R2/R3; audit verdicts VERIFIED ×2; LOG.md round-6 |
| 7 | expansion / quality / discernment / calibration (all improved) | 4 Queue-A ops queued unexercised | r7-01 + r7-02 land 4 exercised ops on libjq (api/data-type/instruction/load-image), audit-bit-exact; evidence ids proven content-addressed across lanes; PIE +0x100000 rule extended to shared objects; second refusal family documented | `.ufo/waves` r7 lanes Q1/Q2/Q3; audit VERIFIED ×2; LOG.md round-7 |
| 8 | expansion / quality / discernment / calibration (all improved) | Queue A rows 6-9 unexercised; row 7 a latent census defect | r8-01 + r8-02 discharge rows 6, 8, 9 and close row 7 byte-exact; non-persistence of annotations proven by re-derivation; partial-graph status semantics documented; audit VERIFIED ×2 with one erratum | `.ufo/waves` r8 lanes; resumed audit (honest no-verdict-at-cap recorded); LOG.md round-8 |
| 9 | expansion / quality / discernment / calibration (all improved) | Queue A rows 10/11/13/14 unexercised; audit-cap uncalibrated (r8 cap expired) | r9-01 + r9-02 discharge 4 rows with audit-bit-exact evidence; bundle input shape + coverage-gate semantics + caller-attested authentication boundary documented; audit-cap calibration measured (40 min suffices; re-stat after first-sighting) | r9 lanes Q1/Q2/Q3; audit VERIFIED ×2 (3-run content-address proof); LOG.md round-9 |
| 10 | expansion / quality / discernment / calibration (all improved) | Queue A rows 15/16/20/21 unexercised; 4 latent census defects (row-7 class); netlog provisioning hint unverified | r10-01 + r10-02 discharge 4 rows, close 4 census defects, refute the netlog hint (har-schema gate), document the third authority grade; audit VERIFIED ×2 no defects | r10 lanes Q1/Q2/Q3; audit (post-sighting protocol held); LOG.md round-10 |
| 11 | expansion / coverage / quality / discernment / calibration (all improved) | Queue A residue (lines 186/188/189) unexercised; Queue B unclassified | Queue A FULLY DRAINED: r11-01 (export chain + capture-process, 4th authority grade), r11-02 (first Apple-graph projection on Linux, feed + header laws, Queue-B recon seeding r12: 5 ready-now); audit VERIFIED ×2, 5 nits errata'd | r11 lanes Q1/Q2/Q3; audit; LOG.md round-11 |
| 12 | expansion / coverage / quality / discernment / calibration (all improved) | Queue-B ready-now rows L195-L203 status mixed (held vs open unclear); phantom evidence id in PROVINCE/LOG | L195 = 6th row-7-class defect (setuptools<81 law); 3 tails discharged live (first Android graph projection, apktool-client first success); L203 = first real JS application-version diff; full Queue-B ledger (open set named); audit VERIFIED ×2, 0 false closes; phantom id ev_4898906e corrected to ev_5cb1856a | r12 lanes Q1/Q2/Q3; audit (adversarial close-check); LOG.md round-12 |
| 13 | depth / quality / calibration (improved); expansion unchanged (deliberate) | queue-drain craft lived only in 14 corpus entries | SKILL.md `## Queue-drain craft` lands: 9 rules, all evidence-cited, verify-lane VERIFIED (0 overclaims, 4 nits: 3 fixed, 1 accepted) | SKILL.md:77-191; verify lane report; LOG.md round-13 |
| 14 | expansion / quality / calibration (improved) — FINAL goal round | Queue-B residual 6 items 'blocked'; coverage map 56/70; one phantom id | 3 out of 6 'blocked' items discharged live (L203 directional law, L204 ilspycmd end-to-end, line 176 via export chain); residue purely device/operator-gated, blockers live-re-verified; sweep: 70/70 coverage, checks 1/2/5/8 PASS, phantom anchored, promotion-eligibility recorded; audit VERIFIED x2 | r14 lanes Q1/Q2/Q3; audit; LOG.md round-14 |
## Planned / retired

- **planned** (next axis-move): integrate round 5 — land the r5 LOG entry and
  the pending audit errata, admit the RISC-V bypass entry it proposes
  (`.ufo/waves/kaidoku-r5/05-riscv-deep.md:94-96`), and repair the drift the
  consistency audit prioritized
  (`.ufo/waves/kaidoku-r5/04-audit-consistency.md:208-212`).
- **retired:** none — no axis has been retired or split; no saturation is
  recorded anywhere in `LOG.md:3-105`.

## Carried debt

Survey findings at round-5 close. The named repairs are being executed by
sibling lanes in the current wave — treat each as **in flight**, not open.

- **Mid-flight round 5:** the wave artifacts exist (fleet
  `.ufo/waves/kaidoku-r5/01`–`05`) but there is no round-5 LOG entry (`LOG.md`
  ends at the r4 follow-up, `LOG.md:105`), no round-5 knowledge file in
  `corpus/knowledge/`, and no `kaidoku.md` yet in fleet
  `.ufo/reports/round-5/` (only `aggregator.md` and sibling reports present).
- **Uncommitted errata:** the working tree carries `## Errata (round 5 audit)`
  blocks on three files at HEAD `d6c7c40`, uncommitted per `git status`
  (2026-10-13): `corpus/knowledge/2026-10-13-r4-11-managed-unlock.md:166`,
  `corpus/knowledge/2026-10-13-r4u-02-jadx-decode.md:234` (locales 88≠92,
  `.ufo/waves/kaidoku-r5/03-audit-C.md:53`),
  `corpus/knowledge/2026-10-13-r4u-04-dnfile-il.md:177` (census 15,992/31,
  `.ufo/waves/kaidoku-r5/03-audit-C.md:89`). The earlier audit-A errata
  (`r4-06:325`, `r4-07:212`, `r4-08:285`) are already committed.
- **Stale PROVINCE lines:** six Frontier bullets still describe pre-r4
  "not yet held" state that the same file's Round-4 Core table holds
  (`PROVINCE.md:70-97` vs `PROVINCE.md:128-140`); the "signal … lane in
  flight" line is stale — that lane landed
  (`PROVINCE.md:159-160` vs `corpus/knowledge/2026-10-13-r4-05-signal-asar.md`);
  `REA_APKTOOL_JAR` is documented at `PROVINCE.md:20` and `PROVINCE.md:134`
  but never exported — the working key is `REA_APKTOOL_COMMAND`
  (`.ufo/waves/kaidoku-r5/04-audit-consistency.md:183-193`).
- **Coverage-map lag:** the map cites 44 of 56 knowledge files; the 12
  unmapped are all r4-era (`.ufo/waves/kaidoku-r5/04-audit-consistency.md:57-64`).
- **Smaller, flagged not fixed:** stale `zstd -d` step in the crash recipe
  (`SKILL.md:48`, per `.ufo/waves/kaidoku-r5/04-audit-consistency.md:134-136`);
  `LOG.md:104` says "five" errata where four are listed and exist
  (`.ufo/waves/kaidoku-r5/04-audit-consistency.md:119-121`); the r1
  "Six ASARs" host count was never erratumed on its own entry
  (`.ufo/waves/kaidoku-r5/04-audit-consistency.md:49-53`); r4-report count
  slips (16 vs 17 entries; "six" operator-gated surfaces listed as seven)
  inherited by MANIFEST (`.ufo/waves/kaidoku-r5/04-audit-consistency.md:152-158`).
