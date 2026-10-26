# R41C1Fetch — round-41 fetch chain (R41-C1, wave-1 pre-freeze)

**Verdict: DONE.** `fetch-vendor.py` is ported to round 41 with the R40-CL6 member-hash
link enforced fail-closed, an optional **nested** chain step that reads a carrier out of a
member SquashFS with the pure-Python reader (extract-one-file **added** to `sqfs-list.py`:
`SquashFS.lookup` + `extract_file` + CLI `--extract/--out`), and 16/16 selftest cases,
13/13 genuine-AVM integration cases and a real-vendor-bytes run against the round-40 V1/V2
pins all green. No reserved image was downloaded or opened, no REA/unblob run, no lane file
outside my artifacts dir, no VCS mutation.

Base `49096c7e6f226af0c750c4b003be58883cb6049f` (`git rev-parse HEAD` of the lane at the time
of writing; the only untracked paths are `plans/round-41-claims.md` (L1's draft) and
`.ufo/waves/round-41/`).

## 1. Deliverables

All under `.ufo/waves/round-41/w1/artifacts/R41C1Fetch/` (lane-relative); host python
3.14.8, stdlib only.

| file | bytes | lines | sha256 |
|---|---|---|---|
| `fetch-vendor.py` | 17 827 | 416 | `1cb0a34688488160bc693369dadf21152050cdd6e1654f7d1f6c168bc8ea0e04` |
| `sqfs-list.py` | 66 932 | 1 585 | `a8e633f5fe34ad9495ef1cf8d4dd43a718e25352b0f5ae13c760655b8664969d` |
| `selftest-genuine-avm.py` | 10 118 | — | `e2015a987cebd247a63aebc5a5359e03d2dc3aaeceb44f50af13417a0cff802e` |
| `selftest-transcripts.txt` | 3 050 | — | `f8ce30d37ae99d38c584eb4c5c49a26dd57e6ab9fc1fee673918db8b991c91c7` |
| `reader-real-vendor.txt` | 1 805 | — | `e925e50dd89beb7d01cf0132735a52b90a7db0f67324436f930fc1998bd271f1` |
| `vendor-chain-evidence.txt` | 2 372 | — | `b592453a2bc83f28c3616f16664c9f6736438189a90a95c21ed07eb697f32608` |
| `vendor-r40-chain.rec.json` | 1 625 | — | `08c4f25357648aba2887153f098314bf989eeb3c84a35abcd07c4ce2ffb82806` |
| `vendor-r40-badmember.rec.json` | 1 498 | — | `3f31aa887b37f67907eba27bd07af0b2131b51779fa75326c3e584120849f075` |
| `diff-fetch-vendor-r40-to-r41.diff` | 20 683 | — | `fe4bd52b774f86280e9a71b7be4e936ae6dd61d427bcd293bbca88d46f3ba629` |
| `diff-sqfs-list-r40-to-r41.diff` | 10 284 | — | `ee8f29c8f2a66d11f817843ec8f9dd4d17f4c6bc767e09d87ddccd5f2277c50d` |

Both code files are stdlib-only and self-contained; `fetch-vendor.py` finds `sqfs-list.py`
next to itself (`os.path.dirname(os.path.abspath(__file__))`), so **the L1 must copy the two
files together** into `tools/round-41/`. `tools/round-40/` was not modified.

## 2. The chain as implemented

One `materialise()` pass per carrier whose spec entry has `external`; each link is checked
before the next is read, and **nothing is written unless every link matched** (the cache
entry appears through `<pin>.bin.part` → `os.replace` only after the pin matches).

    url                                   link `url`            (network/URL error)
      sha256(image) == external.image_sha256      `image_sha256`
      tar member external.member                  `member`   (absent / not a regular file)
      sha256(member) == external.member_sha256    `member_sha256`   ← R40-CL6, NEW
      nested step (only if external.nested)       `nested`, `nested_sha256`
      carve                                       `length`   (non-nested only)
      sha256(carve) == carrier sha256             `carrier_sha256`
      write CACHE/<pin>.bin

Record fields per carrier: `id`, `pin`, `url`, `fetch` (`read` / `cache` / `http N`),
`image_sha256`, `member_detail`, `member_sha256`, `nested{…}`, `nested_detail`,
`carrier_sha256`, `ok`, `path`, `bytes`, plus `link`+`detail` on failure.

Exit codes: **0** every external carrier green; **1** a link failed (nothing cached for that
carrier); **2** usage / spec unreadable (including `--root --rev` where
`.ufo/waves/round-41/c1/carriers.json` does not exist at that rev).

### 2.1 R40-CL6 — member hash is a link, and it is mandatory

`external.member_sha256` hashes the **whole tar member before carving** (the round-40 V1/V2
pins confirm that semantic: member 5 443 592 B → carve 5 442 392 B, and the pin is the
5 442 392-byte carve). A spec that omits `member_sha256` fails closed with
`link=member_sha256, detail="spec omits member_sha256 (required since round 41)"` instead of
silently trusting `length`.

### 2.2 The nested step

```json
"external": { "url": "…", "image_sha256": "…",
              "member": "./var/tmp/filesystem.image",
              "member_sha256": "…",
              "nested": {"path": "filesystem_core.squashfs",
                         "sha256": "<sha256 of that whole file>"} }
```

* the member bytes are opened as a SquashFS image by probing layouts in the order
  `auto, avm, be, le` and taking the first that parses (`open_member`); the **file hash is
  the arbiter**, so a wrong layout guess cannot produce a passing chain;
* `nested.path` is **literal** — no symlink resolution, so no link inside a member can
  redirect the chain; a missing path, a symlink, a directory or a non-SquashFS member all
  fail with `link=nested`;
* the extracted file is hashed **whole** against `nested.sha256`, then carved to **its own**
  superblock `bytes_used` (the member's `bytes_used` is a different image — that was a real
  bug I hit and fixed, see §4.3 `green-carve-length`);
* `nested` wins over `length`: when `nested` is present the carve length is the nested
  carrier's `bytes_used` and any `external.length` is unused; the receipt records it as
  `nested.carrier_bytes_used`.

### 2.3 Extract-one-file: **added**, not reused

Round-40 `sqfs-list.py` had no single-file reader (`collect()` hashes the whole tree and
`iter_file_data()` is per-inode). I added, in `sqfs-list.py`:

* `SquashFS(path=None, layout='auto', data=None)` — in-memory construction (a member of a
  member), `path` then a label only;
* `SquashFS.lookup(rel)` — literal POSIX path → `(kind, payload)`, `SqfsError` if absent;
* `extract_file(img, rel)` — regular-file bytes, fails closed on non-regular/missing and
  checks the byte count against the inode `file_size`;
* CLI `--extract REL --out FILE` (exit 2 on any `SqfsError`, no output file created);
* module docstring `Round-41 additions` §6 and three new selftest cases.

The reader's public surface (`collect`, TSV grammar, `--inspect` keys, exit codes) is
unchanged, so the existing counter/oracle callers keep working.

## 3. Evidence — selftests (transcripts: `selftest-transcripts.txt`)

Host: `Linux 7.2.11-arch1-1`, `Python 3.14.8`; every run `cd $S` with `TMPDIR=$S`
(`/fast/scratch/hyaku/kaidoku-r41/R41C1Fetch`), `python3 -I -B`.

### 3.1 `sqfs-list.py --selftest` → `16/16 passed`, exit 0

Round-40's 13 cases still pass (le/be/avm/gzip/xz/lzma2, auto layout, extended inodes,
fragments, escaping links, bad magic, unsupported compression, truncated) **plus**

| new case | what it pins |
|---|---|
| `extract-one-avm-inmemory` | AVM image built in memory, `data=` construction, `avm_marker`, extract of a fragment-tailed file and of a multi-block file, and the `rel`, `./rel`, `/rel` spellings all give identical bytes; absent path / symlink / directory raise |
| `extract-literal-collisions` | both nested-name collision directions: regular `usr/bin/busy` vs symlink `bin/busy`, and regular `sbin/reboot` vs symlink `usr/sbin/reboot` — each path extracts (or refuses) **exactly**, never by suffix |
| `extract-cli` | `--extract … --out` exit 0 writes the bytes; `--extract docs/abs` exits 2 and writes no file |

### 3.2 `fetch-vendor.py --selftest` → `cases=16 pass=16 fail=0`, exit 0

Synthetic tars + real SquashFS member/inner images built in-process by the reader's own
independent writer (`_build_image`, AVM layout: BE fields, LE metadata headers,
`mkfs_time == bytes_used`). Inner carrier 945 B stored as 1161 B (trailing pad) so the carve
to `bytes_used` is exercised; `inner pin = cf2ff1cc4cff110d0c5c2d989fa3f25d346466ac587eafa27114fa340904d9dc`.

| case | rc | link | cache |
|---|---|---|---|
| `nested-green` | 0 | — | `<pin>.bin` |
| `nested-writes-carved-bytes` | 0 | — | cached sha == pin |
| `plain-green` | 0 | — | `<pin>.bin` |
| `bad-url` | 1 | `url` | none |
| `image-sha` | 1 | `image_sha256` | none |
| `member-sha-mismatch` | 1 | `member_sha256` | none |
| `member-sha-omitted` | 1 | `member_sha256` | none |
| `member-absent` | 1 | `member` | none |
| `nested-sha-mismatch` | 1 | `nested_sha256` | none |
| `nested-path-absent` | 1 | `nested` | none |
| `nested-path-is-symlink` | 1 | `nested` | none |
| `nested-on-nonsquashfs-member` | 1 | `nested` | none |
| `pin-mismatch-whole-member` | 1 | `carrier_sha256` | none |
| `length-overrun` | 1 | `length` | none |
| `nested-pin-mismatch` | 1 | `carrier_sha256` | none |
| `spec-missing-image-sha` | 1 | `spec` | none |

The four required red/green directions are all present: **member sha mismatch → red**,
**image sha mismatch → red**, **nested sha mismatch → red**, **good chain → green**.

### 3.3 `selftest-genuine-avm.py` (integration, `gen-squashfs.py --endian avm-genuine`) → `13/13`, exit 0

The driver builds, in scratch, with `tools/round-40/gen-squashfs.py --endian avm-genuine`:
an inner AVM carrier (xz) carrying a both-direction collision pair
(`usr/bin/busy` regular vs `bin/busy` symlink; `sbin/reboot` regular vs `usr/sbin/reboot`
symlink), an AVM member (gzip) carrying that carrier at
`var/tmp/filesystem_core.squashfs` **plus padding**, a symlink `lib/filesystem_core.squashfs`
and a regular `etc/inner` whose path ends with that symlink's path, and a tar image holding
the member at `./var/tmp/filesystem.image`. `url` is a `file://` URL (no network).

```
PASS green-exit                          rc=0
PASS green-cache-carved-to-bytes_used    cache=True sha=cf2ff1cc4cff110d0c5c2d989fa3f2…04d9dc
PASS green-carve-length                  carved 945, inner 945
PASS green-member-sha-recorded           b8e287738229801f5dd71485da8141ccb1951a42ba8ed8a19279a8f966889c95
PASS green-nested-layout-avm             bytes 1161, carrier_bytes_used 945, carrier_layout avm,
                                         carrier_avm_marker true, carrier_probe_layout auto,
                                         member_layout avm, member_probe_layout auto
PASS green-nested-marker                 true
PASS green-member-layout-avm             avm
PASS reader-extract-byte-identical       --extract output == the file written into the member tree
PASS green-image-cache                   first=read second=cache   (same --image-cache dir)
PASS red-member-sha                      rc=1 link=member_sha256 cache=False
PASS red-image-sha                       rc=1 link=image_sha256
PASS red-nested-sha                      rc=1 link=nested_sha256
PASS red-carrier-pin                     rc=1 link=carrier_sha256
INTEGRATION cases=13 pass=13 fail=0
```

Note the first green iteration was red: the prototype carved the nested file to the
**member's** `bytes_used` (a real defect caught by `green-carve-length`), which is exactly
the class of error the claim's nested step has to survive.

## 4. Evidence — real vendor bytes (round-40 dev inputs; `vendor-chain-evidence.txt`)

Spec: `git show 49096c7e…:.ufo/waves/round-40/c1/carriers.json` (V1 6490 Cable 07.57,
V2 6820v1 LTE 07.30 — already burned in round 40, **not** reserved).

```
cold run, fresh --image-cache:
V1 ok=True fetch=http 200 image_sha256=f518ce6baa05b30d84264d9349cca9bf0b9402986d4112bda8ad73a04f9ede6d
   member_sha256 =334e56dfba6a785590bb5cdbd78fcb5be183b9af160b51fc8935a3015ad3f3d4
   carrier_sha256=ac4098bd11a76f8ad001faac0f1a5e018708d9b03943dfebb2b18a24e0038e95  bytes=5442392
V2 ok=True fetch=http 200 image_sha256=3948449d89708589cde05e8495a34cb7ed1efeb880d1ed4539b07d4594069450
   member_sha256 =cacc6461ba491b3ef73fba9cd7e402adeabad4abba10c738b5bc9b17c15b4b19
   carrier_sha256=5ccc7614263e4b4b392025e1561e071a744b6464a4c88548633e87f71f3d089b  bytes=26013550
exit_code=0
```

Both carrier pins are reproduced **exactly** as round-40 pinned them, and both member hashes
match the pinned `member_sha256` — i.e. the new link is consistent with real vendor bytes.
Whole run (two downloads) took 8.0 s wall.

**R40-CL6 red path on the same real bytes** (every `member_sha256` replaced by `d`×64, warm
image cache): `exit=1`, `V1 ok=False link=member_sha256`, `V2 ok=False link=member_sha256`,
`cache dir created: False` — fail-closed and nothing on disk.

**`--root … --rev 49096c7e…`** (the rev has no `.ufo/waves/round-41/c1/carriers.json`):
`exit=2`, no cache dir — the pre-freeze expected state.

### 4.1 The reader's new extract path on a real vendor AVM carrier (`reader-real-vendor.txt`)

Round-40 V1 carrier (`ac4098bd…e0038e95`, 5 442 392 B), `--layout auto`:

```
layout=avm header_endian=little block_length_signal=plausibility avm_marker=true comp=xz
files=697 dirs=117 symlinks=263 (263 in-tree, 0 escaping) sparse_blocks=1 warnings=[]
extract bin/allcfgconv: rc=0 wall=0.05s bytes=7580
   sha256=17981448c3e29b8d5133978424e06e01b52a442790da8dd91ff8a62477220e10  == the --files row
extract bin/ash (a symlink):  rc=2  "'bin/ash' is a symlink, not a regular file", no output file
```

V2 (26 MB carrier): full walk 0.08 s, `layout=avm, marker=True, files=8, links=85`.

Measured on V1: **zero** both-direction path-suffix collisions between a regular file and a
symlink (697 regular / 263 symlinks). So a both-direction collision fixture has to be built
(the reader selftest builds both; the round-41 counter must do the same) — the vendor
carriers themselves do not supply that shape.

## 5. Integration notes for the L1 / the R41-C1 counter seat

1. **Port both files together** to `tools/round-41/{fetch-vendor, sqfs-list}.py`; they are
   byte-identical to my artifacts. `fetch-vendor.py`'s `CARRIERS` constant is
   `.ufo/waves/round-41/c1/carriers.json` (used by `--root --rev`).
2. **The round-40 counter's spec validator must change.** `tools/round-40/c1-counter.py`
   (`git show …:tools/round-40/c1-counter.py`, the `ext = c.get('external')` block, ~l.483-497)
   requires `('url', 'image_sha256', 'member', 'length')` for every external carrier and
   knows nothing about `nested`. For V4 (nested) that validator would reject the entry. The
   round-41 port must accept **`length` XOR `nested`** and should require
   `member_sha256` (64 hex).
3. **V3 (vendor wrapper, no nested step)** — shape the spec entry like round-40's V1:
   `external = {url, image_sha256, member, member_sha256, length, product}`, `length =
   bytes_used` of the member squashfs (30233394 per the draft), pin = carve sha256.
4. **V4 (nested)** — `external = {url, image_sha256, member, member_sha256, nested:{path,
   sha256}, product}`; no `length`. The nested file is the full carrier; pin =
   sha256(the nested file carved to its own `bytes_used`). Compute `nested.sha256` over the
   **whole** extracted file as it sits in the member (this is what the tool checks), never
   over the carved prefix.
5. The receipt already carries what a counter needs for the claim's fetch-chain clause:
   `image_sha256`, `member_sha256`, `nested.sha256` + `nested.carrier_bytes_used`,
   `carrier_sha256`, `fetch`, `bytes`, `ok`, `link`. `--json-out FILE` writes it.
6. Consumers may keep keying on `ok`/`path`/`bytes`; the `link` vocabulary gained `length`
   (was `member` in round 40 for a bad carve length), `nested`, `nested_sha256`, `spec`, and
   `member_sha256`. Round-40's `member` is now only "member absent / not a regular file".

## 6. Risks and inferences

* **[INFERENCE]** V3/V4 real bytes are untested (reserved, correctly). The nested step is
  exercised on AVM-genuine synthetic members, the reader is exercised on real vendor AVM
  carriers (V1/V2), and every failure mode I could construct fails closed with `link=nested`.
  The first real V4 attempt is the risk point; a failure there is loud, not silent.
* **[INFERENCE]** `nested.path` must be spelled exactly as stored (no `./`, no `..`; `lookup`
  only strips leading `./` and `/`). If the 5491 member stores the carrier under a path with
  a leading `./`, the reader's normalisation covers it; anything else fails with `nested`.
* **[INFERENCE]** Cost on a full rootfs member (≈10⁴ inodes) is a full metadata walk per
  `lookup`; V1 (697 files) is 0.05 s, V2 0.08 s, so a 5491-sized member should be seconds,
  not minutes — not measured.
* The nested file is read fully into memory (member + nested, e.g. 50 MB + 30 MB): fine here,
  worth remembering if a future member is much larger.
* `--image-cache` only stores an image whose sha256 already matched, so a poisoned cache
  entry cannot be admitted (the `cache` hit path re-hashes before use).
* A `file://` URL reports no HTTP status; the sha256 check is the only gate (documented in
  `fetch()`). This is why the integration driver can run with no network.

## 7. Bounds compliance

* Wrote only `.ufo/waves/round-41/w1/artifacts/R41C1Fetch/**` and this report. `git status
  --porcelain` shows only `?? .ufo/waves/round-41/` and L1's `?? plans/round-41-claims.md`.
* Read-only git (`show`, `rev-parse`, `status`); no add/commit/checkout/reset/stash; no jj.
* No REA, no unblob, no sasquatch, no extractor of any kind was run. No download or read of
  FRITZ!Box 3490/5490/5491/7560 images or anything carved from them; the only vendor bytes
  touched are the round-40 dev inputs V1 (6490 07.57) and V2 (6820v1 07.30), cited by sha256
  only. No vendor bytes or extracted vendor files were copied into the lane.
* All scratch under `/fast/scratch/hyaku/kaidoku-r41/R41C1Fetch` (created, used, removed at
  exit); the artifacts contain only code, small text and JSON receipts.
* Leaf seat: no subagents, no background jobs, no `agent://all`.

## 8. Tooling

Nothing installed or upgraded (no pacman, uv, npx, pip). Tools used: `python3` 3.14.8,
`git` (read-only), lane `tools/round-40/gen-squashfs.py` (as a test input generator only).
