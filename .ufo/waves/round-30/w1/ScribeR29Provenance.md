# R29-C1 carrier provenance — routed defect 5

## Scope and outcome

Drafted append-only provenance corrections for every located R29-C1 statement that describes the carrier lists or names as published. No source document was edited; this report is the only lane file written. All five affected files should receive the same correction line at EOF, preserving the old statements.

## Findings

The following excerpts are from the requested search command against `main`. The command was run at **2026-10-23T02:42:54Z** and exited **0**:

`git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin grep -n -i 'published' main -- PROVINCE.md corpus/knowledge/2026-10-22-r29-evm-fresh-selector-naming.md SCORECARD.md corpus/README.md LOG.md SKILL.md`

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/PROVINCE.md:95` — “15 of 16 fresh solcjs-0.8.37 stub carriers holding published function lists”.
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-22-r29-evm-fresh-selector-naming.md:5` — “16 fresh carriers of published interfaces”.
- Same knowledge entry, `:10` — “carriers that hold published function lists”.
- Same knowledge entry, `:76` — “Here, with published names”.
- Same knowledge entry, `:82` — “hold a published function list”.
- Same knowledge entry, `:96-97` — “the other 15 lists were written by the L1 from the published standards without opening them this round.” This acknowledges they were not opened but describes the provenance imprecisely; the correction below states that they are L1-knowledge-based, author-selected names, not opened interfaces.
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/SCORECARD.md:3171` — “fresh published-interface carriers”.
- Same scorecard, `:3182` — “compiled stubs holding published function lists” and “public names”.
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/README.md:79` — “fresh, hex-screened carriers” under “EVM selector naming on fresh published-interface carriers”.
- Same README, `:175` — “16 fresh published-interface carriers”.
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/LOG.md:2997` — “fresh published-interface carriers”.
- Same log, `:3004` — “152 never-written selectors with published names”.

The knowledge entry's `:1` says “the published list behind carrier n04”; this is correctly scoped to n04 and is not a false generalization. Other grep hits are unrelated to R29-C1 (`LOG.md:1389`, `corpus/README.md:44`); the search returned no `SKILL.md` match.

## Append-only correction draft and locations

Append the following single line after the current EOF in each listed file. EOF anchors observed in the lane files: `PROVINCE.md:328`, the R29 knowledge entry `:106`, `SCORECARD.md:3203`, `corpus/README.md:225`, and `LOG.md:3008`.

> Correction (R29-C1 carrier provenance): only carrier n04 rests on an opened source (S088); the other 15 lists were written from the L1's knowledge of the standards and are author-selected names, not opened published interfaces.

Apply that exact line after the EOF of:

1. `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/PROVINCE.md` (after line 328).
2. `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-22-r29-evm-fresh-selector-naming.md` (after line 106).
3. `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/SCORECARD.md` (after line 3203).
4. `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/README.md` (after line 225).
5. `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/LOG.md` (after line 3008).

## Gates, touched surfaces, and limits

- Search gate: requested `git grep` returned the matching output above, exit 0, at 2026-10-23T02:42:54Z. No tests or REA runs were specified or performed.
- Touched surface: this report only. The five source files were read-only; their corrections are drafts, not applied edits.
- No external source was opened and no tool was installed. No scratch scripts, raw-output files, or other scratch artifacts were created.
- Out of scope: changing the original claims, reopening S088, or re-running R29-C1.

Report: .ufo/waves/round-30/w1/ScribeR29Provenance.md
