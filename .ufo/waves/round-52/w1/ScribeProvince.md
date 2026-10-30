# ScribeProvince — R52-C1 PROVINCE.md bindings (round 52, w1, attempt 1)

**Status: settled.** Drafts only; nothing landed, nothing measured beyond committed bytes.
No REA run, no download, no git mutation, no write outside
`.ufo/waves/round-52/w1/ScribeProvince/` (and the scratch, now removed).

## What I produced (all under `.ufo/waves/round-52/w1/ScribeProvince/`)

| artifact | what it is |
|---|---|
| `province-r52-core-section.md` | (1) the `## Round-52 additions to Core` section text, as **one contiguous block** (Branch A: promotion) and as the honest-stop block (Branch B: no Core heading at all), with the per-class census table, the fresh-run receipt pointers as `<PLACEHOLDER — L1: …>`, the honest scope, and a 7-row placeholder ledger naming what each fill must be read from |
| `frontier-note-edits.md` | (2) the exact Frontier-note line edits: which lines lose the LE-members clause, the dated supersession, every old line quoted verbatim, and a byte-exact replacement for each |
| `history-fate.md` | (3) the fate of the round-50 `measured, not promoted` section and of the round-51 NOT-promoted entry pointer (both kept as history, dated cross-references), the claims-vs-landed-entry **conflict**, and the SCORECARD rows the L1 owes |
| `receipts.tsv` | 20 receipts: receipt id · UTC · exit code · stdout sha256 · exact command |
| `law-device-disposition.py`, `binding-check.py` | the two read-only probes I ran, copied out of the scratch so every receipt is re-runnable |

## The three findings that matter

1. **There is no top-level LE-AVM Frontier bullet to delete.** `PROVINCE.md`'s `## Frontier`
   list (lines 73–127) carries **no** LE-AVM clause (receipt `province-le-avm-lines`: the only
   occurrences of "LE AVM members" are lines **394, 405, 408, 416, 430, 438, 448** — the
   round-40/41/42/44/49/50 frontier notes plus the round-41 section's status paragraph). The
   "bullet" the claim's phrasing points at is a **dated round note**, not a Frontier bullet.
   Recommended edit shape: **append-only dated supersession** (the lane's own precedent — the
   round-41 note supersedes the round-40 block *by reference*, and the round-49 note says
   "supersedes … and nothing else"), i.e. land the new `Round-52 frontier note` and touch
   none of the seven lines. The in-place clause removal is supplied line-by-line as Variant 2
   (old line quoted, replacement byte-exact) in case the L1 prefers it; I do not recommend it,
   because it rewrites dated round-40/41/42/44/49/50 history.
2. **The drafted section text satisfies the counter's own binding logic.** The v2 counter
   inherits `tools/round-50/c1-counter.py:2440-2457` (receipt `counter-binding-code`,
   constants at `:377-381`/`:426-428`, receipt `counter-binding-consts`). I re-ran that logic
   over `PROVINCE.md` + my drafted block: **Branch A** → `province_core_section` true,
   `province_core_row` true, `frontier_note` true, heading occurs exactly once (receipt
   `draft-binding-branch-A`, exit 0). **Branch B** → `province_core_section` false,
   `province_core_row` false, `frontier_note` true (receipt `draft-binding-branch-B`, exit 0)
   — i.e. the honest-stop branch reproduces the **round-50 landed shape** ("citation and map
   bindings true with the two Core-promotion bindings false"), so a missed claim lands no
   false promotion. The first draft of Branch B failed `frontier_note` (the note was wrapped
   over five lines and the mark/stem/token must share one line) — fixed before the receipts
   were taken; the failed run is not in the ledger.
3. **Conflict for the canonical judge: the law's width.** The claims' *Width* paragraph says
   the generalisation to "fifo/socket/block rests on the source ground"; the **landed**
   round-51 entry (`corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md`, S250 at tag
   4.7.5) says the opposite for fifo/socket: `mknod` for FIFO (`:1328`) and socket (`:1349`)
   sits **outside** `unsquashfs.c`'s `if(root_process)` gate, so "an unprivileged extraction
   cannot mknod, so char-device/fifo/socket rows all disappear" is **rejected**; and S252
   (CAP_MKNOD) gates **device files**, not FIFOs/sockets. My drafted scope therefore states
   the measured width as **char-device only (28 of 28)** and lists the fifo/socket/block kinds
   as **still Frontier and not exercised**. Two amendment options (A1: amend the claims'
   *Width* sentence to "block-device"; A2: keep the claims sentence and carry the narrowing
   in the round-52 entry) are set out in `history-fate.md` §3. **I did not edit the claims
   file** — it is the L1's amendment surface (`## Wave-1 amendment record`).

## What I measured (committed bytes only, read-only)

| fact | value | receipt |
|---|---|---|
| char-devices per carrier | `c6430` 1, `c6490` 1, `g7581` 13, `g7582` 13 | `census-char-devices` (exit 0, sha `2558bbc7…`) |
| kinds present in the four oracle tables | `symlink`, `dir`, `char-device` only — **no fifo, socket or block row exists** | `census-kinds` |
| undisposed FRITZ!Box device rows (the round-50 miss set) | 12 per carrier (`dev/pts/0-7` `136:0-7`, `dev/tiatm` `230:0`, `dev/ttyp0-2` `3:0-2`) | `census-frtz-twelve`, `census-g7581-devices` |
| device rows carrying **no** disposition in the committed round-50 envelopes | **28 of 28** (0 published, 0 gaps, 0 removals) | `law-device-disposition` (exit 0) |
| gap kinds per carrier | `unpublished-entry` 567/612/636/636 + one `depth-limited` each, `relative_path` null, `input_path` `$output/firmware.bin_extract` | `law-device-disposition` |
| round-50 miss receipt | `carriers_matched 2`, exit 1; `gaps_ok` false on `g7581`/`g7582`; `projection_ok` false on `g7581` only; `nonregular_unpublished_ok` true on all four; `frozen_path_changed []` | `r50-miss-receipt` |
| knowledge files in the lane today | **141** → the round-52 entry is the map's **142nd** | `knowledge-file-count` |
| oracle table digests | `cb691b44…` / `74f17174…` / `e8706799…` / `eff3f15e…` (nonregular), `f657ef51…` / `d4f660aa…` / `03b24463…` / `773fbc32…` (oracle) | `oracle-tables-sha` |

My census probes reproduce the round-51 wave's recorded shas exactly for
`census-char-devices` (`2558bbc72d3412a1`), `census-g7581-devices` (`a4a718f37e4f8d6a`) and
`oracle-tables-sha` (`5c07d99c5b2fd19d`) — an independent reproduction, not a copy.

## Gates I ran, and gates I did not

- **Ran (exit 0 unless stated):** the 20 receipts in `receipts.tsv`; the two branch binding
  checks; `disk-guard.sh status` (exit 0; `/fast/scratch/hyaku` 49 %, 414 G free) before the
  pass.
- **Not run, by contract and by design:** REA (`extract-firmware`) on any carrier; the
  four-carrier vendor re-fetch; the round-52 counter; the pre-freeze controls; any
  `--data-run`. No vendor byte was downloaded and no vendor byte is in the lane. Every
  `<PLACEHOLDER>` in the drafts stays a placeholder: the fresh-run numbers (`carriers_matched`,
  `law_shape_ok`, `census_rederived_ok`, `depth_gap_recorded`, the freeze sha, the gap counts)
  are the L1's to fill from the receipts it produces.

## Out of scope — the L1 must not miss these (I do not own these files)

1. `corpus/README.md:303` carries a **parallel** "Round-50 frontier note" with the same
   Still-Frontier LE-AVM clause; it needs the same dated supersession. `corpus/README.md`
   also needs the `## Coverage map` row for the stem `2026-10-30-r52-avm-le-squashfs-core`
   (the counter's `coverage_map_row` binding needs a `|` line inside `## Coverage map`
   containing the stem) and the `## Knowledge` index row. (README sha256
   `aad0c5907483f38fc0fcf82cb66f63d0b15a6554c3ad2d0d6d85c6a60b5da5db`, 303 lines.)
2. `SCORECARD.md`: the coverage head must name **141/141 → 142/142** (measured count in the
   receipts above); the round-50 section (`:3774-3815`) and the R51-C1/C2 rows (`:3838-3839`)
   stay as history.
3. The round-51 **wave draft** `.ufo/waves/round-51/w1/ScribeEntryC1/entry.md` (sha256
   `1ea47d43…`) was written for the stem `2026-10-30-r51-avm-le-squashfs-core` — **the same
   stem the L1 later used for the landed "NOT promoted" file** (sha256 `5792eebb…`). It must
   never be landed (it would overwrite that entry and import its own placeholders). The
   round-52 entry is a different stem: `2026-10-30-r52-avm-le-squashfs-core`.
4. The landed round-51 entry, its two README rows and the round-50 PROVINCE block are
   **kept byte-identical**; the round-52 supersession is by dated cross-reference
   (`history-fate.md` §1–§2 gives the exact optional insertion line for the round-50 block).

## Honesty note

Nothing in this seat's output is a measurement of round 52. The drafts are shaped so that a
miss is landable without a false claim (Branch B), and so that every number the L1 fills is
traceable to a receipt path. The only cross-claim hazard I found is the fifo/socket width
conflict in §3 above; it is the one item I could not close from inside my seat.
