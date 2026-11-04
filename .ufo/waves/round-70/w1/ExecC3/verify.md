# R70-C3 carrier-evidence verification — seat ExecC3 (session ExecC3-2), 2026-11-04

Independent re-derivation from host bytes of every constant declared for R70-C3's carrier set,
against the frozen registry at operative freeze commit `4737a542ae3b1b910d8fe43efbd572bc578b07c6`
(base `5cc845ca88c90e3e8ceb816f75fe44ddb6758a6d`, operative declaration `8b82516182a269482f3a7dc96b50cd2ac349f3a6`).

Axes (godspeed): (1) coverage of declared constants, (2) evidence precision, (3) wall-clock.
Scratch root: `/fast/scratch/hyaku/kaidoku-r70/ExecC3` — removed at end; REA JSONs copied into this
findings dir first. `/tmp` never used. Tooling record: **nothing installed** (upx 5.2.0, node
v24.21.0 via fnm shim, file/readelf/sha256sum/cmp/jq/git all preinstalled; pacman untouched).

## 1. Inputs read
- `plans/round-70-claims.md` — R70-C3 section (full read).
- `.ufo/waves/round-70/claims.json` — `claims[2]`, atoms A4/A5/A8 (full read).

## 2. Frozen state (read-only git only: show / rev-parse / status)

| Command | Result |
|---|---|
| `git -C <lane> show 4737a54…:tools/round-70/packed-elf.py \| sha256sum` | `1601a5b8c91bac4cf3484ac6f1b0a74bd2a7c59590b7c42f149b510e7d021880` |
| `sha256sum <lane>/tools/round-70/packed-elf.py` (tree) | `1601a5b8…` — **identical** ⇒ no post-freeze edit of the C3 instrument ✓ |
| `git -C <lane> show 4737a54…:.ufo/waves/round-70/claims.json \| sha256sum` | `13e7afb578f5ab7d7b20bb20bf06b3843ec37e74aaf4a735cf23927743b2d36f` |
| `sha256sum <lane>/.ufo/waves/round-70/claims.json` (tree) | `13e7afb5…` — **identical** ✓ |
| `git -C <lane> rev-parse HEAD` | `67217e0987a2b31253d0b77f1490a1bfd031575a` |
| `git -C <lane> status --porcelain -- tools/round-70/ .ufo/waves/round-70/claims.json` | empty (clean) ✓ |

Frozen `CARRIERS` (freeze blob, lines 91–110) — matches atom A5 field-for-field:

```
{"id":"jq",   "kind":"executable",    "source":"/usr/bin/jq",          "sha256":"e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806","min_orig_procedures":100,  "before_max_procedures":10}
{"id":"xxd",  "kind":"executable",    "source":"/usr/bin/xxd",         "sha256":"7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65","min_orig_procedures":50,   "before_max_procedures":10}
{"id":"libz", "kind":"shared-object", "source":"/usr/lib/libz.so.1.3.2","sha256":"6c78c5e58c3bb49a1cd151a95cdf1a17fe07a91a57a59e0279b984c533075ca9","min_orig_procedures":150, "before_max_procedures":120}
{"id":"dinit","kind":"static-exe",    "source":"/usr/bin/docker-init", "sha256":"0bd49c8d4da5601ce955c24a515917c9a132404df633c1e2fa28855cc2e3e115","min_orig_procedures":1000,"before_max_procedures":10}
```
Frozen `DECLARED_ORIG` (line 116): `{"jq": 167, "xxd": 99, "libz": 184, "dinit": 1268}` ✓

Base before-state: `git show 5cc845ca…:tools/round-69/packed-elf.py | sha256sum` →
`4ac0d83baee352e42f63b9ced91df01c2ee01f508a35798e400f13478f8aebcc` == `loaded_by_counter` pin ✓;
its `CARRIERS` holds exactly 3 entries (jq, xxd, libz) and `grep -c "static-exe"` → **0**
(exit 1 = zero matches) ⇒ the base instrument carries no static executable, exactly the claim's
before-world ✓.

## 3. dinit host-byte re-derivation

| Step | Command | Observed |
|---|---|---|
| pin | `sha256sum /usr/bin/docker-init` | `0bd49c8d4da5601ce955c24a515917c9a132404df633c1e2fa28855cc2e3e115` == pin ✓ |
| kind | `file -L /usr/bin/docker-init` | `ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, BuildID[sha1]=1ac9b530…, for GNU/Linux 4.4.0, stripped` ⇒ static-exe grounds ✓ |
| size | `ls -l` | 851288 bytes |
| header | `readelf -h` (original) | Class ELF64, Data LSB 2's complement, Type EXEC, Machine AMD X86-64, entry `0x4031c0`, 12 program headers, 28 section headers |
| copy | `cp` → scratch, `sha256sum` copy | `0bd49c8d…` identical ✓ |
| pack | `upx --best -q -o docker-init.upx docker-init.orig` (upx 5.2.0 == A8 version pin) | `851288 -> 357784  42.03%  linux/amd64`, "Packed 1 file." |
| unpack | `upx -d -o docker-init.unpacked docker-init.upx` | `851288 <- 357784  42.03%`, "Unpacked 1 file." |
| identity | `cmp docker-init.orig docker-init.unpacked` | exit 0 → `ROUNDTRIP_BYTE_IDENTICAL` ✓ |
| packed hash | `sha256sum docker-init.upx` | `b67ce1bdda27880a3448e25d519bcc7af2ffb073bf2ea2867a1d16dbb9f14bc7` — **equals** the route's own `packed_sha256` for dinit in `.ufo/waves/round-70/l1/pre/c3-at-declaration.json` (declaration-rev genuine run) ⇒ deterministic reproduction of the route's pack ✓ |
| header | `readelf -h` (packed) | Class ELF64, LSB, Type EXEC, AMD X86-64, entry `0x52b1b0`, 6 program headers, 0 section headers; `file -L`: `statically linked, no section header` |

## 4. REA counts (pinned package, route command shape)

`node scripts/rea.mjs analyze --format json <path>` at
`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`; node v24.21.0;
`sha256sum …/rea-agents/package.json` → `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c`
== A8 REA pin ✓. Provider: rea-workflow v1 (upstream Ghidra 12.1.4), `confidence: derived`.

| Subject | sha256 | evidence_id | procedures | segments | strings |
|---|---|---|---|---|---|
| docker-init.orig (my run) | `0bd49c8d…` | `ev_247f2b9d6233de3e718ddcebc9f849bde62ea96bc8808f40db2cac4090be7b71` | **1268** | **29** | **1111** |
| docker-init.upx (my run) | `b67ce1bd…` | `ev_e3dd72a8766b015379b735f95c998ecf952b411757c858c265f896949b8b8a28` | **3** | **3** | **5** |

Declared (plan + A5 + frozen `DECLARED_ORIG`/`before_max_procedures`): original 1268/29/1111,
packed 3/3/5 — **both match exactly** ✓. Raw JSONs preserved here as `rea-orig.json`,
`rea-packed.json`. `evidence_id` differs between runs because it embeds the subject's local
path/name; the subject digest and `normalized_result` counts are the stable evidence.

## 5. Ratio arithmetic
`round(10/1268, 4) = 0.0079` ✓ (= plan, = A5, = receipt `ceiling_ratio`). Class ceilings:
jq 10/167 = 0.0599, xxd 10/99 = 0.101, libz 120/184 = 0.6522, dinit 10/1268 = 0.0079 —
all ≤ 0.75 ✓ (A4). `min_orig_procedures`: 1000 ≤ 1268 ✓.

## 6. Other three carriers + packer pins (host vs frozen table)

| Path | measured sha256 | frozen pin | |
|---|---|---|---|
| `/usr/bin/jq` | `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806` | same | ✓ |
| `/usr/bin/xxd` | `7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65` | same | ✓ |
| `/usr/lib/libz.so.1.3.2` | `6c78c5e58c3bb49a1cd151a95cdf1a17fe07a91a57a59e0279b984c533075ca9` | same | ✓ |
| `/usr/bin/upx` | `cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969` | A8 packer pin | ✓ (version 5.2.0 == A8) |

Route-declared orig counts for these three (pre receipt `c3-at-declaration.json`, rev
`8b825161…`): jq 167/30/190, xxd 99/29/103, libz 184/29/199 — each carrier row bound to its
declared original procedure count in `DECLARED_ORIG` ✓ (4 of 4 carriers pinned).

## 7. Producer-binding rejection of the round-69 receipt (supplementary, read-only)

```
python3 -I -B tools/round-70/packed-elf.py --check-receipt \
  .ufo/waves/round-69/l1/scores/c3-at-landing.json --root . --rev 67217e0987a2b31253d0b77f1490a1bfd031575a
```
exit **1**, `met: false`, `failing` includes the producer-binding clause
`instrument.sha256 4ac0d83b… != blob at 67217e09… (1601a5b8…)` and `target 3 != 4`
(also rev, carriers_matched 3 != 4, carrier rows, kinds, ids). The frozen checker is bound to its
own producer bytes ✓ — the C3 predicate's second half, observed at HEAD; L1 scoring runs the same
command at the landing revision.

## 8. Declared vs measured — summary

| Declared (plan/A5/frozen table) | Independently measured | |
|---|---|---|
| dinit sha256 `0bd49c8d…` | same | ✓ |
| kind `static-exe`, statically linked | `file -L`: statically linked, stripped | ✓ |
| orig 1268 procedures / 29 segments / 1111 strings | 1268 / 29 / 1111 | ✓ |
| packed 3 / 3 / 5 | 3 / 3 / 5 | ✓ |
| ceiling 10; ratio 0.0079 | round(10/1268,4)=0.0079; measured packed 3 ≤ 10 | ✓ |
| upx roundtrip sha256 identity (route property) | `cmp` byte-identical; packed copy reproduces route's `b67ce1bd…` | ✓ |
| target 4 carriers, all pins | 4/4 pins match (jq, xxd, libz, dinit) | ✓ |
| no post-freeze instrument edit | freeze blob == tree bytes for checker + claims container | ✓ |
| base has no static-exe carrier | round-69 CARRIERS: 3 rows, zero `static-exe` | ✓ |

## 9. Cleanup
`rea-orig.json`, `rea-packed.json` copied into this findings dir; scratch root
`/fast/scratch/hyaku/kaidoku-r70/ExecC3` removed (`rm -rf`). No file outside
`.ufo/waves/round-70/w1/ExecC3*/` written in the lane; no mutating git/jj command anywhere.

VERDICT: met — every R70-C3 carrier constant re-derives from host bytes exactly as frozen (dinit pin/kind, 1268/29/1111 orig, 3/3/5 packed, ratio 0.0079, byte-identical roundtrip, 4/4 carrier pins, intact freeze bytes, round-69 receipt rejected on producer binding); full-claim scoring remains the frozen checker's at the landing revision.
