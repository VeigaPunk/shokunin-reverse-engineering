# ScorecardRows — R26-C2 replacement text for the SCORECARD owned-axes rows and the SHONEN no-cross-domain-bleed line

Seat: KaidokuR26.ScorecardRows (scribe, leaf). Lane: /home/vgpnk/Projects/shokunin/kaidoku-shokunin.
Claims frozen at `c27f445e70cedbaf5300b2fd0a53e821d9b659a9`; base `a0639d8e61e486e2a716ff94cddd89a73200a02c`.
Read-only on the lane: `git show` / `ls-tree` / `cat-file` / `rev-parse` only, plus sandbox clones under
`/fast/scratch/hyaku/kaidoku-r26/seats/ScorecardRows/`. No lane file edited, no REA call, no web source, no tool
installed. The lane's Git index changed during the seat (`f05c4271…` → `5a74c928…` → `89eaf230…`) from sibling
seats' own work; this seat ran no write, no `git add` and no commit in the lane.

## Verdict

**The replacement text needed for R26-C2 items K1–K6 is in the lane already, landed by the L1 at `46ebfd2f`, and it
passes all six items with zero mismatches.** The L1's row text differs from this seat's independent draft only in the
measured-revision choice (it cites the C1 commit `ebe2cb4a`, this seat's draft cited `c27f445e`); both satisfy the
frozen rules. This report gives (a) the exact landed lines, (b) this seat's independently drafted alternative, (c) the
observed value that makes each of K1–K6 pass, and (d) the verification runs.

The one substantive difference: the landed coverage row names the real C1 commit where the assignment asked for the
placeholder `<C1-COMMIT>`. That is the stronger form — the frozen K4 rule reads the revision following the word
"measured" and requires it to resolve, so a literal `<C1-COMMIT>` fails K4 (verified below: exit 1, K4 mismatch).
The landed `ebe2cb4aff1aea6f45e8bb5583662717ea61c0bb` is the C1 commit adding the round-26 knowledge entry and its
README map row; command A there gives 109/109.

## The exact new lines (landed at `46ebfd2f`, confirmed at lane HEAD `bd0c84bc`)

`SCORECARD.md` `## Owned axes`, lines 23–25 (coverage, depth, calibration, in that file order):

```
| coverage | 9.72 → 10.0 | 109/109 knowledge files mapped at `ebe2cb4aff1aea6f45e8bb5583662717ea61c0bb` (round 26, after the evidence-ID identity entry); index integrity only, **not** fraction of the REA domain held. History: 78/78 at `3395b6d` (luna-round-7; the row kept that revision until round 26), 107/107 at `7ef837a473ae65d924b9ea34e7748f722a6cd7d5`, 108/108 after the round-25 EVM selector-naming entry | `corpus/README.md` `## Coverage map`; command A; measured `ebe2cb4aff1aea6f45e8bb5583662717ea61c0bb`; baseline `a79945c4` | luna-round-1 + luna-round-7; count refreshed rounds 25 and 26 |
| depth | 10 → 10 | 17/17 queue-drain rule blocks have resolvable file/range citations at `ebe2cb4aff1aea6f45e8bb5583662717ea61c0bb` (round 26). History: 9/9 at `638fb211` (luna-round-3); rule blocks grew from 9 to 17 in eight commits from `58116aa1` to `4072ebb3` (2026-10-18 and 2026-10-19), and the row kept 9/9 until round 25 added a recount at `08c7a7299ed61c3fdc30ddb0adfe4e812d5eac76`. **not** semantic correctness, generality, or fresh execution — the r3 semantic contradiction removal is measured by the contradiction census, not this proxy | craft section `SKILL.md:81-314` (heading line 81, last non-blank line 314; the baseline range was `SKILL.md:77-191` at `a79945c4`); command A; measured `ebe2cb4aff1aea6f45e8bb5583662717ea61c0bb`; baseline `a79945c4` | r1 measurement + luna-round-3; rule blocks added 2026-10-18 and 2026-10-19; count refreshed rounds 25 and 26 |
| calibration | 0 → 10 | 9/9 preselected reconciliation obligations aligned (2026-10-15); 2026-10-16 per-client REA surface reconciled to live receipts — **failure-selected completeness**, not unbiased accuracy or mastery | Frozen `evidence/round-1-2026-10-15/rubric.json`; command B; count measured at `c265db9bd3c0883fbaf4487f839559c85a736826` (`result.json` `measured_revision`; the row said `75af886a` until round 26, which is the luna-round-2 receipt reconciliation, not command B's revision); luna-round-2 receipts `.ufo/waves/luna-round-2/receipts/` | operator-steered r1 + luna-round-2; later calibration claims are in the round sections (outside closures: round 24 rejected-honest-stop, round 25 admitted) |
```

`SHONEN.md` line 12 (the asserted line after the `- [~] No cross-domain bleed` box at line 11):

```
  asserted boundary only: `PROVINCE.md:95-116` (the `## Adjacent` refusal list; safety refusal at :114-116; range refreshed round 25 attempt 3, the earlier `88-116` began inside `## Frontier`); province versions are stated at `PROVINCE.md:8-14` (configured client pins `rea-agents@6.7.0`, 207/153; round carrier runs pin `rea-agents@6.5.0`); the 2026-10-15 6.5.0/207/v42 observations in `corpus/lessons/2026-10-15-round-1.md` are superseded there (clause refreshed round 26); no promotion or complete accuracy claimed.
```

The stale `contested` clause is gone; the replacement points at PROVINCE.md's own pin lines (`:8-11` surface summary,
`:12` round-carrier 6.5.0 pin, `:15-18` drift-prone per-client pins, `:24` installed shared skill v42) instead of
re-asserting a version alignment of its own.

## This seat's independent draft (alternative, also verified 0/6)

Produced before the L1's repair landed, from the assignment's own recipe (coverage row carries the `<C1-COMMIT>`
placeholder in the measured cell, as instructed). Same three rows and the same SHONEN line, differing only in which
revision is named and in wording. Full text: `candidate.txt` (sha256 `1c62763f1c0488a4d629ececd3004379fe0b440016f8aa49ac67fa92b469bbf4`).
Coverage names the C1 commit in the measured cell and keeps the 107/107, 108/108 and baseline 70/72 history clauses;
depth names `c27f445e` as measured revision and carries `SKILL.md:81-314` plus the superseded `SKILL.md:81-318` and
baseline `SKILL.md:77-191`; calibration names `c265db9b` (a prefix of `measured_revision`) with `75af886a` kept as the
luna-round-2 receipt commit; SHONEN pins `PROVINCE.md:8-11`, `:15-18`, `:24`, `:12` individually rather than the landed
`:8-14` span. Verified in sandbox clones at `sim-literal` and `sim-substituted`: 5/6 with the literal placeholder, 6/6 once
the real C1 hash is substituted.

## K1–K6: the observed value that makes each item pass

All values observed by running the frozen instrument `tools/round-26/c2-calibration.py` (seat CounterC2's build,
sha256 `3b0f6507e7f77fd1763fc26f2b68922bdb09f8e8f3f27149d0899a21b3a37e8e`) against Git objects, and independently by
command A run from the `## Measurement recipes` recipe A at the revisions cited.

| item | rule | observed value that makes it pass | evidence |
|---|---|---|---|
| K1 | depth row first N/M == command A `rule_blocks` == `citation_resolved_rules` at REV | **17/17** — command A at `46ebfd2f` and at `bd0c84bc`: `rule_blocks 17, citation_resolved_rules 17`; depth observable cell first N/M = `17/17` | observation |
| K2 | depth evidence cell contains `SKILL.md:H-L` for the craft span at REV | **`SKILL.md:81-314`** — heading `## Queue-drain craft` at line 81, next `## ` at 319, last non-blank line 314; the string is in the depth evidence cell | observation |
| K3 | first 7-40 hex revision after "measured" in the depth evidence cell resolves, and command A there gives `rule_blocks` == `citation_resolved_rules` == the K1 N | **`ebe2cb4aff1aea6f45e8bb5583662717ea61c0bb`** — resolves; command A there: `rule_blocks 17, citation_resolved_rules 17` == K1 N 17 | observation |
| K4 | coverage row first N/M == command A `mapped` == `knowledge_files` at REV, and the revision after "measured" gives the same N/M | **109/109** — command A at `46ebfd2f`/`bd0c84bc`: `mapped 109, knowledge_files 109, missing [], dangling []`; at `ebe2cb4a`: same `109/109` | observation |
| K5 | first 7-40 hex revision after "measured" in the calibration evidence cell is a prefix of `measured_revision` in `evidence/round-1-2026-10-15/result.json` at REV | **`c265db9bd3c0883fbaf4487f839559c85a736826`** — equals `measured_revision` at `bd0c84bc` exactly, so the prefix test holds; command B at that revision gives aligned 9/9 | observation |
| K6 | SHONEN line after the no-cross-domain-bleed box contains no "contested", and every `PROVINCE.md:A-B` / `PROVINCE.md:A` pointer is inside PROVINCE.md's line count at REV | box line 11, asserted line 12: **"contested" absent**; pointers `PROVINCE.md:95-116` and `PROVINCE.md:8-14`, both inside PROVINCE.md's **303 lines** at `bd0c84bc` | observation |

Instrument totals at the landed revisions: `items 6, mismatches 0, exit 0` at `46ebfd2f` (landed receipt
`corpus/evidence/round-26/after/c2-at-46ebfd2f.json`) and at lane HEAD `bd0c84bc` (re-run by this seat). Before count at
base `a0639d8e`: 5 mismatches of 6, exit 1 (landed receipt `corpus/evidence/round-26/before/c2-at-a0639d8e.json`).

## Producing commands (all exit 0 unless noted)

- Command A, recipe A extracted verbatim from `SCORECARD.md` `## Measurement recipes` at `c27f445e` into
  `commandA.py` (sha256 `236dde1da2d78b5ee2f4827fb884901857385fe1f40bbb09bbb4b4ab4f6e9b01`), run as
  `python3 -I -B commandA.py <REV>` inside the sandbox clone, 2026-10-22T12:49:01Z:
  - `c27f445e` → `knowledge_files 108, mapped 108, missing [], dangling [], rule_blocks 17, citation_resolved_rules 17`
  - `ebe2cb4a`, `46ebfd2f`, `bd0c84bc` → `knowledge_files 109, mapped 109, missing [], dangling [], rule_blocks 17`
  - `08c7a729` → 108/108, 17/17; `7ef837a4` → 107/107, 17/17; `3395b6d` → 78/78, 9/9
  - `638fb211` → 72/72, 9/9; `a79945c4` → 70/72 with both r14 files missing, 9/9; `c265db9b` → 70/72, 9/9
- Craft span, computed from `git show <REV>:SKILL.md`: `c27f445e` and `08c7a729` → `SKILL.md:81-314`;
  `a79945c4` → `SKILL.md:77-191`.
- Depth-row history check, command A at each of the eight rule-block commits named in the landed row: `58116aa1`→10,
  `265e1aa5`→11, `8cc81a84`→12, `ba06c4dd`→13, `28aa7a98`→14, `2fba56fe`→15, `9c1d1fef`→16, `4072ebb3`→17
  (rule_blocks and citation_resolved_rules equal at each).
- `result.json` `measured_revision` at `c27f445e` and at `bd0c84bc`: `c265db9bd3c0883fbaf4487f839559c85a736826`; at
  `75af886a` the same field already reads `c265db9b…`, confirming `75af886a` is not command B's revision.
- Command B at `75af886a` (from `SCORECARD.md` recipe B, jq on `git show` copies): after stage
  `{"revision":"c265db9bd3c0883fbaf4487f839559c85a736826","aligned":9,"total":9,"score":10}`, exit 0.
  `git ls-tree -r --name-only bd0c84bc -- .ufo/waves/luna-round-2/receipts`: 27 files present.
- Instrument re-run by this seat: `python3 -I -B <CounterC2>/c2-calibration.py --root <sandbox clone> --rev bd0c84bc`
  → `items 6, mismatches 0`, exit 0. This seat's own drafts applied to sandbox clones and re-measured: `sim-literal`
  → 5/6, exit 1, K4 mismatch ("no 7-40 hex revision after 'measured'", the literal `<C1-COMMIT>` is not a hex run);
  `sim-substituted` → 6/6, exit 0. The placeholder fails loudly rather than silently, so it cannot pass K4 by accident.

## Out of scope / not claimed

- This seat does not claim the R26-C1 evidence, the table, the entry or the SOURCES rows; it read the landed C1
  commit only to obtain the measured revision and the post-C1 command A counts.
- "0 mismatches" means six named statements agree with the observed state at the measured revision. It is not a claim
  that SCORECARD.md or SHONEN.md is calibrated in general. Sibling seat C2Cherrypick lists eleven further
  self-assessment statements outside K1–K6 that still disagree with repo state; those are round-report disclosures,
  not items.
- The SHONEN line asserts a boundary and a pointer, not province accuracy, and no promotion or completeness claim.
- No REA call was made by this seat; the REA 6.5.0 pin and carrier belong to R26-C1. No web source was opened; every
  fact above comes from lane Git objects or the local sandbox.

## Artifacts (`<seat>` = /fast/scratch/hyaku/kaidoku-r26/seats/ScorecardRows)

- `candidate.txt` sha256 `1c62763f1c0488a4d629ececd3004379fe0b440016f8aa49ac67fa92b469bbf4` — this seat's drafted rows and SHONEN line
- `landed_rows.txt` sha256 `d5ab20776baeb81996c7d25a20ef66265d6cad519a115106e77dc512739ece1b` — the four landed lines, byte-exact from `46ebfd2f`
- `commandA.py` sha256 `236dde1da2d78b5ee2f4827fb884901857385fe1f40bbb09bbb4b4ab4f6e9b01` — recipe A extracted verbatim from `SCORECARD.md` at `c27f445e`
- `evidence.py` sha256 `c31225d258bf0feae0a15b53e4952cf8199f9b9d2191575eef16ead28ed713ef` — evidence-capture script (command A, craft span, cell parse, pointer check, instrument runs)
- `evidence.json` sha256 `1443be95283e27dc8cdfccccd00bf1344e849d19701b46622c14933567526473` — the run record with per-step UTC time, exit code and stdout
- `verify_candidate.py` sha256 `d52219aa25da53d028076a810b461415d312469afd427940d3983af58061fb27` — applies the drafted rows to a sandbox clone, runs the frozen instrument
- `clone/`, `verify/`, `sim-literal/`, `sim-substituted/`, `sim-split/` — sandbox clones of the lane, none the lane itself

Tools installed or updated: none. Sources opened: none (local Git objects only). REA: not invoked.