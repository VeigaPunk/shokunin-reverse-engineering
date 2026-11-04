# ExecC3 — independent verification of R69-C3's carrier-class evidence

Round 69, wave w1. Operator: leaf verifier. Measured revision `3f3d20fc065b5be62f676028b9a38d316ddfe8fd`;
operative freeze `f15998102f1ce3569e61faa2ac6f286bc414538e`; base `d7d9a62cc70935304e600ed0dee864fc4f1751f7`.
All commands below were run by this seat. Nothing here reuses the route's own analyze receipts: every
count was re-derived from bytes this seat copied and measured.

Scratch: `/fast/scratch/hyaku/kaidoku-r69/ExecC3/` (deleted before yield). No tracked file was touched.

## 0. Environment and pins observed

| item | observed | expected | verdict |
|---|---|---|---|
| `upx --version` first line | `upx 5.2.0` | route pin `upx 5.2.0` | match |
| `sha256sum /usr/bin/upx` | `cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969` | route `UPX_SHA256_PIN` | match |
| `readelf --version` | GNU Binutils 2.47 | — | — |
| instrument `sha256sum tools/round-69/packed-elf.py` | `4ac0d83baee352e42f63b9ced91df01c2ee01f508a35798e400f13478f8aebcc` | frozen input pin | match |
| instrument git rev | `616a5f2f7aabe46f51f2ea06102766f7ce0e3428` | — | parent of the freeze |
| instrument bytes at freeze | same sha256 `4ac0d83b…` (`git show f1599810:tools/round-69/packed-elf.py \| sha256sum`) | frozen input | match |
| `git diff f1599810..HEAD -- tools/round-69/*.py` | empty | no post-freeze edit | match |
| `git merge-base --is-ancestor 616a5f2f f1599810` | yes | instrument before freeze | match |

So the kill rule's "post-freeze instrument edit" clause is not triggered: the measured bytes are the frozen bytes.

## 1. Carrier 3 (`libz`) — pin, format, packed state, round trip

Carrier source `/usr/lib/libz.so.1.3.2` (mode 0755; `/usr/lib/libz.so` and `libz.so.1` are symlinks to it).

```
sha256sum /usr/lib/libz.so.1.3.2
  6c78c5e58c3bb49a1cd151a95cdf1a17fe07a91a57a59e0279b984c533075ca9
```

That equals the `CARRIERS` pin for id `libz` (packed-elf.py:82-83) and the pin named in the claim.

Original format:

```
readelf -h /usr/lib/libz.so.1.3.2
  Class: ELF64
  Data:  2's complement, little endian
  Type:  DYN (Shared object file)
  Machine: Advanced Micro Devices X86-64
  Number of program headers: 11
  Number of section headers: 27

readelf -SW /usr/lib/libz.so.1.3.2 | grep -cE '^\s*\[\s*[0-9]+\]\s'   -> 27
file /usr/lib/libz.so.1.3.2
  ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked,
  BuildID[sha1]=0606e81842eb7aa664b35f3cb354c32c4f3935dc, stripped
```

Control arms on the *original* (must refuse, per `evaluate_carrier`):

```
upx -l ./orig-libz.so.1.3.2 ; echo $?      -> rc=2  (NotPackedException: not packed by UPX)
upx -d ./orig-libz.so.1.3.2 ; echo $?      -> rc=2  (Unpacked 0 files)
```

Pack and packed state:

```
cp /usr/lib/libz.so.1.3.2 ./orig-libz.so.1.3.2 && chmod 755 ./orig-libz.so.1.3.2
upx --best -q -o ./packed-libz.so.1.3.2 ./orig-libz.so.1.3.2   -> rc=0
    108560 ->     65580   60.41%   linux/amd64   packed-libz.so.1.3.2
upx -l ./packed-libz.so.1.3.2                                   -> rc=0 (recognised as UPX-packed)
readelf -SW ./packed-libz.so.1.3.2 | grep -cE '^\s*\[\s*[0-9]+\]\s'  -> 0
readelf -SW ./packed-libz.so.1.3.2  (first line)               -> "There are no sections in this file."
readelf -h ./packed-libz.so.1.3.2  -> Type: DYN (Shared object file); 11 phdrs; 0 section headers
file ./packed-libz.so.1.3.2        -> ELF 64-bit LSB shared object, x86-64, … "no section header"
sha256sum ./packed-libz.so.1.3.2
  a9c544e6da4f93418f15b768873f9ce5177d490e8de7f2e0c30a3f8e0065da5b
```

Round trip:

```
upx -d -q -o ./unpacked-libz.so.1.3.2 ./packed-libz.so.1.3.2   -> rc=0
sha256sum ./unpacked-libz.so.1.3.2
  6c78c5e58c3bb49a1cd151a95cdf1a17fe07a91a57a59e0279b984c533075ca9   == pin
cmp ./unpacked-libz.so.1.3.2 ./orig-libz.so.1.3.2 && echo BYTE-IDENTICAL  -> BYTE-IDENTICAL
readelf -h ./unpacked-libz.so.1.3.2 -> 27 sections, 11 program headers (original shape restored)
```

REA inventory, re-derived by this seat (three independent `rea analyze --format json` runs on
`orig-`, `packed-`, `unpacked-` copies, 184 etc. read from `normalized_result`):

| state | procedure_count | segment_count | string_count |
|---|---|---|---|
| original | **184** | **29** | **199** |
| packed | **98** | **6** | **136** |
| recovered | **184** | **29** | **199** |

This is exactly the claim's `184/29/199 original vs 98/6/136 packed vs 184/29/199 recovered`.
Recovered == original on all three counters → `recovery_ok` is genuinely satisfied, not asserted.

Ratios:

```
declared stub ceiling              = 120 procedures  (CARRIERS libz before_max_procedures)
before_ceiling_ratio = 120/184     = 0.6522   (what the receipt records and the predicate names)
measured packed/orig = 98/184      = 0.5326   (the stronger, measured stub relation — also <= 0.75)
compressed size ratio 65580/108560 = 0.6041
```

## 2. Carriers 1 and 2, for the per-carrier ratio clause

| carrier | pin (observed = CARRIERS) | orig sections/phdrs | orig counts | packed counts | recovered | controls (`upx -l`/`-d` on orig) | size | packed sha256 = route's recorded | ratio |
|---|---|---|---|---|---|---|---|---|---|
| jq | `e8156675…f7806` | 28 / 15 | 167/30/190 | 3/3/3 | 167/30/190 | 2 / 2 | 30800→14036 (45.57%) | `e8b6c9e7…75268a` match | 10/167 = **0.0599** |
| xxd | `7b1e5d0c…ae65` | 27 / 15 | 99/29/103 | 3/3/6 | 99/29/103 | 2 / 2 | 38928→19560 (50.25%) | `1727faf9…eb89ff` match | 10/99 = **0.101** |
| libz | `6c78c5e5…075ca9` | 27 / 11 | 184/29/199 | 98/6/136 | 184/29/199 | 2 / 2 | 108560→65580 (60.41%) | `a9c544e6…65da5b` match | 120/184 = **0.6522** |

jq and xxd are `DYN (Position-Independent Executable file)` per `readelf -h`; libz is
`DYN (Shared object file)`. All three packed copies report 0 sections.

Determinism note (observed): this seat's own `upx --best` outputs hash **identically** to the
`packed_sha256` values recorded in the route's receipt for all three carriers. The route's packed
artifacts are therefore the same bytes an independent packer invocation produces.

## 3. Generalisation probe — a second shared object (not claim input)

Carrier chosen: `/usr/lib/liblzma.so.5.8.4` (same class, compression family, comparable scale).
This carrier is **not** in `CARRIERS`; nothing below feeds the predicate.

```
sha256sum /usr/lib/liblzma.so.5.8.4
  6e4dae5b099ec0e40a56beead2e51f858535aa794b5a8574a6723dfc1da8a3c1   (seat-local pin)
readelf -h -> ELF64, 2's complement little endian, DYN (Shared object file), x86-64,
              11 program headers, 27 section headers
upx -l orig -> rc=2 (not packed)
upx --best  -> rc=0; 219344 -> 127204 (57.99%), linux/amd64
              packed sha256 2acab0192ba37a33141301d11f5a843065e7974e9e179cc531c776c16107d956
upx -l packed -> rc=0
readelf -SW packed -> 0 sections ("There are no sections in this file.")
upx -d -> rc=0; unpacked sha256 6e4dae5b…  == pin; cmp -> BYTE-IDENTICAL
REA counts: orig 417/29/227 ; packed 175/6/177 ; recovered 417/29/227
```

What the probe establishes (observation):

1. The pack-detect-unpack-recover cycle is not a libz special case: a second, larger shared object
   packs (57.99%), lists, holds zero sections packed, unpacks byte-identically and recovers its full
   inventory (417/29/227 == 417/29/227).
2. **The per-carrier stub ceiling is genuinely carrier-specific.** libz's declared ceiling of 120
   procedures accommodates its packed stub (98) with 22 procedures of headroom. The same constant
   applied to liblzma would be *false*: liblzma packs to **175** procedures > 120. The ratio form is
   the transferable part: 175/417 = 0.4197 and 98/184 = 0.5326 are both ≤ 0.75, so a ratio-bounded
   policy generalises where a constant does not. This supports the route's declared-per-carrier design
   (QUALITY #107) and is the number a future fourth carrier would need to re-derive.

## 4. The landing receipt (absent on disk — the route was run by this seat)

`.ufo/waves/round-69/l1/scores/` was empty at start (observed: `total 0`), so
`c3-at-landing.json` did not exist. This seat ran the frozen route itself:

```
python3 -I -B tools/round-69/packed-elf.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --rev 3f3d20fc065b5be62f676028b9a38d316ddfe8fd \
  --pkg /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
  --work /fast/scratch/hyaku/kaidoku-r69/ExecC3 \
  --json-out .ufo/waves/round-69/w1/ExecC3/c3-at-landing-exec3.json
  -> rc=0
```

Receipt comparisons, recorded vs. this seat's own derivation:

| field | route receipt | this seat | match |
|---|---|---|---|
| `libz.pin` | `6c78c5e5…075ca9` | same (host bytes) | yes |
| `libz.format` | ELF64 / 2's complement, little endian / `DYN (Shared object file)` / `Advanced Micro Devices X86-64` | same from `readelf -h` | yes |
| `libz.section_count` (packed) | 0 | 0 | yes |
| `libz.upx_list_rc` | 0 | 0 | yes |
| `libz.before_ceiling` / `ratio` | 120 / 0.6522 | 120 / 120÷184 = 0.6522 | yes |
| `libz.orig_counts` | 184/29/199 | 184/29/199 | yes |
| `libz.packed_counts` | 98/6/136 | 98/6/136 | yes |
| `libz.unpacked_counts` | 184/29/199 | 184/29/199 | yes |
| `libz.packed_sha256` | `a9c544e6…65da5b` | same bytes re-packed independently | yes |
| `libz.control` | list_rc 2, decompress_rc 2 | 2 / 2 | yes |
| `jq` / `xxd` pins, counts, ratios, packed sha256 | as tabled above | identical | yes |
| `target` / `carriers_matched` / `control_ok` / `met_target` / `failing` | 3 / 3 / true / true / [] | independently recomputed from the table: 3/3/true/true/[] | yes |
| `packer` | upx 5.2.0, sha `cf2f6e7c…`, `pin_enforced: true` | host upx equals the pin | yes |
| `instrument` | sha `4ac0d83b…`, rev `616a5f2f…` | frozen bytes, pre-freeze commit | yes |
| arms | all `true` on all three carriers (`refusal_ok` only on jq, which declares an address) | `upx -l`/`-d` controls, 0 sections, sha identity, count equality all re-observed | yes |

No mismatch was found. Two structural notes that are **not** mismatches:

- `before_ceiling_ratio` is the **declared ceil/measured original** ratio (120/184), not the measured
  packed/original ratio (98/184 = 0.5326). The predicate names the former; for libz both are ≤ 0.75,
  so the verdict is unaffected either way. (Observation, reported for clause transparency.)
- The route stores the *packed* section count in `section_count`; the original's 27 sections and 11
  program headers are not recorded per carrier. The claim's "section/segment counts" are therefore
  only partly represented in the receipt, but the arms that use them (`detected`, `recovery_ok`) were
  independently reproduced here (section 1).

Scoring the receipt with the frozen checker:

```
python3 -I -B tools/round-69/packed-elf.py --check-receipt .ufo/waves/round-69/w1/ExecC3/c3-at-landing-exec3.json
{"met": true, "target": 3, "carriers_matched": 3, "control_ok": true, "failing": [],
 "kinds": ["executable","shared-object"], "before_ceilings": [0.0599, 0.101, 0.6522], …}
  -> rc=0
```

## 5. The before-arm

```
python3 -I -B tools/round-69/packed-elf.py --check-receipt .ufo/waves/round-68/l1/scores/c2-at-landing.json
{"met": false, "target": 2, "carriers_matched": 2, "kinds": [null],
 "failing": ["target 2 != 3",
             "carriers_matched 2 != 3",
             "no shared-object carrier: kinds [None]",
             "jq: before_ceiling_ratio None > 0.75",
             "xxd: before_ceiling_ratio None > 0.75"]}
  -> rc=1
```

The round-68 receipt has `target 2`, `carrier_classes null`, `kind_fields [null, null]`,
ids `["jq","xxd"]` — no shared-object carrier and no ceiling records, exactly as the predicate's
before-clause requires. `tools/round-68/packed-elf.py` `CARRIERS` has two entries, no `kind` field,
and `grep -c 'shared-object\|libz'` = 0; the base tree `d7d9a62c` contains no `tools/round-69/` at all.

Note on `.ufo/waves/round-69/l1/pre/c3-at-base.json`: it is a *logged check output* whose first line
is the `+ python3 …` command, not a JSON receipt. Feeding it back to `--check-receipt` exits **2**
(unreadable JSON), so it cannot be mistaken for a pass; its recorded content agrees with the
round-68-receipt run above.

## 6. Clause-strength probes of the frozen checker (synthetic fixtures, not claim input)

Three hand-built receipts in scratch, all scored with the frozen `--check-receipt`:

| fixture | mutation | observed |
|---|---|---|
| `syn-met.json` | none (three carriers, all arms true) | `met true`, `failing []`, rc=0 |
| `syn-loose.json` | libz `before_ceiling_ratio` := 0.9 | `met false`, rc=1, failing exactly `["libz: before_ceiling_ratio 0.9 > 0.75"]` |
| `syn-no-so.json` | all kinds := `executable` | `met false`, rc=1, failing exactly `["no shared-object carrier: kinds ['executable']"]` |

So the ceiling relation and the shared-object-class clause are both load-bearing in the counter.

Two robustness observations (advisory, both fail closed):

- Renaming the shared-object carrier's `id` from `libz` to `not-libz` while keeping
  `kind: shared-object` still scores `met true`. The checker enforces the *class*, not the claim's
  parenthetical `(libz)` naming. This does not affect this round's receipt (its id is `libz`,
  sourced from the frozen `CARRIERS` table), but the counter alone would accept any shared object.
- A receipt whose carriers mix a missing `kind` with a string `kind` (e.g. one carrier without
  `kind`, one `shared-object`) raises `TypeError: '<' not supported between instances of 'str' and
  'NoneType'` at `sort({c.get("kind") …})` (packed-elf.py:292) and exits 1 with a traceback, rather
  than a named failing clause or the route's typed exit 2. Again fails closed; neither frozen receipt
  can hit it (round-68: all `None`; round-69: all strings).

## Verdict on the frozen predicate

Predicate as frozen: the checker must report `met true`, `target 3`, `carriers_matched 3`,
`control_ok true`, `failing []`, every carrier's `before_ceiling_ratio ≤ 0.75`, and one
`shared-object` carrier (`libz`); the same checker over the round-68 receipt must report `target 2`
and no shared-object carrier.

Every clause was observed directly by this seat, from bytes and tools it drove itself:

| clause | observed | status |
|---|---|---|
| `met true` | true (rc 0) | **satisfied** |
| `target 3` | 3 | **satisfied** |
| `carriers_matched 3` | 3 | **satisfied** |
| `control_ok true` | true (all `upx -l`/`-d` on originals rc=2) | **satisfied** |
| `failing []` | [] | **satisfied** |
| every `before_ceiling_ratio ≤ 0.75` | 0.0599 / 0.101 / 0.6522 | **satisfied** |
| one `shared-object` carrier (`libz`) | libz, `DYN (Shared object file)`, pin `6c78c5e5…`, 184/29/199 → 98/6/136 → 184/29/199, byte-identical unpack | **satisfied** |
| before-arm: round-68 receipt → `target 2`, no shared-object | `met false`, target 2, kinds `[None]`, rc 1 | **satisfied** |
| no post-freeze instrument edit | instrument sha = frozen pin at the freeze commit; empty diff since | **satisfied** |

**Verdict: R69-C3's predicate is met as written — observation, not inference.** No count, format,
ratio, pin or packed-hash mismatch was found between the route's three-carrier receipt and this
seat's independent re-derivation. Two counter-strength advisories (id naming not enforced; mixed-kind
`TypeError`) and one clause-reading note (`before_ceiling_ratio` is ceiling/original, not
packed/original) are recorded above; none of them changes the verdict, and none is offered as a
predicate change.
