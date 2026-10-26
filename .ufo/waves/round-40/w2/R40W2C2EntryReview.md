# R40W2C2EntryReview — C2 entry `2026-10-26-r40-sqfs-triage-v2.md` under landing attack (round 40 wave 2)

**Verdict: DEFECTS FOUND** — 2 minor wording defects in the entry itself (no substantive
misattribution; every source anchor, line range and evidence claim otherwise verified against
re-opened bytes), plus 1 low finding in adjacent scope (SKILL block 18's supersession sentence,
which cites this entry). Attacked: every factual sentence of the C2 entry against committed
evidence (dev v1 score 18/26, wave-1 recon reports, the held-out score receipt at `42c10a58`),
every line-range citation in SKILL rule block 19, and the five header sources S112/S118/S119/
S120/S123 re-opened at byte level — S123's anchor re-opened in the installed rea-agents 6.5.0
package and against a freshly downloaded tarball.

Axes (godspeed): coverage = every entry sentence × committed evidence; depth = source anchors
re-opened, not trusted; calibration = severity per finding, unsupported sentences listed
explicitly.

## Findings

### F1 — MINOR — entry :20-22 — dropped "besides `extract-firmware`" qualifier

Entry says: "of 33 operations run on a bare SquashFS carrier only `inspect-firmware-regions`
returns an `ok` envelope with a `normalized_result`". As written this is false:
`extract_firmware` is one of the 33 and returns an `ok` envelope with a `normalized_result`
(that is the entire C2 domain). The cited source states it correctly —
`.ufo/waves/round-40/w1/R40C2ReconDomain.md` §2: "exactly one operation returns an `ok`
envelope with `normalized_result` on a bare SquashFS carrier **besides `extract-firmware`**".
The count 33 is right (21 format-gated ops on both carriers + 10 more on BE + `extract-firmware`
+ `inspect-firmware-regions`, per recon §2; `inspect-artifact` also ran bare and failed, its one
`ok` envelope is on the zip-wrapped carrier, so "bare" holds). Intent and every downstream
conclusion are unaffected; the sentence just needs "other than `extract-firmware`".
Fix: `…only `inspect-firmware-regions` besides `extract-firmware` returns an `ok` envelope…`.

### F2 — MINOR — entry :49 — "18 of 26 classes" should be "18 of 26 envelopes"

Entry says: "the round-39 v1 table agrees with 18 of 26 classes". There are 13 classes; 18/26 is
the envelope count (= 9 of 13 classes agree). The cited artifact
`.ufo/waves/round-40/w1/artifacts/R40C2HeldoutGen/v1-table-on-v2-dev-set.txt` says "v1 labels on
the v2 set: 18/26 agree with the frozen generator class" over the 26 dev envelopes, and its
per-row table shows the 8 DIFF envelopes in exactly the four named classes (H05/H06 clean-empty,
H11/H12 mixed, H21/H22 partial, H25/H26 out-of-domain). The sentence's own first clause ("On the
26 development envelopes") shows the noun slip. Number and miss-set are correct; fix the noun:
"agrees on 18 of 26 envelopes (9 of 13 classes)".

### F3 — LOW — adjacent scope: SKILL block 18 supersession sentence (:331-334), not block 19

The block-18 sentence "this v1 table stays as the round-39 record and mislabels mixed-link
images, partial failures, empty trees and non-firmware envelopes
(`corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md:27-36`)" cites one range for four claims.
Entry :27-36 is the three-outcomes paragraph and covers mixed, partial and empty; the
non-firmware-envelope mislabel is supported by the domain-guard paragraph at entry :19-25 (v1
labels the region-scan envelope `no-squashfs-chunk`). The fourth item resolves elsewhere in the
same entry, so the sentence is true but its citation under-covers it. Recorded because it cites
this entry; it is outside my named block-19 scope.

### INFO — block-19 paragraph citations each include one trailing blank line

The five block-19 citations `:11-18`, `:19-26`, `:27-36`, `:37-45`, `:46-56` each end one line
past the paragraph's last text line (paragraphs run 11-17, 19-25, 27-35, 37-44, 46-50+52-56;
blanks at 18, 26, 36, 45, 51). Every citation resolves to the paragraph it names; the convention
is uniform across all five; no action needed.

## Unsupported sentences (the requested list)

1. Entry :20-22 — the "of 33 operations … only `inspect-firmware-regions` returns an `ok`
   envelope with a `normalized_result`" sentence, as literally written (F1).
2. Entry :49 — "agrees with 18 of 26 classes" (F2).

No other sentence in the entry is unsupported; the two paraphrases below were checked and stand:

- "v1's escaping row matched on `SR` alone" (:28-29) — shorthand, matching the committed dev
  artifact's own wording ("escaping row matches on SR alone"); the full v1 cell set is
  `handler squashfs_v4_*`, gap kinds `*`, dependencies `*`, `-be n/a`, `SR=yes`, `P>0`
  (recon `R40C2ReconMixed.md` §6 spells it out). In the mixed-image context SR is the deciding
  cell.
- "told the reader to ignore the in-tree gaps" (:29) — direct paraphrase of routed defect
  R39-CL2 (`corpus/lessons/round-39-verifier-spotcheck.md:154`): "get an action that tells the
  reader to ignore their in-tree gaps", and of recon §6 ("its `unpublished-entry` gap is never
  read").

## Verified inventory (all checks that passed)

**SKILL rule block 19 structure** (SKILL.md): v2 bullet at :348, marker `<!-- sqfs-triage-table
v2 -->` at :361, actions line at :362 with exactly 11 tokens, table at :363+ with 11 rows, 11
unique labels, every row pinning `extract_firmware`/`unblob`, `mixed-symlinks` (row 7) ahead of
`escaping-symlink-removed` (row 8), one action token per row all inside the vocabulary. Recheck
line verified live: `python3 -I -B tools/round-40/sqfs-triage-v2.py --skill SKILL.md
--table-only` → "rules: 11", exit 0 (output copied to artifacts).

**Block-19 line-range citations all resolve:**

| citation | target | verified |
| --- | --- | --- |
| entry `:11-18` | What-v2-adds paragraph (11-17) | ✓ |
| entry `:19-26` | Domain-guard paragraph (19-25) | ✓ |
| entry `:27-36` | Three-outcomes paragraph (27-35) | ✓ |
| entry `:37-45` | AVM-marker paragraph (37-44) | ✓ |
| entry `:46-56` | Scoring (46-50) + Limits (52-56) | ✓ |
| S112 `:68-69`, `:25,37,68-69` | `get_dependencies` 68-69; `EXECUTABLE="sasquatch"` 25; default `executable = self.EXECUTABLE` 37 | ✓ |
| S112 `:44-50` | header parse → `is_avm = header.bytes_used == header.mkfs_time` (48) → `if not is_avm: append("-be")` (49-50) | ✓ |
| S120 report.py `:91-98` | `ExtractCommandFailedReport` class 91, docstring 92, fields `command/stdout/stderr/exit_code` to 98 | ✓ |
| S120 command.py `:69-77,101-102` | `except FileNotFoundError:` 69 → `ExtractorDependencyNotFoundReport` 70 → raise 77; `get_dependencies` 101-102 | ✓ |
| S118 extractor.py `:50-92` (loop `:58-65`) | `def fix_symlink` 50 … `return path` 92; loop branch 58-65 (report+unlink) | ✓ |
| S119 firmwareAnalysis.js `:137-141` | `unpublished_entries` schema at 137 (kind `symlink`/`special`) | ✓ |
| S119 FirmwarePublication.js `:68-75`, `:301-308`, `:239-307` | unpublished push 70-75; unpublished-entry gap map 301-307; gap construction span | ✓ |
| r39 knowledge `:50-54`, `:29-40` | "No SquashFS chunk" paragraph; "AVM marker versus image damage" paragraph | ✓ |
| this entry `:37-45` (avm row source cell) | the AVM paragraph of the entry under review | ✓ |
| `round-36 K3/before.json`, `c1/K1..K6 after.json`, `c2/H01..H04`, `w2/R39W2C2TableReview.md` | all exist | ✓ |

**Header sources re-opened at byte level:**

- S112 `squashfs.py` (tag 26.6.4 = commit `1fcc7a0a…`) re-fetched today: `SquashFSExtractor`
  spans 24-69, AVM marker logic at 48-50 — "omits `-be` exactly when `mkfs_time == bytes_used`"
  is exact (`is_avm = header.bytes_used == header.mkfs_time; if not is_avm: append("-be")`).
  Row records no file sha256; the quoted anchor lines match.
- S118 `extractor.py` re-fetched: sha256 `1bb49811…` = SOURCES row; `fix_symlink` exactly 50-92.
- S120 `report.py` sha `2329783f…` and `extractors/command.py` sha `8ae7d2a3…` = SOURCES row.
- S119/S123 tarball re-downloaded: sha256 `531717a0…` = SOURCES rows; all 6 anchor files
  byte-identical (`diff -q`) to the installed package
  `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist`.
- S123 anchor re-opened in the installed package: `FirmwareProvider.js:141`
  `const engineName = request.operation === "inspect_firmware_regions" ? "binwalk" : "unblob";`
  (exact line), with `FirmwareRelease.js:16/:22` (`id: "binwalk"` / `id: "unblob"`),
  `FirmwareAnalysisService.js:29` (`operation,` into `createEvidence`),
  `evidence.js:275/:281` (`id: provider.id` / `operation: observation.operation`),
  `firmwareCommands.js:29/:50` (CLI verbs → operation strings). The entry's S123 attribution
  ("where `operation` and `provider.id` are set; `extract_firmware`→`unblob`,
  `inspect_firmware_regions`→`binwalk`") is exact.

**Factual sentences vs committed evidence:**

- Dev v1 score: artifact shows 18/26 with the 8 misses exactly {clean-empty, mixed,
  partial-body-failure, out-of-domain} × 2 — matches entry :48-50 except the F2 noun.
- Domain guard: recon `R40C2ReconDomain.md` §2/§4 confirm 33 operations, the single ok
  non-extract operation, the identical v1 feature vector, and "only the two domain columns
  separate them"; §7 + manifest `out_of_domain` confirm operation and provider change together
  in the held-out set.
- Mixed: recon `R40C2ReconMixed.md` §2 (six carriers, `G={unpublished-entry}`, `SR=yes`, `P>0`)
  and committed round-39 `c1/K5/K6 after.json` (verified: `MaliciousSymlinkRemoved` diagnostics
  present, gap kinds exactly `unpublished-entry`).
- Partial: recon `R40C2ReconPartial.md` (12/12 `extractor-failure` with `P=5`; round-39 body
  recipe `P=0` in 6/6) — "v1's body row demanded `P = 0`" matches the v1 row's `0` cell.
- Clean-empty: recon `R40C2ReconEmpty.md` F1/F3 (14 runs, `G=∅`, `P=0`, v1 says
  `unclassified`; v1 clean row demands `P>0`).
- AVM paragraph: cross-checked against the C1 entry
  `2026-10-26-r40-avm-be-squashfs-core.md` (big-endian fields / little-endian 2-byte metadata
  block lengths; marker-on-standard-BE fails; genuine body extracts without `-be`; the
  inode-table little-endian walk landing on `directory_table_start`) and the r39 knowledge
  `:29-40` ("suggests a SquashFS image of a different endianess", exit 1). Consistent.
- Scoring: manifest seed = `7fce3086…` (the freeze hash), 13 classes × 2, per-carrier
  `label`/`action` assigned at generation (generator docstring: "assigned before any REA run;
  `--run` only fills envelopes"), replicate variation = compression / tree-shape /
  endianness-where-the-class-allows — matches "differ in endianness, compression or tree".
- Held-out result: `.ufo/waves/round-40/l1/scores/c2-at-42c10a58.json` — matched 26/26, exit 0,
  all 25 bindings true (`v2_table_identical`, `manifest_after_freeze`, `manifest_before_envelopes`,
  `seed_matches_freeze`, `carriers_regenerated`, …), 12 distinct decisions, unclassified 2/2.
- Interpreter claims: `sqfs-triage-v2.py` reads OP/PV first (`features()` :517-523), duplicate
  label → exit 2 (:346), no match → (`unclassified`, `none`) (:52-53, :133), domain fall-through
  documented (:46-47).
- Limits: `R40C2AxisFit.md` (c) supports the one-load-bearing-cell limit; the not-covered list
  matches the 13 held-out classes (no `unknown-chunk-handler`/`encrypted-chunk`/`depth-limited`
  class; genuine AVM outcomes are C1's surface).

## Residual risk and verification gaps

- I did not re-run REA, the counters, or the held-out generator (leaf seat; the 26/26 receipt at
  `42c10a58` and the dev-set artifact stand as the scored records; my recheck ran the frozen
  interpreter read-only).
- S112's SOURCES row records no squashfs.py sha256, so my re-fetch is verified by the quoted
  anchor lines and tag commit, not by a recorded hash (S118/S120 hashes match exactly).
- The entry's held-out *result* (26/26) is deliberately not stated in the entry (it lives in the
  claims file and the score receipt); nothing in the entry contradicts it.

## Tooling record

No tool installed, upgraded, moved or removed; no pacman call. Reads plus `curl` downloads of
the two pinned unblob files (S112/S118/S120 URLs), `report.py`/`command.py`, and the rea-agents
6.5.0 tarball into scratch, sha256-checked against `corpus/SOURCES.md`. Scratch
`/fast/scratch/hyaku/kaidoku-r40/R40W2C2EntryReview` removed after writing this report; cited
bytes copied to `.ufo/waves/round-40/w2/artifacts/R40W2C2EntryReview/` (`src/`, `rea-anchors/`,
`recheck-table-only.txt`, `MANIFEST.sha256`). No vendor firmware bytes copied anywhere.

Report: `.ufo/waves/round-40/w2/R40W2C2EntryReview.md`
