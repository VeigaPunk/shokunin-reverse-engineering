# corpus/README.md insertions for round 42 (R42-C1 coverage)

Target: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/README.md` at base `c4a38ea2`
(280 lines). Three insertions; none edits an existing line. The binding that matters is the
`coverage_map_row` one: the round-41 counter's `section()` stops at the next `## `, so a row in
`## Knowledge` does NOT satisfy it — edit 1 is mandatory, edit 2 is index practice.

### EDIT 1 — last row of `## Coverage map` (insert after base line 99, the `2026-10-26-r41-sqfs-triage-v3` row)

```markdown
| SquashFS v3 handler family through REA (round 42) | `2026-10-26-r42-squashfs-v3-core` | **Core** — `extract-firmware --max-depth 1` publishes every oracle regular file at its exact path relative to the chunk extract root on four frozen **published third-party** v3 images (`<<L1:carrier-1-id>>` `<<L1:carrier-1-product>>`, `<<L1:carrier-2-id>>` `<<L1:carrier-2-product>>`, `<<L1:carrier-3-id>>` `<<L1:carrier-3-product>>`, `<<L1:carrier-4-id>>` `<<L1:carrier-4-product>>`), with `sasquatch -le`/`-be` on the plain binary and never `sasquatch-v4be`; the oracle is two non-sasquatch readers (`unsquashfs` 4.7.5 and 7-Zip 26.04) that agree file-for-file; gaps one `unpublished-entry` per retained symlink (or a `MaliciousSymlinkRemoved` diagnostic for an escaping one) plus one `depth-limited`; scored `<<L1:carriers-matched>>`/4, exit `<<L1:counter-exit>>`. Supersedes, for the handlers measured, the `2026-10-26-unblob-format-matrix` row's "coverage claim only, never an extraction outcome" as a status (dated pointer; the old row is not edited). v1/v2 images, v4 Broadcom, non-gzip v3 bodies and the contents of the published files stay Frontier |
```

### EDIT 2 — last row of `## Knowledge` (insert after base line 214; practice, not scored)

```markdown
| `2026-10-26-r42-squashfs-v3-core` | SquashFS v3 handler family via REA, Core: one `SquashFSExtractor` for the whole family, `-le`/`-be` on plain `sasquatch` (both binaries declared as dependencies, `sasquatch-v4be` never executed for v3), chunk end from `bytes_used` plus the 4096/1024 zero-pad probe, a non-sasquatch oracle pair and its LZMA limit, exact extract-root path matching | S112, S116, S121, S119, S118, `<<L1:sources-rows-final>>`, S134; receipts `corpus/evidence/round-42/c1/`; counter `tools/round-42/c1-counter.py` | 2026-10-26 |
```

### EDIT 3 — `## Frontier` (insert after base line 258, the round-41 `sasquatch-v4be` bullet; the older bullets stay as dated history)

```markdown
- sasquatch — 2026-10-26 round 42: the SquashFS v3 handler family (`squashfs_v3`, `_ddwrt` `tqsh`, `_broadcom` `qshs`, `_nonstandard` `sqlz`) is **Core** (`2026-10-26-r42-squashfs-v3-core`), run by the plain `sasquatch` with `-le`/`-be` (never `sasquatch-v4be`); this supersedes the round-38 `unblob-format-matrix` line's "coverage claim only, never an extraction outcome" for the handlers measured, not for the site's coverage statement. Still frontier: SquashFS v1/v2 images, v4 Broadcom, v3 bodies whose blocks are not gzip (an LZMA-block v3 body defeats the `unsquashfs` leg of the oracle pair), big-endian v3 beyond the four frozen carriers, and what the published files do.
```

Notes for the L1:

- The Frontier bullet is keyed on `sasquatch`, not `sasquatch-v4be`, because the round-42 surface is the
  plain binary's `-le`/`-be` leg; the round-41 `sasquatch-v4be` bullet above it stays true for v4 and is
  not superseded.
- If a carrier is big-endian, the wording "little-endian" must not appear in the coverage-map row's
  status sentence; the entry's title already avoids it. The coverage row above is written without an
  endianness claim for that reason.
- If R42-C1 stops, edit 1 and edit 3 land as a `measured, not promoted` row/line with the failing clause
  named, exactly as the round-40 record does — never both.
