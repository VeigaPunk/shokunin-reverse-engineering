# chain-ledger.draft — arc3-loop1-round3 · chain c1 (EVM optimizer-family extension)

<!-- SEAT SC-1 (chain c1, role scribe). status: DRAFT v1 — point-in-time snapshot;
     generated-utc: 2026-10-19T13:10Z; repo-HEAD pin: c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311
     frozen sequence (claims-frozen.md + seat line): compiler check → compile → probe →
     reconcile → controls → rerun, each step sha256-pinned.
     Dual placement: byte-identical to claims/c1/SC-1/receipts/chain-ledger.draft.md;
     both hashes re-derived at close and recorded in seats/SC-1.md (rule #14). -->

## Method and evidence rules

- Every sha256 below was **computed by this seat** with `sha256sum`/Python `hashlib`
  at capture time (2026-10-19T13:07–13:12Z), never copied from a producer's text.
  All bytes referenced live in this seat's artifact tree
  `.ufo/waves/arc3-loop1-round3/claims/c1/SC-1/` (copy of the scratch run at
  `/var/tmp/sc1-r3`, verified 85/85 by `sha256sum -c evidence/MANIFEST.sha256.txt`;
  the manifest's own sha256 is `5c41ab22…`).
- The left half of this ledger is a **reference rehearsal**: this seat ran the whole
  chain itself on scratch carriers so every link has an independent measurement at
  this commit. It does not adjudicate the claim; reviewers/VZ-1/parent own that.
- Status vocabulary: **LANDED** · **PARTIAL** · **GAP** (absent at capture) ·
  **VOID** (0 bytes). "An unrun check has not passed" — GAP rows carry no verdict.
- Recompute: `sha256sum <path>` per row; whole-tree snapshot command in footer.
- Host facts re-derived: node v26.12.0 · npm 11.20.0 · rea-agents 6.4.0 and 6.7.0
  (`npx -y … --version`) · all probes with `TMPDIR=/var/tmp/sc1-r3/tmp` (disk-backed;
  `/tmp` carries `usrquota` — the r1 EDQUOT class stands, re-observed in the mount flags).

## Frozen inputs (SC-1 computed)

| input | sha256 |
|---|---|
| `claims-frozen.md` (round 3) | `ffac38a12355f512f02288b7df4fed1e0922466a64cf9a318642d5e47de3660f` |
| r1 knowledge entry `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md` | `dd986f562a6c7b2e759ebb90c9855adff38e9226b1d9e27af36b6e3a2aefc3d4` |
| r1 predecessor ledger `arc3-loop1-round1/claims/c1/receipts/chain-ledger.draft.md` | `6d9427ccfe1b238dfba8d794e70d4a9fbdae61073bff7753de33d583f772b553` |
| r1 solc install receipt `arc3-loop1-round1/claims/c1/EX-02/install-receipt.txt` | `3541560197b651886f0a7eac98438484c47c0436080641b58444420745e3fcb3` |
| r1 planted set `arc3-loop1-round1/claims/c1/RV-2/expected-selectors.txt` | `85af43370d995e9823cc53d05013a429366ee49b784db9e2731b35ec7be1e1d6` |
| gate `.ufo/gates/custody-pair/custody-pair.py` | `112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa` |
| gate `.ufo/gates/citation-drift/pointer-table.json` | `738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f` |
| gate `.ufo/gates/citation-drift/expected.json` | `ff47bfd60b383c22c0897e8c89081dd738f67d7f28904292c47f5d09e4173ba7` |
| gate `.ufo/gates/c1-census-v10.py` | `d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5` |

## Reference rehearsal — step ledger (SC-1's own run, chain order)

### S0 — compiler check (no install; r1 prefix reused)

| fact | value (SC-1 re-derived) |
|---|---|
| tarball sha256 (receipt claim) | `0e1a1ab6d12c37f5503271b2c4679cd433459c884851920d148d6fb154575a51` (6,476,046 B) |
| cache content file | `~/.npm/_cacache/content-v2/sha512/89/e5/1874f0d118d28cb19a427e2f6d63ae10f804a82fcb7284bbaf7fd7058aa0ecfba8a3971f169f60918b437bd40942bd1c74574f76ae5518bb76f73eec5694`; its sha512 = registry `dist.integrity`; its sha256 = the receipt value → **MATCH** |
| prefix files | `package.json` `b4205b08…` · `package-lock.json` `9f6dcab2…` · `solc/package.json` `b3a90035…` · `solc.js` `188c3fdc…` · `soljson.js` `221d7a66…` — all equal the r1 ledger pins |
| `solcjs --version` | `0.8.37+commit.f401782d.Emscripten.clang` (exit 0) |

No install was performed this round (frozen rule); the r1 receipted prefix is executed
in place from `arc3-loop1-round1/tools/solc-prefix/`.

### S1 — compile (reference carriers, pinned solc)

| leg | source (sha256) | mode | runtime.bin (bytes) | runtime.hex | creation.bin | abi |
|---|---|---|---|---|---|---|
| A `Rv2Token.sol` | `a4bc2d78…` (r1 source) | opt0 (control) | `c1081a56…` (1,943) | `8495d7db…` | `04e07f54…` | `4261652c…` |
| A `Rv2Token.sol` | `a4bc2d78…` | **opt200** | `ed6c8a76…` (978) | `a07bef2e…` | `b3b7e6d6…` | `4261652c…` |
| B `VaultCourt.sol` (authored this seat) | `1af58859…` | opt0 | `f7b94c7a…` (3,197) | `597cce5c…` | `1dbc438a…` | `c9c12697…` |
| B `VaultCourt.sol` | `1af58859…` | **opt200** | `66024ee3…` (1,529) | `b9442675…` | `3e40d9a4…` | `c9c12697…` |

- **opt0 control MATCHES**: leg-A opt0 runtime.bin = `c1081a565869b50387211b25afaf3768294aa774c35845bc3a8c0b12cfe15e74`
  — byte-identical to the r1 pin (`corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:12`).
  The compile pipeline is thereby validated before the optimizer legs are believed.
- compile determinism: full re-run into `out2/` → both opt200 runtimes `cmp` exit 0.
- optimizer deltas: A 1,943 → 978 B; B 3,197 → 1,529 B; ABI unchanged by optimization
  (both modes share the abi sha) — shape delta is byte-level only.
- leg B is the non-ERC-20 shape: `receive()`/`fallback()` payable + mixed mutability
  (payable/nonpayable/view/pure) + public getters; planted K = 10
  (`evidence/planted-K-VaultCourt.json` `ad8347bd…`), vs leg A K = 5 (`bce3e125…`).
- planted sets frozen pre-probe: independent pure-Python keccak == compiler
  `evm.methodIdentifiers` on both carriers, 0 mismatches; written 13:07:38.511Z,
  22.4 s before the first probe file (13:08:00.949Z).

### S2 — probe (rea-agents 6.4.0 unless noted; `TMPDIR` disk-backed)

| leg | probe file sha256 | evidence_id | K | subject digest | exit |
|---|---|---|---|---|---|
| A opt200 hex @6.4.0 | `0b79deb70601…` | `ev_42cd9da2…` | 5 | `a07bef2e…` (the hex file) | 0 |
| A opt200 hex @6.4.0 rerun | `0b79deb70601…` (byte-identical file) | `ev_42cd9da2…` | 5 | `a07bef2e…` | 0 |
| A opt200 hex @6.4.0 renamed path | `649ff9b7…` | `ev_8bc302e0…` | 5 | `a07bef2e…` | 0 |
| A opt200 hex @6.7.0 | `823dd18a…` | `ev_25238e85…` | 5 | `a07bef2e…` | 0 |
| A opt0 hex @6.4.0 | `3be6d01e…` | `ev_01a2d0fd…` | 5 | `8495d7db…` | 0 |
| B opt200 hex @6.4.0 | `d391e5468d03…` | `ev_d1d0bc1c…` | 10 | `b9442675…` | 0 |
| B opt200 hex @6.7.0 | `dd5b3e0159f2…` | `ev_1d504cbc…` | 10 | `b9442675…` | 0 |
| B opt200 raw @6.4.0 | `564f0af6f6ec…` | `ev_e1aa1a50…` | 10 | `66024ee3…` (the bin file) | 0 |
| B opt0 hex @6.4.0 | `23f0bbfb3d26…` | `ev_b295655e…` | 10 | `597cce5c…` | 0 |
| B opt200 creation hex @6.4.0 | `da219709…` | `ev_72ce32af…` | 0 | `2a449601…` | 0 |
| dispatch-less `6001600101` | `e5c324ba…` | `ev_12b72fed…` | 0 | `dc672ce8…` | 0 |
| B bin as hex (mismatch) | `44507bd6…` | — | — | — | 1, typed `invalid_input`/`invalid_request` |
| B opt200 tampered hex | `69e127d9…` | `ev_101dde37…` | 10 | `da4c6ffb…` (tampered hex file) | 0 |

- **K/K on every clean leg**: 5/5 (A opt200, both pins), 10/10 (B opt200 hex+raw, both pins,
  and B opt0), zero missing / zero extra vs the pre-probe planted sets
  (`evidence/probe-sels-*.txt` vs `evidence/planted-K-*.sorted`; MATCH lines in seat report).
- decoded `bytecode.sha256` = the carrier file's sha256 on every leg; raw-path subject ≡
  decoded digest (`66024ee3…`); `dispatch:"abi"` on every recovered function;
  `bytecode.kind` stays `"unknown"` on all legs (consistent with the r1 refuted-hypothesis note).
- mutability inference: A opt200 `{nonpayable:3, view:2}` (same split as the r1 opt0 leg);
  B opt200 `{payable:1, nonpayable:2, view:7}` — the `pure` function reads back as `view`
  (conservative upstream inference; recorded, not a defect).

### S3 — reconcile (independent of the probe)

- M1 (own linear-sweep disassembler + EQ-site parse; `tools/selector-recon.py` `99c3c32d…`,
  the r1 EX-07 tool, byte-identical copy): A opt0/opt200 anchor `5f3560e01c` @25, strict
  chain = 5, EQ sites = 5. B opt0/opt200 anchor `5f3560e01c` @13, **strict chain = 0,
  EQ sites = 10** — the 10-selector dispatcher is a binary-search shape
  (`…80636392a51f11610058…` in the runtime), so the strict `DUP1 PUSH4 EQ PUSH2 JUMPI`
  chain parse reads zero while the loose EQ-site parse reads the full set. Both opt modes
  behave identically at K=10: the shape boundary seen here is selector-count-driven, not
  optimizer-driven.
- offsets: A opt200 probe offsets `{89,129,147,166,206}` are **set-equal** to M1 chain
  dests (dispatch-target JUMPDESTs — the r4 erratum semantics re-confirmed on optimizer
  output); all 10 B offsets (`329,362,424,455,473,504,556,577,631,696`) land on byte `5b`.
- M2 (pure-Python keccak scan of signatures against code): 5/5 and 10/10 found.
- probe-vs-M1 selector sets agree on all four clean legs; tampered leg: M1 reports
  `d0e30db1` present and `d0e30db0` absent — same single substitution the probe reports.
- cross-wave envelope identity: `EX-06/evidence/recheck-rv2token-hex-6.4.0.json`
  (`f2aec424…`) is byte-identical (`cmp` exit 0) to r1's `RV-2/probe-runtime-hex-6.4.0.json`
  — the r1 pin re-derives unchanged in round 3.

### S4 — controls

1. opt0-vs-opt200 comparison legs on the same sources: MATCH both carriers (probe).
2. compiled-byte control: opt0 re-derivation equals the r1 pinned bytes (S1).
3. tamper: one selector byte flipped at offset 75 (`d0e30db0→d0e30db1`) → probe reports
   exactly the mutated selector, zero other drift; carrier digest differs (`d5e63b0c…`).
4. creation code: parsed-and-empty (0 functions, exit 0) — not an exclusion.
5. dispatch-less blob: 0 functions, no false positives.
6. encoding mismatch (bin as hex): typed refusal, exit 1 — fail-closed.
7. planted-K freeze precedes all probe files (S1 timestamps).
8. determinism: compile re-run and probe re-run both byte-identical.

### S5 — rerun (identity)

- identical invocation, identical bytes, same path → **byte-identical envelope** (`cmp` exit 0)
  and same id `ev_42cd9da2…`; 6.7.0 legs re-derive the same K/sets with different id domain.
- same bytes, different path (renamed carrier) → different id `ev_8bc302e0…`, same subject
  digest `a07bef2e…` — path-sensitivity re-confirmed for this verb family (consistent with
  the r1 EX-05 renamed leg). Different bytes → different ids (`ev_01a2d0fd…` vs
  `ev_42cd9da2…` vs `ev_101dde37…`).

**Honest-stop branch status (pre-written in the frozen claim):** the prologue class did
**not** differ — all four carriers sit in the r1-recorded `5f3560e01c` class; the branch is
not triggered. The genuine shape delta found is the K=10 binary-search dispatcher (both
modes), recorded above as the round's delta, not a defect. No honest stop is warranted by
this rehearsal: optimizer-enabled dispatch shapes were recovered K/K, zero extras.

## Wave tracker — chain links to producer seats (snapshot 2026-10-19T13:12Z)

| link | status | artifacts at capture (path → sha256 prefix) | producers |
|---|---|---|---|
| compiler check / prefix reuse | LANDED | r1 receipt `35415601…`; round-3 hashes byte-stable vs r1 ledger (S0) | EX-02 (r1), SC-1 |
| compile | LANDED | `PL-1/evidence/compile-summary.json` `d7f991b2…` (OptVault opt200 776 B, MutMix opt-off); `EX-03/source/carrierA.sol`; `EX-04/`+`EX-05/` carriers incl. opt200; `EX-10/out/VaultB.{nopt,opt200}.runtime.*`; `EX-14/before-state.txt` `dd282e26…`; SC-1 reference (S1) | PL-1, EX-03, EX-04, EX-05, EX-10, EX-14 |
| probe | LANDED | `EX-04/evidence/probe/probe-opt200-hex-6.4.0.compare.json` `acdc086f…` (11/11 set-equal); `EX-06/evidence/recheck-rv2token-hex-6.4.0.json` `f2aec424…` (byte-identical to r1); `EX-07/legA-*, legC-*, optB-*` across 6.4.0/6.5.0/6.7.0 + reruns + `idpath-*`; `EX-10/probe/…`; SC-1 13 legs (S2) | EX-04, EX-06, EX-07, EX-10, SC-1 |
| reconcile | PARTIAL | `EX-07/legA-compare.txt` + `EX-10/recon-B-*.json`; `EX-04/evidence/probe/offset-check-{noopt,opt200}.json` (push4 pc / push2 target / JUMPDEST rows); `RV-3/prereg-verification-plan.md` `feaa3e47…`; SC-1 M1/M2 recompute (S3) | EX-07, EX-10, EX-04, RV-3, SC-1 |
| controls | PARTIAL | SC-1 control set 1–8 (S4); EX-04 offset checks; remainder GAP at capture | SC-1, EX-04 |
| rerun | PARTIAL | SC-1 byte-identical rerun pair + renamed leg (S5); `EX-07/*-rerun.json`; `EX-10/probe-B-nopt-hex-6.4.0-rerun.json` | SC-1, EX-07, EX-10 |
| landing (knowledge entry + map token + command A after + custody post-pair) | PARTIAL / GAP | `records-drafts/map-token-patch.md` `333ca590…`; `RV-4/command-A-before.txt` `9de3cbdd…` (**82/82**, rules 14, depth 10.0 at `c07af80f`); knowledge-entry patch: **GAP**; command A after: **GAP**; custody post-pair: **GAP** | RV-4, SC-2 (drafts), parent |
| seat reports | PARTIAL at capture | `seats/` at 13:12Z held 7 reports — CU-1, EX-04, EX-11, EX-22, EX-25, PL-1, SC-5 (c1 chain: EX-04, EX-11, PL-1); remainder GAP | — |

Directories with 0 files at capture (GAP): `claims/c1/EX-12/`, `claims/c1/VZ-1/`;
`claims/c1/EX-11/` read 0 files at the 13:09Z poll and landed
`command-A-before.txt` + `compare-{carrierA,rv2}.txt` + `control-content-raw.json` by
13:11:57Z — after this table's rows were drafted; re-check at integration (this line
corrected at close, 13:12Z).

## Verification-hygiene observations (recorded, not adjudicated)

1. `tools/selector-recon.py` docstring for the `scan` subcommand states
   `scan <code-file> <sigs-file> [hex|raw]` but the code reads argv[3] as the encoding and
   argv[4] as the signatures — the inverse order. Found by a failed invocation this run
   (`FileNotFoundError: 'hex'`); recorded, tool not patched (patch text belongs to a
   reviewer seat).
2. `rea-agents@6.4.0 --format json` emits the **unwrapped** evidence object
   (`evidence_id` at top level; no `data`/`meta`/`ok` wrapper), while r1's CR-1 battery
   files were wrapper-shaped (produced with `--full-output`). Consumers must accept both.
   The typed-refusal body is a flat object with `category`/`code`/`message` keys.
3. `normalized_result.bytecode.hex` embeds the whole carrier in the envelope — envelope
   size scales with carrier size.
4. Planted-K timing evidence rests on filesystem mtimes; both timestamps quoted (S1).
5. `claims/c1/receipts/` did not exist before this seat; created for this ledger, mirroring
   the r1 layout. The seat-dir copy is byte-identical by construction (hash check at close).
6. SC-1's probe legs ran at scratch paths under `/var/tmp/sc1-r3` — subject digests are
   path-independent (file bytes), ids are not (renamed leg, S5).

## Footer

- Snapshot commands:
  - scratch: `cd /var/tmp/sc1-r3 && sha256sum -c evidence/MANIFEST.sha256.txt`
  - landed copy: `cd .ufo/waves/arc3-loop1-round3/claims/c1/SC-1 && sha256sum -c evidence/MANIFEST.sha256.txt`
- Capture totals: 85 files in the SC-1 artifact tree (manifest `5c41ab22…`); 13 probe legs;
  4 compiled legs; 2 planted sets; 1 command-A before-state run
  (`evidence/command-A-before-c07af80f…json`: 82/82, rules 14/14, coverage 10.0, depth 10.0 —
  SC-1's own run at the HEAD pin, equal to RV-4's).
- Self-identity policy (rule #14): this file's sha256 is recorded in `seats/SC-1.md` at
  close, after the final revision, together with the hash of the byte-identical copy at
  `claims/c1/SC-1/receipts/chain-ledger.draft.md`.
- Superseded by the parent's integration-time ledger at the records commit; every GAP above
  must be re-checked there, not assumed closed.