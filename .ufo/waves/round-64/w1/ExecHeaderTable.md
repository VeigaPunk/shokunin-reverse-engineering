# R64-W1 ExecHeaderTable — V8 code-cache header comparison (static, no d8)

Seat: ExecHeaderTable (round 64, wave w1, attempt 1). Read-only byte/word comparison of the two
pinned `.jsc` artifacts' header block. No d8 run, no instrument edit, no git write, no scratch tree
created. Full table also written to `.ufo/waves/round-64/w1/ExecHeaderTable/header-table.md`.

## Pins verified first

Command: `sha256sum <probe> <typora>` plus `stat -c '%n %s'`, exit 0.

| artifact | path | size (bytes) | sha256 | pin |
|---|---|---|---|---|
| probe | `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-64/inputs/probe-electron.jsc` | 472 | `a86f6ea04b95c9796b87b24aa8a414aba97b4468a6c39bb2298310e28fd1d710` | `a86f6ea0…` MATCH |
| typora | `/home/vgpnk/.local/share/kaidoku-jsc/inputs/atom.compiled.dist.jsc` | 388080 | `6a0cb7b32270498ed190c589ca29c990a0e4b5f06f0cd6a5516e19a715c2dfe9` | `6a0cb7b3…` MATCH |

## First 24 bytes as hex

| artifact | bytes 0–23 |
|---|---|
| probe | `c306dec0112c847650000000db48ba65cbffb033b8010000` |
| typora | `c306dec0112c8476de9f0300990e3624cbffb033d0eb0500` |

Bytes 0–31 (context; observed): probe `c306dec0112c847650000000db48ba65cbffb033b8010000000000000000000001`,
typora `c306dec0112c8476de9f0300990e3624cbffb033d0eb050000000000000000000001`.

## Six little-endian 32-bit words (`struct.unpack('<6I', first24)`)

| word index | probe | typora | equal |
|---|---|---|---|
| 0 | `0xc0de06c3` (3235776195) | `0xc0de06c3` (3235776195) | yes |
| 1 | `0x76842c11` (1988373521) | `0x76842c11` (1988373521) | yes |
| 2 | `0x00000050` (80) | `0x00039fde` (237534) | no |
| 3 | `0x65ba48db` (1706707163) | `0x24360e99` (607522457) | no |
| 4 | `0x33b0ffcb` (867237835) | `0x33b0ffcb` (867237835) | yes |
| 5 | `0x000001b8` (440) | `0x0005ebd0` (388048) | no |

Word 0 is `0xc0de06c3` for both files: the required magic check passes.

## Declared payload length

Word index 5 equals `size - 32` in both files; no other word equals `size - 32` or the file size.

| artifact | size | word 5 | size - 32 | equal | matching indices |
|---|---|---|---|---|---|
| probe | 472 | 440 (`0x1b8`) | 440 | yes | `[5]` |
| typora | 388080 | 388048 (`0x5ebd0`) | 388048 | yes | `[5]` |

Supporting observation: bytes 24–31 are byte-identical in both files (`00000000 00000001`), so the
16 bytes beyond the six words share a prefix and the `size - 32` count is consistent with a 32-byte
pre-payload region.

## Summary of equalities

Equal across both artifacts: words 0, 1, 4 and bytes 24–31. Differing: words 2, 3, 5 (word 5 = payload
length, necessarily different because the file sizes differ).

## Interpretation

None asserted. A bounded search of `/home/vgpnk/.local/share/kaidoku-jsc` (`*.h`, `*.cc`, `*.py`,
`*.js`, `*.ts` containing `c0de06c3`/`C0DE06C3`) returned no matching file; no V8 source is present
locally and no network source was consulted. Therefore no word is assigned a name or meaning, and no
`[INFERENCE]` labels are needed because no semantic claim is made beyond the observed values and
equalities.

## Recovery

Parse command used: `python3 -c "import struct;b=open(p,'rb').read(24);print(b.hex(),struct.unpack('<6I',b))"`
(for each file), exit 0. Full table: `.ufo/waves/round-64/w1/ExecHeaderTable/header-table.md`.

Report: .ufo/waves/round-64/w1/ExecHeaderTable.md
