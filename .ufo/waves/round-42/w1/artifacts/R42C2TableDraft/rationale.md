# Block 21 (table v4, amendment A1) — clause → row map, grammar, new rows, measurements, fallbacks

Seat `R42C2TableDraft`. Base `c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c`; precedence
`plans/round-42-claims.md` § R42-C2 **amendment A1** (15 steps), grammar decision from the L1
(`R42C2Grammar`): a 13th column `failing handler` after `handler`. Drafts: `block21.md`,
`block20-supersession.md`, `entry.md`. Tools: `make-fixture.sh`, `v4-refparse.py`,
`precedence.py`, `check.py`, `make-measurements.sh`. Evidence: `c-grid.tsv.gz`,
`c-heldout.tsv`, `c-dev.tsv`, `c-v3pairs.tsv`, `measurements.md`, the MIT fixtures, the two
own dev envelopes, and the six committed dev-arm envelopes under
`.ufo/waves/round-42/w1/artifacts/R42C1DevRun/envelopes/`.

## 1. Clause → row

Every row pins `operation = extract_firmware` and `provider = unblob`, so step 1 and step 15
are the no-match pair `(unclassified, none)`.

| step | clause | row (label) | cells |
|---|---|---|---|
| 1 | OP ≠ `extract_firmware` or PR ≠ `unblob` | — | no row matches; domain cells on every row |
| 2 | `F = ∅` ∧ `depth-limited ∈ G` | `container-depth-limited` | handler `none`, gap `depth-limited+` |
| 3 | `F = ∅` | `no-squashfs-chunk` | handler `none`, gap `*` |
| 4 | dep gap: D holds `sasquatch-v4be`, else `sasquatch`, else continue | `dep-missing-be`, `dep-missing-le` | gap `missing-extractor-dependency+`, deps `sasquatch-v4be+` then `sasquatch+`; no third row, so a set naming neither falls to step 5 |
| 5 | failure ∧ P > 0 | `partial-body-failure` | gap `extractor-failure+`, files `>0` |
| 6 | failure, P = 0, BE = `no`, `squashfs_v4_be ∈ HF` | `avm-marker-be-dropped` | handler `squashfs_*`, failing handler `squashfs_v4_be`, be `no`, files `0` |
| 7 | failure, P = 0, `HF ∩ L ≠ ∅` | `legacy-body-failure` | handler `squashfs_*`, failing handler `squashfs_v[123]*`, files `0` |
| 8 | failure, P = 0 | `body-extractor-failure` | handler `squashfs_*`, gap `extractor-failure+`, files `0` |
| 9 | `unknown-chunk-handler ∈ G` | `unknown-residue` | handler `squashfs_*`, gap `unknown-chunk-handler+` |
| 10 | `depth-limited ∈ G` | `depth-limited` | handler `squashfs_*`, gap `depth-limited+` |
| 11 | SR = yes ∧ `unpublished-entry ∈ G` | `mixed-symlinks` | gap `unpublished-entry+`, sr `yes` |
| 12 | SR = yes ∧ G = ∅ | `escaping-symlink-removed` | gap `none`, sr `yes` |
| 13 | G = {`unpublished-entry`} | `in-tree-symlink-metadata` | gap exact `unpublished-entry` |
| 14 | G = ∅: P > 0 → clean, P = 0 → clean-empty | `clean`, `clean-empty` | gap `none`, files `>0` / `0` |
| 15 | anything else | — | no match |

Two loosenings are literal rather than narrower, and both are decision-neutral: rows 13-15 use
`sr *` where v3 used `sr no` (step 11 takes every `SR = yes` + `unpublished-entry` envelope one
step earlier, step 12 takes every `SR = yes, G = ∅`). Control: `block21-ctl-srno.md` is the same
block with `sr no` on those three rows; over the 38 664-point grid the two tables differ on **0**
points.

## 2. The thirteen-column grammar

`handler` is a glob over `F` (`none` = `F` empty, `*` = any `F`). `failing handler` is a glob over
`HF` — the handlers of the `extractor-failure` gaps, or `F` when none carries one — and `*`
matches anything, an empty `HF` included. Only steps 6 and 7 name it, because only they say *the
failing handler*. This column is what removes the seam the first draft carried: with a
single handler column keyed on `F`, a two-chunk envelope (`F = {squashfs_v3, squashfs_v4_be}`, one
of them failing) had no way to say which chunk failed, and the table disagreed with the text on
168 grid points. With `failing handler` the two engines agree on **all 38 664** reachable points.

`L` is `{h ∈ F : h starts squashfs_v1 | squashfs_v2 | squashfs_v3}`, so step 7's predicate is
`HF ∩ L`, i.e. "a legacy handler that is also a handler of this envelope". The table says "`HF`
matches `squashfs_v[123]*`". They differ only when `HF ⊄ F`, which REA cannot mint: a gap's
`handler` field is the chunk's own handler (S119 `FirmwarePublication.js:226-238`, handler copied
in `chunkGaps`). The grid therefore generates `HF ⊆ F` only and the divergence is disclosed in the
entry's Limits (1).

Three deltas against the v3 reader, all in `v4-refparse.py` with selftests (12/12):

1. marker `v4`; a craft section whose only marker is v1/v2/v3 is refused (exit 2);
2. `dependencies` accepts the `+` contains form (membership: "D holds `name`"), which repairs the
   round-41 MEDIUM finding `w2/R41W2C2Table.md` F1 — measured: 2 016 of 2 016 grid points with
   `D = {sasquatch, sasquatch-v4be}` and a dependency gap now answer `dep-missing-be`, where the
   exact-set form answered `unclassified`;
3. the thirteenth column, `H` read from chunks ∪ gaps (the v3 reader read chunks only).

## 3. R41-CL4 repaired in prose, and executed

v3's row 1 already read `handler none`, but its other eleven rows read `squashfs_v4_*`, so a carved
v1–v3 chunk matched **no row** — and v3's *precedence* sent the same chunk to `no-squashfs-chunk`.
v4 makes every non-AVM row family-wide and keeps `none` for the true no-chunk case. A v1–v3 chunk
is not `no-squashfs-chunk` because unblob carves it with one of seven handlers (S112
:102,:159,:200,:245,:319,:364,:410) and extracts it with plain `sasquatch` (S112 :37,:51-54): an
outcome about a filesystem the finder did see, and `inspect-input` would send the reader to the
wrong object.

Measured on two own dev envelopes from the same 4 096-byte `squashfs_v3_le.bin` fixture:

```
--max-depth 1  H=['squashfs_v3'] G=['depth-limited'] P=2  v3: (unclassified, none)   v4: (depth-limited, raise-depth)
--max-depth 3  H=['squashfs_v3'] G=none              P=2  v3: (unclassified, none)   v4: (clean, none)
```

## 4. The new rows, from sources and measured envelopes

**`container-depth-limited` (step 2).** The depth ceiling is minted per path REA did not descend
into, with an empty dependency list and a continuation naming the rerun (S119
`FirmwarePublication.js:23-29,:294-299`). A container at `--max-depth 1` therefore produces
`H = {trx_v1}` (a non-SquashFS handler) with `G = {depth-limited}`. Measured on both arms of the
committed whole-TRX run (`.ufo/waves/round-42/w1/artifacts/R42C1DevRun/envelopes/trx-img-with.json`
and `-without`): `P = 3` (the TRX partitions), `G = {depth-limited}`, and the frozen v3 interpreter
answers `(no-squashfs-chunk, inspect-input)` on both. `raise-depth` is the same instruction the
depth row gives, and the row is above `no-squashfs-chunk` because "no handler at this depth" is not
evidence of no image.

**`unknown-residue` (step 9).** `unknown-chunk-handler` is minted per chunk whose handler is null
(S119 `FirmwarePublication.js:286`, `chunkGaps` at :226-238), and unblob carves the unclaimed range
to `<start>-<end>.unknown` in the extraction directory (S118 :116-127: `extension = "unknown"`
:119, `filename = f"{start}-{end}.{extension}"` :123). Measured on the committed carved-x86 run
(`x86-fs-with.json`): `H = {squashfs_v3}`, `G ⊇ {unknown-chunk-handler, depth-limited,
unpublished-entry}`, `P = 138`, and the published set carries
`firmware.bin_extract/786432-851972.unknown` (the 65 540-byte tail after the filesystem, per
`w1/R42C1DevRun.md`). v3 answers `(unclassified, none)`. The row is above the depth row because
that envelope carries both, and `isolate-residue` is the action: keep the residue out of the
filesystem oracle and re-carve the chunk to unblob's end.

## 5. The legacy row's action, justified

`cross-read-legacy`, never the `-be` wrapper:

1. **The AVM pre-check cannot apply.** unblob parses `mkfs_time == bytes_used` and appends `-be`
   only inside `case Endian.BIG, 4:` (S112 :40-50); every other version takes `case Endian.BIG, _`
   → `-be` or `case Endian.LITTLE, _` → `-le` and parses nothing (S112 :51-54). v1/v2 inherit the
   base extractor (S112 :75) and the v3 family overrides only the magic (S112 :323,:368,:414).
   On the wire with unblob 26.6.4: `handler=squashfs_v3 … command='sasquatch -le …'` for the LE
   fixture and `sasquatch -be …` for the BE one.
2. **`unsquashfs` is an independent reader of 1:0-3:0.** 4.7.5 reports `Found a valid … SQUASHFS
   1:0 / 2:0 / 3:0 superblock` and lists all four fixtures (both endiannesses, exit 0); 7-Zip
   26.04 lists the v3 trees and marks the BE one `Big-endian = +`. On six damaged copies the
   superblock still parses (`unsquashfs -s` exit 0) while both readers fail with the message
   sasquatch prints (`FATAL ERROR: File system corruption detected`), so agreement is the damage
   signature and a listing independent reader beside a failing sasquatch is an extractor
   build/argv fault — exactly the separation the action prescribes.

## 6. Measurements (all reproducible from this directory)

| measurement | result |
|---|---|
| grid, REA-reachable shapes (`HF ⊆ F`) | **38 664 / 38 664 agree, 0 differ** (`c-grid.tsv.gz`) |
| round-41 held-out, 52 envelopes | draft vs precedence **52/52**; draft vs frozen v3 interpreter **52/52** |
| dev envelopes, 8 real (`squashfs_v3` ×2, TRX whole ×2, TRX rootfs ×2, x86 rootfs ×2) | draft vs precedence **8/8**; v3 interpreter **0/8** (6 `unclassified`, 2 wrong `no-squashfs-chunk`) |
| four round-41 C1 receipts (real AVM) | both engines `(depth-limited, raise-depth)` |
| dependency membership (`deps=both` ∧ dep gap) | 2 016 / 2 016 `dep-missing-be` |
| `sr no` control (`block21-ctl-srno.md`) | 0 of 38 664 points differ |
| reader selftest | 12 cases, 0 failures (marker refusal, 13-column arity, contains form, handler class, failing-handler class, cause arrow, vocabulary, duplicate label) |

## 7. Fallbacks if the freeze rejects a piece

- **`failing handler` column rejected** (a 12-column table) → steps 6 and 7 collapse onto `F`, the
  168-point two-chunk divergence returns, and the held-out generator must exclude two-family
  envelopes; the entry must carry that as a limit instead of a repair.
- **`HF` from gaps rejected** (chunks only) → same as above, and step 9's handler cell must drop to
  `*` because an unknown chunk has no squashfs handler.
- **`dependencies` contains form rejected** → round-41 F1 returns (`D` naming both binaries →
  `unclassified`) and the entry carries it as a disclosed defect.
- **`squashfs_v[123]*` rejected by the pattern engine** → the legacy row cannot be written (one
  label owns one row, seven names, seven patterns); a `*` cell would also absorb broadcom BE
  failures and loses the family statement.
- **step 9 above step 10 rejected** (depth before residue) → the measured x86 envelope flips from
  `unknown-residue` to `depth-limited`, which is what v3 already said; the row would then be
  reachable only on an envelope with no depth gap.
