# C1 verdict — convergence reconciliation (SEAT VZ-1, chain c1)

Wave `arc3-loop1-round1`, 2026-10-19. Reconciled from `seats/` + `claims/c1/` at
07:41-03 (10:41Z); HEAD `e845c2b524ad2e59871e004c51a1386e192a74ab` throughout
(`git rev-parse HEAD`, re-checked at every sample). Polling: my own 60 s loop, 14+
checks 06:57→07:33, plus targeted re-lists; no seat blocked on me and I blocked on
none.

## VERDICT: C1 **VERIFIED** — wave-level, with 5 named debts and 3 integration
## conditions. NOT-VERIFIED would be wrong: every falsifiable component of the
## frozen claim (`claims-frozen.md:14-38`) has first-hand or independently
## recomputed evidence. What is NOT yet measurable is command A **at the records
## commit**, because that commit does not exist until the parent integrates; the
## predicate is proven at tree level instead (E7).

### Why VERIFIED (claim component → evidence)

| # | Claim component (`claims-frozen.md`) | Verdict | Evidence (recomputed by VZ-1 unless noted) |
|---|---|---|---|
| C1-a | npm `solc` install receipt (name, version, sha256) | PASS | `solc@0.8.37`, tarball sha256 `0e1a1ab6…575a51` (`claims/c1/EX-02/install-receipt.txt`, patch text `claims/c1/EX-02/proposed-receipts-solc-install.patch.md`); I re-hashed the installed tree myself: `node_modules/solc/soljson.js` `221d7a66…abad4c`, `solc/package.json` `b3a90035…3491` — identical to EX-02's receipt and to RV-3's independent capture |
| C1-b | real contract compiled on-host, planted K recorded pre-probe | PASS | four on-host solc-0.8.37 compiles: `Smoke` K=5 (`EX-02/smoke/`), `Rv2Token` K=5 (`RV-2/`, runtime 1943 B `c1081a56…`), `KdxToken` K=6 (`EX-04`/`EX-05`/`EX-06`, runtime 1789 B `9c40940e…`), `KdkToken` K=9 (EX-03's `token.sol`, compiled + probed by this seat, §E6). Compiler provenance is on-bytecode: every probed runtime carries the solc CBOR trailer `736f6c6343 000825` = 0.8.37 (`normalized_result`/`raw_result.metadata`) |
| C1-c | probe recovers K/K selectors | PASS | Rv2Token 5/5 (`ev_45849c8b…` hex, `ev_3aacd424…` raw, `ev_19d7d3cb…` @6.7.0), KdxToken 6/6 (`ev_56d89cb4…` hex, `ev_9259f412…` raw), Rv2Many 11/11 (`ev_d0d0b054…`), KdkToken 9/9 (`ev_92b7e2fc…`, this seat). Zero missing, zero extra in every set. I recomputed the selector sets from the compiled ABIs with keccak-256 (js-sha3) and matched each recovered set byte-for-byte; each selector occurs exactly once as a PUSH4 dispatch immediate in its carrier |
| C1-d | `dispatch:"abi"` (frozen prediction) | PASS | every recovered function in every runtime leg carries `dispatch:"abi"` (checked in all 7 envelopes I parsed) |
| C1-e | knowledge entry + map token landed (patch text) | PASS (patch) | `claims/c1/EX-12/knowledge-entry.patch.md` → `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md`; `claims/c1/EX-13/_scratch/map-token.patch` (frozen byte-copy `claims/c1/RV-4/map-token.frozen.patch`, sha256 `ddfe0116…`) → `corpus/README.md:38`; **stems agree** (the PL-1 plan's `evm-solc` spelling is stale — debt D4) |
| C1-f | command A 81 → 82, prior 81 byte-identical, rules 13/13 | PASS (tree-level) | E7 below |
| C1-g | no config.toml drift (frozen prediction) | PASS | I re-captured the 5 custody paths myself at ~07:10-03: all five sha256 equal CU-1's pre-pair (`claims/cross/receipts/config-pre-pair.txt`, capture 09:57:18Z), including `config.toml` `8cbacd48…c38d`; EX-01 corroborated 5/5 with three hash implementations; EX-02 pre/post install diff empty; EX-10 stanza-scope capture |
| C1-h | encoding legs both verified (`raw|hex`, positional) | PASS | raw and hex legs of the same carrier agree on the selector payload and on the **decoded bytecode** sha (`raw` file sha == decoded sha); positional-arg quirk retained in the entry |
| C1-i | honest-stop branches not needed | PASS | no typed refusal on real runtime bytecode; creation-code legs returned parsed-and-empty (debt D2) |

### First-hand measurements by this seat (E-numbers used above)

- **E1 (before-state).** Recipe A verbatim (`SCORECARD.md:92-124`) at `e845c2b`:
  `{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [],
  "depth_score": 10.0, "knowledge_files": 81, "mapped": 81, "missing": [],
  "rule_blocks": 13}`. Matches EX-11's landed artifact, RV-3, SC-2, PL-1 — five
  independent captures, identical.
- **E2 (keccak recompute).** js-sha3 from the wave prefix: 5/5 Smoke, 5/5 Rv2Token,
  9/9 KdkToken signatures → selectors; every selector found exactly once as a
  `PUSH4` immediate in the corresponding compiled artifact.
- **E3 (envelope audit).** Parsed all `claims/c1/RV-2/probe-*.json` +
  `EX-06/evidence/run-*.json`: selector sets, `dispatch`, `arguments`,
  `stateMutability`, `subject.digest.sha256`, `normalized_result.bytecode.sha256`,
  `provider` (`evmole@0.9.3`), limitations. `rerun-a` ≡ `rerun-b` byte-identical
  (same id); 6.4.0 ≡ 6.7.0 on payload.
- **E4 (id re-derivation).** `claims/c1/EX-09/reid.py` (id = `ev_` + sha256 over
  RFC 8785 canonical JSON of the semantic projection) run by me on 6 envelopes:
  all 6 MATCH, incl. `ev_45849c8b…`, `ev_3aacd424…`, `ev_d0d0b054…`,
  `ev_56d89cb4…`, `ev_c80379e1…`. Envelopes are self-consistent, not transcribed.
- **E5 (custody).** 5/5 sha256 equal to CU-1 pre-pair at ~07:10-03 (no drift).
- **E6 (closing RV-1's gap).** EX-03 landed only `token.sol` (07:11, after RV-1's
  polls closed). I compiled it myself (wave solc, `/dev/shm/vz1/ex03`): KdkToken
  runtime 3457 B `46ccaae1554a9b88…`, hex carrier `eca34f8b…`; ABI-derived K=9;
  probe (`rea-agents@6.7.0`, `TMPDIR` disk-backed) → `ev_92b7e2fc1dbccd5e…`,
  **9/9 recovered, `dispatch:"abi"` on all nine**, inferred arguments equal to the
  ABI's parameter types, decoded sha == my `runtime.bin` sha. Envelope retained at
  `claims/c1/VZ-1/ex03-kdktoken-probe.json`; expected set at
  `claims/c1/VZ-1/ex03-kdktoken-expected.txt`. **Disclosure:** this seat minted one
  new evidence id (`ev_92b7e2fc…`) in the REA store; no repo file outside
  `claims/c1/VZ-1/` and `seats/VZ-1.md` was written.
- **E7 (after-state, tree-level).** `git archive HEAD corpus/knowledge corpus/README.md
  SKILL.md` → fresh scratch repo (`/dev/shm/vz1/after`), commit `f11b03de…`
  (recipe A → 81/81, 13/13) → `git apply` EX-12's diff → commit `03a263be…` →
  recipe A: `{"knowledge_files": 82, "mapped": 82, "missing": [], "dangling": [],
  "citation_resolved_rules": 13, "rule_blocks": 13}`; `git diff --name-only`
  = exactly `corpus/README.md` + `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md`.
  Run **twice, on two different revisions of the patch** (EX-12 revised the
  artifact mid-wave):
  - rev A (diff block sha256 `4b569fb4…`) → entry 8316 B / 31 lines /
    `f95c5a05f0500ab9…` (copy: `claims/c1/VZ-1/applied-entry-copy.md`), 82/82;
  - rev B (current at 07:15, `knowledge-entry.patch.md` sha256 `d662c195…`,
    mtime 07:14:01, diff block sha256 `1bd7d54c…`) → entry 9513 B / 32 lines /
    `a5119120ee6a6142b8be6e297e39c85e0464fb27761c6ee0e7cc7cf8a1d5e56b`, 82/82,
    13/13, same two touched paths.
  Both revisions prove the after-predicate *and* the "prior 81 byte-identical"
  half (only one file added, none modified) without touching the lane repo.
  Consequence: the entry's identity claim in EX-12's step 4 is **stale for the
  current revision** (debt D9; CR-2's F2, independently confirmed here).
- **E8 (citation resolution).** Every `claims/c1/...`, `corpus/...`, `tools/...`
  path cited by the entry resolves to a landed file (only the not-yet-landed
  target entry is absent, as expected pre-integration).
- **E9 (map token).** RV-4's harness + EX-13's own three-variant verification:
  line-neutral 190→190, token multiset 81→82 unique, prior tokens byte-identical,
  `git apply --check` exit 0; the frozen variant is the one whose token matches
  EX-12's file stem (EX-13's `h3`, result sha `b74b8d34…`).

### Reviewer/executor verdicts reconciled (all read first-hand)

| Seat | Verdict as landed | Consistent with my recomputation? |
|---|---|---|
| EX-11 | before-state 81/81/13-13 | yes (E1) |
| EX-01 | custody pre-pair corroboration 5/5 | yes (E5) |
| EX-02 | install + smoke compile + receipt patch | yes (C1-a/b) |
| EX-04 | KdxToken compile (source+carriers+ABI) | yes (hashes match EX-05/EX-06/RV-1) |
| EX-05 | KdxToken hex/raw legs 6/6 | yes (E3) |
| EX-06 | KdxToken legs 6/6 + planted-K pre-probe | yes (E3) |
| EX-07 | 3-way reconciliation: ALL SOURCES AGREE; offsets = JUMPDEST dests | yes (E3/E4) |
| EX-08 | controls (empty/nonbytecode fail-closed) | not re-run by me; artifacts present |
| EX-09 | id stability across 4 runs, byte-identical envelope; id re-derived | yes (E4, using their tool) |
| EX-10 | `[mcp_servers.rea]` pin 6.7.0, no drift | yes (E5) |
| EX-12 | entry patch text, after-state 82/82 | yes (E7) |
| EX-13 | map-token variants h1/h2/h3, line-neutral | yes (E9) |
| RV-1 | 3 landed planted sets MATCH under from-spec keccak | yes (E2) |
| RV-2 | K/K CONFIRMED 6/6, ids reproduce, EX-07 confirmed | yes (E3/E4) |
| RV-3 | ground-truth checks + grading method; smoke bin `530efc7b…` | yes (E2) |
| RV-4 | map-token PASS (line-neutral) | yes (E9) |
| SC-2 | manifest cross-check (109-110/116 rows reproduce) | not re-run by me |
| SC-3 | LOG/SCORECARD drafts (FILL-marked, not applied) | shape only, consistent |

## Named debts (all survive the VERIFIED verdict)

- **D1 — EX-03 did not deliver its task.** Dir empty until 07:11 (only `token.sol`,
  no compile receipt, no carriers, no report); RV-1 documented 16+ polls. The
  compile work is covered by EX-04/EX-05/EX-06 on a *different* contract
  (`KdxToken`); `token.sol` (`KdkToken`) was never compiled or probed by its owner.
  I closed the probe gap (E6, 9/9) but the seat-level delivery gap stands.
- **D2 — creation-code legs return 0 functions** (`ev_c80379e1…`,
  `ev_f875e21e…`, `kind:"unknown"`). The K/K recovery is a **runtime-carrier**
  result. The entry states this honestly; no Core promotion. Carried as scope.
- **D3 — CR-1 and CR-2 produced artifacts but no seat reports at this close.**
  The frozen plan's named attacks (plan.md:324): (a) selectors-from-a-table →
  mutation control, (b) hand-edited carriers → CBOR metadata, (c) re-run dressed
  as a move. State at 07:15: CR-2 landed a substantive critic bundle
  (`proposed-fixes.patch.md`, `entry-version-diff.txt`, three recheck envelopes,
  `command-A-runs.txt` incl. the deliberate name-mismatch negative:
  `001487c` → 82 files vs 81 mapped, `missing:["…evm-solc"]`,
  `dangling:["…evm-real-solc"]` — exactly the failure mode D4 warned about);
  CR-1 landed a 60+-file evidence dir + manifest. **Neither seat's report is
  written**, so their verdicts are not yet reconcilable — read the artifacts.
  (b) is answered on-bytecode (CBOR `solc:000825` + `ipfs` in every envelope);
  (a)/(c) partially (RV-2's `Rv2Many` 11/11 attack carrier; the entry's
  real-signal delta vs r3-07's stub `pure`/empty args).
- **D4 — entry-name divergence in the plan text.** `PL-1/plan.md:273,292,364`
  says `2026-10-19-arc3-r1-evm-solc`; every landed artifact (EX-12, EX-13, RV-3,
  RV-4, SC-3) uses `2026-10-19-arc3-r1-evm-real-solc`. Resolved in the artifacts;
  the plan text is stale and would mislead an integrator who reads only the plan.
- **D5 — RV-1's report conflates carrier vs decoded-bytecode digests.** Its table
  (`seats/RV-1.md:45`) lists `Smoke_sol_Smoke.bin 685 B, sha256 08299f31…` — the
  685 B / `08299f31…` pair is the *decoded bytecode*; the carrier file is 1370 B /
  `530efc7b…` (confirmed by me, RV-3, and RV-2's envelope). Labeling defect only;
  the envelope's own limitations call the distinction out.
- **D6 — SC-1 did not deliver** (planned: independent re-run of S4+S6). Partially
  covered by SC-2 and the RV seats.
- **D7 — /tmp is quota-exhausted fleet-wide** (EDQUOT; my own first scratch write
  failed). Probes need a disk-backed `TMPDIR` (PL-1 F4/F5). Environmental, named
  for the round record; my scratch moved to `/dev/shm/vz1` and is cleaned.
- **D8 — minor hygiene.** `claims/c1/EX-08-search.js` / `EX-08-search2.js` sit at
  the chain root instead of `claims/c1/EX-08/`; PL-1's plan says "QUALITY.md's 16
  criteria" where the file has 15 + 6 weak-material signals (RV-3 counted).
- **D9 — the entry patch was revised mid-wave and its self-verification block is
  stale (REQUIRED FIX before landing).** Three different applied identities were
  observed within ~20 minutes: 8,598 B (CR-2, `claims/c1/CR-2/entry-file-identity.txt`),
  8,316 B (`f95c5a05…`, my rev-A apply, = EX-12's own claimed hash), and
  9,513 B / 32 lines (`a5119120…`, the current rev-B patch sha256 `d662c195…`).
  EX-12's "Verification performed" step 4 still claims 8,316 B / `f95c5a05…`, and
  its `recheck:` line (line 33 of the artifact) still begins `cd /tmp`, which
  **fails on this host with a typed `execution_failure` (EDQUOT, errno -122)**
  — measured by CR-2 three ways (`claims/c1/CR-2/recheck-fail-cdtmp.json`,
  `recheck-fail-root.json`) and passing only with a disk-backed `TMPDIR`
  (`recheck-ok-disk-tmpdir.json`). Integrator: land the current revision, fix the
  `recheck:` line per CR-2's `proposed-fixes.patch.md` F1, and record the **fresh**
  hash of the landed bytes instead of the stale claim. Also carried: CR-2's F3 —
  r3-07's "`kind` needs richer bytecode to engage" hypothesis is refuted (kind
  stayed `unknown` on every real-solc leg) — and CR-2's F4, a **scope-language**
  gap: the edited EVM map row's state cell still reads "held — EVMole selectors
  recovered from synthetic dispatcher", which after the token append understates
  the row (the synthetic-dispatch clause is now one of two carriers). Land a
  one-phrase state-cell refresh or accept the understatement explicitly.

## Integration conditions (must hold or C1's after-state breaks)

1. **Apply hunk B once, not twice.** EX-12's patch carries the same README hunk as
   EX-13's map-token patch (EX-12 says so explicitly). Applying both will fail or
   double-insert; land `corpus/README.md:38` from exactly one of them.
2. **Prefer the frozen map-token artifact.** EX-13's formal
   `claims/c1/EX-13/map-token.patch.md` landed at 07:13 (and
   `map-token.primary.patch`, `map-token.alt-prose.patch`); the byte-identical
   copy RV-4 froze at `claims/c1/RV-4/map-token.frozen.patch` (sha256 `ddfe0116…`)
   is the one RV-4 verified PASS. Use one, not both — they are the same edit.
3. **Land the current revision of the entry** (sha256 `d662c195…` at 07:15) and
   apply CR-2's F1 fix to the `recheck:` line; then record the landed bytes' hash.
4. **Re-run command A at the records commit** (EX-15 owns `command-a-after.txt`)
   and require 82/82, missing [], dangling [], 13/13. Tree-level proof is E7 (two
   patch revisions); the commit-level number is still owed by the round's records.

## Attack log (what I tried to refute, and the outcome)

- *"The probe output was transcribed, not produced."* Refuted: 6/6 ids re-derive
  from envelope bytes under the pinned package's own id function (E4).
- *"The selectors were copied from a planted table."* Refuted for the carriers I
  checked: my independent keccak recompute from the ABI + PUSH4 scan reproduces
  every set (E2/E6); EX-07's disassembler reaches the same sets from bytes.
- *"The carriers are hand-assembled, not compiler output."* Refuted on-bytecode:
  solc CBOR trailer with `000825` + ipfs multihash in every probed runtime
  (E3/E6); RV-1 independently recomputed EX-06's CBOR slice.
- *"The after-state is asserted, not measured."* Refuted by E7 (fresh tree,
  independent apply, 82/82).
- *"The map token breaks line-neutrality."* Refuted: 190→190, single-line diff,
  prior tokens byte-identical (E9).
- *"The entry's citations drift."* Checked: all cited paths resolve (E8). But
  *"the entry's own identity claim is current"* — **sustained**: the patch was
  revised after hashing, so its step-4 hash/size no longer describes the current
  artifact (D9). The claim components are unaffected; the verification block is.
- *"EX-03's contract was never actually a real compile."* Attempted to sustain;
  refuted by doing the work: compiled + probed 9/9 with compiler metadata (E6).
- *"Seat reports overstate their evidence."* Partially sustained twice: RV-1's
  digest labeling (D5) and PL-1's entry-name/QUALITY-count drift (D4/D8) — neither
  changes a claim component.
