# Adversarial spec runs against the real image bytes (R41W2C1Chain)

Every run used the frozen `carriers.json` at d764389e with the two URLs rewritten to
`file://…/imgcache/<image sha>.image` (the bytes already downloaded and hash-verified above),
so no run depends on the network and each failure isolates one link. One carrier per run.
Each run got a **fresh cache directory** plus a parent directory; after the run both were
listed to prove nothing was written.

| variant | mutation | exit | link | cache dir | files written outside cache |
|---|---|---|---|---|---|
| badmember | `member_sha256` = `1111…` | 1 | `member_sha256` | not created | none |
| badnested | `nested.sha256` = `2222…` | 1 | `nested_sha256` | not created | none |
| traversalpin | carrier pin = `../../aaaa…` (64 chars) | 1 | `carrier_sha256` | not created | none |
| badimage | `image_sha256` = `3333…` | 1 | `image_sha256` | not created | none |
| shortlen | V4 `length` = 32720859 (−1) | **0** | none | `ce27ebca….bin` written | none |

Commands (one per variant; `<v>` in the table):

```
python3 -I -B <LANE>/tools/round-41/fetch-vendor.py \
  --spec $S/adv/spec-<v>.json --cache $S/adv/cache-<v>
```

Specs are kept in `adversarial/` (hashes and URLs only; no bytes).

## What the table shows

1. **Fail-closed, before any write.** `member_sha256` (R40-CL6), `nested.sha256`,
   `image_sha256` and the final carrier pin each stop the run with exit 1, and in every case
   the cache directory was not even created — so `<pin>.bin` and `<pin>.bin.part` cannot
   exist after a broken link. The pin is compared to `sha256(carve)` before
   `os.makedirs(cache)` (`materialise`, fetch-vendor.py:235-243 at tip: pin compare 235,
   `makedirs` 239, `open(out + '.part')` 241, `os.replace` 243).
2. **Non-hex pin cannot traverse.** The pin is used as a filename component
   (`os.path.join(cache, pin + '.bin')`), but the write is after `carrier_sha256 != pin`,
   and a sha256 hexdigest can never equal a string containing `/`. The traversal spec fails
   at `carrier_sha256` and writes nothing.
3. **`length` is not enforced on the nested branch.** V4 declares `length` 32720860; the
   `nested` branch replaces it with the reader's `bytes_used` (`materialise`: `length =
   len(body)` after `body[:used]`), so a spec one byte short still materialises rc=0 and
   records `bytes: 32720860` — the declared value is never compared in the fetcher. The
   counter's `carve_ok` (`length == bytes_used == size`) does catch it at score time, so the
   claim is unaffected; the fetcher alone is not a check on the declared length.
