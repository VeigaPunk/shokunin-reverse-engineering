# ScribeBlock30 — R90-C2 craft rule block 30 draft (scribe, round 90)

Seat: `ScribeBlock30` (scribe). Lane `kaidoku-shokunin`. Base revision `fc52cc9dc`. Lane HEAD `18b21f092`.
Scope: drafts block 30 for `SKILL.md` `## Queue-drain craft` in the seat dir and verifies it. R90-C1 is not touched by this seat.
Installs: none (python3 and git only; no pacman, no `uv`/`npm` installs).
Writes: this seat dir (`block-30.md`, `ScribeBlock30.md`, `receipts/`) and the trailer copy `.ufo/waves/round-90/w1/ScribeBlock30.md`. No tracked lane file touched; no mutating git in the lane; all clones and variants ran in a scratch clone of the lane, removed after the receipts were copied.

## 1. Drafted artifact

- Draft: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ScribeBlock30/block-30.md` — one bullet `- **30. …**` in the shape of blocks 28/29 (tag comment, prose, a 4-column decision table, indented `Refs:` line).
- Size: 766 words, 42 backticked spans (gate, `receipts/verify-block30.json` key `gate.candidate`). Shape floor is 25 words and 2 spans.
- Decision table: 10 data rows. Each row routes a revision defect class to its observed failure signature, the guard the revision must inherit, and the criterion. Rows: superseded class dropped (QUALITY 161); input guards and typed refusals dropped (169); isolation listing taken before the child runs (170, 163); carrier-blind scoring absent (168); exit code read as "the file is fixed" (167); bound implemented as a rank key and described as a filter (171); docstring states a rule the code does not apply (162); counter target written as prose (157); receipt taken from a moving tree (146); citation outside the base (159).
- Citations: only `corpus/QUALITY.md` rows (all present at base), `corpus/knowledge/2026-11-04-r89-binfo-field-value-class.md:59-61,65-69,95-98`, `corpus/knowledge/2026-11-04-r88-binfo-chain-geometry.md:38-45`, and `tools/round-89/depth-blocks-v2.py:41-52,105,182-184`. The block cites no round-90 path and no lesson.

## 2. Base-revision facts (checked, not assumed)

| claim | command | result |
|---|---|---|
| base is an ancestor of lane HEAD | `git -C <lane> merge-base --is-ancestor fc52cc9dc 18b21f092` | rc 0 |
| `corpus/lessons/round-89.md` is **absent** at base | `git cat-file -e fc52cc9dc:corpus/lessons/round-89.md` | rc 128, `path … exists on disk, but not in 'fc52cc9dc'` |
| …and present from the lesson commit `81cd0d73b` | `git cat-file -e 81cd0d73b:corpus/lessons/round-89.md` | rc 0 |
| QUALITY rows 146, 157, 159, 161–171 exist at base | `git show fc52cc9dc:corpus/QUALITY.md` and a `^- \*\*Row N \(` scan | all present; copy at `receipts/QUALITY-at-fc52cc9dc.md` |

Consequence: the round-89 lesson the task named is not a base-revision document, so a block that cites it fails QUALITY 159 at base. The draft cites the QUALITY rows that carry the same round-89 cases instead.

## 3. Counter results (frozen `tools/round-89/depth-blocks-v2.py`, read-only use)

All with `python3 -I -B <lane>/tools/round-89/depth-blocks-v2.py`; receipts in `receipts/`.

| arm | command (root / rev / expect) | output | rc |
|---|---|---|---|
| base, expect 29 | `--root <lane> --rev fc52cc9dc --expect-blocks 29` | `blocks 29 resolved 29 expect 29 unresolved 0 met=True exit=0` | 0 (`receipts/lane-root-base-expect29.json`) |
| base, expect 30 (no-work arm) | `--root <lane> --rev fc52cc9dc --expect-blocks 30` | `blocks 29 resolved 29 expect 30 unresolved 0 met=False exit=1` | 1 (`receipts/lane-root-base-expect30.json`) |
| HEAD, expect 29 | `--root <lane> --rev 18b21f092 --expect-blocks 29` | `blocks 29 resolved 29 expect 29 unresolved 0 met=True exit=0` | 0 (`receipts/lane-root-HEAD-expect29.json`) |
| candidate, expect 30 | scratch clone at `fc52cc9dc` + block 30 committed (`681650da23c5`), `--rev <cand> --expect-blocks 30` | `blocks 30 resolved 30 expect 30 unresolved 0 met=True exit=0` | 0 (`receipts/counter-cand-expect30.json`) |
| candidate, expect 29 | same, `--expect-blocks 29` | `blocks 30 resolved 30 expect 29 unresolved 0 met=False exit=1` | 1 (`receipts/counter-cand-expect29.json`) |
| counter selftest | `--selftest` | `SELFTEST cases=10 failures=0` | 0 (`receipts/counter-selftest.txt`) |

Candidate diff against base: `receipts/candidate-diff-stat.txt` reports `SKILL.md | 17 +++++++++++++++++`, 17 insertions and 0 deletions, a pure insertion between block 29 and `## Config custody`; full diff `receipts/candidate-skill.diff` (`grep -c "^-[^-]"` = 0). An earlier driver run dropped SKILL.md's final newline through a `.strip()` in the harness; that run's diff showed a spurious last-line change. It was fixed (`git show` is now read raw) and every arm was re-run; the verdicts were identical in both runs. Only the final run's receipts are kept.

Red worlds for the counter (scratch variants, each a committed clone state; `receipts/counter-red-*.json`):

| world | output | rc |
|---|---|---|
| block 30 replaced by a one-line citation stub | `blocks 30 resolved 29 expect 30 unresolved 1 met=False exit=1` | 1 |
| knowledge range out of bounds (`…r89-binfo-field-value-class.md:900-910`) | `blocks 30 resolved 29 expect 30 unresolved 1 met=False exit=1` | 1 |
| row cites `corpus/knowledge/2026-11-04-r90-missing.md:1-3` (absent) | `blocks 30 resolved 29 expect 30 unresolved 1 met=False exit=1` | 1 |

Negative probes the counter passes; the base-presence gate in §4 refuses each one. Recorded as gaps in the counter, not hidden:

| world | counter | gate |
|---|---|---|
| row cites `corpus/lessons/round-89.md` (absent at base) | `blocks 30 resolved 30 … met=True exit=0` | `missing_paths_at_base=['corpus/lessons/round-89.md']` → fail |
| row cites `tools/round-90/upx-break-repair.py` | `blocks 30 resolved 30 … met=True exit=0` | `missing_paths_at_base=['tools/round-90/upx-break-repair.py']` → fail |
| row cites `QUALITY 999` (no such row) | `blocks 30 resolved 30 … met=True exit=0` | `missing_quality_rows=[999]` → fail |

## 4. Base-presence gate (the check the counter does not perform)

Driver `receipts/verify_block30.py` (scratch clone; lane read-only). It extracts every `corpus/`, `tools/`, `plans/`, `.ufo/` path token from block 30 and runs `git cat-file -e fc52cc9dc:<path>`. It extracts every `QUALITY N` (and the `rows a-b` list in the Refs line), checks each against `^- **Row N (` in base QUALITY, and checks each knowledge `:a-b` against the base line count.

- Candidate: `base_presence_pass=True`, `missing_paths=[]`, `missing_quality_rows=[]`. Knowledge ranges `59-61`, `65-69`, `95-98` (file 126 lines) and `38-45` (file 99 lines) are all `in_range=True`. Results: `receipts/verify-block30.json`, `receipts/verify-summary.txt`, `receipts/driver-run.log`.
- Cited line contents at base are in `receipts/cited-ranges-at-base.txt`. Checked by eye: k89 59-61 holds the composed-class row (`recovered 4 of 4` beside the predecessor's `recovered 0 of 4`); k89 95-98 holds the exit-code remit; k88 38-45 holds the accounting bound and the docker-init `u_len` example behind QUALITY 171.
- `:105` and `:182-184` are `depth-blocks-v2.py` lines (the `met = …` assignment and the `--expect-blocks` required branch), confirmed with `git show fc52cc9dc:tools/round-89/depth-blocks-v2.py | sed -n '105p;182,184p'`.

## 5. Sibling draft observed in the lane worktree (read-only, not edited)

The lane worktree already holds an uncommitted block 30 (`git diff -- SKILL.md`: +16 lines, starting `- **30. A superseding instrument revision inherits the guard set …**`). Observations only:

- `--root <lane> --worktree --expect-blocks 30` → `blocks 30 resolved 30 expect 30 unresolved 0 met=True exit=0` (`receipts/counter-worktree-expect30-observed.json`). Worktree mode reads the moving tree, which QUALITY 146 says not to cite.
- Its four knowledge paths exist at base (`missing=[]`).
- Its QUALITY numbers cited are 157, 162, 163, 167, 168, 169, 170, 171. It does not cite QUALITY 146 (receipt re-take) or QUALITY 159 (separability), and its composition row names the class without a numbered `QUALITY 161` pointer.
- Its author and the L1's intent are not known to this seat. The L1 must choose between it and `block-30.md`; this seat did not modify it.

## 6. Routed findings (for the L1)

1. `corpus/lessons/round-89.md` is not a base-revision document (rc 128 at `fc52cc9dc`; present from `81cd0d73b`). Any block that cites it fails QUALITY 159 at base. The draft avoids it.
2. The frozen counter resolves only `corpus/knowledge/` paths and does not check `QUALITY N` numbers. Three of the four negative probes in §3 pass it. The separability (QUALITY 159) and criterion-pointer checks need a base-tree gate beside the counter. This seat's gate is one such check; it is not a change to the counter.
3. `SKILL.md` in the lane worktree is modified and uncommitted (the sibling block 30 in §5). `git status --porcelain` also lists untracked round-90 paths owned by other seats. This seat's candidate was built from `fc52cc9dc`, not from the worktree.
4. The plan's `Report:` trailer and the seat spec name two report paths. Both carry the same content.

## 7. Not done by this seat

- No R90-C1 work (repair, battery, tamper matrix, derivation). Those belong to other seats.
- No mutation or blinding attack on the counter beyond the red worlds and gap probes above.
- No commit, stage, push, or write to `LOG.md`, `SCORECARD.md`, `tools/round-89/`, `corpus/lessons/round-89.md`, `corpus/QUALITY.md`, or `.ufo/waves/round-89/`.

## 8. Receipts (absolute)

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ScribeBlock30/receipts/verify_block30.py`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ScribeBlock30/receipts/driver-run.log`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ScribeBlock30/receipts/verify-block30.json`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ScribeBlock30/receipts/verify-summary.txt`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ScribeBlock30/receipts/counter-*.json` (base, candidate, red, gap and worktree-observation arms) and `lane-root-*.json`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ScribeBlock30/receipts/counter-selftest.txt`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ScribeBlock30/receipts/candidate-skill.diff` and `candidate-diff-stat.txt`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ScribeBlock30/receipts/cited-ranges-at-base.txt`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ScribeBlock30/receipts/QUALITY-at-fc52cc9dc.md`
- Draft: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ScribeBlock30/block-30.md`
- Trailer copy: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ScribeBlock30.md`
