# W2C1Stale — stale SquashFS v1/v2 Frontier sentences at `29883d4e`

**Verdict: NOT CLEAN.** Two living coverage-map sentences still say standard SquashFS v1/v2 stay Frontier, with no dated supersession on those sentences. The Core rows that should close them cite `.ufo/waves/round-49/l1/scores/c1-final.json`, and that path is absent at this revision. PROVINCE's older notes are superseded by name at line 438. LOG, lessons, and the round-44 knowledge entry are append-only history.

Revision read: `29883d4ec35a31a8393c4ffb220888c44c0bb022` (lane `main`). Freeze ancestor `decc5697bfd4ec1e9de4a762ad199d9bd9c4230d` (merge-base exit 0). Data commit `4aabb0b4bf716fb564c8406509c40b0a67457800` is an ancestor (exit 0). Bytes from `git show` / `git grep` / `git cat-file`, not the worktree. Counters not re-run (not this seat's attack).

Axes: coverage of every mandated hit; depth of each Frontier-status sentence against a dated supersession; calibration so history is not filed as a live repair.

## Findings

| file:line | sentence | repair needed? |
|---|---|---|
| `corpus/README.md:104` | Coverage-map cell, present tense: "**Measured, not promoted** — … the score is not admitted and v1/v2 remain Frontier". | **Yes.** Row `:105` says **Core** and does not say it supersedes this status. Knowledge row `:226` supersedes the round-44 *entry*, not this cell. Round-39's own pattern (row `:93` "supersedes the round-38 Frontier status") is missing here. Keep `:104` as the round-44 outcome; add a dated supersession on `:105` (or on `:104`). |
| `corpus/README.md:101` | Round-42 Core cell, present tense: "v1/v2, broadcom/nonstandard and gzip v3 stay Frontier". | **Yes, the v1/v2 token only.** Nothing names this cell. `PROVINCE.md:438` names the round-42 *frontier note*, and `README.md:278` names the round-44 bullet, not this row. Broadcom and gzip v3 stay Frontier (plan limit 5). Same leftover shape as row `:93` still saying AVM-BE stays Frontier after round 41; that precedent is why this is a one-token pointer, not a row rewrite. |
| `PROVINCE.md:436`, `corpus/README.md:105`, `corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md:3` and `:13` | Each cites `.ufo/waves/round-49/l1/scores/c1-final.json` as the score at the landing revision. The entry's promotion sentence is conditional: "moved to Core … if and only if the counter is met at the landing revision (`…/c1-final.json`)". | **Yes.** At this revision `git cat-file -e` exits 128; `git ls-tree` of `.ufo/waves/round-49/l1/scores/` lists only `c1-at-data-4aabb0b4.json`. That receipt is `carriers_matched 4`, `failing []`, `frozen_path_changed []`, `met_target false`, `exit_code 1`, documentation bindings false (expected before the entry existed; the entry says so). The cited counter sha256 `ac83715b199100774873389ea33fb4819231e1f963225416e86ad422f69d287f` matches that data receipt. Commit the landing score, or stop citing a path that is not in `29883d4e`. Not a counter patch. |
| `LOG.md:3451` | Heading, and the section ends at `:3455`: "## 2026-10-28 — round 49 (KaidokuR49): one freeze, controls scored, data not yet run". | **Append, do not rewrite.** False at this revision: data commit `4aabb0b4` is an ancestor, and `LOG.md` was last touched by `76d7ad6f` ("controls scored at the freeze"), before `4aabb0b4` and before landing `3847f393`. The claims bullet at `:3454` ("Frontier → Core") is the claim direction, not a "remains Frontier" status. Older LOG lines below stay `history, no repair`. |
| `PROVINCE.md:416` | "Still Frontier: SquashFS v1/v2, `squashfs_v3_broadcom`, …" (round-42 frontier note, 2026-10-26). | **No.** `:438` (2026-10-28) names "the v1/v2 clause of the round-42 frontier note". Other families in the same sentence stay Frontier. |
| `PROVINCE.md:424` heading, `:428`, `:430` | "## Round-44 measured, not promoted"; the row "no Core promotion is claimed"; "SquashFS v1/v2 remain Frontier pending a new pre-data freeze…". | **No.** `:438` names "the SquashFS v1/v2 status of the `## Round-44 measured, not promoted` section and of the round-44 frontier note" and the words `measured, not promoted`. The non-v1/v2 "Still Frontier" tail of `:430` is repeated as still-Frontier at `:438`. |
| `corpus/README.md:277` | "SquashFS v1/v2 was measured on four standard fixtures but **remains Frontier**". | **No.** `:278` (2026-10-28): Core, "superseding the round-44 line above." |
| `corpus/README.md:271` | Round-42 bullet: "Still frontier: v1/v2, `squashfs_v3_broadcom`/`_nonstandard`, gzip v3." | **No.** Dated 2026-10-26 append-only bullet. `:278` is the current sasquatch bullet and names `:277`, not `:271`. Same leftover shape as `:266` (BE still listed frontier). Do not rewrite. |
| `corpus/README.md:225` | Knowledge index: "not promoted … no Core claim". | **No.** `:226`: "supersedes the round-44 not-promoted entry". |
| `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:1`, `:9`, `:162`, `:212` | Title "R44-C1 not promoted"; "no Frontier→Core promotion is claimed"; "the v1/v2 families remain Frontier pending a new pre-data freeze"; "these families remain Frontier under the R44-C1 honest stop." | `history, no repair`. Older entry. Supersession is `README.md:226` and the round-49 entry. v2-nonstandard / broadcom / gzip-v3 bullets in that file stay Frontier and are still true. |
| `LOG.md:3198`, `:3201`, `:3218`, `:3224`, `:3227` | Round-44 ledger: "measured 4/4 but not promoted"; "squashfs_v1/squashfs_v2 stay Frontier." | `history, no repair`. True of round 44. |
| `LOG.md:3231`, `:3291`; `SCORECARD.md:3568-3569`, `:3644-3645`, `:3743` | "resume the SquashFS v1/v2 promotion" inside round 44/45/46/48 planned-next lines (R44-CL2). | `history, no repair`. Forward looks, not a current "remains Frontier" sentence. Round-49's SCORECARD text (`:3751-3755`) records only the A9 calibration correction and does not mention the promotion. Not a false Frontier sentence; no capability row was part of the landed correction section. |
| `corpus/lessons/round-44.md:1`, `:36`; `corpus/lessons/round-44-verifier-spotcheck.md:63-64` | Round 44 "measured 4/4 but not promoted" / "measured, not promoted". | `history, no repair`. Lessons were outside the mandated pathspec; supplemental grep only. |
| `SKILL.md` (11 mandated hits), `SHONEN.md` | No sentence says v1/v2 is Frontier, measured-not-promoted, or remains Frontier. SKILL hits are handler names, triage markers, or calibration "v1/v2". SHONEN's "measured but not promoted" is round-40 AVM, not v1/v2. | **No.** Absence of a round-49 line in SHONEN is not a false Frontier claim. |
| `plans/round-42-claims.md`, `plans/round-44-claims.md`, `tools/round-49/**` including `control-fixtures/pos/**` | Frozen plans and the positive-control corpus copies still contain "Still Frontier" / "remain Frontier" beside the round-49 supersession note. | **No.** Frozen. Not living status. |

`squashfs_v2_nonstandard`, `squashfs_v3_broadcom` / `_nonstandard`, gzip v3, v4 Broadcom, LE AVM (`hsqs`), AVM kernels, and nested sub-images below depth 1 are still Frontier in `PROVINCE.md:438`, `README.md:105` and `:278`, and the round-49 entry. Those sentences match plan limit (5). Not findings.

## Commands

Disk guard before the grep: `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status`, exit 0. `/fast/scratch/hyaku` 37% used, 513.5G free. No package installed.

Mandated grep, `GIT_NO_REPLACE_OBJECTS=1`, UTC `2026-10-28T22:39:42Z`, exit 0, 768 matching lines, stdout sha256 `d6ef73d8735408f7fc86f3b5bcf7f9514300ded00d9205c3e47be9988c64abf9`:

```text
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin grep -n -i -E 'squashfs[_ ]v1|squashfs[_ ]v2|SquashFS v1/v2|v1/v2' 29883d4ec35a31a8393c4ffb220888c44c0bb022 -- ':!.ufo' ':!corpus/evidence' ':!corpus/lessons'
```

77 files. Bulk is frozen tools, carriers, and control fixtures (`tools/round-49/carriers.json` 72, `tools/round-44/carriers.json` 72, the two `c1-counter.py` files 48 each). Living non-tool hits extracted to `live-hits.txt` (127 lines). Full stdout: `W2C1Stale/grep-mandated.stdout`.

Supplemental, same rev, exit 0 unless noted:

| utc | command | exit | stdout sha256 |
|---|---|---|---|
| `2026-10-28T22:37:38Z` | `git grep -n -i -E 'squashfs\|SquashFS\|v1/v2' REV -- SHONEN.md`, then `frontier` on `SHONEN.md` | 0, 0 | `d164a688d05b511efbc8e92a535a5aedd9cd15b43da6b68455657e10b6879fdc` (`grep-shonen.txt`, includes the utc header) |
| `2026-10-28T22:37:38Z` | `git grep -n -i -E 'still frontier\|remains frontier\|remain frontier\|measured, not promoted\|not promoted\|stays frontier\|stay frontier' REV -- SKILL.md SHONEN.md SCORECARD.md PROVINCE.md corpus/README.md corpus/SOURCES.md corpus/knowledge LOG.md` | 0 | `5ffdb804a9973586887c7411d581a9818b4620bd0388e93f8a8b59d2cc627625` |
| `2026-10-28T22:38:40Z` | same family pattern restricted to `corpus/lessons` | 0 | `cf4df54d25d006bed878577e7e3502f832b73995c326610776d6e2359a90b35e` |
| `2026-10-28T22:38:50Z` | `git grep -n -E 'R44-CL2\|resume the SquashFS v1/v2\|v1/v2 promotion' REV` on the living docs plus lessons | 0 | `66037bcd6af53fee0a7171b12c7480f227951b9f839fa5a7e3b1ca4b2e061708` |
| `2026-10-28T22:40:18Z` | `merge-base --is-ancestor` freeze and data vs REV; `git log --oneline FREEZE..REV`; `git grep -F 'data not yet run'` at data and REV | ancestor checks 0; both greps hit `LOG.md:3451` | `dd2458e05c1c797965d75b5ccc8597ba02ea2bdcadc828608ab92cd79d566bf6` |
| `2026-10-28T22:41:00Z` | `git cat-file -e REV:.ufo/waves/round-49/l1/scores/c1-final.json` | 128 (absent) | `e6d5bbe04516c3fc550bc86b06e11dfbf6bad8a46428fb671ea8ec3176428ee3` |
| `2026-10-28T22:41:10Z` | `git ls-tree` of the scores dir; `git show` of `c1-at-data-4aabb0b4.json` key extract | 0 | `55252ce48bc8134e3101f719a4695c2bd2363177f5ad00c657b8f0c93f8c2d95` |

Not run: `tools/round-49/c1-counter.py`, `tools/round-49/c2-mismatch.py`. The data-commit score was read from the git blob, not produced by a new REA run.

Receipts: `.ufo/waves/round-49/w2/W2C1Stale/` (`receipts.sha256`). Scratch `/fast/scratch/hyaku/kaidoku-r49/W2C1Stale` removed after the copy.
