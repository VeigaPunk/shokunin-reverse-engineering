# R41W2SrcReopen — findings (S127/S128 live re-open, round 41 wave 2)

Revision under test: `e9a24d07256d1606f01aa4d2d65f74e649c5f3d4` (`corpus/SOURCES.md`, rows at lines 133-134).
Re-open window: 2026-10-26, first server `Date` 21:19:10Z, image bodies 21:19:2x-21:20:3xZ.
Machine result: `check-reopen-output.txt` — **89 PASS, 0 FAIL**, checker exit 0.

## Rows: no falsification

Every checkable cell of both rows re-derived true against independently fetched bytes:
listing 574 B / sha256, info_en + info_de sizes and sha256 (recorded pair and a second fetch pair),
image `HEAD` 200 size / ETag / Last-Modified, ETag `mtime+size` arithmetic, CRLF/not-UTF-8 (with the
row's exact byte offset 17974 for S127), every quoted line at its stated line number, the licence
notice line ranges, the `xx.xx` template-image name on line 1, "no Build number", and the fact that
neither info file says anything about SquashFS or a filesystem layout (scope non-claims hold).
Registry shape: 11 cells, 12 pipes, ids novel against base `49096c7e` (whose max id is S126), appended
in order, used-by `corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md` exists at the same revision,
and the committed rows are byte-identical to the wave-1 draft they came from.

Additional bind attempted beyond the rows' own method (they record a `HEAD` only): both vendor image
bodies were downloaded in scratch, hashed, and deleted. *V3* 33 269 760 B sha256
`770efb4e368a58104bf362c990114db8b70a5060932ce8bcec7ef1bc75045ab7`, *V4* 36 392 960 B sha256
`a5a3a763a615c2dab226d15463bc05fbc74e844736687fa5cc87a91d2f35f661`. Both equal the
`carriers[i].external.image_sha256` pins in `.ufo/waves/round-41/c1/carriers.json`, and both sizes equal
the listing sizes. So the identity page each row cites describes exactly the bytes C1 pinned, not merely
a same-named file. No vendor bytes were kept.

## F1 — landing doc: licence-line citation in the entry is out of range for S127 (minor, not falsifying)

`corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md:128`:

    ... are the provenance [S127 licence lines 665-670 / 688-693 restrict
    redistribution and reverse engineering; ...

As written the bracket attributes both ranges to S127. S127's `info_en.txt` has 672 lines (last index
672), so lines 688-693 cannot be in it; they are S128's (`info_en.txt` 695 lines). The wave-1
crosscheck file shows the intended pairing — `.ufo/waves/round-41/w1/artifacts/R41SrcAvm/identity-crosscheck.tsv:18`
lists `info_en.txt L665-670` for 5490 and `info_en.txt L688-693` for 5491. Both ranges also skip the
notice's first line (© line: S127 L663, S128 L686), which the rows themselves cite as 663-670 / 686-693.
Repair text: `[S127 licence lines 663-670 / S128 686-693 ...]`. Effect if left: a reader following the
citation into S127's file finds no such lines.

## F2 — S128 support cell: "two years before" is 1.80 years (calibration nit)

`HKR 2021/11/17` -> stated release date `2023-09-04` is 656 days = 1.80 years. The inference the row
draws from it ("never date this carrier from the file tail") is unaffected and the staleness is real;
only the round number overstates by ~73 days.

## F3 — lessons gate table: the "located quote (<=25 words)" column is a description for S127/S128

`corpus/lessons/round-41.md:44-45` fills that column with "the info_en.txt product and version lines for
FRITZ!Box 5490, FRITZ!OS 07.31 (row cell, ...)" — a pointer, not a quote; the S129 row on line 46 carries
a verbatim quote. The rows themselves do carry located quotes of 11 / 6 / 4 words, so the registry is
compliant; only the lessons table cell is non-conforming with its own header.

## F4 — rows record no image digest, though the sibling vendor row does (coverage note)

S127/S128 record the image by `HEAD` (size, mtime, ETag) and never give an image sha256; the sibling
vendor row S125 (AVM 6490 Cable, same registry) records its image's sha256 outright. The digests exist
(`carriers.json`) and are reproducible (this re-open did it). Putting `image_sha256` into S127/S128 would
bind the registry's identity claim to the exact carrier bytes without a reader having to consult
`.ufo/`. The rows do not overclaim — their scope cell says "its size and mtime" — so this is an
enhancement, not an error.

## F5 — the anchor-cell quote is a condensation, not contiguous bytes (note)

`Product: FRITZ!Box 5490 / Version: FRITZ!OS 7.31 / Release date: 09/04/2023` joins three labels from
lines 8-14 with ` / ` and normalises tab/space runs. Each fragment is verbatim at its line (checked);
the fully verbatim text is in `w1/artifacts/R41SrcAvm/quote-excerpts.txt` and in `check-reopen-output.txt`.
Same convention as S125, so consistent across the round; recorded so a later reader does not grep for the
slashes in the vendor file.

## F6 — "opened" timestamps are not independently re-observable (limit)

The rows' `opened 2026-10-26T20:21:50Z` / `20:21:52Z` match `w1/R41SrcAvm.md` (20:21:50-51Z and
20:21:52-53Z) and the w1 probe TSV's later consolidated pass, but a re-open can only prove the source is
the same *now*. My earliest observation is the 21:19:10Z server `Date`. [INFERENCE] The timestamps are
consistent with the w1 artifacts; they are not proof of the instant of first access.

## Not attacked (out of this seat's scope)

- Whether the carriers extract, and the C1/C2 counters, receipts and controls (other seats).
- The V3/V4 member carve, `filesystem_core` nesting and lane-built L3/L4 carriers.
- AVM licence interpretation beyond quoting it: the notice forbids reverse engineering and
  redistribution; this seat downloaded the two images to hash them, kept only the digests, and deleted
  the bytes (recorded in `commands.sh` step 6).
