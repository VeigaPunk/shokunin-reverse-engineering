# chain-ledger.draft — arc3-loop1-round4 · chain c1 (EVM family closure — the Vyper leg)

<!-- SEAT SC-1 (chain c1, role scribe). status: DRAFT — point-in-time snapshot;
     the parent regenerates/repins at integration. generated-utc: 2026-10-19T14:12Z.
     repo-HEAD pin: 015e1bab914713568f339fd53999bc180459cc40 (all reads).
     frozen sequence (claims-frozen.md): install → compile → probe(raw|hex) →
     reconciliation → control → rerun. -->

## Method and evidence rules

- Every sha256 below was **computed by this seat** with `sha256sum` at capture
  time (2026-10-19T14:04–14:12Z), never copied from a producing seat's text.
  Paths are relative to the repo root unless noted. The full recompute table is
  `SC-1/c1-inventory.txt` (every file under `claims/c1/`, pycache excluded).
- Status vocabulary: **LANDED** · **PARTIAL** · **GAP** (absent at capture) ·
  **VOID** (0 bytes). "An unrun check has not passed" — GAP rows carry no
  verdict; claim adjudication belongs to reviewers/parent.
- Recompute: `sha256sum <path>` per row; whole-tree snapshot command in footer.
- This seat is a scribe: it ran the probes first-hand (R3/R4/R6/R7 below) to
  give the ledger a measured spine, but it proposes no repo-surface change.

## Frozen inputs (SC-1 computed)

| input | sha256 |
|---|---|
| `.ufo/waves/arc3-loop1-round4/claims-frozen.md` | `096b8b6add977ec6807d86b5051f3c72a757739bb65aeca07b3a169f48faa539` |
| `SKILL.md` (command-A input) | `5eec51c089e57f5d5806b4728261fb8c959637580a73aed7be4cddc1866b8f3f` |
| `corpus/README.md` (command-A input) | `a451ad1664cda0cb87f3a76e974de818a1e401387bad6251b98cd6b0df8ede3a` |
| `LOG.md` | `508aaa8b0e610435dc5ee9cf7ec88f5e7a208a77fc7f68ff40eef378a05b5889` |
| `SCORECARD.md` | `21042196b51dae57182c2d25b014f8928a4360139bbecd72127dac1031c18ef7` |
| `.ufo/gates/c1-census-v10.py` | `d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5` |
| `.ufo/gates/citation-drift/citation-drift-probe.py` | `e2665074a685ca65966f291f98b5e264b15c67827982811a24dc73b16497a36a` |
| `.ufo/gates/citation-drift/pointer-table.json` | `1b3ab955478b5d40f428d733bc482e4037f83bceaa1a39e9046ef82ca6d42d4b` |
| `.ufo/gates/citation-drift/expected.json` | `9df0452c5c132ad00e211781ebccc332de9b1aa1af7eeb50c91bcb0ed2015763` |
| `.ufo/gates/custody-pair/custody-pair.py` | `7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09` |
| `.ufo/gates/custody-pair/README.md` | `f30df42e0a547a0aefd21590c0f975acf06d91161fcb6db77c8934960efeb193` |
| line counts at HEAD | README 190 · SKILL 390 · LOG 1487 · SCORECARD 1580 · PROVINCE 162 |

## Step ledger — one row per step

| # | step | status | key artifacts (path → sha256 prefix) | producer |
|---|---|---|---|---|
| R0 | custody pre-pair (boundary, frozen rule) | GAP (not captured at this seat's close) | custody paths stat/hash read-only all round; `EX-02/custody-stat-readonly.txt` `67b1014e…` (re-derived 14:25Z after RV-2's A2 caught this seat's stale pin `f9ae3dbc…`; the producing seat revised the file between this seat's read and the grade) is the install-window capture | CU-1 (+EX-02) |
| R1 | install (the round's ONE authorized install) | LANDED | `EX-02/install-receipt.txt` `48b942df…`; `EX-02/install.log` `3971d1b7…`; wheel `EX-02/vyper-0.4.3-py3-none-any.whl` `3b967172…`; venv manifest `EX-02/venv-manifest.sha256` `63cb2185…`; `EX-02/attest-output.txt` `3ff616f1…`; `EX-01/env-census.txt` `87e6ba35…` | EX-02, EX-01 |
| R2 | compile (Vyper 0.4.3 carriers, on-host) | LANDED | `EX-02/smoke/{Smoke.vy,compile-receipt.txt,Smoke.runtime.hex,method-identifiers.txt}` (`34bf2c0c…` / `14eb08d7…` / `40650adf…` / `a9a2fe38…`); `EX-04/src/CarrierV.vy` `f4f94727…` + `EX-04/out/` (runtime.bin `57d6fd0a…`, runtime.hex `e0b1021c…`, creation.bin `3c667396…`, creation.hex `34f52280…`, abi `c7902147…`, method-identifiers `0d5cab2f…`, metadata `4589e842…`, opcodes `8da3b5a4…`, compile-receipt `cfa08aa8…`, verify-report `c71cec93…`); `EX-09/vyper/Ex09Vault.{vy,runtime.hex,creation.hex,abi.json}`; `EX-03/token.vy` `acc71444…` + `EX-03/{runtime.hex,creation.hex,abi.json,method-identifiers.json}` | EX-02, EX-04, EX-09, EX-03 |
| R3 | probe hex | LANDED | `EX-04/evidence/probe/probe-6.4.0-hex.json` `c9752447…`; `probe-6.7.0-hex.json` `37946825…`; `EX-09/probe/vy-runtime-hex-{6.4.0,6.7.0}.json`; `EX-09/probe/vy-runtime-0xhex-6.4.0.json`; PL-1's cross-carrier legs `PL-1/evidence/probe/{CarrierV,CarrierW,EX03,Smoke,EX04creation}-*.json` — all 15/15, 9/9, 22/22, 4/4, 7/7 with zero missing / zero extra | EX-04, EX-09, PL-1 |
| R4 | probe raw | LANDED | `EX-04/evidence/probe/probe-6.4.0-raw.json` `1703692c…`; `EX-09/probe/vy-runtime-raw-{6.4.0,6.7.0}.json`; this seat's own three legs `SC-1/evidence/probe-carrierv-{hex-6.4.0,raw-6.4.0,hex-6.7.0}.json` — 15/15 on every leg, decoded `bytecode.sha256 57d6fd0a…` | EX-04, EX-09, SC-1 |
| R5 | reconciliation (planted vs probe vs independent extraction) | LANDED | `EX-05/planted-full.json` `554bf3fd…` (two-impl agreement, K=15), `EX-05/planted.txt` `07b89ba7…`, `EX-05/planted-vs-ex04-planted.txt` `fe8c36c4…`, `planted-vs-ex08.txt` `9ee88c17…`, `planted-vs-method-identifiers.txt` `81781511…`, `crosscheck.txt` `5e23e026…`, `crosscheck-source-derived.txt` `980827a4…`, `digest-agreement.txt` `fa2867dc…`, `erc20-absence.txt` `d7f1691e…`; `EX-08/recon.py` (independent linear-sweep disassembler + keccak M3), `EX-08/sigs-CarrierV.selectors.txt`; `EX-09/planted/planted-K.json` `91c21466…` (peer-oracle re-derived by EX-05, `EX-05/ex09-peer-oracle-recheck.txt` `557dbc61…`, mismatches none); `EX-10/rerun.md` | EX-05, EX-08, EX-09, EX-10 |
| R6 | control (input-shape traps, attack legs, byte-level censuses) | LANDED | `EX-04/evidence/probe/probe-6.4.0-rawonhex.json` `02500262…` (raw-over-hextext trap: parsed-and-empty, decoded sha == the hex text file's own sha `e0b1021c…`); `EX-09/probe/{trap-raw-over-hextext-6.4.0,trap-raw-over-hextext-6.7.0,trap-hex-over-rawbin-*,trap-raw-over-vyhextext-6.4.0,trap-hex-over-vyrawbin-6.4.0}.json`; `EX-09/probe/nb-*.json` (empty / ELF-magic / JSON / text / directory / devnull / nonexistent / bad-encoding / symlink legs); `EX-09/analysis/{dispatch-structure.txt,offset-rule-proof.txt,mutability-census.txt}`; `EX-04/evidence/dispatch-census.py` `69007d30…`; `EX-05/attacks.txt` `e0d52b72…`; `RV-2/evidence/{push4-census.txt,vyper-dispatch-shape.txt}` | EX-04, EX-09, EX-05, RV-2 |
| R7 | rerun / id-domain | PARTIAL | `EX-07/pre-registration.md` (D1–D6 predictions recorded BEFORE the runs) + `EX-07/legs/` (A-hex-6.4.0, A-hex-6.4.0-rerun, AC-creation-6.4.0, AC-creation-6.7.0, AC-creation-raw-6.4.0 …) + `EX-07/compare-legs.py`; `EX-10/evidence/var-*.json` (path-variant legs: abspath / cwd-from-tmp / tmpdir variants) + `EX-10/rerun.md`; `VZ-1/evidence/vyper-kk-rederive.txt` (K/K re-derivation across the wave's own envelopes — every leg 15/15, 7/7, `abi_eq_env` true). Same-path rerun envelope byte-identity: **not established at this seat's close** | EX-07, EX-10, VZ-1 |
| R8 | landing/close (boundary) | GAP (patch-text drafts only) | drafts `records-drafts/knowledge-entry-draft.md`, `records-drafts/map-token-patch.md`, `records-drafts/records-drafts.md`; actual landing **GAP**; command-A at records commit **GAP**; custody post-pair **GAP** | SC-1 |

## Row details

### R1 — install (the round's one authorized install)

`vyper` **0.4.3** (`0.4.3+commit.bff19ea2`), wheel
`vyper-0.4.3-py3-none-any.whl` sha256 `3b967172…`, 403,104 B, installed into
the wave-isolated venv `.ufo/waves/arc3-loop1-round4/tools/vyper-venv/` with
`include-system-site-packages = false`. The receipt records **four
derivations, two seats, one value** for the wheel digest (this seat's fresh
`pip download --no-cache-dir`, the cached copy, the staged copy, and EX-01's
independent census pin), and it equals PyPI's own published digest. The
interpreter is `/usr/bin/python3.14` (Python 3.14.7, sha256 `d78f9cf7…`) — the
environment census found no system `pip` module and no `pip`/`pip3` on `PATH`;
the venv was created with the stdlib `venv` module. Venv `bin/vyper` sha256
`615f792c…`; 157 wheel files byte-identical to the installed tree (RECORD
rewritten by pip, as expected). **No other install was performed by any seat**
— this is the only install this ledger attests.

### R2 — compile (Vyper 0.4.3, on-host)

Four Vyper carriers were compiled on this host with the receipted venv
compiler; byte-exactness is claimed for these pinned bytes only:

- `Smoke` @EX-02 — the install smoke leg, run against the **target venv**
  (not a rehearsal copy). 5 ABI entries (4 functions + constructor);
  runtime 168 B, runtime.hex `40650adf…`.
- `CarrierV` @EX-04 — the round's primary carrier (vault with fees, pause,
  owner; mixed mutability). Source `f4f94727…` (1,9xx B); creation 1,637 B
  `3c667396…`; **runtime 1,562 B `57d6fd0a…`**; hex carrier 3,124 B
  `e0b1021c…`; ABI 15 function entries `c7902147…`; vyper `method_identifiers`
  `0d5cab2f…` (16 keys — the extra key is `__default__()`, see R6).
  `verify-artifacts.py` confirms `runtime_bin_matches_hex` true and
  `runtime_found_in_creation` true at creation offset 20.
- `Ex09Vault` @EX-09 — second independent Vyper carrier, 581 B runtime
  (`54b14e30…`), K=7.
- `StewardToken` @EX-03 — the ERC-20-bearing carrier, 3,337 B runtime
  (`1846469b…`), 22 ABI function entries.
- `CarrierW` @PL-1 — planner prototype, 829 B runtime (`67d1d88f…`), 9 entries.

### R3/R4 — probe, hex and raw legs (this seat's own runs included)

This seat ran three legs of its own against the pinned `rea-agents` versions
with a disk-backed `TMPDIR` (`/var/tmp/sc1-r4/probe-tmp`; the host `/tmp` quota
fails this probe — standing hazard). All three: **15 functions, zero missing /
zero extra**, `dispatch:"abi"` on all fifteen, decoded
`normalized_result.bytecode.sha256 57d6fd0a…` equal to the carrier file's own
sha256:

| leg (this seat) | evidence_id | functions |
|---|---|---|
| `CarrierV` runtime.hex, hex, pin 6.4.0 | `ev_d1792f57…` | 15 |
| `CarrierV` runtime.bin, raw, pin 6.4.0 | `ev_eac08124…` | 15 |
| `CarrierV` runtime.hex, hex, pin 6.7.0 | `ev_62e1b9e6…` | 15 |
| `Smoke` runtime.hex, hex, pin 6.4.0 | `ev_073f845c…` | 4 |
| `CarrierV` creation.hex, hex, pin 6.4.0 | `ev_53732d0f…` | **0** (parsed-and-empty, exit 0) |

Envelopes: `SC-1/evidence/probe-carrierv-{hex-6.4.0,raw-6.4.0,hex-6.7.0}.json`,
`SC-1/evidence/probe-smoke-hex-6.4.0.json`,
`SC-1/evidence/probe-carrierv-creation-6.4.0.json`. The three CarrierV legs
agree function-for-function; the 6.7.0 envelope carries the
`relationship_coverage` key (value `null`) that the 6.4.0 envelope lacks —
consistent with EX-07's pre-registered envelope-delta measurement.

Cross-seat: EX-04's `probe-6.4.0-hex.json`, `probe-6.4.0-raw.json` and
`probe-6.7.0-hex.json` are the same three legs at the same path; EX-09's
`vy-runtime-{hex,raw}-{6.4.0,6.7.0}` and `vy-runtime-0xhex-6.4.0` are the
second carrier's matrix; PL-1 probed five carriers across two pins. VZ-1's
`vyper-kk-rederive.txt` re-derives ABI/planted/envelope set equality for every
envelope in the wave tree (`abi_eq_env: true` on each).

### R5 — reconciliation (three independent sources agree)

- **Planted (pre-probe):** `EX-04/evidence/planted-K.json` recorded
  2026-10-19T14:05:46.622429Z with K=15 and **two independent derivations**
  (pure-Python keccak256 `d7563ac2…` and node keccak `24f33c9c…`) agreeing;
  ERC-20 absence checked against 8 known selectors with zero collisions.
  EX-05 re-derived the same 15 selectors with **four** implementations
  (js-sha3 from the r1 receipted prefix, node:crypto, openssl CLI, pure-Python
  `keccak_ref.py`) and recorded `all_agree: true`.
- **Probe (independent):** the envelopes above — 15/15 on every decoding leg.
- **Extraction (probe-independent):** EX-08's own linear-sweep disassembler +
  keccak M3 leg (**Form-A-scoped**: it parses the default `-O 2` XOR chain and
  returns 0 on the `--no-optimize` and `-O codesize` forms while the probe
  recovers 8/8 on both — CR-1, measured; a shape-blind extractor returning
  empty on a fully-recovered carrier is the round's "false honest-stop"
  hazard); RV-2's byte-level PUSH4 census; EX-04's `dispatch-census.py` (also
  Form-A-scoped by construction).
- **Peer-oracle:** EX-05 re-derived EX-09's planted-K (7/7, mismatches none)
  using two implementations that are not EX-09's own.

All three sources agree on CarrierV's 15 selectors and on every other
carrier's K. **Comparison discipline (CR-1's count-only trap):** the round's
legs are compared as **sets**, never as counts — a tampered carrier keeps
n = K while its set changes, so a count comparison would pass a wrong set.
This ledger's and the entry's K/K statements are set-equality statements.

### R6 — control: the Vyper dispatcher is a THIRD shape, and offsets are NOT JUMPDESTs

This is the round's principal measured delta, and it is corroborated
independently by four seats (EX-04 `dispatch-census.py`, EX-09
`offset-rule-proof.txt` + `dispatch-structure.txt`, RV-2
`vyper-dispatch-shape.txt` + `push4-census.txt`, PL-1 `verify.txt`) plus this
seat's own byte-level re-derivation.

**Dispatch mechanism (Vyper 0.4.3, `CarrierV` 1,562 B).** The prologue is

```
5f 35 60 e0 1c | 60 02 60 0d 82 06 60 01 1b 61 0600 01 60 1e 39 5f 51 56
PUSH0 CALLDATALOAD PUSH1 0xe0 SHR | PUSH1 2 PUSH1 13 DUP3 MOD PUSH1 1 SHL
PUSH2 0x600 ADD PUSH1 0x1e CODECOPY PUSH0 MLOAD JUMP
```

i.e. `bucket = selector % 13`; the runtime copies a **13-entry uint16 jump
table** from offset `0x600` (the tail of the runtime) to memory offset `0x1e`
and `JUMP`s to `table[bucket]`. Every one of the 13 table entries is a
`0x5b` JUMPDEST; `0x5e7` (1511) appears 3× as an empty-bucket sentinel
(buckets 1/7/11). From each bucket head the code falls through a chain of

```
63 <sel:4> 81 18 61 <next:2> 57
PUSH4 sel  DUP2 XOR  PUSH2 next  JUMPI
```

— Vyper compares with **XOR-equals-zero**, not solc's `EQ` (0x14) or `GT`
(0x11). `CarrierV` has 15 such compare sites for 15 selectors over 13 buckets
(4 bucket collisions), and `Ex09Vault` has 7 selectors over 6 buckets.

**Offset semantics — the r1/r3 reading does not generalize.** On this family
**0 of 15** reported `bytecode_offset` values land on a JUMPDEST; every one is
the **fall-through body entry after the compare `JUMPI`**, i.e.
`push4_pc + 11`. This seat re-derived it byte-for-byte on `CarrierV` (all 15
match, and the compare-site JUMPDEST at `offset-12` carries that function's own
selector) and on `Smoke` (all 4 match). EX-09 proved the same rule on two
further carriers (7/7 and 4/4) and stated the contrast: on the solc carriers
the offsets **are** JUMPDESTs. Both readings are correct — they are different
dispatcher conventions. The corpus text that says "offsets land on JUMPDESTs"
must therefore carry its solc-convention scope.

**Zero false positives, byte level.** `CarrierV`'s runtime contains two
non-selector PUSH4 immediates — `08c379a0` (`Error(string)` revert selector, at
6 sites) and `69656e74` (ASCII "ient", a fragment of the "insufficient" revert
string). Neither was reported as a function: the probe's 15 functions are
exactly the 15 planted selectors. The `__default__()` key in vyper's
`method_identifiers` (→ `89402a72`) is a **phantom**: those bytes do not occur
in the runtime at all (this seat's own byte search: ABSENT), and it is not an
ABI function entry. Counting `method_identifiers` keys instead of ABI function
entries would over-count by exactly one per carrier.

**Mutability / argument inference on this family (recorded as a delta).**
This seat compared the probe's `inferred_state_mutability` against the compiled
ABI for all 15 `CarrierV` functions: **7 agree, 8 read `payable`** where the
ABI says `view` (5), `nonpayable` (2) or `pure` (1). No case reads a *more*
restrictive class, and no case misassigns a selector. EX-09's independent
census on `Ex09Vault` found the same direction of divergence (2/7 diverge;
`pure` → `payable`). This is an upstream-inference behavior on this dispatcher
family, recorded as a delta, **not** a defect and **not** a claim about the
contract. `inferred_arguments` on this family also drops the `address` type
(it reads `uint256` for address parameters) — the same class of divergence
noted in the solc rounds.

**Input-shape traps reproduce on Vyper carriers.** raw-over-hextext exits 0
with 0 functions and decoded sha equal to the hex text file's own sha
(`e0b1021c…`) — parsed-and-empty, the r1/r3 class. EX-09's non-bytecode
battery (empty file, ELF magic, JSON, text, directory, `/dev/null`, nonexistent
path, bad encoding, symlink) is the round's typed-refusal evidence; the
creation-code legs (EX-04, EX-09 ×2 pins ×hex/raw/0xhex) are uniformly
parsed-and-empty at exit 0.

### R7 — rerun and the id domain (PARTIAL)

EX-07 recorded its D1–D6 leg matrix and predictions **before** the runs
(`EX-07/pre-registration.md`): path variants, a symlink leg, the raw-on-hex and
hex-on-raw input traps, and a same-request rerun. EX-10's `var-*` legs add
absolute-path / cwd-relative / alternate-TMPDIR variants. VZ-1 re-derived K/K
across the wave's own envelopes. **Gap:** a same-path, same-request rerun
envelope byte-identity check (the r1/r3 `cmp` form) is **not established at
this seat's close** — the artifacts are present (`A-hex-6.4.0-rerun.json`,
`var-*` legs) but the comparison verdict was not in the tree when this ledger
was written. GAP rows carry no verdict.

### R8 — landing (GAP, parent-side by design)

Nothing in this chain has landed. The knowledge entry, the map token, the
records sections and the command-A after-state are all drafts. This seat
proposes no repo-surface change of its own (see the seat report §2).

## Measurement of the chain claim (before → after)

Claim under test: the Vyper leg closes the r3 entry's named Unknown, and
command A re-measures 83 → 84 with the prior 83 byte-identical.

- **Before (measured first-hand, this seat, at HEAD `015e1bab…`):**
  command A (SCORECARD §Measurement recipes A, verbatim) →
  `{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [],
  "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [],
  "revision": "015e1bab914713568f339fd53999bc180459cc40", "rule_blocks": 14}`
  — `SC-1/evidence/command-A-before.json`; matches RV-2's
  `evidence/commandA-before.txt` and VZ-1's `baseline-commandA.json`.
- **Chain-side after (measured now, independent of landing):** the Vyper
  carriers' selectors are recovered K/K by `inspect-evm-interface` — 15/15
  (`CarrierV`, 3 legs), 4/4 (`Smoke`), 7/7 (`Ex09Vault`), 22/22
  (`StewardToken`), 9/9 (`CarrierW`) — against Vyper's own ABI-derived
  selector sets, zero missing / zero extra. The claim's "at least one
  Vyper-compiled contract's selectors are recovered" branch is **satisfied by
  this seat's own runs**; the honest-stop branch (typed refusal / partial
  recovery) was **not** triggered.
- **After (command A 83 → 84): GAP — parent-side.** Neither the entry nor the
  map token had landed at this seat's close. This seat does not claim 84.

## Footer

Whole-tree snapshot (this seat's recompute command):

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round4/claims/c1
find . -type f ! -path '*pycache*' | sort | xargs sha256sum > /var/tmp/sc1-r4/c1-inventory.txt
```

`SC-1/c1-inventory.txt` is the same table at capture time (78 rows at
14:12Z; the wave was still producing artifacts — a re-run at integration will
differ, by design).

Identity discipline (rule #14): this ledger was written once and its own hash
is re-derived in `SC-1/README-identities.txt` after the final write; the
draft's numbers describe the tree at 14:12Z and are superseded by any later
seat artifact.
