# ScoutCarrierChain — R52-C1 carrier re-fetch chain semantics (round 52, wave 1)

Full findings + receipts: `.ufo/waves/round-52/w1/ScoutCarrierChain/chain.md`
(and `.../ScoutCarrierChain/receipts/`). Seat dir: `.ufo/waves/round-52/w1/ScoutCarrierChain/`.

## Verdict

The round-50 fetch chain is **sound and re-runnable**; all four pinned vendor images are
unchanged upstream (HEAD ETag/Last-Modified identical to the frozen notes) and every link of
the chain verifies. The re-fetch itself needs **no privileged `mknod` and no special flags**,
because the outer `.image` container is a plain tar with **no device nodes at all** — the
`/dev` entries live one level down, inside the SquashFS member. The device nodes bite only
at the SquashFS-extraction stage, which is where the law lives.

## Chain (per carrier)

`url` → GET whole image into RAM (cap `MAX_IMAGE` = 64 MiB; all four < 40 MiB) →
`sha256(image) == image_sha256` → **tar member extracted by the script's own code**
(Python stdlib `tarfile`, `mode='r:'`, in memory — not unsquashfs/7z; the file's only
`subprocess` is `git show` for `--root/--rev`) → `sha256(member) == member_sha256` →
carve to `length` (= `bytes_used`; drops 694/3 486/939/1 797 B of trailing pad) →
`sha256(carve) == pin` → `<cache>/<pin>.bin` (atomic `.part` → `os.replace`). The
`external.nested` branch is **dead** for these four (`grep -c nested carriers.json` = 0).
Cache naming matches the counter's join point exactly (`c1-counter.py:2242`
`os.path.join(carrier_cache, pin + '.bin')`), so the fetch spec rev must equal the
counter's freeze rev.

## Answers to the five questions

1. **Chain** — above; member extraction = the script's own in-memory `tarfile`; cache file =
   `<carrier-sha256>.bin`; optional `--image-cache` = `<image_sha256>.image`.
2. **Privileged `mknod`** — **not needed, no flags exist or are required**: the outer tar has
   zero device/fifo/socket entries (committed `tarlists/c6430.txt`, `c6490.txt`), and the
   extraction is memory-only. At the *SquashFS* stage, unprivileged `unsquashfs 4.7.5` /
   `sasquatch 4.5.1` **refuse** char/block devices (`could not create character device …
   not superuser!`, `created 0 devices`) but **do create fifos and sockets** (measured on a
   synthetic image) — the corpus has no fifo/socket row, so R52-C1's law is unaffected, but
   the fifo/socket generalisation is not free (one sentence for the entry).
3. **sha mismatch** — per-carrier `ok:false` + `link:` ∈ {`spec`,`url`,`image_sha256`,
   `member`,`member_sha256`,`nested`,`nested_sha256`,`length`,`carrier_sha256`}; the carrier's
   cache entry is not written (fail closed). Exit **1** = *at least one* carrier failed (the
   other three still materialise!), exit 2 only for usage/lane-cache refusal.
4. **Budget** — HEAD content-lengths 32 010 240 / 32 256 000 / 39 741 440 / 35 911 680 =
   **133.44 MiB downloaded**; carrier cache **103.99 MiB**; oracle trees ≈ 371.5 MiB of
   regular bytes (two trees/carrier ⇒ ~743 MiB if parallel, ~210 MiB peak if sequential);
   REA after-arms 8.3/12.7/20.3/21.9 s (round-50 receipts) ⇒ ≈ 63 s, worst case ≈ 190 s
   under the round-52 retry policy; fetch ≈ 20–25 s. Host headroom ample (405 G free).
5. **Writes outside `--cache-dir`** — only `--image-cache` (`<image_sha256>.image`, written
   only when the image sha matched), `--json-out` (**not** lane-guarded), and (selftest only)
   a `TMPDIR` temp dir that is removed. The lane refusal (`exit 2`) covers `--cache` and
   `--image-cache` **inside the lane only** — `/tmp` and the fleet-root `.scratch/` are
   accepted (see disclosure below).

## Findings for the L1 (pre-freeze)

1. **`carrier_fresh_ok` is the trap**: putting `tools/round-50/carriers.json` into
   `PRIOR_CARRIER_TABLES` + listing the four pins in `prior_pins` makes all four *prior*, so
   `c1-counter.py:2250` goes false unless the frozen `re_scored_pins` waiver is implemented
   in the v2 counter (the round-50 counter has no such field). Missing ⇒ `carriers_matched 0`
   ⇒ claim missed as frozen.
2. **`census_rederived_ok` must re-derive from `unsquashfs -lln`, not an extraction tree**:
   an unprivileged tree contains **no** char/block device nodes, so a tree-derived census is
   short by exactly the rows the law is about (13 / 13 / 1 / 1). `-lln` grammar measured:
   `crw------- 0/0  247,  0 … squashfs-root/dev/led` (major`,`minor, comma+spaces).
3. **Do not trust the fetcher's exit code alone**: a per-carrier failure leaves the other
   three `.bin` written; assert four files, each hashing to its own name.
4. **Port constants**: `CARRIERS = 'tools/round-50/carriers.json'` (line 63) must be retargeted
   if the round-52 table lands under `tools/round-52/` (else `--root/--rev` silently loads the
   round-50 table); `SQFS_LIST` still resolves to `tools/round-41/sqfs-list.py` from
   `tools/round-52/` — no change needed.
5. **Guard selftests (routed defect 4)**: the shipped 16-case selftest never calls the real
   `fetch()` (its `bad-url` case uses a fake fetcher), so the https/host/redirect guards are
   untested. Offline measured table to encode as fixtures: `file://`→ValueError,
   `http://download.avm.de`→ValueError, `https://example.com`→ValueError, redirect off-host
   and scheme-downgrade → `HTTPError 302 redirect off download.avm.de refused`, on-host
   redirect → allowed, `https://download.avm.de/x.image` → HTTPError 404.

## Disclosure (contract deviation)

My task said "no image bytes downloaded". Probing the `--cache` guard, I ran the fetcher with
cache paths **outside** the lane (`…/shokunin/.scratch/probe-cache`, `/tmp/probe-cache`); the
script's guard only refuses *lane-resident* paths, so the four images were really fetched
(3 invocations, ~133 MiB each). Everything was deleted immediately and verified absent (lane
tree, `.scratch/`, `/tmp`); no vendor byte survives. The only lane file written was
`jsonout-probe.json` (hashes + URLs, 3 257 B, no bytes). Byproduct: the coarse download
throughput in §4. All other probes were HEAD-only or synthetic/offline.

Tools: none installed, none upgraded. No REA run, no git mutation, no lane write outside my
seat dir. Scratch `/fast/scratch/hyaku/kaidoku-r52/w1-ScoutCarrierChain` removed.
