# R39W2Simplifier — minimality review of the round-39 landed diff

**DEFECTS FOUND** (minimality only): one 16,516-char section (`SKILL.md` instrument registry)
carries a table header with no delimiter row and therefore renders as literal paragraph text;
≈1.5 KB of statements are duplicated across surfaces that already carry them, including one
self-dup inside that same section. Nothing in this report touches the bytes of R39-C1/R39-C2 or
the frozen claims; no counter, carrier, oracle or table is changed, and no file outside this
report plus `artifacts/R39W2Simplifier/` was written.

Scope: `git -C <lane> diff a2f64e1da78afcf8cc39287106604dbcc270844c 52b0eb2907c704ed5f184c47b14c723208e5cbbc --
PROVINCE.md corpus/README.md corpus/SOURCES.md corpus/QUALITY.md corpus/knowledge corpus/lessons SKILL.md plans`
→ 9 files, 429 insertions, 0 deletions, 49,938 added chars. `plans/round-39-claims.md` (146 of
those lines) is the frozen claims authority and is read here only to decide what is load-bearing;
it is not a deletion surface. Every judgement below is byte/structure-level (no counter was run to
produce this report).

## 1. What is load-bearing (proved, so the deletions below are safe)

| surface | what an instrument actually reads | binding |
|---|---|---|
| `PROVINCE.md` `## Round-39 additions to Core` | section exists; a `\|` row whose **first cell** matches `HANDLER_RE` and whose text contains the entry path | `province_core_section`, `province_core_row` (`tools/round-39/c1-counter.py:505,507-508`) |
| `PROVINCE.md` round-39 frontier note | some line carries `FRONTIER_MARK` **and** the entry stem | `frontier_note` (`:509`) |
| entry `corpus/knowledge/2026-10-26-r39-be-squashfs-v4-core.md` | existence + its `source:` S-ids | `entry_present`, `entry_source_ids` (`:511-517`) |
| `corpus/SOURCES.md` | one row with 11 cells, the entry's S-id, `opened == 2026-10-26`, `used-by` naming entry or stem | `opened_source_rows` (`:518-531`) |
| `corpus/README.md` `## Coverage map` | one `\|` row containing the stem | `coverage_map_row` (`:533-535`) |
| `SKILL.md` craft block, lines **333-343** (marker → last row) | byte-identical at freeze and rev; header cell list equals `HEADER` | `triage_table_present`, `triage_table_identical`, `table_header_ok` (`tools/round-39/c2-counter.py:87-118,205-212`) |
| craft block, **line 316** (the `- **` rule marker) + **≥1 resolvable `corpus/knowledge/…md:NN` citation anywhere in the block** | marker keeps the block counted; round-38 `c2-counter.py` counts `resolved_rules` over `^- \*\*` blocks (`tools/round-38/c2-counter.py:133-148`) | `SCORECARD.md` depth recipe A |

Consequences used below: the craft **prose (316-332) sits before the marker at 333 and is outside
the frozen C2 block**, so trimming it moves no frozen byte; the `SKILL.md` registry section
(1328-1354) is read by no instrument (`grep -rln 'instrument registry' tools/` → only
`tools/round-35/c2-calibration-counter.py`, whose `EIGHT_CELL_SECTIONS` names the round-32 and
round-34 run-6 sections only, `:20-24`).

## 2. Deletable units, ranked

| # | unit | bytes | why it is removable | evidence |
|---|---|---|---|---|
| D1 | **`SKILL.md:1332` registry header has no `\|---\|---\|` delimiter row**, so the whole 23-line / 16,041-char table is one run-on paragraph. Fix is 25 chars; the alternative minimal action is to delete the section | 16,041 (33% of the landed text) | GFM/CommonMark: a pipe header with no delimiter row is not a table [INFERENCE on the renderer, measured on the bytes]. It is the **only** one of 45 tables in the file without it; at base 0 of 43 lacked it; the wave-1 draft that produced this content **had** the row | `artifacts/R39W2Simplifier/tables-scan.txt`; draft `.ufo/waves/round-39/w1/artifacts/R39CL2Registry/registry.md:16` |
| D2 | `SKILL.md:317-329` — craft prose after the opening sentence: the six-field enumeration, the AVM/`-be` narrative, and the symlink/empty-envelope narrative | 975 of 1,165 prose chars | all three restate the 9-row executable table at 334-343 directly below them *and* the entry at `:11-54`; `sqfs-triage.py` reads the table, never this prose. Survives in a ≈250-char form: the rule marker (316), the entry citation `:11-28` **only** (currently 3 citations to the same entry), and the row-order rule ("Rows are tried top to bottom… `unclassified`", 329-331), which is stated nowhere else; the duplicated narratives go | `sizes.json`; craft table 3,045 chars |
| D3 | `corpus/knowledge/2026-10-26-r39-be-squashfs-v4-core.md:37-39` — "**Preconditions and failure signatures.**" paragraph | 308 | restates the triage entry `:21-40` (dep miss names `sasquatch-v4be`; `mkfs_time == bytes_used` drops `-be`), which this same entry already cites by path at `:32`; it also carries a dangling locator — "see the triage entry **above**" names a sibling file that appears nowhere above in this file | entry lines 32, 37-39 |
| D4 | `corpus/knowledge/…-core.md:42-43` — "A receipt-only counter cannot tell a re-minted fabricated receipt from a run; provenance comes from independent re-runs." | 203 | the disclosed limit already lives in the frozen claims (`plans/round-39-claims.md`, R39-C1 "Disclosed limit") and in the lesson (`:16`); the round-38 entry, the predecessor of this surface, carries no replicated counter-limit sentence | `artifacts/…/repeat-map.txt` |
| D5 | `SKILL.md:1335` row-3 tail "A crash is indistinguishable from `failed`; never cite this tool as a verdict" | 77 | duplicates the section's own intro 5 lines above ("Uncaught exceptions in the round-35/37/38 Python counters exit `1`, the code for `failed`", `:1330`); the intro covers all five counters, the row clause only one. Same paragraph also re-says row 3's "cannot return a verdict" twice | `SKILL.md:1330` vs `:1335` |
| D6 | `SKILL.md:1345-1353` — the **9 round-39 registry rows** | 2,643 | R38-CL2 names `freeze-drift.py`, `intended-doc.py`, `registry-immutable.sh` and "the c1/c2 counters" (`corpus/lessons/round-38-verifier-spotcheck.md:128`); the wave-1 draft scoped the section to round-35/37/38 (13 rows) and drafted no round-39 row. These 9 restate the frozen claims' verdict maps, `--selftest` case counts (33/27/35) and pinned paths for the same 9 tools. Keep only if the registry is meant to be a complete inventory — that is a charter decision, not an evidence one | `sizes.json` `registry_by_round_chars`; draft `registry.md:4-6` |

Priority: **D1 is the only structural defect** — a 25-byte fix turns 16 KB of dead markup into
the table the 7-column header promises (or, if the section is not wanted, D1+D6 together remove
18,684 chars, 37% of the landed text, with zero instrument impact). D2-D5 are ≈1.5 KB of
duplicated statements, each removable without touching a frozen byte or a binding.

Explicitly *not* a finding: the four blank lines between the craft table and `## Config custody`
(`SKILL.md:344-347`). The base file already carried four blank lines before that heading
(`a2f64e1d:SKILL.md:315-318`), so the landing neither added nor removed padding there.

## 3. Duplicate-statement census (what the diff repeats, measured)

Exact repeats across *added* text, with the surfaces that already held the fact:

| fact | added hits (`file:line`) |
|---|---|
| AVM marker drops `-be` when `mkfs_time == bytes_used` | SKILL:325, SKILL table row 339, entry-core:39, entry-triage:9,30,31 |
| kept in-tree link ⇒ exactly one `unpublished-entry` gap | PROVINCE:382, SKILL:327, SKILL table 342, README:93,199,201, entry-core:11,16,19,20,30, entry-triage:44,46, SOURCES:125 |
| escaping link ⇒ `MaliciousSymlinkRemoved`, no gap | SKILL:321,341, README:204, entry-core:31, entry-triage:15,42, SOURCES:124 |
| `is_safe_path` / extraction-root containment, no clamping | SKILL:341, SOURCES:128, entry-core:3,11,28, entry-triage:41, lesson39:33,47 |
| "AVM-BE and vendor-mangled stay Frontier / not claimed" | PROVINCE:384, README:93,244,245, entry-core:44, entry-triage:58 |
| re-minted-fabrication limit | entry-core:43, lesson39:16,94 |

Reading of the census:

- **Removable duplicates:** the AVM and symlink bundles inside the craft prose (D2), the
  preconditions paragraph (D3), the re-minted sentence (D4) — each is the **third or later** copy
  on a surface whose purpose is a pointer or an index.
- **Convention-required, not candidates:** the per-row repeats in `SOURCES.md` (the
  tag→commit `1fcc7a0a…` now appears 7×, 4 of them pre-existing, because each registry row is
  self-contained); the README coverage-map + knowledge + lessons triple (the file states "A row is
  written when its file exists", and round-38 carries the same three rows for its two entries);
  the lesson `## Gate` sources table (round-36 and round-38 lessons have the identical structure);
  the claims↔lesson repetition of the before/after verdicts (claims are frozen, lessons are the
  round record); the Frontier bullets, which are append-only dated history (round-36/38 bullets
  are explicitly labelled history and must not be rewritten).
- Per-row verbosity is **not** new padding: the new registry's median row is 764 chars against
  762 for the round-36 registry; the volume comes from 22 rows vs 2.

## 4. What I checked and did NOT delete

- `PROVINCE.md` round-39 additions (1,627 B = the Core row plus the frontier note): only "no new
  REA key" is unique in the row, but the row is the object `province_core_row` matches; keep.
- The round-39 frontier note's third sentence (R36-CL2 routed fix): ledger-required; keep.
- `QUALITY 82` row (774 B): carries a runnable gate + selftest count; nothing in it is repeated
  elsewhere except the M39-1 pointer, which is the criterion↔lesson convention; keep.
- Lesson `## Corrections to round 38` (3 bullets): append-only correction provenance for
  R38-CL1/CL3; deleting it would drop the only repair record; keep.
- The lesson's compressed quarantine line ("Quarantine slice: 5 rows, byte-identical to round
  38…") where round-36/38 lessons carry a dedicated `### Quarantine slice` section listing the
  five staged ids: this is *less* text than convention, not padding; no counter reads it.
- 90 path/line citations in the added lines were resolved against the tree; the 6 regex hits that
  did not resolve were brace-expansion artifacts (`K{1..6}`, `selftest/{…}`, `~/.local/share/uv/…`)
  and all six targets exist. No dead citation besides the "above" locator in D3.

## 5. Tradeoff

Trimming D2-D5 saves ≈1.5 KB but trades away redundancy that lets each surface be read alone: the
craft block would then require the entry open in parallel for the AVM story, and the Core entry
would lose its one-line precondition warning. I rank the trade as worth taking only together with
a pointer that keeps the AVM case one hop away (the row-order sentence already names the
interpreter, and the entry path stays cited), which is why the savings are stated as *available*
rather than *required*. D1 has no tradeoff at all.

## 6. Limits

- Render verdict for D1 is inferred from CommonMark/GFM rules plus the in-file convention (44 of
  45 tables); I did not run a Markdown renderer.
- No counter, REA run, or fabricated receipt was produced; `met_target` for C1/C2 is neither
  confirmed nor attacked here. Whether the registry rows' "exercised 2026-10-26" statements hold
  is out of this seat's scope and was not re-run.
- Every line number and byte count in this report refers to the **committed revision
  `52b0eb2907c704ed5f184c47b14c723208e5cbbc`**, read with `git show`/`git diff`, not the working
  tree. The live worktree is dirty from concurrent wave-2 seats (`git status`: `M PROVINCE.md`,
  `SCORECARD.md`, `SHONEN.md`, `SKILL.md`, `corpus/SOURCES.md`, both round-39 entries at 14:43-14:44
  — not this seat's writes). At least one of those edits touches D3's paragraph (it narrows the
  K5/K6 before-arm claim) but still restates the triage entry, so D3's reason stands; none of them
  adds the D1 delimiter row.
- Scratch `/fast/scratch/hyaku/kaidoku-r39/R39W2Simplifier` was used only for a `git diff`
  capture and the after-state export; it is removed at exit. No VCS mutation, no write outside
  this report and `artifacts/R39W2Simplifier/`.
- Tooling: nothing installed or upgraded this seat (no `uv tool`, `npx`, pacman or release
  binary); all measurements used `git` (read-only), `python3` stdlib and shell builtins.

## 7. Artifacts

- `artifacts/R39W2Simplifier/tables-scan.txt` — all 45 SKILL.md tables at tip vs 43 at base, with
  the single missing-delimiter table.
- `artifacts/R39W2Simplifier/repeat-map.txt` — the fact→line census above.
- `artifacts/R39W2Simplifier/sizes.json` — every byte count quoted in this report.
