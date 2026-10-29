# SrcReopenUnblob — round-50 attempt-2 wave 3 (2026-10-29)

## Verdict

**MET (exit 0).** The unblob 26.6.4 LE-handler source re-open is byte-identical to the attempt-1 receipt (HTTP 200, 19,842 B, sha256 `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287`, 590 lines, fetched 2026-10-29T20:34:12Z), all three located quotes verified verbatim, and a draft S245 row (same URL as S108/S112, LE-branch scope) validates clean: `sources-census.sh validate` exits 0 with exactly one new W04 duplicate-URL warning, as predicted. Draft row + receipts saved for L1 integration.

## Findings

| # | Check | Command (abridged, cwd `$S`) | Result | Exit | sha256 / UTC |
|---|---|---|---|---|---|
| F1 | Fetch source | `curl -sS -o unblob-26.6.4-squashfs.py -w '…' https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py` | `HTTP_STATUS=200 SIZE=19842`; 19,842 B / 590 lines; byte-identical to attempt-1 and to S108's pinned hash | 0 | `2d7b901b…99287` / 2026-10-29T20:34:12Z |
| F2 | Line 455 | read `:450-465` of saved body | `class SquashFSv4LEHandler(_SquashFSBase):` (454) then `NAME = "squashfs_v4_le"` (455) — verbatim | — | body sha F1 |
| F3 | Lines 53-54 | read `:40-75` + grep | 53: `case Endian.LITTLE, _:` / 54: `commands_args.append("-le")` — verbatim | — | body sha F1 |
| F4 | `is_avm` uniqueness | grep `is_avm` whole file | occurrences at lines 48-49 ONLY (`is_avm = header.bytes_used == header.mkfs_time` 48; `if not is_avm:` 49), both inside `case Endian.BIG, 4:` (40-50). **Nuance vs task text:** "line 48 the only is_avm" — the *statement* is on 48, its *use* on 49; the substantive claim (AVM probe exists only in the BE-v4 branch; the LE branch appends `-le` with no AVM test) is CONFIRMED | — | body sha F1 |
| F5 | Baseline validate | `sources-census.sh validate --file $S/fixture/kaidoku-shokunin/corpus/SOURCES.md` (pristine copy; fixture mirrors `corpus/` + `SKILL.md` + `tools/round-27/xpin-attribute.mjs` so all 250 used-by paths resolve; `--file` lane id prints as literal `file`) | 18 × W04 + `file ok`; pre-existing W04 already covers this URL via S112 | 0 | stdout `ee9b71f6…852d21` / 2026-10-29T20:38:19Z |
| F6 | Validate with draft S245 | same command after appending draft row after S248 (line 159) | 19 × W04 + `file ok`; diff vs F5 is exactly: `file→W04→S245 duplicate url raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py across scopes` (tab-separated). No E-code, no E04 (scope string differs from S108/S112), no E11 (used-by = the two r44/r49 entries, which already cite this file's `:48-54`/`:53-54` LE branch) | 0 | stdout `806a9353…6f073` / 2026-10-29T20:40:04Z |
| F7 | Id collision guard | grep `S245` in lane `corpus/SOURCES.md` | no matches at base `f890bbea`; S150–S242 intentionally skipped per `plans/round-50-claims.md:259-261` | — | — |

## Bonus observations (same source, zero extra fetches — C3 context)

- Handler NAME map in the same file: `squashfs_v2_nonstandard` :200, `squashfs_v3` :245, `squashfs_v3_ddwrt` :319, `squashfs_v3_broadcom` :364, `squashfs_v3_nonstandard` :410, `squashfs_v4_le` :455, `squashfs_v4_be` :514, `squashfs_v4_broadcom` :549 — the three no-independent-reader families named in R50-C3 all exist in this one source.
- The BE branch reuses `SquashFSv4LEHandler.C_DEFINITIONS` and parses the header `Endian.BIG` (:42-46); the AVM test compares `bytes_used == mkfs_time` (:48), matching S114/S124's AVM-BE semantics.

## L1 integration notes

- Draft row: `s245-draft-row.md` (this dir). used-by cites existing entries so E11 passes at landing; append the R50-C1 entry to used-by once it lands. opened `2026-10-28` per attempt-2 claims wording; recheck `on-release` (S108 convention) — `180d` (S112 convention) also valid.
- W04 is warning-only by the script's own contract (`sources-census.sh:33,364-365`); landing S245 cannot flip validate exit.
- Full receipts (exact commands, exits, stdout hashes, UTC): `receipts.md`; raw outputs: `validate-baseline.out`, `validate-s245.out`; fetched body: `unblob-26.6.4-squashfs.py` (MIT-licensed upstream source, not vendor bytes).

## Bounds

Read-only on the lane tree except this report + `SrcReopenUnblob/` artifacts. No REA invocation. No git mutation (no git command run at all). No tool installs (authorization unused). Disk-guard checked pre-pass (497.2G free). Scratch `/fast/scratch/hyaku/kaidoku-r50/w3-SrcReopenUnblob` removed after receipts were copied out.
