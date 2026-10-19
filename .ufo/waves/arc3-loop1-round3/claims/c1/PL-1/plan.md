# C1 plan — EVM optimizer-leg (arc3-loop1-round3, seat PL-1, 2026-10-19)

Planner-seat artifact. Scope: turn the frozen C1 claim (optimizer-enabled carrier +
non-ERC-20-shaped carrier, planted selectors recovered K/K by `inspect-evm-interface`,
corpus knowledge entry + line-neutral map token, command A 82 → 83) into an executable
recipe with pre-measured expectations, a planted-selector methodology, prologue-class
expectations against the r1 recorded classes, and pre-written honest-stop branches.

Everything below was **pre-measured on scratch copies** (`/var/tmp/pl1-r3/`) with the
receipted round-1 solc prefix. Per rule #14, no number below transfers as identity:
executors must re-derive every sha256/count/set on their own pinned bytes and cite their
own commands. The pre-measurements exist so that a failure of any step is *detectable*
(a prediction that does not reproduce is a finding, not a nuisance).

## 0. Frozen inputs verified by this seat

- HEAD at planning time `c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311`; command A at HEAD
  (exact SCORECARD recipe, `git show`-based): `knowledge_files 82, mapped 82, missing [],
  dangling [], citation_resolved_rules 14, rule_blocks 14, coverage 10.0, depth 10.0`
  (`evidence/commandA-head.json`). The claim's "prior 82" baseline is real and green.
- Solc receipt re-verified: npm-cache content sha256 `0e1a1ab6d12c37f5503271b2c4679cd433459c884851920d148d6fb154575a51`
  (6,476,046 bytes) = the r1 receipt's tarball sha256; `solcjs --version` and
  `require('solc').version()` both read `0.8.37+commit.f401782d.Emscripten.clang`
  (`evidence/receipt-recheck.txt`). Reuse of the round-1 prefix is receipt-backed; no
  install performed.
- Host constraint standing: every solc/npx invocation needs a **disk-backed TMPDIR**
  (host `/tmp` EDQUOT) — all recipes below carry it.
- Write scope: the corpus entry + README map token land as **patch text** (freeze rule);
  scratch stays in `/var/tmp`; custody paths untouched (hash/stat only).

## 1. Carrier designs

Two carriers satisfy the claim's two shapes; a third (optional) is a cheap extra leg.
Sources are staged verbatim in `evidence/` (`OptVault.sol`, `MutMix.sol`) — byte pins
apply to those exact bytes only.

### A — `OptVault` (optimizer enabled `runs=200`; payable receive/fallback; mixed mutability)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract OptVault {
    address private _owner;
    bool private _paused;
    mapping(address => uint256) private _credit;

    constructor() { _owner = msg.sender; }

    receive() external payable {}
    fallback() external payable {}

    function deposit() external payable returns (uint256) {
        _credit[msg.sender] += msg.value;
        return _credit[msg.sender];
    }

    function withdraw(uint256 amount) external {
        require(!_paused, "paused");
        _credit[msg.sender] -= amount;
        payable(msg.sender).transfer(amount);
    }

    function creditOf(address a) external view returns (uint256) {
        return _credit[a];
    }

    function paused() external view returns (bool) {
        return _paused;
    }

    function setPaused(bool p) external {
        require(msg.sender == _owner, "owner");
        _paused = p;
    }
}
```

Design intent: `receive`+payable `fallback` exercise the **no-selector paths** of the
dispatcher (calldata-size / unknown-selector branches) without adding selectors;
`deposit` is the payable-selector leg; mutability spread nonpayable×2, view×2, payable×1.
Pre-measured (source sha256 `40af90c9f66288b33804f5e08397601db6518b9b293022e847641af8391a764d`):
runtime **776 B** sha256 `544469b7bebfda4e5c9dedc7a11af69fc77d917f1d4258a53d1aa5ed95dfde7f`
(pinned recipe §2: source key `OptVault.sol`). Compile warning: `transfer` deprecated
(expected, kept deliberately — the same warning class r1's Smoke leg carries).

### B — `MutMix` (non-ERC-20, library-bound, mixed mutability; optimizer disabled)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

library MmMath {
    function mulDiv(uint256 x, uint256 y, uint256 d) internal pure returns (uint256) {
        return (x * y) / d;
    }
}

contract MutMix {
    uint256 private _acc;
    address private _who;

    function poke() external pure returns (uint256) {
        return 7;
    }

    function viewAcc() external view returns (uint256) {
        return _acc;
    }

    function setAcc(uint256 a) external {
        _acc = a;
    }

    function scaleAcc(uint256 x, uint256 y) external returns (uint256) {
        _acc = MmMath.mulDiv(_acc, x, y);
        return _acc;
    }

    function pay() external payable {
        _who = msg.sender;
    }

    function who() external view returns (address) {
        return _who;
    }
}
```

Design intent: **no ERC-20 names or shapes**; an internal library (`MmMath`) is inlined
into the caller — the library-bound shape; all four mutability classes appear
(pure, view, payable, nonpayable). Pre-measured (source sha256
`8dcc1870d99d82533745e06468a2c685056475d9562d6f8a828be9adcba3761b`): runtime **1061 B**
sha256 `6267ef53adf978e504a564c66ffa8c62d6c5401fd7dd4606271032643d7eeccf` (key `MutMix.sol`).

### B′ — optional stretch leg: `MutMix` with optimizer ON (`runs=200`)

Same source; pre-measured runtime **497 B** sha256
`200bc9db76cc8592d0f58fdb189be9b5829e5a8db1c9742ca9e502223aab4657` (key `MutMix.sol`).
Run only if budget allows; it widens the optimizer-enabled shape coverage and lands a
below-r1 size-class datum (see §4).

## 2. Compile and identity recipe (load-bearing details, all measured)

Per carrier, in scratch:

1. **Creation leg (the claim's literal flag form):**
   `TMPDIR=<scratch-tmp> <prefix>/node_modules/.bin/solcjs --bin --abi --optimize --optimize-runs 200 -o <out> <src>.sol`
   (verified: solcjs 0.8.37 supports both flags; `--bin` emits **creation** code — there is
   **no `--bin-runtime` in solcjs 0.8.37**).
2. **Runtime leg (standard-JSON, node driver):** input with
   `settings.optimizer = { "enabled": true, "runs": 200 }` and
   `outputSelection evm.deployedBytecode.object` (+ `evm.bytecode.object`, `abi`).
3. **Source-key rule (measured drift, must be pinned):** in standard JSON the *source
   key* is embedded in the metadata and changes the bytes. Measured on OptVault:
   key `OptVault.sol` → creation `919fdef4…` / runtime `544469b7…`;
   key `src/OptVault.sol` → creation `b425e968…` / runtime `393b2891…` (both 821/776 B).
   The literal CLI leg equals the JSON leg **iff** the JSON key equals the path given to
   solcjs: measured `EQUAL_TO_JSON_key_src/OptVault.sol=true`
   (`evidence/cli-json-equivalence.txt`). Executors: pin key = the CLI-given path and
   record this equivalence as the receipt tying the flag-form to the pinned runtime bytes;
   claims of byte-exactness stay scoped to that pinned recipe.
4. Record per carrier: source text sha256, source key, solc string, optimizer settings,
   runtime/creation byte counts + sha256, ABI functions, warnings. Store hex carrier as
   `<name>.runtime.hex` (hex text + trailing newline) and raw as `<name>.runtime.bin`.
5. `TMPDIR` disk-backed on every compile and probe invocation.

## 3. Planted-selector methodology (pre-probe discipline)

Acceptance shape (per carrier, per leg): set-equality of the probe's reported selectors
with the planted set, **K/K, zero extras**, `dispatch:"abi"` on every entry, decoded
`bytecode.sha256` equal to the pinned runtime sha256, and hex-leg ≡ raw-leg payload.

Ordered steps (each leaves a file; ordering is provable by mtime):

1. Compile (step §2); write `runtime.hex`/`.bin`; record their sha256s.
2. **Probe-independent extraction, before any probe:**
   - keccak anchor: compute `keccak256(sig)[:4]` for every external-function signature
     with **two independent oracles** — r1's pure-Python keccak (EX-07 `selector-recon.py
     scan <runtime.hex> hex <sigs.txt>`) and js-sha3 from the receipted prefix
     (`node -e` one-liner). Both must agree (pre-measured agreement, `evidence/scan-*.txt`,
     `evidence/keccak-js-sha3.txt`).
   - dispatch-site record: linear-sweep disassembler (`selector-recon.py extract
     <runtime.hex> hex`) → dispatcher anchor offsets + full PUSH4 inventory +
     `dispatch_eq_sites` (push4_offset / eq / jumpi). The planted entry carries
     `push4_site_pc` per selector from *this* source, not from any probe output.
   - **Write `planted-K.json` now** (sig, selector, source-ABI mutability, push4_site_pc,
     full PUSH4 inventory incl. non-dispatch constants). This file's mtime must precede
     the first probe envelope's mtime (pre-measured prototype ordering: sigs 10:07:38 <
     first envelope 10:07:39).
3. Probe legs at `rea-agents@6.4.0` (hex + raw) and `rea-agents@6.7.0` (hex where
   feasible): `TMPDIR=<scratch-tmp> npx -y rea-agents@<pin> inspect-evm-interface
   <abs-path> <hex|raw> --format json > <envelope>.json`; record exit codes; archive
   envelopes verbatim (stdout) + `.err`.
4. Compare (item 3 vs 2): selectors set-equal; extras/missing named; per-function
   `bytecode_offset` recorded (offsets are dispatch-target JUMPDESTs — r1 erratum);
   mutability/arguments compared against the compiled ABI and **differences recorded as
   upstream-inference deltas, not failures** (see §5, pre-measured `pure → nonpayable`).

Pre-measured prototype results (to reproduce, not to copy):

| carrier | K | probe 6.4.0 hex/raw | probe 6.7.0 hex | extras | decoded sha256 |
|---|---|---|---|---|---|
| OptVault | 5 | 5/5 | 5/5 | 0 (incl. `4e487b71` trap, see §5) | `544469b7…` |
| MutMix | 6 | 6/6 | 6/6 | 0 | `6267ef53…` |
| MutMix-opt (B′) | 6 | 6/6 | — | 0 | `200bc9db…` |
| receive/fallback (A) | — | not reported as functions (no pseudo-selectors) | same | — | — |

Selectors (pre-measured; executors re-derive): OptVault `16c38b3c` setPaused(bool),
`2e1a7d4d` withdraw(uint256), `5c975abb` paused(), `75807250` creditOf(address),
`d0e30db0` deposit() payable. MutMix `0f991d72` setAcc(uint256), `18178358` poke(),
`1b9265b8` pay(), `56076947` scaleAcc(uint256,uint256), `6206a233` viewAcc(),
`d6d21dfd` who().

## 4. Prologue-class expectations vs the r1 recorded classes

r1 recorded: solc 0.8.37 emits `5f3560e01c` (PUSH0; CALLDATALOAD; PUSH1 0xe0; SHR) at
**offset 25** on its optimizer-disabled ERC-20 runtime carriers; the legacy anchor
`60003560e01c` is absent; r3-07's synthetic carrier used `60003560e01c`.

Pre-measured this planning round (independent extractor, `evidence/extract-*.txt`):

- `OptVault` (optimizer ON, runs 200): anchor `5f3560e01c` at **offset 13**;
  `60003560e01c` = −1.
- `MutMix` (optimizer OFF): anchor `5f3560e01c` at **offset 13**; `60003560e01c` = −1.
- `MutMix-opt` (optimizer ON): anchor `5f3560e01c` at **offset 13**; `60003560e01c` = −1.

Expectation for executors: **the prologue class is expected to be `5f3560e01c` on both
optimizer states; the optimizer is not expected to change the class.** The anchor
*offset* is carrier-dependent (13 here vs 25 in r1 — prepended preamble size differs);
the class, not the offset, is the expected invariant. If a probed carrier shows a
prologue class other than `5f3560e01c`/`60003560e01c`, that is the round's delta to
record (honest-stop branch HS-3), not a defect. Carrier sizes 497–1061 B also extend the
*lower* end of the probed size class (r1 carriers were ~1.8–1.9 KB); the r1 "sizes above
the probed class" unknown stays open and must be stated as such in the entry.

Mid-round note (measured by seat EX-04, `seats/EX-04.md`, §Work performed — landed while
this plan was being written): the dispatcher **layout** is not invariant even where the
prologue class is. At K=11 (optimizer-enabled `VaultB`, EX-04) the dispatch is
binary-search shaped (EQ+GT compare legs, one compare per leg); the PL-1 prototypes at
K=5/6 show the linear `DUP1 PUSH4 <sel> EQ PUSH2 <dest> JUMPI` chain. Both layouts are
EVMole-parseable (EX-04 measured K/K zero extras on its opt200 leg); the independent
extractor must state the layout it observed per carrier. Neither layout is a defect.

## 5. Expected result shapes, deltas, and honest-stop branches

Expected per-carrier delta vs r1 (both are entry-worthy observations, pre-measured):

- **`pure → nonpayable` collapse (first measured in this family):** MutMix `poke()`
  (source-ABI `pure`) is reported `nonpayable` on all three probe legs (6.4.0 hex/raw,
  6.7.0 hex) — an upstream-inference limit datum, consistent with r1's "the
  argument/mutability strings are upstream inferences" inference. Other functions agree
  with the ABI (OptVault 5/5; MutMix 5/6).
- **Error-selector trap:** OptVault's bytecode carries a non-dispatch PUSH4 constant
  `4e487b71` at pc 659 (`Panic(uint256)`), and the probe does **not** report it as a
  function — zero false positives holds incl. the error-selector class. Record the
  inventory in `planted-K.json` so this is checkable.
- **No pseudo-selectors:** `receive`/`fallback` (payable) are not reported in
  `functions`; K counts only selective functions. Executors: assert `functions` contains
  only planted 4-byte hex selectors.

Honest-stop branches (pre-written; each names the trigger, the recorded action, and the
claim consequence):

- **HS-1 typed refusal.** Trigger: probe exits 1 with a typed class
  (`invalid_request` / `execution_failure`). Action: archive envelope+err verbatim,
  record the class. Consequence: that leg is REFUSED; if it is the only optimizer leg,
  the chain reports honest stop for the claim (typed evidence), no "held" entry.
- **HS-2 parse-empty.** Trigger: exit 0 with `functions: []` **while** the independent
  extractor confirms the dispatch chain exists in the bytes (this is the optimizer-
  defeats-extractor branch; distinguish carefully from r3-07's wrong-prologue
  silent-empty, where the chain is absent — that one is a carrier defect, fix the
  compile, not a probe finding). **Wrong-encoding legs also read parse-empty at exit 0**
  (the r1 raw-on-hex class; reproduced mid-round by seat EX-04's raw(hex file) trap leg)
  — before treating parse-empty as a probe finding, confirm the envelope's decoded
  `bytecode.sha256` equals the pinned runtime sha256 (HS-7), else it is a mistargeted
  leg. Action: record envelope, anchor offset, and the extractor's chain evidence side
  by side. Consequence: report honest stop with the contrast artifact; do not silently
  re-shape carriers until the contrast is recorded.
- **HS-3 unknown prologue class.** Trigger: anchor class ∉ {`5f3560e01c`,
  `60003560e01c`}. Action: record class bytes + offset + PUSH4 inventory. Consequence:
  recorded as the round's delta; claim still evaluated on K/K (a class change alone is
  not a defect), and the delta goes into the entry's observation list.
- **HS-4 missing selectors (K−a/K).** Trigger: probe misses a planted selector.
  Action: record missing set + the missing selector's push4 site; check hex-leg/raw-leg
  and 6.7.0 to locate the variance. Consequence: claim takes the "honest stop" branch —
  entry states K−a/K and the "zero extras" clause is narrowed to extras only; no
  retry-loop to a "nicer" carrier unless the re-measurement is disclosed as a new leg.
- **HS-5 extras (>0).** Trigger: a reported selector absent from the planted set.
  Action: locate the selector in the PUSH4 inventory; if it matches a non-dispatch
  constant (error selector class), record the false positive with byte evidence.
  Consequence: entry states extras verbatim; "zero extras" is not claimed beyond
  measurement.
- **HS-6 infrastructure/receipt drift.** Trigger: solc version ≠
  `0.8.37+commit.f401782d`, cache sha mismatch, TMPDIR EDQUOT, npx resolution failure.
  Action: stop the leg, re-verify the receipt (`evidence/receipt-recheck.txt` recipe),
  keep the disk-backed TMPDIR. Consequence: never degrade to another compiler or lane;
  a receipt mismatch is an environment finding for the report.
- **HS-7 identity mistarget.** Trigger: an envelope's decoded `bytecode.sha256` ≠ the
  pinned carrier sha256 (the r1 raw-encodes-hex trap class). Action: stop, re-check the
  path/encoding pair, discard the leg. Consequence: no survivor claims from mistargeted
  legs.

## 6. Landing artifacts (patch text only)

### 6.1 Knowledge entry — `corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md`

Name fixed here so entry filename and map token agree (command A's token regex
`2026-10-\d{2}-[a-z0-9-]+` matches exactly). Skeleton (mirror the r1 entry's structure):

- header comment (staging pointer), title (`inspect-evm-interface on optimizer-enabled
  solc 0.8.37 runtime carriers — planted selectors K/K`), `source:` list (envelopes,
  planted-K, extract/scan transcripts, compile receipts), `verified-at:`, `recheck:`
  (runnable one-liner; must carry the disk-backed TMPDIR requirement; compare by
  `subject.digest.sha256` + function payload if the `ev_` id domain re-derives
  differently), REA pins (`6.4.0` + `6.7.0`, provider string, EVMole version as the r1
  entry recorded), carriers with pinned sizes/sha256s (only the *measured* carriers).
- Observations (each with envelope evidence ids): per-carrier K/K zero extras on both
  legs; hex≡raw; optimizer-enabled prologue class + offset vs r1; the `4e487b71`
  non-dispatch trap; the `pure → nonpayable` delta; receive/fallback absence from
  `functions`; B′ size-class extension.
- Inference (recovered selectors = compiled dispatch tables; mutability/arguments =
  upstream inference), Unknowns (still open: larger optimizer-enabled carriers, other
  `runs` values, Vyper, the `ev_` id domain for this verb family, `kind` classification),
  Limitations (tool-reported worker limits + upstream-inference caveat, verbatim from the
  envelope), Scope (RESULT-class, family-scoped to these pinned carriers/recipe).
- Acceptance mapping: every QUALITY.md row 1–15 satisfiable from §3/§6 evidence —
  notably row 12 (byte-exactness only for pinned fixture bytes + regenerating recipe),
  row 14/15 (identity domain: quote `subject.digest.sha256`, never a universal id
  formula), rule #11 citation form: cite stable paths (wave artifacts, corpus/knowledge)
  with stanza/step anchors; **no bare `path:line` into operator-mutable files**.

### 6.2 README map token (line-neutral)

Patch against the EVM row at the work-commit HEAD (verify the before-text with
`git show <work-commit>:corpus/README.md` first):

before (one physical line, README 190 lines):

```
| EVM | `2026-10-13-r3-evm-interface`, `2026-10-19-arc3-r1-evm-real-solc` | held — EVMole selectors recovered from a synthetic dispatcher (r3-07) and from real solc-0.8.37-compiled runtime carriers (arc3-r1); positional encoding quirk |
```

after (still one physical line — token added to the existing row, state cell refreshed;
README stays 190 lines, measured in the overlay prototype):

```
| EVM | `2026-10-13-r3-evm-interface`, `2026-10-19-arc3-r1-evm-real-solc`, `2026-10-19-arc3-r3-evm-optimizer-shapes` | held — EVMole selectors recovered from a synthetic dispatcher (r3-07) and from real solc-0.8.37-compiled runtime carriers (arc3-r1); optimizer-enabled runtime dispatch (arc3-r3); positional encoding quirk |
```

### 6.3 Command A before→after recipe (validated)

- before: run SCORECARD's command A script verbatim with `REV=$(git rev-parse HEAD)` —
  measured 82/82, missing [], dangling [], 14/14, 10.0/10.0 (`evidence/commandA-head.json`).
- after (pre-landing, seats cannot commit): **worktree-overlay mode** — copy
  `git show HEAD:corpus/README.md`, `HEAD:SKILL.md`, and all 82 `corpus/knowledge/*.md`
  into `/var/tmp` overlay; apply the entry + map-token patch texts to the overlay; run
  the same census logic reading from the overlay (script shape in
  `evidence/overlay-commandA.json`'s recipe). Prototype (stub entry): **83/83, missing
  [], dangling [], 14/14, coverage 10.0, depth 10.0**, README 190 lines.
- prior-82 byte-identity: sha256 manifest of the overlay copies vs `git show HEAD:` bytes;
  report the two manifest digests equal. The authoritative command A at the work commit
  is the parent's re-measurement at landing (the claim's 82 → 83 line).

## 7. Work split (suggested; executors choose their own splits)

- EX-a: §0 receipt re-verification + §2 carrier-A compile + §3 planted-K pre-probe +
  probes (6.4.0 hex/raw, 6.7.0 hex) + envelope archival.
- EX-b: same for carrier B (+ B′ if budget allows).
- EX-c (SC-1/SC-2): independent extraction sweep on the executors' pinned bytes (anchor
  classes, PUSH4 inventory, keccak via the second oracle) — reconciliation transcript.
- EX-d: §6.1 entry patch text.
- EX-e: §6.2 map-token patch text + §6.3 overlay run + prior-82 manifest.
- RV-1..4: adversarial legs — hex-shape variants (0x/no-newline/uppercase), mistarget
  hunt (§ HS-7), extras hunt on BOTH legs, mutability-vs-ABI table, id re-derivation
  reruns.
- CR-1/CR-2: QUALITY.md gate + citation-form (#11) + rule #14 self-identity re-derivation
  of every artifact that claims it.
- VZ-1: write-scope/consistency audit (no custody writes, no corpus writes, scratch-only
  claims), patch-text applicability check.

## 8. Evidence index (all under `claims/c1/PL-1/evidence/`, sha256s in `SHA256SUMS`)

`commandA-head.json` (baseline 82/82) · `overlay-commandA.json` (83/83 prototype) ·
`receipt-recheck.txt` (solc receipt re-verified) · `compile-summary.json` (source/runtime/
creation sha256s, ABI, warnings) · `OptVault.runtime.hex|.bin`, `MutMix.runtime.hex|.bin`,
`MutMixOpt.runtime.hex|.bin` · `extract-OptVault.txt`,
`extract-MutMix.txt` (anchors + PUSH4 inventory) · `scan-OptVault.txt`, `scan-MutMix.txt`,
`keccak-js-sha3.txt` (two keccak oracles) · `sigs-OptVault.txt`, `sigs-MutMix.txt` (planted
signature lists; mtime before first envelope) · probe envelopes
`OptVault-6.4.0-{hex,raw}.json`, `OptVault-6.7.0-hex.json`, `MutMix-6.4.0-{hex,raw}.json`,
`MutMix-6.7.0-hex.json`, `MutMixOpt-6.4.0-hex.json` · `cli-json-equivalence.txt` (source-key
drift + flag-form equivalence) · `cli-stdout.txt`.

---
*Planner note:* the plan deliberately contains **no optimistic projection**: every
"expect" statement above is a re-measurement target with a named failure branch.