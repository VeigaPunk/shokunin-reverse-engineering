# ExecHeaderTable — V8 code-cache header table (static, read-only)

Seat: ExecHeaderTable, round 64 wave w1. Scope: compare the first 24 bytes of the two pinned
`.jsc` artifacts as six little-endian 32-bit words. No d8 execution, no mutation of inputs,
no scratch tree created.

## Inputs verified

| artifact | path | size (bytes) | sha256 | pin |
|---|---|---|---|---|
| probe (Electron 42.2.0 code cache) | `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-64/inputs/probe-electron.jsc` | 472 | `a86f6ea04b95c9796b87b24aa8a414aba97b4468a6c39bb2298310e28fd1d710` | `a86f6ea0…` MATCH |
| typora | `/home/vgpnk/.local/share/kaidoku-jsc/inputs/atom.compiled.dist.jsc` | 388080 | `6a0cb7b32270498ed190c589ca29c990a0e4b5f06f0cd6a5516e19a715c2dfe9` | `6a0cb7b3…` MATCH |

Verification command: `sha256sum <probe> <typora>` (exit 0), sizes via `stat -c '%n %s'`.

## First 24 bytes, hex

| artifact | bytes 0–23 |
|---|---|
| probe | `c306dec0112c847650000000db48ba65cbffb033b8010000` |
| typora | `c306dec0112c8476de9f0300990e3624cbffb033d0eb0500` |

Full header block, bytes 0–31 (observed, for context):

| artifact | bytes 0–31 |
|---|---|
| probe | `c306dec0112c847650000000db48ba65cbffb033b8010000000000000000000001` |
| typora | `c306dec0112c8476de9f0300990e3624cbffb033d0eb050000000000000000000001` |

## Six 32-bit words (little-endian, `struct.unpack('<6I', first24)`)

| word index | probe value | typora value | equal |
|---|---|---|---|
| 0 | `0xc0de06c3` (3235776195) | `0xc0de06c3` (3235776195) | yes |
| 1 | `0x76842c11` (1988373521) | `0x76842c11` (1988373521) | yes |
| 2 | `0x00000050` (80) | `0x00039fde` (237534) | no |
| 3 | `0x65ba48db` (1706707163) | `0x24360e99` (607522457) | no |
| 4 | `0x33b0ffcb` (867237835) | `0x33b0ffcb` (867237835) | yes |
| 5 | `0x000001b8` (440) | `0x0005ebd0` (388048) | no |

Word 0 is `0xc0de06c3` in both files (required magic check passes).

## Declared payload length

Word index 5 equals `size - 32` in both files:

| artifact | file size | word 5 | size - 32 | equal | matching word indices |
|---|---|---|---|---|---|
| probe | 472 | 440 (`0x1b8`) | 440 | yes | `[5]` only |
| typora | 388080 | 388048 (`0x5ebd0`) | 388048 | yes | `[5]` only |

No other word in either file equals `size - 32` or the file size itself.
Consistent with this, bytes 24–31 are identical in both files (`00000000 00000001`),
i.e. the region between the six words and the `size - 32` payload count is shared.

## Interpretation

No field names or meanings are asserted. A bounded local search of
`/home/vgpnk/.local/share/kaidoku-jsc` (`*.h`, `*.cc`, `*.py`, `*.js`, `*.ts` for
`c0de06c3` / `C0DE06C3`) returned no matching file; no V8 source is available locally and
no network source was used. All statements above are observations (hex/word dumps and
arithmetic equality checks) only; there are no `[INFERENCE]` claims to label because no
semantic interpretation is made.
