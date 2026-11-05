# fs2 — ExecFreshSource measurement detail (S321 second fresh source)

Full narrative: `.ufo/waves/round-96/w1/ExecFreshSource.md`. This file holds the raw
command lines, exit codes and digests; receipts `fs2-repro.json` / `fs2-head-repro.json`
sit alongside this file.

Clone HEAD `3baac2ef4b9b2830d299125b8184ca06d9e6584d`; scratch `/fast/scratch/hyaku/kaidoku-r96/ExecFreshSource/` (removed).

```
sha256sum /usr/bin/printf /usr/bin/env /usr/bin/head
b2265abe04a2c237be085f12c14d3c70969f34ab3370a56f399727e4b38374d7  /usr/bin/printf
a9ba02dcad338ee7f0b03e58a1cf44009b2bd645b09c2b423242e9791d202301  /usr/bin/env
313bf1f0c296d63fa9534394e22a502cfe29d9fe9e110c5b45f3c070b9ddf3e1  /usr/bin/head
file: all three ELF 64-bit LSB pie x86-64, stripped

python3 -I -B clone/tools/round-96/fresh-source2-check.py --root clone --work $S/fs2 --rev 3baac2ef4b9b2830d299125b8184ca06d9e6584d --json-out fs2-repro.json
exit=0  "fresh-source2 repaired 2 of 2; far-refused 2 of 2; intact 1 of 1 met True exit 0"
packed_sha256=95f2beb30d459f3080a542d29430e91f8b55664efb5c7920c8c3fa880672adb6
blocks=5 deterministic=true collides_public_packed=false intact_identity=true met_target=true
counts={near:2,repaired:2,far:2,far_refused:2}
identical to pre/s321-fresh-source2-at-base.json except revision: YES (field-by-field)

upx --best double-pack of /usr/bin/printf: both 95f2beb30d459f3080a542d29430e91f8b55664efb5c7920c8c3fa880672adb6, cmp BYTE-IDENTICAL
public carriers packed (upx --best): jq e8b6c9e7…, xxd 1727faf9…, libz a9c544e6…, dinit b67ce1bd…, xz a7b4d929… — none equals 95f2bebe…

python3 -I -B clone/tools/round-96/fresh-source2-check.py --root clone --work $S/fs2-head --rev 3baac2ef4b9b2830d299125b8184ca06d9e6584d --source /usr/bin/head --source-sha 313bf1f0c296d63fa9534394e22a502cfe29d9fe9e110c5b45f3c070b9ddf3e1 --json-out fs2-head-repro.json
exit=0  "fresh-source2 repaired 2 of 2; far-refused 2 of 2; intact 1 of 1 met True exit 0"
packed_sha256=b93ac38db8b61a8739adf596268e44b6b36c8e0ffdaaa7d6df0902beef4e9cc0 (supplementary diversity evidence)
```
