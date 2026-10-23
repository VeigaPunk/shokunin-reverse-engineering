# ScribeEntrySkeletonC2 — scoped report

Report capture: `2026-10-23T02:44:48Z` (from `timeout 30 bash -c 'date -u +%Y-%m-%dT%H:%M:%SZ; rc=$?; printf "exit_code=%s\\n" "$rc"; exit "$rc"'`; output `2026-10-23T02:44:48Z`, `exit_code=0`).

## Behavior and touched surfaces

Drafted, in scratch only:

- Entry skeleton: `/fast/scratch/hyaku/kaidoku-r30/seats/w1/ScribeEntrySkeletonC2/entry-draft.md`
- SKILL decision-table section: `/fast/scratch/hyaku/kaidoku-r30/seats/w1/ScribeEntrySkeletonC2/skill-section-draft.md`

The entry includes `source: S090`, the C2 counter recheck command, the frozen R30-C2 claim, all 19 frozen mutant IDs with edits, predicted outcomes, code pointers, and intentionally blank `observed` cells; it includes P2 verbatim and the requested bounds. The SKILL draft names `inspect-rust-binary` and the entry path, and presents the signatures as source-predicted, not measured. No product file was edited. This report is the only file written in the lane.

## Findings and evidence

1. **Observation — draft bytes were written and hashed.** Producer: `timeout 30 bash -c 'sha256sum /fast/scratch/hyaku/kaidoku-r30/seats/w1/ScribeEntrySkeletonC2/entry-draft.md /fast/scratch/hyaku/kaidoku-r30/seats/w1/ScribeEntrySkeletonC2/skill-section-draft.md; rc=$?; printf "exit_code=%s\\n" "$rc"; exit "$rc"'`. Exact output:
   ```
   37f99e7fbeb921ea02142c3a134d92b904da61a084feff13099b57d864d0a513  /fast/scratch/hyaku/kaidoku-r30/seats/w1/ScribeEntrySkeletonC2/entry-draft.md
   fd3f84ff23b592f9568b8a32ecb2997112efa7473d85e47f2c7a82d7b8cf498e  /fast/scratch/hyaku/kaidoku-r30/seats/w1/ScribeEntrySkeletonC2/skill-section-draft.md
   exit_code=0
   ```
   UTC stamp: `2026-10-23T02:44:21Z` from the parallel `date -u` command; the shell tool does not timestamp each sibling command individually.

2. **Observation — the predictions source matches the frozen digest.** Producer: `timeout 30 bash -c 'sha256sum /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c2/predictions.tsv; rc=$?; printf "exit_code=%s\\n" "$rc"; exit "$rc"'`. Exact output: `6852df3ab8d5c98551f8768125fd3cb63d361e58868ff797ceb423c2f6c87315  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c2/predictions.tsv`; `exit_code=0`. UTC stamp: `2026-10-23T02:44:21Z` from the parallel `date -u` command (same timestamp limitation as above).

3. **Observation — drafts are tied to frozen claim text and predictions, not live results.** Producers: successful `functions.read` calls on `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/claims.json:24-35`, `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c2/predictions.tsv`, and `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c2-rust-refusals.py:111-168`. Exact output excerpts:
   - Frozen P2: “A mutant matches when its live REA 6.5.0 inspect-rust-binary run agrees with its frozen prediction: for a predicted refusal, the envelope is not ok and the frozen message appears verbatim in the run's stdout or stderr; for a predicted acceptance, the run exits 0 with an ok inspect_rust_binary envelope whose subject sha256 is the mutant's sha256 and whose package multiset, file_offset and compressed_bytes equal the oracle's reading of the mutant; and its committed envelope, first added after the freeze commit, agrees with the live run on ok and evidence_id.”
   - Predictions excerpt: `g-relocated … ok … RustBinaryImage.js:56 readDependency`; `r-trailing-bytes … Dependency section is not a complete zlib stream … RustAuditableReader.js:79-82,131-134 (node v24.21.0 rejects trailing junk)`; `r-over-1mib … Dependency section exceeds the 1 MiB compressed limit … RUST_SECTION_BYTES`; `r-index-outside … Dependency index 584 from package 0 is outside the package list … rootIndex`.
   - Counter edit excerpt: lines 123-128 construct the three predicted-acceptance mutations; lines 129-168 construct the refusal mutations.

   The `read` device returned the requested file contents successfully but supplies neither process exit codes nor per-call timestamps. UTC report-capture time is `2026-10-23T02:44:48Z`; it is not represented as the original read time. No primary REA package source was opened by this seat; `S090` is included as the requested source identifier.

4. **Unknown — actual REA behavior and P2 match count.** The counter was not run. Therefore there is no counter stdout, exit code, mutant observation, or result claim. In particular, the 3 accepts and 16 refusals in the drafts are frozen predictions only.

## Gates and out-of-scope items

- No REA CLI run; no carrier or mutant was executed.
- No `git`/`jj` commands, writes, installs, or subagent dispatch.
- No checks, builds, tests, or formatters were run.
- The shared C2 counter was not run; its rewrite of shared mutant files remains reserved for the assigned measure seat.
- No HTTP source was opened, so no URL/hash/quote provenance is asserted for S090 by this seat.

## Known limits

The drafts scope the mutant set to ELF x86_64, one `rea-agents@6.5.0` pin, and Node `v24.21.0`. They state the reader bounds: 256 MiB input, 1 MiB compressed section, inflate size at most `min(8 MiB, 64 × compressed-section bytes)`, JSON nesting depth 32, and an 8 MiB report budget. The 256 MiB input and 8 MiB report bounds are explicitly untested by the frozen mutants; their exact outcomes/messages are unknown. No claims are made for other formats or architectures.

## Artifact paths and SHA-256

- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/ScribeEntrySkeletonC2/entry-draft.md` — `37f99e7fbeb921ea02142c3a134d92b904da61a084feff13099b57d864d0a513`
- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/ScribeEntrySkeletonC2/skill-section-draft.md` — `fd3f84ff23b592f9568b8a32ecb2997112efa7473d85e47f2c7a82d7b8cf498e`
