# SEAT RV-7 — chain c2, role reviewer (arc3-loop1-round2)

Task: cross-check EX-11's baseline reproduction against the round-1 recorded
readings (`.ufo/waves/arc3-loop1-round1/claims/c3/VZ-3/attack-log.txt`); flag
discrepancies.

## Verdict

**EX-11's baseline reproduction CONFIRMED on every comparable class** — and the
round-1 record itself independently validated (its control capture reproduces
byte-identically at its own inputs). Discrepancies found are: explained drift
(SCORECARD 1336→1417 tail append; A5 error line `:40`→`:45` from EX-28's re-key),
record-form limits (the round-1 A-series is excerpt-only), and two precision
items in EX-11's report (cD7/cD8 "identical without the plant" holds for verdict
and G11 only — counts differ; a crash is not a declared FAIL, resolved in their
current revision). One claim-wording bound for C2: the frozen sentence "every
round-1 silent-PASS injection now reproduces as a declared FAIL" holds for the
H1/H3 classes only — the H2 class and partial-needle narrowing still read PASS
on the landed revision, consistent with EX-16's named residual.

## 1. Work performed (evidence pointers)

- Inputs pinned: round-1 rev `e845c2b…`; round-1 instrument recovered via
  `git show e845c2b:.ufo/gates/c1-census-v10.py` → `36e96cd5…` 433 L; round-1
  files PROVINCE `d075a3c6…` 162 L, SCORECARD `30129a98…` 1336 L, SKILL
  `5c93c7c1…` 371 L. Round-2 HEAD `14b1682…`; pre-edit instrument `6f1d19ff…`
  490 L; files PROVINCE `d075a3c6…`, SCORECARD `a7c72950…` 1417 L, SKILL
  `483b0eba…` 371 L (`receipts/r2-identity-before.txt`).
- Replay harness (mine): `claims/c2/RV-7/replay-round1-record.py`; all runs on
  byte copies under `/var/tmp/rv7-baseline` (`--root` never the repo). Receipts:
  `claims/c2/RV-7/receipts/` (27 files) + `MANIFEST.sha256`.
- Cross-check artifact: `claims/c2/RV-7/baseline-crosscheck.md` (full table,
  F1–F10).
- EX-11 evidence read: `claims/c2/EX-11/tools/run-before-injections.py`,
  `baseline.md`, `receipts/` (27 outs + `c0-baseline.json` + `summary.txt` +
  47-line `SHA256SUMS`), `receipts-v11-spotcheck/` (5 outs + SHA256SUMS),
  archived instruments, report `seats/EX-11.md`.
- Their harness re-run by me in a shadow work dir
  (`/var/tmp/rv7-baseline/ex11-shadow`); their c0/cA/cA2/cB/cC receipts are
  byte-identical to my runs (cmp), and I re-executed their
  `tools/census-v11-neutered.py` — my run matches their `neutered.out` exactly
  (`receipts/rv7-v11-neutered.out`).
- Every EX-11 artifact pointer verified by sha256: `tools/census-pre-6f1d19ff.py`
  = `6f1d19ff…` (and its source `…/CR-5/tools/census-after.py` has the same
  sha); `tools/census-v11-landed.py` = `82fb807e…`; spotcheck SHA256SUMS pins
  both. Repo target churn recorded: `6f1d19ff…` (490 L) → `82fb807e…` (560 L,
  09:06:50) → `df9ffdf9…` (601 L, 09:11:50, live at my last check; ordinary run
  at HEAD still PASS 0/0/0/0 with `DECLARED FAIL CLASSES: []`).

## 2. Proposed changes

**none** (no patch text authored). Two advisory wording items for the chain's
records/report, text-only, no target written:

- Records text: scope the claim sentence to the H1/H3 classes; the H2 class
  (marker-excused fabricated pins) still reads PASS and is not closed by this
  chain (evidence below). This matches EX-16's landed header ("Still named,
  NOT closed here: H2 …").
- EX-11 §4 item 5: "identical without the plant" should read "identical
  verdict and G11 collateral"; the outputs differ in counts (SKILL loci 0 vs 1,
  CURRENT-OK 9 vs 10).

## 3. Before→after measurement (chain C2)

Commands (all reproducible from the two harnesses above): round-1 replays
`replay-r1-*.out`; round-2 pre-edit `rv7-r2-*.out`; after-state `post-*.out`,
`empty-post.out`, `rv7-v11-neutered.out`.

| reading | round-1 record (36e96cd5 @ e845c2b) | round-2 before (6f1d19ff @ 14b1682) | EX-11 baseline | RV-7 independent | after (82fb807e) |
|---|---|---|---|---|---|
| control | PASS 0/0/0/0, exit 0 (sha `3b677b8e…`) | PASS 0/0/0/0, exit 0 | `c0` = `af1600e7…` | byte-identical to `c0`; r1 control byte-identical to the round-1 capture | PASS, floor line `G2 ok (current-ok loci=5, total 17, floor=1)` |
| anchors | 6.5.0 / 6.5.0 / 6.7.0 | same | same | same | same |
| PROVINCE / SCORECARD / SKILL counts | 162·6 / **1336**·9 / 371·2 | 162·6 / **1417**·9 / 371·2 | same as round-2 | same | 162·6 / 1417·9 / 371·2 |
| H1 absent SKILL | PASS exit 0 | PASS exit 0 (`cA`) | same | same (`rv7-r2-A4`) | **FAIL exit 1**, `UNREADABLE ['SKILL.md: FileNotFoundError']` |
| H1 zero-byte SKILL | not recorded | PASS exit 0 (`cA2`) | same | same (`rv7-r2-empty-skill`) | **FAIL exit 1**, `UNREADABLE ['SKILL.md: 0 lines < declared max 20 (rows beyond EOF)']` |
| H1 control absent PROVINCE | FAIL, `:40,:40,:119` | FAIL, `:40,:45,:119` (`cB`) | same | same (`rv7-r2-A5`) | FAIL, declared class UNREADABLE for PROVINCE + marker SCOPE-ERRORs |
| H3 neutered needles | PASS, loci=0, `G2 ok` | PASS, loci=0 (`cC`) | same | same (`rv7-r2-blind`) | **FAIL exit 1**, `G2 SUSPECT (0/0, floor=1)`, `DECLARED ['BLIND-INSTRUMENT']` |
| A1 tail plant (`:1337`) | FAIL `undeclared=1` | FAIL `undeclared=1` | not in battery | `rv7-r2-A1-at-1337` / `-at-tail` FAIL | (class unchanged; scope bounds untouched) |
| A2 marker strip | FAIL scope-error | covered by EX-16 battery | not in battery | r1 replay byte-matches the record's error string | — |
| H2 marker-excused pin 9.9.9 | PASS, `:20 [pin] kimi=9.9.9 -> historical (inline marker)` | PASS (same detail) | not in battery | `rv7-r2-A3b…` | **still PASS** (`post-A3b.out`) — named residual |
| cD3 weak gate + ptr append | n/a (new class) | PASS exit 0 (my shadow run; totals PROVINCE 4/SCORECARD 2/SKILL 2 = 8 loci) | `cD3` PASS vs stock control `cD4` FAIL `undeclared=1` | replicated | still PASS (their spotcheck: `current-ok loci=2, total 8`) |

Round-1 record fidelity (my replays at the record's own inputs): control
**byte-identical**; A4/A3b PASS exit 0 with the record's exact detail lines;
A1 `undeclared=1` with the exact `:1337 [pin] kimi=6.4.0 -> STALE` line; A2
error string byte-identical; A5 three identical error lines. 7/7 classes.

## 4. Attacks / refutations attempted (verdicts)

1. **"The round-1 record reproduces verbatim."** Control: VERIFIED byte-exact.
   A-series: class + detail lines VERIFIED; byte-level NOT CHECKABLE — the log
   is a filtered excerpt (only the control was archived in full) and the A1
   plant text is not pinned (two plausible texts give identical output).
   Verdict: record honest at class level (F1).
2. **"EX-11's baseline is a different tree/revision than it claims."** REFUTED:
   `tools/census-pre-6f1d19ff.py` sha matches; their three file shas match HEAD
   blobs and my re-hash at 09:07; their c0 equals my independent run byte-for-byte.
3. **"SCORECARD 1336→1417 means scope drift or a reading change."** REFUTED:
   `git diff --numstat e845c2b..HEAD` = `81 0` on SCORECARD with a single
   `@@ -1336,0 +1337,81 @@` hunk; lines 1–1336 byte-identical; loci 9 unchanged;
   control PASS.
4. **"A5 must read `:40,:40,:119` at round 2."** REFUTED — it reads
   `:40,:45,:119`; explained by EX-28's re-key (marker line 40→45, documented in
   the instrument header). Class and exit unchanged (F3).
5. **"EX-11's weakening battery's exit-1s are declared FAILs."** PARTLY REFUTED,
   now resolved: the 09:01 revision's weak-pin variants died with `IndexError: no
   such group` (a crash, exit 1 — I reproduced the crash class myself on the
   pre-edit revision); the current revision keeps them as `cD1a/cD2a` (crash)
   beside group-preserving `cD1b/cD2b`. Only the group-preserving variants may
   be quoted as readings (F4). `cD1b` confirmed: a narrowed PIN needle is
   backstopped by the bare-version needle (dets read `[bare]`).
6. **"cD7 (plant) and cD8 (no plant) are identical."** REFUTED in part: verdict
   and G11 collateral (`['SCORECARD.md:530']`) are identical, but counts differ
   (SKILL loci 0 vs 1; CURRENT-OK 9 vs 10). The plant is assertion-silent
   (0 hits of `6.3.0`) but its count trace is a loci *drop*. Verdict: report
   wording, not a reading error (F8).
7. **"H1 as drafted closes the class."** REFUTED at draft level: the RV-11 draft
   keys on `OSError`, so a zero-byte SKILL.md stays a silent PASS — I measured
   PASS exit 0 pre-edit. CLOSED by the landed revision (rows-beyond-EOF rule):
   FAIL exit 1, `0 lines < declared max 20`, independently reproduced by me and
   present in EX-11's spotcheck. (F6 in the artifact: their receipts/summary.txt
   archives the identity block — I verified it; earlier draft of my artifact said
   otherwise and was corrected.)
8. **"Every round-1 silent-PASS injection now FAILs."** REFUTED as literal
   wording: the H2 class is unaffected — pin 9.9.9 with the inline marker still
   reads PASS `historical (inline marker)` on 82fb807e (`post-A3b.out`); and
   partial narrowing (cD3 weak gate, cD7 weak PIN+VER) still reads PASS with
   loci>0, which no internal floor can catch — exactly EX-16's named H4
   residual. Scope the sentence to H1/H3 (F7).
9. **"The after-state readings are at the settled revision."** NOT YET — the
   target moved three times in my window (`6f1d19ff` → `82fb807e` → `df9ffdf9`,
   601 L, 09:11:50). Both my after-state checks and EX-11's spotcheck are pinned
   to `82fb807e`; I re-ran the ordinary control at the live `df9ffdf9` (PASS
   0/0/0/0, `DECLARED FAIL CLASSES: []`). Any claim evaluation must name the
   revision it graded (F9). Their torn-intermediate catch (`9373964c`, 557 L) is
   consistent with this churn and is the same mid-landing class RV-7 caught in
   round 1.

## 5. Blockers

None. Notes: (a) scratch under `/var/tmp` only; one stray redirect to `/tmp`
failed with `Permission denied` (the standing round-1 `/tmp` defect — root-level
`/tmp` write refused). (b) The live target is a moving artifact; grade C2 at the
parent-frozen revision by sha, not by path. (c) EX-11 pins its pre-edit copy
against the round-1 tree copy (`CR-5/tools/census-after.py`) rather than a
`git show HEAD:` blob — equivalent by sha (`6f1d19ff…`) and arguably more
durable; noted, not a discrepancy.
