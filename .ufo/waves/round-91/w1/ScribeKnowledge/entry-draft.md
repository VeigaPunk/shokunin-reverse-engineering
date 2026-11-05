source: S313 — UPX v5.2.0 `src/p_unix.cpp`, https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_unix.cpp, reopened 2026-11-05 (HTTP 200, 24181 bytes, sha256 `bf83c4133c27d39433db63bf604daf577d429d734c542d29c0b9cc8ed229642e`; decode loop `unpackExtent` at lines 476-504: header read at 485, bound `if (sz_cpr > sz_unc || sz_unc > (int)blocksize)` at 496, payload read `fi->readx(ibuf+j, sz_cpr)` at 504); existing entries `corpus/knowledge/2026-11-04-r90-interior-block-szcpr.md` (interior-block class, the rule this entry's fall-through sits under) and `corpus/knowledge/2026-11-04-r88-binfo-chain-geometry.md` (chain law, intact walk totals).
verified-at: 2026-11-05 (round 91; declaration receipt `.ufo/waves/round-91/l1/scores/c1-at-declaration.json` at `deb2765a55fef0e4e81500a027dfe59951b69e87`; base receipt `.ufo/waves/round-91/pre/c1-base-round90-repair.json` at `2135f6e1d3f69a259b32cc5167c52ccb1a261c24`).
recheck: 180d — the counting command below, and `python3 -I -B tools/round-91/upx-stop-boundary-repair.py --selftest` (expect `SELFTEST cases=4 failures=0`).

# Packed-ELF last-block `sz_cpr`: a stop-boundary tamper is refused, not repaired (round 91, R91-C1)

## The class

A packed UPX 5.2.0 `--best` little-endian ELF. Its last `b_info` block before the chain stop has `sz_cpr` moved by −7 or +7, both values in range (`0 < value <= sz_unc`). Four pinned carriers (`jq`, `xxd`, `libz`, `docker-init`) times two directions make eight cells. Interior blocks belong to the round-90 class, not this one.

The decoder checks each block with one arithmetic bound (S313 line 496: `sz_cpr > sz_unc`). It does not check the next header. The payload read at line 504 uses the stored `sz_cpr`, so the next header's offset depends on that value. An in-range wrong value passes the bound. The file then fails at the payload stage (`upx -t`: `compressed data violation`).

The chain geometry cannot decide the last block. Measured in `.ufo/waves/round-91/l1/scores/c1-at-declaration.json`, field `stored_total` per cell:

- On `jq`, `xxd` and `docker-init`, the +7 walk totals equal `u_len` (30,800; 38,928; 851,288). The intact files total the same (`2026-11-04-r88-binfo-chain-geometry.md`). The total cannot tell +7 from intact.
- On `libz`, the intact file and the +7 file both walk 98,592 of 108,560. The total is not a test there either.
- The −7 walks do not all fall short. `jq` (22,585) and `libz` (87,421) fall short. `xxd` (38,928) and `docker-init` (851,288) equal `u_len`.

So no total-based rule separates the eight cells from the intact files.

## The rule

The round-90 repair (`tools/round-90/upx-break-repair.py`) falls through to the round-89 block-0 law when no successor decides the walk. That fall-through either returns the input unchanged with rc 0 (a file `upx -t` still rejects) or writes the four-byte `UPX!` sentinel outside the tampered window.

The round-91 repair (`tools/round-91/upx-stop-boundary-repair.py`) keeps every other branch. It changes only this fall-through:

- No successor decides the walk. Run `upx -t` on the input.
- `upx -t` green: the input is intact. Return it byte-identical, rc 0.
- `upx -t` red: refuse. Print a typed `stop-boundary:` message, exit rc 2, write no output file.

The packer's verdict chooses only between identity and refusal. The tool never produces output bytes from it.

## Measured

Base `2135f6e1d3f69a259b32cc5167c52ccb1a261c24`, round-90 repair, frozen counter. Receipt `.ufo/waves/round-91/pre/c1-base-round90-repair.json`:

- refused 0 of 8
- unsafe 2 (`jq` −7 writes the sentinel at bytes 10094–10097; `libz` −7 at 60124–60127)
- silent 6 (rc 0, output identical to a file `upx -t` rejects)
- intact 4 of 4 (identity)
- label `refused 0 of 8; unsafe 2; intact 4 of 4`, exit 1, not met.

Declaration `deb2765a55fef0e4e81500a027dfe59951b69e87`, round-91 repair, same counter. Receipt `.ufo/waves/round-91/l1/scores/c1-at-declaration.json`:

- refused 8 of 8, each rc 2 with no output file
- unsafe 0, silent 0
- intact 4 of 4 (identity)
- label `refused 8 of 8; unsafe 0; intact 4 of 4`, exit 0, `met_target` true.

Regression arm, round-90 battery with the round-91 repair. Receipt `.ufo/waves/round-91/l1/scores/c1-regression-at-declaration.json`:

- label `P1 6 of 6; P2 4 of 4; P3 4 of 4`, exit 0
- `controls_ok` true on all eight controls
- revision `deb2765a55fef0e4e81500a027dfe59951b69e87`.

Cheap rules, scored against the frozen label:

- Blanket refusal (refuse every last-block input). Intact 0 of 4 by construction. [INFERENCE] Not measured. Fails the frozen label.
- Geometry-only refusal (refuse when walked total is below `u_len`). [INFERENCE from the `stored_total` fields above] Refuses 3 of 8 tampered cells (`jq` −7, `libz` −7, `libz` +7) and refuses the intact `libz` (98,592 < 108,560). Fails the frozen label. The measured count is pending the wave's executor receipt (`ExecCandidate`), which is not in the lane tree when this entry was drafted.

## Limits

- **Refused, not repaired.** No successor and no decompression decides the last block. This class has no repair in this lane. The mechanism is a typed refusal.
- **Intact means `upx -t` green.** Identity is returned when the packer's own test passes. That is not proof that the bytes match the original packer output. The packer verdict is the only arbiter, and it is pinned to `upx 5.2.0` (sha256 `cf2f6e7c…c969`, checked at drafting). A packer whose `upx -t` disagrees with the decoder would change the outcome.
- **Four carriers, two directions.** Not a population claim about UPX artifacts. 32-bit ELF and `--lzma` output are not measured. They are outside the counter's carrier list.
- **Shared object gap.** `libz`'s chain accounts 98,592 of 108,560 `u_len` bytes, as recorded in the round-88 entry. The total cannot be the test on `libz`.
- **Carrier blindness is audit-level here.** The repair reads no carrier path. The round-90 battery's `carrier_blind` arm carries that claim, and it reports true in the regression receipt.

## Counting command

```sh
python3 -I -B tools/round-91/stop-boundary-battery.py --root . \
  --rev deb2765a55fef0e4e81500a027dfe59951b69e87 \
  --repair-cmd tools/round-91/upx-stop-boundary-repair.py \
  --work <scratch> --expect "refused 8 of 8; unsafe 0; intact 4 of 4" \
  --json-out <receipt>
```

Exit 0 means the label equals `--expect`, eight cells were scored, `unsafe` is 0, and four intact carriers are identical. Base arm: the same command with `--repair-cmd tools/round-90/upx-break-repair.py --rev 2135f6e1d3f69a259b32cc5167c52ccb1a261c24`.

Regression arm:

```sh
python3 -I -B tools/round-90/upx-later-block-battery.py --root . \
  --rev deb2765a55fef0e4e81500a027dfe59951b69e87 \
  --repair-cmd tools/round-91/upx-stop-boundary-repair.py \
  --pkg /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
  --work <scratch> --expect "P1 6 of 6; P2 4 of 4; P3 4 of 4" --json-out <receipt>
```

## Verified

- S313 re-fetched 2026-11-05 with `curl -sL`: rc 0, 24181 bytes, sha256 `bf83c413…642e` (matches). Lines 476, 485, 496 and 504 read as stated (`sed -n '476p;485p;496p;504p'`).
- Instrument sha256 match the `claims.json` pins: `tools/round-91/upx-stop-boundary-repair.py` `473bb3a9…b91`; `tools/round-91/stop-boundary-battery.py` `5998b6bd…893`; `tools/round-90/upx-later-block-battery.py` `5462ef13…210`.
- `/usr/bin/upx` is `upx 5.2.0`, sha256 `cf2f6e7c…c969` (matches pin).
- `python3 -I -B tools/round-91/upx-stop-boundary-repair.py --selftest` in a clone at `deb2765a`: `SELFTEST cases=4 failures=0`, rc 0.
- Counts and labels above are read from the receipt files named in each row. The frozen counter was not re-run for this entry.
