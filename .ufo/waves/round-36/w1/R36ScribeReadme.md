# R36ScribeReadme — corpus/README.md draft text (round 36, W1)

Seat: scribe (drafting only). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Base of this draft: tip `d2e46ef5` (`corpus/README.md`, 249 lines). Claim freeze
`790561d4e3aca732a434081aa9573ec2fa5fd7d0`; frozen claims read from `plans/round-36-claims.md`.
No file in the lane was written except this report. No VCS mutation, no subagents, no background
jobs, no tool install, no scratch dir created (no command needed one).

## Result

Three README edits drafted, append-only, in the existing table shapes:

- **A** — one new `## Coverage map` row carrying the stem `2026-10-26-r36-sasquatch-squashfs-recursion`
  (required by the frozen counter's `coverage_map_row` binding).
- **B** — one dated supersession row immediately after the Firmware row (README:44), which keeps the
  historical clause `recursion blocked by missing sasquatch` verbatim.
- **C** — one dated supersession bullet immediately after the `sasquatch (AUR)` Frontier bullet
  (README:227).

No historical text is rewritten by any draft.

## Why the assignment's third item lands in `## Frontier`, not `## Known gaps`

Assignment says: "the Known-gaps line README:227 (`sasquatch (AUR)`)". At `d2e46ef5`,
README:227 is `- sasquatch (AUR) — unblob squashfs recursion; 7z fallback covers today.` and it sits
inside `## Frontier` (heading README:221; `## Known gaps` starts at README:233). `grep -n sasquatch
corpus/README.md` returns only 44, 162, 227 — there is **no** sasquatch line in `## Known gaps`
(233-249). So draft C is placed in `## Frontier`, exactly the section the assignment's last sentence
covers ("Also draft the README `## Frontier` change if that section lists sasquatch"). No `## Known
gaps` edit is drafted; inventing one would add an unrequested bullet. Report of the discrepancy, not
a repair.

README:162 is a `## Knowledge` index row for the 2026-10-13 entry
(`squashfs needs sasquatch (7z fallback)`); historical, left untouched.

## Draft A — new `## Coverage map` row

Insert **after current line 88** (the `| Instrument admission (shortcut replay) | …` row, last row of
the table) and **before the blank line that precedes `## Knowledge` (README:90)**.

```markdown
| AppImage SquashFS recursion (round 36) | `2026-10-26-r36-sasquatch-squashfs-recursion` | held (bounded) — with sasquatch 4.5.1 on PATH, REA `extract-firmware` (rea-agents 6.5.0, unblob 26.6.4) publishes every regular file of an independent `unsquashfs` 4.7.5 oracle on four frozen carriers: K1 synthetic LE v4 xz 3/3, K2 synthetic LE v4 gzip 4/4, K3 nvim v0.12.6 x86-64 AppImage 2130/2130, K4 nvim v0.12.6 arm64 AppImage 2130/2130, with no `missing-extractor-dependency` gap; the paired no-sasquatch receipts publish none of those files (0/0/2/2 files in total, the two AppImage receipts publishing only carved ELF chunks) and name `sasquatch`; symlinks remain `unpublished-entry` gaps (K2 `var/notice-link`; K3/K4 `.DirIcon`, `nvim.png`) and each AppImage adds 17 unblob recursion outputs (carved ELF chunks, padding). Big-endian, AVM and vendor-mangled images were not tested; receipts `corpus/evidence/round-36/c1/K{1..4}/` |
```

Grounded in the committed receipts (facts below). The first cell is a section label in the shape of
other round rows ("ARM64X hybrid PE native-view import (round 32)"); `held (bounded)` follows the file's
`held (partial)`/`held narrowly` convention and keeps the symlink and big-endian/AVM limits visible.

## Draft B — dated note appended to the Firmware row

The Firmware row (README:44) must keep its text. Insert **immediately after current line 44** (after
the Firmware row, before `| Frontier prerequisites | …`):

```markdown
| Firmware (2026-10-26 note) | `2026-10-26-r36-sasquatch-squashfs-recursion` | dated supersession of the row above, which is not rewritten: the clause `recursion blocked by missing sasquatch` describes the 2026-10-13 unblob 26.6.4 state before sasquatch was installed; with sasquatch 4.5.1 (official onekey-sec `sasquatch_1.0_amd64.deb`, binary sha256 `ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754`) on PATH, REA `extract-firmware` recurses into LE v4 SquashFS and publishes the shipped AppImage payload (K3 2130/2130, K4 2130/2130 regular files against the independent oracle). The GSP binwalk region counts and the RISC-V bypass stated above are unchanged by this note |
```

## Draft C — Frontier supersession bullet

Keep README:227 verbatim. Insert **immediately after current line 227**:

```markdown
- sasquatch (AUR) — dated supersession of the line above (2026-10-26), which is retained as history: the AUR-only premise is superseded by the official onekey-sec `sasquatch_1.0_amd64.deb` (release `sasquatch-v4.5.1-6`; installed binary reports `unsquashfs version 4.5.1 (2022/03/17)`) running from `~/.local/bin`, and with it on PATH REA `extract-firmware` recurses into LE v4 SquashFS on all four round-36 carriers (`corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md`). The `7z fallback` clause is historical and was not re-tested this round (the claim excludes it); big-endian, AVM and vendor-mangled SquashFS remain untested.
```

## Grounded facts behind the drafts

All numbers below were read from the committed receipts at `d2e46ef5` /
`corpus/evidence/round-36/c1/` (`K*/before.json`, `K*/after.json`, `K*/oracle.tsv`,
`K*/oracle-run.json`, `K*/after-run.json`). Read-only commands used: `grep -n`, `sed -n`, `awk`,
`wc -l`, `git rev-parse --short HEAD`, `git status --porcelain`, `git log --oneline -3`,
`git ls-tree -r --name-only HEAD corpus/knowledge`, plus `python3 -` one-liners that parse those
committed JSON/TSV files (no writes).

| carrier | oracle regular files | before: published / oracle hits | before sasquatch gap | after: published / oracle hits | after sasquatch gap | after gaps | after bytes |
|---|---|---|---|---|---|---|---|
| K1 (LE v4 xz, offset 0) | 3 | 0 / 0 | yes, deps `["sasquatch"]`, `squashfs_v4_le`, offset 0 len 73728 | 3 / 3 | no | none | 70086 |
| K2 (LE v4 gzip, 4 KiB blocks, offset 0) | 4 | 0 / 0 | yes, same kind, offset 0 len 208896 | 4 / 4 | no | 1 `unpublished-entry` (`var/notice-link`) | 273971 |
| K3 (nvim 0.12.6 x86-64 AppImage, offset 944632) | 2130 | 2 / 0 | yes, same kind, offset 944632 len 10510336 | 2147 / 2130 | no | 2 `unpublished-entry` (`.DirIcon`, `nvim.png`) | 51122564 |
| K4 (nvim 0.12.6 arm64 AppImage, offset 936456) | 2130 | 2 / 0 | yes, same kind, offset 936456 len 10420224 | 2147 / 2130 | no | 2 `unpublished-entry` (`.DirIcon`, `nvim.png`) | 51792724 |

- Tool identities from the receipts: `unsquashfs version 4.7.5 (2026/03/01)` (oracle);
  unblob `26.6.4`, executable sha256 `0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09`
  (envelope `normalized_result.engine`); REA pin `rea-agents@6.5.0` (run records);
  sasquatch `/home/vgpnk/.local/bin/sasquatch`, sha256
  `ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754`,
  `-version` = `unsquashfs version 4.5.1 (2022/03/17)` (after-run records; the onekey-sec deb
  provenance is the R36ScoutSasquatchRelease report: deb sha256
  `efbc92bd27594e01211e1b582f105a463a0017360a0746a93de3f283906ade95`, member byte-identical to the
  installed binary).
- The 17 extra after-files per AppImage are unblob recursion outputs
  (`*.elf64_extract/carved.elf`, `*.padding` paths); they are not oracle rows.
  [INFERENCE] the K2/K3/K4 `unpublished-entry` gaps are symlink entries (gap objects carry no
  handler/provider/range, and `.DirIcon`/`nvim.png` are AppImage symlinks); the receipt states the
  kind and path, not the inode type.

## Gate observations (read-only; nothing rerun)

- `tools/round-36/c1-counter.py` interim receipt at
  `.ufo/waves/round-36/interim/c1-after-receipts-only.json`, argv
  `--root . --rev 3310d8fa27bfaa95ad858c4aaad6f6377f853982 --freeze 790561d4… --pkg65 <rea-agents 6.5.0>`:
  `carriers_unchanged: true`, `carriers_matched: 4`, per carrier `matched: true`,
  `before_oracle_hits: 0` / `after_oracle_hits` = oracle_files, `before_sasquatch_gap: true`,
  `after_sasquatch_gap: false`, both evidence ids ok. All document bindings were `false`
  (`entry_present`, `province_core_section`, `province_core_row`, `sourced`, `coverage_map_row`),
  `met_target: false` — the documents (entry, SOURCES row, PROVINCE Core row, this README row)
  did not exist yet at that revision. I did not run the counter; this is its stored output.
- `.ufo/waves/round-36/c2/after-at-d2e46ef5.json`: `mismatches: 0`, `guards_ok: true`,
  `met_target: true` at revision `d2e46ef5e2b2e8ba681b2fa55d50f298c4c4b8be`.
- **Calibration coupling for landing (binding on integration):** `c2-counter.py` `command_a`
  computes `mapped` = knowledge stems present in the `## Coverage map` section, `knowledge_files` =
  every `corpus/knowledge/*.md` stem at the measured revision. Today that is 122/122 (verified by the
  same regex locally). Landing the C1 entry **and** draft A makes it 123/123, while
  `SCORECARD.md:23` presently states `122/122 knowledge files mapped at cab59f22…`. C2 check O1
  (`stated` vs `command_a`) then mismatches unless the **first** count in that SCORECARD row is
  re-stated to 123/123 at the landing revision. This is the movement `plans/round-36-claims.md`
  already anticipates ("the row is re-stated then"); it is not mine to edit.
- Same regex reads the first `(\d+)/(\d+) knowledge files mapped`, so appending `123/123` later in
  the row without changing the first `122/122` would still fail O1.
- `SCORECARD.md:3104` also says "Coverage recipe A at `97358f75` gives 110/110 knowledge files
  mapped" (historical line, not read by C2). Observation only.

## Findings / routed notes for L1

1. **Assignment line mismatch:** README:227 is `## Frontier` (221-231), not `## Known gaps`
   (233-249); `## Known gaps` holds no sasquatch line. Draft C therefore sits in Frontier; no
   Known-gaps text is proposed. (Section placement verified by `grep -n '^## '`.)
2. **Firmware row clause is at README:44** and reads `AppImage SquashFS carved but recursion blocked
   by missing sasquatch` (verbatim); draft B supersedes it by date without touching the row.
3. **README `## Knowledge` table has no row for the new entry** (last row README:192,
   `2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop`). Not required by P36-C1 and not in this
   seat's instruction, so not drafted. If parity with rounds 26-34 is wanted, it is a one-row append
   after line 192 in the `| entry | topic | source | verified-at |` shape — flagging, not adding.
4. **Landing order:** entry (ScribeEntry), SOURCES row (ScribeSources), PROVINCE round-36 Core row
   (ScribeProvince), then drafts A/B/C, then SCORECARD O1 re-statement. Draft A alone makes
   `coverage_map_row` true but does not satisfy the counter without the other bindings.
5. **Draft A does not assert `met_target`** — it states the carrier leg and its limits. The frozen
   counter at the landing revision decides the claim.

## Bounds compliance

- Wrote only `.ufo/waves/round-36/w1/R36ScribeReadme.md`. No edit to `corpus/README.md` or any other
  lane file; no writes outside the lane; `/home/vgpnk/Projects/shokuknow` not touched.
- No VCS mutation (`git rev-parse`, `git status --porcelain`, `git log --oneline -3`,
  `git ls-tree` only).
- No subagents, no background jobs, no `agent://all`.
- No installs or upgrades; no pacman; `sasquatch` not reinstalled.
- No frozen predicate, counter, carrier or oracle changed; findings reported, not repaired.

## Artifact paths

- This report: `.ufo/waves/round-36/w1/R36ScribeReadme.md`
- Draft targets: `corpus/README.md` (lines 44, 88, 227 at `d2e46ef5`)
- Evidence read: `corpus/evidence/round-36/c1/K{1..4}/{before,after,before-run,after-run,oracle-run}.json`,
  `corpus/evidence/round-36/c1/K{1..4}/oracle.tsv`, `corpus/evidence/round-36/c1/carriers.json`
- Gate receipts read: `.ufo/waves/round-36/interim/c1-after-receipts-only.json`,
  `.ufo/waves/round-36/c2/after-at-d2e46ef5.json`,
  `.ufo/waves/round-36/w1/R36ScoutSasquatchRelease.md`
- Contract read: `plans/round-36-claims.md`, `tools/round-36/c1-counter.py`,
  `tools/round-36/c2-counter.py`, `tools/round-36/c1-run.sh`, `.ufo/waves/round-36/w1-spec.json`
