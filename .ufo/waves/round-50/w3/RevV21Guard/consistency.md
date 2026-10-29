# Four-file consistency matrix — SquashFS family wording

Seat RevV21Guard, round 50 attempt 2, wave 3 (build). Read-only review; no lane edits.
Measured tree: lane `HEAD 6f4aba63`; contract base `f890bbead20ca2c549487167f56876ae47f1e1a4`.
`git diff f890bbea HEAD --name-only` → `plans/round-50-attempt2-claims.md` only, so the four
target files are byte-identical at base and HEAD (receipt `git-base-head-stat`).

## The five surfaces

| # | Surface | Locus |
|---|---|---|
| S1 | `SKILL.md` decision table | `:57` `Firmware blob`; `:58` `SquashFS v1.0/v2.0` (added in `5855962d`, wave-2 repairs) |
| S2 | `SKILL.md` rule blocks 19–21 | triage tables v2/v3/v4 (`<!-- sqfs-triage-table v{2,3,4} -->`); block 21 = table v4, `:458-544`, marker at `:525-527` |
| S3 | `PROVINCE.md` | round-4 sasquatch bullet `:156-157`; round-36/38/39/40/41/42/44/49 sections and frontier notes `:374-438` |
| S4 | `corpus/README.md` | coverage map `:89-105`, knowledge index `:210-226`, frontier list `:265-278` |
| S5 | `corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md` | the round-49 Core entry; reader census under "What stays Frontier, and why" |

File sha256 at HEAD (receipt `file-sha`, relative-path stdout also in `receipt-file-sha.stdout`):
SKILL.md `19046cf204ce999e5dccb1ebe86eebe9921e84ded8443dd87abc5a693fd8c974` ·
PROVINCE.md `d8425c0a99730986b0ebf0ad04338a8dd054ac003b271c8fa69d482c940a01f1` ·
corpus/README.md `a702bfdd6a32b89427d672b4522878742810e21dbe3f6db2b36c60268e1d2274` ·
knowledge `e320ecb3e024eefbaab1e3fa0e99b237f8e8d7a3e632002d51637760a1f855ec`.

## Matrix — per family, per surface

Status words are quoted or condensed from the cited cell. "—" = the surface says nothing.

| Family | S1 SKILL decision | S2 SKILL blocks 19–21 | S3 PROVINCE | S4 README | S5 r49 entry | Verdict |
|---|---|---|---|---|---|---|
| v1.0 (`squashfs_v1`) | "SquashFS v1.0/v2.0 (standard, gzip) … held r49 on four fixtures" (`:58`) | v2/v3 tables: no handler cell matches (`squashfs_v4_*` only) → `unclassified`; v4 routes reader-backed (`squashfs_*`; legacy glob matches; unsquashfs reads) | Core, r49 row names "the four standard v1.0/v2.0 fixtures" (`:436`) | Core, "v1.0 le/be" (`:105`) | Core 4/4; carriers `v1le`/`v1be` | CONSISTENT (Core) |
| v2.0 (`squashfs_v2`) | same row (`:58`) | same routing; recon `squashfs_v2_squashfs_v2.0_{le,be}_ddefault` → `clean`/`none` | Core (`:436`) | Core (`:105`) | Core 4/4 | CONSISTENT (Core) |
| v2.1 (handler `squashfs_v2`, `s_minor` 1) | "v2.1 … stay frontier" (`:58`) | tables key on handler name, not `s_minor`; a v2.1 body routes exactly like v2.0 (recon `…v2.1_{le,be}_ddefault` → `clean`/`none`) | "no v2.1 image was measured" (`:436`); "v2.1 images (the handler pattern admits `s_minor` 1; nothing measured) stay Frontier" (`:438`) | "v2.1 images" in still-frontier list (`:278`) | Correction 4: handler matches `s_minor` 1, readers read the pair, REA never ran, no carrier | CONSISTENT (frontier/unmeasured); S2 routes by handler — a reader must apply the S1/S3 scope |
| v2ns (`squashfs_v2_nonstandard`) | "no second reader … stay frontier — the v4 triage table (block 21) does not apply to them" (`:58`) | block 21 routes it: `legacy-body-failure` failing-handler glob `squashfs_v[123]*` matches; `clean` row gives the oracle action `none`; 4 committed `*_ddefault` envelopes label `clean`/`none` | Frontier (`:438`, `:430`, `:416`) | Frontier (`:278`, `:277`, `:271`) | Frontier; **no independent reader** (`unsquashfs` exit 1, `7z` exit 2); 2-byte magic diff from v2 | CONTRADICTS — C-A, C-B, C-C |
| v3 (`squashfs_v3`, LZMA) | — | v4 routes reader-backed; recon `squashfs_v3_adaptive_*_ddefault` → `clean`/`none` | Core, r42 row (`:414`); r42 note (`:416`) | Core (`:101`) | Core (cross-ref); LZMA v3 fixture refused by `unsquashfs` — round-42 oracle was backhand-cli + 7-Zip | CONSISTENT (Core) |
| v3_ddwrt (`squashfs_v3_ddwrt`, LZMA) | — | v4 routes reader-backed (Core family) | Core (`:414`); r49 note keeps "the DD-WRT no-pad/4k-pad v3 images" Frontier (`:438`) | Core (`:101`); no-pad/4k-pad frontier (`:278`) | LZMA Core; "v3_ddwrt's no-pad fixture: both readers refuse … Frontier, unchanged"; correction 4 names no-pad/4k-pad Frontier | CONSISTENT; block-22 narrowing must keep `squashfs_v3_ddwrt` reader-backed |
| gzip v3 bodies | not named (`:58` covers only v1/v2 + the three no-reader families) | v4 routes via `squashfs_v[123]*` (reader exists per S5) | Frontier (`:438`, `:430`, `:416`) | Frontier (`:278`, `:277`, `:271`) | "reader exists … stays Frontier because the round-42 Core row covers LZMA v3 … no round-49 REA receipt" | CONSISTENT (frontier); S1 omission only |
| v3_broadcom (`squashfs_v3_broadcom`) | "v3 Broadcom/non-standard stay frontier" (`:58`) | block 21 routes it (C-A/C-B); **7** committed `*_ddefault` envelopes `clean`/`none` | Frontier (`:438`, `:430`, `:416`) | Frontier (`:278`, `:277`, `:271`) | Frontier; **partial reader**: `unsquashfs` refuses, `7z` lists the LE fixture (2 files, 13 B); no REA outcome measured | CONTRADICTS — C-A, C-B (+C-F wording) |
| v3_nonstandard (`squashfs_v3_nonstandard`) | "v3 Broadcom/non-standard stay frontier" (`:58`) | block 21 routes it (C-A/C-B); **8** committed `*_ddefault` envelopes `clean`/`none` | Frontier (`:438`, `:430`, `:416`) | Frontier (`:278`, `:277`, `:271`) | Frontier; both readers refuse | CONTRADICTS — C-A, C-B |
| v4 std LE (`squashfs_v4_le`) | covered only by `Firmware blob` row (`:57`, "held r4u") | v4 family rows (dep-LE, clean, …) | Core, r36 section + note (`:371-376`); r36 SKILL section `:1557-1576` | Core (`:89`, `:210`, `:265-266`) | not this entry's subject | CONSISTENT (Core) |
| v4 std BE (`squashfs_v4_be`) | — (same `Firmware blob` row) | v4 family rows (dep-BE, avm-marker-be-dropped, body-extractor-failure) | Core, r39 row + note (`:382-384`) | Core (`:93`, `:214`, `:268`) | not this entry's subject | CONSISTENT (Core) |
| AVM-BE (`squashfs_v4_be`, AVM layout) | — | v4 AVM rows; layout pre-check (`:493-516`) | Core, r41 row + note (`:400-408`); r40 measured-not-promoted superseded | Core (`:97`, `:218`, `:270`) | not this entry's subject; BE layout ≠ LE subject | CONSISTENT (Core) |
| AVM-LE (`hsqs`, v4.0 xz, `mkfs_time == bytes_used`) | — (no cell) | v4 LE rows apply; the marker is untested on LE (S245: `is_avm` sits in the BE branch only) | **Frontier** in every note: r41 (`:408`), r42 (`:416`), r44 (`:430`), r49 (`:438`) | **Frontier** (`:269`, `:270`, `:277`, `:278`) | "LE AVM members (`hsqs`) … unchanged from the round-41/42 notes; nothing was measured" | CONSISTENT today; R50-C1 lands four pinned members → must stay scoped (F-1/F-2 below) |

## Contradiction register

- **C-A (HIGH; W2Skill F1, routed, unfixed at base).** `SKILL.md:536` `legacy-body-failure` row: failing-handler glob `squashfs_v[123]*` matches `squashfs_v2_nonstandard`, `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`; its cross-read rule ("if the independent readers fail where sasquatch failed the body is damaged and the failure stands") condemns a healthy no-reader body — reader failure there is guaranteed by definition. Reproduced by reading the row; the r49 entry reader census is the authority for "no independent reader".
- **C-B (MEDIUM; W2Skill F2).** `SKILL.md:543` `clean` row action `none` is oracle-backed ("match files to the oracle by exact relative path and sha256"). Committed round-42 recon corpus carries **19** no-reader `_ddefault` envelopes labelled `clean`/`none` — 4 v2ns (`squashfs_v2_nonstandard_squashfs_v2.{0,1}_{le,be}_ddefault`), 7 v3_broadcom, 8 v3_nonstandard (receipt `noreader-clean-count`: `{'squashfs_v2_nonstandard': 4, 'squashfs_v3_broadcom': 7, 'squashfs_v3_nonstandard': 8} total 19`) — while S3/S4/S5 hold all three families Frontier. W2Skill quoted the 4 v2ns rows; the corpus extends the same defect to broadcom/nonstandard (15 more rows). This is exactly the C3 claim's F1/F2; v5 is the fix.
- **C-C (MEDIUM).** `SKILL.md:58` says the v2ns/v2.1/v3-broadcom/nonstandard families "stay frontier — the v4 triage table (block 21) does not apply to them", but block 21's grammar (`handler` glob `squashfs_*`, failing-handler glob `squashfs_v[123]*`) does route them. Two SKILL surfaces disagree about which table applies; the sentence needs a bracketed update when block 22 lands (F-11).
- **C-D (LOW; W2Skill F5 residual).** `SKILL.md:57` `Firmware blob` status "held r4u" carries no per-family SquashFS pointer; a reader routing a SquashFS image through `:57` sees one `held r4u` verb. Row `:58` (added `5855962d`) sits directly below and compensates; `:57` itself unchanged since the r49 landing.
- **C-E (LOW).** `corpus/README.md:44` (2026-10-13 firmware row) "squashfs needs sasquatch (7z fallback)" — already carries its own bracketed 2026-10-26 supersession; keep the round-50 LE-AVM wording from reviving a "7z fallback" route statement.
- **C-F (LOW, wording).** The C3 claim text calls all three families "no independent second reader … per the round-49 entry's reader census", but the census (S5 `:103`) records a **partial** reader for v3_broadcom (`7z` lists the LE fixture). Block 22 must phrase broadcom as "no independent reader (a 7-Zip listing is corroboration, not an oracle)" or it contradicts S5 — and W2Skill F9 records the listing-vs-damage hazard.

## W2Skill F3 verification — the landed PROVINCE row (the seat's named check)

Claim checked: the row fixed for F3 scopes v1.0/v2.0, names the v2.1 exclusion, and carries a Use/expect command and a refusal signature.

- **At the attempt-1 landing `3847f393` the row was still the F3 defect**: "`squashfs_v1` and `squashfs_v2` (SquashFS v1 and v2, gzip bodies, both byte orders)" — unscoped, S108 refs, probe cell naming the counter only (receipt `province-row-at-landing`; matches W2Skill F3/F4 quotes).
- **The fix landed one commit later, in `5855962d` "round-49: wave-2 repairs"** (receipt `git-fourfile-commits`: only `5855962d` and `11ccdb72` touch the four files since `3847f393`; `11ccdb72` = +12 SKILL.md registry rows only). So "fixed at the attempt-1 landing" is accurate at the round-49 tip, **not** at the landing commit itself.
- **Current row (`:436`, byte-identical base..HEAD) — all four properties verified, quoted from receipt `province-row-current`:**
  1. Scopes v1.0/v2.0: "— SquashFS v1 and v2 on the four standard **v1.0/v2.0** fixtures (gzip bodies, both byte orders; 4 KiB each); **not** every v1/v2 image, and **no v2.1 image was measured**".
  2. v2.1 exclusion also in the frontier note (`:438`): "v2.1 images (the handler pattern admits `s_minor` 1; nothing measured) stay Frontier".
  3. Use command: "**Use:** `npx -y rea-agents@6.5.0 extract-firmware --format json --full-output <image> <outdir>` with `sasquatch` 4.5.1 on the child `PATH`".
  4. Expect: "**expect** one chunk whose `handler` is `squashfs_v1` or `squashfs_v2`, `extraction_gaps == []`, and every regular file of `unsquashfs -lls` published under `firmware.bin_extract/` with the same sha256".
  5. Refusal signature: "**refusal signature** without sasquatch: a `missing-extractor-dependency` gap naming `sasquatch` and no published member (round-36 receipts)".
- Verdict: **F3/F4 CONFIRMED FIXED** — in wave-2 repairs `5855962d`, present and byte-unchanged at base `f890bbea` and HEAD.

## Where the attempt-2 landings must NOT contradict

### C1 landing (entry `2026-10-28-r50-avm-le-squashfs-core.md` + PROVINCE/README round-50 rows)

- **F-1 (scope).** All four surfaces today say "LE AVM members (`hsqs`)" Frontier (matrix row above). The entry draft's "What moved, and only what moved" already states the right shape: the four pinned members are the carriers, **the class itself stays Frontier**. The PROVINCE round-50 frontier note must carve only the four members out of the r49 "stay Frontier" list; the r49 note's own words are "…and **nothing else**" (`:438`), so the round-50 note must do its own explicit, dated supersession of the AVM-LE clause only, leaving `squashfs_v2_nonstandard`, `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`, gzip v3, v4 Broadcom, AVM kernels and nested sub-images listed as Frontier.
- **F-2 (counter-pinned strings).** `tools/round-50/c1-counter.py:377-380` pins `ENTRY/STEM = 2026-10-28-r50-avm-le-squashfs-core`, `CORE_HEADING = '## Round-50 additions to Core'`, `FRONTIER_MARK = 'Round-50 frontier note'` (verified by grep at HEAD). The PROVINCE row and README row must use exactly these marks/stem/date (`opened` is `2026-10-28`, attempt-1 date, per the claims doc — do not "fix" it to 2026-10-29).
- **F-3 (marker wording).** The entry (and S245) establish the AVM marker is tested only in unblob's **big-endian** v4 branch and is re-stampable; the PROVINCE/README rows must not claim "REA recognises AVM" — the claim is "publishes every oracle file of these four pinned members", not origin detection.
- **F-4 (budget/depth scope).** xz-only, `--max-depth 1`, raised budgets — consistent with the r41 note's depth framing; must not generalise to "LE AVM images extract" (the 7530/7590 13k-file members are documented as dropped on the 120 s `provider_timeout`).
- **F-5 (licence).** Vendor bytes are never committed (S249, one backup copy); rows must present the carriers as chain-pinned and fetched, never lane-resident.
- **F-6 (Still-Frontier list).** The entry's Still-Frontier list matches S3/S4/S5 today; the round-50 PROVINCE note must not drop or promote any of those items.

### C3 landing (SKILL rule block 22 + `tools/round-50/sqfs-triage-v5.py` + registry row)

- **F-7 (history preservation).** Block 21 stays as history (the claim says so); it is load-bearing for the round-42/43 frozen counters and the R43 score receipt — do not edit it in the C3 commit, or round-42/43 recheck counters break.
- **F-8 (labels).** `clean-unverified`/`record-unverified` and `no-reader-failure`/`preserve-unresolved` are new tokens outside the v1–v4 action vocabulary (`sqfs-triage-actions` lines); the single new instrument-registry v2 row must record them and the narrowed glob (B9 coupling: exactly one new `.py` row, no other `.py`/`.sh` under `tools/round-50/`).
- **F-9 (narrowing).** `legacy-body-failure`'s failing-handler cell narrows to the reader-backed v1–v3 families (`squashfs_v1`, `squashfs_v2`, `squashfs_v3`, `squashfs_v3_ddwrt`) — it must keep matching all four (v1/v2 Core r49; v3/v3_ddwrt Core r42) and drop only v2ns/v3broadcom/v3ns.
- **F-10 (broadcom wording).** Per C-F: "no independent reader" needs the partial-reader parenthetical or S5's census is contradicted.
- **F-11 (SKILL `:58`).** Add the bracketed pointer to block 22 (or rewrite the sentence) when block 22 lands, else C-C stands inside SKILL itself.
- **F-12 (before-state honesty).** The 19 committed `clean`/`none` no-reader envelopes are facts about table v4; block 22 presents v5 as changing the table's answer, never as the envelopes being wrong. Calibration: the C3 before-run over the held-out dir should show the evaluator's actual mismatches — measured here as **19** no-reader `clean`-row envelopes (claim text says "≥4 … incl. the four v2ns rows", true but a floor, not the count).
- **F-13 (held-out dir).** The frozen held-out dir is **126** committed envelope dirs (verified: `ls envelopes | wc -l` = 126, `git ls-tree -r HEAD … | wc -l` = 126). The sibling `a1-out.jsonl` has **135** rows — 9 not backed by a committed envelope dir; the counter must enumerate the dir, not the jsonl.
- **F-14 (non-promotion).** v2ns/v3broadcom/v3ns stay Frontier in every landed text; block 22's `clean-unverified` wording must not read as a capability claim (matches README `:105` "stays Frontier (no independent reader)").

## Calibration notes for the L1

- SKILL.md:523 still calls table v4 "unscored"; the R43 score (`2026-10-27-r43-sqfs-triage-v4-scored`, 78/78) exists in S4/S5. Stale but pre-existing (W2Skill F8) — flag only, any block-22 landing may fix it in passing.
- S1 uses "held r49" where S3/S4 say "Core" — lexical convention of the decision table, not a contradiction.
- The v4 `legacy-body-failure` cause text says unsquashfs "reads 1:0-3:0 (measured on the v1, v2 and v3 fixtures this wave)" while S5 records `unsquashfs` refusing the LZMA v3 fixture (round-42's v3 oracle was backhand-cli + 7-Zip). The cross-read's "and with 7-Zip" branch is what read those; block 22's reader-backed wording should keep both branches named.

## Receipts

All commands, exit codes, stdout sha256s, UTC timestamps: `receipts.tsv` (20 rows, all exit 0) with raw stdout in `receipt-*.stdout` beside it. Disk guard before the pass: `disk-guard` receipt, exit 0.
