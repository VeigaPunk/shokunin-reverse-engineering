# CR-1 r4 — patch text for the round-4 corpus entry (Vyper leg)

Seat CR-1 (chain c1, critic), arc3-loop1-round4. These are **patch texts only** —
no seat writes `corpus/`. Apply-by-content; the parent lands.

Target: the round-4 knowledge entry drafted from this wave's c1 evidence
(EX-02/EX-03/EX-04/EX-05/EX-09/PL-1 legs). Each item below is anchored to a
first-hand measurement recorded under `claims/c1/CR-1/`; no item is inferred.

---

## Edit 1 — scope every dispatch-shape claim to the optimizer mode it was measured under

**Why.** The wave's carriers are all compiled with Vyper's default optimizer
(`-O gas`). That emits exactly ONE of three shapes this seat measured:

| form | trigger (measured) | dispatch structure | `PUSH4` present? |
|---|---|---|---|
| **A** | default `-O gas` (all r4 carriers) | 2-byte CODECOPY bucket table (`PUSH1 02 PUSH1 <n> DUP3 MOD PUSH1 01 SHL PUSH2 <base> ADD PUSH1 1e CODECOPY PUSH0 MLOAD JUMP`) then a **chained** `JUMPDEST PUSH4 <sel> DUP2 XOR PUSH2 <next_test> JUMPI <body>` | yes, once per selector, **zero `EQ` opcodes** |
| **B** | `--no-optimize` / `-O none` | `... PUSH4 <sel> DUP2 EQ ISZERO PUSH2 <body> JUMPI ...` — `EQ` **is** present | yes |
| **C** | `-O codesize` | byte-packed table (`PUSH1 07 ... 0x16 DUP5 DUP5 PUSH1 18 SHR ... MOD ...`) | **no `PUSH4` immediates at all** |

Evidence: `out/K8.runtime.hex` (A), `out/K8.nooptimize.runtime.hex` /
`out/K8.Onone.runtime.hex` (B), `out/K8.Ocodesize.runtime.hex` (C);
`src/shape-classify.py` prints the classification for all 33 carriers;
`probe/K8.nooptimize.6.4.0.json` and `probe/K8.Ocodesize.6.4.0.json` both
recover 8/8. Suggested sentence: *"The round's carriers are default-optimizer
(`-O gas`); Vyper 0.4.3 also emits two further dispatch shapes under
`--no-optimize`/`-O none` and `-O codesize`, both probed here at K/K, and the
shape claims below are scoped to the default-optimizer form."*

## Edit 2 — the `bytecode_offset` reading must be re-scoped, not repeated

**Why.** On every Vyper carrier this seat measured, the reported
`bytecode_offset` equals `PUSH4_opcode_pc + 11` and the byte there is `0x60`
(PUSH1) — **never** `0x5b` (JUMPDEST). Measured `0/8`, `0/30`, `0/3`, `0/2`,
`0/1` across K8/K30/D1/D3/K1; and `2/2` on the tiny S2 carrier lands on `0x34`
(CALLVALUE). EX-09 and PL-1 reached the same conclusion independently in their
seat reports. If the entry repeats the r3 line "offsets land on JUMPDEST", it
will be false for the Vyper leg. Suggested replacement: *"On the Vyper leg the
reported offsets are the post-compare fall-through entries
(`PUSH4_opcode_pc + 11`), not JUMPDESTs — the JUMPDEST reading is scoped to the
solc-convention carriers."*

## Edit 3 — record the bucket table's structural facts, including collisions

**Why.** These are the Vyper-specific structural facts a future round will need,
all measured here: the bucket count `n` is the prologue `MOD` modulus; **every
non-zero bucket entry lands on a JUMPDEST** (checked on all 33 carriers,
`src/vyrecon.py`); and **bucket collisions are the norm, not an anomaly** —
K8 has 2 collisions over 9 buckets, K25 has 7 over 22, K30 has 7 over 35, and
K25 has one 3-way bucket. A future reconciliation that assumes one selector per
bucket will over-count. Suggested sentence: *"The bucket table is a
`selector % n` hash table; collisions are normal (K8: 2 collisions in 9 buckets;
K25: 7 in 22, one of them 3-way), so bucket count is not selector count."*

## Edit 4 — name the reconciliation hazard the Vyper leg introduces (the round's most portable finding)

**Why.** This seat's central attack result. A solc-shaped dispatcher parser
(the `EQ;PUSH2;JUMPI` recipe the r1/r3 rounds used) returns the **empty set** on
**all 33** default-optimizer Vyper carriers while the probe returns full K/K on
each — so a seat running that recipe on a Vyper carrier can enter the
"parsed-empty" honest-stop branch on a fully-recovered carrier, or, worse,
report the probe's correct selectors as reconciliation extras. The r3-heritage
`audit-seat.js` does exactly the latter on this tree: of 26 decoded-digest
groups, **7 are Vyper-shaped** (`EQ-dispatch set (n=0)` with `probe set (n>0)`)
and every recovered selector in them is reported as a false extra —
**15/15, 22/22, 9/9, 8/8, 7/7, 4/4, 3/3, i.e. a 100 % false-positive rate** on
those carriers. The r3 c1 tree shows 59/59 solc-shaped groups and zero such
false extras, so the hazard is introduced by this round's leg, not inherited.
Reproduce: `recon/audit-r4-all.txt` vs `recon/audit-r3-c1.txt`;
`src/eqonly.py` prints the shape-blind empty set per carrier.
Suggested sentence: *"The Vyper leg is the first carrier class where a
`EQ`-based dispatcher reconciliation returns empty on fully-recovered code;
reconcilers must parse the `DUP2 XOR` (and `-O codesize`) forms or report
`unparsed`, never `absent`."*

## Edit 5 — the count-vs-set reconciliation rule (attack-1 corollary)

**Why.** This seat's decisive injection. Flipping one byte of a chain-leg
selector (`364605a1` → `364605a2`) leaves the probe's **count unchanged at 8**
while the **set is wrong** (`missing=[364605a1] extra=[364605a2]`). A
count-only reconciliation therefore passes on a wrong recovery; only a set
comparison catches it. Two further injections (chain-leg `XOR`→`NOT`, and a
retargeted compare destination) both yield `n=7` with the broken selector the
only miss. Suggested sentence: *"Reconciliation must compare recovered sets,
not counts: an injected selector change preserves K while changing the set
(`probe/K8tampered.6.4.0.json`)."*
