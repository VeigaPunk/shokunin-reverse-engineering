# R44ConnRouted — routed-defect ledger, round 44 wave 1

Seat: R44ConnRouted (connector, leaf, read-only). L1: KaidokuR44. Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Base `c29360e3ba5381a5ab69e372d0d9577970f85018` is an ancestor of lane HEAD `fc5eb54a` (receipt K02, exit 0).
Observed 2026-10-28. Receipts: `.ufo/waves/round-44/w1/R44ConnRouted/receipts.json` (21 read-only checks K01–K21;
sha256 `3773c3cf436705b08579d7fb3f1d399f1617c425dc5a37bccd72de09e1c760f1`; runner
`.ufo/waves/round-44/w1/artifacts/R44ConnRouted/routed-checks.py`). Each receipt carries seat, command, cwd, exit code,
stdout sha256, stdout bytes, wall time, and bounded stdout/stderr heads.
Installs/updates: none. Writes: this ledger, the receipts, the runner, and scratch (removed). `plans/round-44-claims.md`
was NOT edited (outside this seat's write set); every amendment below is a proposal for the L1 to integrate.

## 0. Routed-defect sources read

- `.ufo/routed/` does not exist in the lane. No separate routed-defect file was found; the list was assembled from:
  - `.ufo/prompts/kaidoku-round-44.md` §5 item 5 (inherited state) and §7 items 1–5 (scratch discipline);
    the same text is `scripts/hyaku/lane-addendum.md` §7 (lines 488–518).
  - `corpus/lessons/round-43-verifier-spotcheck.md` §"Routed defects" (lines 35–39) and `corpus/lessons/round-43.md`
    M43-1 (line 9) and M43-2 (line 33).
  - `corpus/lessons/round-42.md` "Routed defects into round 43" (lines 71–76) and `corpus/lessons/round-42-verifier-spotcheck.md`
    §5 (lines 84–90). These carry no scratch or fixture defect; R42-V1..V5 are not re-judged here.
  - `.ufo/waves/round-43/w2/R43W2C2MapMut.md` and `R43W2C1Set.md` (the W2 survivors the closure names).

## 1. Ledger

Status vocabulary: ADDRESSED (in draft text with a control), PARTIAL, OPEN (draft silent or wrong), CARRIED, NOT-KAIDOKU.

| defect_id | source | status for round 44 | where addressed (plans/round-44-claims.md unless stated) | receipts |
|---|---|---|---|---|
| R44-SCR-TMP (TMPDIR / mkdtemp /tmp routing; counters must honour TMPDIR and accept a scratch argument) | lane-addendum §7.4; prompt §7.4 | **OPEN.** No literal `/tmp` string in round-39/42/43 tools, but `gettempdir()` falls back to `/tmp` whenever `TMPDIR` and `HYAKU_SCRATCH` are unset in 14 round-40..43 lines. The round-42 C1 counter (the port source) reads only `HYAKU_SCRATCH`/`--work` for its own scratch; `TMPDIR` is set only for child processes. The draft has no predicate or control for this. Proposed A3. | Port text lines 59–64 silent; counting command line 91 takes `--work` only; no tools/round-44 yet (K16 absent). | K11 exit 1 (no literal /tmp), K12 14 gettempdir lines, K14 scratch_root body and TMPDIR reads |
| R44-LFS (LFS fixture custody) | lane prompt routed list (fixture custody) | **ADDRESSED for bytes; PARTIAL for pins.** The four C1 carriers and the v2ns/v3 fixtures are plain git blobs (mode 100644, no `.gitattributes`, not LFS pointers). All 14 fixture files match `tools/round-42/fixtures.json` sha256 and size. Gaps: `carriers.json` must pin its own sha256 and must not copy the fixtures.json `compression` labels (see R44-V2BE, A2); the S138 `__output__` trees are not committed yet (`corpus/evidence/round-44/` untracked, owner R44SrcOracle). | Carriers table lines 43–52; frozen paths lines 209–212 (fixtures.json, the 4 carriers); oracle trees line 213–214 | K03 exit 0 (blob modes, no attrs), K04 exit 0 (14/14 sha_ok and size_ok) |
| R44-SASQ (sasquatch nonstandard magic) | lane prompt routed list | **ADDRESSED as Frontier (v2ns), with one gap.** v2ns carriers carry magic `zlqs` (LE) and `sqlz` (BE), which `file` reports as "data" and `unsquashfs` refuses (exit 1). unblob 26.6.4 registers `squashfs_v2_nonstandard` with magic `0x73716C7A`. Gap: no control proves that the v1/v2 probe refuses `zlqs`/`sqlz` bytes; the round-42 counter's magic table (line 442) carries both. Proposed CTL-C1-4 (A8). | Frontier text lines 54–57 and 114–117 | K06 magic bytes, K09 exit 1 (v2ns refused), K13 magic table, K20 unblob handler |
| R44-M43-2 (frozen raw-numstat predicate vs admitted row block) | round-43 closure; corpus/lessons/round-43.md M43-2 | **PARTIAL.** The text states the fix (lines 232–233: diff expectations are row-identity checks, never raw numstat), but the landing mechanics contradict the freeze rule (A1): appended repairs change frozen blobs, and C1 itself appends to two C2 frozen paths. The round-43 scorer still uses the raw numstat predicate (`sources_numstat_three_additions`). | Freeze rule lines 18–29; frozen paths and landing lines 217–233; Separability lines 177–185 | K17 anchors present, K18 raw numstat predicate at c2-score-r43.py:194 |
| R44-W2-SYM (C2 parent-symlink and dot-dot escape survived round-43 linter) | round-43 closure; R43W2C2MapMut.md lines 57, 59 | **OPEN.** The C2 counter is not written; the draft says it re-runs checks "in a scratch clone" (lines 145–148), which is the exact surface W2 broke. Proposed A6 (read blobs via `git ls-tree`/`git show`; reject mode 120000 and non-normalized paths; controls CTL-C2-4/5). | Lines 145–148, 149–161 (controls list has no symlink or escape control) | K19 (3 SURVIVED lines in the W2 report) |
| R44-W2-C1 (C1 manifest-ID / path / provenance weaknesses) | round-43 closure; R43W2C1Set.md | **PARTIAL.** Per-carrier exact equality is stated (contract; lines 59–88). Not stated: the carrier ID set must equal exactly the four frozen IDs, no duplicates, each path a regular file at FREEZE, and no symlink. Proposed A7. | Predicate lines 59–80 | K03 (carrier blobs are mode 100644, so the regular-file rule is satisfiable) |
| R44-REAP (reaper notice; /tmp and $HYAKU_SCRATCH not citable) | lane-addendum §7.5; prompt §7.5 | **PARTIAL.** C1 data goes to `corpus/evidence/round-44/c1/` (in-tree, lines 92–94). Open: `--json-out <OUT>` (lines 91, 163) is not required to be in-tree; 789 committed evidence files cite `/fast/scratch/hyaku/` absolute paths that the driver may reap (K15). The rerun projection (core profile) excludes absolute paths, so the projection binding is path-independent. Proposed A5. | Counting commands lines 90–92, 162–163 | K15 exit 0 (count 789), K17 anchors |
| R44-V2BE (new, found by this seat): v2-be compression premise | not on the routed list; found in this attack | **OPEN.** Draft lines 85–87 say `v2be` is uncompressed and that this is an oracle property, citing `file`. `unsquashfs 4.7.5 -s` on the same bytes reports "Data is compressed" and "Fragments are compressed"; `file` also says "uncompressed" for v1-be, which unsquashfs reports as compressed; fixtures.json labels all four carriers `gzip`. `file` is not a compression oracle. Proposed A2. | Lines 85–87 and 57 | K05 (`file`), K07 (unsquashfs -s), K10 (fixtures.json labels) |
| R44-OPATH (new): oracle member prefix | not on the routed list; found in this attack | **OPEN.** `unsquashfs -lls` rows carry a `squashfs-root/` prefix and a root directory row; the predicate states "exact relative path" but no strip rule. Proposed A4. | Oracle paragraph lines 82–87 | K08 (3/3/4/4 regular rows), K21 (prefix rows) |
| R44-CONF (status-neutral conformance: SOURCES old-row changes, frontier advancement detail in report) | round-43 closure "Status-neutral report conformance debt" | **CARRIED.** The frontier step (lines 187–205) lists S138/S139 as rows to open this round; the report must log old→new per §2b. | §2b frontier step | none (report duty) |
| R44-M43-1 (premature filing before WAVE-DONE) | round-43 M43-1; QUALITY #47 | **CARRIED.** L1 duty, not in the draft. | Cited rule: run-9 `File only after WAVE-DONE` in `.ufo/prompts/kaidoku-round-43.md` §6 (round-44 prompt location not verified) | none |
| R44-PROMPT (dispatched prompt omits canonical clauses) | round-43 closure | **NOT-KAIDOKU.** Operator/integrator template defect; one report line. | — | none |
| R44-SOURCES-ROUTE (round-43 "preserve honest stop; derive predicate from exact append block") | round-43 closure routed list | **PARTIAL.** C1 names S138/S139 by id (lines 77–80); no row-identity check against the exact appended block is stated, and no numstat ban for SOURCES is stated (A1 note, A7). | Lines 77–80; A1 | none |

## 2. Attacks on the draft (pre-freeze; proposed amendments for the L1)

Severity: BLOCKS-FREEZE means the claim cannot be scored admissibly as drafted. FIX-BEFORE-FREEZE means a predicate or control is missing.

**A1 — BLOCKS-FREEZE (C2 freeze contradicts itself and C1's landing).**
- Freeze rule (lines 20–23): an admissible score needs "no commit in `FREEZE..REV` touches a frozen path of that claim" and "each frozen regular-file blob at FREEZE equals the blob at REV".
- Frozen set for C2 (lines 217–219) includes `SCORECARD.md`, `SHONEN.md`, `corpus/README.md` and `corpus/SOURCES.md`.
- Landing (lines 224–227) says repairs are appended notes "so the frozen blobs stay equal at FREEZE and REV". An append changes the blob.
- Lines 228–231 then relax `frozen_path_changed` for rubric-named paths, while CTL-C2-3 (lines 158–159) says any edit must re-red via `frozen_path_changed`. The two cannot both hold.
- C1 appends S138/S139 to `corpus/SOURCES.md` and a map row to `corpus/README.md` (lines 35–38, 59–61). Both are C2 frozen paths, so any C1 landing at REV turns C2 frozen_path_changed. The Separability section (lines 177–185) says the claims "share" these files, which the freeze rule forbids.
- Proposed amendment: freeze per statement, not per file. The rubric records a sha256 of each asserted statement's text (and its anchor) at FREEZE. C2's frozen-path set excludes `corpus/README.md` and `corpus/SOURCES.md`. The `frozen_path_changed` arm passes for SCORECARD/SHONEN only if the REV diff against FREEZE consists of append-only hunks whose bytes equal the rubric-declared block (hunk-level row identity, never numstat). Any other edit re-reds. Control: CTL-C2-3 must still fail on an undeclared edit.

**A2 — BLOCKS-FREEZE (premise): v2-be "uncompressed" is not a compression measurement.**
- Draft lines 85–87 cite `file` ("version 2.0, uncompressed") as an oracle property. Line 57 says the superblock probe was "verified against `file` output".
- Receipts K05 and K07: `file` says "uncompressed" for v2-be and v1-be. `unsquashfs -s` on the same bytes says "Data is compressed" (and "Fragments are compressed" for v2-be). K10: fixtures.json labels all four carriers `gzip`.
- This seat did not decode the superblock compression field. The conflict is established; the true value is for R44C1Counter to measure.
- Proposed amendment: delete the "uncompressed" premise and the `file`-verification sentence. `carriers.json` records compression as read by the frozen superblock probe, cross-checked against the `unsquashfs -s` "Data is compressed" lines. The counter must not read fixtures.json `compression`. Control: a `carriers.json` whose compression value is edited to disagree with the probe exits non-zero.

**A3 — FIX-BEFORE-FREEZE (scratch / TMPDIR routing).**
- K11: no literal `/tmp` in round-39/42/43 tools (grep exit 1). K12: 14 `gettempdir()` fallbacks in round-40..43 counters and generators; with TMPDIR and HYAKU_SCRATCH unset they resolve to `/tmp`. K14: round-42 C1 `scratch_root()` reads only `HYAKU_SCRATCH` and `--work`; `TMPDIR` is set only for child processes.
- Proposed amendment: the port's scratch function resolves `--work` > `$HYAKU_SCRATCH` > `/fast/scratch/hyaku`, never `gettempdir()`. Children receive `TMPDIR` under the work dir. Control CTL-SCR-1: run the counter with `TMPDIR` set to a decoy under `/fast`, `HYAKU_SCRATCH` unset and `--work` set; before and after listings of `/tmp` and `/var/tmp` must be identical; a `gettempdir()` mutant must fail the control.

**A4 — FIX-BEFORE-FREEZE (oracle member prefix).**
- `unsquashfs -lls` names regular rows `squashfs-root/<name>` and adds a `squashfs-root` directory row (K21 prefix rows; K08 regular-row counts 3/3/4/4).
- Proposed amendment: the census strips exactly one leading `squashfs-root/` from each regular row and drops the directory row. The regular-row count must equal the frozen `expected_files` for each carrier, checked by the counter.

**A5 — FIX-BEFORE-FREEZE (reaper citability and `--json-out` location).**
- K15: 789 committed evidence files cite `/fast/scratch/hyaku/` absolute paths (for example `corpus/evidence/round-40/c1/V2/after.json`). Addendum §7.5 says `$HYAKU_SCRATCH` entries with no live process and no change for 45 minutes are deleted.
- Proposed amendment: the counter refuses an `--json-out` path outside the lane tree or the wave dir, and refuses any receipt field that resolves into scratch. R44 receipts store lane-relative paths. The projection needs no change: the core profile already excludes absolute paths and output directories.

**A6 — FIX-BEFORE-FREEZE (C2 symlink and dot-dot guard).**
- R43W2C2MapMut.md (lines 57, 59): a symlinked parent component and a `../` escape both survived the round-43 linter (exit 0, 136/0). K19 counts 3 SURVIVED lines.
- Proposed amendment: the C2 counter reads blobs through `git ls-tree -r` and `git show`, not a filesystem copy. A rubric path with ls-tree mode 120000 at any ancestor, or a path that is not already normalized, exits 2. Controls: CTL-C2-4 (planted symlinked ancestor in a scratch clone) and CTL-C2-5 (`../` rubric path) must each exit 2.

**A7 — FIX-BEFORE-FREEZE (carrier ID set and regular-file checks).**
- Proposed amendment: add to the C1 predicate: the carrier ID set equals exactly the four frozen IDs; no duplicate ID; each carrier path is a regular file (mode 100644) at FREEZE and REV; `carriers.json` pins each sha256. Control CTL-C1-6: a duplicate or extra carrier ID exits 2.

**A8 — FIX-BEFORE-FREEZE (controls to add).**
- CTL-C1-4: v2ns bytes presented under a `squashfs_v2` binding exit non-zero (the probe must not match `zlqs`/`sqlz` as v1/v2).
- CTL-SCR-1 (A3) and CTL-C1-6 (A7) as above.

**Positive checks (premises that hold):**
- The independent oracle works for the four carriers: `unsquashfs 4.7.5 -lls` exits 0 on v1-le/be and v2-le/be (K08), and exits 1 on v2ns-le (K09). The v2ns Frontier decision is supported.
- The sasquatch dependency is real: unblob 26.6.4 sets `EXECUTABLE = "sasquatch"` for the squashfs extractor, and `get_dependencies()` returns sasquatch and sasquatch-v4be (K20). v1 and v2 inherit the base extractor. CTL-C1-3 (sasquatch stripped from PATH) is therefore a meaningful control. The inherited extractor object is version 3; the command for non-v4 is version-independent, so this is harmless, but the port must not key anything on it.
- Fixture bytes match the pins 14/14 (K04); they are plain blobs (K03).

**A9 — CARRIED to L1.** `corpus/evidence/round-44/` is untracked at observation time (R44SrcOracle in flight). S138's `__output__` trees must be committed and content-addressed before FREEZE.

## 3. Limits

- Read-only. Neither counter exists yet (K16: `tools/round-44` absent). No REA 6.5.0 run; no C1 data procedure; no `c1-run.sh`.
- The superblock compression field was not decoded (A2 states the conflict, not the value).
- The unblob source was fetched to scratch and its sha256 is recorded in K20; it is not committed.
- The `disk-guard.sh status` read (earlier this session, not re-run in receipts): `/tmp` 5% used, `/fast/scratch/hyaku` 27% used.
- Routed items R42-V1..V5 are outside this seat's kaidoku-scratch and fixture list and are not re-judged.
