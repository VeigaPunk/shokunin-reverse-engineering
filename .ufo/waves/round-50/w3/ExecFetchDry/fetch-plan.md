# R50-C1 fetch plan — the exact commands the L1 runs

Seat `ExecFetchDry` (round 50, attempt 2, wave 3). Draft input for the L1.
All paths absolute. Nothing here is executed by the seat beyond the offline
selftest, the HTTP HEADs and the containment tests recorded in
`receipts/*.json` (no image bytes were downloaded; no REA run).

---

## 0. Variables

```bash
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
FREEZE=435d41fd4ad9211d1579fc447936fb33d2b74467      # the committed C1/C2 freeze
CACHE=/fast/scratch/hyaku/kaidoku-r50/carrier-cache    # <pin>.bin  (carrier bytes)
IMAGES=/fast/scratch/hyaku/kaidoku-r50/image-cache    # <image_sha256>.image (raw .image)
WORK=/fast/scratch/hyaku/kaidoku-r50/counter           # the counter's own scratch
PKG65=/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents
mkdir -p "$CACHE" "$IMAGES" "$WORK"
```

`$CACHE` and `$IMAGES` must be **outside** the lane: `fetch-vendor.py` refuses a
lane-resident `--cache` / `--image-cache` with exit 2 (measured, receipt
`03-cache-inside-lane-refused.json`, `04-image-cache-inside-lane-refused.json`).
`$WORK` must be under `/fast/scratch/hyaku/kaidoku-r50/` — the counter hashes the
run's `parameters.output_directory` into the evidence id and requires that prefix
(`PROV_BASE`).

---

## 1. Materialise all four carriers (the fetch)

```bash
cd "$LANE"
python3 -I -B tools/round-50/fetch-vendor.py \
    --root  "$LANE" \
    --rev   "$FREEZE" \
    --cache "$CACHE" \
    --image-cache "$IMAGES" \
    --json-out "$IMAGES/fetch-vendor.json"
```

* **exit 0** = all four chains verified; four `<pin>.bin` written.
* **exit 1** = a chain link failed (the JSON names the failing `link`:
  `spec` | `url` | `image_sha256` | `member` | `member_sha256` | `nested` |
  `nested_sha256` | `length` | `carrier_sha256`). Nothing is written for that
  carrier — fail closed.
* **exit 2** = usage / unreadable spec / lane-resident cache.

### Why `--rev "$FREEZE"` and not something else

`fetch-vendor.py --root R --rev V` resolves its spec as
`git -C R show V:tools/round-50/carriers.json` (`load_spec`, fetch-vendor.py:97-104).
The **counter** resolves the very same table at the **freeze** commit
(`frozen = show(root, freeze, CARRIERS)`, c1-counter.py:2165) and checks the
fetched bytes against *those* frozen pins (`carrier_pin_ok`, c1-counter.py:2251).
So the fetch's `--rev` must be a commit whose `carriers.json` carries the **same
pins as the freeze's**; the freeze commit is the immutable anchor and is the
precedent (round 40/41 counted with `--root <LANE> --rev <FREEZE> --cache <CACHE>`).

Measured: the blob id of `tools/round-50/carriers.json` is
`1bdc1a90f7deb2c6fae7bdde483d87fe96985b8c` at **435d41fd (freeze)**,
**f890bbea (attempt-2 base)** and **6f4aba63 (HEAD)** — identical, so any of the
three works today; `$FREEZE` is the correct choice (receipt
`08-carriers-blob-across-revs.json`). A rev without the file → `SystemExit(2)`
(measured in-process).

### Expected cache contents (four files, names are the frozen carrier `sha256`)

| id | `<pin>.bin` | bytes (= `length` = `bytes_used`) | tar member bytes | pad dropped |
|---|---|---|---|---|
| g7581 | `968d997d5401a483a9250ab0e4e34bd632a40bee000af3419a2b8d0e29fa6845.bin` | 28 368 210 | 28 368 904 | 694 |
| g7582 | `a119b64428e7128e376317472c504605f17f81a2b802439e32194431d94a5bd0.bin` | 28 607 082 | 28 610 568 | 3 486 |
| c6490 | `880370e7f7e15d70b165a96ae3e6efef0cb8dc3e9a6b27b0b925c7fa62caf2d7.bin` | 28 200 029 | 28 200 968 | 939 |
| c6430 | `da1c804940f49fcfb3727efbd4f79a4788f86c5819ddda23b5a8221fb898b46f.bin` | 23 861 507 | 23 863 304 | 1 797 |

Total cache 109 036 828 B (104.0 MiB). Verify after the fetch:

```bash
sha256sum "$CACHE"/*.bin          # each must equal its own file name
ls -l "$CACHE"                     # sizes must equal the table above
```

**The carve must be exact.** `carve_ok` (c1-counter.py:2258-2264) demands
`external.length == bytes_used == len(file)`; a carrier with trailing bytes moves
the oracle root one `<start>-<end>.squashfs_v4_le_extract` level deeper and the
run scores red. `fetch-vendor.py` already carves to `length`, and the frozen
table's `length` equals the superblock `bytes_used` for all four, so the file
size is the check.

### Download volume (HTTP HEAD `Content-Length`, no bytes downloaded)

| id | Content-Length | MiB | ETag | Last-Modified |
|---|---|---|---|---|
| g7581 | 32 010 240 | 30.54 | `"66c33b99-1e87000"` | Mon, 19 Aug 2024 12:33:29 GMT |
| g7582 | 32 256 000 | 30.77 | `"66c33c51-1ec3000"` | Mon, 19 Aug 2024 12:36:33 GMT |
| c6490 | 39 741 440 | 37.91 | `"64f60ee7-25e6800"` | Mon, 04 Sep 2023 17:07:51 GMT |
| c6430 | 35 911 680 | 34.25 | `"64f6f08b-223f800"` | Tue, 05 Sep 2023 09:10:35 GMT |

Total **139 919 360 B (133.4 MiB)** of images; with `--image-cache` the peak on
disk is 133.4 + 104.0 ≈ **237.4 MiB**. All four are under the fetcher's
`MAX_IMAGE = 64 MiB` cap. Peak RSS of one fetch ≈ 97 MB (image + tar member +
carve, all in memory). The HEAD ETags/Last-Modified match the `notes` block of
the frozen `carriers.json` exactly, i.e. the vendor origin still serves the
pinned images; the `image_sha256` check is the authority, not the ETag.

**Recommendation:** pass `--image-cache "$IMAGES"`. A retry after a broken link
then re-uses the already-downloaded image (`fetch()` returns `'cache'`) instead of
re-pulling 133 MiB. The image cache is keyed by `image_sha256`, so a changed
image can never be served from it.

### When to run it

The fetch is network + sha256 only — no REA, no CPU-bound extraction. Run it
**before** the quiet window, so the window is spent on REA alone.

---

## 2. Data run (L1 only, in the quiet window)

One carrier at a time, per carrier id and pin:

```bash
cd "$LANE"
for id in g7581 g7582 c6490 c6430; do
  pin=$(python3 -c "import json;print([c['sha256'] for c in json.load(open('tools/round-50/carriers.json'))['carriers'] if c['id']=='$id'][0])")
  tools/round-50/c1-run.sh after --id "$id" --carrier "$CACHE/$pin.bin" --pin "$pin" --data-run
done
```

`c1-run.sh after` refuses without `--data-run`; the default `--outdir` is
`corpus/evidence/round-50/c1/<id>` and the default scratch base is
`${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kaidoku-r50` (which satisfies the
`/fast/scratch/hyaku/kaidoku-r50/` prefix the counter demands). Exit 0 = ok,
2 = usage/environment/precondition, 3 = tool failure.

---

## 3. Scoring (L1 only, after the landing)

```bash
cd "$LANE"
python3 -I -B tools/round-50/c1-counter.py \
    --root "$LANE" --rev <FINAL_REV> --freeze "$FREEZE" --pkg65 "$PKG65" \
    --work "$WORK" --carrier-cache "$CACHE" \
    --json-out /fast/scratch/hyaku/kaidoku-r50/scores/c1-final.json
```

* `--rev` must be a rev that **descends from the freeze** and first-adds the
  `after.json` receipts **after** it — i.e. the landing rev.
* `--carrier-cache "$CACHE"` is what makes `carrier_present` true: the counter
  looks up `os.path.join(carrier_cache, pin + '.bin')` where
  `pin = (c.get('sha256') or '').lower()` (c1-counter.py:2231, 2242) — the
  **carrier's frozen `sha256` field, lowercased**, exactly the file name
  `fetch-vendor.py` writes (`out = os.path.join(cache, pin + '.bin')`,
  fetch-vendor.py:266). The two agree by construction; no mapping table needed.
* Without `--carrier-cache` the counter scores `carrier_present` false → exit 1.
* **`--rev` must not be after the C3 instrument lands under `tools/round-50/`** —
  see the report's blocker finding. `frozen_drift` (c1-counter.py:1661-1720)
  treats *any* file added under `tools/round-50/` after the freeze as drift and
  the counter exits **2 (could-not-evaluate, `reason: frozen_path_changed`)**.

### C2 consistency at the final rev

```bash
python3 -I -B tools/round-50/c2-record.py --rev <FINAL_REV> --freeze "$FREEZE" \
    --work "$WORK" --json-out /fast/scratch/hyaku/kaidoku-r50/scores/c2-final.json
```

`c2-record.py` freezes the whole `tools/round-50` tree
(`FROZEN = ('tools/round-50', 'plans/round-50-claims.md')`, c2-record.py:123) and
compares it at FREEZE and REV (`freeze_check`, c2-record.py:1055-1069) — the
same trap as C1.

---

## 4. What the fetch does NOT verify (read this before trusting a green fetch)

`fetch-vendor.py` verifies **hashes only**. It does **not** check the
superblock: `hsqs` / v4.0 / xz / `mkfs_time == bytes_used` (the AVM marker) is
checked by the counter's `layout_probe` (c1-counter.py:992) on the *fetched*
bytes, and by `c1-run.sh oracle` before the data run. A green fetch therefore
does not imply `layout_ok`; a red `layout_ok` after a green fetch means the
member is not the image the table claims.
