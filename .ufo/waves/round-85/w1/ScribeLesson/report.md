# ScribeLesson — round 85 lesson + routed corrections (draft; no commit)

Lane `kaidoku-shokunin`, round 85, seat ScribeLesson. Lane-tree bytes untouched; the only
production bytes written are under `.ufo/waves/round-85/w1/ScribeLesson/`. Git was read-only
(`show`, `log`, `cat-file`, `rev-parse`, `merge-base`, `grep`); no clone, no commit, no sandbox
git write was needed.

## What I wrote

- `candidate/corpus/lessons/round-85.md` — the round-85 lesson: title line, `## Gate`
  (S304 admit block + carried S303 rejection with its flip + `pending: non-author closure`),
  `## Mistakes` (one row, M85-1), `## Corrections (append-only)` with C-R2, C-R3, C-R4.
  The round-84 lesson and the round-84 spot-check are **not** rewritten.
- `sweep-red-before.txt` — the R3 pointer sweep over the r84 lesson's own wording at `91eeb72f`
  (RED: `MISSING l1/waves/round-84/w1/SentinelScope/esc-receipt.json`).
- `sweep-green-after.txt` — the corrected pointer's resolution (GREEN: both `.ufo/…` receipts
  `ok`, plus `git cat-file -e` at `91eeb72f`).
- `r2-r4-evidence.txt` — the grep and log outputs (E1–E14).

## Key numbers (all re-derived by the commands quoted in the receipts)

| item | value |
|---|---|
| rows containing `rea-agents-6.5.0.tgz` at `91eeb72f` | **8** (`grep -c -F`) |
| prior rows (excluding S303's own row) | **7** — S079, S080, S083, S090, S092, S119, S123 |
| the URL's table column in each of those rows | column 3 (source) |
| S303's stated count | "five scopes (S083/S090/S092/S119/S123)" — wrong |
| same count at `8ae9c8ee` / `b3084c8c` | 8 / 8 (present when the row was written) |
| R3 sweep, r84 wording | RED, 1 missing path |
| R3 sweep, corrected spelling | GREEN, 2/2 resolve |
| `git log -S 'met = all(arms)' 91eeb72f -- tools` | **no output** |
| committed revisions of `tools/round-84/nested-sqfs.py` carrying a per-run `met` in `score_envelope()` | **0 of 8**; the aggregate `"met": all(arms.values())` is at line 241 in `e0de2088`, line 248 at `91eeb72f` |
| committed mutant receipt for M84-4 | `.ufo/waves/round-84/l1/mistakes/m84-2-nested-met.json` (blob `3f25b629…`, sha256 `45e4bafa…`), added by `b15d8083` (ancestor of `91eeb72f`) |

## S304 gate facts used (supplied by ScribeSource, `w1/ScribeSource/report.md`)

DOI `https://doi.org/10.1016/bs.adcom.2018.03.015` → HTTP 200 → `linkinghub.elsevier.com/…`;
full text read from the archived ORBilu postprint (HTTP 200; ScienceDirect chapter page 403,
ORBilu handle TLS failure). Quote (24 words): "When a test distinguishes the behaviour of a mutant
(from that of the original program) we say that the mutant is 'killed' or 'detected'" — Section 2
"Background", postprint PDF p. 6. Decision: **admit, tier B, scope `mutation-testing survey`, id
S304**. Stated gap: the source is silent on name-matching, so the lane's declared-case binding is
the lane's own tightening and must not be attributed to the source. I did not re-open the source.

## Proposed QUALITY criterion (one, ≤3 lines — for the L1 to decide; QUALITY.md not touched)

> **A count claimed about a registry or a directory is re-derived by command before it is written,
> and every pointer a lesson cites resolves as written.** A scope count is stated as the ids the
> command returns, not as a remembered subset; a path in a lesson is checked with `test -e` at the
> revision it names. Evidence: round-85 lesson M85-1 and C-R2/C-R3
> (`corpus/lessons/round-85.md`); red-before/green-after sweep in
> `.ufo/waves/round-85/w1/ScribeLesson/sweep-red-before.txt` and `sweep-green-after.txt`.

## Open questions for the L1

1. **S303's cell.** The routed R2 calls the "five scopes" text the row's `teaches` reason; it is
   in the **anchor** cell (col 7) — `teaches` holds the rejection and flip. I corrected it where it
   stands and noted the discrepancy. Confirm the L1 wants the anchor cell corrected in the registry
   row (append-only per the plan) rather than only in the lesson.
2. **R4 has no removal commit.** The pickaxe over `tools/` is empty; the field was removed in the
   working tree before the tool's first commit, so no diff can be shown. My correction adds the
   committed receipt instead. If the L1 wants a diff-shaped artifact, it must be re-derived from
   the pre-commit bytes, which are not in the lane.
3. **Receipt id mismatch.** `m84-2-nested-met.json` carries `"mistake": "M84-2"` but supports the
   **M84-4** row. Left as-is (frozen r84 tree); flagged in C-R4 for the L1's call.
4. S304's `used-by` points at `corpus/knowledge/2026-11-04-r85-mutant-kill-binding.md`; row and
   entry must land together or the registry's E11 check fires (ScribeSource's note, unchanged).
5. The spot-check line in `## Gate` reads `pending: non-author closure` as instructed; round 85's
   own outside spot-check is not written yet, and no admission for this round is claimed here.

## Installations

None. No `pacman` transaction (pacman is PAUSED host-wide). No tool was installed or upgraded.
