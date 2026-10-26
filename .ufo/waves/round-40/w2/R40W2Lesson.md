# R40W2Lesson — round-40 lesson Gate draft: sources, assimilation, used-by log, S126 recheck

**DONE** — the round-40 lesson Gate is drafted at
`.ufo/waves/round-40/w2/artifacts/R40W2Lesson/gate.md`; all four new source rows (S123–S126) were
re-opened and every located quote re-found in the bytes this seat fetched or re-hashed, the six used-by
cells were diffed field-by-field, and the assimilation/quarantine record was checked against its artifacts.
No falsification of the landing's source record was found; one count in the assimilation report is off by
one line (`Processing file` ×5, not ×4), and two calibration items are now stated in executable form.
Nothing was written into `corpus/`; the lesson text is for the L1.

Seat R40W2Lesson (leaf, no subagents, no background jobs, no `agent://all`). Revs: base
`fa6a8a3f85ec65946b3a54d37c0ddd1d6748664f`, freeze `7fce308631a8b457d6b7c5a4b39a923c4e9a49de`, measured
`42c10a58cb2cae3a4a0122af35a0cf95ac718043`, tip at dispatch `4d62ee5a86b4692a13f682b29ed7975e8d7e5326`.

## What was attacked

The landing's **documentation record**, not its claim scores: the four SOURCES rows the round added, the
used-by edits it made in place, and the assimilation/quarantine dispositions the lesson must carry. The
question each check answered was "does this sentence reproduce from the bytes it cites, and does the cell
it lives in say only what was measured?"

| surface | check | result |
|---|---|---|
| S123 rea-agents 6.5.0 | tarball re-downloaded (HTTP 200, 5 634 033 B) sha256 `531717a0…218e699` = row; quote `engineName = request.operation === …` at `dist/firmware/FirmwareProvider.js:141`, byte-equal to the installed copy; `dist` members 1 574 = row | **reproduces** |
| S124 Freetz-NG patch | re-fetch at `9a72369…` HTTP 200, 2 217 B, sha256 `7f0a1b25…be1e220fc` = row, `cmp` equal to the retained artifact; line 35 quote and the `swap_block_length` branches present | **reproduces** |
| S125 vendor page | `info_en.txt` sha256 `6c601b34…3d11070a7` = row; image 39 741 440 B sha256 `f518ce6b…04f9ede6d` = the V1 pin; member `./var/content` 346 B sha256 `ab238b0e…38eca9557` = row, with `Product=` / `Version=07.57` / `Build=107830`; `filesystem.image` member size 5 443 592 = row | **reproduces** |
| S126 own-work TSV | TSV sha256 `f205807d…7c8539eb0` = row; image `c7f74691…faed32d32`, log `352e0d79…518aed5d7`; log argv `sasquatch-v4be -no-exit-code -f -d …` with no `-be` | **reproduces**, one count corrected |
| used-by (S112, S114, S118, S119, S120, S121) | field-level diff base → tip: `used-by` is the **only** changed cell on all six; every appended entry's `source:` lines name the row | **reproduces**, CORPUS rule 2 respected |
| registry shape | 126 rows, no duplicate id, last S126; S123 added at the freeze, S124–S126 at the landing | **consistent** |
| collision check | `collision/` 122 registry ids / 132 staged / 17 collisions S106–S122 / next free S123; indented fixture catches the collision, column-zero-only extractor false-greens | **reproduces** |
| quarantine slice | sha256 `7383a90e…628e6a`, 5 rows (S150, S113, S117, S136, S147); verdicts read, not re-fetched | **as reported** |

## Gates

- **Quote located in fetched bytes** (all four rows): pass. Each quote is ≤25 words and is quoted from a
  re-fetched or re-hashed source, not from a seat report.
- **Cell contract** (append-only; only `status` / `recheck` / `used-by` change in place): pass — six rows,
  six `used-by` diffs, zero other cell changes.
- **Citation accuracy** (no used-by entry that does not cite the row): pass — both round-40 entries'
  `source:` lists match the cells; S107/S108 were *not* widened (their draft proposal was declined, so no
  phantom citation).
- **Gate completeness** (the four pieces the wave-2 spec names): pass — sources table, assimilation with
  admit/reject reasons, used-by old→new, S126 recheck stripped.
- **Honest-stop consistency**: pass — the gate states S123–S126 are citations, not execution evidence for
  R40-C1, so it cannot be read as promoting the demoted Core row.

## Findings

- **F1 — the assimilation report's log count is off by one.** `w1/R40AssimE3.md` §"What was done" and its
  known-limits paragraph say "the 12:01 log's four `Processing file` lines"; the log has **five**
  (`grep -c "Processing file" unblob.log` → 5): one for the input image and four for the published files.
  The substance (four published files) is right; the lesson text must not quote the count. Recorded in the
  gate's S126 note.
- **F2 — S114's anchor still carries the defect the source seat found, correctly.** S114's anchor is the
  paraphrase "`mkfs_time` field holds the same value as `bytes_used`" plus no HTTP status, size or sha256;
  the verbatim lines 13-14 sentence and the block-length sentence are absent. Append-only forbids the
  repair, and S124 is the code companion — the lesson should say so explicitly (K-3), or a future reader
  will "fix" the anchor.
- **F3 — K-1 is now executable, and it is the lesson's strongest calibration item.** `unblob`'s
  `ExtractCommandFailedReport` is `Severity.WARNING` (`report.py:94`) and `get_exit_code_from_reports`
  maps `(Severity.WARNING, 0)` (`cli.py:464-475`), and the child argv carries `-no-exit-code`; so an
  extraction that published zero files still exits 0. Any kill control or receipt binding scored on
  `exit != 0` cannot fire. Re-verified against the installed files this round (sha256 in `verify.txt`).
- **F4 — the reject seat's warning about the separator column landed.** The frozen v2 table header
  (`SKILL.md:363`, block marker `:361`) keeps `-be in child argv` between `dependencies` and
  `symlink removed`, so `avm-marker-be-dropped` and `body-extractor-failure` stay separable (K-2). This
  was a *prediction* in wave 1 and is a measurement now.
- **F5 — the three provisional `S123` drafts are resolved, and the collision map's ids are superseded.**
  Three source seats each independently computed "next free = S123"; the freeze took the REA row as S123
  and the landing took S124/S125/S126, so `renumber-map.tsv`'s `S200→S123 / S201→S124 / S192→S125` is
  historical. Both assignments are collision-free; the registry is the authority. The lesson should name
  the supersession so the map is not read as a live mapping.
- **F6 — the two assimilation seats do not contradict each other.** `R40AssimE3` admitted exactly the one
  entry `R40AssimReject` did not re-test (`avm-image-extraction`), and the reject seat's two REJECTs are
  among E3's five refusals; the one difference is `avm-le-image-genuine-marker`, refused on scope by E3
  and ADMIT-AFTER-REWRITE by the reject seat — a scope-vs-quality split, not a factual one. The lesson can
  state both without a reconciliation paragraph.

## Artifacts (this seat)

`.ufo/waves/round-40/w2/artifacts/R40W2Lesson/`

- `gate.md` — the draft `## Gate` section: `### Sources opened this round` (S123–S126, URL, opened,
  located quote), `### Assimilation` (1 admit, 5 refusals with reasons and flips, collision result and
  guard proof, quarantine verdicts), `### used-by change log (old → new)` for the six rows, the calibration
  block K-1–K-3, and `### S126 recheck prose, stripped`
- `verify.txt` — every command run and the output it produced (tarball/patch/vendor/TSV hashes, the log
  greps, the field-level SOURCES diff, collision and quarantine reads, the unblob severity mapping)

## Out of scope / not claimed

- No claim about R40-C1's 3/4 score, the L2 suffix false negative, the C1-extra gate or the demoted Core
  row; those are the C1 seats' and the C1' verdict is not re-scored here.
- No claim about R40-C2's 26/26 or the triage table's content beyond the one column check (K-2).
- The quarantine verdicts are the quarantine seat's live fetches, read here; this seat re-fetched no
  non-AVM web source.
- No vendor bytes were copied into the lane. The 39.7 MB image was downloaded into scratch only to
  re-derive `./var/content`, then deleted with the scratch directory.
- The S126 extraction is read from the retained log, never re-run (the log has no exit status).

## Limits

- The S123 quote is located in the tarball member and the installed copy is byte-equal for that file; the
  row's full 1 574-file `dist` diff was not re-run (the count was).
- `info_de.txt` was hashed from the retained artifact, not re-fetched.
- The `S126` "four published files" rests on the log's four output `Processing file` lines plus the TSV's
  `extracted_files` row, with no exit status in the log (F1, K-1).

## Tooling, writes, custody

- No tool installed, upgraded, moved or removed; no pacman or other transaction was attempted, so the
  host-wide pacman pause is untouched. `unblob` 26.6.4, `sasquatch`/`sasquatch-v4be` 4.5.1 read only.
- No REA call, no `unblob` run, no `sasquatch` run, no carrier touched, no cloned fixture.
- Writes: this report and `.ufo/waves/round-40/w2/artifacts/R40W2Lesson/{gate.md,verify.txt}` only. No
  VCS mutation (read-only `git show/diff/ls-tree`); `SKILL.md`'s ` M` in `git status` is a sibling wave-2
  seat's instrument-registry append, not mine.
- Scratch `/fast/scratch/hyaku/kaidoku-r40/R40W2Lesson` removed before this report was written.
