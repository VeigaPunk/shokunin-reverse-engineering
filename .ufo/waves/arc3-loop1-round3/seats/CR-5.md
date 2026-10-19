# CR-5 — seat report (chain c3, critic), arc3-loop1-round3

Seat: CR-5 · chain c3 · role **critic** · 2026-10-19 · repo
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin` · HEAD
`c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311` (no seat git mutations; scratch under
`/var/tmp/cr5-r3/`, never `/tmp`).
Attacks assigned: **scope creep** (pinning what the r4 precedent forbids);
**NO-ENTRY laundering** (adjudications used to avoid conforming work); **entry
count inflation** (needles nobody needs); plus: check the census against my own
reading.
Artifacts: `claims/c3/CR-5/` (manifest `sha256s.txt`; memo `findings.md`).

## 1. Work performed (evidence pointers)

- **Independent census** (`census/census-cr5.py` → `census-cr5.txt/.json`):
  mechanical scan of the added lines of the four arc3 r1/r2 commits
  (`fbbbd45`,`14b1682`,`28aa7a9`,`c07af80`) over 10 durable-surface files →
  **15 citation-bearing added lines** (6 r1-entry citations, `SCORECARD.md:1435`,
  4 SKILL.md rule-#14 citations, `SHONEN.md:6`, 3 round-report citations).
- **Own conforming-needle set** (`attacks/cr5-candidates.json`, 16 entries; runs
  via `attacks/harness.sh` = the COMMITTED probe against a scratch table+expected,
  named rev): `receipts/candidates-at-head.txt` → **findings=0 at HEAD**.
- **Attack harnesses**: `mutation-battery.sh` (5 drift classes × 4 tables,
  `receipts/mutation-battery.txt`), `robustness-battery.sh`
  (`receipts/robustness-battery.txt`), `nonvacuity-cr5.py`
  (`receipts/nonvacuity-cr5.txt`), blind-and-catch (`receipts/blind-and-catch.txt`),
  negative control (`receipts/negative-control-dead-pin.txt`), work-commit
  emulation (`receipts/work-commit-emulation.txt`), section-key variant
  (`receipts/section-key-anchor-variant.txt`).
- **Objects measured** (re-derived at write): landed table
  `sha256 bfc42f1b…`, 30,348 B, entries/**57**, quoted 4, exempt 8, mtime
  10:12:37; `expected.json` `d97dd60a…` with `pointer_table.sha256 == bfc42f1b…`
  (equality re-checked, pin==table True); prior table at HEAD `738b3a56…` (31 entries).
- **Other seats read**: `seats/EX-41.md`, `seats/EX-43.md`,
  `claims/c3/EX-41/{02-census.txt,03-census-dispositions.md,10-cross-seat-check.txt}`,
  `claims/c3/EX-43/{before.md,census.out,candidate-entries.json}`.

## 2. Proposed changes

- `claims/c3/CR-5/proposed-section-key-anchor-form.patch.md` — **only** proposal:
  move the two added `sc-arc3r{1,2}-section-key` needles from `exact`+line-number
  to `anchor` form (their citation is a section-KEY reference; the table's own
  `skill-registry-row` precedent). Measured: head-rewrite simulation fires 13
  findings on the landed form vs 11 on the variant; both forms stay non-vacuous
  (header removal fires). Not applied — EX-41 owns that file.
- No other proposed change. No corpus/SKILL/README/LOG/SCORECARD edit.

## 3. Before → after measurement for the chain's claim (c3, freshness)

Commands re-run by this seat at the worktree; outputs verbatim in the receipts.

```
before: sha256sum pointer-table.json            → 738b3a569fb7… (31 entries, 14,694 B)
        probe --root . --rev HEAD               → reported findings=0 exit=0
now:    sha256sum pointer-table.json            → bfc42f1bb131… (57 entries, 30,348 B)
        sha256sum expected.json                 → d97dd60a…
        python3 -c "pin==sha256(table)"         → True          (F3 coupling in force)
        probe --root . --rev HEAD               → reported findings=0 exit=0
        probe --root . --rev HEAD --strict      → clean findings=0 exit=0
        probe --selftest                        → cases=13 passed=13 failed=0 exit=0
        entries 31 → 57 (+26); quoted 4 → 4; exempt 3 → 8
acceptance-test evidence (arc3 census vs blindness):
        baseline-31 at pristine HEAD (pre-round control)      → reported findings=0 exit=0
        drift rev 7722ff4d (entry:26 :93-96→:100-104)         → baseline-31 blind (findings=0),
          landed-57 catches (citation_dead) — receipts/blind-and-catch.txt
        mutation battery A/D/E (entry:26 re-point; SCORECARD:1435→SHONEN.md:7;
          SKILL:254→LOG.md:1413-1414)                         → baseline-31 blind on all three,
          landed-57 catches all three — receipts/mutation-battery.txt
        emulated work commit (worktree gates + C2's custody README/py): findings=0
        emulated records commit (work state + CN-2 merged SCORECARD+LOG drafts): findings=0
```

## 4. Attacks/refutations attempted, with verdicts

1. **Scope creep — NOT FOUND.** Zero entries name an operator-mutable path; the
   census instrument is unmodified this round (C3's only write target is its pair);
   `entries[0:31]`/`quoted`/`exempt[0:3]` are byte-equal to pre-landing; the one
   dated-record needle (`sc-arc3r2-cites-shonen`) is tolerant (legit SHONEN
   refresh 81-256/15/15 fires nothing). **Flag (form):** the two section-key
   needles pin SCORECARD line numbers (`exact`) though their citation is a key;
   +1 head line fires 13 findings, 2 attributable to them (§2 patch).
2. **NO-ENTRY laundering — NOT FOUND.** Every adjudicated token was attacked with
   a conforming-needle attempt (my 16 candidates, all green at HEAD): the
   arguably-conformable ones (round-report `corpus/README.md:38`; identity
   records) are *also* covered elsewhere (readme38 anchor; SKILL rule-#14 pins),
   and the rest are non-conforming by construction (operator paths; no stated
   number; count tokens; append-only records). The stale round-report pin
   (`SKILL.md:371`, measured `## Refuses` at HEAD) is exempted with a *measured*
   cause, matching the r4 "declared baseline/quoted class or drop with the
   adjudication named" precedent; pinning it live is refuted as an option
   (`receipts/negative-control-dead-pin.txt` → citation_dead). Also verified the
   probe never reads `exempt` (grep: no match) ⇒ exempt rows cannot mask findings.
3. **Entry count inflation — NOT FOUND.** 26/26 added needles fire under a
   constructed mutation each (one needs both occurrences of its phrase replaced —
   precision note, not dead weight); zero duplicates of existing keys; +26 vs the
   r10 precedent's +18; heaviest cluster 7 needles on the custody README+examples
   matches the r7 entry's 7-needle precedent. Weakest family by value: the three
   v1-shape example anchors (still live; justified by the README's own table).
4. **Census vs my reading — MATCHES.** 15/15 of my rows appear in EX-41's 18-row
   census with identical citing line/target; their extra 3 rows are
   `c1-census-v10.py`'s SCORECARD citations (accurate at HEAD). EX-43's
   before-state claims re-measured: SCORECARD `:1338-1417` pin-free (zero
   `path:line` by my regex); its 17+1 candidates green through my harness.
5. **Refutation attempts that held (recorded, not suppressed):** the landed
   arc3 needles are *blind* to a target shift that keeps the content inside the
   stated range (mutation B) and to a stale range end (mutation C) — the first is
   caught by an existing entry (`r7wall-recheck-quality25`), the second only by a
   stricter needle form; both are the probe's documented content-presence
   semantics, not defects.

## 5. Blockers

- **EX-42 (the assigned census seat) delivered nothing** — `claims/c3/EX-42/`
  empty at polls 10:07, 10:12, 10:15, 10:16 (~14 min). The census function was
  delivered instead by EX-41 (implementer) and EX-43 (before-state); I checked
  those against my own reading (§4.4) and name the gap here rather than treat a
  missing artifact as a pass. If EX-42 lands later, the deltas to check are: any
  row absent from EX-41's 18-row census, and any NO-ENTRY cause not materialized
  in the table's `exempt` ledger.
- Residual coupling for the parent: the table pins four sentences of
  `custody-pair/README.md`, which C2 rewrites in this same round — verified green
  now (`receipts/work-commit-emulation.txt`), re-run after C2's final revision.
  `census-cites-*` needles pin line numbers inside `c1-census-v10.py` (intended;
  a future edit to that instrument's header should expect the fires).