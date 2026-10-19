# RV-3 regrade — drafted c1 knowledge entry at rev 4 (arc3-loop1-round3, late join)

**Why this file exists.** My 13:17Z grade (`quality-grade.md`) pinned rev 2.2
(21,704 B / `5c1818c7…`, literal 17,563 B / `189ac2a2…`) and declared that a
further revision voids it. The scribe revised again at 13:17:51Z; this is the
regrade of the current revision. Method unchanged (pre-registered in
`prereg-verification-plan.md`); every number below is re-derived first-hand.

**Graded artifact:** `.ufo/waves/arc3-loop1-round3/claims/c1/records-drafts/knowledge-entry-draft.md`
22,628 B / sha256 `d9004f4880931455b2c46db32be96e38380c7baddb656a5dd2fae6af3b1a4632`,
mtime 2026-10-19 13:17:51Z.
**Graded text:** the literal block between the BEGIN/END markers, extracted
first-hand — **17,708 B / 37 lines / sha256 `3b5f371e85bdb8054e3a6b04c4b2097179b6a5435476a8f470e0d6c0a45c2215`**
(scratch copy `/dev/shm/rv3r3/literal-r3b.md`; rehearsal tree
`/dev/shm/rv3r3/head3` = `git archive HEAD`).
**Mirror copy:** `SC-2/knowledge-entry-draft.md` 22,071 B / `9b0cb5b8…` carries a
**different literal** — 17,563 B / `189ac2a2…`, byte-identical to the rev-2.2
literal I graded before the interruption (EX-14 froze the same bytes as
`EX-14/inputs/entry-literal-revC.md`). Two literals are in the tree; the parent
must land exactly one (fix R4).

**Delta rev 2.2 → rev 4 (measured, `diff` of the two literals):** exactly four
changed lines — 5 (`source:` block), 13 (carrierB planted-B path), 17
(carrier-A path), 37 (`Sources:`). No measured-result text changed. These are
the c1 verdict's debt repairs #1/#6/#7 (CR-2 F3, CR-2 F4-partial, CR-1
carrier-A path).

**Verdict: ACCEPT-WITH-FIXES** for the rev-4 literal as a landing candidate.
Every hard gate re-derives PASS end-to-end; three accuracy/citation must-fixes
(R1, R2, R3) and two landing-safety must-fixes (R4, F1) remain, plus three
advisories (R5). None of the must-fixes changes a measured result.

## Hard gates (all first-hand at rev 4)

| gate | result | evidence |
|---|---|---|
| proposed stem == map token | PASS | stem `2026-10-19-arc3-r3-evm-optimizer-shapes` present in both map-token copies' PRIMARY lines; my rehearsal token set 82 → 83 |
| command A **before** | PASS | pristine HEAD archive `/dev/shm/rv3r3/head`: `{"knowledge_files":82,"mapped":82,"missing":[],"dangling":[],"citation_resolved_rules":14,"rule_blocks":14,10.0/10.0}` |
| command A **after** (rev-4 literal + additive token) | PASS | `/dev/shm/rv3r3/head3`: `{"knowledge_files":83,"mapped":83,"missing":[],"dangling":[],"citation_resolved_rules":14,"rule_blocks":14,10.0/10.0}` — `evidence/commandA-rehearsal-rev4.txt` |
| prior-82 byte-identical / SKILL untouched / README line-neutral | PASS | `diff -rq` over the 82 knowledge files: no diffs; `cmp SKILL.md`: identical; README 190 → 190 lines, exactly one line differs (`:38`); additive after-sha `a451ad16…` (reworded form would give `016b632e…`) |
| K/K recovered, zero extras | PASS | my own recheck run (byte-identical envelope `05f76b33…`, 13/13, `dispatch:"abi"` ×13) + 6 further envelope legs set-equal to their planted files, zero missing / zero extra (`evidence/kk-recheck-rev4.txt`) |
| decoded `bytecode.sha256` ≡ carrier bytes, offsets JUMPDEST | PASS | decoded `b24a0115…` ≡ `VaultB.opt200.runtime.bin`; all 13 offsets on `0x5b` (byte-index check) |
| recheck line reproduces | PASS | verbatim command re-run 13:23Z → envelope `05f76b33…` == EX-10's capture == SC-2's capture == the draft's declared value |
| citations resolve | **FAIL (fix R3)** | 4 locations fixed at rev 4; 1 expansion still non-existent (`optB-…{-rerun}` 5 missing names, lines 5 and 37) and 1 artifact-class mismatch (`offset-check-*.json` under `evidence/` resolves to the script, not the `evidence/probe/` outputs) |
| label discipline (QUALITY 5/7/11) | PASS | Observation ×13 / Inference / Unknowns / Limitations / Scope; `grep -c` count 0; no `held`/`works` verb in the literal; `/tmp` only inside the documented EDQUOT sentence which carries the disk-backed `TMPDIR` |

## corpus/QUALITY.md criteria — deltas vs my 13:17Z table

Rows 2-13 and 15 re-derive as before (PASS). Changed rows:

| # | criterion | verdict at rev 4 | note |
|---|---|---|---|
| 1 | resolvable source | **FAIL → R3** | `EX-04/planted-B.txt` → root `planted-B.txt` FIXED (467 B, `f32393c0…` re-derived); `offset-check-*.json` → `evidence/probe/…` FIXED in the source block; carrier-A path FIXED (repo-root-absolute); **still open:** `optB-{hex,raw}-{6.4.0,6.5.0,6.7.0}{,-rerun}.json` (5 of 12 names do not exist) and the `evidence/offset-check-*.json` mention on line 21 |
| 4 | absolute path + stable identity | PASS-with-fix | R2 labels still wrong (2,938/1,956 are hex-char counts; files are 2,939/1,957 B) |
| 14 | (superseded) | — | |

## Required fixes (all apply-by-content, not by line number)

**R1 (accuracy, must-fix — QUALITY 1/5).** Line 26 still reads "VaultB (**both
variants**) carries `4e487b71` (panic) plus four revert-path error constants
(`1309a563`, `1dc930eb`, `30cd7471`, `3c3332b9`)". False for nopt, and it
contradicts EX-10's own `recon-B-nopt.json` (`non_dispatch_push4_constants:
["43000825"]`). Measured again at rev 4: nopt's non-dispatch `PUSH4` set is the
trailer constant only; the error/panic data occur as `PUSH32` words
(`…40517f1309a563…`, `…5b7f4e487b71…`); `3c3332b9` does not occur in nopt at
all (0 hits / 3,163 B). Fix text: `proposed-entry-fixes-rev4.patch.md` §FIX-1.

**R2 (accuracy, must-fix — QUALITY 4).** `CarrierB` "hex carrier 2,938 B
`247e09f3…`" — the file is **2,939 B** (2,938 hex chars + trailing newline);
`Rv2TokenOpt` "hex carrier 1,956 B `a07bef2e…`" — the file is **1,957 B**. Both
quoted hashes are the files' sha256s, so the size and the identity must cohere.
(VaultB's hex carriers carry **no** trailing newline — 3,242 / 6,326 B are true
file sizes — so state the convention once.) Fix: §FIX-2.

**R3 (citations, must-fix — QUALITY 1).** (a) Lines 5 and 37:
`optB-{hex,raw}-{6.4.0,6.5.0,6.7.0}{,-rerun}.json` expands to 12 names of which
5 do not exist (only `optB-hex-6.7.0-rerun.json` does) — write the actual set
(CR-2 F2). (b) Line 21 (`evidence/offset-check-*.json`) and the source block's
`offset-check-*.json` resolve to `EX-04/evidence/offset-check.js` (the script);
the outputs are `EX-04/evidence/probe/offset-check-{opt200,noopt}.json`. Fix:
§FIX-3.

**R4 (rule #14 / landing safety, must-fix).** Three identity artifacts are
inconsistent with the tree:
- `SC-2/README-identities.txt` (mtime 13:14:59Z, before the final draft write)
  claims the draft is "21,585 B / `5c1818c7…` ≡ mirror" — actual records-drafts
  copy is 22,628 B / `d9004f48…`, the mirror is 22,071 B / `9b0cb5b8…`, and
  `5c1818c7…` no longer exists in the tree. Its literal row (17,563 B /
  `189ac2a2…`) matches the **mirror's** literal only.
- The rev-4 draft's own final identity row still says the rehearsal literal
  "hashes `189ac2a2…`" while its body now carries `3b5f371e…`.
- The two map-token copies disagree on PRIMARY: `SC-2/map-token-patch.md` =
  **reworded** (after-README `016b632e…`), `records-drafts/map-token-patch.md`
  = **additive** (after-README `a451ad16…` = RV-4's caller-option strict
  additive form). Land exactly one, and land the literal it was rehearsed with.
Fix: §FIX-4 (protocol) — the parent must re-derive the landed file's identity at
landing regardless.

**F1 (internal contradiction, must-fix — CR-2 sustained, still present).** Line
43 ends "r1's `60003560e01c`-class and non-binary prologues remain unvisited
this round" while the round re-probed exactly those (carrier-A `60003560e01c`
3/3; Rv2TokenOpt linear `EQ` chain — my own census corroborates: each of its 5
selectors occurs once as a `PUSH4` immediate, no GT-pivot duplicates, vs
VaultB's duplicated `69fe0e2d`/`8da5cb5b`). Apply CR-2's §F1 replacement text
(§FIX-5).

**R5 (advisories).** (a) CR-1 Edit 1 — the id-comparator advice on line 33
("compare by `subject.digest.sha256`") is costume-dependent: my recheck shows
`subject.digest` = the `.hex` file's digest (`9a1fbfab…`) while the decoded
bytes are `b24a0115…`; recommend the decoded
`normalized_result.bytecode.sha256` (§FIX-6). (b) CR-1 Edit 2 — add the
"whole-file sweep" qualifier to the Rv2TokenOpt 7-immediate sentence. (c) The
bare `Rv2Token.sol` mention (line 16) should carry the r1 path
`.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/Rv2Token.sol` (two further copies
exist this round). (d) The draft header says "Revision 3" while its own revision
log ends at rev 4 — trivial, fix if convenient.

## Independent measurements performed at rev 4 (first-hand)

1. Literal extraction + `diff` vs the graded rev-2.2 literal (4 changed lines).
2. Command A before/after on a pristine HEAD archive with the additive token;
   README line/diff/sha checks; prior-82 `diff -rq`; `cmp SKILL.md`.
3. Verbatim re-run of the entry's recheck line (disk-backed TMPDIR) —
   byte-identical envelope; decoded-digest and JUMPDEST offset checks.
4. Keccak re-derivation (js-sha3, receipted prefix) over 4 landed ABIs; envelope
   vs planted set equality on 7 legs total.
5. Opcode-aware PUSH4 census on the three carrier variants (rev-4 bytes).
6. All 37 quoted `ev_…` ids resolved against the landed artifacts; VZ-1 matrix
   id spot-check.
7. Existence re-derivation of every file-shaped citation in the literal
   (brace-expansion + stated-base resolution).

## Scope

This seat graded a **draft**; nothing was applied to the lane repo by RV-3
(writes: this seat's dir + `seats/RV-3.md` only). The two literals in the tree
are the parent's landing choice; my rehearsal covers the rev-4 one, and the
rev-2.2 one was rehearsed at the pre-interruption grade.
