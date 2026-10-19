# records-outline — arc3-loop1-round1 parent-records package (seat CN-2, cross connector)

Assembled 2026-10-19 by seat CN-2. Status: **v3 — SC-3 (C1) and SC-7 (C3) records
drafts landed and folded; SC-5 (C2) still pending (slot marked ⟨C2⟩); every filled value
below is from a landed in-wave artifact, cited inline.** Method: read the frozen claims
(`claims-frozen.md`), the round's landed artifacts, and the arc2 records conventions
(SCORECARD round sections, LOG entries, `.ufo/reports/*/kaidoku.md`), then reduce the
three chains' material to one package with an explicit consistency contract.

Sources read (all under this wave dir unless noted): `claims-frozen.md`;
`claims/c1/EX-11/{head-sha,command-A-before}.txt`; `claims/c1/EX-02/*` (install patch +
smoke); `claims/c1/EX-05/*` + `claims/c1/EX-06/evidence/*` + `claims/c1/RV-2/*`
(real-bytecode probe legs); `claims/c1/EX-13/_scratch/*` + `claims/c1/RV-4/*` (map
token + frozen verification); `claims/c1/records-drafts/*` (SC-3);
`claims/c2/EX-25/logs/*` (before battery); `claims/c2/SC-4/changeset.md` (+ scratch);
`claims/c3/EX-26/*`, `claims/c3/SC-6/*`, `claims/c3/SC-7/*`, `claims/c3/RV-11/*`,
`claims/c3/EX-30/*`; `claims/cross/receipts/*`;
`.ufo/gates/citation-drift/{expected.json,pointer-table.json}`;
`.ufo/gates/c1-census-v10.py`; `SCORECARD.md`, `LOG.md`, `SHONEN.md`, `corpus/README.md`,
`corpus/QUALITY.md`; seat reports SC-2/SC-3/SC-6/RV-2/RV-4/EX-15/CU-1/EX-26/EX-30.

---

## 1. Package inventory — what the parent lands, where

| # | File | Action | Source material |
|---|---|---|---|
| R1 | `LOG.md` | append one `### arc3-loop1-round1 …` entry at EOF (after `:1394`) | §3 skeleton |
| R2 | `SCORECARD.md` | append one `## arc3-loop1-round1 …` section at EOF (after `:1336`) | §4 skeleton |
| R3 | `.ufo/reports/arc3-loop1-round1/kaidoku.md` | new file | §5 skeleton |
| R4 | `.ufo/waves/arc3-loop1-round1/receipts/` | new dir: `MANIFEST.txt`, `config-post-pair.txt`, `roster-reconciliation.txt`, `solc-install.txt` (EX-02 patch), key envelopes/sha logs; custody chain (pre-pair `b8ed1936…`, snapshots, writer-candidates, sidecars) and containment report refs | EX-02 `proposed-receipts-solc-install.patch.md`; CU-1; EX-15 `containment.md`; VZ-4 |
| R5 | `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md` | new entry, acceptance per `corpus/QUALITY.md`; stem must match the map token exactly. **No seat may write `corpus/` — and no landed seat has drafted the entry patch yet (RV-4 §3 checked 10:08Z: file absent). The parent authors it from the sealed evidence: RV-2 envelopes + EX-02 install receipt + `PROVINCE.md:91-93` baseline.** | C1 work + RV-2/EX-06 evidence |
| R6 | `corpus/README.md` | apply EX-13's `map-token.patch` (sha256 `ddfe0116…`, byte copy `claims/c1/RV-4/map-token.frozen.patch`): in-place EVM row `:38` edit, 190→190 lines, tokens 81→82, prior 81 byte-identical, applied sha256 `b74b8d34…` (RV-4 VERDICT: PASS). No lessons-index row in the frozen claim. Row-prose refresh = parent judgment (RV-4 §4: prose still says "synthetic dispatcher"; precedent rows refresh prose; any refresh must stay line-neutral and re-run RV-4's harness). | EX-13 patch + RV-4 verification |
| R7 | `.ufo/gates/citation-drift/*` | EX-16's real-target writes (probe + expected.json; table must stay byte-stable) | SC-4 changeset §1 (A/B/C) |
| R8 | `SKILL.md:371` | parent applies EX-20's registry-row patch text (line-neutral, 371→371; row `6413e8dc…`→`08be1ec2…`) | EX-20 patch + SC-4 §3 verification |
| R9 | `.ufo/gates/c1-census-v10.py` | EX-28's real-target edit (disposition in instrument header; scope re-key only if a row is undeclared/stale — measured: none) | C3 work + EX-26/SC-6/RV-11 captures |
| R10 | `.ufo/waves/arc3-loop1-round1/` (seats/ + claims/) | wave-artifacts commit content | all seats |

Records package = R1+R2+R3 (+R4 receipts commit). R5–R9 are **work**; they land before
the records commit and are re-measured there.

## 2. Commit sequence and gates (arc2-loop1-round8/10 precedent)

1. **Work commit(s)** — C1 landing (R5+R6+receipts), C2 landing (R7+R8), C3 landing (R9).
   One combined commit is the arc2-r8 precedent; per-chain commits are acceptable if each
   is self-consistent. Non-negotiable couplings in §6.
2. **Gate re-runs post-work-commit** (the probe grades git objects at HEAD — gate runs
   belong post-commit): command A (82/82, 13/13), probe `--selftest` (13/13, exit 0) +
   normal run (findings=0), census v10 (PASS 0/0/0/0). If a probe finding fires from a
   line shift, the pin fix rides an immediate follow-up commit (r10 `02c45d5` precedent)
   — record it; do not squash silently.
3. **Wave-artifacts commit** — `.ufo/waves/arc3-loop1-round1/` (seat reports + claims
   artifacts + receipts).
4. **Records commit** — R1+R2+R3. **Re-run the full gate set at this commit and quote it
   verbatim in R2/R3**: command A **82/82, 13/13, 10.0/10.0, missing [], dangling []**;
   probe selftest 13/13 + findings=0; census PASS 0/0/0/0; custody post-pair 5/5.

## 3. LOG.md entry skeleton (append at EOF) — v3, C1 folded in

Pasteable merged entry (C1 text near-final from SC-3's draft; C2/C3 slots pending
SC-5/SC-7; parent-only values as `[[FILL]]`):

```markdown
### arc3-loop1-round1 — coverage (EVM real-bytecode) + operability (probe guard) + freshness (census disposition)

- Motivating evidence: `PROVINCE.md:91-93` Frontier "EVM bytecode (extended)" —
  selectors held on a synthetic 81-byte dispatcher only (r3-07,
  `corpus/knowledge/2026-10-13-r3-evm-interface.md:47-76`); "real
  solc/vyper-compiled bytecode untested". C2: the citation-drift probe's frozen-run
  guard (R6 debt; `SCORECARD.md` arc2-loop1-round4/r5). C3: the census scope-table
  drift (E22; `SCORECARD.md` arc2-loop1-round3). Round declaration:
  `.ufo/waves/arc3-loop1-round1/claims-frozen.md` (64-seat roster frozen PRE-DISPATCH,
  per the r9 wire-it amendment).
- Dispatch: 64 seats (items array == frozen roster, counted at dispatch),
  `opencode-go/deepseek-v4.1-flash` (opencode-go key 1 of 7 — round robin starts here).
  Delivered [[FILL: n/64]].
- C1 coverage — real solc-compiled bytecode, first held: npm `solc` 0.8.37 installed
  into the wave-isolated prefix (`.ufo/waves/arc3-loop1-round1/tools/solc-prefix/`;
  receipt `receipts/solc-install.txt` per EX-02's patch — tarball sha256
  `0e1a1ab6d12c37f5503271b2c4679cd433459c884851920d148d6fb154575a51`, 6,476,046 B,
  8 packages, `solcjs --version` exit 0; custody 5/5 no drift across the install
  window); two real contracts compiled on-host with that solc — KdxToken (EX-06
  source; runtime sha256 `9c40940e…`, K=6) and Rv2Token (RV-2 source; runtime 1,943 B
  sha256 `c1081a56…`, K=5; standard-JSON in/out receipts under `claims/c1/RV-2/`);
  planted counts recorded pre-probe; `rea inspect-evm-interface <file> <raw|hex>`
  recovered K/K on every canonical leg, zero false positives, `dispatch:"abi"` for
  all: KdxToken raw `ev_4dd5ea20…` / hex `ev_2a79dd25…` (EX-05 primary @6.7.0; EX-06
  `ev_56d89cb4…` hex / `ev_9259f412…` raw byte-identical re-runs; RV-2 re-ran both
  byte-exactly), Rv2Token hex@6.4.0 `ev_45849c8b…` (reproduced ×3 byte-identical) /
  raw@6.4.0 `ev_3aacd424…` / hex@6.7.0 `ev_19d7d3cb…`; KdxToken raw determinism twin
  reproduces `ev_4dd5ea20…` exactly, renamed-path twin differs (`ev_b2937090…` —
  path-sensitivity recorded, not part of the claim). [[FILL: cited leg set — SC-3's
  draft cites the Rv2Token legs only; the parent should cite the full set or state
  the canonical subset; R1/R2/R3 must match whichever set is cited.]] First
  hex@6.4.0 attempt died on host /tmp EDQUOT (`execution_failure`, "Unknown system
  error -122") — host-state, not a bytecode refusal; cleaned and retried in-round.
  Creation-code legs (`Rv2Token.creation.hex`, KdxToken creation raw `ev_1dbb4a08…`,
  EX-02 smoke bin) recovered `functions: []` — creation-code classification stays
  open, not claimed; hex-encoding-on-binary is a typed refusal (`invalid_request`,
  UTF-8). Result lands as
  `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md` [[FILL: entry patch path —
  NOT YET DRAFTED by any seat; parent authors from the sealed evidence]] with sealed
  receipts; the coverage map gains the token line-neutrally (`corpus/README.md:38` EVM
  row, EX-13's patch sha256 `ddfe0116…`, applied sha256 `b74b8d34…`, 190→190 lines,
  tokens 81→82, prior 81 byte-identical — RV-4 verified); command A 81 → 82
  [[FILL: measured at the records commit: 82/82, missing [], dangling [], 13/13 rules;
  prior-81 diff = only the new file]]. Token-without-file pre-flighted as dangling
  (EX-13 scratch `295cd30a`) — entry and token must land in the same commit.
- C2 operability — [[FROM C2 CHAIN (SC-5 pending): `expected.json` pins the sha256 of
  `pointer-table.json`; tampered or absent table → declared could-not-evaluate class
  (exit 2), never silent findings; SKILL.md registry row states the guard semantics;
  selftest 11 → 13 cases at exit 0; findings = 0 at HEAD. Coupling: every future table
  edit must re-pin expected.json in the same commit. Evidence:
  `.ufo/gates/citation-drift/…` + receipts [[FILL: paths]]]]
- C3 freshness — use SC-7's literal C3 bullet verbatim
  (`claims/c3/SC-7/log-entry-draft.md` §LITERAL ENTRY TEXT — complete and
  evidence-cited): E22 (`SCORECARD.md:850-852`) dispositioned by measurement;
  census v10 at HEAD `e845c2b` → PASS 0/0/0/0 (exit 0; capture sha `3b677b8e…`;
  four independent captures one digest — EX-26/SC-6/EX-30/RV-11); no scope row
  undeclared or stale → the re-key branch NOT taken, no row retired; row-level
  history (rows added `265e1aa`, +1 shift `6bc4c29`) + disposition stated in the
  instrument's own header; the records append pre-verified locus-free in the
  census unit (records-tree simulation PASS 0/0/0/0; planted tail locus → FAIL
  undeclared=1 — detector live); census re-run at the records commit
  [[FILL: verbatim quote]]. Header stanza = SC-6 P1 + SC-7 addendum, assembled
  at `claims/c3/SC-7/census-header-draft.md` §2 (also EX-26
  `proposed-census-header-disposition.patch.md`); applied sha256 [[FILL]]. No
  corpus/knowledge edit in this claim (command A's movement is C1's).
- Custody: pre-pair `.ufo/waves/arc3-loop1-round1/claims/cross/receipts/
  config-pre-pair.txt` (CU-1, 2026-10-19T09:57:18Z, 5/5; independently corroborated —
  EX-01 recompute 09:59:53Z (3 implementations agree 5/5), EX-15 T0/T1, EX-14 manifest
  live re-check 10:01:21Z 5/5, EX-10 kimi-stanza byte-identical); post-pair
  [[FILL: path/time]]; zero within-wave drift 5/5 [[FILL]]. Cross-wave diff (arc2-r1
  pre-pair vs T0): the Kimi `config.toml` rewrite (3546e033…→8cbacd48…) predates the
  wave (mtime 2026-10-18 23:20:43 -03) — operator-side class, recorded not attributed;
  the frozen prediction "no config.toml drift" holds inside the wave window.
- Process notes: recipe A's documented invocation form (`REV=HEAD python3 - "$REV"`)
  expands `$REV` empty before the inline assignment — EX-11 pinned the working form
  (`REV=HEAD; python3 - "$REV"`) in `claims/c1/EX-11/command-A-before.txt`; the host
  /tmp EDQUOT episode was cleaned and retried in-round (EX-02 residue sweep); the
  EX-02 smoke leg preceded the canonical probe (smoke bin creation code → `functions:
  []`, selector presence checked from ABI instead); `.ufo/gates/__pycache__/` untracked
  residue created in-window by census runs — kept out of commits.
- Carried debt (named): creation-code `kind` classification (creation blobs yield
  `functions: []`; EVMole needs runtime code); selectors stay bare hashes — no
  signature DB, no name resolution (`PROVINCE.md:93`); vyper leg untested; C2:
  `expected.json` self-digest absent (pin chain terminates there),
  `snapshots.config-toml-landmarks` unreferenced; C3: fixed-bound tail :856+ stays
  undeclared by design [[FILL: any new debt the wave names]].
- Retired: [[FILL: the "EVM bytecode (extended)" frontier bullet moves to Core
  (`PROVINCE.md:91-93` update cited in this entry); or none]].
- Scope: no config edits, no pushes, repo-local; installs limited to npm `solc` + its
  dep tree under the wave prefix.
```

## 4. SCORECARD.md round-section skeleton (append after `:1336`) — v3

Order matters — mirror arc2 round sections exactly; SC-3's draft
(`claims/c1/records-drafts/SCORECARD-section-draft.md`) already follows this order and
carries the pasteable C1 text; SC-5/SC-7 fill the C2/C3 slots.

1. `## arc3-loop1-round1 — coverage + operability + freshness: three claims admitted, 2026-10-19`
   (SC-3's draft title drops "admitted" pending the verdict — [[FILL: final verdict]]).
2. Opening paragraph: arc3 loop 1 round 1 (first round after the operator halt,
   `LOG.md:1385-1393`); wave size/model/roster frozen pre-dispatch; delivery ⟨N⟩/64;
   **Round admitted: ⟨all three claims verify / splits / honest-stop⟩**.
3. Wave bullet: reports `.ufo/waves/arc3-loop1-round1/`; round report
   `.ufo/reports/arc3-loop1-round1/kaidoku.md`; landed at ⟨work⟩ + ⟨artifacts⟩ +
   ⟨records⟩ commits.
4. **C1 coverage (owned)** bullet — SC-3 draft §C1 (paste): install receipt; Rv2Token
   compile (runtime 1,943 B, sha256 `c1081a56…`); K=5 pre-recorded; three legs with
   evidence ids and offsets; hex leg ×3 byte-identical; EDQUOT episode read as
   host-state; creation-code legs `functions: []` (not claimed); entry + line-neutral
   token land together; command A 81→82 [[FILL]]. **Judgment flag (RV-4 §4):** the EVM
   row's state prose is unchanged by the frozen token patch ("held — EVMole selectors
   recovered from synthetic dispatcher; …") while precedent rows refresh prose when
   appending tokens — the frozen claim only requires the token, so the parent decides;
   a prose refresh must keep the edit line-neutral and re-run RV-4's harness.
5. **C2 operability (fleet)** bullet — ⟨C2⟩: guard semantics; exit-2 class; SKILL.md
   row; selftest 11→13; findings=0; re-pin coupling sentence (edit-workflow
   consequence). Evidence + coupling material: SC-4 `changeset.md` §1/§5; RV-6 §4.
6. **C3 freshness (fleet)** bullet — paste SC-7's literal C3 bullet verbatim
   (`claims/c3/SC-7/scorecard-section-draft.md` §LITERAL SECTION TEXT — complete,
   evidence-cited, pin-free by construction): E22 (`SCORECARD.md:850-852`)
   dispositioned by measurement; census v10 at HEAD `e845c2b` → PASS 0/0/0/0
   (capture sha `3b677b8e…`; four captures one digest EX-26/SC-6/EX-30/RV-11); no
   scope row undeclared or stale → the re-key branch not taken, none retired; row
   history (added `265e1aa`, +1 shift `6bc4c29`) + disposition stated in the
   instrument's own header; records append pre-verified locus-free (records-tree
   simulation PASS; planted tail locus FAIL undeclared=1); census at the records
   commit [[FILL: verbatim re-run quote]]; no corpus/knowledge edit. Header stanza
   = SC-6 P1 + SC-7 addendum (`claims/c3/SC-7/census-header-draft.md` §2)
   [[FILL: applied sha256]].
7. Measured-at line: command A ⟨82/82, 13/13, 10.0/10.0⟩; probe 13/13 + findings=0;
   census PASS 0/0/0/0; custody pre/post 5/5 [[FILL: receipt times]]; no `config.toml`
   drift inside the wave window (cross-wave rewrite predates it — operator-side class).
8. Verdict table `| Axis | Before → after | Verdict |` — coverage row per SC-3 draft
   (synthetic 3/3 → real K/K across the cited legs, 81→82); operability row ⟨C2⟩;
   freshness row per SC-7's literal table row (E22 undispositioned → dispositioned by
   measurement; improved); `| depth | 13/13 at the records commit | unchanged |`.
9. Learning trends: expansion (first real-bytecode EVM entry — the synthetic leg is
   superseded); quality; discernment (EDQUOT read as host-state not refusal;
   dangling-token pre-flight; row-insert variant excluded; C3's sentence: the E22 debt
   closed by measurement rather than another re-key, with a live positive control on
   the records-append discipline) ⟨C2 additions⟩.
10. Planned (round 2 per schedule) + carried debt (named — see §3) + retired
    (⟨the EVM-real-bytecode frontier bullet; or none⟩).

## 5. Round-report skeleton — `.ufo/reports/arc3-loop1-round1/kaidoku.md` — v3

```markdown
# kaidoku arc3-loop1-round1 — coverage (EVM real bytecode) / operability (probe guard) /
freshness (census disposition)

Date: 2026-10-19. Wave: 64 seats on `opencode-go/deepseek-v4.1-flash`, roster frozen
pre-dispatch; ⟨N⟩/64 delivered. Work commits: ⟨…⟩. Wave artifacts: ⟨…⟩.

**Round admitted: ⟨…⟩**

## Work performed
1. **C1 — coverage** (owned): the real-bytecode EVM leg — solc 0.8.37 install
   (receipt), two contracts compiled on-host (KdxToken K=6, Rv2Token K=5), K/K
   recovered on every canonical leg (raw+hex; rea 6.4.0/6.7.0), entry + line-neutral
   map token. Pointers: EX-02 (install + smoke), EX-05 (primary KdxToken legs
   `ev_4dd5ea20…`/`ev_2a79dd25…`), EX-06 (KdxToken re-run `ev_56d89cb4…`/
   `ev_9259f412…`), RV-2 (Rv2Token `ev_45849c8b…`/`ev_3aacd424…`/`ev_19d7d3cb…` +
   byte-exact re-runs), EX-07 (reconciliation), EX-13 (map patch), RV-4 (frozen
   verification), EX-11 (command-A before), EX-15/CU-1 (custody/containment),
   SC-3 (records draft).
2. **C2 — operability**: ⟨SC-5 text⟩.
3. **C3 — freshness**: E22 disposition — use SC-7's literal drafts
   (`claims/c3/SC-7/{log-entry,scorecard-section,census-header}-draft.md`);
   four-way census captures (EX-26/SC-6/RV-11/EX-30, one digest `3b677b8e…`);
   records-append simulation (PASS) + planted-locus control (FAIL undeclared=1);
   header stanza [[FILL: applied]]; census re-run at the records commit [[FILL]].

## Landed changes
⟨per-file bullets with commits; R5–R9; receipts R4⟩

## Before → after measurements
⟨C1: command A 81→82 (prior-81 diff = only the new file), K/K legs table;
C2: 11→13, findings 0, exit-2 class; C3: census verbatim before → PASS after;
side-harm check: command A + census + probe at the records commit⟩

## SHONEN — all four boxes retained [~]
⟨four boxes with SHONEN.md:5-6/:7-8/:9-10/:11-12 cites; gate `../PROTOCOL.md:63-72`
(no outside verifier → `[~]`)⟩

## Verdicts
⟨coverage/operability/freshness improved; depth/calibration unchanged;
stagnation/regimen line — arc3 loop 1 starts here⟩
```

## 6. Cross-chain consistency contract (the reconciliation core)

### 6.1 Single-source numbers (must agree across R1/R2/R3)

| Number | Value | Source of truth |
|---|---|---|
| knowledge files / mapped | 81 → 82, 82/82 | command A at records commit |
| rules | 13/13 | command A |
| probe selftest | 11 → 13, 13/13 exit 0 | probe `--selftest` at records commit |
| probe findings | 0 | probe normal run at records commit |
| census | PASS 0/0/0/0 | census v10 at records commit |
| custody | 5/5 pre + 5/5 post | receipts |
| seats | 64 declared == items; ⟨N⟩/64 delivered | roster reconciliation (VZ-4) |

### 6.2 Line-shift couplings (probe pins vs landings)

Pins at HEAD that constrain the landings (`.ufo/gates/citation-drift/pointer-table.json`):
`sc59/60/68/69/72/270/622/698/699` → SCORECARD lines; `readme22-*` → `corpus/README.md:22`;
`readme175-*` → `corpus/README.md:175`; `shonen-skill-range` → `SHONEN.md:6`;
`shonen-province-range` → `SHONEN.md:12`; `skill-registry-row` → SKILL.md anchor
(interactive-r1 row, unaffected by the citation-drift row edit).

- **R6 must be line-neutral**: edit map row `corpus/README.md:38` in place. A NEW map row
  (or a lessons-index row inserted before `:175`) shifts `readme175` → re-point in the
  same commit (r8/r10 precedent) or verify `:175` still matches after the edit.
- **R2/R1 are append-only at EOF** → pins on SCORECARD `≤:699` and `LOG.md:1012` stay
  valid. Do not touch SCORECARD `:19-33` (axes table) or any pinned region.
- **R8 is line-neutral** (371→371 verified by SC-4; row-level patch).
- **R9 must not shift `SKILL.md`/`PROVINCE.md`/`SCORECARD.md`** (census SCOPE covers
  `PROVINCE.md:8-13,15-26,40-44,45-62,64-71,119-131`; `SKILL.md:10-16,18-20`;
  `SCORECARD.md:56-60,273-326,417-466,467-502,503-533,534-560,619-620,636-702,703-768,769-855`).
- Post-work-commit: probe re-run is mandatory; a finding here is a real catch — fix in a
  follow-up commit, record it (never silence).

### 6.3 Digest couplings

- **`expected.json` pins `pointer-table.json`'s sha256** (C2's change): after EX-16 lands,
  ANY table edit (e.g. a pin re-point caused by 6.2) requires re-pinning `expected.json`
  in the same commit, else exit 2. EX-16 must land probe + expected.json + table
  byte-stable (`738b3a56…` stays) — SC-4 changeset §1 C.
- **Row-token reconciliation** (SC-4 §5): EX-20's row text writes `table_tampered` and
  `pointer_table_unreadable`; substitute EX-16's landed finding ids if they differ; the
  "unpinned" clause stands only if EX-16 treats no-pin as CNE; case count 13 only if
  EX-16 lands exactly +2.
- **C1's new knowledge file is additive** (no existing pinned knowledge file edited) —
  pins `mcpreg-errata-anchor-form`, `r416-errata-durable-anchor`, `r7wall-*` stay.
- **Install receipt** (R4): solc 0.8.37, tarball sha256 `0e1a1ab6…`; custody 5/5 identical
  pre/post install (EX-02).

### 6.4 Gate at records commit (C3's claim closes here)

Census + probe + command A all re-run at the records commit; C3's claim language requires
"PASS 0/0/0/0 at the records commit with the disposition stated in the instrument's own
header". **SC-7 pre-verified the drafted records text's census interaction by
simulation** (`/var/tmp/sc7`): records-tree (HEAD census files + the literal SCORECARD
section) → PASS 0/0/0/0 exit 0; same tree + a planted tail pin literal → FAIL
undeclared=1 (the detector is live on the appended region). Records-append discipline
(SC-6 P1 / SC-7): the appended section must carry no `rea-agents@` pin, no bare `6.x.y`
literal, and no `~`//-absolute `path.json|toml|yaml:NNN` pointer inside a REA_GATE block;
if the merged text cannot honor that, the SCOPE bound re-keys in the same commit
(EX-28's instrument; parent applies).

## 7. Merge-slot map (SC drafts → package slots) — v3

| Slot | Needs | From | Status |
|---|---|---|---|
| ⟨C1⟩ claim text + numbers | R1 C1 bullet, R2 §4.4, R3 §Work/Before-after | SC-3 drafts (`claims/c1/records-drafts/`) | **LANDED — fold verbatim; adjust the cited leg set (SC-3 cites Rv2Token only; EX-05/EX-06 KdxToken legs also sealed — see §3); entry-file patch still missing** |
| ⟨C2⟩ claim text + guard semantics sentence + case names | R1 C2 bullet, R2 §4.5, R3 | SC-5 (`claims/c2/SC-5/`) — still empty | PENDING — coupling material landed (SC-4 changeset §1/§5; EX-20 patch; RV-6 harness) |
| ⟨C3⟩ disposition + verbatim census pair + header stanza | R1 C3 bullet, R2 §4.6, R3 | SC-7 literal drafts (`claims/c3/SC-7/{log-entry,scorecard-section,census-header}-draft.md`) + SC-6 P1 + EX-26 patch | **LANDED — paste verbatim; fill `⟨…⟩`/`[[FILL]]` slots** |
| Verdict-table strings + learning-trend sentences | R2 §4.8–9, R3 §Verdicts | CN-2 (this outline) + SC drafts | PARTIAL — C3 row/sentence landed (SC-7) |
| Delivery count + roster reconciliation | R1 dispatch line, R2 opening, R3 header | VZ-4 | PENDING |
| Custody post-pair + in-window drift note | R1 custody line | CU-1 | PENDING (pre-pair landed; 25×60s snapshots; post-pair at close) |

## 8. Named gaps / risks (v3)

- SC-5 (C2 records) still absent — §7 ⟨C2⟩ row PENDING; SC-3 (C1) and SC-7 (C3) landed.
- The C1 knowledge-entry patch (`corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md`)
  is not drafted by any landed seat — the parent authors it from the sealed evidence;
  entry + token land in the same commit (dangling pre-flight measured).
- EX-16 (R7) and EX-28 (R9) real-target writes absent at write time — all C2/C3
  after-values are placeholders until those land; C1's after-value (82/82) is likewise
  pending the parent's landing of R5/R6.
- C1 leg-set choice: SC-3's drafts cite Rv2Token only; EX-05/EX-06 KdxToken legs (K=6)
  are also sealed — pick one cited set and keep R1/R2/R3 consistent.
- SC-4 §6 residual: `expected.json` carries no self-digest (a same-privilege writer can
  delete the pin field and restore silence) — record as a named limit, do not fix.
- SC-4 §6: `snapshots.config-toml-landmarks` is now unreferenced by the table
  (pre-existing; not this round's defect).
- SC-2 manifest cross-check: EX-14's manifest read FAIL (7 problems incl. 1 missing
  `.pyc`); SC-2 proposes a generator exclusion for `__pycache__` — decide for R4.
- Counting discipline: delivery counts come from the roster reconciliation, never from
  the declared 64 (counting lesson `corpus/lessons/2026-10-18-wave-dispatch-counting.md`).

## 9. Wave-environment & containment notes (record, do not absorb)

- **`/tmp` user quota exhausted** (standing hazard already recorded at
  `SCORECARD.md:991` — "/tmp quota hazard = standing (seats relocated, evidence
  intact)"): byte-writes fail `EDQUOT` while 0-byte creates succeed; EX-15 measured
  147 zero-byte files in-window (`claims/c1/EX-15/tmp-quota-casualties.txt`) and proved
  the saturation pre-dates the wave. Records line: recurrence of the standing hazard,
  seats relocated scratch (SC-6/EX-06 used the artifact dir / `/dev/shm`), not a new
  debt class.
- **`.ufo/gates/__pycache__/` untracked residue**: created in-window (06:58:37) by the
  census run (pyc header provenance proven by EX-15); SC-6 removed its own and a new one
  appeared 07:04:16 from another module audit. Must NOT enter the wave-artifacts commit;
  recurring class (also present at r10) — name it in the custody/scope line, keep out of
  commits.
- **Inter-wave `config.toml` drift**: `3546e033…` → `8cbacd48…`, ctime 2026-10-18
  23:20:43 — pre-wave, so C1's prediction "no config.toml drift" is not falsified
  (EX-15 `custody-crosswave-diff.txt`); the C1 claim's drift check is about the wave
  window, which is clean (EX-15 T0==T1, CU-1 snapshots).
- **Census tail-locus coupling** (SC-6 measured, `fixture-tail-locus.txt`): the records
  append (R2) must stay **locus-free in the census's unit scan** — an injected tail
  locus reads UNDECLARED (FAIL, exit 1). If the R2 text cannot avoid a locus, re-key the
  SCOPE bound in the same commit (EX-28's instrument; parent applies). v9 stays red at
  HEAD by construction — v10 is canonical; do not quote v9@HEAD FAIL as the C3 "before"
  without the "by construction" qualifier (SC-6 §1/§2).
