# CR-2 attack notes — language/scope attacks on C1 (arc3-loop1-round3)

Seat CR-2, chain c1, critic. Written 2026-10-19T13:12Z; revised after the entry
draft lands (identity re-derived per rule #14). All measurements by this seat on
`/var/tmp/cr2r3/` scratch with the r1 receipted solc prefix
(`.ufo/waves/arc3-loop1-round1/tools/solc-prefix/`, receipt independently
re-verified: tarball `0e1a1ab6…575a51` = npm-cache sha256; `soljson.js`
`221d7a66…abad4c`, `solc.js` `188c3fdc…5146f`, `solcjs --version`
`0.8.37+commit.f401782d.Emscripten.clang` — all match
`claims/c1/EX-02/install-receipt.txt` §1/§5/§6). Probe legs: `npx -y
rea-agents@{6.4.0,6.7.0}` from the host npx cache (`npm_config_offline=true`),
disk-backed `TMPDIR=/var/tmp/cr2r3` per the r1 entry's recheck note.

## Attack A1 — "optimizer shapes held" generalization beyond the two carriers

**Sub-attack A1a (does the recovery generalize?).** Four independent carriers
built by this seat (two shapes the round did not use), probed at both pins:

| carrier | shape | opt | runtime sha256 | K | probe |
|---|---|---|---|---|---|
| Rv2Token (r1 source `a4bc2d78…`, recompiled) | ERC-20 | off | `c1081a56…` (= r1 pin) | 5/5 | recheck leg, `ev_45849c8b…` |
| Rv2Token | ERC-20 | r200 | `ed6c8a76…` 978 B | 5/5 | `ev_729d908e…` / `ev_fe745dcb…` |
| CrVault (payable receive/fallback, mixed mutability) | non-ERC-20 | off | `8fe0b21a…` 1777 B | — | not probed (control only) |
| CrVault | non-ERC-20 | r200 | `2e636c0f…` 861 B | 7/7 | `ev_b7c10ecf…` / `ev_c2fbe2e1…` |
| CrWide (22 external fns, binary-search dispatch) | non-ERC-20 | off | `83040705…` 2940 B | 22/22 | `ev_fd94e1cb…` |
| CrWide | non-ERC-20 | r200 | `617c91cc…` 1542 B | 22/22 | `ev_65542703…` / `ev_072902e9…` |

Zero missing / zero extra in every leg; planted sets keccak-derived from the
compiled ABIs with the prefix's `js-sha3@0.8.0`; every reported
`bytecode_offset` lands on byte `0x5b` (JUMPDEST). **Verdict: the recovery
result generalizes past the round's two carriers in my hands** (23, 7, 5
selectors; linear and binary-search dispatch; both pins). The extracted
mutability strings were consistent with the ABIs (incl. `payable` on
`donate()`), but are upstream inferences, not verified signatures.

**Sub-attack A1b (is "optimizer shapes" the measured variable?).** Six
compiler pairs (my carriers + PL-1's `OptVault`/`MutMix`, recompiled from their
pinned sources — their runtime sha256s re-derived byte-exact: `544469b7…`,
`6267ef53…`, `200bc9db…`):

- opt-off vs opt-on first-diff offsets: 0x0b (OptVault), 0x0b (CrWide), 0x26
  (CrVault), 0x26 (MutMix), 0x32 (Rv2Token) — i.e. the common prefix always
  covers the runtime prologue + `60043610` calldatasize guard + `5f3560e01c` +
  the first `8063<sel>14` compare; only jump destinations differ.
- prologue-class census over all 14 compiled binaries: `5f3560e01c` in every
  dispatcher carrier at both settings; `60003560e01c` in none.
- the linear (`1461`) vs binary-search (`1161`) split tracks selector count, not
  the optimizer: CrWide uses `1161` with the optimizer **off** as well.

**Verdict: sustained.** "Optimizer-enabled dispatch *shapes* held" is a
mislabel: the optimizer changed bodies, sizes (1943→978; 1769→776; 1061→497 B)
and jump targets, not the dispatch shape class. The measurable claim is
"selector recovery held on optimizer-enabled runtime carriers". Any entry or
map-token text built on the shape phrasing (incl. the stem/token
`…-evm-optimizer-shapes`, `claims/c1/records-drafts/map-token-patch.md`) should
either rename or carry one disambiguating sentence.

## Attack A2 — availability → holding inference

- The verb was **run**, not merely available: 8 probe envelopes this seat plus
  the recorded `available/held` distinction is respected in every leg
  (`runtime_execution: "not-performed"` inside the envelopes; the holding claim
  is about selector recovery only).
- The r1 recheck line reproduces **exactly** at 13:08Z (`ev_45849c8b…`, 5
  functions, `dispatch:"abi"`, decoded `c1081a56…`) — the recorded invocation
  form is real, not asserted.
- Risk to police in the draft: "both pins where feasible" as a blanket escape
  hatch. Measured: both pins work on every carrier I and PL-1 ran; the only
  single-pin legs are PL-1's `MutMixOpt` (6.4.0 only) and SC-1's opt pairs.
  The entry must name any carrier that is not both-pin, or drop the clause.
- Risk to police: any "supported/handles/works for optimized bytecode"
  sentence without a carrier citation — QUALITY.md row 10 (`"Held/works" is
  admitted only for verbs run on a real or synthesized carrier this round`).

**Verdict: no violation found in the artifacts seen so far** (PL-1's probes
carry per-carrier envelopes); the two police-risks above are the checks to
apply to the drafted entry text.

## Attack A3 — contradiction with r1's Unknowns wording (r1 entry vs round text)

r1 facts (verbatim): the Smoke compile **was** optimizer-enabled
(`solcjs --bin --abi --optimize`, `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:11`)
and its probe leg was creation-code, parsed-and-empty (`:15`, `:24`); the
Unknowns list names "optimizer-enabled dispatch shapes beyond the smoke
compile" (`:29`); Scope says "RESULT-class exercise only — no Core promotion,
no availability→holding claim" (`:31`).

Consequences the draft must satisfy:
1. No "first optimizer-enabled compile" phrasing — the smoke compile was one;
   the correct novelty is **first optimizer-enabled *runtime* carriers probed**.
2. The smoke leg's creation blob did contain the optimized dispatcher's bytes
   (receipt §5b shows `…395ff3fe608060405260043610610049575f3560e01c…`), but
   the extractor never recovered it (0 functions, `bytecode.kind:"unknown"`) —
   say that, rather than implying optimizer-enabled bytes were never compiled.
3. The r1 Unknowns line is **not to be edited**; the new entry carries its own
   Unknowns with the residue named (other `--optimize-runs` values, `via-ir`,
   optimizer settings beyond runs=200, sizes above the ~1.9 KB class, other
   solc versions). One round with two carriers cannot close the class.
4. Scope sentence parity with r1 (`:31`): RESULT-class, family-scoped to
   `solc-0.8.37` runtime carriers under the two REA pins.

**Verdict: pending** — no round text exists yet; the checks above are frozen
here and will be applied to the drafted entry on arrival. (Round-3 constraint
source: `claims-frozen.md:16-36`.)

## Side measurements (landing hygiene, offered to the parent)

- **Overlay rehearsal** (line-neutral map token + stub entry on a scratch copy
  of `corpus/`+`SKILL.md`, `evidence/scripts/cmdA-wt.py` self-tested equal to
  recipe A on the pristine worktree): `83/83, 14/14, missing [], dangling [],
  10.0/10.0`; README 190 → 190 lines, exactly 1 changed line, token set 82 → 83
  with **no prior token removed**, new token = the SC-2 stem.
- **Default-runs equivalence**: `--optimize` (default) and `--optimize-runs
  200` are byte-identical for both sources tested (`ed6c8a76…`; `2e636c0f…`).
  The claim's parenthetical is satisfiable by either, but the entry must record
  the command actually run (a claimed flag that was not passed is a fabrication
  even when the bytes agree).
- **Pre-existing map observation**: the coverage-map section contains a second
  occurrence of `2026-10-18-arc2-r7-pe-wall` (bare path form in the PE row);
  set-based recipe A is unaffected. Pre-existing at HEAD, not this round's.

## Text attack on the drafted entry (SC-2 draft; revisions read: rev 2 sha256 `b9ca0310ca7ef099…`, 106 lines, 13:14Z; rev 3 sha256 `9b0cb5b8459313f7…`, 108 lines, 13:20Z — findings T1–T5/T9 unchanged at rev 3)

Full fixes with exact before/after text: `proposed-entry-text-fixes.patch.md`.

| # | Attack | Verdict | Receipt |
|---|---|---|---|
| T1 | Line 42: "r1's `60003560e01c`-class and non-binary prologues remain unvisited this round" — contradicted by the entry's own carrier-A control (that exact class, re-probed 3 pins × hex/raw) and by Rv2TokenOpt's linear `EQ`-only tree (5 EQ, 0 GT, 5/5) | **SUSTAINED** | `EX-07/legA-hex-6.4.0.json` bytecode head `60003560e01c8063a9059cbb146026…`; my byte census in `evidence/shape-analysis.txt`; draft lines 32/39/45/47 |
| T2 | Lines 20/51: `optB-…{,-rerun}.json` claims 6 rerun envelopes; 1 exists | **SUSTAINED** | `ls EX-07 \| grep rerun` → only `optB-hex-6.7.0-rerun.json` (+ legA/legC reruns) |
| T3 | Line 28/51: `EX-04/evidence/planted-B.txt` `f32393c0…` | **SUSTAINED** (file is `EX-04/planted-B.txt`, 467 B, `f32393c0…` re-derived) | sha256 + path check |
| T4 | Lines 36/51: `offset-check-*.json` paths | **SUSTAINED** (actual: `EX-04/evidence/probe/offset-check-{opt200,noopt}.json`) | `ls EX-04/evidence/probe/` |
| T5 | "creation" hashes reproduce only as decoded-byte identities; CarrierB@EX-05 has no `.bin`; r1's convention differs (`.hex`-file hash) | **SUSTAINED as advisory** — all three reproduce as decoded bytes (verified); state the convention | `ac614a6e…`/`8466da5f…`/`6794c3a2…` re-derived; r1 `e6517fb7…` = `.hex` file |
| T6 | Recheck line does not reproduce | **REFUTED** — reproduced byte-identically: 13 fns, `b24a0115…`, `ev_d409bd50b370c55c…`, envelope `05f76b33…` = SC-2's capture = my run | my run under `/var/tmp/cr2r3/recheck`, envelope in `evidence/probes/` (sha `f2aec424…`/`05f76b33…` family) |
| T7 | Availability→holding leakage in the draft | **REFUTED** — no class-level holding sentence; Scope carries the r1-form caveat; both-pin usage stated per carrier | draft lines 24/49 read against envelopes |
| T8 | "first optimizer-enabled compile" contradiction with r1 (Smoke was `--optimize`) | **REFUTED** — phrasing absent; Unknowns residue (runs≠200, viaIR) carried; parent note protects r1 bytes | draft lines 47/67-69; r1 entry `:11`,`:29` |
| T9 | Title/stem "optimizer shapes" mislabels the measured variable (optimizer changes bytes/targets, not shape class; linear-vs-binary tracks selectors) | **SUSTAINED as advisory** (F7); their own pairs show first-diff 0x31 (VaultB) / 0x0b (carrierB@EX-04) | this seat's LCP measurement over EX-10/EX-04 pinned bytes |
| T10 | Map-token row "optimizer-enabled non-ERC-20-shaped carriers" plural overstates | **REFUTED** — ≥3 such carriers landed with envelopes (VaultB opt200, carrierB@EX-04 opt200, CarrierB opt200; + CarrierBErr) | `claims/c1/EX-{10,04,05}` envelopes |

Landing conditions recorded: SC-2's `README-identities.txt` — **resolved**: absent
at 13:14Z, present at 13:20Z (`claims/c1/SC-2/README-identities.txt`); the two
recheck captures present and re-derived (`05f76b33…`, `f2aec424…`). Draft
revisions attacked: rev 2 `b9ca0310…` (13:14Z) and rev 3 `9b0cb5b8…` (13:20Z,
108 lines); T1–T5/T9 still present at rev 3 — apply fixes by content match.

Corroboration added after rev 3 landed: the draft's new "convergence-seat matrix"
row cites `VZ-1/evidence/kk-matrix.json` (8 carriers, all K/K). This seat's
independent recompiles reproduce three of those rows' pinned runtimes byte-exact
(`544469b7…` OptVault opt200, `6267ef53…` MutMix noopt, `200bc9db…` MutMixOpt
opt200 — matches VZ-1's rows and PL-1's own identities), so the roster row's
numbers are independently anchored, not just cross-cited.