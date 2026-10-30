# Draft — `## Round-52 additions to Core` (PROVINCE.md), R52-C1

**Status: DRAFT for the L1's freeze. Nothing here is a measurement.** Every `<PLACEHOLDER …>`
below is a number the L1 fills from the receipts it produces at the freeze and the data run.
No placeholder may be left in the landed file, and no placeholder may be filled with a value
that was not read out of a receipt (exit 0) — an unmeasured cell is a defect, not a
formatting nit.

Constants the v2 counter binds (claims `## R52-C1` → *Landing bindings*):
`core_heading` = `## Round-52 additions to Core` · `frontier_mark` = `Round-52 frontier note` ·
entry stem `2026-10-30-r52-avm-le-squashfs-core` · entry path
`corpus/knowledge/2026-10-30-r52-avm-le-squashfs-core.md` · `opened` `2026-10-30` ·
`prov_base` `/fast/scratch/hyaku/kaidoku-r52`.

**Binding shape the counter requires** (ported from `tools/round-50/c1-counter.py:2440-2457`,
receipt `counter-binding-code`; the constants at `:377-381` and `:426-428`, receipt
`counter-binding-consts`):

- `province_core_section` — a line exactly equal to `## Round-52 additions to Core`
  (`section()` takes the **first** occurrence of the heading line and reads until the next
  `## ` line, so the heading must occur exactly once).
- `province_core_row` — a `|` row **inside** that section whose **first cell** contains the
  token `squashfs_v4_le` (word-boundaried), whose row text contains `AVM[ _-]marker`
  (case-insensitive) **outside** the entry path, and which contains the entry path.
- `frontier_note` — one line anywhere in `PROVINCE.md` carrying `Round-52 frontier note`, the
  stem `2026-10-30-r52-avm-le-squashfs-core`, and an LE-AVM token (`LE AVM` / `AVM LE`,
  case-insensitive) **outside** the stem (the stem itself spells `avm-le` and is stripped
  before the token search).

The drafted text below satisfies all three as written; the check is re-run by the L1's counter
over the landed bytes.

---

## Branch A — the predicate holds (`carriers_matched == 4`, exit 0)

Append **at the end of `PROVINCE.md`** (after line 448, the round-50 frontier note). The
block below is contiguous: the L1 copies it as one piece.

```markdown
## Round-52 additions to Core

| Surface | Ports / keys | Probe | Verified evidence |
|---|---|---|---|
| genuine AVM-marker little-endian SquashFS v4 (`hsqs`, v4.0 xz, `mkfs_time == bytes_used`) members of four public FRITZ!OS images (FRITZ!Box 7581/7582 07.18, 6490 Cable 07.57, 6430 Cable 07.30 x86 members) — handler `squashfs_v4_le` | no new REA key — unblob 26.6.4 runs plain `sasquash -le` for every LE v4 chunk (S245 :53-54; the AVM marker test exists only in the BE branch, :48); `REA_UNBLOB_COMMAND` = unblob 26.6.4; `extract-firmware --max-depth 1` with the frozen `rea_parameters` budgets; the accounting rule is the device-accounting law frozen at `tools/round-52/gap-rule.json` (a device kind carries no disposition; `allowed` for a device kind is the empty list, so a device gap would be red) | entry `corpus/knowledge/2026-10-30-r52-avm-le-squashfs-core.md` (S243, S244, S245, S249, S250, S251, S252); carriers chain-pinned by `tools/round-52/fetch-vendor.py` (vendor bytes never committed) and re-scored from the round-50 pins under an explicit frozen allow-list; receipts `corpus/evidence/round-52/c1/<id>/run.json` and `.../after.json`; counter `tools/round-52/c1-counter.py` at the freeze <PLACEHOLDER — L1: the freeze commit sha> — `carriers_matched <PLACEHOLDER — L1: 4> of 4`, `frozen_path_changed []`, `law_shape_ok` <PLACEHOLDER — L1: true>, `census_rederived_ok` <PLACEHOLDER — L1: true>, `depth_gap_recorded` <PLACEHOLDER — L1: true>, every documentation binding true; score receipt `.ufo/waves/round-52/l1/scores/c1-after.json` |

The per-class census the rule is derived from — four carriers, two classes, read from the
frozen oracle tables `tools/round-50/oracle/<id>.nonregular.tsv` (sha256 `cb691b44…` /
`74f17174…` / `e8706799…` / `eff3f15e…`, receipt `oracle-tables-sha`):

| carrier class | carriers | char-devices per carrier | symlinks | dirs | non-regular entries | other kinds |
|---|---|---|---|---|---|---|
| Cable | `c6430`, `c6490` | **1** (`dev/led` `247:0`) | 568 / 613 | 255 / 300 | 824 / 914 | none |
| FRITZ!Box | `g7581`, `g7582` | **13** (`dev/led` `247:0`; `dev/pts/0`…`dev/pts/7` `136:0`…`136:7`; `dev/tiatm` `230:0`; `dev/ttyp0`…`dev/ttyp2` `3:0`…`3:2`) | 639 / 639 | 349 / 349 | 1001 / 1001 | none |

The class distinction is a property of the carriers' device census, not of the rule: the
frozen rule is the same for all four carriers. Under the law, **28 of 28** char-device census
rows carry no disposition — no published path, no `unpublished-entry` gap, no removal
diagnostic — over the committed round-50 envelopes (receipt `law-device-disposition`, exit 0,
28 rows, 0 with a disposition). The only gap kinds those envelopes contain are
`unpublished-entry` (567 / 612 / 636 / 636) and one `depth-limited` per carrier, whose
`relative_path` is null and whose `input_path` is `$output/firmware.bin_extract` (same
receipt, `gap_kinds` lines).

Scope of this holding — what it does **not** claim:

- The four carriers are **re-measured**, not new coverage: no carrier was added this round,
  and the anti-replay waiver for their four pins is an explicit frozen list, visible in the
  receipt, never silent.
- Four carriers, one vendor (AVM), `xz` only, depth 1 — **not** "every LE AVM image". The
  other models' LE members, the big-endian ARM `sqsh` member inside the Cable images and the
  LE bodies of other vendors are outside this holding.
- The law's measured width is **char-device only** (28 of 28 rows). The corpus contains **no**
  fifo, socket or block-device row on any of the four carriers (the kinds present are
  `symlink`, `dir`, `char-device`), so those kinds of the law are **not exercised**. Per the
  landed round-51 entry `corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md` (S250 at
  tag 4.7.5) the fifo and socket creation calls sit **outside** `unsquashfs.c`'s
  `if(root_process)` gate, so the unprivileged-`mknod` mechanism is established for
  char/block devices only: the fifo/socket part of the law is neither source-grounded nor
  exercised, and it is not claimed here.
- The law is a statement about the entries the extractor **reached**: a device-only subtree
  that was never descended into cannot be distinguished from one that was reached and
  correctly produced no gap. The `depth-limited` gap's `input_path` and `continuation_id` are
  recorded in the receipt so the limit stays visible.
- The documentation bindings are **presence checks**. A cited sentence is not a semantic proof
  of the sentence it binds.
- Availability is not holding: the lane holds hashes, listings and receipts, never the vendor
  bytes (AVM's licence permits one personal backup copy only, S249), and an image AVM replaces
  makes the chain unfetchable.

Round-52 frontier note, 2026-10-30: LE AVM members (`hsqs`) moved Frontier → Core with `2026-10-30-r52-avm-le-squashfs-core` (four chain-pinned FRITZ!OS members re-measured under the device-accounting law frozen at `tools/round-52/gap-rule.json`; `carriers_matched <PLACEHOLDER — L1: 4> of 4`). This note supersedes the LE-AVM clause of the round-40, round-41, round-42, round-44, round-49 and round-50 frontier notes and of the round-41 section's status paragraph, and nothing else. Still Frontier: AVM kernel images, nested sub-images below depth 1, LE AVM rootfs of ~13k files under REA's 120 s limit (FRITZ!Box 7530/7590, observed), and the fifo, socket and block-device kinds of the device-accounting law, which the corpus does not exercise.

The `## Round-50 measured, not promoted (R50-C1 honest stop)` block above and the round-41,
round-42, round-44, round-49 and round-50 frontier notes stay as history; this note
supersedes their LE-AVM clause and rewrites none of their other clauses. The round-51 entry
`corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md` ("NOT promoted (round 51 honest
stop)") also stays as history; its source corrections (S250/S251) are cited by the round-52
entry.
```

### Why the row satisfies `province_core_row`

- first cell: `… — handler `squashfs_v4_le`` → `HANDLER_RE` matches (`squashfs_v4_le` is
  backtick-delimited, so neither word-boundary lookaround fails);
- row text outside the entry path: `genuine AVM-marker little-endian SquashFS v4` →
  `AVM[ _-]marker` matches (`AVM-marker`, case-insensitive);
- the entry path `corpus/knowledge/2026-10-30-r52-avm-le-squashfs-core.md` is in the row.

---

## Branch B — the predicate does **not** hold (honest stop)

If the fresh run reports `carriers_matched < 4`, or any binding is false, **no
`## Round-52 additions to Core` heading may be landed at all** — the heading's presence is
itself the `province_core_section` binding, so landing it would make the counter's
documentation binding assert a promotion the data does not support. Land instead, in the
round-40/round-50 house style:

```markdown
## Round-52 measured, not promoted (R52-C1 honest stop)

Recorded 2026-10-30 after scoring: the frozen counter `tools/round-52/c1-counter.py` at the
freeze <PLACEHOLDER — L1: the freeze commit sha> matched <PLACEHOLDER — L1: the matched count>
of 4 carriers (exit <PLACEHOLDER — L1: the exit code>). <PLACEHOLDER — L1: the failing
clause(s), quoted from the receipt — e.g. `gaps_ok` false on …, or `carriers_matched < 4`>.
The row below is a measurement record, not a Core promotion; LE AVM members (`hsqs`) stay
Frontier and the repair (a further re-freeze) waits for a new freeze.

| Surface | Ports / keys | Probe | Verified evidence |
|---|---|---|---|
| genuine AVM-marker little-endian SquashFS v4 (`hsqs`, v4.0 xz, `mkfs_time == bytes_used`) members of four public FRITZ!OS images — handler `squashfs_v4_le` | <PLACEHOLDER — L1: the ports actually exercised> | <PLACEHOLDER — L1: the receipts, the counter and the score receipt> |

Round-52 frontier note, 2026-10-30: LE AVM members (`hsqs`) **stay Frontier** — the round-52 re-freeze measured <PLACEHOLDER — L1: the matched count> of 4 under the device-accounting law frozen at `tools/round-52/gap-rule.json` (`2026-10-30-r52-avm-le-squashfs-core`). Still Frontier: LE AVM members (`hsqs`), AVM kernel images, nested sub-images below depth 1, LE AVM rootfs of ~13k files under REA's 120 s limit.
```

Branch B leaves **all seven** historical LE-AVM lines untouched (see
`frontier-note-edits.md`), adds **no** `## Round-52 additions to Core` heading, and lands no
`## Round-52 additions to Core`-shaped Core row anywhere else in `PROVINCE.md` (the counter
scopes the row search to the section, but a stray row would be a false promotion claim
anyway).

---

## Placeholder ledger (the L1's fill list)

| # | placeholder | filled from |
|---|---|---|
| 1 | the freeze commit sha in the row | the L1's `FREEZE` record (`.ufo/waves/round-52/l1/FREEZE`) |
| 2 | `carriers_matched <n> of 4` | `corpus/evidence/round-52/l1/scores/c1-after.json` (`carriers_matched`) |
| 3 | `law_shape_ok` | the same receipt, field `law_shape_ok` |
| 4 | `census_rederived_ok` | the same receipt, field `census_rederived_ok` |
| 5 | `depth_gap_recorded` | the same receipt, field `depth_gap_recorded` |
| 6 | the `Round-52 frontier note` line's `carriers_matched` | the same receipt |
| 7 | Branch B's matched count, exit code, failing clause | the same receipt (`carriers`, `failing`, `exit_code`) |

Every fill must be a value read out of the receipt, quoted with its path. A value that cannot
be read stays a `<PLACEHOLDER — L1: …>` and the claim is reported as missed — never
estimated, never carried over from the round-50 receipt.
