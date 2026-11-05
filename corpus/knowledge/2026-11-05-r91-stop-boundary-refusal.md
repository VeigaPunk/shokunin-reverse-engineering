# Packed-ELF last-block `sz_cpr`: a stop-boundary tamper is refused, not repaired (round 91, R91-C1)

source: S313 — UPX v5.2.0 `src/p_unix.cpp`, https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_unix.cpp — reopened 2026-11-05 (round 91), HTTP 200, 24181 bytes, sha256 `bf83c4133c27d39433db63bf604daf577d429d734c542d29c0b9cc8ed229642e`; `unpackExtent` at line 476, `fi->readx(&hdr, szb_info)` at 485, the per-block bound check `if (sz_cpr > sz_unc || sz_unc > (int)blocksize)` at 496, `fi->readx(ibuf+j, sz_cpr)` at 504.
source: S311 (existing, round 89) — UPX v5.2.0 `src/p_lx_elf.cpp`, the `un_shlib_1` peek that reports a desynchronised shared object as `corrupt b_info`.
source: S313 is the only row this entry newly re-grounds; the round-90 entry `corpus/knowledge/2026-11-04-r90-interior-block-szcpr.md` and the round-88 entry `corpus/knowledge/2026-11-04-r88-binfo-chain-geometry.md` supply the chain law the rule uses.
verified-at: 2026-11-05 (round 91; scored receipts `.ufo/waves/round-91/l1/scores/c1-at-declaration.json` at `deb2765a55fef0e4e81500a027dfe59951b69e87`, base receipt `.ufo/waves/round-91/pre/c1-base-round90-repair.json` at `2135f6e1d3f69a259b32cc5167c52ccb1a261c24`)
recheck: 180d — the counting command below and `python3 -I -B tools/round-91/upx-stop-boundary-repair.py --selftest` (4 cases).

## The class

A packed UPX 5.2.0 `--best` little-endian ELF whose **last** `b_info` block before the chain stop carries an `sz_cpr` moved by −7 or +7, both values in range (`0 < value <= sz_unc`). Four pinned carriers (`jq`, `xxd`, `libz`, `docker-init`) × two directions = eight cells. Only the last block is in this class; interior blocks are the round-90 class (`2026-11-04-r90-interior-block-szcpr`).

The decoder's only per-block arithmetic check is the bound at S313 line 496 (`sz_cpr > sz_unc`). It does not cross-check the next header. So an in-range wrong value passes the bound and fails later, at the payload stage (`upx -t`: `compressed data violation`). For the last block the chain geometry cannot decide the value either: on `jq`, `xxd` and `docker-init` a `+7` value keeps the walked total equal to the PackHeader's `u_len`, the same total as the intact file, and on `libz` both the intact file and the `+7` file walk 98,592 of 108,560 bytes. The geometry is not a sufficient test.

## The rule

The round-90 repair (`tools/round-90/upx-break-repair.py`) falls through to the round-89 block-0 law when no successor decides the walk. That fall-through returns the bytes unchanged with rc 0, or writes the four-byte `UPX!` sentinel outside the tampered window. The round-91 repair (`tools/round-91/upx-stop-boundary-repair.py`) keeps every other branch and changes only this one:

- No successor decides the walk. Run `upx -t` on the input. If it is green, the input is intact: return it byte-identical.
- If `upx -t` is red, refuse with rc 2 and write no output file.

The packer's verdict on the input is used only to choose between identity and refusal. The tool never produces output bytes from it.

## Measured

Base `2135f6e1d3f69a259b32cc5167c52ccb1a261c24`, round-90 repair, frozen counter (`tools/round-91/stop-boundary-battery.py`): refused 0 of 8, unsafe 2 (`jq` −7 and `libz` −7 write the sentinel word at bytes 10094–10097 and 60124–60127), silent 6 (rc 0, output identical to a file `upx -t` still rejects), intact 4 of 4 identity.

Declaration `deb2765a55fef0e4e81500a027dfe59951b69e87`, round-91 repair, same counter: refused 8 of 8, unsafe 0, intact 4 of 4, met true (`.ufo/waves/round-91/l1/scores/c1-at-declaration.json`). The regression arm (round-90 battery with the new repair) is recorded in the round-91 lesson with its receipt.

The two cheap rules that the frozen label rejects are blanket refusal (intact 0 of 4) and geometry-only refusal (refuses the intact `libz` and does not cover the `+7` cells); see `.ufo/waves/round-91/w1/ExecCandidate/` in the round-91 wave evidence.

## Limits

- **Refused, not repaired.** No successor and no decompression decides the last block, so the class has no repair in this lane. The mechanism is a typed refusal, not a fix.
- **Packer dependence.** The intact arm depends on `upx -t` on the input as the packer's own verdict. A future packer whose `upx -t` disagrees with the decoder would change the outcome; the frozen pins (`upx 5.2.0`, sha256 `cf2f6e7c…c969`) fix the version this entry measured.
- **Four carriers, two directions.** Not a population claim about every UPX artifact. 32-bit ELF and `--lzma` output are not measured in this entry; they are outside the counter's carrier list.
- **The shared object's 9,968-byte `u_len` gap** is outside this class, as in round 90.

## Counting command

```sh
python3 -I -B tools/round-91/stop-boundary-battery.py --root . \
  --repair-cmd tools/round-91/upx-stop-boundary-repair.py \
  --work <scratch> --rev <rev> --expect "refused 8 of 8; unsafe 0; intact 4 of 4" \
  --json-out <receipt>
```

Exit 0 means the label equals `--expect`, eight cells were scored, `unsafe` is 0, and four intact carriers are identical. The base arm is the same command with `--repair-cmd tools/round-90/upx-break-repair.py` at `2135f6e1d`.
