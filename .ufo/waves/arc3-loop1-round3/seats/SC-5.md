# SC-5 — seat report (chain c3, role scribe)

Wave `arc3-loop1-round3` · seat SC-5 · 2026-10-19. Task: records drafts for the
parent (not applied) — the LOG entry draft and the SCORECARD round-section
draft for C3, **pin-free**; artifacts under
`.ufo/waves/arc3-loop1-round3/claims/c3/records-drafts/` (two files).
Compliance: no git mutations; no LOG/SCORECARD/SHONEN/corpus/SKILL/README
writes; custody paths read-only (hash/stat capture only); scratch under
`/var/tmp/sc5` (never `/tmp`); every write is under this wave's seat/claim
directories.

## 1. Work performed (evidence pointers)

Grounding reads: `claims-frozen.md`; the round-2 scribe precedent
(`.ufo/waves/arc3-loop1-round2/claims/c3/records-drafts/{log-entry-draft.md,
scorecard-section-draft.md}`); `.ufo/gates/c1-census-v10.py` (SCOPE `:215-236`,
locus regexes `:239-243`); `.ufo/gates/citation-drift/{pointer-table.json,
expected.json, citation-drift-probe.py}`; the round-1 EVM entry
(`corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md`); `SCORECARD.md`;
`SKILL.md:378-393`; `.ufo/gates/custody-pair/README.md`.

**Wave-start baseline, measured at HEAD `c07af80` (≈13:05–13:10Z):** census
v10-r9 (instrument sha `d0772ce8…`, bracketed identical before/after) →
`VERDICT: PASS (0/0/0/0)` rc 0; probe default `reported findings=0 exit=0`,
`--strict` `clean findings=0 exit=0`, selftest `cases=13 passed=13` rc 0;
pointer table 31 entries (+4 quoted, 3 exempt), 14,694 B, sha `738b3a56…`;
`expected.json` sha `ff47bfd6…` pinning that digest; probe sha `e2665074…`;
EX-46's `pin-check.py` → `VERDICT MATCH`; command A (SCORECARD recipe,
`REV=c07af80`) → 82/82, 14/14, 10.0/10.0. All of it corroborated
byte-for-byte by EX-44's `claims/c3/EX-44/before-{probe,selftest}.txt` and
EX-46's `claims/c3/EX-46/baseline/sha256-baseline.txt`.

**Artifacts written (this seat's only writes):**

- `.ufo/waves/arc3-loop1-round3/claims/c3/records-drafts/log-entry-draft.md`
  (156 lines; literal entry text 92 lines; file sha256 `12899b4e…222580`,
  literal-text sha256 `c32b990e…4ccab0b5` — re-derived after the last edit).
- `.ufo/waves/arc3-loop1-round3/claims/c3/records-drafts/scorecard-section-draft.md`
  (193 lines; literal section text 77 lines; file sha256 `498efb91…356f2033`,
  literal-text sha256 `4ce06e90…368825978` — re-derived after the last edit,
  including the §3 revision history).
- `.ufo/waves/arc3-loop1-round3/seats/SC-5.md` (this report; identities above
  re-derived at its write time, rule #14).

**Post-landing re-measurement at the work tree (13:13–13:16Z), after EX-41's
designated real-target write:** table 31 → **57 entries** (+26; 0 removed;
14,694 → 30,348 B) sha `bfc42f1b…`; `expected.json` (2,154 B) sha `d97dd60a…`
with `pointer_table.sha256 = bfc42f1b…` (its only top-level key change is
`pointer_table`; frozen-run revision/verdict/findings, snapshot digest and the
13-case selftest table byte-unchanged); frozen-run baseline re-derived at its
pinned revision → `failed findings=32 exit=1` with the expected
`citation_dead` present (EX-41 `06-frozen-run.txt`); probe `0/0` both modes;
selftest 13/13; `pin-check.py` MATCH; census PASS 0/0/0/0; command A unchanged
82/82, 14/14. Corroborated by EX-41's `04-after-probe-and-selftest.txt`,
`07-nonvacuity.txt` (all cases `OK` rc 1), `08-tamper-checks.txt` (byte-changed
table / absent table / unpinned baseline / dead revision → each
could-not-evaluate exit 2) and RV-12's independent re-verification
(`seats/RV-12.md`).

**Pin-free simulation (scorecard draft §3; `/var/tmp/sc5`):** copies of the
three census-scoped files at HEAD + the literal section appended to the scratch
`SCORECARD.md`; instrument sha bracketed `d0772ce8…`. Rev-1/2 section (67
lines, sha `d0bea0ca…`): base PASS 9 loci (`c8d97713…`) → records PASS 9 loci
(`93681ff1…`) → control FAIL undeclared=1 (`7dd51357…`). Rev-3 section (77
lines, sha `4ce06e90…`, the evidence-filled text): records PASS 9 loci
(SCORECARD 1573 lines; `5e7c2c43…`) → control FAIL undeclared=1 (1574 lines;
`cde79294…`). Both revisions: needle-regex scan PIN/VER/PTR/CACHE/REA_GATE each
0 hits.

**Arc3-citation seed survey** (scribe-level, cross-checked): r1-entry citations
into the r3-07 entry (`:149-155`, `:59-70`, `:44-45`, `:93-96`) and QUALITY
rows (`:21`, `:24-25`); map token `corpus/README.md:38`; registry rows
`SKILL.md:389-390`; custody conventions and the round-1 receipts; SCORECARD
arc3 sections pin-free by design. EX-43's census landed the authoritative
version and EX-41's dispositions landed the final mapping (24 new entries + 2
pre-existing covers; 6 NO-ENTRY rows/groups materialised as `exempt` 3 → 8;
one measured-stale round-record citation — `SKILL.md:371` now `## Refuses`).

**Poll cadence:** 60s re-listing (log `/var/tmp/sc5/poll.log`); the table
change (EX-41's landing) was detected at check 3 at 13:12:47Z; verifier seats
re-checked at 13:16Z (RV-12 report landed; RV-11 partial; CR-5/VZ-3 absent).

## 2. Proposed changes

- The two draft files above **are** the proposed change (append texts for
  `LOG.md` EOF and `SCORECARD.md` EOF); the parent applies them at the records
  commit after filling the remaining `⟨FILL⟩`/`⟨PARENT-FILL⟩` slots.
- No patch-text files proposed by this seat. "none" for direct edits: LOG.md,
  SCORECARD.md and every other lane file are untouched by SC-5 (the work-tree
  modifications shown by `git status` are other seats': EX-41's table pair,
  C2's custody tool/README, plus the pre-existing dirty
  `.ufo/waves/arc2-loop1-round10/C3.md`).

## 3. Before→after measurement for the chain's claim

C3's claim: probe table covers the arc3-era pinnable citations; digest re-pinned
in the expected file in the same commit; findings 0 at HEAD in both modes;
selftest 13/13 unchanged; command A unchanged; acceptance = the census with
adjudications.

| check | before (HEAD `c07af80`) | after (work tree, EX-41 landed) |
|---|---|---|
| entries / quoted / exempt | 31 / 4 / 3 | **57 / 4 / 8** (+26, none removed) |
| table bytes / sha256 | 14,694 / `738b3a56…` | 30,348 / `bfc42f1b…` |
| expected-file pin / sha256 | `738b3a56…` / `ff47bfd6…` | `bfc42f1b…` MATCH / `d97dd60a…` |
| frozen-run baseline | pin `679af5d…`, failed, [citation_dead] | re-derived: `failed findings=32 exit=1`, citation_dead present |
| probe at HEAD (default / strict) | reported 0 / clean 0 | reported 0 / clean 0 |
| selftest | 13/13 rc 0 | 13/13 rc 0 |
| census (instrument `d0772ce8…`) | PASS 0/0/0/0 | PASS 0/0/0/0 |
| command A | 82/82, 14/14, 10.0/10.0 | 82/82, 14/14, 10.0/10.0 |
| digest re-derivation (`pin-check.py`) | MATCH | MATCH |
| preflight classes (4 injections) | declared exit-2 classes | declared exit-2 classes (re-verified) |
| scribe-side: records-append loci | n/a | **0 new loci** (9 → 9), no new needle hits |

Gaps named: the verifier-confirmation slot (RV-11/RV-12/CR-5/VZ-3) is filled
only by what had landed at write time; the C1/C2 cross-chain fragments stay
`⟨PARENT-FILL⟩` for the other chains' scribes.

## 4. Attacks/refutations attempted, with verdicts

1. **Planted-pin attack on the draft's pin-free claim** — a planted
   client-token + version-literal line appended with the section flips the
   census to `UNDECLARED (1)` → FAIL rc 1 (both revisions). Verdict: draft text
   clean; the "0 new loci" claim is non-vacuous.
2. **Regex-vacuity attack** — direct scan of the section bytes for all five
   instrument needles: 0 hits each. Verdict: pin-free at the token level.
3. **Identity attack across revisions** — §3/notes edits left the section text
   byte-identical (sha re-derived `4ce06e90…` after each edit); the
   evidence-filled revision was re-simulated on fresh trees. Verdict: no
   carried identity.
4. **Stale-digest incident (caught, corrected)** — `expected.json` was
   rewritten by EX-41 at 13:13:28Z after my first post-landing measurement; the
   draft's first number (`179db3c7…`) went stale. Re-derivation caught it
   (`d97dd60a…`); the draft now records the fresh value and the correction.
   Verdict: a live rule-#14 exercise — the class is real and the fix is in the
   artifact.
5. **Drift-injection pair (EX-43's)** — at a real drift revision the 31-entry
   table reads clean (blind) while the extension catches 2 `citation_dead`.
   Verdict: recorded; the extension adds teeth.
6. **Non-vacuity battery (EX-41's)** — needle + pointer mutation per new entry:
   every case `OK`, rc 1, `citation_dead`. Verdict: recorded.
7. **Neutered needle (EX-44's)** — reports `citation_dead` rc 0; never repairs.
   Verdict: recorded.
8. **Stale-pin / one-byte tamper (EX-46's)** — both `pointer_table_tampered`
   exit 2. Verdict: recorded; the F3 coupling is enforced by preflight.
9. **Rename-fragility battery (RV-12's)** — 34 of 57 entries fire on an honest
   rename with all citing lines updated (14 of them new); advisory patch text
   `claims/c3/RV-12/fragility-mitigations.patch.md`. Verdict: recorded as a
   verifier residual for the parent's carried-debt line; not absorbed, not
   contested.
10. **Self-refutation of an over-claim** — the drafts refuse an "every arc3
    citation covered" count; acceptance is the census with adjudications, per
    the frozen claim.

## 5. Blockers

- Verifier set incomplete at write time (RV-12's seat report landed; RV-11's
  runs partial — one of its checkers crashed mid-run, a seat-level defect;
  CR-5/VZ-3 artifacts absent). The drafts keep the verifier slot; if those
  seats have not landed by the records commit, the parent lands the slot as a
  named gap rather than asserting their verdicts.
- Post-report poll addendum (≈13:18Z): CR-5's critic tree has begun landing
  (`claims/c3/CR-5/` — its own census, mutation battery, a negative-control
  dead-pin receipt, and a non-vacuity battery whose receipt shows one new
  anchor entry, `custody-readme-v2-fieldset`, reading `DEAD` under its phrase
  replacement while the other new anchors `FIRES`). That is a critic finding
  the parent must splice into the verifier slot / carried-debt line if it
  survives CR-5's own report — not absorbed or contested by this seat (no CR-5
  seat report had landed when this addendum was written; RV-11.md, RV-12.md,
  EX-41.md, EX-43.md, EX-44.md, EX-46.md seat reports have landed).
- The records drafts are **not applied** (by task): pending the parent's
  assembly with the C1/C2 records drafts and the verifier confirmations.
- Standing environment hazard: host `/tmp` quota exhaustion — all scratch
  disk-backed; the C1 side's probe work still requires a disk-backed TMPDIR.