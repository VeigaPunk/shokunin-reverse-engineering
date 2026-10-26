# Documentation bindings — literal strings for the R40-C1 freeze (from `artifacts/R40C1Counter/c1-counter.py`)

The counter's constants (read from the peer artifact, `c1-counter.py:174-178,197-203,247-266`):

```
ENTRY      = 'corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md'
STEM       = '2026-10-26-r40-avm-be-squashfs-core'
CORE_HEADING = '## Round-40 additions to Core'
FRONTIER_MARK = 'Round-40 frontier note'
HANDLER    = 'squashfs_v4_be'
HANDLER_RE = re.compile(r'(?<![A-Za-z0-9_-])squashfs_v4_be(?![A-Za-z0-9_-])')
AVM_LAYOUT_RE = re.compile(r'AVM[ _-]layout', re.IGNORECASE)   # IGNORECASE added by R40C1Counter
OPENED     = '2026-10-26'
```

The counter added `re.IGNORECASE` after this seat flagged the flag-less compile, so `AVM-layout`,
`AVM layout` and `AVM_layout` all bind; the text below keeps `AVM-layout`. Its `layout_ok` clause is
not marker-only: BE `sqsh` v4.0 **and** `mkfs_time == bytes_used` **and** `0 < bytes_used <= size`
**and** a little-endian first metadata block header, with the single-block identity used as the
tie-break when both decodes look plausible — which is why a marker-true standard-BE body and a
marker-false AVM-layout body each fail (`artifacts/R40AssimE3/controls/`). Its gap rule is frozen
data: structural kinds (`unknown-chunk-handler`, `depth-limited`) with a null `relative_path` are
allowed by `gap-rule.json`, so the Core row below names the gap story in that shape.

`section()` resolves the heading by exact line equality, `cells()` splits a `|`-leading line and
requires **exactly 11 cells** on a SOURCES row, and `frontier_note` is a **single physical line**.
So: do not wrap the frontier note, do not add trailing spaces to the heading, and keep every SOURCES
cell free of `|`.

## 1. `PROVINCE.md` — append at the end of the file

```markdown
## Round-40 additions to Core

| capability | what is held, and its evidence |
|---|---|
| standard AVM-layout big-endian SquashFS v4 (`squashfs_v4_be`) | **Core** — big-endian superblock with little-endian metadata block-length headers, promoted on the frozen carriers after `extract-firmware` (rea-agents 6.5.0, unblob 26.6.4, `sasquatch-v4be` 4.5.1) republished every oracle regular file on V1/V2/L1/L2 with no failed chunk, gaps limited to the structural kinds frozen in `gap-rule.json`, and the receipts' rerun projection matched; entry `corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md`; the layout is the block-length byte order, not the `mkfs_time == bytes_used` marker |
```

First cell contains `` `squashfs_v4_be` `` (the handler token, unquoted-adjacency-safe because of the
backticks); the row text carries `AVM-layout`/`AVM layout` and the full entry path.

## 2. `PROVINCE.md` — one physical line, appended after the Frontier note block

```markdown
Round-40 frontier note, 2026-10-26: the AVM part of the `- **sasquatch** — …` bullet under `### Round-4 frontier (post-unlock)` (`PROVINCE.md:156-157`) and the AVM clause of the round-39 frontier note (`PROVINCE.md:384`) are superseded by `## Round-40 additions to Core` above — a genuine AVM-layout image (little-endian metadata block lengths) is Core (`2026-10-26-r40-avm-be-squashfs-core`); vendor-mangled images and LE AVM members stay Frontier.
```

Carries `Round-40 frontier note`, the stem, and `AVM-layout` on one line. Do not soft-wrap it.

## 3. `corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md`

Bytes: this seat's `adopted-entry.md`, unchanged. Its six `source:` lines are S123, S124, S125,
S108, S107, S121 — every one of them a row this seat proposes with `opened = 2026-10-26` and
`used-by` naming this entry path.

## 4. `corpus/SOURCES.md` — three rows (from `sources-rows.md`, ids renumbered by document)

S123, S124, S125 as drafted, each with `opened` = 2026-10-26, `status` = mined, `used-by` =
`corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md`, 11 cells. Plus the three in-place
`used-by` extensions on S107, S108, S121 (old→new recorded in `sources-rows.md`).
R40SrcAvmVendor's draft row for the vendor member already names the same `used-by`, so the `sourced`
binding has two independent rows behind it.

## 5. `corpus/README.md` — a row in the `## Coverage map` table

```markdown
| AVM-layout big-endian SquashFS v4 (round 40) | `2026-10-26-r40-avm-be-squashfs-core` | **Core** — big-endian superblock with little-endian metadata block-length headers; marker is a timestamp proxy, not the layout; four frozen carriers (V1/V2 vendor members, L1/L2 lane-built AVM-layout) with an independent pure-Python oracle and a rerun-projection counter |
```

Any `|`-leading line inside `## Coverage map` containing the stem satisfies the binding; this one
also states the content.

## Pre-freeze self-check

`check-doc-bindings.py <lane-root>` applies the counter's own regexes to the five bindings and exits
0 when all are green, 1 otherwise; `--selftest` builds a temporary root that is green, then deletes
the frontier-note line and requires exit 1 (a red case that must fail). Run it after integrating,
before the freeze commit; it is a convenience, not a substitute for the counter.
