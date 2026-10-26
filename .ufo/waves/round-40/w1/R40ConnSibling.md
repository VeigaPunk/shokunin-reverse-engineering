# R40ConnSibling — sibling-overlap scan (read-only) for round 40 surfaces

Seat: `R40ConnSibling-2` (leaf; no subagents, no background jobs). Lane: kaidoku-shokunin round 40 wave 1 (pre-freeze). Verdict: **DONE** — no sibling lane holds AVM / FRITZ!Box / vendor-firmware extraction ground, SquashFS layout readers, or REA extract-firmware receipts; R40-C1/C2 do not duplicate any sibling's Core ground. The round's missing cross-domain line (R39-CL6) must name (a) the shokuknow merge AVM record — including the producer's prior measurement of the **same** V1 image, (b) revenger's declared firmware surface and its fabrication-limit disclosure (M34), and (c) tsukuroi's open ADJ-06 ownership arbitration (kaidoku/revenger).

Bounds compliance: this report and no other file was written, under `.ufo/waves/round-40/w1/artifacts/R40ConnSibling-2/`. No VCS mutation; no REA/unblob runs (nothing needed for a read-only scan); no tool installs (built-in `read`/`grep`/`glob` only — nothing to record under the tooling rule). Scratch `$S` created per bounds and removed before finishing; no scratch paths are cited as evidence.

## 1. Method (exact commands)

All scans are read-only over `/home/vgpnk/Projects/shokunin/*-shokunin/` (21 lanes incl. kaidoku), plus the read-only shokuknow merge tree `/home/vgpnk/Projects/shokuknow/merge/kaidoku/knowledge/` (round-39 closure §3 read the same tree).

1. `glob` `/home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md` → 21/21 lanes have PROVINCE.md; `…/SKILL.md` → 19 (game-dev-2d, audio have none); `…/corpus/knowledge` → 21/21; `…/tools` → 9 (kaidoku, tsukuroi, kama, souji, mado, mori, chousa, kotodama, tameshi).
2. `grep` (gitignore off, paths = all sibling PROVINCE.md + SKILL.md + corpus/knowledge):
   - `AVM|FRITZ|Fritz|fritzbox` → only kaidoku files + one false positive (kotodama `corpus/knowledge/civilizations/thrace-dacia.md:29` = scholar "Fritz Graf").
   - `squashfs|sqfs|sasquatch` → only kaidoku files.
   - `extract-firmware|rea-agents|unblob|REA` → kaidoku (firmware Core rows), revenger (firmware domain + fixtures), game-dev-3d (REA as supporting tool), tsukuroi (ADJ-06/OUT-009 routing rows).
   - `firmware|embedded system|router image` in PROVINCE/SKILL → tsukuroi (driver/firmware health plane, refuses internals), revenger (firmware in domain list), game-dev-3d (context only), mori (routes firmware to tsukuroi).
   - `rerun|re-run|reproduc|receipt|re-mint|fabricat` in PROVINCE/SKILL → revenger, kake, kagi, chousa, game-dev-3d, kengaku, kaidoku (see §4).
   - `triage|decision table|decision-table|action column|scored action` in all SKILL.md → 15 lanes hold decision-table instruments (see §5).
3. `grep` `squashfs|sqfs|sasquatch|avm|unsquashfs` over all sibling `tools/` → only kaidoku (`tools/round-36/37/38/39`), incl. its `gen-squashfs.py` (LE/BE/AVM-marker writer) and `c1-run.sh` oracle arms.
4. `grep` `extract-firmware|firmware` over all sibling `corpus/evidence/` → only kaidoku (round-36..39 c1 before/after receipts; K1..K6).
5. `grep` `avm|FRITZ|fritz|squashfs|sasquatch` over all sibling `.ufo/reports/` → only kaidoku's own arc3-loop1-round4 report (host artifact inventory mention).
6. `read` of: revenger `PROVINCE.md` + `SKILL.md` (fabrication controls, M33/M34/M35, verifier census), tsukuroi `PROVINCE.md` (ADJ-06 table, OUT-008/009, R20-OUT009 note), six shokuknow merge entries (`avm-image-extraction.md`, `avm-le-image-genuine-marker.md`, `sasquatch-unblob-avm-branch.md`, `avm-firmware-image-unblob.md`; `avm-image-build-blocker.md`/`avm-le-variant-reachability.md` exist and were already rejected as stale by the round-39 closure).

## 2. AVM / FRITZ!Box / vendor-firmware extraction ground — none in siblings

No sibling lane (other than kaidoku itself) has any AVM/FRITZ!Box/vendor-firmware extraction data, claims, receipts, or tools:

- The only AVM-relevant material in the fleet tree outside kaidoku is the **shokuknow merge package** (read-only, outside the lanes): `/home/vgpnk/Projects/shokuknow/merge/kaidoku/knowledge/corpus/knowledge/` holds six AVM entries (`avm-image-extraction.md`, `avm-le-image-genuine-marker.md`, `avm-le-variant-reachability.md`, `avm-firmware-image-unblob.md`, `avm-image-build-blocker.md`, `sasquatch-unblob-avm-branch.md`). These are producer/campaign records, not a sibling lane's Core.
- **tsukuroi-shokunin** owns the driver/firmware *health* plane only (`PROVINCE.md:12,49`) and explicitly refuses internals: "binary RE of drivers (→ kaidoku/revenger — tsukuroi tracks *state and health*, not internals)" (`PROVINCE.md:25-27`); ADJ-06 row routes "shipped-artifact reverse engineering beyond health inventory" to "protocol integrator — kaidoku/revenger ownership unresolved" (`PROVINCE.md:51`); OUT-008/OUT-009 pin kaidoku and revenger as the RE owners (`PROVINCE.md:127-129`); R20-OUT009 states "Kaidoku/Revenger arbitration remains unresolved; ask the protocol integrator before an internals handoff" (`PROVINCE.md:148-152`, `:78-80`).
- **revenger-shokunin** declares firmware inside its RE domain — "reverse engineering of shipped artifacts — native binaries, managed assemblies, Electron/JavaScript packages, Android APKs, archives, **firmware**, browser/Electron runtime evidence — using the REA skill and its toolset, with an evidence-ledger discipline" (`PROVINCE.md:3-7`) — but holds **no** AVM/FRITZ!Box/vendor-image data: its firmware ground is the synthetic byte-truth fixture `corpus/fixtures/firmware-r63/generator.py` + `truth.json` (padding/zlib regions; no SquashFS, no AVM), family-coverage counters (`F_FAMILIES` incl. `firmware`), and saved-ledger verifiers. No `extract-firmware` receipt exists in revenger's corpus/evidence.
- **game-dev-3d-shokunin**: REA is a supporting static-inspection tool for 3D artifact evidence only (`PROVINCE.md:8-12,33-41,77-78`); no firmware ground.
- No other lane mentions firmware extraction at all.

## 3. SquashFS layout readers — only kaidoku

`grep squashfs|sqfs|sasquatch|unsquashfs` over all 21 lanes' PROVINCE/SKILL/corpus/knowledge/tools returns nothing outside kaidoku. kaidoku's tools (round-36/37/38/39) are the only SquashFS readers/writers in the fleet: `gen-squashfs.py` (LE/BE/AVM-marker), `sqfs-list.py` (independent reader; round-39), `c1-run.sh` oracle arms via `/usr/bin/unsquashfs` and `sasquatch-v4be -be`. No sibling has a reader to collide with or to borrow.

## 4. REA extract-firmware receipts and receipt-reproduction gates

- **REA extract-firmware receipts:** only kaidoku's `corpus/evidence/round-36|37|38|39/c1/` (K1..K6, `before.json`/`after.json`/`run.json`). Confirmed by §1.4/1.5. No sibling receipt exists on any vendor image, AVM or otherwise.
- **Receipt-reproduction (rerun) gates in siblings (inventory):**
  - **revenger** (closest analog): ten saved-ledger replay verifiers (`SKILL.md` §1, round-66 `measure.py`, HOLD_REPLAY=10/10), scratch-only fixture regeneration and byte-compare (`SKILL.md:176-182,254`), per-verifier **forged-receipt controls** (`SKILL.md:47-50`, `corpus/lessons/round-65.md` C5 `C5_RECEIPT_EVIDENCE_KILLED_ATTRIBUTED` 2/2), and **M34** (counter-substitution: a shaped JSON `{"evidence_id":"invented","operation":"inspect_firmware_regions",...}` satisfies its F presence predicate — `corpus/lessons/round-63.md:219`, `SKILL.md:591-593`). Revenger's round-64 routed row 4 already named the missing instrument: "a future calibration round that registers a receipt/Evidence-ID binding check" (`corpus/lessons/round-64.md:200`).
  - **kake**: `scripts/receipt_replay.py c1|c2` + `measure_c2.py` gates ("Maintained receipt replay registry — round 24", `SKILL.md:534-541`), `canonical_audit.py --manifest` verdict map.
  - **kagi**: `the-janitor tac-check` offline receipt check, `corpus/claim-ledger.sh verify` re-run, receipts bind bytes only (`SKILL.md:38,46,441-472`).
  - **chousa**: `receipt-binding` census gate (QUALITY 42) over lane receipts (`SKILL.md:125`).
  - **game-dev-3d**: bounded saved receipts (`verdicts.json` row-F), `reports/round-102/reruns/manifest.md`, label/pointer controls (NC1–NC5).
  - **kengaku**: pre-registered replication probes and recompute scripts (`corpus/evidence/round9-replication/`, `round11-power/`).
  - **kaidoku's own** round-38/39 `c1-counter.py` already verify evidence-id recomputation (`tools/round-27/xpin-attribute.mjs`) but — as R39-CL5 discloses — cannot refuse a re-minted fabricated receipt; the round-40 C1 scoring-time **rerun clause is the fix** and goes beyond every sibling instrument above (revenger replays committed state; it does not re-run the producer at scoring time).

## 5. Decision-table instruments with scored actions (siblings)

Fifteen sibling lanes carry decision-table instruments; none covers SquashFS/REA envelopes. Closest shapes:

- **kotodama**: `corpus/knowledge/verification/to-verify-triage-protocol.md` — closed-vocabulary statuses `supported`/`partial`/`unresolved` with a "Never" (anti-action) column and a gate (`tools/gates/handoff-packet-check.py`) enforcing them. This is the closest analog to C2's closed-vocabulary `(label, action)` columns (different domain: claim verification).
- **tabi**: `scripts/check-decision-table.mjs` gate scores table rows (threshold = source's own number; `--selftest` 34 cases) plus token-state/browser-evidence/WebMCP decision tables (`SKILL.md:1093,1738,1864,2049,2563-2576`).
- **game-dev-3d**: Unreal claim-label decision table with a fixed label vocabulary and per-label evidence requirements (`SKILL.md:22-51`), backed by reruns and saved receipts.
- **kasegi**: finding-triage decision table + `triage-thresholds.md` (`SKILL.md:134-191,1024`); **mori**: journal classification rows with verdict vocabulary, never actions (`SKILL.md:32-36,374-381`); **kumitate**: dispatch-shape table; **tsukuroi**: health-verdict table + executable `tsukuroi-census.sh`; **tameshi**: gate-shape table (hermetic/live/audit-lane); **lore**: sourced-inspiration decision table + support gates; **kake**: canonical-audit verdict map; **kagi**: vault-ops decision table; **revenger**: claims-label decision tables + verifier census.

R40-C2's contribution is unique among these: a *scored* action column (not just a verdict), a domain guard on `operation`/`provider` (which none of the siblings' tables has; the closest is tabi/game-dev-3d's out-of-scope refusal patterns), and unique per-row labels.

## 6. Duplication verdict

- **R40-C1 (AVM-layout BE SquashFS → Core): does NOT duplicate any sibling's Core ground.** Zero sibling AVM/vendor-firmware/SquashFS carrier data exists (§2/§3/§4). Adjacencies to report, not absorb: (a) revenger's declared firmware surface with the open kaidoku/revenger arbitration; (b) tsukuroi's ADJ-06 routing; (c) the shokuknow merge AVM record — which is evidence *for* the claim, not competing ground (see §7).
- **R40-C2 (triage table v2): does NOT duplicate any sibling's Core ground.** It shares an instrument *shape* with kotodama/tabi/game-dev-3d/mori/kasegi/tsukuroi etc. (§5) but on a domain (SquashFS REA envelopes) no sibling owns. The domain-guard and scored-action-column extensions have no sibling precedent.
- Nothing was absorbed: this scan is report-only per the seat contract.

## 7. Cross-domain evidence the round MUST name (fixes R39-CL6)

The round-39 closure flagged the missing "cross-domain evidence encountered" line (PROTOCOL §Round-robin minimum content). Round 40's report should name at least:

1. **shokuknow merge AVM record** (producer/campaign, not a lane): six entries under `/home/vgpnk/Projects/shokuknow/merge/kaidoku/knowledge/corpus/knowledge/`.
   - `avm-firmware-image-unblob.md` (sources S216–S223, measured 2026-10-24): **the same V1 image** `FRITZ.Box_6490_Cable-07.57.image` (download.avm.de, tar, members `./var/remote/var/tmp/filesystem.image` = AVM_BE **5 443 592 B** and `./var/remote/var/tmp/x86/filesystem.image` = AVM_LE 28 200 968 B), marker `mkfs_time == bytes_used` measured on both (5 442 392 == 5 442 392 BE), unblob 26.6.4 handler selection without `-be` for BE (`squashfs_v4_be` → `sasquatch-v4be -no-exit-code -f -d`), 2 942 BE files extracted. The assignment's V1 BE member size (5 443 592 B) matches this producer record exactly — independent confirmation of the carrier provenance chain before this round's own carve.
   - `avm-image-extraction.md` (S200/S201): a **real** AVM-BE image (Freetz `squashfs4-host-be` recipe, squashfs-tools 4.3 + 23 patches, `-DTARGET_FORMAT=AVM_BE`) builds and extracts; synthetic 4 096 B image; `sqsh` magic, XZ, `mkfs_time` 365 == `bytes_used` 365.
   - `avm-le-image-genuine-marker.md` (S212–S214): AVM_LE marker genuine via a *clean* rebuild; the round-12 "NOT AVM" measurement was a stale-build artifact (changed `-D` not tracked by make) — the stale-binary lesson.
   - `sasquatch-unblob-avm-branch.md` (S189–S192): upstream rule `-be` appended only when `bytes_used != mkfs_time`; branch exercised with a doctored-marker probe; upstream carries no AVM fixture; failure mode is loud ("different endianess" + FATAL, exit 1).
   - `avm-image-build-blocker.md` ("a real AVM image is one release away") and `avm-le-variant-reachability.md`: **rejected as stale** by the round-39 closure (§3, both overturned by `avm-image-extraction.md` / `avm-le-image-genuine-marker.md`) — cite status, never absorb.
2. **tsukuroi ADJ-06 / OUT-008 / OUT-009 / R20-OUT009** (`tsukuroi-shokunin/PROVINCE.md:51,127-129,148-152`): the driver/firmware-internals ownership ruling is **still unresolved** between kaidoku and revenger. R40-C1's vendor-firmware member extraction is kaidoku-owned work; the round should state it does not absorb tsukuroi's health plane and that the arbitration remains open.
3. **revenger's declaration + fabrication disclosure**: `revenger-shokunin/PROVINCE.md:3-7` (firmware in RE domain) and `SKILL.md:591-593` + `corpus/lessons/round-63.md:219` (M34: a fabricated `evidence_id`+`operation` JSON satisfies its F predicate) and `corpus/lessons/round-64.md:200` (evidence-ID binding check deferred to "a future calibration round" — R40-C1's rerun clause is precisely that check). Kotoba independently records the split: "kaidoku's only open split is with revenger" (`kotoba-shokunin/PROVINCE.md:61`).
4. **Adjacent instrument shapes** (one line): kotodama/tabi/game-dev-3d decision-table gates and revenger/kake/kagi receipt-replay gates (§4/§5) — report as adjacency, not absorbed.

## 8. Second-order notes for the L1 (from scan)

- The shokuknow producer's V1 measurement (S216–S223) is a *pre-freeze production record*, not a frozen carrier run; using it as provenance-chain confirmation is fine, but the round's own freeze/carriers must stand on its own carve (the producer's full-image pg run is not this round's REA receipt).
- The producer measured superblocks and handler choice but **not** the little-endian 2-byte metadata block-length headers the draft's P40-C1 predicates on; no sibling data contradicts the draft — it is simply unmeasured elsewhere.
- No sibling gate or counter would be invalidated by C1/C2 landing; the open arbitration (tsukuroi ADJ-06) is the only ownership item the report should explicitly not resolve.

## 9. Evidence backstop

Scans and reads above are reproducible with the exact commands in §1; all cited sibling paths were read at their current working-tree bytes on 2026-10-26. No REA/unblob/git-mutating commands were run; no tools installed; scratch `$S` removed at finish.
