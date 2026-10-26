# Cache poisoning at read time: detected, twice (R41W2C1Chain)

Both scored tools re-hash a cache entry instead of trusting its name:

* `c1-counter.py:1534-1538` — reads `--carrier-cache/<pin>.bin`, then
  `carrier_pin_ok = sha256(raw) == pin` (clause list `CLAUSES`, line 321-326);
* `c1-extra.py:85-92` — same shape (`carrier bytes absent or pin mismatch`).

## Probe

Poison: copy the real cache, flip one byte at offset 1000 of the V3 entry (same length, so
`bytes_used`/size still parse), and delete the V4 entry. Then call the frozen counter's
`measure()` with a stub `rerun` (so no REA run is needed for this probe) and the poisoned
cache:

```
HYAKU_SCRATCH=$S/hy python3 poison_test.py       # poison_test.py in this directory
```

| carrier | carrier_present | carrier_pin_ok | carve_ok | projection | matched |
|---|---|---|---|---|---|
| V3 (1 byte flipped) | true | **false** | true | skipped (`carrier_pin_ok`) | false |
| V4 (entry absent) | **false** | false | false | skipped | false |
| L3 (untouched) | true | true | true | stub error | false |
| L4 (untouched) | true | true | true | stub error | false |

`carriers_matched 0`, `met_target False` (full record: `poison-result.json`).

Notes for calibration:

* a one-byte flip leaves `carve_ok` true (superblock fields intact), so the pin is the only
  gate that catches it — and it does;
* the receipt-derived clauses (`oracle_hits_ok`, `evidence_id_ok`) stay true under poisoning,
  i.e. the score cannot be moved by cache tampering, only blocked;
* `raw = open(fp, 'rb').read()` has no size cap and follows symlinks: a planted
  `<pin>.bin` symlink to `/dev/zero` would OOM the counter before hashing (self-inflicted;
  same unbounded-read class as `fetch-vendor` image reads).
