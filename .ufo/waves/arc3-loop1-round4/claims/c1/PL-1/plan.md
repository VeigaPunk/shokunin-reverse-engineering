# C1 plan — the Vyper leg (arc3-loop1-round4, seat PL-1, 2026-10-19)

Planner-seat artifact. Scope: turn the frozen C1 claim (Vyper leg — at least one
Vyper-compiled contract's selectors recovered by `inspect-evm-interface` K/K
against Vyper's own ABI-derived set, OR the extractor's behavior on Vyper
dispatch shapes sealed as a typed result; corpus entry + line-neutral map token;
command A 83 → 84 with the prior 83 byte-identical) into an executable recipe
with pre-measured expectations, a planted-selector methodology, and the
pre-written honest-stop branches.

Everything below was **pre-measured first-hand by this seat** on scratch copies
(`/var/tmp/pl1-r4/`) using the wave's receipted venv. Per rule #14 no number
transfers as identity: executors re-derive every sha256/count/set on their own
pinned bytes and cite their own commands. The pre-measurements exist so a
failure of any step is *detectable* — a prediction that does not reproduce is a
finding, not a nuisance.

**Status note (the plan was commissioned against a cold tree; it landed warm).**
By the time this file was written, peers had already landed most of the
apparatus: the venv (EX-02), two carrier sources (EX-03, EX-04), the planted
tooling (EX-04, EX-05), an independent extractor + reconciler (EX-08), and a
large probe/trap matrix (EX-09, EX-10). Sections below therefore record **both**
the recipe as planned and **what actually landed**, with the measurements that
decide between them. Where my independent measurement disagrees with a peer
receipt, the disagreement is stated, not smoothed.

## 0. Frozen inputs and state verified by this seat

- Repo HEAD at planning time `015e1bab914713568f339fd53999bc180459cc40`; command A
  baseline re-measured by VZ-1 at that revision: `knowledge_files 83, mapped 83,
  missing [], dangling [], citation_resolved_rules 14, rule_blocks 14, coverage
  10.0, depth 10.0` (`claims/c1/VZ-1/evidence/baseline-commandA.json`). The
  claim's "prior 83" baseline is real and green.
- The authorized install landed: `.ufo/waves/arc3-loop1-round4/tools/vyper-venv/`
  (EX-02, `install.log`, `smoke/compile-receipt.txt`).
- Write scope: the corpus entry + README map token land as **patch text**;
  scratch stays in `/var/tmp`; custody paths hash/stat only.
- Standing host constraint: every npx/solc/vyper invocation needs a **disk-backed
  TMPDIR** (`/tmp` EDQUOT); all recipes below carry it.

## 1. Venv install approach and the python-compatibility pre-check

### 1.1 The pre-check, run before any install decision (this seat, measured)

Host interpreters present:

| interpreter | path | version |
|---|---|---|
| system | `/usr/bin/python3` → `python3.14` | 3.14.7 |
| uv-managed | `~/.local/share/uv/python/cpython-3.11-*/bin/python3.11` | 3.11.17 |
| uv-managed | `~/.local/share/uv/python/cpython-3.12-*/bin/python3.12` | 3.12.15 |
| uv-managed | `~/.local/share/uv/python/cpython-3.13-*/bin/python3.13` | 3.13.16 |

No `pip`/`pip3` on PATH; `uv 0.13.0` present; system python is PEP-668
`EXTERNALLY-MANAGED`. Every interpreter bootstraps `venv` + `ensurepip` cleanly
(all four venvs created, `pip 24.0`/`25.0.1`/`26.2.1` respectively).

`pip install --dry-run vyper` per interpreter — the decisive table:

| interpreter | resolved vyper | deps all wheels? | note |
|---|---|---|---|
| 3.11.17 | **0.4.3** | yes (8 artifacts) | |
| 3.12.15 | **0.4.3** | yes (8 artifacts) | |
| 3.13.16 | **0.4.3** | yes (8 artifacts) | |
| 3.14.7 | **0.4.1** under `--only-binary=:all:` | **no** — `immutables 0.21` has no cp314 wheel | silent downgrade |

**The trap this pre-check exists to catch:** vyper 0.4.3's `requires_python` is
`<4,>=3.10`, so 3.14 is *nominally* in range — but the newest release cannot be
installed wheel-only on 3.14, and a bare `pip install vyper` there resolves the
**older 0.4.1** without an error. A receipt that records only "vyper installed"
on 3.14 can therefore be a 0.4.1 receipt. Two acceptable resolutions:
(a) pin an interpreter in 3.11–3.13 where the whole set is wheel-backed; or
(b) stay on 3.14 and let pip build `immutables` from sdist (the host has
gcc/clang/rustc/make and `Python.h`), then **verify the installed version is
0.4.3, not 0.4.1**.

### 1.2 What actually landed, and my independent re-derivation (rule #14)

EX-02 took path (b): venv on **3.14.7**, `immutables` source-built into
`immutables-0.21-cp314-cp314-linux_x86_64.whl` (EX-01's build-only probe records
sha256 `de9ab13c…`), and the install log shows
`Successfully installed … vyper-0.4.3 …`. My pre-check predicted the trap and
named the fallback; the executor's path is valid and the outcome is the
non-downgraded one. Recorded because the *reason* the 3.14 path is safe here
(the toolchain) is a host fact that could change.

Re-derived first-hand by this seat (not copied from EX-02's receipt):

```
$ .ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper --version
0.4.3+commit.bff19ea2
$ .ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/python -V
Python 3.14.7
sha256 bin/vyper                          615f792c6bc1bdf87cbc4612420a331ec108246d9debadbb3f3b9efa8209dd10
sha256 bin/vyper-json                     c64126b9686ccb76a27620cf07ac9e79a26a729d6e0c4624097d3777b02766fe
sha256 bin/python                         d78f9cf7178ecff09963551399855543c297f37ac207e626228bfe43cb26a70c
sha256 vyper/*.py tree digest             526cf63be87f81c71f243767a0983186691946d4c39c5eed778e57c0c7b6ba56
sha256 vyper-0.4.3.dist-info/RECORD       8bc98248714c40f899823bb568fc3f11b659ed013f375a863bb2cc9ce13cdceb
pip list --format=freeze: asttokens==3.0.2 cbor2==5.9.0 immutables==0.21 lark==1.3.1
  packaging==26.3 pip==26.2.1 pycryptodome==3.24.1 vyper==0.4.3 wheel==0.48.0
vyper_git_commithash: bff19ea2
```

Wheel pin (upstream identity, cross-checked against PyPI's own digest by EX-01):
`vyper-0.4.3-py3-none-any.whl` sha256
`3b9671727c888363740dc678e60336759871487d0e4e9fdd973048fa9635c4fd`
(403,104 B). Note the wheel is `py3-none-any` — pure Python; the only
platform-tagged artifact in the set is `immutables` (plus `cbor2`,
`pycryptodome`).

**Executor rule (if any seat re-installs or re-pins):** the receipt must carry
`vyper --version` output *and* the resolved version string from
`pip list`/`dist-info`; a bare "vyper installed" line is insufficient on 3.14.
Never fall back to a system-wide install; the wave authorizes exactly one
install, into this venv.

### 1.3 Compile invocation (measured; carry the TMPDIR discipline)

```
V=.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper
TMPDIR=/var/tmp/<scratch>/tmp $V -f abi               <src>.vy   # ABI JSON
TMPDIR=/var/tmp/<scratch>/tmp $V -f method_identifiers <src>.vy   # vyper's own selector set
TMPDIR=/var/tmp/<scratch>/tmp $V -f bytecode_runtime  <src>.vy   # runtime hex (0x-prefixed)
TMPDIR=/var/tmp/<scratch>/tmp $V -f bytecode          <src>.vy   # creation hex
```

`-f` accepts a comma list; `bytecode_runtime`/`bytecode` are the two legs this
round needs. Vyper has **no** source-key/standard-JSON drift of the kind r3
measured on solcjs (the Vyper CLI compiles a file path directly); the
solc-era "source key changes the bytes" rule does not transfer and must not be
claimed for Vyper. Optimization mode defaults to `"gas"`; `--optimize codesize`
and `--experimental-codegen` exist and are **unvisited** this round (Unknowns).

## 2. Carrier designs

Claim requirement: **≥4 external functions, mixed mutability.** Four independent
Vyper carriers exist this round; all four satisfy it, and the chain now holds
both the ERC-20-absent and ERC-20-present controls.

| carrier | seat | shape | externals | mutability spread | ERC-20 |
|---|---|---|---|---|---|
| `CarrierV` | EX-04 | payable vault, `__default__` payable | 15 | payable 2 / nonpayable 5 / view 7 / pure 1 | absent (checked ×8) |
| `StewardToken` | EX-03 | ERC-20-shaped token + steward | 22 | payable 1 / nonpayable 9 / view 11 / pure 1 | **present** |
| `Ex09Vault` | EX-09 | small vault | 7 | nonpayable/view/pure/payable | absent |
| `CarrierW` | **PL-1** (this seat) | prototype, constructor with arg, fixed-array/bytes/string params | 9 | payable 2 / nonpayable 2 / view 4 / pure 1 | absent |

Design rules that make a carrier a *test* rather than a demo (all exercised):

1. **At least one payable external** — a payable entry is the one whose
   `stateMutability` the upstream inference gets right/wrong most visibly.
2. **A `__default__` (Vyper fallback)** — mandatory, because it is the trap in
   §3.2: it appears in `method_identifiers` but is not a selector-bearing ABI
   function.
3. **At least one signature needing canonicalization** — Vyper source types are
   not ABI types (`String[32]`, `Bytes[32]`, `uint256[2]`), so the planted set
   must be derived after canonicalization, not by string-copying the source.
4. **At least one selector with a leading zero byte** — the `method_identifiers`
   emission strips it (§3.3). Two of CarrierV's 15 and one of CarrierW's 9 hit
   this naturally; a carrier that does not should be noted, not forced.
5. **Zero ERC-20 selectors in at least one carrier** — so a K/K result cannot be
   an artifact of a well-known table.

`CarrierW` is a **prototype for pre-measurement**, not a claim carrier; the
claim rests on the executors' carriers. Its source is staged verbatim at
`claims/c1/PL-1/evidence/src/CarrierW.vy` (1,711 B, sha256
`5e66c85d2cfe87e4fe35de96b44a44ccfcd84d9a72641069fb1b38a204f0e282`) and its
compiled runtime hex file at `evidence/CarrierW.runtime.hex` (1,661 B of hex
text, file sha256
`406e45ea3c8ab495b18e32ab9933df81ad2fc4588f78e24079ef70209cd24214`), whose
decoded 829 bytes hash to
`67d1d88fc65824acbe75b9f7304bdaf1f122f7173b97b284d3e9f53687115858`.

## 3. Planted-selector methodology (pre-probe discipline)

Acceptance shape per carrier per leg: set-equality of the probe's reported
selectors with the planted set, **K/K, zero extras**, `dispatch:"abi"` on every
entry, decoded `bytecode.sha256` equal to the pinned runtime sha256, and hex-leg
≡ raw-leg payload.

### 3.1 Canonical signature rule (measured, load-bearing)

The keccak input is the **ABI canonical** signature, not the Vyper source
spelling. Measured on `CarrierW`:

```
tag(String[32],Bytes[32],uint256[2],bool)  (source spelling)  -> 9d51c97e   WRONG
tag(string,bytes,uint256[2],bool)          (canonical)        -> 7425570b   CORRECT
tag(string,bytes,uint256[],bool)           (bad array)        -> c12db4c7   WRONG
```

and `7425570b` is what vyper's own `method_identifiers` emits for the same
function. **Do not derive the planted set from the source text.** Derive it from
the compiled `-f abi` output: `type == "function"` entries only, name +
`(` + canonical types + `)` where a `tuple` becomes `(...)` + array suffix.

### 3.2 The `__default__` phantom (the trap this round exists to expose)

Vyper's `method_identifiers` emits an entry for the fallback:

```
EX-04 CarrierV:  method_identifiers n=16   ABI function entries n=15
                 non-function key: __default__() -> 0x89402a72
EX-03 StewardToken: method_identifiers n=23   ABI function entries n=22
                 non-function key: __default__() -> 0x89402a72
```

Measured: `bytes.fromhex('89402a72') in runtime_bytes` is **False** on both
carriers — the value is a keccak of the literal name `__default__()`, is never
dispatched, and the ABI carries the fallback as `{"type": "fallback"}` with no
`name`. A planted set built naively from `method_identifiers` keys would
therefore be **K+1 with a phantom**, and a K/K result would be impossible to
report honestly.

**Rule:** the planted set is the ABI's `type == "function"` entries only.
`method_identifiers` is used as a *secondary* oracle (§3.4) after dropping
non-function keys, never as the primary source.

### 3.3 Leading-zero stripping in `method_identifiers` (measured)

Vyper emits the 4-byte value with leading zero nibbles stripped:

```
0xc751377   -> canonical 0c751377   (fee_of(uint256,uint256))
0x776076f   -> canonical 0776076f   (is_owner(address))
```

EX-05 measured the same on the same carrier (`planted-vs-method-identifiers.txt`:
"two false mismatches; normalization is required"). Any comparison of the
planted set against `method_identifiers` must `zfill(8)`; a naive string compare
reports false mismatches that look like extraction failures.

### 3.4 Two independent oracles (both required)

1. **ABI-derived keccak** — canonical signature → keccak256 → first 4 bytes,
   computed by **two implementations that share no code**, e.g. `js-sha3@0.8.0`
   from the round-1 receipted prefix
   (`.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/js-sha3/`, and
   `node:crypto`'s `keccak-256`), plus a pure-Python keccak. This seat validated
   **five** available oracles against the standard vectors on 2026-10-19:
   `node:crypto` (`c5d24601…`, `a9059cbb`), `js-sha3@0.8.0` (same),
   `EX-08/recon.py keccak-test` (VECTORS PASS), `EX-10/keccak.py vectors`
   (VECTORS PASS), `EX-05/keccak_ref.py` (selfcheck OK). Cross-check against the
   venv's `pycryptodome` (same venv as the compiler) agreed with vyper's own
   `method_identifiers` 10/10 on CarrierW.
2. **Byte-level census** — an independent linear-sweep disassembler that reads
   the PUSH4 immediates and the dispatch structure **without** invoking the
   probe (`EX-08/recon.py extract` is landed and tested; `EX-04/evidence/keccak256.py`
   + `keccak256.js` are the seat's own pair). The census also reports the
   **non-dispatch PUSH4 constants** so "zero extras" is checkable, not asserted.

### 3.5 Ordering (provable by mtime)

1. Compile → write `runtime.hex`/`.bin`, record sha256s.
2. Derive the planted set (ABI-canonical keccak, two oracles) and the byte census
   → **write `planted-K.json` now**. Its mtime must precede the first probe
   envelope's mtime. (Precedent: EX-04 `recorded_utc 2026-10-19T14:05:46.622429Z`
   vs its first envelope at 14:05:59Z.)
3. Probe legs.
4. Reconcile planted vs probe vs census; name missing/extra explicitly.

## 4. Pre-measured expectations (probe matrix, first-hand)

All legs below were run by **this seat** on 2026-10-19 with
`TMPDIR=/var/tmp/pl1-r4/tmp`, pin `rea-agents@6.4.0` / `6.7.0`, provider
`evmole-interface evmole@0.9.3`. Envelopes archived under
`claims/c1/PL-1/evidence/probe/`.

| carrier | bytes | K (ABI fn) | legs | result | decoded sha256 |
|---|---|---|---|---|---|
| `Smoke` (EX-02) | 168 | 4 | 6.4.0 hex | **4/4**, zero extras | `415e6b1b…` |
| `CarrierW` (PL-1) | 829 | 9 | 6.4.0 hex, 6.7.0 hex | **9/9**, zero extras | `67d1d88f…` |
| `CarrierV` (EX-04) | 1,562 | 15 | 6.4.0 hex+raw, 6.7.0 hex+raw | **15/15**, zero extras | `57d6fd0a…` |
| `StewardToken` (EX-03) | 3,337 | 22 | 6.4.0 hex | **22/22**, zero extras | `1846469b…` |
| `EX-04 creation.hex` | 1,637 | — | 6.4.0 hex | **0 functions** (parsed-and-empty) | `3c667396…` |

Verified independently in `evidence/verify.txt`: for each runtime leg the
probe's set equals the set derived by `EX-08/recon.py`'s pure-Python keccak over
the compiled ABI, missing `[]`, extra `[]`, and the decoded
`normalized_result.bytecode.sha256` equals the sha256 of the carrier bytes.
`CarrierV`'s set is identical across hex/raw and both pins, and matches EX-04's
own planted K=15, RV-2's independent oracle, and vyper's `method_identifiers`
(after §3.2/§3.3 normalization).

**Verdict available to the chain today:** the claim's first arm (K/K against
Vyper's own ABI-derived set) is **pre-measured green on four carriers spanning
168–3,337 B**, so the honest-stop branches below are insurance, not the expected
path.

### 4.1 The structural finding: Vyper dispatch is a computed jump table

This is the round's real content and must be in the entry.

Prologue (all four carriers, offset 0):

```
5f 35 60 e0 1c            PUSH0 CALLDATALOAD; PUSH1 0xe0 SHR
60 02 60 <K> 82 06         PUSH1 2; PUSH1 K; DUP3 MOD        <- bucket = selector % K
60 01 1b                   PUSH1 1 SHL                        <- bucket * 2
61 <table> 01              PUSH2 <table> ADD                  <- table base
60 1e 39                   PUSH1 0x1e CODECOPY
5f 51 56                   PUSH0 MLOAD; JUMP                  <- MLOAD = BIG-ENDIAN uint16
```

so the entry is `uint16_be(code[table + 2*(sel % K)])` — a **computed jump
table**, not solc's compare tree. Measured on `CarrierV` (K=15 declared
externals, 13 buckets):

```
table @0x600, BE-read: [668, 1511, 1291, 1024, 1452, 1087, 1341,
                        1511, 1424, 1396, 898, 1511, 24]
  - every entry is a JUMPDEST (13/13)
  - 0x5e7 (1511) appears 3x: the empty-bucket sentinel for K=15 > 13 buckets
  - reported bytecodeOffset = table[sel % K] + 12 for the bucket's first
    occupant; collision-resolved occupants differ (-236, -512, -75, -157, -39)
```

Two consequences executors must state, not assume:

**(a) The reported `bytecode_offset` is NOT a JUMPDEST on Vyper.** Measured
across all three carriers: 0/15, 0/9, 0/22 offsets land on `0x5b` — but
**46/46 are immediately preceded by `0x57` (JUMPI)**, i.e. the value is the
handler body's fall-through address after each compare `JUMPI`. The r1/r3
reading ("every reported offset lands on a JUMPDEST") is **false for Vyper** and
must not be carried into the entry as a general rule. RV-2 reached the same
conclusion independently (`RV-2/evidence/vyper-dispatch-shape.txt`).

**(b) Vyper compares via `XOR` (`0x18`), not `EQ` (`0x14`).** `CarrierV` carries
15 `DUP2-XOR` sites and only 4 `EQ` byte occurrences. An extraction method that
keys on `EQ` (the solc idiom) sees nothing here; a method that keys on `PUSH4`
+ comparison will over-report unless it knows the `XOR`/`JUMPI` pairing. The
byte census must therefore report which comparison opcode it used, per carrier.

Non-dispatch PUSH4 constants measured (zero false positives from the probe):
`08c379a0` (`Error(string)`) ×6 in CarrierV, ×2 in CarrierW; plus the 4-byte
ASCII fragment `69656e74` ("ient", from the revert string `"insufficient"`) at
pc 731 in CarrierV. CarrierV's 21 PUSH4 immediates = 15 selectors + 6 error
constants; CarrierW's 11 = 9 selectors + 2 error constants.

### 4.2 Envelope deltas (Vyper vs solc), measured

- `raw_result.metadata` is **`null`** on every Vyper runtime leg at both pins —
  no CBOR trailer decode (Vyper's trailer is `...a164736f6c6343`-free; the tail
  is the archive/integrity bytes, and no `solc`/`ipfs` ASCII appears). solc
  carriers keep their CBOR decode. Record as a delta, not a defect.
- `relationship_coverage` is **absent at 6.4.0 and present (value `null`) at
  6.7.0**, with the limitation list at 6 vs 7 lines — the r3 Unknown about this
  key **generalizes to Vyper**. EX-07's pre-registration predicted exactly this
  from three carriers × hex/raw; my legs confirm it on Vyper.
- Creation blobs report **0 functions** with a decoded sha256 equal to the
  creation blob's own sha256. Both a Vyper creation blob (EX-04, `3c667396…`)
  and a solc creation blob (EX-09's control, `ac614a6e…`) behave this way.
  Measured why this is *not* the r1 erratum's "creation blobs carry no runtime
  dispatch table": the runtime **is** embedded in the creation blob
  (EX-04: runtime at byte 20 of 1,637; the jump table at runtime `0x600` sits
  inside that copy) — the probe simply does not descend into it. This is a
  **parsed-and-empty** result in the QUALITY row 11 sense, and must be labeled
  as such: the dispatch surface was parsed and came back empty, not excluded
  from inventory.

## 5. Honest-stop branches (pre-written; each names trigger, action, consequence)

- **HS-1 — venv infeasible after one bounded attempt.** Trigger: no host/venv
  interpreter is vyper-compatible after **one** bounded attempt (install exits
  non-zero, or resolves a vyper whose version ≠ the pinned 0.4.3). Action: stop
  the leg; record the interpreter, the exact command, the exit code, and the
  resolver output verbatim; do **not** install anything else, do not fall back
  to a system-wide install, do not switch interpreters twice. Consequence:
  recorded as "not verified — venv infeasible"; the claim lands the honest-stop
  form with the record, no corpus entry asserting recovery.
  *This branch did not trigger: EX-02's install succeeded and this seat
  re-derived `0.4.3+commit.bff19ea2` first-hand.*
- **HS-2 — typed refusal.** Trigger: a probe leg exits 1 with a typed class
  (`invalid_request` / `execution_failure`). Action: archive envelope + stderr
  verbatim, record the class and the exact argv. Consequence: that leg is
  REFUSED; if it is the only Vyper leg, the chain reports the honest stop with
  the typed evidence and lands no "recovered" entry.
  *Not triggered: every leg this seat ran exited 0.*
- **HS-3 — partial recovery (K−a/K).** Trigger: the probe misses ≥1 planted
  selector. Action: record the missing set, each missing selector's `PUSH4` site
  and its `sel % K` bucket from the jump table, and whether it is a
  collision-resolved occupant (the bucket's 2nd/3rd entry). Check hex vs raw and
  6.4.0 vs 6.7.0 to locate the variance. Consequence: **land the exact partial
  set — no costume, no re-shaping the carrier to a nicer K**; the entry states
  K−a/K and the "zero extras" clause is narrowed to extras only. If a re-run is
  disclosed as a new leg, it is a new leg, not a correction.
  *Not triggered: 4/4, 9/9, 15/15, 22/22.*
- **HS-4 — extras > 0.** Trigger: a reported selector absent from the planted
  set. Action: locate it in the PUSH4 census; if it matches a non-dispatch
  constant (the `08c379a0` error class, the ASCII-fragment class, or a
  jump-table byte misread as an immediate), record the false positive with byte
  evidence. Consequence: entry states extras verbatim; "zero extras" is not
  claimed beyond measurement.
- **HS-5 — parse-empty with a live dispatch surface.** Trigger: exit 0,
  `functions: []`, while the independent extractor confirms a dispatch structure
  exists in the bytes. Action: **first** confirm the envelope's decoded
  `bytecode.sha256` equals the pinned carrier sha256 — if it does not, this is
  HS-7, not a finding (the r3 raw-on-hex-text trap class). Then record the
  envelope, the prologue class, and the extractor's chain evidence side by side.
  Consequence: honest stop with the contrast artifact; do not re-shape carriers
  until the contrast is recorded. (Distinguish from the *creation-blob* case in
  §4.2, where the tool's zero is expected and is a parsed-and-empty result.)
- **HS-6 — unknown prologue class.** Trigger: the prologue class is not
  `5f3560e01c` and not the legacy `60003560e01c`. Action: record class bytes +
  offset + PUSH4 inventory + the comparison opcode. Consequence: recorded as the
  round's delta; the claim is still evaluated on K/K — a class change alone is
  not a defect. *(Measured this round: Vyper uses `5f3560e01c` at offset 0, i.e.
  the same class as solc 0.8.37, but a different **dispatch structure** — the
  class is invariant while the layout is not. Do not infer layout from class.)*
- **HS-7 — identity mistarget.** Trigger: an envelope's decoded
  `bytecode.sha256` ≠ the pinned carrier sha256. Action: stop, re-check the
  path/encoding pair, discard the leg. Consequence: no survivor claims from
  mistargeted legs.
- **HS-8 — receipt/identity drift.** Trigger: `vyper --version` ≠
  `0.4.3+commit.bff19ea2`, venv digest drift, TMPDIR EDQUOT, npx resolution
  failure. Action: stop the leg, re-derive the venv identity (§1.2 recipe), keep
  the disk-backed TMPDIR. Consequence: never degrade to another compiler, pin, or
  lane; a receipt mismatch is an environment finding for the report.

## 6. Landing artifacts (patch text only)

### 6.1 Knowledge entry

Filename and map token must agree; command A's token regex is
`2026-10-\d{2}-[a-z0-9-]+`. Skeleton mirrors the r1/r3 entries:

- header comment (staging pointer), title naming the Vyper leg, `source:` list
  (envelopes, planted-K, extract/census transcripts, compile receipt, venv
  receipt), `verified-at:`, `recheck:` (runnable one-liner; must carry the
  disk-backed TMPDIR requirement and compare by decoded `bytecode.sha256` +
  function payload, never by `ev_` id — the id is path-sensitive).
- REA pins (`6.4.0` + `6.7.0`), provider `evmole-interface` / EVMole `0.9.3`.
- Carriers with pinned sizes/sha256s — only *measured* carriers.
- Observations, each with an envelope id: per-carrier K/K zero extras; hex ≡ raw;
  **the computed jump table + `sel % K` bucket arithmetic**; **the offset
  semantics** (fall-through after `JUMPI`, 46/46, never a JUMPDEST);
  **XOR-vs-EQ compare idiom**; the `__default__` phantom; leading-zero
  stripping; `08c379a0` non-dispatch constants and zero false positives;
  `raw_result.metadata: null` on Vyper; `relationship_coverage` 6.4.0-absent /
  6.7.0-present; creation blobs parsed-and-empty.
- Inference (recovered selectors = the compiled dispatch tables; argument/
  mutability strings are upstream inferences), Unknowns (still open: optimizer
  modes `codesize`/`gas` and `--experimental-codegen`; `evm-version` targets;
  Vyper versions other than 0.4.3; the `ev_` id domain; carrier sizes above
  ~3.3 KB; deployment/chain identity — never claimed by the tool), Limitations
  (verbatim from the envelopes), Scope (RESULT-class, family-scoped to the
  pinned carriers and this recipe).
- Acceptance mapping: QUALITY rows 1–15 satisfiable from §3/§4/§6 evidence —
  notably row 11 (creation-blob zero = parsed-and-empty, stated), row 12
  (byte-exactness only for pinned fixture bytes + regenerating recipe), rows
  14/15 (quote `subject.digest.sha256`, never a universal id formula), rule #11
  citation form (stable paths, no bare `path:line` into operator-mutable files).

### 6.2 README map token (line-neutral)

Patch against the EVM row at the work-commit HEAD. Verified before-text
(`corpus/README.md`, one physical line, README is 190 lines):

```
| EVM | `2026-10-13-r3-evm-interface`, `2026-10-19-arc3-r1-evm-real-solc`, `2026-10-19-arc3-r3-evm-optimizer-shapes` | held — EVMole selectors recovered from a synthetic dispatcher (r3-07) and from real solc-0.8.37-compiled runtime carriers (arc3-r1); positional encoding quirk |
```

after (still one physical line — one token added to the existing row, state cell
refreshed; README stays 190 lines):

```
| EVM | `2026-10-13-r3-evm-interface`, `2026-10-19-arc3-r1-evm-real-solc`, `2026-10-19-arc3-r3-evm-optimizer-shapes`, `2026-10-19-arc3-r4-evm-vyper-leg` | held — EVMole selectors recovered from a synthetic dispatcher (r3-07), real solc-0.8.37-compiled runtime carriers (arc3-r1), optimizer-enabled shapes (arc3-r3) and Vyper-0.4.3-compiled runtime carriers (arc3-r4); positional encoding quirk |
```

The entry stem must equal the token's final component; VZ-1/RV-2 re-derive the
line count and the row's before/after sha256 at grade time.

### 6.3 Command A before → after

- before: recipe A verbatim with `REV=015e1bab…` — `83/83, missing [],
  dangling [], 14/14, 10.0/10.0` (VZ-1 baseline; executors re-run it themselves).
- after (seats cannot commit): **worktree-overlay** — copy
  `git show HEAD:corpus/README.md`, `HEAD:SKILL.md` and the 83
  `corpus/knowledge/*.md` into `/var/tmp` overlay; apply the entry + map-token
  patch texts; run the same census logic against the overlay. Expect
  `84/84, missing [], dangling [], 14/14, 10.0/10.0`, README 190 lines.
- prior-83 byte-identity: sha256 manifest of the overlay copies vs `git show
  HEAD:` bytes; report the two manifest digests equal. The authoritative
  measurement at the work commit is the parent's re-run at landing.

## 7. Work split (suggested; executors choose their own)

- **EX-02** — install + venv receipt + compile smoke. *(landed)*
- **EX-03 / EX-04** — the two claim carriers (ERC-20-present / ERC-20-absent),
  compile receipts, planted-K pre-probe. *(landed)*
- **EX-05** — planted tooling, two-oracle keccak, `__default__`/zfill analysis.
  *(landed)*
- **EX-06** — probe legs + envelope archival for the claim carriers. *(pending —
  the seat dir is empty as of this writing; the envelopes this seat produced are
  planner pre-measurements and must not be presented as EX-06's legs.)*
- **EX-08** — independent extraction + 3-way reconciler. *(landed; tested)*
- **EX-09** — trap matrix (encoding, creation/runtime contrast, non-bytecode
  inputs). *(landed)*
- **EX-10** — id-stability battery. *(landed)*
- **SC-1 / RV-1 / RV-2 / CR-1 / VZ-1** — scribe, adversarial legs, grade,
  citation gate, write-scope audit.
- **PL-1** (this seat) — plan + pre-measurement.

## 8. Evidence index (`claims/c1/PL-1/`, all first-hand)

- `evidence/src/CarrierW.vy` — prototype carrier source.
- `evidence/CarrierW.runtime.hex`, `CarrierW.abi.json`,
  `CarrierW.method-identifiers.json` — compiled by this seat with the wave venv.
- `evidence/verify.txt` — the K/K verification transcript (probe set vs
  ABI-derived set vs carrier bytes, per carrier, with the phantom-selector and
  leading-zero checks).
- `evidence/probe/*.json` — eight envelopes: `Smoke-6.4.0-hex`,
  `CarrierW-6.4.0-hex`, `CarrierW-6.7.0-hex`, `CarrierV-6.4.0-hex`,
  `CarrierV-6.4.0-raw`, `CarrierV-6.7.0-hex`, `EX03-6.4.0-hex`,
  `EX04creation-6.4.0-hex`.
- Scratch (not a repo artifact): `/var/tmp/pl1-r4/` — venv dry-run reports
  (`report-{bin,any}-*.json`, the interpreter pre-check), compile outputs,
  jump-table analysis.

---
*Planner note:* the plan contains **no optimistic projection**. Every "expect"
above is a re-measurement target with a named failure branch; the one
pre-measured-green statement (§4) is scoped to the legs this seat actually ran,
and the offset-semantics finding is stated as a **refutation** of the r1/r3
reading rather than as a generalization.
