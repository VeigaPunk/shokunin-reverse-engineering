# PROVINCE.md insertion for round 42 (R42-C1 coverage: SquashFS v3 family, Frontier → Core)

Target: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/PROVINCE.md`.
Insertion point: **end of file**, after base `c4a38ea2` line 408 (the round-41 frontier note is the last
line at the base; the base file is 408 lines). Nothing above is edited: `## Round-41 additions to Core`
(:396-408) and the round-40 `measured, not promoted` block (:388-394) stay byte-identical and become dated
history.

What the round-42 port of the C1 counter reads out of this text (`tools/round-41/c1-counter.py` :1685-1701
and `tools/round-41/c1-extra.py` `note_verdict`, carried to round 42 with the constants changed):

| constant in the round-41 port | value this draft is written against | where it appears below |
|---|---|---|
| `CORE_HEADING` | `## Round-42 additions to Core` | heading |
| `HANDLER` / `HANDLER_RE` | a bare `squashfs_v3` token in the **first cell** of a row in that section | row, first cell (inside the parenthesis list) |
| layout token (round-41's `AVM_LAYOUT_RE`) | **all four** of `little-endian SquashFS v3`, `SquashFS v3`, `v3 family`, `SquashFS version 3`, so the text survives whichever spelling the port adopts | row + note |
| `ENTRY` | `corpus/knowledge/2026-10-26-r42-squashfs-v3-core.md` | row, last cell |
| `FRONTIER_MARK` | `Round-42 frontier note` at the start of **one physical line** | note |
| `STEM` | `2026-10-26-r42-squashfs-v3-core` | note |
| supersede verb (`c1-extra.py` `frontier_content`) | `supersede`/`superseded`/`supersedes`, stated twice | note |

```markdown

## Round-42 additions to Core

| Surface | Ports / keys | Probe | Verified evidence |
|---|---|---|---|
| little-endian SquashFS v3 and its vendor/format variants — the v3 family, i.e. the squashfs_v3 family of handlers (`squashfs_v3`, `squashfs_v3_ddwrt` (`tqsh`), `squashfs_v3_broadcom` (`qshs`), `squashfs_v3_nonstandard` (`sqlz`)), SquashFS version 3 | no new REA key — unblob 26.6.4 routes every SquashFS handler through one `SquashFSExtractor`; a v3 chunk runs the plain `sasquatch` with `-le` on a little-endian body and `-be` on a big-endian one (S112 lines 39-64), so `sasquatch-v4be` is never the v3 extractor though it stays a declared dependency of every SquashFS handler (S112 lines 68-69); `REA_UNBLOB_COMMAND=~/.local/bin/unblob` (26.6.4); `sasquatch` 4.5.1; `extract-firmware --max-depth 1` (the 10 000-entry staging budget) | `extract-firmware` (rea-agents 6.5.0) on four frozen published third-party v3 images no extractor touched before the freeze — `<<L1:carrier-1-product>>`, `<<L1:carrier-2-product>>`, `<<L1:carrier-3-product>>`, `<<L1:carrier-4-product>>` — against an independent oracle pair (`unsquashfs` 4.7.5 and 7-Zip 26.04, neither of which is sasquatch), exact path matching at the chunk extract root | entry `corpus/knowledge/2026-10-26-r42-squashfs-v3-core.md`; carriers `.ufo/waves/round-42/c1/carriers.json`; receipts `corpus/evidence/round-42/c1/C{1..4}/` (`after.json`, `oracle.tsv`, `nonregular.tsv`, `run.json`); counter `tools/round-42/c1-counter.py` -> `<<L1:score-artifact>>`, `carriers_matched <<L1:carriers-matched>>` of 4, exit `<<L1:counter-exit>>` |

The row above is the v3 handler family only. SquashFS v1 and v2 images, SquashFS v4 Broadcom, v3 bodies
whose blocks are not gzip (an LZMA-block v3 body has one working oracle, not two), and anything about the
programs inside a published rootfs stay Frontier.

Round-42 frontier note, 2026-10-26: the little-endian SquashFS v3 bodies and the v3 family of handlers (SquashFS version 3, the squashfs_v3 family) are **Core** for the handlers measured here (`2026-10-26-r42-squashfs-v3-core`); this note **supersedes**, for those handlers only, the status the round-38 `unblob-format-matrix` row carries — its README cell reads "coverage claim only, never an extraction outcome" and its body says "A support matrix claims coverage, never an outcome" — and that status is superseded by `## Round-42 additions to Core` (dated pointer; the old text is not edited), while the matrix row's own producer-coverage scope stands. It also names, without superseding, the triage v3 table's cause cell for a legacy-only chunk (`2026-10-26-r41-sqfs-triage-v3.md:22-24`, restated at :108-110): no envelope is relabelled here, and the round-42 table v4 that could relabel it is R42-C2's surface. Still Frontier: SquashFS v1/v2 images, SquashFS v4 Broadcom, non-gzip v3 bodies, big-endian v3 beyond the four frozen carriers, and the contents of the published files.
```

Line discipline: the note above is ONE physical line in the file. `c1-extra.py`'s round-41
`frontier_content` check reads `prov_text.splitlines()` and tests a single line for its clauses, so a
reflowed note fails it; two supersede-wordings are present because one is easy to lose in a copy-edit
(round-41 F2).

Fallback (required by the claim, not optional): if the counter does not reach 4/4 at the measured
revision, **this section is not landed at all**. The honest-stop replacement is the same heading
`## Round-40 measured, not promoted (R40-C1 honest stop)` pattern used above, with the status line
`<<L1:c1-status-line>>`, the failing carrier clause and score artifact named, and the Frontier note
changed from "is **Core**" to "is **measured, not promoted**" with the same supersession pointer. Do not
land the Core row and the stop record together.
