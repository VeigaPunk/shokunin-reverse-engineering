# LOG.md entry — DRAFT (arc3-loop1-round1, C1 chain records)

Status: DRAFT by seat SC-3 (C1 chain, scribe) — **NOT APPLIED**. Parent
integrates after the wave. Every `[[FILL: …]]` must be replaced from the
wave's sealed receipts (or the sentence rewritten to the honest-stop branch)
before landing. The C2/C3 paragraphs are shape-only: fill from those chains'
records (SC-4/SC-5 and SC-6/SC-7 drafts + chain receipts). The pasteable text
is the block below the horizontal rule; the evidence inventory at the bottom
is SC-3's poll notes, not part of the entry. Updated 2026-10-19 ~10:15Z with
poll evidence (KdxToken/Rv2Token/Rv2Many legs EX-05/EX-06/EX-07/EX-08, RV-2
replication + attacks, EX-02 install receipt, EX-12 entry patch, EX-13 map
variants, EX-15 containment, EX-14 manifest).

---

### arc3-loop1-round1 — coverage (EVM real-bytecode) + operability (probe guard) + freshness (census disposition)

- Motivating evidence: `PROVINCE.md:91-93` Frontier "EVM bytecode (extended)" —
  selectors held on a synthetic 81-byte dispatcher only (r3-07,
  `corpus/knowledge/2026-10-13-r3-evm-interface.md:47-76`); "real
  solc/vyper-compiled bytecode untested". C2: the citation-drift probe's
  frozen-run guard (R6 debt; `SCORECARD.md` arc2-loop1-round4/r5). C3: the
  census scope-table drift (E22; `SCORECARD.md` arc2-loop1-round3). Round
  declaration: `.ufo/waves/arc3-loop1-round1/claims-frozen.md` (64-seat roster
  frozen PRE-DISPATCH, per the r9 wire-it amendment).
- Dispatch: 64 seats (items array == frozen roster, counted at dispatch),
  `opencode-go/deepseek-v4.1-flash` (opencode-go key 1 of 7 — round robin
  starts here). Delivered [[FILL: n/64]].
- C1 coverage — real solc-compiled bytecode, first held: npm `solc` 0.8.37
  installed into the wave-isolated prefix
  (`.ufo/waves/arc3-loop1-round1/tools/solc-prefix/`; install receipt
  `receipts/solc-install.txt` per EX-02's patch — tarball sha256
  `0e1a1ab6d12c37f5503271b2c4679cd433459c884851920d148d6fb154575a51`,
  6,476,046 B, 8 packages, `solcjs --version` exit 0; custody 5/5 no drift
  across the install window); three contracts compiled on-host with that
  solc (two seats' independent `KdxToken` compiles byte-identical: runtime
  raw `9c40940e…`, hex carrier `69a15782…`), planted sets recorded
  pre-probe, and `rea inspect-evm-interface <file> <raw|hex>` recovers K/K
  on every leg — zero missing, zero extra, `dispatch:"abi"`, offsets equal
  to EX-07's independent dispatch parse:
  `Rv2Token` 5/5 (hex `ev_45849c8b…` reproduced ×3 byte-identical; raw
  `ev_3aacd424…`; hex@6.7.0 `ev_19d7d3cb…`; EX-05 twins
  `ev_0636c55d…`/`ev_1a60d32c…`/`ev_76a1c1e3…`),
  `KdxToken` 6/6 (ten legs across pins and carriers: EX-05 ×4 — the
  determinism twin `kdx.raw.rerun` re-issued the SAME id `ev_4dd5ea20…`,
  the renamed twin `ev_b2937090…` shows path-insensitivity; EX-06 ×4 on its
  own compiles `ev_ad8fb290…`/`ev_56d89cb4…`/`ev_0a1317b9…`/`ev_9259f412…`
  plus ×2 on EX-05's bytes `ev_cde546a2…`/`ev_bb616f88…`; RV-2 replays ×2
  re-issuing EX-05's ids),
  `Rv2Many` attack carrier 11/11 (`ev_d0d0b054…` — no truncation).
  Input-shape traps fail closed, not silent: typed `invalid_request` on
  hex-on-binary / malformed hex / missing file; honest 0-function envelopes
  on raw non-bytecode; the one `execution_failure` (EDQUOT, "Unknown system
  error -122") is host-state — EX-15 root-caused the saturated per-UID
  tmpfs quota; the retry sealed clean (EX-08's edge matrix incl. empty /
  ELF-magic / noTMPDIR legs corroborates). Creation blobs parse-and-empty
  (`functions: []`, `kind:"unknown"`) — not claimed as selector recovery.
  Result lands as `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md`
  (EX-12's patch `claims/c1/EX-12/knowledge-entry.patch.md`, 31 lines,
  RESULT-class) with the coverage-map token line-neutral
  (`corpus/README.md:38`; EX-13's verified variants — 190 → 190 lines, only
  :38 differs; land entry + token once and consistently: EX-12's entry stem
  matches EX-13's h3 token `2026-10-19-arc3-r1-evm-real-solc`); command A
  81 → 82, prior 81 byte-identical, rules 13/13 — wave-rehearsed at EX-13's
  patched commits (82/82, missing [], dangling []; the entry-absent control
  measures 81/81 + the dangling token) [[FILL: parent re-measure at the
  records commit]].
- C2 operability — [[FROM C2 CHAIN: the citation-drift probe pins the sha256
  of `pointer-table.json` in `expected.json`; a tampered or absent table
  yields the declared could-not-evaluate class (exit 2), never silent
  findings; the SKILL.md registry row states the guard semantics; selftest
  11 → 13 cases (clean-tree, tampered-table, absent-table) at exit 0;
  findings = 0 at HEAD. Evidence: `.ufo/gates/citation-drift/…` + receipts
  [[FILL: paths]]]]
- C3 freshness — [[FROM C3 CHAIN: the E22 scope-table finding is
  dispositioned by measurement at HEAD: census v10 reports 0 stale / 0
  ambiguous / 0 undeclared / 0 unresolved (5 historical) —
  `claims/c3/EX-26/census-at-HEAD.txt`; [[FILL: re-key applied / row retired
  with cause / disposition already-resolved-by-r8-re-key]]; PASS 0/0/0/0 at
  the records commit [[FILL: path]]]]
- Custody: pre-pair `.ufo/waves/arc3-loop1-round1/claims/cross/receipts/
  config-pre-pair.txt` (CU-1, 2026-10-19T09:57:18Z, 5/5; independently
  corroborated — EX-01 recompute 09:59:53Z (3 implementations agree 5/5),
  EX-15 T0/T1 (containment: custody CLEAN, no stray procs, no OOM),
  EX-14 manifest live re-check 10:01:21Z 5/5, EX-10 kimi-stanza stability
  re-check byte-identical); post-pair [[FILL: path/time]]; zero within-wave
  drift 5/5 [[FILL]]. Cross-wave diff (arc2-r1 pre-pair vs T0, EX-15): the
  Kimi `config.toml` rewrite predates the wave (mtime 2026-10-19 02:20:43Z;
  wave start 09:49Z) — operator-side class, recorded not attributed; the
  frozen prediction "no config.toml drift" holds inside the wave window.
- Process notes: measurement recipe A's documented invocation form
  (`REV=HEAD python3 - "$REV"`) expands `$REV` empty before the inline
  assignment — the working form is `REV=HEAD; python3 - "$REV"` (EX-11;
  SC-3 reproduced the quirk); the host /tmp EDQUOT episode was cleaned and
  retried in-round (EX-02 residue sweep; EX-15 root-caused the saturated
  quota; EX-08's noTMPDIR leg reproduced it); EX-15 recorded a stray repo
  write outside authorized paths (removed, recreated — see its containment
  artifact); EX-13 rehearsed all three map variants with V1-V7 checks
  (line-neutrality, apply-clean, probe findings=0 at the patched commit,
  command A with/without the entry).
- Carried debt (named): creation-code `kind` classification (creation blobs
  yield `functions: []`; EVMole needs runtime code); the `inspect_evm_
  interface` `ev_` id domain was not measured — no content-addressed
  identity claim is made (EX-12's entry says so explicitly); selectors stay
  bare hashes — no signature DB, no name resolution (`PROVINCE.md:93`);
  vyper leg untested; [[FILL: any new debt the wave names]].
- Retired: [[FILL: the "EVM bytecode (extended)" frontier bullet moves to
  Core (`PROVINCE.md:91-93` update cited in this entry); or none]].
- Scope: no config edits, no pushes, repo-local.

---

## SC-3 poll notes (not part of the entry)

Evidence inventory, with SC-3's own re-verification where possible
(poll window 2026-10-19 ~10:00–10:15Z):

- HEAD before the round: `e845c2b524ad2e59871e004c51a1386e192a74ab`
  (`claims/c1/EX-11/head-sha.txt`; SC-3 re-ran `git rev-parse HEAD` — match).
- Command A at HEAD (SC-3 re-ran the recipe from `SCORECARD.md:92-124`):
  `{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [],
  "depth_score": 10.0, "knowledge_files": 81, "mapped": 81, "missing": [],
  "rule_blocks": 13}` — matches `claims/c1/EX-11/command-A-before.txt`.
- Canonical probe (SC-3 re-parsed every leg envelope it could): three
  carriers, K=5/6/11 (`claims/c1/RV-2/expected-selectors.txt`;
  `EX-06/evidence/planted-K.json`; `RV-2/attack/expected-many.txt`). Full leg
  tables: `EX-05/evidence-ids.txt` (×4 kdx + rv2 twins + refusals),
  `EX-06/evidence/*.json` (×4 kdx + ×2 on EX-05 bytes + creation/trap legs),
  `RV-2/probe-*.json` + `rv2-verify-ex05-kdx-*.json` + `attack/probe-many
  .json`, `EX-08/probe-*.json` (edge matrix incl. the synthetic-baseline
  recon legs and the noTMPDIR EDQUOT reproduction). EX-07's
  `reconciliation.md` (3-way, eleven source-sets) verdict: 6/6 zero
  missing/zero extra, offsets equal across legs; two seats' independent
  compiles byte-identical.
- Entry + map artifacts: `claims/c1/EX-12/knowledge-entry.patch.md` (entry
  `2026-10-19-arc3-r1-evm-real-solc.md`, 31 lines; applies with `patch -p1`
  or `git apply -p1`, both exit 0; its map hunk is byte-identical to EX-13's
  rehearsal — land once). `claims/c1/EX-13/verification.txt` — three map
  variants (h1/h2 token `2026-10-19-arc3-r1-evm-solc`, h3 token
  `2026-10-19-arc3-r1-evm-real-solc`); all: V1 line-neutral 190 → 190 only
  :38 differs; V4 `git apply --check` exit 0; V5 citation-drift probe
  findings=0 at the patched commits; V6 command A with entry 82/82,
  missing [], dangling [], 13/13; V7 entry-absent control 81/81 + dangling
  token. **Parent must pair one token variant with the entry stem
  consistently (EX-12's entry matches h3).**
- Install: `.ufo/waves/arc3-loop1-round1/tools/solc-prefix/` (isolated
  prefix; `node_modules/solc` version 0.8.37). Full receipt:
  `claims/c1/EX-02/install-receipt.txt`; proposed target
  `receipts/solc-install.txt`
  (`claims/c1/EX-02/proposed-receipts-solc-install.patch.md`).
- Census at HEAD (C3 chain, EX-26): exit 0; STALE 0 / AMBIGUOUS 0 /
  UNDECLARED 0 / UNRESOLVED 0; HISTORICAL 5 (`PROVINCE.md:67`, `:125`,
  `SCORECARD.md:537`, `:620`, `SKILL.md:12`).
- Custody/containment artifacts at poll close: CU-1 pre-pair (09:57:18Z,
  5/5); `claims/c1/EX-01/config-pre-pair.txt` (recompute 09:59:53Z, 5/5,
  3-impl agreement); `claims/c1/EX-15/custody-T0.txt` + `custody-T1.txt` +
  `custody-crosswave-diff.txt` + `containment.md` (custody CLEAN; no stray
  procs; no OOM; /tmp per-UID tmpfs quota saturated — the EDQUOT root
  cause; a stray repo write outside authorized paths recorded);
  `claims/c1/receipts/config-pre-pair.txt`; `claims/c1/receipts/
  MANIFEST.draft.txt` (EX-14, 34 entries, live re-check 10:01:21Z 5/5);
  `claims/c1/EX-10/kimi-pin-check.txt` (stanza-anchored, recapture
  byte-identical). Wave-level post-pair (after battery close) not yet
  landed; EX-02's own install post-pair shows no drift.
- Seats landed at poll close (32 reports incl. SC-3): EX-01/02/05/06/07/
  09/10/11/15, RV-1/2/4, plus cross/c2/c3-chain reports. C2/C3 chains have
  their own artifacts (e.g. EX-16-target gate work, EX-26 census,
  SC-7's log-entry draft) — not inventoried here.
- The frozen claim's after-shape (claims-frozen.md:27-33) is the authority
  for every remaining [[FILL]]; SC-3 verified the before-values and every
  artifact quoted above.
