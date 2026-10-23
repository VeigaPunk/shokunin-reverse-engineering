# FinalSummaryTruth — independent review of the 8 `## Capabilities` rows at bb0af56c

- Seat: `KaidokuR32A2.FinalSummaryTruth-2` (UFO-FSD reviewer, leaf, no delegation). Godspeed axes named up front: **(A1)** evidence-grounding of every summary row against its historical anchor demonstrations; **(A2)** falsification — row 17 must not repeat the false full mid-run pin-map claim (QUALITY 21 / R17-PINMAP); **(A3)** preservation — luna/arc rows and row 27 byte-unchanged; **(A4)** calibration honesty — four-item vs whole-repertoire limits stated without inflation.
- UTC: opened 2026-10-23T06:39Z window; close 2026-10-23T07:19:49Z.
- Target revision (measured, immutable): `bb0af56c29e7b4c11d0583ed6697d0e17aba9d26` — "round-32: bounded ARM64X native-view evidence, source gate and faithful repertoire repair" (committer date 2026-10-23 04:06:23 -0300 = 07:06:23Z). `SCORECARD.md` blob at this revision: `a41e6bca7a475bac1cae69648951dc8d33b1a218` (`git rev-parse bb0af56c…:SCORECARD.md`). Base for restoration comparison: `283aad7fe56d82f4ed4f8e43f099c2e1ceed5525`.
- Freezes touched only read-only: `claims.json` sha256 `8aa0672cf60d40b7afc53ebc4714e22c3e9f138d4af7ab0abc5039930878b435` (C1, `9a73680a`), `claims-v3.json` sha256 `a3be7e40df5a96cfa50df192adaef5b8f7b1c6e1470c560510f872185ec5171d` (C2v3, `f382e3b7`), counter `tools/round-32/c2-capability-calibration-v3.py` sha256 `5955e8ace76d93c7891a43ca282f129c8874cd1878a05c9f29e0b81d3cab2f9f`. No re-freeze, no relabel, no counter/predicate/route edit by this seat.
- Method: all reads via `git -C <abs> show/ls-tree/diff/grep` at pinned revisions; lane write limited to this report (dir `a2residual/` created, MKDIR_OK). Scratch: `/fast/scratch/hyaku/kaidoku-r32/a2residual/FinalSummaryTruth` (holds extracted `claims-v3.json` only). `df -h /fast`: 222G avail; no clone or build was needed. No REA/Ghidra/carrier run, no operational run, no tool installs (pacman paused; none needed). No owned process left running (only four short-lived `git show` pipelines, all completed).
- Read scope: `corpus/lessons/round-32.md`, the target diff/revision, round-17/18 spotcheck lessons, the four `a2audit/A2Capability{13,14,17,27}.md` reports, `a2audit/A2ReverseDomain.md`, and the anchors themselves. Held item U064N008Hf47eb933 not inspected.

## 1. Section census at bb0af56c (A1)

`## Capabilities` (SCORECARD.md:615) holds exactly **8 data rows** at :619–:626:

| line | row (first cell) | first-working round cell | status at bb0af56c |
|---|---|---|---|
| :619 | pre-registered two-lane live battery on REA 6.5.0 | luna-round-6 | pre-existing, preserved |
| :620 | version-symmetry battery on REA 6.4.0 | luna-round-8 | pre-existing, preserved |
| :621 | config custody pre/post-pair for live-probe rounds | arc2-loop1-round2 | pre-existing, preserved |
| :622 | contained user-service analyze of oversized PEs (analyzer-disable recipe) | arc2-loop1-round7 | pre-existing, preserved |
| :623 | cross-pin evidence-ID attribution for saved REA envelopes | round 27 | pre-existing, **unchanged** (reviewed) |
| :624 | curated source registry for existing REA frontier | arc3-loop1-round13 | **restored** (reviewed) |
| :625 | local raw-quote/heading regression audit | round-14 | **restored** (reviewed) |
| :626 | retained REA Ghidra-session log capture | round-17 | **restored** (reviewed) |

`git -C <lane> diff --stat 283aad7f bb0af56c -- SCORECARD.md` → `5 insertions(+), 0 deletions` (3 rows + explanatory paragraph + blank line). **Purely additive card-wide**: nothing else in SCORECARD.md was modified or removed, so preservation of :619–:623 and of all deeper append-only rows is proven by the zero-deletion diff, not by spot-check. Deeper restoration sources confirmed present at :2141 (r13), :2213 (r14), :2380 (r17) — base lines 2136/2208/2375 shifted +5 by the insertion, byte-identical content.

## 2. Restored row 13 — `corpus/SOURCES.md` + `corpus/lessons/round-13.md` (A1, OBSERVED)

- Anchor substance at bb0af56c: SOURCES.md registry rows S001–S0xx present (99 `| S0`-prefixed rows after later rounds' appends); S022 reasoned rejection verbatim: "REJECTED: its own page requires browser upload and states Electron 17–38 coverage" with explicit flip condition — the "reasoned rejection with evidence and flip" element of the row. Round-13 lesson gate line verbatim: "SOURCES rows: **0 → 22** … statuses mined=21/rejected=1 … exit 0. No older row was edited or superseded." — the census-before/after element.
- Row :624 description is the verbatim deeper-row cell (:2141); evidence cell copies the two counter-visible anchors and drops only the absolute census-command tail (not an anchor; cosmetic). Faithful copy. Matches `anchors_at_freeze["13"]` exactly.

## 3. Restored row 14 — quote-fidelity anchors (A1, OBSERVED)

- `.ufo/waves/round-14/verification.json` (dict, keys `revision`/`commands`) contains the recorded demonstrations verbatim: `"QUOTE_FIDELITY_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0"`, `"QUOTE_FIDELITY_VERDICT: clean mode=frozen manifests=7 findings=0 exit=0"`, plus red verdicts (`quote_not_contiguous`, `quote_location_mismatch` cases). All three anchor paths (`tools/quote-fidelity.py`, `fixtures/expected.json`, `verification.json`) resolve at bb0af56c.
- Independent re-execution by the A2Capability14 seat (scratch, base rev): selftest exit 0 28/28, frozen exit 0 7/7, s017-red exit 1 with `quote_not_contiguous ident=S017-Q1` — identical to committed records. Row :625 is the verbatim deeper-row copy (:2213) with the evidence cell compressed to the three anchors. Faithful. (No re-run by this seat; seat receipt accepted as report evidence per contract — this is my one seat-receipt-dependent element for r14.)

## 4. Restored row 17 — pinmap-claim falsification check (A2, OBSERVED — the decisive item)

**Row :626 does NOT repeat the false claim.** Its what-it-can-do cell ends: "Stored mid-run pin checks are verdicts, not full maps" — QUALITY 21's corrected framing. Verified chain:

- Historical defect: round-17-verifier-spotcheck R17-PINMAP — pass-2 mid-run `pin_checks` retained only `{taken_at_utc, equal, entries, changed, missing}`, not per-path maps, while `SCORECARD.md:2374` and the knowledge entry said "pre/mid/post pin maps with instants" / "each pin map is retained … All maps are equal".
- Discharge: round-18 appended the named correction — present at bb0af56c at SCORECARD.md:2444 ("mid-run instants retain the comparator verdict against the retained pre map, not the map; round-18 receipts retain each mid map with `map_sha256`") and `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:204-205` ("the mid maps themselves were discarded"). QUALITY #21 recorded in `corpus/lessons/round-18.md:23` ("retention claims name retained keys; verdict ≠ object").
- The false wording survives only in the **append-only deeper row :2380** — by design (append-only history is unedited; the round-18 spotcheck verified byte-prefix preservation plus appended correction). The new summary row :626 carries the corrected framing and additionally cites `corpus/lessons/round-17-verifier-spotcheck.md` as evidence, pointing readers at the defect record.
- The row also avoids the sibling trap R17-VALIDATE16: it makes **no receipt-count claim at all** ("all 16 receipts exit 0" was the historical overstatement); it cites `.ufo/waves/round-17/verification.json` without counts.
- Anchor substance exercised by this seat at bb0af56c: `verification.json` = 79 commands, `unexpected_exits: []`; labels `receipt-validate-{calib-shfmt,calib-esbuild-0.25.12,pro-notesmd-cli,pro-aether,pro-esbuild-0.21.5,pro-containerd-shim,pro-esbuild-0.27.7,pro-op}` plus `selftest-receipt-validate` — **9 entries, exits `[0,0,0,0,0,0,0,0,0]`** (8 receipts + 1 selftest; the A2Capability17 report's "×8" counts the receipts, consistent). Committed `runs/calib-shfmt/logs/rea-ghidra-kc2RG0/ghidra.log` re-hashed by this seat: `5179baf17be97553fbcd7596094abc67560a8e04c724d03637d91957994d8581` — equals the receipt binding hash recorded by the A2Capability17 seat; receipt `bound_sessions[0]=/tmp/kr17-rea-rexl9ss6/rea-ghidra-kc2RG0`, `binding{logfile_ok:true,target_ok:true}`. Evidence cell anchor `run-carriers.sh` resolves.

**Residual, disclosed**: a reader citing only the deeper row :2380 would still read the pre-correction pinmap sentence. That is the lane's standing append-only trade-off (correction lives at :2444/knowledge:204, and now also in the summary row); it is disclosed, not introduced by bb0af56c. No action taken — append-only records are out of my write scope and the lane convention forbids in-place edits.

## 5. Unchanged row 27 (A1+A3, OBSERVED)

- Byte-preserved: covered by the zero-deletion diff; `anchors_at_freeze["27"]={tools/round-27/xpin-attribute.mjs}` resolves, as do checker `c2-xpin-check.py`, seat report `BuildXpinTool.md`, and receipts dir `corpus/evidence/round-27/c2/` (4 TSVs; `r26-attribution.tsv` = 24 evidence rows).
- Committed receipts exist — note the precise paths are `.ufo/waves/round-27/after/c2-at-97358f75.txt` (exit 0: `r26_rows_ok=24/24 red_ok=3/3 capability_row=1 source_row=1 rev=97358f75`) and `.ufo/waves/round-27/before/c2-at-cd32264f.txt` (exit 1: `r26_rows_ok=0/24 … rev=cd32264f`) — red-before/green-after intact at bb0af56c. The A2Capability27 report cites these receipts once without the `.ufo/waves/round-27/` directory prefix (it elsewhere mirrors them correctly); cosmetic citation nit in the audit report, not in the landed row.
- A2Capability27 seat additionally re-derived the 24-envelope attribution byte-identical to `r26-attribution.tsv` under both installed pins' code, checker exit 0 at base. Standing disclosed limits (unchanged): attribution is a rule fit — no live 6.7.0 REA run exists anywhere; receipts hold no real 6.7.0 label (SCORECARD.md:3131 at bb0af56c).

## 6. Four-item vs whole-repertoire calibration limits (A4)

Stated limits, each grounded:

1. **Forward denominator is exactly 4**: the statement set is the 4 `capabilities_added` items of scalar-`lane:kaidoku` MANIFEST entries (rounds 13, 14, 17, 27 at fleet pin `cef00867`). A2ReverseDomain broadened the census to map-identified records (45 related) and still found exactly 4 items — no fifth capability is omitted; but the frozen `limits` text's "MANIFEST record covers hyaku-numbered rounds only" is too broad (the round-13 closure's campaign is `kaika`), as A2ReverseDomain notes. The four-item alignment is **not** whole-repertoire calibration.
2. **Reverse domain is not all closures**: `reverse_mismatch=0` covers scalar-lane closure numbers 12–31 only. 11 real map-identified arc3-loop1 closures (rounds 1–11) lack scalar `lane` and are excluded from `closed`; integer round identities collide across namespaces (scalar 12/13/14 exist both as old luna train records and later kaika/hyaku closures), so a namespace-blind reverse join is unsafe. A false-credit row in the luna/arc namespace could not trigger the reverse check. [INFERENCE from static code consequence, per A2ReverseDomain — no counter run by this seat.]
3. **The predicate is lexical, and its pass is not a mastery signal**: description check is a ≥5-shared-word overlap (a verbatim copy passes by construction — that copy *is* the claimed repair); evidence check is anchor-path presence/resolution, not demonstration. The lane's own control proves the ceiling: `.ufo/waves/round-32/controls/c2-negative/receipt.json` — fixture of four rows whose descriptions say "This capability was never demonstrated and cannot capture anything…" — scores `statements=4 match=4 target=4 reverse_mismatch=0`, exit 0, `met_target: true`, verdict "FALSIFIED: negative assessments satisfy frozen lexical predicate; honest stop, no counter change". The landed `## Capabilities` alignment (8 rows, 4 statements matched) therefore cannot support a calibration improvement claim; the honest stop stands, C2 is not re-frozen, re-scaled or relabelled.
4. **Preservation is not re-verification**: keeping the four luna/arc rows is append-only bookkeeping of already-recorded state, not fresh evidence for them; nothing at bb0af56c claims they were re-demonstrated.

## Findings by severity

- **Blocker: none.** No falsifying defect found in the landed rows or the restoration.
- **Minor (pre-existing, disclosed, no action):** deeper r17 row :2380 retains pre-correction pinmap wording ("carries pre/mid/post pin maps with instants"); correction lives at :2444 + knowledge:204 + now the summary row. Append-only convention; readers must not cite :2380 alone.
- **Minor (audit-report cosmetics, lane-side reports, no lane edit by me):** A2Capability27 receipt citation lacks the `.ufo/waves/round-27/{before,after}/` prefix (files verified present at bb0af56c); A2Capability17 "×8" omits the 9th `selftest-receipt-validate` entry (also exit 0). Neither affects any landed claim.
- **Confirms:** restoration is restorative, not acquisitive ("not three new acquisitions" — the paragraph's own wording, verified against the deeper rows); r17 summary row carries the QUALITY 21 distinction and no full-pin-map or 16-receipt claim; oldluna/arc rows and row 27 preserved byte-for-byte.

## Residual risk and verification gaps

- No new operational or reader runs were made (per assignment); all capability evidence is committed-byte re-verification at bb0af56c plus the four seats' scratch re-executions (r14 selftest/frozen/red, r17 log-hash binding, r27 byte-identical TSV + checker) — I accepted those seat receipts for the parts I did not re-execute, and re-executed the hash/exit checks marked OBSERVED above.
- Authenticity-not-forgery limits of r17 receipts and the lexical nature of the C2v3 counter are lane-disclosed limits and remain open by design (frozen).
- The 11 omitted map-identified closures and namespace collisions remain unfixed under the unchanged freeze (A2ReverseDomain's "smallest safe correction" = report, not repair — done here by citation).
- C1 (ARM64X coverage) was not in scope; its freeze bytes verified unchanged at bb0af56c.

## Trailer

- Report path: `.ufo/waves/round-32/a2residual/FinalSummaryTruth.md` (this file).
- Scratch: `/fast/scratch/hyaku/kaidoku-r32/a2residual/FinalSummaryTruth` (`claims-v3.json`, sha256 `a3be7e40…1d`; no claim in this report depends solely on scratch bytes — all decisive bytes are quoted above from lane revisions).
- No git/jj writes outside nothing; lane untouched except this report file and its new directory. No background processes remain.
- UTC close: 2026-10-23T07:19:49Z.
