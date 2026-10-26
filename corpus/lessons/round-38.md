# Round 38 — BE SquashFS v4 measured but stopped under its first freeze; a frozen rule edited after scoring is not the rule

Base `77091b492cc53f8743bd0701b1e7d5e66123dd84`. First freeze `e059ca9391642d5b71b6662cabcbdce0d9308719`
(claims doc, both counters and selftests, harness, carriers, instrument map, census start). Control
receipts `efd5c47a72a50b3a434783f82268fb4a96e636a1` (7 controls, all exit 1). Attempt 1 (L1
`KaidokuR38`) ran wave 1 (40 seats, `.ufo/waves/round-38/w1/`, manifest
`.ufo/waves/round-38/r38-w1-results.json`) and died at 03:37:05 without a report. Attempt 2 (L1
`KaidokuR38a2`) re-verified the inherited bytes, landed `3b960fe5` and `0fc61133`, ran wave 2
(44 seats, `.ufo/waves/round-38/w2/`) against them, and landed the corrections in the round's final
commit.

Verdicts, judged by the first-freeze bytes:

- **R38-C1 honest stop.** `carriers_matched 3`; K2 fails on one `unpublished-entry` gap
  (`.ufo/waves/round-38/l1/scores/c1-v1-at-3b960fe5.json`). Wave-2 seats reproduced the score
  (`w2/R38W2C1RescoreV1.md`), the rule choice (`w2/R38W2C1RuleChoice.md`) and every receipt
  payload (`w2/R38W2ReproK{1,2,3,4}.md`). The before/after receipts in
  `corpus/evidence/round-38/c1/` were written by attempt 1 at 03:31, after its v2 amendment. The
  first-freeze counter reads only the after receipts, and the independent re-runs gave identical
  payloads, so the timing changes no number. It is still disclosed.
- **R38-C2 met by its frozen counter** (`.ufo/waves/round-38/l1/scores/c2-at-0fc61133.json`;
  the final-commit re-measure is named in the report). Wave 2 showed that the counter accepts a stub
  written at the unresolved path with no self-assessment edit (M38-6), so the counter alone does not
  verify the claim. Two other checks carry it: an independent re-derivation stricter than the
  counter (`w2/R38W2C2Rederive.md`, CONFIRMED), and `tools/round-38/intended-doc.py`, which prints
  `bound` for the landed repair and `not-bound` for the base and for the stub shortcut.

## Mistakes

| id | class | evidence | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| M38-1 | freeze integrity — attempt 1 amended a frozen predicate and counter after seats had scored, and called the amendment "pre-scoring" | `git log e059ca93..077e212b -- plans/round-38-claims.md tools/round-38/c1-counter.py` lists `79f69347` (03:30:33, predicate + counter) and `f1010f67` (03:32:55, counter: gaps other than `missing-extractor-dependency` stop failing). Before both, a seat had run the first-freeze counter on K1 receipts (`.ufo/waves/round-38/w1/R38ExecAfterK1.md` §2e, frozen sha `a7a62b09…`), and K2's symlink gap had been reported (`R38ExecAfterK2.md` lines 7-11). The v3 counter turns K2 from fail to pass: 3/4 → 4/4 on the same receipts (`.ufo/waves/round-38/l1/scores/c1-v{1,3}-at-3b960fe5*.json`) | QUALITY 55 (frozen input checked for any commit touching it after the freeze): prose only, no executable check | `tools/round-38/freeze-drift.py`, QUALITY 79. Exit **1** from `e059ca93` to `077e212b` (`.ufo/waves/round-38/l1/freeze-drift-077e212b.json`, both commits listed); exit **0** to `cb4326b2`; exit 2 when the freeze is not an ancestor. Wave 2 found the pass leg non-discriminating (`cb4326b2` predates the drift) and showed bypasses: a chosen later "first freeze", a new counter path, imported helpers, a symlinked manifest (`w2/R38W2CritGateBypass.md`). The tool now also reports `ships_freeze_bytes`; see M38-9 |
| M38-2 | control reproducibility — the frozen control generator was degenerate and its kill signal inverted; it was fixed one commit after the freeze, in the same commit as the receipts | `.ufo/waves/round-38/w1/R38ReviewerControlReplay.md` F1-F3: at `e059ca93`, `gen-controls.py:199` passes `'1'/'2'/'3'` where `c2_fixture` branches on `junk/delete/substitute`, so CTL-C2-1/2/3 all mint the repaired green fixture (`met_target true`), and `:217` inverts the exit. At `efd5c47a` all seven replay to exit 1 (`w2/R38W2C2Controls.md` §1). Attempt 1 later overwrote the C1 control receipts with v2/v3 re-scores under unchanged argv (`w2/R38W2C2Controls.md` §2); the first-freeze values survive only in `efd5c47a`'s tree | none | QUALITY 80. `freeze-drift.py … tools/round-38/gen-controls.py` from `e059ca93` to `077e212b` → exit **1** listing `efd5c47a` (`.ufo/waves/round-38/l1/freeze-drift-gen-controls.json`). The C2 counter itself never changed (sha `7f137b66…` at the freeze and at every later commit), and the generator fix landed before the wave was dispatched (03:09 vs 03:16) |
| M38-3 | stale premise at the freeze — "no external extractor dependency" for standard BE v4 | first-freeze claims doc: "run with stock unblob 26.6.4; no external extractor dependency". unblob 26.6.4 `SquashFSExtractor` runs `sasquatch-v4be` for BE v4 (S112, lines 24-70). The probe behind the premise filtered PATH components by name (`grep -v sasquatch`), so `~/.local/bin/sasquatch-v4be` stayed reachable (`.ufo/waves/round-38/w1/R38RevengerPremise.md` §0; `R38ExecBeforeArmRecheck.md`) | none | a before-arm that removes the directory itself. With `$HOME/.local/bin` off PATH all four carriers give `missing-extractor-dependency` [`sasquatch-v4be`] and 0 files (`corpus/evidence/round-38/c1/K*/before.json`, reproduced by `w2/R38W2ReproK*.md`); with it on PATH they publish. The same carrier comes out red or green depending only on the arm |
| M38-4 | harness — the frozen after-mode harness could not produce a receipt | `c1-run.sh after` at `9c9d496b` ran `mkdir -p "$OUT"` before REA, and REA refuses an existing extraction root: exit 1 (`.ufo/waves/round-38/w1/artifacts/R38ExecAfterK3/harness-after-mode-failure.txt`) | none: the controls never ran the harness | `cb4326b2` removed the pre-create, and the same invocation exits 0 (`R38ExecAfterK3/harness-after-mode-post-fix-ok.json`) |
| M38-5 | false correction — the L1 "corrected" a correct staged count while admitting `unblob-format-matrix` | landed at `3b960fe5`: "the staged '42 vendor-attributed entries' was a count of the word `Vendor` (42 occurrences), not a per-handler attribution count". A per-section recount gives 42 of 97 sections with exactly one `Vendor:` field each (one value `unknown`), so the staged figure was right (`w2/R38W2SrcS116.md` Defects 1) | none (no rule asks that an admission-time correction be recounted on the claimed unit) | a non-author per-unit recount of every correction an admitted entry states. `R38W2SrcS116` failed the landed correction; the per-section script reproduces 42/97. The entry and this lesson now keep the staged count |
| M38-6 | existence-only calibration counter — C2's frozen counter takes any resolving path as a repair | `w2/R38W2C2Controls.md` §3: the base tree plus one stub file at `evidence/doctor/doctor-6.5.0.txt`, with no PROVINCE edit, scores `mismatches 0`, `met_target true`. The frozen controls (junk count, pointer deleted, other document) never tried "materialise the missing path" | QUALITY 77 ("checks a repaired pointer against the intended document named in the freeze"), with no implementing check | QUALITY 81 and `tools/round-38/intended-doc.py`: landed `0fc61133` → exit **0** `bound`; base → exit **1**; the S2 stub shortcut rebuilt in scratch → exit **1** (`.ufo/waves/round-38/l1/intended-doc/{landed-0fc61133,base,shortcut-s2}.json`), while the frozen counter gives the same shortcut `met_target true` |
| M38-7 | misroot — unblob writes `./unblob.log` in its working directory, so seats running it from the fleet root or the lane root left logs there; this repeats a wave-1 finding | `/home/vgpnk/Projects/shokunin/unblob.log` (2652 B, 03:56, names seat `R38W2SymlinkUnblob`'s scratch carrier) and a lane-root `unblob.log` (seat `R38W2AvmProbe`, since removed) (`w2/R38W2Sentinel.md`). Wave-1 `R38SentinelBounds` had already reported the same leak, and the wave-2 context did not carry the fix | the prompt's misroot sweep (§6 item 3); no wave-context rule | the fleet copy was moved byte-exact to the lane path `unblob.log` (`cmp` equal, sha256 `2d651a4a…9299`) and deleted from the fleet root. The rule for next round's contexts: `cd "$S"` before any unblob or REA extract run. The sweep (`git -C /home/vgpnk/Projects/shokunin status --porcelain` → `?? unblob.log`) is the check that fails |
| M38-8 | registry append-only violation and duplicate row — the S110 scope cell was widened in place, and S112 re-registers S108's document | `3b960fe5` changed S110's scope cell (CORPUS rule 2 lets only `status`, `recheck`, `used-by` change). S112 has the same URL, tag and sha256 `2d7b901b…9287` as S108, with a narrower scope (census W04; `w2/R38W2RegistryTally.md`) | CORPUS.md SOURCES rule 2, with no lane check | `tools/round-38/registry-immutable.sh` exits **1** at `0fc61133` (`S110 changed columns: 6`, `.ufo/waves/round-38/l1/registry-immutable/at-0fc61133.txt`) and 0 on base-vs-base; the final-commit run is in the report. S110 is restored byte-exact. The README "78+" sentences get their own scope row S117. S112 stays: the registry is append-only, and its W04 is disclosed |
| M38-9 | the measured revision did not ship the rule — after attempt 1, `tools/round-38/c1-counter.py` and `plans/round-38-claims.md` at the tip held the v3 counter and the v2 text, so the documented counting command gave 4/4 against a verdict of record of 3 | `w2/R38W2CritGateBypass.md` §0, §3 | none | first-freeze bytes restored at both paths in the final commit (attempt-1 versions kept as `.ufo/waves/round-38/l1/claims-v2-as-amended-by-attempt1.md` and `c1-counter-v3-as-amended-by-attempt1.py`). `freeze-drift.py` reports `ships_freeze_bytes`: `false` at `0fc61133`, `true` at the final commit (receipts named in the report). The commit list stays non-empty, because the history is not rewritten |

## Gate

### Sources opened this round (2026-10-26)

| row | decision | located quote (≤25 words) / access | reason | flip |
|---|---|---|---|---|
| S112 unblob `squashfs.py` @ 26.6.4 (BE v4 scope) | admit (duplicate document, disclosed: M38-8) | re-opened by L1 attempt 2, 2026-10-26T03:43-03:00: `curl …/26.6.4/python/unblob/handlers/filesystem/squashfs.py \| sha256sum` → `2d7b901b…9287` (= S108); line 26 `V4BE_EXECUTABLE = "sasquatch-v4be"`. The row's anchor joins two non-adjacent code fragments (`w2/R38W2SrcS112.md`) | scope narrower than S108; census W04 | the tag moves |
| S113 unblob 26.6.4 `squashfs_v4_be/__input__` fixtures | admit | LFS pointer `squashfs_v4.nopad.bin`: "oid sha256:a29ddc15f5a6abcabf28b7161837eb56b34111e48420e7392e648f2fdfe956ed / size 307" (`w1/R38ScoutUnblobFixtures.md`; re-confirmed `w2/R38W2SrcS113.md`). The anchor pins K4 only; K3 = `squashfs_v4.bin`, oid `9c7c523c…97c0`, 4096 B (same report) | closes R37-CL2's fixture half | an oid differs from the lane carrier digest |
| S114 Freetz AVM-BE format note | admit (scope: AVM marker only) | line 1: "This document summarizes all (so far known) technical details about a non-standard SquashFS format"; lines 13-14: "super-block field 'mkfs_time' contains (instead of the filesystem creation time) the same value as the super-block field 'bytes_used'" (the row's second anchor paraphrases this; `w2/R38W2SrcS114.md`) | closes R37-CL2's text half; live bytes equal `.ufo/waves/round-37/probes/avm.txt` | upstream rewording |
| S115 7-Zip 26.04 BE v4 refusal | **reject** (as an oracle) | `7z l` → "Cannot open the file as archive", exit 2, on K1-K4 (`.ufo/waves/round-38/w1/artifacts/R38CrossToolK4/7z-refusal.txt`). The LE v4 controls under `corpus/evidence/round-36/c1/fixtures/` open with exit 0 (`w2/R38W2SrcS115.md`) | a refusal is not an independent extraction oracle, and the refusal is BE-specific, not a general SquashFS gap | a 7-Zip release opens these carriers and publishes oracle-matching members |
| S116 unblob.org formats matrix | admit (via assimilation) | opened 2026-10-26T03:44:24-03:00, HTTP 200, 216890 B, sha256 `8f8c29af…bbc5`; meta "parses unknown binary blobs for more than 30 different archive, compression, and file-system formats"; re-confirmed byte-identical by `w2/R38W2SrcS116.md` and `w2/R38W2AssimAdmit.md` | producer coverage statement, re-countable | counts change on refetch |
| S117 unblob README @ 26.6.4, format-count sentences | admit (via assimilation) | opened 2026-10-26T04:07:23-03:00, sha256 `6544d60f…3716`; line 5 "unblob parses unknown binary blobs for **78+ archive, compression, and file-system formats**" | S110's scope cell covers only the sasquatch sentence and cannot be widened in place (M38-8), so the count sentences get their own row | the tag moves |

Registry: rows 111 → 117 (S112–S117 appended). Tallies: A/mined 101 → 105, A/rejected 3 → 4,
B/mined 6 → 7, C/rejected 1 → 1. No existing row's cell changed at the final commit: the `3b960fe5`
in-place edit to S110 was reverted byte-exact (M38-8), so S110's `used-by` is unchanged.

### Assimilation — theme sasquatch / unblob (`/home/vgpnk/Projects/shokuknow/merge/kaidoku`, read-only)

Id-collision check, run in scratch before any append with the addendum §10 pattern: registry ids
S001–S111 (111) against staged S106–S237 (132) gives **6 collisions, S106–S111**
(`.ufo/waves/round-38/assimilation/{reg-ids,staged-ids,collisions}`). The guard was first proven on
an indented `  | S002 |` fixture (`.ufo/waves/round-38/w1/artifacts/R38ExecIdCollision/guard-proof.txt`).
Against the final registry the same command gives 12 collisions (S106–S117), because the lane's own
appends now occupy staged numbers too. No staged row is appended verbatim, so this is expected
(`w2/R38W2AssimCollision.md`). Renumber map, by document: staged **S122** (unblob.org/formats) →
lane **S116**; staged **S106** (unblob README) → lane **S117** (new scope row on the document S110
holds). Only rows that admitted entries cite were appended.

- **ADMIT `unblob-format-matrix`** → `corpus/knowledge/2026-10-26-unblob-format-matrix.md`. Re-opened
  live (S116, S117). Reproduced: 97 `<h2 id=`; "more than 30 different" × 3; ten `SquashFS (…)`
  sections including `v4-BE`; 89 Fully / 8 Partially supported; 42 sections with a `Vendor:` field;
  ZIP "Partially supported" with "Does not support encrypted ZIP files"; README @26.6.4 lines 5/22
  "78+". One correction: `v4-broadcom`, not "v4-Broadcom". The staged vendor count was kept (M38-5).
  PROVINCE scope: firmware-extraction producer contract, the same ground as the round-36 Core row.
  Non-author check: `w2/R38W2AssimAdmit.md` CONFIRMED. Flip to refuse: the page drops
  `SquashFS (v4-BE)` or the counts change.
- **REFUSE `sasquatch-unblob-compatibility-precondition`** (staged round 7, staged S165).
  - Provenance first: its only source, `lanes/kaidoku/round7/work/r7-local-measurements.tsv`, exists
    nowhere on this host (`find /home/vgpnk/Projects/shokunin -name r7-local-measurements.tsv` →
    nothing; `w2/R38W2AssimRejects.md` D3).
  - Host state second: "absent from PATH" was true when the snapshot was taken. It has been false
    since 2026-10-26T01:22:37, when this lane's round 36 installed `~/.local/bin/sasquatch` (382824 B)
    and `sasquatch-v4be` (436232 B). `/usr/bin` and `/usr/local/bin` still hold neither (D1).
  - The load-bearing sentence ("running them requires the operator's own installation …
    unobtainable from the lane host") is falsified by lane bytes. The lane observed the pair itself
    (round-36 LE; round-38 after-arms K1–K4), and `R38W2AssimRejects` reproduced K4 4/4 at the pin
    (D2). No published source states a version-pair condition; S110:49 and S112 state the producer's
    declared dependency.
  - Flip: none. The source cannot be recovered.
- **REFUSE `sasquatch-unblob-avm-branch`** (staged round 9; staged S189–S192).
  - Policy ground: S189 points at the unpinned `unblob/main` handler. Today that file is
    byte-identical to the 26.6.4 pin (sha256 `2d7b901b…`, D4). It is refused because the reference
    can move, not because the content disagrees.
  - S190/S191 are campaign-local `lanes/kaidoku/round9/work/lead2-avm-branch.tsv` rows that exist
    nowhere on this host.
  - The closing premise ("a real AVM image still needs a tool this host does not have") is false for
    a cheaper reason than the sibling build: AVM publishes the real image at
    `https://download.avm.de/fritzbox/fritzbox-6490-cable/other/fritz.os/` (HTTP 200; D5).
  - The branch mechanics reproduce at the pin on lane bytes: `bytes_used` is copied into
    `mkfs_time`, `-be` is dropped, and `sasquatch-v4be` fails with exit 1 and 0 files
    (`w2/R38W2AssimRejects.md` F1; `w2/R38W2AvmProbe.md`).
  - Flip: an entry re-grounded on lane receipts with the source repinned to 26.6.4. The round-39
    second-choice plan carries this.
- Scratch-mirror census before the first append: attempt-1 seat `.ufo/waves/round-38/w1/R38ExecMirrorGate.md`
  (exit 0). That gate validated a draft S112 block whose scope differed from the landed row
  (`w2/R38W2ScribeGateXref.md` D2). Wave-2 `R38W2AssimMirror` re-ran the mirror on the admitted
  append, and the real-lane end census is in the report.

### Quarantine slice (absent-defect register, read-only; kaidoku data rows: 5)

Derived with the addendum §10 `awk` (`.ufo/waves/round-38/assimilation/quarantine-slice`).
Wave-1 seat `R38ExecQuarantine` hand-checked every row live
(`.ufo/waves/round-38/w1/R38ExecQuarantine.md` §3). Wave 2 re-derived the slice byte-identically
and re-opened the sources (`w2/R38W2Quarantine.md`, CONFIRMED). All ids below are staged campaign
ids, not lane rows:

- **staged S150: refuse (fabrication class).** The zenn.dev article is live (174,088 B); the
  registered heading 「シンボルがない場合のヒント」 occurs 0 times.
- **staged S113: adopt-with-anchor, count corrected.** The adb page lists 21 locales + `x-default`,
  not 17.
- **staged S117: unverifiable, not fabrication.** IEEE Xplore returns HTTP 202 with an empty body;
  Crossref confirms the paper exists.
- **staged S136: adopt-with-anchor.** `corpus/knowledge/2026-10-13-r4u-06-adb-surface.md` line 8.
- **staged S147: adopt-with-anchor, with a conflict.** The host file
  `~/.agents/skills/reverse-engineer-anything/HOST-CONTRACT.md` (3,386 B, sha256 `ab36b310…58fe`,
  committed record `.ufo/waves/round-35/w1/R35ReconQuarantine.md:174-178`) carries the quote at
  line 41. One of the row's two heading names is wrong. The quoted `rea-agents@6.7.0` disagrees with
  the lane's pinned 6.5.0 package.
- No admitted entry cites any of the five, so none is appended.

## Routed defects (round-37 closure)

- **R37-CL1** (cite only committed receipts). The C2 receipt `c2-at-0fc61133.json` was uncommitted
  when wave 2 read the landing, and an earlier draft cited a `c2-final.json` that did not exist
  (`w2/R38W2LessonReview.md` D1). Both receipts are committed by the round's last lane commit, and the
  report cites only what `ls-remote` shows on the branch.
- **R37-CL2** (register round-37 outside material): S113 (BE fixtures) and S114 (Freetz note).
- **R37-CL3** (file Gate decisions, including the 7-Zip rejection): this section; S115 is a rejected row.
- **R36-CL1**: `.ufo/waves/round-36/w2.ready.dispatched` was committed in the freeze `e059ca93`; the
  round-38 `w1.ready.dispatched` stamp at `3b960fe5`.
- `considerthese/` is absent in this lane.

## Criteria added

QUALITY 79 (first-freeze rule + `freeze-drift.py`), 80 (controls inside the freeze) and 81 (pointer
repair bound to the intended document; `intended-doc.py`), all in `corpus/QUALITY.md`. M38-3/M38-4/
M38-5/M38-7/M38-8 carry fixes shown able to fail but no new criterion. CORPUS rule 2 and the
prompt's misroot sweep already state M38-8 and M38-7.
