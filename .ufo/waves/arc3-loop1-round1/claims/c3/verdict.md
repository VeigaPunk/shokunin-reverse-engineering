# C3 verdict — census scope-table re-key at HEAD (chain convergence, seat VZ-3)

Wave arc3-loop1-round1 · chain c3 · 2026-10-19 · HEAD
`e845c2b524ad2e59871e004c51a1386e192a74ab` (no seat commits; parent integrates
records after the wave). Instrument `.ufo/gates/c1-census-v10.py`, 433 lines,
sha256 `36e96cd59b622f7b9acd424156d02184fa690df61dd96242899ad9a3b4f52d48`
(unchanged through the whole wave; mtime 2026-10-18 20:31).

## Verdict: **NOT-VERIFIED (partial)** — evidence-complete except the in-tree header disposition; no evidence contradicts the claim

Rationale: the frozen claim's end-state (`.ufo/waves/arc3-loop1-round1/claims-frozen.md:56-71`)
requires (a) the E22 finding dispositioned by measurement, (b) the census run at
HEAD, (c) the re-key/retire branch **only if** a row is undeclared/stale, (d) the
disposition *stated in the instrument's own header*, and (e) `PASS 0/0/0/0` at the
records commit, command A unchanged. Items (a)(b)(c) are delivered and
independently reproduced; **(d) is not landed** (EX-28, the only seat allowed to
write the target, is undelivered — instrument sha unchanged at every poll through
10:17Z); (e) is structurally parent-side (the records commit does not exist
during the wave; SC-7 pre-verified the drafted records text on a simulation tree).
An unrun check has not passed — hence NOT-VERIFIED, with the closing procedure
below. This is a partial delivery, **not** a refutation: every measured result is
consistent with the claim.

## Claim components — status and evidence

| # | Component | Status | Evidence |
|---|---|---|---|
| 1 | E22 finding dispositioned by measurement | DELIVERED | v9 recovered byte-exact (`213fe679…`, 429 L) from `arc2-loop1-round2/E22.md:264-692` (RV-11, RV-10, CR-5 agree); v9@`679af5d` (766-line) → `FAIL undeclared=2` exit 1 (blocks 731-737 / 747-766) = the finding verbatim; v9@`b21c0da` (701-line) → PASS; v9@HEAD → FAIL undeclared=2 + `SCOPE-ERRORS ["SCORECARD.md:635 marker '2026-10-18' absent"]`; v10@HEAD → PASS. Receipts: `claims/c3/RV-11/scratch/v9-at-*.txt`, `claims/c3/CR-5/receipts/v9-repro766.out` / `v9-repro701.out`, `claims/c3/RV-10/evidence/` |
| 2 | census v10 run at HEAD, recorded verbatim | DELIVERED | **six independent runs, one digest**: EX-26 ×2 (`.exit`=0), EX-29, SC-6, EX-30, RV-11, VZ-3 — all byte-identical, sha256 `3b677b8ee47eccb217616eba641fc0b66f72e53634a5ae51a92f8b04e2a22418` (`claims/c3/EX-26/census-at-HEAD.txt` = `SC-6/…` = `EX-29/census-head-verbose.txt` = `EX-30/census-head-t0.txt` = `RV-11/census-head.out` = `VZ-3/census-at-HEAD-vz3.txt`); verdict `PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`, exit 0 |
| 3 | re-key / retire branch (conditional) | **NOT FIRED — condition measured false** | 0 undeclared, 0 stale, 0 scope errors, 0 unresolved at HEAD; 20 SCOPE rows content-tight (EX-29 `scope-audit.txt` + `row-locus-counts.txt`; PL-3 plan §2: 0 stale-bound, 0 retire-candidates; RV-10 bounds audit: no open-ended/overshooting bound; max declared end 855). r8 re-key proven necessary pre-edit (pre-r8 instrument on post-insertion tree → 3 SCOPE-ERRORs, CR-5 `receipts/v10-r7-at-6bc4c29.out`) and clean post-edit (3 rows +1, byte-identical range content, RV-10 sha256 manifest) |
| 4 | disposition stated in the instrument's own header | **NOT LANDED** | EX-28 undelivered (no `claims/c3/EX-28/`, no `seats/EX-28.md`; instrument sha `36e96cd5…` at every poll, RV-11 poll-log check 10, CR-5 25 checks, RV-10 07:05-07:12, EX-29 07:14, VZ-3 through 10:17Z). Drafts exist, all patch-text only: `SC-6/e22-disposition.draft.md` §6 P1; `SC-7/census-header-draft.md` (assembled SC-6 P1 + records-check sentence, also at `records-drafts/`); `EX-26/proposed-census-header-disposition.patch.md`; `EX-29/PATCH-census-disposition.patch.md` (+ `patch-diff.txt`, `patched-run.txt`) |
| 5 | `PASS 0/0/0/0` at the records commit | **STRUCTURALLY DEFERRED (parent)** | records commit does not exist at wave time. SC-7 simulation: records-tree (HEAD files + drafted SCORECARD section) → PASS 0/0/0/0 exit 0; same tree + planted tail pin → FAIL undeclared=1 exit 1 (`seats/SC-7.md` §3). CR-5 A4 requires the **card-side** disposition sentence too, else the disposition is one-sided (`records-drafts/scorecard-section-draft.md` carries it) |
| 6 | command A unchanged (no corpus/knowledge edit) | T0 DELIVERED, T1 DEFERRED | T0 at HEAD: `{"knowledge_files": 81, "mapped": 81, "missing": [], "dangling": [], "citation_resolved_rules": 13, "coverage_score": 10.0, "depth_score": 10.0}` (`EX-30/recipeA-t0.txt`, pinned rerun identical); corpus aggregates `7480345a…` (83 surfaces) / `ad052608…` (95 files); `git status --porcelain -- corpus/` empty. T1 (after EX-28) pending by construction |

## Before→after reconciliation (the framing flag, converged by four seats)

- Frozen falsifiable: "census verdict at HEAD before the re-key (recorded
  verbatim) → PASS 0/0/0/0 at the records commit". Measured reality: at HEAD the
  v10 instrument already reads **PASS** — the before→after is **PASS→PASS**, not
  FAIL→PASS (EX-26 §3, RV-11 §3, PL-3 §3, CR-5 A4 independently).
- The E22 FAIL class is real and reproduced, but on **historical trees**: v9@679af5d
  (766-line) FAIL undeclared=2; v9@b21c0da PASS. The discriminating unit on **one
  tree** is the instrument revision: **v9@HEAD FAIL (undeclared=2 + marker@635
  SCOPE-ERROR, exit 1) → v10@HEAD PASS** — treatment = the r4 (+2 fixed-bound
  DATED rows, RECEIPT widening) + r8 (+1 shift) re-keys, each proven load-bearing
  (RV-10 §1-2, CR-5 §1, PL-3 §3).
- Therefore the round's freshness movement rests on (i) the instrument-revision
  flip on one tree, (ii) the E22 reproduction at its own tree, (iii) the accuracy
  of the disposition record (the item not yet landed). A manufactured FAIL→PASS
  was correctly not staged.

## Named debt (open items + measured latent holes; none is a HEAD defect)

1. **EX-28 undelivered** — the in-tree header disposition (claim item 4). The
   only seat authorized to write `.ufo/gates/c1-census-v10.py` produced nothing.
2. **Records commit re-run + card-side sentence** — parent-side; SCORECARD.md:850-852
   still reads "re-key or retire next calibration round" and needs the closure
   bullet (`records-drafts/scorecard-section-draft.md`); CR-5 A4: record both
   sides or the disposition is one-sided.
3. **command A T1** — EX-30 pending EX-28; expect 81/81, 13/13, 10.0/10.0
   unchanged (no corpus edit in this claim).
4. **H1 — absent CURRENT-only scoped file reads silent PASS** (measured: remove
   SKILL.md → PASS exit 0, `lines=0 loci=0`, both its rows CURRENT so no marker
   assertion fires; remove PROVINCE.md → FAIL "marker uncheckable"). VZ-3 A4,
   RV-11 A5; patch text `RV-11/proposed-missing-file-guard.patch.md`.
5. **H2 — same-line INLINE_MARKER token excuses an arbitrary pin value** (VZ-3
   A3: pin→`6.4.0` with marker retained → PASS "historical (inline marker)"; A3b:
   fabricated `rea-agents@9.9.9` → PASS). The inline-marker branch does no
   cache-existence check (contrast G17's version-intrinsic branch); G16 only
   re-labels live-equal values, so PL-3's A3 (live-equal + marker) still FAILs —
   the hole is exactly the non-live, non-historical value. Latent at HEAD (all
   marker-excused values at HEAD are genuine 6.4.0 history).
6. **H3 — blind instrument passes** (needles neutered → `loci=0`, `G2 … ok`,
   PASS; CR-5 `receipts/census-blind-at-head.out`; patch text
   `CR-5/proposed-g2-positive-floor.patch.md`). G2's second disjunct is vacuous
   when nothing is found.
7. **H4 — self-certification**: the census cannot detect its own SCOPE widening
   (widened row → still PASS; CR-5 `receipts/census-widened-at-head.out`,
   `widen-swallow.out`). External diff audit (`CR-5/tools/scope-diff.py` +
   `after-audit.sh`) is the certificate for any future re-key.
8. **H5 — gate-free version statement silently skipped** (RV-11 A2: "The build
   shipped 6.7.0 last week." at EOF → PASS; no `rea|kimi|…` token → not a locus
   in this unit). Unit boundary, stated.
9. **H6 — fixed-bound rationale comment unlanded** (RV-10 hunk 1: Z1 §4d's
   rationale never landed at the rows; optional mechanical guard in hunk 2).
10. **Wording** — `SCORECARD.md:908` "(undeclared=2, unreproducible at HEAD)":
    what is unreproducible at HEAD is the 701-line PASS; v9@HEAD FAIL undeclared=2
    **is** reproducible (RV-11 §3 claim 5; patch text
    `RV-11/proposed-scorecard-wording.patch.md`).
11. **/tmp quota exhaustion (standing)** — EDQUOT for this user during the whole
    wave (13G/16G tmpfs; even 1-byte writes fail while `df` shows 3.1G free).
    Every c3 seat relocated scratch (`/var/tmp`, `/dev/shm`, artifact dirs) with
    cause; the wave rule "scratch under /tmp" is not executable as written.
12. **`.ufo/gates/__pycache__/`** transiently recreated by module-import audits
    (EX-26/SC-6 removed theirs; re-appears with concurrent seats) — hygiene note
    for the parent; untracked, no content effect.

## Undelivered seats (c3 roster: PL-3, EX-26..31, SC-6, SC-7, RV-9..11, CR-5, VZ-3)

- **EX-27** — no artifacts, no report.
- **EX-28** — no artifacts, no report (the claim-blocking gap; item 4 above).
- **EX-31** — artifact `claims/c3/EX-31/interplay.md` landed (10:17Z); no seat
  report at verdict-write time.
- **RV-9** — no artifacts, no report.

Delivered (9 + this seat): PL-3, EX-26, EX-29, EX-30, SC-6, SC-7, RV-10, RV-11,
CR-5, VZ-3.

## Closing procedure (what flips this verdict to VERIFIED)

1. Apply one drafted header stanza to `.ufo/gates/c1-census-v10.py` (recommended:
   `SC-7/census-header-draft.md` assembled form — SC-6 P1 + records-check
   sentence; keep the shebang directly after the closing `"""`). Then:
   ```
   sha256sum .ufo/gates/c1-census-v10.py            # new digest ≠ 36e96cd5…
   python3 .ufo/gates/c1-census-v10.py --root .     # PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0), exit 0
   ```
   Audit the diff with `claims/c3/CR-5/tools/scope-diff.py` (must show header-only
   change; no bound movement) and confirm locus counts unchanged
   (PROVINCE 6 / SCORECARD 9 / SKILL 2).
2. At the records commit: re-run the census (the appended records text must stay
   locus-free in this unit — no `rea-agents@x.y.z`, no bare `6.x.y`, no
   `~`/`/`-absolute `path:line` — or re-key the bound in the same commit, the r3
   precedent). Land the card-side closure bullet (`records-drafts/scorecard-section-draft.md`).
3. Re-run command A at the records commit (expect 81/81, 13/13, 10.0/10.0) —
   EX-30 T1 or parent.

## VZ-3's own verification runs (this seat)

- Fresh census at HEAD: `claims/c3/VZ-3/census-at-HEAD-vz3.txt` (sha `3b677b8e…`,
  exit 0) — byte-identical to all five peer captures.
- Independent attacks on `/var/tmp` copies (byte copies of the three scoped files
  + instrument; live configs read read-only): `claims/c3/VZ-3/attack-log.txt` —
  control PASS exit 0; A1 planted tail locus → FAIL undeclared=1 exit 1; A2
  marker strip → SCOPE-ERROR FAIL exit 1; A3/A3b marker-excused pins → PASS
  (H2); A4 SKILL.md absent → PASS exit 0 (H1); A5 PROVINCE.md absent → FAIL
  exit 1.
