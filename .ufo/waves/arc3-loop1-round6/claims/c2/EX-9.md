# EX-9 — c2 chain (corpus Unknown verification) — arc3-loop1-round6

Seat: EX-9 · chain **c2** · 2026-10-19 · lane `kaidoku-shokunin` · dispatch provider `opencode-go-7/deepseek-v4.1-flash` (per `claims-frozen.md`, fourth dispatch).
Target claim: **C2 — close one named corpus Unknown.** EX-7 already delivered the `viaIR` entry; this seat's job per the wave brief is to **independently verify it** (re-derive every number first-hand, rule #14) — not to redo it.

Verdict in one line: **EX-7's viaIR entry is VERIFIED** — command A 84 → 85 measured (not projected), all six bytecode hashes reproduced from an independent compile, the fourth-dispatcher-class walk reproduced byte-for-byte, and all seven own-path probe legs plus the entry's recorded recheck command reproduced — with **one CORRECTED item**: the CBOR-trailer hex transcript at draft line 28 contains a transcription error (`73` where the byte is `64`), which should be fixed before landing.

Artifact draft under verification: `.ufo/waves/arc3-loop1-round6/claims/c2/EX-7/entry-draft/2026-10-19-arc3-r6-viair-dispatch-shape.md` (34 lines).

## 0. Method and independence

- Scratch: `/var/tmp/ex09-r6` (never `/tmp`; EDQUOT standing rule). Nothing in the lane repo was written by this seat except this artifact dir.
- Independent instruments: this seat's own `compile.js` (solc JS API, 3 legs), its own `walk.py` (opcode decoder + dispatch walk, written for this seat), its own probe invocations (`rea-agents@6.4.0`/`6.7.0`), and a **scratch clone** (`git clone --shared` of the lane at `c625d5d`) on which the entry + coverage token were landed and command A re-measured. No EX-7 script was executed except reading its source carrier.
- The carrier source was read from EX-7's delivered tree (sha256 re-hashed `f5391167…80cbbe`, equal to EX-7's stated digest); compiling it is the experiment, not a quote.

## 1. Re-derived first-hand — pre-state, Unknown, toolchain

| item | verdict | first-hand evidence |
|---|---|---|
| Command A before-state at `58c3db7` (work commit) | **REPRODUCED** | SCORECARD.md:88-124 recipe run verbatim → `{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "58c3db7", "rule_blocks": 14}` (`evidence/commandA-before.json`) |
| The viaIR Unknown is real and open at HEAD | **VERIFIED** | `grep -rn -i viaIR corpus/knowledge/*.md` → exactly 2 hits, both Unknowns lists: `2026-10-19-arc3-r3-evm-optimizer-shapes.md:33`, `2026-10-19-arc3-r4-evm-vyper-leg.md:28`. No corpus entry measures the viaIR dispatcher. |
| HEAD / work commits | **REPRODUCED** | `git log --oneline -5` → `c625d5d` records on `58c3db7` work; wave tree untracked as stated |
| solc toolchain | **REPRODUCED** | `node -e "console.log(require('solc').version())"` → `0.8.37+commit.f401782d.Emscripten.clang`; `sha256sum node_modules/solc/soljson.js` → `221d7a667378b5068d913e75fe092507e061363cd1d23b64c49ae82febabad4c`; `package.json` → `b3a90035cab4e8aa43068f33f01497dccfb77b294e1ea30c5fb32a9631e33491` (equal to the r3 record) |
| Entry filenames / token shape | **VERIFIED** | draft stem `2026-10-19-arc3-r6-viair-dispatch-shape` matches the coverage-map regex `2026-10-\d{2}-[a-z0-9-]+` and the `+| EVM |` patch token |
| Patch minus-line byte-exactness | **VERIFIED** | `git show 58c3db7:corpus/README.md` piped to `sed -n 38p` byte-equals the `-| EVM |` line in `EX-7.md` (318 B, equality asserted in Python) |

## 2. Independent compile — six bytecode hashes re-derived

Same source (`ViaIrVault.sol`), same declared settings read from EX-7's `input.json` (viaIR true/false, optimizer 200/off), compiled by this seat's `compile.js` into `/var/tmp/ex09-r6/out/`.

| leg | runtime size | runtime sha256 | creation size | creation sha256 | vs EX-7 |
|---|---|---|---|---|---|
| viair-opt200 | 1,517 B | `2ec3f557f6f2fb229dc49094981723c6efcce3df10f20363ec1732845c99581a` | 1,560 B | `d85fdde93b1fcb620a8a0dcf16885b7b55113b9ef7860ae5ebdbf5ad5fbd83d5` | **REPRODUCED** |
| viair-noopt | 4,144 B | `0cc6938cd768199159cbed74a7e9f5bd4273c583afbf6babca643b0ffdbd29b4` | 4,318 B | `f1125049532f0dd9a71ab0f9963590d7a40913e521c43709400c92b96cc54063` | **REPRODUCED** |
| std-opt200 (control) | 1,921 B | `c2ceabb163ad9c1e6d88244c29c5187602eaf4c810029d0018e76eb9643f7e27` | 1,966 B | `4541fd490eb46198e788c148328dfb74e0ae1fd29c961a47c6f3056b823c5d9e` | **REPRODUCED** |

- ABI **semantically identical across all three legs** (parsed-JSON equality, not file-hash equality): 17 entries = 15 functions + 1 constructor + `receive`; functions view ×7 / pure ×1 / nonpayable ×6 / payable ×1 (`deposit`), plus payable `receive`. `method-identifiers` 15 keys, identical across legs.
- Note: EX-7's `abi.json` sha `63fcf52f…` and `method-identifiers.json` sha `c32e2ef2…` are **file-formatting-scoped** (indent style); this seat's recompiled JSON parses equal but hashes differently (`95e1a2bc…`). The entry says "ABI byte-identical across all three legs" — true within EX-7's own three files; the semantic equality is what I independently confirm.

## 3. Independent dispatch walk (own decoder, `walk.py`)

| item | EX-7 claim | measured this seat | verdict |
|---|---|---|---|
| viaIR prologue | `6080604052 60043610 15 61<0022> 57 …` with `ISZERO` | head `60806040526004361015610022575b3615610018575f80fd5b61002061057e565b005b5f3560e01c…`; decode `PUSH1 4 CALLDATASIZE LT ISZERO PUSH2 0x0022 JUMPI` | **REPRODUCED** |
| Legacy guard contrast | no `ISZERO` (`60043610 61<00e7> 57`) | std head `6080604052600436106100e7575f3560e01c8063…` | **REPRODUCED** |
| viaIR compare tree | 14 × `DUP1 PUSH4 <sel> EQ PUSH2 <dst> JUMPI`, 11-byte stride, ascending | 14 EQ legs; `eq_pc_gaps=[11]×13`; selectors ascending (`01681a62` … `d0e30db0`) | **REPRODUCED** |
| EQ dsts | 253/272/311/340/374/425/485/572/631/694/723/771/935/982, all JUMPDESTs | exact same set; `all_dst_jumpdests=true` | **REPRODUCED** |
| 15th leg | `PUSH4 ee02438e SUB PUSH2 0x000e JUMPI` at push4 pc 194 | exact: pc 194, sel `ee02438e`, dst 14; `SUB` (0x03) not `EQ` | **REPRODUCED** |
| Fall-through | opt200 pc 204 = `CALLVALUE` (0x34); noopt 0x61 | byte at push4_pc+10: `34` (opt200), `61` (noopt) | **REPRODUCED** |
| noopt chain | dsts 208–273, SUB leg at 194 | EQ dsts 208,213,…,273; SUB pc 194 | **REPRODUCED** |
| Control tree | 15 EQ + 3 GT; pivots `6e69f38c`/`90ab171e`/`3f4ba83a` at pcs 19/30/137 | exactly; those three selectors appear twice each | **REPRODUCED** |
| PUSH4 census, opt200 | 19 sites / 18 distinct: 15 selectors + `4e487b71`×2 (553,1143), `0c2eae8d` (1094), `3c3332b9` (1261) | exact pcs and values; selector sites 15, all in `methodIdentifiers` | **REPRODUCED** |
| PUSH4 census, noopt | 15 selectors + `4e487b71`×2 | 17 sites / 16 distinct; extras `4e487b71` @1790,2635 | **REPRODUCED** |
| PUSH4 census, std | 18 selector sites / 15 distinct + `3c3332b9`,`4e487b71`,`0c2eae8d`,`43000825` | 22 sites / 19 distinct; duplicates `6e69f38c`,`90ab171e`,`3f4ba83a`; extras @993/1680/1830/1914 | **REPRODUCED** |
| CBOR trailer | `ipfs` + `solc 0x000825` | trailer at runtime +1464; parses `a2 64"ipfs" 58 22 1220<32> 64"solc" 43 000825` + length `0033` (=51) | **REPRODUCED (transcript CORRECTED, below)** |
| Creation embedding | runtime embedded at +43 of 1,560 B | `creation[43:43+1517] == runtime` is **True**; `find` offset 43 | **REPRODUCED** |

### 3a. Selector derivation and planted set (re-derived, not quoted)

- `js-sha3@0.8.0` (the same library variant EX-7 used, but invoked by this seat from the solc prefix) over all 15 `methodIdentifiers` signatures: **15/15 derived, 0 mismatches** — the selector set is independently reproduced from the ABI signatures.
- `planted-K.json`: K=15, 15 entries, 15 distinct selectors; `planted-K.preact.json`: same; and both sets **equal** `methodIdentifiers` values, with signatures equal to its keys. Pre-compile record and post-fix record agree (the `digestOf` pure→view fix was selector-neutral, as claimed).
- ERC-20 collision check: the 9 canonical ERC-20 selectors (transfer, transferFrom, approve, allowance, balanceOf, totalSupply, name, symbol, decimals) computed with `js-sha3` intersect the planted set in **0** places — "no ERC-20 surface" holds at the selector level.
- Carrier ABI census re-derived: 15 functions + constructor + `receive` = 17 entries; view ×7 / pure ×1 / nonpayable ×6 / payable `deposit`; `receive` payable. Matches the entry's carrier description.

## 4. Independent REA probes (seven own-path legs + one verbatim recheck)

All runs `TMPDIR=/var/tmp/ex09-r6/tmp`, `--format json`; envelopes kept under `EX-9/probe/`. Evidence ids are path-sensitive (QUALITY.md row 15), so these are fresh ids, not EX-7's.

| leg | pin | evidence_id | result |
|---|---|---|---|
| viair-opt200 `runtime.hex` | 6.4.0 | `ev_ce106de4eb4b…` | **15 functions**, all `dispatch:"abi"`, decoded `2ec3f557…`, offsets `[982,935,771,723,694,631,572,485,425,374,340,311,272,253,204]` |
| viair-opt200 `runtime.bin` raw | 6.4.0 | `ev_a8601a140ca9…` | 15/15, same payload |
| viair-opt200 `runtime.hex` | 6.7.0 | `ev_a415455d14ee…` | 15/15, same decoded sha |
| viair-noopt `runtime.hex` | 6.4.0 | `ev_7056473a8a7c…` | 15/15, decoded `0cc6938c…`, offsets `[…,208,204]` |
| std-opt200 `runtime.hex` (control) | 6.4.0 | `ev_2c619f985271…` | 15/15, decoded `c2ceabb1…` |
| TRAP: `raw` fed the hex *text* | 6.4.0 | `ev_de66ca0996b8…` | **0 functions**, decoded sha `b675ec73…` == this seat's hex-file sha; parsed-and-empty |
| creation.hex probe | 6.4.0 | `ev_58ec8e4eafd0…` | **0 functions**, decoded `d85fdde9…` == creation bin sha; parsed-and-empty |

- Function-set exactness per leg: recovered selector set == `methodIdentifiers` values, zero missing / zero extra, all `dispatch:"abi"`.
- Offset semantics: viair-opt200 and viair-noopt **14/15** reported offsets equal their EQ leg's `PUSH2` dst and land on a JUMPDEST; the exception is `ee02438e` (`mark(bytes32)`) at **204 = push4_pc + 10**, not a JUMPDEST, not a PUSH2 target. Control: **15/15** on JUMPDESTs. EX-7's fifth-convention claim **REPRODUCED**.
- Mutability delta vs ABI: **14/15 strict agreement**; only divergence `scale(uint256,uint256)` `pure` → inferred `view` (selector `0x6e69f38c`). Zero payable-reads: the r4 Vyper pattern does not appear. **REPRODUCED**.
- Trap class self-consistency detail: EX-7's hex file carries a trailing newline (3,035 B, sha `19838d66…`); this seat's is 3,034 B (`b675ec73…`). Both decode to the same 1,517 B. The trap claim "decoded sha == the hex file's own sha" is class-correct; the literal digest is file-format-dependent, as the entry itself scopes.
- **Recorded `recheck:` line reproduces verbatim.** Run from the lane repo root exactly as written in the draft (disk-backed `TMPDIR`), it returns **15 functions**, all `dispatch:"abi"`, decoded sha `2ec3f557…` — `ev_71da9d37a97c…` (`EX-9/probe/recheck-literal.json`). The entry's self-check command is executable as written, not just plausible.

## 5. Landing move — measured, not projected

Scratch clone `/var/tmp/ex09-r6/clone` (`git clone --shared` of the lane at `c625d5d`), then:

1. copied the draft to `corpus/knowledge/2026-10-19-arc3-r6-viair-dispatch-shape.md`;
2. replaced `corpus/README.md:38` with EX-7's `+| EVM |` line **byte-exactly** (minus-line verified byte-equal first; landed row text equality asserted against the `+|` line, 446 B);
3. committed as `9f4f569` (scratch only).

Command A at `9f4f569`:

```json
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 85, "mapped": 85, "missing": [], "revision": "9f4f569", "rule_blocks": 14}
```

**84 → 85 measured**, `mapped 85`, `missing []`, `dangling []`, coverage 10.0, `rule_blocks` untouched (c3's axis). This confirms EX-7 §3's projected line; the projection is now a measurement on the exact landing content.

## 6. Corrections (one item) — CORRECTED

Draft line 28 states the CBOR trailer as:

```
a2 64 69706673 58 22 <ipfs 22958d9b…4945d64> 73 736f6c63 43 000825 00 33
```

Measured bytes (`evidence/cbor-and-census.txt`, runtime +1464, 53 B):

```
a2 64 69706673 58 22 1220 22958d9b2c8d598780ac3ddde2db45b5597520a14031175bdd54fe0a2104945d 64 736f6c63 43 000825 00 33
```

- **`73 736f6c63` → `64 736f6c63`.** 0x64 is CBOR `text(4)` for "solc"; the draft's 0x73 would declare a 19-byte string and does not parse. This is a transcription slip in the hex, not a wrong conclusion — the trailer class (`ipfs` + `solc 0x000825` = 0.8.37) is correct.
- The digest ellipsis `<ipfs 22958d9b…4945d64>` glues the following `64` onto the digest; the 34-byte byte-string value is `1220` + 32 bytes, ending `…2104945d`. (The `1220` multihash prefix is omitted in the draft's angle-bracket abstraction — recommend stating `1220<32-byte digest>`.)

Recommended landing action: apply this two-token fix to line 28 of the draft before copying it to `corpus/knowledge/`, or land the entry and append the correction to the round's append-only erratum block (SKILL.md rule: corrections are append-only, naming the row superseded). Everything else in the entry is measurement-clean.

## 7. Per-item verdict summary

| item | verdict |
|---|---|
| C2 falsifiable before → after (84 → 85, mapped 85, missing/dangling empty, K/K evidence cited) | **VERIFIED** — measured on scratch landing `9f4f569` |
| Unknown provenance (r3:33, r4:28) and closure scoping ("solc 0.8.37, this host, this carrier family") | **VERIFIED** |
| Independent recompilation of all three legs (six hashes) | **REPRODUCED** |
| Fourth dispatcher class: inverted guard + 14-leg ascending EQ chain at 11-byte stride + `SUB`-terminated final leg | **REPRODUCED** |
| Pipeline controls the shape (std control = GT/EQ binary search, same source/optimizer) | **REPRODUCED** |
| Offset convention (viaIR 14/15 dst, mark = pc+10; control 15/15 JUMPDEST) | **REPRODUCED** |
| Mutability delta (14/15, `scale` pure→view, zero payable-reads) | **REPRODUCED** |
| Zero false positives (PUSH4 census values/pcs) | **REPRODUCED** |
| Traps: raw-on-hex parsed-and-empty; creation parsed-and-empty with runtime at +43 | **REPRODUCED** |
| CBOR-trailer claim | **REPRODUCED**, with draft hex transcript **CORRECTED** (`73`→`64`; digest tail) |
| Landing patch text and token | **VERIFIED** byte-exact; post-landing command A measured |
| Entry's recorded `recheck:` command | **REPRODUCED** verbatim from the lane repo root — 15/15, decoded `2ec3f557…` (`ev_71da9d37a97c…`) |

No competing design proposed: EX-7's entry is the right closure for this Unknown, and re-deriving it is this seat's contribution. The Vyper `-O codesize` / `--no-optimize` dispatcher Unknown (r4:28) remains open for a different seat — I did not touch it.

## 8. Custody & scope

- Evidence: `EX-9/evidence/` (7 files: command A before/after JSON, per-leg walk JSON, CBOR decode, hash summary) and `EX-9/probe/` (8 sealed envelopes: 7 own-path legs + the verbatim recheck) — 16 files including `EX-9/manifest.sha256` (covers all of the above plus this artifact).
- Scratch `/var/tmp/ex09-r6` (compile outputs, clone, probe TMPDIR); no `/tmp` writes.
- Custody reads only: lane repo at `c625d5d`, r1 solc prefix (read-only), EX-7 delivered tree. Lane `git status` unchanged by this seat apart from this artifact dir being untracked; git history untouched (the clone is a separate repo under `/var/tmp`).
- Honest limits: single solc version (0.8.37), single carrier source, K=15, one 6.7.0 leg (hex only), raw legs at 6.4.0 only; the landing measurement is on a scratch clone of the same tree, not a lane commit — the parent still owns the real landing.
