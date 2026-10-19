# RV-1 — chain c1, reviewer — arc3-loop1-round1 (2026-10-19)

**Seat task (frozen):** independently recompute the planted selectors from `token.sol`
using a DIFFERENT keccak path than EX-03; compare vs `planted-selectors.txt`.

**Verdict: MATCH — 9/9.** EX-03's planted set is independently reproduced by RV-1's own
from-spec Keccak-256, and every checkable EX-03 claim about the carrier verifies,
including a full independent recompile of `token.sol` with the authorized solc 0.8.37.
One caveat on the literal task wording, stated plainly in §1.4: EX-03's path is *also* a
from-spec pure-Python Keccak-256, so "different path" holds at the level of
implementation and — more importantly — of **external validation**, not of language or
library family.

---

## 1. Work performed

All RV-1 artifacts are under `.ufo/waves/arc3-loop1-round1/claims/c1/RV-1/`.

### 1.1 Built and validated a from-spec Keccak-256

- `keccak_ref.py` (sha256 `7a1757d3…f139`): Keccak-f[1600], 24 rounds, rate 136, pad
  `0x01 … 0x80` (Ethereum Keccak-256), plus a `0x06`-pad SHA3-256 twin used **only** as a
  validation oracle.
- Three-way validation (`validate.py` `df4ac847…db1d` → `validation-sha3-and-vectors.txt`
  `c840c4e8…3a42`):
  - 16 inputs including the 135/136/137 and 271/272/273 rate boundaries match
    `node crypto.createHash('sha3-256')` (OpenSSL 3.6.4) **and** `hashlib.sha3_256`
    byte-for-byte → `A. ALL_SHA3_MATCH: True`.
  - `keccak256("")` = `c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470`,
    `keccak256("abc")` = `4e03657aea45a94fc7d47ba826c8d667c0d1e6e33a64a036ec44f58fa12d6c45`
    → `B. ALL_KECCAK_VECTORS_MATCH: True`.
  - ERC-20 selector table (`a9059cbb`, `70a08231`, `095ea7b3`, `18160ddd`, `23b872dd`)
    → `C. ALL_SELECTORS_MATCH: True`.
- Cross-check against `js-sha3@0.8.0` from the authorized solc prefix
  (`xcheck_js_sha3.py` `5b925fc8…9559` → `xcheck-vs-js-sha3.txt` `bc7c5819…a852`): 17
  inputs identical → `XCHECK_ALL_MATCH: True`. Corroboration, **not** my independent path.
- Cross-check against EX-03's own implementation (`evidence-ex03-impl-agreement.txt`
  `470fc8ee…48c7`): 17 inputs, full 32-byte, identical → `IMPL_AGREEMENT: True`.

### 1.2 Primary target — EX-03 `token.sol` (the seat's actual task)

Full reproducible harness: `verify-ex03.sh` (sha256 `f98376a4…10fd`); captured output
`evidence-EX03-primary.txt` (sha256 `1771acbc…c4ff`); recompute `ex03-rv1-recompute.txt`
(sha256 `59f3e304…b10b`).

| # | check | result |
|---|---|---|
| 1 | `token.sol` sha256 / size vs EX-03's stated | `497d70f2…6a6f`, 2417 B — **MATCH** |
| 1 | `keccak256.py` sha256 / size vs EX-03's stated | `7a58534b…9427`, 3812 B — **MATCH** |
| 2 | RV-1 recompute from source | K=9, listed below |
| 3 | selector-set comparison | `missing=[] extra=[]` → **MATCH 9/9** |
| 4 | 4 canonicalization guardrails + NIST-SHA3 contrast | **5/5 OK** |
| 5 | 2 event topic0 full hashes | **2/2 OK** |
| 6 | independent recompile (solc 0.8.37, default settings) | runtime **3457 B**, sha256 **`46ccaae1…395e`**, keccak256 code hash **`42e54374…fd89`** — all **MATCH** |
| 6 | PUSH4 inventory in that runtime | 10 occurrences, 9 distinct; `missing=[]`, **zero extras** → **9/9** |
| 6 | ABI-derived signatures → selectors | 9 functions → same 9 → **MATCH** |

RV-1's recomputed set (selector ← canonical signature):

```
06fdde03 name()          95d89b41 symbol()        313ce567 decimals()
18160ddd totalSupply()   70a08231 balanceOf(address)
a9059cbb transfer(address,uint256)   23b872dd transferFrom(address,address,uint256)
dd62ed3e allowance(address,address)  095ea7b3 approve(address,uint256)
```

Two things worth recording about check 3. First, a naive run of my comparison reported
**MISMATCH** with two "missing" entries — those are EX-03's *supplementary event topic0*
values, which are full 32-byte hashes explicitly labelled in its own header as
`NOT selectors` / `NOT counted in K`. Filtering to 8-hex-char tokens (true selectors) gives
`MATCH 9/9`. The planted file is correct; the shape trap is in any tool that assumes every
non-comment line is a selector. Second, check 6's code-hash agreement is a genuine
independent anchor: `keccak256(runtime)` computed by my implementation matches EX-03's
value, and my implementation is itself pinned to node/OpenSSL and js-sha3 (§1.1).

### 1.3 Secondary coverage — the other planted sets that landed in c1

`verify-planted-set.sh` (`dc28af08…4838`); evidence files `evidence-EX02-smoke.txt`
(`0d6b3354…2a0d`), `evidence-RV2.txt` (`a9c779ca…0cf4`), `evidence-EX06.txt`
(`01c15e47…e921`).

| planted set | carrier | K | selectors | dispatch sites | verdict |
|---|---|---|---|---|---|
| EX-02 `smoke/selectors.txt` | `Smoke_sol_Smoke.bin` 685 B `08299f31…8ebd` | 5 | MATCH | 5/5, 0 extras | **MATCH** |
| RV-2 `expected-selectors.txt` | `Rv2Token.runtime.hex` 1943 B `c1081a56…15e74` | 5 | MATCH | 5/5, 0 extras | **MATCH** |
| EX-06 `planted-K.json` | runtime 1789 B `9c40940e…580e` | 6 | MATCH | 6/6, 0 extras | **MATCH** |

- **EX-06's claimed `push4_site_pc` values reproduce exactly**: 31/42/53/64/75/86 equal the
  `PUSH4` opcode PC of each dispatch block found by my independent pattern search
  (semantics confirmed: EX-06's PC is the `0x63` opcode; my `imm_pc` is one byte later).
- **r4 erratum independently confirmed on real bytecode**: every probe `bytecodeOffset`
  (100/148/178/226/254/302) lands on a `0x5b` JUMPDEST and equals that selector's `JUMPI`
  target computed from my own scan → `A. ERRATUM_CONSISTENT: True`.
- **EX-06's CBOR trailer independently recomputed**: slice `[1736:1787]`, sha256
  `44e987b8…46c6` = stated; `len(code) == start + cborLen + 2`; `000825` = solc 8.37.
- **EX-07's `selector-recon.py` vectors audited**: all four 32-byte values match my keccak.
- EX-06's runtime was extracted from its own probe JSON into
  `RV-1/EX06-KdxToken.runtime.hex` (`69a15782…29ad6`), byte-identical to the digest EX-06's
  transcript records.

### 1.4 On "a DIFFERENT keccak path than EX-03"

State this precisely rather than overclaim it. No keccak library exists on this host —
`sha3`/`Crypto`/`eth_utils`/`eth_hash`/`web3`/`pysha3` MISSING in Python; `ethers`/`web3`/
`js-sha3`/`keccak`/`@noble/hashes` MISSING in node. The only keccak in the authorized
install is `js-sha3@0.8.0`, a dependency of `solc@0.8.37`. EX-03 did **not** use it: its
`keccak256.py` is a from-spec pure-Python implementation (verified — correct `0x01`/`0x81`
Keccak padding, not NIST `0x06`; `--selftest` passes 3/3, exit 0). Mine is also from-spec
pure Python. So the paths are **the same family, independently written** — different state
representation (EX-03 uses a 2-D `a[x][y]` with a transposed ROT table; I use flat
`x + 5y` lanes), and, decisively, **different validation**: EX-03 anchors on 3 published
vectors, while mine is pinned to node/OpenSSL SHA3-256 and `hashlib.sha3_256` across 16
inputs spanning rate boundaries, plus js-sha3 on 17. The two implementations agree on all
17 inputs I tested (§1.1), so the reviewer's conclusion does not rest on my implementation
being right and theirs wrong — it rests on both, against two external oracles.

## 2. Proposed changes

**None.** This seat is a reviewer. No repo file outside
`.ufo/waves/arc3-loop1-round1/claims/c1/RV-1/` and
`.ufo/waves/arc3-loop1-round1/seats/RV-1.md` was created or modified, and no patch text is
proposed: the target verified clean, so there is nothing to correct.

## 3. Before → after measurement relevant to the c1 claim

The c1 claim's falsifiable core is "planted selector count K recorded pre-probe; probe
recovers K/K selectors on **real solc-compiled** bytecode". My independent measurement of
that core — K as planted, K as recomputed by my keccak, K as present at real dispatch sites
in the carrier compiled by me from the same source:

```
EX-03 token.sol  planted K=9  RV-1 recompute 9/9 MATCH  recompiled carrier PUSH4 9/9, extras 0  -> K/K
EX-06 KdxToken   planted K=6  RV-1 recompute 6/6 MATCH  dispatch sites 6/6, extras 0             -> K/K
EX-02 Smoke      planted K=5  RV-1 recompute 5/5 MATCH  dispatch sites 5/5, extras 0             -> K/K
RV-2  Rv2Token   planted K=5  RV-1 recompute 5/5 MATCH  dispatch sites 5/5, extras 0             -> K/K
```

Commands (from `.ufo/waves/arc3-loop1-round1/claims/c1/`, with `RV1DIR` exported to the
absolute path of `RV-1/`):

```
$ bash RV-1/verify-ex03.sh                     -> exit 0, "MATCH 9/9", "9/9 with ZERO extras"
$ bash RV-1/verify-planted-set.sh EX-02/smoke/Smoke.sol EX-02/smoke/selectors.txt EX-02/smoke/out/Smoke_sol_Smoke.bin
$ bash RV-1/verify-planted-set.sh RV-2/Rv2Token.sol RV-2/expected-selectors.txt RV-2/Rv2Token.runtime.hex
$ bash RV-1/verify-planted-set.sh EX-06/evidence/KdxToken.sol RV-1/EX06-planted-bare.txt RV-1/EX06-KdxToken.runtime.hex
-> all exit 0, "MATCH — RV-1 independently reproduces the planted selector set"
```

All four carriers are genuine solc output (Smoke/KdxToken 0.8.37; RV-2 records `solc 000825`
= 8.37 in its own CBOR metadata), so the claim's "real solc-compiled bytecode" wording is
substantiated, not merely asserted.

## 4. Attacks / refutations attempted

- **"keccak-256 is just SHA3-256"** — refuted for my implementation: `keccak256("")` =
  `c5d24601…` ≠ `sha3_256("")` = `a7ffc6f8…`. A naive aliasing implementation would still
  pass the selector tests by accident; this control is what rules that out. **My path is
  not accidentally the SHA3 path.**
- **"a 4-byte selector match in the bytecode is a coincidence"** — refuted: every planted
  selector sits inside a `DUP1 PUSH4 <sel> EQ PUSH2 <dst> JUMPI` block, and in all four
  carriers the block count **equals** K with **zero** extra blocks.
- **"the planted list omits a real function"** — checked by enumerating every dispatch site
  and PUSH4 constant and diffing against the planted set: `[]` in all four carriers.
- **"my source-text extractor might invent or miss signatures"** — this attack *succeeded
  against my own tool, twice, in two different ways.*
  1. **Omission**: it missed `balanceOf(address)`, the auto-getter of
     `mapping(address => uint256) public balanceOf;` in EX-02's `Smoke.sol`, giving K=4
     against a planted K=5.
  2. **Wrong arity — the subtler and more dangerous form**: on EX-03's `token.sol` it
     emitted `name(string)`, `symbol(string)`, `decimals(uint8)` (selectors `5b43bc99`,
     `41bb0559`, `82fd60ab`) by passing the *declared type* as a parameter type. solc
     generates **no-argument** getters for scalar public state variables, so the correct
     values are `name()` `06fdde03`, `symbol()` `95d89b41`, `decimals()` `313ce567`. The
     wrong values look entirely plausible — three plausible-looking selectors that are
     simply not in the contract.
     Both defects were fixed (`recompute.py`, sha256 `76ebcf2c…9106`) and the primary
     comparison re-run **before** any verdict was recorded; the pre-fix output is retained
     at §1.2's history in this report rather than hidden.
     **Verdict: real methodological trap, two-faced. A reviewer recomputing from source
     alone can undercount K by the number of public state-variable getters, and can also
     emit plausible-but-wrong selectors for them. Any seat recomputing from source should
     cross-derive from the compiler ABI as well.**
- **"EX-03's planted file is wrong because my comparison said MISMATCH"** — refuted: the
  two extra entries are 32-byte event topic0 hashes EX-03 explicitly labels as
  non-selectors; filtering to 8-hex selectors gives `MATCH 9/9`. **My comparison tool was
  the thing at fault, not the artifact.**
- **"EX-03's stated numbers are decorative"** — refuted: artifact hashes, bytecode size,
  bytecode sha256, keccak code hash, the PUSH4 inventory, the guardrail values and the
  topic0 hashes all reproduce independently, including via a fresh solc 0.8.37 compile.
- **"EX-03's guardrails are made up"** — refuted: `transfer(address, uint256)` →
  `9d61d234`, `transfer(address,uint)` → `6cb927d8`, `TRANSFER(address,uint256)` →
  `d51e217e`, and `sha3_256("transfer(address,uint256)")[:4]` = `4b40e901` all reproduce.
- **"the probe's `bytecodeOffset` points at the PUSH4 site"** — refuted on real bytecode:
  all six EX-06 offsets are `0x5b` JUMPDESTs equal to my independently computed JUMPI
  targets; the r4 erratum holds.
- **"EX-07's tool contains a fabricated vector"** — partially sustained, cosmetic: its
  vector list (`selector-recon.py:148`) carries a bogus placeholder `70a082313deadceb…`
  for `balanceOf(address)`, silently overwritten by the branch at lines 153-154, so the
  test still asserts the true value. Not a correctness defect; dead misleading data in a
  test table. **Recommend deleting the placeholder.**
- **"EX-06's `planted-K.json` is consumable as a selector list"** — refuted: it is JSON;
  a naive `cmp` reads `{`/`"K":` as selectors and returns MISMATCH (my harness exited 1 on
  exactly this until fed the flattened `RV-1/EX06-planted-bare.txt`). **Shape trap.**

## 5. Blockers and environment

- **Primary target arrived late, and the wave is still writing.** `claims/c1/EX-03/` did
  not exist for ~10 min (20 polls, 07:01→07:08); the directory appeared empty at 07:08:44,
  `token.sol` at 07:12:33, `planted-selectors.txt` at ~07:18:54. This report reflects the
  state at 07:20Z. **Residual risk:** EX-03 may still add a `runtime.hex`/`runtime.bin`
  carrier, a probe receipt, or edit `token.sol` after this verification — the hashes in
  §1.2 are the exact bytes I verified (`token.sol` `497d70f2…6a6f`, 2417 B). If EX-03's
  carrier lands, `verify-planted-set.sh` re-runs the dispatch-site check on it verbatim;
  if `token.sol` changes, the primary verdict must be re-run, not assumed.
- **`/tmp` is unusable (environmental, now three-seat corroborated).** `/tmp` is a 16 G
  tmpfs at 80 % with the user quota exhausted: `echo hi > /tmp/rv1/probe.txt` → `Disk quota
  exceeded` (EDQUOT); inodes 86 % used. Scratch went to `/var/tmp` (and to `/dev/shm` for
  EX-06), all cleaned. EX-02's `install-receipt.txt` §8 records the same condition, EX-06
  reproduced it as an `execution_failure` with `TMPDIR` unset, and EX-03's
  `planted-selectors.txt` closes with the same host note. **Any seat that defaults scratch
  to `/tmp` will fail; set `TMPDIR`.**
- **Not a blocker, for the parent's attention:** the c1 planted sets live under four
  different names and three different shapes (`selectors.txt` bare; `expected-selectors.txt`
  bare + mutability; `planted-K.json` JSON; `planted-selectors.txt` with supplementary
  32-byte topic0 lines and a `#`-comment header). Every cross-seat review paid a shape tax,
  and two of my own tools tripped on it. A single canonical shape — 8-hex selector, space,
  canonical signature, one per line — would make review mechanical.
- **Repo hygiene, not mine:** `git status` shows `?? .ufo/gates/__pycache__/`
  (`c1-census-v10.cpython-314.pyc`, created 07:04) alongside the intended C2/C3 gate edits.
  It is another seat's residue, not RV-1's — RV-1 touched nothing under `.ufo/gates/`.
