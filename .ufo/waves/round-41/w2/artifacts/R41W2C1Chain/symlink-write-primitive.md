# Confirmed: vendor bytes land wherever a planted cache symlink points (R41W2C1Chain)

`fetch-vendor.py` at tip writes the carrier through `open(out + '.part', 'wb')`
(fetch-vendor.py:241) and the image through `open(os.path.join(image_cache, want + '.image'),
'wb')` (line 108). Both follow symlinks. Demonstrated against the real pinned bytes.

## A — carrier cache

```
mkdir -p $S/sym/cache
printf 'PRECIOUS-USER-FILE\n' > $S/sym/target.txt
ln -s ../target.txt "$S/sym/cache/c4f74f54a65e861e…f872a.bin.part"     # V3 pin
python3 -I -B <LANE>/tools/round-41/fetch-vendor.py \
  --spec $S/adv/spec-base.json --cache $S/sym/cache        # EXIT=0
```

Result:

```
-rw-r--r-- 30233394 $S/sym/target.txt     # was 18 bytes; sha256 c4f74f54…f872a (V3 carrier)
lrwxrwxrwx c4f74f54….bin -> ../target.txt  # the cache entry is now a symlink to it
```

So one fetch (a) overwrote a file of the caller's choosing with 30 233 394 bytes of AVM
firmware, and (b) left `<pin>.bin` as a symlink to that file — which the counter then reads
(fetch-vendor/c1-counter only re-hash, so the score is unaffected, but the cache no longer
holds an independent copy).

## B — image cache

```
ln -s ../target2.txt "$S/sym2/imgcache/770efb4e…5ab7.image"
python3 -I -B …/fetch-vendor.py --spec … --cache $S/sym2/cache --image-cache $S/sym2/imgcache
# EXIT=0, fetch="read": the symlink target was read (hash mismatch), the image was fetched
# and then written back THROUGH the symlink
-rw-r--r-- 33269760 $S/sym2/target2.txt   # sha256 770efb4e…5ab7, the vendor image
```

## Impact, and the licence link

* Arbitrary-file overwrite with the acting user's privileges (any writable path: a shell
  rc file, the lane's frozen tools, another seat's artifact).
* The overwritten path is a *carrier-cache or image-cache-shaped name*, so a poisoned cache
  directory (a pre-populated scratch dir, a shared `/fast/scratch` tree, a copied cache) is
  enough; no network or repo write access is needed beyond the fetch itself.
* Licence consequence: the write target can be inside the lane worktree, which turns a
  routine `fetch-vendor.py` run into "30 MB of AVM firmware in a tracked path", i.e. the
  redistribution the frozen table forbids. Nothing in the counter would flag it (see
  `blob-and-licence-scan.md` §5).
* Round-41 wave-1 `R41C1Sentinel` F7 described exactly this; it is unchanged at tip
  (`--cache`/`--image-cache` write side).

## Smallest remediation

```python
fd = os.open(out + '.part', os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW, 0o600)
with os.fdopen(fd, 'wb') as fh:
    fh.write(body)
```
(same for the image-cache write), or refuse when `os.path.islink(path)` for `.part`,
`<pin>.bin` and the image file. `os.replace` itself is safe (it renames over the link).
