# Packed-ELF `b_info` value classes: a wrong-but-in-range `sz_cpr` recovered by the same chain law (round 89, R89-C1)

source: S311 — UPX v5.2.0 `src/p_lx_elf.cpp`, https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_lx_elf.cpp — opened 2026-11-04, HTTP 200, 373743 bytes, sha256 `551fc8675a594937…`; line 7105 (and 7308, the 32-bit twin): "throwCantUnpack("corrupt b_info");"; lines 7096-7104 show the `unpackExtent(sz_elf_hdrs, …)` peek whose short result decides it, so the message names the *block walk*, not one field.
source: S312 — UPX v5.2.0 `src/p_unix.h`, https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_unix.h — opened 2026-11-04, HTTP 200, 6651 bytes, sha256 `73bd992ec0fb4602…`; lines 201-204: "packed_struct(p_info) { // 12-byte packed program header / LE32 p_progid; LE32 p_filesize; LE32 p_blocksize;"; grounds why the locator finds `u_file_size` twelve bytes after `l_magic`.
source: S306 (existing, round 87) — UPX v5.2.0 `src/stub/src/include/linux.h` — the 12-byte `b_info` header the chain walk steps by.
source: S309 (existing, round 88) — UPX v5.2.0 `src/packhead.h` — the PackHeader fields the accounting bound reads (`u_len`, `c_len`, `u_file_size`).
source: S310 (existing, round 88) — UPX v5.2.0 `src/packer.cpp` — the arithmetic gate that raises `header corrupted` before any checksum.
base entries (present at the base revision `0ec2bb40`): `corpus/knowledge/2026-11-04-r88-binfo-chain-geometry.md` (the chain law this entry extends), `corpus/knowledge/2026-11-04-r87-upx-magic-tamper-repair.md` (the anchor class the repair composes), `corpus/knowledge/2026-11-04-r86-record-agreement.md` (a receipt cell is re-derived at the revision it names).
verified-at: 2026-11-04 (round 89; measured revision and receipt in SCORECARD `## 2026-11-04 — round 89`)
recheck: 180d — `python3 -I -B tools/round-89/upx-field-value-repair.py --selftest` and the counting command below. The repair was revised in-round (declared bytes `332917f2…` -> landed `664b973a…`, `claims.json`'s `supersessions` entry): the landed revision's selftest carries 22 cases, failures 0, and the declared bytes' 16 cases, failures 0 — both receipts are in `.ufo/waves/round-89/w1/ScribeEntry/receipts/`.

## The class

[observation] Round 88's limit — "a non-zero but wrong `sz_cpr` is left alone" — is a *class*, not an edge: overwrite block 0's `sz_cpr` with any other in-range value and every bound the packer applies to the field passes (`0 < sz_cpr <= sz_unc`, block inside the tail window). The refusal therefore moves one stage later: `upx -t` answers `Exception: compressed data violation` (measured on all four carriers, `.ufo/waves/round-89/pre/c1-base-r88-repair.json` `precondition.tail`), where the zeroed value answers `CantUnpackException: b_info corrupted`. The round-88 repair cannot see it: its round-87 anchor path reports `intact` (the `UPX!` words are in place) and its geometry gate skips any block whose stored `sz_cpr` is non-zero, so the composed repair scores `recovered 0 of 4` with every control true (same receipt: `recovered 0`, `exit 1`).
[inference] The class is recoverable for the same reason the zeroed class is: `sz_cpr` is redundant with the block boundaries, so the *stored value is not an input to the derivation at all*. Reading it only to decide `intact` versus `corrected` is the whole difference between the two classes.
[unknown] Whether a wrong value in a *later* block is recoverable the same way (this round derives block 0 only), and whether the accounting bound stays unique when two candidates fit `u_len` on a carrier class not measured here (32-bit ELF, LZMA-filtered shared object).

## The rule

The derivation is round 88's chain law with the stored value taken out of the gate (`corpus/knowledge/2026-11-04-r88-binfo-chain-geometry.md`; the code is `tools/round-89/upx-field-value-repair.py:63-106`, whose survivor key is `(total <= ph["u_len"], total, -derived)` at line 95): for each `l_info` candidate, `b0 = l_info + 20`, `sz_unc0 > 0`; scan `s1 > b0 + 12` for a plausible `b_info` under block 0's method (or the PackHeader's) whose chain reaches the end-of-chain sentinel, directly or through the loader-resume step; require `0 < s1 - (b0 + 12) <= sz_unc0`; with the derived value written, walk and sum `sz_unc`, reject a candidate whose total exceeds the PackHeader `u_len` (S309), and among survivors take the one accounting for the most declared bytes, ties to the smaller derived value.

Three outcomes, decided from the stored value only *after* the derivation (`tools/round-89/upx-field-value-repair.py:130-135`):

| stored `sz_cpr` | class | output |
|---|---|---|
| equals the derived value | `intact` | byte-identical to the input |
| `0` | `chain-geometry` | one write at `b0+4` |
| any other value (in range or not) | `field-value` | one write at `b0+4` |

Composition, not replacement: the round-87 anchor path runs first (a magic-tampered carrier keeps its repair, selftest case `magic-class-composed`); when that walk refuses — which a broken first block makes it do — the derivation runs on the original bytes and the *corrected* bytes are re-validated through the anchor path, so a correction that does not restore a plausible chain is refused rather than written.

## Measured (R89-C1)

`python3 -I -B tools/round-89/upx-field-battery.py --root . --repair-cmd tools/round-89/upx-field-value-repair.py --pkg <rea 6.5.0> --work <scratch> --json-out <receipt> --expect-recovered 4`:

| arm | observed | receipt |
|---|---|---|
| real repair | `recovered 4 of 4`, `met_target true`, exit 0, `controls_ok` all true (`N1-refuse-plain`, `N2-corrupt-payload`, `N3-intact-idempotent`, `isolation`), round-88 class regression `recovered 4 of 4` rc 0 | `.ufo/waves/round-89/pre/c1-candidate-at-declaration.json` |
| tamper per carrier | jq 252→244, xxd 249→241, libz 201→193, dinit 226→218 (stored `true - 8`); every repaired file hashes back to its packed pin (`repaired_equals_packed` true per carrier) | same |
| REA 6.5.0 counts of the unpacked result | jq 167/30/190, xxd 99/29/103, libz 184/29/199, dinit 1268/29/1111 (procedures/segments/strings) | same |
| round-88 repair, unchanged (before) | `recovered 0 of 4`, all controls true, exit 1 | `.ufo/waves/round-89/pre/c1-base-r88-repair.json` |
| `identity` | `recovered 0 of 4`, exit 1 (`N1-refuse-plain` false, rc 0) | `.ufo/waves/round-89/pre/c1-control-identity.json` |
| `naive-global` | `recovered 0 of 4`, exit 1 (`N1-refuse-plain` false, rc 0) | `.ufo/waves/round-89/pre/c1-control-naive.json` |
| round-87 class regression | `recovered 8 of 8`, exit 0 | `.ufo/waves/round-89/l1/scores/c1-r87class-regression.json` |
| round-88 class regression | `recovered 4 of 4`, exit 0 (nested round-87 arm `recovered 8 of 8`) | `.ufo/waves/round-89/l1/scores/c1-r88class-regression.json` |

Each recovered case passes five arms: the repair exits 0, the only changed bytes lie inside block 0's four-byte `sz_cpr` window, `upx -t` exits 0, `upx -d` restores the carrier pin, and REA 6.5.0 reports the declared procedure count. The counter runs every repair invocation in a private directory that holds the single input file, and the `isolation` control records the directory listing each invocation saw (round-88 M88-8 / QUALITY 158).

[observation] The accounting bound is unchanged code, not a new rule: the round-89 repair reads the same `u_len` and applies the same key. On docker-init the three survivors are the round-88 ones — derived 136 (accounts 123,942,159 against `u_len` 851,288, so it does not fit), 440 (850,696) and 226 (851,288, exactly `u_len`, which wins) — `.ufo/waves/round-88/w1/ExecGeomCross/evidence/docker-init.derive.json`.

## Refusal signatures by field class (2-carrier probe, round-89)

`.ufo/waves/round-89/l1/scores/block29-cells.json` — jq and xxd, one field per cell, `upx -t` after the tamper (18 cells; 14 answer rc 1, 4 answer rc 0):

| class | `upx -t` | reading |
|---|---|---|
| `b0.sz_unc := 0` | rc 1 `CantUnpackException: b_info corrupted` | no redundancy for the uncompressed length: refuse |
| `b0.sz_cpr := 0` | rc 1 `CantUnpackException: b_info corrupted` | recoverable (chain geometry) |
| `b0.sz_cpr := stored - 8` | rc 1 `Exception: compressed data violation` | recoverable; the only class reaching the payload stage |
| `b0.sz_cpr := 0xFFFFFFF0` | rc 1 `CantUnpackException: b_info corrupted` | recoverable; the gate fires early, the field is still redundant |
| `b0.sz_cpr := sz_unc + 1` | rc 1 `CantUnpackException: header corrupted` | the arithmetic gate, one stage earlier than `b_info` |
| `b0.method ^= 0xFF` | rc 1 `CantUnpackException: bad method 0xfd at 0x240` | the offset names the block; no redundancy: refuse |
| `l_info.version ^= 0xFF` | rc 0 `Tested 1 file.` | tolerated by `upx -t`, but it breaks this lane's locator: refuse |
| `l_info.format ^= 0xFF` | rc 0 `Tested 1 file.` | same |
| PackHeader `u_len := 0` | rc 1 `CantUnpackException: header corrupted 3` | the PackHeader arithmetic gate (S310) |

[observation] The message does not name the field: `b_info corrupted` covers `sz_unc` and `sz_cpr` alike (QUALITY 156), and `sz_cpr = sz_unc + 1` answers `header corrupted` instead, because that value fails a header-level comparison before the block walk starts.

[observation] The message is also carrier-dependent, so a row keyed on it is fragile. The two-carrier
probe above is jq and xxd, both main executables; on the shared object the same class answers
`CantUnpackException: corrupt b_info` instead of `header corrupted` — measured on libz by the
wave's own four-carrier matrix (`.ufo/waves/round-89/w1/ExecMatrix/matrix.json`, an uncommitted seat
receipt: `header corrupted` on three carriers, `corrupt b_info` on libz) and independently by the
source scout on fresh packs (`.ufo/waves/round-89/w1/ScoutUpxSrc/report.md`, §4: libz answers
`corrupt b_info` for `sz_cpr := sz_unc + 1`). The class, not the message, is the stable key.

## Refusal set of the repair itself

Measured by this seat (`receipts/refusals.json` in this seat directory), against the **declared** bytes `332917f2…`: not a little-endian ELF -> rc 2, `refused: not a little-endian ELF`; a PackHeader but no derivable first block -> rc 2, `refused: no l_info candidate carries a derivable first block`; a little-endian ELF with no validated PackHeader -> **rc 1**, `r87repair.Refused: no validated PackHeader in the tail window`, an uncaught traceback rather than the tool's own `refused:` line.

[observation] That third refusal was not typed in the declared bytes: the PackHeader lookup runs inside `derive()` (`tools/round-89/upx-field-value-repair.py:65`), which raises the round-87 module's `Refused`, not this tool's, so it escapes `main`'s `except Refused` and the process exits 1 with a traceback. The declared candidate receipt records the same exit code for the counter's own plain-original arm (`N1-refuse-plain` rc 1 on all four carriers, against rc 2 for the unchanged round-88 repair in `pre/c1-base-r88-repair.json`), while the SKILL registry row for this tool states `rc 2 on a refusal` (`SKILL.md:1960`) — the counter's `N1` arm tests `rc != 0`, so it cannot tell a crash from a typed refusal.

[observation] The landed revision (`664b973a…`, the `claims.json` supersession) converts that refusal: all three refusals now leave as rc 2, the third with the text `refused: upstream refusal: no validated PackHeader in the tail window` (measured on the landed bytes; receipt `receipts/refusals-worktree-revision.json`). The landed revision also adds the round-88 input guards (a regular-file check and a bounded read) that the declared bytes lacked. The entry's class, rule, measurements and limits are unchanged by the revision: the derivation law, the survivor key and the three classes are the same code.

## Limits

- The repair does not decompress what it repairs; the counter's `upx -t`/`upx -d` arms are the guard, and a payload corruption is invisible to the structural walk (selftest case `corrupt-payload-not-structural`).
- One field on four carriers, block 0 only; later-block values and `p_filesize`/`p_blocksize` stay Frontier.
- The counter scores bytes, not provenance; a repair that ran the packer as an oracle is a disclosed cheap rule (round 88's M88-4), not excluded by construction.
- The cost profile is carried from round 88 (`QUALITY 160`; the round-88 repair measured 1.02 s / 14.22 s / 221.85 s at 800 / 3,200 / 12,800 crafted candidates, `.ufo/waves/round-88/l1/scores/c1-candidate-scan-scaling.json`). The round-89 repair's own curve is **unmeasured in a committed receipt**: the one seat-level probe of this tool (`.ufo/waves/round-89/w1/SentinelR89/report.md`, an uncommitted seat report whose cost receipt is still in flight) read 8.378 s at 800 candidates and 125.489 s at 3,200 — an order of magnitude slower than the round-88 curve on a comparable candidate family, because this repair scans every `l_info` candidate instead of skipping the ones whose stored `sz_cpr` is non-zero. No bound is claimed for this round's repair; the round-88 numbers are the round-88 tool's.

## Counting command

```sh
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
python3 -I -B tools/round-89/upx-field-battery.py --root . \
  --repair-cmd tools/round-89/upx-field-value-repair.py \
  --pkg /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
  --work /fast/scratch/hyaku/kaidoku-r89/recheck \
  --json-out /fast/scratch/hyaku/kaidoku-r89/recheck.json --expect-recovered 4
```
