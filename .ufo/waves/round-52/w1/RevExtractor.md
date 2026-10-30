# RevExtractor — r52-w1 report (extract-firmware disposition path, read-only)

Full evidence chain with file:line for every claim: `.ufo/waves/round-52/w1/RevExtractor/analysis.md`.
Scope: rea-agents 6.5.0 read-only source reading, lane receipts (round-40 R40W2C2RegenB note, round-50 c1
`after.json` / oracle `oracle-run.json`), installed unblob 26.6.4 source. Nothing executed in the package; no
probe, no sasquatch/unsquashfs run, no REA run. No tools installed. No scratch directory created.

## Answers
1. **unpublished_entries** is computed by filtering `kind !== "file"` over a full disk walk of `extracted/`
   (`dist/firmware/FirmwarePublication.js:68-77`; walk at `FirmwareFiles.js:122-189`, called at
   `FirmwareProvider.js:260`). No staged-by-handler list exists. The only report comparison is one-way for
   regular files (`FirmwarePublication.js:58-64`, `:77-85`).
2. **Char device → neither gap nor removal.** The walk would stat and gap a device if present (`FirmwareFiles.js:179-183`).
   It is not present: unblob's squashfs handler runs sasquatch with `-no-exit-code` (`UNBLOB:handlers/filesystem/squashfs.py:56-66`),
   sasquatch logs "could not create character device … not superuser!" and exits 0
   (`.ufo/waves/round-50/l1/oracle/c6430/oracle-run.json`), and unblob discards stderr on success
   (`UNBLOB:extractors/command.py:52-68`). REA has no per-entry removal mechanism in the firmware path.
3. **depth-limited gap** comes from `FirmwareReports.js:229-230` → `FirmwarePublication.js:294-300`. The envelope
   carries `input_path` (`$output/firmware.bin_extract` in all four r50 receipts) and `continuation_id`
   (`extraction_continuations` table). `range`, `relative_path`, `root_file_range` are null, so a clause needing a
   byte range cannot be met by this envelope.
4. **readlink ENOENT.** The receipted string (R40W2C2RegenB §6, H10) comes from the in-run poll:
   `FirmwareFiles.js:184` (`readlink`, unguarded; `lstat` at `:158` is guarded) called from
   `FirmwareCommand.js:112-113` every 100 ms while unblob runs. The final inventory cannot race, because the producer
   is stopped first (`FirmwareCommand.js:122`). The racing writer is unblob's own symlink re-creation:
   `UNBLOB:extractor.py:89-91` (`unlink` then `symlink_to` for every in-tree link, via `fix_extracted_directory`
   at `extractor.py:95-113`, called from `processing.py:447/654/678`). Plausible, low per-event probability.
   Same-shape unguarded site with no receipt: `dist/process/capture/FilesystemSnapshot.js:169-170`
   ("symlink projection"); not the source of the lane's receipts.

## Findings the L1 should weigh for the R52-C1 law
- **F1 (gap accounting gap):** the "removal diagnostics" are unblob's `MaliciousSymlinkRemoved`
  (`UNBLOB:extractor.py:58-65, 77-87`). REA routes them to `diagnostics` with `input_path "$input"` and a raw
  private staging path in `link`, and creates no gap (`FirmwareReports.js:65-74, 253-255`). They account exactly for
  the symlinks missing from REA's `unpublished_entries` against the oracle: c6430 1/1 (568 vs 567), c6490 1/1
  (613 vs 612), g7581 3/3 (639 vs 636), g7582 3/3 (639 vs 636). A symlink-count law that ignores MSR rows will not
  reconcile.
- **F2 (silent device loss):** all oracle char devices are silent: 1 (c6430, c6490), 13 (g7581, g7582); REA emits
  0 `special` rows on all four.
- **F3 (probable order dependence, unverified):** `fix_symlink` safety uses `Path.resolve()` (`extractor.py:77-79`)
  over `iterdir()` order (`extractor.py:99`), so MSR removals may depend on directory-entry order. Inference; a
  permutation probe would test it. Not run (not named in my task).

## Contract notes
- Writes confined to `.ufo/waves/round-52/w1/RevExtractor/` and this report. No lane tree, fleet repo, or git
  mutation. No `rea` invocation. Package read-only.
- Receipts read: `corpus/evidence/round-50/c1/{c6430,c6490,g7581,g7582}/{run,after}.json` (read-only),
  `.ufo/waves/round-50/l1/oracle/c6430/oracle-run.json`, `.ufo/waves/round-40/w2/R40W2C2RegenB.md`,
  `tools/round-50/oracle/*.nonregular.tsv`.
- Verdict: analysis complete as assigned; no blockers. Status file written.
