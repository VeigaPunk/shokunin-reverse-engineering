# R41W2C1Chain — vendor chain and licence boundary at 7a24ff74

**Verdict: DEFECTS FOUND** — the *hash* chain and the licence boundary hold (every link fails
closed before a cache byte is written, the frozen pins rebuild from the live vendor URLs today,
and no vendor byte is committed anywhere in `49096c7e..7a24ff74`), but the *write* side of
`fetch-vendor.py` still follows symlinks, so a planted cache entry turns one fetch into an
arbitrary-file overwrite with 30 MB of AVM firmware — the exact redistribution the frozen table
forbids — and the nested carrier's declared `length` is never compared by the fetcher.

What I attacked: `tools/round-41/fetch-vendor.py` (member/nested hash links, carve length, cache
write ordering, pin-as-path), the `--carrier-cache` read side of `c1-counter.py`/`c1-extra.py`,
the real d764389e `carriers.json` against the live AVM URLs, and every blob added between the
base and the tip.

## 1. Findings

| id | finding | severity |
|---|---|---|
| D1 | `fetch-vendor.py` writes the carrier and the image through `open(..., 'wb')`, which follows symlinks: planted `<pin>.bin.part` / `<image_sha>.image` symlinks give an arbitrary-file overwrite with vendor bytes, and the cache entry ends as a symlink to the overwritten file (demonstrated) | **Medium** |
| D2 | the `nested` branch ignores `external.length` (a spec one byte short still materialises rc=0); only the counter's `carve_ok` closes it | Low |
| D3 | "vendor bytes are never committed" is prose in the frozen table, not a binding: no scored tool looks at the tree for carrier bytes, so a future commit of the 63 MB cache would not move any binding | Low (calibration) |
| D4 | schema drift: `carriers_spec` does not require `nested.path` (the fetcher does), and the frozen selftest's nested fixture uses `{'member','length'}` — a shape `fetch-vendor.py` rejects | Info |
| D5 | `--rev` git option injection (Sentinel F8) re-tested: fails closed, no write reachable (`<rev>:<path>` mangling) | Info |
| D6 | pin provenance is self-anchored: AVM publishes no `.sha256`/`.asc` beside the images (both 404), so the chain proves the bytes are the ones fetched at freeze, not that AVM produced them (R40-CL2 class) | Info |
| D7 | cache reads are unbounded and symlink-following (`c1-counter.py:1538`): `<pin>.bin` → `/dev/zero` OOMs the counter before hashing | Info |

### D1 — symlink-following cache writes (Medium, demonstrated)

`materialise` ends with `os.makedirs(cache)` (line 239), `open(out + '.part', 'wb')` (241),
`os.replace` (243); the image cache writes at line 108. `open(...,'wb')` follows a planted
symlink. Against the real pinned bytes:

```
ln -s ../target.txt $S/sym/cache/c4f74f54…f872a.bin.part
python3 -I -B …/fetch-vendor.py --spec … --cache $S/sym/cache     # EXIT=0
→ target.txt 18 B → 30 233 394 B, sha256 c4f74f54…f872a (the V3 carrier)
→ cache/c4f74f54….bin is now a symlink to ../target.txt
```

Same with `--image-cache` (`770efb4e….image` → target2.txt, 33 269 760 B, image digest).
Impact: (a) any writable path can be destroyed/overwritten as the caller; (b) if the target is
inside the lane worktree, one routine fetch puts firmware bytes in a tracked path and the next
`git add -A` commits them — D3 means nothing would notice. Detail:
`artifacts/R41W2C1Chain/symlink-write-primitive.md`. Smallest remediation: open the `.part` and
image paths with `O_NOFOLLOW` (or refuse when `islink`), keeping `os.replace` as is.

### D2 — `length` unenforced on the nested branch (Low)

`materialise` lines 218-232: with `nested`, `length = len(body)` (already carved to the
reader's `bytes_used`) and the declared `ext['length']` is never read. V4 declared
32 720 860 vs 32 720 859 → `rc=0`, `ok=true`, no link. `artifacts/…/adversarial-runs.md`.
The claim is unaffected because `c1-counter.py`'s `carve_ok` requires
`length == bytes_used == size` (true for both vendor carriers in `l1/scores/c1-at-e9a24d07.json`),
but the fetcher's docstring ("carve to `length` (bytes_used for a nested carrier)") overstates
what it checks. Fix: after carving, compare `ext['length']` to `used` when present.

### D3 — the licence rule is not a binding (Low, calibration)

`grep -n "ls-tree|committed|licen"` over the frozen tools returns docstrings only; neither
counter hashes the tree. Round 41's clean tree is therefore a *process* result (wave-1
sentinel + scratch-only extraction), not a scored one. Today it holds — measured in §3 — but a
round-42 seat re-pinning the same spec would score 4/4 with the cache committed. Remediation:
a `no_committed_vendor_bytes` binding over the `--rev` tree (1 678 blobs / 41 MB ≈ 5 s here),
comparing against the pins and the oracle digests and **skipping zero-length oracle rows** —
V3's `tmp/mtab` is the empty file, and 6 zero-byte blobs in this range legitimately collide
with its digest (the only false-positive I hit).

## 2. The chain as claimed — confirmed

Real rebuild at the tip (2026-10-26 18:20, exit 0):

| carrier | image | member | nested | carve = pin | carve bytes |
|---|---|---|---|---|---|
| V3 | `770efb4e…` 33 269 760 B | `87cc5d6b…` 30 236 680 B | — | `c4f74f54…f872a` | 30 233 394 |
| V4 | `a5a3a763…` 36 392 960 B | `4cfc3016…` 33 361 928 B | `4d5de25c…` 32 722 944 B | `ce27ebca…087f` | 32 720 860 |

Both carriers decode to `sqsh` 4.0, `mkfs_time == bytes_used == file size`
(30 233 394 / 32 720 860), compression 4 (xz): **carve length equals `bytes_used` exactly**, and
V4's declared `length` equals it too. The V4 nested file is 2 084 B longer than its own
`bytes_used` and the tail is dropped before the pin — as the frozen table states.

Fail-closed, before any write (fresh cache dir per run, real bytes, URLs via `file://` to the
downloaded images): tampered `member_sha256` → exit 1 / `member_sha256`; tampered
`nested.sha256` → 1 / `nested_sha256`; tampered `image_sha256` → 1 / `image_sha256`;
traversal-shaped pin (`../../aaa…`, 64 chars) → 1 / `carrier_sha256`. In **every** failure the
cache directory was not created at all — not `<pin>.bin`, not `<pin>.bin.part` (pin compare at
line 235 precedes `makedirs` at 239). Fetcher selftest 16/16, exit 0.

Cache poisoning (read side): flip one byte at offset 1000 of the V3 entry, delete the V4 entry,
run the frozen `measure()` with a stub rerun → `carrier_pin_ok false` for V3, `carrier_present
false` for V4, `projection_skipped carrier_pin_ok`, `carriers_matched 0`, `met_target false`
(`poison-result.json`); `c1-extra.py:85-92` re-hashes the same way. A poisoned cache can only
block a score, never move one.

Freeze/provenance adjacent checks: `git diff d764389e..7a24ff74` over the frozen paths is empty
(the post-freeze counter rewrite was reverted to freeze bytes before the score), the score's
argv names `--carrier-cache /fast/scratch/hyaku/kaidoku-r41/cache` (outside the repo), and
`prior_pins` carries round-40's four pins so the same vendor member cannot be re-scored.

## 3. Licence boundary — no vendor byte committed

* 1 678 added blobs, 41 399 075 B, hashed in memory from `git cat-file --batch`: **no match**
  against the 9 round-41 pins, the 8 round-40 pins, or the 2 516 distinct digests in the added
  `oracle.tsv` sets (V4: 6 349 rows / 2 470 distinct). The only hash-set hits are the two
  lane-built carriers (`L3` 187 892 B `04cfb4cd…`, `L4` 169 545 B `4c0e5459…`) and the
  empty-file digest.
* Container test: for every added blob ≥ 32 B (1 672) against both rebuilt carriers,
  `carrier.find(blob)` — 3 344 tests, **0 hits**: no committed blob is a byte run of the
  firmware, which a decompressed-file digest check alone would miss.
* Every added blob ≥ 1 MB, listed with digest in `artifacts/…/blob-and-licence-scan.md` §2:
  V4 `after.json` (2 852 279 B) and the two DevCore REA envelopes (3 016 975 / 3 010 488 B) are
  receipts of **paths, sizes and digests** (`files[]` keys are `path, relative_path, size,
  sha256, reported_sha256, mime_type, analysis_depth, runtime_address, original_file_range`;
  `published_bytes` is a number); no base64 blob, longest string a 1 313-byte unblob banner.
  The fourth is C2's `precedence-check-full.tsv` (labels/actions text). The two DevCore
  envelopes are derived from the *public* `FRITZ.Box_7430-07.31.image`, i.e. the same class of
  derived metadata as V4's receipt — no file bodies either way.
* No `filesystem.image`, `filesystem_core.squashfs`, `FRITZ*` or round-41 `_extract/` path in
  the tip tree; the round-41 C1 carrier dirs hold receipts/oracles/logs plus the two lane-built
  `.sqsh`. `c1-run.sh` extracts into `$scratch/extract` (scratch removed by `trap … EXIT`) and
  moves only `after.json` into `OUTDIR`; the raw envelope only under opt-in
  `C1_KEEP_ENVELOPE=1`.

## 4. Limits

* The chain is anchored at the freeze-time fetch: AVM serves no checksum or signature beside
  these images (`.sha256` and `.asc` both 404), so D6 stays open and no independent attestation
  of `image_sha256` exists in the lane. [INFERENCE] A MITM at freeze time would have fixed the
  pins; every later rebuild (including today's) would faithfully reproduce the wrong bytes.
* My licence test covers byte-exact copies (hash equality to every decompressed vendor file and
  container substrings). It does not test *partial textual quotes* of vendor file contents in
  prose. Two cheap checks came back clean: added text has no hexdump/base64 runs, and the
  distinctive V3 `etc/inittab` lines (`pivot_root /core/`,
  `mount -t squashfs /filesystem_core.squashfs`) occur nowhere under
  `.ufo/waves/round-41` or `corpus/evidence/round-41` (the only `ld-uClibc` hits are file
  *names* in path listings). A per-line cross-check against all 6 349 decompressed V4 files
  was not run.
* D1 needs a symlink planted in the cache directory (pre-populated/poisoned/shared scratch). It
  is a local write primitive, not a remote one; the fetch's own network path is sound.
* No REA or unblob run was needed for any probe (the counter probe used a stub rerun), so
  nothing here re-tests the extractor chain; the committed score receipt's own REA clause is
  left to the seats that own it.

## 5. Reproduce

```
S=/fast/scratch/hyaku/kaidoku-r41/R41W2C1Chain; cd $S
python3 -I -B <LANE>/tools/round-41/fetch-vendor.py --root <LANE> \
  --rev d764389e9cbe61b9d1b07538ff3bff02d50bb34f --cache $S/cache --image-cache $S/imgcache
python3 -I -B <LANE>/tools/round-41/fetch-vendor.py --selftest
python3 -I -B <LANE>/tools/round-41/fetch-vendor.py --spec $S/adv/spec-badmember.json --cache $S/adv/c1
HYAKU_SCRATCH=$S/hy python3 poison_test.py
python3 scan_blobs.py ; python3 substr_scan.py
```

Artifacts (no vendor bytes, digests only): `.ufo/waves/round-41/w2/artifacts/R41W2C1Chain/`
(`fetch-rebuild.md`, `adversarial-runs.md`, `symlink-write-primitive.md`,
`cache-poison-counter.md`, `blob-and-licence-scan.md`, `rev-injection.md`, the spec variants,
`fetch-real.json`, `poison-result.json`, `selftest-fetch-vendor.txt`, the three scan scripts).

Tooling: none installed or upgraded — python3 (host 3.14), git, curl, and the existing
`rea-agents@6.5.0` npx package root only (read as `--pkg65`; no REA run). Scratch
`/fast/scratch/hyaku/kaidoku-r41/R41W2C1Chain` removed after the artifacts were copied; the two
downloaded vendor images (69 662 720 B total) and the rebuilt carriers were never copied into the
lane and are cited by digest only.
