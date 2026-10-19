# CR-1 (arc3-loop1-round4, chain c1, critic) — attack summary

All numbers below are first-hand measurements on this host, 2026-10-19.
Scratch: /var/tmp/cr1-r4/ (disk-backed; /tmp never used).
Compiler: wave venv `.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper`
  `0.4.3+commit.bff19ea2` (EX-02's authorized install; receipt
  `.ufo/waves/arc3-loop1-round4/claims/c1/EX-02/smoke/compile-receipt.txt`).
Probe: `npx -y rea-agents@6.4.0` (primary) / `@6.7.0` (cross-pin), with
  `TMPDIR=/var/tmp/cr1-r4/tmp` (a /tmp-defaulted run fails EDQUOT, errno -122).

## The Vyper 0.4.3 dispatch shape (measured, 3 distinct forms)

Form A (default `-O gas`, the shape every r4 carrier uses):
  prologue `5f3560e01c` then a **2-byte-entry CODECOPY bucket table**
  (`PUSH1 02 PUSH1 <N> DUP3 MOD PUSH1 01 SHL PUSH2 <base> ADD PUSH1 1e CODECOPY PUSH0 MLOAD JUMP`),
  then a **chained** fall-through per function:
  `JUMPDEST PUSH4 <sel> DUP2 XOR PUSH2 <next_test> JUMPI <body>`.
  **Zero `EQ` opcodes anywhere** in the runtime. The `PUSH2` destination is the
  *next test*; the body is the fall-through.
Form B (`--no-optimize` / `-O none`):
  `... PUSH4 <sel> DUP2 EQ ISZERO PUSH2 <body> JUMPI ...` — `EQ` IS present here.
Form C (`-O codesize`):
  a byte-packed table with `PUSH1 07 ... 0x16 DUP5 DUP5 PUSH1 18 SHR ... MOD`,
  **zero `PUSH4` immediates at all**; the probe still recovers 8/8.

Reported `bytecode_offset` for every Vyper function = `PUSH4_opcode_pc + 11`,
and the byte at that offset is `0x60` (PUSH1), **not** `0x5b` (JUMPDEST) —
`0/8`, `0/30`, `0/3`, `0/2`, `0/1` across carriers. The solc-convention
"offset lands on JUMPDEST" reading does NOT hold on Vyper (independently
observed by EX-09 and PL-1 in their seat reports).

## Attack 1 — "silent partial recovery while looking complete"

**Probe verdict: REFUTED.** Four byte-level injections on K8 (8 functions):
| variant | mutation | probe n | probe set vs planted |
|---|---|---|---|
| K8tampered | chain-leg selector `364605a1`→`364605a2` | 8 (= K) | missing `364605a1`, extra `364605a2` |
| K8-legbroken | chain-leg `XOR`→`NOT` (`0x18`→`0x19`) | 7 | missing `364605a1`, no extras |
| K8-partial | chain-leg dest `0188`→`018c` (revert stub) | 7 | missing `364605a1`, no extras |
| K8 (control) | none | 8 | exact |

No variant produced a *complete-looking* wrong set: the recovered set follows
the bytes. The tamper case is the sharp one — **count-only reconciliation
passes (8 = 8) while the set is wrong**; only a set comparison catches it.

**Reconciliation-layer verdict: HAZARD CONFIRMED.** A solc-shaped extractor
(`EQ;PUSH2;JUMPI`, the r1/r3 recipe) returns the EMPTY set on **all 33 Vyper
carriers** while the probe returns full K/K on each — i.e. the recipe's
"parsed-empty" honest-stop branch is reachable on a fully-recovered carrier.
The r3-heritage `audit-seat.js` run over the whole r4 tree
(`recon/audit-r4-all.txt`): 26 decoded-digest groups, of which **7 are
Vyper-shaped** (`EQ-dispatch set (n=0)` with `probe set (n>0)`), and it reports
every recovered selector as a false "extra":
  15/15, 22/22, 9/9, 8/8, 7/7, 4/4, 3/3 — 100% false-positive rate there.
The r3 c1 tree (`recon/audit-r3-c1.txt`) has 59/59 solc-shaped groups and zero
such false extras: the hazard is introduced by the Vyper leg, not inherited.

`EX-08/recon.py` (the chain's own reconciler) handles Form A correctly (8/8)
but returns **0/8 on Form B (`--no-optimize`) and 0/8 on Form C
(`-O codesize`)** — two of the three Vyper shapes are unhandled by the
chain's published instrument. `EX-04/evidence/dispatch-census.py` documents the
Form-A `PUSH4 ... DUP2 XOR` leg explicitly and is Form-A-scoped.

## Attack 2 — decoy constants

**Verdict: REFUTED (zero false positives), on real decoys.**
- `D2` (selector-shaped `bytes4` constants): `a9059cbb` @byte 49 and
  `095ea7b3` @byte 74 sit as **genuine `PUSH4` operands** — 5 `PUSH4`
  immediates, only 3 dispatched. The probe reported 3/3 and neither decoy.
- `D3`/`D4`: `08c379a0` (`Error(string)`) appears twice as a `PUSH4` operand;
  probe reported 0 of them (D3: 3 `PUSH4`/2 dispatched; D4: 7/6).
- `D1`: foreign selector `a9059cbb` embedded as raw data inside a `raw_call`
  argument (`@byte 162`, not at a `PUSH4` boundary); not reported.
- Across all 33 carriers: `decoy_reported = []` everywhere.

## Attack 3 — costume retry on partial recovery

**Verdict: REFUTED — no partial→full transition observed.**
Four costume legs on identical K8 bytes: `6.4.0/hex`, `6.7.0/hex`,
`6.4.0/renamed-file/hex`, `6.4.0/raw-bin`. All four: n=8, identical decoded
`normalized_result.bytecode.sha256 72e5d886da7c…`; four distinct
`evidence_id`s and two distinct `subject.digest.sha256` values
(`b1f7fc882e44…` for the hex file, `72e5d886da7c…` for the raw file).
The only set-changing legs in the whole set are the deliberate injections,
where the probe followed the bytes (byte-truth ahead of planted-truth).
`audit-seat.js` over the r4 tree: 0 `PARTIAL->FULL TRANSITION` lines.

## Three-way reconciliation (independent census vs probe vs planted)

`src/vyrecon.py` derives the dispatch set from the **bucket table + XOR chain**
(never from the probe) and reconciles against Vyper's own
`method_identifiers` (the ABI-derived oracle). On the 26 clean carriers
(K=1..30, D1–D4, S2–S5, 4 EVM-version legs): **K/K everywhere — zero missing,
zero extra, zero bad table entries.** Every non-zero bucket entry lands on a
`JUMPDEST` (bucket collisions are normal: K8 has 2 collisions, K25 has 7).
Cross-pin `@6.7.0` on K8/K30/D4/K1: 8/8, 30/30, 6/6, 1/1, decoded sha
identical to the 6.4.0 legs.

Independent census over the **chain's own landed** Vyper carriers reproduces
every claimed K: EX-02 `Smoke` 4/4, EX-02 `T5` 3/3, EX-09 `Ex09Vault` 7/7,
EX-09 `Smoke` 4/4, EX-09 `Atk3` 8/8, EX-09 `vyper/Ex09Vault` 7/7,
PL-1 `CarrierW` 9/9. The solc leg `EX-09/carriers/VaultB.opt200.runtime.hex`
yields 0 from this Vyper-shaped census, as expected (it is solc-shaped).
