## CLAIM
Final wording for `corpus/README.md:131`: replace the flat "4 nits fixed" with the LOG.md:395-401 decomposition — 2 fixes applied at integration, 1 pre-land self-correction by the distill lane, 1 accepted. The exact replacement row is drafted below; it is the only received draft that also satisfies the wave census regex.

## METHOD
Read-only Git-object reads at HEAD cfc84c2 (`git show`): README :131 with neighbors, LOG.md:385-402, SCORECARD.md:92-123. Cross-read seats X1, P0, PB0, D4, V4, G4, R4, DB4, Y2, CB4 and receipts/census-pre.* (XB1: 7/7 DEBT, TOKENSET 72/72, MAP-ROWS, COMMAND_A 72/72 + 9/9, exit 1). Simulated the census README regexes on the drafted row in python. No probes, no network, no tracked-file writes.

## FINDINGS
- Current :131 ends `...verify-lane VERIFIED, 4 nits fixed`; that string occurs exactly once in the file (unambiguous target). LOG.md:389-390 first said "3 fixed at integration, 1 accepted"; LOG.md:395-401 corrects it: nit 1 (the r10-02 anchor) had been self-corrected by the distill lane before landing, so only 2 fixes applied at integration (r9-02 anchor range; heading scope), 1 accepted (authority enum).
- The V4.md:9 / D4.md:15-18 and DB4.md:8-9 drafts say "2 fixed at integration" and fail the census regex `(?:2|two).fixes.applied.at.integration` (verified in simulation) — the verb must be "applied".
- Final replacement row (tail-only change; 5 pipes / 4 cells before and after; row outside the coverage map, tokens untouched; simulation: all four positives pass, both negatives absent):

```text
| `lessons/round-13-distillation` | (SKILL.md `## Queue-drain craft` — not a corpus note) the 9-rule synthesis of rounds 5-12: content-addressed ids + 3 per-run exception classes, +0x100000 rule (exe + shared objects), refusal families × cost classes, four authority grades, input contracts (canonical bundles, homogeneous feeds), caller-attested attribution, acceptance≠correctness, census-defect class (6 instances), refuted provisioning hints | SKILL.md:81-195; verify-lane VERIFIED, 4 nits: 2 fixes applied at integration, 1 self-corrected by the distill lane before landing, 1 accepted | 2026-10-14 |
```

## THREATS
Textual only; no runtime replay. Census README PASS also requires item 4b (frontier :163 removal/restatement) — this wording flips subcheck 4a only. Wording is coupled to the census regex in receipts/census-pre.sh; if that acceptance script changes, re-verify.

## VERDICT
FINDING: earlier drafts fail the census "2 fixes applied at integration" regex; use the row text above.
