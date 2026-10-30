# Round 52 — PLACEHOLDER (one freeze; the device-accounting law re-frozen and the ddwrt failed-body route repaired)

Lane `kaidoku`, round 52, attempt 1, L1 `KaidokuR52`. Round-start branch tip
`c525de54a53eb3c4fee28ede2721da4527cf8ece`; declared claims at
`ab0eafedc41402b43b41a4362084119578dfe7ce` (`plans/round-52-claims.md`).

**Freeze paragraph (PLACEHOLDER).** The declared freeze is the single later commit that
adds the round-52 instruments (`tools/round-52/**`), the fixtures and the amended claims
file: commit `PLACEHOLDER`, recorded in `.ufo/waves/round-52/l1/FREEZE` and `LOG.md`
**before any data run**. Wave 1 (`r52-w1`, 64 seats, `.ufo/waves/round-52/w1/`) built and
attacked the drafts before that freeze; its findings are folded into the plan's
`## Wave-1 amendment record` (empty until wave-1 attacks land). A counter bug found after
the freeze is a miss, never a patch. Wave 2 (falsify) is dispatched after the landing when
w1 yields ≥32 distinct attack items (32–64 seats), otherwise one residual `task` call of
≤8 reviewer/critic seats; the round total stays ≤128. Wave evidence commit:
`PLACEHOLDER`.

**Claims (one line each; `plans/round-52-claims.md` is authoritative).**
R52-C1 (coverage): land the law-derived gap-accounting package (`tools/round-52/`) and
promote LE AVM members (`hsqs`) Frontier → Core under the corrected device-accounting law,
target `carriers_matched == 4` (g7581, g7582, c6490, c6430) with `law_shape_ok`,
`census_rederived_ok`, `depth_gap_recorded` and every binding true. Before-state (already
committed): the round-50 receipt `carriers_matched 2`, exit 1
(`.ufo/waves/round-50/l1/scores/c1-after-attempt2.json`).
R52-C2 (depth): land triage table v6 as `SKILL.md` rule block 27 plus the instrument
`tools/round-52/sqfs-triage-v6.py`; the ddwrt FAILED no-pad body
`dmg_Z3_v3ddwrt_inode_table` stops routing `legacy-body-failure`/`cross-read-legacy`
(new row `legacy-body-unreadable`, action `preserve-unresolved`, no cross-read); the frozen
executability audit is 1 violation before (over the v5 table bytes at the claims-draft base)
and 0 after; `census_outside` is 0 on both sides (a no-regression binding).
Verdicts: R52-C1 `PLACEHOLDER` · R52-C2 `PLACEHOLDER` — neither claim is scored until the
L1 freezes, runs the pre-freeze controls and performs the four-carrier vendor re-fetch and
the REA data run.

## Mistakes

Seeded with the three inherited defects this round commits to fix (round-51 closure §6.1–§6.3).
A fix counts only once shown able to fail; each evidence pointer and each fix cell below is
`PLACEHOLDER` until the round proves the fix ran. No mistake beyond the inherited ones is
invented here.

| id | class | evidence pointer | captured-by | fix and observed failure |
|---|---|---|---|---|
| M52-1 | dispatch interpolation (inherited M51-6) | PLACEHOLDER — the round-52 proof receipt path is not landed; inherited origin: `corpus/lessons/round-51.md` M51-6 (gen-w1.py item strings carried unresolved `{LANE}`/`{W1}` markers), `.ufo/waves/round-51/l1/dispatch-placeholders.json` (36 items, all 36 unresolved, recorded exit 1), `corpus/lessons/round-51-verifier-spotcheck.md` §6.3 | none at r51 (no pre-dispatch checker existed; the taken dispatch was immutable) | PLACEHOLDER — planned fix: the `check-dispatch.py` assertion run **before the ready file is written**, with its output committed as wave evidence. Observed failure: PLACEHOLDER (not yet observed; a fix that has not been shown able to fail is not a fix). |
| M52-2 | observability — per-seat results fields (inherited r51 §6.2) | PLACEHOLDER — the round-52 proof receipt path is not landed; inherited origin: `.ufo/waves/round-51/l1/wave-accounting.json` (`result_rows_have_ids false`, `result_rows_have_status false` over 36 rows of `r51-w1-results.json`), `corpus/lessons/round-51-verifier-spotcheck.md` §6.2 | none at r51 (the results handoff carried no per-seat id/status, so dead seats were unverifiable) | PLACEHOLDER — planned fix: the `status.json` convention (`seat`, `role`, `status`, `summary`, `artifacts[]`) written by every wave-1 seat, plus `wave-accounting.py` as the reader the L1's wave accounting parses. Observed failure: PLACEHOLDER (not yet observed). |
| M52-3 | round-shape — round-band shortfall (inherited r51 §6.1) | PLACEHOLDER — the round-52 proof receipt path is not landed; inherited origin: `.ufo/waves/round-51/l1/wave-accounting.json` (`results 36`, `floor64_met false`, `second_wave "not launched: orchestrator prohibited additional waves"`), `corpus/lessons/round-51-verifier-spotcheck.md` §6.1 | the band rule (policy `waveMinLanes 64` / `waveMaxLanes 128`; `plans/round-52-claims.md` `## Round shape`) | PLACEHOLDER — planned fix: a 64-seat v2 build+attack wave plus the falsify-wave plan after the landing (32–64 seats when ≥32 distinct attack items exist, else one residual `task` call of ≤8 seats), round total ≤128. Observed failure: PLACEHOLDER (not yet observed). |

### Mid-wave observations (seat ScribeLesson, 2026-10-30 — measurements, NOT proof of the fix)

These are facts measured during wave 1 at the paths named; they are **not** the M52-1/M52-2/
M52-3 fix evidence, and they do not substitute for it. Receipts (command, exit code, stdout
sha256, UTC) are under `.ufo/waves/round-52/w1/ScribeLesson/receipts/`.

- **r52-w1 carries no unresolved placeholders.** The wave spec (64 items) and the rendered
  dispatch (`taskCall.tasks`, 64 tasks) both scan clean for `\{[A-Za-z_][A-Za-z0-9_]*\}` in
  every item string and in the context: 0 tokens on both sides. Receipts `r3-r52-spec-placeholder-scan.json`
  (stdout sha256 `f6e72e43…8c609`) and `r4-r52-dispatch-placeholder-scan.json`
  (stdout sha256 `ebffa1cb…d639`). This is the *content* half of M52-1; the ordering half
  is not demonstrated — see below.
- **The interpolation check did not gate this wave's own ready file.** File mtimes (UTC):
  `w1-spec.json` 10:44:20, `w1-dispatch.json` 10:44:35, **`w1.ready` 10:44:44**,
  `ExecWaveCheck/check-dispatch.py` 10:47:14, its `receipt.json` 10:47:27. The checker was
  therefore created and run **after** `w1.ready` was written, so for r52-w1 the assertion is
  post-hoc evidence, not a pre-dispatch gate; the claims' routed-defect repair 3 asks for the
  check to run *before* dispatch, and that ordering is only demonstrable for the falsify
  wave. Receipt `r5-wave-chronology.json` (stdout sha256 `6b521620…f2f2`). This is recorded
  as an open condition on M52-1, not as a new mistake.
- **The per-seat status convention is in use mid-wave.** At the census instant, 26 of the 40
  seat directories present under `.ufo/waves/round-52/w1/` carried a `status.json`; seats
  still running were expected to be without one, so this snapshot is a progress reading and
  **not** the wave accounting. Receipt `r6-status-json-census.json`
  (stdout sha256 `f40c94be…1158`). The reader exists
  (`ExecStatusHelper/wave-accounting.py`, with its own selftest receipt); M52-2's fix cell
  stays PLACEHOLDER until the L1's accounting runs over the settled wave.
- **Wave shape is inside the band on the spec.** 64 seats dispatched (`counts.spawn 64`),
  roles executor 21 / scribe 8 / reviewer 8 / scout 7 / critic 7 / mutation-tester 4 /
  sentinel 3 / connector 3 / revenger 2 / simplifier 1. Attack share 24/64 = **37.5 %** on
  the claims' definition (reviewer, critic, mutation-tester, labrat, sentinel, revenger)
  and 19/64 = **29.7 %** on the narrower r51 definition (reviewer, critic,
  mutation-tester) — both ≥25 %. With the falsify wave (32–64) the round total is 96–128,
  ≤128; with the ≤8-seat residual call it is ≤72. The falsify wave has not been dispatched,
  so M52-3's fix cell stays PLACEHOLDER.
- **Inherited r51 facts re-read for the row pointers** (read-only, from committed bytes):
  `.ufo/waves/round-51/l1/dispatch-placeholders.json` (36 items, 36 unresolved, recorded
  exit 1; receipt `r1-r51-dispatch-placeholders.json`, stdout sha256
  `959a5920…92a7`) and `.ufo/waves/round-51/l1/wave-accounting.json` (`floor64_met false`,
  `result_rows_have_ids false`, `result_rows_have_status false`; receipt
  `r2-r51-wave-accounting.json`, stdout sha256 `e881cbcd…539e`).

## Gate

PLACEHOLDER — empty until the round's source rows are opened and decided. To be filled by
the L1 (and the ScribeSources seat's ledger) with: the round-52 SOURCES row(s) (including
the round-52 `mknod(2)` row, S252, opened this round) — URL, access date, ≤25-word located
quote, decision and limits; the rows added and any `old→new` supersessions; the
`used-by` update; the assimilation theme and its per-entry gates (≥1 admit, ≥1 reject) or
`Assimilation: none` with the scan receipt; and the non-author spot-check status. Each row
carries its own receipt (command, exit code, stdout sha256, UTC). Not run / not yet opened
at the time of this draft — PLACEHOLDER.

## Census before -> after

- Round start (`.ufo/waves/round-52/l1/sources-census-start.txt`): `sources-census.sh
  validate --root /home/vgpnk/Projects/shokunin kaidoku` → **exit 0**, 19 `W04`
  duplicate-URL lines, final line `kaidoku ok …/corpus/SOURCES.md`.
- Round end: PLACEHOLDER — the same command re-taken at the filing tip, exit 0 required;
  receipt path PLACEHOLDER (expected `.ufo/waves/round-52/l1/sources-census-end.txt`).
  The 19 W04 warnings stand as named debt unless a seat's row-by-row audit lands a
  correction set this round (CORPUS.md rule 2); any correction row supersedes old→new and
  is logged above.

## Honest stop

PLACEHOLDER — empty until the round's outcome is known. To be filled by the L1 with: which
claims verified and which are misses (with the exact receipts and exit codes); whether the
freeze commit was made before any data run; whether the pre-freeze controls were scored and
their verdicts; whether the four-carrier vendor re-fetch and the REA data run completed
(the L1 alone runs REA, in a quiet window); the `## Wave-1 amendment record` contents; any
mutant that came back green when it should be red (kill rule); and the disposition of the
routed defects that were **not** claimed this round (fetch-vendor network-guard selftests,
the preventive fleet-root stray control, census W04 hygiene, the carried L0 credential line).
Nothing in this file asserts a measurement that has not been run.

---

Draft provenance: seat `ScribeLesson` (scribe), wave `r52-w1`, 2026-10-30. Draft only —
this file is an input for the L1's freeze commit and may be rewritten. The `## Mistakes`
rows are seeded from the round-51 closure's routed defects
(`corpus/lessons/round-51-verifier-spotcheck.md` §6.1–§6.3) and `corpus/lessons/round-51.md`
M51-6; no other mistake is claimed. Measurements cited in the mid-wave section live under
`.ufo/waves/round-52/w1/ScribeLesson/receipts/`.
