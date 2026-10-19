# SEAT RV-3 | CHAIN c1 | ROLE reviewer — arc3-loop1-round3 (2026-10-19), LATE JOIN

Task (seat line): grade the drafted knowledge entry against `corpus/QUALITY.md`
and the r1 entry precedent; list required fixes (or "accept").

**Status: COMPLETED the missing work** (the regrade of the post-interruption
revision + the seat report), and **VERIFIED existing work** (my pre-interruption
grade of rev 2.2, re-checked for staleness; the rev-4 fixes, re-derived).

**VERDICT: ACCEPT-WITH-FIXES** on the rev-4 literal
`3b5f371e85bdb8054e3a6b04c4b2097179b6a5435476a8f470e0d6c0a45c2215`
(17,708 B / 37 lines) as a landing candidate. All hard gates re-derive PASS
end-to-end. Three accuracy/citation must-fixes (R1, R2, R3), two landing-safety
must-fixes (R4, F1), three advisories (R5). None changes a measured result.

## 1. Work performed (evidence pointers)

Late join: the seat's dir already held a grade of the rev-2.2 draft
(`quality-grade.md`, 13:17Z, pinning 21,704 B / `5c1818c7…` / literal
`189ac2a2…`) plus its pre-registration and four evidence files. That grade's own
revision-pin clause voids it once the scribe revises again — which happened at
13:17:51Z (rev 4). So I re-derived everything against the current revision
rather than re-asserting the old grade.

- **Regrade:** `claims/c1/RV-3/quality-grade-rev4.md` (`85f2be32…`) — hard-gate
  table, QUALITY-row deltas, required fixes, measurements, scope.
- **Fix text:** `claims/c1/RV-3/proposed-entry-fixes-rev4.patch.md`
  (`1e191bd8…`) — apply-by-content strings for R1/R2/R3/R4/F1/R5a.
- **Evidence added this run:**
  - `evidence/recheck-opt200-rev4-verbatim.json` (`05f76b33…`) — my verbatim
    re-run of the entry's recheck line (disk-backed TMPDIR): 13/13,
    `dispatch:"abi"` ×13, decoded `b24a0115…`, `ev_d409bd50…`.
  - `evidence/kk-recheck-rev4.txt` — K/K re-derivation: keccak from 4 ABIs
    (js-sha3, receipted prefix) + envelope-vs-planted set equality on 7 legs,
    zero missing / zero extra; all 37 quoted `ev_` ids resolve; VZ-1 matrix ids
    present; PUSH4 census of the three carrier variants.
  - `evidence/commandA-rehearsal-rev4.txt`, `evidence/README-after-additive-rev4.md`
    — command A before/after on a pristine `git archive HEAD` tree, README
    line/diff/sha checks, prior-82 `diff -rq`, `cmp SKILL.md`.
  - `evidence/citation-defects-rev4.txt` — brace-expansion citation sweep.
  - `evidence/regrade-rev4-facts.txt` — copy stats/hashes at regrade time.
- **Read-only (not written):** `records-drafts/*`, `SC-2/*`, all EX-*/VZ-1
  artifacts, `.ufo/gates/citation-drift/*` (probe table + expected.json digest
  pair re-verified `bfc42f1b…` by hashing the landed table; no edit).

## 2. Proposed changes

Patch text: `claims/c1/RV-3/proposed-entry-fixes-rev4.patch.md` (six fixes).
Landing hazards for the parent, stated there as FIX-4: **two different literals**
in the tree (records-drafts `3b5f371e…` = rev 4 with the debt repairs;
SC-2 mirror `189ac2a2…` = the rev-2.2 literal, also frozen as
`EX-14/inputs/entry-literal-revC.md`) and **two different PRIMARY map-token
variants** (records-drafts = additive, after-README `a451ad16…`; SC-2 =
reworded, after-README `016b632e…` = RV-4's primary). Land one of each, paired;
then re-pin `SC-2/README-identities.txt`, which currently claims 21,585 B /
`5c1818c7…` — a revision that no longer exists.

## 3. Before → after measurement for the chain's claim (C1)

| quantity | before | after (rev-4 literal + additive token, pristine HEAD archive) |
|---|---|---|
| command A | 82/82, missing [], dangling [], rules 14/14, 10.0/10.0 | **83/83**, same fields (`/dev/shm/rv3r3/head3`) |
| README | 190 lines, `6ac43e83…` | 190 lines, exactly one line differs (`:38`), `a451ad16…` |
| prior-82 knowledge files | — | byte-identical (`diff -rq`: no diffs) |
| SKILL.md | — | byte-identical (`cmp`) |
| K/K (VaultB opt200, own run) | — | 13/13, zero extras, all offsets JUMPDEST, decoded `b24a0115…` |
| K/K (6 further envelope legs) | — | VaultB nopt 13/13; carrierB@EX-04 opt/noopt 11/11; CarrierB 8/8; Rv2TokenOpt 5/5 ×2 — all zero missing / zero extra |
| recheck envelope | — | `05f76b33…` ≡ EX-10 ≡ SC-2 ≡ declared |

Honest-stop branches not triggered (no refusal, no parse-empty, no
unrecorded prologue class). r1-precedent conformance re-checked: same
`source:`/`verified-at:`/`recheck:` header form, carrier block, Observation/
Inference/Unknowns/Limitations/Scope sections, RESULT-class scope, id-domain
hedge, no `held`/`works` verb in the literal.

## 4. Attacks / refutations attempted, with verdicts

| attack | verdict |
|---|---|
| "the pre-interruption grade still covers the current draft" | **SUSTAINED** — rev 4 landed 9 s after my grade; regrade performed |
| "rev 4 resolved all prior defects" | **PARTIALLY SUSTAINED** — 4 citation locations fixed (planted-B path, offset-check dir, carrier-A path, CarrierBErr source); R1 "(both variants)" and R2 size labels unchanged; one expansion still dead (5 of 12 `optB-…-rerun` names, lines 5/37) |
| "the self-identity block is current (rule #14)" | **SUSTAINED** — `README-identities.txt` pins a non-existent revision; the draft's own literal-hash row is stale; the two map-token copies disagree (R4) |
| "the after-state is asserted, not measured" | **REFUTED** — 83/83 measured on a pristine archive |
| "the planted tables ride the probe" | **REFUTED** — independent keccak from the compiled ABIs, set-equal on every leg |
| "the recheck line doesn't reproduce" | **REFUTED** — byte-identical envelope, first-hand |
| "the entry overclaims that the optimizer changed the dispatch shape" | **PARTIALLY SUSTAINED (advisory)** — CR-2 F7: the measured variable is selector recovery on smaller bytes; the round's own pairs show the shape class and selector order unchanged. Title/stem wording is the exposure; optional rename is the parent's call (it re-pairs the map token) |
| "every citation resolves" | **SUSTAINED** — see R3 |

## 5. Blockers

None. Notes: (a) the citation-drift probe is C3's instrument and the rev-4
landing adds no graded `path:line` citation; the probe's README anchors
(`:22`, `:175`, and the `readme38-arc3r1-token` anchor) survive the one-line,
line-neutral edit — the r1 token stays on `:38` and `expected.json` still pins
the landed table digest `bfc42f1b…`; (b) I did not run the probe itself (out of
this seat's scope, C3 owns it); (c) the `optB-…-rerun` expansion defect cannot
be fixed by moving files without touching another seat's artifacts — it is text
that must change, per FIX-3.
