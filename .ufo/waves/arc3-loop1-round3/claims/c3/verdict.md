# C3 verdict — citation-drift probe table: arc3-era coverage extension (chain convergence, seat VZ-3)

Wave `arc3-loop1-round3` · chain c3 · 2026-10-19 · repo
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin` · HEAD (committed revision)
`c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311` (no seat commits; parent integrates).
Frozen claim: `claims-frozen.md:64-81`. Seat line: VZ-3, late join, reconcile
into this file. Evidence: `claims/c3/VZ-3/vz3-reconciliation.txt`
(sha256 `e8e5356a09d022660ca79f61d102515bb68e0492fa1ffbaef69cffeeaad1410a`,
9,749 B — sections 1-16 are the raw first-hand captures cited below;
re-derived after the last append, rule #14).

## Verdict: **VERIFIED** on every leg this seat could measure — the landed pair reproduces under my own tools, and the census acceptance test closes 12/12 on the durable-surface net — **with one named uncovered row** (`LOG.md:1442`, §4 R1) and the two structurally parent-side words ("in the same commit", "at the round's commit") left open by rule

Rationale: the frozen claim requires (a) the table to cover every arc3-introduced
pinnable in-repo citation with NO-ENTRY adjudications where it cannot conform,
(b) the table's sha256 re-pinned in `expected.json` in the same commit (the F3
coupling), (c) probe findings = 0 at HEAD in both modes, (d) selftest 13/13
unchanged, (e) command A unchanged, (f) entries 31 → N counted mechanically.
(a) holds on my own independent census net for every row but one; (b) holds as a
worktree pair (the commit itself is the parent's); (c)-(e) reproduced first-hand
on the landed bytes; (f) measured: **N = 57** (+26). No measured result
contradicts the claim; the one uncovered row is named, not absorbed.

## 1. Claim components — status and evidence

| # | Component | Status | Evidence |
|---|---|---|---|
| 1 | table covers the arc3-era pinnable citations (acceptance = the census) | **VERIFIED with one named gap** | VZ-3's own census net (4 arc3 commits × 6 durable surfaces, hunk line numbers): **12 stated-line rows, 12 covered, 0 uncovered-and-not-exempt** (`vz3-reconciliation.txt` §11); cross-walks: EX-42's 13 kind-A+D rows = my 12 + 1 kind-D row my line-number net cannot enumerate (`SKILL.md:253` → the `arc3-loop1-round1` section key, covered by `sc-arc3r1-section-key`) — set-equal on the 12, and the D row is covered too; EX-41 census 18 line-token rows, EX-43 17+1 candidates, CR-5 15 rows (incl. 3 wave-internal), RV-11 12/12 doc-class pointers covered. The gap is `LOG.md:1442` (§4 R1) |
| 2 | digest re-pin (F3 coupling) | **VERIFIED (pair in the worktree; commit is parent-side)** | table sha256 `bfc42f1bb131cbe3a972a16647d24b1f16d936083dd61496589540e791d58bb7` == `expected.json.pointer_table.sha256`, re-derived 3× by this seat (§2); `expected.json` parsed diff vs HEAD = the pin value only (`_doc`/`frozen_run`/`snapshots`/`selftest` byte-identical, 13 cases); 2,154 B, no trailing newline (the file's own convention) |
| 3 | probe findings = 0 at HEAD, both modes | **VERIFIED** | `reported findings=0 exit=0` / `clean findings=0 exit=0` (§4); independently reproduced by EX-44, EX-46, RV-11, RV-12, CR-5 |
| 4 | selftest 13/13 unchanged | **VERIFIED** | `CLEAN cases=13 passed=13 failed=0 exit=0` (§5); probe byte-identical to the pre-round revision (`e2665074…`) |
| 5 | command A unchanged | **VERIFIED** | SCORECARD.md:88-124 recipe, unmodified, at `c07af80`: `82/82, missing [], dangling [], 14/14, 10.0/10.0` (§8); c1 census instrument `PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)` (§9) |
| 6 | entries 31 → N, counted mechanically | **VERIFIED: N = 57** | 31 → 57 (+26) counted on the landed bytes; object-level additivity: **26 added / 0 removed / 0 modified / 0 duplicate ids**, `quoted` unchanged (4), `exempt` 3 → 8 prefix-equal (§3). PL-3's planned splice (N = 108) was **not** taken — the landed set is EX-41's 26 entries (§4 R4) |
| 7 | rule-#11 conformance of every new entry | **VERIFIED: 26/26 CONFORM** | VZ-3's own re-implementation of the probe's grader (exact/anchor/extracted, target-range grading, `re.M`) → every new needle live and single-hit; no operator-mutable path or `config.toml:N` token in any needle or graded file; the 8 `exempt` rows are ledger, not graded (§10). Independently: RV-11 61/61 CONFORM; CR-5 scope-creep attack NOT FOUND |
| 8 | non-vacuity of the new entries | **VERIFIED** | VZ-3 teeth drill: 3 new entries neutered on a scratch table + scratch expected → exactly 3 `citation_dead` naming those ids, exit 1 (§12). Corroborated: EX-41 40/40 controls, EX-45 26/26, CR-5 26/26 |
| 9 | frozen-run record re-derives | **VERIFIED** | at `679af5d…` strict: `failed findings=32 exit=1`, **17 × `citation_dead`** ⊇ the record's `["citation_dead"]` (§6) |
| 10 | tamper guard holds on the landed pin | **VERIFIED** | one byte appended to a scratch copy → `pointer_table_tampered`, `could-not-evaluate exit=2` (§7) |

## 2. Before → after (the discriminating numbers, VZ-3 first-hand)

| quantity | before (HEAD `c07af80`) | after (worktree, EX-41 rev) |
|---|---|---|
| entries / quoted / exempt | 31 / 4 / 3 | **57 / 4 / 8** (+26; 0 removed; 0 modified) |
| table bytes / sha256 | 14,694 / `738b3a56…` | 30,348 / `bfc42f1b…` |
| expected.json pin / sha256 | `738b3a56…` / `ff47bfd6…` | `bfc42f1b…` **MATCH** / `d97dd60a…` |
| probe default / strict | reported 0 / clean 0 | reported 0 / clean 0 |
| selftest | 13/13 | 13/13 |
| command A | 82/82, 14/14, 10.0/10.0 | 82/82, 14/14, 10.0/10.0 |
| census instrument | PASS 0/0/0/0 | PASS 0/0/0/0 |
| arc3 doc-class stated-line rows covered | **1 / 12** (only `SHONEN.md:6`, pre-existing `shonen-skill-range`) | **12 / 12** (11 new + 1 pre-existing) |

The count is not the acceptance test — the census is, and its live pointer
coverage is 12/12. The single record-side row below is the one exception.

## 3. Cross-seat reconciliation (what each c3 seat delivered, and my check on it)

| seat | artifact | VZ-3 check |
|---|---|---|
| PL-3 (plan) | `plan.md` + 51-entry delta fragment (N=108 projection) + bite suite | read; its base-move handling is honest (re-based on `bfc42f1b`); **not landed** — plan-vs-landed delta named by EX-41, quantified in R4 |
| EX-41 (implementer) | the landed pair | all identities re-derived by this seat; its census (18 rows) matches my net on every row I enumerate |
| EX-42 (census, acceptance) | `census.md`, `enumeration.tsv` (88 rows), `entries-proposal.json` (45 objects: 18 required / 20 recommended / 7 discretionary) | **its seat report never landed** (the wave's interruption); I re-derived its artifact identities and key numbers first-hand: `entries-proposal.json` sha256 `8a9583ce…` reproduced; kind A = 12 rows == my net; §5.4 gap reproduced; §5.3 finding corroborated (R2); one arithmetic nit (R3) |
| EX-43 (before-state) | 31/4/3, `738b3a56…`, 13/13, blindness proof | before-state agrees with mine and with SC-5/EX-44/EX-46 |
| EX-44 (after-state) | poll log, landed copy | agrees on all after-numbers |
| EX-45 (needle quality) | 61/61 needles live; one patch text on a *pre-existing* needle | agrees; no new-entry defect |
| EX-46 (interplay) | census/command A/pin legs | agrees on all three legs |
| SC-5 (scribe) | records drafts (pin-free) | drafts verified pin-free by SC-5's own planted-pin control |
| RV-11 (rule #11) | 61/61 CONFORM; 2 patch texts | agrees; its "review-enforced, not instrument-enforced" finding independently confirmed by the table's own no-number anchors (R2) |
| RV-12 (fragility) | rename/reform/insert ratings + patch text | agrees; advisory, not absorbed (R6) |
| CR-5 (critic) | 3 attacks NOT FOUND; 1 form patch text | its "EX-42 delivered nothing" blocker is **superseded**: EX-42's artifacts landed at 10:16-10:17Z; only its seat report is missing (this file's §3 note) |

## 4. Named residuals (measured; none voids the measured legs)

**R1 — the one uncovered census row (the claim's open arm).**
`LOG.md:1442` states `SHONEN:6 → `81-255`, 14/14 same commit` — a stated-line
citation written by arc3 r2 in a durable document. No entry grades it
(`entries` with `file == LOG.md`: none; the one entry targeting LOG.md is
`skill-rule14-log-fresh-identity`, which grades `LOG.md:1411-1412` from the
SKILL side), and no `exempt` cause's wording reaches it (the LOG class covers
line numbers *inside* LOG and path mentions *without* numbers; this is a stated
number about another file). Reproduced first-hand (§13). It is pinnable under
rule #11 — the table's own `quoted` class exists for append-only records
(`log1005-quoted-claim` is the precedent) — so the claim's "or adjudicated"
arm is not satisfied for this row. EX-42's proposed fix (one `quoted` entry,
`LOG.md:1442`, `must_match` ``SHONEN:6 → \`81-255\` ``, non-vacuity-tested
against its proposal) closes it; landing it requires the F3 re-pin in the same
commit. Live-pointer side is unaffected: `SHONEN.md:6` is graded via
`shonen-skill-range` + `sc-arc3r2-cites-shonen`.

**R2 — the exempt ledger's first clause is falsified by the table's own rows.**
The ledger's largest adjudication says "no stated number means no drift class
for this probe to grade". The `anchor` kind exists for exactly that class, and
the table carries 15 no-line anchors (5 pre-existing, 10 landed this round,
including three grading wave receipt files — counted by this seat). Corroborated independently by
RV-11 attack 2 (the probe passes a laundered `exact` row green → rule #11 is
review-enforced, not instrument-enforced) and CR-5's exempt-ledger review. The
ledger's *operative* ground (scope: wave-internal evidence provenance is not a
lane citation) is coherent and is what its second sentence says; the wording of
the first clause should be corrected when the ledger is next touched.

**R3 — EX-42 census.md arithmetic nit (report-level, not result-level).**
Its §0 says "88 raw rows over 57 distinct path tokens"; on its own
`enumeration.tsv` (88 rows) I count **61 distinct tokens verbatim, 53 distinct
path-prefixes, 49 basenames, 6 citing files**. No decomposition I tested yields
57. The acceptance result does not depend on this number (kind A = 12, all
covered, is the operative figure and it matches my net exactly); recorded so the
records do not quote it as a measured value.

**R4 — plan-vs-landed delta (PL-3 → EX-41).** PL-3's fragment projected N = 108
(51 entries over EX-41's 57); the landed set is EX-41's 26 new entries, N = 57.
EX-41 named this reconciliation gap itself. VZ-3 re-checked: 57 is the
authoritative count on the landed bytes; PL-3's fragment remains un-spliced,
which is a scope decision for the parent, not a defect in the landed pair.

**R5 — parent-side coupling at the records commit (the claim's two open words).**
(1) The pair must land **in the same commit** — a landed table with a stale pin
is `pointer_table_tampered` exit 2 (measured, §7). (2) The table pins C2-owned
wording: four `custody-readme-*` anchors plus the two SKILL registry-row
anchors; C2's revision was green as of 13:16Z (RV-11 attack 5, CR-5's
work-commit emulation), and the probe must be re-run after C2's final revision.
(3) The records commit must append SCORECARD sections **after `:1419`** and LOG
after `:1412` (the new section-key/LOG pins; RV-11's residual, CR-5's head-line
simulation measured 13 findings for a +1 insert above). (4) command A at the
work commit is the parent's integration measurement (expected delta: C1's
corpus landing 82 → 83 only).

**R6 — fragility ratings (advisory).** RV-12: 34/57 entries fire on an honest
rename with citations updated, 25 on anchor-form reform; the three
`census-cites-*` entries pin `.ufo/gates/c1-census-v10.py`, a version-named
instrument path (v9 → v10 precedent). Patch texts exist
(`RV-12/fragility-mitigations.patch.md`, `RV-11/proposed-craft-section-line-pins.patch.md`,
`RV-11/proposed-exempt-ledger-enforcement-note.patch.md`,
`EX-45/proposed-tighten-sc1217.patch.md`, `CR-5/proposed-section-key-anchor-form.patch.md`);
none applied this round; all require the F3 re-pin if taken.

**R7 — probe-semantics caveat (EX-42 L3a, re-confirmed).** Anchor needles are
substring searches: extending a cited token does not redden an anchor, only
deleting it does (measured on three landed anchors). A caveat of the probe, not
of this round's entries.

**R8 — LIVE INCIDENT: a graded wave receipt was transiently clobbered (detected,
measured, resolved).** At ~13:25:02Z another seat wrote its after-state suite
output **over** `.ufo/waves/arc3-loop1-round1/claims/cross/receipts/config-pre-pair.txt`
(305 lines, 304 insertions/51 deletions vs HEAD; the needle `custody receipt
\(CU-1\)` — graded by the landed entry `custody-readme-v1-stanza-example` —
occurrences 0, was 1). The probe at `--rev HEAD` did **not** fire, because it
resolves targets from **Git objects**, not the worktree (`Tree.lines` →
`git_show`); the exposure is the **commit**: on a scratch clone with the
clobbered bytes committed, the probe reads
`citation_dead entry=custody-readme-v1-stanza-example`, `failed findings=1 exit=1`
(measured; §15). By 13:25:55Z the file was restored byte-identical to HEAD
(sha256 `b8ed1936…` both sides, `git status` clean) and the probe reads clean 0.
Two lessons for the parent: (a) re-run the probe **after** the worktree is
settled and re-run it **at the records commit** — a wave-tree clobber can turn
the claim's findings=0 clause red without touching the gate pair; (b) graded
wave receipt paths are write-targets of *other* seats' report dumps, so they
need the same pre-commit check as the custody README. Full sweep (§16): the only
dirty graded paths at 13:25Z were this receipt (since restored) and
`.ufo/gates/custody-pair/README.md` (C2's revision; all four `custody-readme-*`
needles re-measured LIVE on the worktree bytes, as are all three
`skill-registry-*` anchors and `readme38-arc3r1-token`).

## 5. Attacks/refutations attempted by this seat (with verdicts)

| # | attack | verdict |
|---|---|---|
| A1 | "the new entries are broken" — my first conformance sweep flagged 8 | **REFUTED as my own harness bug** (I graded `extracted` needles against the citing file, and dropped `re.M` on the range blob). Fixed by re-implementing the probe's `check_entry` semantics; re-run: **0 flags**. Recorded because a mis-run check has not passed |
| A2 | vacuity of the new needles | **REFUTED** — 3-entry neuter on a scratch pair → exactly 3 `citation_dead`, exit 1 (§12) |
| A3 | silent extension (stale pin survives) | **REFUTED** — one byte appended to a scratch table → `pointer_table_tampered`, exit 2 (§7) |
| A4 | frozen-run record is stale/unreproducible | **REFUTED** — re-derived at `679af5d`, strict, exit 1, 17 `citation_dead` ⊇ `["citation_dead"]` (§6) |
| A5 | the extension silently clobbers existing entries | **REFUTED** — 26/0/0/0 object diff, `quoted` equal, `exempt` prefix equal (§3) |
| A6 | the census acceptance is an unverifiable narrative | **REFUTED** — my own net, built independently (hunk line numbers, own token regex), finds 12 rows and covers 12/12 (§11) |
| A7 | anchor substring semantics | **CONFIRMED as a property** (extend ≠ red, delete = red), matching EX-42's L3a; recorded as R7 |
| A8 | CR-5's blocker "EX-42 delivered nothing" | **REFUTED (superseded)** — EX-42's artifacts landed 10:16-10:17Z; only its seat report is missing. I re-derived its identities and reproduced its §5.3/§5.4 findings first-hand |
| A9 | the claim's "every pinnable citation covered" is satisfiable as stated | **PARTIALLY REFUTED** — `LOG.md:1442` is pinnable, uncovered, and not reached by any exemption's wording → R1. Reported, not absorbed |

## 6. Closing procedure (what the parent must do to make the claim fully true)

1. **Close R1 (one line):** append the `quoted` entry `LOG.md:1442` /
   `must_match` ``SHONEN:6 → \`81-255\` `` (EX-42 §5.4 text) to `entries` — or
   adjudicate it in the `exempt` ledger with wording that reaches a stated
   number about another file. Either way, **re-pin `expected.json`'s
   `pointer_table.sha256` in the same commit** and re-run the probe (both modes,
   expect 0) + selftest (13/13).
2. **Land the two gate files together** — the coupling is enforced by preflight
   (exit 2 on a stale pin), so a split landing cannot silently pass.
3. **Re-run the probe after C2's final custody README/SKILL revision** and after
   any records append; append SCORECARD sections after `:1419` and LOG after
   `:1412` (or re-pin in the same commit if the needles must move).
4. **Re-derive the table digest and every identity this file quotes** at the
   work commit (rule #14) — this verdict binds the worktree bytes measured at
   13:22-13:26Z, HEAD `c07af80`.
5. Quote R3's arithmetic nit with the correct numbers if the census is cited in
   the records.

## Verdict basis note (evidence discipline)

Every row above cites a landed file plus a command result or digest measured by
this seat against the landed bytes; no seat report was treated as evidence
without a first-hand re-derivation. The reconciliation capture
(`claims/c3/VZ-3/vz3-reconciliation.txt`, sections 1-13) holds the raw outputs.
This seat wrote no real target: the gate pair, the custody paths, LOG.md,
SCORECARD.md, SHONEN.md, corpus/, SKILL.md and every README were read-only
(hash/stat/`git show` only); all mutation ran on scratch copies under
`/var/tmp/vz3` (`/tmp` never used); no git mutations.
