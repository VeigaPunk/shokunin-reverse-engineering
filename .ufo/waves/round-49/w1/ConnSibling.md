# ConnSibling — round 49 wave 1 (pre-freeze): sibling-overlap scan

Seat: ConnSibling (connector, leaf, read-only). Lane: kaidoku-shokunin, base `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9`.
Receipt artifact: `.ufo/waves/round-49/w1/ConnSibling/sha256-receipt.txt` (UTC 2026-10-28T21:13:37Z; `sha256sum` exit 0 on all 25 listed files).
Nothing written outside this report and that directory. No sibling or draft counter was executed.

## Verdict

- **R49-C1 (SquashFS v1/v2): no sibling holds SquashFS, sasquatch, squashfs_v1/v2 or extract-firmware ground.** Zero SquashFS/sasquatch/squashfs_v1/v2/extract-firmware hits across all 21 sibling `corpus/knowledge/` trees and all 21 sibling `PROVINCE.md` files (the broader firmware/binwalk/unblob sweep finds only the adjacent items below). Adjacent firmware material exists (revenger C07, a manual readout that explicitly disclaims extraction). One **contested-scope** flag: firmware reverse-engineering ownership between kaidoku and revenger is still an open arbitration (tsukuroi ADJ-06, "integrator's call"). R49-C1 lands on kaidoku's existing round-4 firmware Core row (`PROVINCE.md:132`). Landing text must not claim firmware ownership, and should cite ADJ-06 as open.
- **R49-C2 (calibration): the method family is shared; the instrument is not.** Eight sibling lanes run a self-assessment-vs-repo counter or gate (kagi, souji, kama, tabi, kake, revenger, mori, tameshi). None reads the nine round-48 atoms. **The one place the same job is done:** revenger `corpus/self_assessment_check.py` ("Self-assessment mismatch checker (round-70 C2, calibration)"): it counts lane self-assessment mismatches against repo bytes and the git object store, exits 0/1/2, and its `--self-test` plants one defect per class, the same battery design as C2. Verdict: adjacent. Report, not absorb.
- **Draft hygiene (for L1):** `kaidoku-shokunin/.ufo/waves/round-49/draft/tools/round-49/__pycache__/` holds three `cpython-314` `.pyc` files (mtime 18:09–18:10 UTC today). Git treats them as ignored (`git status --porcelain --ignored` → `!!`), and `draft/mkclone.sh` strips them. A `git add` freeze will not take them; a `cp -r` freeze would. Delete the directory before the freeze commit.

## Method and controls

- Read the full plan first: `.ufo/waves/round-49/draft/plans/round-49-claims.md`, 170 lines, sha256 `984e1026…9f492`.
- Searches (grep tool; parameters recorded here, since the tool writes no receipt):
  - PROVINCE sweep: `(?i)squashfs|sasquatch|unblob|extract-firmware|firmware|binwalk|rea-agents` over `/home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md`.
  - Knowledge sweep, split into glob groups so output stayed bounded: `[a-h]*`, `k[eo]*`, `ku*`, `ka[gkms]*`, `[l-z]*` under `*-shokunin/corpus/knowledge/*.md`, pattern `(?i)squashfs|sasquatch|unblob|extract-firmware|binwalk|firmware-region`. Together the groups cover all 21 sibling lanes.
  - Self-assessment sweep: `(?i)self-assess` over the same knowledge globs and over `*-shokunin/corpus/README.md`.
  - Controls: `(?i)self-assess` over `k[eo]*` returned kotoba hits, and over `ka[gkms]*` returned kake and kama hits. The glob groups expand, so the zero-hit firmware results are real zeros, not expansion failures.
- Not run: no sibling tool or draft counter was executed. Exit codes recorded: `sha256sum` 0 on all 25 files; `ls` on the lane's draft tools 0; `sha256sum` on the `__pycache__` directory itself errors (`Is a directory`, not a file hash; the three `.pyc` files are the artifact). An `ls` for `kaidoku tools/freeze-drift.py` returned 2 (no such path), so no in-lane predecessor is cited at that path.

## Findings — R49-C1 (coverage)

| # | lane | path:line | overlap | verdict |
|---|---|---|---|---|
| A1 | all 21 siblings | `*-shokunin/corpus/knowledge/*.md` (4 glob groups) | Hits only game-dev-3d `corpus/knowledge/rea.md:36-39` (host tool presence: binwalk 3.1.0, unblob 26.6.4) and revenger (A2, A6). No SquashFS, sasquatch, squashfs_v1/v2 or extract-firmware anywhere. | none for SquashFS |
| A2 | revenger | `corpus/knowledge/round-64-firmware-region-byte-evidence.md:5,10,161,187-188,197-198,203` | Same REA verb family (`inspect-firmware-regions`, a saved Binwalk 3.1.0 record) on an authored zlib fixture. Explicitly "does not cover the REA `extract_firmware` route" (:5), has "No extraction, execution or re-analysis" (:198), and says it "does not absorb kaidoku Core's live `inspect-firmware-regions` / `extract-firmware`" (:203). | adjacent — report, not absorb |
| A3 | revenger | `corpus/README.md:47` (C07 held), `:76-79` | C07 "firmware images" held. Says REA `inspect_firmware_regions`/`extract_firmware` need caller-supplied Binwalk/Unblob; next probe is an authored fixture. | adjacent |
| A4 | revenger | `PROVINCE.md:3-7`, `:19-22` | Declares Owns: "reverse engineering of shipped artifacts … firmware", with Binwalk/Unblob listed as caller-supplied engines. Same firmware scope as kaidoku's Core row. | **contested scope** with kaidoku (see A5) |
| A5 | tsukuroi | `PROVINCE.md:51` (ADJ-06), and `## Round 49 — the ownership-source column now cites portable anchors` (≈ lines 297–321) | ADJ-06: "Driver/firmware/package mechanism requires shipped-artifact reverse engineering" — recipient "protocol integrator — kaidoku/revenger ownership unresolved". The round-49 note restates it: "the kaidoku/revenger ownership arbitration stays open (ADJ-06, integrator's call)". | **contested** — landing text: make no ownership claim; cite ADJ-06 as open |
| A6 | revenger | `corpus/knowledge/2026-10-12-rea-readiness-checklist.md:17,40-46`; `corpus/knowledge/seed.md:17,64-67` | Stale presence census of binwalk/unblob; "the firmware route is unprobed". Historical. | adjacent (no claim overlap) |
| A7 | game-dev-3d | `corpus/knowledge/rea.md:36-39` | Tool presence only (`binwalk --version`, `unblob --version`). | none |
| A8 | mori | `PROVINCE.md:12-13` | Driver/firmware *state* routed to tsukuroi. Host state, not artifact extraction. | none |

R49-C1 landing note: kaidoku's own Core already holds firmware extraction (`PROVINCE.md:132`, round-4 row; `:140`, AppImage payload; round-36/39/41/42 SquashFS rows). That is within-lane context, not a sibling overlap. What is new in R49-C1 is the promotion of `squashfs_v1`/`squashfs_v2` only, under the frozen carriers. The contested part is the ownership question in A4/A5, not the SquashFS scope.

## Findings — R49-C2 (calibration)

| # | lane | path:line | overlap | verdict |
|---|---|---|---|---|
| B1 | revenger | `corpus/self_assessment_check.py` (sha256 `82e59fce…0335cc`, 15,993 B), indexed `corpus/README.md:23` (sha `84b5627c…d3002e`) | **Same job.** Counts self-assessment mismatches re-derived from bytes and the git object store, in classes SM1–SM6. SM5 resolves SCORECARD commit citations (the same class as C2 atom A2, dead hash). SM6 re-derives a K-count. `--self-test`: one planted defect per class scores exactly that class. Exit 0 iff n=0, 1 if n>0, 2 if a file is missing. | **adjacent — the one place. Report, not absorb.** C2 has nine named atoms tied to the round-48 closure; revenger's has six general classes. Neither reads the other's files. |
| B2 | kagi | `corpus/self-counts.py` (sha256 `5b600f0a…a6654`), `corpus/README.md:172-175`, `PROVINCE.md:53` | Binds 38 current-tense numbers in SKILL/PROVINCE/README to live rows or ledger verdicts. Same job as C2's count atoms (A3, A8). | adjacent |
| B3 | kagi | `corpus/sources-census.sh` (sha256 `8d30d627…968a`), `PROVINCE.md:55` | SOURCES-CONTRACT-v1 registry census plus a citation handshake with knowledge entries. Source-row checks of the same kind as A6–A8. | adjacent |
| B4 | souji | `PROVINCE.md:285-289`; `census/round-39/c1-counter.py` (sha256 `65e42904…340ff`) | Its own sentence: "C1 binds the lane's own self-assessment to observed repo state and does not certify authorship." This is C2's job in almost the same words. | adjacent |
| B5 | tabi | `scripts/check-selfassessment.mjs` (sha256 `77b5c8ed…c6a9`), `corpus/README.md:584`, `:686` | "Self-assessment calibration": the lane's SCORECARD figures compared with the instruments that produce them. `--selftest` 41 cases. | adjacent |
| B6 | kama | `corpus/knowledge/self-assessment-at-writing.md` (sha256 `cd6e3730…f959`), `PROVINCE.md:120-124`; counter `.ufo/waves/round-29/count-c1.py` (not hashed) | Checks each self-assessment statement against the revision that wrote it (`git blame --line-porcelain`), separating mismatch-at-writing from later drift. Overlaps C2's record-vs-evidence comparison for A1/A9. | adjacent |
| B7 | mori | `tools/mori-freeze-order.py` (sha256 `ec1be305…27b547`), `PROVINCE.md:132-133`, `corpus/README.md:397` | Judges the lane's own claim labels against commit order. Same job as C2 atom A1 (declared-freeze header). | adjacent |
| B8 | kake | `corpus/knowledge/claim-count-derivation.md:7-9`, `corpus/README.md:32` | Every count in a self-assessment document must name its revision and re-derive from committed bytes. Same rule as C2. | adjacent |
| B9 | chousa | `corpus/knowledge/audit-r11.md` (sha256 `7d9c486ad53ad3ae5525c38c93e62b53c5d22e1a00ab4ccc95ab3c9dd42aeca5`), lines 47–49, 69–70, 194 | Pointer audit: row C3 cites `:76` but its span occurs at `:86`. This is the locator-defect class of C2 atoms A6/A7. An audit, not a counter. | adjacent |
| B10 | tameshi | `corpus/README.md:458-462`; `corpus/knowledge/executable-self-assessment.md` | Executable self-assessment rows, calibration C1 over 12 frozen rows. Same job as C2 at a different object. | adjacent |
| B11 | kotoba | `corpus/knowledge/writing-revision-calibration-round61.md:17` | Practice-level borrowing from kama only. No counter. | none |
| B12 | 7 sibling lanes | kaidoku `corpus/SOURCES.md:144-154` vs kake `:146-148`, kama `:150-160`, kengaku `:153-165`, mado `:150-163`, mori `:144-156`, tabi `:152-164`, kotodama `:166-180` | Source ids S138–S148 name different sources in each lane. Ids are per-lane homonyms. C2 counts only kaidoku-local rows, so there is no collision. | none for the counter; landing text should keep ids lane-local |

**Same-job pairs, stated once:** C2's counter and revenger's `self_assessment_check.py` both re-derive a lane's own claims from committed bytes and count the mismatches. This is the one place. Neither should absorb the other. C2 is not the fleet's first self-assessment counter (kama r29, tabi r24, souji r39, kagi r25, revenger r70 — per-lane round numbers, not a global order). What C2 adds is a fixed nine-atom list tied to the round-48 closure and a do-nothing overlay.

## Hygiene and contract items for L1

- **H1 (low):** `.ufo/waves/round-49/draft/tools/round-49/__pycache__/` (`c1-counter.cpython-314.pyc`, `c1-run.cpython-314.pyc`, `c2-mismatch.cpython-314.pyc`). Gitignored, so a `git add tools/round-49` will not stage it. A copy-based freeze would. Delete before freeze. `mkclone.sh` already does `rm -rf "$D/tools/round-49/__pycache__"`.
- **H2 (info):** The plan's freeze list includes `tools/round-49/` as a byte-frozen directory. Drafts sit untracked (`git status` → `??`) and that is expected. No freeze-blocking defect found in the drafts from this seat's scope.

## Tooling

No tools installed or upgraded. Read-only `sha256sum`, `ls`, `git status`/`rev-parse`/`cat-file` only. No scratch directory was created.

Report: `.ufo/waves/round-49/w1/ConnSibling.md` (this file). Receipt: `.ufo/waves/round-49/w1/ConnSibling/sha256-receipt.txt`.
