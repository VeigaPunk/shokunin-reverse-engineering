# Packed-ELF last-block `sz_cpr`: a stop-boundary tamper inside ±16 is repaired by the packer's verdict (round 92, R92-C1)

DRAFT by seat ScribeKnowledge — NOT LANDED. Target: `corpus/knowledge/2026-11-05-r92-stop-boundary-repair.md`. Every result is `RESULT:<pending L1>`; no number here is measured by this seat.

source: S313 — UPX v5.2.0 `src/p_unix.cpp`, https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_unix.cpp — re-opened in round 92: RESULT:<pending L1: access date, HTTP status, size, sha256>. Registry pin (round-91 re-open, same URL): sha256 `bf83c4133c27d39433db63bf604daf577d429d734c542d29c0b9cc8ed229642e`.
source: S311 (existing, round 89) — UPX v5.2.0 `src/p_lx_elf.cpp`, the `un_shlib_1` peek. Not used by this entry's measurements.
source: S313 supplies the per-block bound and the payload read, as the registry row describes them. It supplies no packer verdict, no candidate search and no carrier fact.
verified-at: RESULT:<pending L1: measured revision and receipt paths>
recheck: 180d — the counting command below and `python3 -I -B tools/round-92/stop-boundary-repair-battery.py --help` (exit 0).

## The class

A packed UPX 5.2.0 `--best` little-endian ELF whose **last** `b_info` block before the chain stop has `sz_cpr` moved by −7 or +7, both in range (`0 < value <= sz_unc`). The frozen counter scores five carriers: `jq`, `xxd`, `libz`, `dinit` (= `/usr/bin/docker-init`) and `xz-unseen` (= `/usr/bin/xz`, which the round-91 carrier list does not name), two directions each: ten near cells. Ten far cells at ±40 are the negative control. Five intact carriers are the identity control. Interior blocks are the round-90 class (`2026-11-04-r90-interior-block-szcpr`).

## The rule (as declared; the built tool is verified by the L1)

Candidate: `tools/round-92/upx-stop-boundary-search-repair.py`, sha256 RESULT:<pending L1>.

- Input green under `upx -t` → return the input byte-identical, rc 0.
- Input red → for every `v` in `stored−16 .. stored+16` with `0 < v <= sz_unc`, write `v` into the four-byte `sz_cpr` field of a private copy and run `upx -t` on it.
- Exactly one green value, the output differs from the input only inside the four-byte window, and the output is green → write that output, rc 0.
- Zero or two-or-more green values → typed refusal, rc 2, no output file.

The window `±16` is the tool's declared bound, not a property of the format. The packer's verdict chooses the value; the frozen counter measures whether the written output is locally confined (`unsafe`, `wrong`) only on its own cells.

## Measured

- Do-nothing control, the round-91 repair under the frozen counter at base `73a882712`: `repaired 0 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10`, met False, exit 1 (`.ufo/waves/round-92/pre/c1-control-do-nothing-round91-repair.json`).
- Candidate under the frozen counter at the measured revision: RESULT:<pending L1: label, met_target, exit, revision, counter sha256 `63e9df431f5d7aeeca2bd5384efff36b4f2ebedfdc3ee71aaa250287fc9388bc`>. Receipt: RESULT:<pending L1: `.ufo/waves/round-92/l1/scores/c1-at-<rev>.json`>.
- Per-cell classes (`repaired`, `wrong`, `unsafe`, `silent`, `refused`) and the wall time per tampered cell: RESULT:<pending L1>.
- Reproduction by a wave seat at the same revision: RESULT:<pending L1: seat name and receipt path>.

## Limits

- **Window.** The counter measures near cells at ±7 and far cells at ±40. Deltas 8 to 16 are inside the tool's declared window and are not measured by the frozen counter. Repair of those deltas is not claimed unless a receipt names them.
- **Oracle.** The counter scores `repaired` as byte-identity with the pristine packed bytes it packed itself; the tool selects with `upx -t`. The two oracles differ, so the score does not grade the tool with its own oracle. The intact arm measures identity (rc 0, output equal to input) on five intact carriers; it does not measure `upx -t` agreement on any other input.
- **Counterfeit embedding.** [INFERENCE, not run] A repair whose green test is membership in a table of the five pinned packed images would pass the frozen label, because the pristine bytes are in the table. This counter does not exclude that counterfeit. Round 92's C2 counter excludes the four-entry table (measured: counterfeit B, `intact 4 of 5`, `pre/c2-counterfeit-B-v2.json`); it does not exclude a five-entry table.
- **Five carriers, two directions.** Not a population claim. 32-bit ELF and `--lzma` output are outside the counter's carrier list and are not measured here.
- **Packer dependence.** The result depends on `upx 5.2.0`, sha256 `cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969`. [INFERENCE] A packer whose `upx -t` disagrees with the decoder would change the outcome.
- **Uniqueness.** "Exactly one green value" is measured only where the frozen label reaches `repaired 10 of 10`: on the five carriers, two directions, at ±7.
- **Cost.** The declared search tries up to 33 values, so up to 33 `upx -t` runs per red input. The measured cost is RESULT:<pending L1>. No cost is measured by this entry for the round-92 tool; the round-91 cost curve (`.ufo/waves/round-91/w1/SentinelWrite.md`) concerns the round-91 tool.
- **Refusal.** On any cell where the window has zero or two-or-more green values the declared tool refuses. The round-91 refusal row is superseded only if the frozen label is met at the measured revision.

## Counting command

Template. `<measured revision>` is a placeholder the L1 replaces with the commit it measured. A receipt that still says `<measured revision>` is the round-91 M91-2 defect and is not a result. The counter records `--rev` as a label; it does not verify it.

```sh
python3 -I -B tools/round-92/stop-boundary-repair-battery.py --root . \
  --repair-cmd tools/round-92/upx-stop-boundary-search-repair.py \
  --work <scratch> --rev <measured revision> \
  --expect "repaired 10 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10" \
  --json-out <receipt>
```

Exit 0 means the label equals `--expect` and the counter's own `met` conditions hold. The kill rule's pin check (the counter and imported instrument sha256 against `.ufo/waves/round-92/claims.json`) is a separate step the L1 performs on the receipt. Do-nothing control: the same command with `--repair-cmd tools/round-91/upx-stop-boundary-repair.py` at `73a882712` (exit 1, measured above).

## Gate

| row | URL | access date | HTTP / size / sha256 | located quote (≤25 words) | used for |
|---|---|---|---|---|---|
| S313 | https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_unix.cpp | RESULT:<pending L1> | RESULT:<pending L1> | PENDING-scout | the per-block bound `sz_cpr > sz_unc` and the payload read that places the next header; chain-geometry facts only |

Admit / reject: RESULT:<pending L1>. Registry change (old → new, CORPUS.md rule 2): S313 `used-by` gains `corpus/knowledge/2026-11-05-r92-stop-boundary-repair.md`: RESULT:<pending L1>. Census before/after: RESULT:<pending L1>. Spot-check: RESULT:<pending non-author closure>.
