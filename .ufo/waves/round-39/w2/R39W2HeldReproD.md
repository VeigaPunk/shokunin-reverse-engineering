# R39W2HeldReproD — provenance attack on the committed R39-C2 held-out envelopes H16–H20

**Verdict: CONFIRMED** — for all five ids the carrier's sha256 matches the manifest, a fresh
`rea-agents@6.5.0` run in the manifest's `after` arm reproduces every semantic surface of the
committed `envelope.json` (handlers, `extraction_failed`, gap kinds + dependencies, diagnostics
`__typename__`, sasquatch `-be`, `MaliciousSymlinkRemoved` absence, file count), the frozen
interpreter labels each fresh envelope with the manifest label, and each committed envelope's
`evidence_id` recomputes from its own bytes. Two defects are reported in §6; neither falsifies the
label claim.

Seat: executor leaf (Godspeed). Wrote only this report and
`.ufo/waves/round-39/w2/artifacts/R39W2HeldReproD/`. No VCS mutation, no subagent, no background
job, no `agent://all`. Scratch `/fast/scratch/hyaku/kaidoku-r39/R39W2HeldReproD` removed at exit.
No tool installed or upgraded (npx `rea-agents@6.5.0` as pinned; `unblob` 26.6.4,
`sasquatch`/`sasquatch-v4be` 4.5.1 used as found, untouched). Nothing written outside the lane.

## 1. Axes named (Godspeed)

| axis | move |
|---|---|
| **coverage** | five of twenty held-out ids re-derived end-to-end from committed carrier bytes, not from the author's transcript; also swept all twenty committed envelopes through the interpreter as a supplementary check |
| **depth** | envelope *authenticity* (REA `evidence_id` recomputation) and *determinism* (repeat runs into fresh outdirs), plus a byte-level differential control on the `s_minor` carriers |
| **calibration** | does the manifest `label` survive an independent labeling of an independently produced envelope: yes, 5/5 |

## 2. Method (exact, reproducible)

1. Copy each `carrier.sqsh` from the committed tree into scratch; `sha256sum` against
   `heldout/manifest.json` → 5/5 equal (`artifacts/.../carrier-sha256.txt`).
2. Fresh REA run per id, `after` arm (default PATH, which contains `$HOME/.local/bin`):

   ```
   cd "$S" && REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob \
     npx -y rea-agents@6.5.0 extract-firmware --format json --full-output \
     "$S/hold/$h.sqsh" "$S/repro/$h"
   ```

   Exit 0, `ok=true` for all five; CLI stdout retained as `artifacts/.../H16.json`…`H20.json`, the
   `data` object as `fresh-envelopes/H16.json`…`H20.json`.
3. Feature extraction and leaf-by-leaf comparison against the committed `envelope.json` with
   scratch paths normalised to `<WORK>/<OUT>/<SCRATCH>` (`compare.json`, `deepdiff.txt`).
4. Label the fresh envelope with the frozen interpreter:

   ```
   python3 -I -B tools/round-39/sqfs-triage.py --skill SKILL.md <fresh-envelope.json>
   ```

   (`triage-labels.txt`, `triage-fresh.json`; interpreter sha256
   `ef4a8a8b7428cf7221dd3aa16bc587507d308b1eacf01074def276e744beacf2` identical at freeze
   `8fcda41c` and in the worktree; the triage table block after
   `<!-- sqfs-triage-table v1 -->` is byte-identical at freeze and worktree,
   sha256 `56bc6204ee597cb9d06978b024a290d71bb1dc982246650ce538523922fcef4f`, 8 rules).
5. Authenticity: recompute `evidence_id` from each committed envelope using REA's own
   `semanticProjection` + `digestCanonicalValue` (`eid.py`).

## 3. Result table

| id | class | label (manifest) | fresh label (frozen interpreter) | payload match |
|---|---|---|---|---|
| H16 | body-extractor-failure | body-extractor-failure | body-extractor-failure | **yes** |
| H17 | no-squashfs-chunk | no-squashfs-chunk | no-squashfs-chunk | **yes** |
| H18 | no-squashfs-chunk | no-squashfs-chunk | no-squashfs-chunk | **yes** |
| H19 | version-minor-mismatch | body-extractor-failure | body-extractor-failure | **yes** |
| H20 | version-minor-mismatch | body-extractor-failure | body-extractor-failure | **yes** |

Matched rows (fresh, `--json`): H16 → rule 5, H17 → rule 1, H18 → rule 1, H19 → rule 5,
H20 → rule 5. Labeling the *committed* envelopes with the same interpreter gives the identical five
labels, and the freeze-time `SKILL.md` (`git show 8fcda41c:SKILL.md`) gives them again.

## 4. Payload surfaces, committed vs fresh (all identical)

| id | chunk handler | extraction_failed | gap kinds | gap deps | diag `__typename__` | sasquatch cmds / `-be` | `MaliciousSymlinkRemoved` | files | coverage | published_bytes |
|---|---|---|---|---|---|---|---|---|---|---|
| H16 | `squashfs_v4_be` | true | `extractor-failure` | `[]` | `ExtractCommandFailedReport` | 2 / **yes, yes** | absent | 0 | partial | 0 |
| H17 | — (no chunk) | — | `[]` | `[]` | — | 0 / n/a | absent | 0 | complete | 0 |
| H18 | — (no chunk) | — | `[]` | `[]` | — | 0 / n/a | absent | 0 | complete | 0 |
| H19 | `squashfs_v4_be` | true | `extractor-failure` | `[]` | `ExtractCommandFailedReport` | 2 / **yes, yes** | absent | 0 | partial | 0 |
| H20 | `squashfs_v4_be` | true | `extractor-failure` | `[]` | `ExtractCommandFailedReport` | 2 / **yes, yes** | absent | 0 | partial | 0 |

Also identical: unblob version 26.6.4 and `executable_sha256`
`0ce7b624…cba1d09`, `raw_result.execution` exit code 0, the `FileMagicReport` magic line
(`version 4.0` xz for H16; `version 9.0` zlib / xz for H17/H18; `version 4.5` zlib / xz for
H19/H20), and the decoded sasquatch stderr text modulo the temp path
(H16: `read_id_table: failed to read id table block` + `FATAL ERROR: File system corruption
detected`; H19/H20: `FATAL ERROR: Block size too small.  File system is corrupt.`).

Every leaf difference in `deepdiff.txt` is one of: `evidence_id` (derived from
`parameters.path`/`output_directory`), `parameters.path`, `subject.local_path`/`subject.name`
(my copy path/name), the producer's monotonic `provider_id`/chunk `id`, or base64 `stderr` whose
decoded text differs only by the embedded temp path. No semantic field differs.

Committed-envelope internal consistency: each decoded stderr path, the chunk report `command`
input path and its `_extract` dir all sit under the same `raw_result.report[0].task.path` as the
envelope's own task, so no cross-run splice is visible.

## 5. Authenticity and determinism

- **`evidence_id` recomputation.** REA computes
  `ev_` + sha256 of canonical JSON over `semanticProjection(evidence)` (subject digest/format/
  architecture, provider, profile, predicate, operation, parameters, `raw_result`,
  `normalized_result`, confidence, authority, environment, limitations, locations, evidence_links;
  `relationship_coverage` only when non-null). `eid.py` reimplements that digest from
  `rea-agents@6.5.0` `dist/domain/evidence.js:156-182` + `dist/domain/canonicalDigest.js`, and
  reproduces the stored id **exactly for all five** committed envelopes. Any post-hoc edit of
  `parameters`, `raw_result` or `normalized_result` would break this; none does.
- **Determinism.** A second REA run for H16 and H19 into fresh outdirs reproduces every feature
  column; the only diffs are scratch paths inside base64 stderr plus the producer `provider_id`
  counter (`1068566:1` → `2721571:1`, `1350424:1` → `2791218:1`) and the derived `evidence_id`.
  `provider_id` is run-scoped, not content-derived, and is not a triage feature.
- **Generator provenance.** `tools/round-39/heldout-gen.py` sha256
  `8b3eddf8225cfb1092726f2cabd78040f5ad765c5b4248c690a2d5bfad3cf5fc` and
  `tools/round-37/gen-squashfs.py` sha256
  `1c7c5e88324d64ad5935e81f205a609a8361466e5aea9ba461575f4e01ba8dd5` equal the manifest's declared
  `generator.sha256` / `generator.writer.sha256` and are unchanged between the freeze and the
  worktree.
- **Class grounding in the carrier bytes** (superblock, BE at offset 28/30): H16 `s_major=4,
  s_minor=0`, `bytes_used=328` of 53248 (id table zeroed → the observed sasquatch failure);
  H17 `s_major=9` (zlib), H18 `s_major=9` (xz) — unblob's v4-BE pattern pins `00 04` at offset 28
  (`unblob/handlers/filesystem/squashfs.py:523-529`), so no handler matches;
  H19 `s_major=4, s_minor=5` (zlib), H20 `s_major=4, s_minor=5` (xz) — the pattern pins only
  `s_major`, so the handler matches and sasquatch rejects the header.

## 6. Defects found (neither falsifies the label claim)

1. **Stale, falsified docstring in the generator.**
   `tools/round-39/heldout-gen.py:219`:
   > `"""s_minor 4 -> 5 so no unblob v4 handler matches; the image stays a plain unknown chunk."""`

   Falsified by the handler source (`squashfs.py:523-529` pins only `s_major`), by both committed
   envelopes (chunk `squashfs_v4_be` present) and by both fresh runs. The adjacent `RECIPES`
   comment (`heldout-gen.py:102-105`) states the correct behaviour, so the function docstring —
   not the claim — is the stale artifact. Under the docstring's (wrong) model H19/H20 would have
   been labeled `no-squashfs-chunk` and the C2 counter would fail; the label is only right because
   the *observed* behaviour tracked the `RECIPES` comment.
2. **Rule 5's cause text conflates an unsupported minor version with damage.** The frozen table has
   no version column, so `version-minor-mismatch` can only surface as `body-extractor-failure`,
   whose documented action is "the extractor ran with -be and still failed, so the image body or
   header is damaged … compare against a known-good carrier". Byte-level differential control
   (`s-minor-controls.txt`): patching only bytes 30:32 on scratch copies of H19 and H20 from
   `5` to `0` yields `extraction_failed=false`, 6 published files, `coverage: complete`, no gaps;
   `s_minor=1` reproduces the identical `Block size too small` failure. So these two carriers are
   otherwise intact, and "damaged body/header" is a wrong diagnosis for them and for any future
   `s_minor != 0` image. The manifest is transparent about this (`class` =
   `version-minor-mismatch`, `label` = `body-extractor-failure`, and the `RECIPES` comment calls it
   "a second damaged-image recipe under the same label"), so the deferred claim is not overstated —
   but the table cannot distinguish a version rejection from damage, and the label's prescribed
   action would send an operator to compare carriers instead of to the version field.

Not defects, recorded to prevent misreading: (a) `version-minor-mismatch` → `body-extractor-failure`
is an intentional class→label collapse, not a mislabel, and the runner-up row (`avm-marker-be-dropped`)
is correctly excluded by `-be=yes`; (b) the manifest's `label` is a hard-coded field in
`RECIPES`, so the counter's 20/20 is a check of the table against author-assigned labels — this
seat closed that loop independently by producing the envelopes itself and re-labeling them.

## 7. Supplementary sweep (outside the assigned five, cheap and read-only)

All twenty committed envelopes labeled with the frozen interpreter match their manifest labels
(`labels-all.json`): 20/20, all eight table rows exercised (rule counts: 1×2, 2×2, 3×2, 4×2,
5×4, 6×2, 7×2, 8×4). Not verified here: the four `before`-arm ids (H09–H12) were not re-run — out
of this seat's scope and would need the stripped-PATH arm.

## 8. Limits

- One fresh run per id, plus one determinism repeat each for H16 and H19; no statistical repeat of
  all five.
- `evidence_id` recomputation covers the semantic projection only: `subject.name` and
  `subject.local_path` are display fields outside the digest, so a path/name rebind would be
  invisible to it (the digest covers `parameters.path`, which the manifest's `carrier` +
  sha256 pins).
- `provider_id` (`<n>:1`) is a run counter, not content-derived; its value in the committed
  envelopes cannot be reproduced and was not treated as a provenance signal.
- `unblob`, `sasquatch`, `sasquatch-v4be` and the `rea-agents` package were used as found; their
  installed bytes beyond `unblob`'s launcher sha256 are not attested here.
- Everything above is directly observed at the cited commands; no step is inferred.
