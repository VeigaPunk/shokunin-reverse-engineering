<!-- patch text — PROPOSAL ONLY, seat EX-06 (arc3-loop1-round4, c1). Not applied by this seat.
     Target: the round's C1 corpus entry (corpus/knowledge/, to be landed by the parent).
     Insert as an Observation block in the C1 entry, after the solc dispatch-shape
     observations and before the entry's Unknowns line. Every claim below is first-hand
     from .ufo/waves/arc3-loop1-round4/claims/c1/EX-06/ (envelopes in probe/, census and
     reconstruction in evidence/, full analysis in analysis.txt). -->

- **Observation (RESULT — Vyper leg, first measured: 4 carriers, K/K on every leg):** the
  r1/r3 entries' named Unknown "Vyper and solc versions other than 0.8.37" now has
  measured evidence. Four vyper-compiled runtime carriers (vyper `0.4.3+commit.bff19ea2`,
  on-host compiles by EX-02/EX-03/EX-04) were probed at the first pin (`rea-agents@6.4.0`)
  and the second (`6.7.0`) under a disk-backed `TMPDIR`: `CarrierV` (EX-04, 1,562 B
  `57d6fd0a…`, K=15), `StewardToken` (EX-03, 3,337 B `1846469b…`, K=22), `Smoke` (EX-02,
  168 B `415e6b1b…`, K=4) and `T5` (EX-02, 181 B `e54549b2…`, K=3). Every hex leg is
  set-equal to the carrier's own ABI-derived selector set — zero missing, zero extra,
  `dispatch:"abi"` throughout — and every leg's decoded `bytecode.sha256` equals the
  runtime bytes. The extractor recovers Vyper dispatch tables at K=3…22 with no observed
  degradation. `CarrierV` hex ids: `ev_d1792f57…` @6.4.0 (rerun re-derives),
  `ev_62e1b9e6…` @6.7.0, `ev_eac08124…` raw; `StewardToken` `ev_6b8a15c4…` @6.4.0,
  `ev_b07b8971…` @6.7.0. Zero false positives: `CarrierV`'s 21 PUSH4 immediates resolve
  to 16 distinct values — the 15 planted selectors plus `08c379a0` (`Error(string)`, 6×),
  which the probe correctly did not report as a function.

- **Observation (dispatch-shape class — Vyper jump table, reconstructed at byte level):**
  the vyper carriers share the `5f3560e01c` prologue class but dispatch through a
  **selector-indexed jump table**, not a compare tree: `PUSH1 0x02 PUSH1 0x0d DUP3 MOD`
  (slot = `selector % 13`), `PUSH1 0x01 SHL`, `PUSH2 0x0600 ADD`, `PUSH1 0x1e CODECOPY`,
  `PUSH0 MLOAD JUMP`, then per-entry `JUMPDEST PUSH4<sel> DUP2 XOR PUSH2<next> JUMPI`.
  `CarrierV`'s table at `0x600` is `0x29c 0x5e7 0x50b 0x400 0x5ac 0x43f 0x53d 0x5e7
  0x590 0x574 0x382 0x5e7 0x18` — all 11 distinct heads are JUMPDESTs, and walking the
  chains yields exactly the 15 planted selectors. This is a third dispatch class alongside
  r3's `GT`/`EQ` binary search and r1's linear `EQ` chain.

- **Observation (offset semantics — the r1/r3 "offsets land on JUMPDEST" reading does NOT
  hold for this class):** on `CarrierV` all 15 reported `bytecode_offset`s equal
  `entry_jumpdest + 12` — the first byte after the match test, i.e. the fall-through body
  entry — and all 15 are preceded by `0x57` (JUMPI). **0/15 land on a JUMPDEST.** The
  uniformly observed `probe_offset − push4_immediate_offset = +11` is a property of this
  dispatcher, not a tool defect; the earlier reading is therefore scoped to
  solc-convention carriers (and to the hand-assembled control, whose offsets are declared
  immediates). Reported offsets should be read as "the dispatch test's match-branch
  fall-through", which on solc-convention carriers happens to coincide with a JUMPDEST.

- **Observation (mutability/argument inference degrades on arg-taking Vyper externals —
  measured, mechanism visible):** on `CarrierV` `inferred_state_mutability` agrees with
  the compiled ABI on only 7/15 functions, and the split is structural: **7/7 no-arg
  functions are correct, 8/8 arg-taking functions are inferred `payable`** regardless of
  their true mutability (`view`, `pure` and `nonpayable` all misread). The bytes show why:
  no-arg bodies open with the bare guard `CALLVALUE PUSH2<revert> JUMPI`
  (`346105fc57`), while arg-taking bodies open with the combined
  `PUSH1 0x24 CALLDATASIZE LT CALLVALUE OR PUSH2<revert> JUMPI` (`602436103417`) — the
  value check is folded into a size/value guard the upstream inference does not separate.
  `inferred_arguments` arg *count* is correct 15/15, but 3/15 type strings read `uint256`
  where the ABI declares `address` (all three are single-`address` getters). Selector
  recovery is unaffected (15/15); the degradation is inference-only and is recorded as a
  measured limit of this tool class, not a recovery failure.

- **Observation (normalizer traps when comparing against Vyper's own
  `method_identifiers` — both would produce spurious "missing selector" reports):**
  (i) `__default__` is listed by `method_identifiers` (`0x89402a72`) but is the Vyper
  fallback and is dispatched by fallthrough — the constant does not occur anywhere in
  either carrier's runtime bytes (`bytes.fromhex("89402a72") in code` → False for both
  `CarrierV` and `StewardToken`), and the correct K excludes it; (ii) Vyper's
  `method_identifiers` output **drops leading zeros** (`0x95ea7b3`, `0xc751377`,
  `0x6fdde03` for `approve`, `fee_of`, `name` in EX-03's artifact) — a raw set comparison
  against the probe's 8-char `0x…` form reports three false misses. Left-padding to 8 chars
  makes `StewardToken` 22/22. Any future Vyper K/K harness must apply both normalizations.

- **Observation (envelope delta and id domain, vyper carrier):** 6.7.0 adds a top-level
  `relationship_coverage` key (`null` here) and is otherwise content-identical to 6.4.0;
  `raw_result.metadata` is `null` on this carrier under both pins, unlike the r1/r3 solc
  carriers whose terminal CBOR trailer was decoded. `--full-output` wraps the envelope as
  `{ok, data, meta}` with `data` byte-equal to the bare `--format json` envelope. The
  path-sensitive id reading holds: same bytes + same request at the same path re-derive;
  the same bytes at another absolute path mint a different id (EX-06's `ev_d1792f57…` vs
  EX-04's `ev_405e2a2a…` for identical bytes); uppercase/`0x`-prefixed carriers mint fresh
  ids while decoding to the same bytecode sha256. Compare by decoded `bytecode.sha256`.
  Cross-seat check: EX-06's and EX-04's independently captured envelopes for the same
  carrier are content-identical under a normalized deep-diff (0 diffs after stripping
  `evidence_id`, `local_path`, `name`, `parameters`, `locations`, `diagnostics`).

- **Observation (input traps reproduce on the Vyper class):** `hex` declared on a `.bin`
  carrier → exit 1, typed `{"code":"invalid_request","category":"invalid_input"}`
  (`issues[0].reason == "invalid_format"`), fail-closed; `raw` declared on a `.hex`
  carrier → exit 0, 0 functions, decoded sha256 equal to the hex *file's* sha256
  (`e0b1021c…`) — the r1 `ev_60062ad0…` / r3 `ev_704ce585…` class; the creation blob
  (`CarrierV` creation.hex, 1,637 B) parses to 0 functions, consistent with the r1 erratum
  that creation blobs embed the runtime table while the tool's scope is the runtime entry.
