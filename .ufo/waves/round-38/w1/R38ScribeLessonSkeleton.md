# R38ScribeLessonSkeleton — wave-1 lesson draft (report)

Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (read-only for this seat outside its own
report + artifacts). Base `77091b492cc53f8743bd0701b1e7d5e66123dd84`. Freeze v1
`e059ca9391642d5b71b6662cabcbdce0d9308719`. Control receipts
`efd5c47a72a50b3a434783f82268fb4a96e636a1` (7 controls, all exit 1). Wave-1 dispatch `9c9d496b`.
Status: draft delivered; nothing landed in the corpus; no VCS mutation; no tool installed.

## Behavior

1. Read `plans/round-38-claims.md`, `corpus/lessons/round-37-verifier-spotcheck.md`,
   `corpus/lessons/round-36.md` (format reference), the wave-1 spec for the gate seats, the seven
   control receipts, the assimilation scratch (`reg-ids`, `staged-ids`, `collisions`,
   `quarantine-slice`), the round-37 probes, and the wave-1 executor/scout artifacts.
2. Wrote the lesson draft to
   `.ufo/waves/round-38/w1/artifacts/R38ScribeLessonSkeleton/lesson.md` (157 lines, 19788 B, sha256
   `5f161e5c…0ca3`). Sections: header (freeze v1 + the uncommitted v2 amendment), `## Mistakes`
   (4 rows, each with class · evidence pointer · captured-by · fix · a shown red-before), `## Gate`
   (sources opened this round, assimilation decisions, id-collision numbers, quarantine verdicts,
   kill-rule status), `### Wave-1 falsifiers`, `### Routed defects`, and a `[L1-FILL] citation
   pointers` section left for integration.
3. Built the three fixes the draft claims, and ran each red-then-green:
   - `cited-path-check.py` — red on the round-37 fleet report (exit 1, `:14` names a receipts
     directory holding no `*.json`), green on `corpus/lessons/round-36.md` (20 citations), green on
     the draft itself (13 citations, 27 forward-pointer lines skipped).
   - `lesson-skeleton-gate.sh` — red at `77091b49` for rounds 36 + 37 (`MISSING round-37`, exit 1),
     green for round 36 alone.
   - `premise-check.py` — red on the frozen v1 claims copy (`claims-at-freeze-v1.md:27`) plus
     `tools/round-38/c1-run.sh:6` (exit 1), green on the draft (which quotes the false sentence and
     asserts the declared dependency).
4. Two live source fetches for the gate (both recorded with commands, bytes and sha256 in
   `sources-live.txt`): `unblob.org/formats/` (HTTP 200, 216890 B, 97 `<h2 id=`, 3× the "more than 30"
   sentence) and the Freetz raw note (HTTP 200, 1496 B, byte-identical to the committed
   `.ufo/waves/round-37/probes/avm.txt`, `diff` empty).

## Gates (as filed in the draft)

- Sources opened this round: **S112 admit**, **S113 admit** (closes R37-CL2 fixture half),
  **S114 admit** scope-limited (closes R37-CL2 text half), **S116 admit** (own-work K1/K2
  provenance), **S115 reject** — 7-Zip 26.04 as a BE-v4 oracle, on the empirical ground only: the
  vendor lists SquashFS under "Unpacking only:" yet the installed 26.04 refuses all four carriers
  (exit 2, "Cannot open the file as archive"); flip = a release that opens one and matches the
  oracle. "7-Zip cannot read SquashFS" is explicitly refused as a fabrication.
- Assimilation theme (`/home/vgpnk/Projects/shokuknow/merge/kaidoku`): **id-collision numbers**
  111 registry ids / 132 staged ids / **6 collisions S106–S111**; guard proof reproduces the
  two-space-indented row (`S001 S002`, count 2); 0 rows escape the 0–3-space pattern on either side.
  Resolved by document: 2 of the 6 are the same documents as lane rows (unblob README → S110,
  devttys0 README → S111, dropped), 4 are new (core(5), binwalk, dncil, jadx).
  **Decision 1 admit** `unblob-format-matrix` (live re-count); **Decision 2 refuse**
  `sasquatch-unblob-avm-branch` (superseded premise, unpinned `main` source, campaign-local rows);
  **Decision 3 refuse** the five `avm-*` entries as staged (measurement rows are campaign-local
  `lanes/kaidoku/round{10..14}/work/*.tsv`, QUALITY #1). Each carries reason and flip.
- Quarantine slice (5 rows, re-derived identical, sha256 `7383a90e…`): S150 **REFUSE**
  (fabrication class; named heading 0× against a live 174088 B article), S113 **ADOPT-WITH-ANCHOR**
  with the locale count corrected (22 hreflang = 21 locales + x-default, not "17"), S117
  **UNVERIFIABLE** (IEEE 202/0-byte body; Crossref confirms the paper), S136 and S147
  **ADOPT-WITH-ANCHOR** (S147 also carries the 6.5.0/6.7.0 drift caveat). None is cited by an
  admitted entry.
- Controls: all seven exit 1 → no control met its target → no kill rule stopped C1/C2.

## Touched surfaces

Wrote only:
- `.ufo/waves/round-38/w1/R38ScribeLessonSkeleton.md` (this report)
- `.ufo/waves/round-38/w1/artifacts/R38ScribeLessonSkeleton/{lesson.md, claims-at-freeze-v1.md,
  cited-path-check.py, lesson-skeleton-gate.sh, premise-check.py, red-cited-path.txt,
  red-lesson-gate.txt, red-premise.txt, sources-live.txt}`

Read-only otherwise: `corpus/` (lessons, SOURCES, QUALITY), `plans/`, `tools/round-38/`,
`.ufo/waves/round-38/`, `.ufo/waves/round-37/`, the fleet repo's round-37 report, and
`/home/vgpnk/Projects/shokuknow/merge/kaidoku` (no campaign tool run there). No claim, counter,
carrier, oracle, predicate, PROVINCE/README/SCORECARD/SHONEN/SKILL/SOURCES/knowledge file was
edited. No git/jj command other than read-only `log`/`show`/`status`/`ls-tree`/`cat-file`/`diff`.
Scratch `/fast/scratch/hyaku/kaidoku-r38/R38ScribeLessonSkeleton` removed before this report.

## Findings (evidence, not repairs)

1. **R37-CL1 fix shown able to fail.** The round-37 report's receipts claim is still false on its
   face: the cited subdirectory holds one extract tree and no envelope; only `rea-k3.json` is
   committed. The checker fires on the committed report and on the verifier lesson itself.
2. **The freeze v1 dependency premise is false, and the wave measured it.**
   `claims-at-freeze-v1.md:27` ("no external extractor dependency") and `c1-run.sh:6` contradict
   unblob 26.6.4's own declared dependency (`EXECUTABLE`/`V4BE_EXECUTABLE`,
   `get_dependencies()`), and K1's four arms decide it: off-PATH gap
   `missing-extractor-dependency` / `["sasquatch-v4be"]` / 0 files versus on-PATH 5/5 oracle files,
   0 gaps, same carrier sha256 `1cfb6c33…`. The round-37 statement was a PATH-doctored probe shape;
   it reproduces, and the carrier is not blocked while the tool is resolvable.
3. **Unexpected repo change, adapted to.** During this seat the L1 left an **uncommitted** freeze v2
   amendment in the working tree (`plans/round-38-claims.md`, `tools/round-38/c1-counter.py`;
   mtime 03:25:45 -03:00, still changing at my read). The draft judges only `e059ca93` bytes, keeps
   a frozen v1 copy as evidence, and asserts no v2 count or sentence.
4. **K2 cannot satisfy "carries no extraction gap" as frozen.** `R38ExecAfterK2/after.json` publishes
   all 3 oracle regular files and reports one `unpublished-entry` gap for the symlink
   `firmware.bin_extract/var/lib/run-link`. REPORTED, not repaired.
5. **K1's assigned-arm envelope carries the dependency gap** (`after.json`, `ev_fd9baf66…`), so that
   particular committed candidate after-receipt cannot meet the target; the clean K1 envelope is the
   on-PATH arm (`ev_5353626b…`). K4 (`ev_3d1197d1…`) and post-fix K3 (`ev_fbc3be2e…`) are complete.
6. **The frozen after-mode harness could not run at `9c9d496b`** — `mkdir -p "$OUT"` before REA makes
   REA refuse the pre-existing extraction root (exit 1, "Extraction output root already exists");
   fixed by the L1 at `cb4326b2` (`rm -rf "$OUT"`), verified on K3 (exit 0, 4 files, 0 gaps).
7. At the tip `9c9d496b`, recounts remain at the base: C1 `carriers_matched 0` (`met_target false`),
   C2 `mismatches 1`, `guards_ok false` (`prov_core:REA MCP server` → `evidence/doctor/`). No C2
   drift is visible in this seat's artifact set.

## Out of scope / limits

- Did not run REA, the counters, their selftests, or the controls; did not score C1/C2. The draft
  quotes wave-1 receipts only.
- Did not verify the freeze v2 amendment; it is uncommitted and was still changing.
- No SOURCES rows appended, no entry written, no PROVINCE/README patch; those are the L1's and the
  sibling scribes' seats. The draft's `[L1-FILL]` lines mark every pointer left to integration.
- `cited-path-check.py` is a wording/structural check, not proof of content: it skips `[L1-FILL]`
  forward-pointer lines and treats a receipts directory claim as "receipts in/at/are …".
- No tool installed or upgraded; no pacman, npx, or release binary was executed beyond the two HTTP
  fetches recorded in `sources-live.txt`.

## Artifacts (all under `.ufo/waves/round-38/w1/artifacts/R38ScribeLessonSkeleton/`)

| file | bytes | sha256 |
|---|---|---|
| `lesson.md` | 19788 | `5f161e5c…0ca3` |
| `claims-at-freeze-v1.md` | 8479 | `13ea8eba…9815` |
| `cited-path-check.py` | 4535 | `a1e04432…1d68` |
| `premise-check.py` | 2950 | `932cf816…cef1` |
| `lesson-skeleton-gate.sh` | 648 | `3ba8255f…cdd7` |
| `red-cited-path.txt` | 638 | `d8897fe3…aace` |
| `red-premise.txt` | 766 | `cf5a95b1…fb04` |
| `red-lesson-gate.txt` | 88 | `ba7460ec…4031` |
| `sources-live.txt` | 1301 | `9e44416e…44fe` |
