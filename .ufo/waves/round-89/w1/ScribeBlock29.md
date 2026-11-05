# ScribeBlock29 (round 89, kaidoku) — craft rule block 29 revision candidate

Seat: ScribeBlock29 (scribe), leaf. Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, round 89, L1 KaidokuR89.
Base revision `0ec2bb4016655f605657d6e0e700ec2e6893ac27`. Axes: coverage, depth, calibration.

## Behavior

**No production edit.** L1 KaidokuR89 ruled that craft block 29 is **frozen** — it landed at commit
`8bbb40cc` in the declaration batch, and R89-C2's frozen kill rule reads "the block text changed after
this declaration", so an edit now kills the claim whatever it improves. My draft is kept as the
**round-90 revision candidate** and nothing in `SKILL.md` was touched.

The draft is the **field-class decision table**: for each `b_info`/`l_info`/`p_info`/PackHeader field
class, the pinned packer's refusal signature, the structural redundancy deciding recoverability, and
the lane's move. It separates the classes QUALITY 156 routed from round 88:

- `sz_unc := 0` -> packer `CantUnpackException: b_info corrupted`, **no redundancy** (the derivation's
  own bound `sz_unc0` is the only source) -> **refuse**.
- `sz_cpr := 0` / wrong-in-range / out-of-range / `sz_cpr := sz_unc + 1` -> chain geometry -> **recover**
  (all measured `field-value` or `chain-geometry`, `upx -t` clean, `upx -d` identity true, 4/4 each).
- the `sz_cpr > sz_unc` **arithmetic gate** named as a distinct packer-side refusal class, whose text
  is carrier-dependent.
- an **intact field is left byte-identical**.
- thresholds named: write window `b0+4..b0+8`, bound `0 < derived <= sz_unc0`, accounting key
  `(fits_u_len, total, -derived)`.
- **exit 0 is not recovery**: a `method` or `p_blocksize` tamper returns rc 0 and delta 0 while
  `upx -t` still refuses, so a move is judged by `upx -t` and `upx -d`.

## Routed items for the lesson and the QUALITY rows

### R1 — the plan's routing of `sz_cpr > sz_unc` is wrong as a *lane move*

The frozen plan (`plans/round-89-claims.md`, R89-C2 surface) routes "`sz_cpr > sz_unc` and the
PackHeader classes (arithmetic gate -> refuse)". The measurement says otherwise: the round-89 repair
**recovers** that class and every out-of-range wrong `sz_cpr`, because the derivation never reads the
stored value.

- Matrix pointer: `.ufo/waves/round-89/w1/ExecMatrix/matrix.json`, class `b0.sz_cpr:=sz_unc+1`
  (4 cells: `repair.rc 0`, `repair.info_class "field-value"`, `repaired_tests_clean true`,
  `repaired_identity true`) and class `b0.sz_cpr:=0xFFFFFFF0` (4 cells, same verdict).
- Tool pointer: `tools/round-89/upx-field-value-repair.py` selftest case
  **`wrong-out-of-range-recovered`** (line 214; `wrong-out-of-range-class` at 215) — "An out-of-range
  stored value is the same class: the derivation never reads it, so the packer's arithmetic gate firing
  early changes nothing here."
- I ran that selftest read-only: `python3 -I -B tools/round-89/upx-field-value-repair.py --selftest`
  -> `SELFTEST cases=16 failures=0`, **exit 0**.
- The correction: **`sz_cpr > sz_unc` is a packer-side refusal class, not a lane refusal.** The gate
  decides which message the packer prints; the redundancy (chain geometry, stored-value blind)
  decides the lane move, and for every wrong-value `sz_cpr` that is "recover". Only `sz_unc` has no
  redundancy and is refused.

### R2 — the `header corrupted` message for that class is carrier-dependent

- Matrix pointer: same file, class `b0.sz_cpr:=sz_unc+1` — **libz answers `corrupt b_info`**; jq, xxd
  and docker-init answer `header corrupted`. All four are `upx -t` rc 1. A row keyed on the message
  text splits one class into two; the row must key on the class.
- Packer-side explanation (UPX v5.2.0 `src/p_lx_elf.cpp`, sha256 `551fc867…d2dc`, matching the `S307`
  row at base): line 7105 `throwCantUnpack("corrupt b_info")` sits in the shared-object `un_shlib_1`
  path. `S311`/`S312` — the rows that would license citing these lines in a corpus row — are **absent
  at base** (`git show 0ec2bb40:corpus/SOURCES.md | grep -c "^| S311 "` -> 0), so the quote is recorded
  here, not in the block's Refs line.

### R3 — QUALITY Row 166's `M89-8` pointer is dangling (Row 166 is the row that carries R2)

`corpus/QUALITY.md:274` ends "…(correction routed to the round-90 block revision, **M89-8**)". But
`corpus/lessons/round-89.md` has exactly **seven** mistake rows, `M89-1`..`M89-7` (ids parsed with
`^\| (M89-\d+)` over the `## Mistakes` table at lines 16-26) — **there is no `M89-8` row**. Row 166's
cite is the only bare, path-less `M89-N` cite in rows 160-171; every other cite there is
path-qualified (`corpus/lessons/round-89.md` for Row 161, `ScribeLesson/report.md` for Rows 169 and 171).
The lane's only `M89-8` is ScribeLesson's seat-report row
(`.ufo/waves/round-89/w1/ScribeLesson/report.md:271`), whose subject is a **different** finding (the
dropped predecessor guards), and Row 169 already cites that id path-qualified. The
carrier-dependence fact R2 describes *is* in the lesson, but as prose at
`corpus/lessons/round-89.md:81`, not as a numbered row. **Fix:** add an `M89-8` lesson row for the
carrier-dependent gate (or re-point Row 166 at `corpus/lessons/round-89.md:81`) and path-qualify the
bare cite, per the "a record cell is re-derived by command" law
(`corpus/knowledge/2026-11-04-r86-record-agreement.md:9`).

### R4 — the lesson has a duplicated section heading

`corpus/lessons/round-89.md` carries `## Wave \`r89-w1\` — seat results` twice, at lines **64** and
**66**, with an empty section between them (the second has the content). `c40a36f21` added one copy
(`git show c40a36f21 -- corpus/lessons/round-89.md | grep -c "^+## Wave"` -> 1) over the copy already
at `81cd0d73b`.

## The exact matrix cell ids relied on (carrier, class, `upx -t` message)

All from `.ufo/waves/round-89/w1/ExecMatrix/matrix.json`, `cells[]`, read with `python3 -I`; messages
verbatim, scratch paths normalized to `<work>`.

| # | carrier | class | `upx -t` message | repair |
|---|---|---|---|---|
| 1 | jq | `b0.sz_unc:=0` | `CantUnpackException: b_info corrupted` | rc 2 |
| 2 | xxd | `b0.sz_unc:=0` | `CantUnpackException: b_info corrupted` | rc 2 |
| 3 | libz | `b0.sz_unc:=0` | `CantUnpackException: b_info corrupted` | rc 2 |
| 4 | dinit | `b0.sz_unc:=0` | `CantUnpackException: b_info corrupted` | rc 2 |
| 5 | jq | `b0.sz_cpr:=0` | `CantUnpackException: b_info corrupted` | rc 0, chain-geometry |
| 6 | xxd | `b0.sz_cpr:=0` | `CantUnpackException: b_info corrupted` | rc 0, chain-geometry |
| 7 | libz | `b0.sz_cpr:=0` | `CantUnpackException: b_info corrupted` | rc 0, chain-geometry |
| 8 | dinit | `b0.sz_cpr:=0` | `CantUnpackException: b_info corrupted` | rc 0, chain-geometry |
| 9 | jq | `b0.sz_cpr:=true-8` | `Exception: compressed data violation` | rc 0, field-value |
| 10 | xxd | `b0.sz_cpr:=true-8` | `Exception: compressed data violation` | rc 0, field-value |
| 11 | libz | `b0.sz_cpr:=true-8` | `Exception: compressed data violation` | rc 0, field-value |
| 12 | dinit | `b0.sz_cpr:=true-8` | `Exception: compressed data violation` | rc 0, field-value |
| 13 | jq | `b0.sz_cpr:=true+8` | `Exception: compressed data violation` | rc 0, field-value |
| 14 | xxd | `b0.sz_cpr:=true+8` | `Exception: compressed data violation` | rc 0, field-value |
| 15 | libz | `b0.sz_cpr:=true+8` | `Exception: compressed data violation` | rc 0, field-value |
| 16 | dinit | `b0.sz_cpr:=true+8` | `Exception: compressed data violation` | rc 0, field-value |
| 17 | jq | `b0.sz_cpr:=0xFFFFFFF0` | `CantUnpackException: b_info corrupted` | rc 0, field-value |
| 18 | xxd | `b0.sz_cpr:=0xFFFFFFF0` | `CantUnpackException: b_info corrupted` | rc 0, field-value |
| 19 | libz | `b0.sz_cpr:=0xFFFFFFF0` | `CantUnpackException: b_info corrupted` | rc 0, field-value |
| 20 | dinit | `b0.sz_cpr:=0xFFFFFFF0` | `CantUnpackException: b_info corrupted` | rc 0, field-value |
| 21 | jq | `b0.sz_cpr:=sz_unc+1` | `CantUnpackException: header corrupted` | rc 0, field-value |
| 22 | xxd | `b0.sz_cpr:=sz_unc+1` | `CantUnpackException: header corrupted` | rc 0, field-value |
| 23 | libz | `b0.sz_cpr:=sz_unc+1` | `CantUnpackException: corrupt b_info` | rc 0, field-value |
| 24 | dinit | `b0.sz_cpr:=sz_unc+1` | `CantUnpackException: header corrupted` | rc 0, field-value |
| 25 | jq | `b0.method^=0xFF` | `CantUnpackException: bad method 0xfd at 0x240` | rc 0, `intact`, clean **false** |
| 26 | xxd | `b0.method^=0xFF` | `CantUnpackException: bad method 0xfd at 0x240` | rc 0, `intact`, clean **false** |
| 27 | libz | `b0.method^=0xFF` | `CantUnpackException: bad method 0xfd at 0x2458` | rc 0, `intact`, clean **false** |
| 28 | dinit | `b0.method^=0xFF` | `CantUnpackException: bad method 0xf7 at 0x240` | rc 0, `intact`, clean **false** |
| 29 | jq | `l_info.version^=0xFF` | `Tested 1 file.` (rc 0) | rc 2 |
| 30 | xxd | `l_info.version^=0xFF` | `Tested 1 file.` (rc 0) | rc 2 |
| 31 | libz | `l_info.version^=0xFF` | `Tested 1 file.` (rc 0) | rc 2 |
| 32 | dinit | `l_info.version^=0xFF` | `Tested 1 file.` (rc 0) | rc 2 |
| 33 | jq | `l_info.format^=0xFF` | `Tested 1 file.` (rc 0) | rc 2 |
| 34 | xxd | `l_info.format^=0xFF` | `Tested 1 file.` (rc 0) | rc 2 |
| 35 | libz | `l_info.format^=0xFF` | `Tested 1 file.` (rc 0) | rc 2 |
| 36 | dinit | `l_info.format^=0xFF` | `Tested 1 file.` (rc 0) | rc 2 |
| 37 | jq | `p_info.p_filesize^=0xFF` | `CantUnpackException: p_info corrupted` | rc 2 |
| 38 | xxd | `p_info.p_filesize^=0xFF` | `CantUnpackException: p_info corrupted` | rc 2 |
| 39 | libz | `p_info.p_filesize^=0xFF` | `CantUnpackException: p_info corrupted` | rc 2 |
| 40 | dinit | `p_info.p_filesize^=0xFF` | `CantUnpackException: p_info corrupted` | rc 2 |
| 41 | jq | `p_info.p_blocksize^=0xFF` | `CantUnpackException: p_info corrupted` | rc 0, `intact`, clean **false** |
| 42 | xxd | `p_info.p_blocksize^=0xFF` | `CantUnpackException: p_info corrupted` | rc 0, `intact`, clean **false** |
| 43 | libz | `p_info.p_blocksize^=0xFF` | `CantUnpackException: p_info corrupted` | rc 0, `intact`, clean **false** |
| 44 | dinit | `p_info.p_blocksize^=0xFF` | `CantUnpackException: p_info corrupted` | rc 0, `intact`, clean **false** |
| 45 | jq | `PackHeader.u_len:=0` | `CantUnpackException: header corrupted 3` | **rc 1** (traceback) |
| 46 | xxd | `PackHeader.u_len:=0` | `CantUnpackException: header corrupted 3` | **rc 1** (traceback) |
| 47 | libz | `PackHeader.u_len:=0` | `CantUnpackException: header corrupted 3` | **rc 1** (traceback) |
| 48 | dinit | `PackHeader.u_len:=0` | `CantUnpackException: header corrupted 3` | **rc 1** (traceback) |

Cells 1-4 vs 5-8 are the QUALITY-156 pair: identical verbatim refusal text, opposite lane moves.
Cells 21-24 are R2. Cells 25-28 and 41-44 are the "exit 0 is not recovery" calibration
(`repaired_tests_clean false`, `repair_diff.positions` empty, delta 0, `info.class "intact"`). Cells
45-48's repair tail is `raise Refused("no validated PackHeader in the tail window")` /
`r87repair.Refused: no validated PackHeader in the tail window` — exit 1, not the documented rc 2.

## Gates

| gate | result |
|---|---|
| counter `shape()` (`MIN_WORDS 25`, `MIN_SPANS 2`) on the draft | `(True, [])` — **399 words, 55 spans** |
| counter `resolve()` against `git show 0ec2bb40:<path>` | `(True, [])` |
| QUALITY 159 separability | all three cited corpus documents **present at `0ec2bb40`** (`git show` exit 0 each); the **round-89 entry is not cited** |
| word band 250-400 | 399 |
| backticked spans >= 2 | 55 |
| repair selftest (read-only, for R1) | `SELFTEST cases=16 failures=0`, exit 0 |
| no production edit | `git status --porcelain` (tracked) empty |

## Touched surfaces

Written (this seat only):

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-89/w1/ScribeBlock29/block29.md` —
  the block text only, starting `- **Row 29 (`.
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-89/w1/ScribeBlock29/report.md` —
  citations, number provenance, routed items, full cell-id table.
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-89/w1/ScribeBlock29.md` — this file.

Not touched: `SKILL.md` (block 29 stays frozen as landed at `8bbb40cc`), `claims.json`,
`MANIFEST.json`, `corpus/`, `plans/`, `tools/`, `.ufo/state/`, `.ufo/watchdog.log`, the fleet root,
sibling lanes. No git/jj mutating command was run.

Concurrent changes observed while this seat worked, **not mine and left alone**: other seats landed
`5a46542a5`, `5068ba641` and `fd9f840bd` (the round-89 entry, instrument-registry rows, "QUALITY
166-167"), and `corpus/QUALITY.md` carries an in-flight **uncommitted** edit adding Rows 166-168. I
did not write to `corpus/QUALITY.md` and did not stage, commit or revert anything.
`git diff 8bbb40cc HEAD -- SKILL.md` touches only the instrument-registry table — the frozen Row 29
text is byte-identical to what landed at `8bbb40cc`.

## Out of scope (not done, not claimed)

- **The landed block 29 was not edited or replaced** — it is frozen by the L1's ruling; the draft is a
  round-90 revision candidate only.
- **No rerun of the frozen counters** (`upx-field-battery.py`, `depth-blocks-v2.py --expect-blocks 29`)
  as this seat's evidence; the L1 owns that. The pre-freeze receipts under `.ufo/waves/round-89/pre/`
  were read, not rerun.
- **No SOURCES row added** for the UPX v5.2.0 lines quoted above (`S311`/`S312` absent at base would
  break QUALITY 159); the quotes live in the seat report only.
- **The plan was not edited.** R1 records the conflict for the L1 to route.

## Findings

1. **`b_info corrupted` covers two fields with opposite moves** — the QUALITY-156 defect block 28
   left in place. `sz_unc := 0` and `sz_cpr := 0` produce the *identical* verbatim refusal
   `CantUnpackException: b_info corrupted`, but only the second is recoverable; the repair refuses
   the first with `refused: no l_info candidate carries a derivable first block` (rc 2, 4/4 cells).
2. **The packer's refusal text is carrier-dependent inside one class** (R2).
3. **Exit 0 is not recovery** — `b0.method^=0xFF` and `p_info.p_blocksize^=0xFF` return rc 0 with
   `info.class: "intact"`, delta 0 and `repaired_tests_clean: false`; the repair passes the file
   through unchanged and `upx -t` still refuses it.
4. **`PackHeader.u_len := 0` exits 1 with an uncaught `r87repair.Refused` traceback**
   (`raise Refused("no validated PackHeader in the tail window")`), not the documented rc 2.
5. **The repair refuses `l_info.version`/`l_info.format` tampers that the packer tolerates**
   (`upx -t` rc 0, `Tested 1 file.`); the refusal is the repair's own `l_info` locator gate, not the
   packer's.
6. **`p_info.p_filesize` is refused although it is redundant** — it duplicates the PackHeader's
   `u_file_size`; the repair keys on it and refuses (rc 2) rather than restoring it.
7. **The plan's `sz_cpr > sz_unc -> refuse` routing is wrong as a lane move** (R1).
8. **QUALITY Row 166 — the row that carries R2 — cites a lesson row id that does not exist** (R3):
   the lesson has `M89-1`..`M89-7` only, and the lane's only `M89-8` is a different finding.
9. **The lesson has a duplicated `## Wave r89-w1 — seat results` heading** at lines 64 and 66 (R4).

## Findings provenance

- Items 1-7 come from **ExecMatrix's receipt**
  `.ufo/waves/round-89/w1/ExecMatrix/matrix.json` (tool `field_matrix_r89.py`, sha256
  `f5ca2b35ac10f12b2f88e2e35d560a3899d9a6ee1220a29d4a7c3f7cd8d6dfbc`; `exit 0`, `met_target true`,
  `unclassified []`, `skipped_cells []`, `repair_selftest_rc 0`), re-aggregated by me with
  `python3 -I` over `cells[]` — not copied from ExecMatrix's prose table.
- The derivation thresholds come from the pinned repair source `tools/round-89/upx-field-value-repair.py`.
- The chain-geometry law, the `sz_unc` no-redundancy limit and the `b_info` layout come from the
  base-present knowledge entries cited in the draft's Refs line.

## Scope note for round 90 (observed, not acted on)

The round-90 plan is already open (`plans/round-90-claims.md`, `tools/round-90/`) and its R90-C2
targets **block 30** — the guard-and-control set a superseding instrument revision must inherit
(QUALITY 161/163/167/168/169/170/171) — a different scope from this seat's field-class decision table.
My draft is therefore not automatically an input to R90-C2; I touched neither the round-90 plan nor
its tools. What carries forward is R1/R2's substance (and, if still open, R3/R4).

## Integration note: the wave ledger's copy of this seat is stale

`r89-w1-results.json` (the wave evidence ledger, committed at `c40a36f21`) carries this seat's
**first** yield — R1/R2, the confirmations and the cell-id pointer, but **not R3 or R4**
(`"R3 —"` -> 0, `"R4 —"` -> 0, `"duplicated section heading"` -> 0). The authoritative copies are the
two files on disk (seat `report.md` and this file). Both are now tracked (the wave-evidence commit
swept them in) and my R3/R4 additions are **uncommitted working-tree changes** (85 added lines per
`git diff --stat`). An integrator that reads the ledger copy, or that commits only the committed
state, would miss the two new defects. I do not commit (leaf rule).

## Environment note (blocker for the L1, not actionable by this seat)

After my reply was delivered, L1 KaidokuR89's wake turn failed with
`Devin stream error failed_precondition: Your weekly usage quota has been exhausted`
(`https://app.devin.ai/settings/usage`). That is an account-level quota on the L1's model stream,
not a lane or host fault, and it is not fixable by a tool install — this seat has no authority to
change quota settings. **This seat's deliverables are complete and self-contained on disk**, so the
L1 can integrate from the three files below without depending on the IRC thread surviving.

## Artifact paths

- Block draft (round-90 revision candidate): `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-89/w1/ScribeBlock29/block29.md`
- Seat report: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-89/w1/ScribeBlock29/report.md`
- This report: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-89/w1/ScribeBlock29.md`
- Source of the cell numbers (read, not written by me):
  `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-89/w1/ExecMatrix/matrix.json`
- Frozen landed block 29 (untouched): `SKILL.md` at commit `8bbb40cc`
