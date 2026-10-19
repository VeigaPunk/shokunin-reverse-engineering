# C1 verdict — the Vyper leg (chain convergence, seat VZ-1) — arc3-loop1-round4

Wave `arc3-loop1-round4` · chain c1 · 2026-10-19 · repo
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin` · HEAD at verdict work
`015e1bab914713568f339fd53999bc180459cc40` (no seat commits; parent integrates).
Frozen claim: `.ufo/waves/arc3-loop1-round4/claims-frozen.md` §C1.

**Revision history.** rev 1 — the initial reconciliation (written 14:15Z, before
RV-2's grade landed). **rev 2 — this revision**, after RV-2's grade
(ACCEPT-WITH-FIXES) and the EX-03/EX-04/CR-1 seat reports landed; it folds in
RV-2's four fixes and two advisories as debt 6, renumbers the list, and records
that all 16 c1 seats now have reports. No verdict-relevant measurement changed
between the revisions.

## Verdict: **VERIFIED** — with three named pre-landing entry-text repairs
## (F1/F2/F3) plus RV-2's four reviewer fixes, and all 16 c1 seats reported

The claim's success arm is measured first-hand and independently: at least one
Vyper-compiled contract's selectors **are** recovered by `inspect-evm-interface`
K/K against Vyper's own ABI-derived set — in fact five carriers, on 18 legs, by
this seat's own re-derivation and by ≥3 independent seats each. The honest-stop
branches (venv infeasible / typed refusal / partial recovery) were **not**
triggered on any runtime leg. The landing arm ("lands as a corpus knowledge
entry + line-neutral map token; command A 83 → 84 with the prior 83
byte-identical") is a **parent-side action** whose scripts this seat executed
end-to-end on the **current** pair: 84/84, missing [], dangling [], 14/14,
prior-83 byte-identical, README 190 → 190. No measured result contradicts the
claim; the three defects below (F1/F2/F3) are **entry-text
provenance/mechanism** errors that change no count, set, digest, dispatch-shape
or offset claim, and all three have repair texts ready.

## Claim components — status and evidence

| # | Component | Status | Evidence |
|---|---|---|---|
| 1 | the round's ONE authorized install: vyper into the wave venv, receipted | DELIVERED | `EX-02/install.log`, `install-receipt.txt`, `venv-manifest.sha256`, `attest-output.txt` (8 wheels byte-identical to their pinned payloads, 157 vyper payload files `differ=0 missing=0`, `vyper --version` → `0.4.3+commit.bff19ea2`); **this seat re-derived** `bin/vyper` `615f792c…` and `bin/python` `d78f9cf7…` (= `/usr/bin/python3.14`), both equal to EX-04's and PL-1's receipts; `EX-01/env-census.txt` is the pre-install environment census (no system pip, uv-managed interpreters on disk, cp314 `immutables` wheel absent → source build, which is what EX-02 did) |
| 2 | ≥1 Vyper-compiled carrier, compiled on-host with the receipted compiler | DELIVERED ×5 | `Smoke`@EX-02 (168 B), `CarrierV`@EX-04 (1,562 B), `Ex09Vault`@EX-09 (581 B), `StewardToken`@EX-03 (3,337 B, ERC-20-bearing), `CarrierW`@PL-1 (829 B); **this seat recompiled nothing** but re-derived every carrier's decoded digest from the landed `runtime.hex`/`.bin` and matched it to the envelopes' `normalized_result.bytecode.sha256` on every leg it read |
| 3 | planted selectors recovered **K/K**, zero missing / zero extra, `dispatch:"abi"` | DELIVERED — **this seat re-derived all of it** | this seat's own `js-sha3@0.8.0` (r1 receipted prefix) re-derivation, ABI-keccak vs planted vs sealed envelope, set-equality: `CarrierV` **15/15** on 7 legs, `Ex09Vault` **7/7** on 5 legs, `StewardToken` **22/22** on 2 legs, `CarrierW` **9/9** on 2 legs, `Smoke` **4/4** on 2 legs — `abi == env == planted` **true on every leg**, `missing_vs_env []`, `extra_vs_env []`, `dispatch:"abi"` everywhere (`VZ-1/evidence/vyper-kk-rederive.txt`, `entry-claim-verification.txt`) |
| 4 | planted-K recorded pre-probe | DELIVERED | `EX-04/evidence/planted-K.json` `recorded_utc 2026-10-19T14:05:46.622429Z` precedes EX-04's first probe leg; two independent derivations inside the file agree; this seat's third path (js-sha3 over the compiled ABI) reproduces the same 15 values |
| 5 | zero false positives, byte level | DELIVERED — **independently censused by this seat** | this seat's opcode-boundary disassembly of `CarrierV`: 21 `PUSH4` immediates, 16 distinct — the 15 selectors plus `08c379a0` ×6 only; **no** non-selector constant reported as a function (`VZ-1/evidence/push4-census-independent.txt`). This seat's dispatch-site shape census over 4 carriers (**53 selectors**) found every one at a genuine `PUSH4 sel; DUP2; XOR` Vyper compare site: 0 selectors without a compare-shaped site (`shape-census` runs, same file family) |
| 6 | the round's structural deltas | DELIVERED — **re-derived first-hand** | (a) **third dispatcher shape**: prologue `5f3560e01c6002600d820660011b61060001601e395f5156` = `PUSH0 CALLDATALOAD PUSH1 e0 SHR | PUSH1 2 PUSH1 13 DUP3 MOD PUSH1 1 SHL PUSH2 0x600 ADD PUSH1 1e CODECOPY PUSH0 MLOAD JUMP`; the `0x600` table's **13 entries are all JUMPDESTs**, `0x5e7` sentinel **×3**, `selector % 13` matches the bucket heads (this seat's parse). (b) **offset semantics do not generalize**: `bytecode_offset == push4_pc + 11` **15/15** and `byte[offset−12] == 0x5b` **15/15** (i.e. the offset is the post-compare fall-through, not a JUMPDEST) — the r1/r3 "offsets land on JUMPDESTs" reading is solc-scoped. (c) **mutability delta**: 7/15 agree, 8/15 read `payable` where the ABI declares view/nonpayable/pure, one direction only, no selector misassigned (this seat's own ABI-vs-envelope comparison) |
| 7 | result lands as a corpus knowledge entry + line-neutral map token | PARENT-SIDE, **script-verified on the CURRENT pair** | entry literal extracted from `records-drafts/knowledge-entry-draft.md` between its markers: **32 lines / 18,166 B / `da42d9a2…`**; additive token patch `records-drafts/map-token-patch.md` (`8e3f91e3…`). Applied to a fresh `git clone --no-hardlinks` at HEAD `015e1ba`: clone `36680c2a…`, `git diff --name-status` = exactly `M corpus/README.md` + `A corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md`; README **190 → 190**, after-sha **`1cd052605e9d27f38e8c9b9b164fa64d0482b61d4acf0a2b80223cb4cec29d1e`** — **byte-equal to SC-1's independent rehearsal** (`map-token-patch.md` table) |
| 8 | command A 83 → 84, prior 83 byte-identical | PARENT-SIDE, **script-verified on the CURRENT pair** | before: this seat's exact-recipe run at HEAD = `{"knowledge_files":83,"mapped":83,"missing":[],"dangling":[],"citation_resolved_rules":14,"rule_blocks":14,"coverage_score":10.0,"depth_score":10.0}` (`VZ-1/evidence/baseline-commandA.json`; also RV-2, SC-1, PL-1). after: this seat's clone projection = **84/84, missing [], dangling [], 14/14, 10.0/10.0** (`VZ-1/evidence/projection-commandA.json`); **prior-83 byte-identical: 83/83, diffs=0, missing=0** (per-file `git show` compare against `015e1ba`); added = the one new file. The authoritative read is the parent's at the work commit |
| 9 | recheck line executes verbatim | DELIVERED — **this seat ran it** | `TMPDIR=/var/tmp/r4-recheck npx -y rea-agents@6.4.0 inspect-evm-interface …/EX-04/out/runtime.hex hex --format json` → id `ev_d1792f57…`, **15 functions**, all `dispatch:"abi"`, decoded `57d6fd0a…`; envelope sha256 **`68415a3d…`** — byte-identical to RV-2's copy, EX-05's mirror, RV-1's run and SC-1's run (five-way). The entry's raw leg (`runtime.bin raw`) also re-derived 15/15, decoded `57d6fd0a…` |
| 10 | probe-inert landing | MEASURED | this seat ran the citation-drift probe at HEAD **and** at the projected clone commit, default **and** `--strict`: findings=0 exit=0 ×4; `--selftest` 13/13; pointer-table sha256 `1b3ab955…` equals the expected pin. Census instrument `.ufo/gates/c1-census-v10.py` → **PASS `stale=0 ambiguous=0 undeclared=0 unresolved=0`**, scope-errors `[]`, unreadable `[]`. Custody-pair selftest (read-only) **28/28 CLEAN** |
| 11 | every `ev_` id cited by the entry resolves | VERIFIED | all **16/16** cited ids resolve to real envelopes in the tree with the stated payload (this seat's index over every `claims/c1/**/*.json`) |

## Before → after reconciliation (the discriminating unit)

- **Before (r1/r3 surface, re-measured at HEAD):** the named Unknown was
  "Vyper and solc versions other than 0.8.37"; no Vyper carrier had ever been
  compiled or probed on this host; command A 83/83 at `015e1ba`.
- **After (this wave):** five Vyper 0.4.3 carriers compiled on-host with the
  round's one receipted install, recovered K/K on 18 legs across two REA pins
  and three encodings; the Vyper dispatcher's third shape class measured
  (modulo-indexed jump table + XOR compare chain); the offset-semantics reading
  re-scoped; the mutability inference delta quantified; the zero-false-positive
  clause exercised on real decoys at byte level; the projection lands 83 → 84
  with the prior 83 byte-identical.
- **Headline numbers:** K/K zero-extras on **5 carriers / 18 legs** by this
  seat's own re-derivation; command A 83 → 84 at the clone projection; prior-83
  byte-identity 83/83; README 190 → 190 (`1cd05260…`).

## Named debt (measured residuals; none voids the claim)

1. **F1 — `69656e74` mechanism error (RV-1, sustained; reproduced by this seat).**
   The draft entry's zero-false-positive sentence names `69656e74` as a
   non-selector **`PUSH4` immediate**. It is not: it is a substring of the revert
   string `insufficient` inside a **`PUSH32` payload** at pc=723 (this seat's
   opcode-boundary disassembly: 21 `PUSH4` immediates, 16 distinct, the only
   non-selector one `08c379a0` ×6). The observation's **conclusion** (zero false
   positives) is unchanged and still true; the stated mechanism is
   unreproducible by the method it names. The same claim appears in
   `EX-05/runtime-presence.txt`, `RV-2/evidence/push4-census.txt` and
   `seats/EX-05.md` — repair all four or the corpus will contradict its
   siblings. **Repair text: `RV-1/proposed-entry-correction.patch.md`**
   (`7d90b514…`). Evidence: `VZ-1/evidence/push4-census-independent.txt`.
2. **F2 — "same three legs at the same path" sentence (this seat's own finding;
   no patch text from any seat yet).** The draft says EX-04's own legs
   (`probe-6.4.0-hex.json`, `probe-6.4.0-raw.json`, `probe-6.7.0-hex.json`) "are
   the same three legs at the same path". False: EX-04 ran scratch copies at
   `/var/tmp/ex04-r4/probe/` and got ids `ev_405e2a2a…`, `ev_83a6f336…`,
   `ev_470be5f5…`; the ids the entry cites (`ev_d1792f57…`, `ev_eac08124…`,
   `ev_62e1b9e6…`) belong to **repo-path** runs by EX-05/EX-06/EX-07/RV-1/RV-2 and
   this seat. The sentence also contradicts the entry's own id-domain bullet one
   line later. No count/set/digest is affected. **Repair text:**
   `VZ-1/evidence/finding-F2-same-path-sentence.txt` §Repair (replace the clause
   with the scratch-path attribution + the actual ids).
3. **CR-1 Edits 1–5 (`CR-1/proposed-entry-corrections.patch.md`), all sustained
   by this seat's reading of CR-1's evidence:** (1) scope every dispatch-shape
   claim to the optimizer mode — the round's carriers are all default `-O gas`
   (Form A), while `--no-optimize`/`-O none` (Form B, `EQ` present) and
   `-O codesize` (Form C, **zero `PUSH4` immediates**) are also probed K/K and
   are not yet named in the entry; (2) re-scope the offset reading rather than
   repeat the r3 line (the entry already does this — CR-1's edit confirms it);
   (3) record the bucket table's collision facts (K8: 2 collisions in 9 buckets;
   K25: 7 in 22, one 3-way); (4) **name the reconciliation hazard** — a
   solc-shaped `EQ`-recipe parser returns the empty set on all 33
   default-optimizer Vyper carriers while the probe returns K/K, and the
   r3-heritage `audit-seat.js` reports every recovered selector on those as a
   false extra (100% false-positive rate on 7 of 26 digest groups; the r3 c1
   tree has 59/59 solc-shaped groups and zero such extras); (5) the count-vs-set
   rule — an injected selector flip preserves K while changing the set, so
   count-only reconciliation passes on a wrong recovery. Items 4 and 5 are the
   round's most portable findings and are **absent from the draft entry**.
4. **EX-07's r3-entry correction (`EX-07/proposed-r3-unknowns-correction.patch.md`):**
   the r3 entry's "6.7.0-specific envelope deltas" is measured as a **6.5.0**
   boundary (present at 6.5.0 and 6.7.0, absent at 6.4.0; 66 envelopes, six
   carrier families). Line-neutral replacement given; the r3 entry's own
   reference compared only 6.4.0 vs 6.7.0 and so could not see it.
5. **F3 — the Inference mechanism for the payable-read delta (this seat's own
   finding, from EX-04's A4 re-measurement).** The draft's Inference says the
   divergence "is consistent with an inference that reads the dispatcher's
   compare/fall-through structure rather than per-function prologue guards — the
   XOR-chain dispatcher has no per-function `CALLVALUE` guard". This seat's own
   measurement falsifies the mechanism: the divergence tracks the function's
   **argument count** (8/8 arg-taking functions read `payable`; 7/7 zero-arg
   functions agree), the byte-level correlate is the fused guard
   `PUSH1 <4+32·nargs> CALLDATASIZE LT CALLVALUE OR PUSH2 <revert> JUMPI` that
   every arg-taking body opens with (measured 7 sites of `602436103417`), and
   the same class reproduces on the r3 solc carriers whose dispatch *does* carry
   per-function prologue guards: this seat re-measured VaultB.opt200 **13/13**,
   CarrierB **7/8** (`e7ee6ad6 rate`, nargs=1, pure→view), carrierB@EX-04
   **10/11** (`07bf89ab computeTxHash`, nargs=4, pure→view) — both r3 solc
   divergences are also arg-taking. The Observation sentence itself is accurate
   and stays. **Repair text:**
   `VZ-1/evidence/finding-F3-inference-mechanism.txt` §Repair (replace the
   mechanism clause with the argument-count correlate + the solc reproduction).
6. **RV-2's grade landed (rev-2 update).** RV-2's seat report + `quality-grade.md`
   arrived after this verdict's first write: verdict **ACCEPT-WITH-FIXES**, all
   hard gates re-derived PASS first-hand (baseline 83/83, own three probe legs,
   own keccak oracle, own rehearsal 84/84 with README `1cd05260…` and prior-83
   byte-identical, 19/19 ids resolved, both prior entries' recheck lines
   re-derived). Its four fixes, each re-verified by this seat against the tree:
   **R-F1** the entry's SC-1 brace group lists `c1-inventory.txt` under
   `SC-1/evidence/` but the file is `SC-1/c1-inventory.txt` — confirmed by `ls`;
   **R-F2** the EX-09 brace expansion
   `probe/vy-{runtime,creation}-{hex,raw,0xhex}-{6.4.0,6.7.0}.json` produces 12
   names of which **2 do not exist** (`vy-{runtime,creation}-0xhex-6.7.0.json`;
   the `0xhex` legs are 6.4.0-only) — confirmed by this seat's expansion;
   **R-F3** scope "this entry's scribe's own five probe envelopes" — RV-2
   established they are deterministic re-derivations on the same paths (not
   copies), and the wording should say so; **R-F4 (QUALITY row 15)** the
   id-domain observation cites no corpus file (add `corpus/QUALITY.md:24-25`).
   Two advisories: A1 reorder the id-domain sentence so the true
   path-sensitivity legs (EX-10 `b2-altpath-copy`/`ino-*`, EX-07 D-series) lead —
   the `var-*` legs are cwd/TMPDIR variants at ONE path; A2 re-derive the
   ledger's stale `EX-02/custody-stat-readonly.txt` pin (`f9ae3dbc…` →
   `67b1014e…`; the entry cites that file without a hash, so the entry is clean).
7. **Seat reports:** `EX-03`, `EX-04`, `CR-1` and `RV-2` landed their reports
   after this verdict's first write and are folded in here — EX-04's A4
   re-measurement is the basis of debt 5 (F3); CR-1's report carries the five
   entry edits in debt 3; EX-03's report documents the 13/22 partial reading of
   its own hand-written decoder (this seat's byte check shows all 22 selectors
   sit at genuine `PUSH4` sites, so the probe's 22/22 is right and the decoder is
   scope-limited). `EX-01`'s report is the environment census artifact itself.
   **All 16 c1 seats now have reports** — the chain is complete.
8. **Honest-stop branches not triggered — recorded, not assumed:** the claim's
   pre-written stops (venv infeasible; typed refusal; partial recovery) were
   checked against the tree: the install succeeded on py3.14 via a source-built
   `immutables`; every runtime leg recovered K/K; creation/initcode legs are
   parsed-and-empty **by class** (r1/r3 class, not a partial recovery — the
   runtime is embedded in the creation blob and the tool's scope excludes it);
   trap legs (raw-over-hextext, hex-over-rawbin) reproduce as their declared
   classes. The one **delta** vs pre-registration is EX-12's r3-class 0-byte
   control (not this chain).
9. **Disclosed ordering caveats (carried from the seats' own reports):** EX-04's
   planted file is pre-compile/pre-probe by 13 s; EX-05's mirror is derived from
   EX-04's ABI; EX-07's D-series pre-registration postdates its A/B/C legs
   (disclosed in its own file); CR-1's carriers are its own compiled set (a
   distinct provenance from the claim carriers — stated in its SUMMARY).

## Attacks/refutations attempted (this seat, with verdicts)

| Attack | Verdict |
|---|---|
| "the Vyper K/K is the extractor parroting a planted list" | **REFUTED** — this seat's third keccak path (js-sha3 over the compiled ABI) reproduces the planted set on 5 carriers; RV-1's fourth path (Rust, tables derived from the LFSR) reproduces the 32-byte digests, not just prefixes |
| "zero extras is vacuous" | **REFUTED** — opcode-boundary census: 21 `PUSH4` sites, 6 of them `08c379a0`; the probe reported exactly the 15 selectors |
| "some reported selector is a false positive" | **REFUTED** — 53 selectors across 4 carriers all sit at `PUSH4 … DUP2 XOR` compare sites; 0 without a compare shape |
| "the offset rule still reads as JUMPDEST on Vyper" | **REFUTED** — 0/15 land on `0x5b`; each is `push4_pc + 11`, and `byte[offset−12]` is that selector's own compare JUMPDEST |
| "the jump table is an artifact of one carrier" | **REFUTED** — table at `0x600` is 13 uint16 entries, all JUMPDESTs, `0x5e7` ×3 sentinel, `table_off + 13*2 == len(runtime)` exactly; `selector % 13` matches the heads |
| "the projection breaks the prior 83" | **REFUTED** — 83/83 per-file byte-identical, 0 diffs, 0 missing, 1 added |
| "the token is not line-neutral" | **REFUTED** — README 190 → 190, exactly one differing line (`:38`), after-sha equals SC-1's independent rehearsal |
| "the recheck line does not reproduce" | **REFUTED** — five-way byte-identical envelope `68415a3d…` |
| "the citation-drift table breaks at the landing" | **REFUTED** — findings=0 both modes at HEAD and at the projected commit |
| "the entry's `69656e74` sentence reproduces" | **SUSTAINED (RV-1)** — it does not; repair required (debt 1) |
| "the entry's `same path` sentence is true" | **SUSTAINED (this seat)** — it is false; repair required (debt 2) |
| "a solc-shaped reconciler is safe on this tree" | **SUSTAINED (CR-1)** — it returns empty on 33/33 Vyper carriers and flags correct selectors as extras (debt 3.4) |
| "the r3 entry's 6.7.0-specific delta is still accurate" | **SUSTAINED (EX-07)** — it is a 6.5.0 boundary (debt 4) |
| "the payable-read delta is a Vyper dispatcher-shape effect" | **SUSTAINED (this seat + EX-04 A4)** — it tracks argument count, not dispatcher shape; the same class reproduces on the r3 solc carriers (debt 5) |
| "EX-03's 13/22 decoder reading means the probe over-reports" | **REFUTED** — this seat's byte scan: all 22 selectors sit at genuine `PUSH4` sites (each at one distinct offset, prev byte `0x63`), and this seat's shape census found 0 selectors without a compare-shaped site on that carrier |
| "the entry's SC-1 inventory citation resolves" | **SUSTAINED (RV-2 R-F1)** — the file is `SC-1/c1-inventory.txt`, not under `SC-1/evidence/`; confirmed by this seat |
| "the entry's EX-09 brace expansion resolves" | **SUSTAINED (RV-2 R-F2)** — 12 names expand, 2 (`vy-{runtime,creation}-0xhex-6.7.0.json`) do not exist; confirmed by this seat's re-expansion |
| "the id-domain observation's `var-*` legs demonstrate path-sensitivity" | **SUSTAINED (RV-2 A1)** — those legs are cwd/TMPDIR variants at ONE path (all `ev_45849c8b…`); the claim holds on EX-10's `b2-altpath-copy`/`ino-*` and EX-07's D-series |

## Seat delivery status at verdict time

c1 roster (16): PL-1, EX-01..EX-10, SC-1, RV-1, RV-2, CR-1, VZ-1.
**All 16 have reports and artifacts** — the chain is complete. RV-2's report +
`quality-grade.md` landed last (ACCEPT-WITH-FIXES; debt 6). `EX-01`'s report is
the environment census artifact itself. This seat (VZ-1) writes last.

## Closing procedure (what flips the remaining parent-side words to green)

1. Apply F1 (RV-1's patch), F2 (this seat's repair text), F3 (this seat's repair
   text) and RV-2's R-F1/R-F2/R-F3/R-F4 to the entry literal **before landing**;
   consider CR-1's Edits 1, 3, 4, 5 (2 is already satisfied); re-derive the
   literal's identity after the edits (rule #14) — it is `da42d9a2…` at 32 lines
   / 18,166 B as measured.
2. Land the entry as `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md` and
   the **additive** token line from `records-drafts/map-token-patch.md`; keep
   token == landed stem; insert/delete no lines.
3. Re-run command A at the work commit from real Git objects — expect 84/84,
   missing [], dangling [], 14/14 with the prior 83 byte-identical (this seat's
   clone projection is the pre-flight).
4. Re-run the citation-drift probe at the work commit (both modes) — expect
   findings=0.
5. Apply EX-07's r3-entry patch (debt 4) if the r3 entry is in this round's edit
   scope; re-pin the ledger's stale `custody-stat-readonly.txt` hash (RV-2 A2).
   RV-2's grade gap is **closed** (debt 6, rev 2).

## Verdict basis note (evidence discipline)

Every row cites a landed file plus a command result or digest. Parent-side rows
are labelled as such and were exercised on a clone at the measured numbers, not
claimed as committed. No seat report was treated as evidence without at least one
first-hand measurement by this seat against the landed bytes — including the
five-carrier K/K re-derivation, the recheck run, the opcode-boundary census, the
dispatch-site shape census, the offset-rule re-derivation, the jump-table parse,
the clone projection, and the four instrument runs. The three entry defects this
verdict names (F1/F2/F3) were each re-derived from bytes by this seat before
being recorded; RV-2's four reviewer fixes were each re-verified against the
tree by this seat (R-F1 by `ls`, R-F2 by re-expanding the brace group, R-F3/R-F4
by reading the graded literal). RV-2's grade and RV-1's, CR-1's, EX-04's and
EX-07's findings are folded in as debt with attribution; none was accepted on
the strength of the reporting seat's word alone.

**Update at rev 2 (identity):** this verdict's own byte-identity is recorded in
`claims/c1/VZ-1/evidence/SHA256SUMS.txt` (re-derived after rev 2's final write);
the rev-1 row in that file is superseded. Re-derive it if this file is revised
again (rule #14).
