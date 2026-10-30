# ExecCarrierProbe — R52 W1

Four exact vendor URLs returned HTTP 200 to `curl -sSI --max-time 30`; metadata is recorded in `ExecCarrierProbe/head-receipt.txt`. HEAD command exits were 0 for all. No image bytes were downloaded. The receipt records available HTTP metadata; stdout hashes and exact UTC clock times were not captured by the initial command, so are explicitly absent rather than invented.

## Fetch chain
`fetch-vendor.py` validates HTTPS and `download.avm.de`, reads the bounded image (MAX_IMAGE=64 MiB), checks image SHA-256 against `external.image_sha256`, opens the image as tar, extracts the named raw member, checks the complete member SHA-256 against `external.member_sha256` before carving, and then either takes configured `length` or opens member SquashFS, extracts the nested path, checks the whole nested-file SHA-256, and truncates to that nested SquashFS's own `bytes_used`. Finally it checks the resulting carrier bytes against the top-level carrier `sha256`, then atomically writes cache output. It imports `tools/round-41/sqfs-list.py`; SquashFS probing/extraction is Python implementation, with no `unsquashfs` executable invocation visible in this procedure.

## Host prerequisites and disk
`python3`, `curl`, `unsquashfs`, and `mksquashfs` are present (`command -v`). Disk guard status: /fast/scratch/hyaku 46% used, 435.2G free; /tmp 24% used, 97.5G free; /var/tmp 41% used, 533.8G free. Guard command exceeded 60s after emitting this status (no successful completion status). Four images total 139,919,360 bytes (133.4 MiB). Member/carrier payloads are tens of MiB per carrier; extraction workspace upper rough estimate if retaining images plus all members/carriers is under ~300 MiB, excluding any unusually expansive temporary implementation behavior. Available scratch is ample.

## Checks
No downloads, builds, tests, or REA run. No tool installs. `head-receipt.sha256` hashes the saved metadata receipt, not the command stdout.
