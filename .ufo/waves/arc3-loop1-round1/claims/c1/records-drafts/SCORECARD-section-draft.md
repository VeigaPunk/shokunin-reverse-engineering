# SCORECARD.md round-section — DRAFT (arc3-loop1-round1, C1 chain records)

Status: DRAFT by seat SC-3 (C1 chain, scribe) — **NOT APPLIED**. Parent
integrates after the wave. Every `[[FILL: …]]` must be replaced from the
wave's sealed receipts (or the sentence rewritten to the honest-stop branch)
before landing. The C2/C3 bullets and table rows are shape-only: fill from
those chains' records. The pasteable text is the block below the horizontal
rule; the SC-3 notes at the bottom are not part of the section. Updated
2026-10-19 ~10:15Z with poll evidence (KdxToken/Rv2Token/Rv2Many legs,
EX-02 install receipt, EX-12 entry patch, EX-13 map variants + rehearsed
after-values, EX-15 containment, EX-14 manifest).

---

## arc3-loop1-round1 — coverage + operability + freshness: three claims, 2026-10-19

Round 1 of arc 3 (loop 1) — the first round after the operator halt at
arc2-loop1-round10 (`LOG.md:1385-1393`). The three finite owned proxies
remain saturated at 10.0 (`SCORECARD.md:19-25`, `:626-634`); the operability
and freshness moves are fleet-axis (unowned proxy — the standing recording
ruling, `:376-380`). [[FILL: round verdict qualifier — "Round admitted: all
three claims verify" / partial / honest-stop]]

- Wave: 64 seats frozen PRE-DISPATCH (items == roster asserted at dispatch),
  `opencode-go/deepseek-v4.1-flash` (opencode-go key 1 of 7 — round robin
  starts here); reports `.ufo/waves/arc3-loop1-round1/`; round report
  `.ufo/reports/arc3-loop1-round1/kaidoku.md`. Landed at [[FILL: commit(s)]].
- C1 coverage (owned) — the EVM real-bytecode leg, first held: three
  contracts compiled on-host with npm `solc` 0.8.37 (wave-isolated prefix;
  install receipt `receipts/solc-install.txt`, tarball sha256 `0e1a1ab6…`;
  two seats' independent KdxToken compiles byte-identical), planted sets
  recorded pre-probe; `rea inspect-evm-interface <file> <raw|hex>` recovers
  K/K on every leg — zero missing, zero extra, `dispatch:"abi"`, offsets
  equal to EX-07's independent dispatch parse: `Rv2Token` 5/5 (hex leg
  reproduced ×3 byte-identical, `ev_45849c8b…`), `KdxToken` 6/6 across ten
  legs and both pins (determinism twin re-issuing the same id
  `ev_4dd5ea20…`; path-insensitivity twin `ev_b2937090…`; EX-06's
  `ev_ad8fb290…`/`ev_56d89cb4…`/`ev_0a1317b9…`/`ev_9259f412…`/`ev_cde546a2…`/
  `ev_bb616f88…`; RV-2 replays re-issuing EX-05's ids), `Rv2Many` attack
  carrier 11/11 (`ev_d0d0b054…`). Input-shape traps fail closed (typed
  `invalid_request` on hex-on-binary / malformed hex / missing file; honest
  0-function envelopes on raw non-bytecode); the one `execution_failure`
  (EDQUOT) is host-state — EX-15 root-caused the saturated /tmp quota, the
  retry sealed clean. Creation blobs parse-and-empty (`functions: []`) — not
  claimed. The result lands as
  `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md` (EX-12's patch,
  31 lines) with the coverage-map token line-neutral (`corpus/README.md:38`,
  EX-13's verified variants — 190 → 190 lines, only :38 differs; land entry
  + token once, consistently); command A 81 → 82, prior 81 byte-identical,
  rules 13/13 — wave-rehearsed at EX-13's patched commits (82/82, missing
  [], dangling []; entry-absent control 81/81 + dangling token)
  [[FILL: parent re-measure at the records commit]]. The synthetic-leg
  baseline it supersedes: r3-07,
  `corpus/knowledge/2026-10-13-r3-evm-interface.md:47-76` (3/3 planted
  selectors on a hand-assembled 81-byte dispatcher).
  [[ALT honest-stop (frozen pre-write): the probe typed-refused on real
  bytecode / the install failed; sealed envelope [[FILL: path]]; claim NOT
  verified; no costume retry.]]
- C2 operability — [[FROM C2 CHAIN: the citation-drift probe's frozen-run
  guard closes: `expected.json` pins the sha256 of `pointer-table.json`;
  a tampered or absent table yields the declared could-not-evaluate class
  (exit 2), never silent findings; the SKILL.md registry row states the guard
  semantics; selftest 11 → 13 cases (clean-tree, tampered-table, absent-table)
  at exit 0; findings = 0 at HEAD. Evidence: `.ufo/gates/citation-drift/…`]]
- C3 freshness — [[FROM C3 CHAIN: the E22 scope-table finding dispositioned
  by measurement at HEAD — census v10: 0 stale / 0 ambiguous / 0 undeclared /
  0 unresolved, 5 historical (`claims/c3/EX-26/census-at-HEAD.txt`);
  [[FILL: re-key applied / row retired with cause / already-resolved-by-r8
  re-key, recorded in the census header]]; PASS 0/0/0/0 at the records
  commit]]
- Measured at the records commit: command A [[FILL: 82/82, 13/13,
  10.0/10.0 — rehearsed at EX-13's patched commits]]; probe selftest
  [[FILL: 13/13]] + findings=0; census v10 PASS [[FILL: 0/0/0/0]]; custody
  pre/post pairs 5/5 [[FILL: receipt times]]; no `config.toml` drift inside
  the wave window (the cross-wave diff's rewrite predates the wave —
  operator-side class).

| Axis | Before → after | Verdict |
|---|---|---|
| coverage — C1 | EVM held on the synthetic 81-byte dispatcher only (r3-07: 3/3 planted) → real solc-compiled bytecode on this host: Rv2Token 5/5, KdxToken 6/6 across ten legs (both pins, raw+hex, two independent compiles, determinism twin re-issuing one id), Rv2Many 11/11 — zero missing/zero extra throughout; knowledge 81 → 82, prior 81 byte-identical | [[FILL: improved / honest-stop]] |
| operability — C2 | [[FILL from C2: probe-exempt frozen-run guard → table digest pinned + exit-2 injection classes; selftest 11 → 13]] | [[FILL]] |
| freshness — C3 | [[FILL from C3: E22 drift finding → dispositioned at HEAD; census verdict before → after]] | [[FILL]] |
| depth / calibration | 10.0 / 10 (command A at [[FILL: records commit]]) | unchanged |

Learning trends: [[FILL: expansion — first real-bytecode EVM entry (coverage
surface grows past the synthetic leg); quality; discernment — cite the
round's attacks/refutations, e.g. the EDQUOT episode read as host-state not
refusal, the dangling-token pre-flight, the encoding traps refused typed,
the three-token-variant rehearsal]]. Planned: [[FILL: round 2 per schedule]].
Carried debt (named): creation-code `kind` classification (creation blobs →
`functions: []`); the `inspect_evm_interface` `ev_` id domain unmeasured —
no content-addressed identity claim; selectors stay bare hashes — no
signature DB / no name resolution (`PROVINCE.md:93`); vyper leg untested;
[[FILL: any new debt the wave names]]. Retired: [[FILL: the
EVM-real-bytecode frontier bullet; or none]].

---

## SC-3 notes (not part of the section)

- Format follows the arc2-loop1-round1..round10 sections (`SCORECARD.md:636`,
  `:1270`): intro paragraph → wave bullet → per-claim bullets → "Measured at"
  → axis table → learning trends / planned / carried debt / retired.
- Before-values for the C1 row are SC-3-verified at HEAD
  `e845c2b524ad2e59871e004c51a1386e192a74ab`: command A 81/81, 13/13,
  10.0/10.0, missing [], dangling [] (recipe `SCORECARD.md:92-124`;
  corroborated by `claims/c1/EX-11/command-A-before.txt`).
- "Line-neutral" map claim: the EVM coverage row (`corpus/README.md:38`)
  gains the new token without adding a map row. EX-13's `verification.txt`
  rehearses three variants (h1/h2 token `2026-10-19-arc3-r1-evm-solc`,
  h3 token `2026-10-19-arc3-r1-evm-real-solc`) — all line-neutral (190 →
  190, only :38 differs), apply-clean, probe-clean, and rehearsed to command
  A 82/82 with the entry landed / 81/81 + dangling without it. EX-12's entry
  patch carries the matching map hunk and its entry stem matches h3. **Land
  one token variant + the entry in the same commit; do not double-land the
  map hunk (EX-12's hunk B is byte-identical to EX-13's rehearsal).**
- Prior-81 byte-identity check for the parent:
  `git diff --name-only <before> <records> -- corpus/knowledge` must list only
  the new entry file (1 added, 0 modified, 0 deleted).
- Probe evidence details (SC-3 re-parsed the envelopes): canonical KdxToken
  legs — `EX-05/evidence-ids.txt` and `EX-06/evidence/*.json`; RV-2's
  replication + attack carriers — `RV-2/probe-*.json`, `attack/probe-many
  .json`; EX-08's edge matrix — `EX-08/probe-*.json` (recon baseline legs
  3/3, empty/ELF-magic/text legs, the noTMPDIR EDQUOT reproduction).
  Determinism twin: `kdx.raw` and `kdx.raw.rerun` share `ev_4dd5ea20…`.
  EX-07's `reconciliation.md` is the cross-source verdict (6/6, offsets
  equal, zero missing/extra; Rv2Token 5/5).
- The C3 census at HEAD (exit 0, 0/0/0/0, 5 historical) was sealed by EX-26
  in-round; if no re-key lands, the C3 bullet's disposition is the measured
  "no drift at HEAD; E22 already resolved by the r8 re-key" reading — the
  parent states it per the census header requirement.
- All remaining [[FILL]] fields trace to
  `.ufo/waves/arc3-loop1-round1/claims-frozen.md` (the after-shape, :27-33)
  plus the wave receipts; SC-3 verified the before-values and the artifacts
  inventoried in the LOG draft's poll notes.
