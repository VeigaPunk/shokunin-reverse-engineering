# SCORECARD.md round-section — DRAFT (arc3-loop1-round1, C2 chain records)

Status: DRAFT by seat SC-5 (C2 chain, scribe) — **NOT APPLIED**. Parent
integrates after the wave. Every `[[FILL: …]]` must be replaced from the
wave's sealed receipts (or the sentence rewritten to the honest-stop branch)
before landing. The C1/C3 bullets and table rows are shape-only: fill from
those chains' records (SC-3's `claims/c1/records-drafts/` and SC-6/SC-7
drafts). The pasteable text is the block below the horizontal rule; the SC-5
notes at the bottom are not part of the section.

---

## arc3-loop1-round1 — coverage + operability + freshness: three claims, 2026-10-19

Round 1 of arc 3 (loop 1) — the first round after the operator halt at
arc2-loop1-round10 (`LOG.md:1385-1394`). The three finite owned proxies
remain saturated at 10.0 (`SCORECARD.md:19-25`, `:626-634`); the operability
and freshness moves are fleet-axis (unowned proxy — the standing recording
ruling, `:376-380`). [[FILL: round verdict qualifier — "Round admitted: all
three claims verify" / partial / honest-stop]]

- Wave: 64 seats frozen PRE-DISPATCH (items == roster asserted at dispatch),
  `opencode-go/deepseek-v4.1-flash` (opencode-go key 1 of 7 — round robin
  starts here); reports `.ufo/waves/arc3-loop1-round1/`; round report
  `.ufo/reports/arc3-loop1-round1/kaidoku.md`. Landed at [[FILL: commit(s)]].
- C1 coverage (owned) — [[FROM C1 CHAIN: the EVM real-bytecode leg, first
  held; real solc-compiled contract, K/K selectors, knowledge entry + map
  token, command A 81 → 82; see SC-3's draft for the fill shape]]
- C2 operability (fleet) — the citation-drift probe's frozen-run guard closes
  the R6 debt by measurement, not assertion. Before at HEAD `e845c2b`:
  selftest 11/11, probe `reported findings=0 exit 0`, and `expected.json`
  pins no table digest (`RV-7/verify-pre.log`) — a valid-JSON tampered table
  (entries emptied / `{}` / weakened `must_match`) grades **silent
  `findings=0 exit=0` in both modes** (EX-20, RV-6, SC-4, RV-8); the debt's
  gate-blocking clause is now measured: at the frozen revision `679af5d…`
  the real table yields 16 findings (`failed exit=1` strict) and an emptied
  table yields `clean findings=0 exit=0` (RV-6 attack 5; EX-19). After
  (prototype-measured on scratch; EX-16 applies the real-target patch,
  `claims/c2/PL-2/frozen-run-guard.patch.md`): `expected.json` pins
  `pointer_table.sha256` = `738b3a56…`; the preflight order (expected-load →
  pin-read → table-bytes → digest → parse) makes a tampered table
  `pointer_table_tampered`, an absent table `pointer_table_unreadable`, and
  an unpinned baseline `pointer_table_unpinned` — each exit 2 in probe and
  `--strict` modes, before any entry is graded, so tampering can never read
  as silent findings; drift reporting is unchanged (frozen-rev 16 findings
  rc 0/1). Selftest 11 → 13 (`table_tampered`, `table_absent`), the harness
  pinning each case's table digest so the 11 existing cases stay CLEAN on the
  guard-pass path; prototype verified by SC-5 (`claims/c2/SC-5/pl2-verify.log`:
  13/13 exit 0; tampered/absent/unpinned each exit 2 with the declared ids;
  byte-identical copy rc 0). Guard additivity: byte-identical outputs with
  the original pins, 10/13 AST nodes unchanged (EX-19). The `SKILL.md:371`
  registry row states the preflight semantics and 13 cases (patch text:
  PL-2 patch 3; variant EX-20 `old 6413e8dc… → new 08be1ec2…`, `patch -p1`
  rc 0, line count 371). Landing receipts: [[FILL: EX-16's landed sha256s +
  commit]]. Named consequences: custom-`--table` recipes + new expected =
  exit 2 `pointer_table_tampered` (re-pin or use the committed table — EX-19
  attack 6, RV-8 D1/D2); the pin chain terminates at `expected.json` (EX-24
  R1 registry-level pin recommendation; R2 fail-closed adopted); the 13-case
  reading is the guard-pass path on the existing `clean` fixture + 2 new
  cases (EX-24 §6).
- C3 freshness (fleet) — [[FROM C3 CHAIN: the E22 scope-table finding
  dispositioned by measurement at HEAD — census v10 verdict before → after,
  re-key/retire disposition in the census header; see SC-6/SC-7 drafts]]
- Measured at the records commit: command A [[FILL: 82/82, 13/13,
  10.0/10.0]]; probe selftest [[FILL: 13/13]] + findings=0; census v10 PASS
  [[FILL: 0/0/0/0]]; custody pre/post pairs 5/5 [[FILL: receipt times]].
- Process notes: `/tmp` quota exhaustion fleet-wide (EDQUOT; seats moved
  scratch to `/home`-side, `/var/tmp`, `~/.cache`; the r4 abort class);
  untracked `.ufo/gates/__pycache__/` appeared in-wave — keep out of the
  commit.

| Axis | Before → after | Verdict |
|---|---|---|
| coverage — C1 | [[FILL from C1: synthetic-only → real solc bytecode; knowledge 81 → 82]] | [[FILL]] |
| operability — C2 | probe frozen-run guard: no table digest pinned; valid-JSON tampered table silent rc 0 in both modes (frozen-rev 16 findings → 0 laundered) → table sha256 pinned in `expected.json`; tampered/absent/unpinned each exit 2 (declared CNE classes) before any entry is graded; selftest 11 → 13; registry row states the semantics | improved [[FILL: pending EX-16 landing re-measure]] |
| freshness — C3 | [[FILL from C3: E22 drift finding → dispositioned at HEAD; census verdict before → after]] | [[FILL]] |
| depth / calibration | 10.0 / 10 (command A at [[FILL: records commit]]) | unchanged |

Learning trends: [[FILL: expansion (C1); quality — the probe's frozen-run
baseline is now itself pinned (the "Two evidences" clause applied to the
pointer table, per RV-6's read of the Gate standard); discernment — the
round's attacks: EX-24's pin-mutability analysis (the pin cannot defend
expected.json itself; registry-level pin recommended), EX-23's false-positive
census (report-only guard shape vs CNE shape — the claim's wording requires
CNE), EX-19's additivity proof and the OLD-probe+NEW-expected pairing
constraint, RV-8's consumer sweep (SKILL.md:371 the only live consumer; the
custom-`--table` break measured)]]. Planned: [[FILL: round 2 per schedule]].
Carried debt (named): [[FILL: e.g. custom-`--table` re-pin contract; the
registry-level pin (R1) if adopted; C1/C3 debts]]. Retired: [[FILL: e.g. the
R6 frozen-run-guard debt (`SCORECARD.md:925-926`); or none]].

---

## SC-5 notes (not part of the section)

- Format follows the arc2-loop1-round1..round10 sections (`SCORECARD.md:636`,
  `:1270`): intro paragraph → wave bullet → per-claim bullets → "Measured at"
  → axis table → learning trends / planned / carried debt / retired.
- Before-values for the C2 row are SC-5-verified at HEAD
  `e845c2b524ad2e59871e004c51a1386e192a74ab`: selftest 11/11 exit 0; probe
  findings=0 exit 0 (probe + `--strict`); no table digest in `expected.json`;
  file digests probe `3067621a…`, expected `4e28ba90…`, table `738b3a56…`,
  `SKILL.md` `5c93c7c1…` — corroborated by EX-25 `logs/before-*.txt`, SC-4
  `verify-before.txt`, RV-6 `pre-state-hashes.txt`, RV-8 baseline transcripts.
- After-values are prototype-measured (PL-2's patch applied to a scratch copy
  by SC-5; probe `e2665074…`, expected `ff47bfd6…` — reproduced exactly).
  **EX-16's real-target landing was absent at draft time**; the parent must
  re-run the after matrix on the landed files, capture the landed sha256s +
  commit, and replace every [[FILL]] — do not paste prototype numbers as
  landed numbers.
- The capability row (`SCORECARD.md:918-919`) needs a one-line update if the
  parent wants it: the citation-drift probe row's evidence cell should cite
  the frozen-run guard + 13/13 selftest at the records commit. SC-4/SC-5 own
  SCORECARD patches — this draft's §table is the required content; the
  capability row edit is parent-side (patch text only from seats).
- The C2 verdict's honesty caveat: prototype-measured, not landed-measured.
  If EX-16 lands a different design (e.g. EX-21's skip-on-unpinned
  `table_sha256`), the "unpinned" clause in the row text is wrong and the
  exit-2-on-unpinned claim fails — re-measure before admitting.
- All [[FILL]] fields trace to `.ufo/waves/arc3-loop1-round1/claims-frozen.md`
  (the after-shape, :46-54) plus the wave receipts; SC-5 verified the
  before-values, the prototype behavior, and the artifact inventory in the
  LOG draft's poll notes.
