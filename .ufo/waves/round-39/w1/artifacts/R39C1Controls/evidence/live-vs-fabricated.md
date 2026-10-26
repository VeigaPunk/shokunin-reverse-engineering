# Live REA vs fabricated receipt on a development carrier (no K5/K6, no K1-K4 REA run)

Everything below ran in scratch (`/fast/scratch/hyaku/kaidoku-r39/R39C1Controls/dev`)
on a big-endian v4 carrier built from a fresh tree with the lane generator. No
held-out carrier was built or run, and REA was never pointed at K5 or K6.

## Carrier

```
mkdir -p dev/tree/sub
printf 'hello be\n' > dev/tree/hello.txt
printf 'inner\n'    > dev/tree/sub/inner.txt
ln -s sub/inner.txt   dev/tree/link-in      # resolves in-tree
ln -s ../../etc/passwd dev/tree/link-out    # escapes the image root
python3 tools/round-37/gen-squashfs.py dev/tree dev/carrier.sqsh --endian be --comp gzip
# wrote carrier.sqsh 442 bytes, inodes 6
# sha256 b916a13a558de59ae5d53e28f070c6715337e584f872de5de8b5b11ef75c9fd6
```

## Run 1 (live)

```
cd dev && REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob \
  npx -y rea-agents@6.5.0 extract-firmware --format json --full-output carrier.sqsh out-live
# exit 0
```

`data.normalized_result`:

- chunks: `squashfs_v4_be`, `extraction_failed: false`
- files: `firmware.bin_extract/hello.txt`, `firmware.bin_extract/sub/inner.txt` (both oracle sha256)
- extraction_gaps: `[('unpublished-entry','firmware.bin_extract/link-in')]`
- unpublished_entries: `link-in -> sub/inner.txt`
- diagnostics: `MaliciousSymlinkRemoved` for `link-out`; **no gap** for the escaping link
- evidence_id `ev_c679df68797ccf91ef60d84d1203defc3aed66739bd56621cd18ffddc33bc184`

This is the round-38 rule reproduced on a fresh carrier: in-tree → one
`unpublished-entry` gap, escaping → removed and no gap.

## Run 2 (live, different outdir)

Same command into `out-live2`; exit 0. Normalized predicate fields identical to
run 1; evidence id `ev_4a6ad7428643a0365...` — **different**, because
`parameters.output_directory` and `raw_result.report[].task.path` and the
per-run provider blob ids differ. Two genuine runs never share an evidence id.

## Fabricated receipt

```
python3 _harness/fabricate_receipts.py \
  --carriers dev/carriers.json --lane-root dev --mode forge-remint \
  --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
  --out dev/fab --outdir-base dev/ctl-out
# no REA process, no unblob, no sasquatch
```

Comparison with the live run on the fields P39-C1 names:

```
fabricated == live on the predicate fields: True
fabricated id ev_154c5cdfd8b4ef776...   live id ev_c679df68797ccf91e...
```

## What this proves

1. A receipt that was never produced by REA can be made byte-consistent with a
   real run on every field the drafted predicate checks (handler, no failed
   chunk, oracle paths + sha256, gap kind + path set). CTL-C1-3 is therefore not
   an implementation bug in a sloppy counter; it is the predicate's evidence
   basis.
2. Comparing a committed receipt to a fresh live run on those same fields does
   **not** refuse CTL-C1-3 either (both say the same true thing).
3. Evidence ids are per-run and cannot be compared across runs; a live-run
   binding must compare only `normalized_result` fields, never the id or
   `raw_result`.
4. The only way a counter refuses CTL-C1-3 is to stop treating the committed
   JSON as the evidence: the counter runs `extract-firmware` itself (fresh
   outdir, `sasquatch-v4be` reachable) and scores from **its own envelope**.
   Then fabrication is irrelevant because the measurement happened; the
   committed receipt becomes an optional cross-check on the normalized fields.

## Reproduction files

`dev-live-envelope.json`, `dev-live-envelope-run2.json`, `dev-oracle.tsv`,
`dev-symlinks.tsv`, `dev-carriers.json`, `dev-fabricated-after.json` in this
directory were copied from that scratch run.
