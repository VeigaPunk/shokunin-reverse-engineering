# R42C1Fetch — round-42 C1 carrier fetch tool (schema, fail-closed chain, D5 write-surface fix)

**Verdict: DONE** — `fetch-carrier.py` is written for the draft's carrier schema, fixes round-41 closure
D5 / `R41W2C1Chain.md` D1 at the write surface, and passes 36/36 offline selftest cases (including the
five mandated ones), 13/13 end-to-end cases on genuine SquashFS v3 fixtures, and 6/6 scale/adversarial
probes. Two facts for the freeze are recorded in §3: `unsquashfs` 4.7.5 cannot read v3 LZMA, and the
counter port must read `carve.bytes_used`/`carve.offset` (there is no `external.length` any more).

Artifacts (all under `.ufo/waves/round-42/w1/artifacts/R42C1Fetch/`):

| file | sha256 | role |
|---|---|---|
| `fetch-carrier.py` | `54b03b6df6b72b67af3aef93f013dd3df2d53a08650039a970908bf8b8b64498` | the tool (936 lines, stdlib only) |
| `e2e-real-fixtures.py` | `8801bcba23cf5011c4fcbceb9140501d34dfd5ddbb9236f370f0278715c361bb` | drive on real v3 fixtures |
| `probes.py` | `f41e23a2e760f99ce1fd49d9c485e3855a52c6fa47dfae8f471af39738770dac` | scale + adversarial probes |
| `selftest.txt` `e2e.log` `probes.txt` | `e9219879…` `8bf78572…` `fef23c4a…` | exact run output retained |
| `schema.md` | `bbff62cc…` | frozen schema + counter-port notes |
| `fixtures/` + `SHA256SUMS` | MIT, 4 files, 12 608 B | the real v3 inputs |

Ported from `git show c4a38ea2:tools/round-41/fetch-vendor.py` (`sha256 1cb0a346…`, the round-41 frozen
digest). Destination for integration: `tools/round-42/fetch-carrier.py`; its default spec path is
`.ufo/waves/round-42/c1/carriers.json`, matching the draft's frozen paths.

## 1. What the tool is

Chain, each link checked before the next step, first failure named in the receipt as `link`:

`url` → `image_sha256` → `member` → `member_sha256` → `carve` (bounds) → `carve_sha256` → `cache` →
`verify`, where the **member** is either a tar member (`kind: tar`, exact name, regular file only), a
byte range of the image (`kind: range`, `offset`+`length`), or the whole image (no container); and the
**carve** is `member[carve.offset : carve.offset+carve.bytes_used]` hashed to the carrier pin. The cache
entry is `CACHE/<carve.sha256>.bin` = exactly the carve window, i.e. the filesystem and nothing else.
`carve.offset` is the new degree of freedom the round-41 schema lacked: a rootfs behind a boot header or
a second padding layer no longer needs a nested-reader step.

Strictness that matters for a frozen table: **unknown keys inside `container` and `carve` are a deliberate
`spec` failure** (a typo like `length:` where `bytes_used:` belongs cannot silently skip a check — the
R41-CL1 class), all digests are 64-hex, `bytes_used > 0`, offsets are non-negative integers, and
`member_sha256` is mandatory for any container. Free metadata (`kind`, `product`, `publisher`, `oracle`,
`nonregular`, `receipt`) rides on the record untouched.

Exit codes: `0` every managed carrier materialised and verified, `1` a chain link broke, `2` usage /
unreadable spec / unusable work or cache path. Per-carrier fail-closed: a carrier that breaks a link
leaves no cache entry and no staging file; earlier carriers of the same run keep theirs ("nothing cached"
is per carrier, exactly as the draft's "fail closed … before the next step" implies).

Modes: `--spec`/`--cache`/`--image-cache`/`--work`/`--json-out`; `--root LANE --rev REV` reads the spec
from git (revision must match `^[0-9a-fA-F]{4,64}$`, so option-injection shapes never reach `git`);
`--selftest`. Downloads stage in `--work`, else `$TMPDIR`, else the platform default, and are removed on
every path; `--image-cache` keeps a verified `<image_sha256>.image` so counter-time reruns work offline.

## 2. D5 / D1 — the write surface (round-41 closing defect)

Round 41 wrote `open(out + '.part', 'wb')` then `os.replace`, so a planted `<pin>.bin.part` symlink turned
one fetch into an arbitrary-file overwrite (`R41W2C1Chain.md` D1, demonstrated there with 30 MB of vendor
bytes). What replaces it:

* `_check_path()` walks **every literal component** of `--cache` and `--image-cache` with `lstat` and
  refuses a symlink or a non-directory component (`link: cache`), creating only missing components. The
  path is never `realpath`-ed first, so a symlinked parent cannot be laundered away.
* Entry writes go to a **fresh random** `.NAME.tmp-<pid>-<rand>` opened
  `O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW`, `fsync`, then `os.replace`. No fixed `.part` name exists any more,
  so the round-41 plant target is not even reachable; a planted `<pin>.bin` **symlink is replaced** by a
  regular file (rename acts on the link, never the target), and a planted hardlink is detached the same
  way (proved in selftest 34 / probe `e`).
* After the rename the entry is `lstat`-ed (must be regular), size-checked, and **re-hashed with
  `O_NOFOLLOW`**; a mismatch unlinks it and fails with `link: verify`. The receipt records
  `cache_entry: symlink-replaced` when it replaced a link, so an auditor sees the plant.
* A stale *directory* at `<pin>.bin` fails closed (`link: cache`) with the temp file removed (selftest 33,
  probe `d`).

## 3. Evidence

### 3.1 Selftest — `python3 -I -B fetch-carrier.py --selftest`, exit 0, 36/36

Offline: inline fixtures, an injected fetcher, real filesystem writes under `TMPDIR`. The five mandated
classes and their cases:

| mandated | cases | link observed |
|---|---|---|
| image digest mismatch | `05-image-sha-mismatch`, `06-partial-download-partial`, `07-partial-download-empty` | `image_sha256`, cache dir never created |
| member mismatch | `08-member-sha-mismatch`, `09-member-sha-omitted` | `member_sha256` / `spec` |
| carve mismatch | `13-carve-sha-mismatch`, `14-carve-overrun` | `carve_sha256` / `carve` |
| symlinked cache entry | `24-cache-entry-symlink-replaced`, `25-cache-part-symlink-ignored`, `26-cache-parent-symlink-refused`, `27-cache-entrypoint-is-symlink`, `32-cache-entrypoint-dir-symlink-refused` | rc 0 with `symlink-replaced`, or `cache` |
| partial download | `06`, `07` (short body) + transport short read in e2e `11` | `image_sha256` / `url` |

Beyond those: green chains through tar, range and no-container (`01`-`04`), member absent / symlink /
hardlink / directory (`10`-`13b`), member name with and without `./` (`13c`), zero length and unknown
carve keys (`15`, `16`), non-integer offset (`17`), range overrun (`18`), container unknown key (`19`),
unreachable URL (`20`), non-hex pin (`21`), non-http(s) scheme (`22`), empty spec (`23`), poisoned regular
entry replaced (`31`), entry-is-directory (`33`), hardlink plant (`34`), image-cache symlink refused
(`28`), image-cache hit with a fetcher that would raise (`29`), no staging leftovers (`30`).

### 3.2 End to end on real v3 fixtures — `e2e-real-fixtures.py …`, exit 0, 13/13

Fixtures are unblob 26.6.4 integration inputs (MIT LFS blobs), pinned in `fixtures/SHA256SUMS`;
`squashfs_v3_le.bin` 4 096 B with `bytes_used` 258, `squashfs_v3_be.lzma.bin` 4 096 B with 256.

```
01-raw-https-carve-to-bytes_used      rc=0 fetch=http 200 entry=258 B 4b2ee30a…
02-tar-container-carve-offset         rc=0 container={tar, ./tqsh.bin, 4672 B} carve={offset 512, 258 B}
03-range-container-second-fixture     rc=0 container={range, offset 65536, 4096 B} entry 256 B
04-carve-pin-mismatch-fails-closed    rc=1 link=carve_sha256 cache_dir_created=False
05-planted-cache-symlinks-not-written-through
                                      rc=0 cache_entry=symlink-replaced; victims 4096 B unchanged;
                                      the planted <pin>.bin.part is still a symlink
06-image-cache-hit-second-run         first=read second=cache
07-exit-2-family                      six usage/env cases all exit 2, no cache dir created
08-rev-mode-committed-spec            --root <sandbox clone> --rev <sha> rc=0, entry = pin
09-carve-reads-as-the-whole-filesystem LE unsquashfs rc=0/0 same, 7z rc=0/0 same;
                                      BE-lzma unsquashfs rc=1/1 same, 7z rc=0/0 same
11-http-short-read-is-a-url-link      rc=1 link=url detail="short read … 512 of 4096"
11b-http-404-is-a-url-link            rc=1 link=url detail="HTTPError: HTTP Error 404"
12-relative-spec-and-cache            rc=0 (relative --spec and --cache resolve against the cwd)
13-no-staging-leftovers               none in TMPDIR
```

Case 01 is a real HTTPS fetch of the LFS blob; case 09 proves the cache entry is the whole filesystem: the
carved 258/256 bytes give byte-identical `unsquashfs -lls` and `7z l` output to the 4 096-byte original.

### 3.3 Scale and adversarial probes — `probes.py …`, exit 0, 6/6

```
a-3MiB-carve-offset-tar      image 3 164 160 B, member 3 153 920 B, carve offset 3 145 728 -> pin ok
b-40MiB-flat-range           image 41 951 232 B, range at 40 MiB -> pin ok, max child RSS 31 764 KiB
c-four-concurrent-runs       four simultaneous CLI runs into one cache: rc [0,0,0,0], one entry, pin ok
d-cache-entry-is-directory   rc=1 link=cache, stale directory untouched, no temp left
e-cache-entry-hardlink       rc=0, victim nlink 1 and byte-identical, entry a new inode with the pin
f-no-staging-leftovers       none
```

Memory is flat: 31 MiB on a 40 MiB image (streaming download, streaming hash, only the carve window is
buffered). Concurrency needs no lock because every writer uses `O_EXCL` + rename; the last rename wins and
its digest is verified. (RSS is `RUSAGE_CHILDREN`; the probe streams the image to disk specifically so the
parent's buffer is not charged to the child's fork-time footprint — the first version of the probe reported
150 MiB for that reason and was corrected.)

Pre-freeze behaviour of the frozen invocation on the real lane, today:

```
$ fetch-carrier.py --root <lane> --rev fdabdfa46fd1 --cache …/prefreeze/cache
fetch-carrier: spec: git show fdabdfa46fd1:.ufo/waves/round-42/c1/carriers.json failed:
  fatal: path '.ufo/waves/round-42/c1/carriers.json' does not exist in 'fdabdfa46fd1…'
rc=2        (no cache dir created)
```

## 4. Findings that feed the freeze (C1, not this seat's claim)

1. **`unsquashfs` 4.7.5 cannot read v3 LZMA, and real 2007-2009 v3 rootfs are LZMA.** My measurement on
   the fixtures: both `squashfs_v3_{le,be}.lzma.bin` give `gzip uncompress failed with error code -3` /
   `FATAL ERROR: read_inode …` and `-lls` exits 1, while `7z l -slt` reports `Method = LZMA Spec` and lists
   them; `unsquashfs -s` (superblock only, no metadata decompression) still exits 0; the gzip fixture
   (`Method = ZLIB`) reads in both producers. Two peers then measured the published family and both came
   back with the same verdict, attributed here as their reports, not mine:
   * `R42C1ImgOpenwrt`: all 10 Kamikaze 8.09/8.09.1/8.09.2 candidate rootfs are `Method = LZMA Spec`
     (7z `-slt`), `unsquashfs -lls/-d` exit 1 on all 10 and `-s` exits 0; unblob 26.6.4 + sasquatch 4.5.1
     does extract them at scale (7.09, designated development, rc=0).
   * `R42C1ImgDdwrt`: all six DD-WRT v24 rootfs (`hsqt` LE at 0xE18E0/0xE1868, `tqsh` BE at
     0xD0144/0xD0000/0x0) are SquashFS 3.0 with LZMA blocks; neither reader accepts the published
     `hsqt`/`tqsh` magic until bytes 0..3 are patched, and after patching 7z lists while unsquashfs still
     fails on the codec.
   Consequence for the draft's oracle line ("unsquashfs reads v1-v3 gzip"): a v3 carrier from these
   publishers cannot use unsquashfs as a producer at all, so the oracle pair collapses to 7z plus the lane
   stdlib reader (the peer's raw-LZMA1 decode is reported feasible on the same metadata blocks). This is a
   C1 freeze decision, not this seat's; my tool is codec-agnostic — it carves and pins bytes and never
   decompresses, so it is unaffected either way. [INFERENCE] `unsquashfs -s` exit 0 is not a codec
   clearance: it only proves the superblock parses, and both LZMA fixtures show that split.
2. **`7z x` is not a safe oracle producer.** Peer finding (`R42C1ImgOpenwrt`), and a reason my e2e uses
   listing only: `7z x` refuses vendor symlinks whose target contains `../` as "Dangerous link path", exits
   2, and still **creates a 0-byte regular file at each refused link path** (102 of 177 on 8.09.2/atheros).
   An oracle built from `7z x` output would publish phantom regular files at symlink paths and break the
   "no non-regular oracle entry as a file" binding. `7z l -slt` `Mode` (type char `-`) is the listing my
   e2e compares, and `unsquashfs -lls` the other; neither extracts.
3. **The counter port must not look for `external.length`.** `tools/round-41/c1-counter.py:1559-1566`
   derives `carve_ok` from `ext['length']`; round 42 replaces it with `carve.bytes_used` + `carve.offset`.
   The tool guarantees `bytes_used == size` of the cache entry, which keeps the counter's invariant
   meaningful; only the key changes. Recorded in `schema.md` §2.
4. **Cache contract unchanged**: `<pin>.bin`, so `--carrier-cache` and `c1-run.sh`'s carrier input keep
   working; nothing about `carriers.json`'s non-chain keys is read by this tool, so `id`/`oracle`/
   `nonregular`/`receipt` stay as the C1 seats define them.
5. **No `nested` step.** The AVM v4 member-inside-member shape is a round-41 concern; v3 carriers are a
   tar member or a byte range plus a carve. Adding nesting would have been a second schema for no claim.
6. **Carve offsets of ~1 MB are exactly what the DD-WRT images need.** The peer-reported `hsqt`/`tqsh`
   rootfs offsets (0xE18E0 = 924 896, 0xD0144 = 852 292, 0xD0000 = 851 968) are ordinary for this tool; probe
   `a` exercises 3 145 728, and the carve offset is what keeps the published image and the carrier distinct. 

## 5. Risks and limits

* Pin provenance is unchanged from round 41: without a vendor `.sha256`/`.asc` the chain proves "these are
  the bytes fetched at freeze time". The digest is the arbiter; the URL is only a locator.
* A redirect is followed but the resolved URL is not recorded, so a mirror that moves later shows up as an
  `image_sha256`/`url` failure on refetch rather than as a moved locator.
* `_check_path` validates each cache-path component immediately before the `O_EXCL` create; a racer that
  swaps a component for a symlink in between is a theoretical TOCTOU window (no `openat2(RESOLVE_NO_SYMLINKS)`
  here). [INFERENCE] not reachable for a scratch cache that only the run itself writes.
* The receipt embeds the absolute cache path; everything else is deterministic, so two runs of the same
  spec and tool bytes agree field-for-field apart from `path`.
* `--json-out` is an ordinary `open()`, i.e. it follows a symlink at the receipt path. It is a report, not
  a cache; the tool's write-surface guarantee covers the cache and image-cache only.
* No extractor was run in this seat: no REA, no unblob, no sasquatch, on any image, published or
  development. Readers used: `unsquashfs` 4.7.5 and `7z` (both on PATH), `curl` for the MIT LFS blobs.

## 6. Files touched

Written: `.ufo/waves/round-42/w1/artifacts/R42C1Fetch/{fetch-carrier.py, e2e-real-fixtures.py, probes.py,
selftest.txt, e2e.log, probes.txt, schema.md, fixtures/*}` and this report. Nothing else in the lane: no
`tools/`, `corpus/`, `plans/`, `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`, `LOG.md`; no VCS mutation (only
`git show`/`rev-parse`/`clone --shared` into scratch, and a `-c user.name=fx` commit inside that clone);
no file in `~/.local/bin` or any PATH directory. Scratch `/fast/scratch/hyaku/kaidoku-r42/R42C1Fetch`
removed after the last run; no third-party image or extracted firmware byte was copied anywhere (the four
MIT fixture blobs in `fixtures/` are 12 608 B total, pinned by `SHA256SUMS`).

## 7. Reproduce

```
S=/fast/scratch/hyaku/kaidoku-r42/R42C1Fetch; A=<LANE>/.ufo/waves/round-42/w1/artifacts/R42C1Fetch
mkdir -p "$S"; cd "$S"; export TMPDIR="$S"
python3 -I -B "$A/fetch-carrier.py" --selftest
python3 -I -B "$A/e2e-real-fixtures.py" --tool "$A/fetch-carrier.py" --fixtures "$A/fixtures" --scratch "$S/e2e"
python3 -I -B "$A/probes.py" --tool "$A/fetch-carrier.py" --fixtures "$A/fixtures" --scratch "$S/probes"
```

Tooling: nothing installed or upgraded this wave; `python3` 3.14.8, `unsquashfs` 4.7.5, `7z`, `git`,
`curl` as already on PATH. Run the frozen tool as `python3 -I -B` so no `__pycache__` and no user site
packages enter the invocation.
