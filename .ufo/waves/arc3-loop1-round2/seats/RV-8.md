# RV-8 seat report — arc3-loop1-round2, chain c2, role reviewer

Seat RV-8 | chain c2 | role reviewer | 2026-10-19 | repo HEAD `14b1682`
(census modified in the worktree by EX-16's landing, not committed).

Seat task: review EX-23's header text for accuracy against the landed code —
classes named exist; residuals named exist.

Reviewed artifact: `claims/c2/EX-23/header.patch.md` (12,353 B, 09:09:51
-0300), anchored by EX-23 on digest `82fb807e…` (560 L).

Target digest trail during this seat (all measured): 6f1d19ff (pre-wave) →
EX-16 landings 1431620f / 2a89793a / 9373964c / 59975ae0 / 82fb807e →
076bd621 / c95a5cf3 (per-file floor iterations) → df9ffdf9 (601 L, "r9 final"
12:12:15Z) → a4c16763 (603 L, identity-line fix, 12:16:31Z) → **d0772ce8**
(610 L — the digest at my close; still moving). All core verdicts were
re-verified at d0772ce8; receipts name their digest.

## 1. Work performed (evidence pointers)

- Ground truth: HEAD blob 6f1d19ff / 490 L; final source inventory
  `after/source-class-inventory-final.txt`. At d0772ce8: G19 :169, G20 :177,
  `h3_ok` :565, `declared` :567, `UNREADABLE (could-not-evaluate)` print :597,
  `DECLARED FAIL CLASSES` :596→:603, usage :199, identity line :95.
- Landing reproducibility: reconstructed the target from HEAD's blob +
  EX-16's `receipts/after/landing-diff.patch` → byte-exact digest
  (`/var/tmp/rv8-kai/recon/r82.py`, then df9ffdf9; EX-16 re-cut the receipt as
  the target moved, and each reconstruction matched).
- Residual inventory: round-1 c3 verdict H1-H6 (`before/residuals-inventory.txt`);
  H7 = EX-23's round-2 discovery (`receipts/draft/draft_v11_h7.py`).
- Review harness `header-class-audit.py` (G-labels / dispositions / exit codes /
  H-residuals / sha utterances → resolved against source + inventory). Controls:
  known-good 0 UNKNOWN exit 0 (`before/audit-control.out`); synthetic G19/H9
  3 UNKNOWN exit 1 (`before/audit-negcontrol.out`) — non-vacuous.
- Harness on EX-23's text: **44 rows OK, 0 UNKNOWN, exit 0** — receipts at four
  digests: `after/audit-ex23-patchmd.out` (82fb807e-era source… run against
  df9ffdf9), `-final.out` (a4c16763), `-d0772ce8.out` (close digest).
- EX-23 rebuild identity: re-ran EX-23's `build.py` with paths remapped →
  `draft_v11.py` sha `2ee0a1c9…` == shipped copy (byte-reproducible).
- EX-23's frozen copy of its named digest
  (`/var/tmp/ex23/live-frozen-82fb807e.py`, sha verified) — used to check its
  hunk anchor citations exactly.

## 2. Proposed changes (patch-text paths or "none")

- `claims/c2/RV-8/proposed-dedupe-stanza.patch.md` — dedupe for a landing
  defect found in every late digest (identical paragraph at :82-84 and :85-87,
  not EX-23's). EX-16 owns the write; this seat wrote nothing outside its
  report + `claims/c2/RV-8/`.
- Otherwise none. EX-23's own hunks A-D: B/C are substantively landed by
  EX-16 (see §3), A and D are not (see §3/§6).

## 3. Review verdict — EX-23's header text vs the landed code

**VERDICT: ACCURATE on every class and residual it names, pinned to the digest
it cites (`82fb807e…`); three content defects + one revision-drift issue; all
four hunk anchor citations verified exact against that digest.**

| # | EX-23 claim | Resolution | Receipt |
|---|---|---|---|
| 1 | classes `UNREADABLE (could-not-evaluate)`, `BLIND-INSTRUMENT`; G19/G20 exist | EXIST (d0772ce8: declared :567, prints :597/:603, G19 :169, G20 :177; at 82fb807e :519/:548/:156/:164) | `after/audit-ex23-patchmd-d0772ce8.out` (44 OK, 0 UNKNOWN) |
| 2 | residuals H2/H4/H5/H6 named | EXIST (round-1 inventory items 5-9; landed stanza :82-84 names H2/t5/H4) | `before/residuals-inventory.txt` |
| 3 | H7 closed by the rows-beyond-EOF leg | CONFIRMED, my run at the close digest: 0-line SKILL.md → `UNREADABLE ['SKILL.md: 0 lines < declared max 20 (rows beyond EOF)']`, FAIL exit 1 | `after/landed-runs/h7-zero-line.out`; EX-23 `C-zerobyte.txt` |
| 4 | hunk anchors A :47-48, B :84, C :174, D :74 | EXACT at 82fb807e (frozen-copy grep; D single occurrence there) | `/var/tmp/ex23/live-frozen-82fb807e.py` |
| 5 | §2 BLIND-INSTRUMENT trigger "current-ok loci < 1 (tree level)" | STALE for the landed form: floor is **per readable file** (`h3_ok = all(floor[f]>0 …)` :565; print "current-ok loci per file: PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3; total loci=17; floor=1/file") | `after/landed-runs/d0772ce8-ordinary.out` |
| 6 | §3 "current-ok 5 blocks, total loci 17" | revision-specific; late digests report per-file assertion counts, total 17. EX-23's own §6.2 guard clause ("receipts name 82fb807e and are void for other digests") correctly bounds this | `ordinary-full.out` vs `d0772ce8-ordinary.out` |
| 7 | §4 row D before-cell "PASS would be silent (rows 636-855 beyond EOF)" | **REFUTED**: v10 on SCORECARD truncated to 500 lines reads FAIL exit 1 with 7 marker-beyond-EOF SCOPE-ERRORs — loud, not silent (also false for EX-23's own draft) | `after/landed-runs/v10-scorecard-truncated500.out` |
| 8 | §5.6 "header-only draft output byte-identical to v10 output; receipts diff empty" | claim **TRUE** (my independent rebuild: header-only output == v10 output, only my appended `exit=0` line differs) but the **cited pair is wrong**: `before/ordinary-pass.txt` vs `draft/after-ordinary.txt` differ (3 inserted + 1 replaced line) — that file is the full-draft run, not the header-only run | `after/landed-runs/ex23-hdronly-ordinary.out`, `after/ex23-cited-pair-diff.out` |
| 9 | §2 trigger parenthetical "(absent, zero-byte, truncated, directory, EACCES)" under "raises OSError" | MISLEADING: zero-byte/truncated open fine and trip the `len(lines) < max_end` leg (message "0 lines < declared max 20"), never FileNotFoundError. The OR-clause keeps the cell complete; the parenthetical misplaces two classes | `h7-zero-line.out`, EX-23 `C-zerobyte.txt` |

Landed-code state vs EX-23's hunks (all measured at d0772ce8):

- **Hunk B/C substantively landed by EX-16** (different wording): the second
  docstring no longer says "instrument v9 … FINAL" — it reads `C1 census
  instrument v10-r9 (arc3-loop1-round2: H1+H3 fail-closures; …)` at :95-97,
  and the usage line now names `c1-census-v10.py` at :199. The string "v11"
  appears nowhere in the file; the landed revision id convention is
  **"v10-r9"**, not EX-23's proposed "v11". EX-23's §6.1 anticipated the
  choice ("or land one revision id and record the reconciliation"), so this is
  a convention difference, not an error.
- **Hunk A not landed**: the v11↔r9 reconciliation sentence is absent; with
  the "v10-r9" convention now landed, applying Hunk A verbatim would conflict.
- **Hunk D not landed**: the landed ledger still names only H2/t5/H4; the H5
  boundary, H6 rationale, and the H7-closed record are missing from the target
  (EX-23's proposed additions remain valid content).
- **Duplicate paragraph (landed defect, not EX-23's)**: "Still named, NOT
  closed here" appears verbatim twice at :82-84 and :85-87 in df9ffdf9,
  a4c16763 and d0772ce8 (diff identical, `grep -c` = 2) —
  `proposed-dedupe-stanza.patch.md`. EX-23's Hunk D rewrites ONE copy; applied
  naively to the late digests it leaves a duplicate.

## 4. Before→after measurement (chain C2 claim, at my own hand)

Before (v10 `6f1d19ff`, scratch copies; `before/`):

```
H1 (SKILL.md absent):   PASS exit 0, SKILL.md lines=0 loci=0, G2 ok   [atk-h1-absent-skill.out]
H3 (needles neutered):  PASS exit 0, all files loci=0, G2 ok          [atk-h3-blind.out]
ordinary at repo root:  PASS 0/0/0/0, counts 6/9/2
```

After (close digest `d0772ce8`; identical verdicts at df9ffdf9; this seat's
runs in `after/landed-runs/`):

```
ordinary at repo root:  PASS 0/0/0/0 exit 0; UNREADABLE []; DECLARED []   [d0772ce8-ordinary.out]
H1 (SKILL.md absent):   FAIL exit 1, DECLARED FAIL CLASSES ['UNREADABLE'] [d0772ce8-h1.out]
H3 (blind-all):         FAIL exit 1, DECLARED ['BLIND-INSTRUMENT']        [d0772ce8-h3.out]
H7 (0-line SKILL.md):   FAIL exit 1, UNREADABLE ['... 0 lines < declared max 20 ...'] [h7-zero-line.out]
PIN alone neutered:     PASS exit 0 (partial-blinding residual live)      [final-pin-neut.out]
anchor config missing:  ANCHOR-FAIL exit 2 (HOME=/nonexistent)
SCOPE block HEAD→landed: byte-identical (24-line literal, diff empty)
```

Interim target states (EX-23 receipt trail, cited not re-measured): 9373964c
raised `TypeError: %d format … NoneType` on the H1 injection
(`X-midwrite-9373964c-typeerror.txt`); 076bd621/c95a5cf3 FAILed at HEAD until
the floor was fixed to per-file assertion counts (final PASSes).

## 5. Attacks/refutations attempted (verdicts)

| # | Attack | Verdict | Receipt |
|---|---|---|---|
| A1 | v10 silent-PASS on absent scoped file (H1) | CONFIRMED live | `before/atk-h1-absent-skill.out` |
| A2 | v10 silent-PASS with needles neutered (H3) | CONFIRMED live | `before/atk-h3-blind.out` |
| A3 | review harness vacuous (passes anything)? | REFUTED (negative control: 3 UNKNOWN, exit 1) | `before/audit-negcontrol.out` |
| A4 | harness false-positive on known-good control | found (`exit 1` matcher; git-rev/digest conflation) and fixed; clean after | `before/audit-control.out` |
| A5 | EX-23 §5.6 "header hunks inert" | claim VERIFIED by independent rebuild; citation artifact mismatched (§3 #8) | `ex23-hdronly-ordinary.out` |
| A6 | EX-23 §4 row D before-cell | REFUTED (v10 loud FAIL, §3 #7) | `v10-scorecard-truncated500.out` |
| A7 | EX-23 hunk anchors wrong (suspected from a later-digest grep) | REFUTED for its named digest: exact at 82fb807e; drift is the target's movement | frozen-copy grep |
| A8 | duplicate "Still named" paragraph | CONFIRMED in df9ffdf9/a4c16763/d0772ce8 (identical, count 2) — landed defect | `proposed-dedupe-stanza.patch.md` |
| A9 | partial blindness (PIN alone) invisible to the floor | CONFIRMED live at the final digest (PASS exit 0) — consistent with the landed residual note | `final-pin-neut.out` |
| A10 | machine consumers of the changed output lines | none live in-repo; grep hits are wave records/prose only | consumer grep (`grep -rn`) |

## 6. Blockers

None for this review. Notes for the parent: (a) EX-23's text is accurate for
`82fb807e`; the target then evolved to `d0772ce8` (610 L, moving at my close) —
re-anchor hunks and reconcile §2/§3 for the per-file floor before any
application; (b) Hunk A/D content is still unlanded and the duplicate
paragraph persists — the dedupe patch text is offered for the target; (c) the
"v11" vs landed "v10-r9" naming difference is a convention choice EX-23's §6.1
already delegates. No custody path touched (the 5 paths were not even
hash-captured by this seat); no git mutation; scratch under `/var/tmp/rv8-kai`
(`/tmp` untouched); writes confined to `seats/RV-8.md` + `claims/c2/RV-8/`.
