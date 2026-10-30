# R51 / wave 1 / seat `ScribeReadme` — `corpus/README.md` bindings for R51-C1

**Verdict: the two README drafts are ready for the L1** (coverage-map row + dated frontier-note
edit), every shape gate I could run offline passes, and the promotion claim in both drafts is
explicitly **conditional** on the round-51 counter exiting 0 with `carriers_matched == 4`. Nothing
was written into the lane tree; no REA run was made; no git mutation was performed.

Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` · README read at lane HEAD
`39f41d4f15a87689a41c16c5c17ed885fbfb7da3` (sha256 `7ede85426c4baa5f205482375cf2966abfc21290b587d45ef6cdbdebf80786c4`,
300 lines) · base revision named by my dispatch `f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab`.

## Behaviour delivered

1. **Coverage-map row** (`coverage-map-row.md` §1) — 3 cells, inserted after the round-50 coverage
   row (L106): section `SquashFS LE AVM members (round 51)` | entries
   `` `2026-10-30-r51-avm-le-squashfs-core` `` | state = **Core** with the device-accounting law
   named, the four carriers named, and the receipt pointers as placeholders
   (`corpus/evidence/round-51/c1/<id>/run.json`, `<id>` = `c6430`/`c6490`/`g7581`/`g7582`;
   `.ufo/waves/round-51/l1/scores/c1-{before,after}.json`). A *measured, not promoted* fallback row
   is supplied (§2) for the miss case.
2. **Companion Knowledge-index row** (`coverage-map-row.md` §3, optional) — 4 cells, after the
   round-50 Knowledge row (L228), with one `<S??? round-51 device-node source row(s)>` placeholder
   that **must** be replaced with the real SOURCES id(s) before landing.
3. **Frontier-note edit** (`frontier-note.md`) — §2a a new dated bullet as the last bullet of the
   `## Frontier` section (after L280), §2b a new dated paragraph after the round-50 note (L300, end
   of file). Both carry the mark `Round-51 frontier note`, the entry stem and an `LE AVM` token
   (searched with the stem removed, the way the frozen counters do), and both drop the
   `LE AVM members (`hsqs`)` clause from the still-frontier list while keeping every other
   still-frontier item. §2c supplies, but does **not** recommend, the in-place edits to the seven
   historical lines that name LE AVM as still-Frontier (L97, L106, L271, L272, L279, L280, L300) —
   the lane precedent is append-only dated notes (the round-49 bullet still lists v1/v2 as
   frontier after round 49 promoted it; `PROVINCE.md:448` says the older notes' LE-AVM clause is
   "unchanged by this round").

## Gates I ran (offline; no REA, no lane write, no git mutation)

`receipts/readme-patch-check.log` (script `receipts/patch_readme.py`, scratch-only):

| gate | result |
|---|---|
| `coverage_map_row` shape (counter `tools/round-50/c1-counter.py:2479-2482`) | True |
| coverage row cell count under `cells()` (`c1-counter.py:585-586`) | 3 / 3 |
| no `|` inside any cell | True |
| Knowledge row cell count | 4 / 4 |
| `map_token` (`c2-record.py:490-493`) match inside `## Coverage map` | True |
| B1 mapping simulation: 140 existing knowledge files | unmapped `[]` |
| B1 mapping simulation: 141 files (landing entry present) | unmapped `[]` |
| `unique_section` for `## Coverage map` / `## Knowledge` / `## Frontier` | 1 / 1 / 1 |
| last `## Frontier` bullet is the r51 one; its still-frontier list has no `LE AVM members (`hsqs`)` | True / True |
| frontier-note binding shape in the README (mark + stem + `LE AVM` token, stem removed) | 2 lines, True |
| pipes inside the two frontier lines | 0 / 0 |
| patch shape | 4 hunks, +4 / −0 (insertions only) |
| draft text == verified text | all 4 pasted lines byte-identical to the checked constants |

Not run: the round-51 counter (does not exist yet; its scoring needs the freeze and the data run),
the four-carrier data run, REA, the `PROVINCE.md` twin edit (another seat's surface).

## Findings the L1 should act on

1. **Base-revision conflict in the claims file (verbatim).** `plans/round-51-claims.md` opens
   "Base `1aa273694f4409d3432fbcd73e83a33bee0dd8e9` (lane `main` tip, pushed …)" and R51-C2's
   predicate names "the declared base `1aa27369…`" — but that commit is
   `round-50 verifier spot-check (integrator, hyaku)`, **two commits before** the claims draft
   itself (`f04b51dd round-51: claims draft …`), and my dispatch names `f04b51dd…` as the base
   while lane HEAD is now `39f41d4f round-51: wave-1 spec, dispatch, ready`. Measured:
   `git diff 1aa27369 39f41d4f -- SKILL.md tools/` is **empty** — only
   `plans/round-51-claims.md` (+216 lines) differs. So the C2 before-arm is byte-invariant between
   the declared base and HEAD **for `SKILL.md`/`tools/`**, but the census rule reads claim files:
   `tools/round-48/census2.py:29` hardcodes `CLAIMS = [f"plans/round-{n}-claims.md" for n in
   range(41, 49)]`. If `census3.json`'s re-derive extends that range to round 51, the census at the
   declared base (no `plans/round-51-claims.md` there) differs from the census at the freeze — the
   C2 seat/L1 must pin the claims range of the census3 rule so the "before" arm's
   `census_outside 13` is re-derivable at the declared base. [INFERENCE on the consequence; the
   diff and the constant are measured.]
2. **Coverage count.** `corpus/knowledge/` holds **140** `.md` files today, so the new entry is the
   **141st** — matching the claims' "141/141" plan and the `SCORECARD.md` coverage row, which must
   read `141/141 knowledge files mapped` at the landing (`c2-record.py` atom B1 derives the number
   from `git ls-tree -r --name-only <rev> corpus/knowledge`).
3. **Observation, another seat's write into the lane tree.** At the end of my wave the lane working
   tree carries an untracked `tools/round-51/c1-run.sh` (46 142 B, mtime 2026-10-30 01:58), i.e. a
   wave-1 draft placed **in the lane's `tools/`** rather than under
   `.ufo/waves/round-51/w1/<seat>/`. The wave contract says drafts go under the seat directory and
   never into the lane's `tools/`; I did not touch the file (read-only listing only). If it is a
   sibling seat's port draft, it should be moved into that seat's directory before the freeze
   commit, so the freeze is the single commit that adds the round-51 instruments.
4. **Seven LE-AVM frontier mentions** in the README (L97, L106, L271, L272, L279, L280, L300).
   The two new lines supersede the current statements (L280 bullet, L300 note); the five older ones
   stay as dated history. If the L1 prefers in-place removal, §2c gives every old→new string
   pair — but that rewrites dated history, against the lane's own precedent.

## Touched surfaces (mine) and out of scope

* Written (all under my seat dir): `.ufo/waves/round-51/w1/ScribeReadme.md` (this report),
  `.ufo/waves/round-51/w1/ScribeReadme/coverage-map-row.md`,
  `.ufo/waves/round-51/w1/ScribeReadme/frontier-note.md`,
  `.ufo/waves/round-51/w1/ScribeReadme/receipts/{readme-patch-check.log,README.patched.md,readme-r51.patch,patch_readme.py}`.
* **Not touched:** `corpus/`, `tools/`, `plans/`, `SKILL.md`, `PROVINCE.md`, `LOG.md`,
  `SCORECARD.md`, `SHONEN.md`, `corpus/SOURCES.md`, `corpus/evidence/`, the fleet repo, `.ufo/state/`.
  No commit/stage/stash/jj command; no `git` mutation of any kind; no REA/`rea-agents` invocation;
  no download; scratch `/fast/scratch/hyaku/kaidoku-r51/w1-ScribeReadme` removed after the receipts
  were copied. No tool was installed (no pacman/uv/npx install this wave).

## Artifacts

* `.ufo/waves/round-51/w1/ScribeReadme/coverage-map-row.md` — coverage-map row (3 cells) +
  fallback row + optional Knowledge-index row (4 cells).
* `.ufo/waves/round-51/w1/ScribeReadme/frontier-note.md` — old lines quoted verbatim (L97, L106,
  L271, L272, L279, L280, L300), the two replacements, the optional in-place table, the
  conditionality.
* `.ufo/waves/round-51/w1/ScribeReadme/receipts/readme-r51.patch` — the four insertions as a
  unified diff against the base README (apply or paste; both are equivalent).
* `.ufo/waves/round-51/w1/ScribeReadme/receipts/README.patched.md` — the patched copy (sha256
  `586121bf77960f57c0bd9e0ea9c4deb63e206241f8e38c56dea2dc34f8e39055`).
* `.ufo/waves/round-51/w1/ScribeReadme/receipts/readme-patch-check.log` — the gate log.
* `.ufo/waves/round-51/w1/ScribeReadme/receipts/patch_readme.py` — the re-runnable checker
  (scratch-only inputs; it reads the lane README and writes only into the scratch dir).
