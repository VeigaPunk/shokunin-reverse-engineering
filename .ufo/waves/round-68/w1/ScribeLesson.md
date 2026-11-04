# ScribeLesson — round 68, wave w1 (scribe)

Seat `ScribeLesson` (scribe; leaf member, no dispatch). Drafted the round-68 lesson prose at
`.ufo/waves/round-68/w1/ScribeLesson/lesson.md` (target `corpus/lessons/round-68.md`) and the Gate
fetch receipt beside it. The L1 lands; nothing was landed here, and **no claim verdict is asserted** —
both after-arms belong to the L1's data run and the closure to the non-author judge. No tool was
installed or upgraded this seat (no pacman, no npx, no `uv`); the `npx` cache was not touched.

## Behavior

Read the five required inputs (round-67 spot-check, round-67 lesson, the declaration, the container,
the two base receipts), then measured rather than repeated: counted the source and registry
populations at the base from git blobs, re-opened the UPX pages the round's gate uses, and read the
two instruments, the control receipt and the two plans a census set names. ScoutSource's `gate.md`
did not exist when this seat started and did by mid-task; the lesson's Gate table is built on it and
corroborated by this seat's independent fetch (the sha256s match on every shared candidate).

## Gates (drafted lesson §Gate)

- **Admit — S270**: UPX 5.2.0 manual `doc/upx-doc.txt` at tag `v5.2.0`
  (commit `034b6d0d81c53998c07ad6f34bfead6f5c5445ce`), `NOTES FOR LINUX/ELF386` lines 441-442, byte
  offset 18 963: "Packed programs will be byte-identical to the original after uncompression."
  HTTP 200, 37 208 B, sha256 `4dc547ed…8c42`. Scope: the ELF386 format, which both carriers are —
  **not** the packer in the abstract; the manual's `--exact` WIP note and the WIN32/PE carve-out are
  the row's declared boundary. Independent check at `v5.3.0`: same sentence, line 484, 39 224 B,
  `9b980dca…d3c35`.
- **Reject (b)** the front page `https://upx.github.io/` — HTTP 200, **5 059 B**,
  `f07678bd…1fa7`, no tag/commit in the bytes, `byte-identical` 0 occurrences.
- **Reject (c)** `https://upx.github.io/upx-doc.html` — HTTP 404 (9 379 B, `b6205073…`).
- **Reject (d)** the Debian manpages mirror — the same sentence under `upx-ucl 4.2.4-2`, not the
  5.2.0 binary the route runs.
- **Reject (e)** the ManKier mirror — no revision/tag/commit in the bytes.
- **Note**: a receipt is not a source; the base dry run's sha equality is the measurement, not the
  ground.

## Touched surfaces

Written by this seat, only:
`.ufo/waves/round-68/w1/ScribeLesson/{lesson.md,report.md,gate-fetch.json,upx-doc.txt,upx-home.html}`
and this file. No tracked lane file, no fleet file, no index, no commit. Scratch
`/fast/scratch/hyaku/kaidoku-r68/ScribeLesson/` created and deleted before yield (the two fetched
copies were moved into the wave dir first).

## Findings (for the L1 and the closure)

1. **M68-0 (required, inherited)** — the registry under-reported by the two round-67 gates the plan
   named: `c1-at-base.json` `unregistered` = `tools/round-67/avm-le-counter.py`,
   `tools/round-67/mutation-battery.py`, `mismatches 2`, `registry_rows 73`; independently re-counted
   73 rows between the registry markers at `fcbe200f`. Captured-by: **PROTOCOL §Gate standard —
   Registry + Delivery**. The four repair rows are in the working tree (`git diff SKILL.md` = 4
   insertions), **uncommitted** — the C1 after-arm must be measured at a commit that bears them.
2. **M68-1** — both base receipts record `rev: "main"` and `instrument.rev: null`, so neither before
   arm is bound to a commit; atom A9 was written to close exactly this. Condition on the after
   receipts, not a claim.
3. **M68-2** — the C2 before receipt names `instrument.sha256 7ee286c0…b86c`, which is not the frozen
   `48ef4c68…5276e` and not any committed version (`git show 6020eb60:tools/round-68/packed-elf.py |
   sha256sum` = `48ef4c68…`); `instrument_supersessions` is `[]`. Re-take the before record with the
   frozen bytes or append a disclosed supersession.
4. **M68-3** — `named_but_absent` = 12: `plans/round-51-claims.md` and `plans/round-52-claims.md` name
   six instruments each that do not exist at the base (`tools/round-52` has 0 blobs). Cause
   **unknown** (no round-51/52 report opened); the census reports and excludes them.
5. **M68-4** — the route packs with `--best -q` (no `--exact`), asserts identity as a bare sha
   equality, and records no carrier `format`, while the identity guarantee is format-scoped and the
   PE section denies it without `--exact`; carrier records have no `format` key. Same class as
   M67-0; captured-by QUALITY #107.
6. **M68-5** — ScoutSource's gate table states the front page as 5 056 B; the committed copy and both
   independent fetches are 5 059 B (the sha in the same row is that of the 5 059-byte file).
7. **Arithmetic, not a measurement** — `scope_size 71` = 69 + the two round-68 tools the counting
   commands name; `registry_rows 77` = 73 + 4. `controls.py` is not named in a counting command, so it
   is outside the census's regime; an after run reporting 72 would falsify the predicate's premise,
   not the census.
8. **Source rows in flight** — `S269` is not at the base and is in the working tree (`git diff
   corpus/SOURCES.md` = 1 insertion); `S270` is drafted. The plan named one row, so the census end is
   176 or 177 from a start of 175 — the L1's count, not this lesson's.
9. **Repair 1 is appended but uncommitted** — the round-67 entry carries the `## Correction —
   2026-11-03, round 68` block in the working tree only (`grep -c 'round 68 (appended'` = 0 at
   `2dd5f2cd`, `fcbe200f`, `6020eb60`, `1eaf596e` and `6ffa9ce1`). All the round's repairs (entry
   correction, four registry rows, S269, the new knowledge entry) sit uncommitted at this reading;
   both counters read their subjects at `--rev`, so none can be measured until they are committed.

## Out of scope (not done, by rule)

No instrument executed (census, route, controls, selftests), so no after-arm number is reported; no
verdict, no trend, no admission; no edit to `SKILL.md`, `SOURCES.md`, the plans, the knowledge entry,
the ledger or any tracked file; no commit, push, index or `jj` operation; no subagent, no `labrat`
probe; no pacman transaction; no `npx`.

## Checks the L1/closure should run

- C1 after: `registry-conformance.py --rev <sha>` at the commit bearing the four rows, expecting
  `mismatches 0`, `scope_size 71`, `registry_rows 77`, exit 0, with `rev` and `instrument.rev` both
  set (findings 1–2).
- C2 after: `packed-elf.py` at the measured revision, expecting `carriers_matched 2/2`,
  `control_ok true`, `failing []`, `before_procedures [3, 3]`, exit 0, `instrument.sha256 48ef4c68…`
  (finding 3).
- Closure: re-measure the front page size from the committed copy before citing 5 056 (finding 6),
  and read the census end from `l1/census-end.txt` (finding 8).

## Artifact paths

- `.ufo/waves/round-68/w1/ScribeLesson/lesson.md` — the lesson draft (Gate / Mistakes / Outcome /
  Census).
- `.ufo/waves/round-68/w1/ScribeLesson/report.md` — every source opened, with commands.
- `.ufo/waves/round-68/w1/ScribeLesson/gate-fetch.json`, `upx-doc.txt`, `upx-home.html` — the Gate's
  measured evidence.
- `.ufo/waves/round-68/w1/ScribeLesson.md` — this report.
