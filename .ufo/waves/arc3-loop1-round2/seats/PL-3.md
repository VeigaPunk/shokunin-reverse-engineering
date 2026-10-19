# SEAT PL-3 — chain c3, role planner — arc3-loop1-round2

Seat line: plan C3 (custody receipt v2 tool): interface (capture pre|post + verify
modes), v2 receipt fields (sha256, mtime epoch with correct UTC render, inode, ctime),
back-compat rules for v1 receipts, live-attack design (same-content rewrite on a
SCRATCH copy — never a real custody path). Artifact: `claims/c3/PL-3/plan.md`.

Repo HEAD throughout: `14b1682b1128d2e41085ebc79c9addeb8786d420` (read-only
`git rev-parse`; no git mutation by this seat). Wave rule discipline: writes only
under `claims/c3/PL-3/` + this report; scratch under `/var/tmp/pl3-r2` (`/tmp`
never used).

## 1. Work performed (evidence pointers)

- Read the freeze (`.ufo/waves/arc3-loop1-round2/claims-frozen.md:52-64`), the
  round-1 C3 verdict (`arc3-loop1-round1/claims/c3/verdict.md`), round-1 PL-3 plan
  (format precedent), the v1 receipts (CU-1 `cross/receipts/config-pre-pair.txt`
  sha `b8ed1936…`; its metadata sidecar; EX-01 `claims/c1/EX-01/config-pre-pair.txt`
  sha `28491903…`; EX-02 sha `312c6b40…`), SCORECARD recipes + round-1 section,
  and the custody SOP (`SKILL.md:242-281`).
- **Mid-flight change**: the implementer's tool landed during this seat
  (`.ufo/gates/custody-pair/custody-pair.py`, 39,157 B, sha256
  `112d01dc…61ecea`; `selftest` 15/15 CLEAN exit 0). The plan was rewritten
  accordingly: it now *ratifies the landed interface as the C3 contract* and
  spends its budget on measurement, gap-naming, and the attack table instead of
  inventing an interface in the abstract.
- **Own measurement suite against the landed tool, C0-C14**, all read-only over
  custody paths / mutating only synthetic replicas:
  `claims/c3/PL-3/measurements.txt` (sha256 `57bdff92…`). Summary: control 0;
  in-place same-content rewrite (no sleep) 11 `moved=mtime_ns`; replace-by-rename
  11 `moved=inode`; `cp --preserve=all` forgery 11 `moved=inode`; clean chmod 12
  `moved=mode,ctime_ns`; content flip 10; removed path 13; receipt tamper-away 10;
  truncated/empty receipt 2; v1 stanza live 12 (5/5 sha contract + LABEL-DEFECT);
  v1 sums live 0 (`MATCH-V1-PARTIAL`, 5/5); v1 pipe live 12 (`compared=3/11`);
  fresh live capture 5/5 exit 0 with UTC renders 5/5 AGREE against `date -u`.
- Scratch design prototype (superseded by the landed tool; kept only as the
  pre-landing design proof): `/var/tmp/pl3-r2/proto/custody-receipt.py`
  (sha256 `b1c911f1…`).
- Cross-checks of chain peers, read-only: EX-31 seat report + `identity-rederivation.out`
  (receipt-embedded tool hash = fresh hash on the landed revision); EX-33
  `attack-rewrite.md` (tamper-to-match case); EX-35 `backcompat.md` + adapter patch
  text; EX-36 `registry-row.patch.md`; RV-14 `tool-verification.md` (independent
  14-row battery, same shas); records drafts `claims/c3/records-drafts/`.
- Field-level diff, EX-32's wave receipt vs my landed-revision capture:
  all 11 per-path fields ALL EQUAL (no drift across the 12:04:06Z→12:07:30Z window).

Artifacts of this seat (shas derived immediately before writing this report):

| artifact | sha256 |
|---|---|
| `claims/c3/PL-3/plan.md` (the seat-line artifact; 259 lines) | `7c4e7c3655889792de091bf8d5de1a72b55a8cbab5799f7a136bc466066c5176` |
| `claims/c3/PL-3/measurements.txt` (217 lines, C0-C14) | `57bdff92e954fc419a36878b5d28097e0d897e570c1f77f646d61d36133d9d92` |
| `claims/c3/PL-3/registry-row.patch.md` | `a1e425ecf5f6f7077cbb860ad6327417e4fc77a043dfdf305d0b5e40f12411da` |
| `claims/c3/PL-3/sop-amendment.patch.md` | `070550d5d250e4ada45eb2799d36bbbf1bfe2bf33cf961259051bbbbf3688430` |

(Identity note, C1 rule #14 applied to this seat's own artifacts: the plan's
evidence-digest line was re-derived after the last append to `measurements.txt`
caught a stale self-citation — the plan now cites `57bdff92…`, the pre-append value
`c1b2ba00…` is superseded. No artifact of this seat was edited after the shas above
were taken.)

## 2. Proposed changes

Patch text only (no real-target writes by this seat; C3's real target belongs to
EX-31 alone):

- `claims/c3/PL-3/registry-row.patch.md` — SKILL.md registry row for
  `custody-pair` (entry/verdict map incl. the 10-13 classes, `selftest`
  self-invocation, read-only + tool-identity contract, v1 grading rule).
  **Overlap named**: EX-36 authored its own registry row
  (`claims/c3/EX-36/registry-row.patch.md`, more detailed on the registry
  preamble). The parent should merge into one row; mine contributes the
  measured per-class expectation table, EX-36's the preamble handling.
- `claims/c3/PL-3/sop-amendment.patch.md` — custody SOP v2 amendment (v2 capture
  as the primary artifact; post-pair `verify --live` with exit semantics — 11
  REWRITE-DRIFT voids zero-drift exactly as a content mismatch does; v1 receipts
  verified-not-edited with the label-defect rule; tool-revision re-capture rule).
- Records-side one-liner is embedded in `plan.md` §7 for the parent's
  SCORECARD/LOG entry; NOT a patch file.

## 3. Before → after measurement (chain C3 claim)

**Before** (all re-measured first-hand at HEAD, not quoted): `.ufo/gates/custody-pair/`
absent; v1 label defect live (epoch `1792011200` → `date -u` `20:53:20Z` vs
receipt-printed `17:53:20` under `MTIME_UTC`, `config-pre-pair.txt:15`); sha-only
blindness — same-content rewrite, `sha256sum -c` → `OK`, rc 0, while
`stat` moved (`mtime 1792411355→…356`, `inode` unchanged; rename: `inode
10951213→10951221`).

**After** (landed tool, same claim components):

```
# control
capture --out /var/tmp/pl3-r2/L/pre.txt --paths … → OK paths=2/2 exit=0
verify pre.txt --live → VERDICT: MATCH paths=2 MATCH=2 exit=0
# same-content rewrite, in place, no sleep
verify pre.txt --live → REWRITE-DRIFT moved=mtime_ns; SHA256-CONTRACT: 2/2 agree; exit=11
# replace-by-rename (same bytes)
verify pre.txt --live → REWRITE-DRIFT moved=inode,mtime_ns; exit=11
# clean chmod-only
verify pre-e.txt --live → METADATA-DRIFT moved=mode,ctime_ns; exit=12
# content flip
verify pre.txt --live → CONTENT-DRIFT moved=sha256; exit=10
# path removed / tamper-away / truncated receipt
exit=13 / CONTENT-DRIFT exit=10 / USAGE exit=2 (evidence C5/C6/C7–C9/C14)
# v1 receipts vs live (read-only)
sums-v1 → exit=0, MATCH-V1-PARTIAL 5/5, SHA256-CONTRACT 5/5
v1-stanza → exit=12, SHA256-CONTRACT 5/5, LABEL-DEFECT ×5
pipe-v1 → exit=12, SHA256-CONTRACT 5/5, LABEL-DEFECT ×10, compared=3/11
# live pair by the landed revision (EX-31's, independently re-verified by me + RV-14)
verify capture-pre.txt --live → MATCH 5/5 exit=0; pre↔post → MATCH 5/5 drift=0 exit=0
```

The falsifiable unit, one scratch state: `sha256sum -c` → `OK` rc 0 (v1 method
blind) **vs** `verify --live` → `REWRITE-DRIFT exit 11` with the sha contract
still agreeing — i.e. the new detection is exactly the identity pins, not a
content side effect. Chain verdict: every frozen component measured; the
revision-staleness residual is narrowed to EX-32's earlier wave receipt (EX-31's
pair is on the landed revision), annotated in plan §0.7/§5/§6.1.

## 4. Attacks / refutations attempted (with verdicts)

- *"sha256-only would have caught the rewrite anyway."* **Refuted** (C1/C12:
  digest identical, `sha256sum -c` rc 0, verify still 11). Matches EX-31 A1/RV-14 #7.
- *"Second-resolution ctime pins are enough."* **Refuted** — the no-sleep
  in-place rewrite lands 11 via `mtime_ns`; nanosecond fields are load-bearing
  (also EX-40's declared note).
- *"mtime restoration defeats detection."* **Refuted** — `cp --preserve=all`
  over rename → 11 via inode (C12); mtime-restored in-place → 11 via ctime_ns
  (EX-31 A1; RV-14 #7).
- *"v1 receipts verify cleanly under v2."* **Refuted as a general statement** —
  time-carrying v1 forms exit 12 (LABEL-DEFECT) with the sha contract 5/5; only
  sums-form exits 0. Graded rule recorded in plan §3 so nobody reports either
  extreme.
- *"EX-32's wave receipt satisfies the claim's 'captured by the tool'."*
  **Refuted on revision grounds** (`# tool: 4862f642…` < landed `112d01dc…`),
  softened by the all-fields-equal diff; EX-31's pair satisfies it. Verdict:
  annotate or re-capture EX-32's receipt.
- *"Receipt tampering is caught."* **Partially refuted** — tamper-away → 10 (my
  C6), but tamper-**to-match** passes `verify --live` exit 0 (EX-33 case J);
  sidecar check is the available out-of-band guard. Named limit, plan §6.4/§4 A6b.
- *"The tool might be touching custody."* **Refuted for the observed window** —
  write-guard refuses receipt writes over a custody path (selftest; RV-14 #12),
  and live digests matched the round-1 receipt 5/5 at every capture by this seat.
- *"This seat's own artifact identity can be asserted once."* **Refuted on
  itself** — the plan's `measurements.txt` digest went stale after my C14
  append; caught and re-derived (rule #14; see §1 identity note).

## 5. Blockers

None for this seat; the artifact is complete and re-runnable. Items for the
parent (named, not absorbed):

1. **Commit**: `.ufo/gates/custody-pair/` is untracked (`??`); exclude
   `__pycache__/` (re-created under `.ufo/gates/` and `custody-pair/` by
   import-audits — round-1 SC-2 precedent; EX-31 also names the foreign
   `c1-census-v10` pyc).
2. **EX-32 wave receipt** (`claims/c3/receipts/config-pre-pair-v2.txt`, sha
   `fa9706c6…`) carries the superseded tool sha `4862f642…` — annotate with the
   revision mapping + the all-fields-equal diff (my C10) or re-capture; EX-31's
   pair is the claim-satisfying one.
3. **Registry-row duplication** (mine vs EX-36's) — merge, don't land both.
4. **Observed consistency flag**: `claims/c3/EX-40/matrix-run.txt` reports
   `MATRIX: FAIL` with empty `status=` fields and `paths-recorded=0` for cases the
   landed tool measures as declared (my C0-C14; RV-14); EX-40's scratch oracle in
   its current state does not reproduce its own declared table — the parent
   should have EX-40 reconcile or discard the oracle before the records cite it.
5. **Naming deviation observed**: `claims/c3/receipts/` sits at chain level,
   outside the per-seat artifact convention (`claims/<chain>/<SEAT>/`); it is not
   this seat's write. The parent decides whether the records reference it.
