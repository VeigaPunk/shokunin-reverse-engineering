# DRAFT reject record — AssimGate round 50 — staged `avm-le-variant-reachability`

Verdict: **REJECT** (fourth refusal: R39 critic, R40 AssimReject, R42 Assim, this round). Advice only.

## Why (each point re-measured or re-read on 2026-10-28)

1. **Headline false.** The entry says the AVM_LE route is closed: "With the correct define the image is still little-endian … and its `mkfs_time` … does not equal its `bytes_used`", and that the variant would close only with the option build or genuine firmware.
   - A clean plain-Freetz build with `-DTARGET_FORMAT=AVM_LE` and no option patch gives `mkfs_time` 361 == `bytes_used` 361 (`avm-le-plain550.squashfs`, sha256 `18d3ad05…afaee4`, byte-identical to the option build's `avm-le-genuine.squashfs`). Lane TSVs: `lead2-stale-build.tsv`, row `clean_rebuild_plain_freetz_550_define_AVM_LE`.
   - The 1792847340 reading came from a stale binary: the no-clean rebuild left binary sha256 `1a7cfcf7…` unchanged (`lead2-stale-build.tsv`, `binary_sha256_after_no_clean_rebuild`). Re-measured today: round-12 image sha256 `afeb55a4…` has `mkfs_time` 1792847340, `bytes_used` 365.
   - "With either" is wrong for the option build as well: the option build without `-no-mkfs-time` keeps the timestamp (`avm-le-standard-time.squashfs`, `mkfs_time` 1792871460 per the TSV; sha256 `6d787405…`). Patch 550 (S156) is what sets the marker for AVM_LE.
2. **Mechanism wrong.** The entry's "invisible marker" conclusion is not a route closure. Patch 550 (S156, lines 7-9) writes `mkfs_time` for AVM_LE. Patch 613 (S157) only makes it optional.
3. **No reversal pointer.** Three rounds refused it; no line names the reversing entry `avm-le-image-genuine-marker`.

## Surviving facts (kept in a corrections-only rewrite, if the L1 wants one)

- `#define AVM_LE 2` and `#define AVM_BE 3` (S155, `patch101.patch` lines 7-8): true.
- The string `AVM_BE_AVM_LE` occurs in 0 of the 23 Freetz master patch bodies (re-fetched 2026-10-28; `receipts/freetz-patches/`; the 23 names are in `receipts/freetz-patch-listing-from-html.txt`). The round-11 name was a filename, not a define. True.
- The round-12 LE image is refused by `sasquatch-v4be` ("Block size too small", exit 1, 0 files) — re-measured: true.

## Reversal line (to be appended, dated, to the rewrite)

"Reversal, 2026-10-28 (round 50): the headline 'AVM_LE is not reachable through the recipe; the route closes only with an option build or genuine firmware' is rejected. The stale-binary explanation is correct (`lead2-stale-build.tsv`); a clean build with `-DTARGET_FORMAT=AVM_LE` sets the marker (`avm-le-image-genuine-marker`, sha256 `18d3ad05…`; patch 550 `603c36c9…`). Rejected decision: the `Headline` and `Claim` paragraphs of this file (`merge/kaidoku/knowledge/corpus/knowledge/avm-le-variant-reachability.md`, lines 10-13 and 21-28 of the staged text)."

Flip: a rewrite keeping only the three surviving facts above, with the reversal line, becomes admissible as a corrections-only entry. No new source is needed.
