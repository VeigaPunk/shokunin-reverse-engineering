# CR-1 — chain c1, critic (arc3-loop1-round4)

Seat line: attacks — (1) Vyper's dispatcher is chained selector comparisons, not
a PUSH4 jump table — could the extractor silently partial-recover while looking
complete? check the reconciliation for unplanted-present/planted-absent;
(2) decoy constants; (3) costume retry on partial recovery. Verdicts below.

Repo HEAD `015e1bab914713568f339fd53999bc180459cc40` (unchanged through this
seat's work; `git rev-parse HEAD`). No git mutations. Custody paths untouched.
No corpus/SKILL/PROVINCE/README/LOG/SCORECARD writes — patch text only.
Scratch: `/var/tmp/cr1-r4/` (disk-backed; `/tmp` never used).
Compiler: the wave's authorized venv
`.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper` →
`0.4.3+commit.bff19ea2` (EX-02's install; receipt
`claims/c1/EX-02/smoke/compile-receipt.txt`; this seat installed nothing).
Probe: `npx -y rea-agents@6.4.0` primary, `@6.7.0` cross-pin, with
`TMPDIR=/var/tmp/cr1-r4/tmp` (a `/tmp`-defaulted run fails EDQUOT, errno -122).

Artifact set (this seat's write scope): `claims/c1/CR-1/` — 164 files
(excluding the manifest), `MANIFEST.sha256` sha256
`09ba0223c8767fa2b8ae407d5e62d1ba72ece58c046000653e673bb1dbc7f8f3`,
`sha256sum -c` → 164/164 OK, manifest generated last over a set that excludes
itself. `src/identity-rederive.py` and `src/shape-classify.py` re-derive every
self-claimed identity **from the wave copies** (rule #14).

## 1. Work performed (evidence pointers)

**33 Vyper carriers compiled on-host** with the receipted venv, in
`vy/` + `out/`: K-spread `K1..K30` (`out/K*.runtime.hex`), small-arity `S2..S5`,
four adversarial decoy/shape carriers `D1..D4`, four EVM-version legs
(`out/K8.evm{london,paris,shanghai,cancun,prague}.runtime.hex`), and three
optimizer-mode legs (`out/K8.{nooptimize,Onone,Ocodesize}.runtime.hex`).
Each carrier has its Vyper-emitted oracle `out/<carrier>.methodids.json`
(`vyper -f method_identifiers`) — the planted set is **not** hand-derived.

**Three injections** on K8, each a single byte-level mutation of the chain leg:
`out/K8tampered.runtime.hex` (selector `364605a1`→`364605a2`),
`out/K8-legbroken.runtime.hex` (chain-leg `XOR 0x18`→`NOT 0x19`),
`out/K8-partial.runtime.hex` (compare destination retargeted to the revert stub).

**33 probe envelopes** in `probe/` (one per carrier + the injections, plus
`@6.7.0` legs for K8/K30/D4/K1).

**Instrumentation** in `src/`: `disasm.py` (linear disassembler),
`vyrecon.py` (independent bucket-table + XOR-chain census),
`decoys.py` (decoy classification), `eqonly.py` (the deliberately solc-shaped
`EQ;PUSH2;JUMPI` extractor, for the shape-blind demonstration),
`shape-classify.py` (Form A/B/C classifier), `identity-rederive.py`,
`vycensus.py`, `reconcile.py`; plus the r3-heritage `audit-seat.js` reused
read-only from `claims/c1/CR-1` of round 3.

**Reconciliation outputs** in `recon/`: `SUMMARY.md` (the full attack write-up),
`audit-r4-all.txt` (whole r4 `claims/` tree), `audit-r3-c1.txt` (r3 c1 control),
`audit-r4-c1.txt`, `vyrecon.json`, `command-A.txt`.

## 2. Proposed changes

`claims/c1/CR-1/proposed-entry-corrections.patch.md` — five apply-by-content
items for the round-4 entry (patch text only; no corpus write):

1. scope every dispatch-shape claim to the optimizer mode measured (Form A);
2. re-scope the `bytecode_offset` reading — on Vyper it is
   `PUSH4_opcode_pc + 11`, never a JUMPDEST;
3. record the bucket table's structural facts, including that collisions are
   normal (K8: 2/9; K25: 7/22 with one 3-way);
4. name the reconciliation hazard (a solc-shaped `EQ` parser returns empty on
   fully-recovered Vyper code; 100 % false extras on 7 r4 digest-groups);
5. the count-vs-set rule (an injected selector change preserves K while
   changing the set).

## 3. Before → after measurement for the chain's claim

- **Before-state, first-hand** (`recon/command-A.txt`, SCORECARD recipe A at
  HEAD `015e1bab`): `{"knowledge_files": 83, "mapped": 83, "missing": [],
  "dangling": [], "citation_resolved_rules": 14, "rule_blocks": 14,
  "coverage_score": 10.0, "depth_score": 10.0}` — the claim's stated 83.
  The 83 → 84 flip is the parent's landing step; not measurable by this seat.
- **Claim substance re-measured independently of the probe**: the
  bucket-table + XOR-chain census (`src/vyrecon.py`, never reads an envelope)
  is **set-equal to Vyper's own `method_identifiers` on 26/26 clean carriers**
  (K = 1,2,3,4,5,6,7,8,9,10,12,16,20,25,30; S2–S5; D1–D4; 4 EVM legs) —
  zero missing, zero extra, zero invalid bucket entries. Cross-pin `@6.7.0`
  (K8/K30/D4/K1): 8/8, 30/30, 6/6, 1/1, decoded sha identical to 6.4.0.
- **Independent census over the chain's own landed carriers** reproduces every
  claimed K: EX-02 `Smoke` 4/4, EX-02 `T5` 3/3, EX-09 `Ex09Vault` 7/7,
  EX-09 `Smoke` 4/4, EX-09 `Atk3` 8/8, EX-09 `vyper/Ex09Vault` 7/7,
  PL-1 `CarrierW` 9/9 (the solc carrier `EX-09/carriers/VaultB.opt200` yields 0
  from this Vyper-shaped census, as expected).
- **The Vyper dispatch shape, measured** (3 forms, above); reported
  `bytecode_offset == PUSH4_opcode_pc + 11` and never `0x5b`, on every carrier.

## 4. Attacks / refutations attempted, with verdicts

**Attack 1 — silent partial recovery while looking complete; unplanted-present /
planted-absent.**
Verdict: **REFUTED at the probe; HAZARD CONFIRMED at the reconciliation layer.**
- *Probe is byte-true on all four variants.* `K8tampered`: n stays **8 (=K)**
  but the set changes — `missing=[364605a1] extra=[364605a2]`;
  `K8-legbroken`: n=7, `missing=[364605a1]`, no extras; `K8-partial`: n=7,
  same. No variant produced a complete-looking wrong set; the recovered set
  follows the bytes, and no partial recovery was ever costumed as full.
- *The count-only trap is real*: the tamper case passes a count comparison
  (8 = 8) while the set is wrong. Only a set comparison catches it.
- *The shape-blind trap is the sharper one.* A solc-shaped
  `EQ;PUSH2;JUMPI` extractor returns the **empty set on all 33** carriers
  (`src/eqonly.py`), while the probe returns full K/K on each — the
  "parsed-empty" honest-stop branch is reachable on a fully-recovered carrier.
  The r3-heritage `audit-seat.js` over the r4 tree reports 7 of 26 digest-groups
  as Vyper-shaped (`EQ-dispatch set (n=0)`, `probe set (n>0)`) and flags every
  recovered selector in them as a false extra: 15/15, 22/22, 9/9, 8/8, 7/7,
  4/4, 3/3 — a 100 % false-positive rate. The r3 c1 tree is 59/59 solc-shaped
  with zero such false extras, so the hazard is introduced by this round.
- *The chain's own reconcilers cover Form A only.* `EX-08/recon.py` (r4,
  `claims/c1/EX-08/`) parses the Form-A XOR chain 8/8 but returns **0/8 on
  Form B (`--no-optimize` / `-O none`) and 0/8 on Form C (`-O codesize`)**
  while the probe recovers 8/8 on both. `EX-04/evidence/dispatch-census.py`
  is Form-A-scoped by construction. Not a claim failure — both carriers were
  probed — but the recipe should not be reused on the other two forms.

**Attack 2 — decoy constants.**
Verdict: **REFUTED (zero false positives), exercised on real decoys.**
- `D2` carries selector-shaped `bytes4` constants: `a9059cbb` @byte 49 and
  `095ea7b3` @byte 74 are **genuine `PUSH4` operands** (5 `PUSH4` immediates,
  3 dispatched). The probe reported 3/3 and neither decoy.
- `D3`/`D4` carry `08c379a0` (`Error(string)`) twice as a `PUSH4` operand
  (D3: 3 `PUSH4`/2 dispatched; D4: 7/6). Probe reported neither.
- `D1` embeds the foreign selector `a9059cbb` as raw data inside a `raw_call`
  argument (byte 162, not at a `PUSH4` boundary) — not reported.
- Across all 33 carriers: `decoy_reported = []` everywhere (`recon/SUMMARY.md`,
  `src/decoys.py`).

**Attack 3 — costume retry on partial recovery.**
Verdict: **REFUTED — no partial→full transition anywhere.**
- Four costume legs over identical K8 bytes (`6.4.0/hex`, `6.7.0/hex`,
  `6.4.0/renamed-file/hex`, `6.4.0/raw-bin`): all n=8, identical decoded
  `normalized_result.bytecode.sha256 72e5d886da7c…`; four distinct
  `evidence_id`s and two distinct `subject.digest.sha256` values
  (`b1f7fc882e44…` hex file vs `72e5d886da7c…` raw file) — the comparator must
  be the decoded digest, not the subject digest.
- `audit-seat.js` over the whole r4 `claims/` tree: **0** `PARTIAL->FULL
  TRANSITION` lines; the only set-changing legs in this seat's set are the
  deliberate injections, where the probe followed the bytes.

**Self-refutation recorded (rule #14 discipline).** This seat's first
independent census returned 0/8 on every carrier because it used a 3-byte
stride for the chain leg; Vyper's node is `63 sel 81 18 61 next 57`
(5+1+1+3 = **10** bytes to the `JUMPI`, with the body as the fall-through).
The error was caught by the three-way reconcile (census 0 vs probe 8 vs
oracle 8), not by a self-consistency check — the reconciler's whole purpose.

## 5. Blockers

None. Named residuals for the parent:

1. The five entry edits (§2) are unapplied — patch text only, per seat rules.
2. The 83 → 84 flip and the entry/token landing are parent-side; this seat
   measured the before-state only.
3. The r4 instruments (`EX-08/recon.py`, `EX-04/evidence/dispatch-census.py`,
   the r3-heritage `audit-seat.js`) are Form-A-scoped; if the parent reuses any
   of them for the landing reconciliation, Forms B and C will read as
   "unparsed". `src/shape-classify.py` classifies all three.
4. This seat's own census parses Form A only by construction; Forms B and C
   were verified against the probe + oracle, not by an independent parser
   (that is a deliberate scope statement, not a gap in the claim).
5. `via-IR`/solc legs, other Vyper versions, and Vyper contract sizes above
   ~1.5 KB remain unmeasured here; the chain's largest Vyper carrier is 1.6 KB.
