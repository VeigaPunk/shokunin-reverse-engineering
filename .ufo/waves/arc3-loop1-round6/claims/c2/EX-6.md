# EX-6 — c2 chain (independent verification of EX-7's viaIR entry) — arc3-loop1-round6

Seat: EX-6 · chain c2 (corpus Unknown) · 2026-10-19 · lane `kaidoku-shokunin` · dispatch provider `opencode-go-7/deepseek-v4.1-flash` (per `claims-frozen.md`; the seat's job is verification, not a fourth Unknown claim).
Target: **C2 — close one named corpus Unknown.** EX-7 delivered the `viaIR` dispatcher entry; this seat re-derived every number first-hand (SKILL.md rule #14) rather than quoting it, and adjudicates the draft item by item.

**Verdict in one line: the substance of EX-7's entry REPRODUCES (carriers byte-identical, K/K on every leg, dispatcher class verified on a second independent carrier family); four prose/citation defects must be fixed before landing, none of which change command A.** The landing move projects 85/85 exactly as claimed (measured on a scratch overlay, not quoted).

## 0. What was re-derived first-hand (nothing quoted from EX-7 or prior rounds)

| item | verdict | first-hand evidence |
|---|---|---|
| Command A at work commit `58c3db7` | **REPRODUCED** | ran the `SCORECARD.md:88-124` recipe → `{"citation_resolved_rules":14,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":84,"mapped":84,"missing":[],"rule_blocks":14}` (`verify/commandA-58c3db7.json`) |
| Command A at records commit `c625d5d` | **REPRODUCED** | same recipe → identical 84/84, 14 rules (`verify/commandA-c625d5d.json`) |
| The Unknown is real and open at HEAD | **VERIFIED** | `grep -n -i viaIR corpus/knowledge/*.md` → exactly two hits, both Unknowns bullets: `corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:33` and `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:28`; no pre-existing entry measures the pipeline |
| solc toolchain | **REPRODUCED** | `node -e "require('<prefix>/node_modules/solc').version()"` → `0.8.37+commit.f401782d.Emscripten.clang`; prefix reused read-only from `.ufo/waves/arc3-loop1-round1/tools/solc-prefix/` |
| REA pins | **VERIFIED** | ran the cached `rea-agents@6.4.0` (`~/.npm/_npx/dea9475797100b20/…`) on all primary legs/traps and `rea-agents@6.7.0` (`…/9b9809298fe40d2c/…`) on the viaIR hex; every envelope reports `evmole@0.9.3` |
| HEAD/work commits | **REPRODUCED** | `git log --oneline -2` → `c625d5d` (records) / `58c3db7` (work) |
| Wave tree state | **VERIFIED** | at start `.ufo/waves/arc3-loop1-round6/` held `claims-frozen.md` + the delivered claim files (PL-4/PL-2/RV-3/EX-7/SC-3/RV-7/VZ-4); my writes are confined to `claims/c2/EX-6/` |

## 1. Independent rebuild (my own compile script, not EX-7's)

Source `ViaIrVault.sol` copied read-only from `EX-7/src/` (sha256 `f5391167…80cbbe`, re-hashed). Compiled with my own `verify/scripts/compile3.js` (three legs; same standard-JSON settings as the entry) → **byte-identical outputs**:

| leg | runtime | creation | ABI | method ids |
|---|---|---|---|---|
| `viair-opt200` (viaIR + opt200) | **1,517 B** `2ec3f557f6f2fb229dc49094981723c6efcce3df10f20363ec1732845c99581a` | 1,560 B `d85fdde9…83d5` | `63fcf52f…5119` (17 entries) | `c32e2ef2…975c` (15 keys) |
| `viair-noopt` (viaIR + opt off) | **4,144 B** `0cc6938cd768199159cbed74a7e9f5bd4273c583afbf6babca643b0ffdbd29b4` | 4,318 B `f1125049…4063` | same | same |
| `std-opt200` (viaIR unset + opt200) | **1,921 B** `c2ceabb163ad9c1e6d88244c29c5187602eaf4c810029d0018e76eb9643f7e27` | 1,966 B `4541fd49…c5d9e` | same | same |

All six size/hash pairs in the entry reproduce exactly (`verify/receipts/repro-compile.txt`). The compiler is deterministic on this host, so this is a byte-level reproduction, not a re-synthesis.

Two **independent carriers** were then built to test whether the claimed dispatcher class is carrier-specific (source + full receipts under `verify/src/`, `verify/receipts/`):

- `RelayDesk` — 10 externals + `receive`, no fallback; viaIR opt200 runtime **936 B** `359d6172…f8c8`, legacy control 1,235 B `835cddbe…3101`.
- `RelayDeskFb` — same 10 externals + `receive` + a real `fallback(bytes)`; viaIR opt200 runtime **1,100 B** `b2678621…fb6d`, legacy control 1,412 B `ccd3d675…5446`.

## 2. Adjudication of EX-7's claims (per item)

Byte walks are my own linear-sweep decoder (`verify/scripts/walk.py`; PUSH immediates skipped, JUMPDEST set and PUSH2 target sets computed from the bytes). Walks retained under `verify/walks/`.

| # | EX-7 claim | verdict | my measurement |
|---|---|---|---|
| 1 | three carriers + ABI + method-ids reproduce | **REPRODUCED** | §1 table; all hashes equal |
| 2 | 15/15 on viair-opt200 hex/raw @6.4.0, hex @6.7.0, viair-noopt @6.4.0, std control @6.4.0 | **REPRODUCED** | my fresh envelopes: `ev_13139138…` (hex 6.4.0), `ev_23525e3d…` (raw), `ev_4418d9a4…` (6.7.0), `ev_bcdc973c…` (noopt), `ev_25fb2e00…` (control) — 15/15 each, `missing=[]`, `extra=[]`, `dispatch:"abi"` ×15, decoded sha == the leg's runtime file sha (`verify/probe/summary.json`) |
| 3 | `viaIR` guard is inverted vs legacy | **VERIFIED** | opt200 `[5:14]=600436101561002257`; noopt `600436101561001d57`; legacy `600436106100e757` — `ISZERO` present only under viaIR (`verify/bytes-facts.txt` §2) |
| 4 | 14 EQ legs, strict 11-byte stride, selectors ascending, all dst JUMPDESTs | **VERIFIED** | walk: `eq_count=14`, `eq_pc_gaps=[11]`, `eq_selectors_sorted_ascending=true`, `eq_dsts_all_jumpdest=true`, dsts 253/272/311/340/374/425/485/572/631/694/723/771/935/982; noopt dsts 208–273 |
| 5 | 15th leg is `PUSH4 ee02438e SUB PUSH2 0x000e JUMPI` (SUB, not EQ) | **VERIFIED** | bytes at pc 194: `63ee02438e0361000e57`; `SUB` (0x03) at pc 199; dst 14 = JUMPDEST |
| 6 | the SUB-leg reported offset is `push4_pc+10` = 204, not a JUMPDEST / PUSH2 target | **VERIFIED** | opt200/noopt byte[204] = `0x34` / `0x61`, `JUMPDEST=false`, `in_push2_targets=false`; the probe's 15th offset is 204 on both legs |
| 7 | legacy control compiles GT/EQ binary search instead | **VERIFIED** | `60043610 61<00e7> 57` (dst 231 = JUMPDEST); GT pivots at pcs 19/30/137 = `6e69f38c`/`90ab171e`/`3f4ba83a`; 15 EQ + 3 GT; the three pivots also appear as EQ leaves → 18 selector-ish sites, 15 distinct; probe offsets all 15 JUMPDESTs |
| 8 | 19 opcode-boundary PUSH4 sites, 4 non-selector constants at pcs 553/1094/1143/1261 | **VERIFIED** | `push4_total=19`; non-selectors exactly `4e487b71` ×2 (553, 1143), `0c2eae8d` (1094), `3c3332b9` (1261); noopt 17 (15 + panic ×2); control 22 (18 selector-ish + `3c3332b9`/`4e487b71`/`0c2eae8d`/CBOR `43000825`) |
| 9 | mutability: 14/15 exact, only `scale(uint256,uint256)` pure→view; 0 payable-reads | **REPRODUCED** | joined probe → solc `methodIdentifiers`/ABI: on viair-opt200, viair-noopt and the control the only divergence is `scale` (`view` inferred vs `pure` ABI); no non-payable function reads `payable` |
| 10 | raw-on-hex trap parsed-and-empty, decoded sha = hex file's sha | **REPRODUCED** | `ev_4393f6ef…`: exit 0, 0 functions, decoded `19838d6680f1…` = `runtime.hex` sha |
| 11 | creation probe parsed-and-empty; runtime embedded at +43 | **REPRODUCED** | `ev_560d3b92…`: 0 functions, decoded `d85fdde9…` = creation sha, 1,560 B; `creation[43:43+1517] == runtime`, and 43 is the **unique** embed offset |
| 12 | CBOR trailer `ipfs` + `solc 0x000825` | **VERIFIED** | tail from 1505: `5d64736f6c63430008250033`; ipfs marker at 1466, solc at 1507; standard `a2 64"ipfs" 58 22 <34 B multihash> 73"solc" 43 000825 00 33` |
| 13 | the extractor is not shape-blind to this class (r4 false-honest-stop hazard does not fire) | **VERIFIED** | 15/15 on both viaIR legs and 10/10 on both of my viaIR carriers (below), including the fallback-bearing one |
| 14 | entry's seven `ev_` ids belong to its seven envelopes | **VERIFIED (consistency only)** | `EX-7/probe/*.json` ids begin `ev_409e044…`, `ev_c55a152…`, `ev_285d13d…`, `ev_8ddef76…`, `ev_3b39013…`, `ev_2e7e40b…`, `ev_ff7ee75…` — matching the entry text; my runs mint different ids at different paths, which is the recorded path-sensitive id domain (r3:33/r4 and `corpus/QUALITY.md` #15), so the join is by decoded sha, as the entry itself says |
| 15 | projection `84 → 85`, `mapped 85`, `missing []`, `dangling []` | **REPRODUCED** | scratch overlay of `c625d5d` (`git archive`, no repo mutation) + entry copied into `corpus/knowledge/` + the exact map-token patch applied → `{"knowledge_files":85,"mapped":85,"missing":[],"dangling":[],"coverage_score":10.0,"rule_blocks":14}` (`verify/commandA-overlay-85.json`) |
| 16 | "fourth dispatcher class" / "fifth offset convention" as cross-round taxonomy | **NOT RE-MEASURED (out of this seat's scope)** | I did not re-run the r1/r3/r4 carriers. What I did verify first-hand is the *within-session* distinction: same source, same compiler, same optimizer, `viaIR` unset → GT/EQ binary search; `viaIR:true` → linear EQ chain + SUB leg. The taxonomy against r1/r3/r4 is left as the entry's cited claim |

## 3. Corrections required before landing (substance unaffected)

These are prose/citation defects in the draft; none changes a measured byte, a probe result, or command A.

**(a) "14 explicit external functions" is a miscount; the carrier has 15.**
The entry says: "Source `ViaIrVault.sol` sha256 `f5391167…80cbbe` (14 explicit external functions + `receive()`; ABI-verified mutability census: view ×7 / pure ×1 / nonpayable ×6 / payable `deposit` + payable `receive`; no ERC-20 surface)." The census in the same sentence sums to **15** functions (7+1+6+1), and the compiled ABI has **17 entries = 15 functions + 1 constructor + `receive`** (`{"function":15,"constructor":1,"receive":1}`; `n_functions=15`). The dispatch chain is 14 EQ + 1 SUB = **15 selector legs**, plus the zero-calldata `receive` path. Suggested text: "15 explicit external functions + `receive()`; the selector chain covers the 15 functions (14 EQ + 1 SUB), `receive` is the zero-calldata path." K=15 and 15/15 are correct as measured — only the word "14" is wrong.

**(b) "42 files" under EX-7 is understated; the tree holds 46.**
Actual: `src` 1 + `scripts` 5 + `evidence` 8 + `out` 24 + `probe` 7 + `entry-draft` 1 = **46**. Drop the count or state 46.

**(c) `0c2eae8d` does not appear in the r3 VaultB census.**
The entry says "`3c3332b9`/`0c2eae8d` also appear in the r3 VaultB census". `grep -rn 0c2eae8d corpus/` returns **no hit** anywhere in the corpus; `3c3332b9` appears at `corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:26` (VaultB revert-path constants). `0c2eae8d` is first recorded by this entry's own bytes (appears in the runtime as an error constant, e.g. `630c2eae8d60e31b`), so the cross-ref should cite the byte walk, not r3.

**(d) Byte 14 is a calldata-size router, not purely "the revert path".**
The entry calls dst `0x000e` "the guard's small-calldata revert-path JUMPDEST". Measured: `[14:25] = 5b 36 15 61 0018 57 5f 80 fd 5b …` — at byte 14, `CALLDATASIZE; ISZERO; PUSH2 0x18; JUMPI`: **0-byte calldata jumps to the receive-path trampoline** (dst 24 = `JUMPDEST; PUSH2 0x20; PUSH2 0x57e; JUMP`, i.e. call the body at 0x57e and `STOP`), 1–3 bytes fall through to `PUSH0 DUP1 REVERT`, and a selector mismatch (≥4 bytes) jumps back to 14 and reverts. So it is simultaneously the receive-entry router and the mismatch/small-calldata revert block. With a real `fallback()` (my `RelayDeskFb`), byte 14 routes 0 → receive and everything else → fallback. Suggested wording: "the guard's small-calldata router: zero calldata → `receive`; 1–3 bytes and selector mismatch → revert (or `fallback` when one exists)".

## 4. Extension earned by this seat: viaIR with a real `fallback()` (narrows a named Unknown)

The entry lists "viaIR carriers with `fallback()` (this carrier has none; the SUB-leg/fall-through interaction with a real fallback is unmeasured)" as an Unknown. My `RelayDeskFb` (10 externals + `receive` + `fallback(bytes)`, viaIR opt200, 1,100 B `b2678621…fb6d`) measures it on this host:

- **Probe: 10/10**, `missing=[]`, `extra=[]`, `dispatch:"abi"` ×10, decoded sha == runtime sha (`ev_0897e569…`). The extractor remains K/K with a real fallback present.
- **Class persists:** 9 EQ legs at 11-byte stride, sorted ascending, all dsts JUMPDESTs, final `PUSH4 e5dd3774 SUB PUSH2 0x000e JUMPI` at pc 310, reported offset 320 = pc+10, not a JUMPDEST/PUSH2 target.
- **Difference:** the guard jumps to a later dispatch start (`0x00cd` = 205, vs 34/51 on the no-fallback carriers), and byte 14 routes zero calldata → `receive`, everything else → **fallback** (not revert). So the SUB-leg/fall-through interaction with a fallback is: unknown selectors go to the fallback body via the same byte-14 router.
- This is a **narrowing, not a closure**: one carrier, one solc, one K, opt200 only.

My fallback-free carrier `RelayDesk` independently reproduces the class at K=10 (936 B `359d6172…f8c8`): 9 EQ + 1 SUB, 9/9 EQ offsets are their JUMPDESTs, SUB selector `e5dd3774` is the numerically **largest** selector and its offset is `pc+10 = 166`. In EX-7's carrier the SUB selector `ee02438e` is likewise the largest (`> d0e30db0`) and its handler (204) immediately follows the dispatch block — the mechanism behind the SUB-and-fall-through shape, measured on two families.

## 5. Landing verdict

- The entry draft + map-token patch are **land-ready after corrections (a)–(d)**. The patch text applies cleanly to the `## Coverage map` EVM row (`corpus/README.md:38`) and the overlay measurement is 85/85 with `missing []` / `dangling []` and `rule_blocks` unchanged at 14.
- The draft's internal citations resolve at HEAD: `r3:33` and `r4:28` are Unknowns bullets naming the `viaIR` pipeline; `r3:21` carries the pure/view class; `corpus/QUALITY.md:21` is row 11 (parsed-and-empty); `README.md:38` is the EVM row.
- The `recheck:` command in the entry works as written (disk-backed `TMPDIR` required; a `/tmp` default hits EDQUOT on this host). My re-run at a fresh path produced 15 functions with decoded sha `2ec3f557…`, as the entry predicts; the sealed id differs by path, which the entry's own text anticipates.
- Nothing else changes: no PROVINCE.md, SKILL.md, SCORECARD.md, LOG.md, corpus file, or gate was touched by this seat.

## 6. Custody, scope, limits

- All evidence retained under `.ufo/waves/arc3-loop1-round6/claims/c2/EX-6/verify/` (scripts, sources, compile receipts, byte walks, 10 probe envelopes + summary, command-A results, `bytes-facts.txt`). Scratch was `/var/tmp/ex06-r6/`, never `/tmp`.
- Custody reads only: EX-7's artifact tree (read-only), the wave-1 solc prefix (read-only; no install), r3/r4 corpus entries, SCORECARD/QUALITY/README. `git status` shows only the pre-existing `arc2-loop1-round10/C3.md` modification and the untracked `arc3-loop1-round6/` tree; `git archive` was used for the overlay (no repo mutation).
- A pre-existing `EX-6/{src,evidence,out}` tree predates this run (it is a *different* carrier: 1,127 B opt200 / 3,039 B noopt, source sha `5684069e…`). It is an interrupted prior attempt with no claim artifact; **it is not cited anywhere here**, and my evidence lives in `EX-6/verify/`.
- Honest limits: single solc (0.8.37), three viaIR carriers total (EX-7's K=15 + my K=10 ×2), opt200 primary (noopt only for EX-7's carrier), one REA pin pair (6.4.0/6.7.0), no Vyper IR pipeline, no other solc version, no `runs≠200`, no runtime execution. The comparative "fourth class / fifth convention" claims versus r1/r3/r4 were not re-measured by this seat.

## 7. Reproduce

```bash
SEAT=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round6/claims/c2/EX-6/verify
WAVE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round6/claims/c2/EX-7
PREFIX=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix
mkdir -p /var/tmp/ex06-r6/{repro,own,probe,tmp} && cd /var/tmp/ex06-r6
# 1) byte-identical recompile of EX-7's carrier (source copied read-only)
cp "$WAVE/src/ViaIrVault.sol" repro/
node "$SEAT/scripts/compile3.js" "$PREFIX" repro/ViaIrVault.sol ViaIrVault /var/tmp/ex06-r6/repro
# 2) my carriers
cp "$SEAT/src/RelayDesk.sol" "$SEAT/src/RelayDeskFb.sol" own/
node "$SEAT/scripts/compile3.js" "$PREFIX" own/RelayDesk.sol RelayDesk /var/tmp/ex06-r6/own-relay
node "$SEAT/scripts/compile3.js" "$PREFIX" own/RelayDeskFb.sol RelayDeskFb /var/tmp/ex06-r6/own-fb
# 3) walks
python3 "$SEAT/scripts/walk.py" repro/viair-opt200/runtime.bin
# 4) sealed probes (cached 6.4.0 / 6.7.0; disk-backed TMPDIR mandatory)
TMPDIR=/var/tmp/ex06-r6/tmp node ~/.npm/_npx/dea9475797100b20/node_modules/rea-agents/scripts/rea.mjs \
  inspect-evm-interface repro/viair-opt200/runtime.hex hex --format json
# 5) command A overlay
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
git archive c625d5d | tar -x -C /var/tmp/ex06-r6/overlay
cp "$WAVE/entry-draft/2026-10-19-arc3-r6-viair-dispatch-shape.md" /var/tmp/ex06-r6/overlay/corpus/knowledge/
# apply the EVM-row token patch, then run the SCORECARD.md:88-124 recipe over the overlay
```

Evidence index: `verify/README.txt`. Key files: `verify/bytes-facts.txt`, `verify/receipts/*.txt`, `verify/walks/*.json`, `verify/probe/summary.json`, `verify/commandA-*.json`.
