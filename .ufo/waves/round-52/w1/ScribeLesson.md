# ScribeLesson — round-52 lesson skeleton

Verdict: settled. Drafted `corpus/lessons/round-52.md` as a skeleton with the freeze-paragraph
placeholders, a `## Mistakes` section seeded with the three inherited defects this round
commits to fix, and empty `## Gate` / census / honest-stop sections. No mistake beyond the
inherited ones is claimed.

## Artifact

- `.ufo/waves/round-52/w1/ScribeLesson/lesson.md` (the draft; the L1 may rewrite it into
  the freeze commit)
- `.ufo/waves/round-52/w1/ScribeLesson/receipts/r1-r51-dispatch-placeholders.json`
- `.ufo/waves/round-52/w1/ScribeLesson/receipts/r2-r51-wave-accounting.json`
- `.ufo/waves/round-52/w1/ScribeLesson/receipts/r3-r52-spec-placeholder-scan.json`
- `.ufo/waves/round-52/w1/ScribeLesson/receipts/r4-r52-dispatch-placeholder-scan.json`
- `.ufo/waves/round-52/w1/ScribeLesson/receipts/r5-wave-chronology.json`
- `.ufo/waves/round-52/w1/ScribeLesson/receipts/r6-status-json-census.json`

Every receipt carries the exact command, exit code, stdout sha256 and UTC time. Nothing was
run that is not receipted; the `## Gate` rows and the round's census end are **not run**
(exit 2 could-not-evaluate until the L1 opens them) and are marked as such in the draft.

## The three seeded rows (all fix cells PLACEHOLDER)

| id | class | inherited origin (committed bytes, re-read) | captured-by | planned fix |
|---|---|---|---|---|
| M52-1 | dispatch interpolation (M51-6) | `corpus/lessons/round-51.md` M51-6; `.ufo/waves/round-51/l1/dispatch-placeholders.json` — 36 items, **36 unresolved**, recorded exit 1 | none at r51 | `check-dispatch.py` assertion run **before the ready file**, receipt attached — fix cell PLACEHOLDER until shown able to fail |
| M52-2 | observability, per-seat results fields | `.ufo/waves/round-51/l1/wave-accounting.json` — `result_rows_have_ids false`, `result_rows_have_status false`, 36 rows | none at r51 | `status.json` convention (`seat`/`role`/`status`/`summary`/`artifacts[]`) + `wave-accounting.py` as the L1's reader — fix cell PLACEHOLDER |
| M52-3 | round-shape, round-band shortfall | `.ufo/waves/round-51/l1/wave-accounting.json` — `floor64_met false`, `second_wave "not launched: orchestrator prohibited additional waves"` | the band rule (policy 64–128; claims `## Round shape`) | 64-seat v2 build+attack wave + falsify-wave plan after the landing — fix cell PLACEHOLDER |

## Findings (1–3 most important)

1. **The interpolation checker did not gate this wave's own ready file.** mtimes (UTC):
   `w1-spec.json` 10:44:20 → `w1-dispatch.json` 10:44:35 → **`w1.ready` 10:44:44** →
   `ExecWaveCheck/check-dispatch.py` 10:47:14 → its `receipt.json` 10:47:27. The r52-w1
   dispatch is therefore **not** pre-dispatch-gated: the assertion is post-hoc evidence for
   this wave. The claims' routed-defect repair 3 asks for the check to run *before* the ready
   file, so that ordering is only demonstrable for the falsify wave. I recorded this as an
   open condition on M52-1 (receipt `r5-wave-chronology.json`), **not** as a new mistake —
   the draft invents no mistake beyond the inherited three.
2. **The content half of M52-1 is met in the wave bytes**: the spec (64 items) and the
   rendered dispatch (64 tasks, `counts.spawn 64`) both scan clean for
   `\{[A-Za-z_][A-Za-z0-9_]*\}` in every item string and in the context — 0 tokens on both
   sides (receipts `r3`, `r4`). Contrast with r51, where 36 of 36 items carried unresolved
   markers.
3. **Wave shape is inside the band on the spec, and the per-seat status convention is in
   use.** 64 seats; attack share 24/64 = 37.5 % on the claims' definition and 19/64 = 29.7 %
   on r51's narrower one (both ≥25 %); 64 + falsify 32–64 ⇒ round total 96–128 (≤128), or
   ≤72 with the ≤8-seat residual call. At the census instant 26 of 40 seat directories
   carried a `status.json` (mid-wave progress reading, **not** the wave accounting).

## Bounds and limits

- Lane tree read-only: nothing was written outside
  `.ufo/waves/round-52/w1/ScribeLesson/` (draft + receipts) and this report file. No commit,
  push, stage, stash or mutating git/jj command; no fleet-root write; no REA run; no
  network fetch; no tool installed. Scratch `/fast/scratch/hyaku/kaidoku-r52/w1-ScribeLesson`
  removed before yielding.
- The `## Gate` section, the round-end census and the honest-stop outcome are **not run** by
  this seat — they belong to the L1's freeze/controls/data-run sequence and are marked
  PLACEHOLDER, not guessed.
- Sources rows for round 52 (including the S252 `mknod(2)` row the L1 and a scout opened
  this round) are **not** drafted by this seat: the row grammar and the per-entry gates are
  the ScribeSources seat's, and the claims require per-row receipts I did not produce.

Report path: `.ufo/waves/round-52/w1/ScribeLesson.md`
