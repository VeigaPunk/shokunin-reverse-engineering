# ScoutSurfaces — round-77 surface map: five routed defects → two instruments → record cells

seat: ScoutSurfaces (read-only recon). No production file was edited; every write is under
`.ufo/waves/round-77/w1/ScoutSurfaces/` plus this report.

Revisions: base `188562d4`, declaration `819cf30e`, freeze `6767a879`
(the instrument bytes I ran are the 6767a879 blobs: sha256 `45280392…` for
`tools/round-77/verdict-bind.py`, `174eedb5…` for `tools/round-77/prefile-receipt.py`, copies in
the evidence dir). While this seat ran, the lane advanced to HEAD `509c1051` (commit
`round-77: the wave-1 spec …`); the HEAD column below is that revision, measured at
2026-11-04T07:55:44-03:00 and not re-measured after.

Machine-readable receipt: `ScoutSurfaces/receipt.json` (mentions, blind_spots, scope_arithmetic).

## 0. What was run (exact files, exit codes)

| command | rev | exit | observed |
|---|---|---|---|
| `verdict-bind.py --root <lane> --rev <rev>` | 6767a879 | 1 | `mismatch_count 4`, `bound_clauses 21`, `in_scope_rows 9`, `capability_rows 39`, `validate.defects []` |
| same | 188562d4 | 1 | `mismatch_count 4`, `bound_clauses 21`, `in_scope_rows 9` |
| same | 509c1051 (HEAD) | 0 | `mismatch_count 0`, `bound_clauses 25`, `in_scope_rows 11`, `validate.defects []` |
| `verdict-bind.py --selftest` | — | 0 | `cases 15`, `failures []` |
| `prefile-receipt.py --battery --work <scratch>` | 6767a879 | 1 | `arms_ok 4` / `6` |
| same | 188562d4 | 1 | `arms_ok 4` / `6` |
| same | 509c1051 (HEAD) | 1 | `arms_ok 5` / `6` (A2 `record-receipt` false) |
| `prefile-receipt.py --selftest` | — | 0 | `cases 13`, `failures []` |

Receipts copied into the evidence dir: `c1-at-freeze.json`, `c1-at-base.json`, `c1-at-head.json`,
`c2-at-freeze.json`, `c2-at-base.json`, `c2-at-head.json`, `c2-nolang.json`, `fake-receipt.json`,
`selftest-verdict-bind.txt`, `selftest-prefile.txt`.

## 1. The five routed defects on the two instruments

| # | routed defect (lesson §6) | instrument surface that now touches it | cell / observation at freeze 6767a879 | at HEAD 509c1051 |
|---|---|---|---|---|
| 1 | landing receipt cited as green in three files while red | C1 `bind_cell` over the `## Capabilities` row and the PROVINCE `- **Core — ` bullet; the round-claim row is outside the parsed surface | 4 `value_mismatch` defects: `D24 true` → `false` and `mismatch_count 0` → `1`, twice each (row `capability-row binding`, label `PROVINCE.md line 585`), receipt `.ufo/waves/round-76/l1/scores/c1-at-landing.json` | third site (`SCORECARD.md:5907`) was outside C1's scope and needed the manual correction it now has; C1 exits 0 |
| 2 | tip-receipt revision prose is loose | **no instrument binds it.** C1 reads the receipt bytes named by a cell but never compares the receipt's own `rev` to `--rev`, and `rev <hex>` parses to no clause; C2 `--filing` records `rev = git rev-parse HEAD` while the gate measures the working tree | `parse_clause("rev 1ab1e164")` → `None`; `grep expect_rev` in verdict-bind.py → no receipt-rev check | cells now name `c1-at-tip.json` with the rev in prose; the value binds, the revision claim does not |
| 3 | gate-at-tip "exit 0" is not in its receipt | C2 arm A3 `gate-exits` | `round-76: 5 gate receipts, missing [gate-at-freeze.txt, gate-at-record.txt, gate-at-tip.txt, gate-disclosures.txt, gate-selftest-at-tip.json — all "no exit"]` | `round-77: 2 gate receipts, missing []` → arm true |
| 4 | prefile check retains no receipt | C2 arms A1 (clone run) and A2 (filing receipt at `.ufo/waves/round-77/l1/scores/prefile-at-filing.json`) | A2: `… absent at 6767a879` | A2: absent at HEAD (the receipt is **untracked**) **and it records `exit 1`, `passed false`, `prefile: FAIL`** |
| 5 | D24 admits a false verdict beside a resolving path | C1's whole predicate; selftest case `red-false-annotation` | the same 4 defects above are that class, re-derived | defect class absent from the record; C1 has 15 selftest cases, one red per failure shape |

## 2. Every mention of the false landing annotation (53 spelling hits, 8 files, freeze 6767a879)

Files searched: `SCORECARD.md`, `PROVINCE.md`, `LOG.md`, `SKILL.md`, `corpus/README.md`,
`corpus/lessons/round-76-verifier-spotcheck.md`, `corpus/lessons/round-76.md`,
`corpus/knowledge/2026-11-04-r76-capability-row-binding.md`.
`in_scope` is C1's frozen surface: a `## Capabilities` row whose 4th-cell first numeral is >= 73, or a
`PROVINCE.md` line inside a `- **Core — ` bullet. Hits double where both spellings sit on one line.

| path:line | spelling | in_scope | kind | action |
|---|---|---|---|---|
| SCORECARD.md:636 | `c1-at-landing` | false | other-round-receipt-in-capabilities-row | none |
| SCORECARD.md:638 | `c1-at-landing` | false | other-round-receipt-in-capabilities-row | none |
| SCORECARD.md:641 | `c1-at-landing` | false | other-round-receipt-in-capabilities-row | none |
| SCORECARD.md:642 | `c1-at-landing` | false | other-round-receipt-in-capabilities-row | none |
| SCORECARD.md:643 | `c1-at-landing` | false | other-round-receipt-in-capabilities-row | none |
| SCORECARD.md:646 | `c1-at-landing` | false | other-round-receipt-in-capabilities-row | none |
| SCORECARD.md:649 | `c1-at-landing` | true | other-round-receipt | none |
| SCORECARD.md:656 | `c1-at-landing` | true | false-landing-verdict | instrument-binds |
| SCORECARD.md:656 | `D24 true, mismatch_count 0` | true | false-landing-verdict | instrument-binds |
| SCORECARD.md:5224 | `c1-at-landing` | false | other-round-receipt | none |
| SCORECARD.md:5296 | `c1-at-landing` | false | other-round-receipt | none |
| SCORECARD.md:5397 | `c1-at-landing` | false | other-round-receipt | none |
| SCORECARD.md:5530 | `c1-at-landing` | false | other-round-receipt | none |
| SCORECARD.md:5578 | `c1-at-landing` | false | other-round-receipt | none |
| SCORECARD.md:5598 | `c1-at-landing` | false | other-round-receipt | none |
| SCORECARD.md:5677 | `c1-at-landing` | false | other-round-receipt | none |
| SCORECARD.md:5759 | `c1-at-landing` | false | other-round-receipt | none |
| SCORECARD.md:5810 | `c1-at-landing` | false | other-round-receipt | none |
| SCORECARD.md:5863 | `c1-at-landing` | false | other-round-receipt | none |
| SCORECARD.md:5907 | `c1-at-landing` | false | false-landing-verdict | append-correction |
| SCORECARD.md:5907 | `0 mismatches, nine atoms` | false | false-landing-verdict | append-correction |
| PROVINCE.md:520 | `c1-at-landing` | false | other-round-receipt-in-table-row | none |
| PROVINCE.md:529 | `c1-at-landing` | false | other-round-receipt-in-table-row | none |
| PROVINCE.md:530 | `c1-at-landing` | false | other-round-receipt-in-table-row | none |
| PROVINCE.md:541 | `c1-at-landing` | false | other-round-receipt-in-table-row | none |
| PROVINCE.md:550 | `c1-at-landing` | false | other-round-receipt-in-table-row | none |
| PROVINCE.md:589 | `c1-at-landing` | true | false-landing-verdict | instrument-binds |
| PROVINCE.md:589 | `D24 true, mismatch_count 0` | true | false-landing-verdict | instrument-binds |
| LOG.md:4112 | `c1-at-landing` | false | other-round-receipt | none |
| LOG.md:4134 | `c1-at-landing` | false | other-round-receipt | none |
| LOG.md:4146 | `c1-at-landing` | false | other-round-receipt | none |
| LOG.md:4168 | `c1-at-landing` | false | other-round-receipt | none |
| LOG.md:4226 | `c1-at-landing` | false | other-round-receipt | none |
| LOG.md:4272 | `c1-at-landing` | false | other-round-receipt | none |
| LOG.md:4329 | `c1-at-landing` | false | other-round-receipt | none |
| LOG.md:4384 | `c1-at-landing` | false | other-round-receipt | none |
| LOG.md:4432 | `c1-at-landing` | false | other-round-receipt | none |
| LOG.md:4486 | `c1-at-landing` | false | other-round-receipt | none |
| SKILL.md:1868 | `c1-at-landing` | false | other-round-receipt | none |
| SKILL.md:1869 | `c1-at-landing` | false | other-round-receipt | none |
| SKILL.md:1871 | `c1-at-landing` | false | other-round-receipt | none |
| SKILL.md:1873 | `c1-at-landing` | false | other-round-receipt | none |
| SKILL.md:1874 | `c1-at-landing` | false | other-round-receipt | none |
| corpus/lessons/round-76-verifier-spotcheck.md:6 | `c1-at-landing` | false | defect-description | none |
| corpus/lessons/round-76-verifier-spotcheck.md:64 | `c1-at-landing` | false | defect-description | none |
| corpus/lessons/round-76-verifier-spotcheck.md:64 | `D24 true, mismatch_count 0` | false | defect-description | none |
| corpus/lessons/round-76-verifier-spotcheck.md:64 | `0 mismatches, nine atoms` | false | defect-description | none |
| corpus/lessons/round-76-verifier-spotcheck.md:99 | `c1-at-landing` | false | defect-description | none |
| corpus/lessons/round-76-verifier-spotcheck.md:99 | `D24 true, mismatch_count 0` | false | defect-description | none |
| corpus/lessons/round-76-verifier-spotcheck.md:99 | `0 mismatches, nine atoms` | false | defect-description | none |
| corpus/lessons/round-76-verifier-spotcheck.md:103 | `D24 true, mismatch_count 0` | false | defect-description | none |
| corpus/lessons/round-76.md:80 | `c1-at-landing` | false | disposition-row | none |
| corpus/knowledge/2026-11-04-r76-capability-row-binding.md:1 | `c1-at-landing` | false | pointer-only | none |

Summary: 53 hits, 5 in scope, 3 false-verdict cells (`SCORECARD.md:656`, `PROVINCE.md:589`,
`SCORECARD.md:5907`), of which **2 are inside C1's scope** (4 defects) and **1 is outside**
(`SCORECARD.md:5907` — a round-claim row, never parsed; it needed the record correction the L1
has now appended). Every other hit names a different round's own `c1-at-landing.json` (rounds
67–75), or is the lesson's description of the defect, or is a pointer without a verdict.
`corpus/README.md` has zero hits.

At HEAD `509c1051` the same search returns 54 hits with **0 live false verdicts**: `:656` and
`:589` now point at `c1-at-tip.json` (whose `rev 1ab1e164`, `mismatch_count 0`, `D24 true`, nine
atoms are true), `:5909` cites `c1-at-tip.json` and states the landing value as 1 by construction,
`:591` repeats that sentence, and `:5977` quotes the old annotation only inside the correction note.
Line numbers after 5224 shift by +2.

## 3. C1 scope arithmetic, counted independently

From `git show 6767a879:SCORECARD.md`, parsing the `## Capabilities` table the way the instrument
does (data rows, 4th cell's first numeral):

- capability data rows: **39**
- rows whose first-working round numeral is >= 73: **9**
  (73 kernel-side witness; 73 record-vs-receipt; 73 reader-seam; 74 kernel-witness mutation;
  74 record-audit v2; 75 A12 case-independence; 75 exact-grammar; 76 capability-row binding;
  76 executable printed counting command)
- bound clauses at `--rev 6767a879`: **21** (18 groups; 3 clauses unbound; 4 defects)

So **9 in-scope rows / 21 bound clauses reproduce exactly** (`reproduced: true`).

The frozen predicate's landing floors are `bound_clauses >= 18` (already met) and
`in_scope_rows >= 11` (**not met at freeze**: 9). The two rows that lift 9 to 11 are the round-77
rows that landed later (`evidence-cell verdict binding`, `prefile gate receipt`, both first-working
round 77); at HEAD the count is 41 rows / 11 in scope / 25 bound / 0 defects, exit 0. C1's landing
therefore requires those two rows (and the receipts they cite at
`.ufo/waves/round-77/pre/selftest-c1.json`, `selftest-c2.json`, both present since the declaration
commit `819cf30e`), not only the three annotation corrections.

## 4. Blind spots (command and its output tail)

### 4.1 `tools/round-77/verdict-bind.py`

1. **Scope.** Only `## Capabilities` rows with first-working round >= 73 and PROVINCE
   `- **Core — ` bullets are read. Round-claim rows and `LOG.md` are not.
   `git show 6767a879:SCORECARD.md | grep -n '0 mismatches, nine atoms'` → `5907:…| improved |`;
   `jq -r '.defects[].label' c1-at-freeze.json | sort | uniq -c` →
   `2 ## Capabilities row 'capability-row binding' (first-working round 76)` /
   `2 PROVINCE.md line 585`. The 5907 row (and LOG) never appear.
2. **Syntax.** Only parenthesised groups of 2–220 chars without nested parens are parsed. The
   false verdict at 5907 sits outside the only group on its line:
   `re.findall(r'\(([^()]{2,220})\)', <line 5907>)` → `['capability-row binding']`.
   A verdict written as prose therefore makes no claim.
3. **Field surface.** A claim naming a field the receipt does not carry is `unbound`, never a
   defect. `jq -r '.cells[]|.label as $l|.clauses[]|select(.status=="unbound")|"\($l) :: \(.clause) :: \(.reason)"'`
   → `…'kernel-side environment witness…' :: forged_detected true :: unknown_field`,
   `…'A12 case-independence closure' :: sole true :: unknown_field`,
   `…PROVINCE.md line 585 :: mismatch 1 :: unknown_field`. A false `forged_detected true` would pass.
4. **Revision.** The receipt's own `rev` field is never compared to `--rev`; a hex revision claim
   does not parse. `grep -n 'expect_rev\|receipt.get("rev")' verdict-bind.py` → no match;
   `parse_clause('rev 1ab1e164')` → `None`. A receipt measured at another revision is accepted, so
   routed defect 2's class (loose receipt-revision prose) is **not** closed by C1.

### 4.2 `tools/round-77/prefile-receipt.py`

1. **A2 does not bind `--rev`.** `check_receipt` is called without `expect_rev` for the record
   receipt, so any revision's receipt is accepted if it passes. The live receipt is worse than
   stale: `jq '{rev,exit,passed,prefile_line}' .ufo/waves/round-77/l1/scores/prefile-at-filing.json`
   → `rev 440ee041…, exit 1, passed false, prefile: FAIL`; at HEAD the file is untracked, so A2
   says `absent`. Its stdout names the cause: `prefile: tree NOT CLEAN (7 paths)` (the wave's
   untracked evidence), then `prefile: FAIL`.
2. **A3 sees only the newest round dir.** `jq -r '.arms[]|select(.arm=="gate-exits")|.observed'`
   at base → `round-76: 5 gate receipts, missing [gate-at-freeze.txt, gate-at-record.txt,
   gate-at-tip.txt, gate-disclosures.txt, gate-selftest-at-tip.json — "no exit"]`; at freeze →
   `round-77: 0 gate receipts, missing []`. The round-76 debt is invisible as soon as round-77 exists.
3. **A4–A6 measure the lane HEAD, not `--rev`.** In the base run the red-rev arm reports
   `rev '000…' is not the expected '6767a879…'` while the receipt says `rev 188562d4…`: the red
   arms ran `run_gate(root, …)`, whose receipt rev is `git rev-parse HEAD`. The battery's `rev`
   describes A1–A3 only.
4. **`--check-receipt` has no producer binding.** A fabricated receipt with a self-consistent
   digest, `argv` naming `/nowhere/tools/round-29/prefile-check.sh`, and a nonexistent lane passes:
   `--check-receipt fake-receipt.json` → `{"defects": []}`, exit 0. Nothing hashes the gate script,
   checks the path exists, or pins an instrument.
5. **The four-key claim depends on the caller's LANG.** `env -u LANG -u LC_ALL … --battery` →
   `arms_ok 3`, and the clone-run receipt shows `env_keys ['HOME','PATH','TMPDIR']` —
   `"is not the four-key allowlist"`. `child_env` sets `LANG` from the parent and drops empty
   values; on a host without `LANG` the instrument cannot pass its own A1.

## 5. Findings and risks

- **F1 — the C2 claim understates A3's debt.** The frozen sentence says base `arms_ok 4 of 6`
  with "three round-76 gate receipts without exit"; A3 actually names **five** (three `.txt` from
  the report, plus `gate-disclosures.txt` and `gate-selftest-at-tip.json`). `arms_ok 4` is correct.
- **F2 — freeze arithmetic vs landing floor.** 9 in-scope rows at freeze cannot satisfy
  `in_scope_rows >= 11`; only the two round-77 capability rows lift it. At HEAD both are in and
  C1 exits 0 with 25 bound clauses, 11 rows, defect-free `validate`.
- **F3 — C1 leaves the revision surface open** (blind spot 4.1.4). `c1-at-tip.json`'s values bind,
  but nothing verifies the receipt was measured where its `rev` says.
- **F4 — C2's record arm is revision-blind and the filing receipt is red.** Committing the current
  `.ufo/waves/round-77/l1/scores/prefile-at-filing.json` keeps A2 false at every rev
  (`exit 1`); C2's 6/6 target needs a PASS receipt. `--filing` runs the gate on the lane working
  tree, which the wave's own untracked artifacts make dirty; a clean `--shared` clone at the
  landing rev (the gate path only has to end with `tools/round-29/prefile-check.sh`) is the
  available route.
- **F5 — `--filing`'s `rev` is not the measured bytes** (blind spot 4.2.3): it records
  `rev-parse HEAD` while the gate reads the working tree.
- **F6 — A3's newest-round rule** hides historical receipt debt (blind spot 4.2.2).
- **F7 — C1's unbound field class** lets a false claim whose field the receipt omits pass
  (blind spot 4.1.3); the non-parenthesised surface is exactly why `SCORECARD.md:5907` escaped.
- **F8 — C2 is LANG-dependent** (blind spot 4.2.5): `arms_ok 3` under `env -u LANG`.
- **F9 — the fabricated-receipt pass** (blind spot 4.2.4) is by design ("receipt bytes alone"),
  but it means `--filing` receipts are not provenance-bound; the claim counts each arm as an
  observation, not as authenticity.

Risk to the landing: HEAD moved during this seat and may move again; all HEAD numbers are pinned
to `509c1051`. The two round-77 capability rows cite `.ufo/waves/round-77/pre/selftest-{c1,c2}.json`
— if either is absent at the landing rev, C1 turns red with `absent_receipt`. If the current FAIL
filing receipt is committed as is, C2 tops out at 5/6.

## 6. Remaining unknowns

- Whether C2's filing receipt will be taken from a clean clone or after the wave artifacts are
  committed — both satisfy `argv`, but only the clone path records the landing rev.
- Whether the C1 landing intends the receipt-rev gap (F3) as out of scope; the frozen predicate
  does not name it, and the instrument cannot see it.
