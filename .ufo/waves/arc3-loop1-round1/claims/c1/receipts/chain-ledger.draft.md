# chain-ledger.draft — arc3-loop1-round1 · chain c1 (EVM real-bytecode leg)

<!-- SEAT SC-1 (chain c1, role scribe). status: DRAFT v3 — point-in-time snapshot;
     the parent regenerates/repins at integration. generated-utc: 2026-10-19T10:19Z.
     repo-HEAD pin: e845c2b524ad2e59871e004c51a1386e192a74ab
     frozen sequence (claims-frozen.md): install → compile → probe(raw|hex) →
     reconciliation → control → rerun -->

## Method and evidence rules

- Every sha256 below was **computed by this seat** with `sha256sum` at capture
  time (2026-10-19T09:58–10:19Z), never copied from a producing seat's text —
  including the full recompute of EX-07's reconciliation table (all pins
  matched; see R5). Paths are relative to the repo root unless noted.
- Status vocabulary: **LANDED** · **PARTIAL** · **GAP** (absent at capture) ·
  **VOID** (0 bytes). "An unrun check has not passed" — GAP rows carry no
  verdict; claim adjudication belongs to reviewers/parent.
- Recompute: `sha256sum <path>` per row; whole-tree snapshot command in footer.

## Frozen inputs (SC-1 computed)

| input | sha256 |
|---|---|
| `claims-frozen.md` | `fd670767aeeda0c517e6d56526dd2ef531c60a313d976575218f4f152930c552` |
| `corpus/knowledge/2026-10-13-r3-evm-interface.md` (r3-07 synthetic leg) | `7e8340f9bb4d45f55be7bd8f0a292c5a48412908dd1b3ec7eead65a83659caa8` |
| `SKILL.md` (command-A input) | `5c93c7c1bf45c72ca518f87fbba6f2a0bbf5685f67d263714b210a9a058830d4` |
| `corpus/README.md` (command-A input; = RV-4 `README.before.md`) | `7c0cf67143eebc57a949c54884712262954d2ed984cd66eea8aab44362cb2568` |
| `.ufo/gates/c1-census-v10.py` | `36e96cd59b622f7b9acd424156d02184fa690df61dd96242899ad9a3b4f52d48` |

## Step ledger — one row per step

| # | step | status | key artifacts (path → sha256 prefix) | producer |
|---|---|---|---|---|
| R0 | custody pre-pair (boundary, frozen rule) | LANDED | `claims/cross/receipts/config-pre-pair.txt` `b8ed1936…` + metadata `85fa1860…` + `custody-snapshots.txt` `d7cb11a4…`; c1 copy `claims/c1/receipts/config-pre-pair.txt` `28491903…`; corroborations EX-01 `97d2fab1…`, EX-02 `312c6b40…`/`e696b05f…`, EX-15 T0/T1 `7a4ada55…`/`5a4bdce4…`, EX-10 `306f1f8f…` | CU-1 (+EX-01/02/10/15) |
| R1 | install | LANDED | `EX-02/install-receipt.txt` `35415601…`; `tools/solc-prefix/package.json` `b4205b08…`, `package-lock.json` `9f6dcab2…`, `node_modules/solc/package.json` `b3a90035…`, `solc.js` `188c3fdc…`, `soljson.js` `221d7a66…`; parent patch `EX-02/proposed-receipts-solc-install.patch.md` `1ffde4b2…` | EX-02 |
| R2 | compile | LANDED | KdxToken leg: `EX-04/KdxToken.sol` `c2980385…` (= `EX-06/evidence/KdxToken.sol`), `EX-04/token.runtime.bin` `9c40940e…`, `.hex` `69a15782…`, `token.creation.bin` `6aeba8d7…`, `token.abi` `40ad881e…`; `EX-05/kdx-runtime.{bin,hex}` byte-equal to EX-04's; smoke leg `EX-02/smoke/…` (`Smoke_sol_Smoke.bin` `530efc7b…`, K=5); replication `RV-2/Rv2Token.runtime.{bin,hex}` `c1081a56…`/`d7f73058…`; KdkToken leg `EX-03/token.sol` `497d70f2…` (compiled+probed by VZ-1, K=9) | EX-04, EX-05, EX-06, EX-02, RV-2, VZ-1 |
| R3 | probe raw | LANDED | `EX-05/kdx.raw.json` `f8be246a…` = `ev_4dd5ea20…`, 6/6; `EX-05/kdx.raw.rerun.json` `a5d2e542…` (same id); `EX-05/kdx.raw.renamed.json` `e45d7778…` = `ev_b2937090…`; `EX-06/evidence/run-raw-6.7.0.json` `b374ec27…` = `ev_9259f412…`; `RV-2/probe-runtime-raw-6.4.0.json` `5e5e1faf…` = `ev_3aacd424…` (5/5 Rv2) | EX-05, EX-06, RV-2 |
| R4 | probe hex | LANDED | `EX-05/kdx.hex.json` `93188f83…` = `ev_2a79dd25…`; `EX-06/evidence/run-hex-6.7.0.json` `5188d59f…` = `ev_56d89cb4…`; `run-hex-6.4.0.json` `f1021252…` = `ev_ad8fb290…`; `RV-2/probe-runtime-hex-6.4.0.json` `f2aec424…` = `ev_45849c8b…`; `probe-runtime-hex-6.7.0.json` `12e5d171…` = `ev_19d7d3cb…`; VZ-1 KdkToken leg `VZ-1/ex03-kdktoken-probe.json` `aed448ae…` = `ev_92b7e2fc…` (9/9) — all `dispatch:"abi"` | EX-05, EX-06, RV-2, VZ-1 |
| R5 | reconciliation | LANDED | `EX-07/reconciliation.md` `162b20b7…` (verdict K/K=6/6, 11 source-sets); `reconciliation-run-all-legs.txt` `a356c3a9…` (`VERDICT: ALL SOURCES AGREE`); SC-1 recompute of every pin MATCHED; `EX-06/evidence/planted-K.json` `063eb723…`; `SC-2/` crosschecks + manifest snapshots; `RV-3/independent-verification.txt` `e15c9212…`; tree-level after-state (CR-2 scratch clone + EX-12 patch): 82/82, missing [], dangling [] (`CR-2/command-A-runs.txt` `2405729c…`) | EX-07, SC-2, RV-3, CR-2 |
| R6 | control | LANDED | EX-07's seven controls (tamper/keccak-independence/dispatch-less/extra-PUSH4/creation-vs-runtime/encoding-mismatch/digest pins) in `reconciliation.md`; refusal leg `EX-05/kdx.hex-on-bin.json` `ab073b51…`; creation-empty legs `EX-05/kdx-creation.raw.json` `e6f1b60a…`, `EX-06/…/run-creation-hex.json` `38a05b85…`, `RV-2/probe-creation-hex-6.4.0.json` `95fea9be…`; EX-08 edge battery (empty/elfmagic/nonbytecode/missing, exits decoded below); `RV-2/attack/` (tampered-digest `b9c1af3a…`, drop-one `e9bccfed…`, planted-plus-bogus `2ff578a7…`); name-mismatch control (CR-2 run 3: dangling=1, coverage 9.88) | EX-07, EX-05, EX-06, EX-08, RV-2, CR-2 |
| R7 | rerun | LANDED | `EX-09/rerun-compare.md` `846c9f78…` (id stable: 4 runs, envelope byte-identical); `kdx-rerun-1.json` `020e3800…`, `kdx-rerun-2.json` `7ec49625…`, `reid.py` `879e09a1…`; SC-1 envelope check: `jq -c '.data'` identical (`0144b17d…`) across all 4 rerun files; `RV-2/rv2-rerun-kdx-{hex,raw}-6.7.0.json` byte-equal to EX-06's legs | EX-09, RV-2 |
| R8 | landing/close (boundary) | GAP (patch-text drafts only) | drafts `records-drafts/LOG-entry-draft.md` `2f33bb79…`, `SCORECARD-section-draft.md` `42359161…`; knowledge entry as patch text `EX-12/knowledge-entry.patch.md` `d662c195…` (+ CR-1 additions `d117fcfe…`); map-token `EX-13/_scratch/map-token.patch` `ddfe0116…` (= `RV-4/map-token.frozen.patch`) + `EX-13/map-token.patch.md` `27d59a11…` + `verify-battery.py` `b57bbb86…`; `README.after.md` `b74b8d34…`; verifier `RV-4/verify_map_token.py` `08e052c4…` + selftests + `final-artifact-verification.txt` `d172efb1…`; chain verdict `VZ-1/verdict.md` `ccbad891…` (C1 VERIFIED, wave-level); critic patches `CR-2/proposed-fixes.patch.md` `a62067dd…`, `CR-1/EX-07-reconcile-unwrap.patch.md` `f5e58cf6…`; actual landing **GAP**; command-A at records commit **GAP**; custody post-pair **GAP** | SC-2/SC-3, EX-12, EX-13, RV-4, VZ-1, CR-1, CR-2 |

## Row details

### R0 — custody pre-pair

Canonical CU-1 receipt `b8ed1936…` (capture-utc 2026-10-19T09:57:18Z, 5 paths,
sha256-capture-only) + metadata `85fa1860…` + snapshots `d7cb11a4…`. A copy
landed at `claims/c1/receipts/config-pre-pair.txt` `28491903…` (same 5 values;
copy, not a new capture). Independent recomputes: EX-01 `97d2fab1…` (3
implementations, 5/5), EX-02 pre `312c6b40…` / post `e696b05f…` (diff empty),
EX-15 T0 `7a4ada55…` / T1 `5a4bdce4…` (cross-wave diff `d30cf352…`: config.toml
churned pre-round; matches pre-pair value `8cbacd48…`), EX-10 `306f1f8f…`
(stanza-key anchored, pin `rea-agents@6.7.0`, no in-window drift at 09:58–10:00Z).

### R1 — install

npm `solc` **0.8.37** (`0.8.37+commit.f401782d.Emscripten.clang`), tarball
`https://registry.npmjs.org/solc/-/solc-0.8.37.tgz` sha256
`0e1a1ab6d12c37f5503271b2c4679cd433459c884851920d148d6fb154575a51` (receipted;
tarball bytes not recomputed by SC-1), 6476046 B. Command:
`npm install --prefix .ufo/waves/arc3-loop1-round1/tools/solc-prefix solc@0.8.37`
→ `added 8 packages in 402ms` exit 0. Prefix: 99 files / 9.6M (SC-1 counted).
SC-1 registry check 09:58Z: `npm view solc version` → `0.8.37`, same tarball URL.
SC-1 cross-check: prefix `solc.js`/`soljson.js` byte-identical to ambient
fnm-node-v24.21.0 tree (both files, both trees; VZ-1 re-hashed the tree
independently — same values). Before-state nuance: ambient solc 0.8.37
pre-existed; the receipted install is the isolated pinned copy.

### R2 — compile

- KdxToken (canonical real target): `EX-04/KdxToken.sol` `c2980385…` is
  byte-identical to `EX-06/evidence/KdxToken.sol`; **EX-04, EX-05, EX-06
  independently compiled it to byte-identical carriers** — runtime.bin
  `9c40940e…`, runtime.hex `69a15782…` (SC-1 recomputed each). Creation blob
  `6aeba8d7…` (EX-04 = EX-05). ABI `40ad881e…` (EX-04 = EX-05 = EX-07 copy).
- Smoke leg (EX-02): `Smoke.sol` `647992dd…` → `Smoke_sol_Smoke.bin` `530efc7b…`
  (1370 hex chars), K=5 ABI-derived selectors, all present verbatim.
- Replication leg (RV-2): `Rv2Token` runtime.bin `c1081a56…` / runtime.hex
  `d7f73058…`, expected set `45752a78…`.
- KdkToken leg (EX-03 → VZ-1): `EX-03/token.sol` `497d70f2…`, K=9
  (VZ-1 compiled + probed; `VZ-1/ex03-kdktoken-expected.txt` `ad816bfd…`).
- Compile environment pinned: `EX-05/versions.txt` `9a534576…` (rea-agents 6.7.0
  and 6.4.0; node v26.12.0; positional-encoding usage line).

### R3/R4 — probe (raw | hex) on real solc bytecode

KdxToken K=6 selectors: `095ea7b3` approve, `18160ddd` totalSupply,
`23b872dd` transferFrom, `40c10f19` mint, `70a08231` balanceOf, `a9059cbb`
transfer. Every leg: `inspect_evm_interface`, provider `evmole-interface`
("REA EVM interface adapter", `evmole@0.9.3`), `dispatch:"abi"`, K/K recovered
(Kdx 6/6, Rv2 5/5, Kdk 9/9, Rv2Many 11/11 per VZ-1 verdict).
Subject pins: hex legs subject = `69a15782…` (the hex file), raw legs subject =
`9c40940e…` (the bin file), decoded-bytecode digest `9c40940e…` on all legs —
all recomputed by SC-1 from the files and read from the JSONs.
Identity observations (facts, not adjudication): rerun of the identical raw
invocation re-seals the same id `ev_4dd5ea20…`; the renamed-path leg (same
bytes) seals a different id `ev_b2937090…` with the same code digest.
Cross-pin: 6.4.0 and 6.7.0 legs agree (EX-06 `ev_ad8fb290…` vs `ev_56d89cb4…`;
RV-2 likewise). Cross-seat envelope identity: `CR-2/recheck-ok-disk-tmpdir.json`
`f2aec424…` is byte-identical (`cmp` exit 0) to RV-2's `probe-runtime-hex-6.4.0.json`.

### R5 — reconciliation (SC-1 independently recomputed every pin)

EX-07's verdict (`reconciliation.md` `162b20b7…`): **K/K = 6/6** across eleven
source-sets — M1 strict dispatch parse, M1 EQ-site loose parse, M2 pure-Python
keccak scan, ABI-derived set, planted list, and ten probe legs (EX-05 ×4,
EX-06 ×2, replays/renames) — `missing=[] extra=[]`, driver line
`VERDICT: ALL SOURCES AGREE` (`reconciliation-run-all-legs.txt` `a356c3a9…`,
SC-1 counted the line: 1 occurrence). Byte-offset agreement: probe
`bytecodeOffset` = M1 JUMPDEST targets (100/148/178/226/254/302), independently
confirming the r4 errata semantics. Rv2Token replication: 5/5 across five
sources, offsets equal.
SC-1 recompute table (all matched EX-07's cited values):
`EX-05/kdx-runtime.hex` `69a15782…`; `kdx-runtime.bin` `9c40940e…`;
`kdx-abi.json` `40ad881e…`; `planted-K.json` `063eb723…`;
`run-hex-6.7.0.json` `5188d59f…`; `run-raw-6.7.0.json` `b374ec27…`;
`kdx.hex.json` `93188f83…`; `kdx.raw.json` `f8be246a…`;
`kdx.raw.rerun.json` `a5d2e542…`; `kdx.raw.renamed.json` `e45d7778…`;
`target-KdxToken.runtime.{hex,bin}` same as EX-05's;
`selector-recon.py` `99c3c32d…` (matches the md).
**Catch:** the md self-cites `reconcile.py` `c1be2731…`; SC-1 measured
`647395a0…` on disk at 10:08Z (stale self-reference — the file was revised after
the md, or the md's value was wrong at write; CR-1 landed a wrap-fix patch for
this tool: `EX-07-reconcile-unwrap.patch.md` `f5e58cf6…`).
Independent corroboration: `EX-05/ex07-crosscheck.txt` `c695a93c…` (fourth-party
re-run of the extractor), `SC-2/` crosschecks and manifest snapshots
(`checkfile-run4` `0eb0dc75…`, `crosscheck-run3` `4c120e10…`, `crosscheck-run5`
`a62ea067…`, `manifest-crosscheck.md` `016d3f68…`), `RV-3/independent-verification.txt`
`e15c9212…`.
Command A runs (SC-1 ran the frozen recipe at `e845c2b`; = EX-11 `8787e0c4…` and
RV-4 `ad89810a…` line 1; VZ-1 E1 fifth capture — all identical): before-state
81/81, 13/13, missing [], dangling []. CR-2's three-run record
(`command-A-runs.txt` `2405729c…`): (1) HEAD 81/81; (2) scratch clone with the
EX-12 entry+token patch applied → **82/82, missing [], dangling []** (tree-level
after-state); (3) mismatch-name commit → `dangling:["2026-10-19-arc3-r1-evm-real-solc"]`,
`missing:["2026-10-19-arc3-r1-evm-solc"]`, coverage 9.88 (negative control: the
name coupling matters). Command A at the records commit: GAP (parent-side).

### R6 — control (all landed)

EX-07 controls (documented in `reconciliation.md`, artifacts present):
1. keccak independence: own impl vs js-sha3 7/7 (`keccak-vs-jssha3.txt`
   `169252c7…`), vectors PASS; EX-03's standalone `keccak256.py` `7a58534b…`
   is a third implementation (RV-1 recompute `745f85bb…`).
2. tamper control: byte flip → M1 reports the mutated selector, M2 drops to 5/6
   (byte-sensitive agreement, not parroting).
3. dispatch-less carrier `6001600101` → empty chain, no false positives
   (`EX-05/recon.out.json` `ev_bb3fd00f…` n=0; `recon.640.json` `ev_59fd4927…` n=0).
4. extra-PUSH4 in metadata trailer correctly excluded (Rv2Token).
5. creation-vs-runtime: creation blobs → `functions: []` (EX-05
   `kdx-creation.raw.json` `e6f1b60a…`; EX-06 `run-creation-hex.json`
   `38a05b85…`; RV-2 `probe-creation-hex-6.4.0.json` `95fea9be…`, smoke-bin
   `0097318d…`).
6. digest pins on all legs (SC-1 recomputed).
7. encoding-mismatch: hex-on-bin → typed refusal `invalid_request`/`invalid_input`
   (`kdx.hex-on-bin.json` `ab073b51…`) — fails closed.
EX-08 edge battery (`EX-08/probe-*` JSONs + `.exit` files; SC-1 decoded the exit
hashes: `9a271f2a…`=`0\n`, `4355a46b…`=`1\n`): current state elfmagic/empty/
nonbytecode hex+raw exit 0, missing-file exit 1; carriers `empty.bin`
`e3b0c442…` (0 B), `nonbytecode.bin` `a037bf6e…`; scripts `run-probes.sh`
`50c3d25b…`, `reconstruct.js` `ce947257…`. Note: exit files were revised
in-flight (1 → 0) during the wave window; ledger pins the 10:07Z state.
CR-1 battery: carrier variants (A/B/C/E2/E3, ascii-hex, big64, many-selector
opt0/opt1), fail cases, replay legs, `drift-solc-{6.4.0,6.5.0,6.7.0}.json`
(cross-version probe behavior), `evidence-manifest.sha256.txt` `5aa1aef0…`.
RV-2 attacks: `attack/tampered-digest.json` `b9c1af3a…`,
`tampered-drop-one.json` `e9bccfed…`, `planted-plus-bogus.txt` `2ff578a7…`.

### R7 — rerun (id stability)

EX-09 verdict (`rerun-compare.md` `846c9f78…`): the id **IS stable** across four
distinct runs (EX-05 ×2, EX-09 ×2) of the identical invocation; envelope
byte-identical (9935 B, EX-09 sha `729c4881…`), id `ev_4dd5ea20…`, id
independently re-derived from envelope bytes (RFC 8785 canonical JSON,
`subject.name`/`local_path` excluded); VZ-1 re-ran the reid derivation on six
envelopes — all MATCH (E4). SC-1 partial re-verification: `jq -c '.data'` over
`kdx.raw.json`, `kdx.raw.rerun.json`, `kdx-rerun-1.json`, `kdx-rerun-2.json`
yields the **same sha256 `0144b17d…`** on all four and 9935 bytes of envelope —
byte-identity of the envelope confirmed; EX-09's exact canonicalization hash
`729c4881…` is their projection (not re-derived here). Only cross-run diff is
`meta.duration` outside the envelope. RV-2's `rv2-rerun-kdx-{hex,raw}-6.7.0.json`
are byte-equal to EX-06's leg files (`5188d59f…`, `b374ec27…`).

### R8 — landing / close (GAP at capture)

- Drafts: `records-drafts/LOG-entry-draft.md` `2f33bb79…`,
  `SCORECARD-section-draft.md` `42359161…` (not applied — parent-owned).
- Knowledge entry (patch text, seat-forbidden surface): `EX-12/knowledge-entry.patch.md`
  `d662c195…` → `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md`; CR-1
  additions `d117fcfe…`.
- Map token: `EX-13/_scratch/map-token.patch` `ddfe0116…` (frozen by RV-4 as
  `RV-4/map-token.frozen.patch`, same bytes) + `EX-13/map-token.patch.md`
  `27d59a11…` + `verify-battery.py` `b57bbb86…`; `RV-4/README.after.md`
  `b74b8d34…`; verifier `RV-4/verify_map_token.py` `08e052c4…` with
  selftest-positive `5c6bfbc2…` / selftest-negative `4a8f8640…` and
  `final-artifact-verification.txt` `d172efb1…`.
- RV-4 `command-A-preview.txt` `ad89810a…`: line 1 = before-state (81/81, 13/13
  at `e845c2b`); line 2 = the token-only preview (knowledge_files 81, dangling
  `["2026-10-19-arc3-r1-evm-real-solc"]` at revision `295cd30a` — which does
  **not resolve in this repo**; SC-1 checked: `git rev-parse 295cd30a` → unknown
  revision). Useful negative control: token-without-file ⇒ dangling=1.
- Chain verdict: `VZ-1/verdict.md` `ccbad891…` — **C1 VERIFIED (wave-level)**
  with 5 named debts and 3 integration conditions; C1-f (command A 81→82) PASS
  at tree level; names the PL-1 plan's `evm-solc` spelling as stale (debt D4).
- Actual landing (knowledge file + README edit in the repo), command A at the
  records commit, custody post-pair: **GAP** (parent-side integration).

## Verification-hygiene observations (recorded, not adjudicated)

1. EX-14 `MANIFEST.draft.check.sha256` VOID (`e3b0c442…`); `verify.log`
   `9dabe4ec…` attempt 3 FAIL (`no properly formatted checksum lines found`);
   `MANIFEST.draft.txt` `57b0a875…` is a point-in-time draft (section 1 lists
   0 artifacts at generation). Regenerate after artifacts settle.
2. EX-08 landed two files at `claims/c1/` root instead of its seat dir:
   `EX-08-search.js` `d4a21a24…`, `EX-08-search2.js` `41b18592…`.
3. EX-13 `_scratch/applytest/` is a full scratch git tree (~400 files incl.
   `.git/`) inside the wave dir — scratch litter the parent should exclude
   from integration; `_scratch/map-token.patch` `ddfe0116…` and `patch.raw`
   `ec4ada8e…` are the real artifacts there.
4. `/tmp` usrquota EDQUOT (SC-1 reproduced; `mount | grep ' /tmp '` → `usrquota`;
   SC-1 tee failed 09:58Z). EX-05/EX-06/EX-09 relocated scratch to `/dev/shm`
   and `/var/tmp` (EX-09 records the deviation).
5. `reconcile.py` self-hash mismatch (R5 catch).
6. RV-4 preview revision `295cd30a` unresolvable locally (R8 note).
7. `claims/c1/verdict.md` (root) `5f4b76ef…` is a stale copy of VZ-1's verdict;
   VZ-1's own `VZ-1/verdict.md` was revised to `ccbad891…` (`cmp` differs at
   byte 13531, line 163) — the root copy must not be read as final.
8. `__pycache__` litter under `EX-03/` and `RV-1/` (compiled Python byproducts
   in seat dirs).

## Footer

- Snapshot command:
  `cd .ufo/waves/arc3-loop1-round1 && find claims/c1 seats -type f | sort | xargs sha256sum`
- Capture totals at 10:19Z: 414 files under `claims/c1/` (excluding
  `EX-13/_scratch/applytest` and `__pycache__`); 46 seat reports under `seats/`.
- Superseded by the parent's integration-time ledger at the records commit;
  every GAP above must be re-checked there, not assumed closed.
