# RV-3 proposed entry fixes — rev 4 literal (patch text, NOT applied)

Seat RV-3 · chain c1 · reviewer · 2026-10-19. Target:
`.ufo/waves/arc3-loop1-round3/claims/c1/records-drafts/knowledge-entry-draft.md`
literal block, revision `3b5f371e85bdb8054e3a6b04c4b2097179b6a5435476a8f470e0d6c0a45c2215`
(17,708 B / 37 lines, 13:17:51Z). Apply **by content match**, not by line number.
No corpus file was touched by this seat. Line numbers below are the revision I
attacked.

## FIX-1 (R1) — the "(both variants)" PUSH4 clause, line 26

**Before (verbatim fragment):**

```
VaultB (both variants) carries `4e487b71` (panic) plus four revert-path error constants (`1309a563`, `1dc930eb`, `30cd7471`, `3c3332b9`)
```

**After:**

```
VaultB opt200 carries `4e487b71` (panic) plus four revert-path error constants (`1309a563`, `1dc930eb`, `30cd7471`, `3c3332b9`); the same-source nopt variant carries only the CBOR-trailer constant `43000825` as a non-dispatch `PUSH4` — its error/panic data appear as `PUSH32` revert-data words, and `3c3332b9` does not occur in its bytes at all
```

**Receipts (first-hand):** `EX-10/recon-B-nopt.json` `non_dispatch_push4_constants: ["43000825"]`
(agrees with `EX-10/recon-B-opt200.json` for the opt200 five); my opcode-aware
sweep — nopt 16 sites / 14 unique, non-dispatch = `43000825` only (byte 3,156,
inside the terminal CBOR trailer), `3c3332b9` 0 hits over 3,163 B; opt200 24
sites / 18 unique with the five constants (`3c3332b9` at byte 1,037 as
`PUSH4 3c3332b9; PUSH1 0xe1; SHL` revert-data write).

## FIX-2 (R2) — hex-carrier size labels, lines 14 and 16

**Before (line 14):** `runtime 1,469 B `b9c70178…`, hex carrier 2,938 B `247e09f3…``
**After (line 14):** `runtime 1,469 B `b9c70178…`, hex carrier 2,939 B `247e09f3…` (2,938 hex chars + newline)`

**Before (line 16):** `runtime 978 B `ed6c8a76…`, hex carrier 1,956 B `a07bef2e…``
**After (line 16):** `runtime 978 B `ed6c8a76…`, hex carrier 1,957 B `a07bef2e…` (1,956 hex chars + newline)`

**Receipts (first-hand):** `stat -c%s` — `EX-05/out/CarrierB.runtime.hex` 2,939 B
(sha256 `247e09f3…`), `EX-07/Rv2TokenOpt.runtime.hex` 1,957 B (sha256
`a07bef2e…`). Note `EX-10/out/VaultB.{opt200,nopt}.runtime.hex` have **no**
trailing newline (3,242 / 6,326 B are true sizes) — either state the convention
once or normalize the files at landing.

## FIX-3 (R3) — citation locations

**(a) lines 5 and 37 — the `optB-…` shorthand.** Before:
`` `optB-{hex,raw}-{6.4.0,6.5.0,6.7.0}{,-rerun}.json` ``. After:
`` `optB-{hex,raw}-{6.4.0,6.5.0,6.7.0}.json`, `optB-hex-6.7.0-rerun.json` ``.
Receipt: `ls EX-07/optB*` — the 7 non-rerun names + `optB-hex-6.7.0-rerun.json`;
the other 5 `-rerun` expansions do not exist (CR-2 F2, sustained).

**(b) line 21 — offset-check outputs.** Before: `(`evidence/offset-check-*.json`)`.
After: `` (`evidence/probe/offset-check-{opt200,noopt}.json`) ``. Receipt:
`EX-04/evidence/probe/offset-check-{opt200,noopt}.json` exist;
`EX-04/evidence/offset-check.js` is the script (CR-2 F4; the source block's
`offset-check-*.json` under `evidence/` is the same class — keep it only if the
script citation is intended).

## FIX-4 (R4) — identity/landing protocol (not a text edit)

1. Land exactly **one** literal. `records-drafts/knowledge-entry-draft.md`
   carries `3b5f371e…` (17,708 B, rev 4); `SC-2/knowledge-entry-draft.md`
   carries `189ac2a2…` (17,563 B, rev 2.2 literal, also frozen as
   `EX-14/inputs/entry-literal-revC.md`). They differ in 4 lines; the rev-4 one
   contains the debt repairs.
2. Land exactly **one** map-token variant. `records-drafts/map-token-patch.md`
   PRIMARY = additive (`786efbb2…`, after-README `a451ad16…`); `SC-2/map-token-patch.md`
   PRIMARY = reworded (`25011b3e…`, after-README `016b632e…` = RV-4's primary
   patch). r1-form-safe choice = additive (RV-4 strict criterion).
3. After landing, re-derive the landed entry's sha256/size and re-pin
   `SC-2/README-identities.txt` (it currently claims 21,585 B / `5c1818c7…`,
   a revision that no longer exists; its literal row matches only the mirror).
4. The draft's own header says "Revision 3" while its log ends at rev 4 — align.

## FIX-5 (F1) — the "unvisited this round" contradiction, line 43

Apply CR-2's §F1 replacement (verbatim, from
`claims/c1/CR-2/proposed-entry-text-fixes.patch.md`):

**Before:**
> All were recovered K/K. r1's `60003560e01c`-class and non-binary prologues remain unvisited this round.

**After:**
> All were recovered K/K. The round also re-probed r1's `60003560e01c`-class control (carrier-A, `60003560e01c8063a9059cbb146026…`, 3/3, below) and the linear `EQ`-only compare tree (Rv2TokenOpt, 5 selectors, 5/5). Prologue classes other than `5f3560e01c` and `60003560e01c` remain unvisited.

My own census corroborates the linear chain: Rv2TokenOpt's 5 selectors each
occur exactly once as a `PUSH4` immediate (7 sites / 7 unique), unlike VaultB's
binary-search duplicates.

## FIX-6 (R5a) — id comparator, line 33

**Before:** `compare by `subject.digest.sha256` + payload when citing other seats' ids.`
**After:** `compare by the decoded `normalized_result.bytecode.sha256` + function payload when citing other seats' ids.`

**Receipt (first-hand):** my recheck of `VaultB.opt200.runtime.hex` —
`subject.digest.sha256 9a1fbfab…` (the `.hex` file, newline and costume
included), decoded `normalized_result.bytecode.sha256 b24a0115…` (the runtime
bytes). CR-1 Edit 1, sustained.
