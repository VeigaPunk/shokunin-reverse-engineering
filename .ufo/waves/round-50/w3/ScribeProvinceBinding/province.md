# ScribeProvinceBinding — PROVINCE.md bindings draft (kaidoku round 50, attempt 2, wave 3)

Seat: `ScribeProvinceBinding` · 2026-10-29 · lane base `f890bbead20ca2c549487167f56876ae47f1e1a4`
(read-only; nothing landed, nothing committed, no REA run). Draft for the L1 (`KaidokuR50`) to
integrate; the L1 may rewrite it.

## 0. The entry stem — resolved by the L1's correction commit `6f4aba63`; this draft follows it

At the base given to this seat (`f890bbea`) the **frozen counter** and the **attempt-2
declaration** named two different entries; the counter is the machine gate:

| source | entry path | stem |
|---|---|---|
| `tools/round-50/c1-counter.py:377-378` (byte-frozen at `435d41fd4ad9211d1579fc447936fb33d2b74467`) | `corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md` | `2026-10-28-r50-avm-le-squashfs-core` |
| `plans/round-50-attempt2-claims.md` as of `f890bbea` (the attempt-2 declaration's first draft, *not* frozen) | `corpus/knowledge/2026-10-29-r50-le-avm-hsqs-core.md` | `2026-10-29-r50-le-avm-hsqs-core` |

The counter's `ENTRY`/`STEM` constants are read by four documentation bindings
(`province_core_row`, `frontier_note`, `entry_present`, `coverage_map_row`) and by the
`sourced` binding (the SOURCES `used-by` cell must carry the frozen path or stem). The counter
may not be amended (attempt-2 claims: "no new C1 freeze, no amendment"; the frozen claims:
"a counter bug found after the freeze is reported as a miss, never patched").

**Status at the time this draft was written (2026-10-29T20:35Z):** the L1 has committed
`6f4aba63` "round-50: attempt-2 claims corrected — entry stem pinned to the frozen counter
constants", which replaces the attempt-2 declaration's first-draft stem with the frozen one and
says so in the file: *"this file's first draft wrongly named a `2026-10-29-r50-le-avm-hsqs-core`
stem and is corrected by this commit before any data — the counter, not this file, is the rule"*.
**This draft therefore uses the frozen stem everywhere** (`2026-10-28-r50-avm-le-squashfs-core`),
which is what the counter reads. §3 keeps the rejected variant as the measured consequence, for
the falsify wave's calibration.

## 1. Paste-ready block — append at the end of `PROVINCE.md` (append-only; the round-49 note is history)

```markdown
## Round-50 additions to Core

| Surface | Ports / keys | Probe | Verified evidence |
|---|---|---|---|
| genuine AVM-marker little-endian SquashFS v4 (`hsqs`) members of four public FRITZ!OS images (FRITZ!Box 7581 and FRITZ!Box 7582, FRITZ!OS 07.18; FRITZ!Box 6490 Cable, FRITZ!OS 07.57; FRITZ!Box 6430 Cable, FRITZ!OS 07.30, x86 member) — handler `squashfs_v4_le`, AVM marker `mkfs_time == bytes_used` (v4.0, xz, compression id 4); four chain-pinned carriers of one vendor, depth 1, xz only; **not** every LE AVM image, and the ~13k-file LE AVM rootfs members (FRITZ!Box 7530/7590, FRITZ!OS 08.25) are **not** in this row | no new REA key — unblob 26.6.4 runs plain `sasquatch -le` for every little-endian SquashFS v4 chunk (its LE branch never reads the AVM marker, so the marker is a constant of the pinned bytes and not a routing input; `sasquatch-v4be` is not used and no `-be` binary is needed); `REA_UNBLOB_COMMAND=~/.local/bin/unblob` (26.6.4); `sasquatch` 4.5.1 on the child `PATH`; `extract-firmware --max-depth 1` with the frozen REA parameters `max_depth 1`, `max_output_bytes 536870912`, `max_output_files 100000` (the default 10000-entry staging budget is exceeded by these rootfs) | **Use:** `tools/round-50/c1-run.sh after --id <id> --carrier <CACHE>/<pin>.bin --data-run` (the L1's data procedure; it runs `npx -y rea-agents@6.5.0 extract-firmware --format json --full-output --max-depth 1 --max-output-bytes 536870912 --max-output-files 100000 <carrier> <scratch>/extract` with `REA_UNBLOB_COMMAND=~/.local/bin/unblob`, `sasquatch` 4.5.1 on the child `PATH`, and cwd and `TMPDIR` a private scratch under `/fast/scratch/hyaku/kaidoku-r50/`); the counter's own rerun uses node on the REA 6.5.0 package directly (`node <--pkg65>/rea-agents extract-firmware --format json --full-output --max-depth 1 --max-output-bytes B --max-output-files F <carrier> <outdir>`), never `npx`. **expect** one chunk whose `handler` is `squashfs_v4_le` with no failed chunk, `extraction_gaps` carrying only the frozen gap rule's dispositions (every symlink, char-device, fifo and socket of the oracle as an `unpublished-entry`, an escaping symlink as a `MaliciousSymlinkRemoved` removal at its exact path, the `dev/led` `247:0` char device allowed to carry no record, at most one `depth-limited` gap, no `unknown-chunk-handler`), and every regular file of the independent oracle (`unsquashfs` 4.7.5 listing plus per-file sha256; the lane's pure-Python `tools/round-41/sqfs-list.py --layout auto` reader equals it) published at its exact path under the chunk's extract root with the same sha256 and size and no extra regular file; **refusal signature** without `sasquatch` on the child `PATH`: a `missing-extractor-dependency` gap naming `sasquatch` and no published member | `tools/round-50/c1-counter.py` at the round-50 freeze (its own REA rerun is the measurement; the receipt, not the images, is the evidence); the frozen oracle tables `tools/round-50/oracle/g7581.oracle.tsv` (4556 regular files), `g7582.oracle.tsv` (4564), `c6490.oracle.tsv` (4709), `c6430.oracle.tsv` (3955) with their `*.nonregular.tsv` companions (639, 639, 613 and 568 symlinks; 13, 13, 1 and 1 char devices), and the frozen gap rule `tools/round-50/gap-rule.json`; second reader `/usr/bin/unsquashfs` 4.7.5 (squashfs-tools, a second reader from another release, not an independent producer) plus the lane's `tools/round-41/sqfs-list.py --layout auto`; the four carriers are chain-pinned and never committed (`tools/round-50/carriers.json`: image URL → image sha256 → tar member sha256 → carve to `bytes_used` → carrier sha256; AVM licence S249 — vendor bytes never enter the lane tree, only hashes, listings and receipts); REA receipts under `corpus/evidence/round-50/c1/g7581`, `g7582`, `c6490`, `c6430` (`after.json`, `run.json`) and the counter scores under `.ufo/waves/round-50/l1/scores/`; the carrier clauses matched 4/4 at the data commit `<REV>` (`carriers_matched 4`, `failing []`, `gaps []`; FILLED-AT-LANDING), the score at the landing revision is `.ufo/waves/round-50/l1/scores/c1-final.json` (FILLED-AT-LANDING); entry `corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md` (S243, S244, S245, S249) |

Round-50 frontier note, 2026-10-29: genuine AVM-marker little-endian SquashFS v4 members (the LE AVM `hsqs` rootfs images) moved Frontier → Core with `2026-10-28-r50-avm-le-squashfs-core` (four chain-pinned public FRITZ!OS carriers — FRITZ!Box 7581 and FRITZ!Box 7582 FRITZ!OS 07.18, FRITZ!Box 6490 Cable FRITZ!OS 07.57, FRITZ!Box 6430 Cable FRITZ!OS 07.30 x86 member — handler `squashfs_v4_le`, AVM marker `mkfs_time == bytes_used`, rea-agents 6.5.0 `extract-firmware --max-depth 1` with unblob 26.6.4 and sasquatch 4.5.1, second reader unsquashfs 4.7.5). This note supersedes the LE-AVM clause ("LE AVM members (`hsqs`)") of the round-40 frontier note, of the round-41 supersede body and of the round-41 frontier note, of the round-42 frontier note, of the round-44 frontier note and of the round-49 frontier note, and nothing else. Still Frontier: LE AVM rootfs of ~13k files under REA's own 120 s `provider_timeout` (the FRITZ!Box 7530/7590 08.25 members; measured, load-dependent, not claimed), AVM kernel images, nested sub-images below depth 1, `squashfs_v2_nonstandard` (`v2ns-*`; no independent reader), `squashfs_v3_broadcom`, `squashfs_v3_nonstandard` (and the DD-WRT no-pad/4k-pad v3 images), gzip v3 bodies, v4 Broadcom, v2.1 images and other vendor-mangled images.
```

**Shape rules the frozen counter enforces on that block (the L1 must not wrap the note):**

- The frontier note must be **one physical line** — `c1-counter.py:2454` searches
  `prov_text.splitlines()` for a line carrying `Round-50 frontier note`, the entry stem and an
  `LE AVM`/`AVM LE` token; a note wrapped over two lines fails the binding. The round-49 note
  above is one line for the same reason.
- The table row's **first cell** must name `squashfs_v4_le` (`HANDLER_RE`, word-boundary matched)
  and the row text **outside the entry path** must spell the AVM marker (`AVM[ _-]marker`);
  `corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md` must appear **verbatim** in the row.
- The section heading must be exactly `## Round-50 additions to Core`, and the section runs until
  the next `## ` heading — appending at EOF is correct.

## 2. Companion bindings the same claim needs (the L1's other surfaces, not mine)

| binding | what it needs | counter clause |
|---|---|---|
| `entry_present` | the file `corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md` exists at the landing revision, with `source:` lines naming S243, S244, S245, S249 | `c1-counter.py:2461` |
| `sourced` | those SOURCES rows are **opened 2026-10-28 or 2026-10-29** and their `used-by` cell carries the entry path or stem; the rows do not exist at the tip (`corpus/SOURCES.md` currently ends at S248 — S243, S244, S245 and S249 are still to be landed) | `c1-counter.py:2462-2477` |
| `coverage_map_row` | a `|`-line inside `corpus/README.md` `## Coverage map` carrying the stem, e.g. `| SquashFS LE-AVM (`hsqs`) v4 through REA `extract-firmware` | `2026-10-28-r50-avm-le-squashfs-core` | **Core** — four chain-pinned public FRITZ!OS carriers (7581/7582 07.18, 6490 Cable 07.57, 6430 Cable 07.30 x86), handler `squashfs_v4_le`, AVM marker `mkfs_time == bytes_used`; counter `tools/round-50/c1-counter.py` |` | `c1-counter.py:2479-2482` |

## 3. Variant B (rejected by commit `6f4aba63`) — the attempt-2 declaration's earlier stem

Landing the attempt-2 declaration's **first-draft** stem (`2026-10-29-r50-le-avm-hsqs-core`)
instead of the frozen counter's stem makes these bindings **false** at the landing revision,
with no change to the images or the receipts. Measured with the seat's offline binding check
(`check-bindings.py`, receipt 14 — it applies the counter's own constants, regexes and
`section`/`cells` helpers to the draft text):

| binding | result at the attempt-2 stem |
|---|---|
| `province_core_row` | false — the row must cite the frozen entry path verbatim |
| `frontier_note` | false — the note must carry the frozen stem |
| `coverage_map_row` | false — the README map row must carry the frozen stem |
| `entry_present` | false — the counter reads `corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md` (not measured here: it needs the file at REV) |
| `sourced` | false — the SOURCES `used-by` cell must carry the frozen path or stem |

Consequence: `carriers_matched` may be 4 with every carrier clause green, and C1 still exits 1
on the documentation bindings — a miss caused by naming, not by the images. The counter cannot be
amended, so the entry path is the only free variable; commit `6f4aba63` resolved it in favour of
the counter. If the L1 wants the attempt-2 name visible for the falsify wave, the cheapest
reconciliation is one alias line **inside** the entry (an alias is not a second file, so the
`corpus/knowledge/**.md` count that C2's B1 atom re-derives does not move). Do **not** land a
second knowledge file: it would change that count and need a second coverage-map row.

## 4. What this draft does not claim

- It does not claim the four carriers were extracted: no REA run happened in this wave (the L1
  alone runs REA), and `<REV>`, the 4/4 score and `c1-final.json` are FILLED-AT-LANDING.
- It does not claim the AVM marker proves origin: the marker is a constant of the pinned bytes,
  invisible to unblob's LE branch and re-stampable; the claim is "REA publishes every oracle file
  of these four pinned vendor members".
- It does not claim the `~13k`-file LE AVM rootfs members (FRITZ!Box 7530/7590 08.25): they stay
  Frontier, load-dependent under REA's fixed 120 s `provider_timeout`.
- It does not name the four carrier sha256 pins in the row (they are in
  `tools/round-50/carriers.json` and the receipts; vendor bytes never enter the lane tree).
