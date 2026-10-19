# C1 verdict — EVM optimizer-enabled dispatch shapes (chain convergence, seat VZ-1)

Wave `arc3-loop1-round3` · chain c1 · 2026-10-19 · repo
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin` · HEAD at verdict work
`c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311` (no seat commits; parent integrates).
Frozen claim: `claims-frozen.md:16-36`.

**Revision history of this file.** rev 1 (~13:16Z) and rev 2 (~13:20Z) were
written by this seat pre-interruption and are superseded by this rev 3, written
after the LATE-JOIN reconciliation (this seat's second run). rev 2 was accurate
for the state it measured, but the wave kept delivering: the entry draft moved to
**rev 4** (literal `3b5f371e…`, 17,708 B, mtime 13:17:51Z local) and the
map-token patch was **amended** (records-drafts copy now `9af31408…`, mtime
13:17:15Z; PRIMARY made additive-only), both *after* rev 2's last read. rev 3
re-derives the end-to-end state on the **current** pair and folds in RV-3's
rev-4 regrade, RV-1's audit, and this seat's own late-join measurements.

## Verdict: **VERIFIED** — every measurably-frozen component reproduced first-hand or by ≥2 independent seats; the two claim words that remain structurally open ("lands as a corpus knowledge entry + line-neutral map token", "command A re-measures 82 → 83") are parent-side landing steps whose scripts this seat executed end-to-end on the **current** rev-4 literal + additive token at the measured numbers (83/83, README 190→190, prior-82 byte-identical); no measured result contradicts the claim

Rationale: the frozen claim requires (a) ≥1 **optimizer-enabled** carrier
(`--optimize --optimize-runs 200`) compiled on-host with the pinned solc,
(b) ≥1 **non-ERC-20-shaped** carrier (payable receive/fallback + mixed
mutability, or library-bound), (c) planted selectors recovered **K/K**
(zero missing / zero extras) by `inspect-evm-interface` on both pins where
feasible, with **planted-K recorded pre-probe**, (d) the result lands as a
corpus knowledge entry + **line-neutral** map token, (e) **command A
82 → 83** with the prior 82 byte-identical. (a)-(c) are measured first-hand by
this seat (and independently by RV-3, RV-1, EX-09, RV-2, RV-4, CR-1, CR-2 and
every executor); (d)/(e) at the real work commit are the parent's landing
actions (only the parent commits) and were script-verified by this seat on the
current pair. The honest-stop branches (`claims/c1/PL-1/plan.md:262-302`,
HS-1..HS-7) were not triggered by any leg this seat ran or read: no typed
refusal on any carrier, no parse-empty on any carrier leg, no unrecorded
prologue class, no missing selector, no extras, no identity mistarget.

## Claim components — status and evidence (rev 3, current pair)

| # | Component | Status | Evidence |
|---|---|---|---|
| 1 | optimizer-enabled carrier compiled on-host, pinned solc (no install; receipt re-verified) | DELIVERED | EX-05 `CarrierB`, EX-10 `VaultB.opt200`, EX-04 `carrierB.opt200`, EX-07 `Rv2TokenOpt`, PL-1/EX-02/EX-12 further legs; receipt re-hashed by this seat at rev 3: `soljson.js 221d7a66…abad4c`, `solc/package.json b3a90035…3491` (= r1 receipt pins); **this seat recompiled `VaultB.opt200` byte-exactly** from `EX-10/VaultB.sol` + the receipted prefix: runtime 1,621 B `b24a0115…`, creation 1,655 B `ac614a6e…`, ABI `6dae6710…` (all equal to the landed `out/` files) |
| 2 | non-ERC-20-shaped carrier (payable receive/fallback + mixed mutability / library-bound) | DELIVERED | `VaultB` (library `Fees`, payable receive+fallback, 13 fns), `CarrierB` (payable receive+fallback, library-bound `Ledger` inlined under the optimizer, 8 fns), `carrierB`@EX-04 (2-of-3 multisig vault, 11 fns, zero ERC-20 selectors), `CarrierA` (9 fns), `VaultA` (7 fns) — no ERC-20 token shape among them |
| 3 | planted selectors recovered K/K, zero extras, both pins where feasible | DELIVERED | **this seat re-derived all 7 primary legs at rev 3** with the receipted `js-sha3` (ABI keccak vs planted file vs sealed envelope, set-equality): VaultB opt200 13/13, VaultB nopt 13/13, carrierB@EX-04 opt/noopt 11/11, CarrierB 8/8, CarrierBErr 8/8, Rv2TokenOpt 5/5 — `abi == env == planted` **true on every leg**, `dispatch:"abi"` on every recovered entry; **own 6.7.0 run** on VaultB.opt200 re-derived `ev_ae5aaee0…` = the landed envelope (13/13, decoded `b24a0115…`); 6.5.0/6.7.0 landed legs spot-read (13/13, 8/8, 5/5 ×3, decoded sha equal on every leg) |
| 4 | planted-K recorded pre-probe | DELIVERED with one disclosed correction | mtimes (this seat, rev 3): EX-10 planted 13:07:24Z < first envelope 13:08:10Z (46 s); EX-05 planted 13:08:11Z < envelope 13:08:21Z (10 s); EX-04 scratch ordering (planted written 13:08:25.41Z, probe 13:08:25.41Z — same-second; EX-04's seat report §1 documents the scratch ordering and that copies preserve bytes not mtimes); EX-07's v1 hash-format bug corrected post-probe (planted-K mtime 13:08:53Z > its first leg 13:08:02Z), selectors anchored to r1's pre-existing `expected-selectors.txt` oracle — disclosed in its own `note`, and this seat re-verified its 5/5 independently |
| 5 | result lands as corpus knowledge entry + line-neutral map token | PARENT-SIDE, script-verified on the CURRENT pair | rev-4 literal `3b5f371e…` (17,708 B) + additive PRIMARY token `786efbb2…` (280 B, byte-identical to RV-4's `caller-option-strict-additive.patch` new line — verified by this seat); applied to a fresh `git clone --no-hardlinks` at HEAD: command A **83/83**, missing [], dangling [], 14/14; README **190 → 190**, exactly one line differs (`:38`), after-sha `a451ad16…`; all 82 prior knowledge files byte-identical; `git diff --name-status` = exactly `M corpus/README.md` + `A corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md`. RV-3's independent rev-4 rehearsal (pristine `git archive` tree) agrees: 83/83, README `a451ad16…`, prior-82 `diff -rq` clean, SKILL `cmp` clean (`RV-3/evidence/commandA-rehearsal-rev4.txt`) |
| 6 | command A 82 → 83, prior 82 byte-identical | PARENT-SIDE, script-verified on the CURRENT pair | before: this seat's exact-recipe run at HEAD `c07af80f` = 82/82, missing [], dangling [], 14/14, 10.0/10.0 (rev 3 re-run; also PL-1, SC-2, SC-1, RV-4, EX-12, EX-14, RV-3); after: this seat's clone projection = 83/83 (same fields), prior-82 manifest byte-identical. Authoritative re-measurement at the work commit is the parent's |
| 7 | recheck line executes verbatim | DELIVERED | this seat ran the entry's literal recheck at rev 3 (repo cwd, `TMPDIR=/var/tmp/cr3-recheck`): 6.4.0 → `ev_d409bd50…`, envelope sha256 `05f76b33…`, 13 fns, decoded `b24a0115…` — **byte-identical to EX-10's capture and SC-2's copy** (three-way, `cmp`); 6.7.0 → `ev_ae5aaee0…` = the landed 6.7.0 envelope's id; RV-3 re-ran the 6.4.0 line independently (`RV-3/evidence/recheck-opt200-rev4-verbatim.json`, same `05f76b33…`) |
| 8 | probe-inert landing (no drift instrument breaks) | MEASURED | this seat ran the citation-drift probe: **findings=0 exit=0 in default AND strict at HEAD** (`bfc42f1b…` table == the `expected.json` digest pin) **and at the projected scratch commit**; selftest **13/13 exit 0**; RV-4's independent scratch-clone rehearsals agree for before/after; the `readme38-arc3r1-token` anchor survives the additive line by construction |

## Before → after reconciliation (the discriminating unit)

- **Before (r1 surface, re-measured at HEAD):** r1's entry scope named the
  Unknown "optimizer-enabled dispatch shapes beyond the smoke compile"; r1's
  carriers were optimizer-off (Rv2Token, 1,943 B) or a solcjs `--optimize`
  smoke leg; command A 82/82 at `c07af80f`.
- **After (this wave):** five optimizer-enabled carrier families recovered
  K/K across two pins, with same-source optimizer-off controls where feasible —
  the measured dispatch-shape deltas: runtime 1,943 → 978 B (Rv2TokenOpt),
  3,163 → 1,621 B (VaultB), 3,872 → 1,850 B (carrierB@EX-04), same recovered
  set under both optimizer states; prologue class `5f3560e01c` unchanged on
  all compiled carriers (offset carrier-dependent); binary-search dispatch
  layouts at K=8/11/13 vs r1's linear chains — all EVMole-parseable, zero
  extras; first pure-leg mutability delta (`pure → view`) on **two** selectors
  — EX-04's `computeTxHash` and EX-02's `stamp()` (`c85e07b9`, RV-1's
  correction to rev 2; 35/351 entries across 35 envelopes) — recorded as an
  upstream-inference delta, not a defect.
- **Headline numbers:** probe K/K zero-extras on **8 carriers / ≥20 legs**
  first-hand or envelope-read (this seat's 8-run matrix + 6.7.0 spot-checks +
  the rev-3 7-leg re-derivation); command A 82 → 83 at the clone projection;
  prior-82 byte-identity True; README 190 → 190 (`a451ad16…`).
- **Byte-level zero-false-positive corroboration (this seat, rev 3):** opcode-
  aware PUSH4 census on three carriers — VaultB.opt200's 24 PUSH4 sites are the
  13 selectors (two duplicated by the GT/EQ binary search) + 4 panic/error
  constants + 2 trailer-derived; VaultB.nopt's 16 sites are the 13 selectors
  (two duplicated) + 1 trailer-derived; Rv2TokenOpt's 7 sites are 5 selectors +
  `4e487b71` + the trailer constant `43000825` (site 971 ≥ cborStart 927).
  None of the non-selector constants was reported as a function on any leg —
  the zero-extras clause is exercised on real decoys, not vacuous.

## Named debt (measured residuals; none voids the claim)

**Entry-text fixes, status re-checked by this seat against the rev-4 literal.
RV-3's `RV-3/proposed-entry-fixes-rev4.patch.md` (`1e191bd8…`) carries
apply-by-content text for R1/R2/R3/R4/F1/R5a; CR-2's and CR-1's patch texts
remain valid where not superseded:**

1. **F1 — internal contradiction (CR-2, sustained; still in rev 4).** Line 28
   ends "r1's `60003560e01c`-class and non-binary prologues remain unvisited
   this round" while the round re-probed exactly those (carrier-A
   `60003560e01c` 3/3; Rv2TokenOpt linear `EQ`-only 5/5). Fix:
   `CR-2/proposed-entry-text-fixes.patch.md` §F1 / RV-3 FIX-5.
2. **F2 — citation overclaim (CR-2, sustained; still in rev 4).** The
   `optB-{hex,raw}-{6.4.0,6.5.0,6.7.0}{,-rerun}.json` expansion produces 5
   names that never existed (`optB-{hex,raw}-{6.4.0,6.5.0}-rerun.json`,
   `optB-raw-6.7.0-rerun.json`; only `optB-hex-6.7.0-rerun.json` exists). This
   seat's own brace-expansion sweep (rev 3) confirms: the ONLY unresolved
   citation names in the literal are this set. Fix: write the actual set.
3. **F3 — dead path (this seat + CR-2, **FIXED in rev 4**).** The literal now
   reads `EX-04/planted-B.txt` (root) — exists, sha256 `f32393c0…` matches. ✓
4. **F4 — dead paths (CR-2, sustained; still in rev 4).** The offset-check
   outputs live at `EX-04/evidence/probe/offset-check-{opt200,noopt}.json`, not
   `EX-04/evidence/offset-check-*.json` (that name is the script
   `EX-04/evidence/offset-check.js`). Both the line-5 listing and the line-37
   Sources entry are wrong. (RV-3's FIX-3.)
5. **CR-1 Edit 1 — id comparator advice (this seat's own envelope confirms;
   still in rev 4).** Line 30's "compare by `subject.digest.sha256`" is
   costume-dependent: for hex carriers subject digest = the `.hex` file's
   digest (my 6.4.0 run: subject `9a1fbfab…` = file sha; decoded
   `b24a0115…` = runtime). Fix: compare by decoded
   `normalized_result.bytecode.sha256` (+ payload).
6. **CR-1 Edit 2 — CBOR-trailer wording (sustained, partially addressed).**
   `43000825` is read out of the terminal CBOR trailer by a whole-file sweep
   (code region ends at byte 927; site 971); rev 4 does identify it as "the
   CBOR trailer constant", which addresses the substance — the residual is the
   "5 of 7 immediates" count's whole-file scope.
7. **CR-1 Edit 3 — r1 erratum (measured refutations; NOT applied in rev 4).**
   (a) r1's "creation blobs carry no runtime dispatch table" is false at byte
   level (creation blobs embed the runtime and its EQ;PUSH2;JUMPI sites; the
   probe's 0 is tool scope); (b) r1's "sole non-dispatch PUSH4 constant
   `16ee4b79` @1900" is a metadata artifact (code region ends at 1890). SC-2's
   parent note "no erratum is needed" is superseded by this measured append.
8. **F6 — identity sidecar (CR-2/RV-3, sustained).** `SC-2/README-identities.txt`
   pins the draft at 21,585 B / `5c1818c7…` and the token at `333ca590…` — a
   revision that no longer exists (records-drafts draft is 22,628 B /
   `d9004f48…`; SC-2 mirror 22,071 B / `9b0cb5b8…`; token patch now
   `9af31408…`). Re-derive at landing (rule #14). The literal itself does not
   cite this sidecar.
9. **F5 (advisory) — creation-identity convention.** The quoted creation
   hashes are sha256 over decoded creation bytes, while r1's entry quotes the
   `.hex`-file hash — state the convention once.
10. **F7 (advisory, framing) — "dispatch shapes" vs measured variable.** The
    critics' paired measurements sustain "the optimizer did not change the
    shape class or selector order; it changed bodies/sizes/jump targets — the
    measured variable is selector recovery." Optional stem rename
    `…-optimizer-carriers` (must re-pair the map token if taken).

**Other measured residuals:**

11. **Map-token variant divergence — RESOLVED in rev 3's favour.** SC-2's
    post-verdict amendment made the records-drafts PRIMARY additive-only; this
    seat verified the extracted PRIMARY line is byte-identical to RV-4's
    strict-additive patch new line (`786efbb2…`). Landing must use the
    **records-drafts** copy (the SC-2 mirror still carries the superseded
    reworded variant `333ca590…`, after-README `016b632e…`). The additive
    variant's after-README sha is **`a451ad16…`** (measured by this seat and by
    RV-3).
12. **EX-07 `optB-and-legA-compare.txt`:** the stale "VERDICT: MISMATCH" string
    is gone from the landed artifact (rev 3 grep: the compare text now reads
    "K/K on every leg"); the underlying data was always K/K (this seat's
    independent 5/5). Residual closed by regeneration.
13. **EX-12's pre-registered 0-byte control delta:** expected
    `invalid_request` refusal; measured parsed-and-empty success (n=0, decoded
    `e3b0c442…`) — EX-12's own report records it FALSIFIED; parent adjudicates.
14. **EX-04 planted-B scratch mtimes; SC-2 revision-log timestamps postdate
    their files' mtimes — use mtimes, not the labels.**
15. **Two different literals and two token variants exist in the tree**
    (RV-3's landing hazard, confirmed by this seat): records-drafts draft rev 4
    `3b5f371e…` + additive token `786efbb2…` are the current pair; the SC-2
    mirror (`9b0cb5b8…` literal `189ac2a2…`) and the SC-2 token copy
    (`333ca590…`) are superseded. Land one of each, paired, from the
    records-drafts copies.

## Attacks/refutations attempted (chain roll-up, with verdicts)

| Attack class | Seats | Result |
|---|---|---|
| Wrong-encoding trap (raw over hex text) | EX-04 trap leg, EX-10, entry observation, RV-1 §4.4 | reproduced as parsed-and-empty (exit 0, 0 fns, decoded sha = file's own sha) — HS-7 class, no survivor claim |
| Decoy/false-positive hunt (deadbeef, ffffffff, error selectors, CBOR constants) | EX-06/EX-07 carrier-A, EX-10 decoy carriers, EX-05 CarrierBErr, EX-09, RV-1 §4.2, this seat's PUSH4 census | zero false positives on every leg |
| Missing-selector hunt (optimizer inlining could drop dispatch entries) | all executors + this seat's independent sweep | none missing; optimizer changes bytes not the recoverable set |
| Identity mistarget (envelope decoded sha ≠ pinned runtime) | this seat re-checked every envelope it read (rev 3) | all match pinned runtime sha |
| Id-domain overclaim | EX-11 six-lane re-derivation; EX-07 path sweep; this seat's rerun + 6.7.0 cross-pin | ids re-derive same-path/request; path-sensitive across paths — family-scoped, no formula claimed |
| Pre-probe reordering (post-hoc planting) | mtimes on EX-10/EX-05/EX-04 (+EX-07 disclosed correction); RV-1 §4.1 re-derived from scratch | no leg's planted set was fitted to probe output |
| Manifest drift in landing (prior-82, token pairing) | this seat's clone projection + prior-82 manifest; RV-4 tool + coupling rehearsal (token-without-file → dangling, measured) | clean; token==stem pairing enforced |
| Solc receipt drift / install creep | this seat re-hashed both pinned files + byte-exact recompile; EX-04/PL-1/RV-3 receipt re-verify | receipt holds; no install this wave |
| Large-K dispatch pressure (truncation?) | CR-1 `Cr1Big` K=25 (25/25), CR-2 `CrWide` K=22 (22/22 opt-on **and** off) | held — no truncation, zero extras |
| Metadata-region false positives (CBOR trailer, Panic, error constants) | CR-1 census; this seat's whole-file sweep + decoded digest check; EX-05 CarrierBErr; EX-09 §4.5 | probe never reports metadata/error constants |
| Optimizer body-merge (identical bodies share a dispatch target) | CR-1 O3 (three selectors → one target) | all selectors still reported — no loss, zero extras |
| Costume retry on partial recovery | CR-1 `audit-seat.js` over 233 envelopes; EX-12 rerun byte-identity | no partial→full transition anywhere; tampered VaultCourt selector followed the bytes — byte-truth |
| Input-class edges (0-byte file; source `.sol`; ABI json) | EX-12 controls; CR-1 note | non-bytecode hex text → typed `invalid_request` exit 1; 0-byte → parsed-and-empty — delta vs pre-registration, recorded FALSIFIED |
| Availability→holding leakage | CR-2 A2 | refuted for the draft/artifacts |
| Shape-class generalization beyond the round's two carriers | CR-2 A1a/A1b, CR-1 census, EX-09 §4.7 | recovery generalizes (5/7/22/25 selectors, linear+binary); the optimizer did **not** change the shape class — sustained refinement (debt #10) |
| "The pre-interruption verdict covers the current draft" | RV-3, this seat (rev 3) | **SUSTAINED** — rev 4 landed after rev 2; this rev 3 re-derives on the current pair |
| "The rev-4 fixes closed the prior defects" | RV-3, this seat | **PARTIALLY SUSTAINED** — F3 fixed; F1/F2/F4, CR-1 Edits 1-3, R1/R2, F6 unchanged (see debt) |
| Verdict enumeration gap (pure→view) | RV-1 §4.3 | **SUSTAINED** — rev 2 named only EX-04's `computeTxHash`; EX-02's `stamp()` (`c85e07b9`) is the same class. Corrected in this rev 3 |

## Seat delivery status at verdict time (rev 3)

All 24 c1 seats have landed seat reports or artifacts **except EX-14**
(projection artifacts landed; **no `seats/EX-14.md`** — named as the one
missing seat report) and this seat (VZ-1, writing now). Since rev 2, RV-3,
RV-1, EX-09, RV-2 and the executors' late reports all landed. The parent's
roster reconciliation counts the dispatch items array, not this tally.

## VZ-1's own verification runs (this seat, rev 3 = late join)

| Run | Command (abridged) | Result |
|---|---|---|
| baseline | command A, SCORECARD recipe, `git show` form, at HEAD | 82/82, 14/14, missing/dangling [] |
| solc re-verify | `sha256sum …/solc-prefix/node_modules/solc/{soljson,package}.json` | `221d7a66…`, `b3a90035…` = r1 receipt |
| recompile | `node EX-10/compile.js <abs-prefix> EX-10/VaultB.sol <out> 1 200` | runtime `b24a0115…` 1,621 B, creation `ac614a6e…`, ABI `6dae6710…` — byte-exact |
| K/K re-derive | `node kk-rederive.js` (js-sha3 from receipted prefix; ABI vs planted vs envelope) | 7 legs: `abi == env == planted` true; `dispatch:"abi"` everywhere |
| recheck 6.4.0 | entry's literal recheck, `TMPDIR=/var/tmp/cr3-recheck` | `ev_d409bd50…`, `05f76b33…` = EX-10 = SC-2 (three-way `cmp`) |
| recheck 6.7.0 | same form, `rea-agents@6.7.0` | `ev_ae5aaee0…` = landed 6.7.0 envelope; 13/13 |
| probe | citation-drift at HEAD + at projected commit, default + `--strict` | findings=0 exit=0 ×4; `--selftest` 13/13 exit 0 |
| projection | fresh clone at HEAD + rev-4 literal + additive token, commit, command A | 83/83, prior-82 identical, README 190→190 `a451ad16…`, changed lines [38] |
| PUSH4 census | `node push4-census.js` (opcode-aware) | VaultB opt 24 sites / nopt 16 sites / Rv2TokenOpt 7 sites; non-selector constants unreported |
| citation sweep | brace-expansion over the rev-4 literal (154 candidates) | 12 unresolved — exactly the `optB-…-rerun` set (F2) |

Evidence: `claims/c1/VZ-1/evidence2/` (projection-final.json,
recheck-vaultb-opt200-640.json, recheck-vaultb-opt200-670.json,
kk-rederive.txt/.js, push4-census.txt/.js, citation-sweep-final.txt,
literal-final-rev4.md, SHA256SUMS.txt) + the pre-interruption `VZ-1/evidence/`
and `VZ-1/verification-log.txt`.

## Closing procedure (what flips the remaining parent-side words to green)

1. Apply the entry-text fixes **before landing** — RV-3's
   `proposed-entry-fixes-rev4.patch.md` (FIX-1 R1, FIX-2 R2, FIX-3 R3,
   FIX-5 F1, FIX-6 R5a) plus CR-2's F2 text and CR-1's Edits 1-3 — by content
   match, then re-derive the draft's identity (rule #14).
2. Land the entry file
   (`corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md`, or the
   renamed stem if F7's option is taken) from the corrected literal.
3. Apply the **additive** map token from the **records-drafts** copy
   (`786efbb2…`); keep token == landed stem; do not insert/delete lines.
4. Re-run command A at the work commit from real Git objects; expect
   83/83, missing [], dangling [], 14/14; re-run the citation-drift probe at
   the work commit (both modes) — expect findings=0 (this seat's clone
   projection is the pre-flight).
5. Re-pin `SC-2/README-identities.txt` (or drop its stale rows) at landing.

## Verdict basis note (evidence discipline)

Every component row cites a landed file plus a command result or digest; the
parent-side items are labelled as such and were exercised on a clone at the
measured numbers, not claimed as committed. No seat report was treated as
evidence without at least one first-hand measurement by this seat against the
landed bytes — including the recompile, the 7-leg K/K re-derivation, the two
recheck runs, the four probe runs, the clone projection, the PUSH4 census, and
the citation sweep.
