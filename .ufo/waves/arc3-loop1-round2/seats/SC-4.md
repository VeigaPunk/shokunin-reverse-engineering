# SC-4 — chain c3 — role scribe — wave arc3-loop1-round2 — seat report

Seat SC-4 · chain c3 · role scribe · 2026-10-19 (report written 12:12Z). Task per
seat line: **records drafts for the parent (not applied): LOG + SCORECARD
round-section drafts for C3, PIN-FREE discipline; two files at
`claims/c3/records-drafts/`.** No repo file was written by this seat; no git
mutation; scratch under `/var/tmp/sc4` only.

## 1. Work performed (evidence pointers)

Deliverable — two drafts, also mirrored under the freeze-rule path
`claims/c3/SC-4/` (round-1 SC-7 precedent), shas:

| file | lines | sha256 |
|---|---|---|
| `claims/c3/records-drafts/log-entry-draft.md` (= `claims/c3/SC-4/…`) | 155 | `861aeb2eac99e6ace76f64dc4c03aa67fee5970357f691bc72be02e2d3fc6344` |
| `claims/c3/records-drafts/scorecard-section-draft.md` (= `claims/c3/SC-4/…`) | 198 | `10d157a9d0b3cb11641334ed328de512e61e16303d26ebd73d00dd97c1e9d81b` |

(These are the fresh identities, re-derived after the drafts' last edit — the §3
measurement note — per rule #14. That edit lies outside the BEGIN/END markers:
the measured section block is byte-unchanged at sha `0055feda…`, re-extracted
and re-hashed after the edit; the drafts' file hashes are therefore expected to
drift again if the parent fills slots, and the measured block hash is the one
that must be re-checked, not the file hash.)

Drafted section text (between the BEGIN/END markers of the SCORECARD draft),
final revision: 105 lines, sha256
`0055fedaa0ce834d31d23a846f1dcc0a09d1cfbb5247af8529b8eb2405eea59d`
(copy: `claims/c3/SC-4/section-rev4.txt`). C3 bullet, C3 verdict-table row,
C3 learning sentence and C3 carried-debt lines are drafted complete; C1, C2,
cross-cutting numbers and the records-commit re-run are `⟨FILL⟩` slots for the
other chains/parent (the drafts name the producing seat for each).

Sources read (all round-2 unless noted): `claims-frozen.md:52-64` (C3 claim);
round-1 `claims/c3/verdict.md`, `claims/c3/records-drafts/*`,
`claims/cross/consistency.md:365-373` (label defect),
`claims/cross/receipts/config-pre-pair-metadata.txt`;
`.ufo/gates/c1-census-v10.py` (SCOPE `:139-161`, needles `:163-167`, locus
logic `:327-424`); `.ufo/gates/custody-pair/custody-pair.py`; round-2 C3
artifacts: `claims/c3/EX-31/*`, `EX-32/*`, `EX-33/attack-rewrite.md`,
`EX-35/*`, `EX-37/*`, `EX-40/*`, `PL-3/measurements.txt`, `RV-12/*`,
`RV-14/receipts/*`, `VZ-3/*`, `claims/c3/receipts/config-pre-pair-v2.txt`;
cross artifacts `claims/cross/CU-1/*`, `claims/cross/VZ-4/c3-attacks-out.txt`,
`claims/cross/CN-2/merged-SCORECARD-section.md`.

Independent measurements run by this seat (read-only over repo/custody paths):

- Census simulation, 4 revisions of the drafted section on `/var/tmp/sc4`
  scratch roots; outputs copied to `claims/c3/SC-4/sim-outputs/` (see §3).
- `custody-pair.py selftest --scratch /var/tmp/sc4/selftest-scratch` →
  `CUSTODY_PAIR_SELFTEST: CLEAN cases=15 passed=15 failed=0 exit=0`;
  captured output `claims/c3/SC-4/selftest-scribe.out`, sha256
  `cfee36b6015f0a5aac0c8f6c1ba0fa49b3b7743145575fa30210be6e898e701b`
  (an earlier identical run, output sha `de6f7f81…`, is cited in the LOG draft).
- Needle scan of the final section text with the instrument's own regexes
  (PIN/VER/PTR/CACHE/REA_GATE): **zero hits each**.

Observations recorded for the parent (not my task, but records-relevant):

- **Tool churn inside the wave.** `.ufo/gates/custody-pair/custody-pair.py`
  was observed by seats at several identities within ~2 minutes —
  `4862f642…`/38651 B (CU-1 `tool-revisions.txt`, 09:04:00 -03),
  `b10ad1c8…`/38981 B (RV-14 `tool-state-1.txt`, 09:04:40 -03),
  `72d5231f…`/38651 B (EX-33 §0, "12:04:40Z" = the same instant), settling at
  **`112d01dc…`/39157 B (09:05:19 -03)**, which is the revision the pre/post
  pair, the attack ladders and my selftest all ran against. My own read at
  09:03 caught a revision (`b10ad1c8…`) whose verify summary line raised
  `KeyError: 'sha_agree'`; CU-1's diff shows that line fixed in the next
  revision (rev A → rev B delta). The parent must re-derive the landed identity
  per rule #14 — the drafts say so explicitly and carry no pin.
- **Census instrument also churned** (`82fb807e…` → `09e270c2…` → `c95a5cf3…`
  → `df9ffdf9…` across my 12:07–12:12Z runs; EX-16's v11 landing in flight).
- **Untracked residue**: `.ufo/gates/custody-pair/__pycache__/` and
  `.ufo/gates/__pycache__/` are present (the round-1 recurring class) — they
  must stay out of the wave-artifacts and work commits.

## 2. Proposed changes (patch-text paths or "none")

**None applied by me.** The two drafts above are the proposed text for the
parent's records commit (LOG append at EOF after `LOG.md:1430`; SCORECARD
section append after `SCORECARD.md:1417`, i.e. inside the
census-undeclared tail — hence the pin-free discipline). Remaining `⟨FILL⟩`
slots are named in each draft with their producing seats: C1/C2 bullets and
numbers, delivery count, records-commit re-run quote, and any close-time custody
capture. A separate round-1-style patch to `LOG.md`/`SCORECARD.md` is not
needed; the drafts are paste-ready once slots are filled.

## 3. Before→after measurement (chain c3: C3-complete, pin-free drafts)

Commands (scratch `/var/tmp/sc4`, instrument invoked as
`python3 .ufo/gates/c1-census-v10.py --root <tree> --quiet`; tree = copy of the
three scoped files at HEAD `14b1682` ± the appended section text; control tree
adds one planted `rea-agents@6.4.0` line at the tail):

| section revision | section sha256 | instrument sha | base | records | control |
|---|---|---|---|---|---|
| 1 (skeleton, 77 L) | `683d4bd7…` | `82fb807e…` | PASS 0/0/0/0 (9 loci) | **PASS 0/0/0/0 (9 loci)** | FAIL undeclared=1 (10 loci) |
| 2 (evidence-filled, 90 L) | `f805cbb1…` | `82fb807e…` | PASS (9) | **PASS (9)** | FAIL undeclared=1 (10) |
| 3 (residuals-filled, 102 L) | `e2f9164b…` | `09e270c2…` | FAIL (G2 floor) | FAIL, undeclared=0 (9) | FAIL undeclared=1 (10) |
| 4 (final, 105 L) | `0055feda…` | `c95a5cf3…` | FAIL (G2 floor) | FAIL, undeclared=0 (9) | FAIL undeclared=1 (10) |

Verbatim (rev-2, the clean comparison — instrument `82fb807e…` before and after
the runs):

```
$ python3 .ufo/gates/c1-census-v10.py --root /var/tmp/sc4/sim-records --quiet   # exit 0
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=1507 loci=9
SKILL.md       lines=371  loci=2
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
$ python3 .ufo/gates/c1-census-v10.py --root /var/tmp/sc4/sim-control --quiet   # exit 1
SCORECARD.md   lines=1510 loci=10
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=1 unresolved=0)
```

Reading: the drafted section adds **zero loci** (SCORECARD 9 → 9) and zero
needle hits at every revision; the control proves the detector is live on the
appended region (a planted pin → `UNDECLARED (1)`, exit 1). At revisions 3–4
the **base tree fails identically** (`G2 positive-assertion guard: SUSPECT` —
current-ok loci per file PROVINCE 1 / SCORECARD 4 / SKILL 0, floor 1/file):
that is EX-16's in-flight C2 landing, not the records text — base and records
differ only by the appended region (both 9 loci, undeclared 0). **Parent: do
not land the records section as "green" while the instrument reads red at HEAD;
re-run at the records commit and quote the then-current verdict** (the drafts
say this in their §3 notes).

C3's own claim, measured by peers and re-checked by me where cheap: label defect
reproduced (RV-14 `label-defect-repro.txt`, EX-32 B2: v1 canonical receipt →
5/5 `LABEL-DEFECT` → exit 12, not a silent pass); v2 receipt fields and declared
exit table (EX-31 `exit-codes.txt`); same-content rewrite detection — six forms,
all `REWRITE-DRIFT` exit 11 where sha-only is silent (EX-33 §2, plus EX-31
`attacks.out`, EX-32 battery A, PL-3, VZ-4, RV-14 §8); v1 back-compat 5/5
(EX-35); live pre/post pair `MATCH 5/5 exit 0` with sidecars OK and cross-seat
field agreement (EX-31 pair, re-audited by EX-33 §8; CU-1 corroboration 50/50;
RV-12 capture agrees). My independent selftest: CLEAN 15/15 (§1).

## 4. Attacks / refutations attempted, with verdicts

1. **Pin injection into the drafted region** (my own control): planted
   `rea-agents@6.4.0` at the tail of the records tree → `FAIL undeclared=1`,
   exit 1. Verdict: the pin-free discipline is load-bearing and the detector is
   live on my text's own region.
2. **Self-refutation: can the C3 record be written pin-free at all?** The claim
   concerns three client configs whose filenames are census gate tokens.
   Verdict: yes — the drafts name them by role ("three client configs + two
   shell profiles"), carry no version literal, no `@`-pin, no `path:line`
   pointer; measured zero hits with the instrument's own regexes (four
   revisions).
3. **Are the drafts' filled values overstated?** Each filled slot was checked
   against its artifact: tool sha/exit classes (EX-31), selftest (EX-31 +
   mine), pre/post pair (EX-31 + EX-33 §8 + CU-1), v1 compat (EX-35 + EX-32 B2),
   attacks (EX-33/EX-31/EX-32/PL-3/RV-14/VZ-4). Verdict: no slot asserts an
   unrun check; the two facts that are only mine (selftest run, needle scan)
   are labelled scribe-level.
4. **EX-40's unreadable-path probe (recorded, not fixed):** `capture` over a
   `chmod 000` file raises an uncaught `PermissionError` traceback, exit 1 —
   outside the declared class table (`real-tool-unreadable.txt` +
   `.traceback`). Verdict: a real residual; named in both drafts' carried-debt
   lines.
5. **EX-33's receipt-tamper finding (recorded):** a tampered receipt returned
   `MATCH exit 0` — `verify` never reads the capture-time sidecar. Verdict: a
   real residual (suggested patch text is EX-33's, not landed); named.
6. **Refutation of "the records section is safe to land now":** the instrument
   is red at HEAD during my window for C2-side reasons; my section is not the
   cause (base ≡ records). Verdict: not a refutation of the drafts, but a
   landing precondition — recorded in §3 of the SCORECARD draft.

## 5. Blockers, gaps, and what the parent must do

- **No blocker for the drafts themselves.** Deliverable complete and measured.
- **Gaps named in the drafts:** at write time the chain's verification/verdict
  seats held evidence but no landing reports — `CR-4/` (bench receipts,
  block-level probes, tool-pin; no report), `RV-11/` and `RV-13/` (dirs only),
  `VZ-3/` (independent captures + comparison script, no `verdict.md`). Their
  slots are either filled from other landed artifacts or left `⟨FILL⟩` with the
  producing seat named.
- **Census/records coupling:** re-run the census at the records commit once
  C2's landing settles; if the per-file G2 floor is still red on the base tree,
  that is a C2 finding, and the records commit must not cite a green census.
- **Rule #14 applies to the drafts' own identity claims:** the drafts quote
  tool shas as observations; re-derive at landing (the tool churned four
  observed identities in-window).
- **Residue:** keep `__pycache__` out of commits — `.ufo/gates/custody-pair/__pycache__/`
  and `.ufo/gates/__pycache__/` are untracked and in-window (§1).

- **Late-landed evidence (post-write, for the parent's residual line):**
  `seats/CR-4.md` landed after the drafts were written and measures further
  residual classes the drafts' carried-debt line does not yet enumerate — a
  capture-atomicity (TOCTOU) defect "confirmed, no silent pass"; receipt-store
  forgery and a metadata-layer change-time forgery that defeat a same-privilege
  comparison; and a scoping caveat on the v1-interop clause (same-second
  rewrites). It also confirms the selftest CLEAN 15/15. The drafts carry a
  `⟨FILL: parent keeps these named or records their closure⟩` slot for exactly
  this; fold CR-4's classes there (the parent should take the wording from
  `CR-4/residual-threat-model.md`, sha256 `02ab25eb…` per `seats/CR-4.md:20`).
  `seats/RV-12.md` landed too: its independent comparator agrees on all five
  claim components (label fixed, v1 sha-verifiable, pre-pair captured, zero
  drift) — no refutation.

## 6. Identity at handoff (rule #14 — re-derived, not carried)

| artifact | sha256 at handoff (12:14Z) |
|---|---|
| `seats/SC-4.md` (this report) | re-derive: see `sha256sum` in the wave tree |
| `claims/c3/records-drafts/log-entry-draft.md` | `861aeb2eac99e6ace76f64dc4c03aa67fee5970357f691bc72be02e2d3fc6344` |
| `claims/c3/records-drafts/scorecard-section-draft.md` | `10d157a9d0b3cb11641334ed328de512e61e16303d26ebd73d00dd97c1e9d81b` |
| measured section block | `0055fedaa0ce834d31d23a846f1dcc0a09d1cfbb5247af8529b8eb2405eea59d` |
| `.ufo/gates/custody-pair/custody-pair.py` (chain c3 target) | `112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa` (stable through 12:12Z after the 09:05 churn) |
| `.ufo/gates/c1-census-v10.py` (C2 target, in flight) | `df9ffdf963efa549f55c65770bca25120513015fe3b01c150a1087e0cf8e6b43` |

