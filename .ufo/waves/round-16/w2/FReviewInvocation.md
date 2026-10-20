# FReviewInvocation — r15 inventory argv vs retained receipt and the named append-only correction

Seat: `KaidokuR16.FReviewInvocation` (leaf). Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Scope: round-16 C1/C2 artifacts, route 1 only (invocation consistency: `recheck:` line 3 vs the exercised `-I` absolute argv). Read-only. No script, gate, selftest, control, fixture, build, test, lint, or formatter was executed. Digest and argv comparisons below are static reads of retained bytes, not re-runs of the instruments. No installs or updates.

## Verdict

- The **integrated route-1 correction is factually sound**: its quoted argv, exit claims, digest, source pointer, route anchor, and append-only shape all match the retained round-15 receipt. No defect found in the integrated correction's factual core.
- One **integrated calibration gap**: `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md:78` calls the line-3 spelling “intended guidance” without recording that it is unexercised. Route option (b) is met, but the residual variant is not named as an unexercised variant, which is what QUALITY #18's second branch asks for.
- Four **w1-artifact errata** (two material, two low): a false claim that the retained stderr is truncated before the exception type, and a false baseline claim about the red control's argv conjunct (plus two citation-range errors). Neither material error contaminated the integrated knowledge entry, but they must not propagate into the lesson/submission.
- Two **forward obligations** for L1: the C1 entry's cited `.ufo/waves/round-16/verification.json` does not yet exist, and the documentation-red after-state has not been retained. Two propagation/scope notes follow those obligations.

## Observed facts (static reads)

| Fact | Evidence | Result |
|---|---|---|
| Recorded argv | `.ufo/waves/round-15/verification.json:30-40` (`snapshot-inventory`) and `:47-57` (`inventory-determinism`) | `python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/snapshot-inventory.py --ghidra /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC --select 1.24.7 1.25.7 1.26.8`; both argv arrays identical |
| Correction argv | `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md:83` | Byte-equal to `' '.join(argv)`; static comparison `True` |
| Registry argv | `SKILL.md:487` (`go-snapshot-inventory`) | Same command inside backticks; static comparison `True`; now includes `-I`, absolute path, `--select` |
| Exit codes | `verification.json:41,58` | `0` and `0` |
| Output identity | `verification.json:159,180`; retained stdout fields; `inventory.json` bytes | `inventory_equal: true`; both stdout strings byte-identical, 235,523 B; SHA-256 `ad06fadc0166e172d65325e3366375e2d4a9730d714d154bbcd98137539bb2fe`; `inventory.json` file bytes equal the stdout and carry the same digest; `inventory_sha256` field matches |
| Probe identity | `.ufo/waves/round-15/snapshot-inventory.py` at `7ad23fe…` and current tree; `snapshot-inventory.py:321`; `measurement-pins.json:9` | SHA-256 `6a2a9b289ee456ea90bea8446e7d88ad7aa92035dcfaf5abab15a1b6e97cd55a` both; repaired `entries.sort` at line 321; pin matches |
| Append-only | `git diff 6235498b4112350eebce0812a74af1781fc0ee88 -- corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md` | 17 insertions, 0 deletions; baseline file is 74 lines; line 3 byte-unchanged |
| Baseline `-I` | `git show 6235498…:corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md` | No `python3 -I` occurrence (grep rc 1); no line 83 |
| Route anchor | `corpus/lessons/round-15-verifier-spotcheck.md:185` | Item 1 is wholly on line 185; line 186 is item 2 (supplemental baseline) |
| Lesson pointer | `corpus/lessons/round-16.md:54` | Exists; names the “named append-only r15 correction” and registry alignment |
| C1 recheck | `corpus/knowledge/2026-10-20-r16-go-selection-preview.md:3` | `python3 -I /abs/selection.py --root … --request 1.24.7 --goos linux --goarch amd64`; flags match `selection.py:291-296` (all required) |
| C1 receipt | `.ufo/waves/round-16/verification.json` | **Absent** at this read (glob found no `verification*.json` under the round-16 directory) |

## Defects in current round-16 artifacts

### D1 — Material (calibration/provenance): retained stderr does name the exception type

- Paths: `.ufo/waves/round-16/w1/CorrectionDraft.md:18`, `:40`, `:57`; `.ufo/waves/round-16/w1/CorrectionDraft.candidate.md:15`.
- Claims: “stderr truncated before the exception type”; “the retained stderr of the failed run does not name the exception type”; “the exception type (truncated in the record)”.
- Observed: `.ufo/waves/round-15/verification-initial.json`, commands `snapshot-inventory` (stderr at line 43) and `inventory-determinism` (stderr at line 60), exit 1, contain the complete tail `TypeError: '<' not supported between instances of 'dict' and 'dict'`, after the traceback at `scan_directory` line 322 in the failed-revision script. The retained field is complete; a truncated tool display would explain the w1 wording, but the record itself does not truncate it.
- Impact: the w1 report under-claims evidence it retained. The cause is more specific than “sort in `scan_directory`”: the sort key compared dicts. The integrated knowledge entry (`:58`) does not repeat the false limitation, so the corpus correction is unaffected; the w1 “Limits” and candidate must not be carried into the lesson or L1 report.
- Fix: replace the truncation sentence with the observed `TypeError`; keep the repair scope at line 321/322.
- Confidence: high (direct byte read of the retained field).

### D2 — Material (calibration): ReviewCriterion's red-control baseline claim is wrong, and “marker-only” cannot turn the control green

- Path: `.ufo/waves/round-16/w1/ReviewCriterion.md:23-24`.
- Claims: at baseline `6235498`, the argv conjunct is already true via `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md:83` (the “Executed inventory” argv); only the literal marker is missing; “a marker-only append would turn the control green”.
- Observed: the baseline entry at `6235498` is 74 lines, contains no `python3 -I` (grep rc 1), and has no line 83. The integrated append is 17 insertions, 0 deletions. `documentation-red.json` requires **both** `'Round-16 correction' in kn` **and** the absolute argv substring; a marker-only append cannot satisfy the argv conjunct. The after-state becomes green because the integrated correction contains the marker and the argv; it also contains a distinction, but the control does not test that distinction.
- Impact: F1's conclusion (presence-only control; it never reads line 3) stands, but its cited evidence and counterexample are wrong. The correct counterexample is a **marker + argv** append with no substantive distinction: that is the shape that would go green while line 3 remains divergent. The integrated correction also contains the “not a claim of equivalence” distinction, so its green is substantively defensible under route option (b); the control itself cannot distinguish the two shapes. Do not cite the control as proof of the distinction.
- Fix: correct the baseline anchor; restate the counterexample as marker+argv; keep the recommendation to require line 3 or an explicit distinction label.
- Confidence: high (baseline bytes, diff, and control expression read directly).

### D3 — Low (citation scope): route 1 span `:185-186` includes route 2

- Paths: `.ufo/waves/round-16/w1/CorrectionDraft.md:20`, `:51`; `.ufo/waves/round-16/w1/CorrectionDraft.candidate.md:3`.
- Claim: routed defect 1 at `corpus/lessons/round-15-verifier-spotcheck.md:185-186`.
- Observed: line 185 is item 1 (invocation consistency); line 186 is item 2 (supplemental baseline discoverability). The integrated correction correctly cites `:185`.
- Impact: a reader checking the span sees two different routes attributed to route 1. No effect on the integrated text.
- Fix: use `:185`; the integrated correction already does.
- Confidence: high.

### D4 — Low (anchor precision): probe line ranges

- Paths: `.ufo/waves/round-16/w1/CorrectionDraft.md:21`; `.ufo/waves/round-16/w1/CorrectionDraft.candidate.md:23`.
- Claims: argparse `snapshot-inventory.py:406-417`; stdlib imports `:55-61`.
- Observed: `ArgumentParser` starts at line 404; `add_argument` calls at 406 and 411; the block ends at 418 (`args = parser.parse_args(argv)`). Imports are lines 55-62; `sys` is line 62, outside `:55-61`. The substantive claims (“stdlib-only”; “`-I` is an interpreter flag, not in the probe's argparse”) remain true.
- Impact: citation precision only; no claim failure.
- Fix: `403-418` for the parser block and `55-62` for the imports if the ranges are retained.
- Confidence: high.

## Integrated calibration gap

### C1 — “intended guidance” is an unlabeled intent inference; #18's “unexercised variant” branch is not stated

- Paths: `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md:78-80`; `corpus/QUALITY.md:28` (#18); `corpus/lessons/round-16.md:54`.
- Observed: the correction says “The original `recheck:` at line 3 is intended guidance, not the exact retained argv.” The retained evidence supports “not the exact retained argv”; it does not record authorial intent. A targeted search of `corpus/`, `LOG.md`, `SKILL.md`, and the round-15/round-16 wave records did not find the line-3 spelling in any retained execution record; it appears only in the entry and the w1 drafts. The integrated text does not state that observed fact. The w1 candidate had the more precise “No retained record executes this exact string” and “Source-only preview”; those sentences were dropped at integration.
- Assessment: route option (b) explicitly asks to “explicitly distinguish intended recheck from recorded argv,” so the integrated wording is within the route. The correction's new instruction (“Use this exact argv”) satisfies QUALITY #18's first branch by matching the exercised flags and path. The residual `recheck:` line is the variant that #18's second branch would require naming as unexercised; the correction calls it “intended,” which is not the same as “unexercised,” and QUALITY #5 asks for observation/inference labels. This is a calibration refinement, not a route failure.
- Fix (append-only, no rewrite of line 3): add one observed sentence, e.g. “No retained execution record uses the line-3 spelling; it is an unexercised variant of the recorded argv.” Alternatively label “intended” as `[INFERENCE]` and add the record-absence fact. The correction's “not a claim of equivalence” sentence is already correctly calibrated and should remain.
- Confidence: high on the text; medium on whether L1 treats #18 as applying retroactively to this correction.

## Forward obligations / remaining unknowns for L1

1. **C1 receipt absent.** `corpus/knowledge/2026-10-20-r16-go-selection-preview.md:3` points to `.ufo/waves/round-16/verification.json`, which does not exist at this read. L1 must create it after the wave and run the `recheck:` argv exactly as written (`python3 -I /abs/selection.py --root … --request 1.24.7 --goos linux --goarch amd64`), retaining argv, revision, stdout/stderr, and exit. If L1 runs a different spelling (no `-I`, relative path, or missing `--goos`/`--goarch`), the new C1 entry repeats the r15 defect that route 1 just corrected.
2. **Documentation-red after-state.** `.ufo/waves/round-16/documentation-red.json` contains only the baseline run (exit 1, 0/4). The identical snippet must be run at the integration revision. Because the snippet reads via `git show`, the round-16 paths (`controls.py`, the correction, the SKILL row) must be present at that revision. The control is presence-only; it must not be cited as semantic proof of the correction (the lesson already labels marker evidence as bounded).
3. **Do not propagate D1/D2 into the lesson.** The integrated knowledge entry is clean on the stderr and red-control points; the false w1 sentences should be corrected in the w1 reports or explicitly marked superseded.
4. **Not audited here:** routes 2-4 (supplemental baseline, producing commands, SHONEN), C1 selection logic/fixtures, and the C2 controls beyond the route-1 checks. Other seats own those.

## Checked clean (no finding)

- Exact argv: correction line 83, `SKILL.md:487`, and `verification.json` argv join are byte-identical.
- Exit 0 twice; stdout byte-identical; stdout = `inventory.json` bytes; digest matches `verification.json:180` and the file.
- Probe bytes at `7ad23fe` equal the current tree (`6a2a9b…`); the repaired sort is at line 321; the measurement pin matches.
- Append-only: 17 insertions, 0 deletions; baseline 74 lines; line 3 unchanged.
- Route citation `:185` is exact; the lesson exists and its row 54 names the correction.
- Registry row `SKILL.md:487` now carries the exercised `-I` absolute argv with `--select`; the w1 ReviewCriterion F6 “same omission” statement is **stale/superseded**, not a current defect. Its F4 “round-16 lesson absent” is superseded by the current tree (`round-16.md` now exists). Its F10 is now a commit obligation, not a wording defect: the working tree `SHONEN.md` reads “historical 2026-10-15 operator-steered round 1” (diff against `6235498`), but the repair remains uncommitted until L1 integrates.

## Limits

- No instrument or gate was executed; therefore this report does not claim the probe reproduces `ad06fadc…` on a new run. It confirms only that the retained stdout and file are byte-identical and that the documented argv equals the recorded argv.
- No C1 selection or fixture behavior was evaluated; no C2 routes 2-4 were audited.
- Tool installs/updates: none.
