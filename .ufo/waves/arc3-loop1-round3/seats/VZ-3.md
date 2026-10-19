# VZ-3 — seat report (chain c3, role convergence, LATE JOIN)

Wave `arc3-loop1-round3` · seat VZ-3 · 2026-10-19 · repo
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin` · HEAD (committed revision)
`c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311` (no git mutations by this seat).
Seat line: reconcile the c3 chain into `claims/c3/verdict.md`; poll the seats
dir; name gaps; seat report last.

**Status: COMPLETED the missing work (the chain reconciliation — `claims/c3/verdict.md`
had not landed; this seat wrote it) and INDEPENDENTLY VERIFIED every leg of the
chain's frozen claim first-hand.** The real-path writes (the gate pair, the
custody tool/README) were read-only for this seat: hash/stat/`git show` only.
Scratch under `/var/tmp/vz3` (`/tmp` never used); the clobber-attack demo ran in
a scratch clone under `/var/tmp/vz3/clone` only.

## 1. Work performed (evidence pointers)

Writes (this seat's only writes): `claims/c3/verdict.md` and
`claims/c3/VZ-3/vz3-reconciliation.txt`, plus this report.

- **Reconciliation (the missing work):** `claims/c3/verdict.md` — the chain
  verdict, written to the round-2 `claims/c3/verdict.md` precedent: claim
  components table (10 rows), before→after, per-seat cross-walk (11 seats),
  named residuals R1-R8, attacks A1-A9, closing procedure.
- **Raw captures:** `claims/c3/VZ-3/vz3-reconciliation.txt` (16 sections:
  identities, pin, object diff, probe both modes, selftest, frozen run, tamper
  guard, command A, census instrument, my own rule-#11 audit, my own arc3
  citation census, teeth drill, LOG gap, EX-42 set-equality, live incident,
  graded-path dirtiness sweep). Identity re-derived after the last append:
  sha256 `e8e5356a09d022660ca79f61d102515bb68e0492fa1ffbaef69cffeeaad1410a`,
  9,749 B.
- **Polled the seats dir** (13:22:53Z, 13:24:04Z, 13:26:08Z): 50 reports of 64
  roster names; c3 is complete except **EX-42** (its artifacts landed 10:16-10:17Z
  but its seat report never did — the wave's interruption) and VZ-3 itself
  (this file). Repo-wide missing at my last poll: CN-1, CN-2, EX-09, EX-14,
  EX-30, EX-42, RV-1, RV-3, RV-5, SC-3, SC-4, VZ-1, VZ-2, VZ-4 (VZ-1's c1
  verdict had landed as `claims/c1/verdict.md`).

## 2. Proposed changes

**None.** No patch text; no real-target edit. The landed gate pair needs no
repair on any leg this seat measured. The residuals that *would* need a change
(R1's one entry, R2's one clause, R6's advisory fragility set) are recorded in
the verdict's closing procedure as parent decisions, with the F3 re-pin duty
attached.

## 3. Before → after measurement for the chain's claim

All numbers re-derived by this seat on the settled worktree bytes (final pass
13:26Z), `TMPDIR=/var/tmp/vz3`:

| quantity | before (`c07af80`) | after (landed pair, worktree) |
|---|---|---|
| entries / quoted / exempt (mechanical count) | 31 / 4 / 3 | **57 / 4 / 8** (+26; object diff 26 added / 0 removed / 0 modified / 0 dup ids) |
| table bytes / sha256 | 14,694 / `738b3a56…` | 30,348 / `bfc42f1bb131cbe3a972a16647d24b1f16d936083dd61496589540e791d58bb7` |
| expected.json pin | `738b3a56…` | **`bfc42f1b…` == table digest (MATCH)**; parsed diff vs HEAD = the pin value only; 2,154 B, no trailing newline |
| probe at HEAD (default / strict) | reported 0 / clean 0 | `reported findings=0 exit=0` / `clean findings=0 exit=0` |
| selftest | 13/13 | 13/13 (`CLEAN cases=13 passed=13 failed=0 exit=0`) |
| frozen run at `679af5d…` (strict) | re-derives | `failed findings=32 exit=1`, 17 × `citation_dead` ⊇ `["citation_dead"]` |
| tamper guard (scratch copy, +1 byte) | exit 2 | `pointer_table_tampered`, `could-not-evaluate exit=2` |
| command A (recipe unmodified) | 82/82, 14/14, 10.0/10.0 | 82/82, 14/14, 10.0/10.0 |
| c1 census instrument | PASS 0/0/0/0 | PASS 0/0/0/0 |
| arc3 doc-class stated-line rows covered | 1 / 12 | **12 / 12** (11 new + 1 pre-existing `shonen-skill-range`) |
| rule-#11 conformance of the 26 new entries | — | **26/26 CONFORM** (own re-implementation of the probe's grader) |
| non-vacuity (3 entries neutered on a scratch pair) | — | exactly 3 `citation_dead`, exit 1 |

**Acceptance test (the census, not the count):** my own independent net over the
added lines of the four arc3 r1/r2 commits × the six durable surfaces yields
**12 stated-line rows, all 12 covered, 0 uncovered-and-not-exempt**; EX-42's
kind-A+D set (13 rows) is set-equal on those 12 plus one kind-D row
(`SKILL.md:253` → the r1 SCORECARD section key) my line-number net cannot
enumerate, which is covered by `sc-arc3r1-section-key`. The single gap is
`LOG.md:1442` (verdict §4 R1).

## 4. Attacks/refutations attempted (verdicts)

1. **My own conformance sweep flagged 8 new entries as broken** → REFUTED as my
   harness's bug (I graded `extracted` needles against the citing file and
   dropped `re.M` on the range blob). Re-implemented the probe's `check_entry`
   semantics → 0 flags. Recorded because a mis-run check has not passed.
2. **Vacuity of the new needles** → REFUTED: 3-entry neuter on a scratch
   table+expected fires exactly 3 `citation_dead`, exit 1.
3. **Silent extension / stale pin** → REFUTED: one byte appended to a scratch
   table → `pointer_table_tampered` exit 2.
4. **Frozen-run record stale** → REFUTED: re-derived strict at `679af5d`, exit 1,
   17 `citation_dead`.
5. **The extension clobbers existing entries** → REFUTED: 26/0/0/0 object diff,
   `quoted` equal, `exempt` prefix equal.
6. **The census acceptance is unverifiable narrative** → REFUTED: own net built
   independently (hunk line numbers + own token regex); 12/12 covered.
7. **Anchor substring semantics** → CONFIRMED as a property (extend ≠ red,
   delete = red) — the probe's semantics, not an entry defect.
8. **CR-5's blocker "EX-42 delivered nothing"** → REFUTED (superseded): EX-42's
   artifacts landed 10:16-10:17Z; I re-derived `entries-proposal.json`
   (`8a9583ce…`), reproduced its §5.4 gap and corroborated its §5.3 finding.
9. **"Every pinnable citation is covered or adjudicated"** → PARTIALLY REFUTED:
   `LOG.md:1442` is pinnable, uncovered, and unreached by any exemption's
   wording (verdict R1).
10. **Live incident (new, high-severity, detected by chance in `git status`):**
    a graded wave receipt
    (`.ufo/waves/arc3-loop1-round1/claims/cross/receipts/config-pre-pair.txt`,
    graded by `custody-readme-v1-stanza-example`) was transiently clobbered by
    another seat's report dump at 13:25:02Z. Measured exposure on a scratch
    clone with those bytes committed: `citation_dead`, `failed findings=1 exit=1`
    — the probe at `--rev HEAD` is immune because it resolves from Git objects,
    so the risk is the commit. By 13:25:55Z the file was restored byte-identical
    to HEAD (`b8ed1936…` both sides, status clean) and the probe reads clean 0.
    Recorded as verdict R8 with the reproduction and the sweep (§16: the only
    other dirty graded path is the custody README, whose 4 anchors plus the 3
    `skill-registry-*` anchors and `readme38-arc3r1-token` are all LIVE on the
    worktree bytes).

## 5. Blockers

- **None for this seat's deliverable** — the verdict and this report are landed.
- **Gap named for the parent (not a blocker):** `seats/EX-42.md` never landed,
  so EX-42's own artifact identities (which its `census.md` §6 defers to that
  report) have no home; I re-derived them in
  `claims/c3/VZ-3/vz3-reconciliation.txt` and cited the key values
  (`entries-proposal.json` `8a9583ce…`; `census.md` `6a0da39b…`;
  `enumeration.tsv` `7174d2a8…`; `battery-EX42.txt` `7560ad1e…`;
  `battery-landed.txt` `2dc17571…`; `landed-table-acceptance.txt` `de32f75a…`;
  `enumerator.py` `3f73e052…`; `resolver.py` `cf17641e…`; `resolve.txt`
  `2ff4f4d1…`). If the parent wants a report at that path, this paragraph is the
  substance it needs.
- **Residual for the parent's landing** (verdict §6): close R1 (one `quoted`
  entry for `LOG.md:1442`, or an exemption whose wording reaches it) with the F3
  re-pin in the same commit; land the pair together; re-run the probe after the
  worktree settles and at the records commit (R8); append SCORECARD after
  `:1419` and LOG after `:1412`; re-derive every identity this file quotes.
- **Rule #14 caveat:** the identities above bind the worktree bytes measured at
  13:22-13:26Z, HEAD `c07af80`. The gate pair's mtimes were 10:12:37Z / 10:13:28Z
  at my last check (unchanged by this seat); any later revision invalidates the
  digest claims and they must be re-derived.
