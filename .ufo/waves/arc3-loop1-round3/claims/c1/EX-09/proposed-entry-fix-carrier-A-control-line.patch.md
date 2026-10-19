# Proposed entry-text fix — carrier-A control offset line (EX-09, arc3-loop1-round3, chain c1)

**NOT APPLIED.** No corpus file was touched by this seat. Apply by **content match**,
not by line number (the draft is under active revision; CR-2 §preamble records the same
constraint).

**Target:** `.ufo/waves/arc3-loop1-round3/claims/c1/records-drafts/knowledge-entry-draft.md`
(SC-2 scribe draft). The identical sentence appears in three other places and must be
fixed in each or the round will land the same false statement:

- `.ufo/waves/arc3-loop1-round3/claims/c1/SC-2/knowledge-entry-draft.md:46`
- `.ufo/waves/arc3-loop1-round3/claims/c1/EX-14/inputs/entry-literal-rev2.md:30`
- `.ufo/waves/arc3-loop1-round3/claims/c1/EX-14/inputs/entry-literal-rev4.md:31`
- `.ufo/waves/arc3-loop1-round3/claims/c1/EX-14/inputs/entry-literal-revC.md:31`

(the EX-14 literals are the packaged landing text; the `base-to-projected-rev*.patch`
files carry the same line.)

## F-EX09-1 (sustained — factually false statement)

**Before:**

```
- **Observation (carrier-A control, cross-pin):** 3/3 planted selectors, zero extras, `dispatch:"abi"`, offsets 38/48/58 JUMPDEST, at 6.4.0/6.5.0/6.7.0 × hex/raw; hex ≡ raw payload and decoded-bytecode sha `a92ba152…` per pin (`EX-07/legA-compare.txt`).
```

**Problem.** "offsets 38/48/58 JUMPDEST" is **false**. In the 84-byte control
(decoded sha256 `a92ba15225aaddccff5c0c67fff18c6c13b86be3bc91c07527681fbf500f6f7b`)
the bytes at offsets 38/48/58 are `0x80`/`0x00`/`0x00`; the JUMPDESTs sit at
**40/50/60**. The dispatch nodes declare `PUSH1 0x26`/`0x30`/`0x3a` (= 38/48/58), which
land 2 bytes *before* each JUMPDEST, inside the `PUSH1 00; DUP1; REVERT` guard — the
control's own construction defect, not probe drift (r1 CR-1's record shows the same
58/48/38). The citation given (`EX-07/legA-compare.txt`) does not support the word
"JUMPDEST"; RV-2's contemporaneous measurement records the correct reading
(`seats/RV-2.md:179`; `RV-2/evidence/kk-check-set1.txt:1-5`;
`RV-2/tools/check_legs.py:58-63`).

**Evidence (EX-09, first-hand, re-derived twice):**

- Byte map: `target-carrier-A-control.hex` bytes 36–41 = `60 00 80 fd 5b 60`
  → offset 38 = `0x80`, offset 39 = `0xfd` (REVERT), offset 40 = `0x5b` (JUMPDEST).
- `recon-control.txt` (exit 1): all 49 sources MATCH on sets/offsets/pins; the landing
  check fails with `LANDING ANOMALY: 129 offset-checks hit non-0x5b bytes`
  (= 42 frozen legs × 3 functions + 3 parse dests).
- `jumpdests-control.txt`: `offset 38: byte=80 jumpdest=False next_5b=40`, and likewise
  48→50, 58→60.
- `verify-independent.py` (independent implementation): 42/42 legs confirm all three
  reported offsets are non-JUMPDEST.
- RV-2 independently: *"CR-1's hand-assembled control: reported offsets 38/48/58 are
  the declared jump immediates and its `0x5b` bytes sit at 40/50/60 (immediates 2
  short)"*.

**After (proposed text — states the measured fact and scopes the invariant):**

```
- **Observation (carrier-A control, cross-pin):** 3/3 planted selectors, zero extras, `dispatch:"abi"`, at 6.4.0/6.5.0/6.7.0 × hex/raw; hex ≡ raw payload and decoded-bytecode sha `a92ba152…` per pin (`EX-07/legA-compare.txt`). The reported offsets 38/48/58 are this control's **declared `PUSH1` jump immediates**, not JUMPDESTs — its `0x5b` bytes sit at 40/50/60 (2 bytes later), so it is the one probed carrier where the "offsets land on JUMPDEST" reading does **not** hold; the reading is scoped to solc-convention carriers (`RV-2/evidence/kk-check-set1.txt`; `EX-09/recon-A.md` §4).
```

**Also fix, same root cause (verdict row 3).** `claims/c1/verdict.md` row 3 states
*"all quoted offsets land on JUMPDEST bytes (VaultB lists checked byte-wise by this
seat)"*. The parenthetical scopes it to VaultB, but the row's blanket phrasing would
absorb the draft's false line. Proposed: append to that row —
*"except the r1 hand-assembled control, whose declared dests are 2 bytes before its
JUMPDESTs (`EX-09/recon-A.md` §4; RV-2 `kk-check-set1.txt`)."*

## Receipts

| claim | artifact (this seat, unless noted) |
|---|---|
| byte map of offsets 36–41 | `EX-09/target-carrier-A-control.hex` + re-derived byte dump (`recon-A.md` §4) |
| 129 = 42×3 + 3 | `EX-09/recon-control.txt` final line; arithmetic re-derived independently |
| JUMPDEST positions | `EX-09/jumpdests-control.txt` |
| 42/42 legs confirm non-JUMPDEST | `EX-09/verify-independent.py` output (`/var/tmp/ex09v/verify.txt`) |
| RV-2's independent measurement | `seats/RV-2.md:179`, `RV-2/evidence/kk-check-set1.txt`, `RV-2/tools/check_legs.py:58-63` |
| r1 CR-1's own record (same 58/48/38) | `.ufo/waves/arc3-loop1-round1/claims/c1/CR-1/evidence/out-A-hex.json` |
