# CR-3 — c2 chain (corpus Unknown): independent verification of EX-7's viaIR entry

Seat: CR-3 · chain c2 (`claims-frozen.md` roster: EX-5..EX-12, CR-1..CR-4) · 2026-10-19 · lane `kaidoku-shokunin`.
Target claim: **C2 — close one named corpus Unknown.** The delivered candidate is EX-7's viaIR dispatcher entry
(`claims/c2/EX-7.md` + `EX-7/entry-draft/2026-10-19-arc3-r6-viair-dispatch-shape.md`), which closes the Unknown named at
`corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:33` and `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:28`.
This seat re-derives every number first-hand (rule #14); no prior seat's value is quoted as evidence.

**Verdict: REPRODUCED.** The entry's central claims — 15/15 K/K on the viaIR carriers, the fourth compare-tree class
(inverted `ISZERO` guard + linear ascending EQ chain + `SUB` final leg), the offset convention, zero false positives,
the traps, the creation-embed and CBOR facts — all reproduce on freshly recompiled bytes and freshly sealed probes.
**Two entry wording corrections are required before landing** (C-1, C-2 below; exact patch in
`CR-3/evidence/entry-corrections.patch`), plus one custody-count correction in the seat report (C-3, not the entry).
With the entry + map token applied on a scratch clone, command A **measures 85/85** (not a projection; §8).

## 1. Re-derived items and verdicts

| # | item | verdict | first-hand evidence |
|---|---|---|---|
| 1 | Command A before-state at work commit `58c3db7` | **REPRODUCED** | `evidence/commandA-58c3db7.json` → `{"knowledge_files":84,"mapped":84,"missing":[],"dangling":[],"citation_resolved_rules":14,"rule_blocks":14,"coverage_score":10.0,"depth_score":10.0}` |
| 2 | Command A before-state at records commit `c625d5d` | **REPRODUCED** | `evidence/commandA-c625d5d.json` — identical counters (84/84, 14 rules) |
| 3 | The named Unknown is real and still open | **VERIFIED** | `grep -rn -i viair corpus/knowledge/ corpus/README.md` → exactly two hits, both Unknowns lists: r3 `:33` and r4 `:28`; no entry names a viaIR measurement |
| 4 | solc toolchain receipt | **REPRODUCED** | `node_modules/solc` at `.ufo/waves/arc3-loop1-round1/tools/solc-prefix/`; `node -e …version()` → `0.8.37+commit.f401782d.Emscripten.clang`; `soljson.js` `221d7a6673…abad4c`, `package.json` `b3a90035…33491` — equal to the r3 record |
| 5 | Source digest and three compile legs | **REPRODUCED byte-exactly** | fresh compile from `EX-7/src/ViaIrVault.sol` (`f5391167…80cbbe`, re-hashed) → opt200 runtime 1,517 B `2ec3f557…`, noopt 4,144 B `0cc6938c…`, control 1,921 B `c2ceabb1…`; creations 1,560 B `d85fdde9…`, 4,318 B `f1125049…`, 1,966 B `4541fd49…` — every digest equals EX-7's (`evidence/compile-independent-receipt.txt`) |
| 6 | ABI / method-identifier digests | **REPRODUCED** | all three legs: ABI `63fcf52f…` (17 entries = 15 functions + constructor + receive), `method-identifiers.json` `c32e2ef2…` (15 keys) |
| 7 | viaIR dispatcher class on opt200 | **REPRODUCED** | independent opcode walk (`evidence/walk-viair-opt200.json`): prologue `5f3560e01c` at pc 35; guard `6004 36 10 15 61<0022> 57` (`LT` + `ISZERO`); 14 EQ legs at pcs 41…184, strict 11-byte stride; selectors ascending; dsts `[982,935,771,723,694,631,572,485,425,374,340,311,272,253]`, all JUMPDESTs; SUB leg `ee02438e` at pc 194 → dst 14 |
| 8 | Fourth-class claim on noopt | **REPRODUCED for the compare tree; CORRECTED for the prologue** | noopt: 14 EQ legs (dsts 208–273, stride 11), same SUB leg at 194, same inverted guard — but **no `5f3560e01c` token anywhere** (`'5f3560e01c' in hex` → `False`); selector load is `5f 35 61<0116> 56` into helper `5b 60e0 1c 90 56` at 0x116 (§7 C-1) |
| 9 | Legacy control compiles the r3 class | **REPRODUCED** | std-opt200: guard `6004 36 10 61<00e7> 57` (no `ISZERO`); 15 EQ + 3 GT legs (GT pivots `6e69f38c` pc 19, `90ab171e` pc 30, `3f4ba83a` pc 137); the three pivots duplicate as EQ leaves; all EQ dsts JUMPDESTs (`evidence/walk-std-opt200.json`) |
| 10 | Sealed probes, K/K on every real leg | **REPRODUCED** | my own probes at `/var/tmp/cr03-r6`: opt200 hex `ev_fbf785fb…` 15/15, opt200 raw `ev_b281d1ea…` 15/15, 6.7.0 hex `ev_ff1f2cf8…` 15/15, noopt `ev_cd7893af…` 15/15, control `ev_e71143d2…` 15/15; all `dispatch:"abi"` ×15, decoded sha equals the runtime file sha (`evidence/probe-*.json`) |
| 11 | Probe payload identity vs EX-7's envelopes | **REPRODUCED** | selector/offset/dispatch/args/mutability tuples identical on all seven compared legs; only `ev_` ids differ, explained by the documented path domain (EX-7 ran from `/var/tmp/ex07-r6`; I ran from `/var/tmp/cr03-r6` / the repo path) — `evidence/payload-compare.txt` |
| 12 | Traps (raw-on-hextext, creation) | **REPRODUCED** | 0 functions; decoded sha = hex-text file sha `19838d66…` (`ev_2b1f3203…`) and creation sha `d85fdde9…` (`ev_0bc2b8af…`); parsed-and-empty, `corpus/QUALITY.md:21` citation correct |
| 13 | Creation embedding | **REPRODUCED** | runtime appears exactly once in 1,560 B creation at **+43**; `creation[43:43+1517]==runtime` true (`evidence/creation-embed.txt`) |
| 14 | CBOR trailer | **REPRODUCED** | tail decodes `a2 64 69706673 58 22 … 73 736f6c63 43 000825 00 33`; solc `0x000825` = 0.8.37 |
| 15 | Zero false positives / PUSH4 census | **REPRODUCED** | opt200: 19 PUSH4 sites, 18 distinct = 15 selectors + `4e487b71`×2 (pc 553, 1143) + `0c2eae8d` (1094) + `3c3332b9` (1261); none returned as functions. noopt 17/16; control 22/19 including CBOR `43000825` |
| 16 | Offset convention | **REPRODUCED** | 14/15 offsets = their EQ leg's `PUSH2` dst and land on JUMPDESTs; `mark` offset 204 = push4_pc (194) + 10, byte `0x34` (opt200) / `0x61` (noopt), **not** a PUSH2 target; 204 ∉ PUSH2 targets, 14 ∈ PUSH2 targets |
| 17 | Mutability delta | **REPRODUCED** | `inferred_state_mutability` vs ABI: 14/15 agree; `scale(uint256,uint256)` `6e69f38c` ABI `pure` → inferred `view`; no non-payable function reads payable (only `deposit` `d0e30db0`, ABI payable) |
| 18 | Selector derivations | **REPRODUCED** | independent `js-sha3` derivation of all 15 signatures matches `planted-K.json` exactly; 0 collisions against the 9 ERC-20 selectors (`evidence/selectors-and-abi.txt`) |
| 19 | Pre-compile fix is selector-neutral | **REPRODUCED** | `planted-K.preact.json` (pre-fix, 15:42Z) and `planted-K.json` (post-fix, 15:50Z): K=15 both, selector maps equal |
| 20 | The entry's own recheck command | **REPRODUCED** | run verbatim from repo root → 15 functions, `dispatch:"abi"`, decoded `2ec3f557…`; new id `ev_71da9d37…` minted at the recheck path (`evidence/recheck-entry-command.json`) — exactly what the entry says to expect |
| 21 | Landing move: entry + README token ⇒ 84 → 85 | **REPRODUCED (measured)** | scratch clone of `58c3db7` + entry + token = commit `91d8150`; command A → 85/85, missing/dangling `[]`, coverage 10.0, `rule_blocks` 14 (`evidence/commandA-after-scratch.json`, `evidence/landing-sim.diffstat.txt`) |
| 22 | Carrier function count in the entry | **CORRECTED** | source has **15** `function` declarations, ABI has 15 functions, dispatch has 14 EQ + 1 SUB = 15 selector legs; the draft's "14 explicit external functions + `receive()` = 15 dispatched entries" is a miscount (§7 C-2) |
| 23 | Other r1/r4 offset conventions ("r1 = PUSH1; r4 = push4_pc+11") | **NOT RE-DERIVED** | cited cross-corpus claims, outside this seat's target; not relied on by any verdict here |
| 24 | EX-7 seat report custody count | **CORRECTED** | `EX-7.md:62` says 42 files; actual count is 46 (src 1, scripts 5, evidence 8, out 24, probe 7, entry-draft 1). Bookkeeping only; no evidence file is missing |

## 2. Pre-state — measured, not quoted

Command A (SCORECARD.md:88-124) at both commits:

```
58c3db7: {"citation_resolved_rules":14,"coverage_score":10.0,"dangling":[],"depth_score":10.0,
          "knowledge_files":84,"mapped":84,"missing":[],"revision":"58c3db7","rule_blocks":14}
c625d5d: {"citation_resolved_rules":14,"coverage_score":10.0,"dangling":[],"depth_score":10.0,
          "knowledge_files":84,"mapped":84,"missing":[],"revision":"c625d5d","rule_blocks":14}
```

The Unknown is still open at HEAD: `grep -rn -i viair corpus/knowledge/` returns r3`:33` and r4`:28` only, both as
Unknowns. The entry would be the first corpus measurement of the pipeline.

## 3. Independent compile — fresh bytes, all digests equal

I did not reuse EX-7's `out/` bytes. I copied only `src/ViaIrVault.sol` (sha `f5391167…80cbbe`) into
`/var/tmp/cr03-r6`, compiled it with the receipted solc 0.8.37 and my own standard-JSON settings, and compared:

| leg | settings | runtime | sha256 | creation |
|---|---|---|---|---|
| viair-opt200 | `viaIR:true`, optimizer 200 | 1,517 B | `2ec3f557f6f2…9581a` | 1,560 B `d85fdde9…d83d5` |
| viair-noopt | `viaIR:true`, optimizer off | 4,144 B | `0cc6938cd768…d29b4` | 4,318 B `f1125049…54063` |
| std-opt200 | `viaIR` unset, optimizer 200 | 1,921 B | `c2ceabb163ad…3f7e27` | 1,966 B `4541fd49…c5d9e` |

All six digests match `EX-7/evidence/manifest.sha256` and the compile receipt; `ABI` `63fcf52f…` and
`method-identifiers` `c32e2ef2…` are identical across the three legs. Receipt: `evidence/compile-independent-receipt.txt`.

## 4. Independent byte walk (no reuse of EX-7's walker)

I wrote a fresh opcode-aware disassembler (`walk.py`, push width = `op - 0x5f`) and re-derived the structure from my
own compiled runtime bytes. Key measurements (`evidence/dispatcher-walk-summary.txt`, raw JSON `walk-*.json`):

- opt200: `5f3560e01c` at pc 35; guard `PUSH1 4; CALLDATASIZE; LT; ISZERO; PUSH2 0x0022; JUMPI`; 14 EQ sites at pcs
  41,52,…,184 (all gaps 11); selectors ascending; 14 dsts `982,935,771,723,694,631,572,485,425,374,340,311,272,253`,
  every one a JUMPDEST; SUB leg `PUSH4 ee02438e; SUB; PUSH2 0x000e; JUMPI` at pc 194; fall-through at 204 is
  `CALLVALUE; PUSH2 0x00f9; JUMPI`.
- noopt: same guard shape (`… ISZERO; PUSH2 0x001d; JUMPI`), same 14 EQ legs (dsts 208–273) and same SUB leg at 194,
  but selector load is deferred: `PUSH2 0x0027; PUSH0; CALLDATALOAD; PUSH2 0x0116; JUMP` and the shared helper at
  `0x116` is `JUMPDEST; PUSH1 0xe0; SHR; SWAP1; JUMP`. The runtime contains **zero** `5f3560e01c` tokens.
- std control: `5f3560e01c` at pc 13 preceded by the bare-`LT` guard; 15 EQ legs + 3 GT pivots (pcs 19/30/137); three
  selectors appear twice and are deduplicated by the extractor.

The class is still the fourth class EX-7 names — the compare tree is the identifier. The only correction is the
prologue wording (§7).

## 5. Independent sealed probes — my ids, same payload

I recompiled the carriers and probed my own files under `TMPDIR=/var/tmp/cr03-r6/tmp` (never `/tmp`). All seven probes
exited 0; the five real legs return 15 functions, `dispatch:"abi"` ×15, decoded sha = runtime file sha. Payloads are
tuple-identical to EX-7's envelopes; ids differ because the subject paths differ (EX-7 `/var/tmp/ex07-r6`, CR-3
`/var/tmp/cr03-r6`) — consistent with the path-domain statement both artifacts make. Full table:
`evidence/payload-compare.txt`; envelopes `evidence/probe-*.json`.

The entry's own recheck command, run verbatim from the repo root, also returns 15/15 and decoded `2ec3f557…`
(`evidence/recheck-entry-command.json`).

## 6. Entry claims that were checked and hold

Beyond the table above: ABI mutability census view ×7 / pure ×1 / nonpayable ×6 / payable ×1 + payable `receive`;
ERC-20 absence (my derivation, 0 collisions); `mark` offset 204 is not a JUMPDEST and not a PUSH2 target; the control's
GT pivots at pcs 19/30/137; `4e487b71`×2 + `0c2eae8d` + `3c3332b9` at pcs 553/1143/1094/1261; metadata trailer; the
+43 creation embed; and the two traps. The only numbers that do **not** hold are the function-count phrase and the
blanket prologue phrasing (§7).

## 7. Corrections (required before landing)

### C-1 — `viair-noopt` has no `5f3560e01c` prologue

Draft line 22 says the viaIR runtime opens with the shared `5f3560e01c` prologue, then "The same shape holds in
viair-noopt". The compare tree does hold, but the prologue does not: `viair-noopt` contains no `5f3560e01c` token.
It enters the chain at pc 39 via `5f 35 61<0116> 56` and jumps to a shared helper at `0x116`
(`5b 60e0 1c 90 56` = `JUMPDEST; PUSH1 0xe0; SHR; SWAP1; JUMP`). The class is identified by the compare tree, not
the inline prologue — which is the entry's own conclusion, so this is a precision fix, not a reopening.

Proposed replacement (in `evidence/entry-corrections.patch`):
- "the viaIR runtime opens" → "the viair-opt200 runtime opens";
- after "The same shape holds in viair-noopt …" add: "but with a different prologue form: the noopt runtime contains
  **no `5f3560e01c` token** — it enters the chain at 39 via `5f 35 61<0116> 56` … The class signature is therefore the
  compare tree …, not the inline prologue form."

### C-2 — 15 explicit externals, not 14

Draft line 16 (and `EX-7/src/ViaIrVault.sol:5`, and `EX-7.md:20`) say "14 explicit external functions + `receive()` =
15 dispatched entries". First-hand: `grep -c '^    function ' src/ViaIrVault.sol` → 15; ABI functions → 15; dispatch
selector legs → 14 EQ + 1 SUB = 15. The correct statement is 15 explicit externals (15 selectors) + `receive()`;
ABI 17 = 15 functions + constructor + receive. The error is self-contradictory with the entry's own ABI count and
does not affect K/K (the planted set is 15 and all 15 are recovered). The source file is pinned by sha and should not
be edited; the entry prose should carry the corrected count.

### C-3 — custody count in the seat report (not the entry)

`EX-7.md:62` says 42 files; actual = 46 (§1 row 24). No missing evidence.

## 8. Landing simulation — measured 85/85

I cloned the lane to `/var/tmp/cr03-r6/clone`, checked out the work commit `58c3db7`, copied the entry draft to
`corpus/knowledge/2026-10-19-arc3-r6-viair-dispatch-shape.md`, appended the token to the EVM row of
`corpus/README.md` (the patch text is exactly EX-7's), and committed as `91d8150`. Command A on that commit:

```
{"citation_resolved_rules":14,"coverage_score":10.0,"dangling":[],"depth_score":10.0,
 "knowledge_files":85,"mapped":85,"missing":[],"revision":"91d8150","rule_blocks":14}
```

The diff is exactly two files (`corpus/README.md` +1 token, the new entry) — `evidence/landing-sim.diffstat.txt`,
`evidence/landing-sim-readme.diff.txt`, `evidence/commandA-after-scratch.json`. This is a measurement on a scratch
tree, not a projection; the real repo is untouched.

## 9. Supplement (CR-3 only, not part of EX-7's entry): solc 0.8.28 under viaIR

EX-7's Unknowns include "solc versions other than 0.8.37 under viaIR". I compiled the same source with
`solc@0.8.28+commit.7893614a` (fresh scratch npm install, `soljson.js` `9ef37cc1…1970`) under `viaIR:true` + optimizer
200:

- runtime 1,517 B `3f28f35e…f07967`; creation 1,560 B `e25a5142…9c38f3`;
- **executable code (bytes 0..1463) is byte-identical to the 0.8.37 runtime**; only the 51-byte CBOR metadata differs
  (`solc` `0x00081c` vs `0x000825`, and the ipfs digest);
- REA 6.4.0 probe: 15/15, `dispatch:"abi"` ×15, offsets identical (`982…253,204`) — `ev_3921486e…`.

This narrows (does not fully close) the version Unknown: the dispatcher class and codegen for this carrier family are
stable across 0.8.28/0.8.37. Evidence: `evidence/solc0828-supplement.txt`, `evidence/compile-0.8.28-receipt.txt`,
`evidence/probe-viair-opt200-solc0828-6.4.0.json`, `evidence/walk-2828.json`. If the parent wants this in the entry,
the entry's Unknowns/scope sentence must be amended; otherwise it stands as a seat-level supplement.

## 10. Custody, limits, recommendation

- **Recommendation:** land the entry and the README token after applying C-1 and C-2 (or equivalent wording).
  Re-run command A on the post-landing commit; expected and simulated: 85/85, missing `[]`, dangling `[]`,
  `rule_blocks` 14. C-3 is a seat-report bookkeeping fix only.
- **Custody:** all my evidence is under `claims/c2/CR-3/evidence/` (33 files + `manifest.sha256`). Scratch:
  `/var/tmp/cr03-r6/` and `/var/tmp/r6-recheck` for the entry's recheck command; no `/tmp` use. Custody reads only:
  EX-7 tree, r1 solc prefix, corpus entries, SCORECARD. No tracked file modified; `git status` remains
  `M .ufo/waves/arc2-loop1-round10/C3.md` + untracked `arc3-loop1-round6/`.
- **Limits:** one carrier family, one source; primary pins 6.4.0 (all legs) + 6.7.0 (opt200 hex only); the 0.8.28
  supplement is one older version, opt200 only; `ev_` ids are path-scoped and are not cross-seat comparable — compare
  by decoded `bytecode.sha256` + function payload (QUALITY.md row 15). The r1/r4 offset conventions cited by the entry
  were not re-derived here.
