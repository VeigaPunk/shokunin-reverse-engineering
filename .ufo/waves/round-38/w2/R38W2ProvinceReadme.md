# R38W2ProvinceReadme — PROVINCE.md + corpus/README.md edits at 3b960fe5/0fc61133

**Verdict: CONFIRMED** — every checked property of the two-file diff
(`git diff 077e212b81015f985febc12261ecac4fec71683a 0fc6113376a156fddc3ec385386d71c3a4a9f690 -- PROVINCE.md corpus/README.md`; 60 lines: PROVINCE.md 2 lines modified, corpus/README.md 6 inserted, 0 deleted) holds against the committed receipts, the frozen first-freeze counter, `corpus/SOURCES.md`, and a live refetch of the producer page. No defect found in either file. Two adjacent findings **outside** the two reviewed files are reported at the end for the L1 (A1: the C2 verdict's cited receipt path does not exist and the actual C2 score is uncommitted; A2: a stale present-tense "unmeasured" aside at `PROVINCE.md:372`).

Method: read-only git only (`show`, `diff`, `ls-tree`, `log`, `status`, `cat-file`); no VCS mutation; no subagents; scratch `/fast/scratch/hyaku/kaidoku-r38/R38W2ProvinceReadme` (removed at the end; cited bytes copied to `.ufo/waves/round-38/w2/artifacts/R38W2ProvinceReadme/`). No tool installs were needed (preinstalled git/jq/curl/python3/node used).

## 1. Doctor pointer repair (`PROVINCE.md:44`) — same document: YES

Old: "doctor outputs in `evidence/doctor/`" → New: "doctor outputs in `.ufo/waves/round-19/evidence/doctor/` (doctor-6.5.0.txt, doctor-6.7.0.txt)".

- The old pointer is dangling at repo root: `ls evidence/` shows only `round-1-2026-10-15/`; `ls evidence/doctor/` → "No such file or directory"; tracked `evidence/` files are only `round-1-2026-10-15/{baseline,rea-bundle,result,rubric}.json`.
- The repaired directory exists and holds exactly the two named files: `doctor-6.5.0.txt` (18,131 B) and `doctor-6.7.0.txt` (14,846 B), both dated Oct 20 16:02.
- Same document the prose describes: `doctor-6.7.0.txt` has **zero** `registration:devin`/`registration:omp` findings (grep count 0; registrations listed: claude_code, copilot_cli, cursor, hermes, kimi, opencode, pi) and `registration:kimi` → `ok: false`, `classification: config_drift` — matching the row's unchanged prose "6.7.0 doctor: no devin/omp registration finding, separate Kimi JSON registration missing". `doctor-6.5.0.txt` is a genuine 6.5.0 output (line 80: "the current REA CLI package is 6.5.0").
- The C2 counter independently treats this as the same document: its selftest green case is "repaired by document `.ufo/waves/round-19/evidence/doctor/`" → 0 mismatches, and the landed score `c2-at-0fc61133.json` shows `guards.base_unresolved = [["prov_core:REA MCP server", "evidence/doctor"]]` at base and `unresolved: []` after — i.e. the one base mismatch was exactly this pointer, now resolved.
- Table integrity preserved: line 44 has 5 `|` before and after.
- The sentence's other citation `.ufo/waves/round-19/evidence/province-pins-integrated.json` exists (2,951 B).

## 2. Line-157 frontier note — no supersession claim, accurate

The added sentence (PROVINCE.md:157, the second line of the `sasquatch` bullet that spans :156-157 exactly as the first-freeze claims doc cites it): "Round 38: standard BE v4 measured through `sasquatch-v4be` (`corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md`), not promoted — R38-C1 honest stop, K2's in-tree symlink leaves an `unpublished-entry` gap."

- **No supersession claim**: the added sentence contains no "supersede" language; the pre-existing round-36 clause "[2026-10-26: superseded for LE SquashFS v4 — …; big-endian/AVM stays here.]" is untouched. Correct for an honest stop — BE v4 stays Frontier, nothing is superseded.
- **Accurate, clause by clause** (all against committed bytes):
  - "measured through `sasquatch-v4be`": all four after-receipts name handler `squashfs_v4_be`; all four before-receipts give 0 files with gap `missing-extractor-dependency` [`sasquatch-v4be`]; `~/.local/bin/sasquatch-v4be -v` → "unsquashfs version 4.5.1" (the 4.5.1 pin in the README row is host-verified).
  - "not promoted": no Core row landed — counter bindings `province_core_row: false`, `province_core_section: false`; SCORECARD: "No capabilities row enters".
  - "R38-C1 honest stop": reproduced (§8).
  - "K2's in-tree symlink leaves an `unpublished-entry` gap": `K2/after.json` `normalized_result.unpublished_entries = ["firmware.bin_extract/var/lib/run-link"]`, gap kind `unpublished-entry`, exactly 1.
  - Cited entry path exists (3,760 B).

## 3. Coverage-map rows (`corpus/README.md:91-92`) — numbers match receipts; "not promoted" honest

Row 91 (BE v4): "(K1 5/5, K2 3/3, K3 4/4, K4 4/4) and none without it" — verified against `corpus/evidence/round-38/c1/K{1..4}/{before,after}.json` and the frozen oracles `corpus/evidence/round-37/c1/K{1..4}/oracle.tsv`:

| carrier | oracle.tsv regular files | after published | after gaps | before published | before gap |
|---|---|---|---|---|---|
| K1 | 5 | 5 | 0 | 0 | missing-extractor-dependency |
| K2 | 3 | 3 | 1 (`unpublished-entry`) | 0 | missing-extractor-dependency |
| K3 | 4 | 4 | 0 | 0 | missing-extractor-dependency |
| K4 | 4 | 4 | 0 | 0 | missing-extractor-dependency |

Every published `(relative_path, sha256)` matches its oracle row byte-for-byte (K1's five and K2's three checked individually — e.g. `bin/run 299001868fb8c02f…`, `var/lib/data.bin e96760a87768717b…`). "Every oracle regular file … and none without it" is exact. "K2's in-tree symlink stays an `unpublished-entry` gap" ✓; "R38-C1 ('no extraction gap' on 4/4 under the first-freeze counter) is an honest stop" ✓ — the first-freeze predicate (`plans/round-38-claims.md` at `e059ca93`, lines 25-30) does require "carries no extraction gap" per carrier; "AVM-BE and vendor-mangled images not measured" ✓ (entry Status says the same). "measured, **not promoted** (Frontier)" matches the entry's Status section and the no-Core-row bindings. K1's escaping-symlink half of the entry's two-outcome claim is also receipt-backed (`MaliciousSymlinkRemoved` occurs once in `K1/after.json`).

Row 92 (format matrix): live-refetched today — `curl -fsSL https://unblob.org/formats/` → HTTP 0 exit, 216,890 B, sha256 `8f8c29aff33d5aa1ee2a69f8a66f272d45fa3dd98d271c95337c3ff15a65bbc5` — **identical to S116's recorded digest**; 97 `<h2 id=` sections; "more than 30 different" ×3; `id="squashfs-v4-be">SquashFS (v4-BE)` present. "held as producer coverage statement", "coverage claim only, never an extraction outcome", "two corrections" (`v4-broadcom` spelling; "42 vendor-attributed entries" = 42 occurrences of `Vendor`) all match the entry (`2026-10-26-unblob-format-matrix.md`). Copy of the fetched page: `w2/artifacts/R38W2ProvinceReadme/formats.html`.

Rows are appended inside `## Coverage map` (before `## Knowledge` at :96) after the round-36 rows — no displacement, 0 deletions.

## 4. Knowledge-index rows (`corpus/README.md:199-200`) — sources cited exist

- Row 199 cites **S112, S113, S114** — all present in `corpus/SOURCES.md` at 0fc61133 (lines 118-120), all `mined`, 2026-10-26, 180d, used-by = `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md`. Receipts path `corpus/evidence/round-38/c1/` exists (K1..K4, before/after.json). Topic cells match the entry (structural dependency via handler argv + AVM `-be` drop; before/after arms; two symlink outcomes; "Frontier, not Core").
- Row 200 cites **S116, S110** — both present (lines 116, 122). S116 carries the digest I reproduced live. Topic cells match the entry (97 sections, ten SquashFS variants incl. `v4-BE`, ZIP limitation, "more than 30" vs "78+", assimilated + re-grounded, two corrections).
- The sasquatch entry additionally names S115 as a **rejected** row (7-Zip refusal "recorded as a rejected row (S115), not as a source") — S115 exists at line 121 with status `rejected`, consistent; neither knowledge row cites it as a source.
- The S110 edit (3b960fe5) does what the lesson's Gate section says: scope cell gains "plus its own "78+" format-count sentence (lines 5, 22)" and used-by gains the matrix entry; no status/recheck cell changed.
- Both rows' verified-at = 2026-10-26 = the entries' `verified-at`.

## 5. Lessons row (`corpus/README.md:229`) — every clause checks out

Against `corpus/lessons/round-38.md` (98 lines, landed 0fc61133), `corpus/QUALITY.md` at 3b960fe5, and SCORECARD's Round 38 section:

- "attempt 2 after a dead attempt 1" ✓ (lesson header: attempt 1 died at 03:37:05 without a report).
- "R38-C1 stopped under its first-freeze counter (3/4, K2 in-tree symlink gap)" ✓ (`c1-v1-at-3b960fe5.json`: carriers_matched 3, met_target false; my independent rerun identical, §8).
- "the attempt-1 post-scoring amendments are reported, not adopted (QUALITY 79, `freeze-drift.py`)" ✓ — QUALITY row 79 (corpus/QUALITY.md:87) is exactly the first-freeze rule + `freeze-drift.py` gate; M38-1 records `79f69347`/`f1010f67` and the v3 counter scored `NOT-THE-RULE`; SCORECARD: "The v2/v3 counters are not the rule".
- "R38-C2 pointer repair" ✓ (`c2-at-0fc61133.json`: mismatches 0, guards_ok true, met_target true; counter returns 0 iff met_target — exit 0 confirmed by convention and by the assignment's author verdict; see A1 for the receipt's commit-status defect, which lives in lesson-38.md/SCORECARD.md, not in this row — the row cites no receipt path).
- "one assimilated entry admitted, two refused" ✓ (lesson Gate: ADMIT `unblob-format-matrix`; REFUSE `sasquatch-unblob-compatibility-precondition`, REFUSE `sasquatch-unblob-avm-branch`).
- Placement correct: appended after the `round-36` row in `## Lessons`. (No `round-37` row exists and no `corpus/lessons/round-37.md` exists — only `round-37-verifier-spotcheck.md` — so the 36→38 jump matches the file inventory; round-37 material is carried as routed defects R37-CL1/CL2/CL3 inside the round-38 lesson.)

## 6. Frontier bullet (`corpus/README.md:239`) — consistent

"sasquatch-v4be — 2026-10-26 round 38: standard big-endian v4 measured (…) and **not promoted**: R38-C1 stopped on K2's in-tree symlink gap under its first-freeze counter. Still frontier: standard BE v4 promotion, AVM-BE, vendor-mangled images." — consistent with the PROVINCE note (§2), with the round-36 dated note it follows ("Still frontier: big-endian/AVM (`sasquatch-v4be`) and vendor-mangled images", kept as history), and with SCORECARD's planned round-39 (standard BE v4 promotion first, AVM-BE second). Appended inside `## Frontier` after the round-36 note; no displacement.

## 7. PROVINCE `## Adjacent` line counts — unchanged (SHONEN box 4 range intact)

- PROVINCE.md total: 374 lines → 374 lines. The diff's only hunks are at :44 and :157.
- `## Adjacent` starts at :97 in both versions; the next `## ` header is at :276 in both — the section is 179 lines in both, byte-identical.
- SHONEN box 4 asserts `PROVINCE.md:97-125` (refusal list; safety refusal :116-118; round-36 dated tooling bullet :119-125) — content at :97-125 unchanged; the C2 counter's `observed.adjacent_range = [97, 125]` at 0fc61133 independently confirms the asserted range.

## 8. Independent reproduction of the frozen first-freeze counter

Ran the first-freeze bytes myself (`git show e059ca93:tools/round-38/c1-counter.py`, sha256 `a7a62b098709035607375078a12d2668bb6d36bbabfc5a7459f04d00a9516db8` — matches the digest SCORECARD cites):

```
python3 -I -B c1-counter-frozen.py --root <lane> --rev 3b960fe5… --freeze e059ca93… \
  --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
  --json-out .ufo/waves/round-38/w2/artifacts/R38W2ProvinceReadme/c1-v1-repro.json
→ carriers_matched 3, carriers_unchanged true, met_target false, EXIT=1
  bindings: coverage_map_row true, entry_present true, entry_source_ids [S112,S113,S114],
  frontier_note true, opened_source_rows [S112,S113,S114], province_core_row false,
  province_core_section false, sourced true
```

Identical to the landed `c1-v1-at-3b960fe5.json` (whose per-carrier detail shows K2 failing **only** on `after_gaps_empty: false` with `after_oracle_hits 3/3` — precisely "one unpublished-entry gap", nothing else). The author verdict and every number the two files repeat are reproducible. Counter counter-note (not my scope): the frozen `frontier_note` binding is satisfied by the pre-existing round-36 line containing both "big-endian" and "superseded", not by the new note — a weakness of the frozen counter, not of the landed prose.

## Adjacent findings (NOT defects in PROVINCE.md / corpus/README.md — for the L1)

- **A1 — C2 verdict's cited receipt does not exist; the actual C2 score is uncommitted.** `corpus/lessons/round-38.md` ("R38-C2 is measured at the landing commit (`.ufo/waves/round-38/l1/scores/c2-final.json`)") and the SCORECARD R38-C2 row cite `.ufo/waves/round-38/l1/scores/c2-final.json`; `git log --all -- <that path>` is empty (never committed under any name) and no such file exists. The actual receipt is `.ufo/waves/round-38/l1/scores/c2-at-0fc61133.json` (the counter's own `--json-out`), which is **untracked** (`git status --short` → `??`) and absent from both 0fc61133's tree and HEAD (`git ls-tree` shows only the two c1 score files). This falsifies the lesson's own R37-CL1 sentence "every receipt this round cites is committed: … `.ufo/waves/round-38/l1/scores/` …". The C2 verdict's *content* is supported by the uncommitted receipt (mismatches 0, guards_ok, met_target true), and the reviewed README row cites no receipt path — so the two files under review are clean; the fix belongs to lesson-38.md/SCORECARD.md plus a commit of the score.
- **A2 — stale present-tense "unmeasured" at `PROVINCE.md:372`.** The round-36 Core row still reads "`sasquatch-v4be` is its big-endian sibling, unmeasured" while :157 now says BE v4 measured. Mitigating context: :372 is inside the dated `## Round-36 additions to Core` table; the first-freeze claims doc lists :372 as a C1 surface that moves only on promotion (C1 stopped, so it correctly did not move); the C2 counter passes with 0 mismatches. Observation only — a dated annotation (the lane's own kept-as-history pattern) would remove the present-tense staleness. Not introduced by this diff (the line is untouched pre-existing text).

## Residual risk / limits

- I did not re-run REA `extract-firmware` myself; the receipt numbers are verified against the committed receipts plus the frozen counter's own re-derivation (which recomputes evidence ids via the pinned xpin rule under rea-agents 6.5.0) — receipt *provenance* (independent re-run) is QUALITY 78's bar and was wave-1's exercise, not mine.
- The live unblob.org refetch matched S116's recorded digest exactly today; the entry's 180d recheck stands.
- Tooling record: no installs or upgrades performed (operator 2026-10-19 directive — nothing needed beyond preinstalled git, jq, curl, python3, node v24.21.0).
- Scratch `/fast/scratch/hyaku/kaidoku-r38/R38W2ProvinceReadme` removed after writing this report; cited bytes preserved in `.ufo/waves/round-38/w2/artifacts/R38W2ProvinceReadme/` (`prov-readme.diff`, `c1-counter-frozen.py`, `c1-v1-repro.json`, `formats.html`).
