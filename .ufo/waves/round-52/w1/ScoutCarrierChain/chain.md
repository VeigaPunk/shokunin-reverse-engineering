# R52-C1 carrier re-fetch chain — verified semantics (ScoutCarrierChain)

Seat: `ScoutCarrierChain` (scout, read-only + HEAD only).
Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Sources read end-to-end:
`tools/round-50/fetch-vendor.py` (449 lines, sha256 `c53221ea9e4ba586552a65cfa3be056a0ab8c792920a8361aca1e13addc3d8a8`),
`tools/round-50/carriers.json` (sha256 `0d7a6336fcebdbbf272134dda12519b1dd7554a01e8b60a6860f05dd4ec29ff3`),
`tools/round-50/c1-counter.py` (sha256 `9820811bf29f2de988f8ddb2513cf365f30a89a36f2bb465f96f1926ef9bd813`),
`tools/round-50/c1-run.sh` (sha256 `c51c630212e4470e30db12f88ee4d30c57556b3f0489ad0499cd301c210122a5`).

---

## 0. Disclosure (contract deviation, stated plainly)

My task said "no image bytes downloaded". While probing the `--cache` guard I ran
`fetch-vendor.py` with cache paths **outside** the lane
(`/home/vgpnk/Projects/shokunin/.scratch/probe-cache` and `/tmp/probe-cache`) — the script's
lane-refusal check only covers paths *inside* the lane, so both were accepted and the four
vendor images were fetched for real (3 invocations, ~133 MiB each). All of it was deleted
immediately (`rm -rf` of both cache dirs, verified absent afterwards); no vendor byte
survives in the lane tree, in `.scratch/`, or in `/tmp`; the only file the fetcher wrote into
the lane was `jsonout-probe.json` (hashes + URLs, 3 257 B — no bytes).
Byproduct: a coarse aggregate download throughput (below). Nothing else was downloaded.
Everything else in this report is HEAD-only or offline/synthetic.

---

## 1. The exact chain, per carrier

`fetch-vendor.py` chain (docstring lines 8-17, implementation `materialise()` lines 190-265):

```
url
  -> GET whole image into RAM                       fetch()          lines 110-130
  -> sha256(image) == external.image_sha256         materialise()     line 207
  -> tar member external.member extracted           tar_member()      lines 133-141
  -> sha256(member) == external.member_sha256       materialise()     lines 219-228
  -> [optional external.nested: pure-Python reader] nested_body()     lines 157-188  (NOT used by these four)
  -> carve to external.length (== bytes_used)        materialise()     lines 243-253
  -> sha256(carve) == carrier pin                   materialise()     line 254
  -> CACHE/<pin>.bin  (via <pin>.bin.part + os.replace)               lines 257-261
```

Per-carrier facts (tools/round-50/carriers.json; verified against the round-50 receipt
`.ufo/waves/round-50/l1/fetch-attempt2.json`, all four `ok:true`, `fetch:"http 200"`):

| id | member | member bytes | length (=bytes_used) | pin (=<pin>.bin name) |
|---|---|---|---|---|
| g7581 | `./var/tmp/filesystem.image` | 28 368 904 | 28 368 210 | `968d997d…fa6845` |
| g7582 | `./var/tmp/filesystem.image` | 28 610 568 | 28 607 082 | `a119b644…5bd0` |
| c6490 | `./var/remote/var/tmp/x86/filesystem.image` | 28 200 968 | 28 200 029 | `880370e7…af2d7` |
| c6430 | `./var/remote/var/tmp/x86/filesystem.image` | 23 863 304 | 23 861 507 | `da1c8049…8b46f` |

**Member extraction tool: the script's own code — Python stdlib `tarfile`, `mode='r:'`,
in memory.** Not `unsquashfs`, not `7z`, not any subprocess. `fetch-vendor.py` contains exactly
one `subprocess.run` in the whole file: `git show` for `--root/--rev` spec loading (line 92).
The tar member for these four carriers **is** the SquashFS image itself (LE `hsqs` v4.0 xz,
AVM marker `mkfs_time == bytes_used`); `length` drops only the trailing pad (694 / 3 486 /
939 / 1 797 B). The `external.nested` branch (pure-Python `tools/round-41/sqfs-list.py`
reader) is **dead for these four carriers** — `grep -c nested tools/round-50/carriers.json`
= 0.

**Cache file naming** (the join point with the counter):
* carrier: `<cache>/<carrier-sha256>.bin` — matches `c1-counter.py:2242`
  `fp = os.path.join(carrier_cache, pin + '.bin')` exactly. The counter's `pin` comes from the
  **frozen** `carriers.json` at the freeze commit; the fetcher's `pin` comes from the spec it
  read. **The two must be the same spec at the same rev** or `carrier_pin_ok` goes false.
* raw image (optional `--image-cache`): `<image-cache>/<image_sha256>.image`.

---

## 2. Privileged `mknod`? No — and the device nodes are not where you think

**The OUTER container never contains device nodes.** The FRITZ!Box `.image` is a plain
(uncompressed) tar whose members are regular files and directories only. Committed evidence:
`.ufo/waves/round-50/w1/C1CarrierSelect/receipts/tarlists/c6430.txt` and `c6490.txt` (21 and
19 lines) — `grep -E '^[bcps]'` on both returns **nothing**. The `/dev` entries live inside the
**SquashFS member**, one level down.

**Therefore the outer extraction cannot hit `mknod` at all**: `tar_member()` never writes to a
filesystem — it opens the tar over `io.BytesIO(image)` and reads one member's bytes into RAM
(`tf.extractfile(m).read()`). No node is created, privileged or not. There is **no flag to
pass**: no `-x`/`--no-same-owner`, no `--exclude`, nothing, because nothing is extracted to
disk. Verified: `chain-timing-probe` (a 30 MiB synthetic tar) left the cwd unchanged and wrote
only `<pin>.bin` into the cache dir.

**The device nodes appear at the next stage** (SquashFS extraction), and there the behaviour
is the crux of R52-C1's law. Measured on a synthetic LE `hsqs` image built with the lane's own
writer (`tools/round-41/sqfs-list.py:_build_image`), uid 1000, host `unsquashfs 4.7.5` and
`sasquatch 4.5.1` (the exact pinned tools):

* **char/block device → refused**: `create_inode: could not create character device
  …/dev/led, because you're not superuser!`; summary `created 0 devices`. The node is absent
  from the tree. (Matches the S250 source ground cited in the claims: unsquashfs 4.7.5 gates
  char/block `mknod` behind `if(root_process)`.)
* **fifo → created** (`created 1 fifo`), **socket → created** (`created 1 socket`). So the
  "no fifo/socket" half of the law is *not* observed on this host's extractor for a synthetic
  fifo/socket image. It does not affect the four carriers (census histograms below contain no
  fifo/socket row), so the corpus-exercised part of the law stands — but the **width statement
  ("the generalisation to fifo/socket rests on the source ground and the corpus does not yet
  exercise it") is exactly right, and my probe is direct evidence that the generalisation is
  not free.** Worth one line in the round-52 entry, not a rule change.
* `unsquashfs -lln` (listing only, no extraction) **does** print the device rows:
  `crw------- 0/0                 247,  0 … squashfs-root/dev/led`, `brw… 8, 0 …`,
  `prw-r--r-- …/dev/fifo`, `srw-r--r-- …/dev/sock`. **This is the only way to re-derive the
  char/block census** — the extraction tree does not contain those nodes.
  ⇒ **Consequence for the counter's `census_rederived_ok`:** the non-regular census must be
  re-derived from `unsquashfs -lln` (or the frozen pure-Python reader), **not** from an
  extraction tree; a tree-derived census silently loses every char-device row. Measured
  grammar to parse: `<type><perm> <uid/gid> <major>,  <minor> <date> squashfs-root/<path>`
  (note the comma+spaces between major and minor), plus `-> target` for symlinks and
  `prw-`/`srw-`/`crw-`/`brw-` for the special kinds.

---

## 3. What happens on a sha mismatch at each stage

Per-carrier failure is recorded in the receipt as `ok:false` + `link:<name>` (+ `detail` where
present); **the carrier's cache entry is not written** (fail-closed, `.part` → `os.replace`
only after every hash matched).

| stage | `link` value | `detail` | notes |
|---|---|---|---|
| spec incomplete (`url`/`image_sha256`/`member` missing, or pin ≠ 64 hex) | `spec` | `external lacks <keys> or the carrier pin` | line 196 |
| URL/host/scheme refused or network error | `url` | the exception text | line 203 |
| image sha mismatch | `image_sha256` | **none** (the got-value lives in `rec['image_sha256']`) | line 208 |
| tar member absent | `member` | `member '<x>' absent` | line 214 |
| `member_sha256` omitted | `member_sha256` | `spec omits member_sha256 (required since round 41)` | line 221 |
| member sha mismatch | `member_sha256` | `member <got>, want <want>` | line 225 |
| nested unreadable / not a regular file | `nested` | the reader's error | lines 234/240 |
| nested sha mismatch | `nested_sha256` | `<got> extracted, want <want>` | line 240 |
| `length` not an int / > member size | `length` | `length <x> outside the <n>-byte member` | line 247 |
| carve sha ≠ pin | `carrier_sha256` | `carve <got>, want <want>` | line 255 |

**Exit codes.** `run()` returns `0` iff *every* carrier is `ok`; otherwise `1`. `main()`
returns that value, so **exit 1 = at least one carrier failed, not "nothing happened"**.
Measured with the shipped selftest (16/16 green, exit 0) and per-case: `bad-url → rc 1
link=url`, `image-sha → rc 1 link=image_sha256`, `member-sha-mismatch → rc 1
link=member_sha256`, `member-sha-omitted → rc 1 link=member_sha256`, `member-absent → rc 1
link=member`, `nested-sha-mismatch → rc 1 link=nested_sha256`, `nested-path-absent → rc 1
link=nested`, `nested-path-is-symlink → rc 1 link=nested`, `pin-mismatch → rc 1
link=carrier_sha256`, `length-overrun → rc 1 link=length`, `spec-missing-image-sha → rc 1
link=spec`. **Every failing case wrote an empty cache** (`cache=` empty in all 13 failure
rows). Exit 2 only for usage errors and the lane-resident `--cache`/`--image-cache` refusal.

> **L1 hazard (measured, not inferred):** a run that fails one carrier still exits 1 *after
> materialising the other three* — the failure is per-carrier, the exit code is global. The
> data run must therefore assert **all four `<pin>.bin` present and each hashing to its own
> file name**, not just `exit == 0` of the fetcher and not just the fetcher's exit code.
> (Same class of check the round-50 receipt `11-materialised-cache-verified.json` performed.)

---

## 4. Disk and time budget for all four carriers

HEAD-only receipts (my own, `receipts/head-only.*`, `receipts/head-latency.*`): all four
`HTTP 200`, `content-type: application/octet-stream`, **no `Set-Cookie`**, ETag/Last-Modified
**identical to the pinned notes in `carriers.json`** (so the upstream bytes are unchanged
since round 50 — `66c33b99-1e87000`, `66c33c51-1ec3000`, `64f60ee7-25e6800`, `64f6f08b-223f800`).

| id | HEAD content-length | HEAD latency | carrier bytes written |
|---|---|---|---|
| g7581 | 32 010 240 (30.53 MiB) | 0.78 s | 28 368 210 |
| g7582 | 32 256 000 (30.76 MiB) | 0.80 s | 28 607 082 |
| c6490 | 39 741 440 (37.90 MiB) | 0.77 s | 28 200 029 |
| c6430 | 35 911 680 (34.25 MiB) | 0.71 s | 23 861 507 |
| **total** | **139 919 360 (133.44 MiB)** | 3.11 s | **109 036 828 (103.99 MiB)** |

* **Download traffic:** 133.44 MiB per full re-fetch (one image in RAM at a time; `MAX_IMAGE =
  64 << 20` = 67 108 864 B, all four images < 40 MB, so the cap never trips). If
  `--image-cache` is used, add another 133.44 MiB on disk.
* **Carrier cache:** 103.99 MiB (four `.bin`).
* **Extraction scratch:** the oracle arm writes a full tree per carrier — the frozen oracle
  tables sum to 371.5 MiB of regular-file bytes over the four carriers (c6430 74.0 / c6490
  89.5 / g7581 103.7 / g7582 104.3 MiB), and `c1-run.sh oracle` builds **two** trees per
  carrier (unsquashfs + sasquatch) ⇒ ≈ 743 MiB if all four ran concurrently; sequentially
  (one carrier at a time, scratch dir removed on exit) the peak is ≈ 210 MiB/carrier.
  The REA after-arm adds its own extraction tree (bounded by `--max-output-bytes
  536870912`, `--max-output-files 100000`).
* **Time:** measured REA after-arm durations from the committed round-50 receipts —
  c6430 8.3 s, g7581 12.7 s, c6490 20.3 s, g7582 21.9 s ⇒ **≈ 63 s for the four after-arms**
  (round-50, `rea_attempts:1` each; the round-52 policy allows up to 3 attempts on
  `provider_timeout` and 2 on the ENOENT class, so budget the worst case ≈ 3×).
  Download throughput: **[INFERENCE from the accidental run]** the block that performed three
  full four-carrier fetches completed in 69.93 s ⇒ roughly **20–25 s per complete four-carrier
  fetch (~5–6 MiB/s)**; treat as coarse, it was not measured in isolation.
* **Host headroom:** `disk-guard.sh status` → `/fast/scratch/hyaku` 46 % used, 434.8 G free;
  `/fast` 50 % used, 405 G free. Budget is comfortable.
* **Total quiet-window estimate for the L1:** fetch ≈ 25 s + four after-arms ≈ 63 s (worst
  case ≈ 190 s with the retry policy) + four oracle arms (two full trees each, the heaviest
  part) ⇒ order of minutes, not hours. Run the four carriers **sequentially** to bound scratch.

---

## 5. Does the fetcher write outside `--cache-dir`?

Measured and source-read:

| path | written? | notes |
|---|---|---|
| `--cache` | yes | `<pin>.bin` (+ transient `<pin>.bin.part` in the same dir) — the *only* carrier output |
| `--image-cache` | yes | `<image_sha256>.image`; the raw image is cached **only if its sha matched** (`fetch()` line 126), so a mismatching image is never persisted |
| `--json-out` | yes | wherever told — **not covered by the lane refusal**; measured: writing it inside the lane succeeds (my `jsonout-probe.json`). Point it at a deliberate path; it carries hashes/URLs only, no bytes |
| lane tree | **no** | `--cache`/`--image-cache` inside the lane ⇒ exit 2 (measured twice: `refusing: --cache is inside the lane …`, `refusing: --image-cache is inside the lane …`) |
| cwd / `TMPDIR` | no | the fetch path writes no temp file (image held in RAM); `selftest()` uses `tempfile.mkdtemp` under `TMPDIR` and removes it (`selftest` residue: none) |
| outside the lane | **allowed** | `--cache /home/vgpnk/Projects/shokunin/.scratch/…` and `--cache /tmp/…` were both **accepted** (the guard only tests "inside the lane"). This is exactly how my disclosure in §0 happened. ⇒ **the L1 must pass an explicit out-of-lane cache path and must not rely on the script to refuse `/tmp` or the fleet-root `.scratch/`.** |
| git | read-only | the only subprocess is `git show <rev>:tools/round-50/carriers.json` (line 92) |

---

## 6. Port notes for `tools/round-52/fetch-vendor.py` (the L1's copy)

1. **`CARRIERS = 'tools/round-50/carriers.json'` (line 63)** — the `--root/--rev` mode resolves
   the spec by that literal path. If the round-52 carrier table lands as
   `tools/round-52/carriers.json`, this constant must change, or `--root/--rev` silently loads
   the **round-50** table (whose `external` blocks are identical, so the fetch would still
   succeed but the counter would score the round-52 table's pins — a silent divergence).
2. **`SQFS_LIST` (lines 65-66)** resolves to `tools/round-41/sqfs-list.py` from
   `tools/round-52/` as well (dirname(dirname(file)) = `tools/`) — **no change needed**.
3. **The lane-refusal window** (lines 433-438) computes the lane as
   `dirname(dirname(__file__))/../..` = the lane root for a `tools/round-52/` copy — **still
   correct**. It does *not* refuse `/tmp` or the fleet-root `.scratch/` (§5).
4. **`nested` is dead** for these four carriers (§1) — the round-52 copy inherits that; the
   selftest must still cover it (the shipped 16 cases do).
5. **The routed defect 4 (network-guard selftests)** — measured guard behaviour of the shipped
   `fetch()` and `_AvmOnlyRedirect`, offline, no network:
   `file://…` → `ValueError: url outside https://download.avm.de: file:///etc/passwd`;
   `http://download.avm.de/…` → `ValueError` (scheme);
   `https://example.com/…` → `ValueError` (host);
   redirect to `https://evil.example/…` → `HTTPError: HTTP Error 302: redirect off
   download.avm.de refused`; redirect to `http://download.avm.de/…` (downgrade) → same
   refusal; redirect to `https://download.avm.de/…` → allowed (returns a Request);
   `https://download.avm.de/x.image` (nonexistent) → `HTTPError 404`. **The shipped 16-case
   selftest exercises none of these** (its `bad-url` case uses a *fake* fetcher, and
   `fetch()` is never called — `grep -n 'fetch(' tools/round-50/fetch-vendor.py` shows only
   the definition). The round-52 copy's offline guard selftest must call the real `fetch()`
   and the real redirect handler with fixture inputs and show **green with the guards present,
   red with a guard deleted** — the guard table above is the fixture list.
6. **An image larger than `MAX_IMAGE`** surfaces as `link='url'` with detail
   `image over 67108864 bytes` (the `ValueError` is raised inside `fetch()` and caught by
   `materialise()`'s blanket `except Exception` at line 202) — i.e. an oversize image is
   reported as a *link* failure, not a distinct code. Not a problem for these four (max 37.9 MiB);
   worth a line in the copy's docstring.

---

## 7. Findings the L1 should weigh before the freeze

1. **`carrier_fresh_ok` is the trap in the re-measure.** The claims put
   `tools/round-50/carriers.json` into the v2 counter's `PRIOR_CARRIER_TABLES` and list the
   four pins in the round-52 table's `prior_pins` — both make the four pins *prior*, so
   `c1-counter.py:2250` (`carrier_fresh_ok = pin not in prior`) would be **false for all four**
   unless the frozen `re_scored_pins` allow-list waiver is implemented in the v2 counter. The
   round-50 counter has **no** such waiver field; the port must add it (and the receipt must
   name the allow-list, per the claim). Missing it ⇒ `carriers_matched 0` ⇒ claim missed as
   frozen.
2. **Census re-derivation must use `unsquashfs -lln`, not an extraction tree** (§2): an
   unprivileged tree contains **no** char/block device nodes, so a tree-derived census is
   short by exactly the rows the law is about (13 for g7581/g7582, 1 for c6430/c6490).
   The `-lln` grammar (major`,`minor with comma+spaces) is in §2.
3. **Per-carrier fetch failure is not a run failure.** Assert four `<pin>.bin` files, each
   hashing to its own name (§3), not the fetcher's exit code.
4. **Fetch spec rev must equal the counter's freeze rev** (§1, join point) — `--rev <FREEZE>`,
   not a different rev.
5. **The fifo/socket generalisation is not free** (§2): measured, this host's extractor *does*
   create fifos and sockets while refusing char/block devices. The corpus never exercises it
   (histograms: dir/symlink/char-device only). The claims' F5 width statement is accurate;
   consider one sentence in the round-52 entry recording the measurement.
6. **Path guards:** `--json-out` and any out-of-lane `--cache` are unguarded (§5). The L1
   should pass explicit `/fast/scratch/hyaku/kaidoku-r52/…` paths and never `/tmp` or the
   fleet-root `.scratch/`.

## Receipts (all under `receipts/` in this seat dir)

| file | command | exit | note |
|---|---|---|---|
| `head-only.*` | `python3 -I head.py` | 0 | HEAD-only on the four pinned URLs; Content-Length/ETag/Last-Modified; `Set-Cookie` absent |
| `head-latency.*` | `python3 -I headtime.py` | 0 | per-URL HEAD latency 0.70–0.80 s |
| `fetch-selftest.*` | `python3 -I -B tools/round-50/fetch-vendor.py --selftest` | 0 | `SELFTEST cases=16 pass=16 fail=0`; stdout sha256 `828a9add…8ec` |
| `guard-probe.*` | `python3 -I guardprobe.py` | 0 | offline scheme/host/redirect guard table (§6.5) |
| `device-extract-probe.*` | `python3 -I devprobe.py` | 0 | synthetic LE image: unsquashfs + sasquatch refuse char devices, `created 0 devices` |
| `fifo-socket-probe.*` | `python3 -I fifo_probe.py` | 0 | synthetic fifo/socket: **created 1 fifo, 1 socket**, device refused |
| `kinds-listing-probe.*` | `python3 -I kindsprobe.py` | 0 | `unsquashfs -lln` grammar for char/block/fifo/socket + reader `--nonregular` rows |
| `chain-timing-probe.*` | `python3 -I timeprobe.py` | 0 | 30 MiB synthetic tar → `<pin>.bin` only, cwd unchanged, no `.part` residue, 0.46 s |
| `lane-cache-refusal.*` | `fetch-vendor.py --cache <inside lane>` | 2 | `refusing: --cache is inside the lane (vendor bytes are never committed)` |

Scratch `/fast/scratch/hyaku/kaidoku-r52/w1-ScoutCarrierChain` removed after copying these
receipts; no vendor byte remains anywhere.
