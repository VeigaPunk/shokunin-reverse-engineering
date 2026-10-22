# ReviewLesson — review of `corpus/lessons/round-29.md` at `18be864a528873b2b70d8c94e31f880290249e90`

Reviewed 2026-10-22T20:28Z, read-only on the lane (`git show`/`ls-tree`/`grep`/`diff`; no writes).
Scope: Mistakes table (class / evidence pointer / captured-by / fix shown able to fail with a
resolvable receipt), Gate table against QUALITY row 42 (quote = contiguous served bytes, ≤25 words),
Claims section against `.ufo/waves/round-29/claims.json`.

## Verdict: lesson holds. Every cell resolves; three minor findings, none blocking.

## Mistakes rows — row-by-row

### M29-1 (live seat at filing) — verified

- class: matches routed defect 1, `corpus/lessons/round-28-verifier-spotcheck.md:86` ("do not file
  while any seat is live") and the leftover record at `:24,:28` (` M .ufo/waves/round-28/a2w/
  ExecR27SelftestFix.md`, 19:26Z timestamps after the 19:25Z hard stop, commit `242b0d8b`, verified:
  `242b0d8b8ad6…` = round-28 tip). Observation.
- evidence pointer: spot-check `:86` plus the porcelain line — both resolve. The seat's file is
  committed as evidence at `7431096b` (ls-tree confirms `.ufo/waves/round-28/a2w/ExecR27SelftestFix.md`).
- captured-by: names the rule and that nothing enforced it. The rule's substance is attested
  (routed defect 1; also `w1/ScribeScorecard.md:71`); the *quoted wording* "cancel or settle every
  seat before filing" appears nowhere else in the lane (finding 3 below).
- fix shown able to fail: `tools/round-29/prefile-check.sh` exists at the tip (exits 1 on non-empty
  `git status --porcelain`, `GIT_OPTIONAL_LOCKS=0`, no git writes). Receipt
  `.ufo/waves/round-29/after/prefile-check-red-r28.txt` resolves: clean scratch clone at `242b0d8b`
  → exit 0, then with the seat's post-stop bytes → ` M …/ExecR27SelftestFix.md`, `prefile: NOT CLEAN
  (1 paths)`, exit 1. Both branches demonstrated. Observation.

### M29-2 (ledger vs gate disagreement) — verified

- class: receipt `.ufo/waves/round-29/after/ledger-before-fix.txt` shows
  `.ufo/waves/round-24/tools/freeze-gate.py --rev 7431096b… --disclosures corpus/claim-freezes.tsv`
  → `{"exact": 13, "mismatched": ["round-26", "round-28"], "missing": ["round-29"], …}`, exit 1.
- detail claims re-derived: at `7431096b` the round-26 ledger row said `INSTRUMENT_ABSENT` while the
  gate reports `INSTRUMENT_ABSENT,INSTRUMENT_REVISED` (per-round findings extracted from
  `after/freeze-gates-at-dbd87cfa.txt`); the round-28 row read `INSTRUMENT_UNRESOLVED,INSTRUMENT_UNPINNED`
  (unsorted) and now reads `INSTRUMENT_UNPINNED,INSTRUMENT_UNRESOLVED`. Both corrected rows carry a
  pointer note ("code set corrected in round 29 (M29-2)… `ledger-before-fix.txt`"; "codes re-sorted
  in round 29… M29-2"). Observation.
- captured-by: `--disclosures` exists in the gate at its supersession `9fb4eacd` (round-24), so it
  was available but unused at the round-26/28 filings — consistent with the cell's claim; "nobody
  ran it at filing" is not directly provable from the tree but is supported by the receipt itself.
  Inference.
- fix shown able to fail: same receipt, exit 1 pre-fix; green shown by
  `after/freeze-gates-v2.txt` (both gates `--disclosures` at `18be864a`, `exact:16/19`, exit 0).
  Receipt resolves. Observation.

### M29-3 (unpinned script named in freeze file) — verified, with one weakness

- class/evidence pointer: `claims.json` `primary_rule` text names `tools/round-28/c1-heldout-naming.py`
  ("unchanged from…", a textual reference, present in no `instruments`/`loaded_by_counter`/
  `producers_not_counters` map); the round-29 gate's own receipt
  `after/freeze-gates-at-dbd87cfa.txt` flags `INSTRUMENT_UNPINNED tools/round-28/c1-heldout-naming.py`,
  verdict FLAGGED for `.ufo/waves/round-29/claims.json` at freeze `dbd87cfa`. Observation.
- captured-by: "the freeze gate, but only after the freeze commit" — accurate: the gate can only
  evaluate `claims.json` once committed. Observation.
- fix: disclosed in both ledger rows (`claim-freezes.tsv` round-29: "named as the source of the
  unchanged rule text, not run by the counter and not pinned; M29-3"; `claim-freezes-v2.tsv`
  round-29 identical). Shown able to fail: the flag itself on this round's freeze. Receipt resolves.
- Weakness (finding 2): unlike M29-1/M29-2 the fix is a stated procedure ("a future freeze runs the
  gate on a scratch-clone commit of the candidate claims file before the real freeze") with no
  shipped instrument and no QUALITY row — nothing makes it run. It is a rule-that-nothing-checks,
  the same shape the mistake itself records.

## Gate table — QUALITY row 42 (row text read at `corpus/QUALITY.md:52`)

- Rule re-read: quote copied from contiguous served bytes, ≤25 words, line/section named;
  `composite` label when a rendered-HTML quote crosses tags; fails when the quote is not one
  contiguous run in the bytes whose sha256 the Gate names.
- Independently fetched all three files (2026-10-22, plain `curl`; bytes saved under
  `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ReviewLesson/src/`):
  - `handlers.ts` sha256 `30981efb…c5a38` — matches the Gate cell; the two fragments
    `signatureItem.filtered =` and `signatureItem.name !== expectedCanonical.signature;` are
    verbatim on lines 47–48 (newline + 12-space indent between them), inside `filterResponse`
    lines 39–66. ≤25 words. Compliant; identical format already used for S084 in the round-28
    lesson (precedent), and the "(two consecutive lines)" annotation makes the join explicit.
    Minor: the quote omits the second line's leading indentation, so it is a contiguous-fragments
    join rather than a raw byte-run paste — acceptable under the established convention, noted for
    completeness. Observation.
  - `canonical-signatures.json` sha256 `5572beb5…8b3e2` — matches; equals the S085 digest.
    Counted: 36 keys, 31 with a `signature` field — consistent with the Gate note's "31 kept
    signatures" and S085's "36 keys".
  - `erc-4626.md` sha256 `698c05bf…1e10a` — matches; the 16-word quote is verbatim at line 18,
    in `## Abstract` (`:14`). Minor: "method blocks `:54`–`:481`" is loose — `### Methods` starts
    at `:52`, the first `- name:` (asset) is `:54`, the last (`redeem`) starts `:481` but its block
    runs to ~`:497`, `### Events` at `:498`. The range names the method-heading lines, not the full
    span. Finding 4.
- "S087 and S088 are new rows. No existing row changed status, recheck or used-by": verified —
  `git diff bacbe9cc..18be864a corpus/SOURCES.md` shows only additions (S087, S088, one search-log
  bullet). L1's kept copies exist at `/fast/scratch/hyaku/kaidoku-r29/l1/src/` (same digests).
- Gate note: "6 of the 31 kept signatures do not hash to their key" resolves to
  `corpus/knowledge/2026-10-22-r29-openchain-filtered-unseen.md:25` under `## Rule` (heading `:13`,
  so "Rule" is accurate); the S087 teaches cell states scope ("with the same canonical list;
  not which revision is deployed…") and does not state the non-hashers — consistent with the note.

## Claims section vs claims.json

- R29-C1: targets `runs_ok 16/16`, `rows_complete 152/152`, `tally_equal 1`, `entry_ok 1`, exit 0 —
  identical to `claims.json` target. Observed `named 122, right 122, wrong 0` matches
  `after/c1-at-18be864a.txt` (which also reports `no_name 30`, omitted in the lesson — a triple is
  promised, so not a defect). "152 held-out selectors that appear nowhere in the lane at the base":
  `git grep -F -f <152 selectors> bacbe9cc` → 0 hits (literal, stronger than claims.json's
  "as a word"). Observation.
- R29-C2: targets match except the lesson omits `entries >= 1` from `claims.json`'s target
  (observed 252 ≥ 1, so inconsequential but incomplete — finding 1). Observed `252 entries,
  0 mismatches, 38 predicted true, 214 predicted false` matches `after/c2-at-18be864a.txt`
  (`responses_complete=178/178 … exit=0`). Observation.
- "Not claimed: calibration … six routed defects … SCORECARD round-29 section": matches
  `not_claimed` in `claims.json` and `SCORECARD.md:3184-3193` which lists exactly 6 hygiene items.
  Header claims (base `bacbe9cc`, freeze `dbd87cfa`, data `4fcea978`, measured `18be864a`) all
  verified against `git log`. Observation.

## Findings

1. [low] Lesson R29-C2 target list omits the frozen `entries >= 1` field from `claims.json:60`.
   Observed data satisfies it (252); completeness gap only.
2. [low] M29-3's fix is procedural text with no enforcing instrument or QUALITY row — the same
   "rule nothing checks" shape the Mistakes table exists to record. The red demonstration
   (the gate flag on round-29's own freeze) does resolve.
3. [low] M29-1 captured-by quotes "cancel or settle every seat before filing" as "the round
   contract"; that wording is in no lane file (grep: only this lesson). The routed defect's own
   wording is "do not file while any seat is live" (`round-28-verifier-spotcheck.md:86`). Substance
   verified, attribution unverifiable in-tree (likely the L1's session contract, not committed).
4. [info] S088 section cell "method blocks `:54`–`:481`" spans only the `- name:` heading lines;
   the last block (redeem) continues to ~`:497`. Locations resolve; range is imprecise.

## Missing receipts

None for the lesson's own claims: all three Mistakes fixes have resolvable receipts
(`prefile-check-red-r28.txt`, `ledger-before-fix.txt` + `freeze-gates-v2.txt`,
`freeze-gates-at-dbd87cfa.txt`), all Gate quotes verified against independently fetched bytes with
matching sha256, all observed claim values match `after/` receipts.

Residual risk (outside lesson scope, flagged): the round that minted QUALITY row 47's
"exits 0 immediately before the report commit … output is in the report" left no green
`prefile-check` receipt in the committed report at the tip (`after/` has only the red demo), and
the lane tree at measurement carries ` M SCORECARD.md` plus untracked wave-1 artifacts — in-flight
wave work, so a prefile run *now* would be red; the L1 must produce the green run at filing.

## Scratch artifacts (sha256)

- `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ReviewLesson/src/handlers.ts` — `30981efbc7bc1b541954eb75767c8154562f4f77a9bfc1ad22cf19c8996c5a38`
- `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ReviewLesson/src/canonical-signatures.json` — `5572beb596c9062be042b11be4a8cbd6a875be67a518dc0046b220433878b3e2`
- `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ReviewLesson/src/erc-4626.md` — `698c05bff73bfb796f59cd7c4732edccdf7e40176f9bb027c19a0bbe7251e10a`

Source records: URLs as in the Gate table; fetched 2026-10-22T~20:20Z with plain `curl -sSL`;
sha256 above; located quotes: handlers.ts:47-48 `signatureItem.filtered =` /
`signatureItem.name !== expectedCanonical.signature;`; erc-4626.md:18 `This standard is an
extension on the EIP-20 token that provides basic functionality for depositing`.

No tool installs were needed. No network requests to 4byte.directory or api.openchain.xyz; no REA.
