# Counter-port delta for R42-C1 (what a mechanical port of `tools/round-41/c1-counter.py` gets wrong)

Read-only analysis for the L1. The round-42 counter is described in `plans/round-42-claims.md` as "a
round-42 port of the round-41 C1 counter". A port that changes only paths and ids will fail R42-C1 for
reasons that have nothing to do with the carriers. Each item names the round-41 constant, why it cannot
carry over, and the replacement this seat recommends. **These are recommendations, not results**: nothing
here was run against a carrier.

## D1 (blocking) — `compression_coverage` cannot be satisfied by a v3 carrier set

Round 41 (`tools/round-41/c1-counter.py`, `b['compression_coverage']`):

```python
comps = [d.get('compression') for d in (res.get('carriers') or {}).values()]
b['compression_coverage'] = (any(c == GZIP_ID for c in comps) and any(c in XZ_IDS for c in comps))
```

with `GZIP_ID = 1` and `XZ_IDS = (2, 4)` read from a **v4** superblock's `compression` member. The
`squashfs3_super_block` C definition in unblob 26.6.4 has no compression member at all (S112 :284-315;
v4's struct declares `uint16 compression` at :476), v3 blocks are gzip by construction, and
`unsquashfs -s` names no algorithm on a v3 image. So on four v3 carriers `compression` is absent or
`None` for every one of them, `any(c in XZ_IDS)` is false for ever, and `met_target` can never be true —
the counter would report a real 4/4 as a stop.

Replacement this seat recommends (a binding that is true only if the bytes support it):

```python
b['gzip_leg'] = all(d.get('oracle_unsquashfs_exit') == 0 for d in res['carriers'].values())
# every carrier's blocks are read by the gzip leg of the oracle pair; v3 has no xz leg to bind
```

and drop `compression_coverage` from `BINDINGS`. If the L1 wants a second decompressor leg, it must come
from a measured property (e.g. one carrier with fragments, one without), not from a field v3 lacks.
Evidence for the claim "v3 is gzip-only": the source struct, `unsquashfs -s` output on the fixtures
(`dev-evidence/dev-input-evidence.txt`), and the measured `unsquashfs` failure on an LZMA-block v3 body.

## D2 (blocking if copied) — `layout_ok` tests the AVM layout, which no v3 chunk has

Round 41's `layout_ok` requires a big-endian `sqsh` magic, v4.0, `mkfs_time == bytes_used`, and the
little-endian metadata block-length walk. None of that exists in v3. A port that keeps it fails every
carrier; a port that deletes it loses the structural check entirely.

Replacement: a per-carrier v3 structural clause, all four sub-tests from source, none from an extractor:

1. the magic at offset 0 equals the carrier's frozen handler pattern (S112 :244-264, :318-323,
   :363-368, :409-414) and `s_major == 3`. Measured offsets — do not reuse the v4 ones: `s_major` is the
   u16 at **0x1c (28)** and `s_minor` the u16 at **0x1e (30)**, verified on `squashfs_v3_le.bin`
   (`b[28:30] = 03 00`, `b[30:32] = 00 00`), on `squashfs_v3_be.bin` (`sqsh`, same offsets, BE field
   order) and on `squashfs_v3.le.1kpad.bin` (`b[30:32] = 01 00`, i.e. **version 3.1**). The v4
   `compression` field at 0x14 has no v3 counterpart (0 on all three fixtures), and the legacy 32-bit
   `bytes_used_2` at **0x08 is 0** on all three, so a reader that takes the size from the 32-bit copy
   reads zero — read the 64-bit field the way unblob's own `StructParser` does. A **minor policy is
   mandatory** in the frozen "major/minor" cell: both 3.0 and 3.1 occur in the producer's fixtures and
   nothing read here says which a carrier will be;
2. `0 < bytes_used <= carrier size`, and for an external carrier `carve length == bytes_used`
   (the round-41 `carve_ok` clause, unchanged in spirit);
3. **[INFERENCE, proposal to validate before freezing]** a metadata walk: `inode_table_start` and
   `directory_table_start` are the 64-bit fields at the end of the v3 struct (S112 :284-313), and a v3
   metadata block carries a 2-byte on-disk length before its compressed bytes, so walking those lengths
   from `inode_table_start` should reach `directory_table_start` — the v3 analogue of round 41's
   identity. This seat did not measure the walk; if it does not hold on real carriers, keep sub-tests 1,
   2 and 4 and drop the walk rather than weakening them;
4. the endianness of the two magics decides which of `-le`/`-be` the run must have used, so the receipt's
   handler name and the magic must agree (see D4).

**The frozen `layout_probe` does not merely reject v3 — it reports garbage.** Seat `R42C1Sentinel` ran
the round-41 `layout_probe` on all four v3 fixtures (`python3 -I -B`, one call each): it fails *before* the
magic/version tests, on the v4 `inode_table_start` read from `raw[64:72]` — reason
`inode_table_start 72057594037928190 outside the file` — and it reports `major: 768` (= 0x0300, the
unconditional big-endian read of 0x1c), `bytes_used` 1.38e19 and `compression` 0 on a little-endian v3
carrier (`.ufo/waves/round-42/w1/R42C1Sentinel.md` §10 A8, four-row table). Two consequences: a port check
of the shape `major == 3` over this probe's output rejects every LE v3 carrier, and the failure text reads
like carrier corruption rather than a v4-only tool — do not let a wave-2 seat explain it away as a bad
image.

Trap inside (3) and in the chunk boundary: `_SquashFSBase.calculate_chunk` computes
`end_of_data_offset = (start_offset + bytes_used) & 0xFFFF_FFFF` (S112 :82) before probing the
padding, i.e. the probe offset is truncated to 32 bits, and it returns `start + round_up(bytes_used,
pad)` for a padded image but `start + bytes_used` for a tight one. A carrier carved exactly at
`bytes_used` therefore produces a chunk that ends at `bytes_used`; a carrier left inside its 4 KiB
flash-sector padding produces a chunk to the padded end. The counter's `carve_ok` must not require
`chunk_end - chunk_start == carrier size` without allowing the padding branch, and it must not require
`carve length == bytes_used`: seat `R42C1Sentinel` measured the padded envelope — `squashfs_v3.le.1kpad.bin`
(1024 B, `bytes_used` 320, version 3.1) through REA `--max-depth 1` gives `chunks[0].range = 0-1024`,
handler `squashfs_v3` (`.ufo/waves/round-42/w1/R42C1Sentinel.md` §10 A1-A5). Recommended clause:
`bytes_used <= size <= round_up(bytes_used, 4096)` with a zero tail in the padding.

## D3 — `handler_ok` prefix and the four-name family

Round 41 used `HANDLER = 'squashfs_v4_be'` and `SQUASHFS_PREFIX = 'squashfs_v4'`. For round 42 the prefix
is `squashfs_v3`, and the claim's wording is "names a `squashfs_v3*` handler (**the one frozen per
carrier**)". Two consequences:

- the counter needs a per-carrier expected handler, not a single global handler, because a DD-WRT `tqsh`
  carrier must resolve `squashfs_v3_ddwrt` and an OpenWrt `hsqs` carrier `squashfs_v3`;
- a global `HANDLER_RE` for the *document* bindings should be the bare family head `squashfs_v3`
  (`(?<![A-Za-z0-9_-])squashfs_v3(?![A-Za-z0-9_-])`), which will not match `squashfs_v3_ddwrt`; the
  documents this seat drafted name the head bare in the first cell and the variants in parentheses, so
  both a head regex and a `squashfs_v3` prefix test pass.

## D4 — the argv claim is not in the receipt, and the dependency cell is not about v3

`get_dependencies` returns `[sasquatch, sasquatch-v4be]` for every SquashFS handler (S112 :68-69), so a
`dependencies` cell can name `sasquatch-v4be` on a pure-v3 run. If the port carries round 41's
`dep-missing-*` reasoning into C1 (it does not, but the receipt fields are shared), do not read that cell
as evidence about which binary the chunk used. The v3 argv fact is: plain `sasquatch` with `-le`
(little-endian magic) or `-be` (big-endian magic), measured on the fixtures
(`dev-evidence/dev-input-evidence.txt`), and source-grounded at S112 :39-64.

## D5 — the oracle needs an `oracle_agreement` clause, not just one `oracle.tsv`

Round 41 froze one `oracle.tsv` produced by the lane's own reader. The round-42 claim's oracle is a
**pair** that "must agree file-for-file before a carrier freezes". If the counter only re-reads one
`oracle.tsv`, a carrier whose two readers disagree can still score. Recommended extra clause, evaluated
at the freeze and at the measured revision:

```python
# oracle.tsv is the unsquashfs projection; oracle-7z.tsv is the 7-Zip projection,
# both RESTRICTED to regular files: 7-Zip cannot express a link target
b_pair = [r for r in rows(oracle_7z) if r.kind == 'file'] == [r for r in rows(oracle) if r.kind == 'file']
# and nonregular.tsv stays a single-reader (unsquashfs -lls) table, not an agreed one
```

Concretely: `unsquashfs -lls` gives rel/size/kind, extraction gives sha256; `7z l -slt` gives rel/size/mode
and `7z x` gives sha256. Measured on the fixtures, the two projections are byte-identical for both
endiannesses — on a fixture that has no symlinks. **Scope the clause to regular files**: seat
`R42C1Sentinel` measured that 7-Zip's `-slt` output carries a `Mode` but never a link target, that `7z x`
rewrites an absolute link and writes an escaping relative link as a 0-byte file, and that `unsquashfs`
cannot read an LZMA v3 body — so a literal "the pair agrees file-for-file, symlinks included" is
unsatisfiable on any carrier with links (`.ufo/waves/round-42/w1/R42C1Sentinel.md` §B3). Two readers on
the regular files, one reader on the non-regular table, and the gap rule then accounts for the links. Measured hole: an LZMA-block v3 body defeats `unsquashfs` 4.7.5 (`gzip uncompress failed
with error code -3`, exit 1) while 7-Zip extracts it — so the clause also refuses an LZMA carrier, which
is the desired behaviour (the claim says two readers must agree).

## D6 — `carrier_fresh_ok` chain and the dev-burned fixture

Round 41 read `PRIOR_CARRIERS = '.ufo/waves/round-40/c1/carriers.json'` plus a `prior_pins` list. Round 42
must chain at least to round 41 (`'.ufo/waves/round-41/c1/carriers.json'`), because those pins are the
most likely source of a relabelled receipt. The dev-burned input
(`tests/integration/filesystem/squashfs/squashfs_v3/little_endian/__input__/squashfs_v3_le.bin`, probe
2026-10-26 ~21:40Z) needs no clause of its own: the claim forbids fixtures as carriers, and `kind:
published` with a publisher URL is what makes a carrier admissible. Consider binding `kind ==
'published'` for all four, which also kills a lane-built substitute.

## D7 — `gap_rule.json` shape

The round-41 file's keys (`allowed` per non-regular kind, `required`, `removed`, `structural`) map
unchanged; what changes is content: v3 carriers are whole vendor rootfs images, so expect
`symlink → unpublished-entry`, `dir → []`, `char-device → []` (or `unpublished-entry` if the publisher
image carries device nodes), `fifo`/`socket` usually absent, `structural: {depth-limited: 1,
unknown-chunk-handler: 0}`, and `removed.diagnostic = MaliciousSymlinkRemoved`. `gap_rule_ok` fails on any
non-regular kind the after-receipts exhibit that `allowed` does not name, so the file must be written from
the carriers' `nonregular.tsv` and not guessed.

## D8 — the document bindings this seat's drafts were written against

`check-draft.py` (8 bindings, 14-case selftest) and `gate-crosscheck.py` (the round-41 gate's own code,
7 bindings, constants patched to `## Round-42 additions to Core` / `Round-42 frontier note` /
`squashfs_v3` / a `SquashFS v3`-class format regex / `coverage claim only` as the old-record phrase) both
pass on the drafts. What that proves: the text will not fail on a token, given a port that keeps the
round-41 *shape*. What it does not prove: that the port's chosen regexes are the ones tested here — the
drafts therefore carry five spellings of the format token in both the row and the note
(`little-endian SquashFS v3`, `SquashFS v3`, `v3 family`, `SquashFS version 3`, `squashfs_v3 family`).

## D9 — conflict on the `s_major` offset (reported verbatim for the judge)

`R42C1Sentinel` states: "`s_major=3` sits at 0x1e, not at 28; `layout_probe`'s `raw[28:30]` read returns 3
for these fixtures only by coincidence of neighbouring zeros". My own byte read of the same fixtures
contradicts the offset claim: on `squashfs_v3_le.bin` the bytes at 24..36 are
`00 00 00 00 03 00 00 00 00 00 10 00`, so `b[28:30] = 03 00` (u16 = 3) and `b[30:32] = 00 00` (u16 = 0);
on `squashfs_v3.le.1kpad.bin`, `b[28:30] = 03 00` and `b[30:32] = 01 00` (3.1). `s_major` is therefore at
28 and `s_minor` at 30 on both, which is also what unblob's `squashfs3_super_block` order implies. Their
*conclusion* stands and is what the draft adopts — do not reuse v4 offsets, and do not reuse
`layout_probe`'s v4 field reads — but the specific 0x1e claim is refuted by the bytes; the port must not be
written to read a major at 30.
