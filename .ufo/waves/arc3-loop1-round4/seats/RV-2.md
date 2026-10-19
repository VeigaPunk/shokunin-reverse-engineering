# SEAT RV-2 | CHAIN c1 | ROLE reviewer — arc3-loop1-round4 (2026-10-19)

Task (seat line): grade the drafted entry against `corpus/QUALITY.md` + the r1/r3
entries (incl. the honest-stop/partial forms if triggered); list required fixes.
Seat report.

**VERDICT: ACCEPT-WITH-FIXES.** Every hard gate re-derives PASS end-to-end from
my own runs; three must-fixes (F1/F2 citation, F3 provenance wording), one
QUALITY-row fix (F4, the id-domain corpus citation), two advisories. **None
changes a measured result.** The claim's honest-stop branches are correctly NOT
triggered. Grade file: `claims/c1/RV-2/quality-grade.md`.

Repo HEAD at work: `015e1bab914713568f339fd53999bc180459cc40` (read-only
`git rev-parse`). Lane: devin (`devin/deepseek-v4-1-flash-max`) — the declared
fallback dispatch (`claims-frozen.md:11-15`), not a lane signal. No git
mutations. Writes: only this report + `claims/c1/RV-2/**`. Custody paths never
opened (read-only rule held; no capture attempted). Scratch `/var/tmp/rv2-r4`
(`/tmp` never written).

## 1. Work performed (evidence pointers)

**Graded artifact.** `claims/c1/records-drafts/knowledge-entry-draft.md` 21,166 B
/ 87 lines / sha256 `df9582ac8b253e611eba194ef9b466325d23ebb9a5b5270d64a577dbc37ef094`;
literal extracted first-hand between the BEGIN/END markers — **18,166 B / 32
lines / `da42d9a23eaea87104ad71c7beacf0465a04f27482dd063d625b8e54a7161ebc`**
(≡ SC-1's `README-identities.txt` row). Method pre-registered in
`prereg-verification-plan.md` **before** the draft landed (the file was written
at 14:04Z against an empty `records-drafts/`; the draft arrived 14:10Z).

- **Baseline pinned pre-draft:** command A at HEAD (recipe A verbatim,
  `SCORECARD.md:86-124`) → 83/83, `missing []`, `dangling []`, rules 14/14,
  10.0/10.0 (`evidence/commandA-before.txt`); prior-83 knowledge-file sha256 set
  frozen (`evidence/prior-83.sha256`); README `a451ad16…`, SKILL `5eec51c0…`,
  census instrument `d0772ce8…` (`evidence/baseline-pins.txt`).
- **My own probe legs** (three, disk-backed `TMPDIR=/var/tmp/rv2-r4/tmp`,
  rea-agents 6.4.0 and 6.7.0 from the cached trees): CarrierV hex@6.4.0
  `ev_d1792f57…` 15/15, raw@6.4.0 `ev_eac08124…` 15/15, hex@6.7.0
  `ev_62e1b9e6…` 15/15; every leg `dispatch:"abi"` ×15, decoded
  `57d6fd0a…` ≡ the runtime bytes. Fresh re-run at grade time reproduced the
  envelope sha256 `68415a3d…` (determinism control).
- **Independent oracle** (`evidence/oracle-abi-keccak.txt`, `selectors.js`):
  js-sha3 keccak over `EX-04/out/abi.json` → 15 selectors, set-equal to EX-04's
  planted set AND to vyper's own `method_identifiers` (after zfill-8). Re-used
  to verify PL-1's EX03 (22/22), CarrierW (9/9) and Smoke (4/4) legs.
- **Byte-level censuses** (`evidence/push4-census.txt`,
  `evidence/vyper-dispatch-shape.txt`): 17 distinct PUSH4 immediates = 15
  selectors + `08c379a0` (6 sites) + `69656e74` (1 site), neither reported;
  prologue decode; 13-entry table at `0x600` (all JUMPDEST, `0x5e7` ×3 at
  buckets 1/7/11); 15 XOR compare sites; **offset semantics resolved** (see §3).
- **Cross-round canonical rechecks** (`evidence/recheck-prior-entries.txt`):
  r1 `ev_45849c8b…` 5/5 `c1081a56…`; r3 `ev_d409bd50…` 13/13 `b24a0115…` —
  both prior entries' recheck lines still reproduce at this HEAD.
- **Rehearsal** (`evidence/commandA-rehearsal.txt`): `git archive HEAD` scratch
  tree + literal + PRIMARY token → 84/84, `missing []`, `dangling []`, rules
  14/14; README 190 → 190, after-sha `1cd05260…` ≡ the draft's claim; prior-83
  byte-identical (83/83, 0 modified, 0 removed).
- **Id resolution** (`evidence/ids-resolve.txt`): 19/19 quoted `ev_` ids resolve
  to real envelopes.

## 2. Proposed changes

**None applied.** The fixes are text edits for the entry's author/parent; no
patch file is proposed because the defects are two name corrections plus one
wording scope, all stated in §2 of `quality-grade.md` with the measured
alternatives. I did not edit the draft (a reviewer does not revise the graded
artifact; the r3 RV-3 precedent wrote a patch file, but here the fixes are
one-clause each and the parent lands the literal).

## 3. Before→after measurement for the chain's claim (C1)

| quantity | before (HEAD `015e1bab`) | after (literal + PRIMARY token, scratch) |
|---|---|---|
| knowledge files | 83 | **84** |
| mapped | 83 | **84** |
| missing / dangling | [] / [] | **[] / []** |
| citation-resolved rules | 14 / 14 | **14 / 14** |
| coverage / depth | 10.0 / 10.0 | **10.0 / 10.0** |
| README | 190 lines `a451ad16…` | **190 lines** `1cd05260…` (one line, `:38`) |
| prior-83 | — | **byte-identical 83/83** |

**The round's core measurement, re-derived by me:** Vyper 0.4.3 runtime carriers
recover their planted selector sets K/K (15/15, 22/22, 9/9, 4/4 re-verified;
7/7 via EX-09's legs) with zero missing / zero extra and `dispatch:"abi"`, under
a **third dispatcher shape** — `selector % N` indexes a uint16 jump table whose
entries are JUMPDESTs, and each bucket walks a `PUSH4 sel / DUP2 / XOR / PUSH2
next / JUMPI` chain. On this family **0 of 15** reported `bytecode_offset`
values are JUMPDESTs: each is the match **fall-through** (handler body entry),
with `byte[offset-12]` being the compare-site JUMPDEST that carries that
function's own selector — measured 15/15 by me, 0/7 on Ex09Vault, and
independently by PL-1 (0/15, 0/9, 0/22). The r1/r3 "offsets land on JUMPDESTs"
reading is therefore **solc-scoped**, and the entry says so.

## 4. Attacks / refutations attempted, with verdicts

1. **Oracle-independence** (no planted file trusted; own keccak oracle):
   PASS — 15/15, 22/22, 9/9, 4/4 set-equal, zero missing/extra.
2. **Offset-semantics** (the inherited reading could be false for Vyper):
   CONFIRMED the entry's line — 0/15 JUMPDEST, fall-through rule holds 15/15;
   `byte[offset-12]==0x5b` 15/15 and that site's selector == the reported one
   15/15.
3. **Third-shape claim**: PASS — prologue/table/sentinel/XOR-chain all reproduce
   byte-for-byte; my independent `% 13` census finds 4 colliding buckets (5 extra
   selectors), consistent with the draft's "4 collisions".
4. **Zero-false-positive**: PASS — the two non-selector PUSH4 constants were
   never reported; `89402a72` occurs in neither CarrierV nor StewardToken bytes,
   confirming the `__default__()` phantom.
5. **Mutability/argument delta**: PASS — 7 agree / 8 payable-reads on CarrierV
   (5 view + 2 nonpayable + 1 pure), 5/2 on Ex09Vault; `address` params read
   `uint256`. Direction uniform, no misassignment.
6. **Cited-id resolution**: PASS — 19/19.
7. **Trap class**: PASS — raw-over-hextext 0 functions with decoded sha == the
   hex text's own sha; creation legs uniformly parsed-and-empty.
8. **Id-domain wording** (F4-adjacent): the `var-*` legs the entry lists first
   are **cwd/TMPDIR variants at ONE path** (all share `ev_45849c8b…`) — they are
   the same-path control, not path-sensitivity evidence. The claim still holds
   on EX-10's `b2-altpath-copy`/`ino-*` and EX-07's D-series. Verdict: claim
   HOLDS; wording advisory (A1).
9. **Prior-entries recheck**: PASS — both re-derive exactly, so the new entry
   invalidates neither.
10. **Ledger pin spot-check**: the ledger's `f9ae3dbc…` for
    `EX-02/custody-stat-readonly.txt` is stale (now `67b1014e…`, re-written
    11:09:50); the **entry** cites that file without a hash, so the entry is
    clean. Advisory A2 for the parent.
11. **SC-1 provenance** (does "own five probe runs" overstate?): the staged
    envelopes are byte-identical to RV-2/VZ-1/EX-06 legs, BUT SC-1's scratch
    `/var/tmp/sc1-r4/` holds its own runs at 11:06:25–11:07:05 (earlier than my
    11:06:46 staging) and my fresh re-run reproduced the same sha256 — so the
    identity is tool determinism, not copying, and SC-1's "run first-hand"
    statement is **true**. Verdict: statement true; the *entry's* "own" wording
    reads as independent corroboration and should be scoped (F3).

## 5. Blockers

Required fixes (listed here since the seat format has five sections; full detail
in `quality-grade.md` §2):

- **F1** — `SC-1/evidence/c1-inventory.txt` does not exist; the file is
  `SC-1/c1-inventory.txt`.
- **F2** — the EX-09 brace expansion
  `probe/vy-{runtime,creation}-{hex,raw,0xhex}-{6.4.0,6.7.0}.json` over-claims
  two names; the `0xhex` legs exist at **6.4.0 only**.
- **F3** — scope "this entry's scribe's own five probe envelopes": they are
  verbatim-deterministic copies of RV-2/VZ-1/EX-06 legs on the same paths.
- **F4 (QUALITY row 15)** — the id-domain observation states path-sensitivity
  but cites no corpus file; add `corpus/QUALITY.md:24-25` + the r3-entry pointer.
- **A1** — reorder the id-domain sentence so the true path-sensitivity legs lead.
- **A2** — re-derive the ledger's stale `custody-stat-readonly.txt` pin.

None of the above blocks the landing; none changes a measured result.

None for this seat's deliverable. Two notes for the parent: (i) the graded
revision is the one at mtime 14:10Z — any further revision of the draft voids
this grade's identity pins (method unchanged, numbers re-derivable); (ii) the
rehearsal is tree-form; the parent must re-measure command A at the records
commit from real Git objects (an unrun check has not passed).

Identity (rule #14): this report's own byte-identity and the identity of
`quality-grade.md` are recorded in `claims/c1/RV-2/report.identity.txt`, derived
after the final revision of each file; nothing here claims a hash of itself that
predates that derivation.
