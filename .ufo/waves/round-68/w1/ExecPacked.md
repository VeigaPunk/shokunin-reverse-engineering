# ExecPacked — round 68, wave w1: does the R68-C2 route generalise beyond its two pinned carriers?

- Seat: `ExecPacked` (leaf executor). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
- Assignment: detect → unpack-with-identity → inventory-equality on a **third** host ELF chosen by
  this seat, plus the jq refusal leg; report, not the frozen predicate.
- No tracked file was modified, no index touched, no commit. Scratch
  `/fast/scratch/hyaku/kaidoku-r68/ExecPacked/` holds every artifact; receipts are copied to
  `.ufo/waves/round-68/w1/ExecPacked/receipts/` (54 files, 320 KB) and the scratch dir was deleted.
- Labels: **[obs]** measured here; **[inf]** inference from measurements; **[unk]** not measured.

## 1. Frozen inputs and environment — verified before use [obs]

| item | recorded | matches declaration/receipt |
|---|---|---|
| `tools/round-68/packed-elf.py` sha256 | `48ef4c688a14faf381abbd2cc2b29061035f38c97815e2365957843433e5276e` | yes (frozen input) |
| `tools/round-68/registry-conformance.py` sha256 | `a300d831c7ef1de47448c2feb8dcbd9ceaf597f7e5f4b996a8e4cc510c6e8315` | yes |
| `tools/round-68/controls.py` sha256 | `0657ee080ba92459cfc2916715dce8c0f1c49930e03c8c3d36ac60dbd5618fb4` | yes |
| `/usr/bin/upx` | sha256 `cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969`, `upx 5.2.0` | yes (pre receipt `packer`) |
| REA package | `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`, version `6.5.0`, `package.json` sha256 `a5003023…3050a6c` | yes (route pin) |
| node | `v24.21.0`, `/run/user/1000/fnm_multishells/1981588_1793727763382/bin/node` | same interpreter as the pre receipt |
| lane HEAD at probe time | `6ffa9ce1` (w1 evidence commit); freeze `1eaf596e` | — |

The route's own gates (`REA_VERSION`, `REA_PKGJSON_SHA256`) therefore hold in this environment, so
the arm definitions below are being exercised under the same packer and REA as the frozen predicate.

## 2. What was run

Every argv is in `./commands.txt`; every raw output is in `./receipts/`. Legs:

1. third carrier `/usr/bin/gzip`: copy → `upx -l` on the copy (refusal) → `upx --best` pack →
   `upx -l` on packed → `readelf -SW` section counts before/after → `upx -d` → sha256 →
   `rea analyze` on original, packed, unpacked → `rea decompile` pairs at a function start.
2. the route's jq refusal leg verbatim: `rea decompile <packed jq> 0x103fa0` and
   `rea decompile <unpacked jq> 0x103fa0`.
3. two generalisation side-axes: a different compression level (`upx --lzma` on gzip) and a
   fourth carrier (`/usr/bin/ls`, counts only).
4. a symbolized carrier (a 3-function C program, `gcc -O1 -g`) to test the refusal arm's
   `address_symbol` and `len(code) > 200` sub-conditions.
5. detector soundness probe: the frozen `section_count()` applied to `readelf`'s own failure text.
6. route-equivalent scoring: the frozen helpers `counts_from()` / `section_count()` re-applied to the
   saved envelopes, so the booleans in `./probe.json` are computed by the frozen code, not by eye.

## 3. Per-file table — third carrier `gzip` (plus side-axes)

| file | bytes | sha256 | sections | REA proc/seg/str | evidence_id |
|---|---|---|---|---|---|
| `gzip/orig-gzip` (= `/usr/bin/gzip`) | 109768 | `b1f9e749ee0809d6e90100218e6bc13cdf3f26f23c243d5f62aae39162297cb1` | 29 | 230 / 31 / 235 | `ev_a722a37842e8f15bfd0821a7acddacb07f4e75a5a72c3c51acc928adfbb26155` |
| `gzip/packed-gzip` (`upx --best`) | 62588 | `7090461bbf6591e47a5a1f17e185575e251e546808087a1966a81939e4780665` | **0** | **3 / 3 / 7** | `ev_ff97dddaa18c70a5765385ed74c22c268c92577506fc4f4ea810409f93852236` |
| `gzip/unpacked-gzip` (`upx -d`) | 109768 | `b1f9e749ee0809d6e90100218e6bc13cdf3f26f23c243d5f62aae39162297cb1` | 29 | 230 / 31 / 235 | `ev_a722a37842e8f15bfd0821a7acddacb07f4e75a5a72c3c51acc928adfbb26155` |
| `gzip/lzma-gzip` (`upx --lzma`) | 57856 | `95757e40e1beeddc98599999e9fbbceacabfa6ccc11a59c927ecb56e70b3327f` | **0** | **3 / 3 / 4** | — (counts only) |
| `gzip/lzma-unpacked-gzip` | 109768 | `b1f9e749ee0809d6e90100218e6bc13cdf3f26f23c243d5f62aae39162297cb1` | 29 | 230 / 31 / 235 | `ev_a722a37842e8f15bfd0821a7acddacb07f4e75a5a72c3c51acc928adfbb26155` |
| `gzip/jq-orig` (= `/usr/bin/jq`) | 30800 | `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806` | — | — | — |
| `gzip/jq-packed` | 14036 | `e8b6c9e76b542435a476a584bbe0fdff813c4b05b6d6e9a8e8405b7c7975268a` | — | — | — |
| `gzip/jq-unpacked` | 30800 | `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806` | — | — | — |
| `boundary/ls.orig` (= `/usr/bin/ls`) | 166640 | `29abfee0d588cfbee70103be11aa0a2f81b0d8c1292341e2345fc9f3ffa1558b` | 29 | 572 / 31 / 534 | `ev_288dddfeca5685fa25496c525e0ba16dc12fe25edf2ef3b53d6d640add5f95a1` |
| `boundary/ls.packed` | 77752 | `363248ad4a4c4b80262f913debaf8b9b5801f458e9094f9bd8f39b3a75a06994` | **0** | **3 / 3 / 4** | `ev_7512f882079850c0d0f1c3a61ce7b2ffb3bc2b2e1e9127b393abe40a5c68d32e` |
| `boundary/upx.packed` (`/usr/bin/upx` packed) | 912440 | `6d952fe4caf36d4391fd90c5ee37aa4f5410e553e24494607fa58c6c3ccc7cd6` | — | — | — |
| `sym/prog` (`gcc -O1 -g`) | 17856 | `e5e236166b9bcc8c52329e04ba05f78e0ce0fb8aab482309787c80d3cbb8c61c` | 39 | 23 / 42 / 83 | `ev_3ee049de3f43ce665434b7546dc8b7d8aa5115b9fd3f0c65c0e9ceba46d36f64` |
| `sym/packed-prog` | 7492 | `9f7cbb6b73fa68154a067f8e873e3d3edbaff9726aa3959ea417fd6d61f3dda6` | **0** | **7 / 3 / 3** | — (counts only) |
| `sym/unpacked-prog` | 17856 | `e5e236166b9bcc8c52329e04ba05f78e0ce0fb8aab482309787c80d3cbb8c61c` | 39 | — | — |

Sizes and full hashes are also in `./receipts/hashes.txt`; `./receipts/` holds every raw envelope,
`upx` log and `readelf` dump this table is built from.

Determinism datum [obs]: the `jq-packed` bytes this seat produced are `e8b6c9e7…` — **identical to
the `packed_sha256` recorded in `l1/pre/c2-dryrun-at-base.json`**. Packing `/usr/bin/jq` with
`upx 5.2.0 --best` on this host reproduces the pre-receipt's after-bytes bit-for-bit, so that
receipt's packed-bytes field is a reproducible function of the carrier pin, not a one-off.

## 4. Arm-by-arm verdict on the third carrier (`gzip`, `upx --best`)

| arm (route definition, `tools/round-68/packed-elf.py`) | measurement | verdict |
|---|---|---|
| `detected` — `upx -l` names it packed AND 0 section headers | `upx -l packed` rc 0 (lists `109768 -> 62588`); `readelf -SW` → “There are no sections in this file.” (orig 29 → packed 0) | **true** |
| `before_ok` — REA inventory of the packed bytes below the carrier floor | packed 3 procedures; floor = declared-min//2 = **115** (`min = 230`, the original's own count); also < the route-style 50 (`min = 100`) | **true** |
| `identity_ok` — `upx -d` restores the pin | unpacked sha256 `b1f9e749…` == orig sha256; `upx -d` rc 0 | **true** |
| `recovery_ok` — packed→unpacked inventory equals the original's | 230/31/235 == 230/31/235, and the two `analyze` envelopes carry the **same `evidence_id`** (`ev_a722a378…`) | **true** |
| `refusal_ok` — address-level verb refused on packed, succeeds on unpacked | `decompile packed 0x102060` → rc 1, `code=invalid_request`, 0 bytes; `decompile unpacked 0x102060` → rc 0, 11719 chars, symbol `FUN_00102060` present | **true** |
| `control` — original is neither listed nor decompressible by the packer | `upx -l orig` rc 2 (`NotPackedException`), `upx -d orig` rc 2 (`Unpacked 0 files.`), nothing written | **true** |

`fold` arithmetic on these values: `carriers_matched 1 of 1`, `control_ok true`, `met_target true`,
`failing []` — computed by the frozen `carrier_arms()` and `fold()` over the measured values and
stored in `./probe.json` (`gzip.arms_frozen_helper`, `gzip.fold_target_1`, `gzip.counts_equal`).

**Answer to the assigned question [obs]:** yes — the route's rule (detect → unpack identity →
inventory equality, with the refusal and control arms) holds on a third, unpinned host carrier
`/usr/bin/gzip`, on every arm, first try. Two further axes also hold:

- compression-level invariance [obs]: `--lzma` instead of `--best` still yields 0 sections, `upx -l`
  rc 0, packed inventory 3/3/4, unpacked sha == pin, recovered inventory == original's.
- carrier variety [obs]: `/usr/bin/ls` (572 procedures) packs to a 3-procedure stub; `/usr/bin/upx`
  itself packs (3189408 → 912440) — the packer accepts even that. `/usr/bin/xxd` and `/usr/bin/jq`
  were not re-run here (the route's own receipt covers them; this seat reproduced only jq's refusal
  leg and pack bytes).

## 5. Where the route does *not* generalise as stated — four measured limits

These are generalisation caveats for reuse, **not** failures of the frozen predicate, which is
declared over its two pinned carriers only.

### L1. “Packed bytes at exactly 3 procedures” is a property of these carriers, not of UPX [obs]
Stub inventories measured here: jq 3/3/3 and xxd 3/3/6 (pre receipt), gzip 3/3/7, ls 3/3/4,
symbolized `prog` **7/3/3**. The string/segment arms already differ between the two pinned carriers,
and on a small gcc-built binary the procedure arm is 7 too. Consequence for a fresh carrier: the
`before_ok` floor (`declared_min // 2`) must be chosen per carrier, and with stub = 7 a carrier needs
`declared_min ≥ 16` (floor 8) to clear; a genuine 12-procedure utility would give floor 6 and the arm
would read false on correctly packed bytes. My carrier (23 procedures, floor 11) clears it 7 < 11
[obs], so the mechanism is demonstrated, not merely suspected.

### L2. The refusal arm's `address_symbol` assumes REA's `FUN_%08x` naming [obs]
On the symbolized carrier, `decompile unpacked 0x101177` returns `int main(void)` — REA uses the ELF
symbol when one exists, not `FUN_00101177`. `0x101140` returns `long helper(long x)`. The route's
`c["address_symbol"] in code` test would therefore report `refusal_ok: false` on any carrier whose
function is symbolized, even though the refusal separation itself is perfect (packed rc 1
`invalid_request`, 0 bytes; unpacked rc 0, code returned). Any new carrier with symbols needs the
symbol text pinned, not an address-derived name.

### L3. The refusal arm's `len(code) > 200` encodes jq's function size [obs]
`main` on the symbolized carrier decompiles to **176 chars** (< 200) while separating cleanly; the
jq pin (`0x103fa0`) decompiles to 4841 chars and gzip's `FUN_00102060` to 11719. A small carrier
whose chosen function is under ~200 chars of pseudo-C fails `refusal_ok` for a reason unrelated to
the route's semantics.

### L4. The refusal arm needs a true function start in REA's address space [obs]
`decompile` must be given a **true function start** in REA's address space (ELF VMA + `image_base`,
here `+0x100000`). At gzip's `.text` start `0x102040` the verb returns a 195-char fragment
(`void switchD_00106c0c::default(void)`, no `FUN_` symbol); at a mid-function address `0x103e60` it
returns only 280 chars of `FUN_00102060`, versus 11719 at that function's start `0x102060`. Address
choice changes the arm's outcome by two orders of magnitude; the pin in the carrier table is doing
real work and cannot be inferred by the instrument.

## 6. Detector evidence-integrity observation (not a verdict failure) [obs]

`section_count()` returns 0 for `readelf`'s own failure text: `readelf -SW <nonexistent>` exits 1
with `readelf: Error: '…': No such file`, and the frozen helper scores that text as **0 sections**
(`probe.json :: readelf_failure_section_count = 0`). The detector conjunctions the section arm with
`upx -l` rc 0, so a *verdict* false-positive is not available from this alone — but the receipt's
`section_count: 0` field cannot distinguish “packed image has no section table” from “readelf failed
or is absent”. `readelf` is invoked bare through `PATH` and is **not pinned** in the receipt, unlike
`upx` (rendered as `packer.sha256`). [inf] If readelf were removed from the host, the route would
still pass on the upx arm and record a measured-looking `0`. Severity: evidence integrity, not claim
truth.

## 7. Receipt-provenance observation (for the L1, not a C2 verdict) [obs]

`l1/pre/c2-dryrun-at-base.json` records
`instrument.sha256 = 7ee286c03391dc464c90a3f24498258bfef09dd89300aa9a246fd35ac85ef25c`,
`instrument.rev = null` and top-level `rev = "main"`. The frozen instrument is
`48ef4c688a14faf381abbd2cc2b29061035f38c97815e2365957843433e5276e`. In git,
`tools/round-68/packed-elf.py` **does not exist** at the base `fcbe200f` (`git cat-file -e` fails),
and its first committed revision `6020eb60` already carries the frozen `48ef4c68…`. So the
`7ee286c0…` variant that produced the “route green at the base revision” receipt exists nowhere in
git: that receipt is a working-tree rehearsal, not a revision-anchored measurement. It is still
valid evidence that the route ran green before the freeze (its numbers reproduce here: jq packed
bytes identical, refusal leg identical: packed rc 1 / `invalid_request` / 0 bytes, unpacked rc 0 /
4841 bytes / `FUN_00103fa0`), but it should not be cited as “measured at fcbe200”.

## 8. jq refusal leg — reproduced against the pre receipt [obs]

| run | rc | `code` | code bytes | symbol |
|---|---|---|---|---|
| `decompile gzip/jq-packed 0x103fa0` | 1 | `invalid_request` | 0 | — |
| `decompile gzip/jq-unpacked 0x103fa0` | 0 | null | **4841** | `FUN_00103fa0` present |

Identical to `refusal` in `l1/pre/c2-dryrun-at-base.json` (`packed_rc 1`, `packed_error_code
invalid_request`, `unpacked_code_bytes 4841`, `symbol_present true`). The refusal leg is reproducible
from the pinned jq bytes alone; no state from the pre run is required.

## 9. Verdict

- R68-C2 route generalises to a third carrier: **yes, all five arms + control, measured**
  (`./probe.json`).
- It also survives a different compression level, and its packed-bytes determinism is confirmed by
  reproducing the pre receipt's jq `packed_sha256`.
- It does **not** generalise as an unattended detector-scorer: three arm sub-conditions are shaped by
  the pinned carriers — the “3 procedures” stub constant (7 on a small gcc binary), `FUN_%08x`
  symbol naming (real symbols when present), and `len(code) > 200` (fails at 176 on a legitimate
  function). A new carrier needs a per-carrier declared floor, a pinned function-start address, and
  the name/length expectations re-derived — nothing in the frozen predicate is contradicted.
- One evidence-integrity note (readelf fail-open on its own error text, readelf unpinned) and one
  provenance note (the pre `c2-dryrun-at-base.json` was produced by an uncommitted instrument variant
  at `rev: main`, not by the frozen bytes at `fcbe200`).

## 10. Risks, tools, blockers

- Tools installed/upgraded: **none**. `upx 5.2.0`, `readelf`, `gcc 16.2.1`, `node v24.21.0`,
  `jq`, `python3` were already present; no pacman transaction was attempted (host transactions are
  paused and were not needed).
- Risk [inf]: the L1's after-arm cannot catch L1–L3 on the two pinned carriers, because both are
  stripped and both happen to expose a function whose decompiled body is large (jq 4841 chars; xxd
  carries no pinned address at all) — the limits only surface on a fresh carrier. If a later round
  adds a carrier with symbols or a small binary, the refusal arm must be re-derived first.
- Risk [inf]: `section_count` failing open means `section_count: 0` in any receipt is weaker
  evidence than it reads; a receipt that matters should record `readelf`'s rc and sha256.
- Unknowns: [unk] behaviour on UPX-packed *non-ELF* formats (PE/Mach-O) and on already-packed input
  was not probed (out of scope for this leg); [unk] whether any pinned carrier's pin can drift on a
  rolling-release host update — not probed (would require running the lane instrument, owned by
  other seats).
- No blockers. Scratch `/fast/scratch/hyaku/kaidoku-r68/ExecPacked/` removed after copying receipts.
