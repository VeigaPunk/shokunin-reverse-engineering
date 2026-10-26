## Queue-drain craft

Development fragment for round-40 C2 recon (NOT the frozen SKILL block 19). It is a
`SKILL.md`-shaped section so `sqfs-triage-v2-dev.py --skill` parses it exactly as it will
parse the lane file: marker, actions declaration, then the first markdown table.

Every row below is written against measured round-39/round-40 development envelopes. The
`partial-body-failure` row is the one this wave's recon added: `extractor-failure` gap with
`published files > 0`. It must sit **before** `body-extractor-failure`, which keeps `files = 0`;
`avm-marker-be-dropped` must sit before both because it is the `-be no` specialisation of a
`files = 0` body failure on a big-endian handler.

`mixed-symlinks` is an L1 row shape (mixed escaping + in-tree links: `MaliciousSymlinkRemoved`
present **and** an `unpublished-entry` gap); it is listed for ordering but is not scored in this
seat's dev set — no mixed carrier was built here (sibling seat owns that class).

<!-- sqfs-triage-table v2 -->
<!-- sqfs-triage-actions: none accept-clean reject-image install-extractor use-avm-layout salvage-partial escalate review-symlinks drop-symlink -->

| label | operation | provider | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | action | cause | source |
|---|---|---|---|---|---|---|---|---|---|---|---|
| no-squashfs-chunk | extract_firmware | unblob | none | none | none | n/a | no | * | reject-image | no squashfs_v4_* chunk in the envelope, so the image is not a SquashFS v4 body (s_bad major/minor or another container) | sqfs-triage-v2 dev table; round-39 recon (unblob emits no chunk for an unrecognised image) |
| dep-missing-be | extract_firmware | unblob | squashfs_v4_be | missing-extractor-dependency | sasquatch-v4be | n/a | no | 0 | install-extractor | the BE handler's extractor is absent from the child PATH; no argv was built and no tree was written | round-39 R39C2ReconDep §3 (stripped PATH: deps exactly `sasquatch-v4be`, BE `n/a`) |
| dep-missing-le | extract_firmware | unblob | squashfs_v4_le | missing-extractor-dependency | sasquatch | n/a | no | 0 | install-extractor | the LE handler's extractor is absent from the child PATH; no argv was built and no tree was written | round-39 R39C2ReconDep §3 (stripped PATH: deps exactly `sasquatch`) |
| avm-marker-be-dropped | extract_firmware | unblob | squashfs_v4_be | extractor-failure | none | no | no | 0 | use-avm-layout | the AVM marker (mkfs_time == bytes_used) made unblob drop `-be`, so sasquatch-v4be ran the AVM layout path against a standard-BE body and died at the id table | round-39 R39C2ReconDep §2 (`-be no`, P=0); unblob handlers/filesystem/squashfs.py:44-50 |
| body-extractor-failure | extract_firmware | unblob | squashfs_v4_* | extractor-failure | none | * | no | 0 | escalate | the extractor ran and failed before writing any regular file (id-table damage, bad minor version) | round-39 heldout-gen.py body-extractor-failure + version-minor-mismatch; round-40 recon: zero-id-table 5/5 and bad-minor 1/1 give P=0 |
| mixed-symlinks | extract_firmware | unblob | squashfs_v4_* | unpublished-entry | none | * | yes | * | review-symlinks | the image holds both an escaping link (removed, reported) and an in-tree link (kept, reported as an unpublished entry), so one symlink report is not the whole story | R39-CL2 routed defect; L1 row shape (not scored in this seat's dev set) |
| escaping-symlink-removed | extract_firmware | unblob | squashfs_v4_* | none | none | * | yes | * | drop-symlink | unblob removed a link whose target leaves the extraction root; no gap is recorded for it | round-39 R39C2ReconDep §2 (K1: SR=yes, G empty, P=3) |
| in-tree-symlink-metadata | extract_firmware | unblob | squashfs_v4_* | unpublished-entry | none | * | no | * | review-symlinks | the image holds a link that resolves inside the root; unblob keeps it as metadata and REA reports one unpublished-entry gap | round-39 R39C2ReconDep §2 (K2: G={unpublished-entry}, P=3) |
| clean | extract_firmware | unblob | squashfs_v4_* | none | none | n/a | no | * | accept-clean | the handler ran, the extractor exited 0, no gap and no symlink report (a zero-file tree is still clean) | round-39 R39C2ReconDep §2 + round-40 clean controls (P=5, coverage complete) |
