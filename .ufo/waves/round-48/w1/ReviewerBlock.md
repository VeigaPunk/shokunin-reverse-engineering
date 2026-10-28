# ReviewerBlock — drafted block 25 vs the frozen R48-C1 predicate

Seat verdict: **the draft states every block-level clause the counter checks, with exactly one
measurable defect — a stale `interpreter_sha256` pin** — plus a prompt-level freeze
discrepancy that supersedes every `--freeze dc73587a…` receipt in this wave.

Reviewed artefacts (all read-only):
- Draft: `.ufo/waves/round-48/w1/C1Block/block.md` (10 lines, graft candidate).
- Frozen predicate: `plans/round-48-claims.md` `## R48-C1 — predicate (frozen)`, clauses 1–9.
- Counter: `tools/round-48/meanings.py` at HEAD `663f30ee` (735 lines; byte-identical worktree
  copy, `git status --porcelain` clean on all reviewed surfaces at capture time).
- Receipts for the commands below: `.ufo/waves/round-48/w1/ReviewerBlock/receipts.json`
  (exact command, exit, stdout sha256, UTC).

## Operative freeze (finding F1 — HIGH, prompt-level, not a draft defect)

The prompt declares `dc73587a8b9c1a23ba5a91dc7707ac7381a8b873` "after disclosed amendment
A1". The claims file is the rule: its amendment paragraphs re-declare the freeze as *the
commit that carries the paragraph* — A2 (`ac02a79f`), A3 (`f3a7afc4`), A4 (`0f06251bf`,
the commit named by `git log -1 -- plans/round-48-claims.md` at capture). Each amendment
touches frozen paths, so `gate.freeze_state(root, freeze=dc73587a, rev≥ac02a79)` computes
`history_touched(dc73587a..rev)` non-empty → `frozen_path_changed` → exit 2 for any
post-A2 revision. Consequences:

- Receipts in this wave taken with `--freeze dc73587a --rev dc73587a` (C1Pins, C1Refs,
  C1Struct-2, C2Floor) measure the **pre-amendment artefact**: the claims file at that rev
  contains no A2/A3/A4 paragraph and `meanings.py` is the A1 bytes. They are valid
  before-state controls only.
- Any receipt run with `--freeze dc73587a --rev <post-A2>` exits 2 (could-not-evaluate);
  C1Struct-2's `61b87d74` row already shows the ancestor direction of this.
- L1 must use the operative freeze (currently A4 `0f06251bf…`, **re-derive at landing —
  the freeze has moved four times in this wave**) when re-measuring at the landing
  revision. The predicate clauses 1–9, thresholds, kill rule and forgery list are
  byte-unchanged by A2–A4 (verified: `git diff dc73587a..HEAD` on the claims file touches
  only amendment/control paragraphs).

## Clause-by-clause coverage table

Reviewed under the operative (A4) counter; `score()` at `meanings.py:309`, v3 (`hard=True`).

| # | Frozen clause (claims file) | Counter check (symbol · line @HEAD) | Stated in draft? | Where / evidence |
|---|---|---|---|---|
| 1 | Marker occurs exactly once, marks exactly one craft block; block is last, title starts `25. ` | `marker_occurrences == 1`, `len(marked) == 1`, `blocks[-1] is block`, `block.startswith("25. ")` · :316–334 | Yes (positional) | Line 1 carries `<!-- verdict-meaning-table v1 -->` once; SKILL.md has 0 occurrences at HEAD (grep exit 1) so graft yields 1. `- **25. …` → post-split block text starts `25. `. **Unstated sub-clause:** "last craft block" is positional only — nothing in the text says it must be last; satisfied solely by graft position (craft section ends before `## Config custody` :643; graft after block 24 at :632). |
| 2 | Header exactly `trigger \| v1 hole \| v2 arm \| exit`; two data rows of 4 cells; exits ∈ {0,1,2} | `header == HEADER` (:44), `len(rows)==2`, `len(r)==4`, exit-cell check · :335–349 | Yes | Lines 3–6: exact header, `|---|---|---|---|` separator (skipped by `table()`), two 4-cell rows, exits `1`,`1`. |
| 3 | Each row names exactly one routed id; multiset = {R46-CL7, R47-CL10} once each; arm cell equals `EXPECTED_ARM` | `ID.findall(r[0])`, `counts`, `arm_by_id`, `EXPECTED_ARM` (:45–46) · :352–374 | Yes | Trigger cells `R46-CL7`/`R47-CL10`, exactly one id each (hole cells contain no `R4[67]-CL\d+`); arms `meaning`/`floor` keyed correctly — the R47-CL10 permutation hole is closed. |
| 4 | Every arm cell ∈ {`meaning`,`floor`} | `a not in VOCAB` (:47) · :385 | Yes | Arms are the bare tokens, no backticks needed (`strip("` ")`). |
| 5 | `mutations_sha256` = sha256 over each mutation's name+source body; all four names in block | `MUT_PIN` (:54), `MUT_DIGEST` (:130–141), `unnamed` names · :392–398 | Yes | `mutations_sha256:25ce025f…` — **verified**: executing the A4 bytes gives `MUT_DIGEST = 25ce025f8b2be63a5122583191cbf7588db7dc2894c869fac2ab075a84f5c1ea` (receipts.json). All four names `gold-meaning, swapped-meaning, duplicate-meaning, permuted-arm` present. C1Pins' `80010be3…` was an extraction artefact; `inspect.getsource` recomputation matches. |
| 6 | `interpreter_sha256` = sha256 of `meanings.py` at `--rev` | `SELF_PIN` (:55) vs `files(SELF)` · :408–416 | **Yes but STALE** | Pin `74b8da35…` = the A2 worktree bytes. HEAD/A4 bytes are `00f768c52a78f18a359c193cff08728a8dd8989e45121e7d496012d93d2649d0` (receipts.json). **Clause 6 will fail at landing unless L1 re-pins to the landing tip.** Correct value when drafted; the counter moved under it. |
| 7 | ≥5 resolving citations in `corpus/lessons/ \| corpus/knowledge/ \| plans/ \| tools/round-48/`, each with a line selector, incl. `corpus/lessons/round-47.md` + ≥1 `corpus/knowledge/` entry | `HARD_REF` (:53), `check_refs` (:261–), `MUST_CITE` (:49), `MUST_KNOW` (:50) · :399–407 | Yes | Six `HARD_REF` matches (SELF ref included in the `refs` count; 5 non-SELF): `corpus/lessons/round-47.md:30-50`, `round-46.md:57-66`, `corpus/knowledge/2026-10-25-r34b-…:40-66`, `plans/round-48-claims.md:20` and `:40`, plus `tools/round-48/meanings.py` (SELF → selector check skipped by design). All selectors in range at HEAD: 120, 102, 79, 201 lines respectively. MUST_CITE and MUST_KNOW satisfied. |
| 8 | Registry rows = census2.json path set exactly; committed census = fresh derivation; every verdict map splits into distinct success/not-met/unevaluable meanings | `registry_rows` (:183), `census_doc`/`census_rederive` (:296), `meaning_classes` (:231) · :425–455 | **N/A — not a block clause** | Checks `<!-- instrument-registry -->` rows + `census2.json`, not block text. Currently unmet at HEAD: 0 `tools/round-48/` registry rows vs 42 census paths — the L1 registry repair is a separate landing edit; the block's prose (line 8) states the rule but is **never itself classified** (gap G3). |
| 9 | Battery: `forgeries_total 4, v2_green 4, v3_green 0, genuine_green 1, crash 0` | `run_battery` (:491+), asserted · :461–466 | **N/A — measured, not stated** | Runs the four `MUTATIONS` on the grafted SKILL at `--rev`. Block supplies the names (clause 5); discrimination is verified only at landing. Block content gives `permuted-arm` exactly what it needs (2-row table). |

## "Stated but not checked" (over-statement audit)

- Row **v1 hole** cells (lines 5–6) are unchecked prose — nothing in `score()` reads them.
  Fidelity: `R46-CL7` text is faithful to `corpus/lessons/round-47.md`'s routed defect;
  `R47-CL10` ("rows naming the wrong arm can pass without proving the predicate") covers
  only the C1 side of that defect — the C2 completeness-floor side is unnamed in the row
  (acceptable: the row binds the arm, and the floor side is C2's claim surface).
- **Exit** cells `1`,`1` are unchecked content — the counter only bounds them to {0,1,2}.
- Title tail "a denominator is a floor" is thematic prose; no counter clause binds it.
- Line-8 verdict-map exemplar `0=met…;1=not met…;2=could-not-evaluate…` is never run
  through `meaning_classes` — a dishonest exemplar inside the block text itself would not
  be caught (G3 below).
- No clause is *mis*stated: every stated, checkable item (marker, title, header, rows,
  ids, arms, exits, both pins, names, refs) matches what `score()` enforces, modulo F2.

## Findings (severity order)

- **F1 (HIGH)** Operative freeze is A4 `0f06251bf…`, not the prompt's `dc73587a…`. All
  `--freeze dc73587a` receipts are pre-amendment controls; the landing re-measure must
  re-derive the freeze from the claims file at that time. (See above.)
- **F2 (HIGH, draft-blocking)** `interpreter_sha256:74b8da35…` pins the A2 bytes; HEAD is
  `00f768c5…` and has moved twice since the draft was written. L1 MUST re-pin at the
  landing tip or clause 6 fails. Exact re-pin command:
  `git -C <lane> show <landing-rev>:tools/round-48/meanings.py | sha256sum`.
- **F3 (MEDIUM)** "Last craft block" and "exactly once" are positional/global checks with
  no textual statement in the block — satisfied only by graft placement and SKILL-wide
  marker uniqueness (currently 0 occurrences; graft → 1). Not fixable by text; record as
  a landing-placement requirement.
- **F4 (LOW)** R47-CL10 hole cell is narrower than the routed defect (C1 side only).
- **G1 (LOW)** The block's own verdict-map exemplar is never meaning-classified — rule
  text and instrument rows can drift without a red. Bounded: clause 8 still binds the
  registry cells.
- **G2 (LOW, observed)** `check_refs` exempts SELF (`tools/round-48/meanings.py`) from the
  line-selector rule — deliberate (the sha pin supersedes it); the draft exploits this and
  it is legitimate.
- **G3 (INFO)** Nothing the block states is false; nothing the counter checks at block
  level is missing except the now-stale pin. Draft is landable after F2's re-pin, subject
  to the clause-8/9 surfaces owned by other seats.

## Verification gaps (not run — honest)

- No counter execution by this seat (`meanings.py` was executed only to obtain
  `MUT_DIGEST`, receipted). Battery, graft simulation, and registry-row checks are
  L1/other-seat work.
- `plans/round-48-claims.md` at HEAD is 201 lines (A4 paragraph appended); the 167-line
  figure cited from earlier peers is the A2 bytes — draft selectors `:20`,`:40` remain
  valid at both.
- Freeze may move again (A5+) before landing; F1/F2 must be re-derived at landing time.
  The worktree `meanings.py` changed sha twice inside this review window (74b8da35 →
  75fa4026 → 00f768c5 as A3/A4 landed); `git status` on the surface is clean now.
- `git grep -c verdict-meaning-table HEAD -- SKILL.md` exited 1 with empty stdout
  (= zero occurrences; receipted). A command typo `HEAD:census2.json` exited 128 —
  recorded, not evidence.

## Touched surfaces

Wrote only `.ufo/waves/round-48/w1/ReviewerBlock.md`, `…/ReviewerBlock/report.md`,
`…/ReviewerBlock/receipts.json`. Scratch `/fast/scratch/hyaku/kaidoku-r48/ReviewerBlock`
used for TMPDIR only; removed before yield. No installs (pacman paused; none needed).
No lane, frozen, sibling, or fleet file modified; no git mutation performed anywhere.
