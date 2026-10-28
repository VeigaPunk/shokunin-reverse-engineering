# Round-44 wave-2 integration notes (L1 KaidokuR44a2)

Findings that must land in the record (lesson / LOG / SCORECARD / report) before filing.

## From R44W2C2Freeze (F-1, F-2, F-3 …)
- C2's freeze check covers only the instrument's hard-coded set: `SCORECARD.md`, `SHONEN.md`,
  `SKILL.md`, `tools/round-44/c2-counter.py`, `tools/round-44/c2-rubric.json` + dir `tools/round-44`.
- Six claim-frozen families are NOT covered and score green under a post-freeze mutation:
  `plans/round-44-claims.md` (F-1, high), `corpus/SOURCES.md` (F-2, high; also internally
  contradictory in the claim at :312 vs :318), `tools/round-43/c1-counter.py` (F-3, medium),
  carrier bins, oracle trees, one round-40 receipt.
- The 80/80 at `55bcce69` is unaffected (`git log c48f8a4..55bcce69` over those paths is empty), but
  `frozen_path_changed []` does NOT certify the claim's freeze clause. State that limit in the C2
  verdict. → new routed defect R44-CL7.

## From R44W2Preflight (D-1, D-2, D-3, D-5, D-6)
- D-5 (must fix): the C1 red at `55bcce69` is NOT caused by provenance. `c1-score-at-55bcce69.json`
  has `failing: []` and exactly three falsy bindings — `province_core_section`, `province_core_row`,
  `frontier_note` — i.e. the Core row the round withdrew. The counter implements only the scratch
  clause (`provenance_ok()` requires an absolute path containing `/kaidoku-r44/`, no `..`); it never
  checks the amendment's committed-path clause, which is why the same receipts scored `met_target
  true, exit 0` at `4cc1ac11`. So: the score was WITHDRAWN under the claim text, not rejected by the
  counter. "No run can satisfy the whole frozen text" must be qualified: under the strict reading of
  the amendment clause the conjunction is unsatisfiable for a real scratch run; a substring-shaped
  scratch path (`…/kaidoku-r44/x/corpus/evidence/round-44/c1/v1le`) would satisfy both prose clauses
  and the counter — a loophole, not a legitimate route.
- D-6 (wording): `c86ea508` MODIFIED 8 files under `tools/round-44/`; it added none there.
- D-1: a frozen pathspec that matches nothing at FREEZE exits 0 clean (false green) — fix in the
  gate's next round (require every pathspec to match ≥1 path at FREEZE).
- D-2: the gate's `--pathspec` default (none) does not evaluate the blob backstop; documented
  behaviour should say so.
- D-3: the gate is a tool, not a wired gate; the demonstrated invocation covers one of round 44's
  eleven frozen pathspecs. Wire it into the commit sequence next round.

## From R44W2Misroot
- No kaidoku seat file misrooted at the fleet root. One scratch-discipline defect: a live empty
  `/tmp/kaidoku-r44` directory (no open fd, not cited anywhere) — remove after the wave settles.

## From R44W2Assim / R44W2Sources / R44W2ScoutTool / R44W2ScribeSeats
- Assimilation `none` confirmed (slice byte-identical, S150 refuse, S113 not adopted).
- S138/S139 rows: 11 cells, tier A, status mined, recheck 180d / on-release, used-by present;
  upstream re-open 10/10 listings HTTP 200 with body sha256 equal to the manifest; tag 4.7.5 live.
- Toolchain: all pre-existing; no pacman transaction; backhand not on PATH; scratch-only
  `backhand-cli` 0.25.5 + PySquashfsImage 0.9.0 in wave 1.
- Shape: 37 + 42 = 79 seats; attack share (policy set) 25/79 = 31.6%; w2 17/42 = 40.5%.
