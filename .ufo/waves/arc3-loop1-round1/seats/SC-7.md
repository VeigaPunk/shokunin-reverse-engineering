# Seat SC-7 — chain c3, role scribe — records drafts (census header + LOG entry + SCORECARD section)

Wave arc3-loop1-round1 · 2026-10-19 · HEAD `e845c2b524ad2e59871e004c51a1386e192a74ab`
Seat writes: this report + `claims/c3/SC-7/**` + `claims/c3/records-drafts/**` only.
No git mutation, no install, no custody-path access, nothing applied anywhere.

Status: **COMPLETE**. Three draft files delivered (patch text, NOT applied):
census-header change text, LOG.md entry draft, SCORECARD.md round-section draft
for C3.

## 1. Work performed (each bullet with an evidence pointer)

- Read the frozen claims and rules: `.ufo/waves/arc3-loop1-round1/claims-frozen.md`
  (C3 claim :56-71; seat discipline :73-88; roster :90-98).
- Ran census v10 at HEAD `e845c2b` → `PASS (stale=0 ambiguous=0 undeclared=0
  unresolved=0)`, exit 0; scratch capture `/var/tmp/sc7/census-head-quiet.txt`
  (sha256 `115ab6d2…`). Cross-checked the four independent full captures —
  EX-26 `claims/c3/EX-26/census-at-HEAD.txt`, SC-6, EX-30 `census-head-t0.txt`,
  RV-11 `census-head.out` — each sha256-verified by me: all
  `3b677b8ee47eccb217616eba641fc0b66f72e53634a5ae51a92f8b04e2a22418` (one
  digest, 4-way).
- Located the E22 finding and its history: `SCORECARD.md:850-852` (finding),
  `:908`/`:990`/`:1096` (prior dispositions); row-level re-keys `265e1aa` (r4,
  rows added, fixed-bound) and `6bc4c29` (r8, three rows +1) — corroborated via
  SC-6 draft §1/§3 (sha `ed5cf1f7…`), RV-10 bounds audit, RV-11
  `e22-reproduction.md`, CR-5 §1.
- Read peer artifacts to align the drafts: EX-26 header patch (sha
  `f467814d…`); SC-6 `e22-disposition.draft.md` (P1 stanza base); EX-30
  invariance T0; RV-11 (the `:908` "unreproducible at HEAD" wording
  discrepancy); CR-5 (attacks A1-A4; A4 both-sides-closure requirement;
  census-sha pin recommendation); PL-3 plan (§6 header-edit spec; A5c
  token-free append = preferred form); EX-29 scope audit; CN-2 records
  outline (`claims/cross/records-outline.md` — merge slots §7 expect SC-7 at
  `claims/c3/SC-7/`; couplings §6; C3 closes at §6.4).
- Wrote the three drafts: `claims/c3/SC-7/{census-header-draft,log-entry-draft,
  scorecard-section-draft}.md` — sha256 `5d712057…` / `f1c2b76f…` /
  `b3a2cab5…` — mirrored byte-identical to `claims/c3/records-drafts/` (the
  seat-line path; both live under `claims/c3/`, satisfying the hard rule and
  CN-2 §7's expected location).
- Built and ran the records-tree simulation (see §3) on `/var/tmp/sc7` scratch:
  drafted records text → PASS 0/0/0/0; planted tail locus → FAIL undeclared=1.
- Relocated scratch to `/var/tmp/sc7/` — **/tmp is EDQUOT for this user**
  (`echo test > /tmp/x` → `write error: Disk quota exceeded`; 13G/16G tmpfs by
  other seats; standing hazard `SCORECARD.md:990-991`; r5 mandate was /var/tmp;
  peers used /dev/shm or in-memory). Deviation from "scratch under /tmp", with
  cause; cleaned up at close.
- Polled `seats/` + `claims/` every 60 s (background loop, 12 checks logged by
  report time): C3 peers PL-3, EX-26, EX-29, EX-30, SC-6, RV-10, RV-11, CR-5
  landed; **EX-28 had not landed** (instrument sha unchanged `36e96cd5…` at
  the last check, 10:13:30Z).

## 2. Proposed changes (patch text, NOT applied)

- `claims/c3/records-drafts/census-header-draft.md` (mirror `claims/c3/SC-7/`) —
  census-header change text for `.ufo/gates/c1-census-v10.py` lines 1-2:
  SC-6's P1 stanza (base, sha `ed5cf1f7…`) + one SC-7 records-commit sentence,
  with the full assembled applyable form; §4 reconciles the peer variants
  (EX-26 patch, PL-3 §6, CR-5 requirements). EX-28/parent applies.
- `claims/c3/records-drafts/log-entry-draft.md` — LOG.md entry draft (append
  after `:1394`): CN-2 §3 skeleton; the C3 bullet is complete
  (finding quote → HEAD verdict verbatim → disposition → records-commit
  pre-verification); `⟨…⟩` slots for C1/C2/custody/dispatch.
- `claims/c3/records-drafts/scorecard-section-draft.md` — SCORECARD.md
  round-section draft (append after `:1336`): CN-2 §4 skeleton; the C3 bullet
  (with the CR-5 A4 card-side closure sentence and the instrument sha pin),
  the C3 verdict-table row, the C3 learning sentence and the C3 carried-debt
  line are complete; `⟨…⟩` slots for C1/C2/depth/measured-at.
- No other changes; nothing applied anywhere.

## 3. Before→after measurement (chain c3 claim)

BEFORE — at HEAD `e845c2b` (command and output verbatim; scratch capture
sha256 `115ab6d2…`):

```
$ python3 .ufo/gates/c1-census-v10.py --quiet          # exit 0
live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=1336 loci=9
SKILL.md       lines=371  loci=2
SCOPE-ERRORS (marker assertions): []
G2 positive-assertion guard: ok
G7 configured!=held warnings: []
G11 current-ok without receipt language: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
```

(The finding's own before-state — v9@`679af5d` FAIL undeclared=2 — is
reproduced by RV-11/CR-5/PL-3 on the recovered v9; not re-run by this seat.)

AFTER — simulated records commit (scratch trees under `/var/tmp/sc7`; the
records commit does not exist yet, so this is the closest measurable form —
same instrument, same live anchors, `--root` on a tree carrying the drafted
records text):

```
$ python3 .ufo/gates/c1-census-v10.py --root /var/tmp/sc7/sim-records --quiet   # exit 0
SCORECARD.md   lines=1386 loci=9
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
$ python3 .ufo/gates/c1-census-v10.py --root /var/tmp/sc7/sim-control --quiet   # exit 1
SCORECARD.md   lines=1387 loci=10
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=1 unresolved=0)
```

- sim-records = the three scoped files at HEAD + the drafted SCORECARD section
  (50 lines, extracted between the draft's BEGIN/END markers) appended to
  `SCORECARD.md`; output sha256 `2c7b362e…`.
- sim-control = sim-records + a planted `rea-agents@6.4.0` tail line; output
  sha256 `db0f611f…`. The drafted text adds **zero** loci (9→9) and keeps the
  PASS; the control shows the detector is live on the same appended region
  (same class as SC-6 fixture A1).
- Command A unchanged by this chain: EX-30 T0 `81/81, 13/13, 10.0/10.0`
  (`claims/c3/EX-30/recipeA-t0.txt`); `git status --porcelain -- corpus/`
  empty (EX-30 `gitstatus-corpus-t0.txt`); SC-7 wrote nothing under `corpus/`.

## 4. Attacks / refutations attempted, with verdicts

| # | attack | result | verdict |
|---|---|---|---|
| A1 | records append trips the census (planted `rea-agents@6.4.0` after the drafted section) | FAIL undeclared=1, exit 1 (`/var/tmp/sc7/sim-control.out`) | **caught** — the fail-closed posture holds on the appended region; matches SC-6 A1 / CR-5 / PL-3 A2 |
| A2 | is the drafted text itself pin-free? (census over the drafted tree) | PASS, loci 9→9 (`sim-records.out`) | **verified** — no pin/version/pointer locus in the C3 text; placeholders pin-free too |
| A3 | marker/scope damage from the append | SCOPE-ERRORS `[]`, G11 `[]`, G7 `[]` on the simulated tree | **no damage** — append-only at EOF; declared rows untouched |
| A4 | wrong-path risk (seat line `claims/c3/records-drafts/` vs hard rule + CN-2 §7 `claims/c3/SC-7/`) | both paths written, byte-identical (shas match) | **resolved** |
| A5 | CR-5's "no-op claim" attack (PASS→PASS disposition) — folded | SCORECARD draft now carries the card-side closure of the E22 debt line + the instrument sha pin; freshness movement rests on the disposition record + the v9@HEAD→v10@HEAD flip (peer-measured) | **respected in draft text** |
| A6 | RV-11's `:908` wording discrepancy — folded | my drafts use the precise form ("the FAIL class unreproducible under v10; v9 stays red at HEAD by construction"); RV-11's `:908` patch stays a separate parent proposal | **respected** |

Not duplicated (peer coverage, all read and cited): CR-5 injections +
self-certification/blind-instrument holes; RV-11 A1-A7 (incl. absent-file
hole); PL-3 A1-A8 (incl. laundering A6/A7, A5c preferred token-free append);
SC-6 A1-A6; RV-10 laundering-refusal re-measurement. The drafts are written to
their constraints (fixed-bound posture; no coverage expansion; token-free
append).

## 5. Blockers / environment

- **/tmp EDQUOT** (standing, fleet-wide this wave — VZ-4 counts 147 zero-byte
  casualties): scratch at `/var/tmp/sc7/`, removed at close. The wave rule
  "scratch copies go under /tmp" is not executable as written on this host;
  deviation recorded (peers: /dev/shm, in-memory, artifact dirs).
- **EX-28 (the census-writer seat) had not landed** by the last poll
  (instrument sha256 still `36e96cd5…`, 10:13:30Z): all C3 header proposals
  (EX-26, SC-6 P1, PL-3 §6, SC-7 assembled) remain patch text. The claim's
  terminal reading ("PASS at the records commit") is parent-side and
  pre-verified by the §3 simulation **for the drafted text**; re-verify after
  any merge.
- Merge note: the LOG/SCORECARD drafts keep CN-2's `⟨…⟩` slots by design
  (SC-7 had C3 evidence only). If the merged records text differs from the
  drafts, re-run the census at the records commit before sealing — the drafts'
  sentences are written for the drafted text.
