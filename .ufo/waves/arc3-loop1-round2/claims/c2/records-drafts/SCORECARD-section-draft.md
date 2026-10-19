# SCORECARD.md round-section — DRAFT (arc3-loop1-round2, C2 chain records)

Status: DRAFT by seat SC-3 (chain c2, scribe) — **NOT APPLIED**. Parent
integrates after the wave. Every `[[FILL: …]]` must be replaced from the wave's
sealed receipts (or the sentence rewritten to the honest-stop branch) before
landing. The C1/C3 bullets and table rows are shape-only: fill from those
chains' records drafts. **Pin-free discipline applied** (same rule and reason as
the LOG draft): no bare version pins, no pin form, no absolute `path:line` — the
records-commit census runs after this text is appended. Pasteable text is the
block below the horizontal rule; the SC-3 notes at the bottom are not part of
the section.

---

## arc3-loop1-round2 — depth + freshness + operability: three claims, 2026-10-19

Round 2 of arc 3 (loop 1) — second round of the new stagnation window (2/10)
after round 1 admitted all three claims. The three finite owned proxies remain
saturated at 10.0 (three-way tie; the owned claim is selected by the standing
most-falsifiable-next-claim tie-break); the freshness and operability moves are
fleet-axis. [[FILL: round verdict qualifier — "Round admitted: all three claims
verify" / partial / honest-stop]]

- Wave: 64 seats frozen PRE-DISPATCH (items == roster asserted at dispatch),
  `opencode-go` key 2 of 7 (rotation advanced after round 1); reports
  `.ufo/waves/arc3-loop1-round2/`; round report
  `.ufo/reports/arc3-loop1-round2/kaidoku.md`. Landed at [[FILL: commit(s)]].
- C1 depth (owned) — [[FROM C1 CHAIN: queue-drain rules 13 → 14 — the
  self-identity re-derivation discipline; rule text in the SKILL.md craft
  section with stanza-key + receipt citations; command A 14/14
  citation-resolved at the work commit; prior 13 rules byte-identical; see the
  c1 records drafts for the fill shape]].
- C2 freshness (fleet) — the census fail-closures close the round-1 c3
  verdict's named latent holes H1 and H3 by measurement. Before at HEAD
  `14b1682` (instrument sha256 `6f1d19ff…`, round-1 landed revision): the
  census reads PASS (0/0/0/0) at HEAD, yet a scratch root without SKILL.md
  reads silent PASS, exit 0, with `SKILL.md lines=0 loci=0` — both SKILL.md
  rows are CURRENT, so no marker assertion fires (H1); and a needle-neutered
  copy reads all-zero loci with `G2 positive-assertion guard: ok` → PASS exit 0
  — G2's second disjunct is true exactly when the run finds nothing (H3). The
  existing CNE side covers only files carrying DATED rows (SCORECARD.md absent
  → FAIL, marker-uncheckable). After (landed file sha256 `d0772ce8…`, 610
  lines, worktree-modified — the file moved during the wave, still moving at
  SC-3's close (see the LOG draft); parent commits at records; SC-3 re-ran the
  matrix independently on the measured revision): an absent / EACCES /
  zero-byte / truncated /
  is-a-directory scoped file becomes a declared FAIL class — `UNREADABLE
  (could-not-evaluate)` + `DECLARED FAIL CLASSES: ['UNREADABLE']`, `VERDICT:
  FAIL`, exit 1; a zero-locus run becomes a declared FAIL — `G2 … SUSPECT
  (per file 0/0/0, total loci=0, floor=1/file)` + `DECLARED FAIL CLASSES:
  ['BLIND-INSTRUMENT']`, exit 1; a full-length scoped file stripped of its
  needles is likewise caught (SC-3's null-SKILL attack — the global-floor
  variant alone swallowed it, so EX-14's per-file variant B was adopted on
  measurement). Every round-1 silent-PASS injection re-run on the landed
  instrument returns its declared class (receipts
  `claims/c2/EX-16/receipts/{before,after}/`, plus SC-3's independent re-run
  `evidence/after-*.out`). The ordinary HEAD run stays PASS 0/0/0/0, exit 0,
  counts unchanged (PROVINCE 162/6, SCORECARD 1417/9, SKILL 371/2),
  `DECLARED FAIL CLASSES: []`, `G2 ok (per file PROVINCE.md=17,
  SCORECARD.md=14, SKILL.md=3; total loci=17; floor=1/file)`. Scope bounds
  otherwise byte-stable — the external diff audit on the v11 diff reports 0
  flags: the independent AST creep audit (RV-6's tool, run by SC-3) shows 20
  rows unchanged and key set + canonical row digest identical
  (`evidence/rv6-creep-audit-sc3.out`); EX-16's own scope-diff: ADDED(0)
  REMOVED(0) CHANGED(0) (`claims/c2/EX-16/receipts/after/scope-diff.txt`).
  Named residual: H4 self-certification stays open (the census cannot certify
  its own scope; the external audit is the certificate); per-needle partial
  blindness (the pin needle neutered alone) still reads PASS with loci found
  by the remaining needles — a token floor is not a coverage floor; H2/H5 stay
  carried debt — not this claim.
- C3 operability (fleet) — [[FROM C3 CHAIN: `.ufo/gates/custody-pair/` lands
  as a committed tool; v2 receipt per path adds mtime epoch (UTC-rendered,
  correctly labelled), inode and ctime to the sha256; the label defect is gone;
  a live same-content rewrite is detected by inode/ctime movement; v1 receipts
  stay verifiable against the tool's sha256 fields; the round's own live
  pre/post pair is captured (exit 0, 5/5); see the c3 records drafts for the
  fill shape]].
- Measured at the records commit: command A [[FILL: 82/82, missing [],
  dangling [], 13/13 rules, 10.0/10.0]]; probe selftest [[FILL: 13/13]] +
  findings=0; census [[FILL: PASS 0/0/0/0]]; custody pre/post pairs 5/5
  [[FILL: receipt times]].
- Process notes: `/tmp` (tmpfs + usrquota) standing rule — scratch under
  `/var/tmp` or `/dev/shm`; the wave's `df` shows free space on `/tmp` while
  the per-user quota is the binding constraint (standing r1/r4 record).
  Untracked `.ufo/gates/__pycache__/` present at wave start — keep out of the
  commit.

| Axis | Before → after | Verdict |
|---|---|---|
| depth — C1 | [[FILL from C1: queue-drain rules 13 → 14; citation form tightened to stanza key + receipt; command A 14/14, prior 13 byte-identical]] | [[FILL]] |
| freshness — C2 | census fail-closures: absent scoped file reads silent PASS `lines=0 loci=0` (both its rows CURRENT, no marker assertion fires; EACCES / zero-byte / truncated / is-a-directory the same) → declared `UNREADABLE` FAIL, exit 1; zero-locus run with `G2 … ok` → declared `BLIND-INSTRUMENT` FAIL, exit 1; ordinary HEAD run unchanged PASS 0/0/0/0, counts unchanged, floor declared (current-ok 5 / total 17 / floor 1); bounds otherwise byte-stable, external diff audits 0 flags; residuals named (H4, partial-needle blinding, per-file emptying) | improved (measured on the landed file; parent confirms) |
| operability — C3 | [[FILL from C3: label defect + same-content-rewrite blindness → corrected v2 receipt with epoch/inode/ctime, live 5/5 pair]] | [[FILL]] |
| coverage / calibration | 10.0 / 10 (command A at [[FILL: records commit]]) | unchanged |

Learning trends: [[FILL: expansion (C1); quality — the census's own fail-open
classes are closed by measurement, on the instrument that certifies the other
claims (self-immunity is not claimed: H4 named); discernment — the round's
attacks: [list after the wave's verdicts, e.g. whether any seat found a way to
pass the guards vacuously]]]. Planned: [[FILL: round 3 per schedule]].
Carried debt (named): [[FILL — candidates: H4 self-certification
(external-audit certificate), H2 inline-marker excusal, H5 gate-free version
statement, the r1 custom-table re-pin contract, plus C1/C3 items]]. Retired:
[[FILL — candidate: the r1 H1/H3 latent holes, if the landed guards confirm;
else "none"]].

---

## SC-3 notes (not part of the section)

- Format follows the arc3-loop1-round1 section and the arc2 sections: intro
  paragraph → wave bullet → per-claim bullets → "Measured at" → axis table →
  learning trends / planned / carried debt / retired.
- The C2 bullet's before-values are SC-3-measured at HEAD `14b1682…` on
  scratch copies of the real instrument (real file read-only, sha256
  `6f1d19ff…`): HEAD run PASS 0/0/0/0 exit 0 (`evidence/before-head-baseline.out`);
  H1a absent-SKILL.md silent PASS (`evidence/before-h1-skill-absent.out`); H1b
  absent-SCORECARD.md FAIL (`evidence/before-h1-score-absent.out`); H3
  all-neutered PASS (`evidence/before-h3-blind.out`). Shared instruments: probe
  selftest 13/13 + findings=0 (`evidence/probe-selftest.out`,
  `evidence/probe-head.out`); command A `82/82, 13/13, 10.0/10.0`
  (`evidence/commandA-head.json`).
- After-values are measured on the landed revision `d0772ce8…` (610 lines; the
  file was still moving at SC-3's close) and cited in the C2 bullet; receipts
  in `evidence/after-*`, `evidence/rv6-creep-audit-sc3.out`. The gate file
  moved `82fb807e` → `c95a5cf3` → `df9ffdf9` → `a4c16763` → `d0772ce8` during
  the wave; the final revisions re-keyed the G20 unit text (current-ok
  detections per readable file; per-row and per-block floors refuted, EX-23 §6
  / CR-2 / CR-3). **If the parent's records-commit check finds a different
  sha, re-run the matrix and re-stamp before pasting** — do not paste these
  numbers onto a later revision.
- Named items the parent should keep visible: the landed G2 line's label
  over-claims (per-file disposition counts printed as "loci"; EX-19 §3 — same
  class as the round-1 label defect); per-needle partial blindness stays
  (EX-14 §5, EX-19 A2–A4); EX-19's pointer-shadowing hole (a block carrying a
  version never evaluates its pointer) is named debt, not a HEAD verdict
  defect; H4 self-certification stands (external audit is the certificate).
- The capability table row for the census (if the parent updates it) should
  cite the v11 fail-closure semantics + the external diff-audit certificate at
  the records commit; seat-written capability-row patches belong in the c2
  chain's patch artifacts — this draft's §table is the required content.
- Pin-free self-check receipt: `evidence/pin-free-check.out` (the census's own
  needle regexes run over both draft files → 0 matches; no absolute `path:line`
  either). The check is what backs the drafting rule; re-run it after any edit
  to these drafts before the parent copies text out of them.
- All `[[FILL]]` fields trace to `.ufo/waves/arc3-loop1-round2/claims-frozen.md`
  (C1/C2/C3 claims) plus the wave receipts; SC-3 verified the before-values,
  the shared-instrument readings, and the artifact inventory in the LOG
  draft's notes.
