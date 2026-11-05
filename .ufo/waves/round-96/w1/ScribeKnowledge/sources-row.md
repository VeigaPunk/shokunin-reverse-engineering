# Draft — the S321 row for `corpus/SOURCES.md`

Seat ScribeKnowledge, round 96 attempt 1, lane kaidoku. This is the seat draft of the
row; the L1 appends it. The row is written in the file's 11-column table format
(id | source | kind | tier | scope | anchor | teaches | status | opened | recheck |
used-by), matching the shape of the last rows in the registry (S320 is the current last
row; S319 precedes it).

## The row to append (single line, `|`-delimited, no line breaks)

```
| S321 | `/usr/bin/printf` — sha256 `b2265abe04a2c237be085f12c14d3c70969f34ab3370a56f399727e4b38374d7` (host binary, own-work measurement) | tool | A | fresh-pack held-out arm source diversity | sha256 `b2265abe…`; upx 5.2.0 packable; receipt `pre/s321-fresh-source2-at-base.json` | A second, distinct little-endian x86-64 host binary carries the held-out fresh-pack arm without the carrier-specific cells: packed with `upx --best` twice it is byte-identical (`deterministic true`), its packed bytes collide with no public carrier (`collides_public_packed false`), and the same stop-boundary repair refuses the far cells and repairs the near ones on it (`fresh-source2 repaired 2 of 2; far-refused 2 of 2; intact 1 of 1 met True`) | mined | 2026-11-05 | on-release | corpus/knowledge/2026-11-05-r96-kill-rule-coverage.md |
```

## Field-by-field justification (each field traced to a committed byte)

| column | value | where it comes from |
|---|---|---|
| id | `S321` | the id named in `plans/round-96-claims.md` ("Sourced claim (frontier step)") and in `.ufo/waves/round-96/claims.json` (`sourced_claim.row`); the registry's last row is S320, so S321 is the next free id |
| source | `/usr/bin/printf` — sha256 `b2265abe04a2c237be085f12c14d3c70969f34ab3370a56f399727e4b38374d7` (host binary, own-work measurement) | the host binary the round's sourced step opened; the digest is the committed pin in `.ufo/waves/round-96/pins.sha256` (last line: `b2265abe…  /usr/bin/printf`) and the receipt field `source_sha256` in `.ufo/waves/round-96/pre/s321-fresh-source2-at-base.json` |
| kind | `tool` | the registry's kind enum is `spec\|docs\|paper\|code\|tool\|dataset\|talk\|book\|community\|own-work` (fleet `scripts/sources-census.sh`, E05); the source is a host binary measured by the lane's own instrument, and `tool` is the enum value the item fixes for this row |
| tier | `A` | the row's scope is exactly what the measurement establishes (source diversity of the held-out arm on a pinned, hash-named, re-measurable host binary); no tier-B/C qualifier applies |
| scope | `fresh-pack held-out arm source diversity` | the round-93 carried limit this closes is "the fresh-pack arm has one source" (`plans/round-96-claims.md`, sourced-claim section); the scope names the diversity property, not a repair capability |
| anchor | sha256 `b2265abe…`; upx 5.2.0 packable; receipt `pre/s321-fresh-source2-at-base.json` | the locator: the digest pins the bytes, `upx --version` on this host reads `5.2.0`, and the receipt is the committed measurement |
| teaches | the one grounded line in the row | it states the three properties the receipt actually carries — determinism (`deterministic true`), no public-carrier collision (`collides_public_packed false`), and the repair/refusal classes (`repaired 2 of 2; far-refused 2 of 2; intact 1 of 1`) — with the measured label quoted, so the row is falsifiable against the receipt |
| status | `mined` | the source was opened and measured this round and the row's `teaches` is cited by the knowledge entry |
| opened | `2026-11-05` | today; the source is opened in this round (the round's sourced step), not carried |
| recheck | `on-release` | the row is a host binary, not a published document: it is re-measurable by `sha256sum /usr/bin/printf` and a `fresh-source2-check` rerun; the cadence is the symbolic `on-release` the census accepts (E09) |
| used-by | `corpus/knowledge/2026-11-05-r96-kill-rule-coverage.md` | the knowledge entry this row's citation opens; the entry's provenance trio names S321 |

## Landing requirement (the row and its consumer must land together)

The census's `E11` finding fires for a `mined` row whose `used-by` path is not on disk.
At the declaration commit `e4d1f7de9deae83e6d5f78d2d7f0157196002af0` neither
`corpus/knowledge/2026-11-05-r96-kill-rule-coverage.md` nor `corpus/lessons/round-96.md`
exists, so the row must be landed **in the same commit** as the knowledge entry and the
lesson file — otherwise `E11` fires against S321 alone. This is the same landing
requirement the round-95 seat recorded for S320 (its `M95-a` drafting note).

The knowledge entry's `source:` line also names the row, so the two are mutually
citing: the row's `used-by` names the entry and the entry's `source:` names the row.

## Row-change log

- **S321 appended** (`mined`, opened 2026-11-05, recheck `on-release`, used-by
  `corpus/knowledge/2026-11-05-r96-kill-rule-coverage.md`).
- **No existing row is edited this round.** Rows S001–S320 keep their `status`,
  `recheck` and `used-by` cells unchanged. (CORPUS.md rule 2: only `status`, `recheck`
  and `used-by` change in place, and each such change is logged old→new in the round
  lesson; this round logs none.)
- Registry row count: **225 → 226**.
