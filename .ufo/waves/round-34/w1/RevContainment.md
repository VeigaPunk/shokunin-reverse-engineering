# Round 34 — containment review

**Reviewed revision:** `54a87a51a865ab931fd355e767303337b05cccf4` (sandbox `RevContainment`). **Observed UTC:** `2026-10-23T10:55:13Z` timestamp probe. Static audit only; no production reader/counter, adversarial control, authoring script, selftest, REA, or carrier was run. No fixtures were created, no tools installed, and no lane/fleet Git or jj write was made.

## Findings (severity order)

### Medium — challenge author persists transformed ELF copies rather than making temporary copies

`.ufo/waves/round-34/prep/R34Expected-files/author_challenge.py:176-185,281-345` writes each transformed image to `ROOT/corpus/evidence/round-34/elf-meta/mNN.bin`, chmods it `0644`, then returns without unlinking it; the schedule, checks, and captured readelf outputs are also retained. This is explicit retained output, not a temporary file/directory. It preserves the separate original copy and the mode check is enforced, but does not meet a literal “all transformed copies temporary” requirement. The author script’s default entry point calls `author()`; it was not invoked here.

### Medium — counter bounds reader wall time, but not its output or descendant processes

`tools/round-34/version-needs-counter.py:124-134` runs the selected reader with `subprocess.run(... capture_output=True, timeout=10)`. The 1 MiB stdout check occurs only after `run` has buffered stdout, while stderr is also buffered before truncation. There is no memory/output cap or process-group isolation. A supplied control reader can therefore consume unbounded capture memory within the timeout, and a reader-spawned descendant can survive a timeout (or hold inherited pipes open). The instruction to supply fake TEXT readers constrains operator behavior, not what `--control-reader` enforces. Neither production nor control reader was executed.

### Low — authoring size caps are checked after the writes they are meant to bound

`author_expected.py:458-466,619-633` reads and copies all 12 hard-coded sources before checking the aggregate `CAP_BYTES`; `author_challenge.py:176-185,281-298` writes each transformed copy before checking the retained-total cap. `run_readelf` has a per-call 180-second timeout (`author_expected.py:300-307`), but there is no aggregate authoring deadline or captured-output size limit. The fixed source list and the cap limit expected completed outputs, not peak writes/memory or partial output before failure.

### Low — freeze-integrity selftest has unbounded Git calls and writes outside this seat’s clone

`tools/round-34/freeze-integrity.py:117-120` invokes Git without a timeout. The optional selftest creates Git repositories and commits through `_fixture`/`_selftest_commit` (`:130-164`) beneath the fixed `/fast/scratch/hyaku/kaidoku-r34/R34FreezeSchemaSelftest` root (`:48`, `:375-409`), outside the assigned `.../w1/RevContainment` clone. Its nested gate process has a 120-second process-group timeout (`:176-193`), but that does not bound the parent selftest’s direct Git calls. This code contains no lane/fleet Git target; it was not run because this seat is limited to Git writes in its named clone.

## Residual risk and enforced vs instructed limits

- **Carriers are not executed by the reviewed flows:** `elf-version-needs.py` reads/parses bytes; its optional oracle runs `readelf` on a path, not the ELF as a program. The counter invokes Python on the reader script and supplies the carrier only as a `.data` argument. Both authoring scripts invoke `/usr/bin/readelf` on source/copy paths and parse bytes. These are code-path observations, not runtime evidence.
- **Original bytes are not modified by the authoring paths:** `author_expected.py:455-475` reads the hard-coded source and writes a separate copy; `author_challenge.py:130-168` reads the original copy, patches a `bytearray`-derived value, and writes a separate `elf-meta` file. The counter transforms fetched bytes in memory and writes them under `TemporaryDirectory` (`version-needs-counter.py:109-123`), then unlinks each candidate (`:134`).
- **Mode 0644 is enforced for original copies, retained challenge copies, and counter candidates** (`author_expected.py:464-473`; `author_challenge.py:178-185`; counter `:122-123`). This is a mode check, not immutability: owner write permission remains.
- **Reader limits enforced:** CLI input is capped at 536,870,912 bytes and reads at most cap+1 (`elf-version-needs.py:75-81,581-599`); parse limits entries, section bytes, auxiliary records, and string length (`:75-81`). `parse(data)` itself has no input-size gate and copies bytes-like inputs (`:323-331`).
- **Counter limits enforced:** frozen target is 12; each manifest carrier is capped at 16 MiB (`version-needs-counter.py:141-155`); Git reads have 30-second timeouts (`:70-74`); candidate reader gets a 10-second timeout (`:124-134`). Its temporary files are cleaned by `TemporaryDirectory`. These controls do not impose OS resource limits or process-tree/output caps on the reader.
- **Authoring limits:** the expected-author source list is fixed at 12 and `CAP_BYTES` is 16 MiB; the challenge author consumes manifest rows and checks the combined cap. Both checks happen after carrier writes. Readelf calls have 180-second per-call timeouts, not an aggregate budget.
- **Instructional vs enforced:** “no production runs,” “use fake TEXT readers,” no held-item dependency, and no lane/fleet writes are operator instructions; no runtime guard in these tools disables production scoring or proves a supplied control reader is harmless. A literal scan of reviewed scripts found no `U064N008Hf47eb933`, `R33FixtureBuilder`, `MARKER`, or `log_trap` references. `author_challenge.py` imports only the sibling `author_expected` module plus standard library; the authoring scripts do not write VCS. The only inspected Git writers are freeze-integrity selftest fixture operations under its fixed scratch root; no jj writer was found.

## Pin and caller checks

The three active `tools/round-34` instruments and `author_expected.py` hashes match the frozen `claims.json` pins: counter `d7f0a8cf…`, reader `ac7d24a5…`, freeze-integrity `fe955c57…`, expected author `916e0669…`. `author_challenge.py` is not listed in `instruments`. The archived scratch reader at `prep/R34ElfReader-files/reader.py` differs from the pinned active reader (`fb7e6a65…` vs `ac7d24a5…`); it is an archived development artifact, not the counter’s `READER` path.

No LSP device/server was exposed in the available tools. Literal grep was used only to locate script references and marker/VCS strings; it is not semantic caller proof. The frozen scorecard names the counter command; no production invocation was performed for this review.

## Verification gaps

No scripts, controls, authoring flows, readers, or carriers were run by this reviewer, by instruction. Consequently mode/digest checks on existing filesystem copies, actual process-tree behavior, current authoring output sizes, and runtime non-execution are not independently exercised here. No tools were installed or updated.

## Report trailer

- Written: `.ufo/waves/round-34/w1/RevContainment.md` only.
- No production/shared code or fixture changes; no Git/jj writes; no tools installed.