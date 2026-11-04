# ScribeLesson — seat report (kaidoku round-71, wave w1, attempt 1)

Seat: ScribeLesson-11 (lesson scribe). Assignment: draft `corpus/lessons/round-71.md` under
`.ufo/waves/round-71/w1/ScribeLesson/` for the L1 to land; record the census start; seed the
Gate and Mistakes tables; invent nothing that depends on measurements not yet in the wave outputs.

## Behavior

What was produced, where:

- `round-71.md` — the lesson draft (this dir). Header (base/declaration/freeze, the three
  declared claims), the container A0 erratum note, the wave paragraph, the routed-defects map,
  `## Gate` seeded with S273 (declared admit candidate) and S274 (declared reject candidate)
  plus two extra placeholder rows, the spot-check placeholder, `## Mistakes` seeded with M71-1,
  M71-2 and M71-3, `## Outcome` with per-claim `<L1 fills>` placeholders, `## Census` with the
  recorded start and the end placeholder, and the closing draft VERDICT line.
- `report.md` — this report.
- `.ufo/waves/round-71/w1/ScribeLesson.md` — the seat summary at the path the Report trailer
  names (round-70 precedent: seat-level `.md` files at `w1/` are landed wave evidence).

## Gates exercised (read-only verification only; no claims executed)

1. **Input reads.** `corpus/lessons/round-70.md` (format precedent),
   `corpus/lessons/round-70-verifier-spotcheck.md` (routed defects),
   `plans/round-71-claims.md`, `.ufo/waves/round-71/claims.json`,
   `.ufo/waves/round-71/l1/census-start.txt`, `.ufo/waves/round-71/w1/ScoutSource/fetch-receipt.txt`.
2. **Commit identity (git read-only).** `git log`/`diff-tree`/`ls-tree` on the lane repo:
   - `329208cf4a234aac391b7f02b50769c5920f1beb` — "round-71 declaration: five instruments under
     tools/round-71 …, the claims plan, the census-start receipt"; `diff-tree` confirms exactly
     `tools/round-71/{controls,forged-receipts,packed-elf,registry-census,seam-probe}.py`,
     `plans/round-71-claims.md`, `.ufo/waves/round-71/l1/census-start.txt`. Matches the ticket.
   - `b827a8b5d54f2885ec9be7786389f356c59226ce` — "round-71 freeze: the claims container …";
     `git log --diff-filter=A -- .ufo/waves/round-71/claims.json` names it as the first commit
     adding the container. Matches the ticket and the plan's freeze mechanics.
   - `82c8e620…` — "round-70 verifier spot-check (integrator, hyaku)", parent `2b4d6167…`.
3. **Base-state grounding for M71-1.** `jq` over the committed
   `.ufo/waves/round-71/l1/pre/c3-at-base.json`: rows 88, paths 88, duplicates [],
   six nonconformant rows at SKILL.md lines 88–93 (tools/round-70/{packed-elf,mutation-check,
   contract-probe,seam-probe,forged-receipts,controls}.py), each defects `['pinned-empty']` —
   exactly the six round-70 rows the claims container's A4/A9 describe.

## Findings

1. **Container A0/declaration_pointer hash erratum (the seat's one substantive finding).**
   The frozen `claims.json` A0 says "declaration 46366cc5525f661b97d26a8c70ed3a53d0b4b916
   (the five tools, this plan, the census-start receipt)" and `declaration_pointer` repeats
   that hash with the same subject. Git shows `46366cc5` is the PRE-RECEIPTS commit
   (`l1/pre/{c1-at-base,c2-do-nothing,c3-at-base,controls-at-declaration}.json`,
   `l1/pre/nonce-commitment.txt`, `gen-claims.py`); the five tools + plan + census-start
   receipt live in `329208cf` — the ticket's declaration hash. The five instrument pins are
   content sha256s and unaffected; the freeze remains verifiable. The container is frozen
   bytes, so the draft carries the erratum in its header for the L1 to record append-only
   (round-70 routed-defect-5 pattern). No repair was attempted by this seat.
2. **Census start recorded**: 21 W04 duplicate-URL warnings (the 20 round-70 standing plus
   S272, which shares S260's URL across scopes), 179 rows, exit 0 — receipt
   `.ufo/waves/round-71/l1/census-start.txt` (committed at `329208cf`; the file prints the 21
   W04 lines and the registry ok line). End census left `<L1 fills>`.
3. **Gate seeds**: `ScoutSource/sources.md` was not yet written at draft time, so the S273/S274
   rows carry fetch metadata quoted from the scout's committed `fetch-receipt.txt` (GFM
   508 310 B, sha256 `b153d814…`, byte-identical to the S258 round-58 snapshot; tempfile
   75 198 B, sha256 `edf72176…`, byte-identical to the round-70 seat snapshot) and
   `<L1 fills>` quote/decision-confirmation cells. S274's reason cites the round-70 snapshot
   evidence (line 485 quote; zero `unique`/`distinct`/`collision`/`collide` matches) as
   committed precedent, attributed.
4. **Mistake seeds landed as specified**: M71-1 registry-row-shape (grounded in the committed
   base census receipt), M71-2 launcher-artifact (LC_CTYPE coercion; `PYTHONCOERCECLOCALE=0`
   plus the declared pop; grounded in the frozen instrument pin and container A2), M71-3 left
   as the wave's strongest-finding placeholder.

## Touched surfaces

- `.ufo/waves/round-71/w1/ScribeLesson/round-71.md` (new)
- `.ufo/waves/round-71/w1/ScribeLesson/report.md` (new)
- `.ufo/waves/round-71/w1/ScribeLesson.md` (new, seat summary)
- Nothing else; no product code, no frozen instruments, no `corpus/` files, no state files.

## Out of scope / limits

- No gate was executed; every outcome cell is an explicit `<L1 fills: …>` placeholder.
- `ScoutSource/sources.md` did not exist at draft time; the L1 fills the located quotes,
  word counts and final admit/reject confirmations from it.
- No tool was installed or upgraded (nothing needed); pacman untouched.
- Scratch root `/fast/scratch/hyaku/kaidoku-r71/ScribeLesson/` was created per bounds, used
  for nothing (no clones/fixtures needed) and removed before finish.
- All git commands were read-only (`rev-parse`, `log`, `diff-tree`, `ls-tree`); no mutating
  git/jj command anywhere; no commits, no pushes.

VERDICT: met — lesson draft, Gate/Mistakes seeds and census start delivered with grounded
evidence; the frozen container's A0/declaration_pointer names the pre-receipts commit
`46366cc5` as the declaration — the declaration commit is `329208cf`; erratum named for the
L1, instrument pins unaffected.
