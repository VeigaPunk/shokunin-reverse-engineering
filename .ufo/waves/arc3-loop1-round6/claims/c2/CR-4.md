# CR-4 — c2 chain (corpus Unknown) — arc3-loop1-round6

Seat: CR-4 · chain c2 · 2026-10-19 · lane `kaidoku-shokunin` · dispatch provider `opencode-go-7/deepseek-v4.1-flash` (fourth dispatch, per `claims-frozen.md`).
Target claim: **C2 — close one named corpus Unknown.** Action chosen: **independent verification of EX-7's delivered viaIR entry**, not a competing Unknown. EX-7 already closed the named Unknown (`corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:33`, `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:28`); re-closing it would duplicate work. This seat re-derived every number from the bytes, the toolchain and the probe path, and found **no substantive error** — three precision corrections and one landing-hygiene item are recorded in §3.

Rule #14 compliance: every number below was produced this seat. EX-7's values appear only in the “claim under test” column and are never used as evidence. Scratch root `/var/tmp/cr4-r6/` (never `/tmp`). Custody paths read-only. Lane Git read-only; the only Git commits made are inside a throwaway repo at `/var/tmp/cr4-r6/sim` (§1.5). Write scope used: this artifact dir only.

## 0. Baseline

| item | first-hand evidence |
|---|---|
| HEAD records commit `c625d5d`, work commit `58c3db7` | `git log --oneline -5` (lane root; no mutation) |
| Command A before-state at the work commit | ran the `SCORECARD.md:88-124` recipe verbatim with `REV=58c3db7` → `{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "58c3db7", "rule_blocks": 14}` (`CR-4/evidence/commandA-before-58c3db7.json`) |
| The named Unknown is still open at HEAD | `grep -n "viaIR" corpus/knowledge/*.md` → exactly two hits, both in Unknowns lines: `…r3…:33` (“the `viaIR` pipeline”) and `…r4…:28` (same phrase) |
| `git status` before/after this seat | only the pre-existing ` M .ufo/waves/arc2-loop1-round10/C3.md` and the untracked `?? .ufo/waves/arc3-loop1-round6/` tree — no tracked file touched |
| solc toolchain | `node -e "require('./.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/solc').version()"` → `0.8.37+commit.f401782d.Emscripten.clang`; `sha256sum` `soljson.js 221d7a667378b5068d913e75fe092507e061363cd1d23b64c49ae82febabad4c`, `solc/package.json b3a90035cab4e8aa43068f33f01497dccfb77b294e1ea30c5fb32a9631e33491` (`CR-4/evidence/solc-digests.txt`) |
| carrier source | `sha256 src/ViaIrVault.sol` → `f53911672f2e33eaabaeff85e75c2565bb2899638d194fb3ffe6747abe80cbbe` (matches the source digest EX-7's entry claims to have compiled) |

## 1. Re-derived first-hand

### 1.1 Compile reproduction (my own script, not EX-7's)

`/var/tmp/cr4-r6/compile-cr4.js` is a fresh standard-JSON driver I wrote for this seat; it requires the same receipted solc prefix and uses the three settings the entry declares (`viaIR:true`+optimizer 200; `viaIR:true`+optimizer off; optimizer 200 with `viaIR` unset). Output, run against EX-7's `src/ViaIrVault.sol`:

```
viair-opt200  runtime 1517 B  sha256 2ec3f557f6f2fb229dc49094981723c6efcce3df10f20363ec1732845c99581a
              creation 1560 B sha256 d85fdde93b1fcb620a8a0dcf16885b7b55113b9ef7860ae5ebdbf5ad5fbd83d5
viair-noopt   runtime 4144 B  sha256 0cc6938cd768199159cbed74a7e9f5bd4273c583afbf6babca643b0ffdbd29b4
              creation 4318 B sha256 f1125049532f0dd9a71ab0f9963590d7a40913e521c43709400c92b96cc54063
std-opt200    runtime 1921 B  sha256 c2ceabb163ad9c1e6d88244c29c5187602eaf4c810029d0018e76eb9643f7e27
              creation 1966 B sha256 4541fd490eb46198e788c148328dfb74e0ae1fd29c961a47c6f3056b823c5d9e
```

All six hashes and sizes equal the retained `EX-7/out/` files. I also hashed the retained files directly (`sha256sum out/*/runtime.bin …`) and recomputed all 24 `evidence/compile-receipt-rerun.txt` hash/size lines against the files: **24/24 match** (`CR-4/evidence/compile-rerun.json`; receipt audit performed in the same shell session). ABI and method-identifier files are byte-identical across the three legs (`63fcf52f…` and `c32e2ef2…`), as claimed; the ABI has 17 entries = constructor + 15 functions + `receive`, and the mutability tally is payable 1 / view 7 / nonpayable 6 / pure 1.

This establishes byte-exact reproduction of the carrier set from source with the receipted compiler, independent of EX-7's compile run.

### 1.2 REA probe reproduction (fresh scratch paths, both cached pins)

Every probe below was run this seat from `/var/tmp/cr4-r6/` with `TMPDIR=/var/tmp/cr4-r6/tmp`; the primary legs used `npx --offline`, and the entry's recheck row was run verbatim as written (`npx -y`). The full envelopes are retained under `CR-4/evidence/`. Evidence ids are path-minted, so mine differ from EX-7's by construction; the admissible comparison is decoded `bytecode.sha256` + function payload (`corpus/QUALITY.md:15`).

| leg | pin | n fns | dispatch | decoded sha256 | my `ev_` id | payload vs EX-7 envelope |
|---|---|---|---|---|---|---|
| viair-opt200 `runtime.hex` | 6.4.0 | 15 | `abi` ×15 | `2ec3f557…` | `ev_d3d5a31609…` | identical (15 rows: selector, offset, dispatch, mutability) |
| viair-opt200 `runtime.bin` raw | 6.4.0 | 15 | `abi` ×15 | `2ec3f557…` | `ev_2898539c…` | identical to EX-7's raw envelope |
| viair-noopt `runtime.hex` | 6.4.0 | 15 | `abi` ×15 | `0cc6938c…` | `ev_7ed3ddb9eec…` | identical |
| std-opt200 `runtime.hex` (control) | 6.4.0 | 15 | `abi` ×15 | `c2ceabb1…` | `ev_8aeca9561aa…` | identical |
| viair-opt200 `runtime.hex` | 6.7.0 | 15 | `abi` ×15 | `2ec3f557…` | `ev_e8cfb9803f…` | identical (and identical to the 6.4.0 payload) |
| TRAP: `runtime.hex` fed as `raw` | 6.4.0 | 0 | — | `19838d66…` (= the hex file's own sha) | `ev_7783e2b0c53…` | parsed-and-empty, as claimed |
| `creation.hex` fed as `hex` | 6.4.0 | 0 | — | `d85fdde9…` (= creation bin sha) | `ev_8d3e6bd4d0b…` | parsed-and-empty; metadata at creation offset **1507** |
| entry's own `recheck:` command, run verbatim | 6.4.0 | 15 | `abi` ×15 | `2ec3f557…` | `ev_71da9d37…` | the entry's reproducibility line works as written |

`probe-summary.json` and `payload-compare.txt` hold the machine-readable version. Payload equality covers offsets and `stateMutability`, not just the selector set.

One extra consistency check the entry implies but does not state: the creation probe reports the CBOR trailer at bytecode offset **1507**, and `43 + 1464 = 1507` where 1464 is the runtime's trailer offset. That is independent confirmation that the runtime is embedded at **+43** in the 1,560 B creation blob — `bytes.fromhex(creation)[43:43+1517] == runtime` returned `True` in my own check.

### 1.3 Independent dispatch walk (my own disassembler)

`/var/tmp/cr4-r6/walk-cr4.py` is a fresh minimal EVM linear sweep (opcode + immediate lengths; my first draft had an off-by-one in PUSH immediate accounting and was discarded — the numbers below are from the corrected walker and were cross-checked against the REA offsets). Results:

| leg | len | PUSH4 sites | EQ legs | SUB leg | EQ dsts | stride | ascending | all dst JUMPDEST |
|---|---|---|---|---|---|---|---|---|
| viair-opt200 | 1517 | 19 | 14 | 1 (`ee02438e`, push4 pc 194) | 253, 272, 311, 340, 374, 425, 485, 572, 631, 694, 723, 771, 935, 982 | 11 B ×13 | yes (`01681a62`→`d0e30db0`) | yes (14/14) |
| viair-noopt | 4144 | 17 | 14 | 1 (`ee02438e`, push4 pc 194) | 208, 213, 218, 223, 228, 233, 238, 243, 248, 253, 258, 263, 268, 273 | 11 B ×13 | yes | yes (14/14) |
| std-opt200 | 1921 | 22 | 15 | 0 | 346, 379, 446, 477, 497, 527, 558, 589, 620, 672, 692, 715, 735, 773, 781 | 11/15/26 | no | yes (15/15) |

Guard bytes (runtime prefix; `…` elides the remainder):
- viair-opt200 `6080604052600436101561002257…` — `PUSH1 4 CALLDATASIZE LT ISZERO PUSH2 0x0022 JUMPI` (inverted).
- viair-noopt `6080604052600436101561001d57…` — same ISZERO guard, post-target `0x001d`; its zero-calldata branch is `CALLDATASIZE PUSH2 0x05dc JUMPI` (no ISZERO, the no-optimizer form), a shape detail the entry does not claim beyond “same shape”.
- std-opt200 `6080604052600436106100e757…` — `…LT PUSH2 0x00e7 JUMPI`, no ISZERO.

SUB leg and fall-through: bytes `63 ee02438e 03 61 000e 57` at 194–203 in both viaIR legs; dst `0x000e` is a JUMPDEST (`byte 0x5b` at 14). The handler head after fall-through is 204 in both: opt200 `34 61 00f9 57` (`CALLVALUE; PUSH2 0x00f9; JUMPI`), noopt `61 05a9 56` (`PUSH2 0x05a9; JUMP`). The extractor reports `mark`'s offset as 204 in both, i.e. `push4_pc + 10`, not a JUMPDEST and not a PUSH2 target.

Zero false positives: non-selector PUSH4 sites are exactly `4e487b71` at 553 and 1143, `0c2eae8d` at 1094, `3c3332b9` at 1261 (opt200); `4e487b71` at 1790 and 2635 (noopt); `3c3332b9` 993, `4e487b71` 1680, `0c2eae8d` 1830, `43000825` 1914 (control, the last inside the CBOR trailer). The control's three GT pivots are `6e69f38c` (pc 19), `90ab171e` (pc 30), `3f4ba83a` (pc 137); those three selectors appear twice (GT pivot + EQ leaf), and the extractor deduplicates to 15.

CBOR trailer: exact tail is
`fe a2 64 69706673 58 22 12 20 22958d9b2c8d598780ac3ddde2db45b5597520a14031175bdd54fe0a2104945d 64 736f6c63 43 000825 00 33`
— metadata length 51, `ipfs` bytes(34) with `12 20` sha2-256 multihash prefix, `solc` bytes(3) = `0x000825` (0.8.37), terminator `00 33`. Annotated decode: `CR-4/evidence/cbor-annotated.txt`.

### 1.4 Selector derivation and mutability

- js-sha3 (the copy bundled with the solc prefix) over canonical signatures built from the compiled ABI matches solc's `evm.methodIdentifiers` **15/15**; the planted-K file's selector set equals the method-identifier values exactly; the pre-fix `planted-K.preact.json` has the same 15 selectors; intersection with the 9 ERC-20 selectors is empty. K=15 has three agreeing derivations, as claimed.
- Pre-compile ordering is corroborated by the surviving original scratch tree: `planted-K.json` mtime 12:50:42 precedes the first probe envelope's 12:56:57. The retained `out/` files carry 13:23:32 mtimes because they are the deterministic rerun (receipt 13:23:33) that reproduces the pre-probe bytes; the retained out/ set is not itself the first compile. Content alone cannot prove a timestamp; this is corroboration, not cryptographic proof.
- Mutability vs ABI on viair-opt200: **14/15 agree**; the sole divergence is `scale(uint256,uint256)` ABI `pure` → inferred `view`. The only `payable` read is `deposit()` (`d0e30db0`), which is genuinely payable; zero spurious payable reads, so the r4 Vyper “arg-taking → payable” pattern does not appear.

### 1.5 Command A after-state — scratch landing simulation

Because the lane Git is read-only for this seat, I simulated the landing in a throwaway repo: `git archive HEAD | tar -x -C /var/tmp/cr4-r6/sim`, `git init` + commit (base `6013653`), then copy the entry draft to `corpus/knowledge/2026-10-19-arc3-r6-viair-dispatch-shape.md` and apply the exact EVM-row patch from `EX-7.md` §3, commit (`78b4761`). Command A, run against each revision:

| revision (scratch only) | knowledge_files | mapped | missing | dangling | rule_blocks | citation_resolved_rules | coverage | depth |
|---|---|---|---|---|---|---|---|---|
| `6013653` base (HEAD tree) | 84 | 84 | [] | [] | 14 | 14 | 10.0 | 10.0 |
| `78b4761` landed | **85** | **85** | **[]** | **[]** | 14 | 14 | 10.0 | 10.0 |

This is a measurement on a scratch tree, not a projection: the entry + token land at 85/85 with the other counters untouched. The scratch revisions are not lane commits and are cited only as simulation evidence (`commandA-sim-before.json`, `commandA-sim-after.json`, `scratch-sim-git-log.txt`, `scratch-sim-landing-stat.txt`).

## 2. Per-item verdicts

Legend: **REPRODUCED** = my independent run produced byte-identical output; **VERIFIED** = my first-hand measurement matches the claim; **CORRECTED** = claim is substantively right but its wording/rendering is wrong; **UNVERIFIABLE** = cannot be checked by the admissible route, with the reason stated.

| # | claim under test (EX-7) | my measurement | verdict |
|---|---|---|---|
| 1 | Unknown provenance `r3:33`, `r4:28` | both lines contain “the `viaIR` pipeline” in their Unknowns lists | VERIFIED |
| 2 | carrier source `f5391167…80cbbe`, ABI census 15 fns + receive | source sha matches; ABI 17 entries; tally 1 payable / 7 view / 6 nonpayable / 1 pure + receive | VERIFIED |
| 3 | three compile legs (1517/4144/1921 B; shas `2ec3f557…`, `0cc6938c…`, `c2ceabb1…`) | my own compile reproduced all three runtime + creation hashes byte-for-byte | REPRODUCED |
| 4 | compile rerun byte-identical | my rerun equals the retained `out/`; 24/24 receipt hash/size lines match the files | VERIFIED |
| 5 | K=15 recorded pre-compile with 3 agreeing derivations | js-sha3 ↔ solc 15/15; planted set == method ids; preact set equal; `planted-K.json` mtime precedes the first probe; retained `out/` is the byte-identical rerun | VERIFIED |
| 6 | K/K 15/15 on every real leg (hex, raw, 6.7.0, noopt, control) | my 6.4.0 hex/raw + 6.7.0 + noopt + control probes: 15/15 each, `dispatch:"abi"` ×15, decoded shas as claimed; payloads identical to EX-7's envelopes | REPRODUCED |
| 7 | raw-on-hex trap → 0 fns, decoded sha = hex-text sha `19838d66…` | reproduced exactly | REPRODUCED |
| 8 | creation probe → 0 fns, decoded sha `d85fdde9…`; runtime embedded at +43 of 1,560 B | reproduced; `creation[43:43+1517] == runtime` true; creation trailer offset 1507 = 43+1464 | VERIFIED |
| 9 | fourth dispatcher class: `5f3560e01c`, inverted guard with ISZERO, 14 ascending EQ legs at 11 B stride, SUB-terminated 15th leg | my walk: 14 EQ legs, dsts 253–982, stride 11×13, ascending, `SUB` leg at 194 → 0x000e | VERIFIED |
| 10 | SUB-leg dst 0x000e is the guard JUMPDEST; match falls through to `mark` at 204 (byte `0x34` opt / `0x61` noopt) | byte 14 is `5b`; 204 is `34 61 00f9 57` (opt) / `61 05a9 56` (noopt); extractor offset 204 | VERIFIED |
| 11 | std control compiles the r3 class: guard without ISZERO, GT pivots at pcs 19/30/137, 15 EQ + 3 GT, three duplicated selectors | my walk and probe reproduce all of it; 22 PUSH4 sites = 18 selector sites + 4 constants | VERIFIED |
| 12 | zero false positives; non-selector constants at 553/1094/1143/1261 (opt) etc. | exact pcs and immediates match; no non-selector reported as a function | VERIFIED |
| 13 | offset convention: 14/15 = EQ `PUSH2` dst/JUMPDEST, 15th = push4_pc+10; “the r3 rule is legacy-pipeline-scoped” | 14/15 and 204 confirmed; the scope wording is wrong — r1's legacy linear control is the counterexample (r3 entry :31) | **CORRECTED** (see §3.1) |
| 14 | mutability 14/15, `scale` pure→view, no Vyper payable pattern | reproduced; sole payable read is genuinely payable `deposit` | VERIFIED |
| 15 | CBOR trailer: ipfs + solc 0x000825 = 0.8.37 | substance correct; the written byte sequence is off by one byte in two adjacent places | **CORRECTED** (see §3.2) |
| 16 | selector identity exact; argument strings inferential | selector set exact on all legs; arguments include e.g. `marked(bytes32)` inferred as `uint256`, so the “inferential” disclaimer is doing real work | VERIFIED (as scoped) |
| 17 | landing the entry + token gives command A 85/85, missing/dangling [] | scratch landing simulation `78b4761` → 85/85, other counters unchanged | VERIFIED |
| 18 | custody “42 files” at delivery | 46 files: src 1 + scripts 5 + evidence 8 + out 24 + probe 7 + entry 1 | **CORRECTED** (see §3.3) |
| 19 | lane `git status` unchanged apart from the pre-existing modification | current status matches exactly | VERIFIED |
| 20 | exact `ev_` ids (`ev_409e0442…` etc.) | my runs mint different ids at different paths; this is the recorded path-sensitive domain, and the entry itself says compare by decoded sha + payload. Their ids are present in their envelopes and the payload/decoded-sha comparison passes | **UNVERIFIABLE by design** (not a defect) |
| 21 | Unknown narrowed, not closed (other solc versions, Vyper IR, runs≠200, fallback shapes, receive shapes) | not tested here; the entry declares them as Unknowns, which is the honest disposition | not tested, correctly declared |

## 3. Corrections (apply before or at landing; none changes the token, filename, or 85/85 result)

### 3.1 Offset-scope wording — entry line 24 (and `EX-7.md:40`)

The claim “the r3 statement shape ‘offsets land on JUMPDESTs’ is **legacy-pipeline-scoped**” is false as written. The r3 corpus entry records the counterexample in the legacy pipeline: r1's `60003560e01c` linear control reports its declared `PUSH1` jump immediates at 38/48/58, with the JUMPDESTs two bytes later at 40/50/60 (`corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:31`). The rule is **class-scoped**, not pipeline-scoped: it holds for the solc legacy binary-search class (the std control here, 15/15) and fails for both the r1 linear class and this viaIR class.

Proposed replacement sentence:

> The extractor's offsets mean "handler entry" on all classes so far, but the r3 statement shape "offsets land on JUMPDESTs" is class-scoped, not pipeline-scoped: it holds for the solc legacy binary-search class (the std control here, 15/15) and fails for r1's legacy linear control, whose offsets are declared `PUSH1` jump immediates two bytes before its JUMPDESTs (`corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md`, carrier-A control). viaIR is 14/15; the r4 Vyper rule is push4_pc+11; viaIR's `mark` is push4_pc+10. Offset claims must state the convention per class.

This preserves the entry's actual thesis (“prologue does not identify the pipeline; the compare tree does”) and removes a scope overgeneralization.

### 3.2 CBOR trailer rendering — entry line 28

Written: ``a2 64 69706673 58 22 <ipfs 22958d9b…4945d64> 73 736f6c63 43 000825 00 33``.
Actual bytes: `a2 64 69706673 58 22 12 20 22958d9b2c8d598780ac3ddde2db45b5597520a14031175bdd54fe0a2104945d 64 736f6c63 43 000825 00 33`.

Two adjacent errors: (a) the 34-byte IPFS bytes item is `12 20` + the 32-byte digest, so the digest ends `…2104945d` — the entry's `…4945d64` absorbs the next byte, which is (b) the CBOR text-length `64` that opens the `solc` key. The entry then writes the key as `73 736f6c63` instead of `64 736f6c63`. The conclusion (“`ipfs` + `solc` 0x000825 = 0.8.37”) is unaffected. Use `64 736f6c63`.

### 3.3 Custody file count — `EX-7.md:62`

The delivered `EX-7/` tree has **46** files, not 42 (42 was the count at 13:23:02; the receipt/selector-derivations/manifest files at 13:23:33 and the entry draft at 13:33:07 were added later). Counts: src 1, scripts 5, evidence 8, out 24, probe 7, entry-draft 1. This is a bookkeeping correction only.

### 3.4 Landing-hygiene header — entry lines 1–6

The draft's leading comment says “corpus entry **DRAFT**” and carries a `LAND-MOVE:` instruction addressed to the parent. Landed corpus entries use a one-line provenance comment (compare `corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:1` and `…r4…:1`). Replace it with:

```html
<!-- corpus entry — kaidoku-shokunin arc3-loop1-round6 (2026-10-19), seat EX-7 (c2 chain). Staging: .ufo/waves/arc3-loop1-round6/claims/c2/EX-7/. RESULT-class, no Core promotion. -->
```

A ready-to-apply diff for §3.1, §3.2 and §3.4 against the delivered draft is at `CR-4/evidence/entry-corrections.diff`; the corrected draft is `CR-4/evidence/entry-corrected.md`. I did not modify `EX-7/` — the diff is a proposal for the parent.

## 4. Landing moves

1. Copy the draft (optionally the corrected copy) to `corpus/knowledge/2026-10-19-arc3-r6-viair-dispatch-shape.md`.
2. Apply the EVM-row coverage-map patch exactly as given in `EX-7.md` §3 (token `2026-10-19-arc3-r6-viair-dispatch-shape`). The token matches the recipe's `2026-10-\d{2}-[a-z0-9-]+` pattern.
3. Re-measure command A at the landing commit. Expected from my simulation: `knowledge_files 85, mapped 85, missing [], dangling [], rule_blocks 14, citation_resolved_rules 14, coverage 10.0, depth 10.0`.
4. No SKILL.md, PROVINCE.md, gate or corpus-QUALITY change is part of this claim.

If the parent prefers a minimal landing, the draft as delivered is substantively correct; §3.1–§3.3 are precision issues, not blockers. §3.4 is recommended for corpus hygiene.

## 5. Evidence inventory (`CR-4/evidence/`)

| file | what it is |
|---|---|
| `commandA-before-58c3db7.json` | command A at the work commit (84/84, 14 rules) |
| `commandA-sim-before.json`, `commandA-sim-after.json` | command A on the scratch base and landed revisions (84→85) |
| `scratch-sim-git-log.txt`, `scratch-sim-landing-stat.txt` | the simulation's two commits and the 2-file landing diff |
| `compile-rerun.json` | my independent three-leg compile: lengths + shas |
| `solc-digests.txt` | solc version digests |
| `walk-viair-opt200-cr4.json`, `walk-viair-noopt-cr4.json`, `walk-std-opt200-cr4.json` | my own disassembler output (full site lists, dsts, jumpdest flags, tail) |
| `dispatch-shape-cr4.txt` | compact per-leg shape summary |
| `cbor-tail.txt`, `cbor-annotated.txt` | exact trailer bytes and byte-by-byte decode |
| `probe-summary.json`, `payload-compare.txt` | probe counts/decoded shas/ids and payload comparison against EX-7's envelopes |
| `probe-*.json` (7 full envelopes + entry recheck) | my REA runs at 6.4.0 and 6.7.0, plus the two traps and the entry's own recheck command |
| `mutability-check.txt` | 14/15 agreement, `scale` divergence, payable reads |
| `entry-corrections.diff`, `entry-corrected.md` | proposed precision/hygiene edits to the delivered draft |

## 6. Honest limits

- This is a verification of EX-7's carrier family, not an independent carrier: I reused their `ViaIrVault.sol` and copied their declared compile settings. The reproduction is byte-exact, but it does not add a second source family (e.g. fallback-bearing, receive-less, or different solc versions under viaIR).
- Single solc version (0.8.37); one 6.7.0 leg (hex only); K=15; runtime class 1.5–4.1 KB. The r4 Vyper `--no-optimize` / `-O codesize` Unknown remains open and was not attempted here (no Vyper install was made this seat).
- Exact `ev_` ids are not reproducible across paths by the recorded domain; I compared decoded `bytecode.sha256` + function payloads, per `corpus/QUALITY.md:15`.
- The pre-compile ordering claim rests on the surviving original scratch mtimes plus the file's own `recorded_utc`; mtimes are corroboration, not proof.
- I did not modify any delivered artifact or tracked file. The scratch Git simulation is outside the lane repo; lane Git is untouched.

**C2 verdict: VERIFIED.** EX-7's entry closes the named `viaIR` Unknown with byte-level evidence that reproduces from source and through the tool; command A lands at 85/85 in an isolated landing simulation. The two precision corrections and the custody count do not affect the finding; the landing-hygiene header is recommended before the file enters `corpus/knowledge/`.
