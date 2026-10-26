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
| catch-all | * | * | * | * | * | * | * | * | accept-clean | everything | control |
