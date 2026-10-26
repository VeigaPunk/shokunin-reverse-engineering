# Vendor chain rebuild at tip 7a24ff74 (R41W2C1Chain)

Ran 2026-10-26 18:20 local. Vendor bytes are NOT in this directory or in the lane
(AVM licence); only digests and the fetcher's own JSON record are reproduced here.

```
S=/fast/scratch/hyaku/kaidoku-r41/R41W2C1Chain
cd $S
python3 -I -B <LANE>/tools/round-41/fetch-vendor.py \
  --root <LANE> --rev d764389e9cbe61b9d1b07538ff3bff02d50bb34f \
  --cache $S/cache --image-cache $S/imgcache --json-out $S/fetch-real.json
# EXIT=0, 9.4 s wall (two HTTPS downloads, 33,269,760 + 36,392,960 B)
```

Chain links as measured (record: `fetch-real.json`):

| carrier | image sha256 | image bytes | member sha256 | member bytes | nested sha256 | nested bytes | carve (= pin) | carve bytes |
|---|---|---|---|---|---|---|---|---|
| V3 | `770efb4e…50ab7` | 33 269 760 | `87cc5d6b…ea0f8` | 30 236 680 | — | — | `c4f74f54…f872a` | 30 233 394 |
| V4 | `a5a3a763…5f661` | 36 392 960 | `4cfc3016…92f6c` | 33 361 928 | `4d5de25c…d947` | 32 722 944 | `ce27ebca…087f` | 32 720 860 |

Independent re-checks of the produced cache files (`sha256sum`, superblock decoded by hand):

```
c4f74f54a65e861e22f5d6a47977cdbb3b5345819174f33bc86c63d3d10f872a  cache/c4f74f54….bin
ce27ebca903a1574465ddfa0626943339ce6bc8155f31f88d04049afb570087f  cache/ce27ebca….bin
V3: size 30233394 magic sqsh 4.0 mkfs_time 30233394 bytes_used 30233394 compression 4 (xz)
V4: size 32720860 magic sqsh 4.0 mkfs_time 32720860 bytes_used 32720860 compression 4 (xz)
```

So `size == bytes_used == mkfs_time` for both: carve length equals `bytes_used` exactly, and
the AVM marker is present. The V4 nested file is 2 084 B longer than its own `bytes_used`
(32 722 944 → 32 720 860): the fetcher drops the tail, and the pin is taken over the carved
slice, which is what the frozen table states.

`carriers.json` declares `length` 30233394 (V3) and 32720860 (V4); both equal the measured
`bytes_used`. The counter's `carve_ok` additionally requires `length == bytes_used == size`
and is true for both in the score receipt (`l1/scores/c1-at-e9a24d07.json`).

HTTP: both URLs return 200 (`Content-Length` 33269760 / 36392960) and hash to the frozen
image pins today, so the vendor URL still serves the pinned bytes.

Fetcher selftest (same binary, `--selftest`): 16/16 pass, exit 0 —
`selftest-fetch-vendor.txt` in this directory.
